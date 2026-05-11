# Cold Outreach System

## Goal
Scrape targeted leads, personalize cold emails using templates from the VA Blueprint, and automate SMTP-based outreach with rate limiting and tracking. Target: 10 personalized emails/day → 300/month.

## Inputs
- **Industry**: The target niche (e.g., "Coaches", "SaaS Founders", "E-commerce Brands").
- **Location**: Geographic target (e.g., "United States", "UK").
- **Total Count**: Number of leads desired per batch (default: 50).
- **Email Template**: Which template variant to use (cold_intro, follow_up, value_bomb).

## Tools/Scripts
- Script: `execution/scrape_leads.py` (Apify-based lead scraping)
- Script: `execution/cold_email_sender.py` (SMTP personalized sending)
- Script: `execution/kpi_tracker.py` (daily metric logging)
- Dependencies: `apify-client`, `python-dotenv`, `smtplib` (stdlib)

## Process

### Phase 1: Lead Generation

1. **Test Scrape**
   - Run `execution/scrape_leads.py` with `--max_items 25` and target query.
   - Output: `.tmp/test_leads.json`

2. **Verification**
   - Agent reads `.tmp/test_leads.json`.
   - Check if at least 20/25 (80%) leads match the target **Industry**.
   - **Decision**:
     - **Pass**: Proceed to step 3.
     - **Fail**: Stop. Refine **Industry** or **Location** keywords.

3. **Full Scrape**
   - Run `execution/scrape_leads.py` with full **Total Count**.
   - Output: `.tmp/leads_[timestamp].json`

4. **Normalize to CSV**
   - Run `execution/lead_scraper.py` to standardize the JSON into `leads.csv`.
   - Output: `execution/leads.csv` (the working lead file for the email sender).

### Phase 2: Email Outreach

5. **Configure Credentials**
   - Ensure `.env` has valid SMTP credentials (see `.env.example`).
   - Recommended: Zoho Mail ($1/mo) or Google Workspace.

6. **Send Cold Emails**
   - Run `execution/cold_email_sender.py`.
   - Script reads `execution/leads.csv`, personalizes each email, sends via SMTP.
   - **Rate limiting**: 45-90 second random delay between sends to avoid spam flags.
   - **Daily cap**: 10 emails/day (configurable in script).
   - Output: Sent emails logged to `.tmp/email_log.csv`.

7. **Log KPIs**
   - Run `execution/kpi_tracker.py --emails_sent <N> --responses <N> --meetings <N>`.
   - Output: Appends to `.tmp/kpi_tracking.csv`.

### Phase 3: Follow-Up Sequences

8. **Day 3 Follow-Up**
   - Re-run `cold_email_sender.py` with `--template follow_up` flag on leads that haven't replied.
   - Subject line: "Re: Quick question about [Company]"

9. **Day 7 Value Bomb**
   - Send a free resource or case study to remaining cold leads.
   - Template: `value_bomb` variant.

## Email Templates (from VA Blueprint)

### Template: cold_intro
```
Subject: Quick question about [Company]

Hi [First Name],

I noticed [Company] is growing fast — congrats on that.

I help founders like you save 20+ hours a week by handling the stuff that doesn't need to be you: inbox management, social media scheduling, AI workflow setup, and video editing.

Would a 15-minute call this week make sense to see if I can help?

Best,
[Your Name]
ZENGIGS | Tech-Powered Virtual Assistant
```

### Template: follow_up
```
Subject: Re: Quick question about [Company]

Hi [First Name],

Just bumping this up — I know inboxes get buried.

I recently helped a [similar industry] founder automate their content pipeline, saving them 15 hours/week. Happy to share how.

Worth a quick chat?

[Your Name]
```

## Outputs (Deliverables)
- **Primary**: Booked discovery calls from email responses.
- **Secondary**: `.tmp/kpi_tracking.csv` with daily metrics.
- **Intermediate** (not deliverables): `.tmp/leads_*.json`, `.tmp/email_log.csv`.

## Edge Cases
- **Bounced emails**: Log bounce and remove from leads.csv. Do not re-send.
- **Spam complaints**: Immediately stop campaign for that domain. Review templates.
- **SMTP rate limit hit**: Script auto-pauses and retries after cooldown.
- **Empty leads file**: Script exits gracefully with error message.

## Learnings
- Zoho SMTP has a 500 email/day limit on paid plans — more than enough for 10/day.
- Always personalize the company name — generic emails get 2% reply rate vs 8-12% personalized.
- Sending between 9-11 AM recipient local time yields best open rates.
- The `[First Name]` field is critical — skip the lead if name is missing.
