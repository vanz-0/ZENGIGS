# Directive 02: Cold Outreach Automation System

## Goal
Automate personalized cold email outreach using SMTP, pulling leads from the Supabase `leads` table, and logging interactions back to the database. Target: 10 highly personalized emails/day → 300/month.

## Architecture
- **Layer 1 (Directive)**: This document.
- **Layer 2 (Orchestration)**: System logic reading inputs and calling execution tools.
- **Layer 3 (Execution)**: `execution/cold_email_sender.py`

## Inputs
- **Template Name**: Which template variant to use (`cold_intro`, `follow_up`, `value_bomb`).
- **Daily Cap**: Number of emails to send per batch (default: 10, max: 20).
- **Target Niche**: Optional filter to only target leads from a specific niche.

## Process Flow

1. **Lead Retrieval**
   - The script queries the Supabase `leads` table for rows where `status = 'new'` (or `status = 'sent'` for follow-ups).
   - Filters out any leads missing a `first_name` or `company`.

2. **Personalization Engine**
   - Injects lead variables (`first_name`, `company`, `niche`) into the selected template.
   - If a specific pain point is required, it dynamically selects it based on the niche.

3. **SMTP Dispatch & Rate Limiting**
   - Connects to SMTP (Zoho/Google) using credentials in `.env`.
   - **Rate Limit**: Enforces a strict random delay between 45 to 90 seconds between sends.
   - **Safety Cap**: Halts immediately if the daily cap is reached.

4. **Telemetry & Synchronization**
   - On success: Updates `leads.status = 'contacted'` in Supabase.
   - Inserts a record into `outreach_logs` with the template used.
   - Updates `kpi_logs` for the current date, incrementing `emails_sent`.

## Email Templates
*Stored in `execution/cold_email_sender.py` or a dedicated templates directory.*
- **cold_intro**: Focuses on saving 20+ hours a week via AI/automation.
- **follow_up**: Short bump asking if they saw the previous email.
- **value_bomb**: Offers a free resource tailored to their niche.

## Error Handling & Rate Limiting
- **SMTP Connection Refused / Timeout**:
  - Implements exponential backoff (retry after 30s, 60s, 120s).
  - Fails gracefully after 3 attempts and leaves the lead `status = 'new'`.
- **Bounced Emails**:
  - If a hard bounce is detected via SMTP, the script updates `leads.status = 'bounced'`.
  - Does NOT retry bounced emails under any circumstances.
- **Spam Flags**:
  - If SMTP server returns a spam/block error, the script immediately pauses the entire campaign and alerts the admin.

## Cost Analysis
- **Zoho SMTP**: $1/month (Supports up to 500 emails/day).
- **System Cost per Email**: $0.00
- **ROI**: Based on a 2% conversion rate on 300 emails/mo = 6 meetings/mo.

## Learnable Patterns
- **Time of Day**: Sending between 9-11 AM recipient local time yields the best open rates. The orchestrator should schedule runs for this window.
- **Subject Lines**: Keep them under 5 words. "Quick question about {company}" works better than "Proposal for {company}".
- **Follow-up Timing**: Day 1 (Intro) -> Day 4 (Follow-up) -> Day 9 (Value Bomb).

## Outputs
- **Primary**: Supabase `outreach_logs` and `leads` tables updated.
- **Secondary**: Booked discovery calls.
