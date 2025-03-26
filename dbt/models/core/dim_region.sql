{{ config(materialized="incremental", unique_key="region_id") }}

select
    region_id,
    max(region) as region_name,
    max(region_description) as region_description
from {{ ref("stg_traffic_data") }}
group by region_id

{% if is_incremental() %}

    where region_id not in (select distinct (region_id) from {{ this }})

{% endif %}
