{{
    config(
        materialized="table",
        partition_by={
            "field": "region_id",
            "data_type": "INT64",
            "range": {"start": 1, "end": 30, "interval": 1}
        },
    )
}}

select r.region_id, d.hour, avg(f.speed) as avg_speed, count(*) as data_points
from {{ ref("fct_traffic") }} f
join {{ ref("dim_date") }} d on f.date = d.date
join {{ ref("dim_region") }} r on f.region_id = r.region_id
group by 1, 2
