from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os
import googleapiclient.http

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_drive():
    creds = None
    if os.path.exists('token_drive.pickle'):
        with open('token_drive.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials_drive.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token_drive.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def list_pdfs_from_folder(service, folder_id):
    try:
        query = f"'{folder_id}' in parents and mimeType='application/pdf'"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])
        print(f"📂 Found {len(files)} PDF(s) in folder.")
        return files
    except Exception as e:
        print("❌ Failed to list PDFs:", e)
        return []

def download_pdf(service, file_id, filename):
    try:
        request = service.files().get_media(fileId=file_id)
        with open(filename, 'wb') as f:
            downloader = googleapiclient.http.MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        print(f"⬇️ Downloaded {filename}")
    except Exception as e:
        print(f"❌ Failed to download {filename}:", e)
