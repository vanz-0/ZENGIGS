import os
import sys
import json
from datetime import datetime
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            token_data = json.load(token)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Credentials missing or invalid. Please run create_sheet.py first.")
            sys.exit(1)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def push_to_sheet():
    json_path = '.tmp/upwork_video_leads.json'
    if not os.path.exists(json_path):
        print(f"File {json_path} does not exist.")
        sys.exit(1)
        
    with open(json_path, 'r', encoding='utf-8') as f:
        jobs = json.load(f)
        
    if not jobs:
        print("No jobs found in JSON file.")
        sys.exit(0)
        
    print(f"Loaded {len(jobs)} jobs. Authenticating...")
    creds = get_credentials()
    client = gspread.authorize(creds)
    
    # We will use the existing master sheet
    sheet_url = "https://docs.google.com/spreadsheets/d/1XhyQcGW4IDs5kzH7thoMRpPr_alEkxDEACV1A9KRtVE"
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    spreadsheet = client.open_by_key(sheet_id)
    
    # Get or create "Upwork Leads" tab
    try:
        worksheet = spreadsheet.worksheet("Upwork")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title="Upwork", rows=1000, cols=20)
        
    # Prepare data
    headers = [
        "Title", "URL", "Budget", "Experience Level", "Category", 
        "Skills", "Client Country", "Client Total Spent", "Client Hires", 
        "Posted", "Connects Cost"
    ]
    
    rows = [headers]
    for job in jobs:
        skills = ", ".join(job.get('skills', []))
        client_data = job.get('client', {})
        rows.append([
            job.get('title', ''),
            job.get('url', ''),
            job.get('budget', ''),
            job.get('experience_level', ''),
            job.get('category', ''),
            skills,
            client_data.get('country', ''),
            str(client_data.get('total_spent', 0)),
            str(client_data.get('total_hires', 0)),
            job.get('posted', ''),
            str(job.get('connects_cost', 0))
        ])
        
    # Clear existing and update
    worksheet.clear()
    worksheet.update(values=rows, range_name=f'A1:K{len(rows)}')
    
    # Format headers
    worksheet.format('A1:K1', {
        "textFormat": {"bold": True},
        "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}
    })
    
    print(f"Successfully pushed {len(jobs)} jobs to the 'Upwork' tab in your sheet.")

if __name__ == "__main__":
    push_to_sheet()
