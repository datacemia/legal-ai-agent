from datetime import UTC, datetime

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.api_key import ApiKey
from app.models.user import User
from app.services.api_key_service import hash_api_key


def utc_now():
    return datetime.now(UTC)


def extract_bearer_token(request: Request) -> str:
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    parts = authorization.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header",
        )

    return parts[1].strip()


def get_current_api_context(
    request: Request,
    db: Session = Depends(get_db),
):
    raw_key = extract_bearer_token(request)

    if not raw_key.startswith("rk_live_"):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key format",
        )

    key_hash = hash_api_key(raw_key)

    api_key = (
        db.query(ApiKey)
        .filter(
            ApiKey.key_hash == key_hash,
            ApiKey.is_active,
        )
        .first()
    )

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or revoked API key",
        )

    user = (
        db.query(User)
        .filter(User.id == api_key.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="API key user not found",
        )

    api_key.last_used_at = utc_now()
    db.commit()

    return {
        "user": user,
        "api_key": api_key,
    }


def get_current_api_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    context = get_current_api_context(
        request=request,
        db=db,
    )

    return context["user"]