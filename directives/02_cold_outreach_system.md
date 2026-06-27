# Directive 02: Cold Outreach Automation System

## Goal
Automate cold email outreach targeting ONLY Gmail addresses from `.tmp/gmail_leads.csv` using SMTP. The process is scheduled to run daily via a batch job to protect the domain and sender reputation.

> [!IMPORTANT]
> **CRITICAL RULE**: Do not query the general database/Supabase leads for initial outreach unless explicitly requested. All daily initial outreach MUST go to Gmail leads from `.tmp/gmail_leads.csv` using the batch sender script.

## Architecture
- **Layer 1 (Directive)**: This document.
- **Layer 2 (Orchestration)**: Daily cron execution via `run_batch.bat`.
- **Layer 3 (Execution)**: `execution/send_batch.py` (which leverages SMTP utilities from `cold_email_sender.py`).

## Inputs
- **Lead List**: `.tmp/gmail_leads.csv` (contains names and gmail addresses).
- **Template Name**: `master_v4` (standard high-converting copy).
- **Daily Cap / Batch Size**: 30 emails per batch.


## Process Flow

1. **Lead Retrieval**
   - The script `execution/send_batch.py` reads up to 30 leads from `.tmp/gmail_leads.csv`.
   - The processed batch is sliced out, and the remaining leads are rewritten back to `.tmp/gmail_leads.csv`.

2. **Personalization Engine & Rate Limiting**
   - Extracts the first name from the lead name.
   - Pre-calculates random send times within a 2-hour window (7200 seconds) to guarantee natural email distribution.
   - Wait/sleep intervals are enforced dynamically to space out emails.

3. **Telemetry & Synchronization**
   - Successfully sent emails are recorded in `.tmp/sent_emails.csv`.

## Email Templates
- **master_v4**: Configured template in `execution/send_batch.py` that focuses on the AI/Automation shift in 2026 and offers a free 7-day custom AI asset implementation.

## Error Handling & Rate Limiting
- **Reputation Protection**: Random delays spanning 2 hours prevent rate limits and spam triggers on Gmail SMTP servers.
- **Failures**: Any SMTP connection or credentials failure aborts the batch safely.

## Outputs
- **Primary**: Updated `.tmp/gmail_leads.csv` and logged sends in `.tmp/sent_emails.csv`.
- **Secondary**: Daily outreach telemetry.

