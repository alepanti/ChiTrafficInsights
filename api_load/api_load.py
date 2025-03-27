import requests
import os
import csv
import pytz
from google.cloud import storage
from datetime import datetime, timezone, timedelta

# Chicago Data Portal API URL
API_URL = "https://data.cityofchicago.org/resource/kf7e-cur8.json"

GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
GCS_DEST_PATH = os.getenv('CSV_FILE_PATH')

central_tz = pytz.timezone("America/Chicago")

# Backfill configuration
backfill_start_utc = os.getenv("START_DATE") or None
backfill_end_utc = os.getenv("END_DATE") or None

since_date_utc = (datetime.now(timezone.utc) - timedelta(24))

#convert to central timezone
if backfill_start_utc is not None:
    backfill_start = datetime.strptime(backfill_start_utc, '%Y-%m-%dT%H:%M:%S.000').astimezone(central_tz).strftime("%Y-%m-%dT%H:%M:%S.000")
    backfill_end = datetime.strptime(backfill_end_utc, '%Y-%m-%dT%H:%M:%S.000').astimezone(central_tz).strftime("%Y-%m-%dT%H:%M:%S.000")
else:
    since_date = since_date_utc.astimezone(central_tz).strftime("%Y-%m-%dT%H:%M:%S.000")

# Temporary file path to store the CSV locally before uploading to GCS
TEMP_CSV_FILE = "/tmp/raw_data.csv"

def fetch_paginated_traffic_data(since_time=None, start_time=None, end_time=None):
    
    if since_time:
        url = f"https://data.cityofchicago.org/resource/kf7e-cur8.json?$where=time>'{since_time}'"
    else:
        url = f"https://data.cityofchicago.org/resource/kf7e-cur8.json?$where=time>'{start_time}' AND time<'{end_time}'"

    print(f"Fetching data from: {url}") 

    offset = 0
    limit = 1000 
    all_json_data = []

    while True:
        
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if not data:
            break

        all_json_data.extend(data)

        offset += limit

    return all_json_data

# Function to convert JSON data to CSV and upload it to GCS
def upload_to_gcs(json_data):

    fieldnames = json_data[0].keys() if json_data else []
    rowCount = 0
    with open(TEMP_CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() 
        for row in json_data:
            rowCount+=1
            writer.writerow(row)

    # Upload the file to Google Cloud Storage
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(GCS_DEST_PATH)
    blob.upload_from_filename(TEMP_CSV_FILE)
    print(f"row count: {rowCount}")
    print(f"File successfully uploaded to gs://{GCS_BUCKET_NAME}/{GCS_DEST_PATH}")

def main():
    if backfill_start_utc is None:
        json_data = fetch_paginated_traffic_data(since_time=since_date)
        print(f"Fetching data since {since_date}")
    else:
        json_data = fetch_paginated_traffic_data(start_time=backfill_start, end_time=backfill_end)
        print(f"Fetching data between {backfill_start} and {backfill_end}")

    if json_data:
        upload_to_gcs(json_data)
    else:
        print("No data retrieved. Nothing to upload.")

if __name__ == "__main__":
    main()
