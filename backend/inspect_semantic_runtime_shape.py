#!/usr/bin/env python3
"""Inventory the actual semantic runtime shape in the frozen 45-result corpus.

Read-only. No imports from contract_agent and no mutation of result files.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")

FIXTURE_RE = re.compile(
    r"^(?P<num>0[1-9]|1[0-5])_.+?(?P<lang>_FR|_AR)?\.json$",
    re.IGNORECASE,
)

SEMANTIC_KEY_TERMS = (
    "type",
    "mechan",
    "ground",
    "evidence",
    "semantic",
    "profile",
    "polarity",
    "state",
    "actor",
    "role",
    "trigger",
    "numeric",
    "confidence",
    "coverage",
    "obligation",
    "right",
)

def exact_fixture_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for lang in ("en", "fr", "ar"):
        folder = root / lang
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.json")):
            if path.name.startswith("_"):
                continue
            if FIXTURE_RE.match(path.name):
                files.append(path)
    return files

def clause_results(payload: Any) -> list[dict]:
    if not isinstance(payload, dict):
        return []
    clauses = payload.get("clauses")
    if isinstance(clauses, dict) and isinstance(clauses.get("results"), list):
        return [x for x in clauses["results"] if isinstance(x, dict)]
    return []

def walk_paths(obj: Any, prefix: str = ""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            yield path, value
            yield from walk_paths(value, path)
    elif isinstance(obj, list):
        for index, value in enumerate(obj[:5]):
            path = f"{prefix}[]"
            yield from walk_paths(value, path)

def is_semantic_path(path: str) -> bool:
    low = path.lower()
    return any(term in low for term in SEMANTIC_KEY_TERMS)

def compact_sample(value: Any, limit: int = 500) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        text = value if not isinstance(value, str) else value.replace("\n", " ")
        if isinstance(text, str) and len(text) > limit:
            return text[:limit] + "..."
        return text
    if isinstance(value, dict):
        return {k: compact_sample(v, 180) for k, v in list(value.items())[:12]}
    if isinstance(value, list):
        return [compact_sample(v, 180) for v in value[:5]]
    return repr(value)[:limit]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path, default=Path("regression_results_multilang"))
    ap.add_argument("--out", type=Path, default=Path("semantic_runtime_shape"))
    args = ap.parse_args()

    files = exact_fixture_files(args.input)
    args.out.mkdir(parents=True, exist_ok=True)

    path_counts: Counter[str] = Counter()
    path_types: defaultdict[str, Counter[str]] = defaultdict(Counter)
    path_samples: defaultdict[str, list[dict]] = defaultdict(list)
    top_level_clause_keys: Counter[str] = Counter()
    file_rows = []
    errors = []

    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            clauses = clause_results(payload)
            file_rows.append({"file": str(path), "clauses": len(clauses)})

            for clause_index, clause in enumerate(clauses, 1):
                for key in clause:
                    top_level_clause_keys[key] += 1

                for semantic_path, value in walk_paths(clause):
                    if not is_semantic_path(semantic_path):
                        continue

                    path_counts[semantic_path] += 1
                    path_types[semantic_path][type(value).__name__] += 1

                    samples = path_samples[semantic_path]
                    if len(samples) < 3:
                        samples.append({
                            "file": path.name,
                            "clause_index": clause_index,
                            "value": compact_sample(value),
                        })
        except Exception as exc:
            errors.append({"file": str(path), "error": repr(exc)})

    inventory = []
    for semantic_path, count in path_counts.most_common():
        inventory.append({
            "path": semantic_path,
            "occurrences": count,
            "types": dict(path_types[semantic_path]),
            "samples": path_samples[semantic_path],
        })

    report = {
        "exact_fixture_files": len(files),
        "file_errors": errors,
        "files": file_rows,
        "top_level_clause_keys": dict(top_level_clause_keys.most_common()),
        "semantic_paths": inventory,
    }

    report_path = args.out / "semantic_runtime_shape.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=" * 88)
    print("SEMANTIC RUNTIME SHAPE INVENTORY")
    print("=" * 88)
    print("EXACT FIXTURE FILES:", len(files))
    print("FILE ERRORS:", len(errors))
    print("SEMANTIC PATHS:", len(inventory))
    print("REPORT:", report_path)

    print("\nTOP-LEVEL CLAUSE KEYS")
    for key, count in top_level_clause_keys.most_common():
        if any(term in key.lower() for term in SEMANTIC_KEY_TERMS):
            print(f"{count:4d}  {key}")

    print("\nSEMANTIC PATHS")
    for row in inventory[:120]:
        print(f"{row['occurrences']:4d}  {row['path']}  types={row['types']}")
        for sample in row["samples"][:1]:
            value = json.dumps(sample["value"], ensure_ascii=False)
            print(
                f"      sample={sample['file']}#{sample['clause_index']} "
                f"value={value[:500]}"
            )

    return 2 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
