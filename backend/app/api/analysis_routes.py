import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.models.analysis import AnalysisResult
from app.models.user import User
from app.schemas.analysis_schema import AnalysisResponse
from app.utils.security import get_current_user

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


@router.post("/{document_id}/run", response_model=AnalysisResponse)
def run_analysis(
    document_id: int,
    output_language: str = "en",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    is_admin = current_user.role == "admin"

    has_free_analysis = current_user.free_analyses_used < 1
    has_paid_credit = current_user.analysis_credits > 0

    if not is_admin and not has_free_analysis and not has_paid_credit:
        raise HTTPException(
            status_code=402,
            detail="Payment required. Please buy an analysis credit.",
        )

    is_free_analysis = not is_admin and has_free_analysis

    if output_language not in ["en", "fr", "ar"]:
        output_language = "en"

    document.status = "processing"
    db.commit()

    raw_text = extract_text(document.file_path, document.file_type)
    cleaned_text = clean_text(raw_text)
    detected_language = detect_language(cleaned_text)
    clauses = split_into_clauses(cleaned_text)

    clause_results = analyze_contract_clauses(clauses, output_language)

    if is_free_analysis:
        visible_clause_results = clause_results[:2]
    else:
        visible_clause_results = clause_results

    global_risk = calculate_global_risk(clause_results)
    summary = generate_summary(cleaned_text, output_language)
    simplified = generate_simplified_version(cleaned_text, output_language)

    if is_free_analysis:
        recommendations = [
            "Recommendations are limited to the 2 displayed clauses.",
            "Upgrade to unlock recommendations for all clauses.",
        ]
    else:
        recommendations = [
            "Review all medium and high risk clauses.",
            "Ask a lawyer before signing important contracts.",
        ]

    analysis = AnalysisResult(
        document_id=document.id,
        summary=summary,
        clauses=json.dumps(visible_clause_results, ensure_ascii=False),
        risk_level=global_risk["risk_level"],
        risk_score=global_risk["risk_score"],
        simplified_version=simplified,
        recommendations=json.dumps(recommendations, ensure_ascii=False),
    )

    document.language = detected_language
    document.status = "completed"

    if not is_admin:
        if has_free_analysis:
            current_user.free_analyses_used += 1
        else:
            current_user.analysis_credits -= 1

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


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