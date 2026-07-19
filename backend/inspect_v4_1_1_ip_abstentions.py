#!/usr/bin/env python3
"""Inspect V4.1.1 intellectual-property abstentions without modifying the pipeline."""
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

ROOT = Path("semantic_profile_shadow_v4_1_1")
DETAILS = ROOT / "shadow_details.json"

TARGET_PIPELINE_TYPES = {
    "intellectual_property",
    "ownership",
    "license",
    "work_product",
}

SIGNALS = {
    "en": {
        "OWNERSHIP": (
            r"\bown(?:s|ed|ership)?\b",
            r"\btitle\b",
            r"\bproperty\b",
        ),
        "BACKGROUND_IP": (
            r"\bbackground\s+(?:ip|intellectual property)\b",
            r"\bpre-existing\b",
            r"\bpreexisting\b",
        ),
        "DELIVERABLES_WORK_PRODUCT": (
            r"\bdeliverables?\b",
            r"\bwork product\b",
            r"\bwork made for hire\b",
        ),
        "ASSIGNMENT": (
            r"\bassign(?:s|ed|ment)?\b",
            r"\btransfer(?:s|red)?\b",
        ),
        "LICENSE": (
            r"\blicen[cs]e\b",
            r"\blicen[cs]or\b",
            r"\blicen[cs]ee\b",
        ),
        "RESTRICTION": (
            r"\breverse engineer\b",
            r"\bdecompile\b",
            r"\bderivative works?\b",
            r"\bsublicen[cs]e\b",
        ),
        "NO_GRANT_OR_RETENTION": (
            r"\bno license\b",
            r"\bnothing\b.{0,80}\bgrant",
            r"\bretain(?:s|ed)?\b",
            r"\bremain(?:s|ed)?\b.{0,80}\bproperty\b",
        ),
    },
    "fr": {
        "OWNERSHIP": (
            r"\bpropri[eé]t[eé]\b",
            r"\btitularit[eé]\b",
            r"\bappartien\w*\b",
        ),
        "BACKGROUND_IP": (
            r"\bpropri[eé]t[eé] intellectuelle ant[eé]rieure\b",
            r"\bpr[eé]existant\w*\b",
            r"\bdroits? ant[eé]rieurs?\b",
        ),
        "DELIVERABLES_WORK_PRODUCT": (
            r"\blivrables?\b",
            r"\bproduit du travail\b",
            r"\bœuvre de commande\b",
        ),
        "ASSIGNMENT": (
            r"\bc[eè]d\w*\b",
            r"\btransf[eè]r\w*\b",
        ),
        "LICENSE": (
            r"\blicence\b",
            r"\blicenci[eé]\b",
        ),
        "RESTRICTION": (
            r"\bing[eé]nierie inverse\b",
            r"\bd[eé]compiler\b",
            r"\bœuvres? d[eé]riv[eé]es?\b",
            r"\bsous-licenc\w*\b",
        ),
        "NO_GRANT_OR_RETENTION": (
            r"\bn['’]accorde\b.{0,80}\blicence\b",
            r"\brien\b.{0,80}\bn['’]accorde\b",
            r"\bconserve\b",
            r"\bdemeure\b.{0,80}\bpropri[eé]t[eé]\b",
        ),
    },
    "ar": {
        "OWNERSHIP": (
            r"الملكية",
            r"ملكيتها",
            r"ملكاً|ملكًا",
        ),
        "BACKGROUND_IP": (
            r"الملكية الفكرية السابقة",
            r"الحقوق السابقة",
            r"الموجودة مسبقاً|الموجودة مسبقًا",
        ),
        "DELIVERABLES_WORK_PRODUCT": (
            r"المخرجات",
            r"نواتج العمل",
            r"عملاً بموجب طلب|عملا بموجب طلب",
        ),
        "ASSIGNMENT": (
            r"التنازل",
            r"يتنازل",
            r"تحويل",
            r"نقل",
        ),
        "LICENSE": (
            r"ترخيص",
            r"المرخص له",
            r"المرخص",
        ),
        "RESTRICTION": (
            r"الهندسة العكسية",
            r"فك التجميع",
            r"أعمال مشتقة",
            r"ترخيص من الباطن",
        ),
        "NO_GRANT_OR_RETENTION": (
            r"لا يمنح",
            r"لا تمنح",
            r"يحتفظ",
            r"تبقى.{0,80}ملكية",
        ),
    },
}


def signal_labels(text: str, language: str) -> list[str]:
    labels = []

    for label, patterns in SIGNALS.get(language, {}).items():
        if any(
            re.search(
                pattern,
                text,
                re.IGNORECASE | re.DOTALL,
            )
            for pattern in patterns
        ):
            labels.append(label)

    return labels


def main() -> int:
    if not DETAILS.exists():
        raise SystemExit(
            f"Missing {DETAILS}. "
            "Run the V4.1.1 shadow audit first."
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
        ).strip().lower()
        in TARGET_PIPELINE_TYPES
    ]

    selected.sort(
        key=lambda row: (
            str(row.get("language") or ""),
            str(row.get("document") or ""),
            str(row.get("reference") or ""),
        )
    )

    language_counts = Counter()
    pipeline_counts = Counter()
    signal_counts = Counter()
    no_signal = 0

    print("=" * 100)
    print("V4.1.1 INTELLECTUAL PROPERTY ABSTENTION FORENSICS")
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

        labels = signal_labels(
            source,
            language,
        )

        language_counts[language] += 1
        pipeline_counts[
            str(row.get("pipeline_clause_type") or "")
        ] += 1

        for label in labels:
            signal_counts[label] += 1

        if not labels:
            no_signal += 1

        print()
        print("#" * 100)
        print(f"[{index}/{len(selected)}]")
        print("LANG:", language)
        print("DOC:", row.get("document"))
        print("REF:", row.get("reference"))
        print(
            "PIPELINE:",
            row.get("pipeline_clause_type"),
        )
        print(
            "PROFILE VERSION:",
            profile.get("profile_version"),
        )
        print(
            "PRIMARY:",
            profile.get("primary_type"),
        )
        print(
            "ABSTAIN REASON:",
            profile.get("abstention_reason"),
        )
        print(
            "CANDIDATE:",
            profile.get("candidate_primary_type"),
        )
        print(
            "COVERAGE:",
            profile.get("candidate_coverage"),
        )
        print("SIGNALS:", labels)
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
    print(
        "BY LANGUAGE:",
        dict(language_counts),
    )
    print(
        "BY PIPELINE TYPE:",
        dict(pipeline_counts),
    )
    print(
        "SIGNAL COUNTS:",
        dict(signal_counts),
    )
    print(
        "NO SIGNAL ROWS:",
        no_signal,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
