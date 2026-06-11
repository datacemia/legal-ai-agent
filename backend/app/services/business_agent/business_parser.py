import csv
import io
import re
from datetime import date, datetime
from typing import Any

from fastapi import UploadFile
from openpyxl import load_workbook

from app.services.business_agent.business_kpi_detector import detect_kpi_columns


COLUMN_ALIASES = {
    "date": [
        "date",
        "day",
        "transaction_date",
        "order_date",
        "purchase_date",
        "invoice_date",
        "payment_date",
        "checkout_date",
        "booking_date",
        "created_at",
        "created",
        "time",
        "timestamp",
        "month",
        "period",
        "jour",
        "mois",
        "période",
        "periode",
        "date_transaction",
        "date_commande",
        "date_achat",
        "date_paiement",
        "date_creation",
        "تاريخ",
        "يوم",
        "شهر",
        "فترة",
    ],
    "revenue": [
        "revenue",
        "sales",
        "sale",
        "income",
        "turnover",
        "amount",
        "total_amount",
        "order_total",
        "line_total",
        "item_total",
        "subtotal",
        "total",
        "price_total",
        "purchase_amount",
        "payment_amount",
        "amount_in",
        "credit",
        "credits",
        "payment_received",
        "received",
        "gross_sales",
        "net_sales",
        "total_sales",
        "gross_amount",
        "net_amount",
        "revenue_amount",
        "vente_totale",
        "montant_total",
        "total_commande",
        "montant_achat",
        "montant_paiement",
        "revenu",
        "revenus",
        "chiffre_affaires",
        "ventes",
        "vente",
        "recettes",
        "encaissement",
        "paiement_recu",
        "montant_entrant",
        "إيراد",
        "إيرادات",
        "مبيعات",
        "دخل",
        "المداخيل",
        "مداخيل",
        "مبلغ_داخل",
    ],
    "expenses": [
        "expense",
        "expenses",
        "cost",
        "costs",
        "amount_out",
        "debit",
        "debits",
        "spend",
        "spending",
        "paid",
        "payment",
        "ad_cost",
        "ads_cost",
        "marketing_cost",
        "fees",
        "charge",
        "charges",
        "depense",
        "depenses",
        "cout",
        "couts",
        "frais",
        "paiement",
        "montant_sortant",
        "مصروف",
        "مصروفات",
        "تكلفة",
        "تكاليف",
        "نفقات",
        "دفع",
        "رسوم",
        "مبلغ_خارج",
    ],
    "expense": [
        "expense",
        "expenses",
        "cost",
        "costs",
        "amount_out",
        "debit",
        "debits",
        "spend",
        "spending",
        "paid",
        "payment",
        "ad_cost",
        "ads_cost",
        "marketing_cost",
        "fees",
        "charge",
        "charges",
        "dépense",
        "depense",
        "dépenses",
        "depenses",
        "coût",
        "cout",
        "coûts",
        "couts",
        "frais",
        "paiement",
        "montant_sortant",
        "مصروف",
        "مصروفات",
        "تكلفة",
        "تكاليف",
        "نفقات",
        "دفع",
        "رسوم",
        "مبلغ_خارج",
    ],
    "profit": [
        "profit",
        "net_profit",
        "gross_profit",
        "margin",
        "benefit",
        "bénéfice",
        "benefice",
        "marge",
        "résultat",
        "resultat",
        "ربح",
        "أرباح",
        "هامش",
        "صافي_الربح",
    ],
    "category": [
        "category",
        "type",
        "label",
        "description",
        "merchant",
        "vendor",
        "account",
        "item",
        "product",
        "service",
        "source",
        "channel",
        "catégorie",
        "categorie",
        "libellé",
        "libelle",
        "description",
        "marchand",
        "fournisseur",
        "compte",
        "produit",
        "canal",
        "فئة",
        "نوع",
        "وصف",
        "تاجر",
        "مورد",
        "حساب",
        "منتج",
        "خدمة",
        "مصدر",
        "قناة",
    ],
    "orders": [
        "orders",
        "order",
        "order_id",
        "purchase_id",
        "transaction_id",
        "invoice_id",
        "receipt_id",
        "checkout_id",
        "booking_id",
        "nombre_commandes",
        "commande_id",
        "id_commande",
        "achat_id",
        "id_achat",
        "طلبات",
        "طلب",
        "معرف_الطلب",
        "معرف_الشراء",
    ],
    "customers": [
        "customers",
        "customer",
        "customer_id",
        "user_id",
        "client_id",
        "buyer_id",
        "account_id",
        "member_id",
        "subscriber_id",
        "clients",
        "client",
        "id_client",
        "utilisateur_id",
        "acheteur_id",
        "عملاء",
        "عميل",
        "زبائن",
        "مستخدم",
        "معرف_العميل",
        "معرف_المستخدم",
    ],
}


def normalize_column_name(name: Any) -> str:
    value = str(name or "").strip().lower()

    replacements = {
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "à": "a",
        "â": "a",
        "ä": "a",
        "ù": "u",
        "û": "u",
        "ü": "u",
        "ô": "o",
        "ö": "o",
        "î": "i",
        "ï": "i",
        "ç": "c",
    }

    for source, target in replacements.items():
        value = value.replace(source, target)

    value = re.sub(r"[^\w\u0600-\u06FF]+", "_", value, flags=re.UNICODE)
    value = re.sub(r"_+", "_", value).strip("_")

    return value


def detect_column_mapping(fieldnames: list[str]) -> dict[str, str]:
    normalized_fields = {
        normalize_column_name(field): field
        for field in fieldnames
        if field
    }

    mapping: dict[str, str] = {}

    for target, aliases in COLUMN_ALIASES.items():
        normalized_aliases = [
            normalize_column_name(alias)
            for alias in aliases
        ]

        for alias in normalized_aliases:
            if alias in normalized_fields:
                mapping[target] = normalized_fields[alias]
                break

        if target not in mapping:
            for normalized_field, original_field in normalized_fields.items():
                if any(
                    alias and alias in normalized_field
                    for alias in normalized_aliases
                ):
                    mapping[target] = original_field
                    break

    return mapping


def clean_cell(value: Any) -> Any:
    if value is None:
        return ""

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    return value


def detect_numeric_columns(
    rows: list[dict[str, Any]],
    fieldnames: list[str],
) -> list[str]:
    numeric_columns: list[str] = []

    for field in fieldnames:
        checked = 0
        numeric_count = 0

        for row in rows[:50]:
            value = row.get(field)

            if value in (None, ""):
                continue

            checked += 1

            if parse_number(value) is not None:
                numeric_count += 1

        if checked > 0 and numeric_count / checked >= 0.6:
            numeric_columns.append(field)

    return numeric_columns


def detect_date_columns(
    rows: list[dict[str, Any]],
    fieldnames: list[str],
) -> list[str]:
    date_columns: list[str] = []

    for field in fieldnames:
        normalized = normalize_column_name(field)

        if any(
            token in normalized
            for token in ["date", "day", "month", "period", "jour", "mois", "periode", "تاريخ", "شهر"]
        ):
            date_columns.append(field)
            continue

        checked = 0
        date_count = 0

        for row in rows[:50]:
            value = row.get(field)

            if value in (None, ""):
                continue

            checked += 1

            if parse_period(value) != "Unknown":
                date_count += 1

        if checked > 0 and date_count / checked >= 0.6:
            date_columns.append(field)

    return list(dict.fromkeys(date_columns))


def parse_number(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()

    if not text:
        return None

    negative = False

    if text.startswith("(") and text.endswith(")"):
        negative = True
        text = text[1:-1]

    text = (
        text.replace("$", "")
        .replace("€", "")
        .replace("£", "")
        .replace("MAD", "")
        .replace("DH", "")
        .replace("dhs", "")
        .replace("USD", "")
        .replace("EUR", "")
        .replace(" ", "")
        .strip()
    )

    text = re.sub(r"[^0-9,\.\-]", "", text)

    if not text:
        return None

    if "," in text and "." in text:
        text = text.replace(",", "")
    elif "," in text and "." not in text:
        text = text.replace(",", ".")

    try:
        number = float(text)
        return -number if negative else number
    except ValueError:
        return None


def parse_period(value: Any) -> str:
    if value is None:
        return "Unknown"

    if isinstance(value, datetime):
        return value.strftime("%Y-%m")

    if isinstance(value, date):
        return value.strftime("%Y-%m")

    text = str(value).strip()

    if not text:
        return "Unknown"

    # Accept ISO datetimes with time / fractional seconds, including nanoseconds
    # such as "2023-01-15 18:05:44.055402424".
    iso_date_match = re.match(r"^(\d{4})-(\d{2})-(\d{2})", text)

    if iso_date_match:
        return f"{iso_date_match.group(1)}-{iso_date_match.group(2)}"

    known_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y-%m",
        "%m-%Y",
        "%d-%m-%Y",
        "%Y.%m.%d",
    ]

    for fmt in known_formats:
        try:
            parsed = datetime.strptime(text, fmt)
            return parsed.strftime("%Y-%m")
        except ValueError:
            continue

    # Already a period like 2025-01.
    if re.match(r"^\d{4}-\d{2}$", text):
        return text

    # Keep short month text like Jan 2025 as-is.
    if len(text) <= 20 and re.search(r"\d{4}", text):
        return text

    return "Unknown"


def build_preview(
    filename: str,
    fieldnames: list[str],
    rows: list[dict[str, Any]],
    column_mapping: dict[str, str],
    numeric_columns: list[str],
    date_columns: list[str],
) -> str:
    preview_lines = []

    preview_lines.append("Business data preview:")
    preview_lines.append(f"File name: {filename}")
    preview_lines.append(f"Columns: {', '.join(fieldnames)}")
    preview_lines.append(f"Rows count: {len(rows)}")
    preview_lines.append("")
    preview_lines.append("Detected column mapping:")

    if column_mapping:
        for target, source in column_mapping.items():
            preview_lines.append(f"{target} -> {source}")
    else:
        preview_lines.append(
            "No obvious mapping detected. Infer carefully from column names and sample rows."
        )

    preview_lines.append("")
    preview_lines.append("Detected numeric columns:")

    if numeric_columns:
        preview_lines.append(", ".join(numeric_columns))
    else:
        preview_lines.append("No numeric columns confidently detected.")

    preview_lines.append("")
    preview_lines.append("Detected date columns:")

    if date_columns:
        preview_lines.append(", ".join(date_columns))
    else:
        preview_lines.append("No date columns confidently detected.")

    preview_lines.append("")
    preview_lines.append("Sample rows:")

    for row in rows[:100]:
        preview_lines.append(str(row))

    return "\n".join(preview_lines)


async def extract_business_data(file: UploadFile) -> dict[str, Any]:
    """
    Extract business data from CSV/XLSX and return AI-ready structured data.

    Return shape:
    {
        "raw_preview": str,
        "normalized_rows": list[dict],
        "columns": list[str],
        "column_mapping": dict[str, str],
        "numeric_columns": list[str],
        "date_columns": list[str],
        "row_count": int,
        "file_name": str
    }
    """

    filename = file.filename or ""
    raw = await file.read()

    rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []

    if filename.lower().endswith(".csv"):
        try:
            content = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            content = raw.decode("latin-1")

        reader = csv.DictReader(io.StringIO(content))
        fieldnames = [
            str(field or "").strip()
            for field in (reader.fieldnames or [])
        ]

        for row in reader:
            cleaned_row = {
                str(key or "").strip(): clean_cell(value)
                for key, value in row.items()
                if key is not None
            }

            # Keep only rows that have at least one non-empty value.
            if any(value not in ("", None) for value in cleaned_row.values()):
                rows.append(cleaned_row)

    elif filename.lower().endswith(".xlsx"):
        workbook = load_workbook(io.BytesIO(raw), data_only=True)
        sheet = workbook.active

        data = list(sheet.values)

        if not data:
            return {
                "raw_preview": "",
                "normalized_rows": [],
                "columns": [],
                "column_mapping": {},
                "numeric_columns": [],
                "date_columns": [],
                "row_count": 0,
                "file_name": filename,
            }

        fieldnames = [
            str(col or "").strip()
            for col in data[0]
        ]

        for row in data[1:]:
            row_dict = {
                fieldnames[i]: clean_cell(row[i]) if i < len(row) else ""
                for i in range(len(fieldnames))
                if fieldnames[i]
            }

            if any(value not in ("", None) for value in row_dict.values()):
                rows.append(row_dict)

    else:
        raise ValueError(
            "Only CSV or Excel (.xlsx) files are supported for Business Agent."
        )

    if not rows:
        return {
            "raw_preview": "",
            "normalized_rows": [],
            "columns": fieldnames,
            "column_mapping": {},
            "numeric_columns": [],
            "date_columns": [],
            "row_count": 0,
            "file_name": filename,
        }

    column_mapping = detect_kpi_columns(fieldnames)
    numeric_columns = detect_numeric_columns(rows, fieldnames)
    date_columns = detect_date_columns(rows, fieldnames)

    # Auto-fill mapping when strong detected helpers exist.
    if "date" not in column_mapping and date_columns:
        column_mapping["date"] = date_columns[0]

    raw_preview = build_preview(
        filename=filename,
        fieldnames=fieldnames,
        rows=rows,
        column_mapping=column_mapping,
        numeric_columns=numeric_columns,
        date_columns=date_columns,
    )

    return {
        "raw_preview": raw_preview,
        "normalized_rows": rows,
        "columns": fieldnames,
        "column_mapping": column_mapping,
        "numeric_columns": numeric_columns,
        "date_columns": date_columns,
        "row_count": len(rows),
        "file_name": filename,
    }
