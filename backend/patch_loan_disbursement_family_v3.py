from pathlib import Path
import shutil


PATH = Path(
    "app/services/contract_agent/"
    "semantic_source_profile.py"
)

BACKUP = PATH.with_suffix(
    ".py.before_loan_disbursement_family_v3"
)

source = PATH.read_text(encoding="utf-8")

start_marker = '"LOAN_PRINCIPAL_DISBURSEMENT"'
end_marker = '"ACCELERATION_ON_DEFAULT"'

start = source.find(start_marker)
end = source.find(end_marker, start)

if start < 0 or end < 0:
    raise SystemExit(
        "ERROR: loan disbursement family not found"
    )

block = source[start:end]
original_block = block

replacements = [
    # FR: "mis à disposition" and "mis à la disposition".
    (
        r"mis(?:es)?\s+[àa]\s+disposition",
        r"mis(?:es)?\s+[àa]\s+(?:la\s+)?disposition",
    ),

    # FR: infinitive and conjugated forms of transférer.
    (
        r"transf[eè]re(?:ra|nt)?",
        (
            r"transf[eéè]r(?:er|e|es|ent|era|eront|"
            r"ait|aient|é|ée|és|ées)"
        ),
    ),

    # AR: definite and indefinite nominal forms.
    (
        (
            r"(?:الأموال|المبلغ|المبالغ|"
            r"الحصيلة|العائدات)"
        ),
        (
            r"(?:(?:ال)?أموال|(?:ال)?مبلغ|"
            r"(?:ال)?مبالغ|(?:ال)?حصيلة|"
            r"(?:ال)?عائدات)"
        ),
    ),
]

applied = []

for old, new in replacements:
    count = block.count(old)

    if count == 0:
        print("NOT FOUND:", old)
        continue

    block = block.replace(old, new)
    applied.append((old, count))

if block == original_block:
    raise SystemExit(
        "ERROR: no replacements applied; "
        "inspect the current detector block"
    )

shutil.copy2(PATH, BACKUP)

updated = source[:start] + block + source[end:]
PATH.write_text(updated, encoding="utf-8")

print("PATCH STATUS: APPLIED")
print("BACKUP:", BACKUP)

for expression, count in applied:
    print(f"REPLACED {count}x:", expression)
