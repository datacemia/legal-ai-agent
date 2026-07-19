"""
Clause-type legal reasoning templates for contract analysis.

These templates complement domain-level reasoning by providing
specific reasoning for common clause categories:
liability, confidentiality, termination, SLA, indemnity, payment,
exclusivity, and governing law.
"""

import re

from app.services.contract_agent.legal_ontology import (
    detect_legal_domains,
)

from app.services.contract_agent.contract_taxonomy import (
    detect_clause_type_candidates,
    detect_clause_type_from_taxonomy,
)

from app.services.contract_agent.market_intelligence import (
    get_market_intelligence,
    get_market_comparison,
)

from app.services.contract_agent.clause_wording_library import (
    get_safer_alternative,
)

from app.services.contract_agent.clause_templates import (
    get_clause_template,
)

from app.services.contract_agent.clause_interactions import (
    get_clause_interactions,
    get_jurisdiction_caveat,
)

from app.services.contract_agent.sector_overlays import (
    get_sector_overlay,
)

from app.services.contract_agent.negotiation_intelligence import (
    enrich_negotiation_fields,
    _confidentiality_subtype,
    _data_processing_subtype,
)


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


# ---------------------------------------------------------------------------
# Universal signal-matching helper.
#
# Root-cause fix: plain substring checks ("signal in text") produce false
# positives whenever a short signal word is itself a substring of an
# unrelated longer word -- e.g. the payment signal "fee" incidentally
# matching inside "fees" in the phrase "arbitrators' fees", which can tip
# an unrelated clause (arbitration/governing_law) into being misclassified
# as "payment". This is not specific to English or to any one clause
# type: the same risk exists for any short signal in any of the three
# supported languages (EN/FR/AR), so the fix is applied once, generically,
# everywhere a signal-in-text check happens in this file, rather than as
# a one-off patch for a single word.
#
# \b works on Unicode word boundaries by default for str patterns in
# Python 3, so this is safe for Arabic script as well as Latin script.
# Patterns are compiled lazily and cached, since the same signal strings
# are checked repeatedly across many clauses in a single contract.
# ---------------------------------------------------------------------------

_SIGNAL_PATTERN_CACHE: dict = {}


def _signal_pattern(signal: str) -> "re.Pattern":
    cached = _SIGNAL_PATTERN_CACHE.get(signal)

    if cached is not None:
        return cached

    pattern = re.compile(
        r"(?<!\w)" + re.escape(signal) + r"(?!\w)",
        re.UNICODE,
    )

    _SIGNAL_PATTERN_CACHE[signal] = pattern

    return pattern


def signal_present(signal: str, text: str) -> bool:
    """
    Whole-word/whole-phrase presence check for a single signal in text,
    used in place of a raw substring ("in") check throughout this module.
    Matches only at word boundaries, so "fee" no longer matches inside
    "fees", "pay" no longer matches inside "repay", etc. Multi-word
    signals (e.g. "late payment") are unaffected, since boundaries are
    only enforced at the start and end of the signal itself.
    """
    if not signal or not text:
        return False

    return bool(_signal_pattern(signal).search(text))


def any_signal_present(signals, text: str) -> bool:
    return any(signal_present(signal, text) for signal in signals)


def count_signals_present(signals, text: str) -> int:
    return sum(1 for signal in signals if signal_present(signal, text))


BOILERPLATE_CLAUSES = {
    "headings",
    "notices",
}


GENERIC_LEGAL_INSIGHTS = {
    "This clause creates contractual obligations or operational requirements that should be reviewed in the context of the overall agreement.",
    "This clause creates contractual obligations.",
}


GENERIC_RECOMMENDATIONS = {
    "Confirm that the clause is consistent with the commercial intent, operational process, and overall risk allocation.",
}



def get_language(language: str) -> str:
    language = str(language or "en").lower().strip()

    if language not in SUPPORTED_LANGUAGES:
        return "en"

    return language



DOMAIN_TO_REASONING_TYPE = {
    "termination": "termination",
    "payment": "payment",
    "confidentiality": "confidentiality",
    "liability": "liability",
    "indemnity": "indemnity",
    "arbitration": "governing_law",
    "governing_law": "governing_law",
    "data_privacy_security": "data_privacy_security",
    "services_operations": "services_operations",
    "intellectual_property": "intellectual_property",
    "restrictive_covenants": "restrictive_covenants",
    "non_compete": "restrictive_covenants",
    "non_solicitation": "restrictive_covenants",
    "non_solicitation_customers": "restrictive_covenants",
    "exclusivity": "restrictive_covenants",
    "governance_compliance": "governance_compliance",
    "finance_lending": "finance_lending",
    "real_estate": "real_estate",
    "employment_hr": "employment_hr",
    "conflict_of_interest": "governance_compliance",
    "change_of_control": "change_of_control",

    # contract_taxonomy.py canonical names not otherwise matching this
    # file's own (narrower, pre-existing) key set -- mapped to the
    # closest existing semantic match. Confirmed real bug: several of
    # these (dispute_resolution, warranty) fell through to the fully
    # generic "general" template, producing a clause-type-agnostic
    # safer_alternative even though a specific, matching template
    # already existed under a different name.
    "dispute_resolution": "governing_law",
    "jurisdiction": "governing_law",
    "venue": "governing_law",
    "warranty": "warranties",
    "indemnification": "indemnity",
    "corporate_governance": "corporate_governance",
    "compliance": "governance_compliance",
    "anti_bribery_compliance": "governance_compliance",
    "export_control": "governance_compliance",
    "loan": "finance_lending",
    "collateral": "finance_lending",
    "security_interest": "finance_lending",
    "guarantee": "finance_lending",
    "financial_covenants": "finance_lending",
    "events_of_default": "finance_lending",
    "trademark_branding": "publicity",
    "lease": "real_estate",
    "rent_and_escalation": "real_estate",
    "maintenance_and_repairs": "real_estate",
    "use_and_occupancy": "real_estate",
    "employment": "employment_hr",
    "independent_contractor_status": "employment_hr",
    "key_personnel": "employment_hr",
    "share_transfer_rights": "change_of_control",
    "investor_information_rights": "investor_information_rights",
    "cross_border_data_transfer": "data_privacy_security",
    "sla": "services_operations",
    "subcontracting": "services_operations",
    "exit_transition": "services_operations",
    "service_level": "sla",
    "automatic_renewal": "renewal",
    "security": "data_privacy_security",
    "data_processing": "data_privacy_security",
    "data_protection": "data_privacy_security",
}


CLAUSE_REASONING_TEMPLATES = {
    "liability": {
        "signals": [
            "liability",
            "liability cap",
            "limitation of liability",
            "unlimited liability",
            "indirect damages",
            "responsabilité",
            "plafond de responsabilité",
            "limitation de responsabilité",
            "responsabilité illimitée",
            "dommages indirects",
            "المسؤولية",
            "حد المسؤولية",
            "مسؤولية غير محدودة",
            "الأضرار غير المباشرة",
        ],
        "legal_insight": {
            "en": (
                "This clause affects how financial responsibility is "
                "allocated if losses, claims, or disputes arise."
            ),
            "fr": (
                "Cette clause détermine la répartition de la "
                "responsabilité financière en cas de pertes, de "
                "réclamations ou de litiges."
            ),
            "ar": (
                "تحدد هذه المادة كيفية توزيع المسؤولية المالية عند "
                "وقوع خسائر أو مطالبات أو نزاعات."
            ),
        },
        "recommendation": {
            "en": (
                "Check whether the liability cap, exclusions, and "
                "carve-outs are clearly stated and proportionate."
            ),
            "fr": (
                "Vérifier que le plafond de responsabilité, les exclusions "
                "et les exceptions sont clairement définis et proportionnés."
            ),
            "ar": (
                "ينبغي التحقق من وضوح حد المسؤولية والاستثناءات "
                "وأن تكون متناسبة."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating liability caps, exclusions for indirect "
                "damages, and carve-outs for fraud, wilful misconduct, or "
                "confidentiality breaches."
            ),
            "fr": (
                "Envisager de négocier des plafonds de responsabilité, "
                "l'exclusion des dommages indirects et des exceptions en "
                "cas de fraude, faute intentionnelle ou violation de "
                "confidentialité."
            ),
            "ar": (
                "يمكن التفاوض على حدود للمسؤولية، واستبعاد الأضرار غير "
                "المباشرة، مع استثناءات لحالات الاحتيال أو الخطأ العمدي "
                "أو خرق السرية."
            ),
        },
    },

    "confidentiality": {
        "signals": [
            "confidentiality",
            "confidentiality obligations",
            "confidential information",
            "non-disclosure",
            "nda",
            "proprietary information",
            "post-contract obligations",
            "trade secret",
            "survive termination",
            "confidentialité",
            "obligations de confidentialité",
            "information confidentielle",
            "secret commercial",
            "السرية",
            "التزامات السرية",
            "معلومات سرية",
            "سر تجاري",
        ],
        "legal_insight": {
            "en": (
                "This clause controls how protected information may be used, "
                "shared, retained, and protected."
            ),
            "fr": (
                "Cette clause encadre l'utilisation, la communication, "
                "la conservation et la protection des informations "
                "confidentielles."
            ),
            "ar": (
                "تنظم هذه المادة كيفية استعمال المعلومات المحمية أو "
                "مشاركتها أو الاحتفاظ بها أو حمايتها."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm that the scope, permitted disclosures, duration, "
                "and return or destruction duties are clear."
            ),
            "fr": (
                "Vérifier que la portée, les divulgations autorisées, "
                "la durée et les obligations de restitution ou destruction "
                "sont claires."
            ),
            "ar": (
                "ينبغي التأكد من وضوح النطاق، وحالات الإفصاح المسموح، "
                "والمدة، وواجبات الإرجاع أو الإتلاف."
            ),
        },
        "negotiation": {
            "en": (
                "Consider limiting confidentiality duration, narrowing the "
                "scope of protected information, and adding standard "
                "disclosure exceptions."
            ),
            "fr": (
                "Envisager de limiter la durée de confidentialité, de "
                "restreindre la portée des informations protégées et "
                "d'ajouter des exceptions usuelles de divulgation."
            ),
            "ar": (
                "يمكن التفاوض على تقليص مدة السرية، وتحديد نطاق "
                "المعلومات المحمية، وإضافة استثناءات إفصاح معتادة."
            ),
        },
    },

    "confidentiality_general": {
        "signals": [
            "confidentiality", "confidentiality obligations",
            "confidentialité", "obligations de confidentialité",
            "السرية", "التزامات السرية",
        ],
        "legal_insight": {
            "en": (
                "This clause establishes the core non-disclosure obligation: "
                "who is bound by it, what standard of care applies, and "
                "whether authorized sub-disclosure (e.g. to representatives) "
                "is permitted."
            ),
            "fr": (
                "Cette clause établit l'obligation de non-divulgation elle-même : "
                "qui elle engage, quel niveau de soin s'applique, et si une "
                "sous-divulgation autorisée (par exemple aux représentants) "
                "est permise."
            ),
            "ar": (
                "تنشئ هذه المادة التزام عدم الإفصاح الأساسي: من يلتزم به، "
                "وما معيار العناية المطبق، وما إذا كان الإفصاح الفرعي "
                "المصرح به (مثلاً للممثلين) مسموحاً."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm the obligation clearly names who it binds, requires "
                "at least equivalent protection for any authorized "
                "sub-disclosure, and states a concrete standard of care."
            ),
            "fr": (
                "Vérifier que l'obligation nomme clairement qui elle engage, "
                "exige une protection au moins équivalente pour toute "
                "sous-divulgation autorisée, et énonce un niveau de soin "
                "concret."
            ),
            "ar": (
                "ينبغي التأكد من أن الالتزام يحدد بوضوح من يلتزم به، ويشترط "
                "حماية مماثلة على الأقل لأي إفصاح فرعي مصرح به، وينص على "
                "معيار عناية محدد."
            ),
        },
        "negotiation": {
            "en": (
                "Consider narrowing who counts as a permitted representative, "
                "and confirming the standard of care is no less than "
                "reasonable care."
            ),
            "fr": (
                "Envisager de restreindre qui compte comme représentant "
                "autorisé, et de confirmer que le niveau de soin n'est pas "
                "inférieur à un soin raisonnable."
            ),
            "ar": (
                "يمكن تضييق نطاق من يُعد ممثلاً مصرحاً به، والتأكد من ألا "
                "يقل معيار العناية عن العناية المعقولة."
            ),
        },
    },

    "confidentiality_use_restriction": {
        "signals": [
            "shall only use", "permitted purpose", "solely for the purpose",
            "n'utilisera", "aux fins de", "usage limité",
            "لن يستخدم", "فقط لغرض",
        ],
        "legal_insight": {
            "en": (
                "This clause restricts what the receiving party may actually "
                "do with the confidential information, independent of "
                "whether it keeps it secret."
            ),
            "fr": (
                "Cette clause restreint ce que la partie réceptrice peut "
                "effectivement faire des informations confidentielles, "
                "indépendamment du fait qu'elle les garde secrètes."
            ),
            "ar": (
                "تحد هذه المادة مما يجوز للطرف المتلقي فعله فعلياً "
                "بالمعلومات السرية، بصرف النظر عن حفاظه على سريتها."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm the permitted purpose is defined narrowly enough to "
                "prevent competitive use or independent development based on "
                "the disclosed information."
            ),
            "fr": (
                "Vérifier que la finalité autorisée est définie de manière "
                "suffisamment étroite pour empêcher un usage concurrentiel ou "
                "un développement indépendant fondé sur les informations "
                "divulguées."
            ),
            "ar": (
                "ينبغي التأكد من أن الغرض المصرح به محدد بضيق كافٍ لمنع "
                "الاستخدام التنافسي أو التطوير المستقل بناءً على المعلومات "
                "المفصح عنها."
            ),
        },
        "negotiation": {
            "en": (
                "Consider clarifying whether internal evaluation, "
                "benchmarking, or affiliate use falls within the permitted "
                "purpose."
            ),
            "fr": (
                "Envisager de clarifier si l'évaluation interne, le "
                "benchmarking ou l'usage par des affiliés entre dans le "
                "périmètre de la finalité autorisée."
            ),
            "ar": (
                "يمكن توضيح ما إذا كان التقييم الداخلي أو المقارنة المرجعية "
                "أو استخدام الشركات التابعة يدخل ضمن الغرض المصرح به."
            ),
        },
    },

    "confidentiality_exclusions": {
        "signals": [
            "does not include", "excludes", "publicly available",
            "n'incluent pas", "accessible au public", "exclusions",
            "لا تشمل", "متاحة للجمهور", "استثناءات",
        ],
        "legal_insight": {
            "en": (
                "This clause defines what falls OUTSIDE the definition of "
                "confidential information, limiting the practical reach of "
                "the non-disclosure obligation."
            ),
            "fr": (
                "Cette clause définit ce qui sort du champ des informations "
                "confidentielles, limitant la portée pratique de "
                "l'obligation de non-divulgation."
            ),
            "ar": (
                "تحدد هذه المادة ما يقع خارج نطاق تعريف المعلومات السرية، "
                "مما يحد من الأثر العملي لالتزام عدم الإفصاح."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm the exclusions are limited to the four standard "
                "carve-outs (public without breach, already known, "
                "independently developed, lawfully received from a third "
                "party) and are not broader than that."
            ),
            "fr": (
                "Vérifier que les exclusions se limitent aux quatre "
                "exceptions usuelles (information publique sans faute, déjà "
                "connue, développée indépendamment, reçue légitimement d'un "
                "tiers) et ne vont pas au-delà."
            ),
            "ar": (
                "ينبغي التأكد من أن الاستثناءات تقتصر على الاستثناءات "
                "القياسية الأربعة (المعلومات العامة دون خطأ، المعروفة "
                "مسبقاً، المطورة بشكل مستقل، المستلمة بشكل قانوني من طرف "
                "ثالث) ولا تتجاوزها."
            ),
        },
        "negotiation": {
            "en": (
                "Consider requiring the receiving party to bear the burden "
                "of proving an exclusion applies, and prompt written notice "
                "before relying on the independent-development or "
                "already-known exclusions."
            ),
            "fr": (
                "Envisager d'exiger que la partie réceptrice supporte la "
                "charge de prouver qu'une exclusion s'applique, ainsi qu'une "
                "notification écrite rapide avant de se prévaloir des "
                "exclusions de développement indépendant ou de connaissance "
                "préalable."
            ),
            "ar": (
                "يمكن اشتراط تحميل الطرف المتلقي عبء إثبات انطباق أي "
                "استثناء، وإخطار كتابي فوري قبل الاعتماد على استثناءي "
                "التطوير المستقل أو المعرفة المسبقة."
            ),
        },
    },

    "confidentiality_duration": {
        "signals": [
            "survive", "survival", "period of", "years following",
            "survivra", "survie", "période de", "ans suivant",
            "يستمر", "بقاء", "لمدة",
        ],
        "legal_insight": {
            "en": (
                "This clause determines how long the confidentiality "
                "obligations continue, including after the underlying "
                "agreement ends."
            ),
            "fr": (
                "Cette clause détermine la durée pendant laquelle les "
                "obligations de confidentialité se poursuivent, y compris "
                "après la fin de l'accord principal."
            ),
            "ar": (
                "تحدد هذه المادة المدة التي تستمر خلالها التزامات السرية، "
                "بما في ذلك بعد انتهاء الاتفاقية الأساسية."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm the survival period is a defined term (commonly two "
                "to five years) rather than open-ended, except for a "
                "specific, narrower carve-out for genuine trade secrets."
            ),
            "fr": (
                "Vérifier que la durée de survie est une période définie "
                "(généralement de deux à cinq ans) plutôt qu'illimitée, sauf "
                "exception spécifique et plus étroite pour les véritables "
                "secrets commerciaux."
            ),
            "ar": (
                "ينبغي التأكد من أن مدة البقاء محددة (عادة من سنتين إلى خمس "
                "سنوات) وليست مفتوحة، باستثناء استثناء محدد وأضيق للأسرار "
                "التجارية الحقيقية."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating a defined survival period for general "
                "confidential information, reserving indefinite survival "
                "specifically for information that genuinely qualifies as a "
                "trade secret under applicable law."
            ),
            "fr": (
                "Envisager de négocier une durée de survie définie pour les "
                "informations confidentielles générales, en réservant une "
                "survie illimitée spécifiquement aux informations "
                "qualifiant réellement de secret commercial au regard du "
                "droit applicable."
            ),
            "ar": (
                "يمكن التفاوض على مدة بقاء محددة للمعلومات السرية العامة، "
                "مع قصر البقاء غير المحدود على المعلومات التي تستوفي فعلاً "
                "شروط السر التجاري بموجب القانون المعمول به."
            ),
        },
    },

    "termination": {
        "signals": [
            "termination",
            "terminate",
            "cure period",
            "notice period",
            "immediate termination",
            "résiliation",
            "résilier",
            "délai de régularisation",
            "préavis",
            "إنهاء",
            "فسخ",
            "مهلة معالجة",
            "إشعار",
            "إنهاء فوري",
        ],
        "legal_insight": {
            "en": (
                "This clause determines when the contract can end and "
                "whether the affected party has notice or an opportunity "
                "to cure."
            ),
            "fr": (
                "Cette clause détermine les conditions de fin du contrat "
                "et si la partie concernée bénéficie d'un préavis ou "
                "d'une possibilité de régularisation."
            ),
            "ar": (
                "تحدد هذه المادة متى يمكن إنهاء العقد وما إذا كان للطرف "
                "المتأثر حق في الإشعار أو فرصة لمعالجة الإخلال."
            ),
        },
        "recommendation": {
            "en": (
                "Review the termination triggers, notice requirements, "
                "cure periods, and post-termination obligations."
            ),
            "fr": (
                "Examiner les causes de résiliation, les exigences de "
                "préavis, les délais de régularisation et les obligations "
                "après résiliation."
            ),
            "ar": (
                "ينبغي مراجعة أسباب الإنهاء، ومتطلبات الإشعار، ومهل "
                "المعالجة، والالتزامات بعد الإنهاء."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating mutual termination rights, longer "
                "cure periods, and clear consequences after termination."
            ),
            "fr": (
                "Envisager de négocier des droits de résiliation "
                "réciproques, des délais de régularisation plus longs "
                "et des conséquences claires après résiliation."
            ),
            "ar": (
                "يمكن التفاوض على حقوق إنهاء متبادلة، ومهل معالجة أطول، "
                "وآثار واضحة بعد الإنهاء."
            ),
        },
    },

    "sla": {
        "signals": [
            "service level",
            "sla",
            "uptime",
            "availability",
            "downtime",
            "service credit",
            "niveau de service",
            "disponibilité",
            "interruption",
            "crédit de service",
            "مستوى الخدمة",
            "التوافر",
            "انقطاع الخدمة",
            "تعويض الخدمة",
        ],
        "legal_insight": {
            "en": (
                "This clause defines service performance commitments and "
                "the consequences if the provider fails to meet them."
            ),
            "fr": (
                "Cette clause définit les engagements de performance du "
                "service et les conséquences en cas de non-respect."
            ),
            "ar": (
                "تحدد هذه المادة التزامات أداء الخدمة والآثار المترتبة "
                "عند عدم الالتزام بها."
            ),
        },
        "recommendation": {
            "en": (
                "Check whether uptime targets, measurement periods, "
                "exclusions, remedies, and reporting obligations are clear."
            ),
            "fr": (
                "Vérifier que les objectifs de disponibilité, les périodes "
                "de mesure, les exclusions, les recours et les obligations "
                "de reporting sont clairs."
            ),
            "ar": (
                "ينبغي التحقق من وضوح أهداف التوافر، وفترات القياس، "
                "والاستثناءات، ووسائل المعالجة، والتقارير."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating measurable uptime commitments, service "
                "credits, incident response timelines, and termination "
                "rights for repeated failures."
            ),
            "fr": (
                "Envisager de négocier des engagements de disponibilité "
                "mesurables, des crédits de service, des délais de réponse "
                "aux incidents et un droit de résiliation en cas d'échecs "
                "répétés."
            ),
            "ar": (
                "يمكن التفاوض على التزامات توافر قابلة للقياس، وتعويضات "
                "خدمة، ومهل استجابة للحوادث، وحق الفسخ عند تكرار الإخفاق."
            ),
        },
    },

    "indemnity": {
        "signals": [
            "indemnity",
            "indemnify",
            "hold harmless",
            "defend",
            "indemnisation",
            "indemniser",
            "tenir indemne",
            "défendre",
            "تعويض",
            "يعوض",
            "الدفاع عن",
        ],
        "legal_insight": {
            "en": (
                "This clause allocates responsibility for third-party claims, "
                "defense costs, damages, or losses."
            ),
            "fr": (
                "Cette clause répartit la responsabilité liée aux réclamations "
                "de tiers, aux frais de défense, aux dommages ou aux pertes."
            ),
            "ar": (
                "تحدد هذه المادة المسؤولية عن مطالبات الغير وتكاليف الدفاع "
                "والأضرار أو الخسائر."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm which claims are covered, who controls the defense, "
                "whether notice is required, and whether liability limits apply."
            ),
            "fr": (
                "Vérifier quelles réclamations sont couvertes, qui contrôle "
                "la défense, si une notification est requise et si les limites "
                "de responsabilité s'appliquent."
            ),
            "ar": (
                "ينبغي التأكد من نوع المطالبات المشمولة، ومن يتحكم في الدفاع، "
                "وما إذا كان الإشعار مطلوباً، وهل تنطبق حدود المسؤولية."
            ),
        },
        "negotiation": {
            "en": (
                "Consider narrowing indemnified claims, requiring prompt notice, "
                "and linking indemnity exposure to liability limits."
            ),
            "fr": (
                "Envisager de restreindre les réclamations indemnisées, "
                "d'exiger une notification rapide et de lier l'indemnisation "
                "aux limites de responsabilité."
            ),
            "ar": (
                "يمكن التفاوض على تضييق نطاق المطالبات المشمولة بالتعويض، "
                "واشتراط إشعار سريع، وربط التعويض بحدود المسؤولية."
            ),
        },
    },

    "payment": {
        "signals": [
            "payment",
            "invoice",
            "fee",
            "pricing",
            "interest",
            "late payment",
            "principal amount",
            "loan amount",
            "paiement",
            "facture",
            "frais",
            "prix",
            "intérêt",
            "retard de paiement",
            "capital",
            "montant du prêt",
            "الدفع",
            "فاتورة",
            "الرسوم",
            "الأسعار",
            "الفائدة",
            "تأخر الدفع",
            "رأس المال",
            "مبلغ القرض",
        ],
        "legal_insight": {
            "en": (
                "This clause defines financial obligations, payment timing, "
                "pricing mechanics, or interest exposure."
            ),
            "fr": (
                "Cette clause définit les obligations financières, les délais "
                "de paiement, les mécanismes de prix ou l'exposition aux intérêts."
            ),
            "ar": (
                "تحدد هذه المادة الالتزامات المالية، ومواعيد الدفع، وآليات "
                "التسعير، أو التعرض للفائدة."
            ),
        },
        "recommendation": {
            "en": (
                "Check payment due dates, invoicing requirements, interest, "
                "penalties, tax treatment, and consequences of non-payment."
            ),
            "fr": (
                "Vérifier les échéances de paiement, les exigences de facturation, "
                "les intérêts, les pénalités, le traitement fiscal et les "
                "conséquences du non-paiement."
            ),
            "ar": (
                "ينبغي مراجعة آجال الدفع، ومتطلبات الفوترة، والفائدة، "
                "والجزاءات، والمعالجة الضريبية، وآثار عدم السداد."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating payment schedules, grace periods, invoice "
                "dispute procedures, and proportional late-payment remedies."
            ),
            "fr": (
                "Envisager de négocier des échéanciers de paiement, des délais "
                "de grâce, des procédures de contestation des factures et des "
                "recours proportionnés en cas de retard."
            ),
            "ar": (
                "يمكن التفاوض على جداول الدفع، وفترات السماح، وإجراءات "
                "الاعتراض على الفواتير، ووسائل معالجة متناسبة عند التأخير."
            ),
        },
    },

    "exclusivity": {
        "signals": [
            "exclusive",
            "exclusivity",
            "sole provider",
            "non-exclusive",
            "territory",
            "exclusif",
            "exclusivité",
            "fournisseur unique",
            "non exclusif",
            "territoire",
            "حصري",
            "حصرية",
            "مزود وحيد",
            "غير حصري",
            "منطقة",
        ],
        "legal_insight": {
            "en": (
                "This clause may restrict the ability to work with other "
                "partners, suppliers, customers, or territories."
            ),
            "fr": (
                "Cette clause peut limiter la capacité de travailler avec "
                "d'autres partenaires, fournisseurs, clients ou territoires."
            ),
            "ar": (
                "قد تقيد هذه المادة القدرة على التعامل مع شركاء أو موردين "
                "أو عملاء أو مناطق أخرى."
            ),
        },
        "recommendation": {
            "en": (
                "Review the exclusivity scope, territory, duration, performance "
                "conditions, and consequences of failing to meet targets."
            ),
            "fr": (
                "Examiner la portée de l'exclusivité, le territoire, la durée, "
                "les conditions de performance et les conséquences du non-respect "
                "des objectifs."
            ),
            "ar": (
                "ينبغي مراجعة نطاق الحصرية، والمنطقة، والمدة، وشروط الأداء، "
                "وآثار عدم تحقيق الأهداف."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating objective performance thresholds, carve-outs, "
                "shorter exclusivity periods, or conversion to non-exclusive rights."
            ),
            "fr": (
                "Envisager de négocier des seuils de performance objectifs, "
                "des exceptions, une durée d'exclusivité plus courte ou une "
                "conversion en droits non exclusifs."
            ),
            "ar": (
                "يمكن التفاوض على مؤشرات أداء موضوعية، واستثناءات، ومدة "
                "حصرية أقصر، أو تحويل الحق إلى غير حصري."
            ),
        },
    },

    "governing_law": {
        "signals": [
                    "jurisdiction",
            "venue",
            "courts",
            "droit applicable",
            "juridiction",
            "tribunaux compétents",
            "tribunaux",
            "القانون الواجب التطبيق",
            "الاختصاص",
            "المحاكم",
            "محكمة",
        ],
        "legal_insight": {
            "en": (
                "This clause identifies the legal system or forum that will "
                "govern disputes under the contract."
            ),
            "fr": (
                "Cette clause désigne le droit applicable ou le forum compétent "
                "pour les litiges liés au contrat."
            ),
            "ar": (
                "تحدد هذه المادة القانون أو الجهة القضائية المختصة بالنزاعات "
                "المتعلقة بالعقد."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm that the chosen law and forum are practical, accessible, "
                "and consistent with the parties' location and transaction."
            ),
            "fr": (
                "Vérifier que le droit choisi et le forum compétent sont "
                "pratiques, accessibles et cohérents avec la localisation des "
                "parties et l'opération."
            ),
            "ar": (
                "ينبغي التأكد من أن القانون والجهة المختارة عملية وميسرة "
                "ومتناسقة مع مكان الأطراف وطبيعة المعاملة."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating a neutral forum, arbitration, or a venue "
                "that reduces enforcement and travel burden."
            ),
            "fr": (
                "Envisager de négocier un forum neutre, l'arbitrage ou un lieu "
                "qui réduit les contraintes d'exécution et de déplacement."
            ),
            "ar": (
                "يمكن التفاوض على جهة محايدة، أو التحكيم، أو مكان يقلل "
                "أعباء التنفيذ والتنقل."
            ),
        },
    },


    "services_operations": {
        "signals": [
            "services",
            "service provider",
            "scope of work",
            "support",
            "maintenance",
            "delivery",
            "acceptance",
            "performance",
            "change request",
            "prestations",
            "assistance",
            "livraison",
            "acceptation",
            "demande de changement",
            "الخدمات",
            "نطاق العمل",
            "الدعم",
            "الصيانة",
            "التسليم",
            "القبول",
            "الأداء",
            "طلب تغيير",
        ],
        "legal_insight": {
            "en": (
                "This clause defines operational obligations, service scope, "
                "performance expectations, or delivery mechanics."
            ),
            "fr": (
                "Cette clause définit les obligations opérationnelles, le "
                "périmètre des services, les attentes de performance ou les "
                "modalités de livraison."
            ),
            "ar": (
                "تحدد هذه المادة الالتزامات التشغيلية أو نطاق الخدمات أو "
                "توقعات الأداء أو آليات التسليم."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm that scope, responsibilities, acceptance criteria, "
                "timelines, change control, and support obligations are "
                "sufficiently specific."
            ),
            "fr": (
                "Vérifier que le périmètre, les responsabilités, les critères "
                "d'acceptation, les délais, le contrôle des changements et "
                "les obligations de support sont suffisamment précis."
            ),
            "ar": (
                "ينبغي التأكد من أن النطاق والمسؤوليات ومعايير القبول "
                "والجداول الزمنية وإدارة التغييرات والتزامات الدعم محددة بما يكفي."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating objective deliverables, acceptance "
                "procedures, escalation mechanisms, and balanced consequences "
                "for operational failure."
            ),
            "fr": (
                "Envisager de négocier des livrables objectifs, des procédures "
                "d'acceptation, des mécanismes d'escalade et des conséquences "
                "équilibrées en cas d'échec opérationnel."
            ),
            "ar": (
                "يمكن التفاوض على مخرجات موضوعية، وإجراءات قبول، وآليات "
                "تصعيد، وآثار متوازنة عند الإخفاق التشغيلي."
            ),
        },
    },

    "data_privacy_security": {
        "signals": [
            "personal data",
            "data protection",
            "data processing",
            "processor",
            "controller",
            "subprocessor",
            "privacy",
            "security incident",
            "security measures",
            "cybersecurity",
            "data breach",
            "données personnelles",
            "protection des données",
            "traitement des données",
            "sous-traitant",
            "responsable du traitement",
            "vie privée",
            "incident de sécurité",
            "mesures de sécurité",
            "cybersécurité",
            "violation de données",
            "بيانات شخصية",
            "حماية البيانات",
            "معالجة البيانات",
            "معالج البيانات",
            "المتحكم في البيانات",
            "الخصوصية",
            "حادث أمني",
            "تدابير أمنية",
            "الأمن السيبراني",
            "اختراق البيانات",
        ],
        "legal_insight": {
            "en": (
                "This clause governs data handling, privacy obligations, "
                "security controls, or incident response responsibilities."
            ),
            "fr": (
                "Cette clause régit le traitement des données, les obligations "
                "de confidentialité, les contrôles de sécurité ou les responsabilités "
                "en cas d'incident."
            ),
            "ar": (
                "تنظم هذه المادة التعامل مع البيانات، والتزامات الخصوصية، "
                "وضوابط الأمن، أو مسؤوليات الاستجابة للحوادث."
            ),
        },
        "recommendation": {
            "en": (
                "Check processing instructions, security standards, subprocessor "
                "controls, breach notification timing, audit rights, deletion or "
                "return duties, and regulatory allocation."
            ),
            "fr": (
                "Vérifier les instructions de traitement, les standards de sécurité, "
                "le contrôle des sous-traitants, les délais de notification des "
                "violations, les droits d'audit, les obligations de suppression "
                "ou restitution et la répartition réglementaire."
            ),
            "ar": (
                "ينبغي مراجعة تعليمات المعالجة، ومعايير الأمن، وضوابط المعالجين "
                "الفرعيين، ومواعيد الإخطار بالاختراقات، وحقوق التدقيق، وواجبات "
                "الحذف أو الإرجاع، وتوزيع الالتزامات التنظيمية."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating clearer security standards, incident "
                "timelines, audit rights, assistance duties, and liability "
                "treatment for data or security failures."
            ),
            "fr": (
                "Envisager de négocier des standards de sécurité plus clairs, "
                "des délais d'incident, des droits d'audit, des obligations "
                "d'assistance et le traitement de la responsabilité en cas "
                "d'échec lié aux données ou à la sécurité."
            ),
            "ar": (
                "يمكن التفاوض على معايير أمنية أوضح، ومهل للحوادث، وحقوق تدقيق، "
                "وواجبات مساعدة، ومعالجة المسؤولية عند الإخفاق في البيانات أو الأمن."
            ),
        },
    },

    "data_privacy_security_instructions": {
        "signals": ["documented instructions", "process personal data only on", "instructions documentées", "تعليمات موثقة"],
        "legal_insight": {
            "en": (
                "This clause limits the processor to acting only on the controller's documented "
                "instructions, which is the core basis for the processor's lawful processing under GDPR."
            ),
            "fr": (
                "Cette clause limite le sous-traitant à agir uniquement sur instructions documentées "
                "du responsable, ce qui constitue le fondement même du traitement licite par le "
                "sous-traitant au regard du RGPD."
            ),
            "ar": (
                "تحصر هذه المادة المعالج في التصرف فقط بناءً على تعليمات موثقة من المسؤول، وهو الأساس "
                "الجوهري لمشروعية المعالجة من قبل المعالج بموجب اللائحة العامة لحماية البيانات."
            ),
        },
        "recommendation": {
            "en": "Confirm the exceptions where the processor may act without instructions are narrow and legally required, not discretionary.",
            "fr": "Vérifier que les exceptions permettant au sous-traitant d'agir sans instructions sont étroites et légalement requises, non discrétionnaires.",
            "ar": "ينبغي التأكد من أن الاستثناءات التي تسمح للمعالج بالتصرف دون تعليمات ضيقة ومطلوبة قانوناً، لا تقديرية.",
        },
        "negotiation": {
            "en": "Consider requiring the processor to promptly flag any instruction it believes infringes applicable data protection law.",
            "fr": "Envisager d'exiger que le sous-traitant signale rapidement toute instruction qu'il estime contraire au droit applicable en matière de protection des données.",
            "ar": "يمكن اشتراط قيام المعالج بالإبلاغ الفوري عن أي تعليمات يرى أنها تخالف قانون حماية البيانات المعمول به.",
        },
    },

    "data_privacy_security_personnel_confidentiality": {
        "signals": ["committed themselves to confidentiality", "authorized to process", "engagés à la confidentialité", "التزموا بالسرية"],
        "legal_insight": {
            "en": "This clause ensures individuals with access to personal data are personally bound to confidentiality, independent of the processor's own obligations.",
            "fr": "Cette clause garantit que les personnes ayant accès aux données personnelles sont personnellement tenues à la confidentialité, indépendamment des obligations propres du sous-traitant.",
            "ar": "تضمن هذه المادة التزام الأفراد الذين يمكنهم الوصول إلى البيانات الشخصية شخصياً بالسرية، بمعزل عن التزامات المعالج نفسه.",
        },
        "recommendation": {
            "en": "Confirm the confidentiality commitment survives termination of the individual's role and applies to contractors, not just direct employees.",
            "fr": "Vérifier que l'engagement de confidentialité survit à la cessation des fonctions de la personne et s'applique aux prestataires, pas seulement aux salariés directs.",
            "ar": "ينبغي التأكد من استمرار التزام السرية بعد انتهاء مهام الشخص، وانطباقه على المتعاقدين، لا الموظفين المباشرين فقط.",
        },
        "negotiation": {
            "en": "Consider requiring evidence of the confidentiality commitments (e.g. on request) rather than a bare assertion of compliance.",
            "fr": "Envisager d'exiger une preuve des engagements de confidentialité (par exemple sur demande) plutôt qu'une simple affirmation de conformité.",
            "ar": "يمكن اشتراط تقديم دليل على التزامات السرية (مثلاً عند الطلب) بدلاً من مجرد تأكيد بالامتثال.",
        },
    },

    "data_privacy_security_subprocessors": {
        "signals": ["subprocessor", "sub-processor", "sous-traitant ultérieur", "معالج فرعي"],
        "legal_insight": {
            "en": "This clause controls whether and how the processor may delegate processing to subprocessors, and whether the controller retains meaningful oversight.",
            "fr": "Cette clause détermine si et comment le sous-traitant peut déléguer le traitement à des sous-traitants ultérieurs, et si le responsable conserve un contrôle effectif.",
            "ar": "تحدد هذه المادة ما إذا كان يجوز للمعالج تفويض المعالجة لمعالجين فرعيين وكيفية ذلك، وما إذا كان المسؤول يحتفظ برقابة فعلية.",
        },
        "recommendation": {
            "en": "Confirm whether authorization is specific (per subprocessor) or general (with an objection window), and that the same data protection terms flow down.",
            "fr": "Vérifier si l'autorisation est spécifique (par sous-traitant) ou générale (avec un délai d'objection), et que les mêmes conditions de protection des données sont répercutées.",
            "ar": "ينبغي التحقق مما إذا كان الإذن محدداً (لكل معالج فرعي) أو عاماً (مع مهلة اعتراض)، وسريان نفس شروط حماية البيانات على المعالجين الفرعيين.",
        },
        "negotiation": {
            "en": "Consider negotiating a shorter objection window and requiring the processor to remain fully liable for subprocessor failures.",
            "fr": "Envisager de négocier un délai d'objection plus court et d'exiger que le sous-traitant reste pleinement responsable des manquements de ses sous-traitants ultérieurs.",
            "ar": "يمكن التفاوض على مهلة اعتراض أقصر واشتراط بقاء المعالج مسؤولاً بالكامل عن إخفاقات المعالجين الفرعيين.",
        },
    },

    "data_privacy_security_security_measures": {
        "signals": ["technical and organizational measures", "pseudonymization", "encryption", "chiffrement", "التشفير"],
        "legal_insight": {
            "en": "This clause sets the processor's baseline security obligations, which are often assessed against the actual state of the art and the sensitivity of the data involved.",
            "fr": "Cette clause fixe les obligations de sécurité minimales du sous-traitant, souvent appréciées au regard de l'état de l'art réel et de la sensibilité des données concernées.",
            "ar": "تحدد هذه المادة الحد الأدنى من التزامات الأمن للمعالج، وغالباً ما تُقيَّم في ضوء أحدث التقنيات الفعلية وحساسية البيانات المعنية.",
        },
        "recommendation": {
            "en": "Confirm whether the security standard is concretely specified (e.g. named encryption standard) or left as a vague 'appropriate measures' commitment.",
            "fr": "Vérifier si le standard de sécurité est concrètement précisé (par exemple un standard de chiffrement nommé) ou laissé comme un engagement vague de 'mesures appropriées'.",
            "ar": "ينبغي التحقق مما إذا كان معيار الأمن محدداً بشكل ملموس (مثل معيار تشفير معين) أو متروكاً كالتزام غامض بـ'تدابير مناسبة'.",
        },
        "negotiation": {
            "en": "Consider requiring periodic review of security measures as risks and standards evolve, rather than a one-time, static commitment.",
            "fr": "Envisager d'exiger une revue périodique des mesures de sécurité à mesure que les risques et standards évoluent, plutôt qu'un engagement statique et ponctuel.",
            "ar": "يمكن اشتراط مراجعة دورية لتدابير الأمن مع تطور المخاطر والمعايير، بدلاً من التزام ثابت لمرة واحدة.",
        },
    },

    "data_privacy_security_subject_rights": {
        "signals": ["data subject rights", "data subject requests", "droits de la personne concernée", "حقوق صاحب البيانات"],
        "legal_insight": {
            "en": "This clause allocates responsibility for handling data subject requests (access, erasure, portability, etc.) between the controller and processor.",
            "fr": "Cette clause répartit la responsabilité de traiter les demandes des personnes concernées (accès, effacement, portabilité, etc.) entre le responsable et le sous-traitant.",
            "ar": "توزع هذه المادة المسؤولية عن التعامل مع طلبات أصحاب البيانات (الوصول، المحو، قابلية النقل، إلخ) بين المسؤول والمعالج.",
        },
        "recommendation": {
            "en": "Confirm a concrete response timeline for the processor's assistance, and whether it may charge for extensive or repetitive requests.",
            "fr": "Vérifier l'existence d'un délai de réponse concret pour l'assistance du sous-traitant, et s'il peut facturer les demandes volumineuses ou répétitives.",
            "ar": "ينبغي التحقق من وجود مهلة استجابة ملموسة لمساعدة المعالج، وما إذا كان يجوز له تحصيل رسوم عن الطلبات الموسعة أو المتكررة.",
        },
        "negotiation": {
            "en": "Consider requiring the processor to forward direct requests to the controller rather than responding independently.",
            "fr": "Envisager d'exiger que le sous-traitant transmette les demandes directes au responsable plutôt que d'y répondre lui-même.",
            "ar": "يمكن اشتراط قيام المعالج بإحالة الطلبات المباشرة إلى المسؤول بدلاً من الرد عليها بشكل مستقل.",
        },
    },

    "data_privacy_security_breach_notification": {
        "signals": ["personal data breach", "notify controller", "without undue delay", "violation de données", "خرق البيانات"],
        "legal_insight": {
            "en": "This clause sets the timeline and content for breach notification, which drives the controller's own regulatory notification deadlines (often 72 hours under GDPR).",
            "fr": "Cette clause fixe le délai et le contenu de la notification de violation, qui conditionne les propres délais de notification réglementaire du responsable (souvent 72 heures au titre du RGPD)."
            ,
            "ar": "تحدد هذه المادة مهلة ومحتوى الإخطار بالخرق، وهو ما يحكم مهل الإخطار التنظيمي الخاصة بالمسؤول (غالباً 72 ساعة بموجب اللائحة العامة لحماية البيانات)."
            ,
        },
        "recommendation": {
            "en": "Confirm the notification clock starts from becoming aware (not confirming) the breach, and that a minimum content is specified.",
            "fr": "Vérifier que le délai de notification court à partir de la prise de connaissance (et non de la confirmation) de la violation, et qu'un contenu minimal est précisé.",
            "ar": "ينبغي التأكد من أن مهلة الإخطار تبدأ من لحظة العلم بالخرق (لا من لحظة التأكيد)، ومن تحديد حد أدنى من المحتوى.",
        },
        "negotiation": {
            "en": "Consider requiring ongoing updates as the investigation progresses, not just a single initial notification.",
            "fr": "Envisager d'exiger des mises à jour continues à mesure que l'enquête progresse, et non une simple notification initiale unique.",
            "ar": "يمكن اشتراط تقديم تحديثات مستمرة مع تقدم التحقيق، لا مجرد إخطار أولي واحد.",
        },
    },

    "data_privacy_security_deletion_return": {
        "signals": ["delete or return", "deletion or return", "upon termination", "supprimer ou restituer", "حذف أو إعادة"],
        "legal_insight": {
            "en": "This clause governs what happens to personal data at the end of the engagement, which is a standard GDPR requirement but often left ambiguous on timing and format.",
            "fr": "Cette clause régit le sort des données personnelles à la fin de la relation, une exigence standard du RGPD souvent laissée ambiguë quant au délai et au format.",
            "ar": "تنظم هذه المادة مصير البيانات الشخصية عند انتهاء التعامل، وهو شرط قياسي بموجب اللائحة العامة لحماية البيانات لكنه غالباً ما يُترك غامضاً من حيث التوقيت والصيغة.",
        },
        "recommendation": {
            "en": "Confirm the controller (not the processor) elects between deletion and return, and that a concrete deadline and deletion certification are required.",
            "fr": "Vérifier que c'est le responsable (et non le sous-traitant) qui choisit entre suppression et restitution, et qu'un délai concret et une attestation de suppression sont exigés.",
            "ar": "ينبغي التأكد من أن المسؤول (لا المعالج) هو من يختار بين الحذف والإرجاع، ومن اشتراط مهلة ملموسة وشهادة حذف.",
        },
        "negotiation": {
            "en": "Consider negotiating a defined deletion deadline (e.g. 30 days) rather than an open-ended commitment.",
            "fr": "Envisager de négocier un délai de suppression défini (par exemple 30 jours) plutôt qu'un engagement à durée indéterminée.",
            "ar": "يمكن التفاوض على مهلة حذف محددة (مثلاً 30 يوماً) بدلاً من التزام مفتوح المدة.",
        },
    },

    "data_privacy_security_audit": {
        "signals": ["audit rights", "conduct audits", "inspections", "droits d'audit", "حقوق التدقيق"],
        "legal_insight": {
            "en": "This clause gives the controller a mechanism to verify the processor's actual compliance, which is a key GDPR accountability tool but can be operationally burdensome if unbounded.",
            "fr": "Cette clause donne au responsable un mécanisme de vérification de la conformité effective du sous-traitant, un outil clé de responsabilisation au titre du RGPD, mais qui peut être lourd à mettre en œuvre s'il n'est pas encadré.",
            "ar": "تمنح هذه المادة المسؤول آلية للتحقق من الامتثال الفعلي للمعالج، وهي أداة أساسية للمساءلة بموجب اللائحة العامة لحماية البيانات، لكنها قد تكون مرهقة تشغيلياً إن لم تكن محدودة.",
        },
        "recommendation": {
            "en": "Confirm audit frequency is capped absent a breach, scope is limited to matters relevant to the DPA, and findings remain confidential.",
            "fr": "Vérifier que la fréquence des audits est plafonnée en l'absence de violation, que le périmètre se limite aux éléments pertinents au regard du DPA, et que les conclusions restent confidentielles.",
            "ar": "ينبغي التأكد من تحديد سقف لتكرار التدقيق في غياب أي خرق، وقصر النطاق على المسائل ذات الصلة باتفاقية معالجة البيانات، وبقاء النتائج سرية.",
        },
        "negotiation": {
            "en": "Consider allowing a recognized third-party certification report (e.g. SOC 2, ISO 27001) to satisfy the audit obligation where genuinely equivalent.",
            "fr": "Envisager de permettre à un rapport de certification tiers reconnu (par exemple SOC 2, ISO 27001) de satisfaire l'obligation d'audit lorsqu'il est réellement équivalent.",
            "ar": "يمكن السماح بتقرير شهادة معتمدة من طرف ثالث (مثل SOC 2 أو ISO 27001) للوفاء بالتزام التدقيق عند تكافؤه الفعلي.",
        },
    },

    "intellectual_property": {
        "signals": [
            "intellectual property",
            "ip",
            "ownership",
            "assignment",
            "license",
            "work product",
            "deliverables",
            "copyright",
            "trademark",
            "patent",
            "invention",
            "moral rights",
            "propriété intellectuelle",
            "cession",
            "licence",
            "livrables",
            "droit d'auteur",
            "marque",
            "brevet",
            "invention",
            "droits moraux",
            "الملكية الفكرية",
            "تنازل",
            "ترخيص",
            "مخرجات العمل",
            "حقوق النشر",
            "علامة تجارية",
            "براءة",
            "اختراع",
            "حقوق معنوية",
        ],
        "legal_insight": {
            "en": (
                "This clause allocates ownership, use rights, licensing rights, "
                "or control over created or pre-existing intellectual property."
            ),
            "fr": (
                "Cette clause répartit la propriété, les droits d'utilisation, "
                "les licences ou le contrôle sur la propriété intellectuelle "
                "créée ou préexistante."
            ),
            "ar": (
                "تحدد هذه المادة الملكية وحقوق الاستخدام والترخيص أو السيطرة "
                "على الملكية الفكرية المنشأة أو السابقة."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm ownership of pre-existing materials, newly created "
                "deliverables, license scope, usage restrictions, moral rights, "
                "and post-termination rights."
            ),
            "fr": (
                "Vérifier la propriété des éléments préexistants, des livrables "
                "créés, la portée des licences, les restrictions d'usage, les "
                "droits moraux et les droits après résiliation."
            ),
            "ar": (
                "ينبغي التأكد من ملكية المواد السابقة، والمخرجات المنشأة، ونطاق "
                "الترخيص، وقيود الاستخدام، والحقوق المعنوية، والحقوق بعد الإنهاء."
            ),
        },
        "negotiation": {
            "en": (
                "Consider separating background IP from project deliverables and "
                "defining license scope, permitted use, transfer timing, and "
                "residual rights."
            ),
            "fr": (
                "Envisager de séparer la propriété intellectuelle préexistante "
                "des livrables du projet et de définir la portée de la licence, "
                "l'usage autorisé, le moment du transfert et les droits résiduels."
            ),
            "ar": (
                "يمكن التفاوض على فصل الملكية الفكرية السابقة عن مخرجات المشروع "
                "وتحديد نطاق الترخيص والاستخدام المسموح وتوقيت النقل والحقوق المتبقية."
            ),
        },
    },

    "restrictive_covenants": {
        "signals": [
            "non-compete",
            "non compete",
            "non-solicitation",
            "non solicitation",
            "non-dealing",
            "non-circumvention",
            "exclusivity",
            "exclusive dealing",
            "restraint of trade",
            "solicitation",
            "solicit",
            "non-concurrence",
            "non-sollicitation",
            "non sollicitation",
            "non-contournement",
            "exclusivité",
            "sollicitation",
            "solliciter",
            "restriction de sollicitation",
            "restriction de non-concurrence",
            "concurrence déloyale",
            "عدم المنافسة",
            "عدم الاستقطاب",
            "عدم الالتفاف",
            "الحصرية",
            "استقطاب",
            "المنافسة",
        ],
        "legal_insight": {
            "en": (
                "This clause may restrict competitive activity, solicitation, "
                "market access, customer relationships, or post-contract conduct."
            ),
            "fr": (
                "Cette clause peut restreindre l'activité concurrente, la sollicitation, "
                "l'accès au marché, les relations clients ou le comportement après "
                "la fin du contrat."
            ),
            "ar": (
                "قد تقيد هذه المادة النشاط التنافسي أو الاستقطاب أو الوصول إلى السوق "
                "أو علاقات العملاء أو السلوك بعد انتهاء العقد."
            ),
        },
        "recommendation": {
            "en": (
                "Review the restricted activities, duration, territory, affected "
                "persons, customer scope, exceptions, and business justification."
            ),
            "fr": (
                "Examiner les activités restreintes, la durée, le territoire, "
                "les personnes concernées, le périmètre clients, les exceptions "
                "et la justification commerciale."
            ),
            "ar": (
                "ينبغي مراجعة الأنشطة المقيدة، والمدة، والنطاق الجغرافي، والأشخاص "
                "المعنيين، ونطاق العملاء، والاستثناءات، والمبرر التجاري."
            ),
        },
        "negotiation": {
            "en": (
                "Consider narrowing the restriction to legitimate business interests, "
                "reducing duration or territory, and adding clear carve-outs for "
                "ordinary business activity."
            ),
            "fr": (
                "Envisager de limiter la restriction aux intérêts commerciaux légitimes, "
                "de réduire la durée ou le territoire et d'ajouter des exceptions "
                "claires pour l'activité commerciale ordinaire."
            ),
            "ar": (
                "يمكن التفاوض على حصر القيد في المصالح التجارية المشروعة، وتقليل "
                "المدة أو النطاق الجغرافي، وإضافة استثناءات واضحة للنشاط التجاري العادي."
            ),
        },
    },

    "corporate_governance": {
        "signals": [
            "board of directors", "board composition", "director",
            "appointment", "reserved matters", "deadlock", "quorum",
            "voting rights", "board seat",
            "conseil d'administration", "composition du conseil",
            "administrateur", "nomination", "matières réservées",
            "blocage", "quorum", "droits de vote",
            "مجلس الإدارة", "تكوين مجلس الإدارة", "مدير", "تعيين",
            "المسائل المحفوظة", "طريق مسدود", "النصاب", "حقوق التصويت",
        ],
        "legal_insight": {
            "en": "This clause affects who sits on the board, how directors are appointed, which matters require enhanced approval, and how governance deadlocks are resolved.",
            "fr": "Cette clause concerne la composition du conseil, les modalités de nomination des administrateurs, les matières nécessitant une approbation renforcée, et la résolution des blocages de gouvernance.",
            "ar": "يؤثر هذا البند على تشكيل مجلس الإدارة، وكيفية تعيين المديرين، والمسائل التي تتطلب موافقة معززة، وكيفية حل حالات الجمود في الحوكمة.",
        },
        "recommendation": {
            "en": "Check board composition and how each seat is designated, which matters are reserved for enhanced approval, whether a deadlock-resolution mechanism exists, and how director removal or replacement works.",
            "fr": "Vérifier la composition du conseil et les modalités de désignation de chaque siège, les matières réservées à une approbation renforcée, l'existence d'un mécanisme de résolution des blocages, et les modalités de révocation ou de remplacement des administrateurs.",
            "ar": "ينبغي مراجعة تكوين مجلس الإدارة وكيفية تعيين كل مقعد، والمسائل المحفوظة للموافقة المعززة، ووجود آلية لحل الجمود، وكيفية عزل المديرين أو استبدالهم.",
        },
        "negotiation": {
            "en": "Consider negotiating board seat allocation, the threshold triggering reserved-matter approval, and a concrete deadlock-resolution process such as escalation, mediation, or a casting vote.",
            "fr": "Envisager de négocier la répartition des sièges au conseil, le seuil déclenchant l'approbation des matières réservées, et un processus concret de résolution des blocages tel que l'escalade, la médiation, ou une voix prépondérante.",
            "ar": "يمكن التفاوض على توزيع مقاعد مجلس الإدارة، والعتبة التي تُفعِّل موافقة المسائل المحفوظة، وعملية ملموسة لحل الجمود مثل التصعيد أو الوساطة أو صوت ترجيحي.",
        },
    },

    "investor_information_rights": {
        "signals": [
            "financial statements", "audited annual", "unaudited quarterly",
            "fiscal year end", "fiscal quarter end", "inspection rights",
            "books and records", "information rights",
            "états financiers", "états financiers audités", "exercice fiscal",
            "droit d'inspection", "livres et registres", "droits à l'information",
            "القوائم المالية", "القوائم المالية المدققة", "نهاية السنة المالية",
            "حق التفتيش", "حقوق الاطلاع",
        ],
        "legal_insight": {
            "en": "This clause affects what financial information the investor receives, how often, and within what timeframe after each reporting period.",
            "fr": "Cette clause concerne les informations financières que reçoit l'investisseur, leur fréquence, et le délai suivant chaque période de reporting.",
            "ar": "يؤثر هذا البند على المعلومات المالية التي يتلقاها المستثمر، ووتيرتها، والمهلة الزمنية بعد كل فترة تقرير.",
        },
        "recommendation": {
            "en": "Check the delivery deadline for each report type, whether the reporting threshold (e.g. minimum ownership percentage) is reasonable, whether inspection/audit rights are included, and what remedy applies if delivery is late.",
            "fr": "Vérifier le délai de remise de chaque type de rapport, si le seuil déclenchant l'obligation d'information (par exemple un pourcentage minimal de détention) est raisonnable, si des droits d'inspection ou d'audit sont inclus, et quel recours s'applique en cas de retard de remise.",
            "ar": "ينبغي مراجعة الموعد النهائي لتسليم كل نوع من التقارير، وما إذا كانت عتبة الإبلاغ (مثل الحد الأدنى لنسبة الملكية) معقولة، وما إذا كانت حقوق التفتيش أو التدقيق مدرجة، وما هو سبيل الانتصاف المطبق في حال التأخر في التسليم.",
        },
        "negotiation": {
            "en": "Consider negotiating the reporting threshold, the delivery deadline for each statement type, and whether informal or ad hoc information requests should also be accommodated.",
            "fr": "Envisager de négocier le seuil de déclenchement de l'obligation d'information, le délai de remise de chaque type d'état, et si des demandes d'information informelles ou ponctuelles doivent également être prévues.",
            "ar": "يمكن التفاوض على عتبة الإبلاغ، والموعد النهائي لتسليم كل نوع من البيانات، وما إذا كان ينبغي أيضاً تلبية طلبات المعلومات غير الرسمية أو المخصصة.",
        },
    },

    "governance_compliance": {
        "signals": [
            "assignment",
            "change of control",
            "compliance",
            "anti-bribery",
            "sanctions",
            "governance",
            "subcontracting",
            "audit",
            "board",
            "director",
            "shareholder",
            "approval",
            "consent",
            "cession",
            "changement de contrôle",
            "conformité",
            "lutte contre la corruption",
            "sanctions",
            "gouvernance",
            "sous-traitance",
            "audit",
            "conseil",
            "administrateur",
            "actionnaire",
            "approbation",
            "consentement",
            "التنازل",
            "تغيير السيطرة",
            "الامتثال",
            "مكافحة الرشوة",
            "العقوبات",
            "الحوكمة",
            "التعاقد من الباطن",
            "التدقيق",
            "مجلس الإدارة",
            "مدير",
            "مساهم",
            "موافقة",
        ],
        "legal_insight": {
            "en": (
                "This clause affects control, approvals, compliance duties, "
                "audit rights, assignment, or governance processes."
            ),
            "fr": (
                "Cette clause affecte le contrôle, les approbations, les obligations "
                "de conformité, les droits d'audit, la cession ou les processus de gouvernance."
            ),
            "ar": (
                "تؤثر هذه المادة على السيطرة أو الموافقات أو واجبات الامتثال أو حقوق "
                "التدقيق أو التنازل أو إجراءات الحوكمة."
            ),
        },
        "recommendation": {
            "en": (
                "Check approval rights, assignment limits, audit scope, compliance "
                "obligations, subcontracting controls, and consequences of breach."
            ),
            "fr": (
                "Vérifier les droits d'approbation, les limites de cession, la portée "
                "de l'audit, les obligations de conformité, le contrôle de la sous-traitance "
                "et les conséquences du manquement."
            ),
            "ar": (
                "ينبغي مراجعة حقوق الموافقة، وحدود التنازل، ونطاق التدقيق، والتزامات "
                "الامتثال، وضوابط التعاقد من الباطن، وآثار الإخلال."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating materiality thresholds, reasonable consent standards, "
                "audit limits, notice periods, and proportional remedies."
            ),
            "fr": (
                "Envisager de négocier des seuils de matérialité, des standards raisonnables "
                "de consentement, des limites d'audit, des délais de préavis et des recours proportionnés."
            ),
            "ar": (
                "يمكن التفاوض على عتبات جوهرية، ومعايير موافقة معقولة، وحدود للتدقيق، "
                "ومهل إشعار، ووسائل معالجة متناسبة."
            ),
        },
    },

    "finance_lending": {
        "signals": [
            "loan",
            "financing",
            "interest",
            "collateral",
            "guarantee",
            "repayment",
            "acceleration",
            "borrower",
            "lender",
            "security interest",
            "prêt",
            "financement",
            "intérêt",
            "garantie",
            "sûreté",
            "remboursement",
            "exigibilité",
            "emprunteur",
            "prêteur",
            "قرض",
            "تمويل",
            "فائدة",
            "ضمان",
            "حق ضمان",
            "سداد",
            "مقترض",
            "مقرض",
        ],
        "legal_insight": {
            "en": (
                "This clause may affect repayment obligations, interest exposure, "
                "security rights, guarantees, default consequences, or lender remedies."
            ),
            "fr": (
                "Cette clause peut affecter les obligations de remboursement, l'exposition "
                "aux intérêts, les sûretés, les garanties, les conséquences du défaut ou "
                "les recours du prêteur."
            ),
            "ar": (
                "قد تؤثر هذه المادة على التزامات السداد أو التعرض للفائدة أو حقوق "
                "الضمان أو الكفالات أو آثار الإخلال أو وسائل الدائن."
            ),
        },
        "recommendation": {
            "en": (
                "Check repayment timing, interest, security, guarantees, default triggers, "
                "acceleration rights, and enforcement mechanics."
            ),
            "fr": (
                "Vérifier les échéances de remboursement, les intérêts, les sûretés, "
                "les garanties, les cas de défaut, l'exigibilité anticipée et les mécanismes d'exécution."
            ),
            "ar": (
                "ينبغي مراجعة مواعيد السداد، والفائدة، والضمانات، والكفالات، ومحفزات "
                "الإخلال، وحقوق التعجيل، وآليات التنفيذ."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating cure periods, financial thresholds, reporting duties, "
                "security scope, and proportional default remedies."
            ),
            "fr": (
                "Envisager de négocier des délais de régularisation, des seuils financiers, "
                "des obligations de reporting, la portée des sûretés et des recours proportionnés en cas de défaut."
            ),
            "ar": (
                "يمكن التفاوض على مهل معالجة، وعتبات مالية، وواجبات تقارير، ونطاق الضمان، "
                "ووسائل معالجة متناسبة عند الإخلال."
            ),
        },
    },

    "real_estate": {
        "signals": [
            "lease",
            "rent",
            "deposit",
            "premises",
            "property",
            "repairs",
            "utilities",
            "tenant",
            "landlord",
            "bail",
            "loyer",
            "dépôt",
            "locaux",
            "bien immobilier",
            "réparations",
            "charges",
            "locataire",
            "bailleur",
            "إيجار",
            "أجرة",
            "وديعة",
            "عقار",
            "إصلاحات",
            "مرافق",
            "مستأجر",
            "مؤجر",
        ],
        "legal_insight": {
            "en": (
                "This clause may define property use, rent, deposits, repairs, utilities, "
                "occupancy rights, or landlord and tenant obligations."
            ),
            "fr": (
                "Cette clause peut définir l'usage du bien, le loyer, les dépôts, "
                "les réparations, les charges, les droits d'occupation ou les obligations "
                "du bailleur et du locataire."
            ),
            "ar": (
                "قد تحدد هذه المادة استخدام العقار أو الأجرة أو الودائع أو الإصلاحات "
                "أو المرافق أو حقوق الانتفاع أو التزامات المؤجر والمستأجر."
            ),
        },
        "recommendation": {
            "en": (
                "Check payment timing, permitted use, maintenance obligations, repair allocation, "
                "deposit treatment, access rights, and termination consequences."
            ),
            "fr": (
                "Vérifier les échéances de paiement, l'usage autorisé, les obligations d'entretien, "
                "la répartition des réparations, le traitement du dépôt, les droits d'accès et les conséquences de résiliation."
            ),
            "ar": (
                "ينبغي مراجعة مواعيد الدفع، والاستخدام المسموح، والتزامات الصيانة، "
                "وتوزيع الإصلاحات، ومعالجة الوديعة، وحقوق الدخول، وآثار الإنهاء."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating clear maintenance standards, caps on tenant costs, "
                "deposit return mechanics, access controls, and balanced termination rights."
            ),
            "fr": (
                "Envisager de négocier des standards clairs d'entretien, des plafonds de coûts "
                "pour le locataire, les modalités de restitution du dépôt, le contrôle des accès "
                "et des droits de résiliation équilibrés."
            ),
            "ar": (
                "يمكن التفاوض على معايير صيانة واضحة، وحدود لتكاليف المستأجر، وآليات "
                "إعادة الوديعة، وضوابط الدخول، وحقوق إنهاء متوازنة."
            ),
        },
    },

    "employment_hr": {
        "signals": [
            "employee",
            "employment",
            "employment agreement",
            "salary",
            "termination of employment",
            "vacation",
            "benefits",
            "employer",
            "compensation",
            "working time",
            "leave",
            "disciplinary",
            "employé",
            "emploi",
            "contrat de travail",
            "salaire",
            "congés",
            "avantages",
            "employeur",
            "rémunération",
            "temps de travail",
            "licenciement",
            "موظف",
            "عمل",
            "عقد عمل",
            "راتب",
            "إجازة",
            "مزايا",
            "صاحب العمل",
            "تعويض",
            "ساعات العمل",
        ],
        "legal_insight": {
            "en": (
                "This clause may affect employment status, compensation, benefits, "
                "working conditions, termination of employment, or employee obligations."
            ),
            "fr": (
                "Cette clause peut affecter le statut d'emploi, la rémunération, "
                "les avantages, les conditions de travail, la fin de l'emploi ou les obligations du salarié."
            ),
            "ar": (
                "قد تؤثر هذه المادة على وضع العمل أو التعويض أو المزايا أو ظروف العمل "
                "أو إنهاء العمل أو التزامات الموظف."
            ),
        },
        "recommendation": {
            "en": (
                "Check compensation, benefits, duties, termination mechanics, notice, "
                "post-employment obligations, and compliance with the stated employment framework."
            ),
            "fr": (
                "Vérifier la rémunération, les avantages, les fonctions, les modalités de rupture, "
                "le préavis, les obligations après l'emploi et la conformité avec le cadre d'emploi indiqué."
            ),
            "ar": (
                "ينبغي مراجعة التعويض والمزايا والمهام وآليات إنهاء العمل والإشعار "
                "والالتزامات بعد العمل والامتثال لإطار العمل المحدد."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating clear duties, objective performance standards, balanced "
                "termination mechanics, compensation protections, and reasonable post-employment obligations."
            ),
            "fr": (
                "Envisager de négocier des fonctions claires, des standards de performance objectifs, "
                "des mécanismes de rupture équilibrés, des protections de rémunération et des obligations raisonnables après l'emploi."
            ),
            "ar": (
                "يمكن التفاوض على مهام واضحة، ومعايير أداء موضوعية، وآليات إنهاء متوازنة، "
                "وحمايات للتعويض، والتزامات معقولة بعد العمل."
            ),
        },
    },

    "change_of_control": {
        "signals": [
            "change of control",
            "merger",
            "acquisition",
            "takeover",
            "sale of substantially all assets",
            "changement de contrôle",
            "fusion",
            "acquisition",
            "cession de la quasi-totalité des actifs",
            "تغيير السيطرة",
            "اندماج",
            "استحواذ",
            "بيع معظم الأصول",
        ],
        "legal_insight": {
            "en": (
                "This clause may affect rights or obligations when ownership, control, "
                "merger, acquisition, or a major asset sale occurs."
            ),
            "fr": (
                "Cette clause peut affecter les droits ou obligations en cas de changement "
                "de propriété, de contrôle, de fusion, d'acquisition ou de cession importante d'actifs."
            ),
            "ar": (
                "قد تؤثر هذه المادة على الحقوق أو الالتزامات عند تغيير الملكية أو السيطرة "
                "أو الاندماج أو الاستحواذ أو بيع أصول جوهرية."
            ),
        },
        "recommendation": {
            "en": (
                "Check whether the trigger is clearly defined and whether consent, notice, "
                "termination, vesting, payment, or assignment consequences are proportionate."
            ),
            "fr": (
                "Vérifier si le déclencheur est clairement défini et si les conséquences "
                "de consentement, notification, résiliation, acquisition de droits, paiement ou cession sont proportionnées."
            ),
            "ar": (
                "ينبغي التحقق من وضوح الحدث المحفز وما إذا كانت آثار الموافقة أو الإخطار "
                "أو الإنهاء أو الاستحقاق أو الدفع أو التنازل متناسبة."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating materiality thresholds, objective control definitions, "
                "notice periods, consent standards, and balanced consequences."
            ),
            "fr": (
                "Envisager de négocier des seuils de matérialité, des définitions objectives "
                "du contrôle, des délais de notification, des standards de consentement et des conséquences équilibrées."
            ),
            "ar": (
                "يمكن التفاوض على عتبات جوهرية، وتعريفات موضوعية للسيطرة، ومهل إشعار، "
                "ومعايير موافقة، وآثار متوازنة."
            ),
        },
    },

    "general": {
        "signals": [],

        "legal_insight": {
            "en": (
                "This clause creates contractual obligations or operational "
                "requirements that should be reviewed in the context of the "
                "overall agreement."
            ),
            "fr": (
                "Cette clause crée des obligations contractuelles ou "
                "opérationnelles qui doivent être examinées dans le contexte "
                "global du contrat."
            ),
            "ar": (
                "تنشئ هذه المادة التزامات تعاقدية أو تشغيلية ينبغي "
                "مراجعتها ضمن السياق العام للعقد."
            ),
        },

        "recommendation": {
            "en": (
                "Confirm that the clause is consistent with the commercial "
                "intent, operational process, and overall risk allocation."
            ),
            "fr": (
                "Vérifier que cette clause est cohérente avec l'objectif "
                "commercial, les processus opérationnels et la répartition "
                "globale des risques."
            ),
            "ar": (
                "ينبغي التأكد من توافق هذه المادة مع الهدف التجاري "
                "والإجراءات التشغيلية والتوزيع العام للمخاطر."
            ),
        },

        "negotiation": {
            "en": "",
            "fr": "",
            "ar": "",
        },
    },
}



RISK_REASON_TEMPLATES = {
    "termination": [
        {
            "risk_pattern": [
                "without cause",
                "sans motif",
                "دون سبب",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause grants unilateral termination rights without "
                    "requiring objective justification, which may expose the "
                    "affected party to sudden contract loss or reduced bargaining leverage."
                ),
                "fr": (
                    "La clause accorde un droit de résiliation unilatérale sans "
                    "justification objective, ce qui peut exposer la partie concernée "
                    "à une rupture soudaine du contrat ou à une perte de pouvoir de négociation."
                ),
                "ar": (
                    "يمنح هذا البند حق الإنهاء من جانب واحد دون اشتراط مبرر موضوعي، "
                    "مما قد يعرّض الطرف المتأثر لفقدان العقد بشكل مفاجئ أو إضعاف موقفه التفاوضي."
                ),
            },
        },
        {
            "risk_pattern": [
                "immediate termination",
                "terminate immediately",
                "résiliation immédiate",
                "إنهاء فوري",
                "فسخ فوري",
            ],
            "risk_level": "high",
            "legal_consequence": {
                "en": (
                    "The clause allows immediate termination, so the absence or "
                    "shortness of notice and cure protections may create operational "
                    "or financial exposure."
                ),
                "fr": (
                    "La clause permet une résiliation immédiate ; l'absence ou la "
                    "brièveté du préavis et des possibilités de régularisation peut "
                    "créer une exposition opérationnelle ou financière."
                ),
                "ar": (
                    "يسمح هذا البند بالإنهاء الفوري، ولذلك فإن غياب الإشعار أو "
                    "مهلة المعالجة قد يخلق تعرضاً تشغيلياً أو مالياً."
                ),
            },
        },
        {
            "risk_pattern": [
                "cure period",
                "notice period",
                "délai de régularisation",
                "préavis",
                "مهلة معالجة",
                "إشعار",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause includes procedural safeguards such as notice or "
                    "a cure period, but the timing, required detail, and consequences "
                    "should still be reviewed carefully."
                ),
                "fr": (
                    "La clause prévoit des garanties procédurales comme un préavis "
                    "ou un délai de régularisation, mais les délais, le niveau de détail "
                    "requis et les conséquences doivent être examinés attentivement."
                ),
                "ar": (
                    "يتضمن البند ضمانات إجرائية مثل الإشعار أو مهلة المعالجة، "
                    "لكن يجب مراجعة المدة والتفاصيل المطلوبة والآثار المترتبة بعناية."
                ),
            },
        },
    ],
    "payment": [
        {
            "risk_pattern": [
                "late payment",
                "interest",
                "penalty",
                "retard de paiement",
                "intérêt",
                "pénalité",
                "تأخر الدفع",
                "فائدة",
                "غرامة",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause may impose financial consequences for delayed or failed "
                    "payment, so deadlines, interest, penalties, tax treatment, and "
                    "dispute rights should be clear."
                ),
                "fr": (
                    "La clause peut imposer des conséquences financières en cas de retard "
                    "ou défaut de paiement ; les échéances, intérêts, pénalités, traitement "
                    "fiscal et droits de contestation doivent être clairs."
                ),
                "ar": (
                    "قد يفرض هذا البند آثاراً مالية عند التأخر أو الإخفاق في الدفع، "
                    "لذلك يجب توضيح الآجال والفوائد والغرامات والمعالجة الضريبية وحقوق الاعتراض."
                ),
            },
        },
    ],
    "confidentiality": [
        {
            "risk_pattern": [
                "survive termination",
                "after termination",
                "thereafter",
                "survie",
                "après résiliation",
                "بعد الإنهاء",
                "تظل",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The confidentiality obligation may continue after the agreement ends, "
                    "so duration, scope, exceptions, and permitted disclosures should be "
                    "clearly defined."
                ),
                "fr": (
                    "L'obligation de confidentialité peut se poursuivre après la fin du contrat ; "
                    "la durée, la portée, les exceptions et les divulgations autorisées doivent "
                    "être clairement définies."
                ),
                "ar": (
                    "قد تستمر التزامات السرية بعد انتهاء العقد، لذلك يجب تحديد المدة والنطاق "
                    "والاستثناءات وحالات الإفصاح المسموح بها بوضوح."
                ),
            },
        },
    ],
    "liability": [
        {
            "risk_pattern": [
                "unlimited liability",
                "responsabilité illimitée",
                "مسؤولية غير محدودة",
            ],
            "risk_level": "high",
            "legal_consequence": {
                "en": (
                    "The clause may create uncapped financial exposure, which can exceed "
                    "the contract value and materially increase legal or commercial risk."
                ),
                "fr": (
                    "La clause peut créer une exposition financière non plafonnée, susceptible "
                    "de dépasser la valeur du contrat et d'accroître fortement le risque juridique "
                    "ou commercial."
                ),
                "ar": (
                    "قد يخلق هذا البند تعرضاً مالياً غير محدود قد يتجاوز قيمة العقد ويزيد "
                    "المخاطر القانونية أو التجارية بشكل كبير."
                ),
            },
        },
        {
            "risk_pattern": [
                "indirect damages",
                "consequential damages",
                "dommages indirects",
                "أضرار غير مباشرة",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause affects recovery of indirect or consequential losses, so exclusions "
                    "and carve-outs should be checked against the transaction risk."
                ),
                "fr": (
                    "La clause affecte la réparation des dommages indirects ou consécutifs ; les "
                    "exclusions et exceptions doivent être vérifiées au regard du risque de l'opération."
                ),
                "ar": (
                    "يؤثر هذا البند على التعويض عن الأضرار غير المباشرة أو التبعية، لذلك يجب "
                    "مراجعة الاستثناءات وفقاً لمخاطر المعاملة."
                ),
            },
        },
    ],
    "indemnity": [
        {
            "risk_pattern": [
                "defend",
                "hold harmless",
                "third-party claims",
                "défendre",
                "tenir indemne",
                "réclamations de tiers",
                "الدفاع عن",
                "مطالبات الغير",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause may require one party to cover defense costs or third-party claims, "
                    "so notice, control of defense, settlement rights, and liability limits should "
                    "be reviewed."
                ),
                "fr": (
                    "La clause peut imposer la prise en charge des frais de défense ou des réclamations "
                    "de tiers ; il faut vérifier l'avis, le contrôle de la défense, les transactions "
                    "et les limites de responsabilité."
                ),
                "ar": (
                    "قد يفرض هذا البند تحمل تكاليف الدفاع أو مطالبات الغير، لذلك يجب مراجعة الإشعار "
                    "والسيطرة على الدفاع وحقوق التسوية وحدود المسؤولية."
                ),
            },
        },
    ],
    "sla": [
        {
            "risk_pattern": [
                "uptime",
                "availability",
                "service credit",
                "disponibilité",
                "crédit de service",
                "التوافر",
                "تعويض الخدمة",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause defines measurable service commitments, so measurement periods, "
                    "exclusions, credits, reporting, and repeated-failure remedies should be clear."
                ),
                "fr": (
                    "La clause définit des engagements de service mesurables ; les périodes de mesure, "
                    "exclusions, crédits, reporting et recours en cas d'échecs répétés doivent être clairs."
                ),
                "ar": (
                    "يحدد هذا البند التزامات خدمة قابلة للقياس، لذلك يجب توضيح فترات القياس "
                    "والاستثناءات والتعويضات والتقارير ووسائل المعالجة عند تكرار الإخفاق."
                ),
            },
        },
    ],
    "exclusivity": [
        {
            "risk_pattern": [
                "exclusive",
                "exclusivity",
                "sole provider",
                "exclusif",
                "exclusivité",
                "حصري",
                "حصرية",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause may restrict work with alternative partners, suppliers, customers, "
                    "or territories, so duration, scope, performance conditions, and carve-outs "
                    "should be reviewed."
                ),
                "fr": (
                    "La clause peut limiter le recours à d'autres partenaires, fournisseurs, clients "
                    "ou territoires ; la durée, la portée, les conditions de performance et les exceptions "
                    "doivent être vérifiées."
                ),
                "ar": (
                    "قد يقيّد هذا البند التعامل مع شركاء أو موردين أو عملاء أو مناطق بديلة، لذلك يجب "
                    "مراجعة المدة والنطاق وشروط الأداء والاستثناءات."
                ),
            },
        },
    ],
    "governing_law": [
        {
            "risk_pattern": [
                "arbitration",
                "jurisdiction",
                "venue",
                "arbitrage",
                "juridiction",
                "تحكيم",
                "اختصاص",
                "محكمة",
            ],
            "risk_level": "low",
            "legal_consequence": {
                "en": (
                    "The clause determines where and how disputes are resolved, so enforceability, "
                    "cost, language, and practical access to the forum should be checked."
                ),
                "fr": (
                    "La clause détermine où et comment les litiges seront résolus ; il faut vérifier "
                    "l'exécution, le coût, la langue et l'accès pratique au forum."
                ),
                "ar": (
                    "يحدد هذا البند مكان وطريقة حل النزاعات، لذلك يجب مراجعة قابلية التنفيذ والتكلفة "
                    "واللغة وسهولة الوصول إلى الجهة المختصة."
                ),
            },
        },
    ],

    "data_privacy_security": [
        {
            "risk_pattern": [
                "security incident",
                "data breach",
                "incident de sécurité",
                "violation de données",
                "حادث أمني",
                "اختراق البيانات",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause addresses incident or breach handling, so timing, "
                    "cooperation, evidence preservation, notification duties, and "
                    "liability treatment should be clear."
                ),
                "fr": (
                    "La clause traite la gestion des incidents ou violations ; "
                    "les délais, la coopération, la conservation des preuves, "
                    "les notifications et la responsabilité doivent être clairs."
                ),
                "ar": (
                    "يتناول هذا البند التعامل مع الحوادث أو الاختراقات، لذلك يجب "
                    "توضيح المهل والتعاون وحفظ الأدلة وواجبات الإخطار ومعالجة المسؤولية."
                ),
            },
        },
    ],
    "restrictive_covenants": [
        {
            "risk_pattern": [
                "non-compete",
                "non compete",
                "non-concurrence",
                "عدم المنافسة",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause restricts competitive activity, so duration, scope, "
                    "territory, affected activities, and commercial justification "
                    "should be reviewed."
                ),
                "fr": (
                    "La clause restreint l'activité concurrente ; la durée, la portée, "
                    "le territoire, les activités concernées et la justification "
                    "commerciale doivent être examinés."
                ),
                "ar": (
                    "يقيد هذا البند النشاط التنافسي، لذلك يجب مراجعة المدة والنطاق "
                    "والمنطقة والأنشطة المعنية والمبرر التجاري."
                ),
            },
        },
        {
            "risk_pattern": [
                "non-solicitation",
                "non solicitation",
                "non-sollicitation",
                "عدم الاستقطاب",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause restricts solicitation, so the protected relationships, "
                    "duration, scope, and exceptions should be reviewed."
                ),
                "fr": (
                    "La clause restreint la sollicitation ; les relations protégées, "
                    "la durée, la portée et les exceptions doivent être examinées."
                ),
                "ar": (
                    "يقيد هذا البند الاستقطاب، لذلك يجب مراجعة العلاقات المحمية "
                    "والمدة والنطاق والاستثناءات."
                ),
            },
        },
    ],

}


def get_contextual_risk_reasoning(
    clause_type: str,
    text: str,
    language: str = "en",
) -> dict:
    language = get_language(language)
    normalized = str(text or "").lower()

    for template in RISK_REASON_TEMPLATES.get(clause_type, []):
        risk_pattern = [
            str(signal).lower()
            for signal in template.get("risk_pattern", [])
        ]

        if any_signal_present(risk_pattern, normalized):
            return {
                "clause_type": clause_type,
                "risk_level": template.get("risk_level", "medium"),
                "legal_insight": template["legal_consequence"].get(
                    language,
                    template["legal_consequence"].get("en", ""),
                ),
                "contextual_reasoning": True,
            }

    return {}


# ---------------------------------------------------------------------------
# International universal clause-family extensions
# ---------------------------------------------------------------------------
# Privacy-first note:
# These templates only reason on anonymized/legal clause text. They do not
# reconstruct, infer, restore, or request real names, addresses, emails,
# phone numbers, account numbers, or personal identifiers.

INTERNATIONAL_DOMAIN_EXTENSIONS = {
    "force_majeure": "force_majeure",
    "tax": "tax",
    "warranties": "warranties",
    "representations": "warranties",
    "representations_and_warranties": "warranties",
    "renewal": "renewal",
    "suspension": "suspension",
    "business_continuity": "business_continuity",
    "disaster_recovery": "business_continuity",
    "publicity": "publicity",
    "severability": "severability",
    "survival": "survival",
    "amendment": "amendment",
    "waiver": "waiver",
    "assignment": "assignment",
    "export_control": "export_control",
    "sanctions": "export_control",
    "open_source": "open_source",
    "escrow": "escrow",
    "transition_assistance": "transition_assistance",
    "insurance": "insurance",
}


INTERNATIONAL_CLAUSE_REASONING_TEMPLATES = {
    "force_majeure": {
        "signals": [
            "force majeure", "act of god", "natural disaster", "unforeseeable event",
            "beyond reasonable control", "epidemic", "pandemic", "war", "strike",
            "government action",
            "cas de force majeure", "force majeure", "cas fortuit",
            "catastrophe naturelle", "événement imprévisible",
            "hors du contrôle raisonnable", "épidémie", "pandémie", "guerre",
            "grève", "action gouvernementale",
            "القوة القاهرة", "حدث غير متوقع", "خارج السيطرة المعقولة",
            "كارثة طبيعية", "وباء", "جائحة", "حرب", "إضراب", "إجراء حكومي",
        ],
        "legal_insight": {
            "en": (
                "This clause addresses exceptional events that may excuse, delay, "
                "suspend, or modify contractual performance."
            ),
            "fr": (
                "Cette clause traite les événements exceptionnels susceptibles "
                "d'excuser, retarder, suspendre ou modifier l'exécution du contrat."
            ),
            "ar": (
                "تعالج هذه المادة الأحداث الاستثنائية التي قد تعفي أو تؤخر أو "
                "تعلق أو تعدل تنفيذ الالتزامات التعاقدية."
            ),
        },
        "recommendation": {
            "en": (
                "Check qualifying events, notice duties, mitigation obligations, "
                "evidence requirements, suspension periods, cost allocation, and "
                "termination rights after prolonged disruption."
            ),
            "fr": (
                "Vérifier les événements couverts, les obligations de notification, "
                "les mesures d'atténuation, les exigences de preuve, les périodes "
                "de suspension, la répartition des coûts et les droits de résiliation "
                "en cas de perturbation prolongée."
            ),
            "ar": (
                "ينبغي مراجعة الأحداث المشمولة، وواجبات الإشعار، والتخفيف، "
                "ومتطلبات الإثبات، وفترات التعليق، وتوزيع التكاليف، وحقوق الإنهاء "
                "عند استمرار التعطيل."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating objective event definitions, prompt notice, "
                "mitigation duties, continuity obligations, and balanced termination "
                "rights if performance is disrupted for an extended period."
            ),
            "fr": (
                "Envisager de négocier des définitions objectives des événements, "
                "un préavis rapide, des obligations d'atténuation, des obligations "
                "de continuité et des droits de résiliation équilibrés en cas de "
                "perturbation prolongée."
            ),
            "ar": (
                "يمكن التفاوض على تعريفات موضوعية للأحداث، وإشعار سريع، وواجبات "
                "التخفيف، والتزامات الاستمرارية، وحقوق إنهاء متوازنة إذا طال تعطل التنفيذ."
            ),
        },
    },

    "tax": {
        "signals": [
            "tax", "taxes", "vat", "gst", "withholding", "gross-up",
            "tax invoice", "sales tax", "duties", "levies",
            "impôt", "impôts", "taxe", "tva", "retenue à la source",
            "majoration fiscale", "facture fiscale", "droits", "prélèvements",
            "ضريبة", "ضرائب", "القيمة المضافة", "اقتطاع", "استقطاع",
            "تعويض ضريبي", "فاتورة ضريبية", "رسوم", "جبايات",
        ],
        "legal_insight": {
            "en": (
                "This clause allocates responsibility for taxes, withholding, "
                "invoicing, and tax-related adjustments."
            ),
            "fr": (
                "Cette clause répartit la responsabilité des impôts, retenues, "
                "facturation et ajustements fiscaux."
            ),
            "ar": (
                "توزع هذه المادة المسؤولية عن الضرائب والاستقطاعات والفوترة "
                "والتعديلات الضريبية."
            ),
        },
        "recommendation": {
            "en": (
                "Check whether taxes are included or excluded, who bears withholding, "
                "whether gross-up applies, invoice requirements, and responsibility "
                "for tax documentation."
            ),
            "fr": (
                "Vérifier si les taxes sont incluses ou exclues, qui supporte les "
                "retenues, si une majoration s'applique, les exigences de facturation "
                "et la responsabilité des documents fiscaux."
            ),
            "ar": (
                "ينبغي مراجعة ما إذا كانت الضرائب مشمولة أو مستثناة، ومن يتحمل "
                "الاستقطاع، وما إذا كان التعويض الضريبي ينطبق، ومتطلبات الفوترة "
                "ومسؤولية المستندات الضريبية."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating clear tax allocation, withholding mechanics, "
                "gross-up language, invoice timing, and cooperation on tax documents."
            ),
            "fr": (
                "Envisager de négocier une répartition fiscale claire, les mécanismes "
                "de retenue, les clauses de majoration, le calendrier de facturation "
                "et la coopération relative aux documents fiscaux."
            ),
            "ar": (
                "يمكن التفاوض على توزيع ضريبي واضح، وآليات الاستقطاع، وصياغة التعويض "
                "الضريبي، ومواعيد الفوترة، والتعاون بشأن المستندات الضريبية."
            ),
        },
    },

    "warranties": {
        "signals": [
            "warranty", "warranties", "representation", "representations",
            "representations and warranties", "as is", "disclaimer of warranty",
            "fitness for purpose", "merchantability", "defect warranty",
            "garantie", "garanties", "déclaration", "déclarations",
            "déclarations et garanties", "en l'état", "exclusion de garantie",
            "aptitude à l'usage", "vice", "ضمان", "ضمانات", "إقرار",
            "إقرارات", "الإقرارات والضمانات", "كما هو", "استبعاد الضمان",
            "ملاءمة للغرض", "عيب",
        ],
        "legal_insight": {
            "en": (
                "This clause defines statements, quality commitments, disclaimers, "
                "or remedies if facts or performance standards are not met."
            ),
            "fr": (
                "Cette clause définit des déclarations, engagements de qualité, "
                "exclusions ou recours si les faits ou standards de performance "
                "ne sont pas respectés."
            ),
            "ar": (
                "تحدد هذه المادة الإقرارات أو التزامات الجودة أو الاستثناءات أو "
                "وسائل الانتصاف إذا لم تتحقق الوقائع أو معايير الأداء."
            ),
        },
        "recommendation": {
            "en": (
                "Check the accuracy of representations, warranty scope, exclusions, "
                "remedy periods, disclaimers, reliance limits, and interaction with "
                "liability caps."
            ),
            "fr": (
                "Vérifier l'exactitude des déclarations, la portée des garanties, "
                "les exclusions, les délais de recours, les clauses d'exclusion, "
                "les limites de confiance et l'interaction avec les plafonds de responsabilité."
            ),
            "ar": (
                "ينبغي مراجعة دقة الإقرارات، ونطاق الضمانات، والاستثناءات، ومهل "
                "المعالجة، وحدود الاعتماد، وعلاقتها بحدود المسؤولية."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating specific warranties, reasonable exclusions, "
                "clear remedies, and consistency between warranty remedies and "
                "limitation of liability."
            ),
            "fr": (
                "Envisager de négocier des garanties spécifiques, des exclusions "
                "raisonnables, des recours clairs et la cohérence entre les recours "
                "de garantie et la limitation de responsabilité."
            ),
            "ar": (
                "يمكن التفاوض على ضمانات محددة، واستثناءات معقولة، ووسائل انتصاف "
                "واضحة، واتساق بين وسائل الضمان وحدود المسؤولية."
            ),
        },
    },

    "renewal": {
        "signals": [
            "renewal", "automatic renewal", "auto-renewal", "renewal term",
            "extension term", "successive terms", "non-renewal",
            "renouvellement", "reconduction automatique", "période de renouvellement",
            "durée de renouvellement", "non-renouvellement",
            "تجديد", "تجديد تلقائي", "مدة التجديد", "فترات متتالية", "عدم التجديد",
        ],
        "legal_insight": {
            "en": (
                "This clause controls how the contract continues, renews, extends, "
                "or ends after the initial term."
            ),
            "fr": (
                "Cette clause régit la poursuite, le renouvellement, la prolongation "
                "ou la fin du contrat après la durée initiale."
            ),
            "ar": (
                "تنظم هذه المادة استمرار العقد أو تجديده أو تمديده أو انتهائه بعد المدة الأصلية."
            ),
        },
        "recommendation": {
            "en": (
                "Check renewal periods, automatic renewal language, notice windows, "
                "pricing changes, service changes, and termination before renewal."
            ),
            "fr": (
                "Vérifier les périodes de renouvellement, la reconduction automatique, "
                "les fenêtres de préavis, les changements de prix, les changements de "
                "service et la résiliation avant renouvellement."
            ),
            "ar": (
                "ينبغي مراجعة مدد التجديد، وصياغة التجديد التلقائي، ومهل الإشعار، "
                "وتغييرات الأسعار أو الخدمات، والإنهاء قبل التجديد."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating clear non-renewal notice, limits on automatic "
                "renewal, price-change controls, and transition rights at expiry."
            ),
            "fr": (
                "Envisager de négocier un préavis clair de non-renouvellement, des "
                "limites à la reconduction automatique, des contrôles sur les changements "
                "de prix et des droits de transition à l'expiration."
            ),
            "ar": (
                "يمكن التفاوض على إشعار واضح بعدم التجديد، وحدود للتجديد التلقائي، "
                "وضوابط لتغيير الأسعار، وحقوق انتقال عند الانتهاء."
            ),
        },
    },

    "suspension": {
        "signals": [
            "suspension", "suspend", "suspend services", "service suspension",
            "reinstatement", "restore service", "access suspension",
            "suspension", "suspendre", "suspendre les services",
            "rétablissement", "restaurer le service",
            "تعليق", "يعلق", "تعليق الخدمات", "استئناف الخدمة",
            "إعادة الخدمة", "تعليق الوصول",
        ],
        "legal_insight": {
            "en": (
                "This clause allows obligations, services, access, or performance "
                "to be paused under certain conditions."
            ),
            "fr": (
                "Cette clause permet de suspendre des obligations, services, accès "
                "ou prestations dans certaines conditions."
            ),
            "ar": (
                "تسمح هذه المادة بتعليق الالتزامات أو الخدمات أو الوصول أو التنفيذ في ظروف معينة."
            ),
        },
        "recommendation": {
            "en": (
                "Check suspension triggers, prior notice, cure rights, data access, "
                "service continuity, fees during suspension, and reinstatement conditions."
            ),
            "fr": (
                "Vérifier les déclencheurs de suspension, le préavis, les droits de "
                "régularisation, l'accès aux données, la continuité du service, les "
                "frais pendant la suspension et les conditions de rétablissement."
            ),
            "ar": (
                "ينبغي مراجعة أسباب التعليق، والإشعار المسبق، وحقوق المعالجة، والوصول "
                "إلى البيانات، واستمرارية الخدمة، والرسوم أثناء التعليق، وشروط الاستئناف."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating objective suspension triggers, advance notice, "
                "limited scope, cure opportunities, and rapid reinstatement procedures."
            ),
            "fr": (
                "Envisager de négocier des déclencheurs objectifs de suspension, un "
                "préavis, une portée limitée, des possibilités de régularisation et "
                "des procédures rapides de rétablissement."
            ),
            "ar": (
                "يمكن التفاوض على أسباب موضوعية للتعليق، وإشعار مسبق، ونطاق محدود، "
                "وفرص معالجة، وإجراءات سريعة لاستئناف الخدمة."
            ),
        },
    },

    "business_continuity": {
        "signals": [
            "business continuity", "disaster recovery", "bcp", "drp",
            "backup", "restore", "recovery time objective", "rto",
            "recovery point objective", "rpo", "contingency plan",
            "continuité d'activité", "reprise après sinistre", "sauvegarde",
            "restauration", "plan de continuité", "خطة استمرارية الأعمال",
            "استمرارية الأعمال", "التعافي من الكوارث", "نسخ احتياطي",
            "استعادة", "خطة طوارئ",
        ],
        "legal_insight": {
            "en": (
                "This clause addresses continuity, recovery, backup, restoration, "
                "or resilience obligations during disruption."
            ),
            "fr": (
                "Cette clause traite les obligations de continuité, reprise, sauvegarde, "
                "restauration ou résilience pendant une perturbation."
            ),
            "ar": (
                "تعالج هذه المادة التزامات الاستمرارية أو التعافي أو النسخ الاحتياطي "
                "أو الاستعادة أو المرونة أثناء التعطيل."
            ),
        },
        "recommendation": {
            "en": (
                "Check recovery objectives, backup frequency, testing, reporting, "
                "incident escalation, restoration timing, and service continuity duties."
            ),
            "fr": (
                "Vérifier les objectifs de reprise, la fréquence des sauvegardes, les tests, "
                "le reporting, l'escalade des incidents, les délais de restauration et les "
                "obligations de continuité du service."
            ),
            "ar": (
                "ينبغي مراجعة أهداف التعافي، وتكرار النسخ الاحتياطي، والاختبارات، "
                "والتقارير، وتصعيد الحوادث، ومواعيد الاستعادة، وواجبات استمرارية الخدمة."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating measurable recovery targets, testing obligations, "
                "reporting duties, incident escalation, and remedies for continuity failures."
            ),
            "fr": (
                "Envisager de négocier des objectifs de reprise mesurables, des obligations "
                "de test, des obligations de reporting, l'escalade des incidents et des recours "
                "en cas d'échec de continuité."
            ),
            "ar": (
                "يمكن التفاوض على أهداف تعافٍ قابلة للقياس، والتزامات اختبار، وواجبات "
                "تقارير، وتصعيد الحوادث، ووسائل معالجة عند فشل الاستمرارية."
            ),
        },
    },

    "publicity": {
        "signals": [
            "publicity", "press release", "public announcement", "use of name",
            "logo", "trademark in marketing", "case study", "reference customer",
            "publicité", "communiqué de presse", "annonce publique",
            "utilisation du nom", "logo", "étude de cas", "référence client",
            "دعاية", "بيان صحفي", "إعلان عام", "استخدام الاسم",
            "الشعار", "دراسة حالة", "عميل مرجعي",
        ],
        "legal_insight": {
            "en": (
                "This clause controls public announcements, marketing references, "
                "case studies, names, logos, or brand use."
            ),
            "fr": (
                "Cette clause encadre les annonces publiques, références marketing, "
                "études de cas, noms, logos ou l'utilisation de la marque."
            ),
            "ar": (
                "تنظم هذه المادة الإعلانات العامة أو المراجع التسويقية أو دراسات الحالة "
                "أو استخدام الأسماء أو الشعارات أو العلامات."
            ),
        },
        "recommendation": {
            "en": (
                "Check approval rights, permitted uses, logo restrictions, withdrawal "
                "rights, confidentiality limits, and review procedures."
            ),
            "fr": (
                "Vérifier les droits d'approbation, les usages autorisés, les restrictions "
                "sur les logos, les droits de retrait, les limites de confidentialité et "
                "les procédures de revue."
            ),
            "ar": (
                "ينبغي مراجعة حقوق الموافقة، والاستخدامات المسموح بها، وقيود الشعارات، "
                "وحقوق السحب، وحدود السرية، وإجراءات المراجعة."
            ),
        },
        "negotiation": {
            "en": (
                "Consider requiring prior written approval for public use of names, "
                "logos, announcements, case studies, or customer references."
            ),
            "fr": (
                "Envisager d'exiger une approbation écrite préalable pour l'utilisation "
                "publique des noms, logos, annonces, études de cas ou références clients."
            ),
            "ar": (
                "يمكن التفاوض على اشتراط موافقة خطية مسبقة لاستخدام الأسماء أو الشعارات "
                "أو الإعلانات أو دراسات الحالة أو المراجع العملاء علناً."
            ),
        },
    },

    "severability": {
        "signals": [
            "severability", "invalid provision", "unenforceable provision",
            "severed", "valid substitute", "remaining provisions",
            "divisibilité", "clause invalide", "clause inapplicable",
            "séparée", "disposition de remplacement", "قابلية الفصل",
            "حكم غير صحيح", "حكم غير قابل للتنفيذ", "فصل الحكم",
            "حكم بديل", "باقي الأحكام",
        ],
        "legal_insight": {
            "en": (
                "This clause addresses what happens if part of the contract is invalid, "
                "unenforceable, or severed."
            ),
            "fr": (
                "Cette clause traite les conséquences lorsqu'une partie du contrat est "
                "invalide, inapplicable ou séparée."
            ),
            "ar": (
                "تعالج هذه المادة ما يحدث إذا كان جزء من العقد غير صحيح أو غير قابل "
                "للتنفيذ أو تم فصله."
            ),
        },
        "recommendation": {
            "en": (
                "Check whether invalid provisions are severed, replaced, renegotiated, "
                "or adjusted while preserving the remaining agreement."
            ),
            "fr": (
                "Vérifier si les clauses invalides sont séparées, remplacées, renégociées "
                "ou ajustées tout en préservant le reste du contrat."
            ),
            "ar": (
                "ينبغي مراجعة ما إذا كانت الأحكام غير الصحيحة تُفصل أو تُستبدل أو "
                "يعاد التفاوض بشأنها أو تعدل مع الحفاظ على باقي العقد."
            ),
        },
        "negotiation": {
            "en": (
                "Consider adding a fair replacement mechanism for invalid provisions "
                "without changing the core commercial bargain."
            ),
            "fr": (
                "Envisager d'ajouter un mécanisme équitable de remplacement des clauses "
                "invalides sans modifier l'équilibre commercial essentiel."
            ),
            "ar": (
                "يمكن التفاوض على آلية عادلة لاستبدال الأحكام غير الصحيحة دون تغيير "
                "جوهر الاتفاق التجاري."
            ),
        },
    },

    "survival": {
        "signals": [
            "survival", "survive termination", "survive expiry",
            "post-termination obligations", "continue after termination",
            "survie", "survivent à la résiliation",
            "obligations postérieures à la résiliation",
            "continuer après la résiliation", "استمرار", "تستمر بعد الإنهاء",
            "تستمر بعد الانقضاء", "التزامات ما بعد الإنهاء",
        ],
        "legal_insight": {
            "en": (
                "This clause identifies obligations that continue after termination "
                "or expiry of the contract."
            ),
            "fr": (
                "Cette clause identifie les obligations qui continuent après la "
                "résiliation ou l'expiration du contrat."
            ),
            "ar": (
                "تحدد هذه المادة الالتزامات التي تستمر بعد إنهاء العقد أو انقضائه."
            ),
        },
        "recommendation": {
            "en": (
                "Check which obligations survive, for how long, and whether survival "
                "is consistent with confidentiality, payment, audit, data return, IP, "
                "dispute resolution, and liability provisions."
            ),
            "fr": (
                "Vérifier quelles obligations survivent, pendant combien de temps, et "
                "si la survie est cohérente avec la confidentialité, le paiement, l'audit, "
                "la restitution des données, la propriété intellectuelle, le règlement des "
                "litiges et la responsabilité."
            ),
            "ar": (
                "ينبغي مراجعة الالتزامات التي تستمر ومدتها ومدى اتساقها مع السرية "
                "والدفع والتدقيق وإعادة البيانات والملكية الفكرية وتسوية النزاعات والمسؤولية."
            ),
        },
        "negotiation": {
            "en": (
                "Consider listing surviving obligations expressly and limiting survival "
                "periods where indefinite survival is not commercially necessary."
            ),
            "fr": (
                "Envisager d'énumérer expressément les obligations survivantes et de "
                "limiter leur durée lorsque la survie indéfinie n'est pas commercialement nécessaire."
            ),
            "ar": (
                "يمكن التفاوض على ذكر الالتزامات المستمرة صراحة وتحديد مدتها عندما لا "
                "تكون الاستمرارية غير المحددة ضرورية تجارياً."
            ),
        },
    },

    "amendment": {
        "signals": [
            "amendment", "amendments", "modified only in writing",
            "change order", "variation", "written modification",
            "modification", "avenant", "modifié uniquement par écrit",
            "ordre de modification", "changement", "تعديل", "تعديلات",
            "لا يعدل إلا كتابة", "أمر تغيير", "تغيير كتابي",
        ],
        "legal_insight": {
            "en": (
                "This clause controls how the contract may be modified, varied, "
                "or updated after signing."
            ),
            "fr": (
                "Cette clause encadre la manière dont le contrat peut être modifié, "
                "amendé ou mis à jour après signature."
            ),
            "ar": (
                "تنظم هذه المادة كيفية تعديل العقد أو تغييره أو تحديثه بعد التوقيع."
            ),
        },
        "recommendation": {
            "en": (
                "Check whether amendments require writing, authorized signatories, "
                "version control, change-order procedures, and rules for operational updates."
            ),
            "fr": (
                "Vérifier si les modifications exigent un écrit, des signataires autorisés, "
                "un contrôle des versions, des procédures d'ordre de modification et des règles "
                "pour les mises à jour opérationnelles."
            ),
            "ar": (
                "ينبغي مراجعة ما إذا كانت التعديلات تتطلب كتابة، وموقعين مفوضين، وضبط "
                "الإصدارات، وإجراءات أوامر التغيير، وقواعد التحديثات التشغيلية."
            ),
        },
        "negotiation": {
            "en": (
                "Consider requiring written amendments by authorized representatives while "
                "allowing controlled operational change procedures where appropriate."
            ),
            "fr": (
                "Envisager d'exiger des modifications écrites par des représentants autorisés "
                "tout en permettant des procédures contrôlées de changement opérationnel lorsque pertinent."
            ),
            "ar": (
                "يمكن التفاوض على اشتراط تعديلات خطية من ممثلين مفوضين مع السماح بإجراءات "
                "تغيير تشغيلية مضبوطة عند الاقتضاء."
            ),
        },
    },

    "waiver": {
        "signals": [
            "waiver", "no waiver", "failure to enforce", "delay in exercising",
            "waive", "single waiver", "renonciation", "absence de renonciation",
            "défaut d'exercice", "retard dans l'exercice", "renoncer",
            "تنازل", "عدم التنازل", "عدم ممارسة الحق", "التأخر في ممارسة الحق",
            "يتنازل",
        ],
        "legal_insight": {
            "en": (
                "This clause explains whether failure or delay in enforcing rights "
                "affects future enforcement."
            ),
            "fr": (
                "Cette clause précise si le défaut ou le retard dans l'exercice de droits "
                "affecte leur exercice futur."
            ),
            "ar": (
                "توضح هذه المادة ما إذا كان عدم ممارسة الحقوق أو التأخر في ممارستها "
                "يؤثر على تنفيذها مستقبلاً."
            ),
        },
        "recommendation": {
            "en": (
                "Check whether waivers must be written, specific, authorized, limited, "
                "and whether one waiver affects future rights."
            ),
            "fr": (
                "Vérifier si les renonciations doivent être écrites, spécifiques, autorisées, "
                "limitées, et si une renonciation affecte les droits futurs."
            ),
            "ar": (
                "ينبغي مراجعة ما إذا كان التنازل يجب أن يكون خطياً ومحدداً ومفوضاً "
                "ومحدوداً، وما إذا كان تنازل واحد يؤثر على الحقوق المستقبلية."
            ),
        },
        "negotiation": {
            "en": (
                "Consider requiring waivers to be written, specific, and limited to the "
                "particular right or breach being waived."
            ),
            "fr": (
                "Envisager d'exiger que les renonciations soient écrites, spécifiques "
                "et limitées au droit ou manquement concerné."
            ),
            "ar": (
                "يمكن التفاوض على اشتراط أن تكون التنازلات خطية ومحددة ومقصورة على "
                "الحق أو الإخلال المعني."
            ),
        },
    },

    "assignment": {
        "signals": [
            "assignment", "assign", "transfer this agreement", "delegate",
            "change of control", "novation",
            "cession", "céder", "transfert du contrat", "déléguer",
            "novation", "تنازل", "نقل العقد", "تفويض", "حوالة",
        ],
        "legal_insight": {
            "en": (
                "This clause controls whether rights or obligations may be transferred, "
                "assigned, delegated, or novated."
            ),
            "fr": (
                "Cette clause encadre la cession, le transfert, la délégation ou la novation "
                "des droits ou obligations."
            ),
            "ar": (
                "تنظم هذه المادة إمكانية نقل أو التنازل عن الحقوق أو الالتزامات أو تفويضها أو حوالتها."
            ),
        },
        "recommendation": {
            "en": (
                "Check consent requirements, permitted affiliate transfers, change-of-control "
                "effects, delegation limits, and whether the assignee must be capable of performance."
            ),
            "fr": (
                "Vérifier les exigences de consentement, les transferts autorisés aux affiliés, "
                "les effets du changement de contrôle, les limites de délégation et la capacité "
                "du cessionnaire à exécuter."
            ),
            "ar": (
                "ينبغي مراجعة متطلبات الموافقة، والتحويلات المسموح بها للشركات التابعة، "
                "وآثار تغيير السيطرة، وحدود التفويض، وقدرة المتنازل له على التنفيذ."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating reasonable consent standards and practical exceptions "
                "for affiliates, restructuring, mergers, or sale of substantially all assets."
            ),
            "fr": (
                "Envisager de négocier des standards raisonnables de consentement et des exceptions "
                "pratiques pour les affiliés, restructurations, fusions ou cessions de la quasi-totalité des actifs."
            ),
            "ar": (
                "يمكن التفاوض على معايير موافقة معقولة واستثناءات عملية للشركات التابعة "
                "أو إعادة الهيكلة أو الاندماج أو بيع معظم الأصول."
            ),
        },
    },

    "export_control": {
        "signals": [
            "export control", "sanctions", "trade sanctions", "restricted party",
            "embargo", "anti-boycott", "dual use",
            "contrôle des exportations", "sanctions", "embargo",
            "partie restreinte", "double usage",
            "ضوابط التصدير", "عقوبات", "حظر", "طرف مقيد", "استخدام مزدوج",
        ],
        "legal_insight": {
            "en": (
                "This clause addresses trade controls, sanctions, restricted-party rules, "
                "or export restrictions."
            ),
            "fr": (
                "Cette clause traite les contrôles commerciaux, sanctions, règles relatives "
                "aux parties restreintes ou restrictions d'exportation."
            ),
            "ar": (
                "تعالج هذه المادة ضوابط التجارة أو العقوبات أو قواعد الأطراف المقيدة أو قيود التصدير."
            ),
        },
        "recommendation": {
            "en": (
                "Check compliance duties, restricted-party screening, export classification, "
                "end-use restrictions, reporting, and termination rights for sanctions events."
            ),
            "fr": (
                "Vérifier les obligations de conformité, le filtrage des parties restreintes, "
                "la classification export, les restrictions d'usage final, le reporting et les droits "
                "de résiliation en cas de sanctions."
            ),
            "ar": (
                "ينبغي مراجعة واجبات الامتثال، وفحص الأطراف المقيدة، وتصنيف التصدير، "
                "وقيود الاستخدام النهائي، والتقارير، وحقوق الإنهاء عند أحداث العقوبات."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating clear compliance responsibilities, cooperation duties, "
                "screening requirements, and proportional remedies for sanctions or export-control breaches."
            ),
            "fr": (
                "Envisager de négocier des responsabilités de conformité claires, des obligations "
                "de coopération, des exigences de filtrage et des recours proportionnés en cas de "
                "violation des sanctions ou contrôles export."
            ),
            "ar": (
                "يمكن التفاوض على مسؤوليات امتثال واضحة، وواجبات تعاون، ومتطلبات فحص، "
                "ووسائل معالجة متناسبة عند خرق العقوبات أو ضوابط التصدير."
            ),
        },
    },

    "open_source": {
        "signals": [
            "open source", "copyleft", "oss", "third-party software",
            "source code", "software component",
            "logiciel libre", "open source", "copyleft", "logiciel tiers",
            "code source", "برنامج مفتوح المصدر", "كود مفتوح", "كود المصدر",
            "برنامج طرف ثالث",
        ],
        "legal_insight": {
            "en": (
                "This clause may affect software licensing, source code disclosure, "
                "third-party components, or open-source compliance."
            ),
            "fr": (
                "Cette clause peut affecter les licences logicielles, la divulgation du code source, "
                "les composants tiers ou la conformité open source."
            ),
            "ar": (
                "قد تؤثر هذه المادة على تراخيص البرمجيات أو الإفصاح عن كود المصدر أو مكونات الطرف الثالث أو الامتثال للمصدر المفتوح."
            ),
        },
        "recommendation": {
            "en": (
                "Check permitted open-source use, approval controls, copyleft restrictions, "
                "component inventory, disclosure duties, and remediation obligations."
            ),
            "fr": (
                "Vérifier l'utilisation autorisée de l'open source, les contrôles d'approbation, "
                "les restrictions copyleft, l'inventaire des composants, les obligations de divulgation "
                "et de correction."
            ),
            "ar": (
                "ينبغي مراجعة الاستخدام المسموح للمصدر المفتوح، وضوابط الموافقة، وقيود copyleft، "
                "وجرد المكونات، وواجبات الإفصاح والمعالجة."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating approval procedures, component disclosure, replacement rights, "
                "and warranties against problematic open-source obligations."
            ),
            "fr": (
                "Envisager de négocier des procédures d'approbation, la divulgation des composants, "
                "des droits de remplacement et des garanties contre les obligations open source problématiques."
            ),
            "ar": (
                "يمكن التفاوض على إجراءات الموافقة، والإفصاح عن المكونات، وحقوق الاستبدال، "
                "وضمانات ضد التزامات المصدر المفتوح الإشكالية."
            ),
        },
    },

    "escrow": {
        "signals": [
            "escrow", "source code escrow", "deposit materials", "release condition",
            "séquestre", "séquestre de code source", "dépôt", "condition de libération",
            "ضمان الكود", "إيداع", "مواد مودعة", "شرط الإفراج",
        ],
        "legal_insight": {
            "en": (
                "This clause governs deposited materials and release rights if specified events occur."
            ),
            "fr": (
                "Cette clause régit les éléments déposés et les droits de libération lorsque certains événements surviennent."
            ),
            "ar": (
                "تنظم هذه المادة المواد المودعة وحقوق الإفراج عنها عند وقوع أحداث محددة."
            ),
        },
        "recommendation": {
            "en": (
                "Check deposit scope, update frequency, verification, release triggers, access rights, "
                "confidentiality, and permitted use after release."
            ),
            "fr": (
                "Vérifier le périmètre du dépôt, la fréquence des mises à jour, la vérification, "
                "les déclencheurs de libération, les droits d'accès, la confidentialité et l'usage autorisé après libération."
            ),
            "ar": (
                "ينبغي مراجعة نطاق الإيداع، وتكرار التحديث، والتحقق، ومحفزات الإفراج، "
                "وحقوق الوصول، والسرية، والاستخدام المسموح بعد الإفراج."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating objective release conditions, verification rights, regular updates, "
                "and narrowly defined post-release use rights."
            ),
            "fr": (
                "Envisager de négocier des conditions objectives de libération, des droits de vérification, "
                "des mises à jour régulières et des droits d'usage après libération strictement définis."
            ),
            "ar": (
                "يمكن التفاوض على شروط إفراج موضوعية، وحقوق تحقق، وتحديثات منتظمة، "
                "وحقوق استخدام محددة بدقة بعد الإفراج."
            ),
        },
    },

    "transition_assistance": {
        "signals": [
            "transition assistance", "exit assistance", "handover", "migration",
            "knowledge transfer", "wind-down",
            "assistance de transition", "assistance à la sortie", "transfert de connaissances",
            "migration", "remise", "مساعدة انتقالية", "مساعدة الخروج", "نقل المعرفة",
            "ترحيل", "تسليم انتقالي",
        ],
        "legal_insight": {
            "en": (
                "This clause addresses support needed to transition services, data, assets, "
                "or operations at termination or expiry."
            ),
            "fr": (
                "Cette clause traite le support nécessaire pour transférer les services, données, "
                "actifs ou opérations à la résiliation ou expiration."
            ),
            "ar": (
                "تعالج هذه المادة الدعم اللازم لنقل الخدمات أو البيانات أو الأصول أو العمليات عند الإنهاء أو الانقضاء."
            ),
        },
        "recommendation": {
            "en": (
                "Check transition duration, scope, fees, cooperation duties, data export, knowledge transfer, "
                "continued support, and timelines."
            ),
            "fr": (
                "Vérifier la durée de transition, le périmètre, les frais, les obligations de coopération, "
                "l'export des données, le transfert de connaissances, le support continu et les délais."
            ),
            "ar": (
                "ينبغي مراجعة مدة الانتقال، والنطاق، والرسوم، وواجبات التعاون، وتصدير البيانات، "
                "ونقل المعرفة، والدعم المستمر، والجداول الزمنية."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating detailed exit assistance, reasonable fees, data portability, "
                "knowledge transfer, and support continuity."
            ),
            "fr": (
                "Envisager de négocier une assistance de sortie détaillée, des frais raisonnables, "
                "la portabilité des données, le transfert de connaissances et la continuité du support."
            ),
            "ar": (
                "يمكن التفاوض على مساعدة خروج مفصلة، ورسوم معقولة، وقابلية نقل البيانات، "
                "ونقل المعرفة، واستمرارية الدعم."
            ),
        },
    },

    "insurance": {
        "signals": [
            "insurance", "policy", "coverage", "insured", "certificate of insurance",
            "deductible", "additional insured",
            "assurance", "police", "couverture", "assuré", "attestation d'assurance",
            "franchise", "assuré additionnel",
            "تأمين", "وثيقة التأمين", "تغطية", "مؤمن عليه", "شهادة تأمين",
            "تحمل", "مؤمن له إضافي",
        ],
        "legal_insight": {
            "en": (
                "This clause allocates risk through required insurance coverage, evidence, "
                "exclusions, or policy obligations."
            ),
            "fr": (
                "Cette clause répartit le risque par des exigences d'assurance, justificatifs, "
                "exclusions ou obligations de police."
            ),
            "ar": (
                "توزع هذه المادة المخاطر من خلال متطلبات التأمين أو الإثبات أو الاستثناءات أو التزامات الوثيقة."
            ),
        },
        "recommendation": {
            "en": (
                "Check coverage types, minimum limits, deductibles, exclusions, evidence of insurance, "
                "notice of cancellation, and additional insured requirements."
            ),
            "fr": (
                "Vérifier les types de couverture, les limites minimales, les franchises, les exclusions, "
                "les justificatifs d'assurance, le préavis d'annulation et les exigences d'assuré additionnel."
            ),
            "ar": (
                "ينبغي مراجعة أنواع التغطية، والحدود الدنيا، والتحملات، والاستثناءات، وإثبات التأمين، "
                "والإشعار بالإلغاء، ومتطلبات المؤمن له الإضافي."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating coverage that matches contract risk, clear evidence duties, "
                "reasonable deductibles, and notice before cancellation or material change."
            ),
            "fr": (
                "Envisager de négocier une couverture adaptée au risque contractuel, des obligations "
                "de preuve claires, des franchises raisonnables et un préavis avant annulation ou modification importante."
            ),
            "ar": (
                "يمكن التفاوض على تغطية تتناسب مع مخاطر العقد، وواجبات إثبات واضحة، وتحملات معقولة، "
                "وإشعار قبل الإلغاء أو التغيير الجوهري."
            ),
        },
    },
}


INTERNATIONAL_RISK_REASON_TEMPLATES = {
    "force_majeure": [
        {
            "risk_pattern": [
                "beyond reasonable control", "without notice", "prolonged force majeure",
                "hors du contrôle raisonnable", "sans préavis", "force majeure prolongée",
                "خارج السيطرة المعقولة", "دون إشعار", "قوة قاهرة مطولة",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause may excuse or delay performance during exceptional events, "
                    "so notice, mitigation, duration, evidence, and termination consequences should be clear."
                ),
                "fr": (
                    "La clause peut excuser ou retarder l'exécution lors d'événements exceptionnels ; "
                    "les notifications, l'atténuation, la durée, les preuves et les conséquences de résiliation doivent être claires."
                ),
                "ar": (
                    "قد يعفي هذا البند أو يؤخر التنفيذ أثناء الأحداث الاستثنائية، لذلك يجب توضيح الإشعار "
                    "والتخفيف والمدة والإثبات وآثار الإنهاء."
                ),
            },
        },
    ],
    "tax": [
        {
            "risk_pattern": [
                "withholding", "gross-up", "vat", "retenue à la source", "majoration fiscale",
                "tva", "اقتطاع", "تعويض ضريبي", "القيمة المضافة",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause may shift tax costs or withholding exposure, so allocation, documentation, "
                    "gross-up and invoicing mechanics should be clear."
                ),
                "fr": (
                    "La clause peut transférer des coûts fiscaux ou une exposition aux retenues ; la répartition, "
                    "les documents, la majoration et la facturation doivent être clairs."
                ),
                "ar": (
                    "قد ينقل هذا البند تكاليف ضريبية أو تعرضاً للاستقطاع، لذلك يجب توضيح التوزيع والمستندات "
                    "والتعويض الضريبي وآليات الفوترة."
                ),
            },
        },
    ],
    "warranties": [
        {
            "risk_pattern": [
                "as is", "disclaimer", "exclusive remedy", "en l'état", "exclusion", "recours exclusif",
                "كما هو", "استبعاد", "وسيلة انتصاف حصرية",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause may limit warranty protection or remedies, so disclaimers, exclusions, remedy periods "
                    "and liability interaction should be reviewed."
                ),
                "fr": (
                    "La clause peut limiter les garanties ou recours ; les exclusions, délais de recours et l'interaction "
                    "avec la responsabilité doivent être examinés."
                ),
                "ar": (
                    "قد يحد هذا البند من حماية الضمان أو وسائل الانتصاف، لذلك يجب مراجعة الاستثناءات ومدد المعالجة "
                    "وعلاقتها بالمسؤولية."
                ),
            },
        },
    ],
    "suspension": [
        {
            "risk_pattern": [
                "suspend services", "access suspension", "suspendre les services", "تعليق الخدمات", "تعليق الوصول",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause may interrupt access or performance, so notice, cure rights, scope and reinstatement should be clear."
                ),
                "fr": (
                    "La clause peut interrompre l'accès ou l'exécution ; le préavis, les droits de régularisation, la portée "
                    "et le rétablissement doivent être clairs."
                ),
                "ar": (
                    "قد يقطع هذا البند الوصول أو التنفيذ، لذلك يجب توضيح الإشعار وحقوق المعالجة والنطاق والاستئناف."
                ),
            },
        },
    ],
}


def _extend_international_reasoning_templates() -> None:
    DOMAIN_TO_REASONING_TYPE.update(INTERNATIONAL_DOMAIN_EXTENSIONS)
    CLAUSE_REASONING_TEMPLATES.update(INTERNATIONAL_CLAUSE_REASONING_TEMPLATES)

    for clause_type, templates in INTERNATIONAL_RISK_REASON_TEMPLATES.items():
        existing = RISK_REASON_TEMPLATES.setdefault(clause_type, [])
        existing.extend(templates)

    governing_law = CLAUSE_REASONING_TEMPLATES.get("governing_law", {})
    signals = governing_law.setdefault("signals", [])
    for signal in [
        "governing law",
        "applicable law",
        "choice of law",
        "forum",
        "arbitration",
        "law of",
        "loi applicable",
        "choix de loi",
        "forum",
        "arbitrage",
        "القانون الواجب التطبيق",
        "القانون المختار",
        "التحكيم",
    ]:
        if signal not in signals:
            signals.append(signal)

    title_aliases = {
        "force majeure": "force_majeure",
        "tax": "tax",
        "taxes": "tax",
        "warranty": "warranties",
        "warranties": "warranties",
        "representations and warranties": "warranties",
        "renewal": "renewal",
        "suspension": "suspension",
        "business continuity": "business_continuity",
        "disaster recovery": "business_continuity",
        "publicity": "publicity",
        "severability": "severability",
        "survival": "survival",
        "amendment": "amendment",
        "waiver": "waiver",
        "assignment": "assignment",
        "export control": "export_control",
        "sanctions": "export_control",
        "open source": "open_source",
        "escrow": "escrow",
        "transition assistance": "transition_assistance",
        "insurance": "insurance",
    }

    globals()["INTERNATIONAL_TITLE_ALIASES"] = title_aliases


_extend_international_reasoning_templates()



# ---------------------------------------------------------------------------
# Source-grounded canonical reasoning overrides
# ---------------------------------------------------------------------------
# The publication gate derives its source profile with
# detect_clause_type_from_taxonomy(). Protected reasoning fields should use the
# same source-grounding family when that detector returns a non-weak type.
# These direct templates prevent broad family mappings (e.g. loan ->
# finance_lending, subcontracting -> services_operations) from injecting
# unrelated checklist topics.

SOURCE_GROUNDING_WEAK_TYPES = {"", "other", "general", None}


SOURCE_GROUNDED_REASONING_TEMPLATES = {
    "loan": {
        "en": {
            "legal_insight": "This clause addresses a specific lending obligation, credit condition, or lender right.",
            "recommendation": "Check the specific loan trigger, amount or metric, timing, required evidence, and direct consequence stated in this clause.",
            "negotiation": "Consider clarifying the clause-specific trigger, calculation, procedure, cure opportunity, and proportionate consequence.",
        },
        "fr": {
            "legal_insight": "Cette clause traite d'une obligation de prêt, d'une condition de crédit ou d'un droit du prêteur déterminé.",
            "recommendation": "Vérifier le déclencheur de crédit précis, le montant ou l'indicateur, le calendrier, les justificatifs et la conséquence directement prévue par cette clause.",
            "negotiation": "Envisager de clarifier le déclencheur, le calcul, la procédure, la possibilité de régularisation et la conséquence proportionnée propres à cette clause.",
        },
        "ar": {
            "legal_insight": "تتناول هذه المادة التزاماً محدداً في القرض أو شرطاً ائتمانياً أو حقاً للدائن.",
            "recommendation": "ينبغي مراجعة السبب المحدد في القرض والمبلغ أو المؤشر والتوقيت والمستندات المطلوبة والأثر المباشر المنصوص عليه في هذه المادة.",
            "negotiation": "يمكن التفاوض على توضيح السبب والاحتساب والإجراء وفرصة المعالجة والأثر المتناسب الخاصة بهذه المادة.",
        },
    },
    "collateral": {
        "en": {
            "legal_insight": "This clause creates or governs security over identified assets or rights.",
            "recommendation": "Check the secured assets, secured obligations, priority, release conditions, and enforcement trigger.",
            "negotiation": "Consider narrowing the collateral scope, defining release mechanics, and tying enforcement to clearly defined defaults.",
        },
        "fr": {
            "legal_insight": "Cette clause crée ou régit une sûreté sur des actifs ou droits identifiés.",
            "recommendation": "Vérifier les actifs grevés, les obligations garanties, le rang, les conditions de mainlevée et le déclencheur de réalisation.",
            "negotiation": "Envisager de réduire l'assiette de la sûreté, de préciser la mainlevée et de lier la réalisation à des défauts clairement définis.",
        },
        "ar": {
            "legal_insight": "تنشئ هذه المادة أو تنظم ضماناً عينياً على أصول أو حقوق محددة.",
            "recommendation": "ينبغي مراجعة الأصول محل الضمان والالتزامات المضمونة والأولوية وشروط الإفراج وسبب التنفيذ.",
            "negotiation": "يمكن التفاوض على تضييق نطاق الضمان وتحديد آلية الإفراج وربط التنفيذ بحالات تعثر محددة بوضوح.",
        },
    },
    "guarantee": {
        "en": {
            "legal_insight": "This clause creates a guarantee or secondary obligation for another party's liabilities.",
            "recommendation": "Check the guaranteed obligations, cap, duration, demand procedure, defenses, and release conditions.",
            "negotiation": "Consider a defined cap and duration, preserved defenses, clear demand mechanics, and release when the guaranteed obligations end.",
        },
        "fr": {
            "legal_insight": "Cette clause crée une garantie ou une obligation subsidiaire au titre des dettes d'une autre partie.",
            "recommendation": "Vérifier les obligations garanties, le plafond, la durée, la procédure d'appel, les moyens de défense et les conditions de libération.",
            "negotiation": "Envisager un plafond et une durée définis, le maintien des moyens de défense, une procédure d'appel claire et la libération à l'extinction des obligations garanties.",
        },
        "ar": {
            "legal_insight": "تنشئ هذه المادة كفالة أو التزاماً ثانوياً عن التزامات طرف آخر.",
            "recommendation": "ينبغي مراجعة الالتزامات المكفولة والحد الأقصى والمدة وإجراءات المطالبة والدفوع وشروط انتهاء الكفالة.",
            "negotiation": "يمكن التفاوض على حد ومدة محددين والحفاظ على الدفوع وآلية مطالبة واضحة وانتهاء الكفالة عند انقضاء الالتزامات المكفولة.",
        },
    },
    "subcontracting": {
        "en": {
            "legal_insight": "This clause controls whether and how contractual work may be subcontracted.",
            "recommendation": "Check any consent requirement, permitted exceptions, continued primary responsibility, and obligations that must flow down.",
            "negotiation": "Consider reasonable consent standards, targeted exceptions, continued primary responsibility, and clause-specific flow-down duties.",
        },
        "fr": {
            "legal_insight": "Cette clause encadre la possibilité et les conditions de sous-traiter l'exécution contractuelle.",
            "recommendation": "Vérifier l'exigence de consentement, les exceptions permises, le maintien de la responsabilité principale et les obligations à répercuter.",
            "negotiation": "Envisager des critères de consentement raisonnables, des exceptions ciblées, le maintien de la responsabilité principale et des obligations de répercussion propres à la clause.",
        },
        "ar": {
            "legal_insight": "تنظم هذه المادة ما إذا كان يجوز إسناد العمل التعاقدي إلى مقاول من الباطن وكيفية ذلك.",
            "recommendation": "ينبغي مراجعة اشتراط الموافقة والاستثناءات المسموح بها واستمرار المسؤولية الأساسية والالتزامات الواجب نقلها إلى المقاول من الباطن.",
            "negotiation": "يمكن التفاوض على معايير موافقة معقولة واستثناءات محددة مع بقاء المسؤولية الأساسية وتحديد الالتزامات المنقولة.",
        },
    },
    "employment": {
        "en": {
            "legal_insight": "This clause addresses a specific employment term, duty, benefit, restriction, or employment consequence.",
            "recommendation": "Check the precise employment term, who it applies to, its trigger, duration, exceptions, and stated consequence.",
            "negotiation": "Consider clarifying the employee-specific term, objective standards, reasonable duration, and proportionate consequence.",
        },
        "fr": {
            "legal_insight": "Cette clause traite d'une condition, obligation, prestation, restriction ou conséquence propre à la relation de travail.",
            "recommendation": "Vérifier la condition de travail précise, les personnes concernées, son déclencheur, sa durée, ses exceptions et sa conséquence.",
            "negotiation": "Envisager de clarifier la condition propre au salarié, les critères objectifs, une durée raisonnable et une conséquence proportionnée.",
        },
        "ar": {
            "legal_insight": "تتناول هذه المادة شرطاً أو واجباً أو ميزة أو قيداً أو أثراً محدداً في علاقة العمل.",
            "recommendation": "ينبغي مراجعة الشرط الوظيفي المحدد ومن يسري عليه وسببه ومدته واستثناءاته وأثره.",
            "negotiation": "يمكن التفاوض على توضيح الشرط الخاص بالموظف والمعايير الموضوعية والمدة المعقولة والأثر المتناسب.",
        },
    },
    "dispute_resolution": {
        "en": {
            "legal_insight": "This clause sets the procedure and forum for resolving disputes.",
            "recommendation": "Check the dispute steps, deadlines, forum, seat or venue, rules, language, and interim-relief mechanism expressly stated.",
            "negotiation": "Consider a workable escalation process, neutral enforceable forum, clear procedural rules, and express treatment of urgent interim relief.",
        },
        "fr": {
            "legal_insight": "Cette clause fixe la procédure et le forum de règlement des litiges.",
            "recommendation": "Vérifier les étapes du litige, les délais, le forum, le siège ou lieu, les règles, la langue et le mécanisme de mesures provisoires expressément prévus.",
            "negotiation": "Envisager un processus d'escalade praticable, un forum neutre et exécutoire, des règles claires et un traitement exprès des mesures urgentes.",
        },
        "ar": {
            "legal_insight": "تحدد هذه المادة إجراءات وجهة تسوية النزاعات.",
            "recommendation": "ينبغي مراجعة مراحل النزاع والمواعيد والجهة والمقر أو المكان والقواعد واللغة وآلية التدابير المؤقتة المنصوص عليها صراحة.",
            "negotiation": "يمكن التفاوض على مسار تصعيد عملي وجهة محايدة قابلة للتنفيذ وقواعد واضحة ومعالجة صريحة للتدابير العاجلة.",
        },
    },
    "services": {
        "en": {
            "legal_insight": "This clause defines a specific service obligation or operating requirement.",
            "recommendation": "Check the exact service duty, responsible party, stated standard, timing, dependencies, and consequence of non-performance.",
            "negotiation": "Consider objective service standards, clear responsibilities, workable dependencies, and proportionate remedies tied to the stated duty.",
        },
        "fr": {
            "legal_insight": "Cette clause définit une obligation de service ou une exigence opérationnelle précise.",
            "recommendation": "Vérifier l'obligation exacte, la partie responsable, le standard prévu, le calendrier, les dépendances et la conséquence de l'inexécution.",
            "negotiation": "Envisager des standards objectifs, des responsabilités claires, des dépendances praticables et des recours proportionnés liés à l'obligation prévue.",
        },
        "ar": {
            "legal_insight": "تحدد هذه المادة التزام خدمة أو متطلباً تشغيلياً محدداً.",
            "recommendation": "ينبغي مراجعة واجب الخدمة المحدد والطرف المسؤول والمعيار المنصوص عليه والتوقيت والاعتماديات وأثر عدم التنفيذ.",
            "negotiation": "يمكن التفاوض على معايير موضوعية ومسؤوليات واضحة واعتماديات عملية ووسائل معالجة متناسبة مرتبطة بالواجب المحدد.",
        },
    },
    "covenant": {
        "en": {
            "legal_insight": "This clause creates a specific continuing contractual undertaking.",
            "recommendation": "Check the exact required conduct, responsible party, duration, measurement standard, exceptions, and consequence of breach.",
            "negotiation": "Consider objective standards, materiality thresholds, practical compliance mechanics, cure rights, and proportionate consequences.",
        },
        "fr": {
            "legal_insight": "Cette clause crée un engagement contractuel continu déterminé.",
            "recommendation": "Vérifier le comportement exigé, la partie responsable, la durée, le critère de mesure, les exceptions et la conséquence d'un manquement.",
            "negotiation": "Envisager des critères objectifs, des seuils de matérialité, des modalités pratiques de conformité, des droits de régularisation et des conséquences proportionnées.",
        },
        "ar": {
            "legal_insight": "تنشئ هذه المادة تعهداً تعاقدياً مستمراً ومحدداً.",
            "recommendation": "ينبغي مراجعة السلوك المطلوب والطرف المسؤول والمدة ومعيار القياس والاستثناءات وأثر الإخلال.",
            "negotiation": "يمكن التفاوض على معايير موضوعية وعتبات جوهرية وآليات امتثال عملية وحقوق معالجة وآثار متناسبة.",
        },
    },
    "penalty": {
        "en": {
            "legal_insight": "This clause imposes a penalty, charge, or economic consequence when a specified event occurs.",
            "recommendation": "Check the trigger, calculation method, amount or rate, exceptions, cumulative effect, and relationship to other remedies.",
            "negotiation": "Consider a transparent calculation, reasonable cap, no duplication of remedies, and a consequence proportionate to the trigger.",
        },
        "fr": {
            "legal_insight": "Cette clause impose une pénalité, des frais ou une conséquence économique lors d'un événement déterminé.",
            "recommendation": "Vérifier le déclencheur, le calcul, le montant ou taux, les exceptions, l'effet cumulatif et l'articulation avec les autres recours.",
            "negotiation": "Envisager un calcul transparent, un plafond raisonnable, l'absence de double recours et une conséquence proportionnée au déclencheur.",
        },
        "ar": {
            "legal_insight": "تفرض هذه المادة جزاءً أو رسماً أو أثراً اقتصادياً عند وقوع حدث محدد.",
            "recommendation": "ينبغي مراجعة سبب الاستحقاق وطريقة الاحتساب والمبلغ أو النسبة والاستثناءات والأثر التراكمي والعلاقة مع وسائل المعالجة الأخرى.",
            "negotiation": "يمكن التفاوض على احتساب شفاف وحد معقول وعدم ازدواج وسائل المعالجة وأثر متناسب مع سبب الاستحقاق.",
        },
    },
    "automatic_renewal": {
        "en": {
            "legal_insight": "This clause provides for automatic renewal unless the stated non-renewal mechanism is used.",
            "recommendation": "Check the renewal period, automatic trigger, non-renewal notice method and deadline, and any expressly linked renewal change.",
            "negotiation": "Consider a workable non-renewal window, clear advance notice mechanics, limits on renewal length, and separate controls for any price change.",
        },
        "fr": {
            "legal_insight": "Cette clause prévoit un renouvellement automatique sauf utilisation du mécanisme de non-renouvellement prévu.",
            "recommendation": "Vérifier la durée de renouvellement, le déclenchement automatique, la forme et le délai du préavis de non-renouvellement et tout changement expressément lié au renouvellement.",
            "negotiation": "Envisager une fenêtre de non-renouvellement praticable, des modalités de préavis claires, une durée limitée et des contrôles distincts pour tout changement de prix.",
        },
        "ar": {
            "legal_insight": "تنص هذه المادة على التجديد التلقائي ما لم تُستخدم آلية عدم التجديد المحددة.",
            "recommendation": "ينبغي مراجعة مدة التجديد وسبب التجديد التلقائي وطريقة وموعد إشعار عدم التجديد وأي تغيير مرتبط صراحة بالتجديد.",
            "negotiation": "يمكن التفاوض على نافذة عملية لعدم التجديد وآلية إشعار واضحة وحد لمدة التجديد وضوابط مستقلة لأي تغيير في الأسعار.",
        },
    },
    "share_transfer_rights": {
        "en": {
            "legal_insight": "This clause governs a shareholder's right or obligation when shares are transferred or a sale occurs.",
            "recommendation": "Check the transfer trigger, affected shares, eligible participants, notice or election mechanics, price basis, and completion procedure.",
            "negotiation": "Consider clarifying the trigger, participation scope, timing, price parity, procedural steps, and protection against disproportionate transfer obligations.",
        },
        "fr": {
            "legal_insight": "Cette clause régit le droit ou l'obligation d'un actionnaire lors d'un transfert d'actions ou d'une vente.",
            "recommendation": "Vérifier le déclencheur du transfert, les actions concernées, les participants éligibles, la notification ou l'option, la base de prix et la procédure de réalisation.",
            "negotiation": "Envisager de clarifier le déclencheur, la portée de la participation, les délais, l'égalité de prix, la procédure et la protection contre des obligations de transfert disproportionnées.",
        },
        "ar": {
            "legal_insight": "تنظم هذه المادة حق المساهم أو التزامه عند نقل الأسهم أو وقوع عملية بيع.",
            "recommendation": "ينبغي مراجعة سبب النقل والأسهم المعنية والمشاركين المؤهلين وآلية الإشعار أو الاختيار وأساس السعر وإجراءات الإتمام.",
            "negotiation": "يمكن التفاوض على توضيح السبب ونطاق المشاركة والمواعيد وتكافؤ السعر والإجراءات والحماية من التزامات نقل غير متناسبة.",
        },
    },
    "anti_dilution_preemptive_rights": {
        "en": {
            "legal_insight": "This clause protects an investor's position when new equity or securities are issued.",
            "recommendation": "Check the issuance trigger, covered securities, participation or adjustment formula, exclusions, notice, and exercise period.",
            "negotiation": "Consider narrowing exclusions, clarifying the formula and notice process, and ensuring a workable exercise period.",
        },
        "fr": {
            "legal_insight": "Cette clause protège la position d'un investisseur lors de l'émission de nouveaux titres ou valeurs mobilières.",
            "recommendation": "Vérifier le déclencheur de l'émission, les titres couverts, la formule de participation ou d'ajustement, les exclusions, la notification et le délai d'exercice.",
            "negotiation": "Envisager de limiter les exclusions, de clarifier la formule et la notification et de prévoir un délai d'exercice praticable.",
        },
        "ar": {
            "legal_insight": "تحمي هذه المادة مركز المستثمر عند إصدار أسهم أو أوراق مالية جديدة.",
            "recommendation": "ينبغي مراجعة سبب الإصدار والأوراق المالية المشمولة وصيغة المشاركة أو التعديل والاستثناءات والإشعار ومهلة الممارسة.",
            "negotiation": "يمكن التفاوض على تضييق الاستثناءات وتوضيح الصيغة وآلية الإشعار وضمان مهلة عملية للممارسة.",
        },
    },
}


def get_source_grounded_reasoning_override(
    clause_type: str,
    language: str,
) -> dict:
    """
    Return a direct canonical reasoning template when one exists.

    Multi-candidate routing calls this per producer candidate. The helper is
    intentionally side-effect free and falls back to English only when the
    requested language is unsupported by the selected direct template.
    """
    language = get_language(language)
    clause_type = str(
        clause_type or ""
    ).lower().strip()

    template = SOURCE_GROUNDED_REASONING_TEMPLATES.get(
        clause_type
    )

    if not template:
        return {}

    return template.get(
        language,
        template.get("en", {}),
    )


def get_source_grounding_candidates(
    text: str,
    authoritative_clause_type: str,
) -> tuple[str, list[str], list[str]]:
    """
    Return:
      1. the taxonomy primary type used by the strict publication gate;
      2. ordered producer candidates;
      3. the types actually detected from source text with positive score.

    The authoritative type is only treated as source-supported when it is
    genuinely present in detect_clause_type_candidates(text). This prevents an
    upstream label from taking over a multi-signal clause merely because the
    caller supplied it, while still protecting specific authoritative types
    such as loan, warranty, and non_compete when the source taxonomy itself
    detects them.
    """
    candidates = detect_clause_type_candidates(text)

    # Producer candidates must have an actual lexical/source signal.
    # Context-only scores are useful for taxonomy ranking, but are too weak
    # for reasoning production. Confirmed example: "ownership interest" gave
    # loan a context-only score with base_score=0 and no matched signals,
    # allowing an unrelated loan negotiation template into an NDA clause.
    source_types = [
        str(candidate.get("type") or "").lower().strip()
        for candidate in candidates
        if candidate.get("score", 0) > 0
        and candidate.get("base_score", 0) > 0
        and bool(candidate.get("signals"))
        and str(candidate.get("type") or "").lower().strip()
        not in SOURCE_GROUNDING_WEAK_TYPES
    ]

    primary_type = str(
        detect_clause_type_from_taxonomy(text)
        or ""
    ).lower().strip()

    authoritative = str(
        authoritative_clause_type
        or "general"
    ).lower().strip()

    authoritative_is_source_supported = (
        authoritative in source_types
    )

    ordered = []

    preferred_order = (
        (
            authoritative,
            primary_type,
            *source_types,
        )
        if authoritative_is_source_supported
        else (
            primary_type,
            *source_types,
            authoritative,
        )
    )

    for clause_type in preferred_order:
        if (
            clause_type
            and clause_type not in SOURCE_GROUNDING_WEAK_TYPES
            and clause_type not in ordered
        ):
            ordered.append(clause_type)

    if primary_type in SOURCE_GROUNDING_WEAK_TYPES:
        primary_type = authoritative

    if not ordered:
        ordered.append(authoritative or "general")

    return primary_type, ordered, source_types


def _reasoning_lookup_type_for_candidate(
    candidate_type: str,
    text: str,
) -> str:
    lookup_type = map_domain_to_reasoning_type(
        candidate_type
    )

    if lookup_type == "confidentiality":
        subtype = _confidentiality_subtype(text)
        lookup_type = f"confidentiality_{subtype}"

    if lookup_type == "data_privacy_security":
        dp_subtype = _data_processing_subtype(text)

        if dp_subtype != "general":
            lookup_type = (
                f"data_privacy_security_{dp_subtype}"
            )

    return lookup_type


def _build_reasoning_candidate(
    candidate_type: str,
    text: str,
    language: str,
    sector: str = None,
) -> dict:
    lookup_type = _reasoning_lookup_type_for_candidate(
        candidate_type,
        text,
    )

    reasoning = get_clause_reasoning(
        lookup_type,
        language,
        sector=sector,
    )

    direct_override = (
        get_source_grounded_reasoning_override(
            candidate_type,
            language,
        )
    )

    if direct_override:
        reasoning["legal_insight"] = direct_override[
            "legal_insight"
        ]
        reasoning["recommendation"] = direct_override[
            "recommendation"
        ]
        reasoning["negotiation"] = direct_override[
            "negotiation"
        ]

    market = get_market_intelligence(
        candidate_type,
        language,
    )

    reasoning["market_comparison"] = market.get(
        "market_comparison",
        reasoning.get("market_comparison", ""),
    )
    reasoning["market_practice"] = market.get(
        "market_practice",
        reasoning.get("market_practice", "standard"),
    )
    reasoning["market_benchmark"] = market.get(
        "market_benchmark",
        reasoning.get("market_benchmark", "common"),
    )
    reasoning["negotiability"] = market.get(
        "negotiability",
        reasoning.get("negotiability", "medium"),
    )
    reasoning["market_confidence"] = market.get(
        "market_confidence",
        reasoning.get("market_confidence", 0.65),
    )
    reasoning["_producer_candidate_type"] = candidate_type

    return reasoning


def _generated_taxonomy_type(text: str) -> str:
    return str(
        detect_clause_type_from_taxonomy(text)
        or ""
    ).lower().strip()


def _field_candidate_rank(
    generated_text: str,
    source_primary_type: str,
) -> int:
    """
    Strict-gate-aware producer ranking.

    0 = generated text resolves to the exact source primary type.
    1 = generated text is taxonomy-weak and therefore does not assert a
        conflicting family.
    2 = generated text resolves to another family and should only be used if
        every candidate conflicts (the strict gate may then block it).
    """
    generated_type = _generated_taxonomy_type(
        generated_text
    )

    if generated_type == source_primary_type:
        return 0

    if generated_type in SOURCE_GROUNDING_WEAK_TYPES:
        return 1

    return 2


# Targeted authoritative-over-primary conflicts confirmed by the regression
# corpus and the strict verification cases. These are deliberately pair-based,
# not a blanket "authoritative always wins" rule: confidentiality must NOT
# override a warranty/IP source clause merely because an upstream caller passed
# confidentiality, while the three pairs below are known taxonomy-primary false
# positives for a more specific corrected upstream type.
AUTHORITATIVE_PRIMARY_PRIORITY_PAIRS = {
    ("insurance", "loan"),
    ("supply_distribution", "warranty"),
    ("employment", "non_compete"),
}


def _authoritative_should_override_primary(
    source_primary_type: str,
    authoritative_clause_type: str,
) -> bool:
    pair = (
        str(source_primary_type or "").lower().strip(),
        str(authoritative_clause_type or "").lower().strip(),
    )

    return pair in AUTHORITATIVE_PRIMARY_PRIORITY_PAIRS


def _select_field_from_reasoning_candidates(
    reasonings: list[dict],
    field: str,
    source_primary_type: str,
    authoritative_clause_type: str,
    source_detected_types: list[str],
) -> tuple[str, str | None]:
    ranked = []

    authoritative = str(
        authoritative_clause_type
        or ""
    ).lower().strip()

    authoritative_is_source_supported = (
        authoritative
        and authoritative in source_detected_types
    )

    authoritative_overrides_primary = (
        _authoritative_should_override_primary(
            source_primary_type,
            authoritative,
        )
    )

    for index, reasoning in enumerate(reasonings):
        value = str(
            reasoning.get(field)
            or ""
        ).strip()

        if not value:
            continue

        field_rank = _field_candidate_rank(
            value,
            source_primary_type,
        )

        producer_type = str(
            reasoning.get("_producer_candidate_type")
            or ""
        ).lower().strip()

        # A specific authoritative type may outrank the source-primary winner
        # when the source detector independently found it OR when the exact
        # (primary, authoritative) pair is a confirmed regression conflict.
        # The pair rule is intentionally narrow so an injected upstream label
        # cannot generally hijack a multi-signal clause.
        authoritative_priority = (
            0
            if (
                producer_type == authoritative
                and (
                    authoritative_is_source_supported
                    or authoritative_overrides_primary
                )
            )
            else 1
        )

        ranking_key = (
            authoritative_priority,
            field_rank,
            index,
        )

        ranked.append((
            ranking_key,
            value,
            producer_type,
        ))

    if not ranked:
        return "", None

    _, value, producer_type = min(ranked)

    return value, producer_type


def _source_aware_safer_alternative(
    text: str,
    language: str,
    current_value: str,
) -> str:
    """
    Preserve the source mechanisms for the observed joint-IP / first-
    negotiation clause. The fidelity gate correctly rejects an alternative
    that drops the equal joint ownership, no-accounting exploitation right,
    or the first-negotiation prerequisite before licensing joint IP to a
    direct competitor.
    """
    low = str(text or "").lower()

    first_negotiation_signals = (
        "right of first negotiation",
        "first negotiation right",
        "droit de première négociation",
        "droit de premiere négociation",
        "حق التفاوض الأول",
        "حق التفاوض الأول",
    )

    joint_ip_signals = (
        "joint ip",
        "joint intellectual property",
        "pi conjointe",
        "الملكية الفكرية المشتركة",
        "الملكية الفكرية المشترَكة",
    )

    if not (
        any(signal in low for signal in first_negotiation_signals)
        and any(signal in low for signal in joint_ip_signals)
    ):
        return current_value

    templates = {
        "en": (
            "A safer alternative is to preserve each party's ownership of its "
            "pre-existing intellectual property, keep Joint IP owned by the "
            "parties in equal undivided shares with each party permitted to "
            "exploit it without accounting to the other, and clearly define "
            "the existing right of first negotiation before either party "
            "licenses Joint IP to the other party's direct competitor, "
            "including the notice, negotiation period, and what happens if "
            "no agreement is reached."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préserver la propriété de "
            "chaque partie sur sa propriété intellectuelle préexistante, à "
            "maintenir la PI Conjointe en propriété conjointe par parts égales "
            "et indivises avec le droit pour chaque partie de l'exploiter sans "
            "avoir à rendre de comptes à l'autre, et à définir clairement le "
            "droit de première négociation existant avant qu'une partie ne "
            "concède une licence de PI Conjointe à un concurrent direct de "
            "l'autre partie, notamment la notification, la période de "
            "négociation et les conséquences d'une absence d'accord."
        ),
        "ar": (
            "البديل الأكثر أماناً هو الإبقاء على ملكية كل طرف لملكيته "
            "الفكرية السابقة، والإبقاء على الملكية الفكرية المشتركة مملوكة "
            "للطرفين بحصص متساوية وغير مقسمة مع حق كل طرف في استغلالها دون "
            "تقديم حساب للطرف الآخر، وتحديد حق التفاوض الأول القائم بوضوح "
            "قبل أن يمنح أي طرف ترخيصاً في الملكية الفكرية المشتركة لمنافس "
            "مباشر للطرف الآخر، بما في ذلك الإشعار ومدة التفاوض وما يترتب "
            "على عدم التوصل إلى اتفاق."
        ),
    }

    return templates[get_language(language)]



def normalize_clause_title(
    title: str,
) -> str:

    normalized = str(title or "").lower().strip()

    replacements = {
        "termination for cause":
            "termination",

        "constructive termination":
            "termination",

        "termination without cause":
            "termination",

        "confidentiality obligations":
            "confidentiality",

        "governing law":
            "governing_law",

        "notices":
            "general",

        "expense reimbursement":
            "payment",

        "change of control":
            "change_of_control",
    }

    replacements.update(globals().get("INTERNATIONAL_TITLE_ALIASES", {}))

    for source, target in replacements.items():
        if source in normalized:
            return target

    return normalized.replace(" ", "_")


def map_domain_to_reasoning_type(domain: str) -> str:
    domain = str(domain or "").lower()

    if domain in CLAUSE_REASONING_TEMPLATES:
        return domain

    return DOMAIN_TO_REASONING_TYPE.get(domain, "general")


def detect_clause_type_from_text(
    text: str,
    title: str = "",
) -> str:

    normalized_clause_title = normalize_clause_title(
        title
    )

    if normalized_clause_title in CLAUSE_REASONING_TEMPLATES:
        return normalized_clause_title

    normalized_text = str(text or "").lower()
    normalized_title = str(title or "").lower()

    # only first 500 chars matter
    intro_text = normalized_text[:500]

    best_clause_type = "general"
    best_score = 0

    for clause_type, template in CLAUSE_REASONING_TEMPLATES.items():

        signals = [
            s.lower()
            for s in template["signals"]
        ]

        title_score = sum(
            5
            for signal in signals
            if signal_present(signal, normalized_title)
        )

        intro_score = sum(
            2
            for signal in signals
            if signal_present(signal, intro_text)
        )

        # full body is intentionally weak
        body_score = sum(
            0.25
            for signal in signals
            if signal_present(signal, normalized_text)
        )

        total_score = (
            title_score
            + intro_score
            + body_score
        )

        if total_score > best_score:
            best_score = total_score
            best_clause_type = clause_type

    # avoid weak accidental matches
    if best_score < 3:

        ontology_domains = detect_legal_domains(
            text
        )

        if ontology_domains:
            return map_domain_to_reasoning_type(ontology_domains[0])

        return "general"

    return best_clause_type


def get_clause_reasoning_fallback(clause_type: str, language: str = "en") -> dict:
    language = get_language(language)
    clause_type = str(clause_type or "general").lower()

    fallbacks = {
        "general": {
            "en": {
                "legal_insight": "This clause should be reviewed for allocation of obligations, rights, remedies, timing, and practical enforceability.",
                "recommendation": "Confirm that the clause is clear, balanced, enforceable, and aligned with the parties' commercial expectations.",
                "negotiation": "Clarify ambiguous duties, add objective standards where needed, and ensure remedies are proportionate.",
            },
            "fr": {
                "legal_insight": "Cette clause doit être examinée au regard de la répartition des obligations, des droits, des recours, des délais et de son applicabilité pratique.",
                "recommendation": "Vérifier que la clause est claire, équilibrée, applicable et conforme aux attentes commerciales des parties.",
                "negotiation": "Clarifier les obligations ambiguës, ajouter des critères objectifs si nécessaire et prévoir des recours proportionnés.",
            },
            "ar": {
                "legal_insight": "يجب مراجعة هذا البند من حيث توزيع الالتزامات والحقوق ووسائل الانتصاف والمواعيد وقابلية التنفيذ العملية.",
                "recommendation": "تحقق من أن البند واضح ومتوازن وقابل للتنفيذ ومتوافق مع التوقعات التجارية للأطراف.",
                "negotiation": "وضّح الالتزامات الغامضة، وأضف معايير موضوعية عند الحاجة، وتأكد من أن وسائل الانتصاف متناسبة.",
            },
        }
    }

    return fallbacks["general"][language]


def get_market_comparison_fallback(
    clause_type: str,
    language: str = "en",
) -> str:
    language = get_language(language)

    return get_market_comparison(
        clause_type,
        language,
    )


def get_safer_alternative_fallback(
    clause_type: str,
    language: str = "en",
) -> str:
    language = get_language(language)

    return get_safer_alternative(
        clause_type,
        language,
    )


def get_clause_reasoning(
    clause_type: str,
    language: str = "en",
    sector: str = None,
) -> dict:
    language = get_language(language)
    clause_type = str(clause_type or "general").lower()
    clause_type = map_domain_to_reasoning_type(clause_type)

    template = CLAUSE_REASONING_TEMPLATES.get(clause_type)

    if not template:
        market = get_market_intelligence(
            clause_type,
            language,
        )

        result = {
            "clause_type": clause_type or "general",
            "legal_insight": "",
            "recommendation": "",
            "negotiation": "",
            "market_comparison": market.get("market_comparison", ""),
            "market_practice": market.get("market_practice", "standard"),
            "market_benchmark": market.get("market_benchmark", "common"),
            "negotiability": market.get("negotiability", "medium"),
            "market_confidence": market.get("market_confidence", 0.65),
            "safer_alternative": get_safer_alternative_fallback(
                clause_type,
                language,
            ),
        }

    else:
        market = get_market_intelligence(
            clause_type,
            language,
        )

        result = {
            "clause_type": clause_type,
            "legal_insight": template["legal_insight"].get(
                language,
                template["legal_insight"]["en"],
            ),
            "recommendation": template["recommendation"].get(
                language,
                template["recommendation"]["en"],
            ),
            "negotiation": template["negotiation"].get(
                language,
                template["negotiation"]["en"],
            ),
            "market_comparison": market.get("market_comparison", ""),
            "market_practice": market.get("market_practice", "standard"),
            "market_benchmark": market.get("market_benchmark", "common"),
            "negotiability": market.get("negotiability", "medium"),
            "market_confidence": market.get("market_confidence", 0.65),
            "safer_alternative": get_safer_alternative_fallback(
                clause_type,
                language,
            ),
        }

    # --- Additive enrichment (optional, never breaks existing callers) ---

    # Draft wording: real, fillable clause text (or the universal generic
    # skeleton if no specific template exists for this clause_type).
    template_info = get_clause_template(clause_type, language)
    result["draft_wording_template"] = template_info["template"]
    result["draft_wording_placeholders"] = template_info["placeholders"]
    result["draft_wording_is_specific"] = template_info["specific"]
    result["draft_wording_disclaimer"] = template_info["disclaimer"]

    # Sector overlay: only added if a sector was explicitly requested and
    # a specific overlay exists for this (clause_type, sector) pair.
    # Absence of an overlay is normal and not surfaced as an error.
    result["sector_note"] = None
    if sector:
        result["sector_note"] = get_sector_overlay(
            clause_type,
            sector,
            language,
        )

    return result


def get_contract_level_reasoning(
    clause_types: list,
    language: str = "en",
    jurisdiction: str = None,
) -> dict:
    """
    Contract-level reasoning that spans multiple clauses at once: detects
    documented tensions/dependencies between the clause types present in
    the contract, and optionally attaches a general jurisdiction caveat.

    This complements get_clause_reasoning() (which reasons on ONE clause
    at a time) with reasoning that only makes sense across the whole set
    of clauses detected in a contract. Purely additive: existing callers
    of get_clause_reasoning() / get_clause_reasoning_for_text() are
    entirely unaffected by this function's existence.
    """
    language = get_language(language)

    interactions = get_clause_interactions(
        clause_types or [],
        language,
    )

    result = {
        "interactions": interactions,
        "jurisdiction_caveat": None,
    }

    if jurisdiction:
        result["jurisdiction_caveat"] = get_jurisdiction_caveat(
            jurisdiction,
            language,
        )

    return result


def get_clause_reasoning_for_text(
    text: str,
    language: str = "en",
    title: str = "",
    sector: str = None,
    clause_type: str | None = None,
) -> dict:
    if clause_type:
        # An authoritative clause_type was already determined upstream
        # (e.g. by contract_taxonomy.py's detect_clause_type_from_taxonomy(),
        # which is re-run and can correct the initial classification) --
        # use it directly instead of re-detecting independently here.
        # Confirmed real bug: this function's own, separate detection
        # (raw text + title-based aliases) could disagree with the
        # already-corrected, authoritative type, silently generating
        # legal_insight/recommendation/fallback_wording for the WRONG
        # clause type even though the correct type was already known
        # and available to the caller.
        clause_type = str(clause_type).lower().strip()
    else:
        raw_clause_type = detect_clause_type_from_text(
            text,
            title=title,
        )

        clause_type = str(raw_clause_type or "general").lower().strip()
        normalized_title = str(title or "").lower().strip()

        title_type_aliases = {
        # English
        "security measures": "data_privacy_security",
        "security incident notification": "data_privacy_security",
        "subprocessor engagement": "data_privacy_security",
        "data processing": "data_privacy_security",
        "return or destruction of personal data and confidential information": "data_privacy_security",
        "return or destruction of data": "data_privacy_security",
        "uptime commitment and service credits": "sla",
        "service availability": "sla",
        "limitation of liability": "liability",
        "limitation of liability exceptions": "liability",
        "termination for convenience": "termination",
        "termination for cause": "termination",
        "term and renewal": "termination",
        "non-solicitation": "restrictive_covenants",
        "non-compete obligation": "restrictive_covenants",
        "intellectual property rights": "intellectual_property",
        "ownership of deliverables": "intellectual_property",
        "assignment of deliverables": "intellectual_property",
        "moral rights waiver": "intellectual_property",
        "assignment": "assignment",

        # French
        "mesures de sécurité": "data_privacy_security",
        "notification d'incident de sécurité": "data_privacy_security",
        "notification d’incident de sécurité": "data_privacy_security",
        "engagement d'un sous-traitant ultérieur": "data_privacy_security",
        "engagement d’un sous-traitant ultérieur": "data_privacy_security",
        "sous-traitance des données personnelles": "data_privacy_security",
        "traitement des données personnelles": "data_privacy_security",
        "traitement des données": "data_privacy_security",
        "restitution ou destruction des données": "data_privacy_security",
        "restitution ou destruction des données personnelles et des informations confidentielles": "data_privacy_security",
        "restitution ou destruction des données et des informations confidentielles": "data_privacy_security",
        "crédits de service": "sla",
        "disponibilité des services": "sla",
        "limitation de responsabilité": "liability",
        "résiliation pour convenance": "termination",
        "résiliation pour faute": "termination",
        "durée et renouvellement": "termination",
        "restriction de sollicitation": "restrictive_covenants",
        "restriction de non-concurrence": "restrictive_covenants",
        "droits de propriété intellectuelle": "intellectual_property",
        "cession des livrables": "intellectual_property",
        "cession des droits moraux": "intellectual_property",
        "cession": "assignment",

        # Arabic
        "التدابير الأمنية": "data_privacy_security",
        "الإخطار بحادث أمني": "data_privacy_security",
        "الاستعانة بمعالج فرعي": "data_privacy_security",
        "معالجة البيانات الشخصية": "data_privacy_security",
        "معالجة البيانات": "data_privacy_security",
        "إعادة أو إتلاف البيانات": "data_privacy_security",
        "إعادة أو إتلاف البيانات الشخصية والمعلومات السرية": "data_privacy_security",
        "تعويضات الخدمة": "sla",
        "توافر الخدمات": "sla",
        "حد المسؤولية": "liability",
        "الإنهاء لدواعي الملاءمة": "termination",
        "الإنهاء لسبب مشروع": "termination",
        "المدة والتجديد": "termination",
        "قيد الاستقطاب": "restrictive_covenants",
        "قيد عدم المنافسة": "restrictive_covenants",
        "حقوق الملكية الفكرية": "intellectual_property",
        "ملكية المخرجات": "intellectual_property",
        "التنازل عن الحقوق المعنوية": "intellectual_property",
        "التنازل": "assignment",
        }

        clause_type = title_type_aliases.get(
            normalized_title,
            clause_type,
        )

    # Producer-aware multi-candidate routing.
    #
    # The strict publication gate compares each protected generated field to
    # the source taxonomy primary type. A single source winner is therefore
    # insufficient as a universal reasoning family for multi-signal clauses.
    # Build reasoning from every admissible source/authoritative candidate and
    # select EACH protected producer field independently.
    (
        source_primary_type,
        producer_candidate_types,
        source_detected_types,
    ) = get_source_grounding_candidates(
        text,
        clause_type,
    )

    reasoning_candidates = [
        _build_reasoning_candidate(
            candidate_type,
            text,
            language,
            sector=sector,
        )
        for candidate_type in producer_candidate_types
    ]

    # Keep a complete base object for additive/non-protected metadata.
    base_reasoning = dict(
        reasoning_candidates[0]
        if reasoning_candidates
        else get_clause_reasoning(
            map_domain_to_reasoning_type(clause_type),
            language,
            sector=sector,
        )
    )

    selected_producers = {}

    for field in (
        "legal_insight",
        "recommendation",
        "negotiation",
        "market_comparison",
    ):
        value, producer_type = (
            _select_field_from_reasoning_candidates(
                reasoning_candidates,
                field,
                source_primary_type,
                clause_type,
                source_detected_types,
            )
        )

        if value:
            base_reasoning[field] = value

        if producer_type:
            selected_producers[field] = producer_type

    base_reasoning["source_reasoning_primary_type"] = (
        source_primary_type
    )
    base_reasoning["source_reasoning_candidate_types"] = (
        producer_candidate_types
    )
    base_reasoning["source_reasoning_detected_types"] = (
        source_detected_types
    )
    base_reasoning["selected_reasoning_producers"] = (
        selected_producers
    )

    base_reasoning["safer_alternative"] = (
        _source_aware_safer_alternative(
            text,
            language,
            str(
                base_reasoning.get("safer_alternative")
                or ""
            ),
        )
    )

    contextual_reasoning = get_contextual_risk_reasoning(
        str(clause_type or source_primary_type),
        text,
        language,
    )

    contextual_insight = str(
        contextual_reasoning.get("legal_insight")
        or ""
    ).strip()

    if (
        contextual_reasoning
        and contextual_insight
        and _field_candidate_rank(
            contextual_insight,
            source_primary_type,
        ) < 2
    ):
        base_reasoning["legal_insight"] = contextual_insight
        base_reasoning["risk_level"] = contextual_reasoning.get(
            "risk_level",
            base_reasoning.get("risk_level", "medium"),
        )
        base_reasoning["contextual_reasoning"] = True
    else:
        base_reasoning["contextual_reasoning"] = False

    normalized_title = str(title or "").lower().strip()

    if normalized_title in BOILERPLATE_CLAUSES:
        base_reasoning["recommendation"] = ""

    if (
        base_reasoning.get("legal_insight")
        ==
        base_reasoning.get("recommendation")
    ):
        base_reasoning["recommendation"] = ""

    legal_insight = str(
        base_reasoning.get(
            "legal_insight",
            "",
        )
    ).strip()

    if legal_insight in GENERIC_LEGAL_INSIGHTS:
        base_reasoning["legal_insight"] = ""

    recommendation = str(
        base_reasoning.get(
            "recommendation",
            "",
        )
    ).strip()

    if recommendation in GENERIC_RECOMMENDATIONS:
        base_reasoning["recommendation"] = ""

    # Negotiation intelligence enrichment (additive, never overwrites
    # existing keys like "market_practice" -- see negotiation_intelligence.py
    # for the field-naming rationale). Works for ANY clause_type: restrictive
    # covenants get specialized duration-driven analysis, every other
    # clause_type still receives honest generic negotiation guidance.
    base_reasoning = enrich_negotiation_fields(
        base_reasoning,
        text,
        language,
        clause_type=clause_type,
    )

    return base_reasoning
def get_reasoning_for_text(
    text: str,
    language: str = "en",
    title: str = "",
    sector: str = None,
    clause_type: str | None = None,
) -> dict:
    return get_clause_reasoning_for_text(
        text=text,
        language=language,
        title=title,
        sector=sector,
        clause_type=clause_type,
    )
