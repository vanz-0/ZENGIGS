# Cold Email Campaign Standard Operating Procedure (SOP)

## Goal
Automate the daily process of verifying raw email lists, removing invalid/risky emails, and scheduling 100-200 outreach emails across multiple sender accounts targeting the US market.

## Inputs
*   Raw list of emails (placed in `.tmp/raw_emails.csv`).
*   Configured API keys for Verification Service (e.g., ZeroBounce) in `.env`.
*   Configured API keys for Outreach Tool (e.g., Instantly/Smartlead) in `.env`.

## Process

1.  **Verification Phase (`execution/verify_emails.py`)**
    *   **Trigger:** Daily at 02:00 AM (or via manual run).
    *   **Action:** Reads `.tmp/raw_emails.csv`. Iterates through emails and pings the Verification API.
    *   **Output:** Generates `.tmp/verified_emails.csv` containing only "valid" and "safe-to-send" addresses. Invalid/catch-all emails are discarded or logged separately.

2.  **Outreach Injection Phase (`execution/send_campaign.py`)**
    *   **Trigger:** Following the completion of the Verification Phase.
    *   **Action:** Reads `.tmp/verified_emails.csv`. Selects the daily batch (100-200 emails). Injects these leads into the active campaign in the Outreach Tool.
    *   **Limits:** The Outreach Tool is configured to use 4-8 sender accounts, capping each sender at 25-50 emails/day to mimic human sending patterns.
    *   **Scheduling:** Ensures sending is confined to US business hours (EST/PST).

3.  **Content & Offer**
    *   The campaign sequence should include an AI-personalized icebreaker.
    *   The core offer focuses on "Online Gigs, Virtual Events, and Global Digital Solutions" (excluding the local Kenyan market).

## Handling Errors
*   **Verification API Rate Limit/Errors:** If the API fails, the script will halt, alert via logs, and wait for human intervention or retry the next day to prevent sending unverified lists.
*   **Outreach Tool Errors:** If injection fails, the un-injected verified emails remain in `.tmp/verified_emails.csv` for the next run.
