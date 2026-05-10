from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserResponse
from app.utils.security import require_admin
from app.models.contact import ContactRequest
from app.models.organization import Organization
from app.models.organization_agent import OrganizationAgent
from app.models.organization_member import OrganizationMember
from app.models.organization_usage_log import OrganizationUsageLog

router = APIRouter(prefix="/admin", tags=["Admin"])

VALID_ENTERPRISE_AGENTS = ["legal", "study", "finance", "business"]


class AdminEnterpriseCreateRequest(BaseModel):
    name: str
    slug: str
    owner_email: str
    credits_balance: int = 0
    plan_name: str = "enterprise"
    enabled_agents: list[str] = []


class AdminEnterpriseCreditsRequest(BaseModel):
    credits_balance: int


class AdminEnterpriseStatusRequest(BaseModel):
    status: str


class AdminEnterpriseAgentsRequest(BaseModel):
    enabled_agents: list[str]


@router.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return db.query(User).order_by(User.id.desc()).all()


@router.patch("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    if role not in ["user", "admin", "enterprise_admin", "enterprise_member"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role
    db.commit()
    db.refresh(user)

    return user


@router.patch("/users/{user_id}/credits", response_model=UserResponse)
def update_user_credits(
    user_id: int,
    credits: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.analysis_credits = credits
    db.commit()
    db.refresh(user)

    return user


@router.get("/contact-requests")
def list_contact_requests(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    requests = db.query(ContactRequest).order_by(ContactRequest.id.desc()).all()

    return [
        {
            "id": r.id,
            "full_name": r.full_name,
            "email": r.email,
            "company_name": r.company_name,
            "company_size": r.company_size,
            "use_case": r.use_case,
            "status": r.status,
            "created_at": r.created_at,
        }
        for r in requests
    ]


def normalize_agents(agent_slugs: list[str]) -> list[str]:
    cleaned = []

    for agent in agent_slugs:
        value = str(agent).lower().strip()

        if value not in VALID_ENTERPRISE_AGENTS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid enterprise agent: {agent}",
            )

        if value not in cleaned:
            cleaned.append(value)

    return cleaned


def serialize_enterprise(
    db: Session,
    organization: Organization,
):
    members = (
        db.query(OrganizationMember)
        .filter(OrganizationMember.organization_id == organization.id)
        .all()
    )

    agents = (
        db.query(OrganizationAgent)
        .filter(OrganizationAgent.organization_id == organization.id)
        .all()
    )

    usage_logs = (
        db.query(OrganizationUsageLog)
        .filter(OrganizationUsageLog.organization_id == organization.id)
        .all()
    )

    owner_membership = next(
        (member for member in members if member.role == "owner"),
        None,
    )

    owner_user = None

    if owner_membership:
        owner_user = (
            db.query(User)
            .filter(User.id == owner_membership.user_id)
            .first()
        )

    total_credits_used = sum(log.credits_used for log in usage_logs)

    return {
        "id": organization.id,
        "name": organization.name,
        "slug": organization.slug,
        "status": getattr(organization, "status", "active"),
        "plan_name": organization.plan_name,
        "credits_balance": organization.credits_balance,
        "owner_email": owner_user.email if owner_user else None,
        "members_count": len(members),
        "active_members_count": len(
            [member for member in members if member.status == "active"]
        ),
        "enabled_agents": [
            agent.agent_slug for agent in agents if agent.enabled
        ],
        "agents": [
            {
                "id": agent.id,
                "agent_slug": agent.agent_slug,
                "enabled": agent.enabled,
            }
            for agent in agents
        ],
        "total_requests": len(usage_logs),
        "total_credits_used": total_credits_used,
        "created_at": getattr(organization, "created_at", None),
    }


@router.get("/enterprises")
def list_enterprises(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    organizations = (
        db.query(Organization)
        .order_by(Organization.id.desc())
        .all()
    )

    return [
        serialize_enterprise(db, organization)
        for organization in organizations
    ]


@router.post("/enterprises")
def create_enterprise(
    payload: AdminEnterpriseCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    name = payload.name.strip()
    slug = payload.slug.strip().lower()
    owner_email = payload.owner_email.strip().lower()
    enabled_agents = normalize_agents(payload.enabled_agents)

    if not name or not slug or not owner_email:
        raise HTTPException(
            status_code=400,
            detail="Name, slug, and owner email are required",
        )

    if payload.credits_balance < 0:
        raise HTTPException(
            status_code=400,
            detail="Credits cannot be negative",
        )

    existing_org = (
        db.query(Organization)
        .filter(Organization.slug == slug)
        .first()
    )

    if existing_org:
        raise HTTPException(
            status_code=400,
            detail="Organization slug already exists",
        )

    owner = (
        db.query(User)
        .filter(User.email == owner_email)
        .first()
    )

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner user not found. Create the user account first.",
        )

    organization = Organization(
        name=name,
        slug=slug,
        credits_balance=payload.credits_balance,
        plan_name=payload.plan_name or "enterprise",
    )

    if hasattr(organization, "status"):
        organization.status = "active"

    db.add(organization)
    db.commit()
    db.refresh(organization)

    owner_membership = OrganizationMember(
        organization_id=organization.id,
        user_id=owner.id,
        role="owner",
        status="active",
    )

    owner.role = "enterprise_admin"

    db.add(owner_membership)

    for agent_slug in VALID_ENTERPRISE_AGENTS:
        db.add(
            OrganizationAgent(
                organization_id=organization.id,
                agent_slug=agent_slug,
                enabled=agent_slug in enabled_agents,
            )
        )

    db.commit()
    db.refresh(organization)

    return {
        "success": True,
        "message": "Enterprise created successfully",
        "enterprise": serialize_enterprise(db, organization),
    }


@router.get("/enterprises/{organization_id}")
def get_enterprise(
    organization_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    organization = (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    return serialize_enterprise(db, organization)


@router.patch("/enterprises/{organization_id}/credits")
def update_enterprise_credits(
    organization_id: int,
    payload: AdminEnterpriseCreditsRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    if payload.credits_balance < 0:
        raise HTTPException(
            status_code=400,
            detail="Credits cannot be negative",
        )

    organization = (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    organization.credits_balance = payload.credits_balance

    db.commit()
    db.refresh(organization)

    return {
        "success": True,
        "message": "Enterprise credits updated",
        "enterprise": serialize_enterprise(db, organization),
    }


@router.patch("/enterprises/{organization_id}/status")
def update_enterprise_status(
    organization_id: int,
    payload: AdminEnterpriseStatusRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    if payload.status not in ["active", "suspended"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    organization = (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    if not hasattr(organization, "status"):
        raise HTTPException(
            status_code=500,
            detail="Organization status column is missing. Run migration first.",
        )

    organization.status = payload.status

    db.commit()
    db.refresh(organization)

    return {
        "success": True,
        "message": "Enterprise status updated",
        "enterprise": serialize_enterprise(db, organization),
    }


@router.patch("/enterprises/{organization_id}/agents")
def update_enterprise_agents(
    organization_id: int,
    payload: AdminEnterpriseAgentsRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    enabled_agents = normalize_agents(payload.enabled_agents)

    organization = (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    existing_agents = (
        db.query(OrganizationAgent)
        .filter(OrganizationAgent.organization_id == organization_id)
        .all()
    )

    by_slug = {
        agent.agent_slug: agent
        for agent in existing_agents
    }

    for agent_slug in VALID_ENTERPRISE_AGENTS:
        if agent_slug in by_slug:
            by_slug[agent_slug].enabled = agent_slug in enabled_agents
        else:
            db.add(
                OrganizationAgent(
                    organization_id=organization_id,
                    agent_slug=agent_slug,
                    enabled=agent_slug in enabled_agents,
                )
            )

    db.commit()
    db.refresh(organization)

    return {
        "success": True,
        "message": "Enterprise agents updated",
        "enterprise": serialize_enterprise(db, organization),
    }


@router.get("/enterprises/{organization_id}/members")
def get_enterprise_members_admin(
    organization_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    organization = (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    members = (
        db.query(OrganizationMember, User)
        .join(User, User.id == OrganizationMember.user_id)
        .filter(OrganizationMember.organization_id == organization_id)
        .all()
    )

    return [
        {
            "id": member.id,
            "user_id": user.id,
            "email": user.email,
            "role": member.role,
            "status": member.status,
            "created_at": member.created_at,
        }
        for member, user in members
    ]


@router.get("/enterprises/{organization_id}/usage")
def get_enterprise_usage_admin(
    organization_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    organization = (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    logs = (
        db.query(OrganizationUsageLog, User)
        .join(User, User.id == OrganizationUsageLog.user_id)
        .filter(OrganizationUsageLog.organization_id == organization_id)
        .order_by(OrganizationUsageLog.created_at.desc())
        .limit(100)
        .all()
    )

    usage_by_agent = {}
    total_credits_used = 0

    rows = []

    for log, user in logs:
        total_credits_used += log.credits_used

        if log.agent_slug not in usage_by_agent:
            usage_by_agent[log.agent_slug] = {
                "agent_slug": log.agent_slug,
                "requests": 0,
                "credits_used": 0,
            }

        usage_by_agent[log.agent_slug]["requests"] += 1
        usage_by_agent[log.agent_slug]["credits_used"] += log.credits_used

        rows.append(
            {
                "id": log.id,
                "user_id": log.user_id,
                "email": user.email,
                "agent_slug": log.agent_slug,
                "request_type": log.request_type,
                "credits_used": log.credits_used,
                "created_at": log.created_at,
            }
        )

    return {
        "organization_id": organization.id,
        "organization_name": organization.name,
        "credits_balance": organization.credits_balance,
        "total_requests": len(logs),
        "total_credits_used": total_credits_used,
        "usage_by_agent": list(usage_by_agent.values()),
        "logs": rows,
    }
