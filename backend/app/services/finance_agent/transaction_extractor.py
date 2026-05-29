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
]

TRANSACTION_KEYWORDS = EXPENSE_KEYWORDS + INCOME_KEYWORDS + [
    "transfer",
    "withdrawal",
    "payment",
    "card",
    "refund",
]

BALANCE_KEYWORDS = [
    "solde",
    "balance",
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
            r"-?\d+(?:[.,]\d{2})",
            line,
        )
    )

    return date_found and amount_found


def detect_type(line: str, amount: float) -> str:
    lower = line.lower()

    if any(keyword in lower for keyword in EXPENSE_KEYWORDS):
        return "expense"

    if any(keyword in lower for keyword in INCOME_KEYWORDS):
        return "income"

    if amount < 0:
        return "expense"

    return "income"


def extract_transactions(text: str) -> list[dict]:
    transactions = []

    for line in text.splitlines():
        clean_line = " ".join(line.split())

        if not clean_line:
            continue

        if len(transactions) < 5:
            print(
                "CHECK:",
                clean_line,
                "DATE=",
                extract_date(clean_line),
                "AMOUNT_MATCH=",
                bool(
                    re.search(
                        r"-?\d+(?:[.,]\d{2})",
                        clean_line,
                    )
                ),
            )

        if not has_transaction_signal(clean_line):
            continue

        amounts = re.findall(
            r"-?\d{1,3}(?:[,\s]\d{3})*(?:\.\d{2})|-?\d+(?:[.,]\d{2})",
            clean_line,
        )

        if len(transactions) < 5:
            print("LINE:", clean_line)
            print("AMOUNTS:", amounts)

        if not amounts:
            continue

        amount = parse_amount(amounts[-1])

        if len(transactions) < 5:
            print("SELECTED:", amount)

        transaction_type = detect_type(clean_line, amount)

        if transaction_type == "expense" and amount > 0:
            amount = -abs(amount)

        if transaction_type == "income":
            amount = abs(amount)

        date = extract_date(clean_line)
        description = clean_line

        transactions.append(
            {
                "date": date,
                "description": description,
                "amount": amount,
                "type": transaction_type,
            }
        )

    return transactions
