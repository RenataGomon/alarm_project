Main folder with system architecture

Scripts description:

***'all_regions_prediction.py'*** - code used with cron for making and saving predictions for all regions on Drive every hour. 
upload_prediction_to_drive(folder_id, df) takes two arguments: folder_id (a string) is the identifier of the folder in Google Drive where you want to upload the file, and df (an object of type pandas.DataFrame) is the table with forecasts that will be saved in CSV format. The function does not return a value, but downloads or updates a CSV file in the specified folder on Google Drive. The file name is automatically generated in the form pred_DD-MM-YYYY_HH-00.csv, where the time is specified in the Kyiv time zone.
get_all_regions_prediction_forecast() does not take any arguments and returns an object of type pandas.DataFrame containing hourly forecasts for 26 regions of Ukraine. For each region, it calls the format_prediction_for_one_region function, processes the forecast for ‘today’ and ‘tomorrow’, generates time values in the ‘HH:00’ format (based on the fixed date ‘2025-04-30’), and adds them to the general table. As a result, a table is returned with columns: region_id (region number), region (region name), hour (time), prediction (prediction value).

***'download_prediction_from_drive.py'*** - function to find and download prediction from drive.
download_prediction_from_drive(date_str, hour_str) takes two string arguments: date_str - date in DD-MM-YYYY format, and hour_str - hour in HH-00 format. It generates a file name of the type pred_DD-MM-YYYY_HH-00.csv, and then searches for this file in the specified Google Drive folder using the API. If the file is found, the function loads it into memory using MediaIoBaseDownload, reads it into a pandas.DataFrame object, and returns this object. If the file is not found, a message is displayed and the function returns None.

***'get_data_for_prediction.py'*** - returns dataframe for prediction.
`get_data_for_prediction(region_ids, expected_columns, isw_df=None)` takes the ID of one or more regions, a list of expected columns for the model and optionally a dataframe with vectorised ISW data; returns a combined dataframe with prepared data for prediction (`full_df`) and the dataframe of ISW data that was used (`full_isw_df`).

***'get_prediction.py'*** - html file with UI.
'convert_values_to_boolean(forecast)' - takes a dictionary forecast, where the keys are hours, the values are numerical forecasts.Returns a dictionary with the same keys, where the values are converted to bool.
‘divide_forecast_by_day(forecast)’ takes a forecast dictionary with hourly forecasts in UTC hours. It returns two dictionaries: today_forecast and tomorrow_forecast, divided by Kyiv time depending on the current hour.
‘format_prediction_for_one_region(region_id, for_api=True, isw_df=None)’ takes a region ID, the for_api flag (or return a bool value), and an optional ISW dataframe. It returns a list of three elements: metadata (information about the region), result (forecast in the form of a dictionary with the keys ‘today’ and ‘tomorrow’), and isw_df (the dataframe used).
‘get_predictions(region_id=None, location=’all‘, date=None, file_time=None, for_api=True)’ function accepts optional parameters: Region ID (region_id), location name or ‘all’ (location), date (date), file_time (file_time) and for_api flag. Returns a JSON object with forecasts or an error message. If the date and time are passed, it downloads the forecast from Google Drive. Otherwise, it calculates the forecast for one or all regions in real time.

***'get_recent_isw.py'*** - code used with cron for downloading isw report every day.
‘extract_text_with_links(tag)’ takes: tag (type bs4.element.Tag) - HTML tag to be processed.Returns: str - text containing all text elements from the tag, as well as links from <a> tags.
‘get_conflict_data_from_url(soup, url)’ takes: soup (BeautifulSoup type) - the parsed HTML code of the page to search for headers and content and url (str type) - the URL of the page from which the data is taken. Returns: list of dict - a list of dictionaries, each containing a ‘date’ (str type) and ‘content’ (str type) for each entry.
‘get_all_isw_data()’ does not accept anything: DataFrame - a merged DataFrame with data obtained from both web pages and manual records.
‘safe_create_or_get_folder(folder_name, parent_id=None, retries=3)’ takes: folder_name (type str) - the name of the folder to be created or retrieved. parent_id (type str, default None) - the ID of the parent folder, if any.
‘retries (int type, default 3)’ - the number of attempts to create/retrieve the folder. Returns: str - ID of the found or created folder.
‘save_missing_dates(df, dates_list)’ takes : df (type DataFrame) - DataFrame with updates, dates_list (type list of str) - a list of dates for which updates should be saved if they are not in the DataFrame.Returns: nothing. (Saves files to Google Drive).
‘create_or_get_folder(folder_name, parent_id=None)’  takes: folder_name (type str) - the name of the folder to be created or found, parent_id (type str, default None) - the ID of the parent folder, if any. Returns: str - ID of the found or created folder.
‘upload_csv_to_drive(folder_id, file_name, df)’ takes: folder_id (str type) - ID of the folder on Google Drive where you want to upload CSV, file_name (str type) - name of the file to upload, df (DataFrame type) - DataFrame to upload as CSV. Returns: nothing.
‘save_yesterday_entry(df)’ takes: df (DataFrame type) - DataFrame with updates. Returns: nothing (Saves data for yesterday's date to Google Drive).
‘save_full_csv(df)’ takes: df (DataFrame type) - DataFrame with all updates.  Returns: null (Saves the entire CSV to Google Drive).

***'get_region_id.py'*** - ontaions functions to get region name from id or vica versa.
‘get_region_id(location_name)’ takes: location_name (str) - the name of the region or locality. Returns: region_id (type str or None) - region ID if the location name is found in region_map. If the name is not found, None is returned.
‘get_region_name(region_id)’ takes: region_id (type str) - region ID. Returns: region_name (type str or None) - the name of the region corresponding to the passed ID, or None if such an ID does not exist in the region_map.

***'make_prediction_for_region.py'*** - function to make predictions for one or many regions (here our model is loaded).
'make_prediction_for_all_regions(region_ids)' takes: region_ids (list type): a list of region IDs for which you want to make a prediction. Returns: metadata (dict type): model-specific metadata obtained using the model's get_metadata() method, region_forecasts (dict type): a dictionary forecast for each region, where the key is the region ID and the value is the forecast for each hour (from 0 to 23), isw_df (DataFrame type):  DataFrame containing the data used for the forecast.
‘make_prediction_for_region(region_id, isw_df=None)’ takes: region_id (int type): ID of the region for which you want to make a prediction, isw_df (DataFrame type, default None): additional data that can be used for the prediction.  Returns: metadata (dict type): metadata related to the model, full_forecast (dict type): forecast for each hour for the specified region, isw_df (DataFrame type): the same ISW data used for forecasting.
‘upload_to_drive(file_path, file_name)’ takes: file_path (type str): the path to the file to be uploaded to Google Drive, file_name (type str): the file name that will be used when uploading to Google Drive.  Returns: None.

***'model_utils.py'*** - has TrainedModel class for saving metadata and making predictions with custom probability distribution.
class TrainedModel
‘__init__(self, model)’ takes: model (type: object): a machine learning model (e.g. RandomForest, LogisticRegression, etc.). Returns: None.
‘predict(self, X)’ takes: X (type: ndarray or DataFrame): the input data for prediction (can be in the form of a feature matrix). Returns: preds (type: ndarray): an array of predictions for each observation in X (value 0 or 1), depending on the probability exceeding the threshold of 0.78.
‘get_metadata(self)’ takes: Nothing. Returns: metadata (type: dict): a dictionary containing metadata about the model: last_model_train_time (type: str): the time when the model was trained and last_prediction_time (type: str): the time of the last prediction, or a message about the lack of a prediction.

***'prediction.py'*** - main file with endpoints for user to run in uwsgi command (shown in Deployment).
‘home_page()’ takes: HTTP GET request to /. Returns the HTML page index.html with an empty forecast
‘get_forecast_from_ui()’ takes: HTTP POST request from the form (fields: location, mode, date, time). Returns an HTML page with the forecast or an error message
‘weather_endpoint()’ takes: JSON (fields: token, location, date, time) via POST request to /content/api/v1/integration/generate. Returns JSON response with weather forecast or error (400/403)
‘handle_invalid_usage(error)’ takes : an InvalidUsage error object. Returns: JSON with the error message and the corresponding HTTP status.
‘InvalidUsage(Exception)’ takes: message, status_code (optional), payload (optional). Returns: an exception object with the to_dict() method → a dictionary with an error message.

***'regions_name_map.py'*** - as region name map for consistensy in naming.

***'text_utils.py'*** - has functions needed for vectorizer.
‘remove_stemmed_phrases(tokens, phrase_list)’ takes: tokens - a list of words after stemming, phrase_list - a list of phrases to be removed (also in stemmed form). Returns: A list of tokens without unwanted phrases.
‘clean_and_stem(text)’ takes: text - raw text. Returns: list of cleaned and stemmed tokens (words).
‘bigram_tokenizer(text)’ takes: text - raw text. Returns: list of bigrams (pairs of consecutive words) as strings.
