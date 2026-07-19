from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path("semantic_audit_final")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[SKIP] {path}: {exc}")
        return None


def walk(
    value: Any,
    *,
    path: str = "$",
    results: list[dict[str, Any]],
    file_path: Path,
) -> None:
    if isinstance(value, list):
        sample_keys: list[str] | None = None

        if value and isinstance(value[0], dict):
            sample_keys = sorted(value[0].keys())

        results.append(
            {
                "file": str(file_path),
                "json_path": path,
                "type": "list",
                "count": len(value),
                "sample_keys": sample_keys,
            }
        )

        for index, child in enumerate(value[:5]):
            walk(
                child,
                path=f"{path}[{index}]",
                results=results,
                file_path=file_path,
            )

    elif isinstance(value, dict):
        results.append(
            {
                "file": str(file_path),
                "json_path": path,
                "type": "dict",
                "count": len(value),
                "keys": sorted(value.keys()),
            }
        )

        for key, child in value.items():
            walk(
                child,
                path=f"{path}.{key}",
                results=results,
                file_path=file_path,
            )


def looks_relevant(item: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(item.get("json_path", "")),
            " ".join(item.get("sample_keys") or []),
            " ".join(item.get("keys") or []),
        ]
    ).lower()

    signals = (
        "clause",
        "source_text",
        "primary_type",
        "mechanism",
        "grounding",
        "review",
        "mismatch",
        "partial",
        "fixture",
        "language",
        "semantic",
        "candidate",
    )

    return any(signal in text for signal in signals)


def main() -> int:
    if not ROOT.exists():
        raise SystemExit(
            f"ABORT: directory not found: {ROOT}"
        )

    json_files = sorted(ROOT.rglob("*.json"))

    if not json_files:
        raise SystemExit(
            f"ABORT: no JSON files found in {ROOT}"
        )

    inventory: list[dict[str, Any]] = []

    for file_path in json_files:
        payload = load_json(file_path)

        if payload is None:
            continue

        walk(
            payload,
            path="$",
            results=inventory,
            file_path=file_path,
        )

    relevant = [
        item
        for item in inventory
        if looks_relevant(item)
    ]

    output = {
        "root": str(ROOT),
        "json_files_scanned": len(json_files),
        "all_nodes": len(inventory),
        "relevant_nodes": relevant,
    }

    Path("semantic_audit_schema_inventory.json").write_text(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 100)
    print("SEMANTIC AUDIT SCHEMA INVENTORY")
    print("=" * 100)
    print("FILES:", len(json_files))
    print("RELEVANT NODES:", len(relevant))
    print()

    for item in relevant:
        print("-" * 100)
        print("FILE:", item["file"])
        print("PATH:", item["json_path"])
        print("TYPE:", item["type"])
        print("COUNT:", item.get("count"))

        if item.get("sample_keys"):
            print(
                "SAMPLE KEYS:",
                ", ".join(item["sample_keys"]),
            )

        if item.get("keys"):
            print(
                "KEYS:",
                ", ".join(item["keys"][:30]),
            )

    print()
    print(
        "WRITTEN: semantic_audit_schema_inventory.json"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
