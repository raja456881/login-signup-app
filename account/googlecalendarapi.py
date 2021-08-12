from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import datetime
from datetime import datetime
import pytz
from datetime import timedelta
def main(useremail=None , doctormail=None, required=None):
    print(doctormail)
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']

    start_datetime = datetime.now(tz=pytz.utc)
    flow = InstalledAppFlow.from_client_secrets_file(
        'account/token.json', SCOPES)
    creds = flow.run_local_server(port=0)
    pickle.dump(creds, open("account/token.pkl", 'wb'))
    creds = pickle.load(open("account/token.pkl", 'rb'))


    def build_service():
        service = build("calendar", "v3", credentials=creds)
        return service

    def create_event():
        service = build_service()
        start_datetime = datetime.now(tz=pytz.utc)
        event = (
            service.events()
                .insert(
                calendarId="primary",
                body={
                    "summary": required,
                    "description": "Doctor Appointment",
                    "start": {"dateTime": start_datetime.isoformat()},
                    'timeZone': 'Asia/Kolkata',
                    "end": {
                        "dateTime":(start_datetime + timedelta(minutes=45)).isoformat(),
                        'timeZone': 'Asia/Kolkata',
                    },
                    'attendees': [
                        {'email': doctormail},
                    ],
                },
            )
                .execute()
        )

        print(event)

    create_event()

