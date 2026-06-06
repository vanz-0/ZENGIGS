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
    # VERSION 1: Curiosity / Second Brain
    "intro_v1": {
        "subject": "{first_name} AI - are you using yours?",
        "body": "Hi {first_name}, are you currently using AI OS (the world's current #1 top trending and revolutionized Agentic Operating Systems)?\n\n{sender_name}\n\nSent from my iPhone"
    },
    "explanation_v1": {
        "subject": "Re: {first_name} AI - are you using yours?",
        "body": "Hi {first_name},\n\nThanks for sharing that — it actually helps a lot.\n\nBased on what you do, I can build you a 24/7 AI that handles your workflow the way YOU would handle it. It learns your tone, your rules, your standards. Runs while you sleep. Doesn't need managing.\n\nZero coding on your end. Zero disruption to what's already working.\n\nIt's basically a second brain that reports to you like a loyal employee — except it's always on, always consistent, and never makes excuses.\n\nWould you want to explore setting this up specifically for your business?\n\n{sender_name}"
    },
    "proposal_v1": {
        "subject": "Re: {first_name} AI - are you using yours?",
        "body": "Hi {first_name},\n\nPerfect. I've already got a rough blueprint in my head based on what you shared.\n\nI'm free anytime between 4 PM and 9 PM US time on Thursday and Friday. Just reply with what works for you and we'll map it out. No prep needed on your end.\n\n{sender_name}"
    },

    # VERSION 2: FOMO / Competitors
    "intro_v2": {
        "subject": "Your competitors just got an AI employee",
        "body": "Hi {first_name}, quick question — have you started using AI OS (the world's current #1 top trending and revolutionized Agentic Operating Systems) yet?\n\n{sender_name}\n\nSent from my iPhone"
    },
    "explanation_v2": {
        "subject": "Re: Your competitors just got an AI employee",
        "body": "Hi {first_name},\n\nReally appreciate you sharing the context.\n\nHere's the honest picture: the businesses pulling ahead in your space right now are running lean AI systems that handle repetitive, time-consuming work in the background 24/7 — on autopilot, according to their exact instructions.\n\nI can set that up for you. Custom to your business. No coding. No interference with how you currently work.\n\nOne question: would you be open to building your own personalized AI if it meant getting back 10+ hours a week?\n\n{sender_name}"
    },
    "proposal_v2": {
        "subject": "Re: Your competitors just got an AI employee",
        "body": "Hi {first_name},\n\nGlad to hear you're ready to take the lead.\n\nI have a custom outline ready that shows exactly how we'd set up your AI advantage. Let's get on a quick call — I'm free anytime between 4 PM and 9 PM US time on Thursday and Friday. Which works for you?\n\n{sender_name}"
    },

    # VERSION 3: Problem Fixing / Money on the Table
    "intro_v3": {
        "subject": "{first_name}, you're leaving money on the table",
        "body": "Hi {first_name}, wondering if you are using AI OS (the world's current #1 top trending and revolutionized Agentic Operating Systems) in your workflow?\n\n{sender_name}\n\nSent from my iPhone"
    },
    "explanation_v3": {
        "subject": "Re: {first_name}, you're leaving money on the table",
        "body": "Hi {first_name},\n\nThanks for the context.\n\nBased on what you shared, I can build you a 24/7 AI that handles your specific workflow exactly how you'd handle it yourself — your tone, your rules, your standards. Runs while you sleep. Zero coding on your end.\n\nDo you want to work on setting this up to plug those leaks and get your time back?\n\n{sender_name}"
    },
    "proposal_v3": {
        "subject": "Re: {first_name}, you're leaving money on the table",
        "body": "Hi {first_name},\n\nGreat. I've mapped out a quick proposal based on what you shared — exactly what your AI would handle and what you'd see in week one.\n\nLet's hop on a 15-minute call this week. I'm free anytime between 4 PM and 9 PM US time on Tuesday and Wednesday. What works?\n\n{sender_name}"
    },

    # VERSION 4: Urgency / Market Shift
    "intro_v4": {
        "subject": "Act fast: AI is reshaping your market",
        "body": "Hi {first_name}, are you currently using AI OS (the world's current #1 top trending and revolutionized Agentic Operating Systems) for your business?\n\n{sender_name}\n\nSent from my iPhone"
    },
    "explanation_v4": {
        "subject": "Re: Act fast: AI is reshaping your market",
        "body": "Hi {first_name},\n\nThanks for the details.\n\nTo get you ahead of this, I can build a 24/7 AI that integrates directly into your current workflow. It learns your process daily, stays completely secure, and requires zero coding from you.\n\nWould you be open to building your own personalized AI before your market shifts further?\n\n{sender_name}"
    },
    "proposal_v4": {
        "subject": "Re: Act fast: AI is reshaping your market",
        "body": "Hi {first_name},\n\nExcellent. I put together a quick outline of exactly how your AI setup would work.\n\nI'm free anytime between 4 PM and 9 PM US time on Wednesday and Thursday — happy to walk you through it. Which works?\n\n{sender_name}"
    },

    # VERSION 5: Free Test / Low Risk
    "intro_v5": {
        "subject": "your Free AI OS setup !!!",
        "body": "Hi {first_name}, just wanted to ask if you are using AI OS (the world's current #1 top trending and revolutionized Agentic Operating Systems) right now?\n\n{sender_name}\n\nSent from my iPhone"
    },
    "explanation_v5": {
        "subject": "Re: your Free AI OS setup !!!",
        "body": "Appreciate the quick reply {first_name}.\n\nI'm actually doing a free AI test for a few businesses right now. It's a 24/7 AI that just runs quietly in the background, learns your exact process, and only does what you tell it to.\n\nZero code. Zero disruption to your current tools. Just a risk-free test.\n\nBefore we get into it, what industry are you in? And are you using an AI OS right now?\n\n{sender_name}"
    },
    "proposal_v5": {
        "subject": "Re: your Free AI OS setup !!!",
        "body": "Awesome {first_name}.\n\nI have an exciting proposal ready that details how we can seamlessly implement this solution for you, ensuring your workflow remains uninterrupted.\n\nI’d love to discuss this further during a quick call. I'm available between 4 PM and 9 PM US time on Monday and Tuesday. What time suits you best?\n\n{sender_name}"
    }
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
        
        if not first_name:
            first_name = "there"

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
    msg["From"] = f"{smtp_config.sender_name} <{smtp_config.sender_email}>"
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
