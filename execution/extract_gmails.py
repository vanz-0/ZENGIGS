import csv
import re

def extract_email(text):
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group(0).lower() if match else None

def extract_gmails():
    input_file = '.tmp/free_verified_emails.csv'
    output_file = '.tmp/gmail_leads.csv'
    
    gmails = []
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            line_text = ",".join(row)
            email = extract_email(line_text)
            if email and email.endswith('@gmail.com'):
                # Extract name roughly
                name = row[0] if row else ""
                gmails.append({"name": name.strip(), "email": email})
                
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email"])
        writer.writeheader()
        writer.writerows(gmails)
        
    print(f"Extracted {len(gmails)} Gmails to {output_file}")

if __name__ == "__main__":
    extract_gmails()
