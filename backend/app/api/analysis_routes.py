import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.models.analysis import AnalysisResult
from app.models.job import Job
from app.models.user import User
from app.schemas.analysis_schema import AnalysisResponse

from app.utils.security import get_current_user
from app.utils.billing import check_and_consume_agent_access
from app.services.enterprise_service import (
    check_enterprise_agent_access,
    consume_enterprise_agent_quota,
    consume_enterprise_credits,
)

from app.services.contract_agent.contract_parser import extract_text
from app.services.text_cleaner import clean_text

router = APIRouter(prefix="/analysis", tags=["Analysis"])

LEGAL_AGENT_CREDITS = 8


# =========================
# RATE LIMIT
# =========================
ANALYSIS_ATTEMPTS = {}
MAX_ANALYSIS_ATTEMPTS = 20
ANALYSIS_WINDOW_SECONDS = 60


def check_analysis_rate_limit(user_id: int):
    now = datetime.utcnow()

    attempts = ANALYSIS_ATTEMPTS.get(user_id, [])

    attempts = [
        attempt
        for attempt in attempts
        if (now - attempt).total_seconds() < ANALYSIS_WINDOW_SECONDS
    ]

    if len(attempts) >= MAX_ANALYSIS_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many analyses. Please try again later.",
        )

    attempts.append(now)
    ANALYSIS_ATTEMPTS[user_id] = attempts


# =========================
# RUN ANALYSIS ASYNC JOB
# =========================
@router.post("/{document_id}/run")
def run_analysis(
    document_id: int,
    output_language: str = "en",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_analysis_rate_limit(current_user.id)

    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if document.status == "processing":
        raise HTTPException(
            status_code=429,
            detail="Analysis already in progress",
        )

    enterprise_context = check_enterprise_agent_access(
        db=db,
        user=current_user,
        agent_slug="legal",
    )

    if enterprise_context:
        consume_enterprise_agent_quota(
            db=db,
            access=enterprise_context["access"],
        )

        billing = consume_enterprise_credits(
            db=db,
            user=current_user,
            agent_slug="legal",
            credits_used=LEGAL_AGENT_CREDITS,
            request_type="analysis",
        )
    else:
        billing = check_and_consume_agent_access(
            db=db,
            user=current_user,
            agent_slug="legal",
        )

    if output_language not in ["en", "fr", "ar"]:
        output_language = "en"

    try:
        raw_text = extract_text(
            document.file_path,
            document.file_type,
        )
        document_text = clean_text(raw_text)
    except Exception as e:
        document.status = "failed"
        db.commit()
        raise HTTPException(
            status_code=400,
            detail=f"Could not read uploaded file: {str(e)}",
        )

    document.status = "processing"
    db.commit()
    db.refresh(document)

    job = Job(
        user_id=current_user.id,
        job_type="contract_ai",
        status="pending",
        progress=0,
        status_message="Queued legal analysis...",
        input={
            "document_id": document.id,
            "document_text": document_text,
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
    }


# =========================
# ANALYSIS HISTORY
# IMPORTANT:
# This route must stay BEFORE '/{document_id}'.
# Otherwise FastAPI may interpret 'history' as document_id.
# =========================
@router.get("/history")
def get_analysis_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analyses = (
        db.query(AnalysisResult)
        .join(Document, Document.id == AnalysisResult.document_id)
        .filter(Document.user_id == current_user.id)
        .order_by(AnalysisResult.id.desc())
        .all()
    )

    items = []

    for analysis in analyses:
        clauses = analysis.clauses

        if isinstance(clauses, str):
            try:
                clauses = json.loads(clauses)
            except Exception:
                clauses = []

        document = getattr(analysis, "document", None)

        items.append(
            {
                "id": analysis.id,
                "document_id": analysis.document_id,
                "file_name": document.file_name if document else None,
                "file_type": document.file_type if document else None,
                "summary": analysis.summary,
                "risk_score": analysis.risk_score,
                "clauses": clauses,
                "language": document.language if document else None,
                "status": document.status if document else None,
                "created_at": analysis.created_at,
            }
        )

    return items


# =========================
# GET ANALYSIS
# =========================
@router.get("/{document_id}", response_model=AnalysisResponse)
def get_analysis(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    analysis = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.document_id == document_id)
        .order_by(AnalysisResult.id.desc())
        .first()
    )

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return analysis
