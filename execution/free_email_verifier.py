import re
import dns.resolver
import smtplib
import socket
import csv
import os

# Note: You will need to install dnspython
# pip install dnspython

INPUT_FILE = "../.tmp/raw_emails.txt" # Update to the path of your note file
OUTPUT_FILE = "../.tmp/free_verified_emails.csv"

def extract_email_and_name(line):
    """
    Attempts to extract an email and name from a line of text.
    Assumes format might be: "John Doe johndoe@email.com" or "John Doe, johndoe@email.com"
    """
    line = line.strip()
    if not line:
        return None, None
        
    # Basic email regex extraction
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line)
    if not email_match:
        return None, None
        
    email = email_match.group(0)
    
    # Try to extract the name by removing the email and any commas/extra spaces
    name_part = line.replace(email, '').replace(',', '').strip()
    name = name_part if name_part else "Friend"
    
    return name, email

def check_syntax(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def check_mx_record(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = records[0].exchange
        return str(mx_record)
    except Exception:
        return None

def verify_email(email):
    print(f"Verifying {email}...")
    
    # 1. Syntax Check
    if not check_syntax(email):
        print(" -> Failed: Invalid syntax.")
        return False
        
    domain = email.split('@')[1]
    
    # 2. DNS MX Check
    mx_record = check_mx_record(domain)
    if not mx_record:
        print(" -> Failed: No MX records found for domain.")
        return False
        
    # 3. SMTP Ping (Optional/Advanced - often blocked by local ISPs)
    # For a truly free robust system, MX check is usually the safest local check.
    # We will return True if MX exists, as doing deep SMTP from a residential IP 
    # will often result in timeouts or being blacklisted.
    print(f" -> Passed: MX Record found ({mx_record}).")
    return True

TARGET_LIMIT = 15000

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Could not find input file at {INPUT_FILE}")
        print("Please place your note file there and try again.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = len(lines)
    valid_count = 0
    checked_count = 0

    # Open CSV for incremental writing
    csvfile = open(OUTPUT_FILE, 'w', newline='', encoding='utf-8')
    fieldnames = ['name', 'email']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    csvfile.flush()

    print(f"Starting verification of {total_lines:,} lines. Will stop at {TARGET_LIMIT:,} valid emails.")
    print("-" * 60)

    for index, line in enumerate(lines):
        name, email = extract_email_and_name(line)
        if email:
            checked_count += 1
            is_valid = verify_email(email)
            if is_valid:
                writer.writerow({"name": name, "email": email})
                csvfile.flush()  # Save immediately
                valid_count += 1

                # Print progress every 100 valid emails
                if valid_count % 100 == 0:
                    print(f"\n>>> PROGRESS: {valid_count:,} / {TARGET_LIMIT:,} valid emails collected (checked {checked_count:,} total)\n")

                # Stop at target
                if valid_count >= TARGET_LIMIT:
                    print(f"\n{'='*60}")
                    print(f"✅ TARGET REACHED: {valid_count:,} valid emails collected!")
                    print(f"   Checked {checked_count:,} total emails to get here.")
                    print(f"   Saved to: {OUTPUT_FILE}")
                    print(f"{'='*60}")
                    break

    csvfile.close()
    
    # --- NEW LOGIC: Remove processed lines from the raw file ---
    remaining_lines = lines[index + 1:]
    with open(INPUT_FILE, 'w', encoding='utf-8') as f:
        f.writelines(remaining_lines)
    print(f"\nPruned {index + 1:,} processed lines from {INPUT_FILE}. {len(remaining_lines):,} lines remaining.")

    if valid_count < TARGET_LIMIT:
        print(f"\nVerification Complete! Saved {valid_count:,} valid emails to {OUTPUT_FILE}")
        print(f"(Checked {checked_count:,} total emails)")

if __name__ == "__main__":
    main()
