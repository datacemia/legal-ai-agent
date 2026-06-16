from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    stripe_customer_id = Column(String, nullable=True)
    stripe_session_id = Column(String, nullable=True, index=True)
    stripe_payment_intent_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)

    # Existing field kept for compatibility:
    # free, trial, pro, premium, api_starter, api_pro, etc.
    plan = Column(String, default="free")

    # Stripe/payment status:
    # pending, paid, active, failed, canceled, refunded
    status = Column(String, default="inactive")

    # trial, credits_pack, subscription, api
    product_type = Column(String, nullable=True)

    # legal, finance, study, business
    agent_slug = Column(String, nullable=True)

    # Credits granted by this payment, if any
    credits = Column(Integer, default=0)

    # Amount in cents:
    # $1.00 = 100
    # $49.00 = 4900
    amount = Column(Integer, nullable=True)

    currency = Column(String, default="usd")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
