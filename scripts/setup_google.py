import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pathlib import Path

# Scopes required for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

BASE_DIR = Path(__file__).parent.parent
CREDENTIALS_FILE = BASE_DIR / 'google_credentials.json'
TOKEN_FILE = BASE_DIR / 'config' / 'google_token.pickle'

def main():
    creds = None
    
    # 1. Check if token already exists
    if TOKEN_FILE.exists():
        print(f"Loading token from {TOKEN_FILE}...")
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # 2. If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting new OAuth2 flow...")
            if not CREDENTIALS_FILE.exists():
                print(f"ERROR: Credentials file not found at {CREDENTIALS_FILE}")
                print("Please download it from Google Cloud Console and save it as google_credentials.json in the project root.")
                return

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # 3. Save the credentials for next run
        print(f"Saving token to {TOKEN_FILE}...")
        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        
        print("Done! Token saved. You can now use Google Calendar API.")

if __name__ == '__main__':
    main()
