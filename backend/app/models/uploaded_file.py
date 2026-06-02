from sqlalchemy import (
    Boolean,
    BigInteger,
    Column,
    DateTime,
    Integer,
    JSON,
    String,
    Text,
)

from app.database import Base


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    agent_type = Column(String(50))

    original_file_name = Column(Text)
    stored_file_name = Column(Text)
    file_path = Column(Text)

    mime_type = Column(String(150))
    file_extension = Column(String(20))
    file_size_bytes = Column(BigInteger)

    storage_backend = Column(String(50))

    extracted_text = Column(Text)
    extracted_json = Column(JSON)

    status = Column(String(50))

    consent_for_training = Column(Boolean)

    created_at = Column(DateTime)
