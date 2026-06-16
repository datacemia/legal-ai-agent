from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database import Base


class AgentTrialUsage(Base):
    __tablename__ = "agent_trial_usage"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False, index=True)

    # legal, finance, study, business, sentinel
    agent_slug = Column(String, nullable=False, index=True)

    # user paid the $1 trial
    trial_paid = Column(Boolean, default=False)

    # user already consumed the trial analysis
    trial_used = Column(Boolean, default=False)

    # Stripe Checkout session that paid this trial
    stripe_session_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # when the trial was consumed
    used_at = Column(DateTime, nullable=True)
