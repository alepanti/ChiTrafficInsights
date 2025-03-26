{{
    config(
        materialized='incremental',
        unique_key='record_id'
    )
}}

select * from {{ ref("stg_traffic_data") }}

{% if is_incremental() %}

where
  date > (select max(date) from {{ this }})

{% endif %}