with date_bounds as (
    select
        min(message_date) as start_date,
        max(message_date) as end_date
    from {{ ref('stg_telegram_messages') }}
    where message_date is not null
),

dates as (
    select
        generate_series(
            date_bounds.start_date,
            date_bounds.end_date,
            make_interval(days => 1)
        ) as date
    from date_bounds
)

select
    date,
    extract(year from date) as year,
    extract(month from date) as month,
    extract(day from date) as day,
    trim(to_char(date, 'Day')) as weekday,
    to_char(date, 'YYYYMMDD') as date_key
from dates
