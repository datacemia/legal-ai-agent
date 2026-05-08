from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)

    activation_token = Column(String, nullable=True)
    activation_token_expires = Column(DateTime, nullable=True)

    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)

    last_verification_email_sent_at = Column(DateTime, nullable=True)
    last_reset_email_sent_at = Column(DateTime, nullable=True)

    role = Column(String, default="user")

    # Global subscription plan:
    # trial, paid, pro, premium
    plan = Column(String, default="trial")

    # Global credits usable across all operational agents
    credits_balance = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)