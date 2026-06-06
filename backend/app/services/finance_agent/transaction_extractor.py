import os
import re
import unicodedata
from collections import Counter
from datetime import datetime


DEBUG_FINANCE_EXTRACTOR = os.getenv("FINANCE_EXTRACTOR_DEBUG", "0") == "1"


def debug_log(*args):
    if DEBUG_FINANCE_EXTRACTOR:
        print(*args)
print("RUNEXA_FINANCE_EXTRACTOR_VERSION_ACTIVE", "v9-terminal-balance-authority")

debug_log("RUNEXA_FINANCE_EXTRACTOR_VERSION", "international-multipass-v8-terminal-balance-authority-fr-en-ar")
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
    "سحب نقدي",
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


# Universal FR / EN / AR markers.
# Standard international layer: language-neutral direction detection,
# not bank-specific and not country-specific.
UNIVERSAL_EXPENSE_MARKERS = [
    # FR / EU OCR abbreviations
    "prlv",
    "prlv sepa",
    "prel",
    "prel sepa",
    "prelevement",
    "prélèvement",
    "prelevement sepa",
    "prélèvement sepa",
    "paiement",
    "paiement carte",
    "cb",
    "carte bancaire",
    "retrait",
    "ret dab",
    "dab",
    "distributeur automatique",
    "retrait dab",
    "cash withdrawal",
    "atm withdrawal",
    "achat",
    "carte",
    "frais",
    "commission",
    "virement emis",
    "virement émis",
    "vir emis",
    "vir émis",

    # EN / international
    "direct debit",
    "sepa direct debit",
    "standing order",
    "card payment",
    "purchase",
    "withdrawal",
    "atm",
    "fee",
    "debit",
    "outgoing transfer",
    "transfer sent",

    # AR
    "مدين",
    "خصم",
    "سحب",
    "سحب نقدي",
    "شراء",
    "اقتطاع",
    "دفع",
    "بطاقة",
    "رسوم",
    "عمولة",
    "فاتورة",
    "تحويل صادر",
    "حوالة صادرة",
]

UNIVERSAL_INCOME_MARKERS = [
    # FR
    "virement reçu",
    "virement recu",
    "vir reçu",
    "vir recu",
    "versement",
    "dépôt",
    "depot",
    "salaire",

    # EN / international
    "incoming transfer",
    "transfer received",
    "payment received",
    "payment in",
    "salary",
    "payroll",
    "deposit",
    "credit",

    # AR
    "دائن",
    "إيداع",
    "ايداع",
    "راتب",
    "دخل",
    "تحويل وارد",
    "حوالة واردة",
]

EXPENSE_KEYWORDS += [
    marker for marker in UNIVERSAL_EXPENSE_MARKERS
    if marker not in EXPENSE_KEYWORDS
]

INCOME_KEYWORDS += [
    marker for marker in UNIVERSAL_INCOME_MARKERS
    if marker not in INCOME_KEYWORDS
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
    "wero",
    "vir inst re",
    "virement sepa recu",
    "virement sepa reçu",
    "virement instantane recu",
    "virement instantané reçu",
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
    "prelevement sepa",
    "prélèvement sepa",
    "prlv",
    "prlv sepa",
    "prel",
    "prel sepa",
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
    "يناير": "01",
    "كانون الثاني": "01",
    "فبراير": "02",
    "شباط": "02",
    "مارس": "03",
    "آذار": "03",
    "اذار": "03",
    "أبريل": "04",
    "ابريل": "04",
    "نيسان": "04",
    "مايو": "05",
    "أيار": "05",
    "ايار": "05",
    "يونيو": "06",
    "حزيران": "06",
    "يوليو": "07",
    "تموز": "07",
    "أغسطس": "08",
    "اغسطس": "08",
    "آب": "08",
    "اب": "08",
    "سبتمبر": "09",
    "أيلول": "09",
    "ايلول": "09",
    "أكتوبر": "10",
    "اكتوبر": "10",
    "تشرين الأول": "10",
    "تشرين الاول": "10",
    "نوفمبر": "11",
    "تشرين الثاني": "11",
    "ديسمبر": "12",
    "كانون الأول": "12",
    "كانون الاول": "12",
    "jan": "01",
    "janv": "01",
    "janvier": "01",
    "january": "01",
    "feb": "02",
    "fevrier": "02",
    "février": "02",
    "fevr": "02",
    "févr": "02",
    "february": "02",
    "mar": "03",
    "mars": "03",
    "march": "03",
    "apr": "04",
    "avril": "04",
    "avr": "04",
    "april": "04",
    "may": "05",
    "mai": "05",
    "jun": "06",
    "juin": "06",
    "june": "06",
    "jul": "07",
    "juillet": "07",
    "juil": "07",
    "july": "07",
    "aug": "08",
    "aout": "08",
    "août": "08",
    "august": "08",
    "sep": "09",
    "septembre": "09",
    "sept": "09",
    "september": "09",
    "oct": "10",
    "octobre": "10",
    "october": "10",
    "nov": "11",
    "novembre": "11",
    "november": "11",
    "dec": "12",
    "decembre": "12",
    "décembre": "12",
    "déc": "12",
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
        money_only = re.fullmatch(
            r"\$?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})|\$?\s*\d+\.\d{2}",
            ln.strip(),
        )
        if money_only:
            val = float(ln.replace("$", "").replace(",", "").strip())
            amounts.append(val)
            continue

        low = ln.lower()
        if any(k in low for k in ["purchase", "deposit", "interest", "ach", "virement", "dépot", "dépôt", "crédit", "debit", "مدين", "دائن"]):
            descriptions.append(ln)

    print("DEBIT_CREDIT_BALANCE_COMPONENT_DEBUG", {
        "dates": len(dates),
        "descriptions": len(descriptions),
        "amounts": len(amounts),
        "date_sample": dates[:10],
        "description_sample": descriptions[:10],
        "amount_sample": amounts[:20],
    })

    if not dates or not descriptions or not amounts:
        return []

    # For Bancorp-like OCR: summary amounts appear first, then descriptions, then dates.
    # Use transaction table visible order: date count drives rows.
    tx_count = min(len(dates), len(descriptions))
    if tx_count < 3:
        return []

    # Extract summary totals for validation, if present.
    summary_nums = [float(x.replace(",", "")) for x in re.findall(r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})|\d+\.\d{2})", raw)]
    official_credits = None
    official_debits = None
    if len(summary_nums) >= 4:
        # Bancorp parsed order often includes: beginning, ending, credits, debits somewhere in first block.
        # Use known labels if possible.
        m_credits = re.search(r"Total Credits:\s*\$?(\d+(?:\.\d{2})?)", raw, re.I)
        m_debits = re.search(r"Total Debits\s*\$?(\d+(?:\.\d{2})?)", raw, re.I)
        if m_credits:
            official_credits = float(m_credits.group(1))
        if m_debits:
            official_debits = float(m_debits.group(1))

    # Amount stream fallback: choose amounts after summary by matching row count*3 if possible.
    # Safer for Bancorp image OCR: derive by description keywords and known row amount order from visual table.
    # Skip first four summary values if enough values remain.
    detail_amounts = amounts[4:] if len(amounts) >= tx_count + 4 else amounts

    txs = []
    amt_i = 0

    for idx in range(tx_count):
        mon, day = dates[idx]
        desc = descriptions[idx]
        low = desc.lower()

        if amt_i >= len(detail_amounts):
            break

        # In debit/credit/balance table, each row may expose tx amount plus balance.
        # Parsed OCR frequently lists only one relevant amount per row in amount stream order.
        amount = detail_amounts[amt_i]
        amt_i += 1

        typ = "income" if any(k in low for k in ["deposit", "interest", "credit", "ach", "crédit", "dépôt", "depot", "دائن", "إيداع"]) else "expense"
        signed = amount if typ == "income" else -amount

        txs.append({
            "date": f"{year:04d}-{mon:02d}-{day:02d}",
            "description": desc,
            "amount": round(signed, 2),
            "signed_amount": round(signed, 2),
            "type": typ,
            "currency": "USD" if "usd" in normalized else None,
            "locked_amount": round(signed, 2),
            "_locked_amount": round(signed, 2),
            "locked_type": typ,
            "parser_family": "debit_credit_balance_ledger",
        })

    print("DEBIT_CREDIT_BALANCE_LEDGER_EXTRACTED", {
        "transactions": len(txs),
        "income": sum(1 for tx in txs if tx.get("type") == "income"),
        "expenses": sum(1 for tx in txs if tx.get("type") == "expense"),
        "income_total": round(sum(tx["amount"] for tx in txs if tx.get("type") == "income"), 2),
        "expense_total": round(sum(abs(tx["amount"]) for tx in txs if tx.get("type") == "expense"), 2),
    })

    return txs


def extract_transactions(text: str) -> list[dict]:
    txs = parse_debit_credit_balance_ledger(text)
    if txs and len(txs) >= 3:
        print("STATEMENT_LAYOUT_DETECTED", "debit_credit_balance_ledger")
        print("DEBIT_CREDIT_BALANCE_LEDGER_ROUTE", {
            "transactions": len(txs),
            "income": sum(1 for tx in txs if tx.get("type") == "income"),
            "expenses": sum(1 for tx in txs if tx.get("type") == "expense"),
        })
        return txs

    if (
        "date amount description" in str(text or "").lower()
        or re.search(r"(?m)^\s*\d{4}\s+\d+\.\d{2}\s+\S+", str(text or ""))
    ):
        print("STATEMENT_LAYOUT_DETECTED", "date_amount_description_ledger")
        txs = parse_date_amount_description_ledger(text)
        if txs:
            print("DATE_AMOUNT_DESCRIPTION_LEDGER_ROUTE", {
                "transactions": len(txs),
                "income": 0,
                "expenses": len(txs),
            })
            return txs


    if is_sectioned_activity_statement(text):
        if has_composite_statement_periods(text):
            print("COMPOSITE_STATEMENT_PERIOD_GUARD", {
                "layout": "sectioned_activity_statement",
                "action": "skip_composite_mixed_period_pdf",
            })
        
    txs = parse_global_date_boundary_ledger(text)
    if txs and len(txs) >= 5:
        print("STATEMENT_LAYOUT_DETECTED", "global_date_boundary_ledger")
        print("GLOBAL_DATE_BOUNDARY_LEDGER_ROUTE", {
            "transactions": len(txs),
            "income": sum(1 for tx in txs if tx.get("type") == "income"),
            "expenses": sum(1 for tx in txs if tx.get("type") == "expense"),
        })
        return txs

    return []
    if is_typed_transaction_table_statement(text):
        print("STATEMENT_LAYOUT_DETECTED", "typed_transaction_table_statement")
        txs = parse_typed_transaction_table_statement(text)
        if txs:
            print("TYPED_TRANSACTION_TABLE_ROUTE", {
                "transactions": len(txs),
                "income": sum(1 for tx in txs if tx.get("type") == "income"),
                "expenses": sum(1 for tx in txs if tx.get("type") == "expense"),
                "transfers": sum(1 for tx in txs if tx.get("type") == "transfer"),
            })
            return txs

    if is_sectioned_balance_history_statement(text):
        print("STATEMENT_LAYOUT_DETECTED", "sectioned_balance_history_statement")
        txs = parse_sectioned_balance_history_statement(text)
        if txs:
            print("SECTIONED_BALANCE_HISTORY_STATEMENT_ROUTE", {
                "transactions": len(txs),
                "income": sum(1 for tx in txs if tx.get("type") == "income"),
                "expenses": sum(1 for tx in txs if tx.get("type") == "expense"),
            })
            return txs

    if is_sectioned_ledger_statement(text):
        print("STATEMENT_LAYOUT_DETECTED", "sectioned_ledger_statement")
        txs = parse_sectioned_ledger_statement(text)
        if txs:
            print("SECTIONED_LEDGER_STATEMENT_ROUTE", {
                "transactions": len(txs),
                "income": sum(1 for tx in txs if tx.get("type") == "income"),
                "expenses": sum(1 for tx in txs if tx.get("type") == "expense"),
            })
            return txs

    if is_sectioned_deposit_withdrawal_statement(text):
        print("STATEMENT_LAYOUT_DETECTED", "sectioned_deposit_withdrawal_statement")
        txs = parse_sectioned_deposit_withdrawal_statement(text)
        if txs:
            print("SECTIONED_DW_STATEMENT_ROUTE", {
                "transactions": len(txs),
                "income": sum(1 for tx in txs if tx.get("type") == "income"),
                "expenses": sum(1 for tx in txs if tx.get("type") == "expense"),
            })
            return txs

    if is_visual_debit_credit_balance_table(text):
        print("STATEMENT_LAYOUT_DETECTED", "visual_debit_credit_balance_table")
        txs = parse_visual_debit_credit_balance_table(text)
        if txs:
            print("VISUAL_DCB_TABLE_ROUTE", {
                "transactions": len(txs),
                "income": sum(1 for tx in txs if tx.get("type") == "income"),
                "expenses": sum(1 for tx in txs if tx.get("type") == "expense"),
            })
            return txs

    # Do not strip text globally; it can remove valid transaction sections.
    # Balance-summary rows are filtered later at transaction level.
    text = strip_n26_spaces_sections(text)
    statement_layout = detect_statement_layout(text)
    print("STATEMENT_LAYOUT_DETECTED", statement_layout)

    if statement_layout == "running_balance_column_statement":
        running_balance_transactions = extract_running_balance_column_statement_transactions(text)

        print(
            "RUNNING_BALANCE_COLUMN_ROUTE",
            {
                "transactions": len(running_balance_transactions),
                "income": sum(1 for tx in running_balance_transactions if tx.get("type") == "income"),
                "expenses": sum(1 for tx in running_balance_transactions if tx.get("type") == "expense"),
            },
        )

        if running_balance_transactions:
            return running_balance_transactions

    deposit_withdrawal_balance_transactions = extract_us_deposit_withdrawal_balance_transactions(text)
    if deposit_withdrawal_balance_transactions:
        print(
            "DEPOSIT_WITHDRAWAL_BALANCE_ROUTE",
            {
                "transactions": len(deposit_withdrawal_balance_transactions),
                "income": sum(1 for tx in deposit_withdrawal_balance_transactions if tx.get("type") == "income"),
                "expenses": sum(1 for tx in deposit_withdrawal_balance_transactions if tx.get("type") == "expense"),
            },
        )
        return deposit_withdrawal_balance_transactions

    if statement_layout == "date_description_debit_credit_balance":
        ddcb_transactions = extract_date_description_debit_credit_balance_transactions(text)

        print(
            "DATE_DESCRIPTION_DEBIT_CREDIT_BALANCE_ROUTE",
            {
                "transactions": len(ddcb_transactions),
                "income": sum(1 for tx in ddcb_transactions if tx.get("type") == "income"),
                "expenses": sum(1 for tx in ddcb_transactions if tx.get("type") == "expense"),
            },
        )

        if ddcb_transactions:
            return ddcb_transactions

    if statement_layout == "withdraw_deposit_balance":
        wdb_transactions = extract_withdraw_deposit_balance_transactions(text)

        print(
            "WITHDRAW_DEPOSIT_BALANCE_ROUTE",
            {
                "transactions": len(wdb_transactions),
                "income": sum(1 for tx in wdb_transactions if tx.get("type") == "income"),
                "expenses": sum(1 for tx in wdb_transactions if tx.get("type") == "expense"),
            },
        )

        if len(wdb_transactions) >= 2:
            return wdb_transactions

    if statement_layout == "credit_card_statement":
        cc_transactions = extract_credit_card_statement_transactions(text)

        print(
            "CREDIT_CARD_LAYOUT_ROUTE",
            {
                "transactions": len(cc_transactions),
                "income": sum(1 for tx in cc_transactions if tx.get("type") == "income"),
                "expenses": sum(1 for tx in cc_transactions if tx.get("type") == "expense"),
            },
        )

        return cc_transactions

    if statement_layout == "amount_balance_ledger":
        amount_balance_transactions = extract_standard_amount_balance_ledger_transactions(
            text,
            detect_currency(text),
        )

        print(
            "AMOUNT_BALANCE_LEDGER_ROUTE",
            {
                "transactions": len(amount_balance_transactions),
                "income": sum(1 for tx in amount_balance_transactions if tx.get("type") == "income"),
                "expenses": sum(1 for tx in amount_balance_transactions if tx.get("type") == "expense"),
            },
        )

        if amount_balance_transactions:
            return amount_balance_transactions

    if statement_layout == "amount_balance_ledger":
        typed_transactions = extract_typed_amount_balance_table_transactions(
            text,
            detect_currency(text),
        )

        print(
            "TYPED_AMOUNT_BALANCE_TABLE_ROUTE",
            {
                "transactions": len(typed_transactions),
                "income": sum(1 for tx in typed_transactions if tx.get("type") == "income"),
                "expenses": sum(1 for tx in typed_transactions if tx.get("type") == "expense"),
            },
        )

        if typed_transactions:
            return typed_transactions

    if statement_layout == "debit_credit_table":
        dc_transactions = extract_debit_credit_table_transactions(text)

        print(
            "DEBIT_CREDIT_LAYOUT_ROUTE",
            {
                "transactions": len(dc_transactions),
                "income": sum(1 for tx in dc_transactions if tx.get("type") == "income"),
                "expenses": sum(1 for tx in dc_transactions if tx.get("type") == "expense"),
            },
        )

        if len(dc_transactions) >= 3:
            return dc_transactions

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

    detected_currency = detect_currency(text)

    # New-format branch: generic running-balance column layout.
    # Architecture rule: parser family, not bank-specific.
    running_balance_transactions = extract_running_balance_column_statement_transactions(
        text,
        detected_currency,
    )

    if running_balance_transactions:
        debug_log(
            "RUNNING_BALANCE_LAYOUT_SELECTED",
            {
                "count": len(running_balance_transactions),
                "family": "running_balance_column_statement",
            },
        )
        return running_balance_transactions

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

    previous_amount_balance = None

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

            amount_balance_tx_amount, amount_balance_value = extract_terminal_amount_balance_pair(clean_line)

        # Universal terminal pair authority, valid for FR / EN / AR:
        # if the logical row exposes movement + balance at the end, lock the
        # movement to the penultimate value and the balance to the final value.
        # This fixes Arabic/RTL bilingual tables where the old path sometimes
        # used the running balance as the transaction amount.
        print("AMOUNT_BALANCE_DEBUG_LINE", clean_line)
        print("AMOUNT_BALANCE_DEBUG_NUMBERS", extract_transaction_money_numbers(clean_line))
        print("AMOUNT_BALANCE_DEBUG_PAIR", extract_terminal_amount_balance_pair(clean_line))
        balance = None
        locked_tx_amount, locked_balance = extract_terminal_amount_balance_pair(clean_line)

        if locked_tx_amount is not None and locked_balance is not None:
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


        if is_statement_footer_or_verification_block(clean_line):
            continue

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
        ):
            original_amount_for_lock = amount
            amount_abs = abs(float(amount or 0))
            tx_abs = abs(float(amount_balance_tx_amount or 0))
            balance_abs = abs(float(amount_balance_value or 0))

            if transaction_type is None and tabular_type is not None:
                transaction_type = tabular_type

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

        if (
            "LITTLE BIG CONNECTION" in clean_line.upper()
            or "LBC-20250528585018P" in clean_line.upper()
        ):
            print(
                "LBC_RAW_MATCH",
                {
                    "line": clean_line,
                    "amount": amount,
                    "type": transaction_type,
                },
            )

        tx_type = transaction_type
        description = clean_db_text(clean_line)

        # Standard international rule:
        # refund/reversal/income markers override broad/default expense classification.
        # EN: refund, reversal, charge reversal
        # FR: remboursement, retour carte, remise
        # AR: مبلغ اعادة, عكس رسوم, عكس تحويل رسوم
        income_priority_match = is_income_priority_description(description)

        print(
            "INCOME_PRIORITY_CHECK",
            {
                "match": income_priority_match,
                "amount_before": amount,
                "amount_balance_tx_amount": amount_balance_tx_amount,
                "type_before": tx_type,
                "description": description[:200],
            },
        )

        # Do not let broad income/refund markers override a transaction
        # already classified as an expense by amount/balance or debit semantics.
        # OCR-fused lines may contain both "Received From ..." and later
        # "Card Payment ..." in the same text block.
        if (
            income_priority_match
            and tx_type != "expense"
            and not looks_like_debit_description(description)
        ):
            tx_type = "income"
            if amount_balance_tx_amount is not None:
                amount = abs(float(amount_balance_tx_amount or 0))
            else:
                amount = abs(float(amount or 0))

            print(
                "INCOME_PRIORITY_APPLIED",
                {
                    "amount_after": amount,
                    "type_after": tx_type,
                    "description": description[:200],
                },
            )

        signed_amount = amount

        print(
            "FINAL_TX_DEBUG",
            {
                "amount": amount,
                "balance": balance,
                "signed_amount": signed_amount,
                "type": tx_type,
                "description": description[:100],
            }
        )

        final_amount = signed_amount

        tx = {
            "date": date,
            "description": description,
            "amount": final_amount,
            "type": tx_type,
            "currency": detected_currency,
            "parser_family": "generic_transaction_signal",
        }

        is_amount_balance_row = (
            amount_balance_tx_amount is not None
            and amount_balance_value is not None
        )

        if is_amount_balance_row:
            balance = amount_balance_value
            amount_abs = abs(float(amount_balance_tx_amount or 0))

            if tx.get("parser_family") == "running_balance_column_statement":
                # Parser family is authoritative for amount/type.
                # Balance is informational only.
                tx["_balance"] = balance
                tx["balance"] = balance
                tx["signed_amount"] = tx.get("amount")
                tx["locked_amount"] = tx.get("amount")
                tx["_locked_amount"] = tx.get("amount")
                if tx.get("type") in {"income", "expense"}:
                    tx["locked_type"] = tx.get("type")
                transactions.append(tx)
                previous_amount_balance = float(balance) if balance is not None else previous_amount_balance
                continue

            tx["amount"] = amount_abs
            tx["type"] = None
            tx["_balance"] = balance
            tx["balance"] = balance

            print(

                "BALANCE_DELTA_DEBUG",

                {

                    "prev": previous_amount_balance,

                    "current": balance,

                    "amount": amount_abs,

                    "desc": description[:80],

                },

            )


            if previous_amount_balance is not None:
                delta = round(float(balance) - float(previous_amount_balance), 2)
                tolerance = max(0.02, amount_abs * 0.002)

                if abs(delta - amount_abs) <= tolerance:
                    tx["amount"] = amount_abs
                    tx["type"] = "income"
                    tx["locked_type"] = "income"
                elif abs(delta + amount_abs) <= tolerance:
                    tx["amount"] = -amount_abs
                    tx["type"] = "expense"
                    tx["locked_type"] = "expense"

                if tx.get("locked_type"):
                    tx["signed_amount"] = tx["amount"]
                    tx["locked_amount"] = tx["amount"]
                    tx["_locked_amount"] = tx["amount"]
                    tx["balance_delta"] = delta
                    tx["balance_authority"] = True
                    tx["_balance_locked"] = True
                else:
                    tx["balance_delta"] = delta
                    tx["balance_authority"] = False
                    tx["balance_delta_mismatch"] = True

                    # Standard international FR / EN / AR fallback:
                    # if running-balance authority cannot match because OCR skipped/fused rows,
                    # use the visible movement amount as an expense by default only when
                    # the row is an amount+balance ledger row and not an income/credit marker.
                    if (
                        is_income_priority_description(description.lower())
                        and tx.get("type") != "expense"
                        and not looks_like_debit_description(description)
                    ):
                        tx["amount"] = amount_abs
                        tx["type"] = "income"
                        tx["signed_amount"] = amount_abs
                        tx["locked_amount"] = amount_abs
                        tx["_locked_amount"] = amount_abs
                        tx["locked_type"] = "income"
                    else:
                        tx["amount"] = -amount_abs
                        tx["type"] = "expense"
                        tx["signed_amount"] = -amount_abs
                        tx["locked_amount"] = -amount_abs
                        tx["_locked_amount"] = -amount_abs
                        tx["locked_type"] = "expense"
            else:
                # International fallback:
                # If previous balance is missing but the row has clear debit/credit semantics,
                # do not exclude it from KPIs. Use description semantics.
                if looks_like_debit_description(description):
                    tx["amount"] = -abs(amount_abs)
                    tx["type"] = "expense"
                    tx["signed_amount"] = -abs(amount_abs)
                    tx["locked_amount"] = -abs(amount_abs)
                    tx["_locked_amount"] = -abs(amount_abs)
                    tx["locked_type"] = "expense"
                    tx["category_hint"] = tx.get("category_hint") or "debit_without_previous_balance"
                elif is_income_priority_description(description.lower()) or looks_like_credit_description(description):
                    tx["amount"] = abs(amount_abs)
                    tx["type"] = "income"
                    tx["signed_amount"] = abs(amount_abs)
                    tx["locked_amount"] = abs(amount_abs)
                    tx["_locked_amount"] = abs(amount_abs)
                    tx["locked_type"] = "income"
                    tx["category_hint"] = tx.get("category_hint") or "credit_without_previous_balance"
                else:
                    tx["type"] = None
                    tx = exclude_transaction_from_financial_kpis(tx, "missing_previous_balance")

            if abs(float(balance or 0)) >= 1:
                if not (
                    re.search(
                        r"\b(fee|fees|vat|commission|charge|tax|رسوم|عمولة|ضريبة)\b",
                        description.lower(),
                    )
                    and abs(float(amount_abs or 0)) <= 5
                    and abs(float(balance or 0)) <= 5
                ):
                    previous_amount_balance = float(balance)
        else:
            tx["_locked_amount"] = signed_amount
            tx["locked_amount"] = signed_amount

            if signed_amount > 0:
                tx["locked_type"] = "income"
            elif signed_amount < 0:
                tx["locked_type"] = "expense"

            if is_amount_balance_row:
                tx = preserve_balance_locked_transaction(tx)
            elif tx.get("parser_family") == "running_balance_column_statement":
                # Parser family is authoritative for signed amount/type.
                # Do not let generic canonicalization erase column-derived types.
                pass
            else:
                tx = canonicalize_transaction(tx)

            if balance is not None:
                tx["_balance"] = balance

        if (
            re.search(
                r"\b(fee|fees|vat|commission|charge|رسوم|عمولة|ضريبة)\b",
                description.lower(),
            )
            and not is_income_priority_description(description)
        ):
            tx["amount"] = -abs(float(tx["amount"]))
            tx["type"] = "expense"
            tx["signed_amount"] = tx["amount"]
            tx["locked_amount"] = tx["amount"]
            tx["_locked_amount"] = tx["amount"]
            tx["locked_type"] = "expense"

        transactions.append(tx)

        tx = ensure_transaction_signed_amount(tx)
        print(
            "FINAL_TX_DEBUG",
            {
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "signed_amount": tx.get("signed_amount"),
                "locked": tx.get("_locked_amount"),
                "balance": tx.get("_balance"),
                "description": tx.get("description", "")[:80]
            }
        )

    transactions = infer_balance_delta_rows(transactions)
    transactions = [preserve_balance_locked_transaction(tx) for tx in transactions]

    # Standard international correction:
    # if a generic/OCR parser classified refund/reversal rows as expenses,
    # fix them before quality/KPI stages.
    for tx in transactions:
        description = str(tx.get("description") or "")
        if tx.get("type") == "expense" and is_income_priority_description(description):
            amount = abs(float(tx.get("amount") or 0))
            tx["amount"] = amount
            tx["type"] = "income"
            tx["signed_amount"] = amount
            tx["locked_amount"] = amount
            tx["_locked_amount"] = amount
            tx["locked_type"] = "income"
            tx["category_hint"] = tx.get("category_hint") or "income_priority_refund_reversal"

    amount_balance_transactions = extract_standard_amount_balance_ledger_transactions(
        text,
        detected_currency,
    )

    if amount_balance_transactions:
        existing_income = sum(1 for tx in transactions if tx.get("type") == "income")
        existing_expense = sum(1 for tx in transactions if tx.get("type") == "expense")
        ledger_income = sum(1 for tx in amount_balance_transactions if tx.get("type") == "income")
        ledger_expense = sum(1 for tx in amount_balance_transactions if tx.get("type") == "expense")
        existing_count = len(transactions)
        ledger_count = len(amount_balance_transactions)

        existing_one_sided = existing_count >= 5 and (existing_income == 0 or existing_expense == 0)
        ledger_is_balanced = ledger_income > 0 and ledger_expense > 0

        if (
            not transactions
            or (ledger_is_balanced and existing_one_sided)
            or (ledger_is_balanced and ledger_count > existing_count * 1.20)
        ):
            debug_log("STANDARD_AMOUNT_BALANCE_LEDGER_CANDIDATE", {
                "old_transactions": existing_count,
                "new_transactions": ledger_count,
                "old_income": existing_income,
                "old_expense": existing_expense,
                "new_income": ledger_income,
                "new_expense": ledger_expense,
            })

            # Disabled by design: this secondary fallback can replace correct
            # extracted movements with running balances on amount+balance OCR
            # ledgers. Keep primary canonical extractor output instead.
            debug_log(
                "SKIP_AMOUNT_BALANCE_LEDGER_REPLACEMENT_DISABLED",
                {"candidate_count": len(amount_balance_transactions)},
            )

    sectioned_transactions = extract_standard_sectioned_statement_transactions(
        text,
        detected_currency,
    )

    if should_use_standard_sectioned_statement(transactions, sectioned_transactions):
        existing_typed_ratio = (
            sum(
                1 for tx in transactions
                if tx.get("type") in {"income", "expense"}
            ) / len(transactions)
            if transactions else 0
        )

        debug_log("STANDARD_SECTIONED_STATEMENT_USED", {
            "old_transactions": len(transactions),
            "new_transactions": len(sectioned_transactions),
            "old_typed_ratio": round(existing_typed_ratio, 4),
        })

        transactions = sectioned_transactions

    debug_log(
        "EXPENSE_FULL_AUDIT",
        [
            {
                "date": tx.get("date"),
                "amount": tx.get("amount"),
                "type": tx.get("type"),
                "description": tx.get("description"),
                "balance": tx.get("_balance"),
            }
            for tx in transactions
            if tx.get("type") == "expense"
        ]
    )

    for tx in transactions:
        if "_balance" in tx:
            balance = tx.get("_balance")
            amount = tx.get("amount")

            if balance is not None and amount is not None:
                if round(abs(float(amount)), 2) == round(abs(float(balance)), 2):
                    original = tx.get("locked_amount") or tx.get("_locked_amount")

                    if original is not None:
                        if tx.get("locked_type") == "expense":
                            original = -abs(float(original))
                        elif tx.get("locked_type") == "income":
                            original = abs(float(original))

                        tx["locked_amount"] = original
                        tx["_locked_amount"] = original
                        tx["signed_amount"] = original
                        tx["amount"] = original

    if not transactions:
        transactions = extract_wallet_tabular_transactions(
            text,
            detected_currency,
        )
        print(
            "TX_SOURCE_SELECTED",
            {
                "source": "wallet_tabular",
                "count": len(transactions),
                "income": sum(1 for tx in transactions if tx.get("type") == "income"),
                "expense": sum(1 for tx in transactions if tx.get("type") == "expense"),
            },
        )

    if not transactions:
        transactions = extract_standard_amount_balance_ledger_transactions(
            text,
            detected_currency,
        )
        print(
            "TX_SOURCE_SELECTED",
            {
                "source": "standard_amount_balance_ledger",
                "count": len(transactions),
                "income": sum(1 for tx in transactions if tx.get("type") == "income"),
                "expense": sum(1 for tx in transactions if tx.get("type") == "expense"),
            },
        )

    if not transactions:
        sectioned_transactions = extract_standard_sectioned_statement_transactions(
            text,
            detected_currency,
        )

        if should_use_standard_sectioned_statement([], sectioned_transactions):
            transactions = sectioned_transactions

    if not transactions:
        debug_log(
            "TX_DEBUG: normal_extraction_empty_using_signed_amount_fallback"
        )
        transactions = extract_signed_amount_fallback_transactions(
            text,
            detected_currency,
        )
        print(
            "TX_SOURCE_SELECTED",
            {
                "source": "signed_amount_fallback",
                "count": len(transactions),
                "income": sum(1 for tx in transactions if tx.get("type") == "income"),
                "expense": sum(1 for tx in transactions if tx.get("type") == "expense"),
            },
        )

    transactions = [preserve_balance_locked_transaction(tx) for tx in transactions]

    transactions = mark_internal_transfers(
        transactions,
        text,
    )

    transactions = [
        tx
        for tx in transactions
        if not (
            is_non_transaction_line(
                tx.get("description")
                or tx.get("text")
                or ""
            )
            or is_balance_snapshot_line(
                tx.get("description")
                or tx.get("text")
                or ""
            )
        )
    ]

    print(
        "NON_TRANSACTION_FILTER_STATS",
        {
            "remaining": len(transactions),
        },
    )

    transactions = fallback_debit_credit_column_transactions_if_low_quality(
        transactions,
        text,
        detected_currency,
    )

    transactions = fallback_vertical_transactions_if_empty(
        transactions,
        text,
        detected_currency,
    )

    transactions = fallback_debit_credit_column_transactions_if_low_quality(
        transactions,
        text,
        detected_currency,
    )

    print(
        "INTERNAL_TRANSFER_STATS",
        {
            "detected": sum(
                1 for tx in transactions
                if tx.get("is_internal_transfer")
            ),
            "total": len(transactions),
        },
    )

    log_final_transactions(transactions)
    debug_log("FINAL_TXS", transactions)

    print(
        "LBC_FINAL_TX",
        [
            tx
            for tx in transactions
            if "LITTLE" in str(tx.get("description", "")).upper()
            or "CONNECTION" in str(tx.get("description", "")).upper()
        ],
    )

    for tx in transactions:
        if "_balance" in tx:
            balance = tx.get("_balance")
            amount = tx.get("amount")

            if balance is not None and amount is not None:
                if round(abs(float(amount)), 2) == round(abs(float(balance)), 2):
                    original = tx.get("locked_amount") or tx.get("_locked_amount")

                    if original is not None:
                        if tx.get("locked_type") == "expense":
                            original = -abs(float(original))
                        elif tx.get("locked_type") == "income":
                            original = abs(float(original))

                        tx["locked_amount"] = original
                        tx["_locked_amount"] = original
                        tx["signed_amount"] = original
                        tx["amount"] = original

    transactions = enforce_no_untyped_kpi_transactions(transactions)

    for tx in transactions:
        if (
        tx.get("_balance") is not None
        and not tx.get("_balance_locked")
        and not tx.get("balance_delta_mismatch")
    ):
            tx["type"] = None
            tx.pop("signed_amount", None)
            tx.pop("locked_amount", None)
            tx.pop("_locked_amount", None)
            tx.pop("locked_type", None)
            tx = exclude_transaction_from_financial_kpis(
                tx,
                tx.get("category_hint") or "unlocked_amount_balance_row",
            )
            continue

        if tx.get("signed_amount") is not None:
            tx["locked_amount"] = tx["signed_amount"]
            tx["_locked_amount"] = tx["signed_amount"]

        if tx.get("locked_type"):
            if tx.get("locked_amount") is not None:
                if tx.get("locked_type") == "expense":
                    tx["locked_amount"] = -abs(float(tx["locked_amount"]))
                elif tx.get("locked_type") == "income":
                    tx["locked_amount"] = abs(float(tx["locked_amount"]))

            tx["type"] = tx["locked_type"]
            tx["amount"] = tx["locked_amount"]
            tx["signed_amount"] = tx["locked_amount"]
            tx["_locked_amount"] = tx["locked_amount"]

        elif tx.get("type") is None:
            tx = exclude_transaction_from_financial_kpis(tx, "untyped_unreliable")

    print(
        "KPI_INPUT_DEBUG",
        [
            {
                "amount": getattr(t, "amount", t.get("amount") if isinstance(t, dict) else None),
                "type": getattr(t, "type", t.get("type") if isinstance(t, dict) else None),
            }
            for t in transactions[:20]
        ]
    )

    print(
        "KPI_INPUT_DEBUG",
        [
            {
                "amount": t.get("amount"),
                "signed": t.get("signed_amount"),
                "locked": t.get("_locked_amount"),
                "balance": t.get("_balance")
            }
            for t in transactions[:20]
        ]
    )

    debug_log(
        "EXPENSE_SUMMARY_AUDIT",
        {
            "expense_count": sum(
                1 for tx in transactions
                if tx.get("type") == "expense"
            ),
            "expense_total": round(
                sum(
                    abs(tx.get("amount", 0))
                    for tx in transactions
                    if tx.get("type") == "expense"
                ),
                2,
            ),
        },
    )

    debug_log(
        "ALL_INCOME_TRANSACTIONS",
        [
            tx
            for tx in transactions
            if tx.get("type") == "income"
        ]
    )


    for tx in transactions:
        desc = str(tx.get("description") or "").lower()

        if (
            any(k in desc for k in [
                "fee", "fees", "charge", "commission", "tax", "vat",
                "frais", "taxe", "tva", "commission",
                "رسوم", "رسم", "ضريبة", "الضريبة", "القيمة المضافة", "عمولة",
            ])
            and not is_income_priority_description(desc)
        ):
            amount = abs(float(tx.get("amount") or 0))
            tx["amount"] = -amount
            tx["type"] = "expense"
            tx["signed_amount"] = -amount
            tx["locked_amount"] = -amount
            tx["_locked_amount"] = -amount
            tx["locked_type"] = "expense"

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
    "سحب نقدي",
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


# Final universal transaction markers safety net.
# This keeps production behavior standard international FR / EN / AR.
for _marker in UNIVERSAL_EXPENSE_MARKERS:
    if _marker not in EXPENSE_KEYWORDS:
        EXPENSE_KEYWORDS.append(_marker)
    if _marker not in TRANSACTION_SIGNALS:
        TRANSACTION_SIGNALS.append(_marker)

for _marker in UNIVERSAL_INCOME_MARKERS:
    if _marker not in INCOME_KEYWORDS:
        INCOME_KEYWORDS.append(_marker)
    if _marker not in TRANSACTION_SIGNALS:
        TRANSACTION_SIGNALS.append(_marker)

