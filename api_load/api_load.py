import requests
import os
import csv
import pytz
from google.cloud import storage
from datetime import datetime, timezone, timedelta
import time

API_URL = "https://data.cityofchicago.org/resource/kf7e-cur8.csv"

GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
GCS_DEST_PATH = os.getenv('CSV_FILE_PATH')

central_tz = pytz.timezone("America/Chicago")

start_utc = os.getenv("START_DATE") or None
end_utc = os.getenv("END_DATE") or None

start_date = datetime.strptime(start_utc, '%Y-%m-%dT%H:%M:%S.000').astimezone(central_tz).strftime("%Y-%m-%dT%H:%M:%S.000")
end_date = datetime.strptime(end_utc, '%Y-%m-%dT%H:%M:%S.000').astimezone(central_tz).strftime("%Y-%m-%dT%H:%M:%S.000")


TEMP_CSV_FILE = "/tmp/raw_data.csv"

def get_headers():
    """Fetch and return the CSV headers from the API"""
    header_url = f"{API_URL}?$limit=1"
    print(f"Fetching headers from: {header_url}")
    response = requests.get(header_url, stream=True)
    response.raise_for_status()
    header_reader = csv.reader(response.iter_lines(decode_unicode=True))
    return next(header_reader)

def fetch_paginated_traffic_data(headers):
    """Fetch data rows"""
    offset = 0
    limit = 1000
    all_csv_rows = []

    while True:
        url = f"{API_URL}?$where=time>'{start_date}' AND time<'{end_date}'&$limit={limit}&$offset={offset}"
        
        response = requests.get(url, stream=True)
        response.raise_for_status()

        lines = response.iter_lines(decode_unicode=True)
        reader = csv.reader(lines)
        next(reader)
        batch_rows = list(reader)
        
        if not batch_rows:
            break

        all_csv_rows.extend(batch_rows)
        offset += len(batch_rows)
        time.sleep(3)
    
    return all_csv_rows

def upload_to_gcs(headers, csv_rows):
    """Upload CSV to GCS"""
    row_count = 0
    with open(TEMP_CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in csv_rows:
            row_count += 1
            writer.writerow(row)

    # Upload to GCS
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(GCS_DEST_PATH)
    blob.upload_from_filename(TEMP_CSV_FILE)
    print(f"Row count: {row_count}")
    print(f"File successfully uploaded to gs://{GCS_BUCKET_NAME}/{GCS_DEST_PATH}")

def main():
    try:
        # First get headers
        headers = get_headers()
        
        print(f"Fetching data between {start_date} and {end_date}")

        # Then fetch data
        csv_data = fetch_paginated_traffic_data(headers)
        
        if csv_data:
            upload_to_gcs(headers, csv_data)
        else:
            print("No data retrieved. Nothing to upload.")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()