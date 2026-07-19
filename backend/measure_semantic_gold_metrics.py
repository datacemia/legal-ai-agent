#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from collections import Counter, defaultdict
from pathlib import Path
from app.services.contract_agent.semantic_source_profile import build_semantic_source_profile, canonicalize_pipeline_type

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")

def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise RuntimeError(f"{path}:{line_number}: expected JSON object")
            rows.append(value)
    return rows

def names(mechanisms) -> set[str]:
    result = set()
    if not isinstance(mechanisms, list):
        return result
    for m in mechanisms:
        if isinstance(m, str):
            value = m.strip().upper()
        elif isinstance(m, dict):
            value = str(m.get("kind") or m.get("concept") or m.get("mechanism") or "").strip().upper()
        else:
            continue
        if value:
            result.add(value)
    return result

def ratio(n: int, d: int):
    return round(n / d, 6) if d > 0 else None

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("gold", type=Path)
    ap.add_argument("--out", type=Path, default=Path("semantic_gold/semantic_gold_metrics.json"))
    args = ap.parse_args()

    rows = read_jsonl(args.gold)
    approved = [r for r in rows if str(r.get("review_status") or "").strip().upper() == "APPROVED"]
    type_correct = type_total = tp = fp = fn = abstained = 0
    by_language = defaultdict(Counter)
    findings = []

    for row in approved:
        source = str(row.get("source_text") or "")
        language = str(row.get("language") or "")
        gold_type = canonicalize_pipeline_type(row.get("gold_primary_type"))
        profile = build_semantic_source_profile(source, language=language)
        predicted_type = "unknown" if profile.get("abstained") is True else canonicalize_pipeline_type(profile.get("primary_type"))

        if profile.get("abstained") is True:
            abstained += 1
            by_language[language]["abstained"] += 1

        if gold_type and gold_type != "unknown":
            type_total += 1
            by_language[language]["type_total"] += 1
            if predicted_type == gold_type:
                type_correct += 1
                by_language[language]["type_correct"] += 1

        predicted = names(profile.get("ranked_material_mechanisms"))
        gold = names(row.get("gold_material_mechanisms"))
        local_tp = len(predicted & gold)
        local_fp = len(predicted - gold)
        local_fn = len(gold - predicted)
        tp += local_tp; fp += local_fp; fn += local_fn
        by_language[language]["mechanism_tp"] += local_tp
        by_language[language]["mechanism_fp"] += local_fp
        by_language[language]["mechanism_fn"] += local_fn

        if predicted_type != gold_type or local_fp or local_fn:
            findings.append({
                "language": language,
                "document": row.get("document"),
                "reference": row.get("reference"),
                "source_text": source,
                "gold_primary_type": gold_type,
                "predicted_primary_type": predicted_type,
                "shadow_abstained": profile.get("abstained"),
                "gold_material_mechanisms": sorted(gold),
                "predicted_material_mechanisms": sorted(predicted),
                "false_positive_mechanisms": sorted(predicted - gold),
                "missing_mechanisms": sorted(gold - predicted),
            })

    summary = {
        "rows_total": len(rows),
        "approved_gold_rows": len(approved),
        "primary_type_accuracy": ratio(type_correct, type_total),
        "primary_type_correct": type_correct,
        "primary_type_total": type_total,
        "mechanism_precision": ratio(tp, tp + fp),
        "mechanism_recall": ratio(tp, tp + fn),
        "mechanism_tp": tp,
        "mechanism_fp": fp,
        "mechanism_fn": fn,
        "abstained_on_approved_gold": abstained,
        "by_language": {},
        "findings": findings,
    }
    for language, counts in sorted(by_language.items()):
        summary["by_language"][language] = {
            **dict(counts),
            "primary_type_accuracy": ratio(counts["type_correct"], counts["type_total"]),
            "mechanism_precision": ratio(counts["mechanism_tp"], counts["mechanism_tp"] + counts["mechanism_fp"]),
            "mechanism_recall": ratio(counts["mechanism_tp"], counts["mechanism_tp"] + counts["mechanism_fn"]),
        }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=" * 88)
    print("SEMANTIC GOLD METRICS")
    print("=" * 88)
    print("ROWS TOTAL:", summary["rows_total"])
    print("APPROVED GOLD ROWS:", summary["approved_gold_rows"])
    print("PRIMARY TYPE ACCURACY:", summary["primary_type_accuracy"])
    print("MECHANISM PRECISION:", summary["mechanism_precision"])
    print("MECHANISM RECALL:", summary["mechanism_recall"])
    print("ABSTAINED ON APPROVED GOLD:", summary["abstained_on_approved_gold"])
    print("\nBY LANGUAGE")
    for language, values in summary["by_language"].items():
        print(language.upper(), json.dumps(values, ensure_ascii=False))
    print("\nFINDINGS:", len(findings))
    print("REPORT:", args.out)
    if not approved:
        print("\nNO APPROVED GOLD ROWS. Metrics remain unavailable until human review.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
