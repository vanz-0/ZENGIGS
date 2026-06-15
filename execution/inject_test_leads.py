import os
import json
import time
from dotenv import load_dotenv
from supabase import create_client
from lead_scraper_generic import generate_personalization

load_dotenv()

def get_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        return None
    return create_client(url, key)

def inject_test_leads():
    supabase = get_supabase_client()
    if not supabase: return

    test_leads = [
        {"email": "test1@apify.com", "first_name": "Jan", "company": "Apify", "website": "https://apify.com", "status": "new", "campaign_id": "master_v1"},
        {"email": "test2@supabase.com", "first_name": "Paul", "company": "Supabase", "website": "https://supabase.com", "status": "new", "campaign_id": "master_v2"},
        {"email": "test3@vercel.com", "first_name": "Guillermo", "company": "Vercel", "website": "https://vercel.com", "status": "new", "campaign_id": "master_v3"}
    ]

    for lead in test_leads:
        try:
            supabase.table("leads").upsert(lead, on_conflict="email").execute()
            print(f"Injected test lead: {lead['email']}")
        except Exception as e:
            print(f"Failed to inject {lead['email']}: {e}")

if __name__ == "__main__":
    print("Injecting test leads for verification...")
    inject_test_leads()
    print("Test leads injected.")
