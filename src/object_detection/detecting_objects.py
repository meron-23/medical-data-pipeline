from ultralytics import YOLO
from pathlib import Path
import json
import os
from datetime import datetime
import re
import csv

# Load YOLOv8 model (pretrained on COCO dataset)
model = YOLO("yolov8n.pt")  # lightweight version;

# Directory where images are stored
IMAGE_DIR = Path("data/raw/images")
OUTPUT_DIR = Path("data/raw/detections")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Get all image paths recursively
image_paths = list(IMAGE_DIR.rglob("*.jpg"))

print(f"Found {len(image_paths)} images to scan")

results_csv = OUTPUT_DIR / "all_detections.csv"

with open(results_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["message_id", "image_path", "class", "confidence"])

    for image_path in image_paths:
        results = model(image_path)
        detections = []

        for result in results:
            for box in result.boxes:
                confidence = float(box.conf[0])
                if confidence < 0.5:
                    continue  # skip weak detections

                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]

                # Extract message_id from image filename (e.g., msg_12345.jpg or img_00001.jpg)
                match = re.search(r"msg_(\d+)|img_(\d+)", image_path.name)
                message_id = match.group(1) or match.group(2) if match else None

                if message_id:
                    writer.writerow([message_id, str(image_path), class_name, confidence])