from datetime import datetime
import os

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document_schema import DocumentResponse
from app.utils.file_validator import validate_file
from app.utils.security import get_current_user
from app.services.storage_service import save_upload_file
from app.services.supabase_storage_service import upload_file_to_supabase_storage

router = APIRouter(prefix="/documents", tags=["Documents"])

MAX_DOCUMENT_UPLOAD_BYTES = 15 * 1024 * 1024

RATE_LIMIT_BUCKETS: dict[str, list[datetime]] = {}

RATE_LIMITS = {
    "document_upload": {
        "max_attempts": 10,
        "window_seconds": 60,
    },
    "document_list": {
        "max_attempts": 60,
        "window_seconds": 60,
    },
}


def get_client_identifier(request: Request, user_id: int):
    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
    elif request.client and request.client.host:
        ip = request.client.host
    else:
        ip = "unknown"

    return f"{user_id}:{ip}"


def check_rate_limit(action: str, request: Request, user_id: int):
    now = datetime.utcnow()
    config = RATE_LIMITS[action]
    identifier = get_client_identifier(request, user_id)
    bucket_key = f"{action}:{identifier}"

    attempts = RATE_LIMIT_BUCKETS.get(bucket_key, [])
    attempts = [
        attempt
        for attempt in attempts
        if (now - attempt).total_seconds() < config["window_seconds"]
    ]

    if len(attempts) >= config["max_attempts"]:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
        )

    attempts.append(now)
    RATE_LIMIT_BUCKETS[bucket_key] = attempts


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    request: Request,
    file: UploadFile = File(...),
    contract_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_rate_limit("document_upload", request, current_user.id)

    if not file.filename:
        raise HTTPException(status_code=400, detail="File is required.")

    content = file.file.read()
    file_size = len(content)

    if file_size > MAX_DOCUMENT_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum allowed size is 15 MB.",
        )

    file.file.seek(0)

    try:
        extension = validate_file(file.filename, file_size)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        file_path = save_upload_file(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    stored_file_name = os.path.basename(file_path)
    supabase_storage_path = f"legal/{stored_file_name}"

    storage_result = upload_file_to_supabase_storage(
        local_file_path=file_path,
        storage_path=supabase_storage_path,
        content_type=file.content_type,
    )

    document = Document(
        user_id=current_user.id,
        file_name=file.filename,
        file_type=extension,
        contract_type=contract_type,
        status="uploaded",
        file_path=file_path,
        storage_path=storage_result["storage_path"],
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_rate_limit("document_list", request, current_user.id)

    allowed_plans = ["paid", "pro", "premium"]

    if (
        current_user.role != "admin"
        and current_user.plan not in allowed_plans
    ):
        raise HTTPException(status_code=403, detail="Not allowed")

    return db.query(Document).filter(Document.user_id == current_user.id).all()
