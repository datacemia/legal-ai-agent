from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.api_key import ApiKey
from app.models.api_usage import ApiUsage
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/admin/api",
    tags=["Admin API Management"],
)


class AdminApiUserUpdate(BaseModel):
    api_enabled: bool
    api_plan: str = "none"
    api_credits_balance: int = 0


def require_admin(current_user: User):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )


@router.get("/overview")
def get_admin_api_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    api_users = (
        db.query(User)
        .filter(User.api_enabled == True)  # noqa: E712
        .count()
    )

    active_keys = (
        db.query(ApiKey)
        .filter(ApiKey.is_active == True)  # noqa: E712
        .count()
    )

    total_usage = db.query(ApiUsage).count()

    total_api_credits = sum(
        user.api_credits_balance or 0
        for user in db.query(User).all()
    )

    return {
        "api_users": api_users,
        "active_keys": active_keys,
        "total_usage": total_usage,
        "total_api_credits": total_api_credits,
    }


@router.get("/users")
def list_admin_api_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )

    return [
        {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "plan": user.plan,
            "api_enabled": user.api_enabled,
            "api_plan": user.api_plan,
            "api_credits_balance": user.api_credits_balance,
            "created_at": user.created_at,
        }
        for user in users
    ]


@router.patch("/users/{user_id}")
def update_admin_api_user(
    user_id: int,
    payload: AdminApiUserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    allowed_plans = {
        "none",
        "api_starter",
        "api_pro",
        "api_enterprise",
    }

    if payload.api_plan not in allowed_plans:
        raise HTTPException(
            status_code=400,
            detail="Invalid API plan",
        )

    if payload.api_credits_balance < 0:
        raise HTTPException(
            status_code=400,
            detail="API credits cannot be negative",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user.api_enabled = payload.api_enabled
    user.api_plan = payload.api_plan
    user.api_credits_balance = payload.api_credits_balance

    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "api_enabled": user.api_enabled,
        "api_plan": user.api_plan,
        "api_credits_balance": user.api_credits_balance,
    }


@router.get("/keys")
def list_admin_api_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    rows = (
        db.query(ApiKey, User)
        .join(User, ApiKey.user_id == User.id)
        .order_by(ApiKey.created_at.desc())
        .limit(300)
        .all()
    )

    return [
        {
            "id": api_key.id,
            "user_id": user.id,
            "email": user.email,
            "name": api_key.name,
            "key_prefix": api_key.key_prefix,
            "is_active": api_key.is_active,
            "last_used_at": api_key.last_used_at,
            "created_at": api_key.created_at,
            "revoked_at": api_key.revoked_at,
        }
        for api_key, user in rows
    ]


@router.delete("/keys/{api_key_id}")
def revoke_admin_api_key(
    api_key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    api_key = db.query(ApiKey).filter(ApiKey.id == api_key_id).first()

    if not api_key:
        raise HTTPException(
            status_code=404,
            detail="API key not found",
        )

    api_key.is_active = False

    db.commit()
    db.refresh(api_key)

    return {
        "id": api_key.id,
        "is_active": api_key.is_active,
    }


@router.get("/usage")
def list_admin_api_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    rows = (
        db.query(ApiUsage, User)
        .join(User, ApiUsage.user_id == User.id)
        .order_by(ApiUsage.created_at.desc())
        .limit(300)
        .all()
    )

    return [
        {
            "id": usage.id,
            "user_id": user.id,
            "email": user.email,
            "api_key_id": usage.api_key_id,
            "endpoint": usage.endpoint,
            "agent": usage.agent,
            "credits_used": usage.credits_used,
            "status": usage.status,
            "created_at": usage.created_at,
        }
        for usage, user in rows
    ]
