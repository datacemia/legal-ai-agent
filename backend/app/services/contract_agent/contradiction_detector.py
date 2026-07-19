"""
Universal contract contradiction detector.

Designed for international contract analysis across contract families,
industries, and output languages (EN / FR / AR).

Principles:
- Prefer normalized clause types from the contract taxonomy when available.
- Fall back to multilingual textual signals only when clause_type metadata is missing.
- Do not overstate contradictions: return "potential" inconsistencies that should be reviewed.
- Attach the involved clauses so the UI can show evidence and navigation.
"""

from __future__ import annotations

from typing import Any


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def _lang(language: str) -> str:
    return language if language in SUPPORTED_LANGUAGES else "en"


def normalize_text(value: Any) -> str:
    return " ".join(str(value or "").lower().strip().split())


def get_clause_text(clause: dict) -> str:
    return " ".join(
        str(clause.get(key) or "")
        for key in (
            "quoted_text",
            "original_text",
            "clause_text",
            "text",
            "explanation_simple",
            "legal_insight",
        )
    )


def get_clause_title(clause: dict) -> str:
    return str(
        clause.get("title")
        or clause.get("clause_title")
        or clause.get("name")
        or ""
    ).strip()


def get_clause_reference(clause: dict) -> str:
    return str(
        clause.get("clause_reference")
        or clause.get("reference")
        or clause.get("section")
        or ""
    ).strip()


def get_clause_type(clause: dict) -> str:
    return normalize_text(
        clause.get("clause_type")
        or clause.get("type")
        or clause.get("primary_type")
        or "other"
    ).replace(" ", "_")


def get_secondary_types(clause: dict) -> set[str]:
    values = clause.get("secondary_types") or clause.get("secondary_clause_types") or []

    if isinstance(values, str):
        values = [values]

    return {
        normalize_text(value).replace(" ", "_")
        for value in values
        if normalize_text(value)
    }


def clause_type_set(clause: dict) -> set[str]:
    types = {get_clause_type(clause)}
    types.update(get_secondary_types(clause))
    return {t for t in types if t and t != "other"}


def clause_has_any_type(clause: dict, expected_types: set[str]) -> bool:
    return bool(clause_type_set(clause).intersection(expected_types))


def clause_has_signal(clause: dict, signals: list[str]) -> bool:
    text = normalize_text(" ".join([get_clause_title(clause), get_clause_text(clause)]))
    return any(normalize_text(signal) in text for signal in signals)


def compact_clause(clause: dict) -> dict:
    text = get_clause_text(clause).strip()

    return {
        "title": get_clause_title(clause),
        "reference": get_clause_reference(clause),
        "clause_type": get_clause_type(clause),
        "risk_level": clause.get("risk_level", ""),
        "excerpt": text[:500],
    }


CONTRADICTION_RULES = [
    {
        "id": "liability_cap_vs_unlimited_liability",
        "label": {
            "en": "Liability cap vs. unlimited liability",
            "fr": "Plafond de responsabilité vs responsabilité illimitée",
            "ar": "حد المسؤولية مقابل المسؤولية غير المحدودة",
        },
        "severity": "high",
        "a_types": {"limitation_of_liability", "liability"},
        "a_signals": [
            "liability cap", "limitation of liability", "limited liability",
            "plafond de responsabilité", "limitation de responsabilité",
            "حد المسؤولية", "تحديد المسؤولية",
        ],
        "b_signals": [
            "unlimited liability", "liability without limitation",
            "responsabilité illimitée", "sans limitation de responsabilité",
            "مسؤولية غير محدودة", "دون حد للمسؤولية",
        ],
        "message": {
            "en": "The agreement may contain inconsistent language about whether liability is capped or unlimited.",
            "fr": "L'accord peut contenir des formulations incohérentes quant au caractère plafonné ou illimité de la responsabilité.",
            "ar": "قد يتضمن الاتفاق صياغة غير متسقة بشأن ما إذا كانت المسؤولية محدودة أم غير محدودة.",
        },
    },
    {
        "id": "fixed_term_vs_termination_anytime",
        "label": {
            "en": "Fixed term vs. termination at any time",
            "fr": "Durée fixe vs résiliation à tout moment",
            "ar": "مدة محددة مقابل الإنهاء في أي وقت",
        },
        "severity": "medium",
        "a_types": {"term", "duration"},
        "a_signals": ["fixed term", "initial term", "durée déterminée", "مدة محددة", "مدة أولية"],
        "b_types": {"termination_for_convenience", "termination"},
        "b_signals": ["terminate at any time", "without cause", "résilier à tout moment", "sans motif", "إنهاء في أي وقت", "دون سبب"],
        "message": {
            "en": "The agreement may contain tension between a fixed duration and broad termination rights.",
            "fr": "L'accord peut présenter une tension entre une durée déterminée et de larges droits de résiliation.",
            "ar": "قد يتضمن الاتفاق تعارضاً بين مدة محددة وحقوق إنهاء واسعة النطاق.",
        },
    },
    {
        "id": "confidentiality_fixed_vs_indefinite",
        "label": {
            "en": "Fixed vs. indefinite confidentiality",
            "fr": "Confidentialité à durée fixe vs indéfinie",
            "ar": "سرية محددة المدة مقابل غير محددة المدة",
        },
        "severity": "medium",
        "a_types": {"confidentiality"},
        "a_signals": ["two years", "three years", "five years", "deux ans", "trois ans", "cinq ans", "سنتين", "ثلاث سنوات", "خمس سنوات"],
        "b_types": {"confidentiality"},
        "b_signals": ["indefinitely", "perpetual", "survive indefinitely", "perpétuelle", "indéfiniment", "دائمة", "إلى أجل غير مسمى"],
        "message": {
            "en": "The agreement may use both fixed and indefinite confidentiality survival periods; the scope of each should be reconciled.",
            "fr": "L'accord peut utiliser à la fois des durées de survie de confidentialité fixes et indéfinies ; la portée de chacune devrait être clarifiée.",
            "ar": "قد يستخدم الاتفاق مدد استمرار سرية محددة وغير محددة في آن واحد؛ وينبغي توضيح نطاق كل منهما.",
        },
    },
    {
        "id": "exclusive_vs_non_exclusive",
        "label": {
            "en": "Exclusive vs. non-exclusive",
            "fr": "Exclusif vs non exclusif",
            "ar": "حصري مقابل غير حصري",
        },
        "severity": "high",
        "a_types": {"exclusivity"},
        "a_signals": ["exclusive", "sole provider", "exclusif", "exclusivité", "حصري", "حصرية"],
        "b_types": {"exclusivity"},
        "b_signals": ["non-exclusive", "non exclusive", "non exclusif", "غير حصري"],
        "message": {
            "en": "The agreement may contain both exclusive and non-exclusive language for the same commercial relationship.",
            "fr": "L'accord peut contenir à la fois des formulations exclusives et non exclusives pour la même relation commerciale.",
            "ar": "قد يتضمن الاتفاق صياغة حصرية وغير حصرية معاً لنفس العلاقة التجارية.",
        },
    },
    {
        "id": "court_jurisdiction_vs_mandatory_arbitration",
        "label": {
            "en": "Court jurisdiction vs. mandatory arbitration",
            "fr": "Compétence judiciaire vs arbitrage obligatoire",
            "ar": "الاختصاص القضائي مقابل التحكيم الإلزامي",
        },
        "severity": "medium",
        "a_types": {"jurisdiction", "venue", "governing_law"},
        "a_signals": ["exclusive jurisdiction", "courts of", "tribunaux", "juridiction exclusive", "محكمة", "اختصاص حصري"],
        "b_types": {"arbitration", "dispute_resolution"},
        "b_signals": ["binding arbitration", "finally resolved by arbitration", "arbitration only", "arbitrage obligatoire", "تحكيم إلزامي", "يحل نهائياً بالتحكيم"],
        "message": {
            "en": "Court jurisdiction language may need to be reconciled with mandatory arbitration language.",
            "fr": "Les dispositions relatives à la compétence judiciaire peuvent nécessiter d'être conciliées avec les dispositions d'arbitrage obligatoire.",
            "ar": "قد تحتاج أحكام الاختصاص القضائي إلى التوفيق بينها وبين أحكام التحكيم الإلزامي.",
        },
    },
    {
        "id": "assignment_prohibited_vs_assignment_allowed",
        "label": {
            "en": "Assignment prohibited vs. allowed",
            "fr": "Cession interdite vs autorisée",
            "ar": "حظر التنازل مقابل السماح به",
        },
        "severity": "medium",
        "a_types": {"assignment"},
        "a_signals": ["may not assign", "no assignment", "without prior consent", "ne peut céder", "sans consentement préalable", "لا يجوز التنازل", "دون موافقة مسبقة"],
        "b_types": {"assignment"},
        "b_signals": ["may assign without consent", "freely assign", "cession sans consentement", "peut céder sans consentement", "يجوز التنازل دون موافقة"],
        "message": {
            "en": "Assignment restrictions and assignment permissions may be inconsistent or require clearer carve-outs.",
            "fr": "Les restrictions et les autorisations de cession peuvent être incohérentes ou nécessiter des exceptions plus claires.",
            "ar": "قد تكون قيود التنازل وأذوناته غير متسقة أو تحتاج إلى استثناءات أوضح.",
        },
    },
    {
        "id": "automatic_renewal_vs_no_renewal",
        "label": {
            "en": "Automatic renewal vs. no renewal",
            "fr": "Renouvellement automatique vs absence de renouvellement",
            "ar": "التجديد التلقائي مقابل عدم التجديد",
        },
        "severity": "medium",
        "a_types": {"automatic_renewal", "renewal"},
        "a_signals": ["automatically renew", "automatic renewal", "renouvellement automatique", "يتجدد تلقائيا", "تجديد تلقائي"],
        "b_types": {"term", "duration", "renewal"},
        "b_signals": ["expires automatically", "no renewal", "shall expire", "expire automatiquement", "sans renouvellement", "ينتهي تلقائيا", "دون تجديد"],
        "message": {
            "en": "Renewal language may conflict with expiration or non-renewal language.",
            "fr": "Les dispositions relatives au renouvellement peuvent entrer en conflit avec les dispositions d'expiration ou de non-renouvellement.",
            "ar": "قد تتعارض أحكام التجديد مع أحكام الانتهاء أو عدم التجديد.",
        },
    },
    {
        "id": "payment_advance_vs_payment_after_delivery",
        "label": {
            "en": "Advance payment vs. payment after delivery",
            "fr": "Paiement d'avance vs paiement après livraison",
            "ar": "الدفع المسبق مقابل الدفع بعد التسليم",
        },
        "severity": "medium",
        "a_types": {"payment", "fees", "invoice"},
        "a_signals": ["payment in advance", "pay in advance", "payable upfront", "paiement d'avance", "payable d'avance", "الدفع مقدما"],
        "b_types": {"payment", "fees", "invoice", "acceptance", "delivery"},
        "b_signals": ["payment after delivery", "payment upon acceptance", "payable after acceptance", "paiement après livraison", "paiement à l'acceptation", "الدفع بعد التسليم", "الدفع عند القبول"],
        "message": {
            "en": "Payment timing may be inconsistent between advance payment and payment after delivery or acceptance.",
            "fr": "Le calendrier de paiement peut être incohérent entre un paiement d'avance et un paiement après livraison ou acceptation.",
            "ar": "قد يكون توقيت الدفع غير متسق بين الدفع المسبق والدفع بعد التسليم أو القبول.",
        },
    },
    {
        "id": "warranty_vs_as_is_disclaimer",
        "label": {
            "en": "Warranty vs. \"as is\" disclaimer",
            "fr": "Garantie vs clause « tel quel »",
            "ar": "الضمان مقابل إخلاء المسؤولية \"كما هي\"",
        },
        "severity": "medium",
        "a_types": {"warranty"},
        "a_signals": ["warrants", "warranty", "represents and warrants", "garantit", "garantie", "يضمن", "ضمان"],
        "b_types": {"disclaimer"},
        "b_signals": ["as is", "no warranty", "without warranty", "tel quel", "sans garantie", "كما هي", "دون ضمان"],
        "message": {
            "en": "Warranty commitments may need to be reconciled with warranty disclaimer language.",
            "fr": "Les engagements de garantie peuvent nécessiter d'être conciliés avec les clauses d'exclusion de garantie.",
            "ar": "قد تحتاج التزامات الضمان إلى التوفيق بينها وبين أحكام إخلاء المسؤولية عن الضمان.",
        },
    },
    {
        "id": "data_delete_vs_data_retain",
        "label": {
            "en": "Data deletion vs. data retention",
            "fr": "Suppression des données vs conservation des données",
            "ar": "حذف البيانات مقابل الاحتفاظ بها",
        },
        "severity": "medium",
        "a_types": {"data_protection", "data_processing", "privacy"},
        "a_signals": ["delete", "destroy", "return or destroy", "effacer", "détruire", "supprimer", "حذف", "إتلاف", "إرجاع أو إتلاف"],
        "b_types": {"data_protection", "data_processing", "privacy", "confidentiality"},
        "b_signals": ["retain indefinitely", "retain for", "archival", "conserver indéfiniment", "conserver pendant", "احتفاظ", "يحتفظ إلى أجل غير مسمى"],
        "message": {
            "en": "Data return/deletion obligations may need to be reconciled with data retention language.",
            "fr": "Les obligations de restitution/suppression des données peuvent nécessiter d'être conciliées avec les dispositions de conservation des données.",
            "ar": "قد تحتاج التزامات إعادة/حذف البيانات إلى التوفيق بينها وبين أحكام الاحتفاظ بالبيانات.",
        },
    },
    {
        "id": "audit_rights_vs_no_audit",
        "label": {
            "en": "Audit rights vs. no audit",
            "fr": "Droit d'audit vs absence d'audit",
            "ar": "حق التدقيق مقابل غيابه",
        },
        "severity": "medium",
        "a_types": {"audit_rights", "compliance"},
        "a_signals": ["audit rights", "right to audit", "inspection rights", "droit d'audit", "droit d'inspection", "حق التدقيق", "حق التفتيش"],
        "b_types": {"audit_rights", "compliance"},
        "b_signals": ["no audit", "no inspection", "without audit rights", "aucun droit d'audit", "sans droit d'audit", "لا يوجد حق تدقيق"],
        "message": {
            "en": "Audit access provisions may conflict with language limiting or excluding audit rights.",
            "fr": "Les dispositions d'accès à l'audit peuvent entrer en conflit avec des dispositions limitant ou excluant le droit d'audit.",
            "ar": "قد تتعارض أحكام الوصول للتدقيق مع الأحكام التي تحد من حق التدقيق أو تستبعده.",
        },
    },
    {
        "id": "force_majeure_suspend_vs_terminate",
        "label": {
            "en": "Force majeure: suspend vs. terminate",
            "fr": "Force majeure : suspension vs résiliation",
            "ar": "القوة القاهرة: التعليق مقابل الإنهاء",
        },
        "severity": "low",
        "a_types": {"force_majeure"},
        "a_signals": ["suspend performance", "excused from performance", "suspension de l'exécution", "exonéré d'exécution", "تعليق الأداء", "الإعفاء من الأداء"],
        "b_types": {"force_majeure", "termination"},
        "b_signals": ["terminate for force majeure", "right to terminate", "résilier pour force majeure", "droit de résiliation", "إنهاء بسبب القوة القاهرة"],
        "message": {
            "en": "Force majeure provisions should clarify whether the remedy is suspension, termination, or both.",
            "fr": "Les dispositions de force majeure devraient préciser si le recours consiste en une suspension, une résiliation, ou les deux.",
            "ar": "ينبغي أن توضح أحكام القوة القاهرة ما إذا كان سبيل الانتصاف هو التعليق أو الإنهاء أو كليهما.",
        },
    },
]


def match_side(clauses: list[dict], types: set[str], signals: list[str]) -> list[dict]:
    """
    Require actual textual signal evidence, not clause type alone. Type
    overlap between a_types and b_types (e.g. both sides including
    "payment" or both being "confidentiality") previously let ANY two
    clauses of that shared type trigger a contradiction with zero textual
    evidence.
    """
    matches = []

    for clause in clauses:
        signal_match = bool(signals) and clause_has_signal(clause, signals)

        if not signal_match:
            continue

        matches.append(clause)

    return matches


def same_clause_only(a_matches: list[dict], b_matches: list[dict]) -> bool:
    if not a_matches or not b_matches:
        return False

    a_ids = {id(item) for item in a_matches}
    b_ids = {id(item) for item in b_matches}

    return bool(a_ids.intersection(b_ids)) and len(a_ids.union(b_ids)) == 1


def detect_contract_contradictions(clauses: list[dict], language: str = "en") -> list[dict]:
    """
    Detect potential cross-clause inconsistencies.

    Returns a list of dictionaries:
    {
        "id": str,        # stable technical identifier, never shown to the user
        "label": str,      # short translated title for display
        "severity": "low" | "medium" | "high",
        "message": str,    # translated explanatory sentence
        "clauses": [compact clause evidence]
    }
    """

    language = _lang(language)

    if not clauses:
        return []

    contradictions = []
    seen = set()

    for rule in CONTRADICTION_RULES:
        a_matches = match_side(
            clauses,
            set(rule.get("a_types", set())),
            list(rule.get("a_signals", [])),
        )

        b_matches = match_side(
            clauses,
            set(rule.get("b_types", set())),
            list(rule.get("b_signals", [])),
        )

        if not a_matches or not b_matches:
            continue

        # If the same clause contains both signals, it may be an exception/carve-out
        # rather than a contradiction. Keep only strong cases where at least two
        # distinct clauses are involved.
        if same_clause_only(a_matches, b_matches):
            continue

        evidence = []
        used_ids = set()

        for clause in a_matches[:2] + b_matches[:2]:
            marker = id(clause)
            if marker in used_ids:
                continue
            used_ids.add(marker)
            evidence.append(compact_clause(clause))

        key = (
            rule["id"],
            tuple(
                sorted(
                    f"{item.get('reference')}::{item.get('title')}"
                    for item in evidence
                )
            ),
        )

        if key in seen:
            continue

        seen.add(key)

        message_value = rule["message"]
        if isinstance(message_value, dict):
            message_value = message_value.get(language, message_value.get("en", ""))

        label_value = rule.get("label", {})
        if isinstance(label_value, dict):
            label_value = label_value.get(language, label_value.get("en", rule["id"]))
        else:
            label_value = rule["id"]

        contradictions.append({
            "id": rule["id"],
            "label": label_value,
            "severity": rule["severity"],
            "message": message_value,
            "clauses": evidence,
        })

    return contradictions