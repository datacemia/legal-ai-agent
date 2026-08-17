from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.free_access_request import FreeAccessRequest


router = APIRouter(
    prefix="/free-access-request",
    tags=["Free Access"],
)


class FreeAccessRequestCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    country: str
    agent: str


@router.post("/")
def create_free_access_request(
    data: FreeAccessRequestCreate,
    db: Session = Depends(get_db),
):
    first_name = data.first_name.strip()
    last_name = data.last_name.strip()
    email = data.email.strip().lower()
    country = data.country.strip()
    agent = data.agent.strip()

    if not first_name:
        raise HTTPException(
            status_code=400,
            detail="First name is required.",
        )

    if not last_name:
        raise HTTPException(
            status_code=400,
            detail="Last name is required.",
        )

    if not email or "@" not in email:
        raise HTTPException(
            status_code=400,
            detail="A valid email address is required.",
        )

    if not country:
        raise HTTPException(
            status_code=400,
            detail="Country is required.",
        )

    if not agent:
        raise HTTPException(
            status_code=400,
            detail="Agent is required.",
        )

    existing_request = (
        db.query(FreeAccessRequest)
        .filter(FreeAccessRequest.email == email)
        .first()
    )

    if existing_request:
        raise HTTPException(
            status_code=400,
            detail="A free access request already exists for this email address.",
        )

    request = FreeAccessRequest(
        first_name=first_name,
        last_name=last_name,
        email=email,
        country=country,
        agent=agent,
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    return {
        "message": "Free access request submitted successfully."
    }