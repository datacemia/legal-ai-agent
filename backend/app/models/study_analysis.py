from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from app.database import Base


class StudyAnalysis(Base):
    __tablename__ = "study_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String, nullable=False)
    result = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class StudyAttempt(Base):
    __tablename__ = "study_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    document_hash = Column(String, nullable=True)
    language = Column(String, nullable=False)
    education_level = Column(String, nullable=False)

    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)

    weak_points = Column(JSONB, nullable=False, default=list)
    answers = Column(JSONB, nullable=False, default=list)

    created_at = Column(DateTime, default=datetime.utcnow)
