#!/usr/bin/env python3
"""Inspect V4.1.2a liability abstentions. Read-only."""
from __future__ import annotations
import json, re, sys
from collections import Counter
from pathlib import Path
from app.services.contract_agent.semantic_source_profile import build_semantic_source_profile

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")

DETAILS = Path("semantic_profile_shadow_v4_1_2a/shadow_details.json")
TARGETS = {"liability", "limitation_of_liability"}
SIGNALS = {
    "en": {
        "LIABILITY_CAP": (r"\bliability\b.{0,180}\b(?:shall not exceed|limited to|cap(?:ped)?)\b", r"\baggregate liability\b"),
        "EXCLUDED_DAMAGES": (r"\b(?:indirect|incidental|special|consequential|punitive)\s+damages\b", r"\blost profits?\b"),
        "CARVE_OUT": (r"\bexcept(?:ion)?\b", r"\bshall not apply\b", r"\bexcluding\b"),
        "SUPER_CAP": (r"\btwo times\b", r"\b2x\b", r"\bdouble\b.{0,60}\bcap\b"),
        "AGGREGATE_PERIOD": (r"\b(?:preceding|prior)\s+(?:twelve|12)\s+months?\b", r"\bin the aggregate\b"),
    },
    "fr": {
        "LIABILITY_CAP": (r"\bresponsabilit[eé]\b.{0,180}\b(?:ne pourra exc[eé]der|limit[eé]e? à|plafond)\b", r"\bresponsabilit[eé] globale\b"),
        "EXCLUDED_DAMAGES": (r"\bdommages?\s+(?:indirects?|accessoires?|sp[eé]ciaux?|cons[eé]cutifs?|punitifs?)\b", r"\bmanque à gagner\b"),
        "CARVE_OUT": (r"\bsauf\b", r"\bne s['’]applique pas\b", r"\bà l['’]exception\b"),
        "SUPER_CAP": (r"\bdeux fois\b", r"\b2x\b", r"\bdouble\b.{0,60}\bplafond\b"),
        "AGGREGATE_PERIOD": (r"\b(?:douze|12)\s+mois pr[eé]c[eé]dents?\b", r"\bau total\b", r"\bglobale\b"),
    },
    "ar": {
        "LIABILITY_CAP": (r"المسؤولية.{0,180}(?:لا تتجاوز|محدودة|حد أقصى|سقف)", r"إجمالي المسؤولية"),
        "EXCLUDED_DAMAGES": (r"أضرار.{0,80}(?:غير مباشرة|عرضية|خاصة|تبعية|عقابية)", r"الأرباح الفائتة|خسارة الأرباح"),
        "CARVE_OUT": (r"باستثناء", r"لا ينطبق", r"فيما عدا"),
        "SUPER_CAP": (r"ضعف", r"مرتين", r"2x", r"سقف.{0,60}مضاعف"),
        "AGGREGATE_PERIOD": (r"(?:اثني عشر|اثنا عشر|12).{0,30}(?:شهراً|شهرًا)", r"في المجمل|الإجمالية"),
    },
}

def labels(text, language):
    return [
        label for label, patterns in SIGNALS.get(language, {}).items()
        if any(re.search(p, text, re.I | re.S) for p in patterns)
    ]

def main():
    if not DETAILS.exists():
        raise SystemExit(f"Missing {DETAILS}. Run V4.1.2a shadow first.")
    rows = json.loads(DETAILS.read_text(encoding="utf-8"))
    selected = [
        r for r in rows
        if r.get("type_verdict") == "ABSTAINED"
        and str(r.get("pipeline_clause_type") or "").strip().lower() in TARGETS
    ]
    selected.sort(key=lambda r: (str(r.get("language") or ""), str(r.get("document") or ""), str(r.get("reference") or "")))
    langs, types, reasons, signals = Counter(), Counter(), Counter(), Counter()
    no_signal = 0

    print("=" * 100)
    print("V4.1.2a LIABILITY ABSTENTION FORENSICS")
    print("=" * 100)
    print("ROWS:", len(selected))

    for i, row in enumerate(selected, 1):
        lang = str(row.get("language") or "unknown").lower()
        source = str(row.get("source_text") or "")
        profile = build_semantic_source_profile(source, language=lang)
        found = labels(source, lang)
        langs[lang] += 1
        types[str(row.get("pipeline_clause_type") or "")] += 1
        reasons[str(profile.get("abstention_reason") or "NONE")] += 1
        signals.update(found)
        no_signal += not found

        print("\n" + "#" * 100)
        print(f"[{i}/{len(selected)}]")
        print("LANG:", lang)
        print("DOC:", row.get("document"))
        print("REF:", row.get("reference"))
        print("PIPELINE:", row.get("pipeline_clause_type"))
        print("PROFILE VERSION:", profile.get("profile_version"))
        print("PRIMARY:", profile.get("primary_type"))
        print("ABSTAIN REASON:", profile.get("abstention_reason"))
        print("CANDIDATE:", profile.get("candidate_primary_type"))
        print("COVERAGE:", profile.get("candidate_coverage"))
        print("SIGNALS:", found)
        print("SOURCE:")
        print(source)
        print("RANKED MECHANISMS:")
        for m in profile.get("ranked_material_mechanisms") or []:
            print("-", m.get("kind"), "| role=", m.get("semantic_role"), "| primary=", m.get("candidate_primary_type"), "| eligible=", m.get("primary_eligible"), "| rank=", m.get("rank"))
            for evidence in m.get("source_evidence") or []:
                print("  EVIDENCE:", repr(evidence.get("text")))

    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print("ROWS:", len(selected))
    print("BY LANGUAGE:", dict(langs))
    print("BY PIPELINE TYPE:", dict(types))
    print("ABSTENTION REASONS:", dict(reasons))
    print("SIGNAL COUNTS:", dict(signals))
    print("NO SIGNAL ROWS:", no_signal)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
