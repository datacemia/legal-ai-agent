#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import shutil
from datetime import datetime
from pathlib import Path

TARGET = Path("app/services/contract_agent/unified_report_from_pipeline.py")

FR_ANCHOR = (
    r'        r"\b(?:le\s+présent\s+|le\s+present\s+)?'
    r'(?:accord|contrat)\s+restera\s+en\s+vigueur\s+pendant\s+'
    r'([^.;\n]{2,120})",'
)

AR_ANCHOR = (
    r'        r"(?:تظل|تبقى)\s+(?:هذه\s+)?'
    r'(?:الاتفاقية|العقد)\s+(?:سارية|نافذة)\s+لمدة\s+'
    r'([^.;؛!؟\n]{2,120})",'
)

FR_NEW = r'''        r"\b(?:le\s+présent\s+|le\s+present\s+)?(?:accord|contrat)\s+(?:a|aura)\s+une\s+(?:durée|duree)\s+initiale\s+de\s+([^.;\n]{2,120})",
        r"\b(?:le\s+présent\s+|le\s+present\s+)?(?:accord|contrat)\s+(?:a|aura)\s+pour\s+(?:durée|duree)\s+initiale\s+([^.;\n]{2,120})",
        r"\b(?:la\s+)?(?:durée|duree)\s+initiale\s+(?:du\s+|de\s+l['’])?(?:accord|contrat)\s+(?:est|sera)\s+de\s+([^.;\n]{2,120})",
'''

AR_NEW = r'''        r"(?:تكون|تبلغ)\s+مدة\s+(?:هذه\s+)?(?:الاتفاقية|العقد)\s+الأولية\s+([^.;؛!؟\n]{2,120})",
        r"(?:تكون|تبلغ)\s+المدة\s+الأولية\s+(?:لهذه\s+)?(?:الاتفاقية|العقد)\s+([^.;؛!؟\n]{2,120})",
        r"(?:مدة\s+(?:هذه\s+)?(?:الاتفاقية|العقد)\s+الأولية)\s+(?:هي|تكون|تبلغ)\s+([^.;؛!؟\n]{2,120})",
'''

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    if not TARGET.exists():
        raise SystemExit(f"TARGET NOT FOUND: {TARGET}")

    source = TARGET.read_text(encoding="utf-8")
    ast.parse(source)

    for token in (
        "CONTRACT_DURATION_PATTERNS",
        "extract_contract_duration",
        "build_contract_overview",
    ):
        if token not in source:
            raise SystemExit(f"REQUIRED ANCHOR MISSING: {token}")

    if (
        r"\s+a\s+une\s+(?:durée|duree)\s+initiale\s+de" in source
        or "مدة\\s+(?:هذه\\s+)?(?:الاتفاقية|العقد)\\s+الأولية" in source
    ):
        raise SystemExit(
            "REFUSING DOUBLE PATCH: V4.1.17C duration forms already present"
        )

    fr_count = source.count(FR_ANCHOR)
    ar_count = source.count(AR_ANCHOR)

    if fr_count != 1:
        raise SystemExit(
            f"FR ANCHOR MISMATCH: expected 1, found {fr_count}"
        )
    if ar_count != 1:
        raise SystemExit(
            f"AR ANCHOR MISMATCH: expected 1, found {ar_count}"
        )

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(
        TARGET.name + ".before_v4_1_17c_" + stamp
    )
    shutil.copy2(TARGET, backup)

    updated = source.replace(
        FR_ANCHOR,
        FR_NEW + FR_ANCHOR,
        1,
    )
    updated = updated.replace(
        AR_ANCHOR,
        AR_NEW + AR_ANCHOR,
        1,
    )

    ast.parse(updated)
    compile(updated, str(TARGET), "exec")

    TARGET.write_text(
        updated,
        encoding="utf-8",
        newline="\n",
    )

    print("=" * 96)
    print("V4.1.17C CONTRACT DURATION FORM COVERAGE APPLIED")
    print("=" * 96)
    print("TARGET :", TARGET)
    print("BACKUP :", backup)
    print("SHA256 :", sha256(TARGET))
    print("EN: existing validated forms preserved")
    print("FR: added contract/agreement + initial-duration forms")
    print("AR: added agreement/contract + initial-duration forms")
    print("INVARIANT: only contract/agreement term wording is eligible")
    print("UNTOUCHED: semantic profile, RULES, dominance thresholds,")
    print("           evidence engine, publication gate, risk scoring,")
    print("           taxonomy, frontend")
    print("AST: OK")
    print("=" * 96)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
