from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate_sheets():
    creds = None
    if os.path.exists('token_sheets.pickle'):
        with open('token_sheets.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials_sheets.json', SCOPES_SHEETS)
        creds = flow.run_local_server(port=0)
        with open('token_sheets.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('sheets', 'v4', credentials=creds)

def insert_into_sheet(sheet_service, sheet_id, row):
    try:
        sheet_service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body={"values": [row]}
        ).execute()

        print(f"✅ Inserted: {row}")

    except Exception as e:
        print("❌ Error inserting into sheet:", e)
