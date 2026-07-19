#!/usr/bin/env python3
from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


TARGET = Path(
    "app/services/contract_agent/party_role_detector.py"
)

OLD_FUNCTION = r'''def normalize_anonymized_placeholders_to_roles(text: str, roles: dict, language: str = "en") -> str:
    language = normalize_language(language)
    family = normalize_role_family_key(roles.get("family") if isinstance(roles, dict) else "generic")

    if not isinstance(roles, dict):
        return text

    party_a = str(roles.get("party_a") or ROLE_LABELS["generic"][language][0])
    party_b = str(roles.get("party_b") or ROLE_LABELS["generic"][language][1])

    replacements = {
        "[PARTY_1]": party_a,
        "[PARTY_A]": party_a,
        "[CLIENT]": party_a,
        "[CUSTOMER]": party_a,
        "[BUYER]": party_a,
        "[LESSOR]": party_a,
        "[LANDLORD]": party_a,
        "[LENDER]": party_a,
        "[LICENSOR]": party_a,
        "[CONTROLLER]": party_a,
        "[EMPLOYER]": party_a if family == "employment" else party_a,
        "[PARTY_2]": party_b,
        "[PARTY_B]": party_b,
        "[SERVICE_PROVIDER]": party_b,
        "[PROVIDER]": party_b,
        "[SUPPLIER]": party_b,
        "[VENDOR]": party_b,
        "[SELLER]": party_b,
        "[LESSEE]": party_b,
        "[TENANT]": party_b,
        "[BORROWER]": party_b,
        "[LICENSEE]": party_b,
        "[PROCESSOR]": party_b,
        "[EMPLOYEE]": party_b if family == "employment" else party_b,
    }

    output = text
    for source, target in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        output = output.replace(source, target)

    return output
'''

NEW_BLOCK = r'''_FRENCH_FEMININE_ROLE_LABELS = {
    "partie a",
    "partie b",
    "partie divulgatrice",
    "partie réceptrice",
    "partie receptrice",
    "société",
    "societe",
}


def _french_role_is_feminine(role: str) -> bool:
    normalized = normalize_spaces(role).casefold()
    return normalized in _FRENCH_FEMININE_ROLE_LABELS


def _french_role_starts_with_vowel_sound(role: str) -> bool:
    normalized = normalize_spaces(role).casefold()
    return bool(
        normalized
        and normalized[0] in "aàâäeéèêëiîïoôöuùûüyÿœ"
    )


def _realize_french_placeholder_context(
    text: str,
    placeholder: str,
    role: str,
) -> str:
    """
    Realize a canonical French role inside the determiner/preposition context
    surrounding an anonymized placeholder.

    This is role-metadata driven and contract-family neutral. It repairs:
    - le/la agreement;
    - de + le -> du;
    - à + le -> au;
    - elision before vowel-initial role labels.

    Only placeholder contexts are rewritten. Source evidence that no longer
    contains anonymized placeholders is not recursively normalized.
    """
    escaped = re.escape(placeholder)
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
            rf"(?i)\b(?:de\s+la|de\s+le|du|de\s+l['’])\s*{escaped}",
            forms["de"],
        ),
        (
            rf"(?i)\b(?:à\s+la|a\s+la|à\s+le|a\s+le|au|à\s+l['’]|a\s+l['’])\s*{escaped}",
            forms["a"],
        ),
        (
            rf"(?i)\b(?:le|la|l['’])\s*{escaped}",
            forms["article"],
        ),
    )

    output = text

    for pattern, replacement in patterns:
        def replace_match(match):
            realized = replacement
            original = match.group(0)

            if original and original[0].isupper():
                return realized[:1].upper() + realized[1:]

            return realized

        output = re.sub(
            pattern,
            replace_match,
            output,
        )

    return output


def normalize_anonymized_placeholders_to_roles(text: str, roles: dict, language: str = "en") -> str:
    language = normalize_language(language)
    family = normalize_role_family_key(roles.get("family") if isinstance(roles, dict) else "generic")

    if not isinstance(roles, dict):
        return text

    party_a = str(roles.get("party_a") or ROLE_LABELS["generic"][language][0])
    party_b = str(roles.get("party_b") or ROLE_LABELS["generic"][language][1])

    replacements = {
        "[PARTY_1]": party_a,
        "[PARTY_A]": party_a,
        "[CLIENT]": party_a,
        "[CUSTOMER]": party_a,
        "[BUYER]": party_a,
        "[LESSOR]": party_a,
        "[LANDLORD]": party_a,
        "[LENDER]": party_a,
        "[LICENSOR]": party_a,
        "[CONTROLLER]": party_a,
        "[EMPLOYER]": party_a if family == "employment" else party_a,
        "[PARTY_2]": party_b,
        "[PARTY_B]": party_b,
        "[SERVICE_PROVIDER]": party_b,
        "[PROVIDER]": party_b,
        "[SUPPLIER]": party_b,
        "[VENDOR]": party_b,
        "[SELLER]": party_b,
        "[LESSEE]": party_b,
        "[TENANT]": party_b,
        "[BORROWER]": party_b,
        "[LICENSEE]": party_b,
        "[PROCESSOR]": party_b,
        "[EMPLOYEE]": party_b if family == "employment" else party_b,
    }

    output = text

    if language == "fr":
        for source, target in sorted(
            replacements.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        ):
            output = _realize_french_placeholder_context(
                output,
                source,
                target,
            )

    for source, target in sorted(
        replacements.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        output = output.replace(source, target)

    return output
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

    if "_realize_french_placeholder_context" in source:
        raise SystemExit(
            "ABORT: V4.1.24 placeholder realization already present"
        )

    count = source.count(OLD_FUNCTION)

    if count != 1:
        raise SystemExit(
            "ABORT: expected exactly one "
            "normalize_anonymized_placeholders_to_roles function; "
            f"found exact matches={count}"
        )

    stamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup = TARGET.with_name(
        TARGET.name
        + ".before_v4_1_24_"
        + stamp
    )

    shutil.copy2(
        TARGET,
        backup,
    )

    updated = source.replace(
        OLD_FUNCTION,
        NEW_BLOCK,
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
    print("V4.1.24 LANGUAGE-AWARE ROLE REALIZATION APPLIED")
    print("=" * 96)
    print("TARGET :", TARGET)
    print("BACKUP :", backup)
    print("A: placeholder-to-role mapping preserved")
    print("B: EN realization unchanged")
    print("C: AR realization unchanged")
    print("D: FR determiner agreement added at placeholder boundary")
    print("E: FR de+le/à+le contractions handled")
    print("F: feminine ROLE_LABELS preserved through role metadata")
    print("G: source strings without placeholders are not recursively rewritten")
    print("UNTOUCHED: PII redactor, family detector, semantic profile,")
    print("           publication gate, risk scoring, taxonomy, summary, frontend")
    print("AST: OK")
    print("=" * 96)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
