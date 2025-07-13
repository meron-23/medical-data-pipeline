from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from telethon.tl.functions.messages import GetHistoryRequest
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime
import logging

load_dotenv()

logging.basicConfig(
    filename="image_scraper.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = "scraper_session"

CHANNELS = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/CheMed123"
]

async def download_images(client, channel_url):
    try:
        entity = await client.get_entity(channel_url)
        channel_name = entity.username or entity.title.replace(" ", "_")
        today = datetime.now().strftime("%Y-%m-%d")
        save_path = Path(f"data/raw/images/{today}/{channel_name}")
        save_path.mkdir(parents=True, exist_ok=True)

        messages = await client(GetHistoryRequest(
            peer=entity,
            limit=1000,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        count = 0
        for msg in messages.messages:
            if msg.media and isinstance(msg.media, MessageMediaPhoto):
                filename = save_path / f"img_{count:05d}.jpg"
                await client.download_media(msg, file=filename)
                logging.info(f"Downloaded {filename}")
                count += 1

        logging.info(f"Downloaded {count} images from {channel_name}")

    except Exception as e:
        logging.error(f"Failed to download images from {channel_url}: {e}")

if __name__ == "__main__":
    import asyncio

    async def main():
        async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
            for url in CHANNELS:
                await download_images(client, url)

    asyncio.run(main())
