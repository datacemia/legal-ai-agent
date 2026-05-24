from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User


def require_api_access(user: User):
    if not user.api_enabled:
        raise HTTPException(
            status_code=402,
            detail="API access is not enabled for this account.",
        )

    if not user.api_plan or user.api_plan == "none":
        raise HTTPException(
            status_code=402,
            detail="An active API plan is required.",
        )


def check_api_credits(user: User, required_credits: int):
    balance = int(user.api_credits_balance or 0)

    if balance < required_credits:
        raise HTTPException(
            status_code=402,
            detail={
                "message": "Insufficient API credits.",
                "required_credits": required_credits,
                "available_credits": balance,
            },
        )


def consume_api_credits(
    db: Session,
    user: User,
    credits: int,
):
    current_balance = int(user.api_credits_balance or 0)

    if current_balance < credits:
        raise HTTPException(
            status_code=402,
            detail={
                "message": "Insufficient API credits.",
                "required_credits": credits,
                "available_credits": current_balance,
            },
        )

    user.api_credits_balance = current_balance - credits
    db.commit()
    db.refresh(user)

    return user.api_credits_balance


def require_api_quota(
    db: Session,
    user: User,
    required_credits: int,
):
    require_api_access(user)
    check_api_credits(user, required_credits)

    return consume_api_credits(
        db=db,
        user=user,
        credits=required_credits,
    )