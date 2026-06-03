import os
import re
from collections import Counter
from datetime import datetime


DEBUG_FINANCE_EXTRACTOR = os.getenv("FINANCE_EXTRACTOR_DEBUG", "0") == "1"


def debug_log(*args):
    if DEBUG_FINANCE_EXTRACTOR:
        print(*args)

debug_log("RUNEXA_FINANCE_EXTRACTOR_VERSION", "international-multipass-v7-kpi-neutral-internal-transfers")
CURRENCY_CODES = ["USD", "EUR", "GBP", "AED", "MAD", "CAD", "AUD", "JOD", "SAR", "QAR", "KWD", "BHD", "OMR", "DZD", "TND", "EGP", "CHF", "JPY", "CNY", "INR", "TRY", "NGN", "ZAR", "MULTI"]

CANADA_BANKS = [
    # Big Six / grandes banques canadiennes
    "BANK OF MONTREAL",
    "BMO",
    "BMO BANK OF MONTREAL",
    "BANQUE DE MONTREAL",
    "BANQUE DE MONTRÉAL",
    "BANQUE BMO",

    "TD CANADA TRUST",
    "TD BANK",
    "TORONTO-DOMINION BANK",
    "THE TORONTO-DOMINION BANK",
    "BANQUE TD",
    "BANQUE TORONTO-DOMINION",

    "RBC",
    "ROYAL BANK",
    "ROYAL BANK OF CANADA",
    "RBC ROYAL BANK",
    "BANQUE ROYALE",
    "BANQUE ROYALE DU CANADA",
    "RBC BANQUE ROYALE",

    "SCOTIABANK",
    "SCOTIA",
    "BANK OF NOVA SCOTIA",
    "THE BANK OF NOVA SCOTIA",
    "BANQUE DE NOUVELLE ECOSSE",
    "BANQUE DE NOUVELLE-ECOSSE",
    "BANQUE SCOTIA",

    "CIBC",
    "CIBC BANK",
    "CANADIAN IMPERIAL BANK OF COMMERCE",
    "BANQUE CANADIENNE IMPERIALE DE COMMERCE",
    "BANQUE CANADIENNE IMPÉRIALE DE COMMERCE",
    "BANQUE CIBC",

    "NATIONAL BANK",
    "NATIONAL BANK OF CANADA",
    "NBC",
    "BANQUE NATIONALE",
    "BANQUE NATIONALE DU CANADA",

    # Quebec / caisses / credit unions
    "DESJARDINS",
    "DESJARDINS GROUP",
    "GROUPE DESJARDINS",
    "CAISSE DESJARDINS",
    "CAISSE POPULAIRE DESJARDINS",
    "FEDERATION DES CAISSES DESJARDINS",
    "FÉDÉRATION DES CAISSES DESJARDINS",

    "LAURENTIAN BANK",
    "LAURENTIAN BANK OF CANADA",
    "LBC",
    "BANQUE LAURENTIENNE",
    "BANQUE LAURENTIENNE DU CANADA",

    "MERIDIAN",
    "MERIDIAN CREDIT UNION",
    "COAST CAPITAL",
    "COAST CAPITAL SAVINGS",
    "VANCITY",
    "VANCOUVER CITY SAVINGS CREDIT UNION",
    "SERVUS CREDIT UNION",
    "AFFINITY CREDIT UNION",
    "CONEXUS CREDIT UNION",
    "DUCA CREDIT UNION",
    "ALTERNATIVE SAVINGS",
    "ALTERNATIVE SAVINGS CREDIT UNION",

    # Canadian online / direct banks
    "TANGERINE",
    "TANGERINE BANK",
    "BANQUE TANGERINE",
    "SIMPLII",
    "SIMPLII FINANCIAL",
    "PC FINANCIAL",
    "PRESIDENT'S CHOICE FINANCIAL",
    "PC MONEY",
    "EQ BANK",
    "EQUITABLE BANK",
    "EQUITABLE BANK OF CANADA",
    "BANQUE EQUITABLE",
    "BANQUE ÉQUITABLE",
    "MOTUSBANK",
    "MOTUS BANK",
    "KOHO",
    "NEO FINANCIAL",
    "WEALTHSIMPLE",
    "WEALTHSIMPLE CASH",

    # Regional / specialized Canadian banks
    "CANADIAN WESTERN BANK",
    "CWB",
    "CWB BANK",
    "ATB",
    "ATB FINANCIAL",
    "ATB FINANCIAL BANK",
    "MANULIFE BANK",
    "MANULIFE BANK OF CANADA",
    "BANQUE MANUVIE",
    "BANQUE MANUVIE DU CANADA",
    "HOME BANK",
    "HOME TRUST",
    "HOME TRUST COMPANY",
    "FAIRSTONE BANK",
    "FAIRSTONE BANK OF CANADA",
    "HAVENTREE BANK",
    "BRIDGEWATER BANK",
    "VERSABANK",
    "FIRST NATIONS BANK",
    "FIRST NATIONS BANK OF CANADA",
    "FNBC",
    "PEOPLES BANK",
    "PEOPLES BANK OF CANADA",
    "PEOPLES TRUST",
    "PEOPLES TRUST COMPANY",
    "OAKEN FINANCIAL",
    "OAKEN",
    "MOTIVE FINANCIAL",
    "MOTIVE",
    "ACHIEVA FINANCIAL",
    "OUTLOOK FINANCIAL",
    "MAXA FINANCIAL",
    "ACCELErate FINANCIAL",

    # Foreign banks / Canadian subsidiaries / legacy statements
    "HSBC",
    "HSBC BANK CANADA",
    "BANQUE HSBC CANADA",
    "RBC HSBC",
    "ICICI BANK CANADA",
    "ICICI CANADA",
    "SBI CANADA BANK",
    "STATE BANK OF INDIA CANADA",
    "HABIB CANADIAN BANK",
    "HABIB BANK CANADA",
    "CTBC BANK CANADA",
    "SHINHAN BANK CANADA",
    "KEB HANA BANK CANADA",
    "WOORI BANK CANADA",
    "BANK OF CHINA CANADA",
    "BANK OF CHINA",
    "INDUSTRIAL AND COMMERCIAL BANK OF CHINA CANADA",
    "ICBC CANADA",
    "CITIBANK CANADA",
    "CITI CANADA",

    # Common OCR/header variants
    "BMO BANK",
    "TD TRUST",
    "TD",
    "BANQUE RBC",
    "RBC BANQUE",
    "SCOTIA BANK",
    "BANQUE SCOTIA",
    "BANQUE DE MONTREAL",
    "BANQUE DE MONTRÉAL",
    "BANQUE NATIONALE",
    "BANQUE DESJARDINS",
]


AUSTRALIA_BANKS = [
    # Major Australian banks / Big Four
    "COMMONWEALTH BANK",
    "COMMONWEALTH BANK OF AUSTRALIA",
    "COMMBANK",
    "CBA",
    "WESTPAC",
    "WESTPAC BANKING CORPORATION",
    "NAB",
    "NATIONAL AUSTRALIA BANK",
    "ANZ",
    "ANZ BANK",
    "AUSTRALIA AND NEW ZEALAND BANKING",
    "AUSTRALIA AND NEW ZEALAND BANKING GROUP",

    # Australian regional / digital / specialist banks
    "MACQUARIE BANK",
    "MACQUARIE",
    "BENDIGO BANK",
    "BENDIGO AND ADELAIDE BANK",
    "ADELAIDE BANK",
    "ING AUSTRALIA",
    "ING BANK AUSTRALIA",
    "ING DIRECT AUSTRALIA",
    "AMP BANK",
    "AMP",
    "SUNCORP BANK",
    "SUNCORP",
    "BANKWEST",
    "BANK OF WESTERN AUSTRALIA",
    "BOQ",
    "BANK OF QUEENSLAND",
    "ME BANK",
    "ME BANKING",
    "UBANK",
    "U BANK",
    "RABOBANK AUSTRALIA",
    "RABOBANK",
    "JUDO BANK",
    "VOLT BANK",
    "86400",
    "UP BANK",
    "UP MONEY",
    "BANK AUSTRALIA",
    "AUSWIDE BANK",
    "HERITAGE BANK",
    "PEOPLE'S CHOICE",
    "PEOPLES CHOICE",
    "GREAT SOUTHERN BANK",
    "DEFENCE BANK",
    "TEACHERS MUTUAL BANK",
    "POLICE BANK",
    "IMB BANK",
    "NEWCASTLE PERMANENT",
    "P&N BANK",
    "BEYOND BANK",
    "MYSTATE BANK",
    "REGIONAL AUSTRALIA BANK",
    "BANK OF SYDNEY",
    "HSBC AUSTRALIA",
    "HSBC BANK AUSTRALIA",
    "CITIBANK AUSTRALIA",
]

COUNTRY_TO_CURRENCY = {
    "CANADA": "CAD",
}

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
    "versement",
    "versement espece",
    "versement espèces",
    "dépôt",
    "depot",
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


EXPENSE_KEYWORDS += [
    "naps purchase",
    "naps atm",
    "cbq purchase",
    "electron auth",
    "card bill payment",
    "transfer charge",
    "thirdparty transfer",
    "loan repayment",
    "loan repayment - princ",
    "funds transfer",
]

INCOME_KEYWORDS += [
    "transfer - credit",
    "salary transfer",
    "salary transfer cdd",
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
    "vir recu",
    "vir reçu",
    "vir inst recu",
    "vir inst reçu",
    "vir.web recu",
    "vir.web reçu",
    "vir web recu",
    "vir web reçu",
    "vir emis",
    "vir émis",
    "vir.emis",
    "vir emis web",
    "virement emis",
    "virement émis",
    "prelevement",
    "prélèvement",
    "paiement",
    "paiement carte",
    "carte",
    "retrait",
    "gab",
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
    # International money tokens:
    #   1,234.56  (US/UK/GCC)
    #   1.234,56  (FR/EU)
    #   1234.56 / 1234,56
    # Spaces are intentionally NOT accepted here because OCR often merges
    # amount + balance as: "500 588.33". Arabic OCR has its own path.
    r"(?:\d{1,3}(?:[,.]\d{3})+|\d+)"
    r"(?:[.,]\d{2,3})"
    r"(?![A-Za-z0-9])"
)



def is_arabic_text(text: str) -> bool:
    return bool(re.search(r"[\u0600-\u06FF]", text))


def is_mostly_arabic_text(text: str) -> bool:
    letters = re.findall(r"[A-Za-z\u0600-\u06FF]", str(text or ""))

    if not letters:
        return False

    arabic_letters = re.findall(r"[\u0600-\u06FF]", str(text or ""))

    return len(arabic_letters) / len(letters) >= 0.35


def normalize_arabic_ocr_lines(text: str) -> str:
    if not is_mostly_arabic_text(text):
        return text

    lines = [
        " ".join(line.split())
        for line in text.splitlines()
        if " ".join(line.split())
    ]

    rebuilt = []

    amount_token = r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:[.,]\d{2,3})"

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

        if re.search(
            r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)",
            token,
            flags=re.IGNORECASE,
        ):
            return token

        return token.translate(translation)

    return re.sub(
        r"[A-Za-z0-9+\-.,/]+",
        fix_token,
        value,
    )

def parse_amount(value: str) -> float:
    """Parse international bank amounts safely.

    Supports both major formats without assuming one country:
    - US/UK/GCC: 1,234.56
    - FR/EU:     1.234,56
    - Plain:     1234.56 / 1234,56

    The decimal separator is the last separator when both comma and dot are
    present. This fixes French statements where 9.450,00 must be 9450.00,
    while keeping 9,450.00 as 9450.00.
    """
    raw = str(value or "").strip()
    raw = normalize_arabic_digits(raw)
    raw = raw.replace(" ", "").replace(" ", "").replace(" ", "")
    raw = re.sub(r"[^0-9,\.\-+]", "", raw)

    if not raw or raw in {"-", "+"}:
        raise ValueError("Invalid amount")

    sign = -1 if raw.startswith("-") else 1
    raw = raw.lstrip("+-")

    if "," in raw and "." in raw:
        last_comma = raw.rfind(",")
        last_dot = raw.rfind(".")

        if last_comma > last_dot:
            # European: 1.234,56
            raw = raw.replace(".", "").replace(",", ".")
        else:
            # US/GCC: 1,234.56
            raw = raw.replace(",", "")

    elif "," in raw:
        parts = raw.split(",")

        if len(parts) > 2:
            # 1,234,567 -> thousands only
            raw = "".join(parts)
        elif len(parts) == 2:
            left, right = parts
            if len(right) in (1, 2):
                raw = left + "." + right
            elif len(right) == 3 and len(left) <= 3:
                # 1,234 -> thousands
                raw = left + right
            else:
                raw = left + "." + right

    elif "." in raw:
        parts = raw.split(".")

        if len(parts) > 2:
            # European thousands with decimal may already have been handled
            # above when comma exists. If only dots exist, treat last 1-2
            # digits as decimal, otherwise all dots are thousands.
            if len(parts[-1]) in (1, 2):
                raw = "".join(parts[:-1]) + "." + parts[-1]
            else:
                raw = "".join(parts)
        elif len(parts) == 2:
            left, right = parts
            if len(right) == 3 and len(left) <= 3:
                raw = left + right
            else:
                raw = left + "." + right

    return sign * float(raw)

def normalize_line_for_amount_detection(line: str) -> str:
    """Remove date-like tokens before money detection.

    This prevents OCR/table rows such as:
        20 04 2026 300,00
    from being misread as:
        6 300,00 -> 6300.00

    The rule is structural and bank-neutral: dates are not transaction
    amounts, so they should not participate in money token matching.
    """
    text = str(line or "")

    date_patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b20\d{6}\b",
        r"\b[0-3]\d[0-1]\d20\d{2}\b",
        r"\b\d{2}[./-]\d{2}[./-]\d{2,4}\b",
        r"\b[0-3]?\d\s+[01]?\d\s+20\d{2}\b",
        r"\b20\d{2}\s+[01]?\d\s+[0-3]?\d\b",
        r"\b\d{1,2}\s+"
        r"(?:january|jan|february|feb|march|mar|april|apr|may|"
        r"june|jun|july|jul|august|aug|september|sept|sep|"
        r"october|oct|november|nov|december|dec)"
        r"\s+\d{2,4}\b",
        r"\b\d{1,2}[- ]"
        r"(?:january|jan|february|feb|march|mar|april|apr|may|"
        r"june|jun|july|jul|august|aug|september|sept|sep|"
        r"october|oct|november|nov|december|dec)"
        r"[- ]\d{2,4}\b",
    ]

    for pattern in date_patterns:
        text = re.sub(
            pattern,
            " ",
            text,
            flags=re.IGNORECASE,
        )

    return re.sub(r"\s+", " ", text).strip()


def extract_money_numbers_safely(line: str) -> list[str]:
    """Return decimal money values after removing date noise.

    This is used by the generic bank parser to avoid combining the last digit
    of a date with a transaction amount, for example:
        2026 100,00 -> 6100,00
    """
    cleaned = normalize_line_for_amount_detection(line)

    return re.findall(
        MONEY_NUMBER_PATTERN,
        cleaned,
    )


def looks_like_debit_description(line: str) -> bool:
    lower = line.lower()

    debit_markers = [
        "paiement",
        "operation au debit",
        "opération au débit",
        "debit",
        "débit",
        "retrait",
        "gab",
        "awb gab",
        "awbgab",
        "frais",
        "commission",
        "achat",
        "card",
        "payment",
        "withdrawal",
        "atm",
        "purchase",
        "vir emis",
        "vir émis",
        "vir.emis",
        "virement emis",
        "virement émis",
        "vers ",
    ]

    return any(marker in lower for marker in debit_markers)


def looks_like_credit_description(line: str) -> bool:
    lower = line.lower()

    credit_markers = [
        "virement recu",
        "virement reçu",
        "vir recu",
        "vir reçu",
        "vir.web recu",
        "vir.web reçu",
        "vir web recu",
        "vir web reçu",
        "vir inst recu",
        "vir inst reçu",
        "recu de",
        "reçu de",
        "credit",
        "crédit",
        "deposit",
        "versement",
        "versement espece",
        "versement espèce",
        "versement espèces",
        "depot",
        "dépôt",
        "incoming",
        "received",
        "salary",
        "payroll",
    ]

    return any(marker in lower for marker in credit_markers)


def extract_debit_credit_from_description(line: str) -> tuple[float | None, str | None]:
    """Infer amount/type from debit-credit bank tables.

    This is still general: many bank PDFs expose separate debit and credit
    columns, but OCR often flattens the row into one line. When the
    description clearly says incoming/received, the single visible amount is a
    credit. When it clearly says card/ATM/debit/fee/outgoing, the single
    visible amount is a debit.
    """
    numbers = extract_money_numbers_safely(line)

    if not numbers:
        return None, None

    amount = parse_amount(numbers[0])

    if looks_like_credit_description(line):
        return abs(amount), "income"

    if looks_like_debit_description(line):
        return -abs(amount), "expense"

    return None, None


def pick_bank_amount(
    numbers: list[str],
    line: str,
    account_currency: str | None = None,
) -> float:
    text = normalize_line_for_amount_detection(line.upper())

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

    money_numbers = extract_money_numbers_safely(line)

    if money_numbers:
        return parse_amount(money_numbers[-1])

    raise ValueError(
        "No reliable money amount found in transaction line."
    )




def pick_transaction_amount_from_tabular_numbers(
    numbers: list[str],
    line: str,
    account_currency: str | None = None,
) -> float:
    safe_numbers = extract_money_numbers_safely(line)

    if len(safe_numbers) >= 2:
        return parse_amount(safe_numbers[-2])

    if len(safe_numbers) == 1:
        return parse_amount(safe_numbers[0])

    return pick_bank_amount(
        numbers,
        line,
        account_currency=account_currency,
    )



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


def try_parse_date(raw: str):
    raw = raw.strip()

    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y.%m.%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%d.%m.%y",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%m.%d.%Y",
        "%m/%d/%y",
        "%m-%d-%y",
        "%m.%d.%y",
        "%d %b %Y",
        "%d %B %Y",
        "%d %b %y",
        "%d %B %y",
        "%d-%b-%Y",
        "%d-%B-%Y",
        "%d-%b-%y",
        "%d-%B-%y",
        "%b %d %Y",
        "%B %d %Y",
        "%b %d %y",
        "%B %d %y",
        "%b-%d-%Y",
        "%B-%d-%Y",
        "%b-%d-%y",
        "%B-%d-%y",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(raw, fmt)

            if is_reasonable_year(parsed.year):
                return parsed.date().isoformat()
        except ValueError:
            continue

    return None


def extract_date(
    line: str,
    default_year: int | None = None,
    prefer_us_date: bool = False,
):
    date_candidates = re.findall(
        r"\b(?:"
        r"\d{4}[-/.]\d{1,2}[-/.]\d{1,2}"
        r"|"
        r"\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}"
        r"|"
        r"\d{1,2}[- ](?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)[- ]\d{2,4}"
        r"|"
        r"(?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)[- ]\d{1,2}[- ]\d{2,4}"
        r")\b",
        line,
        flags=re.IGNORECASE,
    )

    for raw_date in date_candidates:
        parsed = try_parse_date(raw_date)
        if parsed:
            return parsed

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


    # Compact DMY format used by AU/UK/EU OCR statements: DDMMYYYY
    # Example: 01022026 -> 2026-02-01. This must be checked before
    # generic numeric date formats because degraded OCR often removes separators.
    compact_dmy_match = re.search(r"\b([0-3]\d)([0-1]\d)(20\d{2})\b", line)

    if compact_dmy_match:
        try:
            parsed = datetime(
                int(compact_dmy_match.group(3)),
                int(compact_dmy_match.group(2)),
                int(compact_dmy_match.group(1)),
            )

            if not is_reasonable_year(parsed.year):
                return None

            return parsed.date().isoformat()

        except ValueError:
            return None

    spaced_dmy_match = re.search(
        r"(?<!\d)([0-3]?\d)\s+([01]?\d)\s+(20\d{2})(?!\d)",
        line,
    )

    if spaced_dmy_match:
        day, month, year = spaced_dmy_match.groups()

        try:
            parsed = datetime(
                int(year),
                int(month),
                int(day),
            )

            if is_reasonable_year(parsed.year):
                return parsed.date().isoformat()

        except ValueError:
            return None


    text_month_us_match = re.search(
        r"\b("
        r"jan|january|feb|february|mar|march|apr|april|may|"
        r"jun|june|jul|july|aug|august|sep|sept|september|"
        r"oct|october|nov|november|dec|december"
        r")\s+(\d{1,2})\s+(\d{2,4})\b",
        line,
        flags=re.IGNORECASE,
    )

    if text_month_us_match:
        month_key = text_month_us_match.group(1).lower()
        day = int(text_month_us_match.group(2))
        year = int(text_month_us_match.group(3))

        if year < 100:
            year += 2000

        month = int(MONTH_ALIASES[month_key])

        try:
            parsed = datetime(year, month, day)

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

    # Bank-table OCR format:
    # code date description value-date amount
    # Example:
    # 0016BK 08 04 VIR.WEB RECU DE NAME 08 04 2026 500,00
    # This is common in statements where dates are printed as separate columns.
    bank_table_dates = re.findall(
        r"(?<!\d)([0-3]?\d)\s+([01]?\d)(?!\d)",
        line,
    )

    if bank_table_dates:
        for day_text, month_text in reversed(bank_table_dates):
            day = int(day_text)
            month = int(month_text)

            year_match = re.search(r"\b(20\d{2})\b", line)
            year = int(year_match.group(1)) if year_match else (default_year or datetime.now().year)

            try:
                parsed = datetime(year, month, day)

                if is_reasonable_year(parsed.year):
                    return parsed.date().isoformat()

            except ValueError:
                continue

    match = re.search(
        r"\b(\d{2}[./-]\d{2}(?:[./-]\d{2,4})?)\b",
        line,
    )

    if not match:
        return None

    raw = match.group(1)

    dmy_formats_with_year = (
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%d.%m.%y",
    )

    us_formats_with_year = (
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%m.%d.%Y",
        "%m/%d/%y",
        "%m-%d-%y",
        "%m.%d.%y",
    )

    formats_with_year = (
        us_formats_with_year + dmy_formats_with_year
        if prefer_us_date
        else dmy_formats_with_year + us_formats_with_year
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
    prefer_us_date: bool = False,
) -> bool:
    if not extract_date(line, default_year=default_year, prefer_us_date=prefer_us_date):
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
        r"\b(?:[0-3]\d[0-1]\d20\d{2}|20\d{2}[0-1]\d[0-3]\d)\b",
        "",
        remaining,
    )

    remaining = re.sub(
        r"\b\d{2}[./-]\d{2}(?:[./-]\d{2,4})?\b",
        "",
        remaining,
    )

    return remaining.strip() == ""



def split_compact_multi_transaction_lines(
    lines: list[str],
    default_year: int | None = None,
    prefer_us_date: bool = False,
) -> list[str]:
    """Split compact OCR lines that contain multiple dated transactions.

    Some PDFs/OCR outputs compress several rows into one physical line, e.g.:
        01/03/2026 Salary +3200,00 02/03/2026 Carrefour -84,56

    This structural normalization is intentionally language-neutral and does
    not change French, English, or Arabic classification rules. It only turns
    compact non-Arab rows into normal one-transaction-per-line candidates so
    the existing parser can process them safely.
    """
    date_token_re = re.compile(
        r"(?<!\d)(?:"
        r"\d{4}-\d{2}-\d{2}"
        r"|\d{1,2}[./-]\d{1,2}[./-]\d{2,4}"
        r"|\d{1,2}[- ](?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)[- ]\d{2,4}"
        r"|(?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)[- ]\d{1,2}[- ]\d{2,4}"
        r")(?!\d)",
        flags=re.IGNORECASE,
    )

    rebuilt: list[str] = []

    for line in lines:
        if is_arabic_text(line):
            rebuilt.append(line)
            continue

        matches = list(date_token_re.finditer(line))

        if len(matches) <= 1:
            rebuilt.append(line)
            continue

        prefix = line[:matches[0].start()].strip()

        if prefix:
            previous_needs_prefix = (
                rebuilt
                and extract_date(
                    rebuilt[-1],
                    default_year=default_year,
                    prefer_us_date=prefer_us_date,
                ) is not None
                and not re.search(MONEY_NUMBER_PATTERN, rebuilt[-1])
            )

            if previous_needs_prefix:
                rebuilt[-1] = f"{rebuilt[-1]} {prefix}".strip()
                debug_log(
                    "TX_DEBUG: compact_prefix_attached",
                    {"prefix": prefix, "combined": rebuilt[-1]},
                )

                for idx, match in enumerate(matches):
                    start = match.start()
                    end = matches[idx + 1].start() if idx + 1 < len(matches) else len(line)
                    segment = line[start:end].strip()

                    if segment:
                        rebuilt.append(segment)
                        debug_log(
                            "TX_DEBUG: compact_multi_tx_split",
                            {"segment": segment},
                        )

                continue
            else:
                first_segment = line[matches[0].start():matches[1].start()].strip()
                rebuilt.append(f"{prefix} {first_segment}".strip())
                debug_log(
                    "TX_DEBUG: compact_multi_tx_split",
                    {"segment": rebuilt[-1]},
                )

                start_index = 1
                for idx in range(start_index, len(matches)):
                    start = matches[idx].start()
                    end = matches[idx + 1].start() if idx + 1 < len(matches) else len(line)
                    segment = line[start:end].strip()

                    if segment:
                        rebuilt.append(segment)
                        debug_log(
                            "TX_DEBUG: compact_multi_tx_split",
                            {"segment": segment},
                        )

                continue

        for idx, match in enumerate(matches):
            start = match.start()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(line)
            segment = line[start:end].strip()

            if segment:
                rebuilt.append(segment)
                debug_log(
                    "TX_DEBUG: compact_multi_tx_split",
                    {"segment": segment},
                )

    return rebuilt


def has_transaction_signal(
    line: str,
    default_year: int | None = None,
    prefer_us_date: bool = False,
) -> bool:
    lower = line.lower()

    metadata_check = (
        lower
        .replace("5", "s")
        .replace("0", "o")
        .replace("1", "l")
    )

    metadata_balance_only = any(
        keyword in metadata_check
        for keyword in BALANCE_KEYWORDS
    )

    date_found = extract_date(
        line,
        default_year=default_year,
        prefer_us_date=prefer_us_date,
    ) is not None

    amounts = extract_money_numbers_safely(line)

    signed_amount_found = bool(
        re.search(
            r"[+-]\s*\d",
            line,
        )
    )

    if metadata_balance_only and not (
        date_found and (signed_amount_found or len(amounts) >= 2)
    ):
        return False

    amount_found = bool(amounts)

    signal_found = any(
        keyword in lower
        for keyword in TRANSACTION_SIGNALS
    )

    return date_found and amount_found and (
        signal_found or amount_found
    )



def is_income_priority_description(text: str) -> bool:
    """Return True for income phrases that must override broad expense words.

    This is intentionally general, not bank-specific. Many banks describe
    inbound cashflow with words that also appear in expense rows, for example
    "Salary Payment" or "Payment In". These income phrases must be
    evaluated before generic expense terms such as "payment" or "transfer".
    """
    lower = text.lower()

    priority_phrases = [
        "salary payment",
        "salary deposit",
        "salary credit",
        "payroll",
        "salary",
        "wage",
        "wages",
        "pay credit",
        "payment in",
        "payment received",
        "osko payment in",
        "incoming transfer",
        "transfer received",
        "transfer in",
        "deposit",
        "versement",
        "versement espece",
        "versement espèce",
        "versement espèces",
        "dépôt",
        "depot",
        "received",
        "freelance",
        "client",
        "virement reçu",
        "virement recu",
        "vir recu",
        "vir reçu",
        "vir inst recu",
        "vir inst reçu",
        "vir.web recu",
        "vir.web reçu",
        "vir web recu",
        "vir web reçu",
        "recu de",
        "reçu de",
        "دائن",
        "إيداع",
        "ايداع",
        "راتب",
        "دخل",
        "تحويل وارد",
        "حوالة واردة",
    ]

    return any(phrase in lower for phrase in priority_phrases)

def detect_type(line: str, amount: float) -> str | None:
    lower = line.lower()

    # Explicit transaction signs are the strongest signal when present.
    # Use signed-number detection instead of raw "+" / "-" so ISO dates
    # such as 2026-02-02 do not make neutral rows look like expenses.
    signed_positive_amount = bool(re.search(r"(?<!\d)\+\s*\d", line))
    signed_negative_amount = bool(re.search(r"(?<!\d)-\s*\d", line))

    if amount > 0 and signed_positive_amount:
        return "income"

    if amount < 0 or signed_negative_amount:
        return "expense"

    # Strong outgoing obligations should stay expenses even if they contain
    # broad words that can appear in other contexts.
    if any(
        keyword in lower
        for keyword in [
            "loyer",
            "rent",
            "mortgage",
            "loan payment",
            "transfer to loan",
            "outgoing transfer",
            "transfer sent",
            "vir emis",
            "vir émis",
            "vir.emis",
            "vir emis web",
            "virement emis",
            "virement émis",
        ]
    ):
        return "expense"

    # General income-priority rule: inbound phrases must be checked before
    # generic expense words such as "payment".
    if is_income_priority_description(lower):
        return "income"

    if any(keyword in lower for keyword in EXPENSE_KEYWORDS):
        return "expense"

    if any(keyword in lower for keyword in INCOME_KEYWORDS):
        return "income"

    if amount < 0:
        return "expense"

    # Neutral descriptions should not default to income.
    # Leave the type unknown so running-balance authority can decide the sign.
    return None

def extract_transaction_amount(line: str) -> float | None:
    numbers = extract_money_numbers_safely(line)

    if not numbers:
        return None

    signed_match = re.search(
        r"([+-])\s*("
        r"(?:\d{1,3}(?:[ ,]\d{3})+|\d+)"
        r"(?:[.,]\d{2})"
        r")",
        normalize_line_for_amount_detection(line),
    )

    if signed_match:
        amount = parse_amount(signed_match.group(2))
        return amount if signed_match.group(1) == "+" else -amount

    if len(numbers) >= 2:
        return parse_amount(numbers[0])

    return parse_amount(numbers[0])



def extract_us_debit_credit_balance(line: str):
    numbers = extract_money_numbers_safely(line)

    if len(numbers) < 3:
        return None, None

    debit = parse_amount(numbers[-3])
    credit = parse_amount(numbers[-2])
    balance = parse_amount(numbers[-1])

    debug_log(
        "TX_DEBUG: us_debit_credit_balance",
        {"debit": debit, "credit": credit, "balance": balance},
    )

    if credit > 0 and debit == 0:
        return credit, "income"

    if debit > 0 and credit == 0:
        return -debit, "expense"

    return None, None


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
        r"\b(?:[0-3]\d[0-1]\d20\d{2}|20\d{2}[0-1]\d[0-3]\d)\b",
        "",
        without_date,
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


    numbers = extract_money_numbers_safely(without_date)

    if not numbers:
        return None, None

    dc_amount, dc_type = extract_debit_credit_from_description(line)

    if dc_amount is not None:
        debug_log(
            "TX_DEBUG: debit_credit_description",
            {"amount": dc_amount, "type": dc_type, "line": line},
        )
        return dc_amount, dc_type

    # General rule: when the statement shows an explicit + / - sign,
    # the sign is more reliable than generic words such as "payment".
    # Example: "Client Payment +7200.00" must be income, not expense.
    signed_match = re.search(
        r"([+-])\s*("
        r"(?:\d{1,3}(?:[ ,]\d{3})+|\d+)"
        r"(?:[.,]\d{2})"
        r")",
        line,
    )

    if signed_match:
        sign = signed_match.group(1)
        signed_amount = parse_amount(signed_match.group(2))

        debug_log(
            "TX_DEBUG: signed_amount_priority",
            {"sign": sign, "amount": signed_amount},
        )

        if sign == "+":
            return abs(signed_amount), "income"

        return -abs(signed_amount), "expense"

    tabular_us_amount, tabular_us_type = extract_us_debit_credit_balance(line)

    if tabular_us_amount is not None:
        return tabular_us_amount, tabular_us_type

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
        amount = pick_transaction_amount_from_tabular_numbers(numbers, line)

        return amount, "income"

    # Income keywords must be evaluated before generic outgoing words such as
    # "payment". This is a general rule, not a bank-specific exception.
    if is_income_priority_description(description):
        amount = pick_transaction_amount_from_tabular_numbers(numbers, line)

        return abs(amount), "income"

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
            "vir emis",
            "vir émis",
            "vir.emis",
            "vir emis web",
            "virement emis",
            "virement émis",
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
        amount = pick_transaction_amount_from_tabular_numbers(numbers, line)

        return -abs(amount), "expense"

    if any(
        keyword in description
        for keyword in [
            "incoming transfer",
            "transfer received",
            "virement reçu",
            "virement recu",
            "vir recu",
            "vir reçu",
            "vir inst recu",
            "vir inst reçu",
            "vir.web recu",
            "vir.web reçu",
            "vir web recu",
            "vir web reçu",
            "recu de",
            "reçu de",
            "salary",
            "payroll",
            "wage",
            "deposit",
            "received",
            "freelance",
            "client",
        ]
    ):
        amount = pick_transaction_amount_from_tabular_numbers(numbers, line)

        return amount, "income"

    return None, None


def extract_amount_balance_line(line: str):
    numbers = extract_money_numbers_safely(line)

    if len(numbers) < 2:
        return None, None

    tx_amount = parse_amount(numbers[-2])
    balance = parse_amount(numbers[-1])

    debug_log(
        "TX_DEBUG: amount_balance_line",
        {"tx_amount": tx_amount, "balance": balance},
    )

    text = line.lower()

    if is_income_priority_description(text):
        return abs(tx_amount), "income"

    if any(k in text for k in EXPENSE_KEYWORDS):
        return -abs(tx_amount), "expense"

    if any(k in text for k in INCOME_KEYWORDS):
        return abs(tx_amount), "income"

    # General safety rule for rows shaped like:
    #     date description transaction_amount running_balance
    # The transaction amount is the penultimate money value and the balance is
    # the last money value. Never return the balance as the row amount.
    # Type can remain unknown here; infer_balance_delta_rows() can later use
    # the running balance delta to set income/expense safely.
    return abs(tx_amount), None


def extract_line_balance(line: str) -> float | None:
    numbers = extract_money_numbers_safely(line)

    if len(numbers) < 2:
        return None

    try:
        return parse_amount(numbers[-1])
    except Exception:
        return None


def is_balance_only_line(
    line: str,
    default_year: int | None = None,
    prefer_us_date: bool = False,
) -> bool:
    """Return True for OCR lines that look like a standalone running balance.

    This supports vertical bank tables where OCR splits:
        date
        description
        transaction amount
        running balance

    into separate physical lines. We only treat a line as balance-only when:
    - it has no date;
    - it contains exactly one money value;
    - after removing that money value, no meaningful letters remain.

    This avoids merging normal transaction rows or metadata into the previous row.
    """
    if extract_date(
        line,
        default_year=default_year,
        prefer_us_date=prefer_us_date,
    ):
        return False

    amounts = re.findall(MONEY_NUMBER_PATTERN, line)

    if len(amounts) != 1:
        return False

    remainder = re.sub(
        MONEY_NUMBER_PATTERN,
        "",
        line,
    )

    remainder = re.sub(
        r"[\s|:;,\-–—_/()]+",
        "",
        remainder,
    )

    return remainder == ""


def is_amount_balance_only_row(
    line: str,
    default_year: int | None = None,
    prefer_us_date: bool = False,
) -> bool:
    if not extract_date(line, default_year=default_year, prefer_us_date=prefer_us_date):
        return False

    amounts = extract_money_numbers_safely(line)

    if len(amounts) != 2:
        return False

    cleaned = normalize_line_for_amount_detection(line)
    cleaned = re.sub(MONEY_NUMBER_PATTERN, " ", cleaned)
    cleaned = re.sub(r"[\s|:;,\-–—_/().]+", "", cleaned)

    return cleaned == ""


def attach_following_balance_lines(
    lines: list[str],
    default_year: int | None = None,
    prefer_us_date: bool = False,
) -> list[str]:
    """Attach OCR standalone balance lines to the previous transaction line.

    General case:
        2026-02-05 Interest Credit 9.85
        12,828.45

    becomes:
        2026-02-05 Interest Credit 9.85 12,828.45

    Then infer_balance_delta_rows() can use the balance delta as the authority.
    """
    rebuilt = []
    i = 0

    while i < len(lines):
        current = lines[i]

        current_has_date = extract_date(
            current,
            default_year=default_year,
            prefer_us_date=prefer_us_date,
        ) is not None

        current_amounts = extract_money_numbers_safely(current)

        if (
            current_has_date
            and current_amounts
            and i + 1 < len(lines)
            and is_balance_only_line(
                lines[i + 1],
                default_year=default_year,
                prefer_us_date=prefer_us_date,
            )
        ):
            combined = f"{current} {lines[i + 1]}"

            debug_log(
                "TX_DEBUG: vertical_balance_attached",
                {
                    "transaction_line": current,
                    "balance_line": lines[i + 1],
                    "combined": combined,
                },
            )

            rebuilt.append(combined)
            i += 2
            continue

        rebuilt.append(current)
        i += 1

    return rebuilt


def infer_balance_delta_rows(rows: list[dict]) -> list[dict]:
    """Infer income/expense from running balance deltas.

    General rule for OCR/table rows shaped like:
        date description transaction_amount running_balance

    When current_balance - previous_balance matches the transaction amount,
    the balance delta is stronger than merchant keywords.
    """
    previous_balance = None
    fixed = []

    for row in rows:
        amount = float(row.get("amount", 0) or 0)
        tx_type = row.get("type")
        balance = row.get("_balance")

        if balance is not None and previous_balance is not None:
            delta = round(float(balance) - float(previous_balance), 2)
            tolerance = max(0.02, abs(amount) * 0.002)

            debug_log(
                "TX_DEBUG: balance_authority",
                {
                    "previous": previous_balance,
                    "current": balance,
                    "delta": delta,
                    "original_amount": amount,
                    "original_type": tx_type,
                }
            )

            debug_log(
                "TX_DEBUG: balance_delta_check",
                {
                    "date": row.get("date"),
                    "amount": amount,
                    "previous_balance": previous_balance,
                    "balance": balance,
                    "delta": delta,
                    "tolerance": tolerance,
                },
            )

            if abs(abs(delta) - abs(amount)) <= tolerance:
                if delta > 0:
                    row["type"] = "income"
                    row["amount"] = abs(amount)
                else:
                    row["type"] = "expense"
                    row["amount"] = -abs(amount)

                amount = row["amount"]
                tx_type = row["type"]

                debug_log(
                    "TX_DEBUG: balance_override",
                    {
                        "new_amount": amount,
                        "new_type": tx_type,
                    }
                )

                debug_log(
                    "TX_DEBUG: balance_delta_applied",
                    {
                        "date": row.get("date"),
                        "amount": row.get("amount"),
                        "type": row.get("type"),
                    },
                )

        if balance is not None:
            previous_balance = balance

        fixed.append(row)

    return fixed


def extract_first_amount_after_date(line: str) -> float | None:
    text = re.sub(
        r"\b\d{4}-\d{2}-\d{2}\b",
        "",
        line,
        count=1,
    )

    text = re.sub(
        r"\b(?:[0-3]\d[0-1]\d20\d{2}|20\d{2}[0-1]\d[0-3]\d)\b",
        "",
        text,
        count=1,
    )


    numbers = extract_money_numbers_safely(text)

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



def normalize_identity_text(value: str) -> str:
    """Normalize names/identity fragments for safe matching.

    Used only to detect likely own-account/internal transfers. It removes
    titles, punctuation and excess spaces without changing transaction parsing.
    """
    text = clean_db_text(str(value or "")).lower()
    text = normalize_arabic_digits(text)
    text = re.sub(r"\b(?:mr|mrs|ms|mme|m\.|mlle|dr|docteur|monsieur|madame)\b", " ", text)
    text = re.sub(r"[^a-z0-9àâäéèêëîïôöùûüçñ\u0600-\u06ff]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_account_holder_identity_tokens(text: str) -> set[str]:
    """Extract likely account-holder identity tokens from the statement.

    This is intentionally conservative and language-neutral. It only returns
    names found near common statement owner labels or very common title/name
    patterns printed in bank headers.
    """
    raw = clean_db_text(str(text or ""))
    candidates: set[str] = set()

    patterns = [
        r"(?:account\s+holder|account\s+name|customer\s+name|client\s+name|titulaire|nom\s+du\s+client)\s*[:\-]?\s*([A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ][A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ'\- ]{3,80})",
        r"\b(?:M\.|MR|MME|MRS|MS|DR)\s+([A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ][A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ'\- ]{3,80})",
        r"\b(?:السيد|السيدة|العميل)\s+([\u0600-\u06ff ]{3,80})",
    ]

    stop_words = [
        "RELEVE", "RELEVÉ", "COMPTE", "BANQUE", "BANK", "PAGE",
        "DATE", "VALEUR", "DEBIT", "CREDIT", "SOLDE", "OPERATIONS",
        "SOCIETE", "SOCIÉTÉ", "GENERALE", "GÉNÉRALE", "BRED",
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, raw, flags=re.IGNORECASE):
            candidate = match.group(1)
            candidate = re.split(
                r"\n|\r|\b(?:RELEV[ÉE]|COMPTE|APPT|ETAGE|BOULEVARD|RUE|AVENUE|PAGE|DATE|SOLDE|VOS CONTACTS)\b",
                candidate,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0]
            normalized = normalize_identity_text(candidate)

            if not normalized:
                continue

            words = normalized.split()
            if len(words) < 2 or len(words) > 6:
                continue

            if any(stop.lower() in normalized for stop in stop_words):
                continue

            candidates.add(normalized)

    return candidates


def extract_account_reference_tokens(text: str) -> set[str]:
    """Extract own-account references that may appear again in transfer rows."""
    raw = clean_db_text(str(text or "")).upper()
    tokens: set[str] = set()

    for iban in re.findall(r"\b[A-Z]{2}\d{2}[A-Z0-9 ]{10,34}\b", raw):
        normalized = re.sub(r"\s+", "", iban)
        if len(normalized) >= 12:
            tokens.add(normalized)

    # French/European account-number-like groups printed in headers.
    for number in re.findall(r"\b\d{5}\s+\d{5}\s+\d{8,12}\s+\d{2}\b", raw):
        tokens.add(re.sub(r"\s+", "", number))

    return tokens


def is_internal_transfer(
    transaction_text: str,
    document_text: str | None = None,
) -> bool:
    """Detect internal/own-account transfers without bank-specific patches.

    Goal: keep parsing intact, but exclude own transfers from financial KPIs
    (income, expenses, score, savings opportunities). The transaction remains
    available as type="transfer" so charts/auditing can still see it.

    Conservative signals:
    - explicit internal-transfer wording in EN/FR/AR;
    - transfer row where sender/recipient matches the account holder name;
    - own IBAN/account reference appears in the row.
    """
    tx = clean_db_text(str(transaction_text or ""))
    lower = tx.lower()

    # Exclude FX/wallet/own-account movements already covered by the legacy list.
    if any(keyword.lower() in lower for keyword in INTERNAL_TRANSFER_KEYWORDS):
        return True

    transfer_markers = [
        "virement", "vir ", "vir.", "transfer", "standing order",
        "paylib", "wero", "internal", "own account", "between accounts",
        "تحويل", "حوالة",
    ]

    if not any(marker in lower for marker in transfer_markers):
        return False

    doc = clean_db_text(str(document_text or ""))

    holder_tokens = extract_account_holder_identity_tokens(doc)
    tx_identity = normalize_identity_text(tx)

    for holder in holder_tokens:
        if not holder:
            continue

        holder_words = holder.split()
        enough_words = len(holder_words) >= 2
        if enough_words and holder in tx_identity:
            debug_log(
                "TX_INTERNAL_TRANSFER: holder_match",
                {"holder": holder, "transaction": tx[:180]},
            )
            return True

    account_tokens = extract_account_reference_tokens(doc)
    compact_tx = re.sub(r"\s+", "", tx.upper())

    for token in account_tokens:
        if token and token in compact_tx:
            debug_log(
                "TX_INTERNAL_TRANSFER: account_reference_match",
                {"token": token[-8:], "transaction": tx[:180]},
            )
            return True

    # Generic own-account phrases across EN/FR/AR.
    own_account_phrases = [
        "own account", "my account", "between my accounts",
        "compte propre", "mes comptes", "entre comptes", "virement interne",
        "transfer interne", "épargne", "epargne", "livret", "ldd", "livret a",
        "حسابي", "حساب خاص", "بين حساباتي", "تحويل داخلي",
    ]

    if any(phrase in lower for phrase in own_account_phrases):
        return True

    return False


def mark_internal_transfers(
    transactions: list[dict],
    text: str,
) -> list[dict]:
    """Mark own-account transfers as neutral KPI movements.

    Enterprise-grade rule:
    - keep the transaction row for auditability;
    - preserve the original signed movement in original_amount / gross_amount;
    - set amount = 0.0 and type = "transfer" so every existing downstream
      calculation that sums either by type OR by sign automatically excludes it.

    This prevents internal transfers from inflating income, expenses, scores,
    budget recommendations, savings opportunities, and cashflow risk.
    """
    marked: list[dict] = []

    for tx in transactions:
        row = dict(tx)
        description = str(row.get("description", ""))

        if is_internal_transfer(description, text):
            original_type = row.get("type")
            original_amount = float(row.get("amount", 0) or 0)

            row["type"] = "transfer"
            row["amount"] = 0.0

            # Audit fields: do not lose the bank movement.
            row["original_type"] = original_type
            row["original_amount"] = round(original_amount, 2)
            row["gross_amount"] = round(original_amount, 2)
            row["movement_amount"] = round(original_amount, 2)

            # Explicit KPI exclusion flags for newer services.
            row["is_internal_transfer"] = True
            row["excluded_from_financial_kpis"] = True
            row["exclude_from_income"] = True
            row["exclude_from_expense"] = True
            row["exclude_from_score"] = True
            row["exclude_from_savings"] = True
            row["exclude_from_cashflow"] = True
            row["category_hint"] = row.get("category_hint") or "internal_transfer"
            row["category"] = row.get("category") or "transfers"

            debug_log(
                "TX_INTERNAL_TRANSFER_MARKED",
                {
                    "date": row.get("date"),
                    "original_amount": original_amount,
                    "kpi_amount": row.get("amount"),
                    "original_type": original_type,
                    "description": description[:160],
                },
            )

        marked.append(row)

    return marked


def movement_total_amount(transactions: list[dict], direction: str) -> float:
    """Gross debit/credit total for reconciliation, including transfers.

    Reconciliation must compare against official statement movement totals,
    which include transfers. Financial KPIs later ignore type="transfer".
    """
    total = 0.0

    for tx in transactions:
        amount = float(tx.get("amount", 0) or 0)
        tx_type = tx.get("type")

        if direction == "debit":
            if tx_type == "expense" or amount < 0:
                total += abs(amount)
        elif direction == "credit":
            if tx_type == "income" or amount > 0:
                total += abs(amount)

    return round(total, 2)



def log_final_transactions(transactions: list[dict]) -> None:
    """Log only the transactions that are finally retained.

    Keep this payload intentionally small so debugging stays readable even on
    large statements.
    """
    for tx in transactions:
        debug_log(
            "TX_FINAL",
            {
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "type": tx.get("type"),
                "description": str(tx.get("description", ""))[:80],
            },
        )



def log_currency_detection_result(
    currency: str,
    source: str,
    confidence: int,
    evidence: str | None = None,
):
    """Emit a stable currency confidence debug line without changing return type."""
    payload = {
        "currency": currency,
        "source": source,
        "confidence": confidence,
    }

    if evidence:
        payload["evidence"] = evidence

    debug_log("CURRENCY_DEBUG: result", payload)


def detect_currency(text: str) -> str:
    """Detect currency safely and generally.

    Conservative order:
    1) explicit ISO/symbol/currency-name in the statement;
    2) if the statement is clearly multi-currency and no explicit currency was found, keep unknown;
    3) explicit country/jurisdiction hint -> country's default currency;
    4) bank hint -> country -> country's default currency;
    5) unknown.

    This avoids hardcoding MAD/QAR/SAR globally and keeps FR/EN/US/UK/EU cases safe.
    """
    normalized = normalize_arabic_digits(clean_db_text(text)).upper()

    mixed_currency_markers = [
        "MULTI CURRENCY",
        "MULTICURRENCY",
        "MIXED CURRENCY",
        "MIXED CURRENCIES",
        "MULTI-CURRENCY",
        "COMPTE MULTIDEVISE",
        "MULTI-DEVISE",
        "MULTIDEVISE",
        "DEVISES MULTIPLES",
        "عملات مختلطة",
        "مختلط عملات",
        "متعدد العملات",
        "تالمع طلتخم",
        "تالمعلا ددعتم",
    ]
    is_mixed_currency_document = any(
        marker.upper() in normalized
        for marker in mixed_currency_markers
    )

    # 1) Explicit currency detection: ISO codes, symbols and common names in EN/FR/AR.
    # Keep this before any country/bank fallback. If the document says USD, it must win.
    patterns = [
        ("USD", [r"\bUSD\b", r"\bUS\$\b", r"\$", "US DOLLAR", "U.S. DOLLAR", "DOLLAR US", "DOLLAR AMERICAIN", "DOLLAR AMÉRICAIN", "دولار أمريكي", "يكيرمأ رالود"]),
        ("EUR", [r"\bEUR\b", "€", "EURO", "يورو", "وروي"]),
        ("GBP", [r"\bGBP\b", "£", "POUND STERLING", "STERLING", "LIVRE STERLING", "جنيه إسترليني", "جنيه استرليني"]),
        ("MAD", [r"\bMAD\b", r"\bDH\b", r"\bDHS\b", "DIRHAM MAROCAIN", "MOROCCAN DIRHAM", "DIRHAM MOROCCO", "درهم مغربي", "يبرغم مهرد"]),
        ("DZD", [r"\bDZD\b", "ALGERIAN DINAR", "DINAR ALGERIEN", "DINAR ALGÉRIEN", "دينار جزائري"]),
        ("TND", [r"\bTND\b", "TUNISIAN DINAR", "DINAR TUNISIEN", "دينار تونسي"]),
        ("EGP", [r"\bEGP\b", "EGYPTIAN POUND", "LIVRE EGYPTIENNE", "LIVRE ÉGYPTIENNE", "جنيه مصري"]),
        ("SAR", [r"\bSAR\b", "SAUDI RIYAL", "RIYAL SAOUDIEN", "ريال سعودي", "يدوعس لاير"]),
        ("QAR", [r"\bQAR\b", "QATARI RIYAL", "RIYAL QATARI", "ريال قطري", "يرطق لاير"]),
        ("AED", [r"\bAED\b", "UAE DIRHAM", "EMIRATI DIRHAM", "DIRHAM EMIRATI", "DIRHAM ÉMIRATI", "درهم إماراتي"]),
        ("KWD", [r"\bKWD\b", "KUWAITI DINAR", "DINAR KOWEITIEN", "DINAR KOWEÏTIEN", "دينار كويتي"]),
        ("BHD", [r"\bBHD\b", "BAHRAINI DINAR", "DINAR BAHREINI", "DINAR BAHREÏNI", "دينار بحريني"]),
        ("OMR", [r"\bOMR\b", "OMANI RIAL", "RIAL OMANI", "ريال عماني"]),
        ("JOD", [r"\bJOD\b", "JORDANIAN DINAR", "DINAR JORDANIEN", "دينار أردني"]),
        ("IQD", [r"\bIQD\b", "IRAQI DINAR", "DINAR IRAKIEN", "دينار عراقي"]),
        ("LBP", [r"\bLBP\b", "LEBANESE POUND", "LIVRE LIBANAISE", "ليرة لبنانية"]),
        ("YER", [r"\bYER\b", "YEMENI RIAL", "RIYAL YEMENITE", "RIYAL YÉMÉNITE", "ريال يمني"]),
        ("LYD", [r"\bLYD\b", "LIBYAN DINAR", "DINAR LIBYEN", "دينار ليبي"]),
        ("SDG", [r"\bSDG\b", "SUDANESE POUND", "LIVRE SOUDANAISE", "جنيه سوداني"]),
        ("SYP", [r"\bSYP\b", "SYRIAN POUND", "LIVRE SYRIENNE", "ليرة سورية"]),
        ("CAD", [r"\bCAD\b", "CANADIAN DOLLAR", "DOLLAR CANADIEN", "دولار كندي"]),
        ("AUD", [r"\bAUD\b", "AUSTRALIAN DOLLAR", "DOLLAR AUSTRALIEN", "دولار أسترالي"]),
        ("CHF", [r"\bCHF\b", "SWISS FRANC", "FRANC SUISSE", "فرنك سويسري"]),
        ("JPY", [r"\bJPY\b", "JAPANESE YEN", "YEN JAPONAIS", "ين ياباني"]),
        ("CNY", [r"\bCNY\b", "CHINESE YUAN", "YUAN CHINOIS", "يوان صيني"]),
        ("INR", [r"\bINR\b", "INDIAN RUPEE", "ROUPEE INDIENNE", "روبية هندية"]),
        ("TRY", [r"\bTRY\b", "TURKISH LIRA", "LIVRE TURQUE", "ليرة تركية"]),
        ("NGN", [r"\bNGN\b", "NAIRA", "نيرة"]),
        ("ZAR", [r"\bZAR\b", "RAND", "راند"]),
    ]

    scores = Counter()

    for code, pats in patterns:
        for pat in pats:
            if re.search(pat, normalized, flags=re.IGNORECASE):
                scores[code] += 1

    if scores:
        explicit_codes = [code for code, count in scores.items() if count > 0]

        if is_mixed_currency_document and len(explicit_codes) > 1:
            debug_log("CURRENCY_DEBUG: explicit_multi", dict(scores))
            log_currency_detection_result(
                "MULTI",
                "explicit_multi_currency",
                100,
                str(dict(scores)),
            )
            return "MULTI"

        detected = scores.most_common(1)[0][0]
        debug_log("CURRENCY_DEBUG: explicit", detected, dict(scores))
        log_currency_detection_result(
            detected,
            "explicit_currency",
            100,
            str(dict(scores)),
        )
        return detected

    # If there is no explicit currency and the document says multi-currency,
    # keep the result explicit as MULTI instead of unknown. Downstream code can
    # then avoid pretending there is one reliable statement currency.
    if is_mixed_currency_document:
        debug_log("CURRENCY_DEBUG: mixed_currency_document -> MULTI")
        log_currency_detection_result(
            "MULTI",
            "mixed_currency_document",
            80,
            "multi_currency_marker",
        )
        return "MULTI"

    COUNTRY_CURRENCY = {
        # Maghreb
        "MOROCCO": "MAD",
        "ALGERIA": "DZD",
        "TUNISIA": "TND",
        "LIBYA": "LYD",

        # Nile / Levant / Mesopotamia
        "EGYPT": "EGP",
        "SUDAN": "SDG",
        "JORDAN": "JOD",
        "LEBANON": "LBP",
        "SYRIA": "SYP",
        "IRAQ": "IQD",
        "PALESTINE": "ILS",

        # GCC / Arabian Peninsula
        "SAUDI_ARABIA": "SAR",
        "QATAR": "QAR",
        "UAE": "AED",
        "KUWAIT": "KWD",
        "BAHRAIN": "BHD",
        "OMAN": "OMR",
        "YEMEN": "YER",

        # Non-Arab markets already supported
        "UNITED_STATES": "USD",
        "UNITED_KINGDOM": "GBP",
        "FRANCE": "EUR",
        "EUROZONE": "EUR",
        "CANADA": "CAD",
        "AUSTRALIA": "AUD",
        "SWITZERLAND": "CHF",
    }

    COUNTRY_HINTS = {
        "MOROCCO": ["MOROCCO", "MAROC", "المغرب", "برغملا"],
        "ALGERIA": ["ALGERIA", "ALGERIE", "ALGÉRIE", "الجزائر", "رئازجلا"],
        "TUNISIA": ["TUNISIA", "TUNISIE", "تونس", "سنوت"],
        "LIBYA": ["LIBYA", "LIBYE", "ليبيا", "ايبيل"],
        "EGYPT": ["EGYPT", "EGYPTE", "ÉGYPTE", "مصر", "رصم"],
        "SUDAN": ["SUDAN", "SOUDAN", "السودان", "نادوسلا"],
        "JORDAN": ["JORDAN", "JORDANIE", "الأردن", "ندرألا"],
        "LEBANON": ["LEBANON", "LIBAN", "لبنان", "نانبل"],
        "SYRIA": ["SYRIA", "SYRIE", "سوريا", "ايروس"],
        "IRAQ": ["IRAQ", "العراق", "قارعلا"],
        "PALESTINE": ["PALESTINE", "فلسطين", "نيطسلف"],
        "SAUDI_ARABIA": ["SAUDI ARABIA", "SAUDI", "KSA", "السعودية", "ةيدوعسلا"],
        "QATAR": ["QATAR", "قطر", "رطق"],
        "UAE": ["UNITED ARAB EMIRATES", "UAE", "EMIRATES", "DUBAI", "ABU DHABI", "EMIRATS", "ÉMIRATS", "الإمارات", "تارامإلا", "دبي", "يبظوبأ"],
        "KUWAIT": ["KUWAIT", "الكويت", "تيوكلا"],
        "BAHRAIN": ["BAHRAIN", "البحرين", "نيرحبلا"],
        "OMAN": ["OMAN", "عمان", "نامع"],
        "YEMEN": ["YEMEN", "اليمن", "نميلا"],
        "UNITED_STATES": ["UNITED STATES","RAMP","RAMP BUSINESS ACCOUNT", "USA", "U.S.A", "AMERICA", "ETATS-UNIS", "ÉTATS-UNIS", "الولايات المتحدة", "أمريكا"],
        "UNITED_KINGDOM": ["UNITED KINGDOM", "UK", "GREAT BRITAIN", "BRITAIN", "ENGLAND", "ROYAUME-UNI", "ANGLETERRE", "المملكة المتحدة", "بريطانيا", "إنجلترا"],
        "FRANCE": ["FRANCE", "فرنسا"],
        "EUROZONE": ["GERMANY", "DEUTSCHLAND", "SPAIN", "ESPAGNE", "ESPAÑA", "ITALY", "ITALIA", "NETHERLANDS", "BELGIUM", "BELGIQUE", "EUROZONE", "EUROPEAN UNION", "UNION EUROPEENNE", "UNION EUROPÉENNE", "ألمانيا", "إسبانيا", "إيطاليا"],
        "CANADA": ["CANADA", "CANADIEN", "كندا"] + CANADA_BANKS,
        "AUSTRALIA": ["AUSTRALIA", "AUSTRALIE", "أستراليا"] + AUSTRALIA_BANKS,
        "SWITZERLAND": ["SWITZERLAND", "SUISSE", "سويسرا"],
    }

    BANK_COUNTRY_HINTS = {
        "MOROCCO": [
            "CIH", "CREDIT IMMOBILIER ET HOTELIER", "CRÉDIT IMMOBILIER ET HÔTELIER",
            "القرض العقاري والسياحي", "يحايسلاو يراقعلا ضرقلا",
            "كنب",
            "يمقر باسح فشك",
            "فشك باسح",
            "ATTIJARI", "ATTIJARIWAFA", "ATTIJARI WAFA", "WAFA", "التجاري وفا بنك", "كنب افو يراجتلا",
            "BMCE", "BANK OF AFRICA", "BANQUE POPULAIRE", "CHAABI", "CREDIT DU MAROC", "CRÉDIT DU MAROC", "CFG BANK", "AL BARID BANK",
        ],
        "ALGERIA": [
            "BNA", "BANQUE NATIONALE D'ALGERIE", "BANQUE NATIONALE D’ALGERIE",
            "CPA", "CREDIT POPULAIRE D'ALGERIE", "CRÉDIT POPULAIRE D'ALGÉRIE",
            "BADR", "BEA", "BANQUE EXTERIEURE D'ALGERIE", "CNEP", "AL BARAKA ALGERIE", "GULF BANK ALGERIA", "AGB",
        ],
        "TUNISIA": [
            "BIAT", "AMEN BANK", "BANQUE DE TUNISIE", "ATTIJARI BANK TUNISIE",
            "ATB", "UIB", "BH BANK", "STB BANK", "BANQUE ZITOUNA", "BTK",
        ],
        "EGYPT": [
            "BANQUE MISR", "NATIONAL BANK OF EGYPT", "NBE", "CIB", "COMMERCIAL INTERNATIONAL BANK",
            "QNB ALAHLI", "ALEXBANK", "BANQUE DU CAIRE", "AAIB", "ARAB AFRICAN INTERNATIONAL BANK",
        ],
        "SAUDI_ARABIA": [
            "AL RAJHI", "ALRAJHI", "AL RAJHI BANK", "ALRAJHI BANK", "مصرف الراجحي", "يحجارلا فرصم",
            "SNB", "SAUDI NATIONAL BANK", "ALAHLI", "RIYAD BANK", "ALINMA", "BANQUE SAUDI FRANSI", "BSF", "SABB", "BANK ALBILAD", "ALJAZIRA",
        ],
        "QATAR": [
            "QNB", "QATAR NATIONAL BANK", "ينطولا رطق كنب", "كنب رطق ينطولا",
            "COMMERCIAL BANK OF QATAR", "CBQ", "DOHA BANK", "QIB", "QATAR ISLAMIC BANK",
        ],
        "UAE": [
            "EMIRATES NBD", "ADCB", "FAB", "FIRST ABU DHABI BANK", "MASHREQ", "DUBAI ISLAMIC BANK", "ADIB", "RAKBANK", "ENBD",
        ],
        "KUWAIT": ["KUWAIT FINANCE HOUSE", "KFH", "NATIONAL BANK OF KUWAIT", "NBK", "GULF BANK KUWAIT", "BOUBYAN"],
        "BAHRAIN": ["NATIONAL BANK OF BAHRAIN", "NBB", "BANK OF BAHRAIN", "BBK", "AHLI UNITED BANK"],
        "OMAN": ["BANK MUSCAT", "NATIONAL BANK OF OMAN", "NBO", "SOHAR INTERNATIONAL", "BANK DHOFAR"],
        "JORDAN": ["ARAB BANK JORDAN", "BANK OF JORDAN", "CAIRO AMMAN BANK", "JORDAN KUWAIT BANK", "البنك العربي الأردني", "يبرعلا يندرألا كنبلا"],
        "IRAQ": ["RAFIDAIN BANK", "RASHEED BANK", "TRADE BANK OF IRAQ", "TBI"],
        "LEBANON": ["BLOM BANK", "BANK AUDI", "BYBLOS BANK", "FRANSABANK", "BANK OF BEIRUT"],
        "PALESTINE": ["BANK OF PALESTINE", "ARAB ISLAMIC BANK", "PALESTINE ISLAMIC BANK"],
        "YEMEN": ["CAC BANK", "YEMEN KUWAIT BANK", "SABA ISLAMIC BANK"],
        "LIBYA": ["JUMHOURIA BANK", "WAHDA BANK", "NORTH AFRICA BANK", "SAHARA BANK"],
        "SUDAN": ["BANK OF KHARTOUM", "FAISAL ISLAMIC BANK SUDAN", "OMDURMAN NATIONAL BANK"],
        "SYRIA": ["COMMERCIAL BANK OF SYRIA", "BANK OF SYRIA AND OVERSEAS", "BBSF"],

        # Non-Arab bank hints preserved
        "CANADA": CANADA_BANKS,
        "AUSTRALIA": AUSTRALIA_BANKS,
        "UNITED_STATES": ["ALLY BANK", "ALLY", "ALLY FINANCIAL", "CHASE", "JPMORGAN", "JPMORGAN CHASE", "BANK OF AMERICA", "WELLS FARGO", "CITI", "CITIBANK", "CAPITAL ONE", "USAA", "PNC BANK", "TD BANK USA", "DISCOVER BANK", "SOFI BANK","BREX","BREX ACCOUNT", "AMERICAN EXPRESS NATIONAL BANK","MERCURY",
    "MERCURY BANKING"],
        "UNITED_KINGDOM": ["BARCLAYS", "LLOYDS", "NATWEST", "HSBC UK", "MONZO", "STARLING", "SANTANDER UK", "TSB BANK"],
        "FRANCE": ["BNP", "BNP PARIBAS", "SOCIETE GENERALE", "SOCIÉTÉ GÉNÉRALE", "CREDIT AGRICOLE", "CRÉDIT AGRICOLE", "LA BANQUE POSTALE", "LCL", "CAISSE D'EPARGNE", "CAISSE D’ÉPARGNE", "BOURSORAMA"],
        "EUROZONE": ["REVOLUT BANK UAB", "N26"],
    }

    def has_hint(hints: list[str]) -> bool:
        for hint in hints:
            h = hint.upper()

            if re.fullmatch(r"[A-Z0-9]{2,4}", h) or re.fullmatch(r"[\u0600-\u06FF]{2,4}", h):
                if re.search(
                    rf"(?<![A-Z0-9\u0600-\u06FF]){re.escape(h)}(?![A-Z0-9\u0600-\u06FF])",
                    normalized,
                ):
                    return True
            elif h in normalized:
                return True

        return False

    # 3) Country/jurisdiction fallback.
    for country, hints in COUNTRY_HINTS.items():
        if has_hint(hints):
            detected = COUNTRY_CURRENCY[country]
            debug_log("CURRENCY_DEBUG: country_hint", country, "->", detected)
            log_currency_detection_result(
                detected,
                "country_hint",
                90,
                country,
            )
            return detected

    # 4) Bank -> country -> currency fallback.
    for country, hints in BANK_COUNTRY_HINTS.items():
        if has_hint(hints):
            detected = COUNTRY_CURRENCY[country]
            debug_log("CURRENCY_DEBUG: bank_country_hint", country, "->", detected)
            log_currency_detection_result(
                detected,
                "bank_country_hint",
                85,
                country,
            )
            return detected

    debug_log("CURRENCY_DEBUG: no_match -> unknown")
    log_currency_detection_result(
        "unknown",
        "no_match",
        0,
    )
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
    raw = raw.strip()

    raw = re.sub(r"^(\d{1,3}),\1,", r"\1,", raw)

    # 5,500,00 -> 500,00 only when it is clearly a duplicated OCR prefix,
    # but keep 3 500,00 / 9 800,00 valid thousands.
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

        values.append(value)

    return values



def arabic_text_variants(text: str) -> list[str]:
    variants = [text.lower()]

    if is_arabic_text(text):
        reversed_words = " ".join(
            word[::-1] if re.search(r"[\u0600-\u06FF]", word) else word
            for word in text.split()
        )
        variants.append(reversed_words.lower())

    return variants


def classify_by_keywords(text: str) -> str | None:
    variants = arabic_text_variants(text)

    # General income-priority rule: inbound phrases must win over broad
    # expense words such as "payment".
    if any(is_income_priority_description(v) for v in variants):
        return "income"

    if any(any(k in v for k in EXPENSE_KEYWORDS) for v in variants):
        return "expense"

    if any(any(k in v for k in INCOME_KEYWORDS) for v in variants):
        return "income"

    # Neutral descriptions should remain unknown.
    # Balance delta logic can then decide income/expense safely.
    return None

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
        return 0.0, 0.0, None

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

            # Standard bank-statement rule:
            # if an explicit transaction amount is present, keep it.
            # The running balance delta may validate the sign, but must not replace
            # the displayed transaction amount because OCR windows can merge rows.
            keyword_type = classify_by_keywords(row.get("text", ""))

            if keyword_type in ("expense", "income"):
                return abs(probable_tx), probable_balance, keyword_type

            return abs(probable_tx), probable_balance, delta_type

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

    # General safety rule:
    # The first Arabic/OCR row cannot be safely classified as income/expense
    # unless a previous running balance exists to validate the balance delta,
    # or the text contains an explicit income/expense signal.
    if prev_balance is None and len(numbers) >= 2:
        if tx_type not in ("income", "expense"):
            return 0.0, probable_balance, "opening_balance"

    return abs(probable_tx), probable_balance, tx_type

def extract_arabic_ocr_transactions(text: str) -> list[dict]:
    if not is_mostly_arabic_text(text):
        return []

    normalized = normalize_arabic_digits(text)
    normalized = clean_db_text(normalized)
    normalized = normalized.replace("\u00a0", " ").replace("\u202f", " ")
    normalized = normalized.replace("،", ",")
    normalized = "\n".join(" ".join(l.split()) for l in normalized.splitlines())

    currency = detect_currency(text)
    debug_log("CURRENCY_DETECTED:", currency)

    debug_log("=== AR DEBUG START ===")
    debug_log("TEXT_LENGTH:", len(normalized))
    dates = find_arabic_ocr_dates(normalized)
    debug_log("DATES_FOUND:", [d["clean"] for d in dates])
    debug_log(
        "AMOUNTS_FOUND:",
        re.findall(
            r"\d{1,3}(?:[ ,]\d{3})*(?:[.,]\d{2})",
            normalized
        )[:30]
    )

    amount_pattern = r"\d{1,3}(?:[ ,]\d{3})*(?:[.,]\d{2})"

    rows = []

    for dm in dates:
        debug_log("---- DATE LOOP ----")
        debug_log("DATE:", dm["clean"])

        date_raw = dm["clean"]

        # Build one transaction segment from this date to the next detected date.
        # This is safer than using physical OCR lines because RTL extraction can place
        # amount/balance pairs before the next date on the same line.
        next_date_start = None

        for d in dates:
            if d["start"] <= dm["start"]:
                continue

            if d.get("partial"):
                continue

            # Do not split the same transaction on value dates like 08/04
            # or duplicated posting dates like 09 04 2026 inside the same OCR row.
            between = normalized[dm["end"]:d["start"]]

            if "\n" not in between and len(between) < 80:
                continue

            next_date_start = d["start"]
            break

        window_start_abs = dm["start"]

        if next_date_start is not None:
            window = normalized[dm["start"]:next_date_start]
        else:
            remaining = normalized[dm["start"]:]
            stop = re.search(
                r"(?:\n\s*[:：]|Document|Generated|Test|بيانات|رابتخا)",
                remaining,
                flags=re.IGNORECASE,
            )
            window = remaining[:stop.start()] if stop else remaining

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

        debug_log("WINDOW:")
        debug_log(window)

        values = extract_money_values_from_window(amount_window)

        debug_log("WINDOW_AMOUNTS:", values)

        if len(values) < 2:
            continue

        # garder l'ordre OCR réel de la ligne:
        # premier montant = transaction probable, dernier montant = solde probable
        clean = values[:4]

        debug_log(
            "ROW_DATE_DEBUG",
            dm["date"],
            window[:250]
        )

        debug_log(
            "ROW_DATE_RAW",
            dm
        )

        rows.append({
            "date": dm["date"],
            "numbers": clean,
            "text": window,
            "probable_balance": clean[-1],
            "probable_tx": clean[0],
        })

    filtered = []

    for index, row in enumerate(rows):
        row["_source_index"] = index
        filtered.append(row)

    rows = filtered

    transactions = []
    previous_balance = None

    for row in rows:
        numbers = row.get("numbers", [])

        if len(numbers) < 2:
            continue

        row_text = str(row.get("text", ""))
        row_is_internal_transfer = is_internal_transfer(row_text, text)

        tx_amount, balance, tx_type = resolve_arabic_row_amount(
            row,
            previous_balance,
        )

        if tx_type == "opening_balance":
            row["resolved_balance"] = balance
            previous_balance = balance
            continue

        row["resolved_balance"] = balance
        previous_balance = balance

        # Internal transfers still update the running balance chain, but are not
        # counted as income/expense because they are movements between own accounts.
        if row_is_internal_transfer:
            continue

        if tx_type == "income":
            signed_amount = abs(tx_amount)
        elif tx_type == "expense":
            signed_amount = -abs(tx_amount)
        else:
            signed_amount = abs(tx_amount)
            tx_type = "unknown"

        transactions.append({
            "date": row["date"],
            "description": clean_db_text(row["text"][:300]),
            "amount": signed_amount,
            "type": tx_type,
            "currency": currency,
        })

    debug_log("ROWS_BUILT:", rows)

    for t in transactions:
        debug_log("AR_TX:", t)

    debug_log("ARABIC_BYPASS_COUNT:", len(transactions))
    log_final_transactions(transactions)
    debug_log("FINAL_TXS", transactions)
    debug_log("=== TX_EXTRACT_DEBUG END ===")
    return transactions



def infer_month_first_date_order(
    text: str,
    detected_currency: str,
) -> bool:
    """Infer whether numeric dates should be parsed as MM/DD/YYYY.

    Conservative rules:
    - USD is month-first by default.
    - CAD is mixed in the real world: many English Canadian statements use
      MM/DD/YYYY, while French/Quebec statements such as Desjardins can use
      DD/MM/YYYY.
    - Non-ambiguous dates inside the document are the strongest signal.
    - French/Quebec markers force day-first.
    - English Canadian bank markers fall back to month-first.
    - Everything else remains day-first to avoid breaking France/UK/EU/Arabic.
    """
    normalized = normalize_arabic_digits(clean_db_text(text)).upper()

    if detected_currency == "USD":
        debug_log("TX_DEBUG: date_order", "USD -> month_first")
        return True

    if detected_currency != "CAD":
        debug_log("TX_DEBUG: date_order", detected_currency, "-> day_first")
        return False

    french_canada_markers = [
        "DESJARDINS",
        "CAISSE DESJARDINS",
        "CAISSE POPULAIRE",
        "QUEBEC",
        "QUÉBEC",
        "MONTRÉAL",
        "MONTREAL",
        "RELEVÉ",
        "SOLDE",
        "OPÉRATION",
        "OPERATION",
        "PAIEMENT",
        "VIREMENT",
    ]

    if any(marker in normalized for marker in french_canada_markers):
        debug_log("TX_DEBUG: date_order", "CAD french_marker -> day_first")
        return False

    # Look for numeric dates and use any non-ambiguous example as proof.
    # MM/DD proof: first <= 12 and second > 12, e.g. 01/18/2026.
    # DD/MM proof: first > 12 and second <= 12, e.g. 15/01/2026.
    for match in re.finditer(
        r"\b(\d{1,2})[./-](\d{1,2})(?:[./-]\d{2,4})?\b",
        normalized,
    ):
        first = int(match.group(1))
        second = int(match.group(2))

        if first <= 12 and second > 12:
            debug_log(
                "TX_DEBUG: date_order",
                "CAD non_ambiguous -> month_first",
                match.group(0),
            )
            return True

        if first > 12 and second <= 12:
            debug_log(
                "TX_DEBUG: date_order",
                "CAD non_ambiguous -> day_first",
                match.group(0),
            )
            return False

    english_canada_bank_markers = [
        "BANK OF MONTREAL",
        "BMO",
        "TD CANADA TRUST",
        "TD BANK",
        "RBC",
        "ROYAL BANK OF CANADA",
        "SCOTIABANK",
        "CIBC",
    ]

    if any(marker in normalized for marker in english_canada_bank_markers):
        debug_log("TX_DEBUG: date_order", "CAD english_bank -> month_first")
        return True

    debug_log("TX_DEBUG: date_order", "CAD ambiguous -> day_first")
    return False


def extract_signed_amount_fallback_transactions(
    text: str,
    detected_currency: str,
) -> list[dict]:
    """Fallback for compact statements without normal transaction rows.

    This is only used when the normal extractor returns no transactions.

    General rule:
        Description A -10.00 Description B +20.00
    becomes:
        Description A / -10.00
        Description B / +20.00

    It uses signed amounts and text positions, not bank names. This prevents
    the previous fallback bug where "+89.90 Aramco Fuel -210.35" became one
    bad description for the -210.35 transaction.
    """
    transactions: list[dict] = []

    normalized_text = normalize_ocr_numeric_text(
        normalize_arabic_digits(
            clean_db_text(str(text))
        )
    )

    signed_amount_re = re.compile(
        r"(?<![\d.,])([+-])\s*("
        r"(?:\d{1,3}(?:[ ,]\d{3})+|\d+)"
        r"(?:[.,]\d{2})"
        r")(?![\d.,])"
    )

    metadata_keywords = [
        "account number",
        "account holder",
        "account name",
        "customer name",
        "client name",
        "statement date",
        "statement period",
        "date range",
        "bank statement",
        "iban",
        "swift",
        "sort code",
        "balance",
        "solde",
    ]

    fallback_transfer_exclusions = [
        "to savings",
        "transfer to savings",
        "savings transfer",
        "own account",
        "between accounts",
        "internal transfer",
        "transfer between accounts",
        "virement interne",
        "compte épargne",
        "compte epargne",
        "livret",
        "تحويل داخلي",
        "حوالة داخلية",
    ]

    sequence = 0

    for raw_line in normalized_text.splitlines():
        line = " ".join(raw_line.split())

        if not line:
            continue

        lower = line.lower()

        if any(keyword in lower for keyword in metadata_keywords):
            continue

        matches = list(signed_amount_re.finditer(line))

        if not matches:
            continue

        for index, match in enumerate(matches):
            previous_end = (
                matches[index - 1].end()
                if index > 0
                else 0
            )

            description_segment = line[
                previous_end:match.start()
            ].strip(" -–—:;,.|")

            if not description_segment:
                continue

            date = extract_date(description_segment)

            description = re.sub(
                r"\b\d{4}-\d{2}-\d{2}\b",
                "",
                description_segment,
                count=1,
            )

            description = re.sub(
                r"\b\d{2}[./-]\d{2}(?:[./-]\d{2,4})?\b",
                "",
                description,
                count=1,
            )

            description = clean_db_text(
                description.strip(" -–—:;,.|")
            )

            if not description:
                continue

            description_lower = description.lower()

            if any(keyword in description_lower for keyword in INTERNAL_TRANSFER_KEYWORDS):
                debug_log(
                    "TX_FALLBACK_SKIP: internal_transfer",
                    description,
                )
                continue

            if any(keyword in description_lower for keyword in fallback_transfer_exclusions):
                debug_log(
                    "TX_FALLBACK_SKIP: transfer_exclusion",
                    description,
                )
                continue

            sign = match.group(1)
            amount = parse_amount(match.group(2))

            if sign == "-":
                amount = -abs(amount)
                transaction_type = "expense"
            else:
                amount = abs(amount)
                transaction_type = "income"

            inferred_type = detect_type(description, amount)

            if inferred_type in ["income", "expense"]:
                transaction_type = inferred_type

                if transaction_type == "expense":
                    amount = -abs(amount)
                else:
                    amount = abs(amount)

            sequence += 1

            row = {
                "date": date or "unknown",
                "description": description,
                "amount": amount,
                "type": transaction_type,
                "currency": detected_currency,
            }

            debug_log(
                "TX_FALLBACK_ROW:",
                {
                    "sequence": sequence,
                    **row,
                },
            )

            transactions.append(row)

    return transactions

def merge_multiline_debit_credit_rows(
    lines: list[str],
    default_year: int | None = None,
    prefer_us_date: bool = False,
) -> list[str]:
    """Rebuild one logical transaction per row from noisy OCR/PDF text.

    International multi-pass rule, not bank-specific:
    - A new transaction can start with a Gregorian date at the beginning
      of the line OR inside the line. This covers EN/FR rows and Arabic/RTL
      rows where OCR outputs description before the Gregorian date.
    - Continuation lines are appended until the next transaction start.
    - A terminal amount+running-balance line closes the current row.
    - Header/footer/verification lines are ignored unless they are already
      inside a transaction buffer.

    This protects previously validated formats while fixing vertical tables
    such as:
        FROM MADA / APPLE PAY ...
        ...
        5.500 588.33
    """
    cleaned_lines = [
        " ".join(str(line or "").split())
        for line in lines
        if " ".join(str(line or "").split())
    ]

    amount_token = r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:[.,]\d{2,3})"

    start_at_beginning_re = re.compile(
        r"^\s*(?:"
        r"\d{4}[-/.]\d{1,2}[-/.]\d{1,2}"
        r"|"
        r"\d{1,2}[- ](?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)[- ]\d{2,4}"
        r"|"
        r"\d{1,2}[./-]\d{1,2}[./-]\d{2,4}"
        r")\b",
        flags=re.IGNORECASE,
    )

    gregorian_anywhere_re = re.compile(
        r"(?<!\d)20\d{2}[-/.]\d{1,2}[-/.]\d{1,2}(?!\d)"
    )

    amount_balance_re = re.compile(
        rf"^\s*({amount_token})\s+({amount_token})\s*$",
        flags=re.IGNORECASE,
    )

    date_amounts_only_re = re.compile(
        rf"^\s*(?:"
        rf"\d{{4}}[-/.]\d{{1,2}}[-/.]\d{{1,2}}"
        rf"|\d{{1,2}}[- ](?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)[- ]\d{{2,4}}"
        rf"|\d{{1,2}}[./-]\d{{1,2}}[./-]\d{{2,4}}"
        rf")\s+(?:{amount_token}\s*){{1,3}}\s*$",
        flags=re.IGNORECASE,
    )

    metadata_markers = [
        "to verify", "please scan", "qr code", "seal", "reference number",
        "account statement", "customer name", "accountnumber", "account number",
        "iban number", "branch", "currency", "openingbalance", "closingbalance",
        "withdrawals", "deposits", "transactiondetail", "transaction detail",
        "hijri", "gregorian", "debit", "credit", "balance",
        "للتحقق", "الختم", "الرقم المرجعي", "كشف حساب", "اسم العميل",
        "رقم الحساب", "الايبان", "الفرع", "العملة", "الرصيد الافتتاحي",
        "رصيد الإقفال", "تفاصيل الحركة", "مدين", "دائن", "الرصيد",
    ]

    def is_metadata_line(line: str) -> bool:
        lower = line.lower()
        if any(marker in lower for marker in metadata_markers):
            # A real transaction row can still contain debit/credit words in the
            # description. Only skip pure header/footer lines with no amount row.
            if not gregorian_anywhere_re.search(line) and not amount_balance_re.match(line):
                return True
        return False

    def is_logical_transaction_start(line: str) -> bool:
        if is_metadata_line(line):
            return False

        if date_amounts_only_re.match(line):
            return False

        if gregorian_anywhere_re.search(line):
            return True

        # Keep legacy EN/FR rows that start with text dates or numeric dates.
        if start_at_beginning_re.search(line):
            parsed = extract_date(
                line,
                default_year=default_year,
                prefer_us_date=prefer_us_date,
            )
            return parsed is not None

        return False

    rebuilt: list[str] = []
    buffer = ""

    def flush_buffer() -> None:
        nonlocal buffer
        if buffer:
            rebuilt.append(buffer.strip())
            buffer = ""

    for clean in cleaned_lines:
        if not clean:
            continue

        is_amount_balance = bool(amount_balance_re.match(clean))
        is_date_amounts_only = bool(date_amounts_only_re.match(clean))
        starts_transaction = is_logical_transaction_start(clean)

        if starts_transaction:
            flush_buffer()
            buffer = clean
            continue

        if buffer and (is_amount_balance or is_date_amounts_only):
            buffer = f"{buffer} {clean}".strip()
            flush_buffer()
            continue

        if buffer:
            # Continuation text belongs to the current transaction until the
            # next logical transaction start or terminal amount/balance line.
            buffer = f"{buffer} {clean}".strip()
            continue

        if is_metadata_line(clean):
            continue

        # Preserve unbuffered lines for legacy fallbacks; they will be filtered
        # later if they do not contain a valid transaction signal.
        rebuilt.append(clean)

    flush_buffer()

    debug_log(
        "TX_DEBUG: reconstructed_rows",
        {"input": len(cleaned_lines), "output": len(rebuilt)},
    )

    return rebuilt

def has_debit_credit_balance_table(text: str) -> bool:
    """Detect bank statements with explicit debit/credit/balance columns.

    Structural and language-neutral:
    - EN: Debit / Credit / Balance
    - FR: Débit / Crédit / Solde
    - AR: مدين / دائن / الرصيد / رصيد

    When this is true, the general table parser is safer than the legacy
    Arabic OCR shortcut because transaction amount and running balance are
    printed in separate columns.
    """
    normalized = normalize_arabic_digits(clean_db_text(text)).lower()

    debit_markers = ["debit", "débit", "مدين", "سحوبات"]
    credit_markers = ["credit", "crédit", "دائن", "إيداعات", "ايداعات"]
    balance_markers = [
        "balance", "solde", "الرصيد", "رصيد",
        "closingbalance", "openingbalance",
    ]
    transaction_markers = [
        "transactiondetail", "transaction detail",
        "تفاصيل الحركة",
        "details operation", "détail opération", "detail operation",
    ]

    has_debit = any(marker in normalized for marker in debit_markers)
    has_credit = any(marker in normalized for marker in credit_markers)
    has_balance = any(marker in normalized for marker in balance_markers)
    has_transaction_detail = any(marker in normalized for marker in transaction_markers)

    return has_balance and ((has_debit and has_credit) or has_transaction_detail)


def extract_official_movement_totals(text: str) -> dict | None:
    """Extract official debit/credit movement totals when printed by the bank.

    This is a standard reconciliation control, not a bank-specific patch.
    It supports common EN/FR labels:
    - Total des mouvements 9.832,14 10.011,70
    - Totaux des mouvements 15.267,53 20.615,05
    - Total withdrawals / deposits
    - Total debits / credits

    Returns the first main-account total found. Annex/savings account totals
    later in the document are intentionally ignored by taking the first match.
    """
    normalized = normalize_arabic_digits(clean_db_text(text))
    normalized = normalized.replace("\u00a0", " ").replace("\u202f", " ")

    amount = r"(?:\d{1,3}(?:[,.]\d{3})+|\d+)(?:[.,]\d{2})"

    patterns = [
        rf"(?:totaux?|total)\s+des\s+mouvements\s+({amount})\s+({amount})",
        rf"(?:total)\s+(?:debit|débit|debits|débits)\s+({amount}).{{0,80}}?(?:credit|crédit|credits|crédits)\s+({amount})",
        rf"(?:withdrawals?|debits?)\s+({amount}).{{0,80}}?(?:deposits?|credits?)\s+({amount})",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            normalized,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if not match:
            continue

        try:
            debit_total = parse_amount(match.group(1))
            credit_total = parse_amount(match.group(2))
        except Exception:
            continue

        if debit_total > 0 or credit_total > 0:
            return {
                "debit_total": round(abs(debit_total), 2),
                "credit_total": round(abs(credit_total), 2),
                "source": "official_statement_totals",
            }

    return None


def reconcile_with_official_movement_totals(
    transactions: list[dict],
    text: str,
    detected_currency: str,
) -> list[dict]:
    """Reconcile extracted totals with official bank totals when available.

    If a PDF contains official movement totals and the parser extracted only a
    small part of the table, add explicit reconciliation rows instead of
    presenting false tiny income/expense numbers. This protects international
    debit/credit-column statements such as SG/BRED/BNP/Credit Agricole, while
    leaving already-good parsers unchanged when totals are close.
    """
    official = extract_official_movement_totals(text)

    if not official:
        return transactions

    extracted_debits = movement_total_amount(transactions, "debit")
    extracted_credits = movement_total_amount(transactions, "credit")

    official_debits = float(official["debit_total"])
    official_credits = float(official["credit_total"])

    debit_gap = round(official_debits - extracted_debits, 2)
    credit_gap = round(official_credits - extracted_credits, 2)

    # Do not adjust for tiny rounding/FX/OCR differences.
    debit_threshold = max(2.0, official_debits * 0.03)
    credit_threshold = max(2.0, official_credits * 0.03)

    if debit_gap <= debit_threshold and credit_gap <= credit_threshold:
        debug_log(
            "TX_RECONCILE: official_totals_close",
            {
                "official_debits": official_debits,
                "extracted_debits": extracted_debits,
                "official_credits": official_credits,
                "extracted_credits": extracted_credits,
            },
        )
        return transactions

    date = None
    for tx in reversed(transactions):
        if tx.get("date") and tx.get("date") != "unknown":
            date = tx.get("date")
            break

    date = date or f"{detect_document_year(text)}-01-01"

    reconciled = list(transactions)

    if debit_gap > debit_threshold:
        reconciled.append({
            "date": date,
            "description": "Official statement debit total reconciliation",
            "amount": -abs(debit_gap),
            "type": "expense",
            "currency": detected_currency,
            "category_hint": "reconciliation",
        })

    if credit_gap > credit_threshold:
        reconciled.append({
            "date": date,
            "description": "Official statement credit total reconciliation",
            "amount": abs(credit_gap),
            "type": "income",
            "currency": detected_currency,
            "category_hint": "reconciliation",
        })

    debug_log(
        "TX_RECONCILE: official_totals_applied",
        {
            "official_debits": official_debits,
            "extracted_debits": extracted_debits,
            "debit_gap": debit_gap,
            "official_credits": official_credits,
            "extracted_credits": extracted_credits,
            "credit_gap": credit_gap,
        },
    )

    return reconciled

def extract_transactions(text: str) -> list[dict]:
    debug_log("=== TX_EXTRACT_DEBUG START ===")
    debug_log("TEXT_SAMPLE:", clean_db_text(str(text))[:500])

    detected_currency = detect_currency(text)
    prefer_us_date = infer_month_first_date_order(text, detected_currency)
    debug_log("TX_DEBUG: detected_currency", detected_currency)
    debug_log("TX_DEBUG: prefer_us_date", prefer_us_date)

    table_statement_detected = has_debit_credit_balance_table(text)

    if not table_statement_detected:
        arabic_transactions = extract_arabic_ocr_transactions(text)
        if arabic_transactions:
            debug_log("TX_DEBUG: arabic_path_used", len(arabic_transactions))
            return arabic_transactions
    else:
        debug_log("TX_DEBUG: table_statement_detected_skip_arabic_shortcut")

    debug_log("TX_DEBUG: general_table_path_used")

    text = normalize_arabic_ocr_lines(text)
    text = normalize_ocr_numeric_text(text)

    transactions = []
    default_year = detect_document_year(text)
    debug_log("TX_DEBUG: default_year", default_year)

    raw_lines = [
        " ".join(line.split())
        for line in text.splitlines()
        if " ".join(line.split())
    ]

    raw_lines = merge_multiline_debit_credit_rows(
        raw_lines,
        default_year=default_year,
        prefer_us_date=prefer_us_date,
    )

    if not is_mostly_arabic_text(text):
        raw_lines = split_compact_multi_transaction_lines(
            raw_lines,
            default_year=default_year,
            prefer_us_date=prefer_us_date,
        )

    debug_log("TX_DEBUG: raw_lines_count", len(raw_lines))
    for idx, raw_line in enumerate(raw_lines[:30]):
        debug_log(f"TX_DEBUG: raw_line[{idx}]", raw_line)

    lines = []
    i = 0

    while i < len(raw_lines):
        current = raw_lines[i]
        current_lower = current.lower()
        current_is_metadata_or_header = any(
            keyword in current_lower
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
                "date description",
                "debit credit",
            ]
        )

        if current_is_metadata_or_header:
            lines.append(current)
            i += 1
            continue

        current_is_date_only = is_date_only_line(
            current,
            default_year=default_year,
            prefer_us_date=prefer_us_date,
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
            extract_date(current, default_year=default_year, prefer_us_date=prefer_us_date)
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

    lines = attach_following_balance_lines(
        lines,
        default_year=default_year,
        prefer_us_date=prefer_us_date,
    )

    debug_log("TX_DEBUG: candidate_lines_count", len(lines))
    for idx, candidate_line in enumerate(lines[:50]):
        debug_log(f"TX_DEBUG: candidate_line[{idx}]", candidate_line, "date=", extract_date(candidate_line, default_year=default_year, prefer_us_date=prefer_us_date), "money=", re.findall(MONEY_NUMBER_PATTERN, candidate_line))

    for clean_line in lines:

        if is_amount_balance_only_row(
            clean_line,
            default_year=default_year,
            prefer_us_date=prefer_us_date,
        ):
            continue

        BALANCE_ROWS = [
            "brought forward",
            "carried forward",
            "opening balance",
            "closing balance",
            "balance forward",
            "opening balance brought forward",
            "solde initial",
            "solde report",
            "solde reporte",
            "solde de clôture",
            "solde de cloture",
            "رصيد افتتاحي",
            "رصيد مرحل",
            "الرصيد الافتتاحي",
        ]

        if any(
            keyword in clean_line.lower()
            for keyword in BALANCE_ROWS
        ):
            continue

        normalized_line = clean_line.lower()

        # Do not skip internal transfers here. Keep the movement for gross
        # statement reconciliation, then mark it as type="transfer" before
        # returning so KPIs exclude it without breaking debit/credit totals.

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
            debug_log("TX_SKIP: metadata", clean_line)
            continue

        if re.fullmatch(
            r"\d{2}[./-]\d{2}[./-]\d{4}\s*[-–]\s*\d{2}[./-]\d{2}[./-]\d{4}",
            clean_line,
        ):
            continue

        if not has_transaction_signal(
            clean_line,
            default_year=default_year,
            prefer_us_date=prefer_us_date,
        ):
            debug_log("TX_SKIP: no_signal", clean_line, "date=", extract_date(clean_line, default_year=default_year, prefer_us_date=prefer_us_date), "money=", re.findall(MONEY_NUMBER_PATTERN, clean_line))
            continue

        debug_log("TX_ACCEPT_SIGNAL:", clean_line)
        tabular_amount, tabular_type = extract_tabular_bank_amount(clean_line)

        amount_balance_tx_amount = None
        amount_balance_value = None

        if tabular_amount is None:
            tabular_amount, tabular_type = extract_amount_balance_line(clean_line)

            amount_balance_numbers = extract_money_numbers_safely(clean_line)
            if len(amount_balance_numbers) >= 2:
                try:
                    amount_balance_tx_amount = parse_amount(amount_balance_numbers[-2])
                    amount_balance_value = parse_amount(amount_balance_numbers[-1])
                except Exception:
                    amount_balance_tx_amount = None
                    amount_balance_value = None

        numbers = extract_money_numbers_safely(clean_line)

        if (
            len(numbers) == 2
            and not is_arabic_text(clean_line)
        ):
            locked_tx_amount = parse_amount(numbers[0])
            locked_balance = parse_amount(numbers[1])

            if tabular_amount is not None:
                tabular_amount = abs(locked_tx_amount)

                if tabular_type == "expense":
                    tabular_amount = -abs(locked_tx_amount)
                elif tabular_type == "income":
                    tabular_amount = abs(locked_tx_amount)

            amount_balance_tx_amount = locked_tx_amount
            amount_balance_value = locked_balance
            balance = locked_balance

        debug_log("TX_DEBUG: tabular", tabular_amount, tabular_type)


        if tabular_amount is not None:
            amount = tabular_amount
        else:
            amount = extract_transaction_amount(clean_line)

        if amount is None:
            fallback_amount = extract_first_amount_after_date(clean_line)
            debug_log("TX_DEBUG: fallback_amount", fallback_amount)

            if fallback_amount is None:
                debug_log("TX_SKIP: no_amount", clean_line)
                continue

            amount = fallback_amount

        transaction_type = tabular_type or detect_type(clean_line, amount)


        if transaction_type == "expense" and amount > 0:
            amount = -abs(amount)

        if transaction_type == "income":
            amount = abs(amount)

        # General non-Arabic safety lock for rows shaped like:
        #     date description transaction_amount running_balance
        # When two money values are present, the first value is the movement
        # and the last value is the running balance. This prevents later
        # fallback logic from accidentally using the balance as the transaction
        # amount. Arabic OCR keeps its separate extraction path unchanged.
        if (
            amount_balance_tx_amount is not None
            and amount_balance_value is not None
            and not is_arabic_text(clean_line)
        ):
            original_amount_for_lock = amount
            amount_abs = abs(float(amount or 0))
            tx_abs = abs(float(amount_balance_tx_amount or 0))
            balance_abs = abs(float(amount_balance_value or 0))

            likely_used_balance = abs(amount_abs - balance_abs) <= max(0.02, balance_abs * 0.0001)
            far_from_tx_amount = abs(amount_abs - tx_abs) > max(0.02, tx_abs * 0.01)

            if likely_used_balance or far_from_tx_amount:
                if transaction_type == "expense":
                    amount = -abs(amount_balance_tx_amount)
                else:
                    amount = abs(amount_balance_tx_amount)

                debug_log(
                    "TX_DEBUG: amount_balance_lock",
                    {
                        "original_amount": original_amount_for_lock,
                        "locked_amount": amount,
                        "balance": amount_balance_value,
                        "type": transaction_type,
                    },
                )

        if amount_balance_tx_amount is not None and amount_balance_value is not None:
            debug_log(
                "TX_DEBUG: amount_balance_parse",
                {
                    "amount": amount_balance_tx_amount,
                    "balance": amount_balance_value,
                    "chosen_amount": amount,
                }
            )

        date = extract_date(
            clean_line,
            default_year=default_year,
            prefer_us_date=prefer_us_date,
        )

        debug_log(
            "AR_TX_FINAL:",
            clean_line,
            "=>",
            amount,
            transaction_type,
        )

        line_balance = extract_line_balance(clean_line)

        debug_log(
            "TX_FINAL_ROW:",
            {
                "date": date,
                "amount": amount,
                "type": transaction_type,
                "currency": detected_currency,
                "balance": line_balance,
            },
        )

        transactions.append(
            {
                "date": date,
                "description": clean_db_text(clean_line),
                "amount": amount,
                "type": transaction_type,
                "currency": detected_currency,
                "_balance": line_balance,
            }
        )

    transactions = infer_balance_delta_rows(transactions)

    for tx in transactions:
        tx.pop("_balance", None)

    if not transactions:
        debug_log(
            "TX_DEBUG: normal_extraction_empty_using_signed_amount_fallback"
        )
        transactions = extract_signed_amount_fallback_transactions(
            text,
            detected_currency,
        )

    transactions = reconcile_with_official_movement_totals(
        transactions,
        text,
        detected_currency,
    )

    transactions = mark_internal_transfers(transactions, text)

    log_final_transactions(transactions)
    debug_log("FINAL_TXS", transactions)
    return transactions
EXPENSE_KEYWORDS += [
    "amazon",
    "starbucks",
    "target",
    "uber",
    "aws billing",
    "openai api",
    "netflix",
    "slack",
    # Common AU/degraded-OCR merchant and bill-payment tokens
    "woolworths",
    "coles",
    "aldi",
    "bpay",
    "telstra",
    "optus",
    "utilities",
    "grocery",
    "groceries",
]

INCOME_KEYWORDS += [
    "payroll",
    "salary",
    "ach credit",
    "deposit",
]

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
