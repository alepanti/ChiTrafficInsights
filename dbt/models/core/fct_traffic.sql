{{
    config(
        materialized='incremental',
        unique_key='record_id'
    )
}}

select * from {{ ref("stg_traffic_data") }}

{% if is_incremental() %}

where
  record_id not in (select record_id from {{ this }})

{% endif %}