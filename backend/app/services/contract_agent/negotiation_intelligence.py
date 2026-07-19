"""
negotiation_intelligence.py

Universal negotiation intelligence for contract clauses.

Goals:
- Works across ANY contract type, sector, and jurisdiction, for ANY
  clause_type -- not only restrictive covenants. A small set of clause
  families (restrictive covenants: non-compete, non-solicitation,
  exclusivity) get deep, quantitative analysis (duration extraction,
  unilateral-language detection, carve-out detection). Every other
  clause_type still receives honest, generically useful negotiation
  guidance rather than being silently skipped.
- Supports EN / FR / AR, including duration expressions written in
  digits or in words in all three languages.
- Avoids absolute legal advice such as "never accept" -- both in
  wording AND in field naming.
- Uses clause characteristics, not contract-specific hardcoding.
- Purely additive when combined with the rest of the contract_agent
  stack: field names are deliberately chosen to avoid colliding with
  keys already produced by market_intelligence.py / clause_wording_library.py
  / legal_reasoning_templates.py (e.g. this module never writes to
  "market_practice", which already has a different vocabulary upstream).
"""

import re
from typing import Optional

from app.services.contract_agent.clause_wording_library import (
    get_safer_alternative,
    normalize_clause_type,
    WORDING_LIBRARY,
)


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def get_language(language: str = "en") -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


# ---------------------------------------------------------------------------
# Duration extraction (EN / FR / AR, digits and written-out numbers,
# months and years).
# ---------------------------------------------------------------------------

_MONTH_UNIT_PATTERNS = [
    # "12 months", "12 month", "12mois", "12 mois", "12 شهر" (with or
    # without a hyphen/space between the number and the unit, and
    # tolerating a redundant parenthesized digit like "12 (12) months").
    r"(\d+)\s*\(\s*\d+\s*\)\s*(?:months?|mois|شهر[ا]?ً?)",
    r"(\d+)[\s-]*(?:months?|mois|أشهر|شهر[ا]?ً?)",
    # "(12) months" / "(12) mois" with the number only inside parens,
    # e.g. "twelve (12) months".
    r"\(\s*(\d+)\s*\)\s*(?:months?|mois|شهر[ا]?ً?)",
]

_YEAR_UNIT_PATTERNS = [
    r"(\d+)\s*\(\s*\d+\s*\)\s*(?:years?|ans?|سن(?:ة|وات))",
    r"(\d+)[\s-]*(?:years?|ans?|سنوات|سنة)",
    r"\(\s*(\d+)\s*\)\s*(?:years?|ans?|سن(?:ة|وات))",
]

_WORD_NUMBERS_MONTHS = {
    "en": {
        "six": 6, "twelve": 12, "eighteen": 18,
        "twenty-four": 24, "twenty four": 24,
        "thirty-six": 36, "thirty six": 36,
    },
    "fr": {
        "six": 6, "douze": 12, "dix-huit": 18, "dix huit": 18,
        "vingt-quatre": 24, "vingt quatre": 24,
        "trente-six": 36, "trente six": 36,
    },
    "ar": {
        "ستة": 6, "ستة أشهر": 6,
        "اثني عشر": 12, "اثنا عشر": 12, "إثني عشر": 12,
        "ثمانية عشر": 18,
        "أربعة وعشرون": 24, "أربعة وعشرين": 24,
        "ستة وثلاثون": 36, "ستة وثلاثين": 36,
    },
}

_WORD_NUMBERS_YEARS = {
    "en": {"one": 1, "a": 1, "an": 1, "two": 2, "three": 3, "five": 5},
    "fr": {"un": 1, "une": 1, "deux": 2, "trois": 3, "cinq": 5},
    "ar": {
        "سنة": 1, "عام": 1,
        "سنتين": 2, "سنتان": 2, "عامين": 2,
        "ثلاث سنوات": 3, "ثلاثة أعوام": 3,
        "خمس سنوات": 5,
    },
}


def _search_unit_patterns(patterns: list, normalized: str) -> Optional[int]:
    for pattern in patterns:
        match = re.search(pattern, normalized)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                continue
    return None


def _search_word_numbers(word_map: dict, unit_markers: list, normalized: str) -> Optional[int]:
    if not any(marker in normalized for marker in unit_markers):
        return None

    for word, number in sorted(word_map.items(), key=lambda kv: -len(kv[0])):
        if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", normalized):
            return number

    return None


def extract_month_duration(text: str) -> Optional[int]:
    """
    Extract a duration in months from clause text, in EN/FR/AR, whether
    expressed in digits ("12 months", "12-month", "twelve (12) months")
    or written out in words ("twelve months", "douze mois",
    "اثني عشر شهراً"), and whether expressed in months or years (years
    are converted to months). Returns None if no duration is found --
    this is an honest, expected result for clauses with no explicit
    duration, not an error.
    """
    normalized = str(text or "").lower().strip()
    if not normalized:
        return None

    months = _search_unit_patterns(_MONTH_UNIT_PATTERNS, normalized)
    if months is not None:
        return months

    years = _search_unit_patterns(_YEAR_UNIT_PATTERNS, normalized)
    if years is not None:
        return years * 12

    month_unit_markers = ["month", "mois", "شهر", "أشهر"]
    for lang_words in _WORD_NUMBERS_MONTHS.values():
        found = _search_word_numbers(lang_words, month_unit_markers, normalized)
        if found is not None:
            return found

    year_unit_markers = ["year", "an", "ans", "سنة", "سنوات", "عام", "عامين", "سنتين", "سنتان"]
    for lang_words in _WORD_NUMBERS_YEARS.values():
        found = _search_word_numbers(lang_words, year_unit_markers, normalized)
        if found is not None:
            return found * 12

    return None


# ---------------------------------------------------------------------------
# Clause-characteristic detectors (language-agnostic signal lists).
# ---------------------------------------------------------------------------

def has_unilateral_language(text: str) -> bool:
    """
    Detects structurally unilateral/asymmetric restriction language,
    without depending on which party-role names a given contract happens
    to use. Deliberately avoids signals tied to specific role words like
    "client"/"provider" -- a contract between a Licensor/Licensee,
    Employer/Employee, Buyer/Seller, or any other pairing should be
    detected just as reliably as one that literally says "Client" and
    "Provider".
    """
    value = str(text or "").lower()

    signals = [
        "one party",
        "without a corresponding right",
        "shall not have a corresponding right",
        "no corresponding right",
        "does not have a corresponding right",
        "shall not have a corresponding restriction",
        "shall not have a corresponding obligation",
        "unilateral",
        "unilaterally",
        "sole discretion",
        "at its sole discretion",
        "one-sided",
        "une seule partie",
        "sans droit correspondant",
        "sans droit réciproque",
        "ne dispose pas d'un droit équivalent",
        "à sens unique",
        "de manière unilatérale",
        "unilatéralement",
        "seule discrétion",
        "à sa seule discrétion",
        "من جانب واحد",
        "دون حق مقابل",
        "لا يتمتع بحق مماثل",
        "بشكل أحادي",
        "منفرد",
        "وفق تقديره المطلق",
    ]

    return any(signal in value for signal in signals)


def has_carveouts(text: str) -> bool:
    value = str(text or "").lower()

    signals = [
        "except",
        "excluding",
        "provided that",
        "shall not apply",
        "carve-out",
        "carve out",
        "general recruitment",
        "public advertisement",
        "without targeting",
        "sauf",
        "à l'exception",
        "a l'exception",
        "ne s'applique pas",
        "ne s applique pas",
        "à moins que",
        "استثناء",
        "باستثناء",
        "لا ينطبق",
        "شريطة",
    ]

    return any(signal in value for signal in signals)


def is_restrictive_covenant(clause_type: str, text: str) -> bool:
    combined = f"{clause_type or ''} {text or ''}".lower()

    # "Exclusive" has two entirely unrelated legal senses: exclusive
    # jurisdiction/court competence (a standard governing-law/dispute-
    # resolution phrase, e.g. "exclusive jurisdiction of the courts",
    # "compétence exclusive des tribunaux") versus commercial
    # exclusivity (an exclusive license, exclusive distribution rights,
    # etc.). Only the latter is a genuine restrictive covenant. Strip
    # known jurisdiction-sense phrasings out before checking for the
    # exclusivity concept below, so they cannot trigger it. Confirmed
    # real bug: a governing-law clause was misclassified as a
    # commercial exclusivity restriction this way, generating a
    # completely unrelated fallback template.
    jurisdiction_sense_patterns = [
        r"exclusive jurisdiction", r"exclusive competence", r"exclusive venue",
        r"compétence exclusive", r"juridiction exclusive",
        r"اختصاص حصري", r"الاختصاص الحصري",
    ]

    for pattern in jurisdiction_sense_patterns:
        combined = re.sub(pattern, " ", combined)

    # "exclusive"/"exclusivity" need negation-aware matching: a naive
    # substring check would treat "non-exclusive" (an extremely common,
    # entirely different licensing concept -- a license explicitly
    # granted WITHOUT exclusivity) as if it were an exclusivity
    # restriction, wrongly triggering restrictive-covenant handling on
    # ordinary non-exclusive license grants. Confirmed real bug: a
    # standard "Licensor grants Licensee a non-exclusive... license"
    # clause was misclassified this way. Reuses _concept_present(),
    # which already implements this exact negation-awareness for the
    # same concept pair elsewhere in this file.
    exclusivity_variants = [
        "exclusivity", "exclusive",
        "exclusivité", "exclusif", "exclusifs", "exclusive", "exclusives",
        "الحصرية", "حصري", "حصرية",
    ]

    if _concept_present(exclusivity_variants, combined):
        return True

    signals = [
        "restrictive_covenants",
        "non-solicitation",
        "non solicitation",
        "non_solicitation",
        "non-compete",
        "non compete",
        "non_compete",
        "non-sollicitation",
        "non-concurrence",
        "عدم الاستقطاب",
        "عدم المنافسة",
        # Requirements-contract style exclusivity, common in procurement
        # and supply agreements ("Buyer shall purchase no less than 70%
        # of its requirements from Supplier") -- functionally an
        # exclusivity/minimum-commitment restriction, but drafted without
        # ever using the word "exclusive" at all, so the signals above
        # alone would miss it entirely.
        "of its requirements",
        "minimum purchase",
        "requirements contract",
        "de ses besoins",
        "exigence d'achat minimum",
        "achat minimum",
        "من احتياجاته",
        "الحد الأدنى للشراء",
    ]

    return any(signal in combined for signal in signals)


# ---------------------------------------------------------------------------
# Specialized analysis: restrictive covenants (duration-driven scoring).
# ---------------------------------------------------------------------------

def evaluate_market_practice(
    clause_type: str,
    text: str,
    language: str = "en",
) -> str:
    """
    Duration-driven market-practice label for restrictive covenants.
    Returns "" for any other clause_type (use
    generic_negotiation_market_practice() for the universal fallback).
    """
    language = get_language(language)

    if not is_restrictive_covenant(clause_type, text):
        return ""

    duration = extract_month_duration(text)
    score = 0

    if duration is None:
        score += 1
    elif duration <= 12:
        score += 0
    elif duration <= 18:
        score += 1
    elif duration <= 24:
        score += 2
    else:
        score += 3

    if has_unilateral_language(text):
        score += 1

    if not has_carveouts(text):
        score += 1

    labels = {
        "en": {
            "common": "Common",
            "negotiated": "Frequently Negotiated",
            "aggressive": "Aggressive",
            "highly_aggressive": "Highly Aggressive",
        },
        "fr": {
            "common": "Courant",
            "negotiated": "Souvent négocié",
            "aggressive": "Agressif",
            "highly_aggressive": "Très agressif",
        },
        "ar": {
            "common": "شائع",
            "negotiated": "غالباً محل تفاوض",
            "aggressive": "متشدد",
            "highly_aggressive": "متشدد جداً",
        },
    }

    if score <= 1:
        key = "common"
    elif score <= 3:
        key = "negotiated"
    elif score <= 5:
        key = "aggressive"
    else:
        key = "highly_aggressive"

    return labels[language][key]


def _restrictive_covenant_subtype(clause_type: str, text: str) -> str:
    """
    Distinguishes which kind of restrictive covenant this is, so the
    generated wording addresses the actual subject of the restriction
    rather than a one-size-fits-all template. Without this, ANY clause
    matching is_restrictive_covenant() -- including a non-compete clause
    about competing services, or a customer non-solicitation clause --
    was silently given personnel-solicitation wording, producing
    confidently wrong, off-topic text rather than just an unfilled field.

    Covers four subtypes common across any contract domain/sector:
      - non_solicitation            (personnel/employees)
      - non_solicitation_customers  (customers/clients)
      - non_compete                 (competing business/services)
      - exclusivity                 (exclusive products/territory/dealing)

    For anything that doesn't clearly match one of these -- e.g.
    non-circumvention or non-dealing clauses common in
    agency/broker/intermediary contracts, or a genuinely novel
    restriction this module has no specific template for -- returns
    "generic" rather than guessing a specific subject. A generic,
    duration-aware template that doesn't claim a false subject is safer
    than a confident but wrong one, which matters for staying correct
    across any contract type in any industry.
    """
    combined = f"{clause_type or ''} {text or ''}".lower()

    # Same jurisdiction-sense exclusion as is_restrictive_covenant()
    # above, applied here too for defense in depth.
    for pattern in [
        r"exclusive jurisdiction", r"exclusive competence", r"exclusive venue",
        r"compétence exclusive", r"juridiction exclusive",
        r"اختصاص حصري", r"الاختصاص الحصري",
    ]:
        combined = re.sub(pattern, " ", combined)

    non_compete_signals = [
        "non-compete", "non compete", "non_compete",
        "non-concurrence", "non concurrence",
        "عدم المنافسة", "قيد عدم المنافسة",
        "competitor", "competitors", "concurrent", "concurrents",
        "concurrence déloyale",
        "منافس", "منافسين", "المنافسة",
        "compete", "competing", "competitive business",
        "concurrente", "concurrentes",
    ]

    exclusivity_signals = [
        "of its requirements", "minimum purchase", "requirements contract",
        "de ses besoins", "exigence d'achat minimum", "achat minimum",
        "من احتياجاته", "الحد الأدنى للشراء",
    ]

    exclusivity_variants_for_subtype = [
        "exclusivity", "exclusive",
        "exclusivité", "exclusif", "exclusifs", "exclusive", "exclusives",
        "الحصرية", "حصري", "حصرية",
    ]

    solicitation_signals = [
        "non-solicitation", "non solicitation", "non_solicitation",
        "non-sollicitation", "non sollicitation",
        "عدم الاستقطاب", "قيد الاستقطاب",
        "solicit", "solliciter", "sollicitation", "استقطاب", "يستقطب",
    ]

    personnel_signals = [
        "personnel", "employee", "employees", "staff",
        "salarié", "salariés", "employé", "employés",
        "موظف", "موظفين", "أفراد", "عامل", "عمال",
    ]

    customer_signals = [
        "customer", "customers", "client", "clients", "clientèle",
        "عميل", "عملاء", "زبون", "زبائن",
    ]

    if any(signal in combined for signal in non_compete_signals):
        return "non_compete"

    if any(signal in combined for signal in exclusivity_signals):
        return "exclusivity"

    if _concept_present(exclusivity_variants_for_subtype, combined):
        return "exclusivity"

    has_solicitation = any(signal in combined for signal in solicitation_signals)
    has_personnel = any(signal in combined for signal in personnel_signals)
    has_customer = any(signal in combined for signal in customer_signals)

    if has_solicitation and has_personnel:
        return "non_solicitation"

    if has_solicitation and has_customer:
        return "non_solicitation_customers"

    if has_solicitation:
        return "non_solicitation"

    return "generic"


def recommended_duration_months(
    clause_type: str,
    text: str,
) -> Optional[int]:
    if not is_restrictive_covenant(clause_type, text):
        return None

    current = extract_month_duration(text)

    if current is None:
        return 12

    if current <= 12:
        return current

    if current <= 18:
        return 12

    if current <= 24:
        return 12 if has_unilateral_language(text) else 18

    return 12


_ACCEPTABLE_COMPROMISE_TEMPLATES = {
    "non_solicitation": {
        "en": "A narrower restriction limited to {months} months, defined personnel, and clear exceptions for general recruitment or non-targeted hiring.",
        "fr": "Une restriction plus étroite limitée à {months} mois, aux personnes définies, avec des exceptions claires pour le recrutement général ou non ciblé.",
        "ar": "قيد أضيق لمدة {months} شهراً، يقتصر على الأشخاص المحددين، مع استثناءات واضحة للتوظيف العام أو غير المستهدف.",
    },
    "non_solicitation_customers": {
        "en": "A narrower restriction limited to {months} months, defined customers or accounts, and clear exceptions for unsolicited or general market activity.",
        "fr": "Une restriction plus étroite limitée à {months} mois, aux clients ou comptes définis, avec des exceptions claires pour les démarches non sollicitées ou l'activité de marché générale.",
        "ar": "قيد أضيق لمدة {months} شهراً، يقتصر على العملاء أو الحسابات المحددة، مع استثناءات واضحة للأنشطة غير الموجهة أو نشاط السوق العام.",
    },
    "non_compete": {
        "en": "A narrower restriction limited to {months} months and a reduced, clearly identified list of named competitors.",
        "fr": "Une restriction plus étroite limitée à {months} mois et à une liste réduite et clairement identifiée de concurrents nommés.",
        "ar": "قيد أضيق يقتصر على {months} شهراً وقائمة مخفضة وواضحة من المنافسين المسمّين.",
    },
    "exclusivity": {
        "en": "A narrower exclusivity restriction limited to {months} months and a clearly defined scope of products, services, or territory.",
        "fr": "Une restriction d'exclusivité plus étroite limitée à {months} mois et à un périmètre clairement défini de produits, services ou territoire.",
        "ar": "قيد حصرية أضيق يقتصر على {months} شهراً ونطاق واضح ومحدد من المنتجات أو الخدمات أو الإقليم.",
    },
    "generic": {
        "en": "A narrower restriction limited to {months} months, tied to a legitimate business interest, with clear exceptions for ordinary business activity.",
        "fr": "Une restriction plus étroite limitée à {months} mois, liée à un intérêt commercial légitime, avec des exceptions claires pour l'activité commerciale ordinaire.",
        "ar": "قيد أضيق يقتصر على {months} شهراً، مرتبط بمصلحة تجارية مشروعة، مع استثناءات واضحة للنشاط التجاري الاعتيادي.",
    },
}


def generate_acceptable_compromise(
    clause_type: str,
    text: str,
    language: str = "en",
) -> str:
    language = get_language(language)

    if not is_restrictive_covenant(clause_type, text):
        return ""

    months = recommended_duration_months(clause_type, text) or 12
    subtype = _restrictive_covenant_subtype(clause_type, text)

    return _ACCEPTABLE_COMPROMISE_TEMPLATES[subtype][language].format(months=months)


def generate_negotiation_boundary(
    clause_type: str,
    text: str,
    language: str = "en",
) -> str:
    language = get_language(language)
    resolved_type = normalize_clause_type(clause_type)

    _TYPE_SPECIFIC_BOUNDARIES = {
        "force_majeure": {
            "en": "Do not accept a suspension period with no maximum duration or no eventual termination right -- require a cap (e.g. 90 days) after which either party may terminate on written notice.",
            "fr": "Ne pas accepter une période de suspension sans durée maximale ni droit de résiliation final -- exiger un plafond (par exemple 90 jours) au-delà duquel chaque partie peut résilier sur notification écrite.",
            "ar": "لا تقبل فترة تعليق دون حد أقصى للمدة أو دون حق نهائي في الإنهاء -- اشترط سقفاً زمنياً (مثلاً 90 يوماً) يحق بعده لأي طرف الإنهاء بإشعار كتابي.",
        },
        "data_privacy_security": {
            "en": "Do not accept processing instructions without a carve-out for processing legally required by applicable law, or subprocessor engagement without prior notice and an objection right.",
            "fr": "Ne pas accepter des instructions de traitement sans exception pour le traitement légalement requis par le droit applicable, ni l'engagement d'un sous-traitant sans préavis et droit d'objection.",
            "ar": "لا تقبل تعليمات معالجة بدون استثناء للمعالجة المطلوبة قانوناً بموجب القانون المعمول به، ولا الاستعانة بمعالج فرعي دون إشعار مسبق وحق اعتراض.",
        },
        "security": {
            "en": "Do not accept a generic 'appropriate measures' standard with no defined baseline -- require alignment with a named industry framework (e.g. ISO/IEC 27001, SOC 2) and periodic review.",
            "fr": "Ne pas accepter une norme générique de « mesures appropriées » sans référentiel défini -- exiger l'alignement sur un cadre sectoriel nommé (par exemple ISO/IEC 27001, SOC 2) et une revue périodique.",
            "ar": "لا تقبل معياراً عاماً لـ«التدابير المناسبة» دون خط أساس محدد -- اشترط التوافق مع إطار قطاعي معروف (مثل ISO/IEC 27001 أو SOC 2) ومراجعة دورية.",
        },
        "payment": {
            "en": "Do not accept a suspension right triggered before a meaningful cure period following undisputed non-payment, or interest terms with no cap tied to the maximum rate permitted by law.",
            "fr": "Ne pas accepter un droit de suspension déclenché avant un délai de régularisation raisonnable suivant un défaut de paiement non contesté, ni des intérêts sans plafond lié au taux maximal autorisé par la loi.",
            "ar": "لا تقبل حق تعليق يُفعَّل قبل مهلة معالجة معقولة بعد تخلف عن سداد غير متنازع عليه، ولا شروط فائدة دون سقف مرتبط بالحد الأقصى المسموح به قانوناً.",
        },
        "termination": {
            "en": "Do not accept a termination-for-cause right with no cure period, or a termination-for-convenience right granted to only one party without an equivalent notice-based right for the other.",
            "fr": "Ne pas accepter un droit de résiliation pour motif sans délai de régularisation, ni un droit de résiliation pour convenance accordé à une seule partie sans droit équivalent moyennant préavis pour l'autre.",
            "ar": "لا تقبل حق إنهاء لسبب دون مهلة معالجة، ولا حق إنهاء لغير سبب يُمنح لطرف واحد فقط دون حق مماثل بإشعار للطرف الآخر.",
        },
        "assignment": {
            "en": "Do not accept an assignment right granted to only one party without an equivalent right for the other, or an affiliate/change-of-control exception broad enough to permit assignment to an unrelated acquirer without consent.",
            "fr": "Ne pas accepter un droit de cession accordé à une seule partie sans droit équivalent pour l'autre, ni une exception affiliée/changement de contrôle assez large pour permettre une cession à un acquéreur non lié sans consentement.",
            "ar": "لا تقبل حق تنازل يُمنح لطرف واحد فقط دون حق مماثل للطرف الآخر، ولا استثناء الشركات التابعة/تغيير السيطرة الواسع بما يكفي للسماح بالتنازل لمُستحوذ غير ذي صلة دون موافقة.",
        },
        "liability": {
            "en": "Do not accept a liability cap with no carve-out for gross negligence, willful misconduct, or confidentiality breaches, or an uncapped exposure that applies to only one party while the other benefits from a cap.",
            "fr": "Ne pas accepter un plafond de responsabilité sans exception pour faute lourde, faute intentionnelle ou violation de confidentialité, ni une exposition illimitée qui ne s'applique qu'à une seule partie tandis que l'autre bénéficie d'un plafond.",
            "ar": "لا تقبل سقفاً للمسؤولية دون استثناء للإهمال الجسيم أو سوء السلوك المتعمد أو خرق السرية، ولا مسؤولية غير محدودة تُطبَّق على طرف واحد فقط بينما يستفيد الطرف الآخر من سقف.",
        },
        "notices": {
            "en": "Do not accept a notice provision with no deemed-receipt mechanism, no fallback delivery method if the primary one fails, or that requires a delivery method operationally impossible for one party (e.g. courier-only to a jurisdiction without reliable courier service).",
            "fr": "Ne pas accepter une clause de notification sans mécanisme de réception réputée, sans mode de transmission de secours en cas d'échec du mode principal, ou exigeant un mode de livraison opérationnellement impossible pour une partie (par exemple, coursier uniquement vers une juridiction sans service de coursier fiable).",
            "ar": "لا تقبل بند إشعار دون آلية استلام مفترض، ودون وسيلة تسليم احتياطية في حال فشل الوسيلة الأساسية، أو يشترط وسيلة تسليم يستحيل تنفيذها عملياً لأحد الطرفين (مثل الاعتماد فقط على البريد السريع إلى ولاية قضائية دون خدمة بريد سريع موثوقة).",
        },
        "intellectual_property": {
            "en": "Do not accept a pre-existing IP or background IP clause with no license-back for the creating party's own tools and methodologies, or a moral rights waiver broader than what is legally required.",
            "fr": "Ne pas accepter une clause de propriété intellectuelle préexistante sans licence de retour pour les outils et méthodologies propres de la partie créatrice, ni une renonciation aux droits moraux plus large que ce qui est légalement requis.",
            "ar": "لا تقبل بند ملكية فكرية سابقة دون ترخيص عودة لأدوات ومنهجيات الجهة المُنشئة الخاصة، ولا تنازلاً عن الحقوق المعنوية أوسع مما يتطلبه القانون.",
        },
        "work_product": {
            "en": "Do not accept an ownership-transfer timing that vests rights before full payment, or a comprehensive assignment with no reservation of the creating party's own background tools and reusable general know-how.",
            "fr": "Ne pas accepter un moment de transfert de propriété qui attribue les droits avant le paiement intégral, ni une cession exhaustive sans réserve pour les outils préexistants et le savoir-faire général réutilisable propres à la partie créatrice.",
            "ar": "لا تقبل توقيت نقل ملكية يمنح الحقوق قبل السداد الكامل، ولا تنازلاً شاملاً دون تحفظ لأدوات الجهة المُنشئة السابقة ومعرفتها العامة القابلة لإعادة الاستخدام.",
        },
        "confidentiality": {
            "en": "Do not accept a confidentiality obligation with no carve-outs for information already known, independently developed, or required to be disclosed by law, or a survival period with no defined end for non-trade-secret information.",
            "fr": "Ne pas accepter une obligation de confidentialité sans exceptions pour les informations déjà connues, développées indépendamment, ou dont la divulgation est requise par la loi, ni une durée de survie sans terme défini pour les informations autres que les secrets commerciaux.",
            "ar": "لا تقبل التزام سرية دون استثناءات للمعلومات المعروفة مسبقاً، أو المطورة بشكل مستقل، أو التي يشترط القانون الإفصاح عنها، ولا مدة بقاء دون نهاية محددة للمعلومات غير المصنفة كأسرار تجارية.",
        },
        "corporate_governance_committee": {
            "en": "Do not accept a review-committee mechanism with no defined meeting frequency, no escalation path for unresolved issues, or no requirement to keep written minutes.",
            "fr": "Ne pas accepter un mécanisme de comité de revue sans fréquence de réunion définie, sans voie d'escalade pour les questions non résolues, ni obligation de conserver un procès-verbal écrit.",
            "ar": "لا تقبل آلية لجنة مراجعة دون تحديد وتيرة الاجتماعات، ودون مسار تصعيد للمسائل غير المحلولة، أو دون الالتزام بالاحتفاظ بمحضر مكتوب.",
        },
        "sla": {
            "en": "Do not accept service-level commitments with no measurement methodology, no remedy for repeated or chronic failures beyond the stated service credits, or exclusions broad enough to cover most realistic outage causes.",
            "fr": "Ne pas accepter des engagements de niveau de service sans méthodologie de mesure, sans recours pour des défaillances répétées ou chroniques au-delà des crédits de service prévus, ni des exclusions assez larges pour couvrir la plupart des causes réalistes d'interruption.",
            "ar": "لا تقبل التزامات مستوى خدمة دون منهجية قياس، ودون سبيل انتصاف للأعطال المتكررة أو المزمنة يتجاوز اعتمادات الخدمة المنصوص عليها، أو استثناءات واسعة بما يكفي لتغطية معظم أسباب الانقطاع الواقعية.",
        },
    }

    if resolved_type in _TYPE_SPECIFIC_BOUNDARIES:
        return _TYPE_SPECIFIC_BOUNDARIES[resolved_type][language]

    if not is_restrictive_covenant(clause_type, text):
        return ""

    templates = {
        "en": (
            "Avoid accepting restrictions that appear disproportionate to the legitimate commercial interest, "
            "lack clear exceptions, or may raise enforceability concerns under the applicable law."
        ),
        "fr": (
            "Éviter d'accepter des restrictions qui semblent disproportionnées par rapport à l'intérêt commercial légitime, "
            "qui manquent d'exceptions claires ou qui peuvent soulever des difficultés d'applicabilité selon le droit applicable."
        ),
        "ar": (
            "ينبغي تجنب قبول القيود التي تبدو غير متناسبة مع المصلحة التجارية المشروعة، "
            "أو التي تفتقر إلى استثناءات واضحة، أو قد تثير إشكالات في قابلية التنفيذ وفقاً للقانون الواجب التطبيق."
        ),
    }

    return templates[language]


_FALLBACK_WORDING_TEMPLATES = {
    "non_solicitation": {
        "en": (
            "Neither party shall directly solicit for employment any personnel of the other party who were "
            "materially involved in the performance of this Agreement, during the Term and for {months} months "
            "thereafter, provided that this restriction shall not apply to general recruitment campaigns, public "
            "advertisements, or hiring not specifically targeted at such personnel."
        ),
        "fr": (
            "Aucune des parties ne devra solliciter directement aux fins d'embauche le personnel de l'autre partie "
            "ayant été matériellement impliqué dans l'exécution du présent Accord, pendant la durée du contrat et "
            "pendant {months} mois par la suite, sous réserve que cette restriction ne s'applique pas aux campagnes "
            "générales de recrutement, aux annonces publiques ou aux recrutements ne visant pas spécifiquement ce "
            "personnel."
        ),
        "ar": (
            "لا يجوز لأي من الطرفين أن يستقطب مباشرة لغرض التوظيف أياً من أفراد الطرف الآخر الذين شاركوا بشكل جوهري "
            "في تنفيذ هذا العقد، خلال مدة العقد ولمدة {months} شهراً بعد ذلك، على ألا ينطبق هذا القيد على حملات "
            "التوظيف العامة أو الإعلانات العامة أو التوظيف غير الموجه تحديداً إلى هؤلاء الأفراد."
        ),
    },
    "non_solicitation_customers": {
        "en": (
            "Neither party shall directly solicit any customer of the other party with whom it had material contact "
            "during the Term, for {months} months thereafter, provided that this restriction shall not apply to "
            "unsolicited approaches or general market or advertising activity not specifically targeted at such "
            "customers."
        ),
        "fr": (
            "Aucune des parties ne devra solliciter directement un client de l'autre partie avec lequel elle a eu un "
            "contact significatif pendant la durée du contrat, pendant {months} mois par la suite, sous réserve que "
            "cette restriction ne s'applique pas aux démarches non sollicitées ou à l'activité commerciale ou "
            "publicitaire générale ne visant pas spécifiquement ces clients."
        ),
        "ar": (
            "لا يجوز لأي من الطرفين أن يستقطب مباشرة أي عميل للطرف الآخر كان على تواصل جوهري معه خلال مدة العقد، "
            "ولمدة {months} شهراً بعد ذلك، على ألا ينطبق هذا القيد على المبادرات غير الموجهة أو النشاط التجاري أو "
            "الإعلاني العام غير الموجه تحديداً إلى هؤلاء العملاء."
        ),
    },
    "non_compete": {
        "en": (
            "Neither party shall knowingly engage in business that is substantially similar to the other party's "
            "business with any named direct competitor of that party, for a period of {months} months after the "
            "Term, but may seek that party's written consent to engage with a specific competitor."
        ),
        "fr": (
            "Aucune des parties ne devra exercer sciemment une activité substantiellement similaire à celle de "
            "l'autre partie avec un concurrent direct nommé de cette dernière, pendant une période de {months} mois "
            "après la durée du contrat, sous réserve de pouvoir solliciter le consentement écrit de cette partie "
            "pour un concurrent spécifique."
        ),
        "ar": (
            "لا يجوز لأي من الطرفين أن يمارس عن علم نشاطاً مماثلاً بشكل جوهري لنشاط الطرف الآخر مع أي منافس مباشر "
            "مسمّى لذلك الطرف، لمدة {months} شهراً بعد انتهاء مدة العقد، مع إمكانية طلب موافقة خطية من ذلك الطرف "
            "للتعامل مع منافس محدد."
        ),
    },
    "exclusivity": {
        "en": (
            "The exclusivity restriction shall apply for a period of {months} months, limited to the specific "
            "products, services, or territory defined in this Agreement, and shall not extend beyond the Term."
        ),
        "fr": (
            "La restriction d'exclusivité s'appliquera pour une période de {months} mois, limitée aux produits, "
            "services ou territoire spécifiquement définis dans le présent Accord, et ne s'étendra pas au-delà de la "
            "durée du contrat."
        ),
        "ar": (
            "يسري قيد الحصرية لمدة {months} شهراً، ويقتصر على المنتجات أو الخدمات أو الإقليم المحدد في هذا العقد، "
            "ولا يمتد إلى ما بعد مدة العقد."
        ),
    },
    "generic": {
        "en": (
            "The restriction shall be limited to {months} months, tied to a legitimate business interest, and "
            "include a clearly defined scope with reasonable exceptions for ordinary business activity."
        ),
        "fr": (
            "La restriction sera limitée à {months} mois, liée à un intérêt commercial légitime, et comportera un "
            "périmètre clairement défini avec des exceptions raisonnables pour l'activité commerciale ordinaire."
        ),
        "ar": (
            "يقتصر القيد على {months} شهراً، ويرتبط بمصلحة تجارية مشروعة، ويتضمن نطاقاً محدداً بوضوح مع استثناءات "
            "معقولة للنشاط التجاري الاعتيادي."
        ),
    },
}


_NUMERIC_ROLE_SIGNALS = {
    "CURE_PERIOD": [
        "cure", "cure period", "cure such breach", "remedy the breach",
        "rectify the breach", "opportunity to cure",
        "régulariser", "délai de régularisation", "remédier à la violation",
        "معالجة الإخلال", "فرصة للمعالجة", "تصحيح الإخلال",
    ],
    "NOTICE_PERIOD": [
        "notice", "written notice", "prior notice", "notification",
        "préavis", "notification écrite", "avis préalable",
        "إشعار", "إخطار كتابي", "إشعار مسبق",
    ],
    "PAYMENT_PERIOD": [
        "invoice", "payment", "due", "overdue", "non-payment",
        "facture", "paiement", "échéance", "impayé",
        "فاتورة", "دفع", "استحقاق", "متأخرات",
    ],
    "INCIDENT_NOTIFICATION_PERIOD": [
        "security incident", "breach notification", "incident report",
        "becoming aware of such incident", "personal data breach",
        "incident de sécurité", "notification de violation",
        "rapport d'incident", "violation de données",
        "حادث أمني", "إخطار بالخرق", "تقرير الحادث", "خرق البيانات",
    ],
    "OBJECTION_PERIOD": [
        "objection", "object to", "opportunity to object", "raise an objection",
        "objection", "s'opposer", "droit d'opposition",
        "اعتراض", "الاعتراض على", "فرصة للاعتراض",
    ],
    "CONFIDENTIALITY_DURATION": [
        "confidentiality", "confidential information", "survive termination",
        "survival period",
        "confidentialité", "informations confidentielles", "survivra",
        "السرية", "المعلومات السرية", "يستمر بعد الإنهاء",
    ],
    "RESTRICTIVE_COVENANT_DURATION": [
        "compete", "competitor", "solicit", "non-compete", "non-solicitation",
        "concurrence", "concurrent", "solliciter", "non-concurrence",
        "منافسة", "منافس", "استقطاب", "عدم المنافسة",
    ],
    "LIABILITY_LOOKBACK_PERIOD": [
        "aggregate liability", "months preceding the claim", "liability cap",
        "responsabilité globale", "précédant la réclamation", "plafond de responsabilité",
        "المسؤولية الإجمالية", "السابقة للمطالبة", "سقف المسؤولية",
    ],
    "INITIAL_TERM": [
        "initial term", "commence on the effective date",
        "durée initiale", "prend effet à la date",
        "المدة الأولية", "يبدأ من تاريخ السريان",
    ],
    "RENEWAL_TERM": [
        "renewal term", "successive", "automatically renew",
        "durée de renouvellement", "période successive", "se renouvelle automatiquement",
        "مدة التجديد", "متتالية", "يتجدد تلقائياً",
    ],
}

# For each role: pre-translated directional negotiation guidance in
# EN/FR/AR, or None when the favorable direction is genuinely ambiguous
# and must not be guessed (per explicit instruction: do not assume a
# longer incident-notification period is automatically favorable,
# since it trades off notification burden against affected-party
# protection in a way that depends on context this module cannot see).
_NUMERIC_ROLE_DIRECTION_TEXT = {
    "CURE_PERIOD": {
        "en": "For this term, a longer cure period gives the party in breach more time to fix the issue, while a shorter cure period gives the other party faster recourse. Choose a direction based on which party you represent.",
        "fr": "Pour ce terme, un délai de régularisation plus long laisse plus de temps à la partie en défaut pour corriger la situation, tandis qu'un délai plus court donne à l'autre partie un recours plus rapide. Choisissez une direction selon la partie que vous représentez.",
        "ar": "بالنسبة لهذا الشرط، تمنح مهلة معالجة أطول الطرف المخالف وقتاً أطول لإصلاح المشكلة، بينما تمنح مهلة أقصر الطرف الآخر إمكانية تصرف أسرع. اختر الاتجاه بناءً على الطرف الذي تمثله.",
    },
    "NOTICE_PERIOD": {
        "en": "For this term, a longer notice period gives the receiving party more time to prepare or react, while a shorter one lets the giving party act sooner. Choose a direction based on which party you represent.",
        "fr": "Pour ce terme, un préavis plus long laisse plus de temps à la partie qui le reçoit pour se préparer ou réagir, tandis qu'un préavis plus court permet à la partie qui le donne d'agir plus vite. Choisissez une direction selon la partie que vous représentez.",
        "ar": "بالنسبة لهذا الشرط، تمنح مهلة إشعار أطول الطرف المتلقي وقتاً أطول للاستعداد أو التصرف، بينما تتيح مهلة أقصر للطرف المُرسل التصرف بسرعة أكبر. اختر الاتجاه بناءً على الطرف الذي تمثله.",
    },
    "PAYMENT_PERIOD": {
        "en": "For this term, a longer payment period favors the paying party's cash flow, while a shorter one favors the receiving party's cash flow. Choose a direction based on which party you represent.",
        "fr": "Pour ce terme, un délai de paiement plus long favorise la trésorerie de la partie qui paie, tandis qu'un délai plus court favorise la trésorerie de la partie qui reçoit. Choisissez une direction selon la partie que vous représentez.",
        "ar": "بالنسبة لهذا الشرط، تخدم مدة سداد أطول التدفق النقدي للطرف الدافع، بينما تخدم مدة أقصر التدفق النقدي للطرف المستلم. اختر الاتجاه بناءً على الطرف الذي تمثله.",
    },
    "CONFIDENTIALITY_DURATION": {
        "en": "For this term, a longer survival period gives the disclosing party more lasting protection, while a shorter one gives the receiving party more freedom sooner. Choose a direction based on which party you represent.",
        "fr": "Pour ce terme, une durée de survie plus longue offre une protection plus durable à la partie divulgatrice, tandis qu'une durée plus courte donne plus de liberté à la partie réceptrice, plus tôt. Choisissez une direction selon la partie que vous représentez.",
        "ar": "بالنسبة لهذا الشرط، تمنح مدة بقاء أطول حماية أكثر ديمومة للطرف المُفصح، بينما تمنح مدة أقصر حرية أكبر للطرف المتلقي في وقت أبكر. اختر الاتجاه بناءً على الطرف الذي تمثله.",
    },
    "RESTRICTIVE_COVENANT_DURATION": {
        "en": "For this term, a longer restriction favors the party imposing it, while a shorter one favors the restricted party's freedom to operate. Choose a direction based on which party you represent.",
        "fr": "Pour ce terme, une restriction plus longue favorise la partie qui l'impose, tandis qu'une restriction plus courte favorise la liberté d'action de la partie restreinte. Choisissez une direction selon la partie que vous représentez.",
        "ar": "بالنسبة لهذا الشرط، يخدم قيد أطول الطرف الذي يفرضه، بينما يخدم قيد أقصر حرية عمل الطرف المقيَّد. اختر الاتجاه بناءً على الطرف الذي تمثله.",
    },
    "OBJECTION_PERIOD": {
        "en": "For this term, a longer objection period gives the objecting party more time to review, while a shorter one lets the other party proceed sooner. Choose a direction based on which party you represent.",
        "fr": "Pour ce terme, un délai d'objection plus long laisse plus de temps à la partie qui s'oppose pour examiner la situation, tandis qu'un délai plus court permet à l'autre partie d'avancer plus vite. Choisissez une direction selon la partie que vous représentez.",
        "ar": "بالنسبة لهذا الشرط، تمنح مهلة اعتراض أطول الطرف المعترض وقتاً أطول للمراجعة، بينما تتيح مهلة أقصر للطرف الآخر المضي قدماً بسرعة أكبر. اختر الاتجاه بناءً على الطرف الذي تمثله.",
    },
    "LIABILITY_LOOKBACK_PERIOD": {
        "en": "For this term, a longer lookback period generally increases the liability cap, while a shorter one generally decreases it. Choose a direction based on which party you represent.",
        "fr": "Pour ce terme, une période de référence plus longue augmente généralement le plafond de responsabilité, tandis qu'une période plus courte le diminue généralement. Choisissez une direction selon la partie que vous représentez.",
        "ar": "بالنسبة لهذا الشرط، تزيد فترة مرجعية أطول عادةً من سقف المسؤولية، بينما تُخفّضه فترة أقصر عادةً. اختر الاتجاه بناءً على الطرف الذي تمثله.",
    },
    "INCIDENT_NOTIFICATION_PERIOD": None,
    "INITIAL_TERM": None,
    "RENEWAL_TERM": None,
}


def classify_numeric_term_role(clause_text: str) -> str:
    """
    Classifies which semantic role a clause's numeric term most likely
    represents (NOTICE_PERIOD, CURE_PERIOD, PAYMENT_PERIOD, etc.),
    contract-agnostically, from context signals in the clause text.
    Returns "" (unclassified) rather than guessing when no signal
    clearly matches -- an honest "don't know" is safer than a
    confidently wrong role assignment.
    """
    text = str(clause_text or "").lower()

    if not text:
        return ""

    for role, signals in _NUMERIC_ROLE_SIGNALS.items():
        if any(signal in text for signal in signals):
            return role

    return ""


def extract_remedies_mechanisms(clause_text: str) -> dict:
    """
    Extracts which specific remedies mechanisms are present in a
    clause's own text, contract-agnostically, for source-aware content
    generation rather than a fully generic remedies template.

    Confirmed test-driven requirement: "The non-breaching party may
    seek injunctive relief in addition to other remedies without
    posting bond" must yield INJUNCTIVE_RELIEF_AVAILABLE,
    NON_EXCLUSIVE_REMEDIES, and NO_BOND_REQUIRED -- and generated
    negotiation content must reference at least one of them, not a
    mechanism-agnostic "clarify the scope... remedies" template.
    """
    text = str(clause_text or "").lower()
    mechanisms = {}

    if any(s in text for s in ("injunctive relief", "injonction", "إنصاف قضائي", "أمر قضائي زجري")):
        mechanisms["INJUNCTIVE_RELIEF_AVAILABLE"] = True

    if any(s in text for s in ("without posting bond", "without the necessity of posting bond", "sans constitution de garantie", "دون تقديم كفالة", "دون سند ضمان")):
        mechanisms["NO_BOND_REQUIRED"] = True

    if any(s in text for s in ("in addition to any other available remed", "in addition to other remed", "en plus de tout autre recours", "بالإضافة إلى أي سبل انتصاف أخرى")):
        mechanisms["NON_EXCLUSIVE_REMEDIES"] = True

    if any(s in text for s in ("sole and exclusive remedy", "sole remedy", "exclusive remedy", "seul et unique recours", "سبيل الانتصاف الوحيد")):
        mechanisms["EXCLUSIVE_REMEDY"] = True

    return mechanisms


def generate_remedies_specific_content(clause_text: str, language: str = "en") -> str:
    """
    Builds fallback-wording content referencing the SPECIFIC remedies
    mechanisms actually present in the clause (injunctive relief, bond
    waiver, remedy exclusivity/non-exclusivity), rather than the fully
    generic "clarify the scope, objective standards..." template that
    applies identically to any clause type. Returns "" when no
    recognized mechanism is present, so the honest generic fallback is
    used instead of fabricating specificity that isn't there.
    """
    mechanisms = extract_remedies_mechanisms(clause_text)

    if not mechanisms:
        return ""

    parts_en = []
    parts_fr = []
    parts_ar = []

    if "INJUNCTIVE_RELIEF_AVAILABLE" in mechanisms:
        parts_en.append("confirm injunctive relief remains available without requiring proof of irreparable harm beyond what is already stated")
        parts_fr.append("confirmer que le recours à une injonction reste disponible sans exiger une preuve de préjudice irréparable au-delà de ce qui est déjà énoncé")
        parts_ar.append("تأكيد استمرار توفر الإنصاف القضائي دون اشتراط إثبات ضرر يتعذر تداركه يتجاوز ما هو منصوص عليه بالفعل")

    if "NO_BOND_REQUIRED" in mechanisms:
        parts_en.append("preserve the bond waiver so the non-breaching party is not required to post security to obtain injunctive relief")
        parts_fr.append("préserver la dispense de garantie afin que la partie non défaillante ne soit pas tenue de constituer une caution pour obtenir une injonction")
        parts_ar.append("الإبقاء على الإعفاء من الكفالة بحيث لا يُلزم الطرف غير المخالف بتقديم ضمان للحصول على الإنصاف القضائي")

    if "NON_EXCLUSIVE_REMEDIES" in mechanisms:
        parts_en.append("keep the listed remedies expressly non-exclusive of any other remedy available at law or equity")
        parts_fr.append("maintenir le caractère expressément non exclusif des recours énumérés par rapport à tout autre recours disponible en droit ou en équité")
        parts_ar.append("الحفاظ على الطابع غير الحصري صراحة لسبل الانتصاف المذكورة بالنسبة لأي سبيل انتصاف آخر متاح بموجب القانون أو مبادئ العدالة")
    elif "EXCLUSIVE_REMEDY" in mechanisms:
        parts_en.append("confirm whether this remedy is intended to be the sole and exclusive remedy, or whether other remedies remain available")
        parts_fr.append("confirmer si ce recours est destiné à être le seul et unique recours, ou si d'autres recours restent disponibles")
        parts_ar.append("تأكيد ما إذا كان هذا السبيل مقصوداً ليكون سبيل الانتصاف الوحيد والحصري، أو ما إذا كانت سبل انتصاف أخرى لا تزال متاحة")

    _templates = {
        "en": f"A safer alternative is to {', '.join(parts_en)}.",
        "fr": f"Une alternative plus sûre consiste à {', '.join(parts_fr)}.",
        "ar": f"البديل الأكثر أماناً هو {'، '.join(parts_ar)}.",
    }

    return _templates.get(language, _templates["en"])


def extract_governing_law_forum(clause_text: str) -> dict:
    """
    Extracts the actual named governing law and forum/jurisdiction from
    a clause's own text, contract-agnostically, for source-aware
    content generation.

    Confirmed test-driven requirement: a clause naming "Delaware law"
    and "exclusive jurisdiction of courts in Wilmington, Delaware" must
    not receive generic "specify governing law and forum" advice --
    the actual named law and forum should be referenced.
    """
    text = str(clause_text or "")
    result = {}

    law_match = re.search(
        r"(?:laws? of|lois de|قوانين)\s+(?:the\s+)?(?:State\s+of\s+|l'[EÉ]tat\s+d[eu]\s+)?([A-ZÀ-Ü][\w\s,]{2,40}?)(?:,|\.|\s+without|\s+sans|$)",
        text,
    )
    if not law_match:
        law_match = re.search(
            r"\bgoverned by\s+([A-ZÀ-Ü][\w\s]{2,30}?)\s+laws?\b",
            text,
        )
    if law_match:
        result["GOVERNING_LAW"] = law_match.group(1).strip()

    exclusivity = bool(re.search(r"exclusive jurisdiction|juridiction exclusive|اختصاص حصري", text, re.IGNORECASE))
    if exclusivity:
        result["JURISDICTION_EXCLUSIVITY"] = "EXCLUSIVE"

    forum_match = re.search(
        r"courts? located in\s+([\w\s,]{2,40}?)(?:\.|,\s|$)|tribunaux (?:de|situés à)\s+([\w\s,]{2,40}?)(?:\.|,\s|$)",
        text,
        re.IGNORECASE,
    )
    if not forum_match:
        forum_match = re.search(
            r"courts?\s+in\s+([\w\s,]{2,40}?)(?:\.|$)",
            text,
            re.IGNORECASE,
        )
    if forum_match:
        result["FORUM_LOCATION"] = (forum_match.group(1) or (forum_match.group(2) if forum_match.lastindex and forum_match.lastindex >= 2 else "")).strip()

    return result


def generate_governing_law_specific_content(clause_text: str, language: str = "en") -> str:
    """
    Builds fallback-wording content referencing the ACTUAL named
    governing law and forum extracted from the clause, rather than the
    fully generic "specify governing law, forum, dispute escalation
    steps..." template. Returns "" when no specific law/forum can be
    extracted, so the honest generic fallback is used instead.
    """
    extracted = extract_governing_law_forum(clause_text)

    if not extracted.get("GOVERNING_LAW") and not extracted.get("FORUM_LOCATION"):
        return ""

    law = extracted.get("GOVERNING_LAW", "")
    forum = extracted.get("FORUM_LOCATION", "")
    is_exclusive = extracted.get("JURISDICTION_EXCLUSIVITY") == "EXCLUSIVE"

    _templates = {
        "en": (
            f"A safer alternative is to confirm that {law or 'the named governing law'} remains the agreed governing law, and "
            + (f"to consider whether the exclusive jurisdiction of courts in {forum} is acceptable to both parties or whether a non-exclusive or neutral forum would be preferable." if is_exclusive and forum
               else f"to confirm the forum in {forum} remains acceptable to both parties." if forum
               else "to confirm the forum remains acceptable to both parties.")
        ),
        "fr": (
            f"Une alternative plus sûre consiste à confirmer que le droit de {law or 'la juridiction nommée'} demeure le droit applicable convenu, et "
            + (f"à examiner si la compétence exclusive des tribunaux de {forum} est acceptable pour les deux parties ou si un for non exclusif ou neutre serait préférable." if is_exclusive and forum
               else f"à confirmer que le for de {forum} demeure acceptable pour les deux parties." if forum
               else "à confirmer que le for demeure acceptable pour les deux parties.")
        ),
        "ar": (
            f"البديل الأكثر أماناً هو تأكيد أن قانون {law or 'الجهة المذكورة'} يظل القانون الواجب التطبيق المتفق عليه، و"
            + (f"النظر فيما إذا كان الاختصاص الحصري لمحاكم {forum} مقبولاً لكلا الطرفين أو ما إذا كان اختصاص غير حصري أو محايد أفضل." if is_exclusive and forum
               else f"تأكيد أن مقر التقاضي في {forum} يظل مقبولاً لكلا الطرفين." if forum
               else "تأكيد أن مقر التقاضي يظل مقبولاً لكلا الطرفين.")
        ),
    }

    return _templates.get(language, _templates["en"])


def extract_warranty_mechanisms(clause_text: str) -> dict:
    """
    Extracts which specific mechanisms a warranty/disclaimer-type
    clause actually discusses, contract-agnostically, so generated
    content can reference the SPECIFIC ones present instead of a
    generic "state warranties precisely..." template that doesn't
    reflect a clause that is really about license/ownership/warranty
    disclaimers combined.

    Confirmed real gap: "Nothing in this Agreement grants any license
    or ownership interest in the Confidential Information. All
    Confidential Information is provided 'as is' without warranty of
    any kind" discusses THREE distinct mechanisms (no license grant, no
    ownership transfer, warranty disclaimer/as-is), but the generic
    warranty template references none of them by name.
    """
    text = str(clause_text or "").lower()
    mechanisms = {}

    if any(s in text for s in ("no license", "not grant any license", "grants any license", "aucune licence", "n'accorde aucune licence", "accorde de licence", "لا يمنح أي ترخيص")):
        mechanisms["NO_LICENSE_GRANT"] = True

    if any(s in text for s in ("no ownership interest", "ownership interest in", "aucun droit de propriété", "transfère de droit de propriété", "droit de propriété", "أي حق ملكية")):
        mechanisms["NO_OWNERSHIP_TRANSFER"] = True

    if any(s in text for s in ('"as is"', "as is", "without warranty", "en l'état", "sans garantie", "كما هي", "دون أي ضمان", "دون ضمان")):
        mechanisms["WARRANTY_DISCLAIMER_AS_IS"] = True

    return mechanisms


def generate_warranty_specific_content(clause_text: str, language: str = "en") -> str:
    """
    Builds fallback-wording content referencing the SPECIFIC mechanisms
    actually present in a warranty-type clause (no license grant, no
    ownership transfer, as-is/warranty disclaimer), rather than the
    fully generic "state warranties precisely, define their duration..."
    template that applies identically regardless of what the clause
    actually says. Returns "" when no recognized mechanism is present,
    so the honest generic fallback is used instead of fabricating
    specificity that isn't there.
    """
    mechanisms = extract_warranty_mechanisms(clause_text)

    if not mechanisms:
        return ""

    parts_en = []
    parts_fr = []
    parts_ar = []

    if "NO_LICENSE_GRANT" in mechanisms:
        parts_en.append("preserve the express statement that no license is granted, while identifying any limited use of the information that is strictly necessary for the stated purpose")
        parts_fr.append("préserver l'énoncé exprès selon lequel aucune licence n'est accordée, tout en identifiant tout usage limité de l'information strictement nécessaire à la finalité énoncée")
        parts_ar.append("الحفاظ على النص الصريح بعدم منح أي ترخيص، مع تحديد أي استخدام محدود للمعلومات يكون ضرورياً بشكل صارم للغرض المنصوص عليه")

    if "NO_OWNERSHIP_TRANSFER" in mechanisms:
        parts_en.append("preserve the express statement that no ownership interest is transferred, while clarifying which party retains ownership of any underlying materials or intellectual property")
        parts_fr.append("préserver l'énoncé exprès selon lequel aucun droit de propriété n'est transféré, tout en précisant quelle partie conserve la propriété des éléments sous-jacents ou de la propriété intellectuelle")
        parts_ar.append("الحفاظ على النص الصريح بعدم نقل أي حق ملكية، مع توضيح الطرف الذي يحتفظ بملكية أي مواد أساسية أو ملكية فكرية")

    if "WARRANTY_DISCLAIMER_AS_IS" in mechanisms:
        parts_en.append("consider carving out a baseline warranty (e.g. that the disclosing party has the right to share the information) rather than a fully unqualified 'as is' disclaimer")
        parts_fr.append("envisager de prévoir une garantie minimale (par exemple, que la partie divulgatrice dispose du droit de partager l'information) plutôt qu'une exonération totalement inconditionnelle « en l'état »")
        parts_ar.append("النظر في تضمين ضمان أساسي (مثل امتلاك الطرف المُفصح الحق في مشاركة المعلومات) بدلاً من إخلاء مسؤولية غير مشروط بالكامل على أساس \"كما هي\"")

    _templates = {
        "en": f"A safer alternative is to {', and '.join(parts_en)}.",
        "fr": f"Une alternative plus sûre consiste à {', et à '.join(parts_fr)}.",
        "ar": f"البديل الأكثر أماناً هو {'، و'.join(parts_ar)}.",
    }

    return _templates.get(language, _templates["en"])


def generate_mechanism_driven_acceptable_compromise(
    clause_text: str,
    clause_type: str,
    language: str = "en",
) -> str:
    """
    Generates acceptable_compromise content from the SAME extracted
    mechanism profile that already feeds generate_warranty_specific_
    content() / generate_remedies_specific_content() /
    generate_governing_law_specific_content() for fallback_wording --
    closing the gap where acceptable_compromise previously had no
    connection to mechanism extraction at all, relying only on numeric-
    role classification. Returns "" when no mechanism can be extracted
    for this clause_type, so the honest generic fallback is used
    instead of fabricating specificity that isn't there.

    Follows: SOURCE MECHANISM STATE -> NEGOTIABLE DIMENSION ->
    CONTROLLED ALTERNATIVE. Does not assume any position is universally
    preferable; describes the trade-off rather than picking a side when
    the represented party is unknown.
    """
    resolved_type = normalize_clause_type(str(clause_type or ""))
    parts_en, parts_fr, parts_ar = [], [], []

    if resolved_type == "warranty":
        mechanisms = extract_warranty_mechanisms(clause_text)

        if "NO_LICENSE_GRANT" in mechanisms:
            parts_en.append("preserve the no-license position while expressly identifying any limited use of the information that is strictly necessary for the stated contractual purpose")
            parts_fr.append("préserver la position de non-octroi de licence tout en identifiant expressément tout usage limité de l'information strictement nécessaire à la finalité contractuelle énoncée")
            parts_ar.append("الحفاظ على موقف عدم منح الترخيص مع تحديد أي استخدام محدود للمعلومات يكون ضرورياً بشكل صارم للغرض التعاقدي المنصوص عليه")

        if "NO_OWNERSHIP_TRANSFER" in mechanisms:
            parts_en.append("preserve existing ownership while clarifying the rights strictly necessary to use an agreed deliverable or piece of information")
            parts_fr.append("préserver la propriété existante tout en précisant les droits strictement nécessaires à l'utilisation d'un livrable ou d'une information convenue")
            parts_ar.append("الحفاظ على الملكية القائمة مع توضيح الحقوق الضرورية بشكل صارم لاستخدام مُخرَج أو معلومة متفق عليها")

        if "WARRANTY_DISCLAIMER_AS_IS" in mechanisms:
            parts_en.append("preserve the disclaimer while identifying any expressly negotiated representation (e.g. the disclosing party's authority to share the information) that should remain outside the disclaimer's scope")
            parts_fr.append("préserver l'exonération tout en identifiant toute déclaration expressément négociée (par exemple, le pouvoir de la partie divulgatrice de partager l'information) devant rester hors du champ de l'exonération")
            parts_ar.append("الحفاظ على إخلاء المسؤولية مع تحديد أي إقرار متفاوض عليه صراحة (مثل صلاحية الطرف المُفصح لمشاركة المعلومات) ينبغي أن يبقى خارج نطاق إخلاء المسؤولية")

    elif resolved_type == "remedies":
        mechanisms = extract_remedies_mechanisms(clause_text)

        if "INJUNCTIVE_RELIEF_AVAILABLE" in mechanisms:
            parts_en.append("preserve access to injunctive relief while identifying whether any procedural condition, bond treatment, or cumulative-remedy language remains negotiable")
            parts_fr.append("préserver l'accès à l'injonction tout en déterminant si une condition procédurale, un traitement de la caution, ou une formulation de recours cumulatifs reste négociable")
            parts_ar.append("الحفاظ على إمكانية الحصول على الإنصاف القضائي مع تحديد ما إذا كان أي شرط إجرائي أو معاملة الكفالة أو صياغة سبل الانتصاف التراكمية لا تزال قابلة للتفاوض")

        if "EXCLUSIVE_REMEDY" in mechanisms and "NON_EXCLUSIVE_REMEDIES" not in mechanisms:
            parts_en.append("confirm whether the exclusive-remedy structure should remain exclusive, or whether identified additional remedies should be preserved alongside it")
            parts_fr.append("confirmer si la structure de recours exclusif doit le rester, ou si des recours supplémentaires identifiés doivent être préservés en complément")
            parts_ar.append("تأكيد ما إذا كان يجب أن تبقى بنية سبيل الانتصاف الحصري كما هي، أو ما إذا كان ينبغي الحفاظ على سبل انتصاف إضافية محددة إلى جانبها")

    elif resolved_type in ("governing_law", "dispute_resolution"):
        extracted = extract_governing_law_forum(clause_text)

        if extracted.get("GOVERNING_LAW"):
            law = extracted["GOVERNING_LAW"]
            if extracted.get("JURISDICTION_EXCLUSIVITY") == "EXCLUSIVE":
                parts_en.append(f"preserve {law} as the governing-law framework while negotiating whether the forum should remain exclusive or whether a non-exclusive or neutral forum mechanism would be acceptable to both parties")
                parts_fr.append(f"préserver le droit de {law} comme cadre juridique applicable tout en négociant si le for doit rester exclusif ou si un mécanisme de for non exclusif ou neutre serait acceptable pour les deux parties")
                parts_ar.append(f"الحفاظ على قانون {law} كإطار قانوني واجب التطبيق مع التفاوض حول ما إذا كان ينبغي أن يبقى الاختصاص القضائي حصرياً أو ما إذا كانت آلية اختصاص غير حصري أو محايد ستكون مقبولة لكلا الطرفين")
            else:
                parts_en.append(f"preserve {law} as the governing-law framework while confirming the forum mechanism is objectively identified and acceptable to both parties")
                parts_fr.append(f"préserver le droit de {law} comme cadre juridique applicable tout en confirmant que le mécanisme de for est objectivement identifié et acceptable pour les deux parties")
                parts_ar.append(f"الحفاظ على قانون {law} كإطار قانوني واجب التطبيق مع التأكد من أن آلية الاختصاص محددة بشكل موضوعي ومقبولة لكلا الطرفين")

    if not parts_en:
        return ""

    _join_en = ", while also identifying whether to "
    _join_fr = ", tout en déterminant également s'il convient de "
    _join_ar = "، مع تحديد ما إذا كان ينبغي أيضاً "

    _templates = {
        "en": f"A source-derived compromise is to {_join_en.join(parts_en) if len(parts_en) > 1 else parts_en[0]}.",
        "fr": f"Un compromis fondé sur la source consiste à {_join_fr.join(parts_fr) if len(parts_fr) > 1 else parts_fr[0]}.",
        "ar": f"تسوية مستندة إلى المصدر تتمثل في {_join_ar.join(parts_ar) if len(parts_ar) > 1 else parts_ar[0]}.",
    }

    return _templates.get(language, _templates["en"])


_MECHANISM_BOUNDARY_TEXT = {
    "NO_LICENSE_GRANT": {
        "en": "Do not accept generated wording that introduces an implied or unrestricted use right beyond the no-license position the source expressly states.",
        "fr": "Ne pas accepter une formulation générée qui introduit un droit d'utilisation implicite ou non restreint au-delà de la position de non-octroi de licence expressément énoncée par la source.",
        "ar": "لا تقبل صياغة مُولّدة تُدخل حق استخدام ضمني أو غير مقيد يتجاوز موقف عدم منح الترخيص المنصوص عليه صراحة في المصدر.",
    },
    "NO_OWNERSHIP_TRANSFER": {
        "en": "Do not accept generated wording that transfers background or pre-existing rights beyond the no-transfer position the source expressly states.",
        "fr": "Ne pas accepter une formulation générée qui transfère des droits préexistants au-delà de la position de non-transfert expressément énoncée par la source.",
        "ar": "لا تقبل صياغة مُولّدة تنقل حقوقاً سابقة أو أساسية تتجاوز موقف عدم النقل المنصوص عليه صراحة في المصدر.",
    },
    "WARRANTY_DISCLAIMER_AS_IS": {
        "en": "Do not accept generated wording that silently introduces a broad affirmative warranty the source's disclaimer does not support.",
        "fr": "Ne pas accepter une formulation générée qui introduit silencieusement une garantie affirmative étendue que l'exonération de la source ne prévoit pas.",
        "ar": "لا تقبل صياغة مُولّدة تُدخل ضمناً ضماناً إيجابياً واسعاً لا يدعمه إخلاء المسؤولية المنصوص عليه في المصدر.",
    },
    "NON_EXCLUSIVE_REMEDIES": {
        "en": "Do not accept generated wording that converts the source's non-exclusive remedies into an exclusive remedy without explicit negotiation.",
        "fr": "Ne pas accepter une formulation générée qui transforme les recours non exclusifs de la source en un recours exclusif sans négociation explicite.",
        "ar": "لا تقبل صياغة مُولّدة تُحوّل سبل الانتصاف غير الحصرية في المصدر إلى سبيل انتصاف حصري دون تفاوض صريح.",
    },
    "NO_BOND_REQUIRED": {
        "en": "Do not accept generated wording that introduces a mandatory bond as a prerequisite to equitable relief where the source expressly waives that requirement.",
        "fr": "Ne pas accepter une formulation générée qui introduit une caution obligatoire comme condition préalable à un recours en équité alors que la source y renonce expressément.",
        "ar": "لا تقبل صياغة مُولّدة تُدخل كفالة إلزامية كشرط مسبق للانتصاف العادل بينما يتنازل المصدر صراحة عن هذا الشرط.",
    },
    "JURISDICTION_EXCLUSIVITY": {
        "en": "Do not accept generated wording that changes the forum-selection mechanism without clearly identifying which party's jurisdictional position is being altered.",
        "fr": "Ne pas accepter une formulation générée qui modifie le mécanisme de sélection du for sans identifier clairement la position juridictionnelle de quelle partie est modifiée.",
        "ar": "لا تقبل صياغة مُولّدة تُغيّر آلية اختيار الاختصاص القضائي دون تحديد واضح لموقف أي طرف يجري تعديله.",
    },
}


_RIGHT_VERBS_WITH_OBJECT = [
    r"owns?", r"shall own", r"retains?\s+ownership\s+of", r"licenses?", r"licensing",
    r"assigns?", r"transfers?\s+ownership\s+of", r"grants?\s+a\s+license\s+to\s+use",

    r"poss[èe]de", r"détient\s+la\s+propriété\s+de", r"conc[èe]de\s+une\s+licence\s+sur", r"licence",
    r"cède", r"transf[èe]re\s+la\s+propriété\s+de",

    r"يملك", r"يحتفظ\s+بملكية", r"يمنح\s+ترخيصاً\s+ل",
    r"يُحيل", r"ينقل\s+ملكية",
]

_PARTY_ROLE_WORDS = [
    "client", "provider", "supplier", "vendor", "buyer", "seller",
    "licensor", "licensee", "employer", "employee", "lessor", "lessee",
    "landlord", "tenant", "borrower", "lender", "guarantor",
    "party a", "party b", "the parties", "assignor", "assignee",
    "disclosing party", "receiving party",
    "the relevant party", "the other party", "either party", "that party",

    "client", "prestataire", "fournisseur", "acheteur", "vendeur",
    "concédant", "concessionnaire", "employeur", "employé",
    "bailleur", "locataire", "emprunteur", "prêteur",
    "la partie concernée", "l'autre partie", "cette partie",

    "العميل", "مقدم الخدمة", "المورد", "المشتري", "البائع",
    "المرخِّص", "المرخَّص له", "صاحب العمل", "الموظف",
    "المؤجر", "المستأجر", "المقترض", "المقرض",
    "الطرف المعني", "الطرف الآخر", "ذلك الطرف",
]


def validate_semantic_object_sanity(text: str) -> str:
    """
    Catches generated text where a legal right's verb (owns/licenses/
    assigns) has a bare PARTY as its direct object rather than an
    asset -- a clearly malformed construction regardless of contract
    domain (e.g. "Licensor owns Licensee" instead of "Licensor owns the
    Software", or "licensing of the relevant party" instead of
    "licensing of the relevant technology"). This is a narrow, well-
    defined safety net for one failure mode (party-as-object), not a
    complete semantic-role validation system.

    Returns a description of the malformed pattern found, or "" if
    none is found. A right-verb followed by "to"/"by"/"from" + a party
    (marking the party as a RECIPIENT or SOURCE, not the object being
    owned/licensed) is correctly NOT flagged.
    """
    if not text:
        return ""

    text_lower = str(text).lower()

    for verb_pattern in _RIGHT_VERBS_WITH_OBJECT:
        for party_word in _PARTY_ROLE_WORDS:
            # Direct object: verb immediately followed by the party
            # word (optionally via "of"/"de"/"من" or an article/
            # possessive), and NOT preceded by "to"/"by"/"from" right
            # before the party word, which would mark it as a
            # recipient/source instead of the thing being owned/
            # licensed/assigned.
            pattern = rf"\b{verb_pattern}\s+(?!to\s|by\s|from\s|à\s|par\s|من\s|إلى\s|ل)(of\s+|de\s+|the\s+|its\s+|their\s+|le\s+|la\s+|les\s+|son\s+|sa\s+|ses\s+|ال)?{re.escape(party_word)}\b"
            match = re.search(pattern, text_lower)
            if match:
                return f"party_as_object: '{match.group(0).strip()}'"

    return ""


def generate_mechanism_driven_negotiation_boundary(
    clause_text: str,
    clause_type: str,
    language: str = "en",
) -> str:
    """
    Generates negotiation_boundary content from the SAME extracted
    mechanism profile used for fallback_wording, following LEGAL
    MECHANISM -> MATERIAL FAILURE MODE -> BOUNDARY. Returns "" when no
    mechanism can be extracted, so the honest generic boundary is used
    instead. Deliberately avoids "standard market practice" / "industry
    standard" style phrasing, since no configured playbook or verified
    benchmark backs such claims here -- boundaries are phrased as
    concrete failure modes tied to the source's own mechanism instead.
    """
    resolved_type = normalize_clause_type(str(clause_type or ""))
    found_mechanisms = []

    if resolved_type == "warranty":
        found_mechanisms = list(extract_warranty_mechanisms(clause_text).keys())
    elif resolved_type == "remedies":
        remedies_mechanisms = extract_remedies_mechanisms(clause_text)
        found_mechanisms = [m for m in remedies_mechanisms if m in _MECHANISM_BOUNDARY_TEXT]
    elif resolved_type in ("governing_law", "dispute_resolution"):
        extracted = extract_governing_law_forum(clause_text)
        if extracted.get("JURISDICTION_EXCLUSIVITY"):
            found_mechanisms = ["JURISDICTION_EXCLUSIVITY"]

    for mechanism in found_mechanisms:
        if mechanism in _MECHANISM_BOUNDARY_TEXT:
            return _MECHANISM_BOUNDARY_TEXT[mechanism].get(
                language, _MECHANISM_BOUNDARY_TEXT[mechanism]["en"]
            )

    return ""


def numeric_role_direction_guidance(role: str, language: str = "en") -> str:
    """
    Returns pre-translated directional negotiation guidance for a
    classified numeric role (which side longer/shorter favors), or an
    empty string when the role is unclassified or its direction is
    genuinely ambiguous (per _NUMERIC_ROLE_DIRECTION_TEXT) -- callers
    must treat an empty result as "abstain", not as license to invent a
    generic numeric range.
    """
    per_language = _NUMERIC_ROLE_DIRECTION_TEXT.get(role)

    if not per_language:
        return ""

    return per_language.get(language, per_language["en"])


def _corporate_governance_subtype(text: str) -> str:
    """
    Distinguishes board/shareholder governance matters from operational
    review-committee/recurring-meeting mechanisms, since these are
    substantively different subjects that previously shared the same
    board-composition-focused template regardless of which one a given
    clause actually addresses.

    Confirmed real gap: a clause establishing "a joint security
    governance committee, meeting quarterly, to review incident trends"
    was matched to corporate_governance (a reasonable top-level type)
    but then received wording about board composition, appointment
    rights, and deadlock resolution -- none of which addresses the
    clause's actual subject: meeting cadence, attendees, agenda, and
    escalation for an operational review committee.

    Returns "board" (the existing template's actual subject) or
    "committee" (the operational review-meeting subject needing its
    own template). Defaults to "board" when no clear committee/meeting
    signal is present, preserving prior behavior for genuine
    board/shareholder clauses.
    """
    combined = str(text or "").lower()

    committee_signals = [
        "review meeting", "review committee", "joint committee",
        "steering committee", "working committee", "meet quarterly",
        "meeting quarterly", "meet monthly", "meeting monthly",
        "meet annually", "meeting annually", "meet semi-annually",
        "review incident", "review performance", "review trends",
        "action items", "meeting minutes", "escalation procedure",

        "réunion de revue", "comité de revue", "comité conjoint",
        "comité de pilotage", "se réunir trimestriellement",
        "réunion trimestrielle", "se réunir mensuellement",
        "examiner les tendances", "examiner la performance",
        "points d'action", "procès-verbal de réunion",
        "procédure d'escalade",

        "اجتماع مراجعة", "لجنة مراجعة", "لجنة مشتركة", "لجنة توجيهية",
        "ربع سنوي", "اجتماع شهري", "تجتمع شهرياً", "مراجعة الاتجاهات",
        "مراجعة الأداء", "بنود العمل", "محضر الاجتماع", "إجراء التصعيد",
    ]

    board_signals = [
        "board composition", "board of directors", "appointment rights",
        "reserved matters", "deadlock", "voting rights", "quorum",
        "shareholder approval", "shareholder consent",

        "composition du conseil", "conseil d'administration",
        "droits de nomination", "matières réservées", "impasse",
        "droits de vote", "quorum", "approbation des actionnaires",

        "تكوين مجلس الإدارة", "مجلس الإدارة", "حقوق التعيين",
        "المسائل المحفوظة", "طريق مسدود", "حقوق التصويت", "النصاب",
        "موافقة المساهمين",
    ]

    if any(signal in combined for signal in committee_signals):
        return "committee"

    if any(signal in combined for signal in board_signals):
        return "board"

    return "board"


def _confidentiality_subtype(text: str) -> str:
    """
    Distinguishes which sub-topic of confidentiality a clause addresses,
    so fallback wording addresses the actual subject rather than a
    one-size-fits-all confidentiality template. Common in NDAs and
    confidentiality sections that split these into separate numbered
    sub-clauses:

      - duration        (survival period, post-termination duration)
      - exclusions       (carve-outs: public info, independently
                           developed, already known, received from a
                           third party)
      - use_restriction  (permitted purpose / authorized use limits)
      - general          (the core non-disclosure obligation itself,
                           or anything not clearly matching the above)

    Returns "general" rather than guessing when no sub-topic is clearly
    signalled -- a correct, if less specific, template is always safer
    than a confidently wrong one.
    """
    combined = str(text or "").lower()

    duration_signals = [
        "survive", "survival", "period of", "years following",
        "months following", "years after", "months after",
        "shall remain in effect for", "for a period of",
        "survivra", "survie", "période de", "ans suivant",
        "mois suivant", "ans après", "mois après", "durée de",
        "restera en vigueur pendant",
        "يستمر", "بقاء", "لمدة", "سنوات بعد", "أشهر بعد",
    ]

    exclusions_signals = [
        "does not include", "shall not include", "excludes",
        "exclusions", "publicly available", "publicly accessible",
        "independently developed", "already known", "rightfully",
        "lawfully received", "prior to disclosure",
        "n'incluent pas", "ne comprennent pas", "exclusions",
        "accessible au public", "accessibles publiquement",
        "développées indépendamment", "connues légitimement",
        "reçues légitimement", "avant leur divulgation",
        "لا تشمل", "لا تتضمن", "استثناءات", "متاحة للجمهور",
        "معروفة بالفعل", "تم تطويرها بشكل مستقل",
    ]

    use_restriction_signals = [
        "shall only use", "shall use", "solely for the purpose",
        "only for the purpose", "use such information solely",
        "not use", "permitted purpose",
        "n'utilisera", "aux fins de", "uniquement aux fins",
        "usage limité", "à des fins autres",
        "لن يستخدم", "فقط لغرض", "للأغراض المحددة",
    ]

    if any(signal in combined for signal in duration_signals):
        return "duration"

    if any(signal in combined for signal in exclusions_signals):
        return "exclusions"

    if any(signal in combined for signal in use_restriction_signals):
        return "use_restriction"

    return "general"


def _data_processing_subtype(text: str) -> str:
    """
    Distinguishes which GDPR/data-processing sub-topic a clause
    addresses, so fallback wording addresses the actual subject rather
    than the one broad 'data_privacy_security' template shared by every
    data-processing-related clause. Common in DPAs and data-processing
    sections that split these into separate numbered sub-clauses:

      - instructions          (process only on documented instructions)
      - personnel_confidentiality (personnel confidentiality commitment)
      - subprocessors         (subprocessor engagement/authorization)
      - security_measures     (technical and organizational measures)
      - subject_rights        (assistance with data subject requests)
      - breach_notification   (personal data breach notification)
      - deletion_return       (deletion or return of data on termination)
      - audit                 (audit/inspection rights)
      - general               (anything not clearly matching the above)

    Returns "general" rather than guessing when no sub-topic is clearly
    signalled -- a correct, if less specific, template is always safer
    than a confidently wrong one.
    """
    combined = str(text or "").lower()

    breach_notification_signals = [
        "personal data breach", "data breach",
        "violation de données", "violation de données à caractère personnel",
        "خرق البيانات",
    ]

    deletion_return_signals = [
        "delete or return", "deletion or return", "delete existing copies",
        "upon termination", "return all", "delete all",
        "supprimer ou restituer", "suppression ou restitution",
        "à la résiliation", "supprimer les copies",
        "حذف أو إعادة", "عند الإنهاء", "حذف النسخ",
    ]

    audit_signals = [
        "audit rights", "conduct audits", "inspections", "demonstrate compliance",
        "droits d'audit", "conduire des audits", "inspections",
        "démontrer la conformité",
        "حقوق التدقيق", "إجراء عمليات تدقيق", "تفتيش", "إثبات الامتثال",
    ]

    subprocessors_signals = [
        "subprocessor", "sub-processor", "engage a subprocessor",
        "sous-traitant ultérieur", "engager un sous-traitant",
        "معالج فرعي", "الاستعانة بمعالج فرعي",
    ]

    security_measures_signals = [
        "technical and organizational measures", "pseudonymization",
        "encryption", "appropriate to the risk",
        "mesures techniques et organisationnelles", "pseudonymisation",
        "chiffrement", "proportionnées au risque",
        "التدابير التقنية والتنظيمية", "إخفاء الهوية", "التشفير",
    ]

    subject_rights_signals = [
        "data subject rights", "data subject requests", "exercising data subject",
        "droits de la personne concernée", "demandes des personnes concernées",
        "حقوق صاحب البيانات", "طلبات أصحاب البيانات",
    ]

    personnel_confidentiality_signals = [
        "committed themselves to confidentiality", "authorized to process",
        "statutory obligation of confidentiality", "persons authorized",
        "engagés à la confidentialité", "personnes autorisées à traiter",
        "obligation légale de confidentialité",
        "التزموا بالسرية", "الأشخاص المصرح لهم", "التزام قانوني بالسرية",
    ]

    instructions_signals = [
        "documented instructions", "process personal data only on",
        "instructions from controller", "unless required to do otherwise by",
        "instructions documentées", "traiter les données uniquement sur",
        "instructions du responsable",
        "تعليمات موثقة", "معالجة البيانات فقط بناءً على", "تعليمات المسؤول",
    ]

    # Audit and subject-rights are checked before breach_notification:
    # their own signals are specific enough not to collide with other
    # sub-topics, whereas "personal data breach" can appear as an
    # incidental exception qualifier in an otherwise-unrelated clause
    # (e.g. an audit-frequency clause worded "no more than once per
    # year absent a Personal Data breach").
    if any(signal in combined for signal in audit_signals):
        return "audit"

    if any(signal in combined for signal in subject_rights_signals):
        return "subject_rights"

    if any(signal in combined for signal in breach_notification_signals):
        return "breach_notification"

    if any(signal in combined for signal in deletion_return_signals):
        return "deletion_return"

    if any(signal in combined for signal in subprocessors_signals):
        return "subprocessors"

    if any(signal in combined for signal in security_measures_signals):
        return "security_measures"

    if any(signal in combined for signal in personnel_confidentiality_signals):
        return "personnel_confidentiality"

    if any(signal in combined for signal in instructions_signals):
        return "instructions"

    return "general"


def generate_fallback_wording(
    clause_type: str,
    text: str,
    language: str = "en",
) -> str:
    language = get_language(language)

    if not is_restrictive_covenant(clause_type, text):
        return ""

    months = recommended_duration_months(clause_type, text) or 12
    subtype = _restrictive_covenant_subtype(clause_type, text)

    return _FALLBACK_WORDING_TEMPLATES[subtype][language].format(months=months)


# ---------------------------------------------------------------------------
# Universal fallback: guarantees every clause_type gets honest,
# generically useful negotiation guidance -- not just restrictive
# covenants. This is what makes the module work for ANY contract in
# ANY domain rather than silently no-op'ing outside its specialty.
# ---------------------------------------------------------------------------

_NEGOTIABILITY_LABELS = {
    "en": {"low": "Low", "medium": "Medium", "high": "High"},
    "fr": {"low": "Faible", "medium": "Moyenne", "high": "Élevée"},
    "ar": {"low": "منخفضة", "medium": "متوسطة", "high": "مرتفعة"},
}

_GENERIC_ACCEPTABLE_COMPROMISE = {
    "en": (
        "A reasonable compromise typically narrows the scope, adds objective "
        "criteria or thresholds, and includes standard exceptions appropriate "
        "to this type of clause."
    ),
    "fr": (
        "Un compromis raisonnable consiste généralement à restreindre la "
        "portée, à ajouter des critères ou seuils objectifs, et à inclure les "
        "exceptions usuelles adaptées à ce type de clause."
    ),
    "ar": (
        "يتمثل التسوية المعقولة عادة في تضييق النطاق، وإضافة معايير أو حدود "
        "موضوعية، وتضمين الاستثناءات المعتادة المناسبة لهذا النوع من البنود."
    ),
}

_GENERIC_NEGOTIATION_BOUNDARY = {
    "en": (
        "Avoid accepting terms that are open-ended, lack objective criteria, "
        "or are materially more one-sided than standard market practice for "
        "this type of clause."
    ),
    "fr": (
        "Éviter d'accepter des conditions ouvertes, dépourvues de critères "
        "objectifs, ou nettement plus déséquilibrées que la pratique de "
        "marché habituelle pour ce type de clause."
    ),
    "ar": (
        "ينبغي تجنب قبول شروط مفتوحة أو تفتقر إلى معايير موضوعية أو غير "
        "متوازنة بشكل واضح مقارنة بممارسة السوق المعتادة لهذا النوع من "
        "البنود."
    ),
}


_GENERIC_FALLBACK_WORDING = {
    "en": (
        "A fallback formulation typically narrows the obligation to an "
        "objective, measurable standard and specifies the remedy or "
        "process that applies if that standard is not met."
    ),
    "fr": (
        "Une formulation de repli consiste généralement à restreindre "
        "l'obligation à une norme objective et mesurable, et à préciser "
        "le recours ou la procédure applicable en cas de non-respect."
    ),
    "ar": (
        "تتمثل الصياغة البديلة عادة في تضييق الالتزام إلى معيار "
        "موضوعي وقابل للقياس، وتحديد وسيلة الانتصاف أو الإجراء "
        "المطبق في حال عدم الوفاء بهذا المعيار."
    ),
}


# ---------------------------------------------------------------------------
# Cross-field negotiation consistency check.
#
# Root cause this addresses: an LLM can populate "fallback_wording" and
# "acceptable_compromise" independently of each other for the SAME clause,
# with no guarantee they describe the same negotiation position -- e.g.
# fallback_wording proposing an 18-month restriction while
# acceptable_compromise proposes 12 months for the identical clause. This
# was observed across multiple, unrelated clause types (termination, SLA,
# restrictive covenants), confirming it is a general LLM-output-pairing
# problem rather than something specific to one clause_type -- so the fix
# is a generic, clause_type-agnostic numeric consistency check rather than
# a per-type patch.
#
# Deliberately conservative: only flags when both fields mention a number
# for the SAME unit category (months/days/years/percentage/count), so
# unrelated numbers (e.g. one field discussing a duration, the other a
# headcount) are never falsely flagged.
# ---------------------------------------------------------------------------

_UNIT_KEYWORDS = {
    "percentage": ["%"],
    "years": ["years", "year", "ans", "an", "سنوات", "سنة", "عام", "عامين"],
    "months": ["months", "month", "mois", "أشهر", "شهرا", "شهراً", "شهر"],
    "business_days": [
        "business days", "business day",
        "jours ouvrables", "jour ouvrable",
        "أيام عمل", "يوم عمل",
    ],
    "days": ["days", "day", "jours", "jour", "أيام", "يوما", "يوماً", "يوم"],
    "count": [
        "competitors", "competitor", "concurrents", "concurrent",
        "parties", "entities", "منافسين", "منافسون", "أطراف",
    ],
}

# Matches both period and comma as decimal separator ("1.5%" and the
# French/European convention "1,5%"), since this module explicitly
# targets contracts in any of the three supported languages, not just
# English-formatted numbers.
_NUMBER_TOKEN_PATTERN = re.compile(r"\d+(?:[.,]\d+)?")

# How far past a bare number to look for a unit keyword. Real contract
# drafting frequently writes numbers as "twelve (12) months" or
# "three (3) named competitors" -- punctuation and filler words (named,
# specific, direct...) can sit between the digit and the unit noun, so a
# strict adjacency regex ("\d+\s*months?") misses most real-world
# phrasing. Searching a short window after the number instead is more
# robust than trying to enumerate every possible filler word.
_UNIT_SEARCH_WINDOW = 40

# A tighter window used specifically for word-form numbers ("two years").
# Kept narrower than _UNIT_SEARCH_WINDOW because some of the underlying
# words ("a", "an", "one", "two"...) are short and common in ordinary
# prose; requiring the unit word close by (not just anywhere in a 40-char
# window) keeps false positives low.
_WORD_NUMBER_SEARCH_WINDOW = 15

# Deliberately excluded from word-number scanning: too short/ambiguous
# and far too common in ordinary contract prose ("a party", "an
# Affiliate", "one of the five") to safely treat as a duration mention
# just because a year-marker happens to appear somewhere nearby.
_AMBIGUOUS_WORD_NUMBERS = {"a", "an", "one"}


def _closest_unit_in_window(window: str):
    """
    Finds whichever unit keyword appears CLOSEST (earliest) in the given
    window, rather than checking unit categories in a fixed, arbitrary
    order and taking the first match. This matters because a single
    sentence commonly packs several different numbers with different
    units close together -- e.g. "interest at 1.5% per month" has both
    "%" and "month" within a few characters of the "1.5". Checking
    categories in a fixed order (e.g. always "months" before
    "percentage") would misattribute the "1.5" to "months" simply
    because "month" happens to also be present somewhere in the wider
    window, even though "%" is immediately adjacent and is the number's
    real unit. Picking the closest keyword instead is a much more
    reliable proxy for "which unit this number actually belongs to".

    Matching is word-boundary-aware (not substring), since a short
    keyword like "an" (French for "year") is a literal substring of
    unrelated English words like "annual" or "announce" -- a naive
    substring search previously misread "three (3) times the annual
    fees" as "three ANnual" containing a year-marker, incorrectly
    converting it to "3 years" (36 months). Word boundaries prevent this
    without needing to special-case any specific word.
    """
    best_unit = None
    best_position = None

    for unit, keywords in _UNIT_KEYWORDS.items():
        for keyword in keywords:
            if keyword == "%":
                match = re.search(re.escape(keyword), window)
            else:
                match = re.search(
                    r"(?<!\w)" + re.escape(keyword) + r"(?!\w)",
                    window,
                )

            if not match:
                continue

            position = match.start()

            if best_position is None or position < best_position:
                best_position = position
                best_unit = unit

    return best_unit


def _window_has_unit_keyword(window: str, keywords: list) -> bool:
    """
    Word-boundary-aware check for whether any of the given unit keywords
    appears in the window -- shared by both the digit-based and
    word-number-based extraction paths. See _closest_unit_in_window for
    why this cannot be a plain substring ("in") check: short keywords
    like "an" (French for "year") are literal substrings of unrelated
    English words such as "annual".
    """
    return any(
        re.search(r"(?<!\w)" + re.escape(keyword) + r"(?!\w)", window)
        for keyword in keywords
    )


def extract_numbers_with_units(text: str) -> dict:
    """
    Extract every (unit_category -> [values]) numeric mention found in
    text, across a small set of negotiation-relevant units common to any
    contract domain, in EN/FR/AR. A clause/field may mention more than one
    number for the same unit; all are kept.

    Each bare number is matched against a short window of text
    immediately following it (rather than requiring the unit word to sit
    directly adjacent) so common drafting patterns like "twelve (12)
    months" or "five (5) named direct competitors" are recognized despite
    the parenthesis and filler words between the digit and the unit noun.
    Whichever unit keyword is CLOSEST within that window wins (see
    _closest_unit_in_window), rather than checking categories in a fixed
    order -- this avoids cross-contamination when a sentence packs
    multiple different units close together (e.g. "1.5% per month").

    Both digit-based ("24 months", "two years") and word-based durations
    are recognized, and any year-based mention is converted to months
    (× 12) at extraction time -- without this, "twelve (12) months" and
    "two years" would land in separate, never-compared unit categories
    even though they describe genuinely different positions (12 vs 24
    months) on the same negotiation point.

    "percentage" values are returned scaled ×10 (one decimal digit
    preserved: 1.5% -> 15, 1% -> 10) rather than as plain integers, so
    meaningfully different rates are never conflated by truncation. This
    is an internal representation detail -- callers only ever compare
    these values for set overlap (see detect_negotiation_inconsistency),
    never display them directly, so the scaling is invisible downstream.
    """
    normalized = str(text or "").lower()

    if not normalized:
        return {}

    found: dict = {}

    for match in _NUMBER_TOKEN_PATTERN.finditer(normalized):
        window = normalized[match.end():match.end() + _UNIT_SEARCH_WINDOW]
        raw_value_str = match.group().replace(",", ".")

        unit = _closest_unit_in_window(window)

        if unit is None:
            continue

        try:
            if unit == "percentage":
                # Scaled by 10 (one decimal digit preserved: 1.5% -> 15,
                # 1% -> 10) so meaningfully different rates are never
                # conflated by plain integer truncation -- which would
                # otherwise make "1.5%" and "1%" both collapse to "1"
                # and hide a real negotiation difference.
                value = round(float(raw_value_str) * 10)
            elif unit == "years":
                value = int(float(raw_value_str)) * 12
                unit = "months"
            else:
                value = int(float(raw_value_str))
        except (TypeError, ValueError):
            continue

        found.setdefault(unit, []).append(value)

    for lang_word_map in list(_WORD_NUMBERS_MONTHS.values()) + list(_WORD_NUMBERS_YEARS.values()):
        for word, number in lang_word_map.items():
            if word in _AMBIGUOUS_WORD_NUMBERS:
                continue

            pattern = re.compile(r"(?<!\w)" + re.escape(word) + r"(?!\w)")

            for match in pattern.finditer(normalized):
                window = normalized[match.end():match.end() + _WORD_NUMBER_SEARCH_WINDOW]

                if _window_has_unit_keyword(window, _UNIT_KEYWORDS["years"]):
                    found.setdefault("months", []).append(number * 12)
                elif _window_has_unit_keyword(window, _UNIT_KEYWORDS["months"]):
                    found.setdefault("months", []).append(number)

    return found


# ---------------------------------------------------------------------------
# Qualitative concept-pair mismatch check.
#
# Complements the numeric consistency check above for cases with no
# comparable number on either side -- e.g. clause 9.3 observed in testing:
# fallback_wording proposed giving the restricted party a right to
# terminate "for cause", while acceptable_compromise proposed "for
# convenience with a longer notice period" for the SAME asymmetry. These
# are two legally distinct termination bases; granting one does not
# remedy an imbalance framed around the other. Neither field contains a
# number, so the numeric check alone cannot catch this.
#
# This covers a small set of common, domain-independent legal dichotomies
# (for cause / for convenience, with notice / without notice, exclusive /
# non-exclusive, limited / unlimited) that recur across many clause types
# (termination, exclusivity, liability, IP licensing...), not just one.
# Deliberately conservative: only fires when one field asserts one side
# of a pair and the OTHER field asserts the opposite side WITHOUT also
# mentioning the first side (e.g. a compromise that mentions both "for
# cause" and "for convenience" together, describing a mutual right, is
# not flagged).
# ---------------------------------------------------------------------------

_CONCEPT_PAIRS = [
    {
        "en": (["for cause"], ["for convenience"]),
        "fr": (["pour faute"], ["pour convenance"]),
        "ar": (["لسبب مشروع"], ["لدواعي الملاءمة"]),
    },
    {
        "en": (["with notice"], ["without notice"]),
        "fr": (["avec préavis"], ["sans préavis"]),
        "ar": (["بإشعار"], ["دون إشعار"]),
    },
    {
        "en": (["exclusive"], ["non-exclusive"]),
        "fr": (
            ["exclusif", "exclusive", "exclusifs", "exclusives"],
            ["non exclusif", "non exclusive", "non exclusifs", "non exclusives"],
        ),
        "ar": (["حصري", "حصرية"], ["غير حصري", "غير حصرية"]),
    },
    {
        "en": (["unlimited"], ["limited"]),
        "fr": (
            ["illimité", "illimitée", "illimités", "illimitées"],
            ["limité", "limitée", "limités", "limitées"],
        ),
        "ar": (["غير محدود", "غير محدودة"], ["محدود", "محدودة"]),
    },
    {
        "en": (["uncapped"], ["capped"]),
        "fr": (
            ["non plafonné", "non plafonnée", "non plafonnés", "non plafonnées", "sans plafond"],
            ["plafonné", "plafonnée", "plafonnés", "plafonnées"],
        ),
        "ar": (["غير مسقوف", "دون سقف", "بلا حد أقصى"], ["مسقوف", "بحد أقصى"]),
    },
]


def _concept_present(concept_variants: list, text: str) -> bool:
    """
    Whole-phrase presence check across a list of morphological variants
    of the same negotiation concept (e.g. French gender/number agreement:
    "exclusif"/"exclusive"/"exclusifs"/"exclusives"), avoiding a
    substring-collision bug where one concept phrase is literally
    embedded inside its own negated counterpart in any of the three
    supported languages -- e.g. "exclusive" inside "non-exclusive",
    "exclusif" inside "non exclusif", "حصري" inside "غير حصري". A naive
    substring check cannot tell these apart. Requires a true word
    boundary on both sides AND explicitly excludes matches immediately
    preceded by a negation prefix (non-, non , without , sans , غير ,
    دون ) that is not already part of the concept phrase being searched
    for.
    """
    if not concept_variants or not text:
        return False

    for concept in concept_variants:
        pattern = (
            r"(?<!non-)(?<!non )(?<!without )(?<!sans )(?<!غير )(?<!دون )"
            + r"\b" + re.escape(concept) + r"\b"
        )

        if re.search(pattern, text):
            return True

    return False


def detect_concept_mismatch(fallback_wording: str, acceptable_compromise: str) -> bool:
    fallback_lower = str(fallback_wording or "").lower()
    compromise_lower = str(acceptable_compromise or "").lower()

    if not fallback_lower or not compromise_lower:
        return False

    for pair_set in _CONCEPT_PAIRS:
        for variants_a, variants_b in pair_set.values():
            fb_has_a = _concept_present(variants_a, fallback_lower)
            fb_has_b = _concept_present(variants_b, fallback_lower)
            ac_has_a = _concept_present(variants_a, compromise_lower)
            ac_has_b = _concept_present(variants_b, compromise_lower)

            if fb_has_a and not fb_has_b and ac_has_b and not ac_has_a:
                return True

            if fb_has_b and not fb_has_a and ac_has_a and not ac_has_b:
                return True

    return False


def detect_negotiation_inconsistency(
    fallback_wording: str,
    acceptable_compromise: str,
) -> bool:
    """
    True if fallback_wording and acceptable_compromise appear to describe
    divergent negotiation positions for what should be a single, coherent
    stance on the same clause. Combines two complementary heuristics:

    1. Numeric: both fields mention a number for the same unit category
       (e.g. both discuss a duration in months), but with no overlapping
       value.
    2. Conceptual: one field asserts one side of a common legal dichotomy
       (for cause / for convenience, with notice / without notice,
       exclusive / non-exclusive, limited / unlimited) while the other
       asserts the opposite side, without either field acknowledging
       both -- catching cases with no comparable number on either side.

    This is a heuristic, not a proof of inconsistency: it can still miss
    purely qualitative disagreements outside the concept pairs above, and
    it will not flag two fields that happen to share at least one
    matching value/concept even if they differ in other ways. It is
    intentionally biased toward avoiding false positives over catching
    every possible mismatch.
    """
    a = extract_numbers_with_units(fallback_wording)
    b = extract_numbers_with_units(acceptable_compromise)

    for unit, a_values in a.items():
        b_values = b.get(unit)

        if not b_values:
            continue

        if set(a_values).isdisjoint(set(b_values)):
            return True

    return detect_concept_mismatch(fallback_wording, acceptable_compromise)


# ---------------------------------------------------------------------------
# Source-fidelity risk gating.
#
# Root cause this addresses: a generated fallback_wording/acceptable_compromise
# can be internally consistent with each other (same number in both) while
# still being WRONG relative to the source clause -- e.g. a clause with a
# 60-day non-renewal notice AND a separate 90-day termination-for-convenience
# notice, where the generated text cross-attributes the 90-day figure to the
# non-renewal notice instead. detect_negotiation_inconsistency() cannot catch
# this (the two generated fields agree with each other), and a plain "is this
# number anywhere in the source" check would also miss it (90 IS in the
# source, just for a different concept) -- verifying this properly requires
# an AI call to check WHICH concept each number is attached to.
#
# That AI call is comparatively costly, so it should only run on clauses
# that genuinely carry this risk: the source must contain 2+ DIFFERENT
# numbers of the same unit (the precise condition for cross-attribution to
# even be possible), and the generated text must itself reference a number
# (our own generic filler text never does, so it cannot mis-attribute one).
# These gates are pure, language-agnostic functions reusing
# extract_numbers_with_units -- one code path covers EN/FR/AR and any
# contract domain, not a per-language special case.
# ---------------------------------------------------------------------------

def source_has_ambiguous_numeric_risk(clause_text: str) -> bool:
    """
    True if the clause text contains 2+ DIFFERENT numeric values for the
    same unit category (e.g. two different day-counts, two different
    percentages) -- the precise condition under which a generated field
    could cross-attribute one concept's number to a different concept in
    the same clause. A clause with at most one distinct value per unit
    has no such risk.
    """
    numbers = extract_numbers_with_units(clause_text)
    return any(len(set(values)) >= 2 for values in numbers.values())


_NEGATION_MARKERS = [
    "no ", "not ", "never ", "none ",
    "non ", "pas ", "aucun ", "aucune ",
    "لا ", "غير ", "دون ", "ليس ",
]


_WAIVABLE_RIGHT_TERMS = [
    ("jury trial", "procès devant jury", "محاكمة أمام هيئة محلفين"),
]

_JURISDICTION_REFERENCE_TERMS = [
    "jurisdiction", "courts", "venue",
    "compétence", "tribunaux", "juridiction",
    "اختصاص", "محاكم",
]

_EXCLUSIVITY_MARKERS_FOR_JURISDICTION = [
    "exclusive", "exclusively",
    "exclusive", "exclusivement", "exclusivité",
    "حصري", "حصرية", "حصراً",
]


def _text_has_exclusive_jurisdiction_marker(text: str) -> bool:
    """
    True if the text discusses jurisdiction/courts/venue AND marks it
    as exclusive, in either order and within a reasonable proximity
    (the whole text, since jurisdiction clauses are typically short and
    self-contained). Used to compare source vs fallback: silently
    dropping "exclusive" while still discussing the same courts/
    jurisdiction concept narrows an important, commonly-negotiated
    restriction without any negation marker or numeric change to
    trigger the other fidelity checks.
    """
    lowered = str(text or "").lower()

    has_jurisdiction_term = any(
        term in lowered for term in _JURISDICTION_REFERENCE_TERMS
    )
    has_exclusivity_marker = any(
        marker in lowered for marker in _EXCLUSIVITY_MARKERS_FOR_JURISDICTION
    )

    return has_jurisdiction_term and has_exclusivity_marker


def source_vs_fallback_exclusive_jurisdiction_mismatch(
    clause_text: str,
    fallback_wording: str,
) -> bool:
    """
    True if the source states exclusive jurisdiction but the generated
    fallback_wording discusses the same jurisdiction/courts concept
    without preserving the exclusivity, or vice versa. Confirmed real
    bug: a source clause granting "exclusive jurisdiction... of the
    courts located in Wilmington, Delaware" was restated by the
    fallback as "the courts of Delaware or other competent
    jurisdictions" -- silently broadening what the source restricted to
    one exclusive venue, with no negation word or number involved to
    trigger any other check.
    """
    source_lower = str(clause_text or "").lower()
    fallback_lower = str(fallback_wording or "").lower()

    if not source_lower or not fallback_lower:
        return False

    source_has_jurisdiction = any(
        term in source_lower for term in _JURISDICTION_REFERENCE_TERMS
    )
    fallback_has_jurisdiction = any(
        term in fallback_lower for term in _JURISDICTION_REFERENCE_TERMS
    )

    if not (source_has_jurisdiction and fallback_has_jurisdiction):
        return False

    source_exclusive = _text_has_exclusive_jurisdiction_marker(source_lower)
    fallback_exclusive = _text_has_exclusive_jurisdiction_marker(fallback_lower)

    return source_exclusive != fallback_exclusive


_RIGHT_WAIVER_MARKERS = [
    "waive", "waives", "waived", "waiving",
    "no right to", "shall not have the right", "not entitled to",
    "renonce", "renonce à", "renoncent à", "renonciation",
    "تنازل", "يتنازل", "تتنازل", "دون حق",
]


def _text_negates_right_nearby(term: str, text: str) -> bool:
    """
    True if `term` appears in `text` with a waiver/negation marker
    somewhere in the preceding ~60 characters -- unlike a simple
    adjacent-word concept pair, a waiver clause typically separates the
    negation from the right itself with variable text (e.g. "waives ANY
    RIGHT TO a jury trial"), so this cannot be matched as one fixed
    phrase.
    """
    lowered = str(text or "").lower()

    if not lowered or term not in lowered:
        return False

    idx = lowered.find(term)
    window = lowered[max(0, idx - 60):idx]

    return any(marker in window for marker in _RIGHT_WAIVER_MARKERS)


def source_vs_fallback_right_waiver_mismatch(
    clause_text: str,
    fallback_wording: str,
) -> bool:
    """
    True if the source clause and the generated fallback_wording take
    OPPOSITE positions on whether a known waivable right (e.g. a jury
    trial) is waived -- in either direction: the source waives it but
    the fallback presents it as available, or vice versa. Both texts
    must actually mention the underlying right (e.g. "jury trial") for
    this to fire; a field that never mentions the right at all is not
    compared.
    """
    source_lower = str(clause_text or "").lower()
    fallback_lower = str(fallback_wording or "").lower()

    if not source_lower or not fallback_lower:
        return False

    for term_variants in _WAIVABLE_RIGHT_TERMS:
        for term in term_variants:
            if term not in source_lower or term not in fallback_lower:
                continue

            source_negated = _text_negates_right_nearby(term, source_lower)
            fallback_negated = _text_negates_right_nearby(term, fallback_lower)

            if source_negated != fallback_negated:
                return True

    return False


def fallback_has_negated_concept_term(fallback_wording: str) -> bool:
    """
    True if fallback_wording contains a negation word immediately
    preceding a known concept-pair term (e.g. "no uncapped liability",
    "pas plafonné"). This exact double-negation pattern is where a real
    polarity-inversion bug was confirmed in testing: "no uncapped
    liability" means the liability IS capped -- the opposite of what
    "uncapped" alone would mean -- but a simple word-presence check
    cannot catch it, since the SAME word ("uncapped") appears whether
    the text is correct or inverted. Only checking for a negation
    marker immediately before the concept term catches this.
    """
    text = str(fallback_wording or "").lower()

    if not text:
        return False

    for pair_set in _CONCEPT_PAIRS:
        for variants_a, variants_b in pair_set.values():
            for concept in variants_a + variants_b:
                for negation in _NEGATION_MARKERS:
                    if (negation + concept) in text:
                        return True

    return False


_ALL_KNOWN_WORDING_LIBRARY_TEXTS = {
    text.strip()
    for language_variants in WORDING_LIBRARY.values()
    for text in language_variants.values()
}


_TERMINATION_BASIS_TERMS = [
    ("for convenience", "for cause"),
    ("sans motif", "pour motif"),
    ("لغير سبب", "لسبب"),
]


_NON_EXCLUSIVE_REMEDY_PATTERNS = [
    r"\bother\s+(?:\w+\s+)?remed(?:y|ies)\b",
    r"\badditional\s+(?:\w+\s+)?remed(?:y|ies)\b",
    r"\bseek\s+\w*\s*remed(?:y|ies)\b",
    r"\bpursue\s+\w*\s*remed(?:y|ies)\b",
    r"\bretain\s+\w*\s*remed(?:y|ies)\b",
    r"\bremedies?\s+(?:also\s+)?available\b",
    r"\bwithout\s+limit(?:ing|ation\s+of)\s+(?:\w+\s+)?(?:other|additional)\s+remed(?:y|ies)\b",
    r"\bwithout\s+prejudice\s+to\s+(?:\w+\s+)?(?:other|additional)\s+remed(?:y|ies)\b",
    r"\badditional\s+compensation\b",
    r"\bfurther\s+compensation\b",

    r"\bautres?\s+recours\b",
    r"\brecours?\s+suppl[ée]mentaires?\b",
    r"\bconserver\s+\w*\s*recours\b",
    r"\bsans\s+limiter\s+(?:\w+\s+)?(?:d'\s*)?autres?\s+recours\b",
    r"\bsans\s+préjudice\s+(?:d[e']\s*)?(?:\w+\s+)?autres?\s+recours\b",
    r"\bindemnisation\s+suppl[ée]mentaire\b",
    r"\bcompensation\s+suppl[ée]mentaire\b",

    r"سبل\s+انتصاف\s+أخرى",
    r"سبل\s+انتصاف\s+إضافية",
    r"دون\s+الإخلال\s+بـ?\s*سبل\s+انتصاف",
    r"دون\s+تقييد\s+سبل\s+انتصاف",
    r"تعويض\s+إضافي",
]

_EXCLUSIVE_REMEDY_MARKERS = [
    "sole remedy", "exclusive remedy", "sole and exclusive remedy",
    "only remedy",
    "seul recours", "recours exclusif", "seul et unique recours",
    "الحل الوحيد", "سبيل الانتصاف الوحيد", "سبيل الانتصاف الحصري",
]


def source_vs_fallback_exclusive_remedy_mismatch(
    clause_text: str,
    generated_text: str,
) -> bool:
    """
    True if the source states a remedy is sole/exclusive, and the
    generated text (fallback_wording or acceptable_compromise) uses
    ANY of several non-exclusive-remedy phrasings (seek/pursue/retain
    additional/other remedies) -- normalizing the many ways this
    concept can be phrased into a single check, rather than relying on
    the AI verification call's own judgment for this pattern.

    Confirmed real, non-deterministic gap: "Client shall be entitled to
    service credits... which shall be Client's sole and exclusive
    remedy" contradicted by generated text saying the Client "may also
    pursue other remedies" was caught by the AI verification call in
    one run, but the same underlying contradiction phrased as "may
    also seek additional remedies" in a later run was missed entirely
    -- confirming the AI's own polarity-inversion judgment is not
    reliable enough for this specific, recurring pattern.
    """
    source_lower = str(clause_text or "").lower()
    generated_lower = str(generated_text or "").lower()

    if not source_lower or not generated_lower:
        return False

    source_is_exclusive = any(marker in source_lower for marker in _EXCLUSIVE_REMEDY_MARKERS)
    if not source_is_exclusive:
        return False

    return any(
        re.search(pattern, generated_lower, re.IGNORECASE)
        for pattern in _NON_EXCLUSIVE_REMEDY_PATTERNS
    )


_DISPLAY_PATTERNS_BY_CATEGORY = {
    "percentage": re.compile(r"\d+(?:[.,]\d+)?\s*%", re.IGNORECASE),
    "months": re.compile(r"\(?\d+\)?\s*(?:months?|mois|أشهر|شهرا?ً?)", re.IGNORECASE),
    "business_days": re.compile(r"\(?\d+\)?\s*(?:business\s+days?|jours?\s+ouvrables?|أيام\s+عمل)", re.IGNORECASE),
    "days": re.compile(r"\(?\d+\)?\s*(?:days?|jours?|أيام)", re.IGNORECASE),
    "years": re.compile(r"\(?\d+\)?\s*(?:years?|ans?|سنوات?)", re.IGNORECASE),
    "count": re.compile(r"\(?\d+\)?\s*(?:competitors?|concurrents?|منافسين)", re.IGNORECASE),
}


def find_all_numeric_deltas_for_display(
    clause_text: str,
    generated_text: str,
) -> list:
    """
    Detects EVERY unit category (percentage/months/days/years/count)
    where the generated text's value genuinely differs from the
    source's value(s) for that same category -- not just the single
    delta an AI explanation happens to mention.

    Confirmed real gap: a clause with two independent numeric facts
    (interest rate 1.5% and a 60-day payment threshold) had the
    generated text change BOTH (to 1.25% and 90 days), but only the
    percentage delta was ever surfaced in the fidelity note -- the AI
    explanation mentions at most one change per call, silently dropping
    any additional, independently-verifiable delta in the same clause.

    Returns a list of "X -> Y" display strings, one per category with a
    genuine mismatch. Uses extract_numbers_with_units() (which already
    handles unit normalization, e.g. years->months, and scaling for
    reliable comparison) to DETECT which categories mismatch, then a
    separate raw-text regex per category to extract a human-readable
    phrase for each side, since the internal detection representation
    (e.g. percentage x10) is not meant for display.
    """
    source_numbers = extract_numbers_with_units(clause_text or "")
    generated_numbers = extract_numbers_with_units(generated_text or "")

    deltas = []

    for category in source_numbers:
        if category not in generated_numbers:
            continue

        source_values = set(source_numbers[category])
        generated_values = set(generated_numbers[category])

        if generated_values - source_values and source_values - generated_values:
            display_pattern = _DISPLAY_PATTERNS_BY_CATEGORY.get(category)
            if not display_pattern:
                continue

            source_match = display_pattern.search(str(clause_text or ""))
            generated_match = display_pattern.search(str(generated_text or ""))

            # "months" internally also represents years-worded text
            # (converted via x12 at extraction time), so fall back to
            # the "years" display pattern when the "months" one finds
            # no match -- otherwise a genuine years-based delta (e.g.
            # "five (5) years" -> "ten (10) years") is silently dropped
            # since the source text never contains the word "months".
            if category == "months":
                years_pattern = _DISPLAY_PATTERNS_BY_CATEGORY["years"]
                if not source_match:
                    source_match = years_pattern.search(str(clause_text or ""))
                if not generated_match:
                    generated_match = years_pattern.search(str(generated_text or ""))

            if source_match and generated_match:
                source_display = source_match.group(0).strip()
                generated_display = generated_match.group(0).strip()
                if source_display != generated_display:
                    deltas.append(f"{source_display} -> {generated_display}")

    return deltas


def source_vs_fallback_termination_basis_confusion(
    clause_text: str,
    fallback_wording: str,
) -> bool:
    """
    True if the source denies a right under one specifically-named
    termination basis (e.g. "for convenience") and the generated text
    grants a right under a DIFFERENT, specifically-named basis (e.g.
    "for cause"). This is NOT a contradiction -- these are distinct
    legal grounds a contract can treat completely differently -- but is
    used to SUPPRESS the AI fidelity check for this pattern, since
    repeated attempts at fixing this via prompt instructions failed to
    reliably prevent the AI verification call from confusing the two
    bases into a false "contradicts the original" claim.

    Confirmed real, recurring false positive: source clause denies
    Provider a right to terminate "for convenience"; generated
    fallback_wording states Provider may terminate "for cause" (true,
    confirmed by a separate clause elsewhere in the same contract) --
    the AI verification call incorrectly flagged this as contradicting
    the source's "for convenience" denial on three separate attempts,
    despite explicit prompt instructions not to.
    """
    source_lower = str(clause_text or "").lower()
    fallback_lower = str(fallback_wording or "").lower()

    if not source_lower or not fallback_lower:
        return False

    for basis_a, basis_b in _TERMINATION_BASIS_TERMS:
        source_denies_a = basis_a in source_lower and any(
            neg in source_lower for neg in ("shall not", "no right", "not have a right", "ne peut pas", "ne dispose pas", "لا يحق", "ليس له الحق")
        )
        fallback_grants_b = basis_b in fallback_lower

        if source_denies_a and fallback_grants_b:
            return True

        # Symmetric check for the other ordering (basis_b denied, basis_a granted).
        source_denies_b = basis_b in source_lower and any(
            neg in source_lower for neg in ("shall not", "no right", "not have a right", "ne peut pas", "ne dispose pas", "لا يحق", "ليس له الحق")
        )
        fallback_grants_a = basis_a in fallback_lower

        if source_denies_b and fallback_grants_a:
            return True

    return False


_LIABILITY_EXCEPTION_CATEGORY_TERMS = [
    "confidentiality", "personal data", "data breach", "gross negligence",
    "willful misconduct", "intellectual property", "indemnification",
    "payment obligations",

    "confidentialité", "données personnelles", "violation de données",
    "faute lourde", "faute intentionnelle", "propriété intellectuelle",
    "indemnisation", "obligations de paiement",

    "السرية", "البيانات الشخصية", "خرق البيانات", "الإهمال الجسيم",
    "سوء السلوك المتعمد", "الملكية الفكرية", "التعويض", "التزامات الدفع",
]


def source_lists_liability_exceptions(clause_text: str) -> bool:
    """
    True if the source clause has the structural pattern of a liability
    exception list: 'the limitation... shall not apply to X, Y, Z',
    meaning those categories are EXCLUDED from (i.e. uncapped under)
    the referenced cap. Used to detect a specific, real polarity
    inversion: generated text can silently rewrite an exception-listing
    clause as though it were itself a positive cap on those same
    categories, which says the opposite of what the source means.
    """
    text = str(clause_text or "").lower()

    if not text:
        return False

    exception_markers = [
        "shall not apply to", "does not apply to", "excludes",
        "shall not include",
        "ne s'applique pas à", "ne s'applique pas aux", "exclut",
        "لا ينطبق", "يستثني",
    ]

    return any(marker in text for marker in exception_markers)


_LIABILITY_CATEGORY_SIGNALS = {
    "FRAUD": [
        "fraud", "fraudulent",
        "fraude", "frauduleux",
        "احتيال", "احتيالي",
    ],
    "WILFUL_MISCONDUCT": [
        "wilful misconduct", "willful misconduct", "intentional misconduct",
        "faute intentionnelle", "faute délibérée",
        "سوء السلوك المتعمد", "سوء تصرف متعمد",
    ],
    "GROSS_NEGLIGENCE": [
        "gross negligence",
        "faute lourde", "négligence grave",
        "الإهمال الجسيم", "إهمال جسيم",
    ],
    "CONFIDENTIALITY_BREACH": [
        "confidentiality", "breach of confidentiality", "confidential information",
        "confidentialité", "violation de confidentialité", "informations confidentielles",
        "السرية", "خرق السرية", "المعلومات السرية",
    ],
    "DATA_PROTECTION_BREACH": [
        "data protection", "personal data breach", "data breach",
        "protection des données", "violation de données",
        "حماية البيانات", "خرق البيانات",
    ],
    "INDEMNIFICATION_OBLIGATION": [
        "indemnification", "indemnify", "indemnity obligations",
        "indemnisation", "obligations d'indemnisation",
        "التعويض", "التزامات التعويض",
    ],
    "IP_INFRINGEMENT": [
        "intellectual property infringement", "ip infringement", "infringement of third-party",
        "atteinte à la propriété intellectuelle", "contrefaçon",
        "التعدي على الملكية الفكرية", "انتهاك الملكية الفكرية",
    ],
    "PAYMENT_OBLIGATION": [
        "payment obligations", "failure to pay",
        "obligations de paiement", "défaut de paiement",
        "التزامات الدفع", "التخلف عن الدفع",
    ],
    "PERSONAL_INJURY": [
        "personal injury", "bodily injury", "death",
        "dommage corporel", "blessure corporelle", "décès",
        "الإصابة الشخصية", "الإصابة الجسدية", "الوفاة",
    ],
    "PROPERTY_DAMAGE": [
        "property damage", "damage to property",
        "dommage matériel", "dommage aux biens",
        "الأضرار المادية", "أضرار الممتلكات",
    ],
}

_LIABILITY_EXCLUSION_STATE_MARKERS = [
    "shall not apply to", "does not apply to", "excluded from the limitation",
    "excluded from the cap", "not subject to the limitation",
    "unlimited liability", "liability shall be unlimited",

    "ne s'applique pas à", "ne s'applique pas aux", "ne sont pas soumis à", "exclu du plafond",
    "exclus de la limitation", "non soumis à la limitation",
    "responsabilité illimitée", "la responsabilité est illimitée",

    r"لا\s+يسري.*على", r"لا\s+تسري.*على", "لا تنطبق على", "مستثنى من حد المسؤولية",
    "مستثناة من حد المسؤولية", "غير خاضع لحد المسؤولية",
    "غير خاضعة لحد المسؤولية", "مسؤولية غير محدودة",
]

_LIABILITY_CAP_STATE_MARKERS = [
    "capped at", "limited to", "shall not exceed", "maximum liability",
    "aggregate liability shall not exceed", "subject to a cap of",
    "limit liability", r"limit\b.*\bto", r"limiting\b.*\bto", "set a cap",
    "remains subject to the general cap", "subject to the general cap",

    r"plafonn[ée]e?\s+(?:à|au|aux)", "ne saurait excéder", "ne peut excéder", "responsabilité maximale",
    "soumis à un plafond de", r"limiter\b.*\bà", "fixer un plafond",
    "reste soumis au plafond général", "soumis au plafond général",
    r"limit[ée]e?\s+(?:à|au|aux)",

    "محدد بحد أقصى", "محددة بحد أقصى", "تقتصر المسؤولية على",
    "لا تتجاوز المسؤولية", "الحد الأقصى للمسؤولية", "تخضع لحد أقصى",
    "مسؤولية محدودة بـ", r"تقتصر\b.*\bعلى", "وضع سقف",
    "يخضع للحد الأقصى العام", "خاضع للحد العام",
]


def _sentence_split(text: str) -> list:
    """
    Splits text into sentences on '.', '!', or '?' followed by
    whitespace -- a pragmatic boundary for legal clause text, which is
    typically structured as short, self-contained sentences even when
    listing multiple categories. Deliberately does NOT split on ';',
    since legal clauses commonly use semicolons to separate items
    within a single exclusion list introduced by a colon (e.g. "shall
    not apply to: (a)...; (b)...; (c)..."), where all listed items
    share the same exclusion state from the shared introductory clause
    -- splitting there would incorrectly separate each list item into
    its own "sentence", losing that shared context. Sentence scoping is
    what prevents an exclusion stated for one category from being
    incorrectly applied to a genuinely different category discussed in
    an unrelated, separate sentence.
    """
    if not text:
        return []
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def extract_liability_states(text: str) -> dict:
    """
    Extracts, per normalized liability category, the cap_state implied
    by the text -- scoped sentence-by-sentence so that a category's
    treatment is only ever determined by the sentence(s) that actually
    discuss it, not by markers appearing elsewhere in unrelated
    sentences (the category-separation requirement).

    Returns {category: cap_state}, where cap_state is one of
    "EXCLUDED_FROM_GENERAL_CAP", "GENERAL_CAP", "SPECIAL_CAP", or
    absent entirely if the category is not mentioned at all in the
    text. "SPECIAL_CAP" is used whenever a specific multiplier/number is
    present alongside a cap marker; "GENERAL_CAP" otherwise.
    """
    states = {}

    for sentence in _sentence_split(text):
        sentence_lower = sentence.lower()

        has_exclusion = any(
            re.search(m, sentence_lower) if any(tok in m for tok in (".*", "\\b", "[", "(?:")) else m in sentence_lower
            for m in _LIABILITY_EXCLUSION_STATE_MARKERS
        )
        has_cap = any(
            re.search(m, sentence_lower) if any(tok in m for tok in (".*", "\\b", "[", "(?:")) else m in sentence_lower
            for m in _LIABILITY_CAP_STATE_MARKERS
        )

        if not has_exclusion and not has_cap:
            continue

        for category, signals in _LIABILITY_CATEGORY_SIGNALS.items():
            if not any(signal in sentence_lower for signal in signals):
                continue

            if has_exclusion:
                states[category] = "EXCLUDED_FROM_GENERAL_CAP"
            elif has_cap:
                has_multiplier = bool(re.search(r"\b\d+\s*(?:x|×|times|fois|مرة|مرات)\b", sentence_lower)) or \
                    bool(re.search(r"\btwice\b|\bdouble\b|\bضعف\b", sentence_lower))
                states[category] = "SPECIAL_CAP" if has_multiplier else "GENERAL_CAP"

    return states


_MATERIAL_OBLIGATION_CONCEPT_SIGNALS = {
    "NOTICE_PREREQUISITE": [
        "prior written notice", "advance written notice", "prompt written notice",
        "notify before", "notice as a condition to", "before relying on",

        "notification écrite préalable", "préavis écrit", "notifier avant",
        "avis écrit préalable", "sous réserve d'une notification",

        "إشعار كتابي مسبق", "إخطار كتابي مسبق", "إشعار قبل",
        "إخطار قبل", "شريطة تقديم إشعار",
    ],
    "EVIDENTIARY_BURDEN": [
        "burden of proving", "bears the burden of proof", "must demonstrate",
        "must establish", "responsible for proving", "burden of proof",

        "charge de la preuve", "charge de prouver", "supporte la charge de la preuve", "doit démontrer",
        "doit établir", "est tenu de prouver",

        "عبء الإثبات", "يتحمل عبء الإثبات", "يجب عليه إثبات",
        "يتعين عليه إثبات", "ملزم بإثبات",
    ],
    "CERTIFICATION_DUTY": [
        "certify in writing", "written certification", "provide a certificate",
        "confirm in writing", "written certificate",

        "certifier par écrit", "certification écrite", "fournir une attestation",
        "confirmer par écrit",

        "يشهد كتابياً", "شهادة خطية", "تقديم شهادة", "يؤكد كتابياً",
    ],
    "CONSENT_PREREQUISITE": [
        "prior written consent", "subject to consent", "may not without consent",
        "approval required",

        "consentement écrit préalable", "sous réserve du consentement",
        "ne peut sans consentement", "approbation requise",

        "موافقة كتابية مسبقة", "رهناً بالموافقة", "لا يجوز دون موافقة",
        "تتطلب الموافقة",
    ],
}

_MATERIAL_OBLIGATION_SEVERITY = {
    "NOTICE_PREREQUISITE": "medium",
    "EVIDENTIARY_BURDEN": "medium",
    "CERTIFICATION_DUTY": "medium",
    "CONSENT_PREREQUISITE": "high",
}


def detect_material_obligation_changes(
    clause_text: str,
    generated_text: str,
) -> list:
    """
    Detects procedural obligations/prerequisites (notice, evidentiary
    burden, certification duty, consent) that the generated text
    introduces but the source clause does not express at all --
    an ABSENT -> REQUIRED transition, contract-agnostic and
    concept-scoped so a concept already present in the source (even
    phrased differently) is correctly recognized as already-required
    rather than newly introduced.

    Confirmed test-driven gap: source silently omits any notice
    prerequisite for relying on an exclusion; generated text states a
    party "must provide prior written notice before relying on" that
    same exclusion -- a genuinely new procedural obligation the source
    never mentions, worth surfacing for human review (not necessarily
    wrong -- may be an intentional negotiation proposal).

    Returns a list of {"concept", "source_state", "generated_state",
    "severity"} dicts, one per concept newly introduced.
    """
    source_lower = str(clause_text or "").lower()
    generated_lower = str(generated_text or "").lower()

    if not source_lower or not generated_lower:
        return []

    issues = []

    for concept, signals in _MATERIAL_OBLIGATION_CONCEPT_SIGNALS.items():
        generated_has_concept = any(signal in generated_lower for signal in signals)

        if not generated_has_concept:
            continue

        source_has_concept = any(signal in source_lower for signal in signals)

        if source_has_concept:
            # Already required in the source (possibly phrased
            # differently) -- not a newly introduced obligation.
            continue

        issues.append({
            "concept": concept,
            "source_state": "ABSENT",
            "generated_state": "REQUIRED",
            "severity": _MATERIAL_OBLIGATION_SEVERITY.get(concept, "medium"),
        })

    return issues


def compare_liability_states(
    clause_text: str,
    generated_text: str,
) -> list:
    """
    Compares per-category liability cap_state between source and
    generated text, returning a list of structured issues for every
    category whose treatment materially changed -- in EITHER direction
    (uncapped-to-capped or capped-to-uncapped), per the bidirectional
    requirement. Categories not mentioned in the source are skipped
    (UNKNOWN baseline, nothing to compare against); categories mentioned
    in the source but not in the generated text are also skipped (the
    generated text simply doesn't address them, which is not itself an
    inversion).
    """
    source_states = extract_liability_states(clause_text)
    generated_states = extract_liability_states(generated_text)

    issues = []

    _uncapped_like = {"EXCLUDED_FROM_GENERAL_CAP", "UNCAPPED"}
    _capped_like = {"GENERAL_CAP", "SPECIAL_CAP"}

    for category, source_state in source_states.items():
        generated_state = generated_states.get(category)

        if not generated_state:
            continue

        is_inversion = (
            (source_state in _uncapped_like and generated_state in _capped_like)
            or (source_state in _capped_like and generated_state in _uncapped_like)
        )

        if is_inversion:
            issues.append({
                "category": category,
                "source_state": source_state,
                "generated_state": generated_state,
            })

    return issues


def generated_text_caps_excepted_category(
    clause_text: str,
    generated_text: str,
) -> bool:
    """
    Backward-compatible boolean wrapper over compare_liability_states(),
    kept for any existing call sites -- returns True if ANY category
    shows a material cap-state inversion in either direction.
    """
    return bool(compare_liability_states(clause_text, generated_text))


_INHERITANCE_MARKERS = [
    "similar notice", "same notice", "equivalent notice", "like notice",
    "on the same terms", "under the same conditions", "in the same manner",
    "with equivalent notice", "on similar terms", "the same notice period",

    "préavis similaire", "même préavis", "un préavis équivalent",
    "dans les mêmes conditions", "de la même manière",
    "aux mêmes conditions", "le même délai de préavis",

    "بإشعار مماثل", "بنفس الإشعار", "بإشعار مكافئ", "بنفس الشروط",
    "بالطريقة نفسها", "بشروط مماثلة", "بنفس مهلة الإشعار",
]

_CLAUSE_CONNECTORS_PATTERN = r"\b(?:and|while|whereas|et|tandis que|alors que)\b|(?<=\s)و"


_COMPREHENSIVE_TRANSFER_MARKERS = [
    "vest in", "vests in", "shall vest", "assigned to and vest",
    "automatically assigned", "all right, title, and interest",
    "without further action",

    "reviennent à", "seront dévolus à", "cédés à", "transférés automatiquement",
    "tous droits, titres et intérêts", "sans autre formalité",

    "تؤول إلى", "تنتقل إلى", "تُنقل تلقائياً", "جميع الحقوق والملكية والمصلحة",
    "دون أي إجراء إضافي",
]

_USAGE_RIGHT_INTRODUCTION_MARKERS = [
    "may use", "may reuse", "retains the right to use",
    "retains rights to use", "shall retain", "may continue to use",
    "reserves the right to use",

    "peut utiliser", "peut réutiliser", "conserve le droit d'utiliser",
    "conserve des droits d'utilisation", "se réserve le droit d'utiliser",

    "إعادة استخدام", "يحتفظ بحق استخدام", "يحتفظ بحقوق استخدام",
]


def generated_text_introduces_unaddressed_usage_right(
    clause_text: str,
    generated_text: str,
) -> bool:
    """
    True if the source comprehensively transfers ownership (vesting,
    assignment, "all right, title, and interest", "without further
    action") with no reservation for the transferring party, but the
    generated text introduces a usage/reuse/retention right for that
    same party that the source never mentions at all.

    Confirmed real gap: source states Deliverables "shall be
    automatically assigned to and vest in Client... without further
    action by either Party" -- a comprehensive, exhaustive transfer
    with nothing reserved -- but generated text states "Provider may
    use the general concepts developed for other clients", introducing
    a usage right the source is silent on. Unlike the denied-right
    checks above (which require an EXPLICIT denial), this pattern
    involves an ABSENCE of any mention -- inherently a softer signal,
    so this is scoped narrowly to comprehensive, exhaustive-sounding
    transfer language specifically, to limit false-positive risk on
    ordinary assignment clauses that aren't meant to be exhaustive.
    """
    source_lower = str(clause_text or "").lower()
    generated_lower = str(generated_text or "").lower()

    if not source_lower or not generated_lower:
        return False

    has_comprehensive_transfer = any(
        marker in source_lower for marker in _COMPREHENSIVE_TRANSFER_MARKERS
    )

    if not has_comprehensive_transfer:
        return False

    introduces_usage_right = any(
        marker in generated_lower for marker in _USAGE_RIGHT_INTRODUCTION_MARKERS
    )

    if not introduces_usage_right:
        return False

    # The specific right introduced must not already be discussed
    # anywhere in the source (even briefly) -- if the source itself
    # mentions retained/reserved/licensed-back rights, this is not an
    # unaddressed gap, it's the generated text correctly reflecting an
    # existing carve-out.
    retained_rights_markers = [
        "retain", "reserve", "license back", "background ip",
        "conserve", "réserve", "licence de retour",
        "يحتفظ", "يحفظ", "ترخيص عودة",
    ]

    if any(marker in source_lower for marker in retained_rights_markers):
        return False

    return True


_LIMITED_TERMINATION_MARKERS = [
    "only for", "solely for", "may terminate only", "limited to",

    "uniquement pour", "seulement pour", "ne peut résilier que",
    "limité à",

    "فقط لـ", "فقط في حال", "لا يجوز.*إلا", "يقتصر على",
]

_UNRESTRICTED_TERMINATION_MARKERS = [
    "for any reason", "for any reason or no reason", "without cause",
    "at its sole discretion", "for no reason",

    "pour quelque raison que ce soit", "sans motif", "pour toute raison",
    "à sa seule discrétion",

    "لأي سبب", "دون سبب", "لأي سبب أو دون سبب", "وفق تقديره المطلق",
]


_AUTOMATIC_RENEWAL_MARKERS = [
    "renews automatically", "renewing automatically", "automatically renew",
    "shall automatically renew", "automatic renewal", "renew automatically",

    "se renouvelle automatiquement", "renouvellement automatique",
    "se renouvellera automatiquement", "reconduction automatique",
    "se reconduit automatiquement",

    r"يتجدد.*تلقائياً", "التجديد التلقائي", r"يجدد.*تلقائياً",
]

_MUTUAL_CONSENT_RENEWAL_MARKERS = [
    "mutual written consent", "mutual consent", "only by mutual",
    "requires the agreement of both parties", "renewal upon mutual consent",
    "shall not renew unless both parties agree", "both parties must agree to renew",
    "renew only upon", "consent of both parties",

    "consentement mutuel", "accord mutuel", "seulement par consentement mutuel",
    "requiert l'accord des deux parties", "ne se renouvelle que si les deux parties",
    "sur accord des deux parties",

    "بموافقة متبادلة", "موافقة الطرفين", "لا يتجدد إلا بموافقة الطرفين",
    "باتفاق الطرفين",
]


_MANDATORY_PARTICIPATION_MARKERS = [
    "shall be required to vote in favor", "shall be required to consent",
    "required to vote in favor of and consent to", "mandatory participation",
    "obligated to consent", "shall vote in favor of and consent",
    "required to vote in favour", "shall be obligated to vote",

    "seront tenus de voter", "tenus de voter en faveur et de consentir",
    "participation obligatoire", "obligés de consentir",

    "سيكونون ملزمين بالتصويت", r"ملزم\w*\s+بالتصويت\s+لصالح\s+والموافقة\s+على",
    "المشاركة الإلزامية", r"ملزم\w*\s+بالموافقة",
]

_DISCRETIONARY_RIGHT_INTRODUCED_MARKERS = [
    "opportunity to negotiate", "may negotiate", "right to negotiate terms",
    "may object", "may decline", "at their discretion", "opportunity to object",
    "right to consent or object", "may choose whether",

    "possibilité de négocier", "peut négocier", "droit de négocier les conditions",
    "peut s'opposer", "peut refuser", "à sa discrétion",

    "فرصة للتفاوض", "يجوز له التفاوض", "حق التفاوض على الشروط",
    "يجوز له الاعتراض", "يجوز له الرفض", "وفق تقديره",
]


def fallback_wording_changes_right_polarity(
    clause_text: str,
    generated_text: str,
) -> bool:
    """
    True if the source expresses MANDATORY_PARTICIPATION (a party is
    bound to vote in favor/consent with no discretion), but the
    generated text introduces a discretionary right (an opportunity to
    negotiate, object, or decline) that the source does not grant.
    This is a right-polarity change -- from an obligation to a right --
    not a numeric or drafting detail.

    Confirmed real pattern: source states other shareholders "shall be
    required to vote in favor of and consent to" a drag-along
    transaction (mandatory, no discretion); generated fallback_wording
    proposes shareholders should have "the opportunity to negotiate
    terms before being required to consent" -- introducing a
    discretionary negotiation right the source's mandatory language
    does not contemplate.
    """
    source_lower = str(clause_text or "").lower()
    generated_lower = str(generated_text or "").lower()

    if not source_lower or not generated_lower:
        return False

    has_mandatory_in_source = any(
        re.search(m, source_lower) if any(tok in m for tok in (".*", "\\b", "\\w")) else m in source_lower
        for m in _MANDATORY_PARTICIPATION_MARKERS
    )

    if not has_mandatory_in_source:
        return False

    has_discretionary_in_generated = any(m in generated_lower for m in _DISCRETIONARY_RIGHT_INTRODUCED_MARKERS)

    return has_discretionary_in_generated


_NOTICE_NOT_REQUIRED_MARKERS = [
    "with no notice", "no notice period", "without notice",
    "no notice required", "immediately upon",

    "sans préavis", "aucun préavis", "sans notification préalable",
    "immédiatement dès",

    "دون إشعار", "لا يشترط إشعار", "بدون إخطار", "فوراً عند",
]

_NOTICE_REQUIRED_INTRODUCED_MARKERS = [
    "notice period", "days prior notice", "days' prior notice",
    "advance notice", "days' notice", "prior written notice",

    "délai de préavis", "jours de préavis", "préavis préalable",
    "notification préalable",

    "مهلة إشعار", "أيام إشعار مسبق", "إشعار مسبق", "إخطار مسبق",
]


def compromise_introduces_notice_requirement(
    clause_text: str,
    generated_text: str,
) -> bool:
    """
    True if the source expresses NOTICE_NOT_REQUIRED (event-triggered
    automatic termination with no notice concept at all, or explicit
    "with no notice" language), but the generated text introduces a
    notice-period requirement. This is a procedural mechanism change --
    from an automatic, notice-free process to a notice-based one -- not
    a numeric detail, since the source has no comparable numeric notice
    role to begin with.

    Confirmed real pattern: source states the agreement "shall
    terminate automatically upon the earlier of a Qualified IPO or a
    sale of the Company" (event-triggered, no notice concept
    whatsoever); generated acceptable_compromise proposes "a notice
    period of 30 days prior to termination" -- introducing a
    notice-based procedural requirement an event-triggered automatic
    termination mechanism does not have.
    """
    source_lower = str(clause_text or "").lower()
    generated_lower = str(generated_text or "").lower()

    if not source_lower or not generated_lower:
        return False

    has_notice_required_in_source = any(m in source_lower for m in _NOTICE_REQUIRED_INTRODUCED_MARKERS)

    if has_notice_required_in_source:
        # Source already has a notice concept -- any change here is a
        # numeric/procedural detail comparison, not an introduction of
        # a wholly new mechanism.
        return False

    has_explicit_no_notice = any(m in source_lower for m in _NOTICE_NOT_REQUIRED_MARKERS)
    has_automatic_termination = bool(
        re.search(
            r"terminate[s]?\s+automatically|automatic\s+termination"
            r"|prendra\s+fin\s+automatiquement|se\s+termine\s+automatiquement"
            r"|résiliation\s+automatique|prend\s+fin\s+automatiquement"
            r"|ينتهي.*تلقائياً|الإنهاء\s+التلقائي",
            source_lower,
        )
    )

    if not (has_explicit_no_notice or has_automatic_termination):
        return False

    return any(m in generated_lower for m in _NOTICE_REQUIRED_INTRODUCED_MARKERS)


def fallback_wording_changes_renewal_mechanism(
    clause_text: str,
    generated_text: str,
) -> bool:
    """
    True if the source expresses AUTOMATIC renewal (renews unless
    notice is given -- an opt-out mechanism) but the generated text
    expresses MUTUAL-CONSENT renewal (requires both parties to
    affirmatively agree -- an opt-in mechanism). This is a genuine
    mechanism change, not a numeric detail, even though both texts
    commonly also contain notice-period numbers that could otherwise
    cause this to be misclassified as a mere numeric_source_delta.

    Confirmed pattern from specification: "automatic renewal unless
    notice" -> "renewal only by mutual written consent" changes WHO
    must act for the contract to continue (the renewing party doing
    nothing, vs both parties affirmatively agreeing), which is a
    materially different mechanism regardless of what number (if any)
    appears in either version.
    """
    source_lower = str(clause_text or "").lower()
    generated_lower = str(generated_text or "").lower()

    if not source_lower or not generated_lower:
        return False

    has_automatic_in_source = any(
        re.search(m, source_lower) if any(tok in m for tok in (".*", "\\b")) else m in source_lower
        for m in _AUTOMATIC_RENEWAL_MARKERS
    )

    if not has_automatic_in_source:
        return False

    has_mutual_consent_in_generated = any(m in generated_lower for m in _MUTUAL_CONSENT_RENEWAL_MARKERS)

    return has_mutual_consent_in_generated


def fallback_wording_removes_termination_limitation(
    clause_text: str,
    generated_text: str,
) -> bool:
    """
    True if the source LIMITS a party's termination right to a specific
    cause condition (e.g. "Client may terminate only for Provider's
    uncured material breach"), but the generated text grants that same
    party an unrestricted right ("for any reason"/"no reason"),
    removing the limitation the source imposes. Contract-agnostic and
    party-agnostic: works regardless of which party was limited in the
    source, since it checks the same party-role word appears near both
    the source's limitation and the generated text's unrestricted
    grant.

    Confirmed real, previously-invisible pattern: source limits Client
    to termination "only for Provider's uncured material breach";
    generated fallback_wording states "Client may terminate... for any
    reason" -- a material expansion of Client's right that fell through
    to a mere numeric_source_delta classification since both texts
    share the number "60" (for entirely different purposes: a cure
    period in the source, a notice period in the generated text).
    """
    source_lower = str(clause_text or "").lower()
    generated_lower = str(generated_text or "").lower()

    if not source_lower or not generated_lower:
        return False

    has_limitation = any(
        re.search(m, source_lower) if any(tok in m for tok in (".*", "\\b")) else m in source_lower
        for m in _LIMITED_TERMINATION_MARKERS
    )

    if not has_limitation:
        return False

    has_unrestricted_grant = any(m in generated_lower for m in _UNRESTRICTED_TERMINATION_MARKERS)

    return has_unrestricted_grant


def fallback_wording_contains_inherited_denied_right(
    clause_text: str,
    fallback_wording: str,
) -> str:
    """
    Returns a deterministic warning message if fallback_wording grants
    a party a right by CONTEXTUALLY INHERITING an explicit basis stated
    earlier in the same sentence (via a marker like "similar notice" /
    "same terms"), where that inherited basis is one the source
    explicitly denies that party -- or an empty string if no such
    issue is found.

    This is the contextual-paraphrase counterpart to
    acceptable_compromise_introduces_denied_right(): that function
    catches the basis stated LITERALLY; this one catches it stated BY
    REFERENCE. Confirmed real gap: "Client may terminate for
    convenience upon sixty (60) days' notice, and Provider may
    terminate with similar notice" -- Provider's clause never contains
    the word "convenience" at all, so a literal search finds nothing,
    even though "with similar notice" plainly means Provider gets the
    SAME "for convenience" right Client has, which the source
    explicitly denies Provider.
    """
    source_lower = str(clause_text or "").lower()
    fallback_lower = str(fallback_wording or "").lower()

    if not source_lower or not fallback_lower:
        return ""

    denial_markers = ("shall not", "no right", "not have a right", "ne peut pas", "ne dispose pas", "لا يحق", "ليس له الحق")

    for basis_a, basis_b in _TERMINATION_BASIS_TERMS:
        for denied_basis, other_basis in ((basis_a, basis_b), (basis_b, basis_a)):
            if denied_basis not in fallback_lower:
                continue

            segments = re.split(_CLAUSE_CONNECTORS_PATTERN, fallback_lower)
            if len(segments) < 2:
                continue

            first_segment_has_basis = denied_basis in segments[0]

            for later_segment in segments[1:]:
                if denied_basis in later_segment or other_basis in later_segment:
                    # This segment explicitly names its own basis
                    # (possibly a different, legitimate one) -- not an
                    # inheritance case.
                    continue

                has_inheritance_marker = any(
                    marker in later_segment for marker in _INHERITANCE_MARKERS
                )

                if first_segment_has_basis and has_inheritance_marker:
                    source_denies = denied_basis in source_lower and any(
                        neg in source_lower for neg in denial_markers
                    )

                    if source_denies:
                        return (
                            f'The generated fallback wording contextually grants a right '
                            f'("{denied_basis}", inherited via a phrase such as "similar notice") '
                            f"that the source clause explicitly denies to the party in this segment. "
                            f"Manual review recommended to confirm this is an intentional negotiation proposal."
                        )

    return ""


def acceptable_compromise_introduces_denied_right(
    clause_text: str,
    acceptable_compromise: str,
) -> str:
    """
    Returns a deterministic warning message if acceptable_compromise
    grants a party the SAME termination basis the source explicitly
    denies them, or an empty string if no such issue is found.

    This is the complementary, opposite-purpose check to
    source_vs_fallback_termination_basis_confusion() above: that
    function SUPPRESSES a false alarm when a DIFFERENT basis is
    introduced; this function DETECTS a genuine issue when the SAME
    denied basis is introduced specifically within acceptable_compromise
    -- a field the existing fidelity check does not examine for this
    pattern at all.

    Confirmed real gap: source clause explicitly denies Provider a
    right to terminate "for convenience". fallback_wording correctly
    uses a different basis ("for cause") for Provider, so no issue
    there. But acceptable_compromise separately states "Allow the
    Provider to terminate for convenience with a similar notice
    period" -- reintroducing the exact basis the source denies -- and
    this went completely unflagged, since should_check_wording_fidelity()
    only routes fallback_wording through this kind of check.
    """
    source_lower = str(clause_text or "").lower()
    compromise_lower = str(acceptable_compromise or "").lower()

    if not source_lower or not compromise_lower:
        return ""

    denial_markers = ("shall not", "no right", "not have a right", "ne peut pas", "ne dispose pas", "لا يحق", "ليس له الحق")

    all_basis_terms = {term for pair in _TERMINATION_BASIS_TERMS for term in pair}

    for basis_term in all_basis_terms:
        source_denies = basis_term in source_lower and any(
            neg in source_lower for neg in denial_markers
        )
        compromise_grants = basis_term in compromise_lower

        if source_denies and compromise_grants:
            return (
                f"The generated acceptable compromise introduces a right "
                f'("{basis_term}") that the source clause explicitly denies. '
                f"Manual review recommended to confirm this is an intentional "
                f"negotiation proposal."
            )

    return ""


_EXPLICIT_CHANGE_SIGNAL_WORDS = [
    "increase", "reduce", "extend", "instead of", "rather than",
    "change to", "shorten", "lengthen", "raise", "lower", "narrow",
    "widen", "expand", "restrict to", "cap at", "limit to",

    "augmenter", "réduire", "prolonger", "au lieu de", "plutôt que",
    "porter à", "raccourcir", "allonger", "diminuer", "restreindre à",
    "plafonner à", "limiter à", "étendre",

    "زيادة", "تخفيض", "تمديد", "بدلاً من", "بدل", "تقصير", "تقليل",
    "تقييد إلى", "تحديد بـ",
]


def fallback_wording_contains_explicit_change_signal(fallback_wording: str) -> bool:
    """
    True if fallback_wording contains an explicit word signalling a
    deliberate change (extend/reduce/increase/instead of/etc.), in any
    of the three supported languages. Used to deterministically suppress
    the AI fidelity-verification call, rather than relying on the AI to
    correctly recognize the same signal itself.

    Confirmed real, recurring bug: the AI verification prompt already
    explicitly listed these words as change-signalling language that
    should prevent flagging a fidelity issue, yet the AI verification
    call still flagged a fallback_wording that literally said "extend
    the notice period... to twenty (20) Business Days" -- a textbook
    case of the exact pattern the prompt told it to recognize. Checking
    this deterministically in code, rather than trusting the AI to apply
    its own documented instruction, removes this specific unreliability
    entirely.
    """
    text = str(fallback_wording or "").lower()

    if not text:
        return False

    return any(signal in text for signal in _EXPLICIT_CHANGE_SIGNAL_WORDS)


def should_check_wording_fidelity(
    clause_text: str,
    fallback_wording: str,
    acceptable_compromise: str,
) -> bool:
    """
    Gates the AI fidelity-verification call. Two independent triggers:

      1. Cross-attribution risk (source has 2+ DIFFERENT values for the
         same unit, e.g. a 60-day notice AND a separate 90-day notice in
         the same clause): checks fallback_wording AND
         acceptable_compromise COMBINED, since a mix-up between two real
         source concepts is a legitimate risk in either field, whether
         it is framed as a restatement or a proposal.

      2. Plain restatement-accuracy risk (source has only ONE value for
         a unit): checks fallback_wording ONLY, never
         acceptable_compromise. acceptable_compromise is, by
         definition, always a negotiation proposal -- offering a
         different number than the source is its normal, expected
         function, not a fidelity concern, and checking it here produced
         confirmed false positives (a compromise explicitly framed as
         "increase the notice period to 90 days" is not a restatement
         error just because 90 differs from the source's 60).
         fallback_wording is the field that more often restates the
         clause's own terms with at most a minor, usually-signalled
         adjustment, so a wrong, unsignalled number there is more likely
         a genuine restatement error.

      3. Negated-polarity risk: fallback_wording contains a negation
         word immediately preceding a known dichotomy term (capped/
         uncapped, exclusive/non-exclusive, limited/unlimited...) -- a
         confirmed real bug pattern where the SAME word as the source
         ("uncapped") gets wrapped in an extra negation ("no uncapped
         liability"), inverting its meaning in a way no simple
         word-presence comparison can detect. Independent of the
         numeric checks above -- runs even when the clause has no
         recognized numbers at all.

      4. Right-waiver mismatch: the source and fallback_wording take
         opposite positions on whether a known waivable right (e.g. a
         jury trial) is waived -- in either direction. A confirmed real
         bug: a clause where "each Party irrevocably waives any right to
         a jury trial" was inverted by the generated fallback into
         "the option... to request a jury trial", with zero numbers and
         no existing concept-pair term anywhere in the clause to trigger
         any other check. The negation and the right are often separated
         by variable text ("waives ANY RIGHT TO a"), so this needs its
         own proximity-based check rather than a fixed-phrase pair.

    All four funnel through the same AI call (verify_wording_fidelity_to_source),
    which is additionally instructed not to flag a deliberately different
    number offered as a genuine negotiation proposal -- this gate decides
    whether it's worth ASKING; the AI decides the answer.
    """
    if str(fallback_wording or "").strip() in _ALL_KNOWN_WORDING_LIBRARY_TEXTS:
        return False

    if fallback_wording_contains_explicit_change_signal(fallback_wording):
        return False

    if source_vs_fallback_termination_basis_confusion(clause_text, fallback_wording):
        return False

    if fallback_has_negated_concept_term(fallback_wording):
        return True

    if source_vs_fallback_right_waiver_mismatch(clause_text, fallback_wording):
        return True

    if source_vs_fallback_exclusive_jurisdiction_mismatch(clause_text, fallback_wording):
        return True

    source_numbers = extract_numbers_with_units(clause_text)

    if not source_numbers:
        return False

    if source_has_ambiguous_numeric_risk(clause_text):
        combined_generated = extract_numbers_with_units(
            f"{fallback_wording or ''} {acceptable_compromise or ''}"
        )

        if set(source_numbers) & set(combined_generated):
            return True

    fallback_numbers = extract_numbers_with_units(fallback_wording or "")

    return bool(set(source_numbers) & set(fallback_numbers))


def generic_negotiation_market_practice(
    negotiability: Optional[str],
    language: str = "en",
) -> Optional[str]:
    """
    Honest, non-fabricated market-practice label for any clause_type,
    derived from an existing negotiability rating (e.g. the "negotiability"
    field already produced by market_intelligence.py: "low"/"medium"/"high").
    Returns None if no negotiability rating is available, rather than
    guessing.
    """
    language = get_language(language)
    key = str(negotiability or "").lower().strip()

    if key not in _NEGOTIABILITY_LABELS[language]:
        return None

    return _NEGOTIABILITY_LABELS[language][key]


def generate_generic_acceptable_compromise(language: str = "en") -> str:
    language = get_language(language)
    return _GENERIC_ACCEPTABLE_COMPROMISE[language]


def generate_generic_negotiation_boundary(language: str = "en") -> str:
    language = get_language(language)
    return _GENERIC_NEGOTIATION_BOUNDARY[language]


def generate_generic_fallback_wording(language: str = "en") -> str:
    language = get_language(language)
    return _GENERIC_FALLBACK_WORDING[language]


# ---------------------------------------------------------------------------
# Public entry point.
# ---------------------------------------------------------------------------

def enrich_negotiation_fields(
    analysis: dict,
    clause_text: str,
    language: str = "en",
    clause_type: Optional[str] = None,
) -> dict:
    """
    Add negotiation-intelligence fields to an existing clause analysis
    dict, for ANY clause_type in ANY contract domain.

    Field names are deliberately namespaced under "negotiation_*" (plus
    "acceptable_compromise" and "fallback_wording", which are new,
    non-colliding keys) so this never silently overwrites the
    "market_practice" field already produced upstream by
    market_intelligence.py, which uses a different vocabulary
    (e.g. "frequently_negotiated") for a different purpose (general
    market comparison vs. this module's duration/language-driven
    negotiation scoring).

    Restrictive covenants (non-compete, non-solicitation, exclusivity)
    get specialized, quantitative analysis. Every other clause_type
    still receives honest, generically useful negotiation guidance
    (never a silent no-op), clearly marked via
    analysis["negotiation_specific"] = False so callers can distinguish
    specific from generic guidance.
    """
    if not isinstance(analysis, dict):
        return analysis

    language = get_language(language)

    resolved_clause_type = str(
        clause_type
        or analysis.get("clause_type")
        or analysis.get("type")
        or analysis.get("category")
        or ""
    )

    if is_restrictive_covenant(resolved_clause_type, clause_text):
        market = evaluate_market_practice(resolved_clause_type, clause_text, language)
        if market:
            analysis["negotiation_market_practice"] = market

        acceptable = generate_acceptable_compromise(resolved_clause_type, clause_text, language)
        if acceptable:
            analysis["acceptable_compromise"] = acceptable

        boundary = generate_negotiation_boundary(resolved_clause_type, clause_text, language)
        if boundary:
            analysis["negotiation_boundary"] = boundary

        wording = generate_fallback_wording(resolved_clause_type, clause_text, language)
        if wording:
            analysis["fallback_wording"] = wording

        analysis["negotiation_specific"] = True
        return analysis

    # Universal fallback: every other clause_type still gets honest,
    # generic negotiation guidance instead of being silently skipped.
    generic_market = generic_negotiation_market_practice(
        analysis.get("negotiability"),
        language,
    )
    if generic_market:
        analysis["negotiation_market_practice"] = generic_market

    analysis["acceptable_compromise"] = generate_generic_acceptable_compromise(language)

    # Try the type-specific boundary function first -- it now also
    # covers several non-restrictive-covenant types (force_majeure,
    # data_privacy_security, security, payment, termination) with
    # concrete, actionable content, not just restrictive covenants.
    # Falls back to the fully generic boundary only when no
    # type-specific content is available for this clause_type.
    type_specific_boundary = generate_negotiation_boundary(resolved_clause_type, clause_text, language)
    analysis["negotiation_boundary"] = (
        type_specific_boundary or generate_generic_negotiation_boundary(language)
    )

    if not str(analysis.get("fallback_wording") or "").strip():
        # Consult the rich, clause-type-specific wording library (49+
        # clause types, EN/FR/AR) BEFORE falling back to the fully
        # generic, clause-type-agnostic text. Confirmed real bug: every
        # non-restrictive-covenant clause type (confidentiality,
        # warranty, remedies, and dozens more) was receiving the exact
        # same generic template regardless of type, even though a
        # dedicated entry already existed in this library. This
        # function already degrades gracefully to its own general
        # wording when a clause_type has no dedicated entry, so it is
        # always safe to call here.
        lookup_type = resolved_clause_type

        # Confidentiality clauses commonly split into several distinct
        # sub-clauses within the same contract (the general obligation,
        # a use restriction, exclusions, a survival/duration clause),
        # which previously all shared the identical generic
        # "confidentiality" wording regardless of their actual
        # sub-topic. Refine to a sub-topic-specific entry when the
        # resolved type is (or aliases to) confidentiality.
        if normalize_clause_type(resolved_clause_type) == "confidentiality":
            subtype = _confidentiality_subtype(clause_text)
            lookup_type = f"confidentiality_{subtype}"

        # Corporate governance clauses commonly cover two substantively
        # different subjects under the same top-level type: board/
        # shareholder matters (composition, reserved matters, deadlock)
        # versus operational review-committee/recurring-meeting
        # mechanisms (cadence, attendees, agenda, escalation). Refine
        # to the subject-specific entry the same way confidentiality is
        # refined above.
        if normalize_clause_type(resolved_clause_type) == "corporate_governance":
            cg_subtype = _corporate_governance_subtype(clause_text)
            if cg_subtype == "committee":
                lookup_type = "corporate_governance_committee"

        # Data-processing/GDPR clauses commonly split into several
        # distinct sub-clauses within the same DPA (processing
        # instructions, personnel confidentiality, subprocessors,
        # security measures, data subject rights assistance, breach
        # notification, deletion/return, audit rights), which
        # previously all shared the identical generic
        # "data_privacy_security" wording regardless of their actual
        # sub-topic, since both data_processing and data_protection
        # alias to that one entry. Refine to a sub-topic-specific entry
        # the same way confidentiality is refined above.
        if normalize_clause_type(resolved_clause_type) == "data_privacy_security":
            dp_subtype = _data_processing_subtype(clause_text)
            if dp_subtype != "general":
                lookup_type = f"data_privacy_security_{dp_subtype}"

        analysis["fallback_wording"] = get_safer_alternative(
            lookup_type,
            language,
        )

    analysis["negotiation_specific"] = False

    return analysis
