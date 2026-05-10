import os
import ssl
import smtplib
import secrets
from datetime import datetime
from email.message import EmailMessage

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import FRONTEND_URL
from app.database import get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember
from app.models.enterprise_invitation import EnterpriseInvitation
from app.utils.security import get_current_user
from app.models.organization_usage_log import OrganizationUsageLog

router = APIRouter(prefix="/enterprise", tags=["Enterprise"])


def require_enterprise_admin(current_user: User):
    if current_user.role != "enterprise_admin":
        raise HTTPException(status_code=403, detail="Enterprise admin access required")
    return current_user


def require_enterprise_member(
    db: Session,
    current_user: User,
):
    membership = (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.user_id == current_user.id,
            OrganizationMember.status == "active",
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Enterprise membership required",
        )

    return membership


def send_enterprise_invite_email(
    to_email: str,
    organization_name: str,
    role: str,
    accept_url: str,
):
    login_url = f"{FRONTEND_URL}/login"

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("SMTP_FROM_EMAIL", smtp_user)
    from_name = os.getenv("SMTP_FROM_NAME", "Runexa")

    if not smtp_host or not smtp_user or not smtp_password:
        print("SMTP not configured. Enterprise invite:", login_url)
        return

    msg = EmailMessage()
    msg["Subject"] = f"You have been invited to {organization_name}"
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email

    msg.set_content(
        f"""
Hello,

You have been added to the Runexa enterprise workspace:

{organization_name}

Your organization role is: {role}

Accept your invitation here:

{accept_url}

If you were not expecting this invitation, you can ignore this email.
"""
    )

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print("Enterprise invite email sent to:", to_email)

    except Exception as e:
        print("SMTP ENTERPRISE INVITE ERROR:", repr(e))


@router.get("/me")
def get_enterprise_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    membership = require_enterprise_member(db, current_user)

    organization = (
        db.query(Organization)
        .filter(Organization.id == membership.organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role,
        },
        "organization": {
            "id": organization.id,
            "name": organization.name,
            "slug": organization.slug,
            "plan_name": organization.plan_name,
            "credits_balance": organization.credits_balance,
        },
        "membership": {
            "id": membership.id,
            "role": membership.role,
            "status": membership.status,
        },
    }


@router.get("/members")
def get_enterprise_members(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_enterprise_admin(current_user)

    membership = (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.user_id == current_user.id,
            OrganizationMember.status == "active",
        )
        .first()
    )

    if not membership:
        raise HTTPException(status_code=404, detail="No organization found")

    members = (
        db.query(OrganizationMember, User)
        .join(User, User.id == OrganizationMember.user_id)
        .filter(OrganizationMember.organization_id == membership.organization_id)
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


from pydantic import BaseModel


class EnterpriseInviteRequest(BaseModel):
    email: str
    role: str = "member"


class EnterpriseAcceptInviteRequest(BaseModel):
    token: str


@router.post("/invite")
def invite_enterprise_member(
    payload: EnterpriseInviteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_enterprise_admin(current_user)

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

    invite_email = payload.email.strip().lower()

    if not invite_email:
        raise HTTPException(
            status_code=400,
            detail="Email is required",
        )

    existing_user = (
        db.query(User)
        .filter(User.email == invite_email)
        .first()
    )

    # If the user already exists, make sure they are not already
    # a member of this organization.
    if existing_user:
        existing_membership = (
            db.query(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == membership.organization_id,
                OrganizationMember.user_id == existing_user.id,
            )
            .first()
        )

        if existing_membership:
            raise HTTPException(
                status_code=400,
                detail="User is already in this organization",
            )

    token = secrets.token_urlsafe(32)

    # Create an invitation even if the user account does not exist yet.
    # This allows the invited person to receive the email, create an account,
    # then accept the invitation with the same email address.
    invitation = EnterpriseInvitation(
        organization_id=membership.organization_id,
        email=invite_email,
        role=payload.role,
        token=token,
        status="pending",
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    accept_url = f"{FRONTEND_URL}/entreprises/accept?token={token}"

    organization = (
        db.query(Organization)
        .filter(Organization.id == membership.organization_id)
        .first()
    )

    send_enterprise_invite_email(
        to_email=invite_email,
        organization_name=organization.name if organization else "Runexa Enterprise",
        role=payload.role,
        accept_url=accept_url,
    )

    return {
        "success": True,
        "message": "Invitation email sent. Waiting for user acceptance.",
        "invitation_id": invitation.id,
        "email": invite_email,
    }


@router.post("/accept-invite")
def accept_enterprise_invite(
    payload: EnterpriseAcceptInviteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    invitation = (
        db.query(EnterpriseInvitation)
        .filter(
            EnterpriseInvitation.token == payload.token,
            EnterpriseInvitation.status == "pending",
        )
        .first()
    )

    if not invitation:
        raise HTTPException(status_code=404, detail="Invalid or expired invitation")

    if current_user.email.lower() != invitation.email.lower():
        raise HTTPException(
            status_code=403,
            detail="This invitation belongs to another email",
        )

    existing_membership = (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.organization_id == invitation.organization_id,
            OrganizationMember.user_id == current_user.id,
        )
        .first()
    )

    if existing_membership:
        invitation.status = "accepted"
        invitation.accepted_at = datetime.utcnow()
        db.commit()
        return {"success": True, "message": "Invitation already accepted"}

    new_member = OrganizationMember(
        organization_id=invitation.organization_id,
        user_id=current_user.id,
        role=invitation.role,
        status="active",
    )

    invitation.status = "accepted"
    invitation.accepted_at = datetime.utcnow()

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return {
        "success": True,
        "message": "Enterprise invitation accepted",
        "member_id": new_member.id,
    }


@router.get("/usage")
def get_enterprise_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    membership = require_enterprise_member(db, current_user)

    logs = (
        db.query(OrganizationUsageLog, User)
        .join(User, User.id == OrganizationUsageLog.user_id)
        .filter(OrganizationUsageLog.organization_id == membership.organization_id)
        .order_by(OrganizationUsageLog.created_at.desc())
        .limit(50)
        .all()
    )

    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "email": user.email,
            "agent_slug": log.agent_slug,
            "request_type": log.request_type,
            "credits_used": log.credits_used,
            "created_at": log.created_at,
        }
        for log, user in logs
    ]


@router.get("/usage/summary")
def get_enterprise_usage_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    membership = require_enterprise_member(db, current_user)

    logs = (
        db.query(OrganizationUsageLog)
        .filter(OrganizationUsageLog.organization_id == membership.organization_id)
        .all()
    )

    total_credits_used = sum(log.credits_used for log in logs)
    total_requests = len(logs)

    usage_by_agent = {}

    for log in logs:
        if log.agent_slug not in usage_by_agent:
            usage_by_agent[log.agent_slug] = {
                "agent_slug": log.agent_slug,
                "requests": 0,
                "credits_used": 0,
            }

        usage_by_agent[log.agent_slug]["requests"] += 1
        usage_by_agent[log.agent_slug]["credits_used"] += log.credits_used

    return {
        "total_requests": total_requests,
        "total_credits_used": total_credits_used,
        "usage_by_agent": list(usage_by_agent.values()),
    }
