import json
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.models.job import Job
from app.security.api_key_auth import get_current_api_context
from app.services.api_usage_service import record_api_usage
from app.services.quota_service import require_api_quota
from app.services.rate_limit_service import check_api_rate_limit
from app.services.business_agent.business_parser import extract_business_data
from app.services.cloud_storage_service import (
    download_api_file_from_cloud,
    upload_api_file_to_cloud,
)
from app.services.contract_agent.contract_parser import extract_text


router = APIRouter()


def _make_json_safe(value):
    return json.loads(
        json.dumps(
            value,
            ensure_ascii=False,
            default=str,
        )
    )


def _normalize_language(output_language: str) -> str:
    if output_language not in ["en", "fr", "ar"]:
        return "en"

    return output_language


@router.get("/v1/test-api-key")
def test_api_key(
    context=Depends(get_current_api_context),
    db: Session = Depends(get_db),
):
    user = context["user"]
    api_key = context["api_key"]

    check_api_rate_limit(db=db, user=user)

    remaining_credits = require_api_quota(
        db=db,
        user=user,
        required_credits=0,
    )

    record_api_usage(
        db=db,
        user_id=user.id,
        api_key_id=api_key.id,
        endpoint="/v1/test-api-key",
        agent="test",
        credits_used=0,
        status="success",
    )

    return {
        "ok": True,
        "user_id": user.id,
        "email": user.email,
        "api_key_id": api_key.id,
        "remaining_api_credits": remaining_credits,
    }


@router.post("/v1/legal/analyze")
async def api_legal_analyze(
    file: UploadFile = File(...),
    output_language: str = Form("en"),
    context=Depends(get_current_api_context),
    db: Session = Depends(get_db),
):
    user = context["user"]
    api_key = context["api_key"]

    check_api_rate_limit(db=db, user=user)

    output_language = _normalize_language(output_language)

    required_credits = 12

    remaining_credits = require_api_quota(
        db=db,
        user=user,
        required_credits=required_credits,
    )

    uploaded = await upload_api_file_to_cloud(
        file=file,
        folder="upload",
    )

    document = Document(
        user_id=user.id,
        file_name=uploaded["file_name"],
        file_path=uploaded["storage_path"],
        file_type=uploaded["ext"].replace(".", ""),
        status="pending",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    job = Job(
        user_id=user.id,
        job_type="contract_ai",
        status="pending",
        progress=0,
        status_message="Legal API analysis queued...",
        input={
            "document_id": document.id,
            "storage_bucket": uploaded["storage_bucket"],
            "storage_path": uploaded["storage_path"],
            "content_type": uploaded["content_type"],
            "output_language": output_language,
            "access_type": "api",
            "credits_used": required_credits,
            "api_key_id": api_key.id,
        },
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    record_api_usage(
        db=db,
        user_id=user.id,
        api_key_id=api_key.id,
        endpoint="/v1/legal/analyze",
        agent="legal",
        credits_used=required_credits,
        status="queued",
    )

    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "status_message": job.status_message,
        "credits_used": required_credits,
        "remaining_api_credits": remaining_credits,
    }


@router.post("/v1/finance/analyze")
async def api_finance_analyze(
    file: UploadFile = File(...),
    output_language: str = Form("en"),
    context=Depends(get_current_api_context),
    db: Session = Depends(get_db),
):
    user = context["user"]
    api_key = context["api_key"]

    check_api_rate_limit(db=db, user=user)

    output_language = _normalize_language(output_language)

    required_credits = 7

    remaining_credits = require_api_quota(
        db=db,
        user=user,
        required_credits=required_credits,
    )

    uploaded = await upload_api_file_to_cloud(
        file=file,
        folder="finance",
    )

    job = Job(
        user_id=user.id,
        job_type="finance_ai",
        status="pending",
        progress=0,
        status_message="Finance API analysis queued...",
        input={
            "storage_bucket": uploaded["storage_bucket"],
            "storage_path": uploaded["storage_path"],
            "file_name": uploaded["file_name"],
            "content_type": uploaded["content_type"],
            "user_id": user.id,
            "output_language": output_language,
            "access_type": "api",
            "credits_used": required_credits,
            "api_key_id": api_key.id,
        },
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    record_api_usage(
        db=db,
        user_id=user.id,
        api_key_id=api_key.id,
        endpoint="/v1/finance/analyze",
        agent="finance",
        credits_used=required_credits,
        status="queued",
    )

    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "status_message": job.status_message,
        "credits_used": required_credits,
        "remaining_api_credits": remaining_credits,
    }


@router.post("/v1/business/analyze")
async def api_business_analyze(
    file: UploadFile = File(...),
    output_language: str = Form("en"),
    context=Depends(get_current_api_context),
    db: Session = Depends(get_db),
):
    user = context["user"]
    api_key = context["api_key"]

    check_api_rate_limit(db=db, user=user)

    output_language = _normalize_language(output_language)

    required_credits = 30

    uploaded = await upload_api_file_to_cloud(
        file=file,
        folder="business",
    )

    await file.seek(0)

    try:
        parsed_data = await extract_business_data(file)
        parsed_data = _make_json_safe(parsed_data)

    except ValueError as error:
        record_api_usage(
            db=db,
            user_id=user.id,
            api_key_id=api_key.id,
            endpoint="/v1/business/analyze",
            agent="business",
            credits_used=0,
            status="failed",
        )

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        record_api_usage(
            db=db,
            user_id=user.id,
            api_key_id=api_key.id,
            endpoint="/v1/business/analyze",
            agent="business",
            credits_used=0,
            status="failed",
        )

        raise HTTPException(
            status_code=400,
            detail=f"Could not read uploaded business file: {str(error)}",
        )

    if not parsed_data:
        record_api_usage(
            db=db,
            user_id=user.id,
            api_key_id=api_key.id,
            endpoint="/v1/business/analyze",
            agent="business",
            credits_used=0,
            status="failed",
        )

        raise HTTPException(
            status_code=400,
            detail="Could not extract business data from file.",
        )

    remaining_credits = require_api_quota(
        db=db,
        user=user,
        required_credits=required_credits,
    )

    job = Job(
        user_id=user.id,
        job_type="business_ai",
        status="pending",
        progress=0,
        status_message="Business API analysis queued...",
        input={
            "parsed_data": parsed_data,
            "storage_bucket": uploaded["storage_bucket"],
            "storage_path": uploaded["storage_path"],
            "file_name": uploaded["file_name"],
            "content_type": uploaded["content_type"],
            "output_language": output_language,
            "access_type": "api",
            "credits_used": required_credits,
            "api_key_id": api_key.id,
        },
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    record_api_usage(
        db=db,
        user_id=user.id,
        api_key_id=api_key.id,
        endpoint="/v1/business/analyze",
        agent="business",
        credits_used=required_credits,
        status="queued",
    )

    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "status_message": job.status_message,
        "credits_used": required_credits,
        "remaining_api_credits": remaining_credits,
    }


@router.post("/v1/study/analyze")
async def api_study_analyze(
    file: UploadFile = File(...),
    output_language: str = Form("en"),
    education_level: str = Form("university"),
    context=Depends(get_current_api_context),
    db: Session = Depends(get_db),
):
    user = context["user"]
    api_key = context["api_key"]

    check_api_rate_limit(db=db, user=user)

    output_language = _normalize_language(output_language)

    required_credits = 5

    uploaded = await upload_api_file_to_cloud(
        file=file,
        folder="study",
    )

    file_path = download_api_file_from_cloud(
        storage_path=uploaded["storage_path"],
        suffix=uploaded["ext"],
    )

    file_type = uploaded["ext"].replace(".", "")

    try:
        extracted_text = extract_text(
            file_path,
            file_type,
        )

    except Exception as error:
        record_api_usage(
            db=db,
            user_id=user.id,
            api_key_id=api_key.id,
            endpoint="/v1/study/analyze",
            agent="study",
            credits_used=0,
            status="failed",
        )

        raise HTTPException(
            status_code=400,
            detail=f"Could not extract text from uploaded study file: {str(error)}",
        )

    if not extracted_text or not extracted_text.strip():
        record_api_usage(
            db=db,
            user_id=user.id,
            api_key_id=api_key.id,
            endpoint="/v1/study/analyze",
            agent="study",
            credits_used=0,
            status="failed",
        )

        raise HTTPException(
            status_code=400,
            detail="Could not extract readable text from uploaded study file.",
        )

    remaining_credits = require_api_quota(
        db=db,
        user=user,
        required_credits=required_credits,
    )

    job = Job(
        user_id=user.id,
        job_type="study_ai",
        status="pending",
        progress=0,
        status_message="Study API analysis queued...",
        input={
            "text": extracted_text,
            "file_path": file_path,
            "storage_bucket": uploaded["storage_bucket"],
            "storage_path": uploaded["storage_path"],
            "file_name": uploaded["file_name"],
            "user_id": user.id,
            "education_level": education_level,
            "output_language": output_language,
            "weak_points": [],
            "cache_key": str(uuid.uuid4()),
            "access_type": "api",
            "credits_used": required_credits,
            "api_key_id": api_key.id,
        },
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    record_api_usage(
        db=db,
        user_id=user.id,
        api_key_id=api_key.id,
        endpoint="/v1/study/analyze",
        agent="study",
        credits_used=required_credits,
        status="queued",
    )

    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "status_message": job.status_message,
        "credits_used": required_credits,
        "remaining_api_credits": remaining_credits,
    }


@router.get("/v1/jobs/{job_id}")
def api_get_job(
    job_id: int,
    context=Depends(get_current_api_context),
    db: Session = Depends(get_db),
):
    user = context["user"]
    api_key = context["api_key"]

    check_api_rate_limit(db=db, user=user)

    job = (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.user_id == user.id,
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    record_api_usage(
        db=db,
        user_id=user.id,
        api_key_id=api_key.id,
        endpoint=f"/v1/jobs/{job_id}",
        agent="jobs",
        credits_used=0,
        status="success",
    )

    return {
        "id": job.id,
        "job_type": job.job_type,
        "status": job.status,
        "progress": job.progress,
        "status_message": job.status_message,
        "result": job.result,
        "error": job.error,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
    }
