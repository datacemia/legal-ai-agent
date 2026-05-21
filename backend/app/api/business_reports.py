from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.security import get_current_user
from app.utils.billing import check_and_consume_agent_access
from app.services.business_agent.business_weekly_report import (
    generate_weekly_report_for_user,
)
from app.services.enterprise_service import (
    check_enterprise_agent_access,
    consume_enterprise_agent_quota,
    consume_enterprise_credits,
)


router = APIRouter(
    prefix="/business",
    tags=["Business Reports"],
)

BUSINESS_WEEKLY_REPORT_CREDITS = 5


class BusinessWeeklyReportRequest(BaseModel):
    output_language: str = "en"


def _is_global_subscription_user(user: User) -> bool:
    """
    Pro/Premium users get weekly CEO reports included.
    """

    plan = str(getattr(user, "plan", "") or "").lower().strip()
    role = str(getattr(user, "role", "") or "").lower().strip()

    if role in {
        "admin",
        "enterprise_admin",
        "enterprise_member",
    }:
        return True

    if plan in {
        "pro",
        "premium",
        "paid",
        "enterprise",
    }:
        return True

    return False


@router.post("/weekly-report")
def generate_business_weekly_report(
    payload: BusinessWeeklyReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate an AI CEO Weekly Report.

    Monetization rules:
    - Business analysis upload costs 30 credits in the main Business Agent.
    - Weekly CEO Report costs 5 credits for credit/free users.
    - Pro/Premium/Enterprise users get reports included.
    - Enterprise users can also be charged custom enterprise credits if configured.
    """

    output_language = payload.output_language or "en"

    if output_language not in {"en", "fr", "ar"}:
        raise HTTPException(
            status_code=400,
            detail="Unsupported output language. Use en, fr, or ar.",
        )

    enterprise_context = check_enterprise_agent_access(
        db=db,
        user=current_user,
        agent_slug="business",
    )

    if enterprise_context:
        consume_enterprise_agent_quota(
            db=db,
            access=enterprise_context["access"],
        )

        consume_enterprise_credits(
            db=db,
            user=current_user,
            agent_slug="business",
            credits_used=BUSINESS_WEEKLY_REPORT_CREDITS,
            request_type="weekly_report",
        )

    elif not _is_global_subscription_user(current_user):
        check_and_consume_agent_access(
            db=db,
            user=current_user,
            agent_slug="business_report",
            credits_used=BUSINESS_WEEKLY_REPORT_CREDITS,
        )

    report = generate_weekly_report_for_user(
        db=db,
        user_id=current_user.id,
        output_language=output_language,
    )

    if report.get("error") == "No business analysis found.":
        raise HTTPException(
            status_code=404,
            detail="No business analysis found. Analyze a business file first.",
        )

    return report
