In this folder lies scripts where we checked our API connections, but this scripts are unused in final project.

Scripts description:

get_weather_forecast.py - This code returns weather forecast for 24 hours in a given location. The code works with the visual crossing weather API. To get the data, user needs to insert their token and their RSA key from API to WEATHER_RSA_KEY="", and send a "Post" request from Postman using this link http://<your_server_ip>:8000/content/api/v1/integration/generate. User should pass their token and needed location in request ("Ukraine" or "Region name, Ukraine" The request returns all weather information provided by visual crossing for given location.

get_air_alarm_status.py - This code returns up-to-date information on air alerts in Ukraine. The code works with the API from this website https://devs.alerts.in.ua/ . To get the data, user needs to insert the token and their RSA API key, save this script on the server and use a Postman to get a response same as in get_weather_forecast.py file. The request returns all regions and communities where there is an alarm.

Detailed information about this file's functions can be found here: Libraries used in this script can be found at the beginning of the file. Main functions used:

extract_text_with_links() - extracts text and hyperlinks from HTML tags;
get_conflict_data_from_url() - parses the ISW HTML page and extracts report headings, dates, and content;
get_all_isw_data() - loads all ISW pages, aggregates the data, and saves them to the local ukraine_conflict_updates.csv file;
safe_create_or_get_folder() and create_or_get_folder() - are responsible for creating or finding folders on Google Drive;
upload_csv_to_drive() - uploads or updates .csv files in the appropriate folder;
save_entry_to_drive_csv() - determines the correct folder structure based on the report date and uploads the corresponding .csv file;
main() - orchestrates the entire process — it fetches ISW data and uploads each record to Google Drive.
To use the script, the user needs to:

Create a project in Google Cloud Console.
Enable the Google Drive API for the project.
Create a service account and generate a JSON key file.
Download the .json key file and provide the correct path in the SERVICE_ACCOUNT_FILE variable.
Create a root folder in Google Drive and set its ID in the ROOT_FOLDER_ID variable.
Share access to that folder with the service account’s email (found inside the JSON file).
Install the required Python packages: google-api-python-client, google-auth, pandas, requests, beautifulsoup4.
Run the script using the command: python your_script.py.
get_and_download_recent_isw_data.py - This Python script checks for and processes the most recent daily report (specifically, yesterday’s report) from the Institute for the Study of War (ISW) website. It parses the ISW updates page, searches for the report matching yesterday’s date, extracts its content, and appends it to a local CSV file (ukraine_conflict_updates.csv) if it hasn’t been saved already. The script also uploads the new entry to Google Drive in a structured folder system (year/month/date.csv) using the save_entry_to_drive_csv function (imported from get_and_download_hist_isw_data.py file).
This script is intended to be used with a cron job on a server, running automatically every day to keep the dataset up to date without manual intervention. It ensures that each report is processed and saved only once, making it ideal for automated daily archival of ISW conflict updates.
