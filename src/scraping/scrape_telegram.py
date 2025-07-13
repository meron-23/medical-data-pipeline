from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from pathlib import Path
import logging
import base64


load_dotenv()

# Setup logging
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = "scraper_session"

# List of channels
CHANNELS = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
    "https://t.me/CheMed123"
]

def clean_for_json(obj):
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return obj.hex()  # or base64.b64encode(obj).decode('utf-8')
    else:
        return obj
    
async def scrape_channel(client, channel_url):
    try:
        channel = await client.get_entity(channel_url)
        history = await client(GetHistoryRequest(
            peer=channel,
            limit=1000,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        raw_messages = [msg.to_dict() for msg in history.messages]
        messages = clean_for_json(raw_messages)
        today = datetime.now().strftime("%Y-%m-%d")
        channel_name = channel.username or channel.title.replace(" ", "_")
        save_dir = Path(f"../data/raw/telegram_messages/{today}")
        save_dir.mkdir(parents=True, exist_ok=True)

        file_path = save_dir / f"{channel_name}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

        logging.info(f"Scraped {len(messages)} messages from {channel_name}")

    except Exception as e:
        logging.error(f"Failed to scrape {channel_url}: {e}")

if __name__ == "__main__":
    import asyncio

    async def main():
        async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
            for url in CHANNELS:
                await scrape_channel(client, url)

    asyncio.run(main())
