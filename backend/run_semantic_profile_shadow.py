#!/usr/bin/env python3
"""Run semantic_source_profile.py in shadow mode over the exact 45 fixtures."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from app.services.contract_agent.semantic_source_profile import (
    UNKNOWN,
    build_semantic_source_profile,
    canonicalize_pipeline_type,
)

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")

FIXTURE_RE = re.compile(r"^(?:0[1-9]|1[0-5])_.+?(?:_FR|_AR)?\.json$", re.I)


def exact_files(root: Path) -> list[Path]:
    files = []
    for lang in ("en", "fr", "ar"):
        folder = root / lang
        if folder.is_dir():
            files.extend(
                path for path in sorted(folder.glob("*.json"))
                if not path.name.startswith("_") and FIXTURE_RE.match(path.name)
            )
    return files


def results(payload):
    clauses = payload.get("clauses") if isinstance(payload, dict) else None
    if isinstance(clauses, dict) and isinstance(clauses.get("results"), list):
        return [x for x in clauses["results"] if isinstance(x, dict)]
    return []


def source(item):
    return str(
        item.get("_source_text_exact")
        or item.get("original_text")
        or item.get("clause_text")
        or item.get("quoted_text")
        or ""
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--out", type=Path, default=Path("semantic_profile_shadow"))
    args = ap.parse_args()

    files = exact_files(args.input)
    args.out.mkdir(parents=True, exist_ok=True)

    rows = []
    errors = []
    language_counts = Counter()
    verdicts = Counter()
    mechanism_counts = Counter()
    abstention_reasons = Counter()

    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            for index, item in enumerate(results(payload), 1):
                text = source(item)
                profile = build_semantic_source_profile(text)
                language_counts[profile["source_language"]] += 1

                for mechanism in profile["ranked_material_mechanisms"]:
                    mechanism_counts[mechanism["kind"]] += 1

                actual = canonicalize_pipeline_type(item.get("clause_type"))
                shadow = canonicalize_pipeline_type(profile["primary_type"])

                if profile["primary_type"] == UNKNOWN:
                    verdict = "ABSTAINED"
                    abstention_reasons[
                        profile.get("abstention_reason") or "UNSPECIFIED"
                    ] += 1
                elif actual == shadow:
                    verdict = "MATCH"
                else:
                    verdict = "DIVERGENCE"
                verdicts[verdict] += 1

                evidence_errors = []
                for mechanism in profile["ranked_material_mechanisms"]:
                    spans = mechanism.get("source_evidence") or []
                    if not spans:
                        evidence_errors.append(f"{mechanism['kind']}:NO_EVIDENCE")
                    for span in spans:
                        if text[span["start"]:span["end"]] != span["text"]:
                            evidence_errors.append(f"{mechanism['kind']}:SPAN_MISMATCH")

                rows.append({
                    "language": profile["source_language"],
                    "document": path.name,
                    "reference": (
                        item.get("reference")
                        or item.get("clause_number")
                        or item.get("number")
                        or f"clause_{index}"
                    ),
                    "source_text": text,
                    "pipeline_clause_type": item.get("clause_type"),
                    "semantic_profile_version": profile.get("profile_version"),
                    "shadow_primary_type": profile["primary_type"],
                    "shadow_primary_type_confidence": profile["confidence"],
                    "shadow_abstained": profile["abstained"],
                    "shadow_abstention_reason": profile.get("abstention_reason"),
                    "shadow_candidate_primary_type": profile.get(
                        "candidate_primary_type"
                    ),
                    "shadow_candidate_coverage": profile.get(
                        "candidate_coverage"
                    ),
                    "shadow_primary_evidence_coverage": profile.get(
                        "primary_evidence_coverage"
                    ),
                    "shadow_dominance_margin": profile.get(
                        "dominance_margin"
                    ),
                    "shadow_candidate_margin": profile.get(
                        "candidate_margin"
                    ),
                    "shadow_dominance_scores": profile.get(
                        "dominance_scores"
                    ) or [],
                    "shadow_supporting_mechanisms": profile.get(
                        "supporting_mechanisms"
                    ) or [],
                    "extracted_mechanisms": profile["extracted_mechanisms"],
                    "grounded_mechanisms": profile["grounded_mechanisms"],
                    "ranked_material_mechanisms": profile[
                        "ranked_material_mechanisms"
                    ],
                    "semantic_profile_hash": profile["semantic_profile_hash"],
                    "type_verdict": verdict,
                    "evidence_errors": evidence_errors,
                })
        except Exception as exc:
            errors.append({"file": str(path), "error": repr(exc)})

    evidence_failures = [row for row in rows if row["evidence_errors"]]
    divergences = [
        row for row in rows if row["type_verdict"] == "DIVERGENCE"
    ]

    summary = {
        "exact_fixture_files": len(files),
        "clauses_audited": len(rows),
        "file_errors": errors,
        "language_counts": dict(language_counts),
        "type_verdicts": dict(verdicts),
        "abstention_reasons": dict(abstention_reasons),
        "ranked_mechanism_counts": dict(mechanism_counts),
        "evidence_integrity_failures": len(evidence_failures),
        "type_divergences": len(divergences),
        "publication_gate_modified": False,
        "publication_baseline_asserted_here": False,
        "note": (
            "Shadow audit only. Divergence is a review candidate, "
            "not automatically a pipeline defect."
        ),
    }

    (args.out / "shadow_details.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (args.out / "shadow_divergences.json").write_text(
        json.dumps(divergences, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (args.out / "shadow_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=" * 88)
    print("SEMANTIC SOURCE PROFILE — SHADOW AUDIT")
    print("=" * 88)
    print("EXACT FIXTURE FILES:", len(files))
    print("CLAUSES AUDITED:", len(rows))
    print("FILE ERRORS:", len(errors))
    print("LANGUAGES:", dict(language_counts))
    print("TYPE VERDICTS:", dict(verdicts))
    print("ABSTENTION REASONS:", dict(abstention_reasons))
    print("EVIDENCE INTEGRITY FAILURES:", len(evidence_failures))
    print("TYPE DIVERGENCES:", len(divergences))
    print("RANKED MECHANISMS:", dict(mechanism_counts))
    print("SUMMARY:", args.out / "shadow_summary.json")

    print("\nTOP TYPE DIVERGENCES")
    for row in divergences[:50]:
        print(
            f"{row['language'].upper()} | {row['document']} | "
            f"{row['reference']} | "
            f"pipeline={row['pipeline_clause_type']} | "
            f"shadow={row['shadow_primary_type']} | "
            f"mechanisms="
            f"{[m['kind'] for m in row['ranked_material_mechanisms']]}"
        )

    return 2 if errors or evidence_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
