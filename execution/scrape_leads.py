#!/usr/bin/env python3
"""
Scrape leads using Apify's code_crafter/leads-finder actor.

Usage:
    python execution/scrape_leads.py --query "Coaches" --location "United States" --max_items 50
    python execution/scrape_leads.py --query "SaaS Founders" --location "UK" --max_items 25 --no-email-filter
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to load dotenv if available
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


@dataclass
class ScrapeConfig:
    """Configuration for a lead scraping run."""
    query: str
    location: str
    max_items: int = 25
    output_prefix: str = "leads"
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


def scrape_leads(config: ScrapeConfig) -> Optional[List[Dict[str, Any]]]:
    """
    Run the Apify actor to scrape leads.

    Returns a list of lead dicts, or None on failure.
    """
    api_token = os.getenv("APIFY_API_TOKEN")
    if not api_token:
        logger.error("APIFY_API_TOKEN not found in environment. Check .env file.")
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
    logger.debug(f"Actor input: {json.dumps(run_input, indent=2)}")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            run = client.actor("code_crafter/leads-finder").call(run_input=run_input)
            break
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Actor failed after {max_retries} attempts: {e}")
                return None
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")

    if not run:
        logger.error("Actor run failed to start")
        return None

    logger.info(f"Scrape finished. Fetching from dataset {run['defaultDatasetId']}...")

    results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    logger.info(f"Found {len(results)} leads.")
    return results


def save_results(results: List[Dict], prefix: str = "leads") -> Optional[str]:
    """Save results to a timestamped JSON file in .tmp/."""
    if not results:
        logger.warning("No results to save.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = ".tmp"
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(output_dir, f"{prefix}_{timestamp}.json")

    with open(filename, "w") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Results saved to {filename}")

    # Print summary
    response = {
        "success": True,
        "leadsFound": len(results),
        "outputFile": filename,
    }
    print(json.dumps(response, indent=2))
    return filename


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape leads using Apify")
    parser.add_argument("--query", required=True, help="Search query (e.g., 'Coaches')")
    parser.add_argument("--location", required=True, help="Location (e.g., 'United States')")
    parser.add_argument("--max_items", type=int, default=25, help="Max leads to scrape (default: 25)")
    parser.add_argument("--output_prefix", default="leads", help="Output file prefix")
    parser.add_argument("--job_titles", nargs='+', help="Specific job titles to target")
    parser.add_argument("--company_keywords", nargs='+', help="Company keyword filters")
    parser.add_argument("--no-email-filter", action="store_true", help="Don't filter by validated emails")

    args = parser.parse_args()

    try:
        config = ScrapeConfig(
            query=args.query,
            location=args.location,
            max_items=args.max_items,
            output_prefix=args.output_prefix,
            require_email=not args.no_email_filter,
            job_titles=args.job_titles,
            company_keywords=args.company_keywords,
        )
    except ValueError as e:
        logger.error(f"Invalid configuration: {e}")
        sys.exit(1)

    results = scrape_leads(config)

    if results:
        save_results(results, prefix=config.output_prefix)
    else:
        print(json.dumps({"success": False, "error": "No leads found or API error."}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
