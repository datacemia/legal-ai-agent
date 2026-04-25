from datetime import datetime
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    file_name: str
    file_type: str
    contract_type: str | None = None
    language: str | None = None
    status: str
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True