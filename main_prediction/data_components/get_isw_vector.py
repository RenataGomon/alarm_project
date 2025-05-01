import os
import requests
import pandas as pd
import re
import io
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import bigrams
from nltk.stem import PorterStemmer
import pickle
from main_prediction.text_utils import bigram_tokenizer
from datetime import datetime, timedelta

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

API_KEY = ""
API_KEY_asya = ""
PARENT_FOLDER_ID = ""
VECTORISER_FILE_ID = ''


def search_file_by_path(path_parts, parent_id):
    if not path_parts:
        return parent_id

    query = f"'{parent_id}' in parents and trashed = false"
    url = f"https://www.googleapis.com/drive/v3/files?q={query}&key={API_KEY}&fields=files(id,name,mimeType)"

    response = requests.get(url)
    response.raise_for_status()
    files = response.json()["files"]

    next_part = path_parts[0]
    for file in files:
        if file["name"] == next_part:
            return search_file_by_path(path_parts[1:], file["id"])

    raise FileNotFoundError(f"'{next_part}' not found in folder ID {parent_id}")


def get_isw_from_drive(date_str, max_days_back=30):
    """
    Tries to download the ISW file for the given date, going back up to `max_days_back` days
    if the file isn't found.
    """
    target_date = datetime.strptime(date_str, "%d-%m-%Y")

    for _ in range(max_days_back):
        day, month, year = target_date.strftime("%d-%m-%Y").split("-")
        filename = f"{day}-{month}-{year}.csv"
        path_parts = [year, month, filename]

        try:
            file_id = search_file_by_path(path_parts, PARENT_FOLDER_ID)
            download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={API_KEY}"
            response = requests.get(download_url)
            response.raise_for_status()
            print(f"Found file for {target_date.strftime('%d-%m-%Y')}")
            return response.content
        except Exception as e:
            print(f"File not found for {target_date.strftime('%d-%m-%Y')}, trying previous day...")
            target_date -= timedelta(days=1)

    print(f"No file found within {max_days_back} days before {date_str}")
    return None


def load_vectorizer_from_models():
    current_dir = os.path.dirname(__file__)
    vectorizer_path = os.path.join(current_dir, '..', '..', 'models', 'vectorizer.pkl')
    vectorizer_path = os.path.abspath(vectorizer_path)

    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)

    return vectorizer


def vectorise_isw_for_date(date_str):
    content = get_isw_from_drive(date_str)
    if content is None:
        return None

    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        return None

    vectorizer = load_vectorizer_from_models()

    if vectorizer:
        if 'content' in df.columns:
            isw_vector = vectorizer.transform(df['content'])
            feature_names = vectorizer.get_feature_names_out()
            vectorized_df = pd.DataFrame(isw_vector.toarray(), columns=feature_names)
        else:
            vectorized_df = pd.DataFrame()
    else:
        vectorized_df = pd.DataFrame()

    return vectorized_df



