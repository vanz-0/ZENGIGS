import os
import csv
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Supabase credentials not found in .env")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def clean_name(raw_name: str):
    """Extracts a reasonably clean first and last name from messy raw data."""
    parts = raw_name.split()
    if not parts:
        return "there", ""
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""
    # simple cleanup if first name has weird characters
    first_name = ''.join(e for e in first_name if e.isalnum())
    return first_name.capitalize(), last_name.capitalize()

def load_leads(limit=30):
    input_file = ".tmp/free_verified_emails.csv"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    loaded = 0
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if loaded >= limit:
                break
                
            email = row.get("email", "").strip()
            if not email:
                continue
                
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
                # Upsert or insert, assuming email might be unique
                supabase.table("leads").upsert(data, on_conflict="email").execute()
                print(f"Loaded: {first_name} ({email})")
                loaded += 1
            except Exception as e:
                print(f"Failed to load {email}: {e}")

    print(f"\nSuccessfully loaded {loaded} verified leads into Supabase.")
    print("You can now run: python execution/cold_email_sender.py --template intro_v5 --daily_cap 30")

if __name__ == "__main__":
    load_leads(30)
