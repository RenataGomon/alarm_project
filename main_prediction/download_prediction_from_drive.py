from googleapiclient.http import MediaIoBaseDownload
import io

from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd

PREDICTIONS_FOLDER_ID = ""

SERVICE_ACCOUNT_FILE = '/home/ubuntu/jn/air-alarms-data-506614e0f8b8.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
PREDICTIONS_FOLDER_ID = ""

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

drive_service = build('drive', 'v3', credentials=credentials)


def download_prediction_from_drive(date_str, hour_str):
    file_name = f"pred_{date_str}_{hour_str}.csv"

    query = f"name='{file_name}' and '{PREDICTIONS_FOLDER_ID}' in parents"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print(f"No file found named {file_name} in folder {PREDICTIONS_FOLDER_ID}")
        return None

    file_id = files[0]['id']

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    fh.seek(0)
    df = pd.read_csv(fh)
    print(f"Successfully downloaded: {file_name}")

    return df
