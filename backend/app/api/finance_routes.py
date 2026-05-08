import json

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.security import get_current_user
from app.utils.billing import check_and_consume_agent_access
from app.models.user import User
from app.models.finance_analysis import FinanceAnalysis
from app.schemas.finance_schema import FinanceHistoryItem

from app.services.finance_agent.statement_parser import extract_statement_text
from app.services.finance_agent.finance_ai_agent import analyze_bank_statement


router = APIRouter(prefix="/finance", tags=["Finance"])


# 🔹 OLD JSON API (keep as is)
@router.post("/analyze")
def analyze_finance(data: dict, current_user: User = Depends(get_current_user)):
    expenses = data.get("expenses", [])

    total = sum(e["amount"] for e in expenses)

    categories = {}
    for e in expenses:
        categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]

    waste = []
    recommendations = []

    if categories.get("subscriptions", 0) > 30:
        waste.append("High spending on subscriptions")
        recommendations.append("Consider cancelling unused subscriptions")

    if categories.get("food", 0) > 200:
        waste.append("High food expenses")
        recommendations.append("Reduce eating out")

    return {
        "total_spent": total,
        "categories": categories,
        "waste_detected": waste,
        "recommendations": recommendations,
    }


# 🔥 MAIN ROUTE WITH BILLING
@router.post("/analyze-statement")
async def analyze_statement(
    file: UploadFile = File(...),
    output_language: str = Form("en"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF bank statements are allowed.",
        )

    billing = check_and_consume_agent_access(
        db=db,
        user=current_user,
        agent_slug="finance",
    )

    text = await extract_statement_text(file)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF.",
        )

    result = analyze_bank_statement(text, output_language)

    analysis = FinanceAnalysis(
        user_id=current_user.id,
        file_name=file.filename,
        result=json.dumps(result, ensure_ascii=False),
        access_type=billing["access_type"],
        credits_used=billing["credits_used"],
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return result


# 📜 HISTORY
@router.get("/history", response_model=list[FinanceHistoryItem])
def get_finance_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analyses = (
        db.query(FinanceAnalysis)
        .filter(FinanceAnalysis.user_id == current_user.id)
        .order_by(FinanceAnalysis.id.desc())
        .all()
    )

    return [
        {
            "id": analysis.id,
            "file_name": analysis.file_name,
            "result": json.loads(analysis.result),
            "created_at": analysis.created_at,
        }
        for analysis in analyses
    ]