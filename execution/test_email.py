import sys
import os
import logging
from cold_email_sender import SMTPConfig, send_email, personalize_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_test():
    try:
        smtp_config = SMTPConfig.from_env()
    except Exception as e:
        logger.error(f"Failed to load SMTP config: {e}")
        sys.exit(1)

    lead = {"first_name": "Test", "company": "Test Company", "email": "Merchzenith@gmail.com"}
    email_data = personalize_email("master_v4", lead, smtp_config.sender_name)
    
    if not email_data:
        logger.error("Failed to generate email data.")
        sys.exit(1)

    logger.info(f"Sending test email to {lead['email']} as {smtp_config.sender_name} <{smtp_config.sender_email}>...")
    
    success = send_email(smtp_config, lead["email"], email_data["subject"], email_data["body"])
    
    if success:
        logger.info("✅ Test email sent successfully!")
    else:
        logger.error("❌ Failed to send test email.")

if __name__ == "__main__":
    run_test()
