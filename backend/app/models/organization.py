from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    # public unique identifier
    slug = Column(String, unique=True, index=True, nullable=False)

    # active, suspended
    status = Column(String, default="active", nullable=False)

    # enterprise credits shared by organization
    credits_balance = Column(Integer, default=0, nullable=False)

    # enterprise, custom, etc
    plan_name = Column(String, default="enterprise", nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )
