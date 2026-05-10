from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.models.organization_member import OrganizationMember
from app.models.organization_usage_log import OrganizationUsageLog
from app.models.user import User


def consume_enterprise_credits(
    db: Session,
    user: User,
    agent_slug: str,
    credits_used: int,
    request_type: str = "analysis",
):
    membership = (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.user_id == user.id,
            OrganizationMember.status == "active",
        )
        .first()
    )

    if not membership:
        return False

    organization = (
        db.query(Organization)
        .filter(Organization.id == membership.organization_id)
        .first()
    )

    if not organization:
        return False

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

    return True