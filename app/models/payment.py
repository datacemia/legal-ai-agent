from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stripe_customer_id = Column(String, nullable=True)
    plan = Column(String, default="free")
    status = Column(String, default="inactive")
    created_at = Column(DateTime, default=datetime.utcnow)