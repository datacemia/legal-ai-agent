import hashlib
import secrets
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.api_key import ApiKey


API_KEY_PREFIX = "rk_live"


def utc_now():
    return datetime.now(UTC)


def hash_api_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def generate_api_key() -> str:
    token = secrets.token_urlsafe(32)
    return f"{API_KEY_PREFIX}_{token}"


def create_api_key(
    db: Session,
    user_id: int,
    name: str,
):
    raw_key = generate_api_key()
    key_hash = hash_api_key(raw_key)
    key_prefix = raw_key[:16]

    api_key = ApiKey(
        user_id=user_id,
        name=name,
        key_prefix=key_prefix,
        key_hash=key_hash,
        is_active=True,
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return {
        "id": api_key.id,
        "name": api_key.name,
        "key_prefix": api_key.key_prefix,
        "api_key": raw_key,
        "created_at": api_key.created_at,
    }


def list_api_keys(
    db: Session,
    user_id: int,
):
    keys = (
        db.query(ApiKey)
        .filter(ApiKey.user_id == user_id)
        .order_by(ApiKey.created_at.desc())
        .all()
    )

    return [
        {
            "id": key.id,
            "name": key.name,
            "key_prefix": key.key_prefix,
            "is_active": key.is_active,
            "last_used_at": key.last_used_at,
            "created_at": key.created_at,
            "revoked_at": key.revoked_at,
        }
        for key in keys
    ]


def revoke_api_key(
    db: Session,
    user_id: int,
    api_key_id: int,
):
    api_key = (
        db.query(ApiKey)
        .filter(
            ApiKey.id == api_key_id,
            ApiKey.user_id == user_id,
        )
        .first()
    )

    if not api_key:
        return None

    api_key.is_active = False
    api_key.revoked_at = utc_now()

    db.commit()
    db.refresh(api_key)

    return {
        "id": api_key.id,
        "name": api_key.name,
        "key_prefix": api_key.key_prefix,
        "is_active": api_key.is_active,
        "revoked_at": api_key.revoked_at,
    }