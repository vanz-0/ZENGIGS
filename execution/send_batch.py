import os
import csv
import time
import random
import logging
from cold_email_sender import SMTPConfig, send_email, personalize_email

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

INPUT_FILE = ".tmp/gmail_leads.csv"
SENT_FILE = ".tmp/sent_emails.csv"
TEMPLATE = "master_v4"
BATCH_SIZE = 30

def send_batch():
    if not os.path.exists(INPUT_FILE):
        logger.error(f"Input file {INPUT_FILE} not found.")
        return

    try:
        smtp_config = SMTPConfig.from_env()
    except Exception as e:
        logger.error(f"Failed to load SMTP config: {e}")
        return

    # Read verified leads
    leads = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)

    if not leads:
        logger.info("No leads available to send.")
        return

    # Take the first BATCH_SIZE leads
    batch = leads[:BATCH_SIZE]
    remaining = leads[BATCH_SIZE:]

    sent_count = 0
    failed_count = 0
    successfully_sent = []

    logger.info(f"Starting batch of {len(batch)} emails...")

    # Pre-calculate random send times within a 2-hour window (7200 seconds)
    # This guarantees the first email does NOT go out exactly at 5:00 PM
    send_times = sorted([random.randint(60, 7200) for _ in range(len(batch))])
    
    start_time = time.time()
    
    for i, lead_data in enumerate(batch):
        # Calculate delay to hit our randomly scheduled time
        target_time = start_time + send_times[i]
        now = time.time()
        if target_time > now:
            delay = target_time - now
            logger.info(f"  \u23f3 Waiting {delay:.1f}s until next randomly scheduled send...")
            time.sleep(delay)

        # Convert CSV row to the format expected by personalize_email
        email = lead_data.get("email", "").strip()
        raw_name = lead_data.get("name", "").strip()
        
        if not email:
            failed_count += 1
            continue

        # Extract first name roughly if available, else let personalize_email handle it
        first_name = "there"
        if raw_name:
            first_name = raw_name.split()[0]
            first_name = ''.join(e for e in first_name if e.isalnum())

        lead = {
            "first_name": first_name,
            "company": "your company", # Fallback
            "email": email
        }

        email_data = personalize_email(TEMPLATE, lead, smtp_config.sender_name)
        if not email_data:
            failed_count += 1
            continue

        logger.info(f"[{i+1}/{len(batch)}] Sending to {email} as {smtp_config.sender_name} <{smtp_config.sender_email}>...")
        
        success = send_email(smtp_config, email, email_data["subject"], email_data["body"])
        
        if success:
            logger.info(f"  \u2705 Sent successfully!")
            sent_count += 1
            successfully_sent.append(lead_data)
        else:
            logger.error(f"  \u274c Failed to send.")
            failed_count += 1

    logger.info("--- Batch Complete ---")
    logger.info(f"Sent: {sent_count}")
    logger.info(f"Failed: {failed_count}")

    # Update files
    file_exists = os.path.isfile(SENT_FILE)
    with open(SENT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(successfully_sent)
        
    with open(INPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email"])
        writer.writeheader()
        writer.writerows(remaining)
        
    logger.info(f"Updated CSVs. {len(remaining)} leads remaining in {INPUT_FILE}.")

if __name__ == "__main__":
    send_batch()
