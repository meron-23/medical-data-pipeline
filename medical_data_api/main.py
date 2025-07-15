from fastapi import FastAPI, Query
from typing import List
from .schemas import TopProduct, ChannelActivity, SearchMessage
from . import crud

app = FastAPI(
    title="Medical Business Analytics API",
    description="Answers key business questions using scraped Telegram data",
    version="1.0.0"
)

@app.get("/api/reports/top-products", response_model=List[TopProduct])
def top_products(limit: int = 10):
    return crud.get_top_products(limit)

@app.get("/api/channels/{channel_name}/activity", response_model=List[ChannelActivity])
def channel_activity(channel_name: str):
    return crud.get_channel_activity(channel_name)

@app.get("/api/search/messages", response_model=List[SearchMessage])
def search_messages(query: str = Query(..., min_length=2)):
    return crud.search_messages(query)


