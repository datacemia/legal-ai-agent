#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

from app.services.contract_agent.semantic_source_profile import (
    build_semantic_source_profile,
)

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(
            encoding="utf-8",
            errors="backslashreplace",
        )

DETAILS = Path(
    "semantic_profile_shadow_v4_1_3_after_pipeline/"
    "shadow_details.json"
)

TARGETS = {
    "data_protection",
    "data_processing",
    "privacy",
}

SIGNALS = {
    "en": {
        "PROCESSING_INSTRUCTIONS": (
            r"process.{0,100}personal data.{0,140}instructions?",
            r"personal data.{0,140}only.{0,80}(?:instructions?|purposes?)",
        ),
        "SECURITY_SAFEGUARDS": (
            r"(?:administrative|technical|physical).{0,120}(?:safeguards?|measures?)",
            r"appropriate technical and organizational measures",
        ),
        "BREACH_NOTIFICATION": (
            r"(?:notify|notification).{0,120}(?:security incident|data breach|personal data breach)",
        ),
        "DATA_RETURN_DELETE": (
            r"(?:return|delete|destroy).{0,100}(?:personal data|customer data)",
            r"(?:personal data|customer data).{0,120}(?:return|delete|destroy)",
        ),
        "DATA_SUBJECT_RIGHTS": (
            r"data subject.{0,120}(?:request|rights?|access|erasure|rectification)",
            r"assist.{0,120}(?:data subject|controller)",
        ),
        "SUBPROCESSOR": (
            r"subprocessor",
            r"sub-processor",
        ),
        "CONFIDENTIAL_PERSONNEL": (
            r"authori[sz]ed persons?.{0,140}confidentiality",
            r"persons? authori[sz]ed to process.{0,140}confidentiality",
        ),
        "TRANSFER_RESTRICTION": (
            r"(?:cross-border|international) transfer",
            r"transfer.{0,100}personal data.{0,120}(?:country|jurisdiction|EEA)",
        ),
    },
    "fr": {
        "PROCESSING_INSTRUCTIONS": (
            r"traiter.{0,100}donn[eé]es? [aà] caract[eè]re personnel.{0,140}instructions?",
            r"donn[eé]es? [aà] caract[eè]re personnel.{0,140}uniquement.{0,80}(?:instructions?|finalit[eé]s?)",
        ),
        "SECURITY_SAFEGUARDS": (
            r"(?:mesures?|garanties?).{0,120}(?:administratives?|techniques?|physiques?|organisationnelles?)",
            r"mesures techniques et organisationnelles appropri[eé]es",
        ),
        "BREACH_NOTIFICATION": (
            r"notifi.{0,120}(?:incident de s[eé]curit[eé]|violation de donn[eé]es)",
        ),
        "DATA_RETURN_DELETE": (
            r"(?:restituer|supprimer|d[eé]truire).{0,100}(?:donn[eé]es? [aà] caract[eè]re personnel|donn[eé]es? du client)",
            r"(?:donn[eé]es? [aà] caract[eè]re personnel|donn[eé]es? du client).{0,120}(?:restituer|supprimer|d[eé]truire)",
        ),
        "DATA_SUBJECT_RIGHTS": (
            r"personnes? concern[eé]es?.{0,120}(?:demande|droits?|acc[eè]s|effacement|rectification)",
            r"assister.{0,120}(?:responsable du traitement|personnes? concern[eé]es?)",
        ),
        "SUBPROCESSOR": (
            r"sous-traitant ult[eé]rieur",
            r"sous-traitant secondaire",
        ),
        "CONFIDENTIAL_PERSONNEL": (
            r"personnes? autoris[eé]es?.{0,140}confidentialit[eé]",
            r"autoris[eé]es? [aà] traiter.{0,140}confidentialit[eé]",
        ),
        "TRANSFER_RESTRICTION": (
            r"transfert(?:s)? international(?:aux)?",
            r"transf[eé]rer.{0,100}donn[eé]es? [aà] caract[eè]re personnel.{0,120}(?:pays|juridiction|EEE)",
        ),
    },
    "ar": {
        "PROCESSING_INSTRUCTIONS": (
            r"(?:يعالج|معالجة).{0,100}البيانات الشخصية.{0,140}(?:التعليمات|تعليمات)",
            r"البيانات الشخصية.{0,140}(?:فقط|حصراً|حصرًا).{0,80}(?:التعليمات|الأغراض)",
        ),
        "SECURITY_SAFEGUARDS": (
            r"(?:ضمانات|تدابير).{0,120}(?:إدارية|تقنية|فنية|مادية|تنظيمية)",
            r"تدابير تقنية وتنظيمية مناسبة",
        ),
        "BREACH_NOTIFICATION": (
            r"(?:يخطر|إخطار|إشعار).{0,120}(?:حادث أمني|خرق البيانات|انتهاك البيانات)",
        ),
        "DATA_RETURN_DELETE": (
            r"(?:إعادة|حذف|إتلاف).{0,100}(?:البيانات الشخصية|بيانات العميل)",
            r"(?:البيانات الشخصية|بيانات العميل).{0,120}(?:إعادة|حذف|إتلاف)",
        ),
        "DATA_SUBJECT_RIGHTS": (
            r"(?:صاحب البيانات|أصحاب البيانات).{0,120}(?:طلب|حقوق|الوصول|المحو|التصحيح)",
            r"(?:يساعد|مساعدة).{0,120}(?:المتحكم|صاحب البيانات|أصحاب البيانات)",
        ),
        "SUBPROCESSOR": (
            r"معالج فرعي",
            r"المعالج من الباطن",
        ),
        "CONFIDENTIAL_PERSONNEL": (
            r"(?:الأشخاص|الموظفون) المصرح لهم.{0,140}السرية",
            r"المصرح لهم بمعالجة.{0,140}السرية",
        ),
        "TRANSFER_RESTRICTION": (
            r"نقل دولي للبيانات",
            r"نقل.{0,100}البيانات الشخصية.{0,120}(?:دولة|بلد|ولاية قضائية)",
        ),
    },
}

def labels(text: str, language: str) -> list[str]:
    return [
        label
        for label, patterns in SIGNALS.get(language, {}).items()
        if any(
            re.search(pattern, text, re.I | re.S)
            for pattern in patterns
        )
    ]

def main() -> int:
    if not DETAILS.exists():
        raise SystemExit(
            f"Missing {DETAILS}. Run V4.1.3 post-pipeline shadow first."
        )

    rows = json.loads(
        DETAILS.read_text(encoding="utf-8")
    )

    selected = [
        row
        for row in rows
        if row.get("type_verdict") == "ABSTAINED"
        and str(
            row.get("pipeline_clause_type") or ""
        ).strip().lower() in TARGETS
    ]

    selected.sort(
        key=lambda row: (
            str(row.get("language") or ""),
            str(row.get("document") or ""),
            str(row.get("reference") or ""),
        )
    )

    langs = Counter()
    types = Counter()
    reasons = Counter()
    signals = Counter()
    no_signal = 0

    print("=" * 100)
    print("V4.1.3 DATA PROTECTION ABSTENTION FORENSICS")
    print("=" * 100)
    print("ROWS:", len(selected))

    for index, row in enumerate(selected, 1):
        language = str(
            row.get("language") or "unknown"
        ).lower()
        source = str(
            row.get("source_text") or ""
        )
        profile = build_semantic_source_profile(
            source,
            language=language,
        )
        found = labels(source, language)

        langs[language] += 1
        types[str(row.get("pipeline_clause_type") or "")] += 1
        reasons[str(profile.get("abstention_reason") or "NONE")] += 1
        signals.update(found)
        no_signal += int(not found)

        print("\n" + "#" * 100)
        print(f"[{index}/{len(selected)}]")
        print("LANG:", language)
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

        for mechanism in (
            profile.get("ranked_material_mechanisms")
            or []
        ):
            print(
                "-",
                mechanism.get("kind"),
                "| role=",
                mechanism.get("semantic_role"),
                "| primary=",
                mechanism.get("candidate_primary_type"),
                "| eligible=",
                mechanism.get("primary_eligible"),
                "| rank=",
                mechanism.get("rank"),
            )
            for evidence in (
                mechanism.get("source_evidence")
                or []
            ):
                print(
                    "  EVIDENCE:",
                    repr(evidence.get("text")),
                )

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
