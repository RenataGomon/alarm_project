import datetime as dt
import json
import requests
from flask import Flask, jsonify, request

API_TOKEN = ""  # Token for authenticating API users
ALERTS_API_KEY = ""  # Token for access to the airborne alarms API

app = Flask(__name__)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {"message": self.message}

def get_alerts_for_region():
    url = f"https://api.alerts.in.ua/v1/alerts/active.json?token={ALERTS_API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise InvalidUsage(f"Error API: {response.text}", status_code=response.status_code)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/")
def home_page():
    return "<h1>Air alarm monitoring service in Ukraine</h1>"

@app.route("/content/api/v1/integration/generate", methods=["POST"])
def region_alert_endpoint():
    json_data = request.get_json()
    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("Invalid API token", status_code=403)

    start_dt = dt.datetime.now()

    alerts_data = get_alerts_for_region()

    end_dt = dt.datetime.now()

    return jsonify({
        "event_start_datetime": start_dt.isoformat(),
        "event_finished_datetime": end_dt.isoformat(),
        "event_duration": str(end_dt - start_dt),
        "alerts_data": alerts_data
    })

