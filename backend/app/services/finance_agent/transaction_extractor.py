import re
from collections import Counter
from datetime import datetime


CURRENCY_CODES = ["USD", "EUR", "GBP", "AED", "MAD", "CAD", "JOD", "SAR", "QAR", "KWD", "BHD", "OMR"]

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
    "card",
    "direct debit",
    "standing order",
    "facture",
    "invoice",
    "abonnement",
    "premium",
    "recurring",
    "netflix",
    "transport",
]

INCOME_KEYWORDS = [
    "salary",
    "payroll",
    "incoming",
    "incoming transfer",
    "credit",
    "deposit",
    "freelance",
    "client",
]

EXPENSE_KEYWORDS += [
    "ticket",
    "e-ticket",
    "sncf",
    "train",
    "transport",
    "atm",
    "visa",
    "debit",
    "debit card",
    "purchase",
    "withdrawal",
    "مدين",
    "خصم",
    "سحب",
    "شراء",
    "outgoing",
    "outgoing transfer",
    "fee",
    "card payment",
    "direct debit",
    "sepa direct debit",
]

INCOME_KEYWORDS += [
    "credit",
    "credited",
    "deposit",
    "transfer in",
    "دائن",
    "إيداع",
    "تحويل وارد",
]

BALANCE_KEYWORDS = [
    "statement period",
    "statement date",
    "account holder",
    "account number",
    "currency",
    "generated test data",
    "opening balance",
    "closing balance",
    "balance",
    "solde",
    "total",
    "report",
    "fx conversion",
    "wallet credit",
    "periode",
    "période",
]


INTERNAL_TRANSFER_KEYWORDS = [
    "fx",
    "exchange",
    "currency exchange",
    "currency conversion",
    "conversion",
    "wallet",
    "between accounts",
    "own account",
    "internal transfer",
    "transfer between accounts",
    "balance transfer",
    "virement interne",
    "transfer interne",
    "internal saving",
    "livret",
]


TRANSACTION_SIGNALS = [
    "virement",
    "virement recu",
    "virement reçu",
    "prelevement",
    "prélèvement",
    "paiement",
    "paiement carte",
    "carte",
    "retrait",
    "frais",
    "commission",
    "remboursement",
    "retour carte",
]


MONTH_ALIASES = {
    "jan": "01",
    "january": "01",
    "feb": "02",
    "february": "02",
    "mar": "03",
    "march": "03",
    "apr": "04",
    "april": "04",
    "may": "05",
    "jun": "06",
    "june": "06",
    "jul": "07",
    "july": "07",
    "aug": "08",
    "august": "08",
    "sep": "09",
    "sept": "09",
    "september": "09",
    "oct": "10",
    "october": "10",
    "nov": "11",
    "november": "11",
    "dec": "12",
    "december": "12",
}



AMOUNT_PATTERN = (
    r"[+-]?"
    r"(?:\d{1,3}(?:[ ,]\d{3})+|\d+)"
    r"(?:[.,]\d{1,2})?"
)

UNSIGNED_AMOUNT_PATTERN = (
    r"(?:\d{1,3}(?:[ ,]\d{3})+|\d+)"
    r"(?:[.,]\d{1,2})?"
)

MONEY_NUMBER_PATTERN = (
    r"(?<![A-Za-z0-9])"
    r"\d{1,3}(?:[ ,]\d{3})*(?:[.,]\d{2})"
    r"(?![A-Za-z0-9])"
)



def is_arabic_text(text: str) -> bool:
    return bool(re.search(r"[\u0600-\u06FF]", text))


def normalize_arabic_ocr_lines(text: str) -> str:
    if not is_arabic_text(text):
        return text

    lines = [
        " ".join(line.split())
        for line in text.splitlines()
        if " ".join(line.split())
    ]

    rebuilt = []

    amount_token = r"(?:\d{1,3}(?:[ ,]\d{3})+|\d+)(?:[.,]\d{2})"

    amount_balance_date_re = re.compile(
        rf"({amount_token})\s+({amount_token})\s+(20\d{{6}})"
    )

    for line in lines:
        match = amount_balance_date_re.search(line)

        if not match:
            rebuilt.append(line)
            continue

        amount = match.group(1)
        date = match.group(3)

        rebuilt.append(
            f"{date} arabic ocr transaction card payment {amount}"
        )

    return "\n".join(rebuilt)


def normalize_ocr_numeric_text(value: str) -> str:
    translation = str.maketrans({
        "O": "0",
        "o": "0",
        "I": "1",
        "l": "1",
        "L": "1",
        "S": "5",
    })

    def fix_token(match):
        token = match.group(0)

        if not re.search(r"\d", token):
            return token

        return token.translate(translation)

    return re.sub(
        r"[A-Za-z0-9+\-.,/]+",
        fix_token,
        value,
    )

def parse_amount(value: str) -> float:
    value = value.strip().replace(" ", "")

    if "," in value and "." in value:
        value = value.replace(",", "")
    elif "," in value:
        parts = value.split(",")

        if len(parts) == 2 and len(parts[1]) == 3:
            value = value.replace(",", "")
        else:
            value = value.replace(",", ".")

    return float(value)


def pick_bank_amount(
    numbers: list[str],
    line: str,
    account_currency: str | None = None,
) -> float:
    text = line.upper()

    currency_amounts = re.findall(
        r"\b(?:USD|EUR|GBP|AED|MAD|CAD|JOD|SAR|QAR|KWD|BHD|OMR|دينار|دولار|درهم|ريال)\s*([+-]?\d[\d,]*(?:[.,]\d{1,2})?)",
        text,
        flags=re.IGNORECASE,
    )

    if currency_amounts:
        return parse_amount(currency_amounts[-1])

    if account_currency:
        matches = re.findall(
            rf"{account_currency}\s*([\d,]+(?:[.,]\d{{1,2}})?)",
            text,
        )

        if matches:
            return parse_amount(matches[-1])

    text = re.sub(r"\b\d{2}[./-]\d{2}[./-]\d{4}\b", "", text)
    text = re.sub(r"\b\d{2}[./-]\d{2}\b", "", text)
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "", text)
    text = re.sub(r"\b20\d{6}\b", "", text)

    money_numbers = re.findall(
        MONEY_NUMBER_PATTERN,
        text,
    )

    if money_numbers:
        return parse_amount(money_numbers[0])

    if len(numbers) >= 2:
        return parse_amount(numbers[-2])

    return parse_amount(numbers[-1])


def is_reasonable_year(year: int) -> bool:
    return 2000 <= year <= datetime.now().year + 1


def detect_document_year(text: str) -> int:
    years = []

    for match in re.findall(r"\b(20\d{2})-\d{2}-\d{2}\b", text):
        year = int(match)
        if is_reasonable_year(year):
            years.append(year)

    for match in re.findall(r"\b(20\d{2})\d{4}\b", text):
        year = int(match)
        if is_reasonable_year(year):
            years.append(year)

    for match in re.findall(r"\b\d{2}[./-]\d{2}[./-](20\d{2})\b", text):
        year = int(match)
        if is_reasonable_year(year):
            years.append(year)

    for match in re.findall(r"\b\d{2}[./-]\d{2}[./-](\d{2})\b", text):
        year = 2000 + int(match)
        if is_reasonable_year(year):
            years.append(year)

    if not years:
        return datetime.now().year

    return Counter(years).most_common(1)[0][0]


def extract_date(
    line: str,
    default_year: int | None = None,
):
    iso_match = re.search(
        r"\b(\d{4}-\d{2}-\d{2})\b",
        line,
    )

    if iso_match:
        try:
            parsed = datetime.strptime(
                iso_match.group(1),
                "%Y-%m-%d",
            )

            if not is_reasonable_year(parsed.year):
                return None

            return parsed.date().isoformat()

        except ValueError:
            pass


    compact_match = re.search(r"\b(20\d{2})(\d{2})(\d{2})\b", line)

    if compact_match:
        try:
            parsed = datetime(
                int(compact_match.group(1)),
                int(compact_match.group(2)),
                int(compact_match.group(3)),
            )

            if not is_reasonable_year(parsed.year):
                return None

            return parsed.date().isoformat()

        except ValueError:
            return None


    text_month_match = re.search(
        r"\b(\d{1,2})\s+"
        r"(january|jan|february|feb|march|mar|april|apr|may|"
        r"june|jun|july|jul|august|aug|september|sept|sep|"
        r"october|oct|november|nov|december|dec)"
        r"\s+(\d{2,4})\b",
        line,
        flags=re.IGNORECASE,
    )

    if text_month_match:
        day = int(text_month_match.group(1))
        month_key = text_month_match.group(2).lower()
        year = int(text_month_match.group(3))

        if year < 100:
            year += 2000

        month = int(MONTH_ALIASES[month_key])

        try:
            parsed = datetime(year, month, day)

            if parsed.year < 2000 or parsed.year > datetime.now().year + 1:
                return None

            return parsed.date().isoformat()
        except ValueError:
            return None

    match = re.search(
        r"\b(\d{2}[./-]\d{2}(?:[./-]\d{2,4})?)\b",
        line,
    )

    if not match:
        return None

    raw = match.group(1)

    formats_with_year = (
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%d.%m.%y",
    )

    for fmt in formats_with_year:
        try:
            parsed = datetime.strptime(raw, fmt)

            if not is_reasonable_year(parsed.year):
                return None

            return parsed.date().isoformat()

        except ValueError:
            continue

    formats_without_year = (
        "%d/%m",
        "%d-%m",
        "%d.%m",
    )

    for fmt in formats_without_year:
        try:
            parsed = datetime.strptime(raw, fmt)

            year = default_year or datetime.now().year

            parsed = parsed.replace(year=year)

            if not is_reasonable_year(parsed.year):
                return None

            return parsed.date().isoformat()

        except ValueError:
            continue

    return None


def is_date_only_line(
    line: str,
    default_year: int | None = None,
) -> bool:
    if not extract_date(line, default_year=default_year):
        return False

    remaining = re.sub(
        r"\b\d{1,2}\s+"
        r"(january|jan|february|feb|march|mar|april|apr|may|"
        r"june|jun|july|jul|august|aug|september|sept|sep|"
        r"october|oct|november|nov|december|dec)"
        r"\s+\d{2,4}\b",
        "",
        line,
        flags=re.IGNORECASE,
    )

    remaining = re.sub(
        r"\b\d{4}-\d{2}-\d{2}\b",
        "",
        remaining,
    )

    remaining = re.sub(
        r"\b\d{2}[./-]\d{2}(?:[./-]\d{2,4})?\b",
        "",
        remaining,
    )

    return remaining.strip() == ""


def has_transaction_signal(
    line: str,
    default_year: int | None = None,
) -> bool:
    lower = line.lower()

    metadata_check = (
        lower
        .replace("5", "s")
        .replace("0", "o")
        .replace("1", "l")
    )

    if any(keyword in metadata_check for keyword in BALANCE_KEYWORDS):
        return False

    date_found = extract_date(
        line,
        default_year=default_year,
    ) is not None

    amount_found = bool(
        re.search(
            MONEY_NUMBER_PATTERN,
            line,
        )
    )

    signal_found = any(
        keyword in lower
        for keyword in TRANSACTION_SIGNALS
    )

    return date_found and amount_found and (
        signal_found or amount_found
    )


def detect_type(line: str, amount: float) -> str:
    lower = line.lower()

    # outgoing payments have priority
    if any(keyword in lower for keyword in EXPENSE_KEYWORDS):
        return "expense"

    # common outgoing transfers
    if any(
        keyword in lower
        for keyword in [
            "loyer",
            "rent",
            "mortgage",
            "loan payment",
        ]
    ):
        return "expense"

    if any(keyword in lower for keyword in INCOME_KEYWORDS):
        return "income"

    if amount < 0:
        return "expense"

    return "income"


def extract_transaction_amount(line: str) -> float | None:
    transaction_part = re.split(
        r"\bbalance\b|\bsolde\b",
        line,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    transaction_part = re.sub(
        r"\b\d{4}-\d{2}-\d{2}\b",
        "",
        transaction_part,
        count=1,
    )

    transaction_part = re.sub(
        r"\b20\d{6}\b",
        "",
        transaction_part,
        count=1,
    )

    transaction_part = re.sub(
        r"\b\d{2}[./-]\d{2}(?:[./-]\d{2,4})?\b",
        "",
        transaction_part,
        count=1,
    )

    transaction_part = re.sub(
        r"\b\d{1,2}\s+"
        r"(january|jan|february|feb|march|mar|april|apr|may|"
        r"june|jun|july|jul|august|aug|september|sept|sep|"
        r"october|oct|november|nov|december|dec)"
        r"\s+\d{2,4}\b",
        "",
        transaction_part,
        count=1,
        flags=re.IGNORECASE,
    )

    money_matches = re.findall(
        rf"{AMOUNT_PATTERN}\s*(?:[A-Z]{{3}}|DH|DHS|€|\$|£)?",
        transaction_part,
        flags=re.IGNORECASE,
    )

    money_matches = [
        value
        for value in money_matches
        if re.search(r"[.,]\d{2}", value)
    ]

    if not money_matches:
        return None

    for value in money_matches:
        cleaned = value.strip()

        if cleaned.lower().startswith("balance"):
            continue

        if cleaned.startswith("+") or cleaned.startswith("-"):
            numeric = re.search(
                AMOUNT_PATTERN,
                cleaned,
            )
            if numeric:
                return parse_amount(numeric.group(0))

    numeric = re.search(
        AMOUNT_PATTERN,
        money_matches[0],
    )

    if not numeric:
        return None

    return parse_amount(numeric.group(0))


def extract_tabular_bank_amount(
    line: str,
) -> tuple[float | None, str | None]:
    normalized = line.lower()

    NON_TRANSACTION_KEYWORDS = [
        "account number",
        "account holder",
        "account name",
        "customer name",
        "client name",
        "statement date",
        "statement period",
        "period",
        "date range",
        "periode",
        "période",
        "du ",
        " au ",
        "bank statement",
        "example bank",
        "iban",
        "swift",
        "sort code",
    ]

    if any(keyword in normalized for keyword in NON_TRANSACTION_KEYWORDS):
        return None, None

    if any(
        keyword in normalized
        for keyword in [
            "balance carried forward",
            "closing balance",
            "opening balance",
        ]
    ):
        return None, None

    without_date = re.sub(
        r"\b\d{4}-\d{2}-\d{2}\b",
        "",
        line,
        count=1,
    )

    without_date = re.sub(
        r"\b\d{2}[./-]\d{2}(?:[./-]\d{2,4})?\b",
        "",
        without_date,
        count=1,
    )

    without_date = re.sub(
        r"\b\d{1,2}\s+"
        r"(january|jan|february|feb|march|mar|april|apr|may|"
        r"june|jun|july|jul|august|aug|september|sept|sep|"
        r"october|oct|november|nov|december|dec)"
        r"\s+\d{2,4}\b",
        "",
        without_date,
        count=1,
        flags=re.IGNORECASE,
    )


    numbers = re.findall(
        MONEY_NUMBER_PATTERN,
        without_date,
    )

    if not numbers:
        return None, None

    description = normalized

    if any(
        keyword in description
        for keyword in [
            "fx conversion",
            "fx exchange",
            "currency exchange",
            "currency conversion",
            "wallet credit",
            "wallet",
            "internal transfer",
        ]
    ):
        return None, None

    if any(
        keyword in description
        for keyword in [
            "retour carte",
            "refund",
            "reversal",
            "remboursement",
        ]
    ):
        amount = pick_bank_amount(numbers, line)

        return amount, "income"

    if any(
        keyword in description
        for keyword in [
            "atm",
            "visa",
            "card",
            "debit",
            "direct debit",
            "standing order",
            "withdrawal",
            "payment",
            "purchase",
            "recurring",
            "fee",
            "card payment",
            "sepa direct debit",
            "outgoing transfer",
            "ticket",
            "e-ticket",
            "restaurant",
            "supermarket",
            "pharmacy",
            "pharmacie",
            "fuel",
            "uber",
            "transport",
            "rent",
            "arabic ocr transaction",
        ]
    ):
        amount = pick_bank_amount(numbers, line)

        return -abs(amount), "expense"

    if any(
        keyword in description
        for keyword in [
            "incoming transfer",
            "transfer received",
            "virement reçu",
            "virement recu",
            "salary",
            "payroll",
            "wage",
            "deposit",
            "received",
            "freelance",
            "client",
        ]
    ):
        amount = pick_bank_amount(numbers, line)

        return amount, "income"

    return None, None


def extract_first_amount_after_date(line: str) -> float | None:
    text = re.sub(
        r"\b\d{4}-\d{2}-\d{2}\b",
        "",
        line,
        count=1,
    )


    numbers = re.findall(
        MONEY_NUMBER_PATTERN,
        text,
    )

    if not numbers:
        return None

    if len(numbers) >= 3:
        return parse_amount(numbers[-2])

    return parse_amount(numbers[-1])


def normalize_arabic_digits(value: str) -> str:
    return value.translate(
        str.maketrans(
            "٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹",
            "01234567890123456789",
        )
    )


def extract_arabic_ocr_transactions(text: str) -> list[dict]:
    if not is_arabic_text(text):
        return []

    normalized = normalize_arabic_digits(text)
    normalized = normalized.replace("\u00a0", " ").replace("\u202f", " ")
    normalized = normalized.replace("،", ",")
    normalized = "\n".join(" ".join(l.split()) for l in normalized.splitlines())

    print("=== AR DEBUG START ===")
    print("TEXT_LENGTH:", len(normalized))
    print("DATES_FOUND:", re.findall(r"\b20\d{6}\b", normalized))
    print(
        "AMOUNTS_FOUND:",
        re.findall(
            r"\d{1,3}(?:[ ,]\d{3})*(?:[.,]\d{2})",
            normalized
        )[:30]
    )

    amount_pattern = r"\d{1,3}(?:[ ,]\d{3})*(?:[.,]\d{2})"
    date_pattern = r"\b20\d{6}\b"

    rows = []

    for dm in re.finditer(date_pattern, normalized):
        print("---- DATE LOOP ----")
        print("DATE:", dm.group(0))

        date_raw = dm.group(0)

        start = max(0, dm.start() - 90)
        end = min(len(normalized), dm.end() + 90)
        window = normalized[start:end]

        print("WINDOW:")
        print(window)

        amounts = []

        print(
            "WINDOW_AMOUNTS:",
            re.findall(amount_pattern, window)
        )
        for am in re.finditer(amount_pattern, window):
            raw = am.group(0)
            try:
                value = parse_amount(raw)
            except Exception:
                continue

            absolute_pos = start + am.start()
            distance = abs(absolute_pos - dm.start())

            amounts.append((distance, value, raw))

        if len(amounts) < 2:
            continue

        amounts.sort(key=lambda x: x[0])
        nearest_values = [x[1] for x in amounts[:4]]

        clean = []
        for v in nearest_values:
            if not any(abs(v - old) < 0.01 for old in clean):
                clean.append(v)

        if len(clean) < 2:
            continue

        tx_amount = clean[0]
        balance = clean[1]

        rows.append({
            "date": f"{date_raw[:4]}-{date_raw[4:6]}-{date_raw[6:8]}",
            "amount": tx_amount,
            "balance": balance,
            "text": window,
        })

    unique = {}
    for r in rows:
        unique[r["date"]] = r

    rows = sorted(unique.values(), key=lambda x: x["date"])

    transactions = []

    for i, row in enumerate(rows):
        tx_type = "income"

        if i > 0:
            previous_balance = rows[i - 1]["balance"]
            diff = round(row["balance"] - previous_balance, 2)

            if abs(diff + row["amount"]) < 0.1:
                tx_type = "expense"
            elif abs(diff - row["amount"]) < 0.1:
                tx_type = "income"
            else:
                lower = row["text"].lower()
                if any(k in lower for k in EXPENSE_KEYWORDS):
                    tx_type = "expense"
                elif any(k in lower for k in INCOME_KEYWORDS):
                    tx_type = "income"

        transactions.append({
            "date": row["date"],
            "description": row["text"][:300],
            "amount": row["amount"] if tx_type == "income" else -abs(row["amount"]),
            "type": tx_type,
        })

    print("ROWS_BUILT:", rows)

    for t in transactions:
        print("AR_TX:", t)

    print("ARABIC_BYPASS_COUNT:", len(transactions))
    return transactions


def extract_transactions(text: str) -> list[dict]:
    arabic_transactions = extract_arabic_ocr_transactions(text)
    if arabic_transactions:
        return arabic_transactions

    print("RAW_AR_TEXT_SAMPLE:", text[:1000])

    text = normalize_arabic_ocr_lines(text)
    text = normalize_ocr_numeric_text(text)

    transactions = []
    default_year = detect_document_year(text)

    raw_lines = [
        " ".join(line.split())
        for line in text.splitlines()
        if " ".join(line.split())
    ]

    lines = []
    i = 0

    while i < len(raw_lines):
        current = raw_lines[i]

        current_is_date_only = is_date_only_line(
            current,
            default_year=default_year,
        )

        if current_is_date_only:
            combined = current
            j = i + 1

            while j < len(raw_lines) and j <= i + 4:
                combined += " " + raw_lines[j]

                if re.search(MONEY_NUMBER_PATTERN, raw_lines[j]):
                    break

                j += 1

            lines.append(combined)
            i = j + 1
            continue

        if (
            extract_date(current, default_year=default_year)
            and not re.search(MONEY_NUMBER_PATTERN, current)
        ):
            combined = current
            j = i + 1

            while j < len(raw_lines) and j <= i + 4:
                combined += " " + raw_lines[j]

                if re.search(MONEY_NUMBER_PATTERN, raw_lines[j]):
                    break

                j += 1

            lines.append(combined)
            i = j + 1
            continue

        lines.append(current)
        i += 1

    for clean_line in lines:

        normalized_line = clean_line.lower()

        if any(k in normalized_line for k in INTERNAL_TRANSFER_KEYWORDS):
            continue

        if any(
            keyword in normalized_line
            for keyword in [
                "account number",
                "account holder",
                "account name",
                "customer name",
                "client name",
                "statement date",
                "statement period",
                "date range",
                "periode",
                "période",
                "bank statement",
                "iban",
                "swift",
                "sort code",
            ]
        ):
            continue

        if re.fullmatch(
            r"\d{2}[./-]\d{2}[./-]\d{4}\s*[-–]\s*\d{2}[./-]\d{2}[./-]\d{4}",
            clean_line,
        ):
            continue

        if not has_transaction_signal(
            clean_line,
            default_year=default_year,
        ):
            continue

        tabular_amount, tabular_type = extract_tabular_bank_amount(clean_line)


        if tabular_amount is not None:
            amount = tabular_amount
        else:
            amount = extract_transaction_amount(clean_line)

        if amount is None:
            fallback_amount = extract_first_amount_after_date(clean_line)

            if fallback_amount is None:
                continue

            amount = fallback_amount

        transaction_type = tabular_type or detect_type(clean_line, amount)


        if transaction_type == "expense" and amount > 0:
            amount = -abs(amount)

        if transaction_type == "income":
            amount = abs(amount)

        date = extract_date(
            clean_line,
            default_year=default_year,
        )

        print(
            "AR_TX_FINAL:",
            clean_line,
            "=>",
            amount,
            transaction_type,
        )

        transactions.append(
            {
                "date": date,
                "description": clean_line,
                "amount": amount,
                "type": transaction_type,
            }
        )

    return transactions
EXPENSE_KEYWORDS += [
    "مدين",
    "خصم",
    "سحب",
    "شراء",
    "دفع",
    "بطاقة",
    "رسوم",
    "عمولة",
    "فاتورة",
    "اشتراك",
    "تحويل صادر",
    "حوالة صادرة",
]

INCOME_KEYWORDS += [
    "دائن",
    "إيداع",
    "ايداع",
    "راتب",
    "دخل",
    "تحويل وارد",
    "حوالة واردة",
    "قبض",
]

EXPENSE_KEYWORDS += [
    "arabic ocr transaction",
]
