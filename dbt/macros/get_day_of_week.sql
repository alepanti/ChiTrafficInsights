{#
    Return day of week
#}

{% macro get_day_of_week(day_of_week) %}
    case cast( {{ day_of_week}} as integer)
        when 1 then 'Sunday'
        when 2 then 'Monday'
        when 3 then 'Tuesday'
        when 4 then 'Wednesday'
        when 5 then 'Thursday'
        when 6 then 'Friday'
        when 7 then 'Saturday'
        else 'Empty'
    end
{%- endmacro %}