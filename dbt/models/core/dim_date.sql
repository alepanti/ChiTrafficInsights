{{ config(materialized="incremental", unique_key="date") }}

select DISTINCT(date), hour, day_of_week, weekday, month, year
from {{ ref("stg_traffic_data") }}

{% if is_incremental() %} where date not in (select date from {{ this }}) {% endif %}
