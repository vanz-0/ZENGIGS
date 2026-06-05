import csv
import os
import time

VERIFIED_EMAILS_PATH = "../.tmp/verified_emails.csv"
OUTREACH_API_KEY = os.getenv("OUTREACH_API_KEY", "your_outreach_api_key")
CAMPAIGN_ID = "us_online_services_campaign"
DAILY_LIMIT = 200 # Across all senders

def add_lead_to_campaign(lead_data):
    """
    Mock function simulating API call to Instantly, Smartlead, or Lemlist.
    """
    # In reality: requests.post(..., json={"email": lead_data['email'], "campaign_id": CAMPAIGN_ID})
    time.sleep(0.2)
    return True

def main():
    if not os.path.exists(VERIFIED_EMAILS_PATH):
        print(f"Error: No verified emails found at {VERIFIED_EMAILS_PATH}. Run verify_emails.py first.")
        return

    leads_to_inject = []
    remaining_leads = []

    # Read verified emails
    with open(VERIFIED_EMAILS_PATH, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        all_leads = list(reader)

    # Slice the daily limit
    leads_to_inject = all_leads[:DAILY_LIMIT]
    remaining_leads = all_leads[DAILY_LIMIT:]

    print(f"Injecting {len(leads_to_inject)} leads into Campaign: {CAMPAIGN_ID}")
    
    success_count = 0
    for lead in leads_to_inject:
        print(f"Adding {lead.get('email')}...")
        if add_lead_to_campaign(lead):
            success_count += 1
    
    print(f"Successfully added {success_count} leads to the campaign.")

    # Rewrite the verified emails file without the injected leads
    if remaining_leads:
        with open(VERIFIED_EMAILS_PATH, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=remaining_leads[0].keys())
            writer.writeheader()
            writer.writerows(remaining_leads)
        print(f"Saved {len(remaining_leads)} remaining leads for future injections.")
    else:
        # Empty the file if all leads are consumed
        open(VERIFIED_EMAILS_PATH, 'w').close()
        print("All verified leads have been injected. Queue is empty.")

if __name__ == "__main__":
    main()
