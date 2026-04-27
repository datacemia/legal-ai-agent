from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class ContactRequest(Base):
    __tablename__ = "contact_requests"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    company_name = Column(String)
    company_size = Column(String)
    use_case = Column(Text, nullable=False)
    status = Column(String, default="new")
    created_at = Column(DateTime, default=datetime.utcnow)