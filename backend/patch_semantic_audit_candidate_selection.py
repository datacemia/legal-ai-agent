from pathlib import Path
import py_compile
import re
import shutil

TARGET = Path("audit_semantic_correctness.py")
BACKUP = Path(
    "audit_semantic_correctness.py."
    "before_candidate_selection_patch"
)

if not TARGET.exists():
    raise SystemExit(
        "ABORT: audit_semantic_correctness.py introuvable"
    )

source = TARGET.read_text(encoding="utf-8")

if not BACKUP.exists():
    shutil.copy2(TARGET, BACKUP)

original = source

# ------------------------------------------------------------------
# 1. Ajouter un helper qui exclut les mécanismes synthétiques sans
#    normalized_relation des comparaisons d'attributs.
# ------------------------------------------------------------------

HELPER = r'''

def auditable_relation_candidates(
    mechanisms: list[dict[str, Any]],
    expected_concept: str,
) -> list[dict[str, Any]]:
    """
    Return candidates that contain a usable normalized relation.

    Detector-only mechanisms remain valid for concept-presence metrics,
    but they must not produce actor/object/polarity mismatches when their
    normalized_relation is absent or empty.
    """
    selected: list[dict[str, Any]] = []

    for candidate in relation_candidates(
        mechanisms,
        expected_concept,
    ):
        relation = relation_payload(candidate)

        if not isinstance(relation, dict):
            continue

        if not any(
            value not in (None, "", [], {})
            for value in relation.values()
        ):
            continue

        selected.append(candidate)

    return selected
'''

if "def auditable_relation_candidates(" not in source:
    anchors = [
        "\ndef actual_states(",
        "\ndef actual_numeric_roles(",
        "\ndef gold_audit(",
    ]

    anchor = next(
        (value for value in anchors if value in source),
        None,
    )

    if anchor is None:
        raise SystemExit(
            "ABORT: aucun point d'insertion sûr trouvé "
            "pour auditable_relation_candidates"
        )

    source = source.replace(
        anchor,
        HELPER + anchor,
        1,
    )

# ------------------------------------------------------------------
# 2. Remplacer les appels utilisés dans les contrôles gold.
#
# Bloc réel observé :
#
# candidates = relation_candidates(
#     material,
#     rel["concept"],
# )
# ------------------------------------------------------------------

candidate_pattern = re.compile(
    r'(?P<indent>^[ \t]*)candidates = relation_candidates\(\n'
    r'(?P=indent)[ \t]+material,\n'
    r'(?P=indent)[ \t]+rel\["concept"\],\n'
    r'(?P=indent)\)',
    re.MULTILINE,
)

source, candidate_replacements = candidate_pattern.subn(
    lambda match: (
        f'{match.group("indent")}'
        f'candidates = auditable_relation_candidates(\n'
        f'{match.group("indent")}    material,\n'
        f'{match.group("indent")}    rel["concept"],\n'
        f'{match.group("indent")})'
    ),
    source,
)

if candidate_replacements == 0:
    raise SystemExit(
        "ABORT: aucun bloc relation_candidates(material, "
        'rel["concept"]) trouvé'
    )

# ------------------------------------------------------------------
# 3. Pour les échecs HIGH uniquement, reconnaître le prerequisite
#    déjà prouvé par :
#
#    INVESTOR_CONSENT_RIGHT
#    + CONSENT_REQUIRED / PRIOR_APPROVAL / PRIOR_CONSENT
#
# CONSENT_PREREQUISITE et INVESTOR_CONSENT_RIGHT restent deux concepts.
# ------------------------------------------------------------------

old_missing_block = '''        for c in sorted(required - actual_concepts):
            high.append(f"MISSING_MATERIAL_MECHANISM:{c}")
'''

new_missing_block = '''        effective_actual_concepts = set(actual_concepts)

        consent_states = {
            "CONSENT_REQUIRED",
            "PRIOR_APPROVAL",
            "PRIOR_CONSENT",
        }

        if (
            "CONSENT_PREREQUISITE" in required
            and "INVESTOR_CONSENT_RIGHT"
                in effective_actual_concepts
            and bool(states_actual & consent_states)
        ):
            effective_actual_concepts.add(
                "CONSENT_PREREQUISITE"
            )

        for c in sorted(
            required - effective_actual_concepts
        ):
            high.append(
                f"MISSING_MATERIAL_MECHANISM:{c}"
            )
'''

if old_missing_block not in source:
    raise SystemExit(
        "ABORT: bloc MISSING_MATERIAL_MECHANISM "
        "exact non trouvé"
    )

source = source.replace(
    old_missing_block,
    new_missing_block,
    1,
)

# ------------------------------------------------------------------
# 4. Empêcher un diagnostic WRONG_* lorsqu'aucune relation exploitable
#    n'existe. Le bloc actuel contient déjà `candidates and`, donc le
#    filtrage ci-dessus suffit.
# ------------------------------------------------------------------

required_markers = [
    "def auditable_relation_candidates(",
    "candidates = auditable_relation_candidates(",
    "effective_actual_concepts = set(actual_concepts)",
]

for marker in required_markers:
    if marker not in source:
        raise SystemExit(
            f"ABORT: marqueur final absent: {marker}"
        )

if source == original:
    raise SystemExit("ABORT: aucune modification produite")

TARGET.write_text(source, encoding="utf-8")

try:
    py_compile.compile(
        str(TARGET),
        doraise=True,
    )
except Exception:
    shutil.copy2(BACKUP, TARGET)
    raise SystemExit(
        "ABORT: erreur de syntaxe; backup restauré"
    )

print("PATCH APPLIED")
print(f"TARGET: {TARGET}")
print(f"BACKUP: {BACKUP}")
print(
    "RELATION CALLS REPLACED:",
    candidate_replacements,
)
print("PY_COMPILE: PASS")
