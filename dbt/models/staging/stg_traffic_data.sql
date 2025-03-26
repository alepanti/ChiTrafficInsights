with
    rawdata as (
        select *, row_number() over (partition by record_id) as row_num
        from {{ source("staging", "raw_data") }}
    )
select
    -- identifiers
    record_id,
    {{ dbt.safe_cast("region_id", api.Column.translate_type("integer")) }} as region_id,

    -- timestamps
    cast(time as timestamp) as date,

    -- traffic info
    cast(speed as numeric) as speed,

    -- record estimation method
    {{ dbt.safe_cast("bus_count", api.Column.translate_type("integer")) }} as bus_count,
    {{ dbt.safe_cast("num_reads", api.Column.translate_type("integer")) }} as num_reads,

    -- location info
    region,
    description as region_description,
    cast(west as numeric) as west_long,
    cast(east as numeric) as east_long,
    cast(south as numeric) as south_lat,
    cast(north as numeric) as north_lat,
    st_geogpoint(
        cast(json_extract_scalar(nw_location, '$.coordinates[0]') as float64),
        cast(json_extract_scalar(nw_location, '$.coordinates[1]') as float64)
    ) as nw_location,
    st_geogpoint(
        cast(json_extract_scalar(se_location, '$.coordinates[0]') as float64),
        cast(json_extract_scalar(se_location, '$.coordinates[1]') as float64)
    ) as se_location,

    -- date info
    {{ dbt.safe_cast("hour", api.Column.translate_type("integer")) }} as hour,
    {{ dbt.safe_cast("day_of_week", api.Column.translate_type("integer")) }}
    as day_of_week,
    {{ get_day_of_week("day_of_week") }} as weekday,
    {{ dbt.safe_cast("month", api.Column.translate_type("integer")) }} as month,
    extract(year from time) as year

from rawdata
where row_num = 1

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var("is_test_run", default=false) %} limit 100 {% endif %}
