#!/usr/bin/env python3
from __future__ import annotations

import ast
from pathlib import Path

TARGET = Path("app/services/contract_agent/semantic_source_profile.py")

# Optional Arabic combining marks/tatweel between lexical letters.
AR_MARKS = r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]*"


def arabic_literal(text: str) -> str:
    """
    Build a regex fragment tolerant to Arabic combining marks/tatweel
    between letters, while leaving the global matching engine untouched.
    """
    return AR_MARKS.join(text)


A = arabic_literal

AR_PATTERNS = {
    "BACKGROUND_IP_RETENTION": (
        rf"(?:{A('يحتفظ')}|{A('تحتفظ')}).{{0,120}}"
        rf"(?:{A('بملكية')}|{A('بكامل')}\s+{A('الحقوق')}|{A('بجميع')}\s+{A('الحقوق')}).{{0,280}}"
        rf"(?:(?:{A('السابقة')}|{A('المسبقة')}|{A('سابقة')}).{{0,180}}"
        rf"(?:{A('أدوات')}|{A('منهجيات')}|{A('أطر')}|{A('خبرات')}|{A('معارف')}|{A('ملكية')}\s+{A('فكرية')})"
        rf"|(?:{A('أدوات')}|{A('منهجيات')}|{A('أطر')}|{A('خبرات')}|{A('معارف')}|{A('ملكية')}\s+{A('فكرية')}).{{0,180}}"
        rf"(?:{A('السابقة')}|{A('المسبقة')}|{A('سابقة')}))",
    ),
    "LICENSE_GRANT": (
        rf"(?:{A('يمنح')}|{A('تمنح')}).{{0,100}}"
        rf"(?:{A('المرخص')}|{A('مانح')}\s+{A('الترخيص')}).{{0,100}}"
        rf"(?:{A('المرخص')}\s+{A('له')}|{A('العميل')}|{A('المستخدم')}).{{0,100}}"
        rf"(?:{A('ترخيص')}[اًًاا]?|{A('رخصة')}).{{0,240}}",
    ),
    "LICENSE_RESTRICTION": (
        rf"(?:{A('لا')}\s+{A('يجوز')}|{A('يحظر')}|{A('يمتنع')}).{{0,120}}"
        rf"(?:{A('المرخص')}\s+{A('له')}|{A('المستخدم')}|{A('العميل')})?.{{0,160}}"
        rf"(?:{A('هندسة')}\s+{A('عكسية')}|"
        rf"{A('فك')}\s+{A('تجميع')}|"
        rf"{A('فك')}\s+{A('الترجمة')}|"
        rf"{A('إنشاء')}\s+{A('مصنفات')}\s+{A('مشتقة')}|"
        rf"{A('إنشاء')}\s+{A('أعمال')}\s+{A('مشتقة')}|"
        rf"{A('ترخيص')}\s+{A('من')}\s+{A('الباطن')}).{{0,220}}",
    ),
    "IP_RIGHTS_RETENTION": (
        rf"(?:{A('يحتفظ')}|{A('تحتفظ')}).{{0,100}}"
        rf"(?:{A('المرخص')}|{A('مالك')}\s+{A('الحقوق')}|{A('الطرف')}).{{0,120}}"
        rf"(?:{A('بكامل')}|{A('بجميع')}).{{0,80}}"
        rf"(?:{A('الحقوق')}|{A('حقوق')}\s+{A('الملكية')}\s+{A('الفكرية')}).{{0,220}}"
        rf"(?:{A('البرنامج')}|{A('البرمجيات')}|"
        rf"{A('المادة')}\s+{A('المرخصة')}|"
        rf"{A('التعديلات')}|{A('التحسينات')})",
    ),
}


def node_offsets(source: str, node: ast.AST) -> tuple[int, int]:
    lines = source.splitlines(keepends=True)
    start = sum(len(line) for line in lines[: node.lineno - 1]) + node.col_offset
    end = sum(len(line) for line in lines[: node.end_lineno - 1]) + node.end_col_offset
    return start, end


def render_tuple(patterns: tuple[str, ...], indent: str) -> str:
    body = ",\n".join(
        f'{indent}    r"{pattern}"'
        for pattern in patterns
    )
    return "(\n" + body + ",\n" + indent + ")"


def main() -> int:
    if not TARGET.exists():
        raise SystemExit(f"ABORT: missing {TARGET}")

    source = TARGET.read_text(encoding="utf-8")

    # Hard guard: this patch must start from restored V4.1.10b-style engine.
    forbidden_markers = (
        "_arabic_match_view_with_source_map",
        "_evidence(source, pattern, rule.kind, lang)",
    )
    present = [marker for marker in forbidden_markers if marker in source]
    if present:
        raise SystemExit(
            "ABORT: global Arabic matching patch is still present: "
            + ", ".join(present)
        )

    tree = ast.parse(source)
    found: dict[str, ast.Call] = {}

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "_r":
            continue
        if len(node.args) < 4:
            continue

        kind_node = node.args[0]
        if not (
            isinstance(kind_node, ast.Constant)
            and isinstance(kind_node.value, str)
            and kind_node.value in AR_PATTERNS
        ):
            continue

        if kind_node.value in found:
            raise SystemExit(
                f"ABORT: duplicate canonical rule {kind_node.value}"
            )

        found[kind_node.value] = node

    missing = sorted(set(AR_PATTERNS) - set(found))
    if missing:
        raise SystemExit(
            "ABORT: missing canonical rules: " + ", ".join(missing)
        )

    edits: list[tuple[int, int, str]] = []

    for kind, call in found.items():
        ar_node = call.args[3]

        if not isinstance(ar_node, ast.Tuple):
            raise SystemExit(
                f"ABORT: {kind} Arabic patterns are not a literal tuple"
            )

        start, end = node_offsets(source, ar_node)
        line_start = source.rfind("\n", 0, start) + 1
        indent = source[line_start:start]

        edits.append(
            (
                start,
                end,
                render_tuple(AR_PATTERNS[kind], indent),
            )
        )

    updated = source

    for start, end, replacement in sorted(edits, reverse=True):
        updated = updated[:start] + replacement + updated[end:]

    ast.parse(updated)
    compile(updated, str(TARGET), "exec")

    backup = TARGET.with_suffix(
        TARGET.suffix + ".v4_1_10b_proven_before_ip_ar.bak"
    )
    backup.write_text(source, encoding="utf-8")
    TARGET.write_text(updated, encoding="utf-8")

    print("PATCHED:", TARGET)
    print("BACKUP:", backup)
    print("BASELINE GUARD: V4.1.10b-style global engine confirmed")
    print("CHANGED RULES:", sorted(found))
    print("SCOPE: Arabic pattern tuples only")
    print("EN/FR PATTERNS: untouched")
    print("GLOBAL MATCHING ENGINE: untouched")
    print("EXACT-SOURCE EVIDENCE: untouched")
    print("RANKS/ROLES/ELIGIBILITY/DOMINANCE: untouched")
    print("SYNTAX: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
