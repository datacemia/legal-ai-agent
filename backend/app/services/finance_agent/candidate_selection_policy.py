from __future__ import annotations

import math
import re
from typing import Any, Iterable, Mapping, Optional


OFFICIAL_SUMMARY_FIELDS = (
    "opening_balance",
    "deposits",
    "withdrawals",
    "ending_balance",
)

INCOME_TYPES = {
    "income",
    "credit",
    "deposit",
    "deposits",
    "addition",
    "additions",
}

EXPENSE_TYPES = {
    "expense",
    "debit",
    "withdrawal",
    "withdrawals",
    "subtraction",
    "subtractions",
}


def safe_money(value: Any) -> Optional[float]:
    """
    Convert a monetary value without converting a missing value to zero.

    Supported examples:
      1,234.56
      1.234,56
      (123.45)
      123.45-
      $123.45
      EUR 123,45
    """
    if value is None or isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        number = float(value)
        if not math.isfinite(number):
            return None
        return round(number, 2)

    text = str(value).strip()
    if not text:
        return None

    negative = False

    if text.startswith("(") and text.endswith(")"):
        negative = True
        text = text[1:-1].strip()

    if text.endswith("-"):
        negative = True
        text = text[:-1].strip()

    text = text.replace("\u00a0", "").replace(" ", "")

    # Remove currency symbols and alphabetic currency labels.
    text = re.sub(r"[€$£¥₹₩₽₺₴₦₱฿₪₫]", "", text)
    text = re.sub(
        r"(?i)(USD|EUR|GBP|AUD|CAD|NZD|AED|SAR|QAR|MAD|DZD|ZAR|INR|JPY|CNY|CHF|BDT|XAF|XOF)",
        "",
        text,
    )

    # Keep only numeric punctuation and signs.
    text = re.sub(r"[^0-9,.\-+]", "", text)

    if not text or text in {"-", "+", ".", ","}:
        return None

    if "," in text and "." in text:
        # 1.234,56
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        # 1,234.56
        else:
            text = text.replace(",", "")
    elif "," in text:
        decimal_part = text.rsplit(",", 1)[-1]

        # 1234,56
        if len(decimal_part) in {1, 2}:
            text = text.replace(".", "").replace(",", ".")
        # 1,234
        else:
            text = text.replace(",", "")

    try:
        number = float(text)
    except (TypeError, ValueError):
        return None

    if not math.isfinite(number):
        return None

    if negative:
        number = -abs(number)

    return round(number, 2)


def normalize_official_summary(
    summary: Optional[Mapping[str, Any]],
) -> dict[str, Any]:
    if not summary:
        return {}

    normalized: dict[str, Any] = {}

    aliases = {
        "opening_balance": (
            "opening_balance",
            "beginning_balance",
            "starting_balance",
            "start_balance",
        ),
        "deposits": (
            "deposits",
            "credits",
            "total_credits",
            "income",
            "income_total",
        ),
        "withdrawals": (
            "withdrawals",
            "debits",
            "total_debits",
            "expenses",
            "expense_total",
        ),
        "ending_balance": (
            "ending_balance",
            "closing_balance",
            "end_balance",
        ),
    }

    for canonical_field, possible_fields in aliases.items():
        for field in possible_fields:
            value = safe_money(summary.get(field))
            if value is not None:
                normalized[canonical_field] = value
                break

    for metadata_field in (
        "source",
        "evidence",
        "currency",
        "account_scope",
        "confidence",
    ):
        value = summary.get(metadata_field)
        if value is not None:
            normalized[metadata_field] = value

    return normalized


def summary_has_flow_totals(
    summary: Optional[Mapping[str, Any]],
) -> bool:
    normalized = normalize_official_summary(summary)

    return (
        normalized.get("deposits") is not None
        or normalized.get("withdrawals") is not None
    )


def summary_identity_gap(
    summary: Optional[Mapping[str, Any]],
) -> Optional[float]:
    normalized = normalize_official_summary(summary)

    opening = normalized.get("opening_balance")
    deposits = normalized.get("deposits")
    withdrawals = normalized.get("withdrawals")
    ending = normalized.get("ending_balance")

    if None in (opening, deposits, withdrawals, ending):
        return None

    return round(
        abs((opening + deposits - withdrawals) - ending),
        2,
    )


def summary_quality(
    summary: Optional[Mapping[str, Any]],
) -> tuple[int, int, int, int]:
    normalized = normalize_official_summary(summary)

    flow_count = (
        int(normalized.get("deposits") is not None)
        + int(normalized.get("withdrawals") is not None)
    )

    completeness = sum(
        normalized.get(field) is not None
        for field in OFFICIAL_SUMMARY_FIELDS
    )

    identity_gap = summary_identity_gap(normalized)
    identity_valid = int(
        identity_gap is not None and identity_gap <= 0.05
    )

    evidence = normalized.get("evidence")
    evidence_count = (
        len(evidence)
        if isinstance(evidence, Mapping)
        else 0
    )

    return (
        flow_count,
        identity_valid,
        completeness,
        evidence_count,
    )


def merge_official_summaries(
    current: Optional[Mapping[str, Any]],
    new: Optional[Mapping[str, Any]],
) -> dict[str, Any]:
    """
    Non-destructive merge.

    Missing values never erase known values.
    The strongest summary provides priority values.
    """
    current_normalized = normalize_official_summary(current)
    new_normalized = normalize_official_summary(new)

    if not current_normalized:
        return new_normalized

    if not new_normalized:
        return current_normalized

    current_score = summary_quality(current_normalized)
    new_score = summary_quality(new_normalized)

    if new_score >= current_score:
        preferred = new_normalized
        secondary = current_normalized
    else:
        preferred = current_normalized
        secondary = new_normalized

    merged = dict(secondary)
    merged.update(preferred)

    for field in OFFICIAL_SUMMARY_FIELDS:
        if merged.get(field) is None:
            fallback = secondary.get(field)
            if fallback is not None:
                merged[field] = fallback

    return normalize_official_summary(merged)


def candidate_totals(
    transactions: Iterable[Mapping[str, Any]],
) -> tuple[float, float]:
    income_total = 0.0
    expense_total = 0.0

    for transaction in transactions or []:
        tx_type = str(
            transaction.get("type")
            or transaction.get("transaction_type")
            or ""
        ).strip().lower()

        raw_signed_amount = transaction.get("signed_amount")
        raw_amount = transaction.get("amount")

        signed_amount = safe_money(raw_signed_amount)
        amount = safe_money(raw_amount)

        if signed_amount is not None:
            effective_amount = signed_amount
        elif amount is not None:
            effective_amount = amount
        else:
            continue

        if tx_type in INCOME_TYPES:
            income_total += abs(effective_amount)
        elif tx_type in EXPENSE_TYPES:
            expense_total += abs(effective_amount)
        elif effective_amount > 0:
            income_total += effective_amount
        elif effective_amount < 0:
            expense_total += abs(effective_amount)

    return round(income_total, 2), round(expense_total, 2)


def candidate_official_gaps(
    income_total: Any,
    expense_total: Any,
    official_summary: Optional[Mapping[str, Any]],
) -> tuple[Optional[float], Optional[float], int, float]:
    normalized = normalize_official_summary(official_summary)

    ledger_income = safe_money(income_total) or 0.0
    ledger_expense = safe_money(expense_total) or 0.0

    official_income = normalized.get("deposits")
    official_expense = normalized.get("withdrawals")

    income_gap = (
        round(abs(ledger_income - official_income), 2)
        if official_income is not None
        else None
    )

    expense_gap = (
        round(abs(ledger_expense - official_expense), 2)
        if official_expense is not None
        else None
    )

    compared_components = (
        int(income_gap is not None)
        + int(expense_gap is not None)
    )

    total_gap = round(
        sum(
            gap
            for gap in (income_gap, expense_gap)
            if gap is not None
        ),
        2,
    )

    return (
        income_gap,
        expense_gap,
        compared_components,
        total_gap,
    )


def money_tolerance(
    official_value: Optional[float],
) -> float:
    if official_value is None:
        return 0.05

    return max(
        0.05,
        round(abs(official_value) * 0.00001, 2),
    )


def candidate_reconciliation_status(
    candidate: Mapping[str, Any],
    official_summary: Optional[Mapping[str, Any]],
) -> str:
    normalized = normalize_official_summary(official_summary)

    official_income = normalized.get("deposits")
    official_expense = normalized.get("withdrawals")

    income_gap = safe_money(candidate.get("income_gap"))
    expense_gap = safe_money(candidate.get("expense_gap"))

    available = 0
    matched = 0

    if official_income is not None:
        available += 1

        if (
            income_gap is not None
            and income_gap <= money_tolerance(official_income)
        ):
            matched += 1

    if official_expense is not None:
        available += 1

        if (
            expense_gap is not None
            and expense_gap <= money_tolerance(official_expense)
        ):
            matched += 1

    if available == 0:
        return "unavailable"

    if matched == available:
        return "reconciled"

    if matched > 0:
        return "partially_reconciled"

    return "unreconciled"


def refresh_candidate_against_official_summary(
    candidate: dict[str, Any],
    official_summary: Optional[Mapping[str, Any]],
) -> dict[str, Any]:
    transactions = candidate.get("transactions") or []

    if transactions:
        income_total, expense_total = candidate_totals(
            transactions
        )
    else:
        income_total = (
            safe_money(candidate.get("income_total"))
            or 0.0
        )
        expense_total = (
            safe_money(candidate.get("expense_total"))
            or 0.0
        )

    (
        income_gap,
        expense_gap,
        compared_components,
        total_gap,
    ) = candidate_official_gaps(
        income_total,
        expense_total,
        official_summary,
    )

    candidate["count"] = len(transactions)
    candidate["income_total"] = income_total
    candidate["expense_total"] = expense_total
    candidate["income_gap"] = income_gap
    candidate["expense_gap"] = expense_gap
    candidate["official_components_compared"] = (
        compared_components
    )
    candidate["official_total_gap"] = total_gap
    candidate["reconciliation_status"] = (
        candidate_reconciliation_status(
            candidate,
            official_summary,
        )
    )

    normalized_official = normalize_official_summary(official_summary)
    opening = normalized_official.get("opening_balance")
    ending = normalized_official.get("ending_balance")
    if opening is not None and ending is not None:
        expected_net = round(ending - opening, 2)
        actual_net = round(income_total - expense_total, 2)
        candidate["expected_net"] = expected_net
        candidate["actual_net"] = actual_net
        candidate["balance_net_gap"] = round(abs(actual_net - expected_net), 2)
    else:
        candidate["expected_net"] = None
        candidate["actual_net"] = round(income_total - expense_total, 2)
        candidate["balance_net_gap"] = None

    return candidate


def refresh_candidates_against_official_summary(
    candidates: Iterable[dict[str, Any]],
    official_summary: Optional[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    return [
        refresh_candidate_against_official_summary(
            candidate,
            official_summary,
        )
        for candidate in candidates
    ]


def candidate_selection_key(
    candidate: Mapping[str, Any],
    official_summary: Optional[Mapping[str, Any]],
) -> tuple[Any, ...]:
    has_official = summary_has_flow_totals(
        official_summary
    )

    status = str(
        candidate.get("reconciliation_status")
        or "unavailable"
    )

    status_rank = {
        "reconciled": 0,
        "partially_reconciled": 1,
        "unreconciled": 2,
        "unavailable": 3,
    }.get(status, 3)

    total_gap = candidate.get("official_total_gap")
    if total_gap is None:
        total_gap = float("inf")

    balance_net_gap = candidate.get("balance_net_gap")
    if balance_net_gap is None:
        balance_net_gap = float("inf")

    direction_collapse = bool(
        candidate.get("direction_collapse", False)
    )

    duplicate_count = int(
        candidate.get("duplicate_count", 0) or 0
    )
    invalid_date_count = int(
        candidate.get("invalid_date_count", 0) or 0
    )
    balance_error_count = int(
        candidate.get("balance_error_count", 0) or 0
    )

    count = int(
        candidate.get("count")
        or len(candidate.get("transactions") or [])
    )

    structural_score = float(
        candidate.get(
            "structural_score",
            candidate.get("score", 0.0),
        )
        or 0.0
    )

    if has_official:
        return (
            status_rank,
            direction_collapse,
            float(total_gap),
            float(balance_net_gap),
            duplicate_count,
            invalid_date_count,
            balance_error_count,
            -count,
            structural_score,
        )

    return (
        direction_collapse,
        float(balance_net_gap),
        duplicate_count,
        invalid_date_count,
        balance_error_count,
        structural_score,
        -count,
    )


def choose_best_candidate(
    candidates: Iterable[dict[str, Any]],
    official_summary: Optional[Mapping[str, Any]],
) -> Optional[dict[str, Any]]:
    refreshed = refresh_candidates_against_official_summary(
        candidates,
        official_summary,
    )

    usable = [
        candidate
        for candidate in refreshed
        if candidate.get("transactions")
        or int(candidate.get("count", 0) or 0) > 0
    ]

    if not usable:
        return None

    selected = min(
        usable,
        key=lambda candidate: candidate_selection_key(
            candidate,
            official_summary,
        ),
    )

    status = selected.get(
        "reconciliation_status",
        "unavailable",
    )

    if status == "reconciled":
        reason = "reconciled_official_summary"
    elif status == "partially_reconciled":
        reason = "partially_reconciled_official_summary"
    elif summary_has_flow_totals(official_summary):
        reason = (
            "best_candidate_despite_official_summary_mismatch"
        )
    else:
        reason = (
            "best_structural_quality_without_official_summary"
        )

    selected["selection_reason"] = reason

    return selected


def looks_like_multi_account_statement(
    text: str,
) -> bool:
    lowered = (text or "").lower()

    markers = (
        "summary of accounts",
        "combined statement of accounts",
        "checking/prepaid and savings",
        "multiple accounts",
        "account balance summary",
    )

    marker_hits = sum(
        marker in lowered
        for marker in markers
    )

    account_number_hits = len(
        re.findall(
            r"\baccount\s+(?:number|no\.?)\b",
            lowered,
        )
    )

    activity_summary_hits = lowered.count(
        "activity summary"
    )
    ending_balance_hits = lowered.count(
        "ending balance"
    )

    return (
        marker_hits >= 1
        and (
            account_number_hits >= 2
            or activity_summary_hits >= 2
            or ending_balance_hits >= 3
        )
    )


def build_final_finance_summaries(
    transactions: Iterable[Mapping[str, Any]],
    official_summary: Optional[Mapping[str, Any]],
    parser_name: Optional[str] = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    transactions_list = list(transactions or [])

    income_total, expense_total = candidate_totals(
        transactions_list
    )

    normalized_official = normalize_official_summary(
        official_summary
    )

    (
        income_gap,
        expense_gap,
        compared_components,
        total_gap,
    ) = candidate_official_gaps(
        income_total,
        expense_total,
        normalized_official,
    )

    temporary_candidate = {
        "income_gap": income_gap,
        "expense_gap": expense_gap,
    }

    reconciliation_status = (
        candidate_reconciliation_status(
            temporary_candidate,
            normalized_official,
        )
    )

    ledger_summary = {
        "deposits": income_total,
        "withdrawals": expense_total,
        "transaction_count": len(transactions_list),
        "source": parser_name,
    }

    reconciliation = {
        "income_gap": income_gap,
        "expense_gap": expense_gap,
        "total_gap": total_gap,
        "official_components_compared": compared_components,
        "status": reconciliation_status,
    }

    return (
        ledger_summary,
        normalized_official,
        reconciliation,
    )
