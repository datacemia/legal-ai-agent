from __future__ import annotations

import ast
import hashlib
import shutil
from pathlib import Path


TARGET = Path(
    "app/services/contract_agent/semantic_source_profile.py"
)

BACKUP = TARGET.with_suffix(
    ".py.before_v4_1_14a_loan_core"
)

ANCHOR = '    _r("FINANCIAL_REPORTING_OBLIGATION",'

RULE_BLOCK = r'''    _r("FINANCIAL_COVENANT",
       (
           r"\bborrower\b.{0,160}\b(?:covenants?|undertakes?|agrees?)\s+to\s+maintain\b.{0,180}\b(?:ratio|coverage\s+ratio|financial\s+ratio)\b.{0,180}",
           r"\bdebt[-\s]+service\s+coverage\s+ratio\b.{0,120}\b(?:not\s+less\s+than|at\s+least|minimum)\b.{0,80}",
       ),
       (
           r"\bemprunteur\b.{0,160}\bs[\'’]engage\s+[àa]\s+maintenir\b.{0,180}\b(?:ratio|ratio\s+de\s+couverture)\b.{0,180}",
           r"\bratio\s+de\s+couverture\s+du\s+service\s+de\s+la\s+dette\b.{0,120}\b(?:d[\'’]au\s+moins|au\s+moins|minimum)\b.{0,80}",
       ),
       (
           r"(?:يتعهد|يلتزم).{0,100}المقترض.{0,120}(?:بالحفاظ|بالمحافظة).{0,160}(?:نسبة|معدل).{0,160}",
           r"(?:نسبة|معدل)\s+تغطية\s+خدمة\s+الدين.{0,120}(?:لا\s+تقل\s+عن|بحد\s+أدنى).{0,80}",
       ),
       94, "loan", DOMAIN_CORE, True, polarity="REQUIRED"),

    _r("VOLUNTARY_PREPAYMENT_RIGHT",
       (
           r"\bborrower\b.{0,80}\bmay\s+prepay\b.{0,80}\b(?:loan|principal)\b.{0,180}\b(?:without\s+(?:penalty|premium)|no\s+(?:penalty|premium))\b",
           r"\bprepay\b.{0,100}\b(?:in\s+whole\s+or\s+in\s+part|whole\s+or\s+part)\b.{0,160}\bwithout\s+(?:penalty|premium)\b",
       ),
       (
           r"\bemprunteur\b.{0,80}\b(?:pourra|peut)\s+rembourser\b.{0,80}\b(?:pr[eê]t|principal)\b.{0,80}\bpar\s+anticipation\b.{0,180}\bsans\s+p[eé]nalit[eé]\b",
           r"\brembours\w*\s+par\s+anticipation\b.{0,100}\b(?:en\s+tout\s+ou\s+partie|totalement\s+ou\s+partiellement)\b.{0,160}\bsans\s+p[eé]nalit[eé]\b",
       ),
       (
           r"(?:يجوز|يحق)\s+للمقترض.{0,120}(?:السداد|التسديد|الوفاء).{0,80}(?:المبكر|المسبق|قبل\s+موعد\s+الاستحقاق).{0,180}(?:دون|بدون).{0,40}(?:غرامة|جزاء)",
           r"(?:سداد|تسديد)\s+(?:القرض|المبلغ\s+الأصلي).{0,80}(?:مبكر(?:اً|ًا|ا)|مسبق(?:اً|ًا|ا)).{0,160}(?:دون|بدون).{0,40}(?:غرامة|جزاء)",
       ),
       93, "loan", DOMAIN_CORE, True, polarity="RIGHT"),

    _r("LOAN_PRINCIPAL_DISBURSEMENT",
       (
           r"\blender\b.{0,80}\bshall\s+disburse\b.{0,100}\bprincipal\s+amount\s+of\s+the\s+loan\b.{0,80}\bto\s+borrower\b.{0,220}\bconditions?\s+precedent\b",
           r"\bdisburse\b.{0,100}\bprincipal\s+amount\b.{0,100}\bloan\b.{0,100}\bborrower\b.{0,220}\bconditions?\s+precedent\b",
       ),
       (
           r"\bpr[eê]teur\b.{0,80}\bd[eé]caissera\b.{0,100}\bmontant\s+en\s+principal\s+du\s+pr[eê]t\b.{0,80}\b[àa]\s+l[\'’]emprunteur\b.{0,220}\bconditions?\s+pr[eé]alables?\b",
           r"\bd[eé]caiss\w*\b.{0,100}\bprincipal\b.{0,100}\bpr[eê]t\b.{0,100}\bemprunteur\b.{0,220}\bconditions?\s+pr[eé]alables?\b",
       ),
       (
           r"(?:يصرف|سيصرف)\s+المقرض.{0,100}المبلغ\s+الأصلي\s+للقرض.{0,80}(?:إلى|لـ?)\s*المقترض.{0,220}(?:الشروط\s+المسبقة|الشروط\s+السابقة)",
           r"(?:صرف|يصرف).{0,100}المبلغ\s+الأصلي.{0,100}القرض.{0,100}المقترض.{0,220}(?:استيفاء|استكمال).{0,80}الشروط\s+المسبقة",
       ),
       96, "loan", DOMAIN_CORE, True, polarity="REQUIRED"),

    _r("ACCELERATION_ON_DEFAULT",
       (
           r"\b(?:upon|following)\b.{0,60}\b(?:event\s+of\s+default|default)\b.{0,120}\blender\b.{0,100}\bmay\s+declare\b.{0,180}\b(?:outstanding|remaining)\s+principal\b.{0,100}\b(?:accrued\s+interest|interest\s+accrued)\b.{0,120}\bimmediately\s+(?:due|payable|due\s+and\s+payable)\b",
           r"\blender\b.{0,100}\bmay\s+declare\b.{0,180}\b(?:entire|all)\b.{0,80}\b(?:loan|principal|indebtedness)\b.{0,120}\bimmediately\s+(?:due|payable|due\s+and\s+payable)\b.{0,160}\bdefault\b",
       ),
       (
           r"\b(?:en\s+cas|[àa]\s+la\s+suite)\b.{0,60}\b(?:d[eé]faut|cas\s+de\s+d[eé]faut)\b.{0,120}\bpr[eê]teur\b.{0,100}\b(?:peut|pourra)\s+d[eé]clarer\b.{0,180}\bprincipal\s+restant\b.{0,100}\bint[eé]r[eê]ts\s+courus\b.{0,120}\bimm[eé]diatement\s+exigible\b",
           r"\bpr[eê]teur\b.{0,100}\b(?:peut|pourra)\s+d[eé]clarer\b.{0,180}\b(?:totalit[eé]|int[eé]gralit[eé])\b.{0,80}\b(?:pr[eê]t|principal|dette)\b.{0,120}\bimm[eé]diatement\s+exigible\b.{0,160}\bd[eé]faut\b",
       ),
       (
           r"(?:عند|في\s+حال).{0,60}(?:وقوع\s+)?(?:حالة\s+تعثر|تعثر|حالة\s+إخلال).{0,120}(?:يجوز|يحق)\s+للمقرض.{0,100}(?:إعلان|أن\s+يعلن).{0,180}(?:المبلغ\s+الأصلي\s+المتبقي|كامل\s+المبلغ\s+الأصلي).{0,100}(?:الفوائد\s+المتراكمة|الفائدة\s+المتراكمة).{0,120}(?:فوراً|فورًا|حالاً|حالًا)",
           r"(?:يجوز|يحق)\s+للمقرض.{0,100}(?:إعلان|أن\s+يعلن).{0,180}(?:كامل|جميع).{0,80}(?:القرض|المبلغ\s+الأصلي|المديونية).{0,120}(?:مستحق(?:اً|ًا|ا)\s+فوراً|واجبة\s+الأداء\s+فوراً).{0,160}(?:تعثر|إخلال)",
       ),
       97, "loan", DOMAIN_CORE, True, polarity="RIGHT"),

'''

def main() -> int:
    if not TARGET.exists():
        raise SystemExit(f"ERROR: target not found: {TARGET}")

    source = TARGET.read_text(encoding="utf-8")

    new_kinds = (
        "FINANCIAL_COVENANT",
        "VOLUNTARY_PREPAYMENT_RIGHT",
        "LOAN_PRINCIPAL_DISBURSEMENT",
        "ACCELERATION_ON_DEFAULT",
    )

    already_present = [
        kind for kind in new_kinds
        if f'_r("{kind}"' in source
    ]

    if already_present:
        raise SystemExit(
            "ERROR: refusing double patch; already present: "
            + ", ".join(already_present)
        )

    anchor_count = source.count(ANCHOR)
    if anchor_count != 1:
        raise SystemExit(
            "ERROR: expected exactly one "
            "FINANCIAL_REPORTING_OBLIGATION anchor, "
            f"found {anchor_count}"
        )

    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)

    updated = source.replace(
        ANCHOR,
        RULE_BLOCK + ANCHOR,
        1,
    )

    ast.parse(updated)
    compile(updated, str(TARGET), "exec")

    TARGET.write_text(
        updated,
        encoding="utf-8",
        newline="\n",
    )

    print("PATCH SUCCESS")
    print("FILE:", TARGET)
    print("BACKUP:", BACKUP)
    print(
        "SHA256:",
        hashlib.sha256(TARGET.read_bytes()).hexdigest(),
    )
    print("ADDED:")
    for kind in new_kinds:
        print("-", kind)
    print("UNCHANGED:")
    print("- FINANCIAL_REPORTING_OBLIGATION")
    print("- NON_COMPETE_RESTRICTION")
    print("- RESERVED_MATTERS_CONSENT")
    print("- dominance thresholds")
    print("- evidence engine")
    print("- publication gate")
    print("AST: OK")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
