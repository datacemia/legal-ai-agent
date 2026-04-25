from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime

from app.database import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    summary = Column(Text, nullable=True)
    clauses = Column(Text, nullable=True)
    risk_level = Column(String, nullable=True)
    risk_score = Column(Integer, nullable=True)
    simplified_version = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)