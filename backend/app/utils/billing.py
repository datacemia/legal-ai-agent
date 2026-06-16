from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.agent_trial_usage import AgentTrialUsage
from app.models.usage_log import UsageLog


AGENT_CREDIT_COSTS = {
    "legal": 12,
    "finance": 7,
    "study": 5,
    "business": 30,
}


ACTIVE_SUBSCRIPTION_PLANS = {"pro", "premium"}


def _get_int(value, default: int = 0) -> int:
    try:
        return int(value or default)
    except (TypeError, ValueError):
        return default


def check_and_consume_agent_access(
    db: Session,
    user: User,
    agent_slug: str,
):
    """
    Runexa agent access rules:

    1. Admin users have free unlimited access.
    2. Subscription credits are consumed first.
    3. Purchased credits are consumed second.
    4. A paid $1 trial gives one use per agent.
    5. If none of the above applies, payment is required.

    Expected User fields:
    - role
    - plan
    - subscription_status
    - subscription_credits_balance
    - credits_balance

    Notes:
    - subscription_credits_balance = monthly Pro credits that reset each billing cycle.
    - credits_balance = purchased credits that do not expire.
    """

    if agent_slug not in AGENT_CREDIT_COSTS:
        raise HTTPException(status_code=400, detail="Unknown agent")

    user_role = (user.role or "user").lower().strip()
    user_plan = (user.plan or "free").lower().strip()
    subscription_status = (getattr(user, "subscription_status", "") or "").lower().strip()

    credit_cost = AGENT_CREDIT_COSTS[agent_slug]

    # Admin has free unlimited access
    if user_role == "admin":
        usage = UsageLog(
            user_id=user.id,
            agent_slug=agent_slug,
            access_type="admin",
            credits_used=0,
            credits_source="admin",
        )

        db.add(usage)
        db.commit()

        return {
            "access_type": "admin",
            "credits_used": 0,
            "credits_source": "admin",
        }

    # Active Pro/Premium subscription uses monthly subscription credits first
    is_active_subscription = (
        user_plan in ACTIVE_SUBSCRIPTION_PLANS
        and subscription_status in {"active", "trialing", "paid"}
    )

    if is_active_subscription:
        subscription_credits = _get_int(
            getattr(user, "subscription_credits_balance", 0)
        )

        if subscription_credits >= credit_cost:
            user.subscription_credits_balance = subscription_credits - credit_cost

            usage = UsageLog(
                user_id=user.id,
                agent_slug=agent_slug,
                access_type=user_plan,
                credits_used=credit_cost,
                credits_source="subscription",
            )

            db.add(usage)
            db.commit()
            db.refresh(user)

            return {
                "access_type": user_plan,
                "credits_used": credit_cost,
                "credits_source": "subscription",
            }

    # Purchased credits are global and do not expire
    purchased_credits = _get_int(getattr(user, "credits_balance", 0))

    if purchased_credits >= credit_cost:
        user.credits_balance = purchased_credits - credit_cost

        usage = UsageLog(
            user_id=user.id,
            agent_slug=agent_slug,
            access_type="credits",
            credits_used=credit_cost,
            credits_source="purchased",
        )

        db.add(usage)
        db.commit()
        db.refresh(user)

        return {
            "access_type": "credits",
            "credits_used": credit_cost,
            "credits_source": "purchased",
        }

    # $1 trial per agent
    trial = (
        db.query(AgentTrialUsage)
        .filter(
            AgentTrialUsage.user_id == user.id,
            AgentTrialUsage.agent_slug == agent_slug,
        )
        .first()
    )

    if not trial or not trial.trial_paid:
        raise HTTPException(
            status_code=402,
            detail=f"$1 trial payment required for {agent_slug}",
        )

    if trial.trial_used:
        raise HTTPException(
            status_code=403,
            detail=f"Trial already used for {agent_slug}",
        )

    trial.trial_used = True

    usage = UsageLog(
        user_id=user.id,
        agent_slug=agent_slug,
        access_type="trial",
        credits_used=0,
        credits_source="trial",
    )

    db.add(usage)
    db.commit()

    return {
        "access_type": "trial",
        "credits_used": 0,
        "credits_source": "trial",
    }
