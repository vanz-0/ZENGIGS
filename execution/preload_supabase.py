import os
import csv
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def clean_name(raw_name: str):
    parts = raw_name.split()
    if not parts: return "there", ""
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""
    first_name = ''.join(e for e in first_name if e.isalnum())
    return first_name.capitalize(), last_name.capitalize()

def load_safe_leads():
    # Read the original file
    with open(".tmp/free_verified_emails.csv", "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    
    # Skip the 30 currently being processed by send_batch.py
    safe_rows = rows[30:]
    
    loaded = 0
    # Let's load the next 100 leads into Supabase to prepare the queue
    for row in safe_rows[:100]:
        email = row.get("email", "").strip()
        raw_name = row.get("name", "").strip()
        first_name, last_name = clean_name(raw_name)

        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "company": "",
            "status": "new",
            "source": "free_verified_csv"
        }
        
        try:
            supabase.table("leads").upsert(data, on_conflict="email").execute()
            loaded += 1
        except Exception as e:
            print(f"Failed to load {email}: {e}")

    print(f"Successfully pre-loaded {loaded} leads into Supabase!")

if __name__ == "__main__":
    load_safe_leads()
