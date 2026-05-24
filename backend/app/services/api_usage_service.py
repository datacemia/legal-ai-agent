from sqlalchemy.orm import Session

from app.models.api_usage import ApiUsage


def record_api_usage(
    db: Session,
    user_id: int,
    endpoint: str,
    agent: str | None = None,
    credits_used: int = 0,
    status: str = "success",
    api_key_id: int | None = None,
):
    usage = ApiUsage(
        user_id=user_id,
        api_key_id=api_key_id,
        endpoint=endpoint,
        agent=agent,
        credits_used=credits_used,
        status=status,
    )

    db.add(usage)
    db.commit()
    db.refresh(usage)

    return usage