from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False, index=True)

    # legal, finance, study, business, sentinel
    agent_slug = Column(String, nullable=False, index=True)

    # admin, trial, credits, pro, premium
    access_type = Column(String, nullable=False)

    credits_used = Column(Integer, default=0)

    # admin, trial, subscription, purchased
    credits_source = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
