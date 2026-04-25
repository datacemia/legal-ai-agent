import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.config import (
    STRIPE_ENABLED,
    STRIPE_SECRET_KEY,
    STRIPE_WEBHOOK_SECRET,
    FRONTEND_URL,
    ANALYSIS_PRICE_EUR,
)
from app.database import get_db
from app.models.user import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


@router.post("/create-checkout-session")
def create_checkout_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not STRIPE_ENABLED or not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe is not configured yet"
        )

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Contract Analysis Credit",
                    },
                    "unit_amount": ANALYSIS_PRICE_EUR * 100,
                },
                "quantity": 1,
            }
        ],
        success_url=f"{FRONTEND_URL}/dashboard?payment=success",
        cancel_url=f"{FRONTEND_URL}/dashboard?payment=cancel",
        metadata={
            "user_id": str(current_user.id),
            "credits": "1",
        },
    )

    return {"checkout_url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    if not STRIPE_ENABLED or not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=503,
            detail="Stripe webhook is not configured yet"
        )

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["metadata"].get("user_id")
        credits = int(session["metadata"].get("credits", "1"))

        user = db.query(User).filter(User.id == int(user_id)).first()

        if user:
            user.analysis_credits += credits
            db.commit()

    return {"received": True}