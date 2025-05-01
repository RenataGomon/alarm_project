import datetime as dt
import os
import pandas as pd

from main_prediction.get_region_id import get_region_name

from main_prediction.data_components.get_weather_forecast import get_forecast, get_weather_dataframe
from main_prediction.data_components.get_isw_vector import vectorise_isw_for_date
from main_prediction.data_components.merge_dataset_for_pediction import merge_prediction_dataset
from main_prediction.data_components.get_alarm_percent import get_other_alarm_percent

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
regions_path = os.path.join(base_dir, "main_prediction", "data_components", "regions.csv")


def get_data_for_prediction(region_ids, expected_columns, isw_df=None):
    rows = []
    full_isw_df = isw_df

    if full_isw_df is None:
        date_for_isw = (dt.datetime.today() - dt.timedelta(days=1)).strftime('%d-%m-%Y')
        full_isw_df = vectorise_isw_for_date(date_for_isw)

    if type(region_ids) == int:
        region_id_s = []
        region_id_s.append(region_ids)
        region_ids = region_id_s

    for region_id in region_ids:
        location = "Ukraine," + get_region_name(region_id)
        forecast = get_forecast(location)
        weather_df = get_weather_dataframe(forecast)
        other_alarm_percent = get_other_alarm_percent(region_id)

        if full_isw_df is None or full_isw_df.empty:
            raise ValueError(f"Missing or empty ISW dataframe for region {region_id}")

        merged_df = merge_prediction_dataset(
            region_id,
            weather_df,
            full_isw_df,
            other_alarm_percent,
            expected_columns
        )
        rows.append(merged_df)

    full_df = pd.concat(rows, ignore_index=True)

    return full_df, full_isw_df
