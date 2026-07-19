import json
from pathlib import Path

BASE = Path("semantic_audit_final")
NEW = Path("semantic_audit_lot7b1")


def load(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    d = {}
    for r in rows:
        key = (r["fixture_id"], r["language"])
        d[key] = r
    return d


for name in [
    "semantic_gold_critical_failures.json",
    "semantic_gold_high_failures.json",
]:
    print("\n" + "=" * 100)
    print(name)
    print("=" * 100)

    old = load(BASE / name)
    new = load(NEW / name)

    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    common = sorted(set(old) & set(new))

    print(f"Added   : {len(added)}")
    print(f"Removed : {len(removed)}")

    if added:
        print("\n--- NEW FAILURES ---")
        for k in added:
            print(k)
            print(json.dumps(new[k], ensure_ascii=False, indent=2))

    changed = 0
    for k in common:
        if old[k] != new[k]:
            changed += 1

    print(f"\nChanged existing failures: {changed}")
