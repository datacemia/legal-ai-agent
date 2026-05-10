import os
import ssl
import secrets
import smtplib
import re
from datetime import datetime, timedelta
from email.message import EmailMessage

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from authlib.integrations.starlette_client import OAuth

from app.config import FRONTEND_URL
from app.database import get_db
from app.models.user import User
from app.models.enterprise_invitation import EnterpriseInvitation
from app.models.organization_member import OrganizationMember
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from app.utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

RATE_LIMIT_SECONDS = 60

# ================= AJOUT =================
LOGIN_ATTEMPTS = {}
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 60


def check_login_rate_limit(email: str):
    now = datetime.utcnow()
    email = email.strip().lower()

    attempts = LOGIN_ATTEMPTS.get(email, [])
    attempts = [
        attempt for attempt in attempts
        if (now - attempt).total_seconds() < LOGIN_WINDOW_SECONDS
    ]

    if len(attempts) >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Please try again later.",
        )

    attempts.append(now)
    LOGIN_ATTEMPTS[email] = attempts
# ================= FIN AJOUT =================




def auto_accept_enterprise_invites_for_user(db: Session, user: User):
    """Attach a newly created user to any pending enterprise invitations.

    Safe behavior:
    - does nothing if there is no pending invitation for this email
    - does not change the user's platform role
    - avoids duplicate OrganizationMember rows
    """
    invite_email = user.email.strip().lower()

    pending_invites = (
        db.query(EnterpriseInvitation)
        .filter(
            EnterpriseInvitation.email == invite_email,
            EnterpriseInvitation.status == "pending",
        )
        .all()
    )

    if not pending_invites:
        return

    for invitation in pending_invites:
        existing_membership = (
            db.query(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == invitation.organization_id,
                OrganizationMember.user_id == user.id,
            )
            .first()
        )

        if not existing_membership:
            db.add(
                OrganizationMember(
                    organization_id=invitation.organization_id,
                    user_id=user.id,
                    role=invitation.role,
                    status="active",
                )
            )

        invitation.status = "accepted"
        invitation.accepted_at = datetime.utcnow()

    db.commit()


# ================= OAUTH =================

oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="microsoft",
    client_id=os.getenv("MICROSOFT_CLIENT_ID"),
    client_secret=os.getenv("MICROSOFT_CLIENT_SECRET"),
    authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
    access_token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    api_base_url="https://graph.microsoft.com/v1.0/",
    client_kwargs={"scope": "User.Read"},
)


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = os.getenv(
        "GOOGLE_REDIRECT_URI",
        "https://legal-ai-agent-production-fa17.up.railway.app/auth/google/callback"
    )
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    email = user_info["email"]

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            password_hash="",
            is_active=True,
            email_verified=True,
            role="user",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": str(user.id)})

    return RedirectResponse(
        url=(
            f"{FRONTEND_URL}/oauth-success"
            f"?token={access_token}"
            f"&role={user.role}"
            f"&plan={user.plan}"
            f"&credits_balance={user.credits_balance}"
        )
    )


@router.get("/microsoft/login")
async def microsoft_login(request: Request):
    redirect_uri = os.getenv(
        "MICROSOFT_REDIRECT_URI",
        "https://legal-ai-agent-production-fa17.up.railway.app/auth/microsoft/callback"
    )
    return await oauth.microsoft.authorize_redirect(request, redirect_uri)


@router.get("/microsoft/callback")
async def microsoft_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.microsoft.authorize_access_token(request)

    resp = await oauth.microsoft.get("me", token=token)
    user_info = resp.json()

    email = user_info.get("mail") or user_info.get("userPrincipalName")

    if not email:
        raise HTTPException(status_code=400, detail="Microsoft email not found")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            password_hash="",
            is_active=True,
            email_verified=True,
            role="user",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": str(user.id)})

    return RedirectResponse(
        url=(
            f"{FRONTEND_URL}/oauth-success"
            f"?token={access_token}"
            f"&role={user.role}"
            f"&plan={user.plan}"
            f"&credits_balance={user.credits_balance}"
        )
    )


# ================= PASSWORD VALIDATION =================

def validate_password(password: str):
    if len(password) < 12:
        return "Password must be at least 12 characters."

    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return "Password must contain at least one number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."

    return None


# ================= EMAIL FUNCTIONS =================

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

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print("Verification email sent to:", to_email)

    except Exception as e:
        print("SMTP ERROR:", repr(e))


def send_reset_email(to_email: str, token: str):
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("SMTP_FROM_EMAIL", smtp_user)
    from_name = os.getenv("SMTP_FROM_NAME", "Runexa")

    msg = EmailMessage()
    msg["Subject"] = "Reset your password"
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email

    msg.set_content(f"""
Reset your password:

{reset_url}

If you did not request this, ignore this email.
""")

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print("Reset email sent to:", to_email)

    except Exception as e:
        print("SMTP ERROR:", repr(e))


# ================= REGISTER =================

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    error = validate_password(user.password)
    if error:
        raise HTTPException(status_code=400, detail=error)

    token = secrets.token_urlsafe(32)

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        is_active=True,
        email_verified=False,
        activation_token=token,
        activation_token_expires=datetime.utcnow() + timedelta(hours=24),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    auto_accept_enterprise_invites_for_user(db, new_user)

    send_verification_email(new_user.email, token)

    return new_user


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.activation_token == token).first()

    if not user or user.activation_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired verification link")

    user.email_verified = True
    user.activation_token = None

    db.commit()

    return {"message": "Email verified successfully. You can now login."}


# ================= LOGIN =================

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    check_login_rate_limit(user.email)

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
    check_login_rate_limit(form_data.username)

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


# ================= RESEND VERIFICATION =================

@router.post("/resend-verification")
def resend_verification(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email", "").strip()

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"message": "If this email exists, a verification link has been sent."}

    if user.email_verified:
        return {"message": "Email already verified."}

    now = datetime.utcnow()

    if user.last_verification_email_sent_at and (
        now - user.last_verification_email_sent_at
    ).total_seconds() < RATE_LIMIT_SECONDS:
        return {"message": "Please wait before requesting another email."}

    token = secrets.token_urlsafe(32)
    user.activation_token = token
    user.last_verification_email_sent_at = now

    db.commit()

    send_verification_email(user.email, token)

    return {"message": "Verification email sent."}


# ================= FORGOT PASSWORD =================

@router.post("/forgot-password")
def forgot_password(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email", "").strip().lower()

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"message": "If this email exists, a reset link has been sent."}

    now = datetime.utcnow()

    if user.last_reset_email_sent_at and (
        now - user.last_reset_email_sent_at
    ).total_seconds() < RATE_LIMIT_SECONDS:
        return {"message": "Please wait before requesting another email."}

    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expires = datetime.utcnow() + timedelta(minutes=15)
    user.last_reset_email_sent_at = now

    db.commit()

    send_reset_email(user.email, token)

    return {"message": "Password reset email sent."}


@router.post("/reset-password")
def reset_password(payload: dict, db: Session = Depends(get_db)):
    token = payload.get("token")
    new_password = payload.get("password")

    user = db.query(User).filter(User.reset_token == token).first()

    if not user or user.reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    error = validate_password(new_password)
    if error:
        raise HTTPException(status_code=400, detail=error)

    user.password_hash = hash_password(new_password)
    user.reset_token = None

    db.commit()

    return {"message": "Password updated successfully"}