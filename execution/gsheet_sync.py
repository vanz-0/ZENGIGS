#!/usr/bin/env python3
"""
Synchronizes leads from Supabase to a Google Sheet.

Usage:
    python execution/gsheet_sync.py
"""

import os
import sys
import logging

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import gspread
from google.oauth2.service_account import Credentials

try:
    from supabase import create_client, Client
except ImportError:
    logging.error("supabase not installed. Run: pip install supabase")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        logger.error("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")
        sys.exit(1)
    return create_client(url, key)

def get_google_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_path = "credentials.json"
    if not os.path.exists(creds_path):
        logger.error(f"Credentials file '{creds_path}' not found.")
        sys.exit(1)
    
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        logger.error("Missing GOOGLE_SHEET_ID in .env")
        sys.exit(1)
        
    try:
        credentials = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(sheet_id).sheet1
        return sheet
    except Exception as e:
        logger.error(f"Google Sheets connection failed: {e}")
        sys.exit(1)

def sync_to_gsheet():
    logger.info("Connecting to Supabase...")
    supabase = get_supabase_client()
    
    logger.info("Fetching leads from Supabase...")
    res = supabase.table("leads").select("*").execute()
    leads = res.data
    
    if not leads:
        logger.info("No leads found in Supabase.")
        return
        
    logger.info(f"Fetched {len(leads)} leads. Connecting to Google Sheets...")
    sheet = get_google_sheet()
    
    # Prepare data for sheet
    headers = ["id", "email", "first_name", "last_name", "company", "website", "location", "niche", "campaign_id", "free_offer_text", "business_summary", "recent_data", "personalization_line", "status", "source", "created_at"]
    rows = [headers]
    
    for lead in leads:
        row = [str(lead.get(col, "")) for col in headers]
        rows.append(row)
        
    try:
        sheet.clear()
        sheet.update(range_name='A1', values=rows)
        logger.info(f"Successfully synced {len(leads)} leads to Google Sheets.")
    except Exception as e:
        logger.error(f"Failed to update Google Sheet: {e}")

if __name__ == "__main__":
    sync_to_gsheet()
