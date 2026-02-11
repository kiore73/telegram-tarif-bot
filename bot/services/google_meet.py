import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from pathlib import Path
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# Scopes needed
SCOPES = ['https://www.googleapis.com/auth/calendar']

BASE_DIR = Path(__file__).parent.parent.parent
TOKEN_FILE = BASE_DIR / 'config' / 'google_token.pickle'

@dataclass
class MeetingLink:
    url: str
    event_id: str

class GoogleMeetService:
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
                # Save refreshed token
                with open(TOKEN_FILE, 'wb') as token:
                    pickle.dump(self.creds, token)
            else:
                # If no valid token found, we can't do much automatically in a server context without interactive login
                # But here we assume set_google.py was run locally.
                # In docker, we mount the token file.
                logger.error("No valid Google token found. Run setup_google.py locally.")
                return

        self.service = build('calendar', 'v3', credentials=self.creds)

    def create_meeting(self, summary: str, description: str, start_time: datetime.datetime, duration_minutes: int = 60) -> MeetingLink | None:
        """Create a Google Meet event and return the link."""
        if not self.service:
            logger.error("Google Calendar service not initialized.")
            return None

        end_time = start_time + datetime.timedelta(minutes=duration_minutes)

        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Europe/Moscow', # Use user's timezone if possible, default to Moscow
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Europe/Moscow',
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': f"meet-{int(start_time.timestamp())}",
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                }
            },
        }

        try:
            event = self.service.events().insert(
                calendarId='primary', 
                body=event, 
                conferenceDataVersion=1
            ).execute()
            
            meet_link = event.get('hangoutLink')
            event_id = event.get('id')
            logger.info(f"Meeting created: {meet_link}")
            return MeetingLink(url=meet_link, event_id=event_id)

        except Exception as e:
            logger.error(f"Error creating meeting: {e}")
            return None

# Singleton instance
# google_meet_service = GoogleMeetService() 
# Not creating globally to avoid init on import if token missing
