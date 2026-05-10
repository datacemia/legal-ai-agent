from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.models.organization_agent import OrganizationAgent
from app.models.organization_member import OrganizationMember
from app.models.organization_usage_log import OrganizationUsageLog
from app.models.user import User


def get_active_enterprise_membership(
    db: Session,
    user: User,
):
    return (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.user_id == user.id,
            OrganizationMember.status == "active",
        )
        .first()
    )


def get_user_enterprise_context(
    db: Session,
    user: User,
):
    membership = get_active_enterprise_membership(db, user)

    if not membership:
        return None, None

    organization = (
        db.query(Organization)
        .filter(Organization.id == membership.organization_id)
        .first()
    )

    if not organization:
        return None, None

    if getattr(organization, "status", "active") != "active":
        raise HTTPException(
            status_code=403,
            detail="Enterprise organization is suspended",
        )

    return organization, membership


def get_enabled_enterprise_agent(
    db: Session,
    organization_id: int,
    agent_slug: str,
):
    return (
        db.query(OrganizationAgent)
        .filter(
            OrganizationAgent.organization_id == organization_id,
            OrganizationAgent.agent_slug == agent_slug,
            OrganizationAgent.enabled == True,
        )
        .first()
    )


def consume_enterprise_credits(
    db: Session,
    user: User,
    agent_slug: str,
    credits_used: int,
    request_type: str = "analysis",
):
    organization, membership = get_user_enterprise_context(db, user)

    if not organization or not membership:
        return False

    organization_agent = get_enabled_enterprise_agent(
        db=db,
        organization_id=organization.id,
        agent_slug=agent_slug,
    )

    if not organization_agent:
        raise HTTPException(
            status_code=403,
            detail=f"{agent_slug} agent is not enabled for this organization",
        )

    if credits_used <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid enterprise credit cost",
        )

    if organization.credits_balance < credits_used:
        raise HTTPException(
            status_code=402,
            detail="Insufficient enterprise credits",
        )

    organization.credits_balance -= credits_used

    usage_log = OrganizationUsageLog(
        organization_id=organization.id,
        user_id=user.id,
        agent_slug=agent_slug,
        request_type=request_type,
        credits_used=credits_used,
    )

    db.add(usage_log)
    db.commit()
    db.refresh(organization)

    return {
        "access_type": "enterprise",
        "credits_used": credits_used,
        "organization_id": organization.id,
        "organization_credits_balance": organization.credits_balance,
    }
