from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime

from app.database import Base


class CreditTransaction(Base):
    __tablename__ = "credit_transactions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Positive for credits added, negative for credits consumed/reset if needed.
    amount = Column(Integer, nullable=False)

    # subscription, purchased, trial, admin, usage, stripe
    source = Column(String, nullable=False)

    # credit, debit, reset, refund, adjustment
    type = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    stripe_event_id = Column(String, nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
