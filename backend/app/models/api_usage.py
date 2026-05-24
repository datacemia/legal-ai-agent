from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class ApiUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"), nullable=True)

    endpoint = Column(String, nullable=False)
    agent = Column(String, nullable=True)

    credits_used = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default="success")

    created_at = Column(DateTime, server_default=func.now())