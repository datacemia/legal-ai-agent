from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models.api_usage import ApiUsage

from app.database import get_db
from app.utils.security import get_current_user
from app.models.user import User
from app.services.api_key_service import (
    create_api_key,
    list_api_keys,
    revoke_api_key,
)


router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"],
)


class ApiKeyCreateRequest(BaseModel):
    name: str = "Default API key"


@router.post("")
def create_key(
    payload: ApiKeyCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not payload.name.strip():
        raise HTTPException(
            status_code=400,
            detail="API key name is required",
        )

    return create_api_key(
        db=db,
        user_id=current_user.id,
        name=payload.name.strip(),
    )


@router.get("")
def list_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_api_keys(
        db=db,
        user_id=current_user.id,
    )


@router.delete("/{api_key_id}")
def revoke_key(
    api_key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    revoked = revoke_api_key(
        db=db,
        user_id=current_user.id,
        api_key_id=api_key_id,
    )

    if not revoked:
        raise HTTPException(
            status_code=404,
            detail="API key not found",
        )

    return revoked

@router.get("/usage")
def get_api_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(ApiUsage)
        .filter(ApiUsage.user_id == current_user.id)
        .order_by(ApiUsage.created_at.desc())
        .limit(100)
        .all()
    )

    return [
        {
            "id": row.id,
            "api_key_id": row.api_key_id,
            "endpoint": row.endpoint,
            "agent": row.agent,
            "credits_used": row.credits_used,
            "status": row.status,
            "created_at": row.created_at,
        }
        for row in rows
    ]