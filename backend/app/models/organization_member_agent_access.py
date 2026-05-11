from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
)
from sqlalchemy.sql import func

from app.database import Base


class OrganizationMemberAgentAccess(Base):
    __tablename__ = "organization_member_agent_access"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
    )

    member_id = Column(
        Integer,
        ForeignKey("organization_members.id"),
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    agent_slug = Column(
        String,
        nullable=False,
    )

    is_enabled = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    analysis_quota = Column(
        Integer,
        default=0,
        nullable=False,
    )

    analyses_used = Column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )