import json
from pathlib import Path


def load_failures(directory: str):
    path = Path(directory) / "semantic_gold_failures.json"

    if not path.exists():
        candidates = list(Path(directory).glob("*failure*.json"))
        if not candidates:
            raise SystemExit(
                f"No failure JSON found in {directory}"
            )
        path = candidates[0]

    data = json.loads(path.read_text(encoding="utf-8"))

    rows = data if isinstance(data, list) else (
        data.get("failures")
        or data.get("rows")
        or data.get("clauses")
        or []
    )

    normalized = {}

    for row in rows:
        fixture = (
            row.get("fixture_id")
            or row.get("id")
            or row.get("clause_id")
            or "UNKNOWN"
        )
        language = row.get("language") or row.get("lang") or "UNKNOWN"

        critical = tuple(sorted(
            row.get("critical")
            or row.get("critical_failures")
            or []
        ))

        high = tuple(sorted(
            row.get("high")
            or row.get("high_failures")
            or []
        ))

        normalized[(fixture, language)] = {
            "critical": critical,
            "high": high,
        }

    return path, normalized


BASELINE = "semantic_audit_final"
CURRENT = "semantic_audit_lot7b1"

base_path, base = load_failures(BASELINE)
current_path, current = load_failures(CURRENT)

print("BASELINE:", base_path)
print("CURRENT :", current_path)
print()

keys = sorted(set(base) | set(current))

new_critical = []
resolved_critical = []
new_high = []
resolved_high = []

for key in keys:
    old = base.get(key, {"critical": (), "high": ()})
    new = current.get(key, {"critical": (), "high": ()})

    old_critical = set(old["critical"])
    new_critical_set = set(new["critical"])
    old_high = set(old["high"])
    new_high_set = set(new["high"])

    for failure in sorted(new_critical_set - old_critical):
        new_critical.append((*key, failure))

    for failure in sorted(old_critical - new_critical_set):
        resolved_critical.append((*key, failure))

    for failure in sorted(new_high_set - old_high):
        new_high.append((*key, failure))

    for failure in sorted(old_high - new_high_set):
        resolved_high.append((*key, failure))


def show(title, rows):
    print("=" * 100)
    print(title, len(rows))
    print("=" * 100)

    for fixture, language, failure in rows:
        print(f"{fixture} [{language}] {failure}")

    print()


show("NEW CRITICAL", new_critical)
show("RESOLVED CRITICAL", resolved_critical)
show("NEW HIGH", new_high)
show("RESOLVED HIGH", resolved_high)
