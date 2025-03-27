import datetime
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
import re
import time
from bs4 import BeautifulSoup, NavigableString
import requests
from datetime import datetime


ROOT_FOLDER_ID = ""
SERVICE_ACCOUNT_FILE = ''
SCOPES = ['https://www.googleapis.com/auth/drive']


credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)


urls = [
    "https://understandingwar.org/backgrounder/ukraine-conflict-updates",
    "https://www.understandingwar.org/backgrounder/ukraine-updates-october-1-november-30-2024",
    "https://www.understandingwar.org/backgrounder/ukraine-conflict-updates-june-1-september-30-2024",
    "https://www.understandingwar.org/backgrounder/ukraine-conflicts-updates-january-2-may-31-2024",
    "https://www.understandingwar.org/ukraine-conflicts-updates-2023",
    "https://www.understandingwar.org/backgrounder/ukraine-conflict-updates-2022",
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

def extract_text_with_links(tag):
    result = ""
    for elem in tag.descendants:
        if elem.name == "a" and elem.has_attr("href"):
            result += elem['href'] + " "
        elif isinstance(elem, str):
            result += elem.strip() + " "
    return result.strip()

def get_conflict_data_from_url(soup, url):
    data = []

    heading_pattern = re.compile(
        r"Russian Offensive Campaign Assessment,?\s*"
        r"([A-Z][a-z]+ \d{1,2}, \d{4}|"
        r"\d{1,2} [A-Z][a-z]+ \d{4}|"
        r"[A-Z][a-z]+ \d{1,2})"
    )

    elements = soup.find_all(string=heading_pattern)

    for element in elements:
        heading_text = element.strip()

        date_match = re.search(
            r"([A-Z][a-z]+ \d{1,2}, \d{4}|"
            r"\d{1,2} [A-Z][a-z]+ \d{4}|"
            r"[A-Z][a-z]+ \d{1,2})",
            heading_text
        )

        if not date_match:
            print(f"Missed - date could not be recognized in: {heading_text}")
            continue

        date_str = date_match.group(1)

        parsed_date = None
        for fmt in ("%B %d, %Y", "%d %B %Y", "%B %d"):
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue

        if not parsed_date:
            print(f"Date format could not be recognized: {date_str}")
            continue

        if parsed_date.year == 1900:
            try:
                year = int(re.findall(r"\d{4}", url)[-1])
            except IndexError:
                year = datetime.today().year
            parsed_date = parsed_date.replace(year=year)

        date = parsed_date.strftime("%d-%m-%Y")

        content = ""

        next_heading = element.find_next(string=heading_pattern)

        for elem in element.next_elements:
            if elem == next_heading:
                break
            if elem == element:
                continue

            if isinstance(elem, NavigableString):
                text_piece = elem.strip()
                if text_piece:
                    content += text_piece + " "

        data.append({
            "date": date,
            "content": content.strip()
        })

    return data


def get_all_isw_data():
    all_data = []

    for url_ in urls:
        response = requests.get(url_, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        page_data = get_conflict_data_from_url(soup, url_)
        all_data.extend(page_data)

    df = pd.DataFrame(all_data)
    df.to_csv("ukraine_conflict_updates.csv", index=False)
    return df


def safe_create_or_get_folder(folder_name, parent_id=None, retries=3):
    for attempt in range(retries):
        try:
            return create_or_get_folder(folder_name, parent_id)
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    raise RuntimeError(f"Failed to create folder '{folder_name}' after {retries} attempts.")


def create_or_get_folder(folder_name, parent_id=None):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    if folders:
        return folders[0]['id']
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id] if parent_id else []
    }
    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    return folder['id']


def upload_csv_to_drive(folder_id, file_name, df):
    content = df.to_csv(index=False)
    media = MediaInMemoryUpload(content.encode(), mimetype='text/csv')

    query = f"name='{file_name}' and '{folder_id}' in parents"
    existing_files = drive_service.files().list(q=query, fields="files(id)").execute().get('files', [])

    if existing_files:
        file_id = existing_files[0]['id']
        drive_service.files().update(fileId=file_id, media_body=media).execute()
    else:
        file_metadata = {
            'name': file_name,
            'parents': [folder_id],
            'mimeType': 'text/csv'
        }
        drive_service.files().create(body=file_metadata, media_body=media).execute()


def save_entry_to_drive_csv(entry):
    date_str = entry['date']
    try:
        cleaned_date = re.match(r"\d{2}-\d{2}-\d{4}", date_str)
        if not cleaned_date:
            print(f"Unable to recognize date: '{date_str}'")
            return

        date_obj = datetime.datetime.strptime(cleaned_date.group(), "%d-%m-%Y")
    except Exception as e:
        print(f"Skipping: '{date_str}' — {e}")
        return

    year_str = str(date_obj.year)
    month_str = date_obj.strftime("%m")
    file_name = date_obj.strftime("%d-%m-%Y") + ".csv"

    try:
        year_folder_id = safe_create_or_get_folder(year_str, parent_id=ROOT_FOLDER_ID)
        month_folder_id = safe_create_or_get_folder(month_str, parent_id=year_folder_id)

        df = pd.DataFrame([entry])
        upload_csv_to_drive(month_folder_id, file_name, df)
        print(f"Downloaded: {year_str}/{month_str}/{file_name}")
        time.sleep(0.5)

    except Exception as e:
        print(f"Error during downloading '{file_name}': {e}")


def main():
    get_all_isw_data()
    df = pd.read_csv("ukraine_conflict_updates.csv")
    for _, row in df.iterrows():
        save_entry_to_drive_csv({"date": row["date"], "content": row["content"]})
        

if __name__ == "__main__":
    main()
