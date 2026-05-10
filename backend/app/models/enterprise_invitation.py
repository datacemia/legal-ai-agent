from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class EnterpriseInvitation(Base):
    __tablename__ = "enterprise_invitations"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False)
    email = Column(String, nullable=False, index=True)
    role = Column(String, default="member")
    token = Column(String, unique=True, nullable=False, index=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime, nullable=True)