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

def check_and_consume_agent_access(
    db: Session,
    user: User,
    agent_slug: str,
):
    if agent_slug not in AGENT_CREDIT_COSTS:
        raise HTTPException(status_code=400, detail="Unknown agent")

    # Admin has free unlimited access
    if user.role == "admin":
        usage = UsageLog(
            user_id=user.id,
            agent_slug=agent_slug,
            access_type="admin",
            credits_used=0,
        )

        db.add(usage)
        db.commit()

        return {
            "access_type": "admin",
            "credits_used": 0,
        }

    credit_cost = AGENT_CREDIT_COSTS[agent_slug]

    # Global credits usable across all agents
    if user.credits_balance >= credit_cost:
        user.credits_balance -= credit_cost

        usage = UsageLog(
            user_id=user.id,
            agent_slug=agent_slug,
            access_type="credits",
            credits_used=credit_cost,
        )

        db.add(usage)
        db.commit()
        db.refresh(user)

        return {
            "access_type": "credits",
            "credits_used": credit_cost,
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
    )

    db.add(usage)
    db.commit()

    return {
        "access_type": "trial",
        "credits_used": 0,
    }