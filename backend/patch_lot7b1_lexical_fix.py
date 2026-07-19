from pathlib import Path
import shutil

TARGET = Path(
    "app/services/contract_agent/"
    "semantic_source_profile.py"
)

BACKUP = TARGET.with_suffix(
    ".py.before_lot7b1_lexical_fix"
)

text = TARGET.read_text(encoding="utf-8")

if "LOT 7B-1 LEXICAL FIX" in text:
    raise SystemExit("PATCH ALREADY APPLIED")

replacements = [
    (
        # FR EXIT_ASSISTANCE:
        # tolerate modifiers between "assistance" and "à la sortie".
        '''                r"\\b(?:fournir|fournira|assurer|assurera)\\b"
                r"[^.;!?]{0,80}"
                r"\\b(?:assistance|services?|soutien)\\s+"
                r"(?:[àa]\\s+la\\s+|de\\s+)?"
                r"(?:sortie|transition|migration)\\b"
''',
        '''                # LOT 7B-1 LEXICAL FIX — optional qualification
                # between assistance/support and exit/transition.
                r"\\b(?:fournir|fournira|assurer|assurera)\\b"
                r"[^.;!?]{0,80}"
                r"\\b(?:assistance|services?|soutien)\\b"
                r"[^.;!?]{0,50}"
                r"\\b(?:[àa]\\s+la\\s+|de\\s+)?"
                r"(?:sortie|transition|migration)\\b"
'''
    ),
    (
        # AR EXIT_ASSISTANCE:
        # tolerate subject after verb and qualification after assistance.
        '''                r"(?:يقدم|يوفر|تقديم)"
                r"[^.;؛!?]{0,80}"
                r"(?:مساعدة|خدمات|دعم)"
                r"[^.;؛!?]{0,40}"
                r"(?:الخروج|الانتقال|التحول)"
''',
        '''                # LOT 7B-1 LEXICAL FIX — verb may precede
                # the service provider; assistance may be qualified.
                r"(?:يقدم|يوفر|تقديم)"
                r"[^.;؛!?]{0,100}"
                r"(?:مساعدة|خدمات|دعم)"
                r"[^.;؛!?]{0,60}"
                r"(?:للخروج|الخروج|للانتقال|الانتقال|للتحول|التحول)"
'''
    ),
    (
        # AR RENT_OBLIGATION:
        # support verb-before-tenant and indefinite accusative rent.
        '''            (
                r"(?:الإيجار\\s+الأساسي|الأجرة\\s+الأساسية|الإيجار|الأجرة)"
                r"[^.;؛!?]{0,100}"
                r"(?:مستحق|واجب\\s+الدفع|يدفع|يسدد)"
            ),
''',
        '''            (
                r"(?:الإيجار\\s+الأساسي|الأجرة\\s+الأساسية|الإيجار|الأجرة)"
                r"[^.;؛!?]{0,100}"
                r"(?:مستحق|واجب\\s+الدفع|يدفع|يسدد)"
            ),
            # LOT 7B-1 LEXICAL FIX — payment verb may precede tenant.
            (
                r"(?:يدفع|يسدد|يؤدي)"
                r"[^.;؛!?]{0,50}"
                r"(?:المستأجر)"
                r"[^.;؛!?]{0,80}"
                r"(?:إيجار(?:اً|ًا|ا)?\\s+أساسي(?:اً|ًا|ا)?|"
                r"أجرة(?:ً|ًا|ا)?\\s+أساسية|"
                r"إيجار(?:اً|ًا|ا)?|أجرة(?:ً|ًا|ا)?)"
            ),
'''
    ),
    (
        # AR GUARANTEE:
        # support مكفولة in addition to مضمونة.
        '''                r"(?:التزامات|ديون|مديونية|التزامات\\s+السداد)"
                r"[^.;؛!?]{0,120}"
                r"(?:مضمونة\\s+من\\s+قبل|مضمونة\\s+بواسطة|يضمنها|تكفلها)"
''',
        '''                # LOT 7B-1 LEXICAL FIX — generic Arabic
                # guarantee participles: مضمونة / مكفولة.
                r"(?:التزامات|ديون|مديونية|التزامات\\s+السداد)"
                r"[^.;؛!?]{0,120}"
                r"(?:مضمونة|مكفولة)"
                r"[^.;؛!?]{0,30}"
                r"(?:من\\s+قبل|بواسطة|بـ)?"
                r"|"
                r"(?:التزامات|ديون|مديونية|التزامات\\s+السداد)"
                r"[^.;؛!?]{0,120}"
                r"(?:يضمنها|تكفلها)"
'''
    ),
]

for old, new in replacements:
    count = text.count(old)

    if count != 1:
        raise SystemExit(
            f"PATCH FAILED: expected one match, found {count}\\n"
            f"Fragment:\\n{old[:200]}"
        )

    text = text.replace(old, new, 1)

shutil.copy2(TARGET, BACKUP)
TARGET.write_text(text, encoding="utf-8")

print("PATCH APPLIED:", TARGET)
print("BACKUP:", BACKUP)
