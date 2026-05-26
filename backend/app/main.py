import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()

from app.config import FRONTEND_URL
from app.database import Base, engine

from app.api.agent0_waitlist_routes import router as agent0_waitlist_router
from app.api.admin_api_routes import router as admin_api_management_router
from app.api.admin_routes import router as admin_router
from app.api.analysis_routes import router as analysis_router
from app.api.auth_routes import router as auth_router
from app.api.business_export_routes import router as business_export_router
from app.api.business_reports import router as business_reports_router
from app.api.business_routes import router as business_router
from app.api.contact_routes import router as contact_router
from app.api.document_routes import router as document_router
from app.api.enterprise_agent_access_routes import (
    router as enterprise_agent_access_router,
)
from app.api.enterprise_routes import router as enterprise_router
from app.api.finance_routes import router as finance_router
from app.api.job_routes import router as job_router
from app.api.payment_routes import router as payment_router
from app.api.study_routes import router as study_router
from app.api.user_routes import router as user_router

from app.api import api_keys
from app.api import public_api

# Import models so SQLAlchemy registers all tables before create_all().
from app.models.agent0_waitlist import Agent0Waitlist
from app.models.agent_trial_usage import AgentTrialUsage
from app.models.analysis import AnalysisResult
from app.models.api_key import ApiKey
from app.models.api_usage import ApiUsage
from app.models.business_analysis import BusinessAnalysis
from app.models.contact import ContactRequest
from app.models.document import Document
from app.models.finance_analysis import FinanceAnalysis
from app.models.finance_chat_message import FinanceChatMessage
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember
from app.models.organization_usage_log import OrganizationUsageLog
from app.models.payment import Payment
from app.models.study_analysis import StudyAnalysis, StudyAttempt
from app.models.usage_log import UsageLog
from app.models.user import User


app = FastAPI(
    title="Legal AI Agent API",
    version="1.0.0",
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
    )

    return response


allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.100.10:3000",
    "https://runexa.ai",
    "https://www.runexa.ai",
]

if FRONTEND_URL and FRONTEND_URL not in allowed_origins:
    allowed_origins.append(FRONTEND_URL)

secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise RuntimeError("SECRET_KEY environment variable is required.")

app.add_middleware(
    SessionMiddleware,
    secret_key=secret_key,
    same_site="lax",
    https_only=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


# =========================
# Core routes
# =========================

app.include_router(auth_router)
app.include_router(document_router)
app.include_router(analysis_router)
app.include_router(payment_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(contact_router)
app.include_router(admin_api_management_router)
app.include_router(api_keys.router)
app.include_router(public_api.router)


# =========================
# Agent routes
# =========================

app.include_router(finance_router)
app.include_router(study_router)
app.include_router(business_router)
app.include_router(business_reports_router)
app.include_router(business_export_router)
app.include_router(job_router)


# =========================
# Enterprise / Labs routes
# =========================

app.include_router(agent0_waitlist_router)
app.include_router(enterprise_router)
app.include_router(enterprise_agent_access_router)


@app.get("/")
def root():
    return {
        "message": "Legal AI Agent API is running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }
