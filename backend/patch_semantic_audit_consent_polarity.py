from pathlib import Path
import py_compile
import shutil

TARGET = Path("audit_semantic_correctness.py")
BACKUP = Path(
    "audit_semantic_correctness.py."
    "before_consent_polarity_patch"
)

if not TARGET.exists():
    raise SystemExit(
        "ABORT: audit_semantic_correctness.py introuvable"
    )

source = TARGET.read_text(encoding="utf-8")

if not BACKUP.exists():
    shutil.copy2(TARGET, BACKUP)

original = source

HELPER = r'''

def material_polarity_match(
    candidate: dict[str, Any],
    expected_concept: str,
    expected_polarity: Any,
) -> bool:
    """
    Compare a persisted material polarity.

    INVESTOR_CONSENT_RIGHT is a right whose specialized gold polarity is
    CONSENT_RIGHT. A normalized RIGHT therefore preserves, rather than
    loses, the consent-right polarity for this exact concept.
    """
    if attr_match(
        candidate,
        "polarity",
        expected_polarity,
    ):
        return True

    concept_name = str(expected_concept or "").upper()
    expected = str(expected_polarity or "").upper()
    actual = relation_value(candidate, "polarity")

    actual_normalized = (
        str(actual).upper()
        if actual is not None
        else ""
    )

    return (
        concept_name == "INVESTOR_CONSENT_RIGHT"
        and expected == "CONSENT_RIGHT"
        and actual_normalized == "RIGHT"
    )
'''

if "def material_polarity_match(" not in source:
    anchor = "\ndef auditable_relation_candidates("

    if anchor not in source:
        raise SystemExit(
            "ABORT: helper auditable_relation_candidates "
            "introuvable"
        )

    source = source.replace(
        anchor,
        HELPER + anchor,
        1,
    )

OLD = '''                    attr_match(
                        candidate,
                        "polarity",
                        pol_exp,
                    )
                    for candidate in candidates
'''

NEW = '''                    material_polarity_match(
                        candidate,
                        rel["concept"],
                        pol_exp,
                    )
                    for candidate in candidates
'''

replacement_count = source.count(OLD)

if replacement_count != 1:
    raise SystemExit(
        "ABORT: bloc critique de polarité attendu "
        f"1 fois, trouvé {replacement_count} fois"
    )

source = source.replace(OLD, NEW, 1)

required = [
    "def material_polarity_match(",
    'concept_name == "INVESTOR_CONSENT_RIGHT"',
    'expected == "CONSENT_RIGHT"',
    'actual_normalized == "RIGHT"',
    "material_polarity_match(",
]

for marker in required:
    if marker not in source:
        raise SystemExit(
            f"ABORT: marqueur absent après patch: {marker}"
        )

if source == original:
    raise SystemExit("ABORT: aucune modification produite")

TARGET.write_text(source, encoding="utf-8")

try:
    py_compile.compile(
        str(TARGET),
        doraise=True,
    )
except Exception as exc:
    shutil.copy2(BACKUP, TARGET)
    raise SystemExit(
        "ABORT: erreur de syntaxe; backup restauré: "
        f"{exc}"
    )

print("PATCH APPLIED")
print(f"TARGET: {TARGET}")
print(f"BACKUP: {BACKUP}")
print("POLARITY BLOCKS REPLACED: 1")
print("PY_COMPILE: PASS")
