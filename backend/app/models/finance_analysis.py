from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime

from app.database import Base


class FinanceAnalysis(Base):
    __tablename__ = "finance_analyses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    file_name = Column(String, nullable=False)

    result = Column(Text, nullable=False)

    # optional billing metadata
    access_type = Column(String, default="trial")
    credits_used = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)