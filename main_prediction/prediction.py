import datetime as dt
from flask import Flask, jsonify, request, render_template
import logging
from main_prediction.get_region_id import get_region_id
from main_prediction.get_prediction import get_predictions

logging.basicConfig(level=logging.INFO)

API_TOKEN = ""

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


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# UI home page
@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html", forecast={}, error=None)


# UI forecast form submission
@app.route("/get_forecast", methods=["POST"])
def get_forecast_from_ui():
    location = request.form.get("location")
    mode = request.form.get("mode")
    date = request.form.get("date")
    time = request.form.get("time")

    if not location:
        return render_template("index.html", error="Please select a location.")

    try:
        if location == "all":
            region_id = None
        else:
            region_id = int(location)

        if mode == "previous":
            if not date or not time:
                return render_template("index.html",
                                       error="Please provide both date and time for previous predictions.")

            formatted_date = dt.datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
            formatted_time = dt.datetime.strptime(time, "%H:%M").strftime("%H-00")

            response = get_predictions(region_id=region_id, location=location, date=formatted_date,
                                       file_time=formatted_time)
            data = response.get_json()

            if not data or "regions_forecast" not in data:
                return render_template("index.html", error="Couldn't find prediction for the given date and time.")

        else:
            response = get_predictions(region_id=region_id, location=location)
            data = response.get_json()

        regions_forecast = data.get("regions_forecast", [])

        merged_forecast = {}
        for region_dict in regions_forecast:
            merged_forecast.update(region_dict)

        now = dt.datetime.now().strftime("%Y-%m-%d")

        return render_template("index.html", forecast=merged_forecast, now=now)

    except Exception as e:
        return render_template("index.html", error=str(e))


# API endpoint for tools like Postman
@app.route("/content/api/v1/integration/generate", methods=["POST"])
def weather_endpoint():
    json_data = request.get_json()
    required_info = ["token", "location"]

    for field in required_info:
        if json_data.get(field) is None:
            raise InvalidUsage(f"{field} is required", status_code=400)

    token = json_data.get("token")
    location = json_data.get("location")
    date = json_data.get("date")
    time = json_data.get("time")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    region_id = get_region_id(location)
    response = get_predictions(region_id=region_id, location=location, date=date, file_time=time, for_api=True)
    return response


if __name__ == "__main__":
    app.run(debug=True)
