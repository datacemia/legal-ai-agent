from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    contract_type = Column(String, nullable=True)
    language = Column(String, nullable=True)
    status = Column(String, default="uploaded")
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)