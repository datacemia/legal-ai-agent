from pydantic import BaseModel
from typing import Any
from datetime import datetime


class FinanceHistoryItem(BaseModel):
    id: int
    file_name: str
    result: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True