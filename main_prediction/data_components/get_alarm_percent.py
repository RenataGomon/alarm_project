import requests
import json
import pandas as pd
import os

ALERTS_API_KEY = ""

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def get_alerts():
    """Get active air alarms from alerts.in.ua"""
    url = f"https://api.alerts.in.ua/v1/alerts/active.json?token={ALERTS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise InvalidUsage(f"Error with API: {response.text}", status_code=response.status_code)


def match_region(region_name: str, active_alerts: list) -> int:
    """Match normalized region names against alerts"""
    normalized_name = region_name.replace("АР ", "").replace("область", "").strip()
    for alert_name in active_alerts:
        alert_normalized = alert_name.replace("область", "").strip()
        if normalized_name in alert_normalized or alert_normalized in normalized_name:
            return 1
    return 0


def calculate_other_regions_with_alarm_percent_by_id(region_id: int, df: pd.DataFrame) -> float:
    """Calculate % of other regions with alarm"""
    row = df[df['region_id'] == region_id]

    if row.empty:
        regions_list = "\n".join(f"{r['region_id']}: {r['region']}" for _, r in df[['region', 'region_id']].drop_duplicates().iterrows())
        raise ValueError(f"Region with ID {region_id} not found. Available regions:\n{regions_list}")

    total_regions = len(df)
    active_count = df['was_alarm'].sum()
    was_alarm = row.iloc[0]['was_alarm']

    if total_regions <= 1:
        return 0.0

    if was_alarm == 1:
        return (active_count - 1) / (total_regions - 1)
    else:
        return active_count / (total_regions - 1)


def get_other_alarm_percent(region_id: int) -> float:
    """Return percentage of other regions that currently have alarms"""

    alerts_data = get_alerts()
    active_regions = [alert["location_title"] for alert in alerts_data.get("alerts", [])]

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    regions_path = os.path.join(base_dir, "data_components", "regions.csv")

    df_regions = pd.read_csv(regions_path)

    kyiv_row = pd.DataFrame([{
        'region': 'Київ',
        'center_city_ua': 'Київ',
        'center_city_en': 'Kyiv',
        'region_alt': 'Київ',
        'region_id': 26
    }])
    df_regions = pd.concat([df_regions, kyiv_row], ignore_index=True)

    df_regions['was_alarm'] = df_regions['region'].apply(lambda r: match_region(r, active_regions))

    return calculate_other_regions_with_alarm_percent_by_id(region_id, df_regions)
