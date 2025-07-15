from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TopProduct(BaseModel):
    product_name: str
    mention_count: int

class ChannelActivity(BaseModel):
    date: datetime
    message_count: int

class SearchMessage(BaseModel):
    message_id: int
    channel_name: str
    message_date: datetime
    text: str
