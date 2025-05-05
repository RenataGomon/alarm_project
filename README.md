# Air Alarm Prediction Project
## Project description:
The goal of this project is to create and train a machine learning model to make air alert predictions in Ukraine. Our program analyses data and makes predictions about air alerts by gathering real-time data from multiple sources, including military reports, weather forecasts, air alerts, and data from Telegram channels.

This is a web-based SaaS platform deployed on an AWS EC2 instance for predicting potential air alarms in Ukraine using weather forecast, real-time air alarm status, ISW reports, and a trained machine learning model. The system offers an intuitive interface for making new predictions and retrieving past forecasts from Google Drive.

## Requirements:
All the Python dependencies required to run this project are listed in the requirements.txt file.
To install them, make sure you have Python 3 and run:
``` pip install -r requirements.txt ```


## Features
### New Prediction:
- Select a region from a predefined list.
- View air alarm forecast for the next 24 hours.
### Previous Prediction:
- Select region, date, and time.
- View historical prediction results retrieved from a shared Google Drive.


## Technologies Used
- All packages in requirements.txt
- Jupyter Notebook (port :8888) — for development and model testing
- uWSGI (port :8000) — serves the production frontend interface
- RandomForestClassifier — machine learning model used for predictions
- APIs:
  - Weather data: Weather Crossing API
  - Air alarm status API
- ISW Reports — are saved on Google Drive by cron once a day

## System Architecture diagram 

## Project Structure

## Deployment
- EC2 Amazon Instance Setup: Ubuntu with necessary Python environment
- Jupyter Notebook accessible at http://<your-ec2-ip>:8888
- Production Web App available at http://<your-ec2-ip>:8000

In order to run uwsgi you need to run this command in terminal:
``` uwsgi --http 0.0.0.0:8000 --wsgi-file main_prediction/prediction.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191 --harakiri 200 ```


## Installation (Local Dev)
Clone the repository:
``` git clone https://github.com/yourusername/air-alarm-prediction.git
cd air-alarm-prediction ```
Leave only these folders: main_prediction, models (others are unnecessary as they were used on preparation stage of the project)

## Usage
Navigate to the web app at http://<your-ec2-ip>:8000
Choose between:
New Prediction: select a region and view forecasted air alarms
Previous Prediction: select a date/time and region to retrieve archived predictions

## Model
Trained using RandomForestClassifier
Input features include:
Weather forecast for region with dayly data and hourly data
Percent of other regions with alarm
Vectorised ISW report for previous day

## Authors
Team of 4 2nd year bachelor's Applied Mathematics students, National University of Kyiv-Mohyla Academy:
Renata Gomon, Anastasiia Konstantynovska, Daria Zasko, Khrystyna Skulysh

## License
This project is for academic use only.
