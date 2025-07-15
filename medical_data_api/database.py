import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Load values from .env

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "medical_data"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "your_password"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )