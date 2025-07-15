-- Fail if any message has length < 1
select *
from {{ ref('stg_telegram_messages') }}
where length(text) < 1
