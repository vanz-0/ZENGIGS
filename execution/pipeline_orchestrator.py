#!/usr/bin/env python3
"""
ZENGIGS Master Pipeline Orchestrator.

Orchestrates the entire flow from scraping leads to sending outreach emails.
Follows the directives laid out in directives/02_cold_outreach_system.md and 05_lead_scraping.md.

Usage:
    python execution/pipeline_orchestrator.py --action scrape --query "Coaches" --location "UK"
    python execution/pipeline_orchestrator.py --action outreach --template cold_intro
"""

import os
import sys
import subprocess
import argparse
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ORCHESTRATOR] - %(message)s')
logger = logging.getLogger(__name__)

def run_script(script_name: str, args: list) -> bool:
    """Run a Python script as a subprocess."""
    cmd = [sys.executable, f"execution/{script_name}"] + args
    logger.info(f"Executing: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        logger.info(f"Script output:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Script failed with error code {e.returncode}")
        logger.error(f"Error output:\n{e.stderr}")
        return False

def run_scrape(query: str, location: str, max_items: int, mode: str):
    """Run the scraping and normalization pipeline."""
    logger.info(f"=== Starting Scrape Pipeline (Mode: {mode}) ===")
    args = [
        "--query", query,
        "--location", location,
        "--max_items", str(max_items),
        "--mode", mode
    ]
    success = run_script("scrape_leads.py", args)
    if success:
        logger.info("Scrape Pipeline Completed Successfully.")
    else:
        logger.error("Scrape Pipeline Failed.")

def run_outreach(template: str, daily_cap: int, dry_run: bool):
    """Run the cold outreach pipeline."""
    logger.info("=== Starting Outreach Pipeline ===")
    args = [
        "--template", template,
        "--daily_cap", str(daily_cap)
    ]
    if dry_run:
        args.append("--dry_run")
        
    success = run_script("cold_email_sender.py", args)
    if success:
        logger.info("Outreach Pipeline Completed Successfully.")
    else:
        logger.error("Outreach Pipeline Failed.")

def main():
    parser = argparse.ArgumentParser(description="ZENGIGS Master Pipeline Orchestrator")
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
        run_scrape(args.query, args.location, args.max_items, args.mode)
        
    if args.action in ["outreach", "full"]:
        run_outreach(args.template, args.daily_cap, args.dry_run)

if __name__ == "__main__":
    main()
