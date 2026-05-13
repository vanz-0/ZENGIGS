#!/usr/bin/env python3
"""
Automated cold email sender with SMTP, personalization, Supabase sync, and rate limiting.

Usage:
    python execution/cold_email_sender.py
    python execution/cold_email_sender.py --template follow_up --daily_cap 15
    python execution/cold_email_sender.py --dry_run
"""

import os
import sys
import time
import random
import smtplib
import logging
import argparse
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from supabase import create_client, Client
except ImportError:
    logger.error("supabase not installed. Run: pip install supabase")
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

@dataclass
class SMTPConfig:
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
            raise ValueError("Missing SMTP credentials in .env")

        return cls(host=host, port=port, email=email, password=password, sender_name=sender_name)

# ─── Supabase Client ──────────────────────────────────────────────────────────

def get_supabase_client() -> Optional[Client]:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        return None
    return create_client(url, key)

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

def fetch_leads(supabase: Client, template: str, daily_cap: int) -> List[Dict]:
    """Fetch leads from Supabase based on template strategy."""
    try:
        if template == "cold_intro":
            # Fetch 'new' leads
            res = supabase.table("leads").select("*").eq("status", "new").limit(daily_cap).execute()
        else:
            # Fetch 'contacted' leads for follow-ups
            res = supabase.table("leads").select("*").eq("status", "contacted").limit(daily_cap).execute()
        
        return res.data
    except Exception as e:
        logger.error(f"Failed to fetch leads from Supabase: {e}")
        return []

def personalize_email(template_name: str, lead: Dict, sender_name: str) -> Optional[Dict[str, str]]:
    template = TEMPLATES.get(template_name)
    if not template:
        return None

    first_name = lead.get("first_name") or "there"
    company = lead.get("company") or "your company"

    placeholders = {
        "first_name": first_name.capitalize(),
        "company": company,
        "sender_name": sender_name,
    }

    return {
        "subject": template["subject"].format(**placeholders),
        "body": template["body"].format(**placeholders),
    }

def send_email(smtp_config: SMTPConfig, to_email: str, subject: str, body: str) -> bool:
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
            return False
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP Authentication Error. Check .env credentials.")
            return False
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"SMTP error after {max_retries} attempts: {e}")
                return False
            wait_time = 30 * (attempt + 1)
            logger.warning(f"SMTP error: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
    return False

def update_supabase_logs(supabase: Client, lead: Dict, template: str, success: bool, error_msg: str = ""):
    """Update lead status and outreach logs in Supabase."""
    new_status = "contacted" if success else ("bounced" if "refused" in error_msg.lower() else "failed")
    
    try:
        # Update lead status
        supabase.table("leads").update({"status": new_status}).eq("id", lead["id"]).execute()
        
        # Insert outreach log
        supabase.table("outreach_logs").insert({
            "lead_id": lead["id"],
            "email": lead["email"],
            "template_used": template,
            "status": "sent" if success else "failed",
            "error_message": error_msg if not success else None
        }).execute()
        
    except Exception as e:
        logger.error(f"Failed to log outreach to Supabase: {e}")

def update_kpi_tracker(supabase: Client, sent_count: int):
    if sent_count == 0: return
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Check if row exists
        res = supabase.table("kpi_logs").select("emails_sent").eq("log_date", today).execute()
        if res.data:
            new_total = res.data[0]["emails_sent"] + sent_count
            supabase.table("kpi_logs").update({"emails_sent": new_total}).eq("log_date", today).execute()
        else:
            supabase.table("kpi_logs").insert({"log_date": today, "emails_sent": sent_count}).execute()
    except Exception as e:
        logger.error(f"Failed to update KPIs: {e}")

# ─── Main Pipeline ────────────────────────────────────────────────────────────

def send_cold_emails(template: str = "cold_intro", daily_cap: int = 10, dry_run: bool = False):
    supabase = get_supabase_client()
    if not supabase:
        logger.error("Could not connect to Supabase. Check .env.")
        sys.exit(1)

    if not dry_run:
        try:
            smtp_config = SMTPConfig.from_env()
        except ValueError as e:
            logger.error(str(e))
            sys.exit(1)
    else:
        smtp_config = None
        logger.info("🏜️  DRY RUN mode — no emails will actually be sent.")

    leads = fetch_leads(supabase, template, daily_cap)
    if not leads:
        logger.info(f"No leads found for template '{template}'.")
        return

    logger.info(f"Processing {len(leads)} leads (daily cap: {daily_cap}, template: {template})")

    sent = 0
    failed = 0

    for i, lead in enumerate(leads):
        email_data = personalize_email(template, lead, smtp_config.sender_name if smtp_config else "ZENGIGS")
        if not email_data:
            failed += 1
            continue

        if dry_run:
            logger.info(f"  [{i+1}/{len(leads)}] Would send to {lead['email']}: \"{email_data['subject']}\"")
            sent += 1
        else:
            success = send_email(smtp_config, lead["email"], email_data["subject"], email_data["body"])
            
            error_msg = "" if success else "SMTP Send Failed"
            update_supabase_logs(supabase, lead, template, success, error_msg)

            if success:
                sent += 1
                logger.info(f"  ✅ [{i+1}/{len(leads)}] Sent to {lead['email']}")
            else:
                failed += 1
                logger.warning(f"  ❌ [{i+1}/{len(leads)}] Failed: {lead['email']}")

        # Rate limiting: strictly 45-90 seconds between sends
        if i < len(leads) - 1 and not dry_run:
            delay = random.randint(45, 90)
            logger.info(f"  ⏳ Rate Limit: Waiting {delay}s before next send...")
            time.sleep(delay)

    if not dry_run:
        update_kpi_tracker(supabase, sent)

    logger.info(f"--- Campaign Summary ---")
    logger.info(f"Sent   : {sent}")
    logger.info(f"Failed : {failed}")

def main():
    parser = argparse.ArgumentParser(description="Send personalized cold emails via Supabase leads")
    parser.add_argument("--template", default="cold_intro", choices=list(TEMPLATES.keys()), help="Email template")
    parser.add_argument("--daily_cap", type=int, default=10, help="Max emails per run")
    parser.add_argument("--dry_run", action="store_true", help="Preview without sending")

    args = parser.parse_args()
    send_cold_emails(args.template, args.daily_cap, args.dry_run)

if __name__ == "__main__":
    main()
