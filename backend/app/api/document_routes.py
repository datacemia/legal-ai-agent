from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document_schema import DocumentResponse
from app.utils.file_validator import validate_file
from app.utils.security import get_current_user
from app.services.storage_service import save_upload_file

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    contract_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = file.file.read()
    file_size = len(content)
    file.file.seek(0)

    try:
        extension = validate_file(file.filename, file_size)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        file_path = save_upload_file(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    document = Document(
        user_id=current_user.id,
        file_name=file.filename,
        file_type=extension,
        contract_type=contract_type,
        status="uploaded",
        file_path=file_path,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ✅ UPDATED: allow premium plan
    if current_user.role != "admin" and current_user.plan != "premium":
        raise HTTPException(status_code=403, detail="Not allowed")

    return db.query(Document).filter(Document.user_id == current_user.id).all()