#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from collections import Counter
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")

DETAILS = Path("semantic_profile_shadow_v4_1_9_after_pipeline/shadow_details.json")
TARGETS = {
    "governance", "corporate_governance", "board", "board_composition",
    "reserved_matters", "voting_rights", "approval_rights", "shareholder_rights",
}

SIGNALS = {
    "BOARD_COMPOSITION": [
        r"\bboard of directors\b.{0,180}\b(?:consist of|comprise|composed of|members?|directors?)\b",
        r"\bconseil d['’]administration\b.{0,180}\b(?:compos[eé]|comprend|constitu[eé]|membres?|administrateurs?)\b",
        r"(?:مجلس الإدارة|مجلس الادارة).{0,180}(?:يتكون|يتألف|يضم|أعضاء|مديرين)",
    ],
    "BOARD_APPOINTMENT_RIGHT": [
        r"\b(?:appoint|designate|nominate|elect)\b.{0,160}\b(?:director|board member)\b",
        r"\b(?:nommer|d[eé]signer|proposer|[eé]lire)\b.{0,160}\b(?:administrateur|membre du conseil)\b",
        r"(?:تعيين|يسمي|يرشح|انتخاب).{0,160}(?:عضو مجلس|عضو في المجلس|مدير)",
    ],
    "BOARD_REMOVAL_RIGHT": [
        r"\b(?:remove|dismiss|replace)\b.{0,160}\b(?:director|board member)\b",
        r"\b(?:r[eé]voquer|destituer|remplacer)\b.{0,160}\b(?:administrateur|membre du conseil)\b",
        r"(?:عزل|إقالة|استبدال).{0,160}(?:عضو مجلس|عضو في المجلس|مدير)",
    ],
    "RESERVED_MATTERS_APPROVAL": [
        r"\b(?:reserved matters?|specified matters?)\b.{0,220}\b(?:consent|approval|approve|supermajority)\b",
        r"\b(?:mati[eè]res r[eé]serv[eé]es?|d[eé]cisions r[eé]serv[eé]es?)\b.{0,220}\b(?:consentement|approbation|majorit[eé] qualifi[eé]e)\b",
        r"(?:المسائل المحجوزة|القرارات المحجوزة).{0,220}(?:موافقة|اعتماد|أغلبية خاصة|أغلبية معززة)",
    ],
    "VOTING_THRESHOLD": [
        r"\b(?:majority|supermajority|unanimous|two[- ]thirds?|three[- ]quarters?)\b.{0,180}\b(?:vote|approval|consent)\b",
        r"\b(?:majorit[eé]|unanimit[eé]|deux tiers|trois quarts)\b.{0,180}\b(?:vote|approbation|consentement)\b",
        r"(?:أغلبية|أغلبية خاصة|بالإجماع|ثلثي|ثلاثة أرباع).{0,180}(?:تصويت|موافقة|اعتماد)",
    ],
    "QUORUM_REQUIREMENT": [
        r"\bquorum\b.{0,220}\b(?:meeting|board|shareholders?|members?)\b",
        r"\bquorum\b.{0,220}\b(?:r[eé]union|conseil|actionnaires?|membres?)\b",
        r"(?:النصاب|نصاب الانعقاد).{0,220}(?:اجتماع|مجلس|مساهمين|أعضاء)",
    ],
    "COMMITTEE_GOVERNANCE": [
        r"\b(?:governance|steering|audit|compensation|nomination) committee\b.{0,220}\b(?:establish|meet|review|oversee|approve)\b",
        r"\bcomit[eé] (?:de gouvernance|de pilotage|d['’]audit|des r[eé]mun[eé]rations|de nomination)\b.{0,220}\b(?:mettre en place|se r[eé]unir|examiner|superviser|approuver)\b",
        r"(?:لجنة الحوكمة|اللجنة التوجيهية|لجنة التدقيق|لجنة التعويضات|لجنة الترشيحات).{0,220}(?:إنشاء|تجتمع|مراجعة|الإشراف|الموافقة)",
    ],
    "MANAGEMENT_AUTHORITY": [
        r"\b(?:management|chief executive officer|ceo|manager)\b.{0,220}\b(?:authority|responsible for|manage|conduct the business)\b",
        r"\b(?:direction|directeur g[eé]n[eé]ral|g[eé]rant)\b.{0,220}\b(?:pouvoir|responsable de|g[eé]rer|diriger l['’]activit[eé])\b",
        r"(?:الإدارة|المدير التنفيذي|المدير العام).{0,220}(?:سلطة|مسؤول عن|إدارة|تسيير الأعمال)",
    ],
    "SHAREHOLDER_APPROVAL_RIGHT": [
        r"\bshareholders?\b.{0,200}\b(?:approve|approval|consent|required vote)\b",
        r"\bactionnaires?\b.{0,200}\b(?:approuver|approbation|consentement|vote requis)\b",
        r"(?:المساهم|المساهمون|المساهمين).{0,200}(?:موافقة|اعتماد|تصويت مطلوب)",
    ],
    "INFORMATION_OR_REPORTING_GOVERNANCE": [
        r"\bboard\b.{0,160}\b(?:receive|review|be provided with)\b.{0,160}\b(?:reports?|budgets?|business plans?)\b",
        r"\bconseil\b.{0,160}\b(?:recevra|examinera|se verra remettre)\b.{0,160}\b(?:rapports?|budgets?|plans? d['’]affaires)\b",
        r"(?:المجلس).{0,160}(?:يتلقى|يراجع|يقدم له).{0,160}(?:تقارير|ميزانيات|خطط الأعمال)",
    ],
}

compiled = {k: [re.compile(p, re.I | re.S) for p in pats] for k, pats in SIGNALS.items()}

if not DETAILS.exists():
    raise SystemExit(f"Missing {DETAILS}")

rows = json.loads(DETAILS.read_text(encoding="utf-8"))
selected = [
    row for row in rows
    if row.get("type_verdict") == "ABSTAINED"
    and str(row.get("pipeline_clause_type") or "").strip().lower() in TARGETS
]
selected.sort(key=lambda r: (str(r.get("language") or ""), str(r.get("document") or ""), str(r.get("reference") or "")))

langs, types, reasons, sigs = Counter(), Counter(), Counter(), Counter()
no_signal = 0

for row in selected:
    source = str(row.get("source_text") or "")
    hits = [name for name, pats in compiled.items() if any(p.search(source) for p in pats)]
    row["_governance_signals"] = hits
    langs[str(row.get("language") or "UNKNOWN")] += 1
    types[str(row.get("pipeline_clause_type") or "UNKNOWN")] += 1
    reasons[str(row.get("shadow_abstention_reason") or "None")] += 1
    sigs.update(hits)
    no_signal += int(not hits)

print("=" * 100)
print("V4.1.9 GOVERNANCE ABSTENTION FORENSICS")
print("=" * 100)
print("ROWS:", len(selected))
print("BY LANGUAGE:", dict(langs))
print("BY PIPELINE TYPE:", dict(types))
print("ABSTENTION REASONS:", dict(reasons))
print("SIGNAL COUNTS:", dict(sigs))
print("NO SIGNAL ROWS:", no_signal)

for i, row in enumerate(selected, 1):
    print("\n" + "=" * 100)
    print(f"[{i}/{len(selected)}]")
    print("LANG:", row.get("language"))
    print("DOC:", row.get("document"))
    print("REF:", row.get("reference"))
    print("PIPELINE:", row.get("pipeline_clause_type"))
    print("ABSTAIN REASON:", row.get("shadow_abstention_reason"))
    print("SIGNALS:", row.get("_governance_signals"))
    print("SOURCE:")
    print(row.get("source_text"))
    print("MECHANISMS:", [m.get("kind") for m in (row.get("ranked_material_mechanisms") or [])])
