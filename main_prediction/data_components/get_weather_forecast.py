import datetime as dt
import json
import requests
import pandas as pd
import os
import pickle
import joblib
import pytz

WEATHER_RSA_KEY = ""


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def convert_f_to_c(fahrenheit: float):
    return round((fahrenheit - 32) * 5 / 9, 1)


def get_weather(location: str, date1: str):
    url_base = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    date2 = (dt.datetime.strptime(date1, '%Y-%m-%d') + dt.timedelta(1)).strftime('%Y-%m-%d')
    url = f"{url_base}/{location}/{date1}/{date2}?key={WEATHER_RSA_KEY}"
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    else:
        raise InvalidUsage(response.text, status_code=response.status_code)


def get_forecast(location: str):
    today = dt.datetime.utcnow()
    time_start = today.strftime('%H')

    weather = get_weather(location, today.strftime('%Y-%m-%d'))

    today_day = weather.get("days")[0]
    today_hourly = today_day.get("hours")

    tomorrow_day = weather.get("days")[1]
    tomorrow_hourly = tomorrow_day.get("hours")

    forecast = []

    for hour in today_hourly:
        if int(hour.get("datetime")[:2]) >= int(time_start):
            forecast.append({
                **extract_day_info(today_day),
                **extract_hour_info(hour)
            })

    for hour in tomorrow_hourly:
        if int(hour.get("datetime")[:2]) < int(time_start):
            forecast.append({
                **extract_day_info(tomorrow_day),
                **extract_hour_info(hour)
            })

    return forecast


def extract_day_info(day: dict) -> dict:
    return {
        'day_datetime': day.get('datetime'),
        'day_datetimeEpoch': day.get('datetimeEpoch'),
        'day_tempmax': convert_f_to_c(day.get('tempmax')),
        'day_tempmin': convert_f_to_c(day.get('tempmin')),
        'day_dew': day.get('dew'),
        'day_humidity': day.get('humidity'),
        'day_precip': day.get('precip'),
        'day_windspeed': day.get('windspeed'),
        'day_pressure': day.get('pressure'),
        'day_cloudcover': day.get('cloudcover'),
        'day_visibility': day.get('visibility'),
        'day_solarenergy': day.get('solarenergy'),
        'day_moonphase': day.get('moonphase')
    }


def extract_hour_info(hour: dict) -> dict:
    return {
        'hour_datetime': hour.get('datetime'),
        'hour_datetimeEpoch': hour.get('datetimeEpoch'),
        'hour_temp': convert_f_to_c(hour.get('temp')),
        'hour_humidity': hour.get('humidity'),
        'hour_dew': hour.get('dew'),
        'hour_precip': hour.get('precip'),
        'hour_snow': hour.get('snow'),
        'hour_snowdepth': hour.get('snowdepth'),
        'hour_windgust': hour.get('windgust'),
        'hour_windspeed': hour.get('windspeed'),
        'hour_winddir': hour.get('winddir'),
        'hour_pressure': hour.get('pressure'),
        'hour_visibility': hour.get('visibility'),
        'hour_cloudcover': hour.get('cloudcover'),
        'hour_solarradiation': hour.get('solarradiation'),
        'hour_solarenergy': hour.get('solarenergy')
    }


def load_scaler_from_models():
    current_dir = os.path.dirname(__file__)
    scaler_path = os.path.join(current_dir, '..', '..', 'models', 'scaler.pkl')
    scaler_path = os.path.abspath(scaler_path)

    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    return scaler


def get_weather_dataframe(weather_data):
    df = pd.DataFrame(weather_data)

    desired_columns = [
        'day_datetime', 'day_datetimeEpoch', 'day_tempmax', 'day_tempmin', 'day_dew',
        'day_humidity', 'day_precip', 'day_windspeed', 'day_pressure', 'day_cloudcover',
        'day_visibility', 'day_solarenergy', 'day_moonphase',
        'hour_datetime', 'hour_datetimeEpoch', 'hour_temp', 'hour_humidity', 'hour_dew',
        'hour_precip', 'hour_snow', 'hour_snowdepth', 'hour_windgust', 'hour_windspeed',
        'hour_winddir', 'hour_pressure', 'hour_visibility', 'hour_cloudcover',
        'hour_solarradiation', 'hour_solarenergy'
    ]

    df = df[[col for col in desired_columns if col in df.columns]]

    utc = pytz.utc
    kyiv = pytz.timezone("Europe/Kyiv")

    df['hour'] = pd.to_datetime(df['hour_datetime'], format='%H:%M:%S').apply(
        lambda x: utc.localize(dt.datetime.combine(dt.datetime.utcnow().date(), x.time()))
        .astimezone(kyiv)
        .hour
    )

    df = df.drop(columns=['day_datetime', 'hour_datetime', 'date'], errors='ignore')

    columns_to_scale = [
        'day_tempmax', 'day_tempmin',
        'day_dew', 'day_humidity', 'day_precip', 'day_windspeed',
        'day_pressure', 'day_cloudcover', 'day_visibility', 'day_solarenergy',
        'day_moonphase', 'hour_temp', 'hour_datetimeEpoch',
        'hour_humidity', 'hour_dew', 'hour_precip', 'hour_snow',
        'hour_snowdepth', 'hour_windgust', 'hour_windspeed', 'hour_winddir',
        'hour_pressure', 'hour_visibility', 'hour_cloudcover',
        'hour_solarradiation', 'hour_solarenergy'
    ]

    scaler = load_scaler_from_models()

    if scaler:
        scaled_values = scaler.transform(df[columns_to_scale])
        df[columns_to_scale] = scaled_values
    else:
        df = pd.DataFrame()

    return df