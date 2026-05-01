from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.contact import ContactRequest

router = APIRouter(prefix="/contact", tags=["Contact"])


class ContactRequestCreate(BaseModel):
    full_name: str
    email: str
    company_name: str | None = ""
    company_size: str | None = ""
    use_case: str


# ✅ NEW: validation email entreprise
def is_business_email(email: str) -> bool:
    blocked_domains = [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "live.com",
        "icloud.com",
        "aol.com",
        "protonmail.com",
        "proton.me",
        "mail.com",
        "gmx.com",
        "yandex.com",
    ]

    domain = email.split("@")[-1].lower()
    return domain not in blocked_domains


@router.post("/")
def create_contact(
    data: ContactRequestCreate,
    db: Session = Depends(get_db),
):
    # ✅ NEW: blocage emails perso
    if not is_business_email(data.email):
        raise HTTPException(
            status_code=400,
            detail="Please use a company email address."
        )

    contact = ContactRequest(
        full_name=data.full_name,
        email=data.email,
        company_name=data.company_name,
        company_size=data.company_size,
        use_case=data.use_case,
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return {"message": "Request submitted successfully"}