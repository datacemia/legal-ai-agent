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
    "تحويل داخلي",
    "يلخاد ليوحت",
    "حوالة داخلية",
    "ةيلخاد ةلاوح",
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




def clean_db_text(value: str) -> str:
    if not isinstance(value, str):
        return value

    # caractères interdits PostgreSQL JSON/TEXT
    value = value.replace("\x00", "")

    # autres caractères contrôle OCR
    value = re.sub(
        r"[\x01-\x08\x0b\x0c\x0e-\x1f]",
        "",
        value,
    )

    return value.strip()


def detect_currency(text: str) -> str:
    """Detect currency safely from explicit text, country hints, then bank hints.

    Order is intentionally conservative:
    1) explicit ISO/symbol/currency-name detection wins;
    2) country or jurisdiction hints are used only when no explicit currency exists;
    3) bank hints are last-resort and avoid ambiguous mixed-currency documents;
    4) otherwise return "unknown" instead of inventing a currency.
    """
    normalized = normalize_arabic_digits(clean_db_text(text)).upper()

    # Documents that explicitly say they are multi-currency should not be forced
    # to a single bank-default currency unless a currency is explicitly present.
    mixed_currency_markers = [
        "MULTI CURRENCY",
        "MULTICURRENCY",
        "MIXED CURRENCY",
        "MIXED CURRENCIES",
        "COMPTE MULTIDEVISE",
        "MULTI-DEVISE",
        "MULTIDEVISE",
        "عملات مختلطة",
        "مختلط عملات",
        "تالمع طلتخم",
    ]
    is_mixed_currency_document = any(
        marker.upper() in normalized
        for marker in mixed_currency_markers
    )

    # Explicit currency detection: ISO codes, symbols and common names in EN/FR/AR.
    patterns = [
        ("USD", [r"\bUSD\b", r"\bUS\$\b", r"\$", "US DOLLAR", "DOLLAR US", "DOLLAR AMÉRICAIN", "DOLLAR AMERICAIN", "دولار أمريكي", "دولار"]),
        ("EUR", [r"\bEUR\b", "€", "EURO", "يورو"]),
        ("GBP", [r"\bGBP\b", "£", "POUND STERLING", "STERLING", "LIVRE STERLING", "جنيه إسترليني", "جنيه استرليني"]),
        ("MAD", [r"\bMAD\b", r"\bDH\b", r"\bDHS\b", "DIRHAM MAROCAIN", "MOROCCAN DIRHAM", "درهم مغربي"]),
        ("AED", [r"\bAED\b", "UAE DIRHAM", "EMIRATI DIRHAM", "DIRHAM ÉMIRATI", "DIRHAM EMIRATI", "درهم إماراتي"]),
        ("JOD", [r"\bJOD\b", "JORDANIAN DINAR", "DINAR JORDANIEN", "دينار أردني"]),
        ("SAR", [r"\bSAR\b", "SAUDI RIYAL", "RIYAL SAOUDIEN", "ريال سعودي"]),
        ("QAR", [r"\bQAR\b", "QATARI RIYAL", "RIYAL QATARI", "ريال قطري", "يرطق لاير"]),
        ("KWD", [r"\bKWD\b", "KUWAITI DINAR", "DINAR KOWEÏTIEN", "DINAR KOWEITIEN", "دينار كويتي"]),
        ("BHD", [r"\bBHD\b", "BAHRAINI DINAR", "DINAR BAHREÏNI", "DINAR BAHREINI", "دينار بحريني"]),
        ("OMR", [r"\bOMR\b", "OMANI RIAL", "RIAL OMANI", "ريال عماني"]),
        ("CAD", [r"\bCAD\b", "CANADIAN DOLLAR", "DOLLAR CANADIEN", "دولار كندي"]),
        ("AUD", [r"\bAUD\b", "AUSTRALIAN DOLLAR", "DOLLAR AUSTRALIEN", "دولار أسترالي"]),
        ("CHF", [r"\bCHF\b", "SWISS FRANC", "FRANC SUISSE", "فرنك سويسري"]),
        ("JPY", [r"\bJPY\b", "JAPANESE YEN", "YEN JAPONAIS", "ين ياباني"]),
        ("CNY", [r"\bCNY\b", "CHINESE YUAN", "YUAN CHINOIS", "يوان صيني"]),
        ("INR", [r"\bINR\b", "INDIAN RUPEE", "ROUPEE INDIENNE", "روبية هندية"]),
        ("TRY", [r"\bTRY\b", "TURKISH LIRA", "LIVRE TURQUE", "ليرة تركية"]),
        ("EGP", [r"\bEGP\b", "EGYPTIAN POUND", "LIVRE ÉGYPTIENNE", "LIVRE EGYPTIENNE", "جنيه مصري"]),
        ("TND", [r"\bTND\b", "TUNISIAN DINAR", "DINAR TUNISIEN", "دينار تونسي"]),
        ("DZD", [r"\bDZD\b", "ALGERIAN DINAR", "DINAR ALGÉRIEN", "DINAR ALGERIEN", "دينار جزائري"]),
        ("NGN", [r"\bNGN\b", "NAIRA", "نيرة"]),
        ("ZAR", [r"\bZAR\b", "RAND", "راند"]),
    ]

    scores = Counter()

    for code, pats in patterns:
        for pat in pats:
            if re.search(pat, normalized, flags=re.IGNORECASE):
                scores[code] += 1

    if scores:
        return scores.most_common(1)[0][0]

    # Country/jurisdiction fallback. Safer than bank fallback because it uses
    # explicit country context from the statement.
    country_currency_hints = [
        ("USD", ["UNITED STATES", "USA", "U.S.A", "US BANK", "AMERICA", "ÉTATS-UNIS", "ETATS-UNIS", "الولايات المتحدة", "أمريكا"]),
        ("GBP", ["UNITED KINGDOM", "UK", "GREAT BRITAIN", "BRITAIN", "ENGLAND", "ROYAUME-UNI", "ANGLETERRE", "المملكة المتحدة", "بريطانيا", "إنجلترا"]),
        ("EUR", ["FRANCE", "GERMANY", "DEUTSCHLAND", "SPAIN", "ESPAÑA", "ESPAGNE", "ITALY", "ITALIA", "NETHERLANDS", "BELGIUM", "BELGIQUE", "EUROZONE", "EUROPEAN UNION", "UNION EUROPÉENNE", "UNION EUROPEENNE", "فرنسا", "ألمانيا", "إسبانيا", "إيطاليا"]),
        ("MAD", ["MOROCCO", "MAROC", "المغرب", "برغملا"]),
        ("QAR", ["QATAR", "قطر", "رطق"]),
        ("JOD", ["JORDAN", "الأردن", "ندرأ"]),
        ("AED", ["UNITED ARAB EMIRATES", "UAE", "DUBAI", "ABU DHABI", "EMIRATES", "ÉMIRATS", "EMIRATS", "الإمارات", "تارامإ", "دبي", "أبوظبي"]),
        ("SAR", ["SAUDI ARABIA", "KSA", "SAUDI", "السعودية", "ةيدوعسلا"]),
        ("KWD", ["KUWAIT", "الكويت", "تيوك"]),
        ("BHD", ["BAHRAIN", "البحرين", "نيرحب"]),
        ("OMR", ["OMAN", "عمان", "نامع"]),
        ("CAD", ["CANADA", "CANADIEN", "كندا"]),
        ("AUD", ["AUSTRALIA", "AUSTRALIE", "أستراليا"]),
        ("CHF", ["SWITZERLAND", "SUISSE", "سويسرا"]),
        ("JPY", ["JAPAN", "JAPON", "اليابان"]),
        ("CNY", ["CHINA", "CHINE", "الصين"]),
        ("INR", ["INDIA", "INDE", "الهند"]),
        ("TRY", ["TURKEY", "TURQUIE", "تركيا"]),
        ("EGP", ["EGYPT", "ÉGYPTE", "EGYPTE", "مصر"]),
        ("TND", ["TUNISIA", "TUNISIE", "تونس"]),
        ("DZD", ["ALGERIA", "ALGÉRIE", "ALGERIE", "الجزائر"]),
        ("ZAR", ["SOUTH AFRICA", "AFRIQUE DU SUD", "جنوب أفريقيا"]),
    ]

    for code, hints in country_currency_hints:
        if any(hint.upper() in normalized for hint in hints):
            return code

    # Bank fallback is last-resort. It is skipped for explicit mixed-currency
    # statements because a bank can issue accounts in several currencies.
    if is_mixed_currency_document:
        return "unknown"

    bank_currency_hints = [
        # Qatar
        ("QAR", ["QNB", "QATAR NATIONAL BANK", "ينطولا رطق كنب", "كنب رطق ينطولا"]),

        # Morocco
        ("MAD", ["CIH", "ATTIJARI", "ATTIJARIWAFA", "WAFA", "BMCE", "BANK OF AFRICA", "CHAABI", "BANQUE POPULAIRE", "CREDIT DU MAROC", "CRÉDIT DU MAROC", "CFG BANK", "AL BARID BANK"]),

        # UAE
        ("AED", ["EMIRATES NBD", "ADCB", "FAB", "FIRST ABU DHABI BANK", "MASHREQ", "DUBAI ISLAMIC BANK", "ADIB"]),

        # Saudi Arabia
        ("SAR", ["AL RAJHI", "ALRAJHI", "AL RAJHI BANK", "ALRAJHI BANK", "مصرف الراجحي", "يحجارلا فرصم", "SNB", "SAUDI NATIONAL BANK", "RIYAD BANK", "ALINMA", "BANQUE SAUDI FRANSI"]),

        # Kuwait / Bahrain / Oman
        ("KWD", ["KUWAIT FINANCE HOUSE", "KFH", "NATIONAL BANK OF KUWAIT", "NBK"]),
        ("BHD", ["NATIONAL BANK OF BAHRAIN", "NBB", "BANK OF BAHRAIN"]),
        ("OMR", ["BANK MUSCAT", "NATIONAL BANK OF OMAN", "NBO"]),

        # UK
        ("GBP", ["BARCLAYS", "LLOYDS", "NATWEST", "HSBC UK", "MONZO", "STARLING", "SANTANDER UK", "TSB BANK"]),

        # US
        ("USD", ["CHASE", "JPMORGAN", "JPMORGAN CHASE", "BANK OF AMERICA", "WELLS FARGO", "CITI", "CITIBANK", "CAPITAL ONE", "USAA", "PNC BANK", "TD BANK USA"]),

        # France / Eurozone banks
        ("EUR", ["BNP", "BNP PARIBAS", "SOCIETE GENERALE", "SOCIÉTÉ GÉNÉRALE", "CREDIT AGRICOLE", "CRÉDIT AGRICOLE", "LA BANQUE POSTALE", "LCL", "CAISSE D'EPARGNE", "CAISSE D’ÉPARGNE", "BANQUE POPULAIRE FRANCE", "BOURSORAMA", "REVOLUT BANK UAB", "N26"]),

        # Jordan / Arab Bank. Kept last because Arab Bank can be multi-country/multi-currency.
        ("JOD", ["ARAB BANK JORDAN", "BANK OF JORDAN", "البنك العربي الأردني", "يبرعلا يندرألا كنبلا"]),
    ]

    for code, hints in bank_currency_hints:
        if any(hint.upper() in normalized for hint in hints):
            return code

    return "unknown"

def detect_statement_month_year(text: str):
    text = clean_db_text(normalize_arabic_digits(text))

    # exemples: 20260401 20260430
    m = re.search(r"(20\d{2})([01]\d)[0-3]\d\s+(20\d{2})([01]\d)[0-3]\d", text)
    if m and m.group(1) == m.group(3) and m.group(2) == m.group(4):
        return int(m.group(1)), int(m.group(2))

    # exemples: 01.04.2026 30.04.2026
    m = re.search(r"[0-3]?\d[./-]([01]?\d)[./-](20\d{2}).{0,20}[0-3]?\d[./-]\1[./-]\2", text)
    if m:
        return int(m.group(2)), int(m.group(1))

    return None, None


def iter_lines_with_offsets(text: str):
    offset = 0
    for line in text.splitlines(True):
        yield offset, line
        offset += len(line)


def find_arabic_ocr_dates(text: str):
    text = clean_db_text(normalize_arabic_digits(text))

    text = (
        text.replace("٫", ".")
            .replace("٬", ".")
            .replace("·", ".")
            .replace("•", ".")
            .replace("․", ".")
            .replace("﹒", ".")
            .replace("．", ".")
    )

    found = []
    statement_year, statement_month = detect_statement_month_year(text)

    def add_date(year, month, day, start, end, partial=False):
        try:
            parsed = datetime(int(year), int(month), int(day))
        except Exception:
            return

        if not is_reasonable_year(parsed.year):
            return

        found.append({
            "clean": f"{parsed.year}{parsed.month:02d}{parsed.day:02d}",
            "date": parsed.date().isoformat(),
            "start": start,
            "end": end,
            "partial": partial,
        })

    def normalize_year(year: str):
        if len(year) == 4 and year.startswith("20"):
            return year

        if len(year) in (2, 3):
            return "20" + year[-2:]

        return None

    # DD.MM.YYYY / D.M.YY / D.M.YYY
    # strict: refuse de commencer juste après chiffre ou virgule
    date_pattern = re.compile(
        r"(?<![\d,])([0-3]?\d)\s*[./-]\s*([01]?\d)\s*[./-]\s*(\d{2,4})(?!\d)"
    )

    # YYYY.MM.DD
    ymd_pattern = re.compile(
        r"(?<![\d,])(20\d{2})\s*[./-]\s*([01]?\d)\s*[./-]\s*([0-3]?\d)(?!\d)"
    )

    for line_start, line in iter_lines_with_offsets(text):
        if any(x in line for x in [
            "الحساب",
            "باسحلا",
            "account",
            "iban",
            "الفترة",
            "ةرتفلا",
        ]):
            continue

        for m in date_pattern.finditer(line):
            day, month, year = m.groups()
            y = normalize_year(year)

            if not y:
                continue

            add_date(
                y,
                month,
                day,
                line_start + m.start(),
                line_start + m.end(),
            )

        for m in ymd_pattern.finditer(line):
            year, month, day = m.groups()

            add_date(
                year,
                month,
                day,
                line_start + m.start(),
                line_start + m.end(),
            )

        # dates partielles OCR: "01 2026", "02 2026"
        # utilise le mois de la période si disponible
        if statement_year and statement_month:
            m = re.search(r"^\s*([0-3]?\d)\s+(20\d{2})\b", line)
            if m:
                day, year = m.groups()
                if int(year) == statement_year:
                    add_date(
                        statement_year,
                        statement_month,
                        int(day),
                        line_start + m.start(1),
                        line_start + m.end(2),
                    )

        # format DDMMYYYY (ex: 01042026)
        # Important: keep the exact match offsets, not the whole line.
        # Otherwise amount extraction can merge two different transactions.
        for m in re.finditer(
            r"(?<!\d)([0-3]\d)([0-1]\d)(20\d{2})(?!\d)",
            line,
        ):
            day, month, year = m.groups()

            try:
                date_obj = datetime(
                    int(year),
                    int(month),
                    int(day),
                )
            except Exception:
                continue

            add_date(
                date_obj.year,
                date_obj.month,
                date_obj.day,
                line_start + m.start(),
                line_start + m.end(),
            )

        # compact YYYYMMDD
        for m in re.finditer(
            r"(?<!\d)(20\d{2}[01]\d[0-3]\d)(?!\d)",
            line,
        ):
            raw = m.group(1)

            add_date(
                raw[:4],
                raw[4:6],
                raw[6:8],
                line_start + m.start(),
                line_start + m.end(),
            )

    # fallback général OCR: "01 2026", "02 2026", etc.
    # seulement si aucune vraie date complète n'a été trouvée
    if not found:
        partial_re = re.compile(r"(?<![\d,])([0-3]?\d)\s+(20\d{2})(?!\d)")

        for line_start, line in iter_lines_with_offsets(text):
            if any(x in line for x in [
                "الحساب", "باسحلا", "account", "iban", "الفترة", "ةرتفلا"
            ]):
                continue

            for m in partial_re.finditer(line):
                day, year = m.groups()

                if not (1 <= int(day) <= 31):
                    continue

                month = statement_month or 1

                add_date(
                    int(year),
                    month,
                    int(day),
                    line_start + m.start(),
                    line_start + m.end(),
                    partial=True,
                )

    unique = {}
    for d in found:
        unique[(d["date"], d["start"])] = d

    return sorted(unique.values(), key=lambda x: x["start"])



def clean_ocr_amount_raw(raw: str) -> str:
    """Normalize common Arabic/OCR duplicated amount fragments without changing valid formats."""
    raw = raw.strip()

    # OCR duplicates: 149,149,00 -> 149,00 ; 399,399,00 -> 399,00
    raw = re.sub(r"^(\d{1,3}),\1,", r"\1,", raw)

    # OCR prefix before amount: 5,500,00 -> 500,00
    raw = re.sub(r"^(\d),(\d{3},\d{2})$", r"\2", raw)

    return raw


def extract_money_values_from_window(amount_window: str) -> list[float]:
    """
    General Arabic bank OCR amount extraction.

    Strategy:
    - Work line by line.
    - Prefer the last physical OCR line containing at least 2 money values.
      This avoids polluted lines such as:
          1182 388.45
          388,45 23 221,77
      where the second line is the reliable transaction/balance pair.
    - Keep OCR order: first value = probable transaction, last value = probable balance.
    """
    money_re = re.compile(
        r"(?<![\d,\.])"
        r"(?:\d{1,3}(?:[ ,]\d{3})+|\d+)"
        r"(?:[.,]\d{2})"
        r"(?!\d)"
    )

    candidates: list[list[float]] = []

    for line in amount_window.splitlines():
        line_values = []

        for m in money_re.finditer(line):
            raw = clean_ocr_amount_raw(m.group(0))

            try:
                value = parse_amount(raw)
            except Exception:
                continue

            # OCR pollution: ex "182 388.45" should become "388.45" when possible.
            if value > 100000:
                alt = re.search(r"(\d{1,3}[.,]\d{2})$", raw)
                if alt:
                    try:
                        value = parse_amount(alt.group(1))
                    except Exception:
                        continue
                else:
                    continue

            # Defensive guard: avoid impossible synthetic artifacts.
            if value <= 0 or value > 1000000:
                continue

            if not any(abs(value - old) < 0.01 for old in line_values):
                line_values.append(value)

        if len(line_values) >= 2:
            candidates.append(line_values)

    if candidates:
        # Use the last reliable line. In Arabic OCR, duplicated English/localized
        # amount lines often appear before the final amount+balance line.
        return candidates[-1]

    # Fallback: no line has two values, use all unique values in OCR order.
    values = []
    for m in money_re.finditer(amount_window):
        raw = clean_ocr_amount_raw(m.group(0))

        try:
            value = parse_amount(raw)
        except Exception:
            continue

        if value > 100000:
            alt = re.search(r"(\d{1,3}[.,]\d{2})$", raw)
            if alt:
                try:
                    value = parse_amount(alt.group(1))
                except Exception:
                    continue
            else:
                continue

        if value <= 0 or value > 1000000:
            continue

        if not any(abs(value - old) < 0.01 for old in values):
            values.append(value)

    return values



def classify_by_keywords(text: str) -> str:
    lower = text.lower()

    if any(k in lower for k in EXPENSE_KEYWORDS):
        return "expense"

    if any(k in lower for k in INCOME_KEYWORDS):
        return "income"

    return "income"


def resolve_arabic_row_amount(row: dict, prev_balance: float | None) -> tuple[float, float, str]:
    """Resolve transaction amount, balance and type for one OCR row.

    General, conservative strategy:
    1) Keep OCR order: first reliable value = movement candidate, last reliable value = balance candidate.
    2) If a previous balance exists, the balance delta is the source of truth for the sign.
    3) If the detected movement matches the delta, keep the movement value.
    4) If the movement is missing/polluted but the balance delta is plausible, use the delta.
    5) If no balance relation can be proven, fall back to keywords/sign without breaking FR/EN.
    """
    numbers = [float(n) for n in row.get("numbers", []) if n is not None]

    if not numbers:
        return 0.0, 0.0, "income"

    probable_tx = float(row.get("probable_tx") or numbers[0])
    probable_balance = float(row.get("probable_balance") or numbers[-1])

    if prev_balance is not None and len(numbers) >= 2:
        # First trust the detected balance column when it is plausible.
        delta = round(probable_balance - prev_balance, 2)

        if abs(delta) > 0.01 and abs(delta) < 100000:
            tolerance = max(0.15, abs(probable_tx) * 0.002)
            delta_type = "income" if delta > 0 else "expense"

            if abs(abs(delta) - abs(probable_tx)) <= tolerance:
                return abs(probable_tx), probable_balance, delta_type

            # General fallback for rows with fees/taxes/merged OCR: net cash movement equals balance delta.
            # If explicit row keywords exist, they can override the sign for rare statements where
            # the displayed balance delta and transaction columns disagree due to OCR/table noise.
            keyword_type = classify_by_keywords(row.get("text", ""))
            if keyword_type in ("expense", "income"):
                return abs(delta), probable_balance, keyword_type

            return abs(delta), probable_balance, delta_type

        # If the probable balance is not usable, try every possible balance candidate.
        candidates = []
        for bal in numbers:
            if bal <= 0:
                continue

            candidate_delta = round(bal - prev_balance, 2)
            if abs(candidate_delta) < 0.01 or abs(candidate_delta) > 100000:
                continue

            for tx in numbers:
                if abs(tx - bal) < 0.01:
                    continue

                tolerance = max(0.15, abs(tx) * 0.002)
                score = abs(abs(candidate_delta) - abs(tx))

                if score <= tolerance:
                    position_penalty = 0 if abs(bal - probable_balance) < 0.01 else 0.05
                    candidates.append((score + position_penalty, tx, bal, candidate_delta))

        if candidates:
            _, tx, bal, candidate_delta = min(candidates, key=lambda x: x[0])
            return abs(tx), bal, "income" if candidate_delta > 0 else "expense"

    # No reliable previous balance: use OCR-order fallback and text hints.
    tx_type = classify_by_keywords(row.get("text", ""))
    return abs(probable_tx), probable_balance, tx_type

def extract_arabic_ocr_transactions(text: str) -> list[dict]:
    if not is_arabic_text(text):
        return []

    normalized = normalize_arabic_digits(text)
    normalized = clean_db_text(normalized)
    normalized = normalized.replace("\u00a0", " ").replace("\u202f", " ")
    normalized = normalized.replace("،", ",")
    normalized = "\n".join(" ".join(l.split()) for l in normalized.splitlines())

    currency = detect_currency(text)
    print("CURRENCY_DETECTED:", currency)

    print("=== AR DEBUG START ===")
    print("TEXT_LENGTH:", len(normalized))
    dates = find_arabic_ocr_dates(normalized)
    print("DATES_FOUND:", [d["clean"] for d in dates])
    print(
        "AMOUNTS_FOUND:",
        re.findall(
            r"\d{1,3}(?:[ ,]\d{3})*(?:[.,]\d{2})",
            normalized
        )[:30]
    )

    amount_pattern = r"\d{1,3}(?:[ ,]\d{3})*(?:[.,]\d{2})"

    rows = []

    for dm in dates:
        print("---- DATE LOOP ----")
        print("DATE:", dm["clean"])

        date_raw = dm["clean"]

        # Build one transaction segment from this date to the next detected date.
        # This is safer than using physical OCR lines because RTL extraction can place
        # amount/balance pairs before the next date on the same line.
        next_date_start = None

        for d in dates:
            if d["start"] > dm["start"]:
                next_date_start = d["start"]
                break

        window_start_abs = dm["start"]

        if next_date_start is not None:
            window = normalized[dm["start"]:next_date_start]
        else:
            line_end = normalized.find("\n", dm["end"])

            if line_end == -1:
                line_end = len(normalized)

            next_line_end = normalized.find("\n", line_end + 1)

            if next_line_end == -1:
                next_line_end = len(normalized)

            window = normalized[dm["start"]:next_line_end]

        # ignore lignes header/période
        if any(x in window for x in [
            "الفترة",
            "ةرتفلا",
            "period",
            "statement"
        ]):
            continue

        # enlever la date de la ligne avant extraction montants
        amount_window = (
            window[:dm["start"] - window_start_abs]
            +
            window[dm["end"] - window_start_abs:]
        )

        # retirer toutes les dates OCR restantes du segment avant montants
        amount_window = re.sub(
            r"(?<![\d,])([0-3]?\d)\s*[./-]\s*([01]?\d)\s*[./-]\s*(\d{2,4})(?!\d)",
            " ",
            amount_window,
        )

        amount_window = re.sub(
            r"(?<!\d)(20\d{2}[01]\d[0-3]\d)(?!\d)",
            " ",
            amount_window,
        )

        amount_window = re.sub(
            r"(?<!\d)([0-3]\d[0-1]\d20\d{2})(?!\d)",
            " ",
            amount_window,
        )

        if dates:
            amount_window = re.sub(
                r"^\s*([0-3]?\d)\s+(20\d{2})\b",
                " ",
                amount_window,
            )

        print("WINDOW:")
        print(window)

        values = extract_money_values_from_window(amount_window)

        print("WINDOW_AMOUNTS:", values)

        if len(values) < 2:
            continue

        # garder l'ordre OCR réel de la ligne:
        # premier montant = transaction probable, dernier montant = solde probable
        clean = values[:4]

        rows.append({
            "date": dm["date"],
            "numbers": clean,
            "text": window,
            "probable_balance": clean[-1],
            "probable_tx": clean[0],
        })

    seen = set()
    filtered = []

    for row in rows:
        key = (
            row["date"],
            row["probable_tx"],
            row["probable_balance"],
        )

        if key not in seen:
            seen.add(key)
            filtered.append(row)

    rows = filtered

    transactions = []
    previous_balance = None

    for row in rows:
        numbers = row.get("numbers", [])

        if len(numbers) < 2:
            continue

        row_text_lower = str(row.get("text", "")).lower()
        is_internal_transfer = any(
            keyword.lower() in row_text_lower
            for keyword in INTERNAL_TRANSFER_KEYWORDS
        )

        tx_amount, balance, tx_type = resolve_arabic_row_amount(
            row,
            previous_balance,
        )

        row["resolved_balance"] = balance
        previous_balance = balance

        # Internal transfers still update the running balance chain, but are not
        # counted as income/expense because they are movements between own accounts.
        if is_internal_transfer:
            continue

        transactions.append({
            "date": row["date"],
            "description": clean_db_text(row["text"][:300]),
            "amount": tx_amount if tx_type == "income" else -abs(tx_amount),
            "type": tx_type,
            "currency": currency,
        })

    print("ROWS_BUILT:", rows)

    for t in transactions:
        print("AR_TX:", t)

    print("ARABIC_BYPASS_COUNT:", len(transactions))
    print("FINAL_TXS", transactions)
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
                "description": clean_db_text(clean_line),
                "amount": amount,
                "type": transaction_type,
            }
        )

    print("FINAL_TXS", transactions)
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
