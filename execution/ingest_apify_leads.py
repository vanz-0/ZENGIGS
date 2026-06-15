import os
import json
import glob
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Supabase credentials not found in .env")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def ingest_leads():
    files = glob.glob(".tmp/leads/*.json")
    if not files:
        print("No JSON files found in .tmp/leads/")
        return

    print(f"Found {len(files)} JSON files to ingest.")
    
    total_added = 0
    total_skipped = 0

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print(f"Processing {file_path} ({len(data)} records)...")
        
        batch = []
        for row in data:
            # We need an email
            email = row.get("email") or row.get("personal_email")
            if not email:
                total_skipped += 1
                continue
                
            lead_data = {
                "campaign_id": "one_one",
                "source": "lead_find",
                "first_name": row.get("first_name", ""),
                "last_name": row.get("last_name", ""),
                "email": email,
                "company": row.get("company_name", ""),
                "website": row.get("company_website", ""),
                "location": f"{row.get('city', '')}, {row.get('state', '')}".strip(", "),
                "niche": row.get("industry", ""),
                "business_summary": row.get("company_description", "")
            }
            batch.append(lead_data)
            
        if batch:
            try:
                # Upsert based on email to prevent duplicates
                response = supabase.table("leads").upsert(batch, on_conflict="email").execute()
                total_added += len(batch)
            except Exception as e:
                print(f"Error upserting batch: {e}")

    print("\n--- Ingestion Complete ---")
    print(f"Total leads added/updated: {total_added}")
    print(f"Total skipped (no email): {total_skipped}")

if __name__ == "__main__":
    ingest_leads()
