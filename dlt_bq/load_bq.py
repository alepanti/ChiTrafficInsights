import dlt
from dlt.sources.filesystem import filesystem, read_csv


@dlt.resource(name="raw_data", write_disposition="replace")
def csv_source():
    files = filesystem()
    reader = (files | read_csv())

    
    row_count = 0
    for row in reader:
        row_count += 1
        yield row
    print(f"Total rows yielded: {row_count}")
    
pipeline = dlt.pipeline(
    pipeline_name="chicago_traffic",
    destination="bigquery",
    dataset_name="traffic_data",
)
info = pipeline.run(csv_source())
print(info)