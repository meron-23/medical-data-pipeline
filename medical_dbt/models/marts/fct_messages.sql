select
    s.message_id,
    s.channel_name,
    s.message_date,
    s.message_length,
    s.has_media
from {{ ref('stg_telegram_messages') }} s
