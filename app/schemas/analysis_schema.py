from datetime import datetime
from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    id: int
    document_id: int
    summary: str | None = None
    clauses: str | None = None
    risk_level: str | None = None
    risk_score: int | None = None
    simplified_version: str | None = None
    recommendations: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True