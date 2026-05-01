from pydantic import BaseModel
from datetime import datetime
from typing import Any


class BusinessHistoryItem(BaseModel):
    id: int
    file_name: str
    result: Any
    created_at: datetime

    class Config:
        from_attributes = True