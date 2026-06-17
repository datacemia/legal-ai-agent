import os
from datetime import datetime

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import (
    STRIPE_ENABLED,
    STRIPE_SECRET_KEY,
    STRIPE_WEBHOOK_SECRET,
    FRONTEND_URL,
)
from app.database import get_db
from app.models.user import User
from app.models.payment import Payment
from app.models.agent_trial_usage import AgentTrialUsage
from app.models.credit_transaction import CreditTransaction
from app.utils.security import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


TRIAL_AGENTS = {"legal", "finance", "study", "business"}

CREDIT_PACKS = {
    "starter": {
        "name": "Runexa Credits Starter",
        "credits": 50,
        "amount": 900,
    },
    "growth": {
        "name": "Runexa Credits Growth",
        "credits": 150,
        "amount": 2400,
    },
    "scale": {
        "name": "Runexa Credits Scale",
        "credits": 500,
        "amount": 7500,
    },
}

API_PLANS = {
    "api_starter": {
        "name": "Runexa API Starter",
        "credits": 100,
        "amount": 2900,
    },
    "api_pro": {
        "name": "Runexa API Pro",
        "credits": 500,
        "amount": 9900,
    },
}

PRO_PLAN = {
    "name": "Runexa Pro",
    "credits": 500,
    "amount": 4900,
}


class CheckoutRequest(BaseModel):
    product_type: str
    agent_slug: str | None = None
    pack: str | None = None
    api_plan: str | None = None


def _require_stripe_config():
    if not STRIPE_ENABLED or not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe is not configured yet",
        )


def _get_or_create_stripe_customer(user: User, db: Session) -> str:
    if user.stripe_customer_id:
        return user.stripe_customer_id

    customer = stripe.Customer.create(
        email=user.email,
        metadata={
            "user_id": str(user.id),
        },
    )

    user.stripe_customer_id = customer.id
    db.commit()
    db.refresh(user)

    return customer.id


def _create_price_data(
    name: str,
    amount: int,
    recurring: bool = False,
):
    price_data = {
        "currency": "usd",
        "product_data": {
            "name": name,
        },
        "unit_amount": amount,
    }

    if recurring:
        price_data["recurring"] = {
            "interval": "month",
        }

    return price_data


def _to_plain_dict(obj):
    """
    Convert StripeObject instances into plain Python dictionaries.
    This avoids AttributeError: get with some stripe-python versions.
    """
    if obj is None:
        return {}

    if isinstance(obj, dict):
        return obj

    if hasattr(obj, "to_dict_recursive"):
        return obj.to_dict_recursive()

    if hasattr(obj, "to_dict"):
        return obj.to_dict()

    return dict(obj)


def _stripe_get(obj, key: str, default=None):
    data = _to_plain_dict(obj)
    return data.get(key, default)


def _create_payment_record(
    db: Session,
    user_id: int,
    session,
    product_type: str,
    plan: str | None = None,
    agent_slug: str | None = None,
    credits: int = 0,
    amount: int | None = None,
    stripe_subscription_id: str | None = None,
):
    payment = Payment(
        user_id=user_id,
        stripe_customer_id=_stripe_get(session, "customer"),
        stripe_session_id=_stripe_get(session, "id"),
        stripe_payment_intent_id=_stripe_get(session, "payment_intent"),
        stripe_subscription_id=stripe_subscription_id or _stripe_get(session, "subscription"),
        product_type=product_type,
        plan=plan or "free",
        agent_slug=agent_slug,
        credits=credits,
        amount=amount,
        currency="usd",
        status="pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(payment)
    db.commit()

    return payment


@router.post("/create-checkout-session")
def create_checkout_session(
    payload: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_stripe_config()

    customer_id = _get_or_create_stripe_customer(current_user, db)

    product_type = payload.product_type.strip().lower()

    metadata = {
        "user_id": str(current_user.id),
        "product_type": product_type,
    }

    mode = "payment"
    line_item = None
    plan = "free"
    agent_slug = None
    credits = 0
    amount = None

    if product_type == "trial":
        if not payload.agent_slug or payload.agent_slug not in TRIAL_AGENTS:
            raise HTTPException(status_code=400, detail="Invalid trial agent")

        existing_trial = (
            db.query(AgentTrialUsage)
            .filter(
                AgentTrialUsage.user_id == current_user.id,
                AgentTrialUsage.agent_slug == payload.agent_slug,
            )
            .first()
        )

        if existing_trial and existing_trial.trial_paid:
            raise HTTPException(
                status_code=409,
                detail=f"Trial already activated for {payload.agent_slug}",
            )

        agent_slug = payload.agent_slug
        credits = 0
        amount = 100
        plan = "trial"

        metadata.update(
            {
                "agent_slug": agent_slug,
                "credits": "0",
                "plan": plan,
            }
        )

        line_item = {
            "price_data": _create_price_data(
                name=f"Runexa {agent_slug.title()} Trial",
                amount=amount,
            ),
            "quantity": 1,
        }

    elif product_type == "credits_pack":
        if not payload.pack or payload.pack not in CREDIT_PACKS:
            raise HTTPException(status_code=400, detail="Invalid credit pack")

        pack = CREDIT_PACKS[payload.pack]
        credits = pack["credits"]
        amount = pack["amount"]
        plan = "free"

        metadata.update(
            {
                "pack": payload.pack,
                "credits": str(credits),
                "plan": plan,
            }
        )

        line_item = {
            "price_data": _create_price_data(
                name=pack["name"],
                amount=amount,
            ),
            "quantity": 1,
        }

    elif product_type == "subscription":
        mode = "subscription"
        credits = PRO_PLAN["credits"]
        amount = PRO_PLAN["amount"]
        plan = "pro"

        metadata.update(
            {
                "plan": plan,
                "credits": str(credits),
            }
        )

        pro_price_id = os.getenv("STRIPE_PRICE_PRO_MONTHLY")

        if pro_price_id:
            line_item = {
                "price": pro_price_id,
                "quantity": 1,
            }
        else:
            line_item = {
                "price_data": _create_price_data(
                    name=PRO_PLAN["name"],
                    amount=amount,
                    recurring=True,
                ),
                "quantity": 1,
            }

    elif product_type == "api":
        if not payload.api_plan or payload.api_plan not in API_PLANS:
            raise HTTPException(status_code=400, detail="Invalid API plan")

        api_plan = API_PLANS[payload.api_plan]
        credits = api_plan["credits"]
        amount = api_plan["amount"]
        plan = payload.api_plan

        metadata.update(
            {
                "api_plan": payload.api_plan,
                "credits": str(credits),
                "plan": plan,
            }
        )

        line_item = {
            "price_data": _create_price_data(
                name=api_plan["name"],
                amount=amount,
            ),
            "quantity": 1,
        }

    else:
        raise HTTPException(status_code=400, detail="Invalid product type")

    session = stripe.checkout.Session.create(
        mode=mode,
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[line_item],
        success_url=f"{FRONTEND_URL}/dashboard?payment=success",
        cancel_url=f"{FRONTEND_URL}/pricing?payment=cancel",
        metadata=metadata,
        subscription_data={
            "metadata": metadata,
        }
        if mode == "subscription"
        else None,
    )

    _create_payment_record(
        db=db,
        user_id=current_user.id,
        session=session,
        product_type=product_type,
        plan=plan,
        agent_slug=agent_slug,
        credits=credits,
        amount=amount,
    )

    return {
        "checkout_url": session.url,
    }


def _mark_payment_paid(db: Session, session, status: str = "paid"):
    payment = (
        db.query(Payment)
        .filter(Payment.stripe_session_id == _stripe_get(session, "id"))
        .first()
    )

    if payment:
        payment.status = status
        payment.stripe_customer_id = _stripe_get(session, "customer")
        payment.stripe_payment_intent_id = _stripe_get(session, "payment_intent")
        payment.stripe_subscription_id = _stripe_get(session, "subscription")
        payment.updated_at = datetime.utcnow()


def _already_processed_event(db: Session, event_id: str) -> bool:
    return (
        db.query(CreditTransaction)
        .filter(CreditTransaction.stripe_event_id == event_id)
        .first()
        is not None
    )


def _record_credit_transaction(
    db: Session,
    user_id: int,
    amount: int,
    source: str,
    transaction_type: str,
    description: str,
    stripe_event_id: str | None = None,
):
    tx = CreditTransaction(
        user_id=user_id,
        amount=amount,
        source=source,
        type=transaction_type,
        description=description,
        stripe_event_id=stripe_event_id,
        created_at=datetime.utcnow(),
    )

    db.add(tx)


def _handle_checkout_completed(db: Session, event):
    event = _to_plain_dict(event)
    session = _to_plain_dict(event["data"]["object"])
    metadata = _to_plain_dict(_stripe_get(session, "metadata"))

    user_id = metadata.get("user_id")
    product_type = metadata.get("product_type")

    if not user_id or not product_type:
        return

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        return

    user.stripe_customer_id = _stripe_get(session, "customer") or user.stripe_customer_id

    _mark_payment_paid(db, session, status="paid")

    if product_type == "trial":
        agent_slug = metadata.get("agent_slug")

        if not agent_slug:
            return

        trial = (
            db.query(AgentTrialUsage)
            .filter(
                AgentTrialUsage.user_id == user.id,
                AgentTrialUsage.agent_slug == agent_slug,
            )
            .first()
        )

        if not trial:
            trial = AgentTrialUsage(
                user_id=user.id,
                agent_slug=agent_slug,
                trial_paid=True,
                trial_used=False,
                stripe_session_id=_stripe_get(session, "id"),
                created_at=datetime.utcnow(),
            )
            db.add(trial)
        else:
            trial.trial_paid = True
            trial.stripe_session_id = _stripe_get(session, "id")

        _record_credit_transaction(
            db=db,
            user_id=user.id,
            amount=0,
            source="trial",
            transaction_type="credit",
            description=f"$1 trial activated for {agent_slug} agent",
            stripe_event_id=event["id"],
        )

    elif product_type == "credits_pack":
        credits = int(metadata.get("credits", "0"))

        if credits > 0:
            user.credits_balance = int(user.credits_balance or 0) + credits

            _record_credit_transaction(
                db=db,
                user_id=user.id,
                amount=credits,
                source="purchased",
                transaction_type="credit",
                description=f"Purchased credit pack: +{credits} credits",
                stripe_event_id=event["id"],
            )

    elif product_type == "subscription":
        credits = int(metadata.get("credits", "500"))

        user.plan = "pro"
        user.subscription_status = "active"
        user.subscription_credits_balance = credits

        _record_credit_transaction(
            db=db,
            user_id=user.id,
            amount=credits,
            source="subscription",
            transaction_type="credit",
            description=f"Runexa Pro subscription activated: {credits} monthly credits",
            stripe_event_id=event["id"],
        )

    elif product_type == "api":
        api_plan = metadata.get("api_plan")
        credits = int(metadata.get("credits", "0"))

        if api_plan:
            user.api_enabled = True
            user.api_plan = api_plan
            user.api_credits_balance = int(user.api_credits_balance or 0) + credits

            _record_credit_transaction(
                db=db,
                user_id=user.id,
                amount=credits,
                source="api",
                transaction_type="credit",
                description=f"{api_plan} activated: +{credits} API credits",
                stripe_event_id=event["id"],
            )

    db.commit()


def _handle_invoice_paid(db: Session, event):
    event = _to_plain_dict(event)
    invoice = _to_plain_dict(event["data"]["object"])
    subscription_id = _stripe_get(invoice, "subscription")

    if not subscription_id:
        return

    subscription = stripe.Subscription.retrieve(subscription_id)
    metadata = _stripe_get(subscription, "metadata") or {}

    user_id = metadata.get("user_id")
    product_type = metadata.get("product_type")
    credits = int(metadata.get("credits", "500"))

    if not user_id or product_type != "subscription":
        return

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        return

    user.plan = "pro"
    user.subscription_status = "active"
    user.subscription_credits_balance = credits

    current_period_end = _stripe_get(subscription, "current_period_end")

    if current_period_end:
        user.subscription_current_period_end = datetime.utcfromtimestamp(
            current_period_end
        )

    _record_credit_transaction(
        db=db,
        user_id=user.id,
        amount=credits,
        source="subscription",
        transaction_type="reset",
        description=f"Monthly subscription credits reset to {credits}",
        stripe_event_id=event["id"],
    )

    db.commit()


def _handle_subscription_updated(db: Session, event):
    event = _to_plain_dict(event)
    subscription = _to_plain_dict(event["data"]["object"])
    metadata = _to_plain_dict(_stripe_get(subscription, "metadata"))

    user_id = metadata.get("user_id")

    if not user_id:
        return

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        return

    user.subscription_status = _stripe_get(subscription, "status") or "none"

    current_period_end = _stripe_get(subscription, "current_period_end")

    if current_period_end:
        user.subscription_current_period_end = datetime.utcfromtimestamp(
            current_period_end
        )

    if user.subscription_status in {"canceled", "unpaid", "incomplete_expired"}:
        user.plan = "free"
        user.subscription_credits_balance = 0

    db.commit()


def _handle_subscription_deleted(db: Session, event):
    event = _to_plain_dict(event)
    subscription = _to_plain_dict(event["data"]["object"])
    metadata = _to_plain_dict(_stripe_get(subscription, "metadata"))

    user_id = metadata.get("user_id")

    if not user_id:
        return

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        return

    user.plan = "free"
    user.subscription_status = "canceled"
    user.subscription_credits_balance = 0

    db.commit()



@router.get("/trial-status/{agent_slug}")
def get_trial_status(
    agent_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    normalized_agent_slug = (agent_slug or "").lower().strip()

    if normalized_agent_slug not in TRIAL_AGENTS:
        raise HTTPException(status_code=400, detail="Invalid trial agent")

    trial = (
        db.query(AgentTrialUsage)
        .filter(
            AgentTrialUsage.user_id == current_user.id,
            AgentTrialUsage.agent_slug == normalized_agent_slug,
        )
        .first()
    )

    return {
        "agent_slug": normalized_agent_slug,
        "trial_paid": bool(trial and trial.trial_paid),
        "trial_used": bool(trial and trial.trial_used),
    }


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    if not STRIPE_ENABLED or not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=503,
            detail="Stripe webhook is not configured yet",
        )

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            STRIPE_WEBHOOK_SECRET,
        )
        event = _to_plain_dict(event)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    event_id = event["id"]

    if _already_processed_event(db, event_id):
        return {"received": True, "duplicate": True}

    event_type = event["type"]

    if event_type == "checkout.session.completed":
        _handle_checkout_completed(db, event)

    elif event_type == "invoice.paid":
        _handle_invoice_paid(db, event)

    elif event_type == "customer.subscription.updated":
        _handle_subscription_updated(db, event)

    elif event_type == "customer.subscription.deleted":
        _handle_subscription_deleted(db, event)

    return {"received": True}
