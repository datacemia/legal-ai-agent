from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.api_usage import ApiUsage
from app.models.user import User


API_RATE_LIMITS_PER_MINUTE = {
    "api_starter": 10,
    "api_pro": 60,
    "api_enterprise": 300,
}


def utc_now():
    return datetime.now(UTC)


def get_api_rate_limit(user: User) -> int:
    api_plan = str(user.api_plan or "none").lower().strip()

    return API_RATE_LIMITS_PER_MINUTE.get(api_plan, 0)


def check_api_rate_limit(
    db: Session,
    user: User,
):
    limit = get_api_rate_limit(user)

    if limit <= 0:
        raise HTTPException(
            status_code=402,
            detail="An active API plan is required.",
        )

    since = utc_now() - timedelta(minutes=1)

    requests_count = (
        db.query(ApiUsage)
        .filter(
            ApiUsage.user_id == user.id,
            ApiUsage.created_at >= since,
        )
        .count()
    )

    if requests_count >= limit:
        raise HTTPException(
            status_code=429,
            detail={
                "message": "API rate limit exceeded.",
                "limit_per_minute": limit,
                "requests_last_minute": requests_count,
            },
        )

    return {
        "limit_per_minute": limit,
        "requests_last_minute": requests_count,
    }