# Air Alarm Prediction Project
## Project description:
The goal of this project is to create and train a machine learning model to make air alert predictions in Ukraine. Our program analyses data and makes predictions about air alerts by gathering real-time data from multiple sources, including military reports, weather forecasts, air alerts, and data from Telegram channels.

This is a web-based SaaS platform deployed on an AWS EC2 instance for predicting potential air alarms in Ukraine using weather forecast, real-time air alarm status, ISW reports, and a trained machine learning model. The system offers an intuitive interface for making new predictions and retrieving past forecasts from Google Drive.

## Requirements:
All the Python dependencies required to run this project are listed in the requirements.txt file.
To install them, make sure you have Python 3 and run:
``` pip install -r requirements.txt ```


## System Capabilities 
### New Prediction:
- Select a region from a predefined list.
- View air alarm forecast for the next 24 hours.
<img width="1426" alt="Screenshot 2025-05-05 at 20 52 24" src="https://github.com/user-attachments/assets/91c34410-a638-4c4a-8764-a0e6b8f75df0" />


### Previous Prediction:
- Select region, date, and time.
- View historical prediction results retrieved from a shared Google Drive.
<img width="1422" alt="Screenshot 2025-05-05 at 21 58 12" src="https://github.com/user-attachments/assets/9c2cd036-0cf8-4041-8b40-888b26ec1848" />


## Technologies Used
- All packages in requirements.txt
- Jupyter Notebook (port :8888) — for development and model testing
- uWSGI (port :8000) — serves the production frontend interface
- RandomForestClassifier — machine learning model used for predictions
- APIs:
  - Weather data: Weather Crossing API (you need to get API key)
  - Air alarm status API from https://devs.alerts.in.ua/ (you need to get API key)
- ISW Reports — are saved on Google Drive by cron once a day (get your API key from Google Cloud Console)

## System Architecture diagram 
![IMAGE 2025-05-06 11:50:16](https://github.com/user-attachments/assets/51f2ea20-7b25-4f60-8ff2-a0adedb90d25)

## Project Structure
In our repository you can find many files that we needed at some stage of this project, but they are no longer used. In order to use our system you need to have this structure with this file names (detailed description about each file can be found in READMEs in respective folders)

```
alarm_project/
│
├── main_prediction/                               # Main folder with system architecture
│   ├── data_components                            # folder with scripts to get data for prediction
|   │   ├── get_alarm_percent.py                   # returns percent of other regions with alarm from Air Alarm API
|   │   ├── get_isw_vector.py                      # returns tf_idf vector of isw report from Drive
|   │   ├── get_weather_forecast.py                # returns weather forecast from Weather Crossing API
|   │   └── merge_dataset_for_prediction.py        # returns dataset with data listed above for model prediction
|   |   
│   ├── templates                                  # folder with html related files
|   │   ├── update_html.ipynb                      # ipynb file for updating html
|   │   └── index.html                             # html file with UI
|   |   
│   ├── all_regions_prediction.py                  # code used with cron for making and saving predictions for all regions on Drive every hour
│   ├── download_prediction_from_drive.py          # function to find and download prediction from drive
│   ├── get_data_for_prediction.py                 # returns dataframe for prediction
│   ├── get_prediction.py                          # html file with UI
│   ├── get_recent_isw.py                          # code used with cron for downloading isw report every day
│   ├── get_region_id.py                           # contaions functions to get region name from id or vica versa
│   ├── make_prediction_for_region.py              # function to make predictions for one or many regions (here our model is loaded)
│   ├── model_utils.py                             # has TrainedModel class for saving metadata and making predictions with custom probability distribution
│   ├── prediction.py                              # main file with endpoints for user to run in uwsgi command (shown in Deployment)
│   ├── regions_name_map.py                        # has region name map for consistensy in naming
│   └── text_utils.py                              # has functions needed for vectorizer
│
├── models/                                        # folder with needed pickle objects
│   ├── RandomForest_model_1.pkl                   # model for prediction
│   ├── scaler.pkl                                 # fscaler for weather data
│   └── vectorizer.pkl                             # tf_idf vectorizer for isw reports
│
├── your_google_drive_access_file.json             # file from Google Drive API for access to files
└── requirements.txt                               # Python dependencies
```

## Deployment
- EC2 Amazon Instance Setup: Ubuntu with necessary Python environment
- Jupyter Notebook accessible at http://<your-ec2-ip>:8888
- Uwsgi available at http://<your-ec2-ip>:8000

In order to run uwsgi you need to run this command in terminal:
``` uwsgi --http 0.0.0.0:8000 --wsgi-file main_prediction/prediction.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191 --harakiri 200 ```


## Installation (Local Dev)
- Set up EC2 Amazon Instance
- Connect to it via terminal and ssh
- In order to set up your server run this commands:
``` cd Downloads

sudo apt update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y

 
sudo apt-get install -y make build-essential zlib1g-dev libffi-dev libssl-dev libbz2-dev libreadline-dev libsqlite3-dev liblzma-dev libncurses-dev tk-dev
 
curl https://pyenv.run | bash
 
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
 
exec "$SHELL"

pyenv --version

pyenv global 3.8.0
 
python -V

cd /home/ubuntu

sudo apt update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y

mkdir jn

cd jn

python -m venv .venv

. .venv/bin/activate

pip install --upgrade pip
 
pip install notebook

jupyter notebook --generate-config
 
nano /home/ubuntu/.jupyter/jupyter_notebook_config.py

# Add this 4 lines below in opened file after c is determined
# The IP address the notebook server will listen on.
c.NotebookApp.ip = '0.0.0.0' # default value is 'localhost'
c.NotebookApp.open_browser = False # default value is True`
c.NotebookApp.password = u'sha1:b33024f36caa:ca337d6d6204ef502d69f8a49a915881c5e47ffa' 

jupyter notebook
```

Add requirements.txt in jupyter notebook, by opening it in browser: http://<your_ip>:8888/
then run in terminal:
```pip install -r requirements.txt```

After that you can clone our reposytory:
``` git clone https://github.com/yourusername/air-alarm-prediction.git ```
``` cd air-alarm-prediction ```
But leave only these folders: main_prediction, models (others are unnecessary as they were used on preparation stage of the project)

## Usage
Don't forget to run command in Deployment section.
Then navigate to the uwsgi at http://<your-ec2-ip>:8000
Choose between:
- New Prediction: select a region and view forecasted air alarms
- Previous Prediction: select a date/time and region to retrieve archived predictions

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
