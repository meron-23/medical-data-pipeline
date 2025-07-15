with raw as (
    select *
    from raw.telegram_messages
)

select
    message_id,
    channel as channel_name,
    date as message_date,
    text,
    has_media,
    length(text) as message_length
from raw
