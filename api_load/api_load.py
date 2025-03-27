import requests
import os
import csv
from google.cloud import storage
from datetime import datetime, timezone, timedelta

# Chicago Data Portal API URL (CSV format)
API_URL = "https://data.cityofchicago.org/resource/kf7e-cur8.json"

GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
GCS_DEST_PATH = os.getenv('CSV_FILE_PATH')

# Backfill configuration
BACKFILL_DATE = os.getenv("BACKFILL_DATE", "2025-01-01T00:00:00.000")
start_date = BACKFILL_DATE or (datetime.now(timezone.UTC) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.000")

# Temporary file path to store the CSV locally before uploading to GCS
TEMP_CSV_FILE = "/tmp/raw_data.csv"

def fetch_paginated_traffic_data(since_time):
    offset = 0
    limit = 1000 
    all_json_data = []

    print(f"Fetching data from API")
    while True:

        url = f"{API_URL}?$where=time>'{since_time}'&$limit={limit}&$offset={offset}&$order=time DESC"
        
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
    last_timestamp = BACKFILL_DATE or start_date
    print(f"Fetching data since {last_timestamp}")
    
    json_data = fetch_paginated_traffic_data(last_timestamp)

    if json_data:
        upload_to_gcs(json_data)
    else:
        print("No data retrieved. Nothing to upload.")

if __name__ == "__main__":
    main()
