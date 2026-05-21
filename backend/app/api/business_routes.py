import json
import os
from pathlib import Path
from uuid import uuid4

import requests
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
BUSINESS_STORAGE_BUCKET = os.getenv(
    "SUPABASE_BUSINESS_BUCKET",
    "business-files",
)


def _get_supabase_config():
    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not service_role_key:
        raise HTTPException(
            status_code=500,
            detail="Supabase storage is not configured.",
        )

    return supabase_url.rstrip("/"), service_role_key


def _safe_business_file_name(original_name: str) -> str:
    suffix = Path(original_name or "business_file").suffix.lower()

    if suffix not in [".csv", ".xlsx"]:
        suffix = ".csv"

    return f"{uuid4().hex}{suffix}"


def _business_storage_path(user_id: int, original_name: str) -> str:
    safe_name = _safe_business_file_name(original_name)

    return f"user-{user_id}/{safe_name}"


async def _upload_business_file_to_supabase(
    file: UploadFile,
    user_id: int,
) -> dict:
    supabase_url, service_role_key = _get_supabase_config()
    storage_path = _business_storage_path(
        user_id=user_id,
        original_name=file.filename or "business_file",
    )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    upload_url = (
        f"{supabase_url}/storage/v1/object/"
        f"{BUSINESS_STORAGE_BUCKET}/{storage_path}"
    )

    response = requests.post(
        upload_url,
        headers={
            "Authorization": f"Bearer {service_role_key}",
            "apikey": service_role_key,
            "Content-Type": (
                file.content_type
                or "application/octet-stream"
            ),
            "x-upsert": "true",
        },
        data=content,
        timeout=60,
    )

    if response.status_code not in [200, 201]:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to upload business file to storage: "
                f"{response.text}"
            ),
        )

    return {
        "storage_bucket": BUSINESS_STORAGE_BUCKET,
        "storage_path": storage_path,
        "file_name": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(content),
    }


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

    storage_data = await _upload_business_file_to_supabase(
        file=file,
        user_id=current_user.id,
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
            "storage_bucket": storage_data["storage_bucket"],
            "storage_path": storage_data["storage_path"],
            "file_name": storage_data["file_name"],
            "content_type": storage_data["content_type"],
            "size_bytes": storage_data["size_bytes"],
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
