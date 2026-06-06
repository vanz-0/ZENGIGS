import os
import csv
import time

# Note: You will need to install the Resend Python SDK
# pip install resend

REPLIED_LEADS_PATH = "../.tmp/replied_leads.csv"
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "your_resend_api_key")

def send_offer_via_resend(lead_data):
    """
    Mock function simulating the Resend API call.
    In reality:
    import resend
    resend.api_key = RESEND_API_KEY
    resend.Emails.send({
        "from": "onboarding@yourtier2domain.com",
        "to": lead_data['email'],
        "subject": "Your Digital Footprint Proposition + Free Trial",
        "html": "<p>Hi, here are the case studies and the free trial link...</p>"
    })
    """
    time.sleep(0.3) # Simulate network call
    return True

def main():
    if not os.path.exists(REPLIED_LEADS_PATH):
        print(f"No new replies found at {REPLIED_LEADS_PATH}. Waiting for next batch.")
        return

    with open(REPLIED_LEADS_PATH, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        leads = list(reader)

    if not leads:
        print("Reply file is empty.")
        return

    print(f"Found {len(leads)} leads who replied positively. Initiating Tier 2 sending via Resend...")
    
    success_count = 0
    for lead in leads:
        print(f"Sending core offer to: {lead.get('email')}...")
        if send_offer_via_resend(lead):
            success_count += 1
            print(" -> Sent Successfully")
        else:
            print(" -> Failed to Send")

    print(f"Successfully delivered {success_count} core offers.")
    
    # Empty the file after processing to avoid double sending
    open(REPLIED_LEADS_PATH, 'w').close()
    print("Cleared processed leads from queue.")

if __name__ == "__main__":
    main()
