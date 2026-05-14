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
from app.services.enterprise_service import (
    check_enterprise_agent_access,
    consume_enterprise_agent_quota,
    consume_enterprise_credits,
)

from app.services.contract_agent.contract_parser import extract_text
from app.services.text_cleaner import clean_text
from app.services.contract_agent.clause_splitter import split_into_clauses
from app.services.language_service import detect_language
from app.services.contract_agent.contract_agent import analyze_contract_clauses

from app.services.contract_agent.summary_service import (
    generate_summary_data,
    render_summary_text,
    calculate_global_risk,
    generate_simplified_version,
)
from app.services.contract_agent.validator import (
    validate_contract_result,
)

router = APIRouter(prefix="/analysis", tags=["Analysis"])

LEGAL_AGENT_CREDITS = 8


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

    document.status = "processing"

    db.commit()

    raw_text = extract_text(
        document.file_path,
        document.file_type
    )

    cleaned_text = clean_text(raw_text)

    detected_language = detect_language(cleaned_text)

    clauses = split_into_clauses(cleaned_text)

    print("\n=== CLAUSES DEBUG ===")
    print("CLAUSES COUNT:", len(clauses))

    for i, c in enumerate(clauses[:10]):
        print(f"\n--- CLAUSE {i + 1} ---")
        print(c[:500])

    print("=====================\n")

    clause_results = analyze_contract_clauses(
        clauses,
        output_language
    )

    global_risk = calculate_global_risk(clause_results)

    print("\n=== LEGAL SUMMARY TEXT DEBUG ===")
    print(cleaned_text[:3000])
    print("TEXT LENGTH:", len(cleaned_text))
    print("================================\n")

    summary_data = generate_summary_data(
        cleaned_text,
        output_language
    )

    summary = render_summary_text(
        summary_data,
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

    response = {
        "id": analysis.id,
        "document_id": analysis.document_id,
        "summary": analysis.summary,

        "clauses": clause_results,

        "risk_level": analysis.risk_level,
        "risk_score": analysis.risk_score,

        "simplified_version": analysis.simplified_version,

        "recommendations": recommendations,

        "created_at": analysis.created_at,

        "contract_quality_score": summary_data.get(
            "contract_quality_score"
        ),

        "overall_balance": summary_data.get(
            "overall_balance"
        ),

        "contract_complexity": summary_data.get(
            "contract_complexity"
        ),

        "jurisdiction_detected": summary_data.get(
            "jurisdiction_detected"
        ),
    }

    response["quality_check"] = validate_contract_result(
        response
    )

    return response


# ================= ANALYSIS HISTORY =================
# IMPORTANT:
# This route must stay BEFORE "/{document_id}".
# Otherwise FastAPI may interpret "history" as document_id.
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

    for a in analyses:
        clauses = a.clauses

        if isinstance(clauses, str):
            try:
                clauses = json.loads(clauses)
            except Exception:
                clauses = []

        document = getattr(a, "document", None)

        items.append(
            {
                "id": a.id,
                "document_id": a.document_id,
                "file_name": document.file_name if document else None,
                "file_type": document.file_type if document else None,
                "summary": a.summary,
                "risk_score": a.risk_score,
                "clauses": clauses,
                "language": document.language if document else None,
                "status": document.status if document else None,
                "created_at": a.created_at,
            }
        )

    return items


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
