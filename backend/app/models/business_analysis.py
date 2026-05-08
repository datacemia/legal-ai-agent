from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class BusinessAnalysis(Base):
    __tablename__ = "business_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String, nullable=False)
    result = Column(Text, nullable=False)

    access_type = Column(String, default="trial")
    credits_used = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())