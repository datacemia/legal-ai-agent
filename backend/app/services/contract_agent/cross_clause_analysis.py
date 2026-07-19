"""
Universal cross-clause risk analyzer.

This module detects legal and commercial interactions between clauses
across an entire contract. It is designed to work across contract types,
industries, and languages (EN / FR / AR) without assuming a specific
jurisdiction or sector.

Important design principle:
- This module does not decide final legal risk by keywords alone.
- It identifies cross-clause issues that should be reviewed together.
- Final risk calibration should consider contract context, party roles,
  sector practice, carve-outs, exceptions, and negotiated balance.
"""

from __future__ import annotations

from typing import Any


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def normalize_language(language: str = "en") -> str:
    value = str(language or "en").lower().strip()
    return value if value in SUPPORTED_LANGUAGES else "en"


def normalize_text(value: Any) -> str:
    return " ".join(str(value or "").lower().strip().split())


def clause_text(clause: dict) -> str:
    return normalize_text(
        " ".join(
            [
                str(clause.get("title") or ""),
                str(clause.get("clause_title") or ""),
                str(clause.get("clause_type") or ""),
                str(clause.get("quoted_text") or ""),
                str(clause.get("original_text") or ""),
                str(clause.get("clause_text") or ""),
                str(clause.get("clause") or ""),
                str(clause.get("explanation_simple") or ""),
            ]
        )
    )


def clause_label(clause: dict) -> str:
    return str(
        clause.get("clause_reference")
        or clause.get("reference")
        or clause.get("title")
        or clause.get("clause_title")
        or ""
    ).strip()


def get_clause_type(clause: dict) -> str:
    return normalize_text(
        clause.get("clause_type")
        or clause.get("type")
        or "other"
    ).replace(" ", "_")


SIGNAL_SETS: dict[str, list[str]] = {
    "service_level": [
        "service level", "sla", "uptime", "availability", "downtime",
        "service credit", "niveau de service", "disponibilité",
        "crédit de service", "مستوى الخدمة", "التوافر", "تعويض الخدمة",
    ],
    "services": [
        "services", "service", "deliverables", "deliverable",
        "statement of work", "scope of work", "work product",
        "professional services", "implementation", "support",
        "maintenance", "delivery", "acceptance",
        "prestations", "prestation", "livrables", "livrable",
        "cahier des charges", "périmètre des travaux",
        "mise en œuvre", "support", "maintenance",
        "livraison", "acceptation",
        "الخدمات", "الخدمة", "المخرجات", "المخرج",
        "نطاق العمل", "بيان العمل", "الأعمال المهنية",
        "التنفيذ", "الدعم", "الصيانة", "التسليم", "القبول",
    ],
    "liability": [
        "liability", "limitation of liability", "liability cap",
        "indemnity", "indemnification", "responsabilité",
        "limitation de responsabilité", "plafond de responsabilité",
        "indemnisation", "المسؤولية", "حد المسؤولية", "تعويض",
    ],
    "termination": [
        "termination", "terminate", "expiration", "non-renewal",
        "résiliation", "expirer", "non-renouvellement",
        "إنهاء", "فسخ", "انتهاء", "عدم التجديد",
    ],
    "payment": [
        "payment", "fees", "invoice", "late payment", "outstanding fees",
        "paiement", "frais", "facture", "retard de paiement",
        "الدفع", "الرسوم", "فاتورة", "تأخر الدفع",
    ],
    "confidentiality": [
        "confidentiality", "confidential information", "trade secret",
        "confidentialité", "information confidentielle", "secret commercial",
        "السرية", "معلومات سرية", "سر تجاري",
    ],
    "data_protection": [
        "data protection", "personal data", "data processing", "privacy",
        "security incident", "protection des données", "données personnelles",
        "traitement des données", "vie privée", "incident de sécurité",
        "حماية البيانات", "البيانات الشخصية", "معالجة البيانات", "حادث أمني",
    ],
    "ip": [
        "intellectual property", "ip", "ownership", "assignment",
        "deliverables", "license", "propriété intellectuelle", "cession",
        "livrables", "licence", "الملكية الفكرية", "التنازل", "ترخيص",
    ],
    "restrictive_covenants": [
        "non-compete", "non compete", "non-solicitation", "non solicitation",
        "exclusivity", "exclusive dealing", "non-concurrence",
        "non-sollicitation", "exclusivité", "عدم المنافسة", "عدم الاستقطاب",
        "الحصرية",
    ],
    "dispute_resolution": [
        "governing law", "jurisdiction", "venue", "arbitration",
        "mediation", "court", "droit applicable", "juridiction",
        "arbitrage", "médiation", "tribunal", "القانون الواجب التطبيق",
        "الاختصاص", "تحكيم", "وساطة", "محكمة",
    ],
    "assignment": [
        "assignment", "assign", "transfer", "change of control",
        "cession", "transfert", "changement de contrôle",
        "التنازل", "نقل", "تغيير السيطرة",
    ],
    "renewal": [
        "renewal", "automatic renewal", "renew", "extension",
        "renouvellement", "renouvellement automatique", "prolongation",
        "تجديد", "تجديد تلقائي", "تمديد",
    ],
    "warranty": [
        "warranty", "warranties", "as is", "without warranty",
        "garantie", "sans garantie", "tel quel", "ضمان", "بدون ضمان",
    ],
    "audit": [
        "audit", "inspection", "audit rights", "droit d'audit",
        "inspection", "تدقيق", "تفتيش", "حق التدقيق",
    ],
    "insurance": [
        "insurance", "insured", "coverage", "assurance", "assuré",
        "couverture", "تأمين", "مؤمن", "تغطية",
    ],
}


TYPE_ALIASES: dict[str, set[str]] = {
    "service_level": {"service_level", "sla", "performance"},
    "services": {
        "services", "service", "statement_of_work", "scope_of_work",
        "deliverables", "deliverable", "delivery", "acceptance",
        "support", "maintenance", "implementation",
        "professional_services", "work_product", "change_request",
    },
    "liability": {"liability", "limitation_of_liability", "indemnity", "insurance"},
    "termination": {"termination", "termination_for_cause", "termination_for_convenience", "term", "duration", "default"},
    "payment": {"payment", "fees", "pricing", "invoice", "late_payment", "refund", "tax", "interest", "repayment"},
    "confidentiality": {"confidentiality"},
    "data_protection": {"data_protection", "data_processing", "privacy", "security", "cybersecurity"},
    "ip": {"intellectual_property", "ip_assignment", "ownership", "license", "work_product", "moral_rights"},
    "restrictive_covenants": {"restrictive_covenants", "non_compete", "non_solicitation", "exclusivity", "post_termination_obligations"},
    "dispute_resolution": {"governing_law", "jurisdiction", "venue", "arbitration", "mediation", "dispute_resolution"},
    "assignment": {"assignment", "change_of_control"},
    "renewal": {"renewal", "automatic_renewal"},
    "warranty": {"warranty", "disclaimer"},
    "audit": {"audit", "audit_rights"},
    "insurance": {"insurance"},
}


def clause_has_domain(clause: dict, domain: str) -> bool:
    ctype = get_clause_type(clause)

    if ctype in TYPE_ALIASES.get(domain, set()):
        return True

    text = clause_text(clause)
    return any(signal in text for signal in SIGNAL_SETS.get(domain, []))


def find_clauses(clauses: list[dict], domain: str) -> list[dict]:
    return [clause for clause in clauses if clause_has_domain(clause, domain)]


def compact_clause_refs(items: list[dict], limit: int = 3) -> list[str]:
    refs = []
    seen = set()

    for item in items:
        ref = clause_label(item)
        if not ref:
            continue
        key = ref.lower()
        if key in seen:
            continue
        seen.add(key)
        refs.append(ref)
        if len(refs) >= limit:
            break

    return refs


MESSAGES: dict[str, dict[str, str]] = {
    "service_level_liability": {
        "en": "Service commitments should be reviewed together with liability caps and remedies to confirm whether service credits are the only remedy or whether material failures have additional consequences.",
        "fr": "Les engagements de niveau de service doivent être examinés avec les plafonds de responsabilité et les recours afin de vérifier si les crédits de service constituent le seul recours ou si les manquements importants ont d'autres conséquences.",
        "ar": "ينبغي مراجعة التزامات مستوى الخدمة مع حدود المسؤولية ووسائل الانتصاف للتأكد مما إذا كانت تعويضات الخدمة هي الوسيلة الوحيدة أو إذا كانت الإخفاقات الجوهرية تؤدي إلى آثار إضافية.",
    },
    "termination_payment": {
        "en": "Termination rights should be checked against payment provisions to confirm treatment of accrued fees, refunds, suspension rights, and unpaid amounts after termination.",
        "fr": "Les droits de résiliation doivent être vérifiés avec les clauses de paiement afin de confirmer le traitement des frais acquis, remboursements, droits de suspension et montants impayés après résiliation.",
        "ar": "ينبغي مقارنة حقوق الإنهاء مع أحكام الدفع لتحديد مصير الرسوم المستحقة، والمبالغ القابلة للاسترداد، وحقوق التعليق، والمبالغ غير المدفوعة بعد الإنهاء.",
    },
    "confidentiality_data": {
        "en": "Confidentiality obligations should align with data protection provisions, especially for personal data, security incidents, return or deletion duties, and survival periods.",
        "fr": "Les obligations de confidentialité doivent être cohérentes avec les clauses de protection des données, notamment pour les données personnelles, incidents de sécurité, obligations de restitution ou suppression et durées de survie.",
        "ar": "يجب أن تكون التزامات السرية متسقة مع أحكام حماية البيانات، خصوصاً بالنسبة للبيانات الشخصية، والحوادث الأمنية، وواجبات الإرجاع أو الحذف، ومدد البقاء بعد انتهاء العقد.",
    },
    "ip_services": {
        "en": "Service and deliverable obligations should be reviewed together with intellectual property ownership to confirm who owns outputs, pre-existing materials, configurations, and derivative work.",
        "fr": "Les obligations de services et de livrables doivent être examinées avec les clauses de propriété intellectuelle afin de confirmer qui détient les résultats, éléments préexistants, configurations et œuvres dérivées.",
        "ar": "ينبغي مراجعة التزامات الخدمات والمخرجات مع أحكام الملكية الفكرية لتحديد مالك النتائج والمواد السابقة والإعدادات والأعمال المشتقة.",
    },
    "restrictive_termination": {
        "en": "Post-termination restrictions should be reviewed with the term and termination clauses to confirm duration, scope, trigger date, and proportionality after the relationship ends.",
        "fr": "Les restrictions post-contractuelles doivent être examinées avec les clauses de durée et de résiliation afin de confirmer la durée, le périmètre, le point de départ et la proportionnalité après la fin de la relation.",
        "ar": "ينبغي مراجعة القيود اللاحقة للانتهاء مع أحكام مدة العقد والإنهاء لتحديد المدة والنطاق وتاريخ بدء السريان والتناسب بعد انتهاء العلاقة.",
    },
    "renewal_termination": {
        "en": "Renewal mechanics should be reviewed with termination and non-renewal rights to ensure notice periods, renewal dates, and exit rights are consistent.",
        "fr": "Les mécanismes de renouvellement doivent être examinés avec les droits de résiliation et de non-renouvellement afin de vérifier la cohérence des préavis, dates de renouvellement et droits de sortie.",
        "ar": "ينبغي مراجعة آليات التجديد مع حقوق الإنهاء وعدم التجديد للتأكد من اتساق آجال الإشعار وتواريخ التجديد وحقوق الخروج.",
    },
    "dispute_liability": {
        "en": "Dispute resolution should be reviewed with liability and indemnity provisions to understand forum, cost allocation, available remedies, confidentiality, and enforcement consequences.",
        "fr": "Le règlement des litiges doit être examiné avec les clauses de responsabilité et d'indemnisation afin de comprendre le forum, la répartition des coûts, les recours disponibles, la confidentialité et les conséquences d'exécution.",
        "ar": "ينبغي مراجعة تسوية النزاعات مع أحكام المسؤولية والتعويض لفهم جهة الفصل، وتوزيع التكاليف، ووسائل الانتصاف المتاحة، والسرية، وآثار التنفيذ.",
    },
    "assignment_ip_data": {
        "en": "Assignment or change-of-control rights should be reviewed with IP, confidentiality, and data protection obligations because transfers may affect control over assets, confidential information, and personal data.",
        "fr": "Les droits de cession ou de changement de contrôle doivent être examinés avec les obligations de propriété intellectuelle, confidentialité et protection des données, car les transferts peuvent affecter le contrôle des actifs, informations confidentielles et données personnelles.",
        "ar": "ينبغي مراجعة حقوق التنازل أو تغيير السيطرة مع التزامات الملكية الفكرية والسرية وحماية البيانات، لأن عمليات النقل قد تؤثر على التحكم في الأصول والمعلومات السرية والبيانات الشخصية.",
    },
    "warranty_liability": {
        "en": "Warranty language should be reviewed with liability limitations and disclaimers to confirm whether remedies for defective performance are meaningful or heavily restricted.",
        "fr": "Les garanties doivent être examinées avec les limitations et exclusions de responsabilité afin de vérifier si les recours en cas de mauvaise exécution sont effectifs ou fortement limités.",
        "ar": "ينبغي مراجعة الضمانات مع حدود وإخلاءات المسؤولية للتأكد مما إذا كانت وسائل الانتصاف عند سوء الأداء فعالة أو مقيدة بشدة.",
    },
    "audit_data_security": {
        "en": "Audit rights should be reviewed with data protection and security obligations to confirm whether compliance can be verified in practice.",
        "fr": "Les droits d'audit doivent être examinés avec les obligations de protection des données et de sécurité afin de vérifier si la conformité peut être contrôlée en pratique.",
        "ar": "ينبغي مراجعة حقوق التدقيق مع التزامات حماية البيانات والأمن للتأكد مما إذا كان يمكن التحقق من الامتثال عملياً.",
    },
    "insurance_liability": {
        "en": "Insurance obligations should be reviewed with liability caps and indemnities to confirm whether insurance coverage supports the allocated contractual risk.",
        "fr": "Les obligations d'assurance doivent être examinées avec les plafonds de responsabilité et les indemnisations afin de vérifier si la couverture soutient correctement la répartition contractuelle des risques.",
        "ar": "ينبغي مراجعة التزامات التأمين مع حدود المسؤولية والتعويضات للتأكد من أن التغطية التأمينية تدعم توزيع المخاطر التعاقدية.",
    },
}


RULES: list[dict[str, Any]] = [
    {
        "id": "service_level_liability",
        "domains": ["service_level", "liability"],
        "severity": "medium",
    },
    {
        "id": "termination_payment",
        "domains": ["termination", "payment"],
        "severity": "medium",
    },
    {
        "id": "confidentiality_data",
        "domains": ["confidentiality", "data_protection"],
        "severity": "medium",
    },
    {
        "id": "ip_services",
        "domains": ["ip", "services"],
        "severity": "medium",
    },
    {
        "id": "restrictive_termination",
        "domains": ["restrictive_covenants", "termination"],
        "severity": "medium",
    },
    {
        "id": "renewal_termination",
        "domains": ["renewal", "termination"],
        "severity": "medium",
    },
    {
        "id": "dispute_liability",
        "domains": ["dispute_resolution", "liability"],
        "severity": "low",
    },
    {
        "id": "assignment_ip_data",
        "domains": ["assignment", "ip", "data_protection"],
        "severity": "medium",
    },
    {
        "id": "warranty_liability",
        "domains": ["warranty", "liability"],
        "severity": "medium",
    },
    {
        "id": "audit_data_security",
        "domains": ["audit", "data_protection"],
        "severity": "low",
    },
    {
        "id": "insurance_liability",
        "domains": ["insurance", "liability"],
        "severity": "low",
    },
]


def build_issue(
    rule: dict,
    matched: dict[str, list[dict]],
    language: str,
) -> dict:
    rule_id = rule["id"]
    message = MESSAGES.get(rule_id, {}).get(
        language,
        MESSAGES.get(rule_id, {}).get("en", "Related clauses should be reviewed together."),
    )

    clause_refs = []
    related_domains = {}

    for domain, items in matched.items():
        refs = compact_clause_refs(items)
        related_domains[domain] = refs
        clause_refs.extend(refs)

    # preserve order while deduplicating
    seen = set()
    deduped_refs = []
    for ref in clause_refs:
        key = ref.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped_refs.append(ref)

    return {
        "id": rule_id,
        "severity": rule.get("severity", "medium"),
        "message": message,
        "domains": list(matched.keys()),
        "clauses": deduped_refs,
        "related_domains": related_domains,
    }


def analyze_cross_clause_risks(
    clauses: list[dict],
    language: str = "en",
) -> list[dict]:
    """
    Detect cross-clause legal/commercial issues.

    Returns a list of structured review points. These are not automatic
    contradictions and should not be treated as High Risk by themselves.
    """

    language = normalize_language(language)

    if not clauses:
        return []

    issues = []
    seen = set()

    for rule in RULES:
        matched: dict[str, list[dict]] = {}

        for domain in rule.get("domains", []):
            domain_clauses = find_clauses(clauses, domain)

            if not domain_clauses:
                matched = {}
                break

            matched[domain] = domain_clauses

        if not matched:
            continue

        issue_id = rule.get("id", "")
        if issue_id in seen:
            continue

        seen.add(issue_id)
        issues.append(
            build_issue(
                rule=rule,
                matched=matched,
                language=language,
            )
        )

    return issues
