Contains modules for receiving, processing, and normalising meteorological and textual data from external sources. It serves as an interface between third-party APIs (Visual Crossing Weather API, Google Drive API) and local machine learning models that expect structured feature vectors.
  -**'get_alarm_percent.py'** : provides functionality to interact with the [alerts.in.ua](https://alerts.in.ua) API and compute statistics related to active air raid alerts in Ukraine.
  
  To run this code:
  1. Get your API Key from  https://alerts.in.ua
  2. Set your `ALERTS_API_KEY` at the top of the script.
  3. Ensure `regions.csv` is available in the `data_components` directory.
  4. Call `get_other_alarm_percent(region_id)` with a valid region ID

  -**'get_isw_vector.py'** : script to automatically download ISW (Institute for the Study of War) daily reports from Google Drive, preprocess the text and vectorise their content using the saved TF-IDF

  Step-by-Step Setup 
  1. Open Terminal
  2. Clone the repository:
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
  3. Install all required Python packages:
    pip install -r requirements.txt
  4. Configure API keys and Drive folder
    ID API_KEY – generated via Google Cloud Console (you must enable the Google Drive API).
    PARENT_FOLDER_ID – can be found in the URL of your Google Drive folder:https://drive.google.com/drive/folders/<PARENT_FOLDER_ID>
  5. Ensure models/vectorizer.pkl exists
This script is used as a module — you import and call a function, not run it directly.

  -**'get_weather_forecast.py'** : fetches detailed hourly and daily weather data using the Visual Crossing Weather API, transforms and standardizes the data, and returns a cleaned and optionally scaled pandas.DataFrame.

  Step-by-Step Setup:
  1. Open Terminal
  2. Clone the repository:
  git clone https://github.com/your-username/your-repo-name.git
  cd your-repo-name
  3. Install dependencies:
  pip install -r requirements.txt
  4. Configure the Weather API key
  5. Ensure models/scaler.pkl exists
  This script is used as a module — you import and call a function, not run it directly.

  -**'merge_dataset_for_prediction.py'** : prepares the final input dataset used in prediction models by merging weather data, ISW data, and region information.

