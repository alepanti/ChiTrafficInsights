import json
import gzip
file_path = "chicago_traffic_data_chicago_traffic_1742592009.509649.3ed3430e9f.jsonl"

with gzip.open(file_path, "rt", encoding="utf-8") as f:
    for _ in range(5):  # Read first 5 lines
        print(json.loads(f.readline().strip()))
