import csv
import io
from fastapi import UploadFile

from openpyxl import load_workbook


async def extract_business_data(file: UploadFile) -> str:
    filename = file.filename or ""
    raw = await file.read()

    rows = []
    fieldnames = []

    # ✅ CSV SUPPORT
    if filename.lower().endswith(".csv"):
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            content = raw.decode("latin-1")

        reader = csv.DictReader(io.StringIO(content))
        fieldnames = reader.fieldnames or []

        for row in reader:
            rows.append(row)

    # ✅ EXCEL SUPPORT (.xlsx)
    elif filename.lower().endswith(".xlsx"):
        workbook = load_workbook(io.BytesIO(raw))
        sheet = workbook.active

        data = list(sheet.values)

        if not data:
            return ""

        fieldnames = [str(col) for col in data[0]]

        for row in data[1:]:
            row_dict = {
                fieldnames[i]: row[i] if i < len(row) else None
                for i in range(len(fieldnames))
            }
            rows.append(row_dict)

    else:
        raise ValueError(
            "Only CSV or Excel (.xlsx) files are supported for Business Agent."
        )

    if not rows:
        return ""

    preview_lines = []
    preview_lines.append("Business data preview:")
    preview_lines.append(f"Columns: {', '.join(fieldnames)}")
    preview_lines.append(f"Rows count: {len(rows)}")
    preview_lines.append("")
    preview_lines.append("Sample rows:")

    for row in rows[:100]:
        preview_lines.append(str(row))

    return "\n".join(preview_lines)