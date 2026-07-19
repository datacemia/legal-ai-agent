#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import shutil
from datetime import datetime
from pathlib import Path

TARGET = Path("app/services/contract_agent/semantic_source_profile.py")
ANCHOR = '    _r("DATA_PROTECTION_AUDIT_COOPERATION",'

RULE_BLOCK = r"""    _r("SECURITY_AUDIT_RIGHT",
       (
           r"\b(?:client|customer|party|recipient|auditor)\b[^.;!?]{0,120}\b(?:shall\s+have\s+the\s+right|has\s+the\s+right|may|is\s+entitled)\b[^.;!?]{0,180}\b(?:conduct|perform|carry\s+out)\b[^.;!?]{0,100}\b(?:on[-\s]?site\s+)?(?:security|cybersecurity|information\s+security)\s+(?:audit|assessment|inspection)\b[^.;!?]{0,260}",
           r"\b(?:right\s+to|may)\b[^.;!?]{0,120}\b(?:audit|inspect|examine|review)\b[^.;!?]{0,180}\b(?:security\s+controls?|security\s+systems?|information\s+security|cybersecurity|security\s+program(?:me)?)\b[^.;!?]{0,260}",
       ),
       (
           r"\b(?:client|partie|b[eé]n[eé]ficiaire|auditeur)\b[^.;!?]{0,120}\b(?:aura\s+le\s+droit|a\s+le\s+droit|peut|pourra|est\s+en\s+droit)\b[^.;!?]{0,180}\b(?:r[eé]aliser|effectuer|conduire|mener)\b[^.;!?]{0,100}\b(?:un\s+)?(?:audit|contr[oô]le|inspection)\s+(?:de\s+)?(?:s[eé]curit[eé]|cybers[eé]curit[eé]|s[eé]curit[eé]\s+de\s+l[\'’]information)\b[^.;!?]{0,260}",
           r"\b(?:droit\s+d[\'’]|peut|pourra)\b[^.;!?]{0,120}\b(?:auditer|inspecter|examiner|contr[oô]ler)\b[^.;!?]{0,180}\b(?:contr[oô]les?\s+de\s+s[eé]curit[eé]|syst[eè]mes?\s+de\s+s[eé]curit[eé]|s[eé]curit[eé]\s+de\s+l[\'’]information|cybers[eé]curit[eé])\b[^.;!?]{0,260}",
       ),
       (
           r"(?:يحق|يجوز)\s+ل(?:لعميل|لطرف|للمستفيد|لمدقق)[^.;؛!?]{0,180}(?:إجراء|تنفيذ|القيام\s+ب)[^.;؛!?]{0,100}(?:تدقيق|مراجعة|تفتيش)\s+(?:أمني|للأمن|لأمن\s+المعلومات|للأمن\s+السيبراني|سيبراني)[^.;؛!?]{0,260}",
           r"(?:الحق\s+في|يجوز|يحق)[^.;؛!?]{0,120}(?:تدقيق|تفتيش|فحص|مراجعة)[^.;؛!?]{0,180}(?:ضوابط\s+الأمن|أنظمة\s+الأمن|أمن\s+المعلومات|الأمن\s+السيبراني|برنامج\s+الأمن)[^.;؛!?]{0,260}",
       ),
       94, "security", DOMAIN_CORE, True, polarity="RIGHT"),

    _r("DATA_PROTECTION_AUDIT_RIGHT",
       (
           r"\b(?:controller|customer|client|data\s+protection\s+authority|auditor)\b[^.;!?]{0,120}\b(?:shall\s+have\s+the\s+right|has\s+the\s+right|may|is\s+entitled)\b[^.;!?]{0,180}\b(?:audit|inspect|examine|review)\b[^.;!?]{0,180}\b(?:personal\s+data|data\s+protection|privacy|processing\s+activities|processor)\b[^.;!?]{0,260}",
       ),
       (
           r"\b(?:responsable\s+du\s+traitement|client|autorit[eé]\s+de\s+protection\s+des\s+donn[eé]es|auditeur)\b[^.;!?]{0,120}\b(?:aura\s+le\s+droit|a\s+le\s+droit|peut|pourra|est\s+en\s+droit)\b[^.;!?]{0,180}\b(?:auditer|inspecter|examiner|contr[oô]ler)\b[^.;!?]{0,180}\b(?:donn[eé]es?\s+personnelles?|protection\s+des\s+donn[eé]es|vie\s+priv[eé]e|activit[eé]s?\s+de\s+traitement|sous-traitant)\b[^.;!?]{0,260}",
       ),
       (
           r"(?:يحق|يجوز)\s+ل(?:لمتحكم|للعميل|لسلطة\s+حماية\s+البيانات|لمدقق)[^.;؛!?]{0,180}(?:تدقيق|تفتيش|فحص|مراجعة)[^.;؛!?]{0,180}(?:البيانات\s+الشخصية|حماية\s+البيانات|الخصوصية|أنشطة\s+المعالجة|المعالج)[^.;؛!?]{0,260}",
       ),
       93, "data_protection", DOMAIN_CORE, True, polarity="RIGHT"),

    _r("FINANCIAL_RECORDS_AUDIT_RIGHT",
       (
           r"\b(?:lender|investor|buyer|customer|party|auditor)\b[^.;!?]{0,120}\b(?:shall\s+have\s+the\s+right|has\s+the\s+right|may|is\s+entitled)\b[^.;!?]{0,180}\b(?:audit|inspect|examine|review)\b[^.;!?]{0,180}\b(?:books?\s+and\s+records?|financial\s+records?|accounting\s+records?|accounts?|financial\s+statements?)\b[^.;!?]{0,260}",
       ),
       (
           r"\b(?:pr[eê]teur|investisseur|acheteur|client|partie|auditeur)\b[^.;!?]{0,120}\b(?:aura\s+le\s+droit|a\s+le\s+droit|peut|pourra|est\s+en\s+droit)\b[^.;!?]{0,180}\b(?:auditer|inspecter|examiner|contr[oô]ler)\b[^.;!?]{0,180}\b(?:livres?\s+et\s+registres?|documents?\s+financiers?|registres?\s+comptables?|comptes?|[eé]tats?\s+financiers?)\b[^.;!?]{0,260}",
       ),
       (
           r"(?:يحق|يجوز)\s+ل(?:لمقرض|للمستثمر|للمشتري|للعميل|لطرف|لمدقق)[^.;؛!?]{0,180}(?:تدقيق|تفتيش|فحص|مراجعة)[^.;؛!?]{0,180}(?:الدفاتر\s+والسجلات|السجلات\s+المالية|السجلات\s+المحاسبية|الحسابات|القوائم\s+المالية|البيانات\s+المالية)[^.;؛!?]{0,260}",
       ),
       93, "financial_reporting", DOMAIN_CORE, True, polarity="RIGHT"),

    _r("COMPLIANCE_AUDIT_RIGHT",
       (
           r"\b(?:customer|client|party|authority|auditor)\b[^.;!?]{0,120}\b(?:shall\s+have\s+the\s+right|has\s+the\s+right|may|is\s+entitled)\b[^.;!?]{0,180}\b(?:audit|inspect|examine|review)\b[^.;!?]{0,180}\b(?:compliance\s+with|anti[-\s]?bribery|anti[-\s]?corruption|sanctions|export\s+controls?|code\s+of\s+conduct|applicable\s+law)\b[^.;!?]{0,260}",
       ),
       (
           r"\b(?:client|partie|autorit[eé]|auditeur)\b[^.;!?]{0,120}\b(?:aura\s+le\s+droit|a\s+le\s+droit|peut|pourra|est\s+en\s+droit)\b[^.;!?]{0,180}\b(?:auditer|inspecter|examiner|contr[oô]ler)\b[^.;!?]{0,180}\b(?:conformit[eé]\s+[àa]|lutte\s+contre\s+la\s+corruption|anticorruption|sanctions|contr[oô]le\s+des\s+exportations|code\s+de\s+conduite|droit\s+applicable)\b[^.;!?]{0,260}",
       ),
       (
           r"(?:يحق|يجوز)\s+ل(?:لعميل|لطرف|للسلطة|لمدقق)[^.;؛!?]{0,180}(?:تدقيق|تفتيش|فحص|مراجعة)[^.;؛!?]{0,180}(?:الامتثال|مكافحة\s+الرشوة|مكافحة\s+الفساد|العقوبات|ضوابط\s+التصدير|مدونة\s+السلوك|القانون\s+المعمول\s+به)[^.;؛!?]{0,260}",
       ),
       92, "compliance", DOMAIN_CORE, True, polarity="RIGHT"),

"""

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    if not TARGET.exists():
        raise SystemExit(f"TARGET NOT FOUND: {TARGET}")
    source = TARGET.read_text(encoding="utf-8")
    ast.parse(source)
    kinds = ("SECURITY_AUDIT_RIGHT", "DATA_PROTECTION_AUDIT_RIGHT", "FINANCIAL_RECORDS_AUDIT_RIGHT", "COMPLIANCE_AUDIT_RIGHT")
    present = [kind for kind in kinds if f'_r("{kind}"' in source]
    if present:
        raise SystemExit("REFUSING DOUBLE PATCH; PRESENT: " + ", ".join(present))
    anchor_count = source.count(ANCHOR)
    if anchor_count != 1:
        raise SystemExit(f"EXPECTED EXACTLY ONE DATA_PROTECTION_AUDIT_COOPERATION ANCHOR; FOUND {anchor_count}")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(TARGET.name + ".before_v4_1_17b_" + stamp)
    shutil.copy2(TARGET, backup)
    updated = source.replace(ANCHOR, RULE_BLOCK + ANCHOR, 1)
    ast.parse(updated)
    compile(updated, str(TARGET), "exec")
    TARGET.write_text(updated, encoding="utf-8", newline="\n")
    print("=" * 96)
    print("V4.1.17B CONTEXTUAL AUDIT RIGHTS APPLIED")
    print("=" * 96)
    print("TARGET :", TARGET)
    print("BACKUP :", backup)
    print("SHA256 :", sha256(TARGET))
    print("ADDED  :")
    for kind in kinds:
        print("-", kind)
    print("INVARIANT: audit object/context selects domain; notice remains procedural")
    print("UNKNOWN AUDIT CONTEXT: no generic primary type added; profiler may abstain")
    print("UNTOUCHED: NOTICE_PROCEDURE, TERMINATION_NOTICE_PERIOD,")
    print("           DATA_PROTECTION_AUDIT_COOPERATION, dominance thresholds,")
    print("           evidence engine, publication gate, risk scoring, frontend")
    print("AST: OK")
    print("=" * 96)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
