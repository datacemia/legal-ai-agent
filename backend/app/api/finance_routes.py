import json
import os
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.security import get_current_user
from app.utils.billing import check_and_consume_agent_access
from app.models.user import User
from app.models.finance_analysis import FinanceAnalysis
from app.models.finance_chat_message import FinanceChatMessage
from app.models.job import Job
from app.models.uploaded_file import UploadedFile
from app.schemas.finance_schema import FinanceHistoryItem

from app.services.finance_agent.statement_parser import extract_statement_text
from app.services.finance_agent.finance_ai_agent import analyze_bank_statement
from app.services.finance_agent.finance_chat_agent import answer_finance_question

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

MAX_FINANCE_UPLOAD_BYTES = 15 * 1024 * 1024
MAX_FINANCE_CHAT_CHARS = 2000

RATE_LIMIT_BUCKETS: dict[str, list[datetime]] = {}

RATE_LIMITS = {
    "finance_analyze_json": {"max_attempts": 20, "window_seconds": 60},
    "finance_statement": {"max_attempts": 8, "window_seconds": 60},
    "finance_chat": {"max_attempts": 20, "window_seconds": 60},
    "finance_chat_history": {"max_attempts": 40, "window_seconds": 60},
    "finance_history": {"max_attempts": 40, "window_seconds": 60},
}


def get_client_identifier(request: Request, user_id: int):
    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
    elif request.client and request.client.host:
        ip = request.client.host
    else:
        ip = "unknown"

    return f"{user_id}:{ip}"


def check_rate_limit(action: str, request: Request, user_id: int):
    now = datetime.utcnow()
    config = RATE_LIMITS[action]
    identifier = get_client_identifier(request, user_id)
    bucket_key = f"{action}:{identifier}"

    attempts = RATE_LIMIT_BUCKETS.get(bucket_key, [])
    attempts = [
        attempt
        for attempt in attempts
        if (now - attempt).total_seconds() < config["window_seconds"]
    ]

    if len(attempts) >= config["max_attempts"]:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
        )

    attempts.append(now)
    RATE_LIMIT_BUCKETS[bucket_key] = attempts


# 🔹 OLD JSON API
@router.post("/analyze")
def analyze_finance(
    request: Request,
    data: dict,
    current_user: User = Depends(get_current_user),
):
    check_rate_limit("finance_analyze_json", request, current_user.id)

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
    request: Request,
    file: UploadFile = File(...),
    output_language: str = Form("en"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_rate_limit("finance_statement", request, current_user.id)

    if output_language not in ["en", "fr", "ar"]:
        output_language = "en"

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

    upload_dir = "storage/finance"
    os.makedirs(upload_dir, exist_ok=True)

    unique_name = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(upload_dir, unique_name)

    content = await file.read()

    if len(content) > MAX_FINANCE_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum allowed size is 15 MB.",
        )

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    uploaded_file = UploadedFile(
        user_id=current_user.id,
        agent_type="finance",
        original_file_name=file.filename,
        stored_file_name=unique_name,
        file_path=file_path,
        mime_type=file.content_type,
        file_extension="pdf",
        file_size_bytes=len(content),
        storage_backend="local",
        status="uploaded",
        consent_for_training=False,
    )

    db.add(uploaded_file)
    db.commit()
    db.refresh(uploaded_file)

    job = Job(
        user_id=current_user.id,
        job_type="finance_ai",
        status="pending",
        progress=0,
        status_message="Finance analysis queued...",
        input={
            "file_bytes": content.hex(),
            "file_name": file.filename,
            "user_id": current_user.id,
            "output_language": output_language,
            "access_type": billing["access_type"],
            "credits_used": billing["credits_used"],
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


# 💬 FINANCE CHAT COACH
@router.post("/chat")
def chat_with_finance_coach(
    request: Request,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_rate_limit("finance_chat", request, current_user.id)

    analysis_id = data.get("analysis_id")
    question = data.get("question")
    output_language = data.get("output_language", "en")

    if output_language not in ["en", "fr", "ar"]:
        output_language = "en"

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

    if len(str(question)) > MAX_FINANCE_CHAT_CHARS:
        raise HTTPException(
            status_code=413,
            detail="Question is too long.",
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
    request: Request,
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_rate_limit("finance_chat_history", request, current_user.id)

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
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_rate_limit("finance_history", request, current_user.id)

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
