#!/usr/bin/env python3
"""
Scrape leads using Apify's code_crafter/leads-finder actor and save to Supabase.

Usage:
    python execution/scrape_leads.py --query "SaaS Founders" --location "United States" --max_items 50
"""

import os
import sys
import json
import time
import argparse
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to load dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from apify_client import ApifyClient
except ImportError:
    logger.error("apify-client not installed. Run: pip install apify-client")
    sys.exit(1)

try:
    from supabase import create_client, Client
except ImportError:
    logger.error("supabase not installed. Run: pip install supabase")
    sys.exit(1)

# ─── Configuration ────────────────────────────────────────────────────────────

@dataclass
class ScrapeConfig:
    query: str
    location: str
    max_items: int = 50
    require_email: bool = True
    job_titles: Optional[List[str]] = None
    company_keywords: Optional[List[str]] = None

    def __post_init__(self):
        if not self.query:
            raise ValueError("Search query is required")
        if not self.location:
            raise ValueError("Location is required")
        if self.max_items < 1:
            raise ValueError("max_items must be at least 1")

# ─── Supabase Client ──────────────────────────────────────────────────────────

def get_supabase_client() -> Optional[Client]:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        logger.error("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY required in .env")
        return None
    return create_client(url, key)

# ─── Scraper Logic ────────────────────────────────────────────────────────────

def scrape_leads(config: ScrapeConfig) -> Optional[List[Dict[str, Any]]]:
    """Run Apify actor to scrape leads with exponential backoff."""
    api_token = os.getenv("APIFY_API_TOKEN")
    if not api_token:
        logger.error("APIFY_API_TOKEN not found in .env")
        return None

    client = ApifyClient(api_token)

    run_input = {
        "fetch_count": config.max_items,
        "contact_job_title": config.job_titles or [config.query],
        "company_keywords": config.company_keywords or [config.query],
        "contact_location": [config.location.lower()],
        "language": "en",
    }
    if config.require_email:
        run_input["email_status"] = ["validated"]

    logger.info(f"Starting scrape for '{config.query}' in '{config.location}' (limit: {config.max_items})")

    # Exponential backoff for API calls
    max_retries = 3
    for attempt in range(max_retries):
        try:
            run = client.actor("code_crafter/leads-finder").call(run_input=run_input)
            break
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Apify actor failed after {max_retries} attempts: {e}")
                return None
            wait_time = 2 ** (attempt + 1)
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)

    if not run:
        logger.error("Actor run failed to start")
        return None

    dataset_id = run["defaultDatasetId"]
    logger.info(f"Scrape finished. Fetching from dataset {dataset_id}...")

    results = list(client.dataset(dataset_id).iterate_items())
    logger.info(f"Found {len(results)} raw leads.")
    return results

def normalize_and_save(results: List[Dict], niche: str) -> Dict[str, Any]:
    """Normalize raw Apify data and save to Supabase."""
    if not results:
        return {"success": False, "saved": 0, "error": "No results"}

    supabase = get_supabase_client()
    if not supabase:
        return {"success": False, "saved": 0, "error": "No Supabase client"}

    normalized = []
    for row in results:
        email = row.get("email") or row.get("contact_email")
        first_name = row.get("first_name") or row.get("contact_first_name", "")
        last_name = row.get("last_name") or row.get("contact_last_name", "")
        company = row.get("company_name") or row.get("company", "")
        website = row.get("company_domain") or row.get("website", "")
        location = row.get("contact_location") or row.get("location", "")

        if not email:
            continue # Email is required

        normalized.append({
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "company": company,
            "website": website,
            "location": location,
            "niche": niche,
            "status": "new",
            "source": "apify_scrape"
        })

    if not normalized:
        logger.warning("No leads had valid emails after normalization.")
        return {"success": True, "saved": 0}

    # Upsert to Supabase
    saved_count = 0
    try:
        # Supabase Python client upsert
        res = supabase.table("leads").upsert(normalized, on_conflict="email").execute()
        saved_count = len(res.data)
        logger.info(f"Successfully upserted {saved_count} leads to Supabase.")
    except Exception as e:
        logger.error(f"Supabase upsert failed: {e}")
        # Fallback to local JSON
        backup_file = f".tmp/leads_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(".tmp", exist_ok=True)
        with open(backup_file, "w") as f:
            json.dump(normalized, f, indent=2)
        logger.info(f"Saved normalized leads to {backup_file} as fallback.")
        return {"success": False, "saved": 0, "error": str(e), "fallback": backup_file}

    # Update KPI tracker
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        kpi_res = supabase.table("kpi_logs").upsert(
            {"log_date": today, "leads_scraped": saved_count}, 
            on_conflict="log_date"
        ).execute()
    except Exception as e:
        logger.warning(f"Failed to update KPIs: {e}")

    return {"success": True, "saved": saved_count}

def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape B2B leads via Apify and sync to Supabase")
    parser.add_argument("--query", required=True, help="Search query (e.g., 'SaaS Founders')")
    parser.add_argument("--location", required=True, help="Location (e.g., 'United States')")
    parser.add_argument("--max_items", type=int, default=50, help="Max leads to scrape")
    parser.add_argument("--no-email-filter", action="store_true", help="Don't filter by validated emails")

    args = parser.parse_args()

    try:
        config = ScrapeConfig(
            query=args.query,
            location=args.location,
            max_items=args.max_items,
            require_email=not args.no_email_filter,
        )
    except ValueError as e:
        logger.error(f"Invalid config: {e}")
        sys.exit(1)

    # 1. Scrape
    results = scrape_leads(config)

    # 2. Normalize and Sync
    if results:
        sync_res = normalize_and_save(results, niche=config.query)
        
        # Cost Tracking
        cost_per_lead = 0.015 # Approx Apify cost
        total_cost = config.max_items * cost_per_lead
        logger.info(f"--- Cost Analysis ---")
        logger.info(f"Requested leads : {config.max_items}")
        logger.info(f"Estimated Cost  : ${total_cost:.2f}")
        logger.info(f"Saved to DB     : {sync_res.get('saved', 0)}")
        
        print(json.dumps(sync_res))
    else:
        print(json.dumps({"success": False, "error": "No results or API failure"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
