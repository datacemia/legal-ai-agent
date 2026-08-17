from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class FreeAccessRequest(Base):
    __tablename__ = "free_access_requests"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    country = Column(String, nullable=False)
    agent = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)