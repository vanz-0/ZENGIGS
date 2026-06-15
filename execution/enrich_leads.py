import os
import sys
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

def enrich_leads(limit=1000):
    supabase = get_supabase_client()
    if not supabase:
        print("Could not connect to Supabase.")
        return

    # Fetch leads that need enrichment (where personalization is null)
    # Since we can easily query IS NULL, we'll fetch 'new' leads without a personalization line.
    res = supabase.table("leads").select("*").eq("status", "new").is_("personalization_line", "null").limit(limit).execute()
    leads = res.data

    if not leads:
        print("No new leads to enrich.")
        return

    print(f"Starting enrichment for {len(leads)} leads...")
    enriched_count = 0

    for i, lead in enumerate(leads):
        website = lead.get("website")
        company = lead.get("company")
        lead_id = lead.get("id")

        if not website:
            print(f"[{i+1}/{len(leads)}] Skipping {lead_id} - no website")
            continue

        safe_company = company.encode("ascii", "ignore").decode() if company else "Unknown"
        print(f"[{i+1}/{len(leads)}] Enriching {safe_company} ({website})...")
        
        try:
            result = generate_personalization(website, company)
            
            # Update Supabase
            update_data = {
                "business_summary": result.get("business_summary", ""),
                "recent_data": result.get("recent_data", ""),
                "personalization_line": result.get("personalization_line", ""),
            }
            
            supabase.table("leads").update(update_data).eq("id", lead_id).execute()
            enriched_count += 1
            print(f"  -> Success: {result.get('personalization_line')}")
            
        except Exception as e:
            print(f"  -> Failed: {e}")
            
        # Small delay to respect rate limits
        time.sleep(1)

    print(f"Enrichment complete. Enriched {enriched_count} leads.")

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    enrich_leads(limit)
