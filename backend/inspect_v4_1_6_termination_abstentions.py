#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from collections import Counter
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")

DETAILS = Path("semantic_profile_shadow_v4_1_6_payment_after_pipeline/shadow_details.json")
TARGETS = {"termination","termination_for_cause","termination_for_convenience","term_and_termination"}

SIGNALS = {
    "TERMINATION_RIGHT": [r"\b(?:may|shall have the right to)\s+terminate\b", r"\b(?:peut|a le droit de)\s+r[eé]silier\b", r"(?:يجوز|له|لها).{0,50}(?:فسخ|إنهاء)"],
    "TERMINATION_FOR_CAUSE": [r"\bterminate\b.{0,180}\b(?:material breach|breach|default|cause)\b", r"\br[eé]silier\b.{0,180}\b(?:manquement grave|manquement|d[eé]faut|faute)\b", r"(?:فسخ|إنهاء).{0,180}(?:إخلال جوهري|إخلال|تخلف|سبب)"],
    "TERMINATION_FOR_CONVENIENCE": [r"\bterminate\b.{0,160}\b(?:for convenience|without cause|at any time)\b", r"\br[eé]silier\b.{0,160}\b(?:pour convenance|sans motif|[aà] tout moment)\b", r"(?:فسخ|إنهاء).{0,160}(?:للملاءمة|دون سبب|في أي وقت)"],
    "NOTICE_PERIOD": [r"\b(?:upon|on)\s+\w+(?:\s+\(\d+\))?\s+days?['’]?\s+(?:prior\s+)?written notice\b", r"\bmoyennant\s+un\s+pr[eé]avis\s+[eé]crit\s+de\s+\w+(?:\s+\(\d+\))?\s+jours?\b", r"(?:بإشعار خطي مسبق|بموجب إشعار خطي).{0,80}(?:يوماً|يومًا|يوما|يوم)"],
    "CURE_PERIOD": [r"\b(?:cure|remedy)\b.{0,120}\bwithin\b.{0,60}\bdays?\b", r"\b(?:rem[eé]dier|corriger)\b.{0,120}\bdans\s+un\s+d[eé]lai\b.{0,60}\bjours?\b", r"(?:معالجة|تصحيح|تدارك).{0,120}(?:خلال|في غضون).{0,60}(?:يوماً|يومًا|يوما|يوم)"],
    "IMMEDIATE_TERMINATION": [r"\bterminate\s+immediately\b", r"\br[eé]silier\s+imm[eé]diatement\b", r"(?:فسخ|إنهاء).{0,30}(?:فوراً|فورًا|على الفور)"],
    "INSOLVENCY_TRIGGER": [r"\b(?:insolven|bankrupt|bankruptcy|receivership|liquidation)\w*\b", r"\b(?:insolvabilit[eé]|faillite|redressement judiciaire|liquidation)\b", r"(?:إعسار|إفلاس|تصفية|حراسة قضائية)"],
    "AUTOMATIC_TERMINATION": [r"\b(?:terminate|expire|end)\w*\s+automatically\b", r"\b(?:prend fin|expire|r[eé]sili[eé])\s+automatiquement\b", r"(?:ينتهي|تنتهي|تنقضي).{0,50}تلقائي"],
    "POST_TERMINATION_EFFECTS": [r"\bupon termination\b.{0,220}\b(?:return|delete|pay|cease|survive)\b", r"\b[aà] la r[eé]siliation\b.{0,220}\b(?:restituer|supprimer|payer|cesser|survivre)\b", r"(?:عند الإنهاء|عند الفسخ).{0,220}(?:إعادة|حذف|سداد|التوقف|تستمر)"],
}
COMPILED = {k:[re.compile(p,re.I|re.S) for p in v] for k,v in SIGNALS.items()}

def main():
    if not DETAILS.exists():
        raise SystemExit(f"Missing {DETAILS}")
    rows = json.loads(DETAILS.read_text(encoding="utf-8"))
    selected = [r for r in rows if r.get("type_verdict")=="ABSTAINED" and str(r.get("pipeline_clause_type") or "").strip().lower() in TARGETS]
    selected.sort(key=lambda r:(str(r.get("language") or ""),str(r.get("document") or ""),str(r.get("reference") or "")))
    langs, types, reasons, sigs = Counter(), Counter(), Counter(), Counter()
    no_signal = 0
    for row in selected:
        text = str(row.get("source_text") or "")
        hits = [name for name,pats in COMPILED.items() if any(p.search(text) for p in pats)]
        row["_signals"] = hits
        langs[str(row.get("language") or "UNKNOWN")] += 1
        types[str(row.get("pipeline_clause_type") or "UNKNOWN")] += 1
        reasons[str(row.get("shadow_abstention_reason") or "None")] += 1
        sigs.update(hits)
        no_signal += int(not hits)

    print("="*100)
    print("V4.1.6 TERMINATION ABSTENTION FORENSICS")
    print("="*100)
    print("ROWS:", len(selected))
    print()
    print("ROWS:", len(selected))
    print("BY LANGUAGE:", dict(langs))
    print("BY PIPELINE TYPE:", dict(types))
    print("ABSTENTION REASONS:", dict(reasons))
    print("SIGNAL COUNTS:", dict(sigs))
    print("NO SIGNAL ROWS:", no_signal)

    for i,row in enumerate(selected,1):
        print("\n"+"="*100)
        print(f"[{i}/{len(selected)}]")
        print("LANG:", row.get("language"))
        print("DOC:", row.get("document"))
        print("REF:", row.get("reference"))
        print("PIPELINE:", row.get("pipeline_clause_type"))
        print("ABSTAIN REASON:", row.get("shadow_abstention_reason"))
        print("SIGNALS:", row.get("_signals"))
        print("SOURCE:")
        print(row.get("source_text"))
        print("MECHANISMS:", [m.get("kind") for m in (row.get("ranked_material_mechanisms") or [])])

if __name__ == "__main__":
    main()
