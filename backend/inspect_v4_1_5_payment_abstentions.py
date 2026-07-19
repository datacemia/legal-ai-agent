#!/usr/bin/env python3
"""Read-only payment abstention forensics for semantic profile V4.1.5."""
from __future__ import annotations
import json, re, sys
from collections import Counter
from pathlib import Path

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")

DETAILS = Path("semantic_profile_shadow_v4_1_5_after_pipeline/shadow_details.json")
TARGETS = {"payment", "fees", "compensation", "pricing", "invoice"}

SIGNALS = {
    "PAYMENT_DUTY": [r"\b(?:shall|must|will)\s+(?:pay|remit)\b", r"\b(?:paiera|payera|r[èe]glera|versera|acquittera)\b", r"(?:يدفع|تدفع|يسدد|تسدد|يلتزم.{0,40}بالدفع)"],
    "PAYMENT_DEADLINE": [r"\b(?:within|no later than|due within|due on|payable within)\b.{0,80}\b(?:day|days|date)\b", r"\b(?:dans un d[ée]lai de|au plus tard|exigible|payable sous)\b.{0,80}\b(?:jour|jours|date)\b", r"(?:خلال|في موعد لا يتجاوز|مستحق.{0,30}خلال).{0,80}(?:يوم|أيام|تاريخ)"],
    "INVOICE_TRIGGER": [r"\b(?:invoice|invoiced|receipt of invoice|billing)\b", r"\b(?:facture|facturation|r[ée]ception de la facture)\b", r"(?:فاتورة|الفاتورة|الفوترة|استلام.{0,30}فاتورة)"],
    "FEES_CHARGES": [r"\b(?:fees?|charges?|service fees?|subscription fees?)\b", r"\b(?:frais|honoraires|redevances|charges)\b", r"(?:رسوم|أتعاب|مصاريف|تكاليف)"],
    "INSTALLMENT_SCHEDULE": [r"\b(?:installments?|monthly payments?|quarterly payments?|payment schedule)\b", r"\b(?:versements?|mensualit[ée]s|paiements? mensuels?|[ée]ch[ée]ancier)\b", r"(?:أقساط|دفعات شهرية|جدول السداد|جدول الدفع)"],
    "LATE_PAYMENT_INTEREST": [r"\b(?:late payment|overdue|past due)\b.{0,100}\b(?:interest|rate)\b", r"\b(?:retard de paiement|impay[ée]|arri[ée]r[ée])\b.{0,100}\b(?:int[ée]r[êe]t|taux)\b", r"(?:تأخر.{0,30}الدفع|متأخرات|مبالغ متأخرة).{0,100}(?:فائدة|معدل)"],
    "REIMBURSEMENT_RECONCILIATION": [r"\b(?:reimburse|reimbursement|reconcile|reconciliation|true[- ]?up)\b", r"\b(?:rembourser|remboursement|r[ée]gularis[ée]|r[ée]gularisation)\b", r"(?:تعويض|تسوية|مطابقة الحسابات)"],
    "BASE_COMPENSATION": [r"\b(?:base salary|annual salary|compensation)\b", r"\b(?:salaire de base|r[ée]mun[ée]ration)\b", r"(?:راتب أساسي|راتب سنوي|تعويض)"],
    "PRICE_ONLY": [r"\b(?:price|pricing|unit price)\b", r"\b(?:prix|tarification|prix unitaire)\b", r"(?:سعر|تسعير|سعر الوحدة)"],
}
compiled = {k: [re.compile(p, re.I | re.S) for p in v] for k, v in SIGNALS.items()}
rows = json.loads(DETAILS.read_text(encoding="utf-8"))
selected = [r for r in rows if r.get("type_verdict") == "ABSTAINED" and str(r.get("pipeline_clause_type") or "").strip().lower() in TARGETS]

langs, types, reasons, signals = Counter(), Counter(), Counter(), Counter()
no_signal = []
for row in selected:
    text = str(row.get("source_text") or "")
    hits = [name for name, pats in compiled.items() if any(p.search(text) for p in pats)]
    row["_forensic_signals"] = hits
    langs[str(row.get("language") or "UNKNOWN")] += 1
    types[str(row.get("pipeline_clause_type") or "UNKNOWN")] += 1
    reasons[str(row.get("shadow_abstention_reason") or "None")] += 1
    signals.update(hits)
    if not hits:
        no_signal.append(row)

print("=" * 100)
print("V4.1.5 PAYMENT ABSTENTION FORENSICS")
print("=" * 100)
print("ROWS:", len(selected))
print()
print("ROWS:", len(selected))
print("BY LANGUAGE:", dict(langs))
print("BY PIPELINE TYPE:", dict(types))
print("ABSTENTION REASONS:", dict(reasons))
print("SIGNAL COUNTS:", dict(signals))
print("NO SIGNAL ROWS:", len(no_signal))

for i, row in enumerate(selected, 1):
    print("\n" + "=" * 100)
    print(f"[{i}/{len(selected)}]")
    print("LANG:", row.get("language"))
    print("DOC:", row.get("document"))
    print("REF:", row.get("reference"))
    print("PIPELINE:", row.get("pipeline_clause_type"))
    print("ABSTAIN REASON:", row.get("shadow_abstention_reason"))
    print("SIGNALS:", row.get("_forensic_signals"))
    print("SOURCE:")
    print(row.get("source_text"))
    print("MECHANISMS:", [m.get("kind") for m in (row.get("ranked_material_mechanisms") or [])])
