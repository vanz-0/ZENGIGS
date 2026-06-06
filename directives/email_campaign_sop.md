# Cold Email Campaign SOP: Two-Tier Architecture

## Goal
Execute a two-tier outreach strategy to protect core domain reputation. Use a bulk-friendly ESP (Brevo) for initial icebreakers, and a high-deliverability ESP (Resend) for delivering core offers and free trials ONLY to leads who respond.

## Process Flow

### Phase 1: Local Email Verification
*   **Tool:** `execution/free_email_verifier.py`
*   **Input:** Place raw leads in `.tmp/raw_emails.txt`.
*   **Action:** Runs syntax and DNS MX checks locally.
*   **Output:** Generates `.tmp/free_verified_emails.csv`.

### Phase 2: Tier 1 - The Icebreaker (Brevo)
*   **Tool:** `execution/send_campaign.py` (Adapted for Brevo/Instantly)
*   **Input:** `.tmp/free_verified_emails.csv`
*   **Action:** Sends one of the 5 curiosity-invoking icebreaker variations. No links, no heavy HTML.
*   **Outcome:** If no reply, leave them alone. Do NOT send the core offer.

### Phase 3: Tier 2 - The Core Offer (Resend)
*   **Tool:** `execution/send_resend_offer.py`
*   **Input:** Leads who replied positively are manually or automatically placed into `.tmp/replied_leads.csv`.
*   **Action:** Triggers the Resend API to deliver the detailed proposition, case studies, and the free trial offer.
*   **Safety:** Because this is only sent to engaged leads, it maintains exceptional deliverability and domain trust.

## Important Rules
- **Domain Separation:** Never use the same domain for Tier 1 and Tier 2. Tier 1 should use disposable/burner domains. Tier 2 should use a trusted subdomain of your main company domain.
- **Data Privacy:** Ensure the text files in `.tmp/` are regularly cleared after processing to protect lead data.
