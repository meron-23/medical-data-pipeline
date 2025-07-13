# Ethiopian Medical Business Data Platform

An end-to-end data engineering pipeline for extracting, transforming, and analyzing insights from **Ethiopian medical Telegram channels** — built with `Telethon`, `PostgreSQL`, `dbt`, `YOLO`, and `FastAPI`.

---

## Project Goals

- Extract raw messages and media (e.g., product images) from public Telegram channels related to Ethiopian medical businesses.
- Populate a raw data lake with timestamped JSON files.
- Transform and remodel the data into a dimensional star schema using `dbt`.
- Enrich image data using object detection (`YOLO`).
- Expose clean, analytical insights via a REST API built with `FastAPI`.

---

## Tech Stack

| Layer         | Tooling                        |
|---------------|--------------------------------|
| Extraction    | `Telethon`, `Python`           |
| Storage       | Raw JSON (Data Lake)           |
| Warehouse     | `PostgreSQL`                   |
| Transformation| `dbt`                          |
| Enrichment    | `YOLOv5 / YOLOv8`              |
| API Layer     | `FastAPI`, `Uvicorn`           |
| Orchestration | `Docker`, `docker-compose`     |
| Secrets Mgmt  | `.env`, `python-dotenv`        |

---

## Project Structure
```bash
├── data/ # Data lake and images
│ └── raw/
│ ├── telegram_messages/YYYY-MM-DD/
│ └── images/YYYY-MM-DD/
├── src/
│ ├── scraping/ # Telegram scraping + image download
│ ├── transformations/ # dbt models
│ ├── object_detection/ # YOLO detection scripts
│ ├── api/ # FastAPI server
│ └── utils/ # Shared helpers
├── db/ # SQL setup scripts
├── .env # Secrets (NOT committed)
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your_username/medical-data-pipeline.git
cd medical-data-pipeline
```

### 2. Set Up .env
```bash
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=medical_data
```
### 3. Build with Docker
```bash
docker-compose up --build
```

### Cpntributors
**Meron Muluye** -Data Engineer @ Kara Solutions

