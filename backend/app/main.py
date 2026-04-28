import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import FRONTEND_URL

from app.api.auth_routes import router as auth_router
from app.api.document_routes import router as document_router
from app.api.analysis_routes import router as analysis_router
from app.api.payment_routes import router as payment_router
from app.api.user_routes import router as user_router
from app.api.admin_routes import router as admin_router
from app.api.contact_routes import router as contact_router

from app.database import engine, Base
from app.models.user import User
from app.models.document import Document
from app.models.analysis import AnalysisResult
from app.models.payment import Payment
from app.models.contact import ContactRequest

app = FastAPI(
    title="Legal AI Agent API",
    version="1.0.0"
)

# ✅ AJOUT OBLIGATOIRE POUR GOOGLE OAUTH
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "change-me"),
    same_site="lax",
    https_only=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        FRONTEND_URL,
    ],
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


@app.get("/")
def root():
    return {"message": "Legal AI Agent API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}