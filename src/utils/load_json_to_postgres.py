import os
import json
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

DATA_DIR = "data/raw/telegram_messages"
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host="localhost",
    port=5432
)

def load_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def insert_message(cur, message, channel_name):
    cur.execute("""
        INSERT INTO raw.telegram_messages (message_id, channel, date, text, has_media)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (
        message.get("id"),
        channel_name,
        message.get("date"),
        message.get("message"),
        "media" in message
    ))

cur = conn.cursor()

for date_folder in os.listdir(DATA_DIR):
    folder_path = os.path.join(DATA_DIR, date_folder)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".json"):
                channel_name = file.replace(".json", "")
                full_path = os.path.join(folder_path, file)
                print(f"Inserting: {full_path}")
                messages = load_json_file(full_path)
                for msg in messages:
                    insert_message(cur, msg, channel_name)

conn.commit()
cur.close()
conn.close()
