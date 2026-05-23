import json

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.security import get_current_user
from app.utils.billing import check_and_consume_agent_access
from app.models.user import User
from app.models.finance_analysis import FinanceAnalysis
from app.models.finance_chat_message import FinanceChatMessage
from app.schemas.finance_schema import FinanceHistoryItem

from app.services.finance_agent.statement_parser import extract_statement_text
from app.services.finance_agent.finance_ai_agent import analyze_bank_statement
from app.services.finance_agent.finance_chat_agent import answer_finance_question

# 🔥 Finance OS V2 modules
from app.services.finance_agent.transaction_extractor import extract_transactions
from app.services.finance_agent.subscription_detector import detect_recurring_subscriptions
from app.services.finance_agent.budget_engine import build_recommended_budget
from app.services.finance_agent.forecasting import predict_cashflow
from app.services.finance_agent.scoring import calculate_financial_scores
from app.services.finance_agent.charts_builder import build_financial_charts
from app.services.finance_agent.savings_opportunities import (
    detect_savings_opportunities,
)
from app.services.finance_agent.insights_engine import (
    generate_financial_insights,
)
from app.services.finance_agent.alerts_engine import (
    generate_financial_alerts,
)


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


# 🔥 MAIN ROUTE WITH BILLING + FINANCE OS V2
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

    # 🔥 1. Main AI analysis
    result_ai = analyze_bank_statement(text, output_language)

    fallback_income = result_ai.get("total_income_estimate")

    # 🔥 2. Finance OS V2 features
    transactions = extract_transactions(text)
    subscriptions = detect_recurring_subscriptions(transactions)

    savings_opportunities = detect_savings_opportunities(
        transactions=transactions,
        subscriptions=subscriptions,
    )

    budget = build_recommended_budget(
        transactions=transactions,
        fallback_income=fallback_income,
    )

    forecast = predict_cashflow(
        transactions=transactions,
        fallback_income=fallback_income,
    )

    scores = calculate_financial_scores(
        transactions=transactions,
        subscriptions=subscriptions,
        fallback_income=fallback_income,
    )

    alerts = generate_financial_alerts(
        transactions=transactions,
        subscriptions=subscriptions,
        forecast=forecast,
        scores=scores,
    )

    insights = generate_financial_insights(
        transactions=transactions,
        subscriptions=subscriptions,
        scores=scores,
        forecast=forecast,
        opportunities=savings_opportunities,
    )

    charts = build_financial_charts(transactions)

    # 🔥 3. Final combined result
    result = {
        **result_ai,
        "transactions": transactions,
        "charts": charts,
        "subscriptions_detected": subscriptions,
        "savings_opportunities": savings_opportunities,
        "recommended_budget": budget,
        "cashflow_forecast": forecast,
        "financial_habit_scores": scores,
        "financial_alerts": alerts,
        "financial_insights": insights,
    }

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

    result["id"] = analysis.id

    return result


# 💬 FINANCE CHAT COACH
@router.post("/chat")
def chat_with_finance_coach(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analysis_id = data.get("analysis_id")
    question = data.get("question")
    output_language = data.get("output_language", "en")

    if not analysis_id:
        raise HTTPException(
            status_code=400,
            detail="analysis_id is required.",
        )

    if not question:
        raise HTTPException(
            status_code=400,
            detail="question is required.",
        )

    analysis = (
        db.query(FinanceAnalysis)
        .filter(
            FinanceAnalysis.id == analysis_id,
            FinanceAnalysis.user_id == current_user.id,
        )
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Finance analysis not found.",
        )

    analysis_result = json.loads(analysis.result)

    response = answer_finance_question(
        analysis_result=analysis_result,
        question=question,
        output_language=output_language,
    )

    user_message = FinanceChatMessage(
        user_id=current_user.id,
        analysis_id=analysis_id,
        role="user",
        content=question,
    )

    assistant_message = FinanceChatMessage(
        user_id=current_user.id,
        analysis_id=analysis_id,
        role="assistant",
        content=response["answer"],
    )

    db.add(user_message)
    db.add(assistant_message)

    db.commit()

    return response


# 💬 FINANCE CHAT HISTORY
@router.get("/chat/history/{analysis_id}")
def get_finance_chat_history(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analysis = (
        db.query(FinanceAnalysis)
        .filter(
            FinanceAnalysis.id == analysis_id,
            FinanceAnalysis.user_id == current_user.id,
        )
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Finance analysis not found.",
        )

    messages = (
        db.query(FinanceChatMessage)
        .filter(
            FinanceChatMessage.analysis_id == analysis_id,
            FinanceChatMessage.user_id == current_user.id,
        )
        .order_by(FinanceChatMessage.id.asc())
        .all()
    )

    return [
        {
            "id": message.id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at,
        }
        for message in messages
    ]


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
