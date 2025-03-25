import dlt
from dlt.sources.filesystem import filesystem, read_jsonl

filesystem_source = filesystem()
files_list = list(filesystem_source)

# Print out the files being processed (this will print all file names or data items)
print("Files being processed:", files_list)
pipeline = dlt.pipeline(
    pipeline_name="chicago_traffic",
    destination="bigquery",
    dataset_name="traffic_data",
)
load_info = pipeline.run(filesystem_source)
    
print(load_info)