from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=True)
    activation_token = Column(String, nullable=True)
    activation_token_expires = Column(DateTime, nullable=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)

    role = Column(String, default="user")

    plan = Column(String, default="free")

    free_analyses_used = Column(Integer, default=0)
    analysis_credits = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)