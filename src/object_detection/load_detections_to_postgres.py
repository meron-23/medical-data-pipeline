import csv
import psycopg2

DETECTIONS_CSV = "data/raw/detections/all_detections.csv"

conn = psycopg2.connect(
    dbname="medical_data",
    user="postgres",
    password="meronyeyenekonjo24",
    host="localhost",
    port=5432
)
cur = conn.cursor()

with open(DETECTIONS_CSV, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("""
            INSERT INTO mart.fct_image_detections (message_id, image_path, detected_class, confidence_score)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (
            int(row["message_id"]),
            row["image_path"],
            row["class"],
            float(row["confidence"])
        ))

conn.commit()
cur.close()
conn.close()

print("All detections loaded into PostgreSQL.")
