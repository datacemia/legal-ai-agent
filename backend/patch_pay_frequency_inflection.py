from pathlib import Path
import shutil


PATH = Path(
    "app/services/contract_agent/"
    "semantic_source_profile.py"
)

BACKUP = PATH.with_suffix(
    ".py.before_pay_frequency_inflection"
)

source = PATH.read_text(encoding="utf-8")

start_marker = '"PAY_FREQUENCY"'
start = source.find(start_marker)

if start < 0:
    raise SystemExit(
        "ERROR: PAY_FREQUENCY family not found"
    )

next_rule = source.find("\n    _r(", start + len(start_marker))

if next_rule < 0:
    raise SystemExit(
        "ERROR: next semantic rule not found"
    )

block = source[start:next_rule]
original_block = block

# "payables?" matches:
# - English payable
# - French payable
# - French payables
#
# Avoid replacing a token already made plural-aware.
block = block.replace(
    r"\bpayable\b",
    r"\bpayables?\b",
)

block = block.replace(
    r"payable\s+mensuellement",
    r"payables?\s+mensuellement",
)

block = block.replace(
    r"payable.{0,",
    r"payables?.{0,",
)

if block == original_block:
    raise SystemExit(
        "ERROR: no PAY_FREQUENCY payable expression "
        "was found. Print the family block before editing."
    )

shutil.copy2(PATH, BACKUP)

updated = source[:start] + block + source[next_rule:]
PATH.write_text(updated, encoding="utf-8")

print("PATCH STATUS: APPLIED")
print("BACKUP:", BACKUP)
