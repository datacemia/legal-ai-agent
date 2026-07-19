"""
sector_overlays.py

Sector-specific enrichment layered on top of the universal clause
categories, for the small set of (clause_type, sector) combinations
where a specific sector materially changes what should be checked
(e.g. data_privacy_security in fintech vs. healthcare).

Design goals (same as the rest of the contract_agent stack):
- The universal engine (market_intelligence.py / clause_wording_library.py
  / clause_templates.py / clause_interactions.py) already works for ANY
  contract in ANY domain on its own. This module is a pure, OPTIONAL
  enrichment on top of that -- it never gates or blocks the core
  reasoning, and its absence for a given (clause_type, sector) pair is
  not an error.
- Supports EN / FR / AR.
- Purely additive: does not modify any other file in the stack, only
  imports the shared clause-type resolver so it stays in sync.
- Honest by design: if no overlay is defined for a given
  (clause_type, sector) pair, this returns None rather than fabricating
  sector-flavored text that isn't actually sector-specific. A caller
  should treat None as "no additional sector note for this combination"
  and simply keep using the universal reasoning already produced
  elsewhere in the stack.
"""

from app.services.contract_agent.market_intelligence import (
    normalize_clause_type,
    get_language,
)


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def _normalize_sector(sector: str) -> str:
    return str(sector or "").lower().strip().replace(" ", "_").replace("-", "_")


SECTOR_ALIASES = {
    "fin_tech": "fintech",
    "financial_services": "fintech",
    "banking": "fintech",
    "payments": "fintech",
    "health": "healthcare",
    "medical": "healthcare",
    "life_sciences": "healthcare",
    "pharma": "healthcare",
    "power": "energy",
    "utilities": "energy",
    "oil_and_gas": "energy",
    "telecommunications": "telecom",
    "telco": "telecom",
    "public_sector": "government_contracting",
    "government": "government_contracting",
    "defense": "government_contracting",
    "insurer": "insurance_sector",
    "insurtech": "insurance_sector",
    "manufacturing": "manufacturing_industrial",
    "industrial": "manufacturing_industrial",
    "industrials": "manufacturing_industrial",
}


def normalize_sector(sector: str) -> str:
    value = _normalize_sector(sector)
    return SECTOR_ALIASES.get(value, value)


# ---------------------------------------------------------------------------
# Overlays: (clause_type, sector) -> {en, fr, ar}
# Only defined for combinations where the sector genuinely changes what
# should be reviewed. Absence of an entry is expected and normal for the
# vast majority of (clause_type, sector) pairs.
# ---------------------------------------------------------------------------

SECTOR_OVERLAYS = {
    ("data_privacy_security", "fintech"): {
        "en": (
            "In fintech contracts, data and security clauses should also "
            "be checked against applicable payment-services and card-data "
            "security requirements (such as PCI-DSS for cardholder data), "
            "in addition to general data-protection obligations."
        ),
        "fr": (
            "Dans les contrats fintech, les clauses relatives aux données "
            "et à la sécurité doivent également être vérifiées au regard "
            "des exigences de sécurité applicables aux services de paiement "
            "et aux données de carte (telles que PCI-DSS pour les données "
            "porteur), en plus des obligations générales de protection des "
            "données."
        ),
        "ar": (
            "في عقود التكنولوجيا المالية، يجب أيضاً مراجعة بنود البيانات "
            "والأمن في ضوء متطلبات أمن خدمات الدفع وبيانات البطاقات "
            "المعمول بها (مثل معيار PCI-DSS لبيانات حامل البطاقة)، إضافة "
            "إلى الالتزامات العامة لحماية البيانات."
        ),
    },
    ("data_privacy_security", "healthcare"): {
        "en": (
            "In healthcare contracts, data clauses commonly need to "
            "reference applicable health-data protection frameworks (such "
            "as HIPAA or equivalent regimes) and any business-associate or "
            "processor obligations specific to health information."
        ),
        "fr": (
            "Dans les contrats du secteur de la santé, les clauses de "
            "données doivent généralement faire référence aux cadres de "
            "protection des données de santé applicables (tels que HIPAA "
            "ou des régimes équivalents) et aux obligations spécifiques des "
            "partenaires ou sous-traitants concernant les informations de "
            "santé."
        ),
        "ar": (
            "في عقود القطاع الصحي، غالباً ما يجب أن تشير بنود البيانات إلى "
            "أطر حماية بيانات الصحة المعمول بها (مثل HIPAA أو أنظمة "
            "مماثلة) والتزامات الشركاء التجاريين أو المعالجين الخاصة "
            "بالمعلومات الصحية."
        ),
    },
    ("data_privacy_security", "telecom"): {
        "en": (
            "In telecom contracts, data clauses should also address "
            "sector-specific data-retention and lawful-interception "
            "obligations, which often diverge from, and can be stricter "
            "than, general data-protection deletion duties."
        ),
        "fr": (
            "Dans les contrats télécoms, les clauses de données doivent "
            "également traiter des obligations sectorielles de "
            "conservation des données et d'interception légale, qui "
            "divergent souvent des obligations générales de suppression et "
            "peuvent être plus strictes."
        ),
        "ar": (
            "في عقود الاتصالات، يجب أن تعالج بنود البيانات أيضاً التزامات "
            "قطاعية خاصة بالاحتفاظ بالبيانات والتنصت القانوني، والتي "
            "غالباً ما تختلف عن واجبات الحذف العامة لحماية البيانات وقد "
            "تكون أكثر صرامة."
        ),
    },
    ("data_privacy_security", "government_contracting"): {
        "en": (
            "In government contracts, data clauses often need to reference "
            "specific government security accreditation frameworks, "
            "data-residency requirements, and national-security or "
            "classified-information handling rules beyond general "
            "commercial data-protection standards."
        ),
        "fr": (
            "Dans les contrats publics, les clauses de données doivent "
            "souvent faire référence à des cadres d'accréditation "
            "sécuritaire gouvernementaux spécifiques, à des exigences de "
            "résidence des données et à des règles de traitement des "
            "informations classifiées ou liées à la sécurité nationale, "
            "au-delà des standards commerciaux généraux de protection des "
            "données."
        ),
        "ar": (
            "في العقود الحكومية، غالباً ما يجب أن تشير بنود البيانات إلى "
            "أطر اعتماد أمني حكومية محددة، ومتطلبات إقامة البيانات محلياً، "
            "وقواعد التعامل مع المعلومات السرية أو المتعلقة بالأمن الوطني، "
            "بما يتجاوز المعايير التجارية العامة لحماية البيانات."
        ),
    },

    ("liability", "fintech"): {
        "en": (
            "In fintech contracts, liability clauses should be checked "
            "against applicable financial-services regulation and "
            "consumer-protection rules, which in many jurisdictions cannot "
            "be excluded or capped below statutory minimums."
        ),
        "fr": (
            "Dans les contrats fintech, les clauses de responsabilité "
            "doivent être vérifiées au regard de la réglementation "
            "applicable aux services financiers et des règles de protection "
            "des consommateurs, qui dans de nombreuses juridictions ne "
            "peuvent être exclues ou plafonnées en deçà des minimums légaux."
        ),
        "ar": (
            "في عقود التكنولوجيا المالية، يجب مراجعة بنود المسؤولية في "
            "ضوء تنظيم الخدمات المالية المعمول به وقواعد حماية المستهلك، "
            "والتي لا يمكن في العديد من الولايات القضائية استبعادها أو "
            "تحديدها دون الحدود الدنيا القانونية."
        ),
    },
    ("liability", "healthcare"): {
        "en": (
            "In healthcare contracts, liability clauses should be reviewed "
            "against professional-liability and patient-safety regulation, "
            "since claims involving personal injury or malpractice are "
            "typically treated as a carve-out from any general liability "
            "cap."
        ),
        "fr": (
            "Dans les contrats de santé, les clauses de responsabilité "
            "doivent être examinées au regard de la réglementation relative "
            "à la responsabilité professionnelle et à la sécurité des "
            "patients, les réclamations pour dommage corporel ou faute "
            "professionnelle étant généralement traitées comme une "
            "exception au plafond général de responsabilité."
        ),
        "ar": (
            "في عقود الرعاية الصحية، يجب مراجعة بنود المسؤولية في ضوء "
            "تنظيم المسؤولية المهنية وسلامة المرضى، إذ تُعامل المطالبات "
            "المتعلقة بالإصابة الشخصية أو الخطأ المهني عادة كاستثناء من "
            "حد المسؤولية العام."
        ),
    },
    ("liability", "insurance_sector"): {
        "en": (
            "In insurance-sector contracts, liability clauses should be "
            "checked against applicable insurance regulation, which can "
            "impose mandatory minimum coverage, claims-handling duties, or "
            "restrictions on limiting liability toward policyholders."
        ),
        "fr": (
            "Dans les contrats du secteur de l'assurance, les clauses de "
            "responsabilité doivent être vérifiées au regard de la "
            "réglementation d'assurance applicable, qui peut imposer une "
            "couverture minimale obligatoire, des obligations de gestion "
            "des sinistres ou des restrictions sur la limitation de "
            "responsabilité envers les assurés."
        ),
        "ar": (
            "في عقود قطاع التأمين، يجب مراجعة بنود المسؤولية في ضوء "
            "تنظيم التأمين المعمول به، والذي قد يفرض حداً أدنى إلزامياً "
            "للتغطية، أو واجبات في معالجة المطالبات، أو قيوداً على تحديد "
            "المسؤولية تجاه حاملي وثائق التأمين."
        ),
    },

    ("insurance", "healthcare"): {
        "en": (
            "In healthcare contracts, required insurance should typically "
            "include professional liability / malpractice coverage in "
            "addition to general commercial liability insurance."
        ),
        "fr": (
            "Dans les contrats de santé, l'assurance requise devrait "
            "généralement inclure une couverture de responsabilité "
            "professionnelle / faute médicale en plus de l'assurance "
            "responsabilité civile commerciale générale."
        ),
        "ar": (
            "في عقود الرعاية الصحية، ينبغي أن يشمل التأمين المطلوب عادة "
            "تغطية المسؤولية المهنية / الخطأ الطبي بالإضافة إلى تأمين "
            "المسؤولية التجارية العامة."
        ),
    },
    ("insurance", "energy"): {
        "en": (
            "In energy-sector contracts, required insurance should be "
            "reviewed against sector-specific environmental-liability and "
            "operator-liability requirements, which are often mandated by "
            "regulation independent of the parties' agreement."
        ),
        "fr": (
            "Dans les contrats du secteur de l'énergie, l'assurance requise "
            "doit être examinée au regard des exigences sectorielles de "
            "responsabilité environnementale et de responsabilité de "
            "l'exploitant, souvent imposées par la réglementation "
            "indépendamment de l'accord des parties."
        ),
        "ar": (
            "في عقود قطاع الطاقة، يجب مراجعة التأمين المطلوب في ضوء "
            "متطلبات المسؤولية البيئية ومسؤولية المشغل الخاصة بالقطاع، "
            "والتي غالباً ما تفرضها الأنظمة بصرف النظر عن اتفاق الطرفين."
        ),
    },
    ("insurance", "manufacturing_industrial"): {
        "en": (
            "In manufacturing and industrial contracts, required insurance "
            "should typically include product-liability coverage in "
            "addition to general liability, given the elevated risk of "
            "physical injury or property damage from defective goods."
        ),
        "fr": (
            "Dans les contrats de fabrication et industriels, l'assurance "
            "requise devrait généralement inclure une couverture de "
            "responsabilité produit en plus de la responsabilité civile "
            "générale, compte tenu du risque accru de dommage corporel ou "
            "matériel lié à des produits défectueux."
        ),
        "ar": (
            "في العقود الصناعية والتصنيعية، ينبغي أن يشمل التأمين المطلوب "
            "عادة تغطية مسؤولية المنتج بالإضافة إلى المسؤولية العامة، "
            "نظراً لارتفاع مخاطر الإصابة الجسدية أو الأضرار المادية "
            "الناتجة عن منتجات معيبة."
        ),
    },

    ("export_control", "energy"): {
        "en": (
            "In the energy sector, export-control clauses should be "
            "checked against dual-use technology restrictions and "
            "sanctions regimes specific to energy infrastructure and "
            "equipment, which are frequently updated and sector-targeted."
        ),
        "fr": (
            "Dans le secteur de l'énergie, les clauses de contrôle des "
            "exportations doivent être vérifiées au regard des restrictions "
            "applicables aux technologies à double usage et des régimes de "
            "sanctions spécifiques aux infrastructures et équipements "
            "énergétiques, fréquemment mis à jour et ciblés sur ce secteur."
        ),
        "ar": (
            "في قطاع الطاقة، يجب مراجعة بنود ضوابط التصدير في ضوء قيود "
            "التقنيات مزدوجة الاستخدام وأنظمة العقوبات الخاصة بالبنية "
            "التحتية والمعدات المتعلقة بالطاقة، والتي كثيراً ما تُحدَّث "
            "وتستهدف هذا القطاع تحديداً."
        ),
    },
    ("export_control", "manufacturing_industrial"): {
        "en": (
            "In manufacturing and industrial contracts, export-control "
            "clauses should address whether the goods or components "
            "qualify as dual-use items subject to export licensing "
            "requirements before cross-border shipment or technology "
            "transfer."
        ),
        "fr": (
            "Dans les contrats de fabrication et industriels, les clauses "
            "de contrôle des exportations doivent traiter la question de "
            "savoir si les biens ou composants relèvent de la catégorie des "
            "produits à double usage soumis à une exigence de licence "
            "d'exportation avant tout envoi transfrontalier ou transfert de "
            "technologie."
        ),
        "ar": (
            "في العقود الصناعية والتصنيعية، يجب أن تعالج بنود ضوابط "
            "التصدير ما إذا كانت السلع أو المكونات تندرج ضمن فئة السلع "
            "مزدوجة الاستخدام الخاضعة لمتطلبات ترخيص التصدير قبل الشحن "
            "العابر للحدود أو نقل التقنية."
        ),
    },

    ("anti_bribery_compliance", "government_contracting"): {
        "en": (
            "In government-contracting agreements, anti-bribery and "
            "compliance clauses should reference applicable public-"
            "procurement integrity rules in addition to general anti-"
            "corruption standards, since public contracts are typically "
            "subject to heightened scrutiny and specific debarment "
            "consequences."
        ),
        "fr": (
            "Dans les contrats publics, les clauses anti-corruption et de "
            "conformité doivent faire référence aux règles d'intégrité des "
            "marchés publics applicables en plus des standards généraux "
            "anti-corruption, les contrats publics étant généralement "
            "soumis à un contrôle renforcé et à des conséquences "
            "spécifiques d'exclusion."
        ),
        "ar": (
            "في عقود التعاقد الحكومي، يجب أن تشير بنود مكافحة الرشوة "
            "والامتثال إلى قواعد نزاهة المشتريات العامة المعمول بها "
            "بالإضافة إلى المعايير العامة لمكافحة الفساد، إذ تخضع العقود "
            "الحكومية عادة لرقابة مشددة وعواقب استبعاد محددة."
        ),
    },
    ("audit_rights", "government_contracting"): {
        "en": (
            "In government contracts, audit rights are often broader and "
            "mandated by procurement regulation (including audits by the "
            "government itself or its inspectors general), beyond what "
            "would typically be negotiated in a purely commercial contract."
        ),
        "fr": (
            "Dans les contrats publics, les droits d'audit sont souvent "
            "plus étendus et imposés par la réglementation des marchés "
            "publics (y compris des audits menés par l'administration "
            "elle-même ou ses corps d'inspection), au-delà de ce qui serait "
            "généralement négocié dans un contrat purement commercial."
        ),
        "ar": (
            "في العقود الحكومية، غالباً ما تكون حقوق التدقيق أوسع "
            "ومفروضة بموجب تنظيم المشتريات (بما في ذلك عمليات تدقيق تجريها "
            "الجهة الحكومية نفسها أو هيئات التفتيش التابعة لها)، بما "
            "يتجاوز ما يُتفاوض عليه عادة في عقد تجاري بحت."
        ),
    },

    ("financial_covenants", "fintech"): {
        "en": (
            "In fintech lending or financial-services contracts, financial "
            "covenants should be checked against applicable capital-"
            "adequacy or regulatory-ratio requirements imposed by financial "
            "regulators, which may be stricter than the contractually "
            "negotiated thresholds."
        ),
        "fr": (
            "Dans les contrats de prêt ou de services financiers fintech, "
            "les engagements financiers doivent être vérifiés au regard des "
            "exigences d'adéquation des fonds propres ou de ratios "
            "réglementaires imposées par les régulateurs financiers, qui "
            "peuvent être plus strictes que les seuils négociés "
            "contractuellement."
        ),
        "ar": (
            "في عقود الإقراض أو الخدمات المالية للتكنولوجيا المالية، يجب "
            "مراجعة التعهدات المالية في ضوء متطلبات كفاية رأس المال أو "
            "النسب التنظيمية التي تفرضها الجهات الرقابية المالية، والتي "
            "قد تكون أكثر صرامة من الحدود المتفاوض عليها تعاقدياً."
        ),
    },

    ("warranty", "manufacturing_industrial"): {
        "en": (
            "In manufacturing and industrial contracts, warranty clauses "
            "should be checked against applicable product-safety and "
            "product-liability regulation, since certain safety-related "
            "warranty obligations may not be waivable or limitable by "
            "contract."
        ),
        "fr": (
            "Dans les contrats de fabrication et industriels, les clauses "
            "de garantie doivent être vérifiées au regard de la "
            "réglementation applicable en matière de sécurité et de "
            "responsabilité des produits, certaines obligations de garantie "
            "liées à la sécurité ne pouvant être écartées ou limitées par "
            "contrat."
        ),
        "ar": (
            "في العقود الصناعية والتصنيعية، يجب مراجعة بنود الضمان في ضوء "
            "تنظيم سلامة المنتجات ومسؤولية المنتج المعمول به، إذ قد لا "
            "يجوز التنازل عن بعض التزامات الضمان المتعلقة بالسلامة أو "
            "تحديدها تعاقدياً."
        ),
    },
}


def get_sector_overlay(
    clause_type: str,
    sector: str,
    language: str = "en",
) -> str:
    """
    Return a sector-specific enrichment note for a (clause_type, sector)
    pair, or None if no overlay is defined for that combination.

    None is an expected, normal result for the vast majority of
    combinations -- it means "the universal clause reasoning already
    produced elsewhere in the stack applies as-is, with no sector-specific
    addition needed here." It is not an error and should not be treated
    as a gap to fill by the caller; the core engine already covers any
    contract in any domain on its own.
    """
    language = get_language(language)
    normalized_type = normalize_clause_type(clause_type)
    normalized_sector = normalize_sector(sector)

    if not normalized_sector:
        return None

    entry = SECTOR_OVERLAYS.get((normalized_type, normalized_sector))
    if not entry:
        return None

    return entry.get(language, entry.get("en"))


def list_supported_sectors() -> list:
    return sorted({sector for (_, sector) in SECTOR_OVERLAYS.keys()})


def list_covered_clause_types_for_sector(sector: str) -> list:
    normalized_sector = normalize_sector(sector)
    return sorted({
        clause_type
        for (clause_type, s) in SECTOR_OVERLAYS.keys()
        if s == normalized_sector
    })
