import dlt
import requests
import os
from datetime import datetime, UTC, timedelta

# Chicago Data Portal API
API_URL = "https://data.cityofchicago.org/resource/kf7e-cur8.json"

# backfill
BACKFILL_DATE = os.getenv("BACKFILL_DATE", None)
# batch load last day
start_date = BACKFILL_DATE or (datetime.now(UTC) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.000")

def get_api_url(since_time):
    return f"{API_URL}?$where=time>'{since_time}'"

# Fetch data in batches of 1000
@dlt.resource(name="chicago_traffic", write_disposition="append")
def fetch_traffic_data(pipeline):

    last_timestamp = BACKFILL_DATE or start_date
    offset = 0
    limit = 1000  # API allows a max of 1000 rows per request
    print(last_timestamp)
    while True:
        # Construct paginated API URL
        url = f"{API_URL}?$where=time>'{last_timestamp}'&$limit={limit}&$offset={offset}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data:
            break

        print("Sample row:", data[0]) # debugging
        print(f"DEBUG: Extracted {len(data)} rows (Offset: {offset})")  # Debugging output

        yield from data

        offset += limit

pipeline = dlt.pipeline(
    pipeline_name="chit_pipeline",
    destination="filesystem",
    dataset_name="chicago_traffic_data",
)

load_info = pipeline.run(fetch_traffic_data(pipeline))

print(f"Load Info: {load_info}")
