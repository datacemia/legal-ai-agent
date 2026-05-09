from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.agent0_waitlist import Agent0Waitlist
from app.models.user import User
from app.utils.security import get_current_user


router = APIRouter(prefix="/agent0-waitlist", tags=["Agent 0 Waitlist"])


class Agent0WaitlistCreate(BaseModel):
    full_name: str
    email: EmailStr
    country: str | None = None
    profile: str | None = None
    interest_level: str | None = None
    protect_target: str | None = None
    message: str | None = None
    consent: bool = True


@router.post("/")
def create_agent0_waitlist_entry(
    payload: Agent0WaitlistCreate,
    db: Session = Depends(get_db),
):
    entry = Agent0Waitlist(
        full_name=payload.full_name,
        email=payload.email,
        country=payload.country,
        profile=payload.profile,
        interest_level=payload.interest_level,
        protect_target=payload.protect_target,
        message=payload.message,
        consent=payload.consent,
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {
        "saved": True,
        "id": entry.id,
    }


@router.get("/")
def list_agent0_waitlist_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    return (
        db.query(Agent0Waitlist)
        .order_by(Agent0Waitlist.id.desc())
        .all()
    )