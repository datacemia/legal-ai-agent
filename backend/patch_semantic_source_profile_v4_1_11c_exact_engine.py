#!/usr/bin/env python3
from __future__ import annotations

import ast
from pathlib import Path

TARGET = Path("app/services/contract_agent/semantic_source_profile.py")

OLD_EVIDENCE = """def _evidence(source: str, pattern: str, label: str) -> Iterable[dict]:
    for match in re.finditer(pattern, source, re.IGNORECASE | re.DOTALL):
        yield {"label": label, "start": match.start(), "end": match.end(), "text": match.group(0)}
"""

NEW_EVIDENCE = """def _arabic_match_view_with_source_map(source: str) -> tuple[str, list[int]]:
    match_chars: list[str] = []
    source_map: list[int] = []

    for index, char in enumerate(str(source or "")):
        codepoint = ord(char)
        is_arabic_mark = (
            0x0610 <= codepoint <= 0x061A
            or 0x064B <= codepoint <= 0x065F
            or codepoint == 0x0670
            or 0x06D6 <= codepoint <= 0x06ED
        )

        if char == "\\u0640" or is_arabic_mark:
            continue

        match_chars.append(char)
        source_map.append(index)

    return "".join(match_chars), source_map


def _evidence(
    source: str,
    pattern: str,
    label: str,
    language: str | None = None,
) -> Iterable[dict]:
    if language != "ar":
        for match in re.finditer(
            pattern,
            source,
            re.IGNORECASE | re.DOTALL,
        ):
            yield {
                "label": label,
                "start": match.start(),
                "end": match.end(),
                "text": match.group(0),
            }
        return

    match_view, source_map = _arabic_match_view_with_source_map(source)

    if not match_view or not source_map:
        return

    for match in re.finditer(
        pattern,
        match_view,
        re.IGNORECASE | re.DOTALL,
    ):
        if match.end() <= match.start():
            continue

        start = source_map[match.start()]
        end = source_map[match.end() - 1] + 1

        yield {
            "label": label,
            "start": start,
            "end": end,
            "text": source[start:end],
        }
"""

OLD_CALL = "            spans.extend(_evidence(source, pattern, rule.kind))"
NEW_CALL = "            spans.extend(_evidence(source, pattern, rule.kind, lang))"

OLD_BACKGROUND = """    _r("BACKGROUND_IP_RETENTION",
       (r"\\bretains?\\b.{0,80}\\b(?:ownership\\s+of|all\\s+right,\\s+title,\\s+and\\s+interest\\s+in)\\b.{0,180}\\b(?:pre-existing|preexisting)\\b.{0,160}\\b(?:tools?|methodologies|frameworks?|know-how|intellectual\\s+property)\\b",),
       (r"\\bconserve\\b.{0,100}\\b(?:propri[eé]t[eé]|int[eé]gralit[eé]\\s+des\\s+droits)\\b.{0,180}\\b(?:pr[eé]exist\\w*)\\b.{0,160}\\b(?:m[eé]thodologies?|cadres?|savoir-faire|propri[eé]t[eé]\\s+intellectuelle)\\b",),
       (r"(?:يحتفظ|تحتفظ).{0,100}(?:بملكية|بكامل\\s+الحقوق|بجميع\\s+الحقوق).{0,220}(?:السابقة|المسبقة|سابقة).{0,160}(?:منهجيات|أطر|خبرات|ملكية\\s+فكرية)",),
       92, "intellectual_property", DOMAIN_CORE, True),
"""

NEW_BACKGROUND = """    _r("BACKGROUND_IP_RETENTION",
       (
           r"\\bretains?\\b.{0,80}\\b(?:ownership\\s+of|all\\s+right,\\s+title,\\s+and\\s+interest\\s+in)\\b.{0,260}(?:(?:pre-existing|preexisting)\\b.{0,160}\\b(?:tools?|methodologies|frameworks?|know-how|intellectual\\s+property)|(?:tools?|methodologies|frameworks?|know-how|intellectual\\s+property)\\b.{0,160}\\b(?:pre-existing|preexisting))",
       ),
       (
           r"\\bconserve\\b.{0,100}\\b(?:propri[eé]t[eé]|int[eé]gralit[eé]\\s+des\\s+droits)\\b.{0,260}(?:(?:pr[eé]exist\\w*)\\b.{0,160}\\b(?:m[eé]thodologies?|cadres?|savoir-faire|propri[eé]t[eé]\\s+intellectuelle)|(?:m[eé]thodologies?|cadres?|savoir-faire|propri[eé]t[eé]\\s+intellectuelle)\\b.{0,160}\\b(?:pr[eé]exist\\w*))",
       ),
       (
           r"(?:يحتفظ|تحتفظ).{0,120}(?:بملكية|بكامل\\s+الحقوق|بجميع\\s+الحقوق).{0,280}(?:(?:السابقة|المسبقة|سابقة).{0,180}(?:أدوات|منهجيات|أطر|خبرات|معارف|ملكية\\s+فكرية)|(?:أدوات|منهجيات|أطر|خبرات|معارف|ملكية\\s+فكرية).{0,180}(?:السابقة|المسبقة|سابقة))",
       ),
       92, "intellectual_property", DOMAIN_CORE, True),
"""


def require_exactly_once(source: str, needle: str, label: str) -> None:
    count = source.count(needle)
    if count != 1:
        raise SystemExit(
            f"ABORT: expected exactly one {label}; found {count}. "
            "No file modified."
        )


def main() -> int:
    if not TARGET.exists():
        raise SystemExit(f"ABORT: missing {TARGET}")

    source = TARGET.read_text(encoding="utf-8")

    require_exactly_once(source, OLD_EVIDENCE, "_evidence baseline block")
    require_exactly_once(source, OLD_CALL, "_evidence call-site")
    require_exactly_once(source, OLD_BACKGROUND, "BACKGROUND_IP_RETENTION rule")

    updated = source.replace(OLD_EVIDENCE, NEW_EVIDENCE, 1)
    updated = updated.replace(OLD_CALL, NEW_CALL, 1)
    updated = updated.replace(OLD_BACKGROUND, NEW_BACKGROUND, 1)

    ast.parse(updated)
    compile(updated, str(TARGET), "exec")

    backup = TARGET.with_suffix(
        TARGET.suffix + ".before_v4_1_11c_exact_engine.bak"
    )
    backup.write_text(source, encoding="utf-8")
    TARGET.write_text(updated, encoding="utf-8")

    print("PATCHED:", TARGET)
    print("BACKUP:", backup)
    print("VERIFY:")
    print("- _evidence has 4th language parameter")
    print("- Arabic normalizer is present")
    print("- extract_source_mechanisms passes lang")
    print("- BACKGROUND_IP_RETENTION is order-tolerant EN/FR/AR")
    print("- exact-source evidence invariant unchanged")
    print("SYNTAX: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
