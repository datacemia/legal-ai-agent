import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.config import FRONTEND_URL

from app.database import engine, Base

from app.api.auth_routes import router as auth_router
from app.api.document_routes import router as document_router
from app.api.analysis_routes import router as analysis_router
from app.api.payment_routes import router as payment_router
from app.api.user_routes import router as user_router
from app.api.admin_routes import router as admin_router
from app.api.contact_routes import router as contact_router
from app.api.finance_routes import router as finance_router
from app.api.study_routes import router as study_router
from app.api.business_routes import router as business_router

from app.models.user import User
from app.models.document import Document
from app.models.analysis import AnalysisResult
from app.models.payment import Payment
from app.models.contact import ContactRequest
from app.models.finance_analysis import FinanceAnalysis
from app.models.study_analysis import StudyAnalysis
from app.models.business_analysis import BusinessAnalysis


app = FastAPI(
    title="Legal AI Agent API",
    version="1.0.0",
)

allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.100.10:3000",
]

if FRONTEND_URL:
    allowed_origins.append(FRONTEND_URL)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SECRET_KEY"],
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

app.include_router(auth_router)
app.include_router(document_router)
app.include_router(analysis_router)
app.include_router(payment_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(contact_router)
app.include_router(finance_router)
app.include_router(study_router)
app.include_router(business_router)


@app.get("/")
def root():
    return {"message": "Legal AI Agent API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}