#!/usr/bin/env python3
"""
ZENGIGS Master Pipeline Orchestrator.

Enqueues jobs into the Supabase workflow_jobs table for the worker to process.
"""

import os
import sys
import argparse
import logging
from dotenv import load_dotenv
from supabase import create_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ORCHESTRATOR] - %(message)s')
logger = logging.getLogger(__name__)

# Load Supabase
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL else None

def enqueue_job(job_type: str, parameters: dict):
    if not supabase:
        logger.error("Supabase credentials missing. Cannot enqueue job.")
        return
    try:
        data = {
            "job_type": job_type,
            "parameters": parameters,
            "status": "pending"
        }
        res = supabase.table("workflow_jobs").insert(data).execute()
        logger.info(f"Successfully enqueued {job_type} job. ID: {res.data[0]['id']}")
    except Exception as e:
        logger.error(f"Failed to enqueue job: {e}")

def main():
    parser = argparse.ArgumentParser(description="ZENGIGS Master Pipeline Orchestrator (Job Enqueuer)")
    parser.add_argument("--action", choices=["scrape", "outreach", "full"], required=True, help="Action to perform")
    
    # Scrape args
    parser.add_argument("--query", help="Search query for scrape")
    parser.add_argument("--location", help="Location for scrape")
    parser.add_argument("--max_items", type=int, default=50, help="Max leads to scrape")
    parser.add_argument("--mode", choices=["test", "active"], default="active", help="Scrape mode")
    
    # Outreach args
    parser.add_argument("--template", default="cold_intro", help="Email template")
    parser.add_argument("--daily_cap", type=int, default=10, help="Max emails to send")
    parser.add_argument("--dry_run", action="store_true", help="Dry run for outreach")
    
    args = parser.parse_args()
    
    if args.action in ["scrape", "full"]:
        if not args.query or not args.location:
            logger.error("--query and --location are required for scraping.")
            sys.exit(1)
        enqueue_job("scrape", {
            "query": args.query,
            "location": args.location,
            "max_items": args.max_items,
            "mode": args.mode
        })
        
    if args.action in ["outreach", "full"]:
        enqueue_job("outreach", {
            "template": args.template,
            "daily_cap": args.daily_cap,
            "dry_run": args.dry_run
        })

if __name__ == "__main__":
    main()
