from fastapi import APIRouter, Depends
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


@router.post("/")
def create_contact(
    data: ContactRequestCreate,
    db: Session = Depends(get_db),
):
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