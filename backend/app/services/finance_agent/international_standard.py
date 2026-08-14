"""Conservative production hardening for international bank statements.

This module is deliberately bank-agnostic.  It normalizes Unicode/OCR text and
transaction output across French, English and Arabic without replacing the
existing layout-specific parsers.  Existing parser decisions remain authoritative.
"""
from __future__ import annotations

import re
import unicodedata
from datetime import datetime
from typing import Any, Iterable

_ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
_BIDI_CONTROLS = dict.fromkeys(map(ord, "\u061c\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069"), None)
_SPACE_RE = re.compile(r"[\t\u00a0\u1680\u2000-\u200a\u202f\u205f\u3000]+")
_MULTI_SPACE_RE = re.compile(r" {2,}")
_MULTI_BLANK_RE = re.compile(r"\n{3,}")

# Semantic concepts, not bank names.  Variants cover FR / EN / AR and common OCR.
LABELS = {
    "debit": ("debit", "débit", "withdrawal", "money out", "مدين", "خصم", "سحب"),
    "credit": ("credit", "crédit", "deposit", "money in", "دائن", "إيداع", "ايداع"),
    "balance": ("balance", "solde", "رصيد"),
    "opening_balance": (
        "opening balance", "beginning balance", "starting balance",
        "solde initial", "solde d'ouverture", "الرصيد الافتتاحي", "رصيد أول المدة",
    ),
    "closing_balance": (
        "closing balance", "ending balance", "final balance",
        "solde final", "solde de clôture", "الرصيد الختامي", "رصيد آخر المدة",
    ),
    "date": ("date", "operation date", "transaction date", "date opération", "تاريخ", "تاريخ العملية"),
    "description": ("description", "details", "narrative", "libellé", "nature", "بيان", "الوصف", "تفاصيل"),
    "amount": ("amount", "montant", "المبلغ"),
}


def normalize_statement_text(text: str) -> str:
    """Normalize encoding/OCR artifacts while preserving line and column order."""
    value = unicodedata.normalize("NFKC", str(text or ""))
    value = value.translate(_ARABIC_DIGITS).translate(_BIDI_CONTROLS)
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = _SPACE_RE.sub(" ", value)
    value = "\n".join(_MULTI_SPACE_RE.sub(" ", line).strip() for line in value.splitlines())
    return _MULTI_BLANK_RE.sub("\n\n", value).strip()


def _safe_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number != number or number in (float("inf"), float("-inf")):
        return None
    return round(number, 2)


def _valid_iso_date(value: Any) -> bool:
    """Accept structurally valid transaction dates without inferring locale.

    This validator does not reinterpret ambiguous numeric dates. It only
    verifies that the value already matches one of the date representations
    supported by the extraction contract.
    """

    text = str(value or "").strip()

    if not text:
        return False

    supported_formats = (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y.%m.%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d.%m.%Y",
        "%m-%d-%Y",
        "%m/%d/%Y",
        "%m.%d.%Y",
    )

    for date_format in supported_formats:
        try:
            datetime.strptime(text, date_format)
            return True
        except ValueError:
            continue

    return False


def standardize_transactions(
    transactions: Iterable[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    """Return a stable transaction contract without changing parser economics.

    Invalid rows are discarded. Existing signed amounts and locked parser
    fields are preserved.

    Rows are deduplicated only when both their strong source provenance and
    their complete normalized economic identity are identical.
    """

    source_transactions = list(transactions or [])
    output: list[dict[str, Any]] = []

    seen_provenance: set[
        tuple[
            str,
            str,
            str,
            float,
            str,
            str,
        ]
    ] = set()

    audit = {
        "input_count": len(source_transactions),
        "rejected_non_dict": 0,
        "rejected_invalid_amount": 0,
        "rejected_zero_amount": 0,
        "rejected_invalid_date": 0,
        "rejected_duplicate": 0,
        "output_count": 0,
    }

    samples = {
        "invalid_amount": [],
        "zero_amount": [],
        "invalid_date": [],
        "duplicate": [],
    }

    for index, original in enumerate(source_transactions):
        if not isinstance(original, dict):
            audit["rejected_non_dict"] += 1
            continue

        tx = dict(original)

        raw_amount = tx.get("signed_amount")

        if raw_amount is None:
            raw_amount = tx.get("amount")

        amount = _safe_float(raw_amount)

        if amount is None:
            audit["rejected_invalid_amount"] += 1

            if len(samples["invalid_amount"]) < 10:
                samples["invalid_amount"].append(
                    {
                        "index": index,
                        "date": tx.get("date"),
                        "amount": tx.get("amount"),
                        "signed_amount": tx.get("signed_amount"),
                        "description": str(
                            tx.get("description") or ""
                        )[:120],
                    }
                )

            continue

        if amount == 0:
            audit["rejected_zero_amount"] += 1

            if len(samples["zero_amount"]) < 10:
                samples["zero_amount"].append(
                    {
                        "index": index,
                        "date": tx.get("date"),
                        "amount": tx.get("amount"),
                        "signed_amount": tx.get("signed_amount"),
                        "description": str(
                            tx.get("description") or ""
                        )[:120],
                    }
                )

            continue

        if not _valid_iso_date(tx.get("date")):
            audit["rejected_invalid_date"] += 1

            if len(samples["invalid_date"]) < 10:
                samples["invalid_date"].append(
                    {
                        "index": index,
                        "date": tx.get("date"),
                        "amount": amount,
                        "description": str(
                            tx.get("description") or ""
                        )[:120],
                    }
                )

            continue

        description = normalize_statement_text(
            str(tx.get("description") or "")
        )

        description = " ".join(
            description.split()
        )[:500]

        if not description:
            description = "Transaction"

        locked_type = str(
            tx.get("locked_type") or ""
        ).lower()

        current_type = str(
            tx.get("type") or ""
        ).lower()

        if locked_type in {"income", "expense"}:
            tx_type = locked_type

        elif current_type in {"income", "expense"}:
            tx_type = current_type

        else:
            tx_type = (
                "income"
                if amount > 0
                else "expense"
            )

        if (
            tx_type == "income"
            and amount < 0
            and not tx.get("locked_type")
        ):
            tx_type = "expense"

        elif (
            tx_type == "expense"
            and amount > 0
            and not tx.get("locked_type")
        ):
            tx_type = "income"

        currency = str(
            tx.get("currency") or "UNKNOWN"
        ).upper().strip()

        if not re.fullmatch(
            r"[A-Z]{3}|UNKNOWN|MULTI",
            currency,
        ):
            currency = "UNKNOWN"

        date_value = str(tx["date"])

        tx.update(
            {
                "date": date_value,
                "description": description,
                "amount": amount,
                "signed_amount": amount,
                "type": tx_type,
                "currency": currency,
            }
        )

        provenance = (
            tx.get("source_span")
            or tx.get("source_line_id")
            or tx.get("source_row_id")
        )

        parser_family = str(
            tx.get("parser_family") or ""
        )

        if provenance not in (None, ""):
            provenance_key = (
                parser_family,
                repr(provenance),
                date_value,
                amount,
                tx_type,
                description,
            )

            if provenance_key in seen_provenance:
                audit["rejected_duplicate"] += 1

                if len(samples["duplicate"]) < 10:
                    samples["duplicate"].append(
                        {
                            "index": index,
                            "date": date_value,
                            "amount": amount,
                            "type": tx_type,
                            "parser_family": parser_family,
                            "provenance": repr(provenance),
                            "description": description[:120],
                        }
                    )

                continue

            seen_provenance.add(provenance_key)

        output.append(tx)

    audit["output_count"] = len(output)

    print(
        "STANDARDIZE_TRANSACTIONS_AUDIT",
        {
            **audit,
            "samples": samples,
        },
    )

    return output
def detect_supported_languages(text: str) -> list[str]:
    """Diagnostic only: return languages visibly present in a statement."""
    normalized = normalize_statement_text(text).casefold()
    found: list[str] = []
    if re.search(r"[\u0600-\u06ff]", normalized):
        found.append("ar")
    if any(token in normalized for token in ("solde", "débit", "crédit", "libellé", "relevé")):
        found.append("fr")
    if any(token in normalized for token in ("balance", "debit", "credit", "statement", "transaction")):
        found.append("en")
    return found or ["und"]
