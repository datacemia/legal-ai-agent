import os
import ssl
import secrets
import smtplib
from email.message import EmailMessage

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config import FRONTEND_URL
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from app.utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


def send_verification_email(to_email: str, token: str):
    verify_url = f"{FRONTEND_URL}/verify-email?token={token}"

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("SMTP_FROM_EMAIL", smtp_user)
    from_name = os.getenv("SMTP_FROM_NAME", "Runexa")

    if not smtp_host or not smtp_user or not smtp_password:
        print("SMTP not configured. Verification link:", verify_url)
        return

    msg = EmailMessage()
    msg["Subject"] = "Verify your Runexa account"
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email

    msg.set_content(
        f"""
Welcome to Runexa.

Please verify your email address using this link:

{verify_url}

If you did not create this account, you can ignore this email.
"""
    )

    context = ssl.create_default_context()

    # ✅ FIX SANS CASSER (debug SMTP)
    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print("Verification email sent to:", to_email)

    except Exception as e:
        print("SMTP ERROR:", repr(e))


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    token = secrets.token_urlsafe(32)

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        is_active=True,
        email_verified=False,
        activation_token=token,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_verification_email(new_user.email, token)

    return new_user


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.activation_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification link")

    user.email_verified = True
    user.activation_token = None

    db.commit()

    return {"message": "Email verified successfully. You can now login."}


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, existing_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not existing_user.email_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before login",
        )

    token = create_access_token({"sub": str(existing_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": existing_user,
    }


@router.post("/token")
def token_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == form_data.username).first()

    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(form_data.password, existing_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not existing_user.email_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before login",
        )

    token = create_access_token({"sub": str(existing_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
    }