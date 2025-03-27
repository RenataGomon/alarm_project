from bs4 import BeautifulSoup, Tag, NavigableString
import requests
import pandas as pd
from datetime import datetime, timedelta
import re
from get_and_download_hist_isw_data import save_entry_to_drive_csv

def extract_text_with_links(tag):
    result = ""
    for elem in tag.descendants:
        if elem.name == "a" and elem.has_attr("href"):
            result += elem['href'] + " "
        elif isinstance(elem, str):
            result += elem.strip() + " "
    return result.strip()

def extract_conflict_update_for_yesterday(soup):
    yesterday = datetime.today() - timedelta(days=1)
    formatted_date = yesterday.strftime("%B %d, %Y")
    heading_pattern = re.compile(r"Russian Offensive Campaign Assessment,\s*(.+)")

    headings = soup.find_all(string=heading_pattern)

    target_heading = None
    next_heading = None

    for i, heading in enumerate(headings):
        if formatted_date in heading:
            target_heading = heading
            if i + 1 < len(headings):
                next_heading = headings[i + 1]
            break

    if not target_heading:
        print(f"No report found for {formatted_date}")
        return None

    content = ""

    for elem in target_heading.find_next().next_elements:
        if elem == next_heading:
            break
        if isinstance(elem, NavigableString) and elem.strip():
            content += elem.strip() + " "
        elif isinstance(elem, Tag):
            content += extract_text_with_links(elem) + " "

    return {
        "date": yesterday.strftime("%d-%m-%Y"),
        "content": content.strip()
    }

def main():
    url = "https://understandingwar.org/backgrounder/ukraine-conflict-updates"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    update = extract_conflict_update_for_yesterday(soup)
    if not update:
        return

    csv_file = "ukraine_conflict_updates.csv"
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["date", "content"])

    if update["date"] not in df["date"].values:
        df = pd.concat([df, pd.DataFrame([update])], ignore_index=True)
        df.to_csv(csv_file, index=False)
        print(f"Report by {update['date']} is added")
        save_entry_to_drive_csv(update)
    else:
        print(f"Report by {update['date']} is already exists in CSV")

if __name__ == "__main__":
    main()
