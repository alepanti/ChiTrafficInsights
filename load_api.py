import requests
import os
import csv
from google.cloud import storage
from datetime import datetime, timezone, timedelta

# Chicago Data Portal API URL (JSON format)
API_URL = "https://data.cityofchicago.org/resource/kf7e-cur8.json"

# GCS configuration
GCS_BUCKET_NAME = 'chi-traffic-json'  # Replace with your bucket name
GCS_DEST_PATH = 'chicago_traffic_data.csv'  # Path where the file will be stored

# Backfill configuration (You can override BACKFILL_DATE with an environment variable)
BACKFILL_DATE = os.getenv("BACKFILL_DATE", "2025-03-25T15:30:00.000")
start_date = BACKFILL_DATE or (datetime.now(timezone.UTC) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.000")

# Temporary file path to store the CSV locally before uploading to GCS
TEMP_CSV_FILE = "/tmp/chicago_traffic_data.csv"

# Function to fetch paginated traffic data in JSON format
def fetch_paginated_traffic_data(since_time):
    offset = 0
    limit = 1000  # The API allows a max of 1000 rows per request
    all_json_data = []

    while True:
        print(f"Fetching data from API with offset {offset} since {since_time}")
        url = f"{API_URL}?$where=time>'{since_time}'&$limit={limit}&$offset={offset}&$order=time DESC"
        
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if not data:  # Break if there's no data
            print("DEBUG: No data received from API, stopping pagination.")
            break

        all_json_data.extend(data)  # Append the data to our list

        offset += limit  # Increment the offset for pagination

    return all_json_data  # Return the list of all JSON data

# Function to convert JSON data to CSV and upload it to GCS
def upload_to_gcs(json_data):
    # Define CSV fieldnames based on the JSON data keys
    fieldnames = json_data[0].keys() if json_data else []

    # Write CSV data to a temporary file as plain text
    with open(TEMP_CSV_FILE, mode='w', newline='') as file:  # No encoding specified, plain text
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write header row
        for row in json_data:
            writer.writerow(row)

    # Upload the file to Google Cloud Storage
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(GCS_DEST_PATH)
    blob.upload_from_filename(TEMP_CSV_FILE)

    print(f"File successfully uploaded to gs://{GCS_BUCKET_NAME}/{GCS_DEST_PATH}")

def main():
    # Start the data extraction from the given or calculated start date
    last_timestamp = BACKFILL_DATE or start_date
    print(f"Fetching data since {last_timestamp}")
    
    json_data = fetch_paginated_traffic_data(last_timestamp)

    if json_data:
        upload_to_gcs(json_data)
    else:
        print("No data retrieved. Nothing to upload.")

if __name__ == "__main__":
    main()
