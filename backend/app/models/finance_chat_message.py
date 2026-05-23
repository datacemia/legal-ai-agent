from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class FinanceChatMessage(Base):
    __tablename__ = "finance_chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    analysis_id = Column(
        Integer,
        ForeignKey("finance_analyses.id"),
        nullable=False,
        index=True,
    )

    role = Column(
        Text,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )