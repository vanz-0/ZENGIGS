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
    sender_email: str

    @classmethod
    def from_env(cls) -> 'SMTPConfig':
        host = os.getenv("SMTP_HOST")
        port = int(os.getenv("SMTP_PORT", "587"))
        email = os.getenv("SMTP_EMAIL")
        password = os.getenv("SMTP_PASSWORD")
        sender_name = os.getenv("SENDER_NAME", "ZENGIGS")
        sender_email = os.getenv("SENDER_EMAIL") or email

        if not all([host, email, password]):
            raise ValueError("Missing SMTP credentials in .env")

        return cls(host=host, port=port, email=email, password=password, sender_name=sender_name, sender_email=sender_email)

# ─── Supabase Client ──────────────────────────────────────────────────────────

def get_supabase_client() -> Optional[Client]:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        return None
    return create_client(url, key)

# ─── Email Templates ─────────────────────────────────────────────────────────

TEMPLATES = {
    # MASTER TEMPLATES (Combined)
    "master_v1": {
        "subject": "you're leaving money on the table, {first_name}",
        "body": "Hi {first_name},\n\n{personalization}Let's be direct. If you aren't building your own AI operating system or running an AI-driven company in 2026, you are leaving massive amounts of money on the table.\n\nThe market has completely shifted. Traditional models are being swallowed by businesses that have automated their core workflows. Your competitors are already transitioning.\n\nI build custom AI systems and autonomous agents that run 24/7. No coding required on your end. I can build you an AI setup that immediately reclaims your time and scales your output.\n\nI want to prove it. Let me build a custom AI asset for you over the next 7 days, 100% free. If it doesn't dramatically improve your workflow, you don't pay a cent.\n\nWorth 15 minutes to see how it works? Let me know and we'll hop on a quick call.\n\nBest,\n{sender_name}"
    },
    "master_v2": {
        "subject": "quick question about 2026, {first_name}",
        "body": "Hi {first_name},\n\n{personalization}It's 2026. If you don't have your own AI company or an AI operating system doing the heavy lifting, you're falling behind fast.\n\nI build autonomous AI systems for founders who want to scale without adding headcount. We are talking about custom AI agents that learn your rules and run your operations 24/7.\n\nYou're doing too much manual work that an AI OS could handle in seconds. I'm so confident I can fix this that I'm willing to build you a custom AI asset for free.\n\nIf it doesn't save you 10+ hours a week immediately, keep it at no cost. No strings attached.\n\nAre you open to a brief 15-minute call this week to see a live demo?\n\nCheers,\n{sender_name}"
    },
    "master_v3": {
        "subject": "the AI shift is happening, {first_name}",
        "body": "Hi {first_name},\n\n{personalization}I'll keep this brief. We're well into 2026, and if you aren't integrating an AI OS or launching your own AI-driven solutions, you are actively losing ground to those who are.\n\nThe window to capitalize on this is closing. I help businesses transition by building them custom, autonomous AI systems that handle their repetitive workflows 24/7.\n\nI don't expect you to take my word for it. I want to build a risk-free AI asset specifically for your use case over the next few days. If you don't see immediate ROI and time saved, you pay nothing.\n\nLet's stop leaving money on the table. Are you opposed to a 15-minute chat to explore this?\n\nThanks,\n{sender_name}"
    },
    "master_v4": {
        "subject": "you're leaving money on the table, {first_name}",
        "body": "Hi {first_name},\n\n{personalization}By now, the reality of 2026 is clear: if you aren't operating an AI company or running your business on an AI OS, you are moving too slow.\n\nEvery day you delay, you leave money on the table while competitors automate their growth. I specialize in building custom AI systems that take over the heavy lifting so you can focus on scaling.\n\nI'm ready to prove my value upfront. Let me build a fully customized AI workflow for you in the next 7 days, completely free of charge. If it doesn't radically improve your efficiency, we part ways.\n\nDo you have 15 minutes this week to see what this looks like?\n\nBest,\n{sender_name}"
    },
    "master_v5": {
        "subject": "falling behind in 2026, {first_name}",
        "body": "Hi {first_name},\n\n{personalization}The market is ruthless right now. If you aren't actively building an AI company or leveraging an AI OS, you are leaving serious revenue behind.\n\nYou don't need to learn how to code to catch up. I build bespoke 24/7 AI systems that plug right into your existing operations and run on autopilot.\n\nI'd love to set up a free 14-day implementation trial. I will build you a high-converting AI asset from scratch. If it doesn't immediately boost your metrics, you don't owe me a dime.\n\nLet's plug the leak in your workflow. Let me know if you're open to a casual 15-minute video call to discuss.\n\nRespectfully,\n{sender_name}"
    },
    # ─── Lead Find / One One / Down ────────────────────────────────────────────
    "down": {
        "subject": "quick note, {first_name}",
        "body": "Hi {first_name},\n\n{personalization}I run ZENGIGS - we build the latest AI systems for businesses that are ready to scale.\n\nI'd love to show you what we've put together for companies like {company}. No pitch deck. Just a quick 15-minute call and I'll show you exactly what we'd build for you.\n\nWorth it?\n\nRegards,\nMax"
    },

    # ─── Follow-Up (Replied Leads Only) ─────────────────────────────────────────
    "follow_up_c": {
        "subject": "your competitors already did this, {first_name}",
        "body": "Hey {first_name},\n\nSent you a note last week about building a free AI asset for {company} — wanted to check if it landed or slipped through.\n\nIf the timing's off, no worries at all. If you're even slightly curious, I'm happy to show you what's possible in 15 minutes.\n\nMax"
    }
}

# ─── Core Functions ───────────────────────────────────────────────────────────

def fetch_leads(supabase: Client, template: str, daily_cap: int, campaign_id: str = None) -> List[Dict]:
    """Fetch leads from Supabase, optionally filtered by campaign_id.
    
    Status routing:
      - new          → initial outreach templates (master_*, down, cold_intro)
      - replied      → follow-up templates (follow_up_*) — ONLY sent to leads who replied
      - contacted    → legacy follow-up fallback
    """
    try:
        # Follow-up templates: ONLY target leads who have actually replied
        if template.startswith("follow_up_"):
            q = supabase.table("leads").select("*").eq("status", "replied")
            if campaign_id:
                q = q.eq("campaign_id", campaign_id)
            res = q.limit(daily_cap).execute()

        # Initial outreach templates: target fresh leads
        elif template == "cold_intro" or template.startswith("master_") or template == "down":
            q = supabase.table("leads").select("*").eq("status", "new").filter("personalization_line", "not.is", "null")
            if campaign_id:
                q = q.eq("campaign_id", campaign_id)
            res = q.limit(daily_cap).execute()

        # Fallback: contacted leads for any other template
        else:
            q = supabase.table("leads").select("*").eq("status", "contacted").filter("personalization_line", "not.is", "null")
            if campaign_id:
                q = q.eq("campaign_id", campaign_id)
            res = q.limit(daily_cap).execute()

        return res.data
    except Exception as e:
        logger.error(f"Failed to fetch leads from Supabase: {e}")
        return []

def personalize_email(template_name: str, lead: Dict, sender_name: str) -> Optional[Dict[str, str]]:
    template = TEMPLATES.get(template_name)
    if not template:
        return None

    first_name = lead.get("first_name")
    if not first_name or first_name.lower() == "there":
        # Fallback: Generate from email
        email_str = lead.get("email", "")
        if "@" in email_str:
            prefix = email_str.split("@")[0]
            # Try to get something name-like
            clean_prefix = ''.join(c for c in prefix if c.isalpha() or c == '.')
            if '.' in clean_prefix:
                first_name = clean_prefix.split('.')[0]
            else:
                first_name = clean_prefix
                
            # Filter out generic business prefixes
            generic_prefixes = {"info", "contact", "support", "hello", "admin", "sales", "team", "office"}
            if first_name.lower() in generic_prefixes:
                first_name = "there"
        
        if not first_name:
            first_name = "there"

    company = lead.get("company") or "your company"
    personalization = lead.get("personalization_line")

    placeholders = {
        "first_name": first_name.capitalize(),
        "company": company,
        "sender_name": sender_name,
        "personalization": f"{personalization}\n\n" if personalization else ""
    }

    return {
        "subject": template["subject"].format(**placeholders),
        "body": template["body"].format(**placeholders),
    }

def send_email(smtp_config: SMTPConfig, to_email: str, subject: str, body: str) -> bool:
    msg = MIMEMultipart()
    msg["From"] = f"{smtp_config.sender_name} <{smtp_config.sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    max_retries = 2  # Max 2 retries (30s + 60s = 90s ceiling — never blocks the queue for hours)
    for attempt in range(max_retries + 1):
        try:
            with smtplib.SMTP(smtp_config.host, smtp_config.port, timeout=20) as server:
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
            if attempt == max_retries:
                logger.error(f"SMTP failed after {max_retries + 1} attempts, skipping: {e}")
                return False
            wait_time = 30 * (2 ** attempt)  # 30s, then 60s
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

def send_cold_emails(template: str = "cold_intro", daily_cap: int = 10, dry_run: bool = False, campaign_id: str = None):
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

    leads = fetch_leads(supabase, template, daily_cap, campaign_id=campaign_id)
    if not leads:
        label = f"campaign '{campaign_id}'" if campaign_id else f"template '{template}'"
        logger.info(f"No leads found for {label}.")
        return

    logger.info(f"Processing {len(leads)} leads (cap: {daily_cap}, template: {template}, campaign: {campaign_id or 'all'})")

    sent = 0
    failed = 0

    for i, lead in enumerate(leads):
        email_data = personalize_email(template, lead, smtp_config.sender_name if smtp_config else "ZENGIGS")
        if not email_data:
            failed += 1
            continue

        if dry_run:
            divider = "-" * 60
            print(f"\n{divider}")
            print(f"TO:      {lead['email']}")
            print(f"SUBJECT: {email_data['subject']}")
            print(f"BODY:\n{email_data['body']}")
            print(divider)
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
    parser.add_argument("--campaign", default=None, help="Filter by campaign_id (e.g. 'one_one')")

    args = parser.parse_args()
    send_cold_emails(args.template, args.daily_cap, args.dry_run, campaign_id=args.campaign)

if __name__ == "__main__":
    main()
