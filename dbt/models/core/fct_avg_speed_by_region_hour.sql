{{ config(materialized="table") }}

select
    d.date,
    r.region_id,
    d.hour,
    avg(f.speed) as avg_speed
from {{ ref("fct_traffic") }} f
join {{ ref("dim_date") }} d on f.date = d.date
join {{ ref("dim_region") }} r on f.region_id = r.region_id
group by d.date, r.region_id, d.hour
