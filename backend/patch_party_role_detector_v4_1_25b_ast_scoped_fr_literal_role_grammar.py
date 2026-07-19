#!/usr/bin/env python3
from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path(
    "app/services/contract_agent/party_role_detector.py"
)

HELPERS = r'''
def _normalize_french_literal_role_grammar(
    text: str,
    roles: dict,
) -> str:
    """
    Normalize French determiner and preposition grammar around canonical
    literal party-role labels already present in generated text.

    The active party-role metadata is the only role vocabulary source.
    """
    if not isinstance(text, str):
        return text

    if not isinstance(roles, dict):
        return text

    party_a = str(
        roles.get("party_a")
        or ROLE_LABELS["generic"]["fr"][0]
    ).strip()

    party_b = str(
        roles.get("party_b")
        or ROLE_LABELS["generic"]["fr"][1]
    ).strip()

    output = text

    for role in sorted(
        {party_a, party_b},
        key=len,
        reverse=True,
    ):
        if not role:
            continue

        escaped = re.escape(role)
        feminine = _french_role_is_feminine(role)
        elided = _french_role_starts_with_vowel_sound(role)

        if elided:
            forms = {
                "article": f"l’{role}",
                "de": f"de l’{role}",
                "a": f"à l’{role}",
            }
        elif feminine:
            forms = {
                "article": f"la {role}",
                "de": f"de la {role}",
                "a": f"à la {role}",
            }
        else:
            forms = {
                "article": f"le {role}",
                "de": f"du {role}",
                "a": f"au {role}",
            }

        patterns = (
            (
                rf"(?i)\b(?:de\s+la|de\s+le|du|de\s+l['’])\s+{escaped}\b",
                forms["de"],
            ),
            (
                rf"(?i)\b(?:à\s+la|a\s+la|à\s+le|a\s+le|au|à\s+l['’]|a\s+l['’])\s+{escaped}\b",
                forms["a"],
            ),
            (
                rf"(?i)\b(?:le|la|l['’])\s+{escaped}\b",
                forms["article"],
            ),
        )

        for pattern, replacement in patterns:
            def replace_match(match):
                original = match.group(0)

                if original and original[0].isupper():
                    return (
                        replacement[:1].upper()
                        + replacement[1:]
                    )

                return replacement

            output = re.sub(
                pattern,
                replace_match,
                output,
            )

    return output
'''.strip()


def node_offsets(
    source: str,
    node: ast.AST,
) -> tuple[int, int]:
    lines = source.splitlines(
        keepends=True
    )

    start = sum(
        len(line)
        for line in lines[:node.lineno - 1]
    ) + node.col_offset

    end = sum(
        len(line)
        for line in lines[:node.end_lineno - 1]
    ) + node.end_col_offset

    return start, end


def main() -> int:
    if not TARGET.exists():
        raise SystemExit(
            f"TARGET NOT FOUND: {TARGET}"
        )

    source = TARGET.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(source)

    functions = {
        node.name: node
        for node in tree.body
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
    }

    if "_normalize_french_literal_role_grammar" in functions:
        raise SystemExit(
            "ABORT: V4.1.25 helper already installed"
        )

    target_fn = functions.get(
        "normalize_ai_role_words"
    )

    if target_fn is None:
        raise SystemExit(
            "ABORT: normalize_ai_role_words not found"
        )

    fn_start, fn_end = node_offsets(
        source,
        target_fn,
    )

    fn_source = source[
        fn_start:fn_end
    ]

    old_fr_branch = '''    if language == "fr":
        return _normalize_generated_role_text_fr(
            value,
            party_a,
            party_b,
        )
'''

    new_fr_branch = '''    if language == "fr":
        output = _normalize_generated_role_text_fr(
            value,
            party_a,
            party_b,
        )

        return _normalize_french_literal_role_grammar(
            output,
            roles,
        )
'''

    count = fn_source.count(
        old_fr_branch
    )

    if count != 1:
        raise SystemExit(
            "ABORT: expected exactly one FR branch "
            "inside normalize_ai_role_words; "
            f"found {count}"
        )

    updated_fn = fn_source.replace(
        old_fr_branch,
        new_fr_branch,
        1,
    )

    helper_insert_at = fn_start

    updated = (
        source[:helper_insert_at]
        + HELPERS
        + "\n\n\n"
        + updated_fn
        + source[fn_end:]
    )

    ast.parse(updated)

    compile(
        updated,
        str(TARGET),
        "exec",
    )

    stamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup = TARGET.with_name(
        TARGET.name
        + ".before_v4_1_25b_"
        + stamp
    )

    shutil.copy2(
        TARGET,
        backup,
    )

    TARGET.write_text(
        updated,
        encoding="utf-8",
        newline="\n",
    )

    print("=" * 96)
    print("V4.1.25B AST-SCOPED FR LITERAL ROLE GRAMMAR APPLIED")
    print("=" * 96)
    print("TARGET :", TARGET)
    print("BACKUP :", backup)
    print("A: helper inserted immediately before normalize_ai_role_words")
    print("B: FR branch patched inside normalize_ai_role_words only")
    print("C: placeholder realization V4.1.24/A preserved")
    print("D: EN branch unchanged")
    print("E: AR branch unchanged")
    print("F: no executive_summary/frontend changes")
    print("AST: OK")
    print("=" * 96)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
