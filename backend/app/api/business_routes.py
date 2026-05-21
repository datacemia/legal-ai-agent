import json

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.security import get_current_user
from app.utils.billing import check_and_consume_agent_access

from app.models.user import User
from app.models.job import Job
from app.models.business_analysis import BusinessAnalysis

from app.schemas.business_schema import BusinessHistoryItem

from app.services.business_agent.business_parser import extract_business_data

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


def _make_json_safe(value):
    return json.loads(
        json.dumps(
            value,
            ensure_ascii=False,
            default=str,
        )
    )


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
        parsed_data = await extract_business_data(file)
        parsed_data = _make_json_safe(parsed_data)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read uploaded business file: {str(error)}",
        )

    if not parsed_data:
        raise HTTPException(
            status_code=400,
            detail="Could not extract business data from file.",
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
            "parsed_data": parsed_data,
            "file_name": file.filename,
            "content_type": file.content_type,
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
