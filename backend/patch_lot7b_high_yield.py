from pathlib import Path
import shutil

TARGET = Path(
    "app/services/contract_agent/semantic_source_profile.py"
)
BACKUP = TARGET.with_suffix(".py.before_lot7b_high_yield")

text = TARGET.read_text(encoding="utf-8")

MARKER = '    _r("ACCELERATION_ON_DEFAULT",'

if MARKER not in text:
    raise SystemExit(
        "PATCH FAILED: insertion marker not found"
    )

if "LOT 7B — HIGH-YIELD MULTILINGUAL FAMILIES" in text:
    raise SystemExit("PATCH ALREADY APPLIED")

BLOCK = r'''
    # LOT 7B — HIGH-YIELD MULTILINGUAL FAMILIES
    #
    # Contract-agnostic, jurisdiction-neutral normalized concepts.
    # Lexical recognition is multilingual; semantic concepts remain shared.

    _r(
        "INDEPENDENT_CONTRACTOR",
        (
            # EN
            (
                r"\b(?:independent\s+contractor|independent\s+service\s+provider)\b"
                r".{0,180}?"
                r"\b(?:not\s+(?:an?\s+)?(?:employee|agent|partner|joint\s+venturer)|"
                r"no\s+(?:employment|agency|partnership|joint\s+venture))\b"
            ),
            # FR
            (
                r"\b(?:prestataire|entrepreneur|contractant)\s+indépendant\b"
                r".{0,180}?"
                r"\b(?:n['’]est\s+pas|ne\s+constitue\s+pas|aucun\s+lien)\b"
                r".{0,80}?"
                r"\b(?:salarié|mandataire|agent|associé|coentrepreneur)\b"
            ),
            # AR
            (
                r"(?:متعاقد|مقاول|مقدم\s+خدمات)\s+مستقل"
                r".{0,180}?"
                r"(?:ليس|لا\s+يعد|لا\s+يعتبر)"
                r".{0,80}?"
                r"(?:موظف|عامل|وكيل|شريك)"
            ),
        ),
    ),

    _r(
        "EXIT_ASSISTANCE",
        (
            # EN
            (
                r"\b(?:upon|following|after)\s+"
                r"(?:expiration|termination|expiry)\b"
                r".{0,180}?"
                r"\b(?:exit|transition|migration)\s+assistance\b"
            ),
            (
                r"\b(?:provide|perform|render)\b"
                r".{0,80}?"
                r"\b(?:exit|transition|migration)\s+(?:assistance|services)\b"
            ),
            # FR
            (
                r"\b(?:à|après|lors\s+de)\s+(?:l['’])?"
                r"(?:expiration|échéance|résiliation)\b"
                r".{0,180}?"
                r"\b(?:assistance|services?)\s+(?:de\s+)?"
                r"(?:sortie|transition|migration)\b"
            ),
            # AR
            (
                r"(?:عند|بعد)\s+(?:انتهاء|إنهاء|فسخ)"
                r".{0,180}?"
                r"(?:مساعدة|خدمات)"
                r".{0,50}?"
                r"(?:الخروج|الانتقال|التحول)"
            ),
        ),
    ),

    _r(
        "TERM_DURATION",
        (
            # EN
            (
                r"\b(?:initial\s+)?term\s+(?:of|shall\s+be|is)\s+"
                r"(?:approximately\s+|up\s+to\s+)?"
                r"\d+(?:\.\d+)?\s+"
                r"(?:days?|months?|years?)\b"
            ),
            # FR
            (
                r"\b(?:durée|période)\s+(?:initiale\s+)?"
                r"(?:du\s+présent\s+\w+\s+)?"
                r"(?:est|sera|de)\s+"
                r"\d+(?:[.,]\d+)?\s+"
                r"(?:jours?|mois|ans?|années?)\b"
            ),
            # AR
            (
                r"(?:مدة|فترة)"
                r".{0,50}?"
                r"(?:الأولية|الابتدائية)?"
                r".{0,30}?"
                r"(?:\d+|[٠-٩]+)"
                r"\s*(?:يوماً|يوم|أشهر|شهراً|شهر|سنوات|سنة)"
            ),
        ),
    ),

    _r(
        "RENT_OBLIGATION",
        (
            # EN
            (
                r"\b(?:tenant|lessee)\b"
                r".{0,80}?"
                r"\b(?:shall|must|will)\s+pay\b"
                r".{0,60}?"
                r"\b(?:base\s+)?rent\b"
            ),
            # FR
            (
                r"\b(?:preneur|locataire)\b"
                r".{0,80}?"
                r"\b(?:paiera|payera|doit\s+payer|versera)\b"
                r".{0,60}?"
                r"\b(?:loyer|loyer\s+de\s+base)\b"
            ),
            # AR
            (
                r"(?:المستأجر)"
                r".{0,80}?"
                r"(?:يدفع|يسدد|يلتزم\s+بدفع)"
                r".{0,60}?"
                r"(?:الإيجار|الأجرة|بدل\s+الإيجار)"
            ),
        ),
    ),

    _r(
        "SECURITY_INTEREST",
        (
            # EN
            (
                r"\b(?:borrower|debtor|grantor)\b"
                r".{0,120}?"
                r"\b(?:grants?|creates?|provides?)\b"
                r".{0,60}?"
                r"\b(?:first[-\s]priority\s+)?"
                r"(?:security\s+interest|lien|charge)\b"
            ),
            # FR
            (
                r"\b(?:emprunteur|débiteur|constituant)\b"
                r".{0,120}?"
                r"\b(?:consent|accorde|constitue|octroie)\b"
                r".{0,60}?"
                r"\b(?:sûreté|nantissement|gage|hypothèque)\b"
            ),
            # AR
            (
                r"(?:المقترض|المدين|مقدم\s+الضمان)"
                r".{0,120}?"
                r"(?:يمنح|ينشئ|يقدم)"
                r".{0,60}?"
                r"(?:ضماناً|ضمانا|حق\s+ضمان|رهناً|رهنا)"
            ),
        ),
    ),

    _r(
        "GUARANTEE",
        (
            # EN
            (
                r"\b(?:obligations?|indebtedness|payment)\b"
                r".{0,100}?"
                r"\b(?:is|are|shall\s+be)\s+guaranteed\s+by\b"
            ),
            (
                r"\b(?:guarantor|parent\s+company)\b"
                r".{0,100}?"
                r"\b(?:guarantees?|unconditionally\s+guarantees?)\b"
            ),
            # FR
            (
                r"\b(?:obligations?|dette|paiement)\b"
                r".{0,100}?"
                r"\b(?:est|sont|sera|seront)\s+garanti(?:e|es|s)?\s+par\b"
            ),
            (
                r"\b(?:garant|caution|société\s+mère)\b"
                r".{0,100}?"
                r"\b(?:garantit|se\s+porte\s+caution)\b"
            ),
            # AR
            (
                r"(?:التزامات|ديون|سداد)"
                r".{0,100}?"
                r"(?:مضمونة|يضمنها|يكفلها)"
            ),
            (
                r"(?:الضامن|الكفيل|الشركة\s+الأم)"
                r".{0,100}?"
                r"(?:يضمن|يكفل)"
            ),
        ),
    ),

    _r(
        "DRAG_ALONG_RIGHT",
        (
            # EN
            (
                r"\b(?:drag[-\s]along|compel|require)\b"
                r".{0,120}?"
                r"\b(?:other|remaining|minority)\s+shareholders?\b"
                r".{0,100}?"
                r"\b(?:sell|transfer)\b"
            ),
            # FR
            (
                r"\b(?:droit|clause)\s+(?:de\s+)?"
                r"(?:sortie|cession)\s+forcée\b"
            ),
            (
                r"\b(?:contraindre|obliger)\b"
                r".{0,120}?"
                r"\b(?:autres?|minoritaires?)\s+actionnaires?\b"
                r".{0,100}?"
                r"\b(?:céder|vendre)\b"
            ),
            # AR
            (
                r"(?:حق|بند)"
                r".{0,30}?"
                r"(?:السحب|الجر|الإلزام\s+بالبيع|البيع\s+الإجباري)"
            ),
            (
                r"(?:إجبار|إلزام)"
                r".{0,120}?"
                r"(?:المساهمين|الشركاء)"
                r".{0,100}?"
                r"(?:بيع|نقل)"
            ),
        ),
    ),

    _r(
        "MANDATORY_PARTICIPATION",
        (
            # EN
            (
                r"\b(?:shall|must)\s+(?:participate|join|take\s+part)\b"
                r".{0,100}?"
                r"\b(?:sale|transfer|transaction)\b"
            ),
            # FR
            (
                r"\b(?:doit|devra)\s+(?:participer|prendre\s+part)\b"
                r".{0,100}?"
                r"\b(?:vente|cession|opération)\b"
            ),
            # AR
            (
                r"(?:يجب|يتعين|يلتزم)"
                r".{0,30}?"
                r"(?:بالمشاركة|المشاركة|الانضمام)"
                r".{0,100}?"
                r"(?:البيع|النقل|الصفقة)"
            ),
        ),
    ),

    _r(
        "OBLIGATION_TO_CONSENT",
        (
            # EN
            (
                r"\b(?:shall|must)\s+(?:give|provide|deliver)\b"
                r".{0,40}?"
                r"\b(?:its\s+)?consent\b"
            ),
            # FR
            (
                r"\b(?:doit|devra)\s+(?:donner|fournir|accorder)\b"
                r".{0,40}?"
                r"\b(?:son\s+)?consentement\b"
            ),
            # AR
            (
                r"(?:يجب|يتعين|يلتزم)"
                r".{0,40}?"
                r"(?:بمنح|بإعطاء|بتقديم|منح|إعطاء|تقديم)"
                r".{0,30}?"
                r"(?:موافقته|الموافقة)"
            ),
        ),
    ),

    _r(
        "OBLIGATION_TO_VOTE_IN_FAVOR",
        (
            # EN
            (
                r"\b(?:shall|must)\s+vote\b"
                r".{0,30}?"
                r"\b(?:in\s+favor|for|to\s+approve)\b"
            ),
            # FR
            (
                r"\b(?:doit|devra)\s+voter\b"
                r".{0,30}?"
                r"\b(?:en\s+faveur|pour|afin\s+d['’]approuver)\b"
            ),
            # AR
            (
                r"(?:يجب|يتعين|يلتزم)"
                r".{0,30}?"
                r"(?:بالتصويت|التصويت)"
                r".{0,30}?"
                r"(?:لصالح|بالموافقة\s+على|تأييداً|تأييدا)"
            ),
        ),
    ),

    _r(
        "PARTICIPATION_OPTION",
        (
            # EN
            (
                r"\b(?:may|shall\s+have\s+the\s+(?:option|right)\s+to)\b"
                r".{0,60}?"
                r"\b(?:participate|join)\b"
                r".{0,100}?"
                r"\b(?:sale|transfer|transaction)\b"
            ),
            # FR
            (
                r"\b(?:peut|aura\s+le\s+(?:choix|droit)\s+de)\b"
                r".{0,60}?"
                r"\b(?:participer|prendre\s+part)\b"
                r".{0,100}?"
                r"\b(?:vente|cession|opération)\b"
            ),
            # AR
            (
                r"(?:يجوز|يحق)"
                r".{0,60}?"
                r"(?:المشاركة|الانضمام)"
                r".{0,100}?"
                r"(?:البيع|النقل|الصفقة)"
            ),
        ),
    ),

    _r(
        "SAME_TERMS_RIGHT",
        (
            # EN
            (
                r"\b(?:same|identical|no\s+less\s+favorable)\s+"
                r"(?:terms|conditions)\b"
                r".{0,140}?"
                r"\b(?:sale|transfer|shares?)\b"
            ),
            # FR
            (
                r"\b(?:mêmes?|identiques?|non\s+moins\s+favorables?)\s+"
                r"(?:conditions|modalités)\b"
                r".{0,140}?"
                r"\b(?:vente|cession|actions?)\b"
            ),
            # AR
            (
                r"(?:بنفس|ذات|مماثلة)"
                r"\s*(?:الشروط|الأحكام)"
                r".{0,140}?"
                r"(?:البيع|النقل|الأسهم)"
            ),
        ),
    ),

    _r(
        "PREEMPTIVE_RIGHT",
        (
            # EN
            (
                r"\b(?:pre[-\s]?emptive\s+right|right\s+of\s+first\s+offer|"
                r"right\s+of\s+first\s+refusal)\b"
            ),
            (
                r"\bright\s+to\s+(?:subscribe|purchase)\b"
                r".{0,100}?"
                r"\b(?:pro\s+rata|newly\s+issued|new\s+shares?)\b"
            ),
            # FR
            (
                r"\b(?:droit\s+de\s+préemption|droit\s+préférentiel|"
                r"droit\s+de\s+première\s+offre|"
                r"droit\s+de\s+premier\s+refus)\b"
            ),
            (
                r"\bdroit\s+de\s+(?:souscrire|acquérir)\b"
                r".{0,100}?"
                r"\b(?:au\s+prorata|nouvelles?\s+actions?)\b"
            ),
            # AR
            (
                r"(?:حق\s+الأولوية|حق\s+الشفعة|"
                r"حق\s+العرض\s+الأول|حق\s+الرفض\s+الأول)"
            ),
            (
                r"حق"
                r".{0,30}?"
                r"(?:الاكتتاب|شراء)"
                r".{0,100}?"
                r"(?:بنسبة|تناسبياً|الأسهم\s+الجديدة)"
            ),
        ),
    ),

'''

shutil.copy2(TARGET, BACKUP)

text = text.replace(MARKER, BLOCK + MARKER, 1)
TARGET.write_text(text, encoding="utf-8")

print("PATCH APPLIED:", TARGET)
print("BACKUP:", BACKUP)
