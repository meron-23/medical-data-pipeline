from .database import get_connection
from typing import List, Dict
import psycopg2.extras

def get_top_products(limit: int = 10) -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
        SELECT LOWER(unnested_word) AS product_name, COUNT(*) AS mention_count
        FROM (
            SELECT unnest(string_to_array(text, ' ')) AS unnested_word
            FROM mart.fct_messages
        ) AS words
        GROUP BY product_name
        ORDER BY mention_count DESC
        LIMIT %s;
    """
    cur.execute(query, (limit,))
    results = cur.fetchall()
    conn.close()
    return results

def get_channel_activity(channel_name: str) -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
        SELECT DATE(message_date) AS date, COUNT(*) AS message_count
        FROM mart.fct_messages
        WHERE channel_name = %s
        GROUP BY date
        ORDER BY date;
    """
    cur.execute(query, (channel_name,))
    results = cur.fetchall()
    conn.close()
    return results

def search_messages(query_str: str) -> List[Dict]:
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
        SELECT message_id, channel_name, message_date, text
        FROM mart.fct_messages
        WHERE text ILIKE %s
        LIMIT 50;
    """
    cur.execute(query, (f"%{query_str}%",))
    results = cur.fetchall()
    conn.close()
    return results
