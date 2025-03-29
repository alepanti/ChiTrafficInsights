{{
    config(
        materialized="incremental",
        unique_key="date",
        partition_by={
            "field": "date",
            "data_type": "timestamp",
            "granularity": "month",
        },
        cluster_by=["weekday", "hour"],
    )
}}

select distinct (date), hour, day_of_week, weekday, month, year
from {{ ref("stg_traffic_data") }}

{% if is_incremental() %} where date not in (select date from {{ this }}) {% endif %}
