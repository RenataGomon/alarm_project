import datetime
import pandas as pd
import requests
import re
import time
from bs4 import BeautifulSoup, NavigableString
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

ROOT_FOLDER_ID = ""
SERVICE_ACCOUNT_FILE = '/home/ubuntu/jn/air-alarms-data-506614e0f8b8.json'
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

manual_entries = [
    {
        "date": "26-02-2022",
        "content": "Institute for the Study of War, Russia Team. February 26, 3:00 pm EST. Russian forces’ main axes of advance in the last 24 hours focused on Kyiv, northeastern Ukraine, and southern Ukraine. Russian airborne and special forces troops are engaged in urban warfare in northwestern Kyiv, but Russian mechanized forces are not yet in the capital. Russian forces from Crimea have changed their primary axes of advance from a presumed drive toward Odesa to focus on pushing north toward Zaporizhie and the southeastern bend of the Dnipro River and east along the Azov Sea coast toward Mariupol. These advances risk cutting off the large concentrations of Ukrainian forces still defending the former line of contact between unoccupied Ukraine and occupied Donbas. Ukrainian leaders may soon face the painful decision of ordering the withdrawal of those forces and the ceding of more of eastern Ukraine or allowing much of Ukraine’s uncommitted conventional combat power to be encircled and destroyed. There are no indications as yet of whether the Ukrainian government is considering this decision point. Ukrainian resistance remains remarkably effective and Russian operations especially on the Kyiv axis have been poorly coordinated and executed, leading to significant Russian failures on that axis and at Kharkiv. Russian forces remain much larger and more capable than Ukraine’s conventional military, however, and Russian advances in southern Ukraine may threaten to unhinge the defense of Kyiv and northeastern Ukraine if they continue unchecked. Key Takeaways: Russia has failed to encircle and isolate Kyiv with the combination of mechanized and airborne attacks as it had clearly planned to do. Russian forces are now engaging in more straightforward mechanized drives into the capital along a narrow front along the west bank of the Dnipro River and toward Kyiv from a broad front to the northeast. Russian forces have temporarily abandoned failed efforts to seize Chernihiv and Kharkiv to the northeast and east of Kyiv and are bypassing those cities to continue their drive on Kyiv. Russian attacks against both cities appear to have been poorly designed and executed and to have encountered more determined and effective Ukrainian resistance than they expected. Russian movements in eastern Ukraine remain primarily focused on pinning the large concentration of Ukrainian conventional forces arrayed along the former line of contact in the east, likely to prevent them from interfering with Russian drives on Kyiv and to facilitate their encirclement and destruction. Russian forces coming north from Crimea halted their drive westward toward Odesa, and Ukrainian forces have retaken the critical city of Kherson. Some Russian troops remain west of the Dnipro River and are advancing on Mikolayiv, but the main axes of advance have shifted to the north and east toward Zaporizhie and Mariupol respectively. Russian forces have taken the critical city of Berdyansk from the west, threatening to encircle Mariupol even as Russian forces based in occupied Donbas attack Mariupol from the east, likely to pin defenders in the city as they are encircled. Russian successes in southern Ukraine are the most dangerous and threaten to unhinge Ukraine’s successful defenses and rearguard actions to the north and northeast. Russian troops are facing growing morale and logistics issues, predictable consequences of the poor planning, coordination, and execution of attacks along Ukraine’s northern border."
    }
   ,
    {
        "date": "25-02-2022",
        "content": "Institute for the Study of War, Russia Team. February 25, 3:00 pm EST. Russian forces entered major Ukrainian cities—including Kyiv and Kherson—for the first time on February 25. Russian forces’ main axes of advance focused on Kyiv (successfully isolating the city on both banks of the Dnipro River). Russian military operations along Ukraine’s northern border have been less well-planned, organized, and conducted than those emanating from Crimea. They have also been less successful so far. The divergence in performance likely arises in part from differences in the composition and organization of the Russian ground forces elements in the Western Military District and Belarus (to Ukraine’s north) and Southern Military District and Black Sea Fleet (to its south and east), as ISW has previously observed. Determined and well-organized Ukrainian resistance around Kyiv and Kharkiv has also played an important role in preventing the Russian military from advancing with the speed and success for which it had reportedly planned. The Russian military has deployed additional forces to southeastern Belarus, likely beyond those Moscow had planned to use against Ukraine, to offset these problems and challenges. Russian forces remain much larger and more capable than Ukraine’s conventional military, however. Russia will likely defeat Ukrainian regular military forces and secure their territorial objectives at some point in the coming days or weeks if Putin is determined to do so and willing to pay the cost in blood and treasure. Key Takeaways: Russian forces entered the outskirts of Kyiv on the west bank of the Dnipro on February 25. Russian sabotage groups in civilian clothes are reportedly active in downtown Kyiv. Russian forces have so far failed to enter Kyiv’s eastern outskirts. Ukrainian forces have successfully slowed Russian troops, which have temporarily abandoned the failed attempt to take the city of Chernihiv and are instead bypassing it. Elements of the Russian 76th VDV (Airborne) division have concentrated in southeastern Belarus likely for use along the Chernihiv-bypass axis toward Kyiv in the next 24 hours. Russian forces will likely envelop Kharkhiv in the next 24 hours after failing to enter the city through frontal assaults on February 24. Russian forces have achieved little success on frontal assaults or envelopments against Ukrainian forces in Donbas but may not have intended to do more than pin Ukrainian forces in the east. North of Crimea, Russian forces fully captured Kherson and are likely on the verge of seizing Melitopol in the east. Unconfirmed reports indicate that Russian forces had bypassed Kherson earlier and headed directly for Mykolaiv and Odessa. Russian forces may be assembling in Stolin, Belarus, to open a new line of advance against Rivne in western Ukraine."
    },
    {
        "date": "24-02-2022",
        "content": "Mason Clark, George Barros, and Kateryna Stepanenko. February 24, 3:00 pm EST. Russian President Vladimir Putin began a large-scale invasion of Ukraine on February 24 likely aimed at full regime change and the occupation of Ukraine. His claimed objective to “demilitarize” and “de-nazify” Ukraine is a transparent cover for an unprovoked war of aggression to occupy a neighboring state. Putin and Kremlin media continue to deny that the Russian invasion is a war, instead describing it as a special military operation. Putin’s messaging is likely aimed at a domestic Russian audience, which the Kremlin has not fully prepared for the costs of a war against Ukraine. Russian officials and state media have been denying and mocking Western warnings of the impending Russian invasion for months and as recently as February 23. Russian forces remain much larger and more capable than Ukraine’s conventional military. Russia will likely defeat Ukrainian regular military forces and secure their territorial objectives at some point in the coming days or weeks if Putin is determined to do so and willing to pay the cost in blood and treasure. Key Takeaways: Ukrainian forces are successfully slowing Russian offensives on all axes of advance other than a Russian breakout from the Crimean Peninsula. Russian failure to ground the Ukrainian air force or cripple Ukrainian command and control is likely enabling these initial Ukrainian successes. Ukrainian forces are contesting the Hostomel military airport, 20 km northwest of Kyiv, as of 9:30 pm local time. Russian VDV (Airborne) troops landed at Hostomel and have also failed to capture the Boryspil airport southeast of Kyiv. Ukraine’s contestation of the airport deprives Russian forces of any location to airlift forces onto Kyiv’s western flank overnight. Russian forces are rapidly advancing north from Crimea, securing Kherson city. Their deepest penetration to date is about 60 kilometers. Russian forces are advancing on Kyiv from Belarus on both sides of the Dnipro River. Russian forces secured the Chernobyl Exclusion Zone (on the west bank) at 7:30 pm local time, but Ukrainian forces have slowed Russian advances east of the Dnipro at Chernihiv. Russian forces likely seek to cut off Ukrainian troops on the line of contact in Donbas using an envelopment behind the Ukrainian front lines through Luhansk Oblast. Russian frontal assaults have taken little territory in Donetsk and Luhansk at this time. Russian military operations began with a short and incomplete air campaign on February 24 around 4:00 am local time targeting Ukrainian air defenses, supply depots, and airfields across unoccupied Ukraine. However, portions of the Ukrainian Air Force remain operational and Ukrainian command and control appears intact. US defense officials estimate initial strikes comprised over 100 missiles including a mix of short and medium-range ballistic missiles, cruise missiles, and sea-launched missiles. An estimated 75 Russian bombers participated in the attack. Russia did not successfully ground the Ukrainian air force or cripple the Ukrainian armed forces, enabling several Ukrainian successes on February 24. ISW incorrectly forecasted that any Russian offensive would begin with a concentrated air and missile campaign to cripple Ukrainian command and control and infrastructure. The Russian failure to comprehensively strike key Ukrainian assets is a surprising break from expected Russian operations and has likely enabled stiffer Ukrainian defense. The Ukrainian military has shot down seven Russian aircraft and seven helicopters as of 8:00 pm local time, February 24. Russia has not demonstrated its full air and missile capabilities and will likely conduct further waves of strikes in the coming days aimed at degrading Ukraine’s command and control and ability to redeploy forces."
    }
]

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

    heading_pattern = re.compile(r"Russian Offensive Campaign Assessment,?\s*"
                                 r"([A-Z][a-z]+ \d{1,2}, \d{4}|"
                                 r"\d{1,2} [A-Z][a-z]+ \d{4}|"
                                 r"[A-Z][a-z]+ \d{1,2})")

    elements = soup.find_all(string=heading_pattern)

    for element in elements:
        heading_text = element.strip()
        date_match = re.search(r"([A-Z][a-z]+ \d{1,2}, \d{4}|"
                               r"\d{1,2} [A-Z][a-z]+ \d{4}|"
                               r"[A-Z][a-z]+ \d{1,2})", heading_text)

        if not date_match:
            continue

        date_str = date_match.group(1)
        parsed_date = None
        for fmt in ("%B %d, %Y", "%d %B %Y", "%B %d"):
            try:
                parsed_date = datetime.datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        if not parsed_date:
            continue

        if parsed_date.year == 1900:
            try:
                year = int(re.findall(r"\d{4}", url)[-1])
            except IndexError:
                year = datetime.datetime.today().year
            parsed_date = parsed_date.replace(year=year)

        date = parsed_date.strftime("%d-%m-%Y")
        next_heading = element.find_next(string=heading_pattern)

        content = ""
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
        all_data.extend(get_conflict_data_from_url(soup, url_))
    df_url = pd.DataFrame(all_data)
    manual_df = pd.DataFrame(manual_entries)
    df = pd.concat([df_url, manual_df], ignore_index=True)
    return df


# === Google Drive ===
def safe_create_or_get_folder(folder_name, parent_id=None, retries=3):
    for attempt in range(retries):
        try:
            return create_or_get_folder(folder_name, parent_id)
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    raise RuntimeError(f"Failed to create folder '{folder_name}'")


def save_missing_dates(df, dates_list):
    for target_date in dates_list:
        entry = df[df["date"] == target_date]
        if entry.empty:
            print(f"Missing: {target_date} — not found in data")
            continue

        row = entry.iloc[0]
        date_obj = datetime.datetime.strptime(target_date, "%d-%m-%Y")
        year_str = date_obj.strftime("%Y")
        month_str = date_obj.strftime("%m")
        day_str = date_obj.strftime("%d")

        file_name = f"{day_str}-{month_str}-{year_str}.csv"

        year_folder_id = safe_create_or_get_folder(year_str, parent_id=ROOT_FOLDER_ID)
        month_folder_id = safe_create_or_get_folder(month_str, parent_id=year_folder_id)

        upload_csv_to_drive(month_folder_id, file_name, pd.DataFrame([row]))
        print(f"Uploaded: {year_str}/{month_str}/{file_name}")



def create_or_get_folder(folder_name, parent_id=None):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = drive_service.files().list(q=query, fields="files(id)").execute()
    folders = results.get('files', [])
    if folders:
        return folders[0]['id']
    metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id] if parent_id else []
    }
    folder = drive_service.files().create(body=metadata, fields='id').execute()
    return folder['id']


def upload_csv_to_drive(folder_id, file_name, df):
    content = df.to_csv(index=False)
    media = MediaInMemoryUpload(content.encode(), mimetype='text/csv')
    query = f"name='{file_name}' and '{folder_id}' in parents"
    existing = drive_service.files().list(q=query, fields="files(id)").execute().get('files', [])
    if existing:
        drive_service.files().update(fileId=existing[0]['id'], media_body=media).execute()
    else:
        metadata = {
            'name': file_name,
            'parents': [folder_id],
            'mimeType': 'text/csv'
        }
        drive_service.files().create(body=metadata, media_body=media).execute()


def save_yesterday_entry(df):
    yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%d-%m-%Y")
    entry = df[df["date"] == yesterday]
    if entry.empty:
        print("No update for yesterday.")
        return

    row = entry.iloc[0]
    date_obj = datetime.datetime.strptime(row['date'], "%d-%m-%Y")
    year_str = date_obj.strftime("%Y")
    month_str = date_obj.strftime("%m")
    day_str = date_obj.strftime("%d")

    file_name = f"{day_str}-{month_str}-{year_str}.csv"

    year_folder_id = safe_create_or_get_folder(year_str, parent_id=ROOT_FOLDER_ID)
    month_folder_id = safe_create_or_get_folder(month_str, parent_id=year_folder_id)

    upload_csv_to_drive(month_folder_id, file_name, pd.DataFrame([row]))

    print(f"Saved yesterday’s update to: {year_str}/{month_str}/{file_name}")


def save_full_csv(df):
    base_folder_id = safe_create_or_get_folder("air_alarms_project_data_team5", parent_id=ROOT_FOLDER_ID)
    upload_csv_to_drive(base_folder_id, "ukraine_conflict_updates.csv", df)
    print("Saved full CSV to Google Drive")


def main():
    df = get_all_isw_data()
    save_full_csv(df)
    save_yesterday_entry(df)


if __name__ == "__main__":
    main()
