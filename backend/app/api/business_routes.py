import json
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.security import get_current_user
from app.utils.billing import check_and_consume_agent_access

from app.models.user import User
from app.models.job import Job
from app.models.business_analysis import BusinessAnalysis

from app.schemas.business_schema import BusinessHistoryItem

from app.services.enterprise_service import (
    check_enterprise_agent_access,
    consume_enterprise_agent_quota,
    consume_enterprise_credits,
)


router = APIRouter(
    prefix="/business",
    tags=["Business"],
)

BUSINESS_AGENT_CREDITS = 30
BUSINESS_UPLOAD_DIR = Path("uploads/business_jobs")
BUSINESS_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _safe_business_file_name(original_name: str) -> str:
    suffix = Path(original_name).suffix.lower()
    return f"{uuid4().hex}{suffix}"


def _save_business_upload(file: UploadFile) -> str:
    safe_name = _safe_business_file_name(file.filename or "business_file")
    output_path = BUSINESS_UPLOAD_DIR / safe_name

    with output_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(output_path)


@router.post("/analyze")
async def analyze_business(
    file: UploadFile = File(...),
    output_language: str = Form("en"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if output_language not in ["en", "fr", "ar"]:
        output_language = "en"

    if not file.filename:
        raise HTTPException(status_code=400, detail="File is required.")

    allowed_extensions = (".csv", ".xlsx")

    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Only CSV or Excel (.xlsx) files are supported.",
        )

    enterprise_context = check_enterprise_agent_access(
        db=db,
        user=current_user,
        agent_slug="business",
    )

    if enterprise_context:
        consume_enterprise_agent_quota(
            db=db,
            access=enterprise_context["access"],
        )

        billing = consume_enterprise_credits(
            db=db,
            user=current_user,
            agent_slug="business",
            credits_used=BUSINESS_AGENT_CREDITS,
            request_type="analysis",
        )
    else:
        billing = check_and_consume_agent_access(
            db=db,
            user=current_user,
            agent_slug="business",
        )

    try:
        file_path = _save_business_upload(file)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save business file: {str(error)}",
        )

    job = Job(
        user_id=current_user.id,
        job_type="business_ai",
        status="pending",
        progress=0,
        status_message={
            "en": "Queued business analysis...",
            "fr": "Analyse business en file d’attente...",
            "ar": "تمت إضافة تحليل الأعمال إلى قائمة الانتظار...",
        }.get(output_language, "Queued business analysis..."),
        input={
            "file_path": file_path,
            "file_name": file.filename,
            "output_language": output_language,
            "access_type": billing.get("access_type"),
            "credits_used": billing.get("credits_used", 0),
        },
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "status_message": job.status_message,
    }


@router.get("/history", response_model=list[BusinessHistoryItem])
def get_business_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analyses = (
        db.query(BusinessAnalysis)
        .filter(BusinessAnalysis.user_id == current_user.id)
        .order_by(BusinessAnalysis.id.desc())
        .all()
    )

    history = []

    for analysis in analyses:
        try:
            parsed_result = json.loads(analysis.result)
        except Exception:
            parsed_result = {"error": "Invalid stored analysis result."}

        history.append(
            {
                "id": analysis.id,
                "file_name": analysis.file_name,
                "result": parsed_result,
                "created_at": analysis.created_at,
            }
        )

    return history
