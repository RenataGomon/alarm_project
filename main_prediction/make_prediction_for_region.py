import pickle
from main_prediction.get_data_for_prediction import get_data_for_prediction
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path
import main_prediction.model_utils
import types
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging

logging.basicConfig(level=logging.INFO)

SCOPES = ['https://www.googleapis.com/auth/drive.file']


def make_prediction_for_all_regions(region_ids):
    def custom_load(path):
        with open(path, "rb") as f:
            return pickle.load(f, fix_imports=True, encoding='bytes')

    sys.modules['__main__'] = types.ModuleType('__main__')
    sys.modules['__main__'].TrainedModel = main_prediction.model_utils.TrainedModel

    model_data = custom_load("models/RandomForest_model_1.pkl")
    model = model_data["model"]
    feature_names = model_data["feature_names"]

    data, isw_df = get_data_for_prediction(region_ids, feature_names)

    predictions = model.predict(data)
    metadata = model.get_metadata()

    data["prediction"] = predictions

    region_forecasts = {}
    for region_id in region_ids:
        if region_id in [1, 12]:
            forecast = {hour: 1 for hour in range(24)}
        else:
            region_data = data[data["region_id"] == region_id]
            forecast = {int(hour): int(pred) for hour, pred in zip(region_data["hour"], region_data["prediction"])}
        region_forecasts[region_id] = forecast

    return metadata, region_forecasts, isw_df


def make_prediction_for_region(region_id, isw_df=None):
    def custom_load(path):
        with open(path, "rb") as f:
            return pickle.load(f, fix_imports=True, encoding='bytes')

    sys.modules['__main__'] = types.ModuleType('__main__')
    sys.modules['__main__'].TrainedModel = main_prediction.model_utils.TrainedModel

    model_data = custom_load("models/RandomForest_model_1.pkl")

    model = model_data["model"]
    feature_names = model_data["feature_names"]

    data, isw_df = get_data_for_prediction(region_id, feature_names, isw_df)

    prediction = model.predict(data)
    metadata = model.get_metadata()

    full_forecast = {int(hour): int(pred) for hour, pred in zip(data["hour"], prediction)}

    return [metadata, full_forecast, isw_df]


def upload_to_drive(file_path, file_name):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'air-alarms-data-506614e0f8b8.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='text/csv')
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()

    print(f"File uploaded to Drive with ID: {file.get('id')}")

