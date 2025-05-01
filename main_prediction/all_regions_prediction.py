import datetime as dt

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
import pandas as pd
import pytz
from main_prediction.get_prediction import divide_forecast_by_day, convert_values_to_boolean, format_prediction_for_one_region

PREDICTIONS_FOLDER_ID = ""

SERVICE_ACCOUNT_FILE = '/home/ubuntu/jn/main_prediction/air-alarms-data-506614e0f8b8.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
PREDICTIONS_FOLDER_ID = ""

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

drive_service = build('drive', 'v3', credentials=credentials)


def upload_prediction_to_drive(folder_id, df):
    kyiv_time = dt.datetime.now(pytz.timezone('Europe/Kyiv'))
    file_name = f"pred_{kyiv_time.strftime('%d-%m-%Y_%H')}-00.csv"

    content = df.to_csv(index=False)
    media = MediaInMemoryUpload(content.encode(), mimetype='text/csv')

    query = f"name='{file_name}' and '{folder_id}' in parents"
    existing_files = drive_service.files().list(q=query, fields="files(id)").execute().get('files', [])

    if existing_files:
        file_id = existing_files[0]['id']
        drive_service.files().update(fileId=file_id, media_body=media).execute()
    else:
        file_metadata = {
            'name': file_name,
            'parents': [folder_id],
            'mimeType': 'text/csv'
        }
        drive_service.files().create(body=file_metadata, media_body=media).execute()


def get_all_regions_prediction_forecast():

    all_predictions = []
    utc = pytz.utc
    dummy_date = "2025-04-30"

    isw_df = None

    for r_id in range(1, 27):
        try:
            if isw_df is None:
                metadata, region_pred, isw_df = format_prediction_for_one_region(r_id, for_api=False)
            else:
                metadata, region_pred, _ = format_prediction_for_one_region(r_id, for_api=False, isw_df=isw_df)

            region_name = list(region_pred.keys())[0]

            for day_part in ("today", "tomorrow"):
                for hour, pred in region_pred[region_name][day_part].items():
                    utc_dt = utc.localize(dt.datetime.strptime(f"{dummy_date} {hour}", "%Y-%m-%d %H:%M"))
                    kyiv_hour_str = utc_dt.strftime("%H:00")

                    all_predictions.append({
                        "region_id": r_id,
                        "region": region_name,
                        "hour": kyiv_hour_str,
                        "prediction": pred
                    })

        except Exception as e:
            print(f"Error for region {r_id}: {e}")

    return pd.DataFrame(all_predictions)


upload_prediction_to_drive(PREDICTIONS_FOLDER_ID, get_all_regions_prediction_forecast())

