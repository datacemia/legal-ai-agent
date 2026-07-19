from pathlib import Path
import shutil

TARGET = Path(
    "app/services/contract_agent/"
    "semantic_source_profile.py"
)

BACKUP = TARGET.with_suffix(
    ".py.before_lot7b1_safe"
)

MARKER = '    _r("ACCELERATION_ON_DEFAULT",'

text = TARGET.read_text(encoding="utf-8")

if "LOT 7B-1 SAFE MULTILINGUAL COVERAGE" in text:
    raise SystemExit("PATCH ALREADY APPLIED")

if MARKER not in text:
    raise SystemExit("PATCH FAILED: marker not found")

BLOCK = r'''
    # LOT 7B-1 SAFE MULTILINGUAL COVERAGE
    #
    # New contract-agnostic legal mechanism families.
    # DOMAIN_SECONDARY + eligible=False prevents these additions
    # from displacing an already validated primary legal type.

    _r(
        "INDEPENDENT_CONTRACTOR",
        (
            (
                r"\b(?:consultant|contractor|service\s+provider)\b"
                r"[^.;!?]{0,100}"
                r"\b(?:is|acts?\s+as)\s+(?:an?\s+)?independent\s+contractor\b"
                r"[^.;!?]{0,180}"
            ),
            (
                r"\bindependent\s+contractor\b"
                r"[^.;!?]{0,140}"
                r"\bnot\s+(?:an?\s+)?"
                r"(?:employee|agent|partner|joint\s+venturer)\b"
            ),
        ),
        (
            (
                r"\b(?:consultant|prestataire|entrepreneur|contractant)\b"
                r"[^.;!?]{0,100}"
                r"\b(?:est|agit\s+en\s+qualit[eé]\s+de)\b"
                r"[^.;!?]{0,40}"
                r"\b(?:prestataire|entrepreneur|contractant)\s+ind[eé]pendant\b"
            ),
            (
                r"\b(?:prestataire|entrepreneur|contractant)\s+ind[eé]pendant\b"
                r"[^.;!?]{0,140}"
                r"\b(?:et\s+non|n['’]est\s+pas)\b"
                r"[^.;!?]{0,60}"
                r"\b(?:salari[eé]|employ[eé]|mandataire|agent|associ[eé]|"
                r"coentrepreneur)\b"
            ),
        ),
        (
            (
                r"(?:الاستشاري|المستشار|المتعاقد|المقاول|مقدم\s+الخدمات)"
                r"[^.;؛!?]{0,100}"
                r"(?:مقاول|متعاقد|مقدم\s+خدمات)\s+مستقل"
                r"[^.;؛!?]{0,180}"
            ),
            (
                r"(?:مقاول|متعاقد|مقدم\s+خدمات)\s+مستقل"
                r"[^.;؛!?]{0,140}"
                r"(?:وليس|ولا\s+يعد|ولا\s+يعتبر)"
                r"[^.;؛!?]{0,70}"
                r"(?:موظف|عامل|وكيل|شريك)"
            ),
        ),
        89,
        "employment",
        DOMAIN_SECONDARY,
        False,
        polarity="OBLIGATION",
    ),

    _r(
        "EXIT_ASSISTANCE",
        (
            (
                r"\b(?:upon|following|after)\s+"
                r"(?:expiration|expiry|termination)\b"
                r"[^.;!?]{0,120}"
                r"\b(?:provider|supplier|vendor|contractor)\b"
                r"[^.;!?]{0,80}"
                r"\b(?:shall|must|will)\s+provide\b"
                r"[^.;!?]{0,80}"
                r"\b(?:exit|transition|migration)\s+"
                r"(?:assistance|services?|support)\b"
            ),
            (
                r"\b(?:provide|perform|render)\b"
                r"[^.;!?]{0,80}"
                r"\b(?:exit|transition|migration)\s+"
                r"(?:assistance|services?|support)\b"
            ),
        ),
        (
            (
                r"\b(?:[àa]|apr[eè]s|lors\s+de)\s+"
                r"(?:l['’])?(?:expiration|[eé]ch[eé]ance|r[eé]siliation)\b"
                r"[^.;!?]{0,120}"
                r"\b(?:prestataire|fournisseur)\b"
                r"[^.;!?]{0,80}"
                r"\b(?:fournira|doit\s+fournir|devra\s+fournir)\b"
                r"[^.;!?]{0,80}"
                r"\b(?:assistance|services?|soutien)\s+"
                r"(?:[àa]\s+la\s+|de\s+)?"
                r"(?:sortie|transition|migration)\b"
            ),
            (
                r"\b(?:fournir|fournira|assurer|assurera)\b"
                r"[^.;!?]{0,80}"
                r"\b(?:assistance|services?|soutien)\s+"
                r"(?:[àa]\s+la\s+|de\s+)?"
                r"(?:sortie|transition|migration)\b"
            ),
        ),
        (
            (
                r"(?:عند|بعد)\s+(?:انتهاء|إنهاء|فسخ)"
                r"[^.;؛!?]{0,120}"
                r"(?:المزود|مقدم\s+الخدمة|المورد)"
                r"[^.;؛!?]{0,80}"
                r"(?:يقدم|يوفر|يلتزم\s+بتقديم)"
                r"[^.;؛!?]{0,80}"
                r"(?:مساعدة|خدمات|دعم)"
                r"[^.;؛!?]{0,40}"
                r"(?:الخروج|الانتقال|التحول)"
            ),
            (
                r"(?:يقدم|يوفر|تقديم)"
                r"[^.;؛!?]{0,80}"
                r"(?:مساعدة|خدمات|دعم)"
                r"[^.;؛!?]{0,40}"
                r"(?:الخروج|الانتقال|التحول)"
            ),
        ),
        91,
        "services",
        DOMAIN_SECONDARY,
        False,
        polarity="REQUIRED",
    ),

    _r(
        "TERM_DURATION",
        (
            (
                r"\b(?:initial\s+)?term\s+"
                r"(?:of\s+(?:this|the)\s+(?:agreement|contract)\s+)?"
                r"(?:is|shall\s+be|will\s+be|of)\s+"
                r"(?:approximately\s+|up\s+to\s+)?"
                r"(?:\w+(?:[-\s]\w+){0,3}\s+)?"
                r"\(\d+\)\s+(?:days?|months?|years?)\b"
            ),
            (
                r"\b(?:initial\s+)?term\s+of\s+"
                r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
                r"\s+(?:days?|months?|years?)\b"
            ),
        ),
        (
            (
                r"\b(?:dur[eé]e|p[eé]riode)\s+(?:initiale\s+)?"
                r"(?:du\s+pr[eé]sent\s+(?:accord|contrat)\s+)?"
                r"(?:est|sera|de)\s+"
                r"(?:[\wàâäéèêëîïôöùûüçœ'-]+(?:\s+[\wàâäéèêëîïôöùûüçœ'-]+){0,3}\s+)?"
                r"\(\d+\)\s+(?:jours?|mois|ans?|ann[eé]es?)\b"
            ),
            (
                r"\b(?:dur[eé]e|p[eé]riode)\s+(?:initiale\s+)?"
                r"(?:de|est|sera)\s+\d+\s+"
                r"(?:jours?|mois|ans?|ann[eé]es?)\b"
            ),
        ),
        (
            (
                r"(?:مدة|فترة)"
                r"[^.;؛!?]{0,70}"
                r"(?:الأولية|الابتدائية)?"
                r"[^.;؛!?]{0,30}"
                r"(?:[\u0621-\u064A]+(?:\s+[\u0621-\u064A]+){0,3}\s+)?"
                r"\([0-9٠-٩]+\)\s*"
                r"(?:يوماً|يومًا|يوما|يوم|أشهر|شهراً|شهرًا|شهر|"
                r"سنوات|سنة)"
            ),
            (
                r"(?:مدة|فترة)"
                r"[^.;؛!?]{0,70}"
                r"[0-9٠-٩]+\s*"
                r"(?:يوماً|يومًا|يوما|يوم|أشهر|شهراً|شهرًا|شهر|"
                r"سنوات|سنة)"
            ),
        ),
        88,
        "termination",
        DOMAIN_SECONDARY,
        False,
        polarity="DURATION",
    ),

    _r(
        "RENT_OBLIGATION",
        (
            (
                r"\b(?:tenant|lessee)\b"
                r"[^.;!?]{0,80}"
                r"\b(?:shall|must|will)\s+pay\b"
                r"[^.;!?]{0,80}"
                r"\b(?:base\s+rent|rent)\b"
            ),
            (
                r"\b(?:base\s+rent|rent)\b"
                r"[^.;!?]{0,100}"
                r"\b(?:payable|shall\s+be\s+paid|must\s+be\s+paid)\b"
            ),
        ),
        (
            (
                r"\b(?:locataire|preneur)\b"
                r"[^.;!?]{0,80}"
                r"\b(?:doit\s+payer|devra\s+payer|paiera|payera|versera)\b"
                r"[^.;!?]{0,80}"
                r"\b(?:loyer\s+de\s+base|loyer)\b"
            ),
            (
                r"\b(?:loyer\s+de\s+base|loyer)\b"
                r"[^.;!?]{0,100}"
                r"\b(?:payable|sera\s+pay[eé]|doit\s+[eê]tre\s+pay[eé])\b"
            ),
        ),
        (
            (
                r"(?:المستأجر)"
                r"[^.;؛!?]{0,80}"
                r"(?:يدفع|يسدد|يلتزم\s+بدفع|يتعين\s+عليه\s+دفع)"
                r"[^.;؛!?]{0,80}"
                r"(?:الإيجار\s+الأساسي|الأجرة\s+الأساسية|الإيجار|الأجرة)"
            ),
            (
                r"(?:الإيجار\s+الأساسي|الأجرة\s+الأساسية|الإيجار|الأجرة)"
                r"[^.;؛!?]{0,100}"
                r"(?:مستحق|واجب\s+الدفع|يدفع|يسدد)"
            ),
        ),
        92,
        "payment",
        DOMAIN_SECONDARY,
        False,
        polarity="REQUIRED",
    ),

    _r(
        "SECURITY_INTEREST",
        (
            (
                r"\b(?:borrower|debtor|grantor)\b"
                r"[^.;!?]{0,140}"
                r"\b(?:grants?|creates?|provides?)\b"
                r"[^.;!?]{0,80}"
                r"\b(?:first[-\s]priority\s+)?"
                r"(?:security\s+interest|lien|charge)\b"
                r"[^.;!?]{0,160}"
                r"\b(?:collateral|assets?|property)\b"
            ),
            (
                r"\b(?:security\s+interest|lien|charge)\b"
                r"[^.;!?]{0,160}"
                r"\b(?:collateral|assets?|property)\b"
            ),
        ),
        (
            (
                r"\b(?:emprunteur|d[eé]biteur|constituant)\b"
                r"[^.;!?]{0,140}"
                r"\b(?:consent|accorde|constitue|octroie)\b"
                r"[^.;!?]{0,80}"
                r"\b(?:s[uû]ret[eé]|nantissement|gage|hypoth[eè]que)\b"
                r"[^.;!?]{0,160}"
            ),
            (
                r"\b(?:s[uû]ret[eé]\s+de\s+premier\s+rang|"
                r"nantissement|gage|hypoth[eè]que)\b"
                r"[^.;!?]{0,180}"
            ),
        ),
        (
            (
                r"(?:المقترض|المدين|مقدم\s+الضمان)"
                r"[^.;؛!?]{0,140}"
                r"(?:يمنح|ينشئ|يقدم)"
                r"[^.;؛!?]{0,80}"
                r"(?:ضماناً|ضمانًا|ضمانا|حق\s+ضمان|رهناً|رهنًا|رهنا)"
                r"[^.;؛!?]{0,160}"
                r"(?:الضمانات|الأصول|الممتلكات)"
            ),
            (
                r"(?:ضماناً|ضمانًا|ضمانا|حق\s+ضمان|رهناً|رهنًا|رهنا)"
                r"[^.;؛!?]{0,100}"
                r"(?:ذا\s+أولوية|ذي\s+أولوية|من\s+الدرجة\s+الأولى)"
            ),
        ),
        94,
        "loan",
        DOMAIN_SECONDARY,
        False,
        polarity="RIGHT",
    ),

    _r(
        "GUARANTEE",
        (
            (
                r"\b(?:borrower['’]s?\s+)?"
                r"(?:obligations?|indebtedness|payment\s+obligations?)\b"
                r"[^.;!?]{0,120}"
                r"\b(?:is|are|shall\s+be|will\s+be)\s+guaranteed\s+by\b"
            ),
            (
                r"\b(?:guarantor|parent\s+company)\b"
                r"[^.;!?]{0,120}"
                r"\b(?:guarantees?|unconditionally\s+guarantees?)\b"
                r"[^.;!?]{0,180}"
                r"\b(?:obligations?|indebtedness|payment)\b"
            ),
        ),
        (
            (
                r"\b(?:obligations?|dette|endettement|paiement)\b"
                r"[^.;!?]{0,120}"
                r"\b(?:est|sont|sera|seront)\s+"
                r"garanti(?:e|es|s)?\s+par\b"
            ),
            (
                r"\b(?:garant|caution|soci[eé]t[eé]\s+m[eè]re)\b"
                r"[^.;!?]{0,120}"
                r"\b(?:garantit|se\s+porte\s+caution)\b"
                r"[^.;!?]{0,180}"
                r"\b(?:obligations?|dette|paiement)\b"
            ),
        ),
        (
            (
                r"(?:التزامات|ديون|مديونية|التزامات\s+السداد)"
                r"[^.;؛!?]{0,120}"
                r"(?:مضمونة\s+من\s+قبل|مضمونة\s+بواسطة|يضمنها|تكفلها)"
            ),
            (
                r"(?:الضامن|الكفيل|الشركة\s+الأم)"
                r"[^.;؛!?]{0,120}"
                r"(?:يضمن|يكفل)"
                r"[^.;؛!?]{0,180}"
                r"(?:الالتزامات|الديون|المديونية|السداد)"
            ),
        ),
        93,
        "loan",
        DOMAIN_SECONDARY,
        False,
        polarity="OBLIGATION",
    ),

'''

shutil.copy2(TARGET, BACKUP)

text = text.replace(
    MARKER,
    BLOCK + MARKER,
    1,
)

TARGET.write_text(
    text,
    encoding="utf-8",
)

print("PATCH APPLIED:", TARGET)
print("BACKUP:", BACKUP)
