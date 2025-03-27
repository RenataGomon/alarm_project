import datetime as dt
import json
import requests
from flask import Flask, jsonify, request

API_TOKEN = ""
WEATHER_RSA_KEY = ""

app = Flask(__name__)


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

def check_date(date_str: str):
    try:
        dt.date.fromisoformat(date_str)
        return True
    except ValueError:
        return False


def convert_f_to_c(fahrenheit: float):
    return float(fahrenheit - 32) * 5 / 9


def get_weather(location: str, date1: str):
    url_base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    date2 = (dt.datetime.strptime(date1, '%Y-%m-%d') + dt.timedelta(1)).strftime('%Y-%m-%d')
    
    url = f"{url_base_url}/{location}/{date1}/{date2}?key={WEATHER_RSA_KEY}"

    headers = {"X-Api-Key": WEATHER_RSA_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    else:
        raise InvalidUsage(response.text, status_code=response.status_code)

def get_forecast(location: str):
    today = dt.datetime.utcnow()
    time_start = today.strftime('%H')
    
    weather = get_weather(location, today.strftime('%Y-%m-%d'))

    today_hourly_information = weather.get("days")[0].get("hours")
    tomorrow_hourly_information = weather.get("days")[1].get("hours")
    
    forecast = []
    for hour in today_hourly_information:
        if int(hour.get("datetime")[:2]) >= int(time_start[:2]):
            forecast.append(hour)
    
    for hour in tomorrow_hourly_information:
        if int(hour.get("datetime")[:2]) < int(time_start[:2]):
            forecast.append(hour)
            
    return forecast

    
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>KMA H2: air alarm prediction Saas.</h2></p>"


@app.route("/content/api/v1/integration/generate", methods=["POST"])
def weather_endpoint():
    json_data = request.get_json()

    required_info = ["token", "location"]
    
    for field in required_info:
        if json_data.get(field) is None:
            raise InvalidUsage(f"{field} is required", status_code=400)

    token = json_data.get("token")
    location = json_data.get("location")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    forecast = get_forecast(location)
    timestamp = dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    result = {
        "location": location,
        "timmestamp": timestamp,
        "weather_forcast_for_24_h": forecast
        }
    

    return jsonify(result)
