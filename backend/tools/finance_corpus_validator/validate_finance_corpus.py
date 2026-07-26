#!/usr/bin/env python3
r"""Runexa Finance corpus validator.

Run from the backend project root, for example on Windows:

    py tools\finance_corpus_validator\validate_finance_corpus.py \
        --corpus "C:\\Users\\rachi\\legal-ai-agent\\backend\\ejjami" \
        --backend "C:\\Users\\rachi\\legal-ai-agent\\backend" \
        --expected tools\finance_corpus_validator\expected_values.csv \
        --output validation_results

The validator:
1. extracts official statement totals when a trustworthy summary is present;
2. merges manually reviewed truth values from expected_values.csv;
3. runs the current Runexa extractor;
4. compares counts, income, expenses, balances, currency and dates;
5. writes CSV, JSON and HTML reports;
6. stores every extracted transaction in agent_transactions.json for debugging.

Auto-detected values are accepted as ground truth only when the official summary
reconciles: opening + deposits - withdrawals == closing within tolerance.
"""
from __future__ import annotations

import argparse
import csv
import html
import importlib
import json
import math
import os
import re
import sys
import traceback
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Optional

VALIDATOR_VERSION = "v8-component-account-summary-truth"

try:
    import fitz  # PyMuPDF
except ImportError as exc:
    raise SystemExit("PyMuPDF is required: pip install pymupdf") from exc


MONEY_TOKEN = r"[-+]?\(?\d{1,3}(?:[\s,.']\d{3})*(?:[,.]\d{2,3})\)?|[-+]?\(?\d+(?:[,.]\d{2,3})\)?"
CURRENCY_CODES = (
    "USD", "EUR", "GBP", "MAD", "SAR", "AED", "QAR", "KWD", "BHD", "OMR",
    "CAD", "AUD", "CHF", "JPY", "CNY", "INR", "TRY", "DZD", "TND", "EGP",
    "JOD", "NGN", "ZAR"
)


@dataclass
class Truth:
    source: str = "none"
    confidence: str = "none"
    currency: Optional[str] = None
    opening_balance: Optional[float] = None
    deposits: Optional[float] = None
    withdrawals: Optional[float] = None
    closing_balance: Optional[float] = None
    transaction_count: Optional[int] = None
    credit_count: Optional[int] = None
    debit_count: Optional[int] = None
    notes: str = ""


@dataclass
class AgentResult:
    status: str = "error"
    currency: Optional[str] = None
    income: float = 0.0
    expenses: float = 0.0
    net: float = 0.0
    transaction_count: int = 0
    income_count: int = 0
    expense_count: int = 0
    opening_balance: Optional[float] = None
    closing_balance: Optional[float] = None
    invalid_date_count: int = 0
    hijri_primary_date_count: int = 0
    error: str = ""


def parse_money(value: Any) -> Optional[float]:
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    negative = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    s = re.sub(r"[^0-9,.'+\-\s]", "", s).replace("'", "").replace(" ", "")
    if not re.search(r"\d", s):
        return None

    # Infer decimal separator from the final punctuation group.
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        tail = s.rsplit(",", 1)[1]
        s = s.replace(",", ".") if len(tail) in (2, 3) else s.replace(",", "")
    elif "." in s:
        parts = s.split(".")
        if len(parts) > 2:
            s = "".join(parts[:-1]) + "." + parts[-1]

    try:
        number = float(s)
        return -abs(number) if negative else number
    except ValueError:
        return None


def read_pdf_text(path: Path) -> str:
    with fitz.open(path) as doc:
        return "\n".join(page.get_text("text") or "" for page in doc)


def detect_currency(text: str) -> Optional[str]:
    upper = text.upper()
    counts = {code: len(re.findall(rf"\b{code}\b", upper)) for code in CURRENCY_CODES}
    symbols = {
        "MAD": ["DH", "DHS"],
        "SAR": ["RIYAL", "ريال"],
        "EUR": ["€"],
        "GBP": ["£"],
    }
    for code, tokens in symbols.items():
        counts[code] += sum(upper.count(token.upper()) for token in tokens)

    # A bare "$" is ambiguous (USD, AUD, CAD, NZD, etc.) and must not
    # determine the currency by itself. Count only explicit US-dollar markers.
    counts["USD"] += len(re.findall(r"(?<![A-Z])US\$(?![A-Z])|\bUS\s+DOLLARS?\b", upper))

    best = max(counts, key=counts.get)
    return best if counts[best] else None


def find_labeled_money(text: str, labels: Iterable[str], window: int = 100) -> Optional[float]:
    for label in labels:
        for match in re.finditer(label, text, flags=re.I | re.S):
            chunk = text[match.end(): match.end() + window]
            money = re.search(MONEY_TOKEN, chunk)
            if money:
                value = parse_money(money.group(0))
                if value is not None:
                    return abs(value)
    return None


def find_labeled_count_and_total(text: str, section_labels: Iterable[str]) -> tuple[Optional[int], Optional[float]]:
    count_marker = re.compile(
        r"(?:count|number(?:\s+of)?|transactions?|nombre|nb\.?|عدد)\s*[:#-]?\s*"
        rf"(?P<count>\d{{1,5}})\b",
        flags=re.I,
    )

    for label in section_labels:
        match = re.search(label, text, flags=re.I | re.S)
        if not match:
            continue
        chunk = text[match.end():match.end() + 250]

        # Only accept a transaction count when an explicit count marker is
        # present. Otherwise the first number after the label is usually the
        # monetary total itself (for example: "Total credits $7,981.25").
        count_match = count_marker.search(chunk)
        if not count_match:
            continue

        count_candidate = int(count_match.group("count"))
        remainder = chunk[count_match.end():]
        total_match = re.search(MONEY_TOKEN, remainder)
        if not total_match:
            continue
        total_candidate = parse_money(total_match.group(0))
        if total_candidate is not None and 0 <= count_candidate <= 10000 and total_candidate >= 0:
            return count_candidate, abs(total_candidate)

    return None, None





def find_sequential_activity_summary(text: str) -> dict[str, Any]:
    """Extract the first complete sequential Activity summary block."""
    lines = [
        " ".join(line.split())
        for line in str(text or "").splitlines()
        if " ".join(line.split())
    ]

    field_patterns = {
        "opening_balance": re.compile(r"^(?:beginning|opening)\s+balance", re.I),
        "deposits": re.compile(r"^(?:deposits(?:/additions)?|total\s+credits?)$", re.I),
        "withdrawals": re.compile(r"^(?:withdrawals(?:/subtractions)?|total\s+debits?)$", re.I),
        "closing_balance": re.compile(r"^(?:ending|closing)\s+balance", re.I),
    }

    for i, line in enumerate(lines):
        if line.lower() != "activity summary":
            continue

        block = lines[i+1:i+16]
        result = {}

        for j, candidate in enumerate(block):
            for field, pattern in field_patterns.items():
                if field in result:
                    continue
                if pattern.search(candidate):
                    for value_line in block[j+1:j+4]:
                        m = re.search(MONEY_TOKEN, value_line)
                        if m:
                            value = parse_money(m.group(0))
                            if value is not None:
                                result[field] = abs(value)
                                break

        if all(k in result for k in ("opening_balance","deposits","withdrawals","closing_balance")):
            gap = abs(
                result["opening_balance"]
                + result["deposits"]
                - result["withdrawals"]
                - result["closing_balance"]
            )
            result["accounting_identity_gap"] = gap
            result["accounting_identity_valid"] = gap <= 1.0
            return result

    return {}


def find_parallel_accounting_summary(text: str) -> dict[str, Any]:
    """Map adjacent summary values to EN/FR/AR headers by column order."""
    lines = [" ".join(x.split()) for x in str(text or "").splitlines() if " ".join(x.split())]
    labels = [
        ("opening_balance", ("opening balance", "beginning balance", "solde initial", "solde précédent", "solde precedent", "الرصيد الافتتاحي")),
        ("deposits", ("total credits", "deposits/additions", "argent entrant", "total des crédits", "total des credits", "إجمالي الدائن")),
        ("withdrawals", ("total debits", "withdrawals/subtractions", "argent sortant", "total des débits", "total des debits", "إجمالي المدين")),
        ("closing_balance", ("closing balance", "ending balance", "solde final", "nouveau solde", "الرصيد الختامي")),
    ]
    token_re = re.compile(
        r"(?<![A-Za-z0-9])[-+]?\s*(?:[$€£¥]|(?:USD|EUR|GBP|AUD|CAD|JPY|SAR|AED|MAD)\s*)?"
        r"(?:\d{1,3}(?:[,\u00a0 ]\d{3})+|\d+)(?:[.,]\d{1,3})(?![A-Za-z0-9])",
        re.I,
    )
    for i, line in enumerate(lines):
        low = line.casefold()
        positions = []
        for key, variants in labels:
            hits = [low.find(v.casefold()) for v in variants if v.casefold() in low]
            if hits:
                positions.append((min(hits), key))
        if len(positions) < 4:
            continue
        positions.sort()
        for value_line in lines[i + 1:i + 4]:
            vals = []
            for m in token_re.finditer(value_line):
                value = parse_money(m.group(0))
                if value is not None:
                    vals.append(abs(value))
            if len(vals) < 4:
                continue
            out = {positions[j][1]: vals[j] for j in range(4)}
            gap = abs(out["opening_balance"] + out["deposits"] - out["withdrawals"] - out["closing_balance"])
            out["accounting_identity_gap"] = round(gap, 2)
            out["accounting_identity_valid"] = gap <= max(1.0, abs(out["closing_balance"]) * 0.0001)
            return out
    return {}


def find_component_account_summary(text: str) -> dict[str, Any]:
    """Extract account summaries whose credits/debits are split across categories.

    Example:
        Beginning Balance
        Deposits
        Electronic Deposits
        Other Credits
        Electronic Payments
        Other Withdrawals
        Ending Balance

    The parser searches only a local summary block and sums component rows.
    It returns values only when the accounting identity reconciles.
    """
    lines = [
        " ".join(line.split())
        for line in str(text or "").splitlines()
        if " ".join(line.split())
    ]

    opening_patterns = (
        re.compile(r"^(?:beginning|opening|previous)\s+balance\b", re.I),
        re.compile(r"^statement\s+opening\s+balance\b", re.I),
    )
    closing_patterns = (
        re.compile(r"^(?:ending|closing|new)\s+balance\b", re.I),
    )
    credit_patterns = (
        re.compile(r"^deposits?\b", re.I),
        re.compile(r"^electronic\s+deposits?\b", re.I),
        re.compile(r"^other(?:s)?\s+credits?\b", re.I),
        re.compile(r"^total\s+credits?\b", re.I),
        re.compile(r"^credits?\b", re.I),
    )
    debit_patterns = (
        re.compile(r"^electronic\s+payments?\b", re.I),
        re.compile(r"^other\s+withdrawals?\b", re.I),
        re.compile(r"^withdrawals?\b", re.I),
        re.compile(r"^total\s+debits?\b", re.I),
        re.compile(r"^debits?\b", re.I),
    )
    block_starts = (
        re.compile(r"^account\s+summ(?:ary|yar)\b", re.I),
        re.compile(r"^account\s+summary\b", re.I),
    )
    block_ends = (
        re.compile(r"^(?:daily\s+account\s+activity|transaction\s+details|transaction\s+history)\b", re.I),
    )

    def first_money(line: str) -> Optional[float]:
        match = re.search(MONEY_TOKEN, line)
        if not match:
            return None
        value = parse_money(match.group(0))
        return abs(value) if value is not None else None

    for start, line in enumerate(lines):
        if not any(pattern.search(line) for pattern in block_starts):
            continue

        block: list[str] = []
        for candidate in lines[start + 1:start + 35]:
            if any(pattern.search(candidate) for pattern in block_ends):
                break
            block.append(candidate)

        opening = None
        closing = None
        credits: list[float] = []
        debits: list[float] = []

        for candidate in block:
            value = first_money(candidate)
            if value is None:
                continue

            if opening is None and any(pattern.search(candidate) for pattern in opening_patterns):
                opening = value
                continue
            if closing is None and any(pattern.search(candidate) for pattern in closing_patterns):
                closing = value
                continue
            if any(pattern.search(candidate) for pattern in credit_patterns):
                credits.append(value)
                continue
            if any(pattern.search(candidate) for pattern in debit_patterns):
                debits.append(value)

        if opening is None or closing is None or not credits or not debits:
            continue

        deposits = round(sum(credits), 2)
        withdrawals = round(sum(debits), 2)
        gap = abs(opening + deposits - withdrawals - closing)
        tolerance = max(1.0, abs(closing) * 0.0001)

        if gap <= tolerance:
            return {
                "opening_balance": opening,
                "deposits": deposits,
                "withdrawals": withdrawals,
                "closing_balance": closing,
                "accounting_identity_gap": round(gap, 2),
                "accounting_identity_valid": True,
                "credit_component_count": len(credits),
                "debit_component_count": len(debits),
            }

    return {}


def extract_official_truth(text: str, tolerance: float) -> Truth:
    compact = re.sub(r"[\t ]+", " ", text)
    currency = detect_currency(compact)

    # Sequential summaries place each label and value on separate lines.
    # Use the first complete account block on combined statements.
    sequential = find_sequential_activity_summary(text)
    if sequential:
        opening = sequential.get("opening_balance")
        deposits = sequential.get("deposits")
        withdrawals = sequential.get("withdrawals")
        closing = sequential.get("closing_balance")
        truth = Truth(
            source="auto_sequential_activity_summary",
            confidence="candidate",
            currency=currency,
            opening_balance=opening,
            deposits=deposits,
            withdrawals=withdrawals,
            closing_balance=closing,
        )
        gap = abs(opening + deposits - withdrawals - closing)
        if gap <= tolerance:
            truth.confidence = "verified_reconciled"
            truth.notes = f"sequential official summary reconciled; gap={gap:.2f}"
        else:
            truth.confidence = "rejected_unreconciled"
            truth.notes = f"sequential official summary did not reconcile; gap={gap:.2f}"
            truth.opening_balance = None
            truth.deposits = None
            truth.withdrawals = None
            truth.closing_balance = None
        return truth

    # Some official summaries split deposits and withdrawals across several
    # category rows. Sum those rows only when the complete summary reconciles.
    component = find_component_account_summary(text)
    if component:
        opening = component["opening_balance"]
        deposits = component["deposits"]
        withdrawals = component["withdrawals"]
        closing = component["closing_balance"]
        gap = abs(opening + deposits - withdrawals - closing)
        return Truth(
            source="auto_component_account_summary",
            confidence="verified_reconciled",
            currency=currency,
            opening_balance=opening,
            deposits=deposits,
            withdrawals=withdrawals,
            closing_balance=closing,
            notes=(
                "component official summary reconciled; "
                f"credits={component.get('credit_component_count', 0)}, "
                f"debits={component.get('debit_component_count', 0)}, "
                f"gap={gap:.2f}"
            ),
        )

    # A detected four-column accounting summary is authoritative as a unit.
    # Never mix its fields with loose label matching: that can assign the same
    # nearby number to opening, credits, debits and closing and falsely produce
    # a zero reconciliation gap.
    parallel = find_parallel_accounting_summary(text)
    if parallel:
        opening = parallel.get("opening_balance")
        deposits = parallel.get("deposits")
        withdrawals = parallel.get("withdrawals")
        closing = parallel.get("closing_balance")
        truth = Truth(
            source="auto_parallel_accounting_summary",
            confidence="candidate",
            currency=currency,
            opening_balance=opening,
            deposits=deposits,
            withdrawals=withdrawals,
            closing_balance=closing,
        )
        gap = abs((opening or 0) + (deposits or 0) - (withdrawals or 0) - (closing or 0))
        if gap <= tolerance:
            truth.confidence = "verified_reconciled"
            truth.notes = f"positional official summary reconciled; gap={gap:.2f}"
        else:
            truth.confidence = "rejected_unreconciled"
            truth.notes = f"positional official summary did not reconcile; gap={gap:.2f}"
            truth.opening_balance = truth.deposits = truth.withdrawals = truth.closing_balance = None
        return truth

    opening = find_labeled_money(compact, [
        r"Opening\s*Balance", r"Beginning\s*Balance", r"Solde\s+initial",
        r"Ancien\s+solde", r"الرصيد\s*الافتتاحي", r"رصيد\s*افتتاحي"
    ])
    closing = find_labeled_money(compact, [
        r"Closing\s*Balance", r"Ending\s*Balance", r"Nouveau\s+solde",
        r"Solde\s+final", r"رصيد\s*الإقفال", r"الرصيد\s*الختامي"
    ])

    debit_count, withdrawals = find_labeled_count_and_total(compact, [
        r"Withdrawals", r"Total\s+Debits?", r"Retraits?", r"D[ée]bits?", r"سحوبات", r"مدين"
    ])
    credit_count, deposits = find_labeled_count_and_total(compact, [
        r"Deposits", r"Total\s+Credits?", r"Cr[ée]dits?", r"Versements?", r"إيداعات", r"دائن"
    ])

    withdrawals = withdrawals or find_labeled_money(compact, [
        r"Total\s+(?:withdrawals|debits?)", r"Retraits?\s+totaux?", r"Total\s+des\s+d[ée]bits?",
        r"إجمالي\s*(?:السحوبات|المدين)"
    ])
    deposits = deposits or find_labeled_money(compact, [
        r"Total\s+(?:deposits|credits?)", r"D[ée]p[ôo]ts?\s+totaux?", r"Total\s+des\s+cr[ée]dits?",
        r"إجمالي\s*(?:الإيداعات|الدائن)"
    ])

    truth = Truth(
        source="auto_official_summary",
        confidence="candidate",
        currency=currency,
        opening_balance=opening,
        deposits=deposits,
        withdrawals=withdrawals,
        closing_balance=closing,
        credit_count=credit_count,
        debit_count=debit_count,
        transaction_count=(credit_count + debit_count) if credit_count is not None and debit_count is not None else None,
    )

    values = (opening, deposits, withdrawals, closing)
    if all(v is not None for v in values):
        # Guard against cross-label leakage where one nearby amount is copied
        # into all four fields and therefore appears to reconcile perfectly.
        if len({round(float(v), 2) for v in values}) == 1:
            truth.confidence = "rejected_ambiguous"
            truth.notes = "all four official-summary fields resolved to the same amount; rejected as label leakage"
            truth.opening_balance = truth.deposits = truth.withdrawals = truth.closing_balance = None
            truth.transaction_count = truth.credit_count = truth.debit_count = None
            return truth
        gap = abs((opening or 0) + (deposits or 0) - (withdrawals or 0) - (closing or 0))
        if gap <= tolerance:
            truth.confidence = "verified_reconciled"
            truth.notes = f"official summary reconciled; gap={gap:.2f}"
        else:
            truth.confidence = "rejected_unreconciled"
            truth.notes = f"official summary did not reconcile; gap={gap:.2f}"
            truth.opening_balance = truth.deposits = truth.withdrawals = truth.closing_balance = None
            truth.transaction_count = truth.credit_count = truth.debit_count = None
    else:
        missing = [
            name
            for name, value in {
                "opening": opening,
                "deposits": deposits,
                "withdrawals": withdrawals,
                "closing": closing,
            }.items()
            if value is None
        ]

        if len(missing) == 1:
            missing_field = missing[0]

            if missing_field == "opening":
                opening = closing - deposits + withdrawals
            elif missing_field == "deposits":
                deposits = closing - opening + withdrawals
            elif missing_field == "withdrawals":
                withdrawals = opening + deposits - closing
            elif missing_field == "closing":
                closing = opening + deposits - withdrawals

            gap = abs(opening + deposits - withdrawals - closing)

            if gap <= tolerance:
                truth.opening_balance = opening
                truth.deposits = deposits
                truth.withdrawals = withdrawals
                truth.closing_balance = closing
                truth.confidence = "verified_derived_reconciled"
                truth.source = f"auto_derived_{missing_field}"
                truth.notes = (
                    f"{missing_field} derived from three official summary values; "
                    f"gap={gap:.2f}"
                )
            else:
                truth.confidence = "partial_candidate"
                truth.notes = "official summary incomplete; manual review required"
        else:
            truth.confidence = "partial_candidate"
            truth.notes = "official summary incomplete; manual review required"
    return truth


def load_manual_truth(path: Optional[Path]) -> dict[str, Truth]:
    if not path or not path.exists():
        return {}
    rows: dict[str, Truth] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            filename = (row.get("filename") or "").strip()
            if not filename or filename.startswith("#"):
                continue
            def f(name: str) -> Optional[float]:
                return parse_money(row.get(name))
            def i(name: str) -> Optional[int]:
                val = f(name)
                return int(val) if val is not None else None
            rows[filename.casefold()] = Truth(
                source="manual_csv",
                confidence=(row.get("confidence") or "manual").strip(),
                currency=(row.get("currency") or "").strip().upper() or None,
                opening_balance=f("opening_balance"),
                deposits=f("deposits"),
                withdrawals=f("withdrawals"),
                closing_balance=f("closing_balance"),
                transaction_count=i("transaction_count"),
                credit_count=i("credit_count"),
                debit_count=i("debit_count"),
                notes=(row.get("notes") or "").strip(),
            )
    return rows


def merge_truth(auto: Truth, manual: Optional[Truth]) -> Truth:
    if not manual:
        return auto
    merged = Truth(**asdict(auto))
    for field in (
        "currency", "opening_balance", "deposits", "withdrawals", "closing_balance",
        "transaction_count", "credit_count", "debit_count", "notes"
    ):
        value = getattr(manual, field)
        if value not in (None, ""):
            setattr(merged, field, value)
    merged.source = "manual_csv"
    merged.confidence = manual.confidence or "manual"
    return merged


def import_agent(backend: Path):
    sys.path.insert(0, str(backend))
    statement_parser = importlib.import_module("app.services.finance_agent.statement_parser")
    extractor = importlib.import_module("app.services.finance_agent.transaction_extractor")
    return statement_parser, extractor


def safe_float(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def tx_amount(tx: dict[str, Any]) -> float:
    return safe_float(tx.get("signed_amount") if tx.get("signed_amount") is not None else tx.get("amount"))


def is_kpi_transaction(tx: dict[str, Any]) -> bool:
    if tx.get("excluded_from_financial_kpis") or tx.get("is_internal_transfer"):
        return False
    typ = str(tx.get("type") or "").lower()
    return typ in {"income", "expense"} and abs(tx_amount(tx)) > 0


def parse_iso_date(value: Any) -> tuple[bool, bool]:
    s = str(value or "").strip()
    if not s:
        return False, False
    hijri = bool(re.match(r"^14\d{2}-\d{2}-\d{2}$", s))
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True, hijri
    except ValueError:
        return False, hijri


def run_agent(path: Path, statement_parser: Any, extractor: Any) -> tuple[AgentResult, list[dict[str, Any]]]:
    try:
        text = statement_parser.extract_statement_text_from_path(str(path))
        transactions = extractor.extract_transactions_from_pdf_path(str(path), text)
        if hasattr(extractor, "append_fx_fee_transactions"):
            transactions = extractor.append_fx_fee_transactions(transactions)
        transactions = list(transactions or [])
        kpi = [tx for tx in transactions if isinstance(tx, dict) and is_kpi_transaction(tx)]

        income_rows = [tx for tx in kpi if str(tx.get("type")).lower() == "income"]
        expense_rows = [tx for tx in kpi if str(tx.get("type")).lower() == "expense"]
        income = round(sum(abs(tx_amount(tx)) for tx in income_rows), 2)
        expenses = round(sum(abs(tx_amount(tx)) for tx in expense_rows), 2)

        currencies = [str(tx.get("currency") or "").upper() for tx in transactions if tx.get("currency")]
        currency = max(set(currencies), key=currencies.count) if currencies else detect_currency(text)

        dates = [parse_iso_date(tx.get("date")) for tx in transactions]
        invalid_dates = sum(1 for valid, _ in dates if not valid)
        hijri_dates = sum(1 for _, hijri in dates if hijri)

        balances = []
        for tx in transactions:
            raw = tx.get("balance") if tx.get("balance") is not None else tx.get("_balance")
            val = parse_money(raw)
            if val is not None:
                balances.append(val)

        result = AgentResult(
            status="ok" if transactions else "no_transactions",
            currency=currency,
            income=income,
            expenses=expenses,
            net=round(income - expenses, 2),
            transaction_count=len(transactions),
            income_count=len(income_rows),
            expense_count=len(expense_rows),
            opening_balance=balances[0] if balances else None,
            closing_balance=balances[-1] if balances else None,
            invalid_date_count=invalid_dates,
            hijri_primary_date_count=hijri_dates,
        )
        serializable_transactions = [tx for tx in transactions if isinstance(tx, dict)]
        return result, serializable_transactions
    except Exception as exc:
        return AgentResult(status="error", error=f"{type(exc).__name__}: {exc}"), []


def delta(actual: Optional[float], expected: Optional[float]) -> Optional[float]:
    if actual is None or expected is None:
        return None
    return round(actual - expected, 2)


def ratio_error(actual: Optional[float], expected: Optional[float]) -> Optional[float]:
    if actual is None or expected is None:
        return None
    if abs(expected) < 0.005:
        return 0.0 if abs(actual) < 0.005 else math.inf
    return round(abs(actual - expected) / abs(expected), 6)


def classify(row: dict[str, Any], amount_tolerance: float, ratio_tolerance: float, count_tolerance: int) -> str:
    if row["agent_status"] != "ok":
        return "FAIL_AGENT"
    if row["truth_confidence"] not in {"verified_reconciled", "verified_derived_reconciled", "manual", "reviewed", "verified"}:
        return "NEEDS_TRUTH"

    checks = []
    for prefix in ("income", "expenses"):
        d = row.get(f"{prefix}_delta")
        r = row.get(f"{prefix}_error_ratio")
        if d is not None and r is not None:
            checks.append(abs(d) <= amount_tolerance or r <= ratio_tolerance)
    if row.get("transaction_count_expected") is not None:
        checks.append(abs(row["transaction_count_actual"] - row["transaction_count_expected"]) <= count_tolerance)
    if row.get("currency_expected"):
        checks.append(row.get("currency_actual") == row.get("currency_expected"))
    if row.get("hijri_primary_date_count", 0) > 0:
        return "FAIL_HIJRI_PRIMARY_DATE"
    return "PASS" if checks and all(checks) else "FAIL_MISMATCH"


def write_reports(
    rows: list[dict[str, Any]],
    output_dir: Path,
    agent_transactions: Optional[dict[str, list[dict[str, Any]]]] = None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with (output_dir / "finance_corpus_results.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
    with (output_dir / "finance_corpus_results.json").open("w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=2, default=str)

    # Keep detailed agent output separate from the aggregate report so the CSV/HTML
    # stay compact while failed statements remain fully inspectable.
    with (output_dir / "agent_transactions.json").open("w", encoding="utf-8") as fh:
        json.dump(agent_transactions or {}, fh, ensure_ascii=False, indent=2, default=str)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["validation_status"]] = counts.get(row["validation_status"], 0) + 1
    headers = [
        "validation_status", "filename", "truth_confidence", "currency_expected", "currency_actual",
        "income_expected", "income_actual", "income_delta", "expenses_expected", "expenses_actual",
        "expenses_delta", "transaction_count_expected", "transaction_count_actual",
        "hijri_primary_date_count", "agent_error"
    ]
    trs = []
    for row in rows:
        cells = "".join(f"<td>{html.escape(str(row.get(h, '')))}</td>" for h in headers)
        trs.append(f"<tr class='{html.escape(row['validation_status'])}'>{cells}</tr>")
    summary = " ".join(f"<strong>{html.escape(k)}</strong>: {v}" for k, v in sorted(counts.items()))
    page = f"""<!doctype html><html><head><meta charset='utf-8'><title>Runexa Finance corpus validation</title>
<style>body{{font-family:Arial,sans-serif;margin:24px}}table{{border-collapse:collapse;width:100%;font-size:12px}}th,td{{border:1px solid #ddd;padding:6px;text-align:left}}th{{position:sticky;top:0;background:#eee}}.PASS{{background:#e9f8ee}}.FAIL_MISMATCH,.FAIL_AGENT,.FAIL_HIJRI_PRIMARY_DATE{{background:#fdecec}}.NEEDS_TRUTH{{background:#fff7dd}}</style></head>
<body><h1>Runexa Finance corpus validation</h1><p>{summary}</p><table><thead><tr>{''.join(f'<th>{h}</th>' for h in headers)}</tr></thead><tbody>{''.join(trs)}</tbody></table></body></html>"""
    (output_dir / "finance_corpus_report.html").write_text(page, encoding="utf-8")


def main() -> int:
    print(f"RUNEXA_FINANCE_VALIDATOR_VERSION_ACTIVE {VALIDATOR_VERSION}")
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--backend", type=Path, required=True)
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--output", type=Path, default=Path("validation_results"))
    parser.add_argument("--pattern", default="*.pdf")
    parser.add_argument("--amount-tolerance", type=float, default=1.00)
    parser.add_argument("--ratio-tolerance", type=float, default=0.005)
    parser.add_argument("--count-tolerance", type=int, default=0)
    parser.add_argument("--summary-reconciliation-tolerance", type=float, default=1.00)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    corpus = args.corpus.resolve()
    backend = args.backend.resolve()
    if not corpus.is_dir():
        parser.error(f"Corpus directory not found: {corpus}")
    if not backend.is_dir():
        parser.error(f"Backend directory not found: {backend}")

    manual = load_manual_truth(args.expected)
    statement_parser, extractor = import_agent(backend)
    files = sorted(corpus.rglob(args.pattern), key=lambda p: p.name.casefold())
    if args.limit > 0:
        files = files[:args.limit]

    rows: list[dict[str, Any]] = []
    all_agent_transactions: dict[str, list[dict[str, Any]]] = {}
    for index, path in enumerate(files, 1):
        print(f"[{index}/{len(files)}] {path.name}", flush=True)
        try:
            raw_text = read_pdf_text(path)
            auto_truth = extract_official_truth(raw_text, args.summary_reconciliation_tolerance)
        except Exception as exc:
            auto_truth = Truth(source="none", confidence="text_error", notes=f"{type(exc).__name__}: {exc}")
        truth = merge_truth(auto_truth, manual.get(path.name.casefold()))
        result, transactions = run_agent(path, statement_parser, extractor)
        relative_path = str(path.relative_to(corpus))
        all_agent_transactions[relative_path] = transactions

        row: dict[str, Any] = {
            "filename": path.name,
            "relative_path": relative_path,
            "truth_source": truth.source,
            "truth_confidence": truth.confidence,
            "truth_notes": truth.notes,
            "currency_expected": truth.currency,
            "currency_actual": result.currency,
            "opening_balance_expected": truth.opening_balance,
            "opening_balance_actual": result.opening_balance,
            "closing_balance_expected": truth.closing_balance,
            "closing_balance_actual": result.closing_balance,
            "income_expected": truth.deposits,
            "income_actual": result.income,
            "income_delta": delta(result.income, truth.deposits),
            "income_error_ratio": ratio_error(result.income, truth.deposits),
            "expenses_expected": truth.withdrawals,
            "expenses_actual": result.expenses,
            "expenses_delta": delta(result.expenses, truth.withdrawals),
            "expenses_error_ratio": ratio_error(result.expenses, truth.withdrawals),
            "net_expected": round(truth.deposits - truth.withdrawals, 2) if truth.deposits is not None and truth.withdrawals is not None else None,
            "net_actual": result.net,
            "transaction_count_expected": truth.transaction_count,
            "transaction_count_actual": result.transaction_count,
            "income_count_expected": truth.credit_count,
            "income_count_actual": result.income_count,
            "expense_count_expected": truth.debit_count,
            "expense_count_actual": result.expense_count,
            "invalid_date_count": result.invalid_date_count,
            "hijri_primary_date_count": result.hijri_primary_date_count,
            "agent_status": result.status,
            "agent_error": result.error,
        }
        row["validation_status"] = classify(row, args.amount_tolerance, args.ratio_tolerance, args.count_tolerance)
        rows.append(row)

    write_reports(rows, args.output.resolve(), all_agent_transactions)
    print(f"\nReports written to: {args.output.resolve()}")
    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["validation_status"]] = status_counts.get(row["validation_status"], 0) + 1
    print(json.dumps(status_counts, ensure_ascii=False, indent=2))
    return 1 if any(k.startswith("FAIL") for k in status_counts) else 0


if __name__ == "__main__":
    raise SystemExit(main())
