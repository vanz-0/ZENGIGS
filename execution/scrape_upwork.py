#!/usr/bin/env python3
"""
Scrape Upwork job listings using Apify and save to Supabase active_bids table.

Usage:
    python execution/scrape_upwork.py --query "virtual assistant" --max_items 20
    python execution/scrape_upwork.py --query "automation" --max_items 10 --mode test
"""

import os
import sys
import json
import time
import argparse
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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


# ─── Apify Actor IDs for Upwork ──────────────────────────────────────────────
# These are community-maintained actors on the Apify Store.
# If one breaks, swap the ACTOR_ID to another maintained scraper.
UPWORK_ACTORS = [
    "epctex/upwork-scraper",        # Primary
    "bebity/upwork-scraper",        # Fallback 1
]

def get_supabase_client() -> Optional[Client]:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        logger.error("SUPABASE_URL and key required in .env")
        return None
    return create_client(url, key)


def scrape_upwork_jobs(query: str, max_items: int = 20) -> Optional[List[Dict[str, Any]]]:
    """Scrape Upwork job listings via Apify."""
    api_token = os.getenv("APIFY_API_TOKEN")
    if not api_token:
        logger.error("APIFY_API_TOKEN not found in .env")
        return None

    client = ApifyClient(api_token)

    run_input = {
        "searchQueries": [query],
        "maxItems": max_items,
    }

    logger.info(f"Scraping Upwork for '{query}' (limit: {max_items})...")

    for actor_id in UPWORK_ACTORS:
        try:
            logger.info(f"Trying actor: {actor_id}")
            run = client.actor(actor_id).call(run_input=run_input, timeout_secs=120)
            if run:
                dataset_id = run["defaultDatasetId"]
                results = list(client.dataset(dataset_id).iterate_items())
                logger.info(f"Got {len(results)} results from {actor_id}")
                return results
        except Exception as e:
            logger.warning(f"Actor {actor_id} failed: {e}")
            continue

    logger.error("All Upwork actors failed.")
    return None


def normalize_and_save(results: List[Dict], query: str) -> Dict[str, Any]:
    """Normalize Upwork results and save to active_bids table."""
    if not results:
        return {"success": False, "saved": 0, "error": "No results"}

    supabase = get_supabase_client()
    if not supabase:
        return {"success": False, "saved": 0, "error": "No Supabase client"}

    normalized = []
    for row in results:
        job_title = row.get("title") or row.get("jobTitle") or row.get("name", "Untitled")
        link = row.get("url") or row.get("link") or row.get("jobUrl", "")
        budget = row.get("budget") or row.get("price") or ""
        description = row.get("description") or row.get("snippet", "")

        normalized.append({
            "platform": "Upwork",
            "job_title": job_title[:255],
            "status": "scraped",
            "applied_at": datetime.now().isoformat(),
            "link": link,
        })

    if not normalized:
        return {"success": True, "saved": 0}

    saved = 0
    try:
        res = supabase.table("active_bids").insert(normalized).execute()
        saved = len(res.data)
        logger.info(f"Saved {saved} Upwork jobs to active_bids.")
    except Exception as e:
        logger.error(f"Supabase insert failed: {e}")
        backup = f".tmp/upwork_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(".tmp", exist_ok=True)
        with open(backup, "w") as f:
            json.dump(normalized, f, indent=2)
        return {"success": False, "saved": 0, "error": str(e), "fallback": backup}

    return {"success": True, "saved": saved, "platform": "Upwork"}


def main():
    parser = argparse.ArgumentParser(description="Scrape Upwork job listings via Apify")
    parser.add_argument("--query", required=True, help="Search query (e.g., 'virtual assistant')")
    parser.add_argument("--max_items", type=int, default=20, help="Max jobs to scrape")
    parser.add_argument("--mode", choices=["test", "active"], default="active")
    args = parser.parse_args()

    items = 1 if args.mode == "test" else args.max_items
    results = scrape_upwork_jobs(args.query, items)

    if results:
        res = normalize_and_save(results, args.query)
        print(json.dumps(res))
    else:
        print(json.dumps({"success": False, "error": "Scrape failed"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
