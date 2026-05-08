import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.models.analysis import AnalysisResult
from app.models.user import User
from app.schemas.analysis_schema import AnalysisResponse

from app.utils.security import get_current_user
from app.utils.billing import check_and_consume_agent_access

from app.services.contract_parser import extract_text
from app.services.text_cleaner import clean_text
from app.services.clause_splitter import split_into_clauses
from app.services.language_service import detect_language
from app.services.contract_agent import analyze_contract_clauses

from app.services.summary_service import (
    generate_summary,
    calculate_global_risk,
    generate_simplified_version,
)

router = APIRouter(prefix="/analysis", tags=["Analysis"])


# ================= RATE LIMIT =================
ANALYSIS_ATTEMPTS = {}
MAX_ANALYSIS_ATTEMPTS = 3
ANALYSIS_WINDOW_SECONDS = 60


def check_analysis_rate_limit(user_id: int):
    now = datetime.utcnow()

    attempts = ANALYSIS_ATTEMPTS.get(user_id, [])

    attempts = [
        attempt for attempt in attempts
        if (now - attempt).total_seconds() < ANALYSIS_WINDOW_SECONDS
    ]

    if len(attempts) >= MAX_ANALYSIS_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many analyses. Please try again later.",
        )

    attempts.append(now)

    ANALYSIS_ATTEMPTS[user_id] = attempts


# ================= RUN ANALYSIS =================
@router.post("/{document_id}/run", response_model=AnalysisResponse)
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

    billing = check_and_consume_agent_access(
        db=db,
        user=current_user,
        agent_slug="legal",
    )

    if output_language not in ["en", "fr", "ar"]:
        output_language = "en"

    document.status = "processing"

    db.commit()

    raw_text = extract_text(
        document.file_path,
        document.file_type
    )

    cleaned_text = clean_text(raw_text)

    detected_language = detect_language(cleaned_text)

    clauses = split_into_clauses(cleaned_text)

    clause_results = analyze_contract_clauses(
        clauses,
        output_language
    )

    global_risk = calculate_global_risk(clause_results)

    summary = generate_summary(
        cleaned_text,
        output_language
    )

    simplified = generate_simplified_version(
        cleaned_text,
        output_language
    )

    recommendations = [
        "Review all medium and high risk clauses.",
        "Ask a lawyer before signing important contracts.",
    ]

    analysis = AnalysisResult(
        document_id=document.id,

        summary=summary,

        clauses=json.dumps(
            clause_results,
            ensure_ascii=False
        ),

        risk_level=global_risk["risk_level"],

        risk_score=global_risk["risk_score"],

        simplified_version=simplified,

        recommendations=json.dumps(
            recommendations,
            ensure_ascii=False
        ),

        access_type=billing["access_type"],

        credits_used=billing["credits_used"],
    )

    document.language = detected_language

    document.status = "completed"

    db.add(analysis)

    db.commit()

    db.refresh(analysis)

    return analysis


# ================= GET ANALYSIS =================
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