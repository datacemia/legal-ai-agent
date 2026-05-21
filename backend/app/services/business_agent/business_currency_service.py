import re
from collections import Counter
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any


DEFAULT_CURRENCY_CODE = "USD"


CURRENCY_METADATA: dict[str, dict[str, str]] = {
    "USD": {
        "symbol": "$",
        "name": "US Dollar",
        "position": "prefix",
        "locale": "en-US",
    },
    "EUR": {
        "symbol": "€",
        "name": "Euro",
        "position": "prefix",
        "locale": "fr-FR",
    },
    "MAD": {
        "symbol": "د.م",
        "name": "Moroccan Dirham",
        "position": "suffix",
        "locale": "fr-MA",
    },
    "GBP": {
        "symbol": "£",
        "name": "British Pound",
        "position": "prefix",
        "locale": "en-GB",
    },
    "CAD": {
        "symbol": "C$",
        "name": "Canadian Dollar",
        "position": "prefix",
        "locale": "en-CA",
    },
    "AUD": {
        "symbol": "A$",
        "name": "Australian Dollar",
        "position": "prefix",
        "locale": "en-AU",
    },
    "AED": {
        "symbol": "AED",
        "name": "UAE Dirham",
        "position": "suffix",
        "locale": "ar-AE",
    },
    "SAR": {
        "symbol": "SAR",
        "name": "Saudi Riyal",
        "position": "suffix",
        "locale": "ar-SA",
    },
    "QAR": {
        "symbol": "QAR",
        "name": "Qatari Riyal",
        "position": "suffix",
        "locale": "ar-QA",
    },
    "KWD": {
        "symbol": "KWD",
        "name": "Kuwaiti Dinar",
        "position": "suffix",
        "locale": "ar-KW",
    },
    "BHD": {
        "symbol": "BHD",
        "name": "Bahraini Dinar",
        "position": "suffix",
        "locale": "ar-BH",
    },
    "OMR": {
        "symbol": "OMR",
        "name": "Omani Rial",
        "position": "suffix",
        "locale": "ar-OM",
    },
    "EGP": {
        "symbol": "EGP",
        "name": "Egyptian Pound",
        "position": "suffix",
        "locale": "ar-EG",
    },
    "TND": {
        "symbol": "TND",
        "name": "Tunisian Dinar",
        "position": "suffix",
        "locale": "ar-TN",
    },
    "DZD": {
        "symbol": "DZD",
        "name": "Algerian Dinar",
        "position": "suffix",
        "locale": "ar-DZ",
    },
    "JPY": {
        "symbol": "¥",
        "name": "Japanese Yen",
        "position": "prefix",
        "locale": "ja-JP",
    },
    "CNY": {
        "symbol": "¥",
        "name": "Chinese Yuan",
        "position": "prefix",
        "locale": "zh-CN",
    },
    "INR": {
        "symbol": "₹",
        "name": "Indian Rupee",
        "position": "prefix",
        "locale": "en-IN",
    },
    "BRL": {
        "symbol": "R$",
        "name": "Brazilian Real",
        "position": "prefix",
        "locale": "pt-BR",
    },
    "MXN": {
        "symbol": "MX$",
        "name": "Mexican Peso",
        "position": "prefix",
        "locale": "es-MX",
    },
    "CHF": {
        "symbol": "CHF",
        "name": "Swiss Franc",
        "position": "suffix",
        "locale": "de-CH",
    },
    "SEK": {
        "symbol": "SEK",
        "name": "Swedish Krona",
        "position": "suffix",
        "locale": "sv-SE",
    },
    "NOK": {
        "symbol": "NOK",
        "name": "Norwegian Krone",
        "position": "suffix",
        "locale": "nb-NO",
    },
    "DKK": {
        "symbol": "DKK",
        "name": "Danish Krone",
        "position": "suffix",
        "locale": "da-DK",
    },
    "ZAR": {
        "symbol": "R",
        "name": "South African Rand",
        "position": "prefix",
        "locale": "en-ZA",
    },
    "NGN": {
        "symbol": "₦",
        "name": "Nigerian Naira",
        "position": "prefix",
        "locale": "en-NG",
    },
    "TRY": {
        "symbol": "₺",
        "name": "Turkish Lira",
        "position": "prefix",
        "locale": "tr-TR",
    },
}


CURRENCY_SYMBOL_TO_CODE: dict[str, str] = {
    "$": "USD",
    "US$": "USD",
    "USD": "USD",
    "€": "EUR",
    "EUR": "EUR",
    "£": "GBP",
    "GBP": "GBP",
    "C$": "CAD",
    "CA$": "CAD",
    "CAD": "CAD",
    "A$": "AUD",
    "AU$": "AUD",
    "AUD": "AUD",
    "د.م": "MAD",
    "درهم": "MAD",
    "DH": "MAD",
    "DHS": "MAD",
    "MAD": "MAD",
    "AED": "AED",
    "د.إ": "AED",
    "SAR": "SAR",
    "ر.س": "SAR",
    "QAR": "QAR",
    "ر.ق": "QAR",
    "KWD": "KWD",
    "BHD": "BHD",
    "OMR": "OMR",
    "EGP": "EGP",
    "TND": "TND",
    "DZD": "DZD",
    "JPY": "JPY",
    "¥": "JPY",
    "CNY": "CNY",
    "RMB": "CNY",
    "INR": "INR",
    "₹": "INR",
    "BRL": "BRL",
    "R$": "BRL",
    "MXN": "MXN",
    "MX$": "MXN",
    "CHF": "CHF",
    "SEK": "SEK",
    "NOK": "NOK",
    "DKK": "DKK",
    "ZAR": "ZAR",
    "NGN": "NGN",
    "₦": "NGN",
    "TRY": "TRY",
    "₺": "TRY",
}


CURRENCY_COLUMN_NAMES = {
    "currency",
    "curr",
    "devise",
    "monnaie",
    "moneda",
    "عملة",
    "العملة",
    "currency_code",
    "currencycode",
    "iso_currency",
}


MONEY_KEYWORDS = {
    "revenue",
    "revenues",
    "sales",
    "income",
    "turnover",
    "expenses",
    "expense",
    "cost",
    "costs",
    "profit",
    "margin",
    "cashflow",
    "cash_flow",
    "mrr",
    "arr",
    "cac",
    "ltv",
    "ad_spend",
    "spend",
    "budget",
    "price",
    "amount",
    "total",
    "invoice",
    "payment",
    "paid",
    "refund",
    "discount",
    "salary",
    "payroll",
    "rent",
    "revenue_per_customer",
}


def normalize_currency_code(value: Any) -> str | None:
    if value is None:
        return None

    raw = str(value).strip()

    if not raw:
        return None

    upper = raw.upper().replace(".", "").strip()

    if upper in CURRENCY_METADATA:
        return upper

    if raw in CURRENCY_SYMBOL_TO_CODE:
        return CURRENCY_SYMBOL_TO_CODE[raw]

    if upper in CURRENCY_SYMBOL_TO_CODE:
        return CURRENCY_SYMBOL_TO_CODE[upper]

    compact = (
        raw.replace(" ", "")
        .replace("\u00a0", "")
        .replace(".", "")
        .upper()
    )

    if compact in CURRENCY_SYMBOL_TO_CODE:
        return CURRENCY_SYMBOL_TO_CODE[compact]

    return None


def get_currency_metadata(code: str | None) -> dict[str, str]:
    normalized = normalize_currency_code(code) or DEFAULT_CURRENCY_CODE

    metadata = CURRENCY_METADATA.get(
        normalized,
        CURRENCY_METADATA[DEFAULT_CURRENCY_CODE],
    ).copy()

    metadata["code"] = normalized

    return metadata


def detect_currency_in_text(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    upper_text = text.upper()

    # Prefer explicit ISO codes over ambiguous symbols.
    for code in CURRENCY_METADATA.keys():
        pattern = rf"(?<![A-Z]){re.escape(code)}(?![A-Z])"

        if re.search(pattern, upper_text):
            return code

    # Then check symbols / localized names.
    sorted_symbols = sorted(
        CURRENCY_SYMBOL_TO_CODE.keys(),
        key=len,
        reverse=True,
    )

    for symbol in sorted_symbols:
        if symbol and symbol in text:
            return CURRENCY_SYMBOL_TO_CODE[symbol]

        if symbol and symbol.upper() in upper_text:
            return CURRENCY_SYMBOL_TO_CODE[symbol]

    return None


def normalize_numeric_value(value: Any) -> float | None:
    """
    Converts international numeric text into float.

    Supported examples:
    - 137,300.50
    - 137 300,50
    - 137.300,50
    - 137300.50
    - 137300,50
    - $137,300.50
    - 137000 MAD
    - د.م 137000
    """

    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, int | float):
        if isinstance(value, float) and not value == value:
            return None

        return float(value)

    text = str(value).strip()

    if not text:
        return None

    # Remove currency words/symbols and keep digits, separators and minus.
    cleaned = text

    for token in sorted(CURRENCY_SYMBOL_TO_CODE.keys(), key=len, reverse=True):
        cleaned = cleaned.replace(token, "")

    cleaned = re.sub(
        r"[^\d,\.\-\s\u00a0]",
        "",
        cleaned,
    )

    cleaned = cleaned.replace("\u00a0", " ").strip()

    if not cleaned:
        return None

    negative = False

    if cleaned.startswith("(") and cleaned.endswith(")"):
        negative = True
        cleaned = cleaned[1:-1]

    if cleaned.count("-") > 0:
        negative = True
        cleaned = cleaned.replace("-", "")

    cleaned = cleaned.strip()

    # Remove spaces used as thousand separators.
    cleaned_no_spaces = cleaned.replace(" ", "")

    if not cleaned_no_spaces:
        return None

    has_comma = "," in cleaned_no_spaces
    has_dot = "." in cleaned_no_spaces

    normalized = cleaned_no_spaces

    if has_comma and has_dot:
        last_comma = normalized.rfind(",")
        last_dot = normalized.rfind(".")

        if last_comma > last_dot:
            # 137.300,50 -> 137300.50
            normalized = normalized.replace(".", "")
            normalized = normalized.replace(",", ".")
        else:
            # 137,300.50 -> 137300.50
            normalized = normalized.replace(",", "")

    elif has_comma and not has_dot:
        comma_parts = normalized.split(",")

        if len(comma_parts[-1]) in {1, 2}:
            # 137300,50 -> decimal comma
            normalized = normalized.replace(",", ".")
        else:
            # 137,300 -> thousand comma
            normalized = normalized.replace(",", "")

    elif has_dot and not has_comma:
        dot_parts = normalized.split(".")

        if len(dot_parts) > 2:
            # 1.234.567 -> thousands
            normalized = normalized.replace(".", "")
        elif len(dot_parts[-1]) == 3 and len(dot_parts[0]) <= 3:
            # 137.300 -> likely thousands
            normalized = normalized.replace(".", "")
        else:
            # 137300.50 -> decimal dot
            normalized = normalized

    try:
        parsed = Decimal(normalized)
    except InvalidOperation:
        return None

    if negative:
        parsed = -parsed

    return float(parsed)


def parse_money(value: Any) -> dict[str, Any]:
    currency_code = detect_currency_in_text(value)
    amount = normalize_numeric_value(value)

    return {
        "amount": amount,
        "currency_code": currency_code,
        "has_currency": currency_code is not None,
        "raw": value,
    }


def is_money_column(column_name: Any) -> bool:
    if column_name is None:
        return False

    normalized = (
        str(column_name)
        .lower()
        .strip()
        .replace(" ", "_")
        .replace("-", "_")
    )

    if normalized in CURRENCY_COLUMN_NAMES:
        return False

    return any(keyword in normalized for keyword in MONEY_KEYWORDS)


def detect_currency_from_columns(rows: list[dict[str, Any]]) -> list[str]:
    detected: list[str] = []

    for row in rows:
        for key, value in row.items():
            key_normalized = str(key).lower().strip()

            if key_normalized in CURRENCY_COLUMN_NAMES:
                code = normalize_currency_code(value)

                if code:
                    detected.append(code)

    return detected


def detect_currency_from_values(rows: list[dict[str, Any]]) -> list[str]:
    detected: list[str] = []

    for row in rows:
        for key, value in row.items():
            if value is None:
                continue

            if not is_money_column(key):
                # Still detect if value contains explicit currency symbol/code.
                code = detect_currency_in_text(value)

                if code:
                    detected.append(code)

                continue

            code = detect_currency_in_text(value)

            if code:
                detected.append(code)

    return detected


def detect_currency(
    rows: list[dict[str, Any]] | None,
    default_currency: str = DEFAULT_CURRENCY_CODE,
) -> dict[str, Any]:
    safe_rows = rows or []

    column_codes = detect_currency_from_columns(safe_rows)
    value_codes = detect_currency_from_values(safe_rows)

    all_codes = column_codes + value_codes

    if all_codes:
        counts = Counter(all_codes)
        code = counts.most_common(1)[0][0]
        detected_from = "columns" if code in column_codes else "values"
    else:
        code = normalize_currency_code(default_currency) or DEFAULT_CURRENCY_CODE
        counts = Counter({code: 1})
        detected_from = "default"

    metadata = get_currency_metadata(code)

    unique_codes = sorted(set(all_codes or [code]))

    return {
        "code": metadata["code"],
        "symbol": metadata["symbol"],
        "name": metadata["name"],
        "locale": metadata["locale"],
        "position": metadata["position"],
        "detected_from": detected_from,
        "multi_currency_detected": len(unique_codes) > 1,
        "detected_currencies": unique_codes,
        "confidence": calculate_currency_confidence(
            selected_code=metadata["code"],
            detected_codes=all_codes,
            detected_from=detected_from,
        ),
    }


def detect_multi_currency(rows: list[dict[str, Any]] | None) -> dict[str, Any]:
    safe_rows = rows or []

    all_codes = (
        detect_currency_from_columns(safe_rows)
        + detect_currency_from_values(safe_rows)
    )

    counts = Counter(all_codes)
    unique = sorted(counts.keys())

    return {
        "multi_currency_detected": len(unique) > 1,
        "detected_currencies": unique,
        "counts": dict(counts),
    }


def calculate_currency_confidence(
    selected_code: str,
    detected_codes: list[str],
    detected_from: str,
) -> float:
    if detected_from == "default":
        return 0.35

    if not detected_codes:
        return 0.35

    counts = Counter(detected_codes)
    total = sum(counts.values())

    if total <= 0:
        return 0.35

    share = counts[selected_code] / total

    base = 0.65 if detected_from == "values" else 0.8

    confidence = min(0.99, max(base, share))

    return round(confidence, 2)


def format_money(
    value: Any,
    currency: dict[str, Any] | str | None = None,
    decimals: int = 2,
    compact: bool = False,
) -> str:
    amount = normalize_numeric_value(value)

    if amount is None:
        return "-"

    if isinstance(currency, dict):
        code = currency.get("code")
    else:
        code = currency

    metadata = get_currency_metadata(code)

    quantizer = Decimal("1") if decimals <= 0 else Decimal("1." + ("0" * decimals))

    decimal_amount = Decimal(str(amount)).quantize(
        quantizer,
        rounding=ROUND_HALF_UP,
    )

    if compact:
        abs_amount = abs(float(decimal_amount))

        if abs_amount >= 1_000_000_000:
            number = f"{float(decimal_amount) / 1_000_000_000:.1f}B"
        elif abs_amount >= 1_000_000:
            number = f"{float(decimal_amount) / 1_000_000:.1f}M"
        elif abs_amount >= 1_000:
            number = f"{float(decimal_amount) / 1_000:.1f}K"
        else:
            number = f"{float(decimal_amount):,.{decimals}f}"
    else:
        number = f"{decimal_amount:,.{decimals}f}"

        if decimals > 0:
            number = number.rstrip("0").rstrip(".")

    symbol = metadata["symbol"]

    if metadata["position"] == "prefix":
        return f"{symbol}{number}"

    return f"{number} {symbol}"


def normalize_money_columns(
    rows: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    """
    Returns a copy of rows where money-like values are converted to floats.

    This should be used before KPI calculations.
    It does not remove original non-money columns.
    """

    normalized_rows: list[dict[str, Any]] = []

    for row in rows or []:
        normalized_row: dict[str, Any] = {}

        for key, value in row.items():
            if is_money_column(key):
                parsed = normalize_numeric_value(value)
                normalized_row[key] = parsed if parsed is not None else value
            else:
                normalized_row[key] = value

        normalized_rows.append(normalized_row)

    return normalized_rows


def attach_currency_to_result(
    result: dict[str, Any],
    rows: list[dict[str, Any]] | None,
    default_currency: str = DEFAULT_CURRENCY_CODE,
) -> dict[str, Any]:
    currency = detect_currency(
        rows=rows,
        default_currency=default_currency,
    )

    result["currency"] = currency

    if currency.get("multi_currency_detected"):
        result["currency_warning"] = {
            "code": "multi_currency_detected",
            "message": "Multiple currencies detected in uploaded data.",
            "detected_currencies": currency.get("detected_currencies", []),
            "source": "business_currency_service",
        }

    return result


def build_currency_warning(
    currency: dict[str, Any],
    language: str = "en",
) -> str | None:
    if not currency.get("multi_currency_detected"):
        return None

    if language == "fr":
        return "Plusieurs devises ont été détectées dans les données importées."

    if language == "ar":
        return "تم اكتشاف عدة عملات داخل البيانات التي تم رفعها."

    return "Multiple currencies detected in uploaded data."


def get_money_display_fields(
    result: dict[str, Any],
    fields: list[str],
    decimals: int = 2,
) -> dict[str, str]:
    currency = result.get("currency") or get_currency_metadata(DEFAULT_CURRENCY_CODE)
    output: dict[str, str] = {}

    for field in fields:
        value = result.get(field)

        if value is None and isinstance(result.get("kpis"), dict):
            value = result["kpis"].get(field)

        if value is None and isinstance(result.get("advanced_kpis"), dict):
            value = result["advanced_kpis"].get(field)

        output[field] = format_money(
            value,
            currency=currency,
            decimals=decimals,
        )

    return output


def summarize_currency_context(
    currency: dict[str, Any],
) -> dict[str, Any]:
    return {
        "code": currency.get("code"),
        "symbol": currency.get("symbol"),
        "name": currency.get("name"),
        "detected_from": currency.get("detected_from"),
        "multi_currency_detected": currency.get("multi_currency_detected", False),
        "detected_currencies": currency.get("detected_currencies", []),
        "confidence": currency.get("confidence"),
    }
