import os
import json
import csv
import re
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        try:
            with open('token.json', 'r') as token:
                token_data = json.load(token)
                creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except Exception as e:
            print(f"Error loading token: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            creds_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def extract_email(text):
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group(0).lower() if match else None

def process_and_upload():
    print("Reading and filtering emails...")
    gmails = []
    yahoos = []
    hotmails = []

    input_file = '.tmp/free_verified_emails.csv'
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
        for row in reader:
            line_text = ",".join(row)
            email = extract_email(line_text)
            if email:
                if email.endswith('@gmail.com'):
                    gmails.append([email])
                elif email.endswith('@yahoo.com') or email.endswith('@ymail.com'):
                    yahoos.append([email])
                elif email.endswith('@hotmail.com'):
                    hotmails.append([email])

    print(f"Found {len(gmails)} Gmails, {len(yahoos)} Yahoos, {len(hotmails)} Hotmails.")

    print("Authenticating with Google Sheets...")
    creds = get_credentials()
    client = gspread.authorize(creds)
    
    sheet_name = "Filtered Email List (1000)"
    print(f"Creating new spreadsheet: {sheet_name}")
    
    try:
        spreadsheet = client.create(sheet_name)
        
        # Set up Gmail tab
        worksheet = spreadsheet.sheet1
        worksheet.update_title("Gmails")
        if gmails:
            worksheet.update('A1', [['Email']] + gmails)
        
        # Set up Yahoo tab
        yahoo_ws = spreadsheet.add_worksheet(title="Yahoos", rows=str(max(100, len(yahoos)+10)), cols="10")
        if yahoos:
            yahoo_ws.update('A1', [['Email']] + yahoos)
            
        # Set up Hotmail tab
        hotmail_ws = spreadsheet.add_worksheet(title="Hotmails", rows=str(max(100, len(hotmails)+10)), cols="10")
        if hotmails:
            hotmail_ws.update('A1', [['Email']] + hotmails)
            
        print(f"Successfully created spreadsheet!")
        print(f"URL: {spreadsheet.url}")
        
    except Exception as e:
        print(f"Failed to create spreadsheet: {e}")

if __name__ == "__main__":
    process_and_upload()
