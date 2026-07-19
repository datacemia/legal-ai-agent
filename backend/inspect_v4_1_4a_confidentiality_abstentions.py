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
    "semantic_profile_shadow_v4_1_4a_exact_source_after_pipeline/"
    "shadow_details.json"
)

TARGETS = {"confidentiality"}

SIGNALS = {
    "en": {
        "CONFIDENTIALITY_DUTY": (
            r"(?:shall|must) (?:hold|keep|maintain).{0,120}confidential",
            r"strict confidence",
        ),
        "USE_RESTRICTION": (
            r"use.{0,120}confidential information.{0,100}(?:solely|only)",
        ),
        "SURVIVAL_DURATION": (
            r"confidentiality obligations?.{0,120}(?:survive|continue|remain)",
            r"trade secrets?.{0,120}(?:survive|remain)",
        ),
        "EXCEPTIONS": (
            r"confidential information does not include",
            r"publicly available",
            r"independently developed",
            r"rightfully received",
        ),
        "COMPELLED_DISCLOSURE": (
            r"(?:required by law|legal process|court order|subpoena)",
            r"compelled disclosure",
        ),
        "REPRESENTATIVE_FLOWDOWN": (
            r"representatives?.{0,160}confidentiality obligations?",
            r"need to know.{0,120}representatives?",
        ),
        "NO_LICENSE": (
            r"nothing.{0,100}grants?.{0,80}licen[cs]e",
            r"no licen[cs]e",
        ),
        "INJUNCTIVE_RELIEF": (
            r"irreparable harm.{0,180}injunctive relief",
        ),
    },
    "fr": {
        "CONFIDENTIALITY_DUTY": (
            r"(?:doit|devra|conservera|gardera).{0,120}confidentiel",
            r"plus stricte confidentialit[eé]",
        ),
        "USE_RESTRICTION": (
            r"utilis\w*.{0,120}informations? confidentielles?.{0,100}(?:uniquement|qu['’]aux fins)",
        ),
        "SURVIVAL_DURATION": (
            r"obligations? de confidentialit[eé].{0,140}(?:survivront|subsisteront|demeureront)",
            r"secrets? commerciaux?.{0,140}(?:survivront|demeureront)",
        ),
        "EXCEPTIONS": (
            r"informations? confidentielles? n['’]inclu(?:t|ent) pas",
            r"publiquement accessibles?",
            r"d[eé]velopp[eé]es? ind[eé]pendamment",
            r"re[cç]ues? l[eé]gitimement",
        ),
        "COMPELLED_DISCLOSURE": (
            r"(?:exig[eé] par la loi|proc[eé]dure judiciaire|ordonnance d['’]un tribunal|assignation)",
            r"divulgation impos[eé]e",
        ),
        "REPRESENTATIVE_FLOWDOWN": (
            r"repr[eé]sentants?.{0,180}obligations? de confidentialit[eé]",
            r"besoin d['’]en conna[iî]tre.{0,120}repr[eé]sentants?",
        ),
        "NO_LICENSE": (
            r"rien.{0,120}n['’]accorde.{0,80}licence",
            r"aucune licence",
        ),
        "INJUNCTIVE_RELIEF": (
            r"pr[eé]judice irr[eé]parable.{0,220}(?:mesure injonctive|injonction)",
        ),
    },
    "ar": {
        "CONFIDENTIALITY_DUTY": (
            r"(?:يجب|يلتزم|يتعين).{0,120}(?:الحفاظ|المحافظة).{0,100}(?:سرية|سري)",
            r"بسرية تامة",
        ),
        "USE_RESTRICTION": (
            r"(?:يستخدم|تستخدم|لا يستخدم|لا تستخدم).{0,120}المعلومات السرية.{0,100}(?:فقط|إلا|حصراً|حصرًا)",
        ),
        "SURVIVAL_DURATION": (
            r"التزامات السرية.{0,140}(?:تستمر|تبقى|تظل)",
            r"الأسرار التجارية.{0,140}(?:تستمر|تبقى|تظل)",
        ),
        "EXCEPTIONS": (
            r"(?:لا تشمل|لا تتضمن)\s+المعلومات السرية",
            r"متاحة للجمهور",
            r"تطويرها بشكل مستقل",
            r"استلامها بشكل مشروع",
        ),
        "COMPELLED_DISCLOSURE": (
            r"(?:يقتضي القانون|بموجب أمر قضائي|إجراء قانوني|استدعاء قضائي)",
            r"الإفصاح الإلزامي",
        ),
        "REPRESENTATIVE_FLOWDOWN": (
            r"(?:الممثلين|ممثلي).{0,180}(?:التزامات السرية|بالتزام السرية)",
            r"بحاجة إلى المعرفة.{0,120}(?:الممثلين|ممثلي)",
        ),
        "NO_LICENSE": (
            r"(?:لا يمنح|لا تمنح).{0,100}ترخيص",
            r"لا يوجد ترخيص",
        ),
        "INJUNCTIVE_RELIEF": (
            r"(?:ضرر لا يمكن إصلاحه|ضرر يتعذر جبره).{0,220}(?:أمر زجري|إنصاف قضائي)",
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
            f"Missing {DETAILS}. "
            "Run the V4.1.4a exact-source post-pipeline shadow first."
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
    print("V4.1.4a CONFIDENTIALITY ABSTENTION FORENSICS")
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
        found = labels(
            source,
            language,
        )

        langs[language] += 1
        types[
            str(row.get("pipeline_clause_type") or "")
        ] += 1
        reasons[
            str(profile.get("abstention_reason") or "NONE")
        ] += 1
        signals.update(found)
        no_signal += int(not found)

        print()
        print("#" * 100)
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

    print()
    print("=" * 100)
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
