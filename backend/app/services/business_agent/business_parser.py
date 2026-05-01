import csv
import io
import re
from typing import Any

from fastapi import UploadFile
from openpyxl import load_workbook


COLUMN_ALIASES = {
    "date": [
        "date",
        "day",
        "transaction_date",
        "created_at",
        "created",
        "time",
        "month",
        "period",
    ],
    "revenue": [
        "revenue",
        "sales",
        "sale",
        "income",
        "turnover",
        "amount_in",
        "credit",
        "credits",
        "payment_received",
        "received",
        "gross_sales",
        "net_sales",
        "total_sales",
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
    ],
}


def normalize_column_name(name: Any) -> str:
    value = str(name or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def detect_column_mapping(fieldnames: list[str]) -> dict[str, str]:
    normalized_fields = {
        normalize_column_name(field): field for field in fieldnames if field
    }

    mapping: dict[str, str] = {}

    for target, aliases in COLUMN_ALIASES.items():
        normalized_aliases = [normalize_column_name(alias) for alias in aliases]

        for normalized_field, original_field in normalized_fields.items():
            if normalized_field in normalized_aliases:
                mapping[target] = original_field
                break

        if target not in mapping:
            for normalized_field, original_field in normalized_fields.items():
                if any(alias in normalized_field for alias in normalized_aliases):
                    mapping[target] = original_field
                    break

    return mapping


def clean_cell(value: Any) -> Any:
    if value is None:
        return ""

    return value


async def extract_business_data(file: UploadFile) -> str:
    filename = file.filename or ""
    raw = await file.read()

    rows = []
    fieldnames = []

    if filename.lower().endswith(".csv"):
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            content = raw.decode("latin-1")

        reader = csv.DictReader(io.StringIO(content))
        fieldnames = reader.fieldnames or []

        for row in reader:
            rows.append({key: clean_cell(value) for key, value in row.items()})

    elif filename.lower().endswith(".xlsx"):
        workbook = load_workbook(io.BytesIO(raw), data_only=True)
        sheet = workbook.active

        data = list(sheet.values)

        if not data:
            return ""

        fieldnames = [str(col or "").strip() for col in data[0]]

        for row in data[1:]:
            row_dict = {
                fieldnames[i]: clean_cell(row[i]) if i < len(row) else ""
                for i in range(len(fieldnames))
            }
            rows.append(row_dict)

    else:
        raise ValueError(
            "Only CSV or Excel (.xlsx) files are supported for Business Agent."
        )

    if not rows:
        return ""

    column_mapping = detect_column_mapping(fieldnames)

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
        preview_lines.append("No obvious mapping detected. Infer carefully from column names and sample rows.")

    preview_lines.append("")
    preview_lines.append("Sample rows:")

    for row in rows[:100]:
        preview_lines.append(str(row))

    return "\n".join(preview_lines)