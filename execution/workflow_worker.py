#!/usr/bin/env python3
"""
ZENGIGS Workflow Worker.

Polls the `workflow_jobs` table in Supabase for pending jobs and executes them.
Intended to be run periodically via cron or Windows Task Scheduler.
"""

import os
import sys
import subprocess
import logging
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [WORKER] - %(message)s')
logger = logging.getLogger(__name__)

# Load Supabase
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("Supabase credentials missing.")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
MAX_RETRIES = 3

def run_script(script_name: str, args: list) -> tuple:
    """Run a Python script as a subprocess. Returns (success, output)."""
    cmd = [sys.executable, f"execution/{script_name}"] + args
    logger.info(f"Executing: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        logger.info(f"Script output:\n{result.stdout}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Script failed with error code {e.returncode}")
        logger.error(f"Error output:\n{e.stderr}")
        return False, e.stderr

def fetch_pending_job():
    try:
        # Get one pending job
        res = supabase.table("workflow_jobs").select("*").eq("status", "pending").order("created_at").limit(1).execute()
        if res.data:
            return res.data[0]
        return None
    except Exception as e:
        logger.error(f"Failed to fetch job: {e}")
        return None

def process_job(job):
    job_id = job['id']
    job_type = job['job_type']
    params = job['parameters']
    retry_count = job.get('retry_count', 0)
    
    logger.info(f"Processing job {job_id} of type '{job_type}' (Retry: {retry_count})")
    
    # Mark as running
    supabase.table("workflow_jobs").update({"status": "running"}).eq("id", job_id).execute()
    
    success = False
    error_msg = ""
    
    if job_type == "scrape":
        args = [
            "--query", params.get("query", ""),
            "--location", params.get("location", ""),
            "--max_items", str(params.get("max_items", 50)),
            "--mode", params.get("mode", "active")
        ]
        success, error_msg = run_script("scrape_leads.py", args)
        
    elif job_type == "outreach":
        # The user mentioned pausing outreach due to spam issues, so we can mock or just execute as normal
        args = [
            "--template", params.get("template", "cold_intro"),
            "--daily_cap", str(params.get("daily_cap", 10))
        ]
        if params.get("dry_run", False):
            args.append("--dry_run")
        success, error_msg = run_script("cold_email_sender.py", args)
    else:
        success = False
        error_msg = f"Unknown job_type: {job_type}"
        
    if success:
        logger.info(f"Job {job_id} completed successfully.")
        supabase.table("workflow_jobs").update({
            "status": "completed",
            "error_message": None
        }).eq("id", job_id).execute()
    else:
        logger.error(f"Job {job_id} failed.")
        new_retry_count = retry_count + 1
        new_status = "pending" if new_retry_count < MAX_RETRIES else "failed"
        
        supabase.table("workflow_jobs").update({
            "status": new_status,
            "retry_count": new_retry_count,
            "error_message": error_msg[:1000] # Truncate long errors
        }).eq("id", job_id).execute()
        
        if new_status == "failed":
            logger.error(f"Job {job_id} permanently failed after {MAX_RETRIES} retries.")

def main():
    logger.info("Worker started. Checking for pending jobs...")
    
    # Process jobs sequentially until there are no more pending
    while True:
        job = fetch_pending_job()
        if not job:
            logger.info("No pending jobs found. Exiting.")
            break
        process_job(job)

if __name__ == "__main__":
    main()
