from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.contact import ContactRequest

router = APIRouter(prefix="/contact", tags=["Contact"])

@router.post("/")
def create_contact(
    full_name: str,
    email: str,
    company_name: str = "",
    company_size: str = "",
    use_case: str = "",
    db: Session = Depends(get_db),
):
    contact = ContactRequest(
        full_name=full_name,
        email=email,
        company_name=company_name,
        company_size=company_size,
        use_case=use_case,
    )

    db.add(contact)
    db.commit()

    return {"message": "Request submitted successfully"}