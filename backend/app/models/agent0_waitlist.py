from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime

from app.database import Base


class Agent0Waitlist(Base):
    __tablename__ = "agent0_waitlist"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    country = Column(String, nullable=True)
    profile = Column(String, nullable=True)
    interest_level = Column(String, nullable=True)
    protect_target = Column(String, nullable=True)
    message = Column(Text, nullable=True)

    consent = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)