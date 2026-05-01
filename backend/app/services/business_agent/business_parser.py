import csv
import io
from fastapi import UploadFile


async def extract_business_data(file: UploadFile) -> str:
    filename = file.filename or ""

    if not filename.lower().endswith(".csv"):
        raise ValueError("Only CSV files are supported for Business Agent V1.")

    raw = await file.read()

    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError:
        content = raw.decode("latin-1")

    rows = []
    reader = csv.DictReader(io.StringIO(content))

    for row in reader:
        rows.append(row)

    if not rows:
        return ""

    preview_lines = []
    preview_lines.append("Business data CSV preview:")
    preview_lines.append(f"Columns: {', '.join(reader.fieldnames or [])}")
    preview_lines.append(f"Rows count: {len(rows)}")
    preview_lines.append("")
    preview_lines.append("Sample rows:")

    for row in rows[:100]:
        preview_lines.append(str(row))

    return "\n".join(preview_lines)