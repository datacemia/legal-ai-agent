from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    job_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")

    input = Column(JSONB, nullable=False, default=dict)
    result = Column(JSONB, nullable=True)

    error = Column(Text, nullable=True)
    attempts = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, server_default=func.now())
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)