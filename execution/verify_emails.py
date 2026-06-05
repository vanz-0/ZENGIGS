import csv
import os
import json
import time

# NOTE: This is a scaffold. You will need to install requests (pip install requests)
# and add your actual API keys to a .env file.
# import requests

RAW_EMAILS_PATH = "../.tmp/raw_emails.csv"
VERIFIED_EMAILS_PATH = "../.tmp/verified_emails.csv"
API_KEY = os.getenv("VERIFICATION_API_KEY", "your_placeholder_api_key")

def verify_email_mock(email):
    """
    Mock function simulating an API call to ZeroBounce, NeverBounce, etc.
    In a real scenario, this would be:
    response = requests.get(f"https://api.verification-service.com/v1/verify?email={email}&api_key={API_KEY}")
    return response.json()
    """
    # Simulate API latency
    time.sleep(0.5)
    
    # Mock logic: assume emails with 'test' or 'spam' are invalid, others valid.
    if 'test' in email or 'spam' in email:
        return {"status": "invalid"}
    return {"status": "valid"}

def main():
    if not os.path.exists(RAW_EMAILS_PATH):
        print(f"Error: {RAW_EMAILS_PATH} not found. Please provide the raw emails list.")
        return

    verified_list = []

    print("Starting email verification process...")
    with open(RAW_EMAILS_PATH, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        # Assuming the CSV has an 'email' column
        for row in reader:
            email = row.get('email')
            if not email:
                continue
            
            print(f"Verifying: {email}...")
            result = verify_email_mock(email)
            
            if result.get("status") == "valid":
                verified_list.append(row)
                print(f" -> Valid")
            else:
                print(f" -> Invalid/Risky. Skipping.")

    if verified_list:
        with open(VERIFIED_EMAILS_PATH, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=verified_list[0].keys())
            writer.writeheader()
            writer.writerows(verified_list)
        print(f"Verification complete. Saved {len(verified_list)} safe emails to {VERIFIED_EMAILS_PATH}")
    else:
        print("No valid emails found to save.")

if __name__ == "__main__":
    # Ensure .tmp exists relative to script
    os.makedirs("../.tmp", exist_ok=True)
    main()
