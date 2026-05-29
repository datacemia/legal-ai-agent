import re
from datetime import datetime


EXPENSE_KEYWORDS = [
    "paiement",
    "carte",
    "retrait",
    "debit",
    "débit",
    "prelevement",
    "prélèvement",
    "virement emis",
    "virement émis",
    "frais",
    "commission",
    "achat",
    "payment",
    "withdrawal",
    "bill",
    "rent",
    "shopping",
    "restaurant",
    "market",
    "supermarket",
    "fuel",
    "pharmacy",
    "subscription",
    "membership",
    "transfer sent",
]

INCOME_KEYWORDS = [
    "salaire",
    "salary",
    "credit",
    "crédit",
    "versement",
    "virement recu",
    "virement reçu",
    "remboursement",
    "deposit",
    "dépôt",
    "transfer received",
]

BALANCE_KEYWORDS = [
    "opening balance",
    "closing balance",
    "ancien solde",
    "nouveau solde",
    "total",
    "report",
]


def parse_amount(value: str) -> float:
    value = value.replace(" ", "")

    if "," in value and "." in value:
        value = value.replace(",", "")
    else:
        value = value.replace(",", ".")

    return float(value)


def extract_date(line: str):
    match = re.search(r"(\d{2}[/-]\d{2}(?:[/-]\d{2,4})?)", line)

    if not match:
        return None

    raw = match.group(1)

    for fmt in (
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%d/%m",
        "%d-%m",
    ):
        try:
            parsed = datetime.strptime(raw, fmt)

            if parsed.year == 1900:
                parsed = parsed.replace(year=datetime.now().year)

            return parsed.date().isoformat()

        except ValueError:
            continue

    return None


def has_transaction_signal(line: str) -> bool:
    lower = line.lower()

    if any(keyword in lower for keyword in BALANCE_KEYWORDS):
        return False

    date_found = extract_date(line) is not None

    amount_found = bool(
        re.search(
            r"[+-]?\d+(?:[.,]\d{2})",
            line,
        )
    )

    return date_found and amount_found


def detect_type(line: str, amount: float) -> str:
    lower = line.lower()

    if any(keyword in lower for keyword in INCOME_KEYWORDS):
        return "income"

    if any(keyword in lower for keyword in EXPENSE_KEYWORDS):
        return "expense"

    if amount < 0:
        return "expense"

    return "income"


def extract_transaction_amount(line: str) -> float | None:
    money_matches = re.findall(
        r"[+-]?\d+(?:[.,]\d{2})\s*(?:MAD|USD|EUR|GBP|CAD|DH|DHS|€|\$|£)?",
        line,
        flags=re.IGNORECASE,
    )

    if not money_matches:
        return None

    for value in money_matches:
        cleaned = value.strip()

        if cleaned.lower().startswith("balance"):
            continue

        if cleaned.startswith("+") or cleaned.startswith("-"):
            numeric = re.search(r"[+-]?\d+(?:[.,]\d{2})", cleaned)
            if numeric:
                return parse_amount(numeric.group(0))

    numeric = re.search(
        r"[+-]?\d+(?:[.,]\d{2})",
        money_matches[0],
    )

    if not numeric:
        return None

    return parse_amount(numeric.group(0))


def extract_transactions(text: str) -> list[dict]:
    transactions = []

    for line in text.splitlines():
        clean_line = " ".join(line.split())

        if not clean_line:
            continue

        if not has_transaction_signal(clean_line):
            continue

        amount = extract_transaction_amount(clean_line)

        if amount is None:
            continue

        transaction_type = detect_type(clean_line, amount)

        if transaction_type == "expense" and amount > 0:
            amount = -abs(amount)

        if transaction_type == "income":
            amount = abs(amount)

        date = extract_date(clean_line)

        transactions.append(
            {
                "date": date,
                "description": clean_line,
                "amount": amount,
                "type": transaction_type,
            }
        )

    return transactions