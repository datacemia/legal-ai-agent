#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from app.services.contract_agent.semantic_source_profile import build_semantic_source_profile

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")

FIXTURE_RE = re.compile(r"^(?:0[1-9]|1[0-5])_.+?(?:_FR|_AR)?\.json$", re.I)

def exact_fixture_files(root: Path) -> list[Path]:
    files = []
    for language in ("en", "fr", "ar"):
        folder = root / language
        if not folder.is_dir():
            continue
        files.extend(
            p for p in sorted(folder.glob("*.json"))
            if not p.name.startswith("_") and FIXTURE_RE.match(p.name)
        )
    return files

def clause_results(payload: Any) -> list[dict]:
    clauses = payload.get("clauses") if isinstance(payload, dict) else None
    if isinstance(clauses, dict) and isinstance(clauses.get("results"), list):
        return [x for x in clauses["results"] if isinstance(x, dict)]
    return []

def exact_source(item: dict) -> str:
    return str(item.get("_source_text_exact") or item.get("original_text") or item.get("clause_text") or item.get("quoted_text") or "")

def source_language(path: Path) -> str:
    name = path.name.upper()
    return "fr" if "_FR" in name else "ar" if "_AR" in name else "en"

def reference(item: dict, index: int) -> str:
    return str(item.get("clause_reference") or item.get("reference") or item.get("clause_number") or item.get("number") or item.get("clause_id") or f"clause_{index}")

def mechanism_snapshot(profile: dict) -> list[dict]:
    out = []
    for m in profile.get("ranked_material_mechanisms") or []:
        if not isinstance(m, dict):
            continue
        out.append({
            "kind": m.get("kind"),
            "semantic_role": m.get("semantic_role"),
            "candidate_primary_type": m.get("candidate_primary_type"),
            "primary_eligible": m.get("primary_eligible"),
            "polarity": m.get("polarity"),
            "procedural_state": m.get("procedural_state"),
            "source_evidence": m.get("source_evidence") or [],
        })
    return out

def build_rows(root: Path):
    rows, errors = [], []
    for path in exact_fixture_files(root):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            lang = source_language(path)
            for index, item in enumerate(clause_results(payload), 1):
                source = exact_source(item)
                profile = build_semantic_source_profile(source, language=lang)
                rows.append({
                    "review_status": "PENDING",
                    "reviewer": "",
                    "review_notes": "",
                    "language": lang,
                    "document": path.name,
                    "reference": reference(item, index),
                    "title": item.get("title") or item.get("clause_title") or "",
                    "source_text": source,
                    "pipeline_primary_type": item.get("clause_type"),
                    "pipeline_confidence": item.get("confidence"),
                    "shadow_profile_version": profile.get("profile_version"),
                    "shadow_primary_type": profile.get("primary_type"),
                    "shadow_confidence": profile.get("confidence"),
                    "shadow_abstained": profile.get("abstained"),
                    "shadow_abstention_reason": profile.get("abstention_reason"),
                    "shadow_candidate_primary_type": profile.get("candidate_primary_type"),
                    "shadow_candidate_coverage": profile.get("candidate_coverage"),
                    "shadow_ranked_material_mechanisms": mechanism_snapshot(profile),
                    "gold_primary_type": "",
                    "gold_material_mechanisms": [],
                    "gold_actor_object_arguments": [],
                    "gold_polarity": [],
                    "gold_procedural_states": [],
                    "gold_numeric_semantic_roles": [],
                    "gold_source_evidence_spans": [],
                })
        except Exception as exc:
            errors.append({"file": str(path), "error": repr(exc)})
    return rows, errors

def select_review_set(rows: list[dict], per_type_language: int) -> list[dict]:
    buckets = defaultdict(list)
    for row in rows:
        buckets[(row["language"], str(row.get("pipeline_primary_type") or "unknown"))].append(row)
    selected, seen = [], set()
    for key in sorted(buckets):
        abstained = [r for r in buckets[key] if r.get("shadow_abstained") is True]
        for row in abstained[:per_type_language]:
            ident = (row["document"], row["reference"])
            if ident not in seen:
                selected.append(row); seen.add(ident)
    for key in sorted(buckets):
        for row in buckets[key]:
            ident = (row["document"], row["reference"])
            if ident not in seen:
                selected.append(row); seen.add(ident); break
    return selected

def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--out", type=Path, default=Path("semantic_gold"))
    ap.add_argument("--per-type-language", type=int, default=3)
    args = ap.parse_args()

    rows, errors = build_rows(args.input)
    args.out.mkdir(parents=True, exist_ok=True)
    review_rows = select_review_set(rows, max(1, args.per_type_language))

    full_path = args.out / "gold_all_355.jsonl"
    review_path = args.out / "gold_review_set.jsonl"
    summary_path = args.out / "gold_builder_summary.json"
    write_jsonl(full_path, rows)
    write_jsonl(review_path, review_rows)

    language_counts = Counter(r["language"] for r in rows)
    abstention_counts = Counter(r["language"] for r in rows if r.get("shadow_abstained") is True)
    pipeline_types = Counter(str(r.get("pipeline_primary_type") or "unknown") for r in rows)
    review_langs = Counter(r["language"] for r in review_rows)
    review_types = Counter(str(r.get("pipeline_primary_type") or "unknown") for r in review_rows)

    summary = {
        "exact_fixture_files": len(exact_fixture_files(args.input)),
        "clauses_total": len(rows),
        "file_errors": errors,
        "language_counts": dict(language_counts),
        "shadow_abstentions": sum(abstention_counts.values()),
        "shadow_abstentions_by_language": dict(abstention_counts),
        "pipeline_type_counts": dict(pipeline_types.most_common()),
        "review_set_size": len(review_rows),
        "review_set_language_counts": dict(review_langs),
        "review_set_type_counts": dict(review_types.most_common()),
        "gold_fields_are_human_only": True,
        "publication_gate_modified": False,
        "pipeline_modified": False,
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=" * 88)
    print("SEMANTIC GOLD CORPUS BUILDER")
    print("=" * 88)
    print("EXACT FIXTURE FILES:", summary["exact_fixture_files"])
    print("CLAUSES TOTAL:", summary["clauses_total"])
    print("FILE ERRORS:", len(errors))
    print("LANGUAGES:", summary["language_counts"])
    print("SHADOW ABSTENTIONS:", summary["shadow_abstentions"])
    print("ABSTENTIONS BY LANGUAGE:", summary["shadow_abstentions_by_language"])
    print("REVIEW SET SIZE:", summary["review_set_size"])
    print("REVIEW LANGUAGES:", summary["review_set_language_counts"])
    print("FULL GOLD TEMPLATE:", full_path)
    print("REVIEW GOLD TEMPLATE:", review_path)
    print("SUMMARY:", summary_path)
    print("\nTOP REVIEW TYPES")
    for clause_type, count in review_types.most_common(50):
        print(f"{count:4d}  {clause_type}")
    return 2 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
