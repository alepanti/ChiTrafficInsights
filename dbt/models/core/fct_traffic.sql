{{
    config(
        materialized="incremental",
        unique_key="record_id",
        partition_by={
            "field": "date",
            "data_type": "timestamp",
            "granularity": "day",
        },
        cluster_by="region_id",
    )
}}

select record_id, region_id, date, speed
from {{ ref("stg_traffic_data") }}

{% if is_incremental() %}

    where record_id not in (select record_id from {{ this }})

{% endif %}
