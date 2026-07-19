from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


TARGET_TERMS = (
    "review_required",
    "partial_extraction",
    "primary_type_mismatch",
)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[SKIP] {path}: {exc}")
        return None


def walk(
    value: Any,
    *,
    json_path: str = "$",
) -> list[tuple[str, Any]]:
    matches: list[tuple[str, Any]] = []

    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{json_path}.{key}"

            normalized_key = key.lower()

            if any(
                term in normalized_key
                for term in TARGET_TERMS
            ):
                matches.append((child_path, child))

            matches.extend(
                walk(
                    child,
                    json_path=child_path,
                )
            )

    elif isinstance(value, list):
        for index, child in enumerate(value):
            matches.extend(
                walk(
                    child,
                    json_path=f"{json_path}[{index}]",
                )
            )

    return matches


def describe(value: Any) -> dict[str, Any]:
    result: dict[str, Any] = {
        "type": type(value).__name__,
    }

    if isinstance(value, list):
        result["count"] = len(value)

        if value:
            first = value[0]

            if isinstance(first, dict):
                result["sample_keys"] = sorted(first.keys())
                result["sample"] = first
            else:
                result["sample"] = first

    elif isinstance(value, dict):
        result["count"] = len(value)
        result["keys"] = sorted(value.keys())

    else:
        result["value"] = value

    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect semantic-audit JSON files and locate "
            "gold-review candidate collections."
        )
    )

    parser.add_argument(
        "audit_dir",
        nargs="?",
        default="semantic_audit_final",
        help="Semantic audit output directory.",
    )

    parser.add_argument(
        "--out",
        default="gold_review_source_inventory.json",
        help="Inventory output JSON file.",
    )

    args = parser.parse_args()

    audit_dir = Path(args.audit_dir)
    output_path = Path(args.out)

    if not audit_dir.exists():
        print(f"ABORT: directory not found: {audit_dir}")
        return 1

    json_files = sorted(audit_dir.rglob("*.json"))

    if not json_files:
        print(f"ABORT: no JSON files found in {audit_dir}")
        return 1

    inventory: dict[str, Any] = {
        "audit_directory": str(audit_dir),
        "json_files_scanned": len(json_files),
        "matches": [],
    }

    for path in json_files:
        payload = load_json(path)

        if payload is None:
            continue

        for json_path, value in walk(payload):
            inventory["matches"].append(
                {
                    "file": str(path),
                    "json_path": json_path,
                    "description": describe(value),
                }
            )

    output_path.write_text(
        json.dumps(
            inventory,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 80)
    print("GOLD REVIEW SOURCE INVENTORY")
    print("=" * 80)
    print("AUDIT DIRECTORY:", audit_dir)
    print("JSON FILES SCANNED:", len(json_files))
    print("MATCHES:", len(inventory["matches"]))
    print()

    for index, match in enumerate(
        inventory["matches"],
        start=1,
    ):
        description = match["description"]

        print(f"[{index}]")
        print("FILE:", match["file"])
        print("JSON PATH:", match["json_path"])
        print("TYPE:", description.get("type"))

        if "count" in description:
            print("COUNT:", description["count"])

        if "value" in description:
            print("VALUE:", description["value"])

        if description.get("sample_keys"):
            print(
                "SAMPLE KEYS:",
                ", ".join(description["sample_keys"]),
            )

        print()

    print("INVENTORY WRITTEN:", output_path)

    if not inventory["matches"]:
        print()
        print(
            "No matching collections found. "
            "The detailed candidates may use different names "
            "or be stored outside the selected audit directory."
        )
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
