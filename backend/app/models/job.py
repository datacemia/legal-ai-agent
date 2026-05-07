from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    job_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")

    input = Column(JSON, nullable=False, default=dict)
    result = Column(JSON, nullable=True)

    error = Column(Text, nullable=True)
    attempts = Column(Integer, nullable=False, default=0)

    progress = Column(Integer, nullable=False, default=0)
    status_message = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)