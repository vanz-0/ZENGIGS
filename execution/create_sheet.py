import os
import json
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

def create_lead_sheet():
    print("Authenticating with Google Sheets...")
    creds = get_credentials()
    client = gspread.authorize(creds)
    
    sheet_name = "ZENGIGS Master Lead Database"
    print(f"Creating new spreadsheet: {sheet_name}")
    
    try:
        spreadsheet = client.create(sheet_name)
        
        # Define the tabs we want
        tabs = [
            "Upwork",
            "Fiverr",
            "PeoplePerHour",
            "Gmail Script",
            "Reddit Script",
            "LinkedIn Script",
            "Google Maps"
        ]
        
        # Rename default sheet to the first tab
        worksheet = spreadsheet.sheet1
        worksheet.update_title(tabs[0])
        
        # Create the rest of the tabs
        for tab in tabs[1:]:
            print(f"Creating tab: {tab}")
            spreadsheet.add_worksheet(title=tab, rows="1000", cols="20")
            
        print(f"Successfully created spreadsheet!")
        print(f"URL: {spreadsheet.url}")
        
        # Save the URL to a text file for reference
        with open('.tmp/new_sheet_url.txt', 'w') as f:
            f.write(spreadsheet.url)
            
    except Exception as e:
        print(f"Failed to create spreadsheet: {e}")

if __name__ == "__main__":
    create_lead_sheet()
