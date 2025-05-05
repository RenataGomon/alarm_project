import datetime as dt
from flask import jsonify
import pandas as pd
import pytz
from collections import defaultdict

from main_prediction.get_region_id import get_region_name

from main_prediction.make_prediction_for_region import make_prediction_for_region, make_prediction_for_all_regions

from main_prediction.download_prediction_from_drive import download_prediction_from_drive


def convert_values_to_boolean(forecast):
    return {hour: bool(value) for hour, value in forecast.items()}


def divide_forecast_by_day(forecast):
    utc = pytz.utc
    kyiv = pytz.timezone("Europe/Kyiv")

    current_hour_kyiv = dt.datetime.now(kyiv).hour

    today_forecast = {}
    tomorrow_forecast = {}

    for utc_hour, pred in forecast.items():
        utc_dt = utc.localize(dt.datetime.combine(dt.datetime.utcnow().date(), dt.time(utc_hour)))

        kyiv_hour = utc_dt.astimezone(kyiv).hour
        formatted_hour = f"{kyiv_hour:02}:00"

        if kyiv_hour >= current_hour_kyiv:
            today_forecast[formatted_hour] = pred
        else:
            tomorrow_forecast[formatted_hour] = pred

    return today_forecast, tomorrow_forecast


def format_prediction_for_one_region(region_id, for_api=True, isw_df=None):
    region_name = get_region_name(region_id)

    always_alarm_regions = [1, 12]  # 1 = Simferopol, 12 = Luhansk

    if region_id in always_alarm_regions:
        full_forecast = {hour: 1 for hour in range(24)}
        metadata = {
            "region_id": region_id,
            "note": f"{region_name} uses fallback alarm data due to constant alarm in region"
        }
    else:
        prediction_info = make_prediction_for_region(region_id, isw_df)
        metadata, full_forecast, isw_df = prediction_info

    today_forecast, tomorrow_forecast = divide_forecast_by_day(full_forecast)

    if for_api:
        today_forecast = convert_values_to_boolean(today_forecast)
        tomorrow_forecast = convert_values_to_boolean(tomorrow_forecast)

    result = {
        region_name: {
            "today": today_forecast,
            "tomorrow": tomorrow_forecast
        }
    }

    return [metadata, result, isw_df]


def get_predictions(region_id=None, location="all", date=None, file_time=None, for_api=True):
    all_region_predictions = []
    metadata = None

    if date and file_time:
        formatted_time = dt.datetime.strptime(f"{date} {file_time}", "%d-%m-%Y %H-%M")
        date = formatted_time.strftime("%d-%m-%Y")
        time_for_filename = formatted_time.strftime("%H-%M")
        time_for_sorting = formatted_time.strftime("%H:%M")

        df = download_prediction_from_drive(date, time_for_filename)
        if df is not None:
            df['hour_dt'] = pd.to_datetime(df['hour'], format='%H:%M')

            if region_id is not None:
                df = df[df['region_id'] == region_id]

            regions = defaultdict(lambda: {"today": {}, "tomorrow": {}})
            today_end_time = pd.to_datetime("23:00", format="%H:%M")
            tomorrow_start_time = pd.to_datetime("00:00", format="%H:%M")

            for region_name, group in df.groupby('region', sort=False):
                group = group.sort_values(by='hour_dt').reset_index(drop=True)

                today_hours = []
                tomorrow_hours = []

                for _, row in group.iterrows():
                    hour_str = row['hour_dt'].strftime('%H:%M')
                    prediction = bool(row['prediction'])

                    if row['hour_dt'] <= today_end_time and row['hour_dt'] >= pd.to_datetime(time_for_sorting,
                                                                                             format='%H:%M'):
                        today_hours.append((hour_str, prediction))
                    else:
                        tomorrow_hours.append((hour_str, prediction))

                today_hours_sorted = sorted(
                    today_hours,
                    key=lambda h: (
                        (pd.to_datetime(h[0], format='%H:%M') - pd.to_datetime(time_for_sorting,
                                                                               format='%H:%M')).seconds
                    )
                )

                regions[region_name]["today"] = dict(today_hours_sorted)
                regions[region_name]["tomorrow"] = dict(tomorrow_hours)

            output = [{region: data} for region, data in regions.items()]
            return jsonify({"metadata": {"file_found": True}, "regions_forecast": output})

        else:
            return jsonify({"Error": f"No file found in folder"})

    elif region_id:
        metadata, region_pred, _ = format_prediction_for_one_region(region_id, for_api=for_api)
        all_region_predictions.append(region_pred)

    elif location == "all":
        region_ids = list(range(1, 27))
        metadata, all_forecasts, isw_df = make_prediction_for_all_regions(region_ids)

        for region_id, forecast in all_forecasts.items():
            region_name = get_region_name(region_id)
            today, tomorrow = divide_forecast_by_day(forecast)

            if for_api:
                today = convert_values_to_boolean(today)
                tomorrow = convert_values_to_boolean(tomorrow)

            region_result = {
                region_name: {
                    "today": today,
                    "tomorrow": tomorrow
                }
            }
            all_region_predictions.append(region_result)


    else:
        return jsonify({"Error": "Region not found"})

    result = {
        "metadata": metadata,
        "regions_forecast": all_region_predictions
    }
    
    if for_api:
        return jsonify(result)
    else:
        return result
