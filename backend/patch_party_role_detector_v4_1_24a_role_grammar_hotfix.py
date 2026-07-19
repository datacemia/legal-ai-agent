#!/usr/bin/env python3
from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path(
    "app/services/contract_agent/party_role_detector.py"
)

OLD = '''def _french_role_is_feminine(role: str) -> bool:
    normalized = normalize_spaces(role).casefold()
    return normalized in _FRENCH_FEMININE_ROLE_LABELS


def _french_role_starts_with_vowel_sound(role: str) -> bool:
    normalized = normalize_spaces(role).casefold()
    return bool(
        normalized
        and normalized[0] in "aàâäeéèêëiîïoôöuùûüyÿœ"
    )
'''

NEW = '''def _normalize_role_label_for_grammar(role: str) -> str:
    return " ".join(
        str(role or "").split()
    ).casefold()


def _french_role_is_feminine(role: str) -> bool:
    normalized = _normalize_role_label_for_grammar(
        role
    )
    return normalized in _FRENCH_FEMININE_ROLE_LABELS


def _french_role_starts_with_vowel_sound(role: str) -> bool:
    normalized = _normalize_role_label_for_grammar(
        role
    )
    return bool(
        normalized
        and normalized[0] in "aàâäeéèêëiîïoôöuùûüyÿœ"
    )
'''


def main() -> int:
    if not TARGET.exists():
        raise SystemExit(
            f"TARGET NOT FOUND: {TARGET}"
        )

    source = TARGET.read_text(
        encoding="utf-8"
    )

    ast.parse(source)

    if "_normalize_role_label_for_grammar" in source:
        raise SystemExit(
            "ABORT: V4.1.24A already installed"
        )

    count = source.count(OLD)

    if count != 1:
        raise SystemExit(
            "ABORT: expected exactly one V4.1.24 "
            f"grammar helper block; found {count}"
        )

    stamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup = TARGET.with_name(
        TARGET.name
        + ".before_v4_1_24a_"
        + stamp
    )

    shutil.copy2(
        TARGET,
        backup,
    )

    updated = source.replace(
        OLD,
        NEW,
        1,
    )

    ast.parse(updated)
    compile(
        updated,
        str(TARGET),
        "exec",
    )

    TARGET.write_text(
        updated,
        encoding="utf-8",
        newline="\n",
    )

    print("=" * 96)
    print("V4.1.24A ROLE GRAMMAR NORMALIZATION HOTFIX APPLIED")
    print("=" * 96)
    print("TARGET :", TARGET)
    print("BACKUP :", backup)
    print("A: removed undefined normalize_spaces dependency")
    print("B: added local stdlib-only role-label normalization")
    print("C: FR gender/article/contraction logic unchanged")
    print("D: EN and AR realization unchanged")
    print("UNTOUCHED: PII redactor, family detector, semantic profile,")
    print("           publication gate, scoring, taxonomy, summary, frontend")
    print("AST: OK")
    print("=" * 96)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
