#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import shutil
import sys


TARGET = Path(
    "app/services/contract_agent/normalized_legal_relation.py"
)


def replace_once(
    content: str,
    old: str,
    new: str,
    label: str,
) -> str:
    count = content.count(old)

    if count == 0:
        raise RuntimeError(
            f"[FAIL] Bloc introuvable : {label}"
        )

    if count > 1:
        raise RuntimeError(
            f"[FAIL] Bloc ambigu ({count} occurrences) : {label}"
        )

    return content.replace(old, new, 1)


def main() -> int:
    if not TARGET.exists():
        print(f"[FAIL] Fichier introuvable : {TARGET}")
        return 1

    original = TARGET.read_text(encoding="utf-8")
    patched = original

    # 1. Rôle EXECUTIVE multilingue EN / FR / AR
    consultant_block = '''    "CONSULTANT": (
        r"\\bconsultant\\b",
        r"\\bconsultant(?:e)?\\b",
        r"(?:الاستشاري|المستشار)",
    ),
'''

    executive_block = consultant_block + '''    "EXECUTIVE": (
        r"\\bexecutive\\b",
        r"\\bdirigeant(?:e)?\\b",
        r"(?:المدير\\s+التنفيذي|المديرة\\s+التنفيذية)",
    ),
'''

    if '"EXECUTIVE": (' not in patched:
        patched = replace_once(
            patched,
            consultant_block,
            executive_block,
            "ajout du rôle EXECUTIVE",
        )
    else:
        print("[SKIP] EXECUTIVE existe déjà")

    # 2. Stems arabes
    old_stems = '''        "استشاري",
        "مستشار",
    )
'''

    new_stems = '''        "استشاري",
        "مستشار",
        "مدير",
        "مديرة",
    )
'''

    if '"مدير",' not in patched:
        patched = replace_once(
            patched,
            old_stems,
            new_stems,
            "ajout des stems arabes EXECUTIVE",
        )
    else:
        print("[SKIP] Stems arabes EXECUTIVE déjà présents")

    # 3. Actions canoniques
    old_actions_tail = '''    "EXCLUDED_DAMAGES": "EXCLUDE_DAMAGE_CATEGORY",
}
'''

    new_actions_tail = '''    "EXCLUDED_DAMAGES": "EXCLUDE_DAMAGE_CATEGORY",
    "NON_COMPETE": "COMPETE",
    "TRANSITION_PLAN": "IMPLEMENT_TRANSITION_PLAN",
}
'''

    actions_present = (
        '"NON_COMPETE": "COMPETE"' in patched
        and '"TRANSITION_PLAN": "IMPLEMENT_TRANSITION_PLAN"' in patched
    )

    if not actions_present:
        if (
            '"NON_COMPETE": "COMPETE"' in patched
            or '"TRANSITION_PLAN": "IMPLEMENT_TRANSITION_PLAN"' in patched
        ):
            raise RuntimeError(
                "[FAIL] État partiel des actions canoniques"
            )

        patched = replace_once(
            patched,
            old_actions_tail,
            new_actions_tail,
            "ajout des actions canoniques",
        )
    else:
        print("[SKIP] Actions canoniques déjà présentes")

    # 4. Polarité NON_COMPETE
    polarity_anchor = '''    if normalized_concept == "LICENSE_RESTRICTION":
        return "PROHIBITION"
'''

    polarity_replacement = '''    if normalized_concept == "LICENSE_RESTRICTION":
        return "PROHIBITION"

    if normalized_concept == "NON_COMPETE":
        return "PROHIBITION"
'''

    non_compete_polarity = '''    if normalized_concept == "NON_COMPETE":
        return "PROHIBITION"
'''

    if non_compete_polarity not in patched:
        patched = replace_once(
            patched,
            polarity_anchor,
            polarity_replacement,
            "polarité NON_COMPETE",
        )
    else:
        print("[SKIP] Polarité NON_COMPETE déjà présente")

    # 5. Polarité TRANSITION_PLAN
    old_obligation_family = '''    if normalized_concept in {
        "SECURITY_MEASURES",
        "SERVICE_SCOPE",
        "INDEPENDENT_CONTRACTOR",
    }:
        return "OBLIGATION"
'''

    new_obligation_family = '''    if normalized_concept in {
        "SECURITY_MEASURES",
        "SERVICE_SCOPE",
        "INDEPENDENT_CONTRACTOR",
        "TRANSITION_PLAN",
    }:
        return "OBLIGATION"
'''

    if new_obligation_family not in patched:
        patched = replace_once(
            patched,
            old_obligation_family,
            new_obligation_family,
            "polarité TRANSITION_PLAN",
        )
    else:
        print("[SKIP] Polarité TRANSITION_PLAN déjà présente")

    # 6. Acteurs normalisés
    roles_anchor = '''    elif normalized_concept in {
        "SECURITY_MEASURES",
        "SERVICE_SCOPE",
    }:
'''

    roles_replacement = '''    elif normalized_concept == "NON_COMPETE":
        for candidate in (
            "EXECUTIVE",
            "CONSULTANT",
            "PROVIDER",
        ):
            if candidate in role_set:
                obligated_actor = candidate
                break

    elif normalized_concept == "TRANSITION_PLAN":
        for candidate in (
            "PROVIDER",
            "SUPPLIER",
            "PROCESSOR",
            "COMPANY",
        ):
            if candidate in role_set:
                obligated_actor = candidate
                break

    elif normalized_concept in {
        "SECURITY_MEASURES",
        "SERVICE_SCOPE",
    }:
'''

    non_compete_roles_present = (
        'elif normalized_concept == "NON_COMPETE":' in patched
    )
    transition_roles_present = (
        'elif normalized_concept == "TRANSITION_PLAN":' in patched
    )

    if not non_compete_roles_present and not transition_roles_present:
        patched = replace_once(
            patched,
            roles_anchor,
            roles_replacement,
            "rôles NON_COMPETE et TRANSITION_PLAN",
        )
    elif non_compete_roles_present and transition_roles_present:
        print("[SKIP] Branches de rôles déjà présentes")
    else:
        raise RuntimeError(
            "[FAIL] État partiel des branches de rôles"
        )

    if patched == original:
        print("[OK] Aucun changement nécessaire")
        return 0

    backup = TARGET.with_suffix(TARGET.suffix + ".bak")
    shutil.copy2(TARGET, backup)
    TARGET.write_text(patched, encoding="utf-8")

    print(f"[OK] Patch appliqué : {TARGET}")
    print(f"[OK] Sauvegarde créée : {backup}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
