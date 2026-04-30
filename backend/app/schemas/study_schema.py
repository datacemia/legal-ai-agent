from datetime import datetime
from typing import Any
from pydantic import BaseModel


class StudyHistoryItem(BaseModel):
    id: int
    file_name: str
    result: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True