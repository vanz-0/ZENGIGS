#!/usr/bin/env python3
"""
Automated cold email sender with SMTP, personalization, and rate limiting.

Usage:
    python execution/cold_email_sender.py
    python execution/cold_email_sender.py --template follow_up --daily_cap 15
    python execution/cold_email_sender.py --dry_run
"""

import os
import sys
import csv
import json
import time
import random
import smtplib
import logging
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ─── Configuration ────────────────────────────────────────────────────────────

@dataclass
class SMTPConfig:
    """SMTP server configuration loaded from environment."""
    host: str
    port: int
    email: str
    password: str
    sender_name: str

    @classmethod
    def from_env(cls) -> 'SMTPConfig':
        host = os.getenv("SMTP_HOST")
        port = int(os.getenv("SMTP_PORT", "587"))
        email = os.getenv("SMTP_EMAIL")
        password = os.getenv("SMTP_PASSWORD")
        sender_name = os.getenv("SENDER_NAME", "ZENGIGS")

        if not all([host, email, password]):
            raise ValueError(
                "Missing SMTP credentials. Ensure SMTP_HOST, SMTP_EMAIL, and SMTP_PASSWORD are set in .env"
            )

        return cls(host=host, port=port, email=email, password=password, sender_name=sender_name)


# ─── Email Templates ─────────────────────────────────────────────────────────

TEMPLATES = {
    "cold_intro": {
        "subject": "Quick question about {company}",
        "body": """Hi {first_name},

I noticed {company} is growing fast — congrats on that.

I help founders like you save 20+ hours a week by handling the stuff that doesn't need to be you: inbox management, social media scheduling, AI workflow setup, and video editing.

Would a 15-minute call this week make sense to see if I can help?

Best,
{sender_name}
ZENGIGS | Tech-Powered Virtual Assistant"""
    },
    "follow_up": {
        "subject": "Re: Quick question about {company}",
        "body": """Hi {first_name},

Just bumping this up — I know inboxes get buried.

I recently helped a founder in your space automate their content pipeline, saving them 15 hours/week. Happy to share how.

Worth a quick chat?

{sender_name}"""
    },
    "value_bomb": {
        "subject": "Free resource for {company}",
        "body": """Hi {first_name},

I put together a quick checklist of the top 5 tasks founders should delegate first to save 10+ hours/week. Thought it might be useful for you.

No strings attached — just reply "send it" and I'll share the link.

Cheers,
{sender_name}
ZENGIGS"""
    },
}


# ─── Core Functions ───────────────────────────────────────────────────────────

def load_leads(filepath: str) -> List[Dict[str, str]]:
    """Load leads from a CSV file."""
    if not os.path.exists(filepath):
        logger.error(f"Leads file not found: {filepath}")
        return []

    leads = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip leads without required fields
            if not row.get("first_name") or not row.get("email"):
                logger.warning(f"Skipping lead with missing name/email: {row}")
                continue
            leads.append(row)

    logger.info(f"Loaded {len(leads)} leads from {filepath}")
    return leads


def personalize_email(template_name: str, lead: Dict[str, str], sender_name: str) -> Optional[Dict[str, str]]:
    """Generate a personalized email from a template and lead data."""
    template = TEMPLATES.get(template_name)
    if not template:
        logger.error(f"Unknown template: {template_name}. Available: {list(TEMPLATES.keys())}")
        return None

    placeholders = {
        "first_name": lead.get("first_name", "there"),
        "company": lead.get("company", "your company"),
        "sender_name": sender_name,
    }

    return {
        "subject": template["subject"].format(**placeholders),
        "body": template["body"].format(**placeholders),
    }


def send_email(smtp_config: SMTPConfig, to_email: str, subject: str, body: str) -> bool:
    """Send a single email via SMTP with retry logic."""
    msg = MIMEMultipart()
    msg["From"] = f"{smtp_config.sender_name} <{smtp_config.email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    max_retries = 3
    for attempt in range(max_retries):
        try:
            with smtplib.SMTP(smtp_config.host, smtp_config.port, timeout=30) as server:
                server.starttls()
                server.login(smtp_config.email, smtp_config.password)
                server.send_message(msg)
            return True

        except smtplib.SMTPRecipientsRefused:
            logger.warning(f"Recipient refused (bounced): {to_email}")
            return False  # Don't retry bounces

        except smtplib.SMTPException as e:
            if attempt == max_retries - 1:
                logger.error(f"SMTP error after {max_retries} attempts for {to_email}: {e}")
                return False
            wait_time = 2 ** attempt
            logger.warning(f"SMTP error (attempt {attempt + 1}): {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)

        except Exception as e:
            logger.error(f"Unexpected error sending to {to_email}: {e}")
            return False

    return False


def log_send(log_file: str, lead: Dict, template: str, success: bool) -> None:
    """Append a send record to the email log CSV."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_exists = os.path.exists(log_file)

    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "email", "first_name", "company", "template", "status"])
        writer.writerow([
            datetime.now().isoformat(),
            lead.get("email", ""),
            lead.get("first_name", ""),
            lead.get("company", ""),
            template,
            "sent" if success else "failed",
        ])


# ─── Main Pipeline ────────────────────────────────────────────────────────────

def send_cold_emails(
    leads_file: str = "execution/leads.csv",
    template: str = "cold_intro",
    daily_cap: int = 10,
    dry_run: bool = False,
) -> Dict:
    """
    Main outreach pipeline: load leads, personalize, send, log.

    Returns a summary dict with counts.
    """
    # Load config
    if not dry_run:
        try:
            smtp_config = SMTPConfig.from_env()
        except ValueError as e:
            logger.error(str(e))
            return {"success": False, "error": str(e)}
    else:
        smtp_config = None
        logger.info("🏜️  DRY RUN mode — no emails will actually be sent.")

    # Load leads
    leads = load_leads(leads_file)
    if not leads:
        return {"success": False, "error": f"No valid leads found in {leads_file}"}

    # Cap to daily limit
    batch = leads[:daily_cap]
    logger.info(f"Processing {len(batch)} leads (daily cap: {daily_cap}, template: {template})")

    log_file = ".tmp/email_log.csv"
    sent = 0
    failed = 0

    for i, lead in enumerate(batch):
        email_data = personalize_email(template, lead, smtp_config.sender_name if smtp_config else "ZENGIGS")
        if not email_data:
            failed += 1
            continue

        if dry_run:
            logger.info(f"  [{i+1}/{len(batch)}] Would send to {lead['email']}: \"{email_data['subject']}\"")
            sent += 1
        else:
            success = send_email(smtp_config, lead["email"], email_data["subject"], email_data["body"])
            log_send(log_file, lead, template, success)

            if success:
                sent += 1
                logger.info(f"  ✅ [{i+1}/{len(batch)}] Sent to {lead['email']}")
            else:
                failed += 1
                logger.warning(f"  ❌ [{i+1}/{len(batch)}] Failed: {lead['email']}")

        # Rate limiting: random delay between 45-90 seconds
        if i < len(batch) - 1 and not dry_run:
            delay = random.randint(45, 90)
            logger.info(f"  ⏳ Waiting {delay}s before next send...")
            time.sleep(delay)

    result = {
        "success": True,
        "sent": sent,
        "failed": failed,
        "total": len(batch),
        "template": template,
        "logFile": log_file,
    }
    print(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Send personalized cold emails")
    parser.add_argument("--leads", default="execution/leads.csv", help="Path to leads CSV")
    parser.add_argument("--template", default="cold_intro", choices=list(TEMPLATES.keys()), help="Email template")
    parser.add_argument("--daily_cap", type=int, default=10, help="Max emails per run (default: 10)")
    parser.add_argument("--dry_run", action="store_true", help="Preview without sending")

    args = parser.parse_args()
    send_cold_emails(args.leads, args.template, args.daily_cap, args.dry_run)


if __name__ == "__main__":
    main()
