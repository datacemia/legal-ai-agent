from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.organization_member import OrganizationMember
from app.models.organization_member_agent_access import OrganizationMemberAgentAccess
from app.utils.security import get_current_user


router = APIRouter(prefix="/enterprise", tags=["Enterprise Agent Access"])


ALLOWED_ENTERPRISE_AGENTS = ["legal", "study", "business"]


class MemberAgentAccessUpdate(BaseModel):
    agent_slug: str
    is_enabled: bool = True
    analysis_quota: int


def require_enterprise_admin(current_user: User):
    if current_user.role != "enterprise_admin":
        raise HTTPException(status_code=403, detail="Enterprise admin access required")


def get_admin_membership(db: Session, current_user: User):
    membership = (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.user_id == current_user.id,
            OrganizationMember.status == "active",
        )
        .first()
    )

    if not membership:
        raise HTTPException(status_code=404, detail="Organization not found")

    return membership


@router.get("/member-agent-access/{member_id}")
def get_member_agent_access(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_enterprise_admin(current_user)
    admin_membership = get_admin_membership(db, current_user)

    member = (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.id == member_id,
            OrganizationMember.organization_id == admin_membership.organization_id,
        )
        .first()
    )

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    access_rows = (
        db.query(OrganizationMemberAgentAccess)
        .filter(
            OrganizationMemberAgentAccess.organization_id == admin_membership.organization_id,
            OrganizationMemberAgentAccess.member_id == member.id,
        )
        .all()
    )

    existing_by_agent = {row.agent_slug: row for row in access_rows}

    return [
        {
            "agent_slug": agent_slug,
            "is_enabled": existing_by_agent.get(agent_slug).is_enabled
            if agent_slug in existing_by_agent
            else False,
            "analysis_quota": existing_by_agent.get(agent_slug).analysis_quota
            if agent_slug in existing_by_agent
            else 0,
            "analyses_used": existing_by_agent.get(agent_slug).analyses_used
            if agent_slug in existing_by_agent
            else 0,
        }
        for agent_slug in ALLOWED_ENTERPRISE_AGENTS
    ]


@router.patch("/member-agent-access/{member_id}")
def update_member_agent_access(
    member_id: int,
    payload: MemberAgentAccessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_enterprise_admin(current_user)
    admin_membership = get_admin_membership(db, current_user)

    if payload.agent_slug not in ALLOWED_ENTERPRISE_AGENTS:
        raise HTTPException(status_code=400, detail="Invalid enterprise agent")

    if payload.analysis_quota < 0:
        raise HTTPException(status_code=400, detail="Quota cannot be negative")

    member = (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.id == member_id,
            OrganizationMember.organization_id == admin_membership.organization_id,
        )
        .first()
    )

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    access = (
        db.query(OrganizationMemberAgentAccess)
        .filter(
            OrganizationMemberAgentAccess.organization_id == admin_membership.organization_id,
            OrganizationMemberAgentAccess.member_id == member.id,
            OrganizationMemberAgentAccess.agent_slug == payload.agent_slug,
        )
        .first()
    )

    if not access:
        access = OrganizationMemberAgentAccess(
            organization_id=admin_membership.organization_id,
            member_id=member.id,
            user_id=member.user_id,
            agent_slug=payload.agent_slug,
            is_enabled=payload.is_enabled,
            analysis_quota=payload.analysis_quota,
            analyses_used=0,
        )
        db.add(access)
    else:
        access.is_enabled = payload.is_enabled
        access.analysis_quota = payload.analysis_quota

    db.commit()
    db.refresh(access)

    return {
        "success": True,
        "member_id": member.id,
        "user_id": member.user_id,
        "agent_slug": access.agent_slug,
        "is_enabled": access.is_enabled,
        "analysis_quota": access.analysis_quota,
        "analyses_used": access.analyses_used,
    }