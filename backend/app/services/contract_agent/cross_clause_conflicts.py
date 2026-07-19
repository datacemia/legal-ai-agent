"""
Universal cross-clause conflict detector for Runexa Legal Agent.

Design goals:
- Standard international logic, not jurisdiction-specific.
- Works across contract families: SaaS, cybersecurity, employment,
  procurement, licensing, lending, real estate, distribution, corporate,
  insurance, construction, healthcare, energy, NDA, MSA, etc.
- Multilingual signal support: EN / FR / AR.
- Prefer clause_type / primary_type metadata when available.
- Fall back to multilingual text signals when metadata is absent.
- Return structured conflicts with clause references for frontend display.

This module intentionally detects possible inconsistencies only.
It should not replace legal reasoning. It flags items for review.
"""

from __future__ import annotations

import re
from typing import Any


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


LOCALIZED_MESSAGES = {
    "en": {
        "liability_cap_vs_uncapped": "The agreement may contain inconsistent liability language: one provision limits liability while another appears to create uncapped or unlimited exposure.",
        "termination_notice_conflict": "The agreement may contain inconsistent termination notice language: one provision requires notice while another appears to allow termination without notice.",
        "governing_law_conflict": "The agreement may reference multiple governing laws, courts, seats, or venues that should be reconciled.",
        "payment_deadline_conflict": "The agreement may contain inconsistent payment deadlines or timing obligations.",
        "confidentiality_duration_conflict": "The agreement may contain inconsistent confidentiality survival periods, such as fixed-term and indefinite obligations.",
        "exclusive_vs_nonexclusive": "The agreement may contain inconsistent exclusivity language, including both exclusive and non-exclusive rights.",
        "ip_ownership_conflict": "The agreement may contain inconsistent intellectual property ownership or assignment language.",
        "assignment_conflict": "The agreement may contain inconsistent assignment rights, such as a consent requirement and a unilateral assignment permission.",
        "renewal_conflict": "The agreement may contain inconsistent renewal or expiration mechanics.",
        "audit_conflict": "The agreement may contain inconsistent audit or inspection rights.",
        "data_return_retention_conflict": "The agreement may contain inconsistent data return, destruction, or retention obligations.",
        "warranty_disclaimer_conflict": "The agreement may contain both affirmative warranty language and broad disclaimer language that should be reconciled.",
        "service_level_remedy_conflict": "Service-level remedies should be checked against liability limits and any exclusive-remedy language.",
        "priority_of_terms_conflict": "The agreement may contain inconsistent order-of-precedence or priority-of-terms language.",
    },
    "fr": {
        "liability_cap_vs_uncapped": "Le contrat peut contenir une incohérence sur la responsabilité : une clause limite la responsabilité tandis qu'une autre semble créer une exposition non plafonnée ou illimitée.",
        "termination_notice_conflict": "Le contrat peut contenir une incohérence sur le préavis de résiliation : une clause exige un préavis tandis qu'une autre semble permettre une résiliation sans préavis.",
        "governing_law_conflict": "Le contrat peut mentionner plusieurs droits applicables, tribunaux, sièges ou lieux de règlement des litiges qui doivent être harmonisés.",
        "payment_deadline_conflict": "Le contrat peut contenir des délais de paiement ou obligations de calendrier incohérents.",
        "confidentiality_duration_conflict": "Le contrat peut contenir des durées de confidentialité incohérentes, par exemple des obligations à durée fixe et des obligations indéfinies.",
        "exclusive_vs_nonexclusive": "Le contrat peut contenir une incohérence sur l'exclusivité, avec des droits à la fois exclusifs et non exclusifs.",
        "ip_ownership_conflict": "Le contrat peut contenir une incohérence sur la propriété intellectuelle, la titularité ou la cession des droits.",
        "assignment_conflict": "Le contrat peut contenir des droits de cession incohérents, par exemple une exigence de consentement et une autorisation unilatérale de cession.",
        "renewal_conflict": "Le contrat peut contenir des mécanismes incohérents de renouvellement ou d'expiration.",
        "audit_conflict": "Le contrat peut contenir des droits d'audit ou d'inspection incohérents.",
        "data_return_retention_conflict": "Le contrat peut contenir des obligations incohérentes de restitution, destruction ou conservation des données.",
        "warranty_disclaimer_conflict": "Le contrat peut contenir à la fois des garanties affirmatives et des exclusions générales de garantie qui doivent être harmonisées.",
        "service_level_remedy_conflict": "Les recours liés aux niveaux de service doivent être vérifiés au regard des plafonds de responsabilité et de toute clause de recours exclusif.",
        "priority_of_terms_conflict": "Le contrat peut contenir des règles incohérentes de priorité ou d'ordre de prévalence des documents.",
    },
    "ar": {
        "liability_cap_vs_uncapped": "قد يتضمن العقد صياغة غير متسقة بشأن المسؤولية: فهناك حكم يحد المسؤولية بينما يبدو حكم آخر أنه ينشئ تعرضًا غير محدود أو غير مقيد.",
        "termination_notice_conflict": "قد يتضمن العقد صياغة غير متسقة بشأن إشعار الإنهاء: فهناك حكم يتطلب إشعارًا بينما يبدو حكم آخر أنه يسمح بالإنهاء دون إشعار.",
        "governing_law_conflict": "قد يشير العقد إلى أكثر من قانون واجب التطبيق أو محكمة أو مقر أو مكان لتسوية النزاعات، ويجب التوفيق بينها.",
        "payment_deadline_conflict": "قد يتضمن العقد مواعيد دفع أو التزامات زمنية غير متسقة.",
        "confidentiality_duration_conflict": "قد يتضمن العقد مددًا غير متسقة لالتزامات السرية، مثل التزامات محددة المدة وأخرى غير محددة المدة.",
        "exclusive_vs_nonexclusive": "قد يتضمن العقد صياغة غير متسقة بشأن الحصرية، بما في ذلك حقوق حصرية وغير حصرية في الوقت نفسه.",
        "ip_ownership_conflict": "قد يتضمن العقد صياغة غير متسقة بشأن ملكية حقوق الملكية الفكرية أو التنازل عنها.",
        "assignment_conflict": "قد يتضمن العقد حقوق تنازل غير متسقة، مثل اشتراط الموافقة وفي الوقت نفسه السماح بالتنازل من طرف واحد.",
        "renewal_conflict": "قد يتضمن العقد آليات غير متسقة بشأن التجديد أو انتهاء المدة.",
        "audit_conflict": "قد يتضمن العقد حقوق تدقيق أو تفتيش غير متسقة.",
        "data_return_retention_conflict": "قد يتضمن العقد التزامات غير متسقة بشأن إرجاع البيانات أو إتلافها أو الاحتفاظ بها.",
        "warranty_disclaimer_conflict": "قد يتضمن العقد ضمانات صريحة وفي الوقت نفسه استثناءات عامة من الضمان يجب التوفيق بينها.",
        "service_level_remedy_conflict": "يجب مقارنة وسائل الانتصاف الخاصة بمستوى الخدمة مع حدود المسؤولية وأي صياغة تجعلها وسيلة الانتصاف الحصرية.",
        "priority_of_terms_conflict": "قد يتضمن العقد قواعد غير متسقة بشأن أولوية المستندات أو ترتيب سريان الشروط.",
    },
}


SIGNALS = {
    "liability_cap": [
        "liability cap", "cap on liability", "limitation of liability", "limited liability", "shall not exceed", "aggregate liability",
        "plafond de responsabilité", "limitation de responsabilité", "responsabilité limitée", "ne saurait excéder",
        "حد المسؤولية", "تحديد المسؤولية", "لا تتجاوز المسؤولية",
    ],
    "uncapped_liability": [
        "unlimited liability", "liability without limitation", "uncapped liability", "not subject to the limitation", "shall not apply to",
        "responsabilité illimitée", "sans limitation de responsabilité", "non soumise à la limitation",
        "مسؤولية غير محدودة", "دون حد للمسؤولية", "لا يخضع لحد المسؤولية",
    ],
    "notice_required": [
        "notice period", "prior written notice", "written notice", "days' notice", "non-renewal notice",
        "préavis", "notification écrite préalable", "avis écrit", "jours de préavis",
        "إشعار", "إخطار خطي", "إشعار مسبق", "مهلة إشعار",
    ],
    "without_notice": [
        "without notice", "without prior notice", "immediate termination", "terminate immediately",
        "sans préavis", "sans notification préalable", "résiliation immédiate",
        "دون إشعار", "دون إخطار", "إنهاء فوري",
    ],
    "governing_law": [
        "governing law", "laws of", "law of", "droit applicable", "lois de", "القانون الواجب التطبيق", "قوانين",
    ],
    "jurisdiction_venue": [
        "courts of", "exclusive jurisdiction", "venue", "seat of arbitration", "tribunal", "juridiction", "siège de l'arbitrage", "محكمة", "اختصاص", "مقر التحكيم",
    ],
    "payment_timing": [
        "days of invoice", "days after invoice", "payment due", "payable within", "net ",
        "jours suivant la facture", "payable dans", "échéance de paiement",
        "يوماً من الفاتورة", "مستحق خلال", "موعد الدفع",
    ],
    "fixed_confidentiality": [
        "one year", "two years", "three years", "five years", "for a period of", "months after", "years after",
        "un an", "deux ans", "trois ans", "cinq ans", "pour une période de",
        "سنة", "سنتين", "ثلاث سنوات", "خمس سنوات", "لمدة",
    ],
    "indefinite_confidentiality": [
        "indefinitely", "perpetual", "trade secrets", "as long as permitted", "survive indefinitely",
        "indéfiniment", "perpétuel", "secrets commerciaux", "aussi longtemps que permis",
        "غير محددة", "دائمة", "أسرار تجارية", "طالما يسمح القانون",
    ],
    "exclusive": [
        "exclusive", "exclusivity", "sole provider", "sole supplier",
        "exclusif", "exclusivité", "fournisseur unique",
        "حصري", "حصرية", "مزود وحيد",
    ],
    "non_exclusive": [
        "non-exclusive", "non exclusive", "not exclusive",
        "non exclusif", "non-exclusive", "غير حصري", "ليست حصرية",
    ],
    "ip_provider_owned": [
        "provider retains", "supplier retains", "vendor retains", "pre-existing intellectual property", "background ip", "underlying software",
        "le prestataire conserve", "le fournisseur conserve", "propriété intellectuelle préexistante", "logiciel sous-jacent",
        "يحتفظ مقدم الخدمة", "يحتفظ المورد", "الملكية الفكرية السابقة", "البرنامج الأساسي",
    ],
    "ip_client_owned_all": [
        "client owns all", "customer owns all", "assigned to client", "vest in client", "all intellectual property shall belong to client",
        "le client détient tous", "cédés au client", "appartiennent au client",
        "يمتلك العميل جميع", "يتنازل عنها للعميل", "تؤول إلى العميل",
    ],
    "assignment_consent_required": [
        "may not assign without", "prior written consent", "consent of the other party", "shall not assign",
        "ne peut céder sans", "consentement écrit préalable", "ne peut pas céder",
        "لا يجوز التنازل دون", "موافقة خطية مسبقة", "لا يجوز أن يتنازل",
    ],
    "assignment_allowed_unilateral": [
        "may assign without consent", "assign without consent", "freely assign", "without the consent",
        "peut céder sans consentement", "cession sans consentement", "librement céder",
        "يجوز التنازل دون موافقة", "التنازل بحرية",
    ],
    "automatic_renewal": [
        "automatically renew", "automatic renewal", "renews automatically",
        "renouvellement automatique", "se renouvelle automatiquement",
        "يتجدد تلقائيا", "تجديد تلقائي",
    ],
    "expires_no_renewal": [
        "expires automatically", "shall expire", "no renewal", "non-renewable",
        "expire automatiquement", "prend fin", "non renouvelable",
        "ينتهي تلقائيا", "غير قابل للتجديد", "ينتهي دون تجديد",
    ],
    "audit_rights": [
        "audit", "inspection", "inspect records", "audit rights",
        "audit", "inspection", "droit d'audit", "vérification",
        "تدقيق", "تفتيش", "حق التدقيق",
    ],
    "no_audit": [
        "no audit", "not subject to audit", "no inspection rights",
        "aucun audit", "pas de droit d'audit", "non soumis à audit",
        "لا تدقيق", "لا يخضع للتدقيق", "لا حق في التفتيش",
    ],
    "data_return_destroy": [
        "return or destroy", "delete all", "destroy all", "return all data", "deletion of data",
        "restituer ou détruire", "supprimer toutes", "détruire toutes", "restitution des données",
        "إرجاع أو إتلاف", "حذف جميع", "إتلاف جميع", "إرجاع البيانات",
    ],
    "data_retain": [
        "retain", "retention", "keep copies", "archive copies", "backup copies",
        "conserver", "conservation", "copies d'archive", "copies de sauvegarde",
        "يحتفظ", "الاحتفاظ", "نسخ احتياطية", "نسخ أرشيفية",
    ],
    "warranty_affirmative": [
        "represents and warrants", "warrants that", "shall warrant", "guarantees",
        "déclare et garantit", "garantit que", "garantie",
        "يقر ويضمن", "يضمن أن", "ضمان",
    ],
    "warranty_disclaimer": [
        "as is", "no warranty", "without warranty", "disclaims all warranties",
        "tel quel", "sans garantie", "exclut toute garantie",
        "كما هو", "بدون ضمان", "إخلاء جميع الضمانات",
    ],
    "service_level": [
        "service level", "sla", "uptime", "availability", "service credit",
        "niveau de service", "disponibilité", "crédit de service",
        "مستوى الخدمة", "التوافر", "تعويض الخدمة",
    ],
    "exclusive_remedy": [
        "sole and exclusive remedy", "exclusive remedy", "sole remedy",
        "recours exclusif", "seul recours", "recours unique",
        "وسيلة الانتصاف الوحيدة", "الجزاء الحصري",
    ],
    "priority_terms": [
        "order of precedence", "prevails over", "takes precedence", "priority of documents",
        "ordre de priorité", "prévaut sur", "priorité des documents",
        "ترتيب الأولوية", "يسود على", "أولوية المستندات",
    ],
}


JURISDICTION_TERMS = [
    "france", "french law", "paris", "morocco", "maroc", "casablanca",
    "new york", "delaware", "california", "england", "english law",
    "switzerland", "geneva", "uae", "dubai", "abu dhabi",
    "فرنسا", "المغرب", "الدار البيضاء", "نيويورك", "إنجلترا", "سويسرا", "جنيف", "الإمارات", "دبي",
]


PAYMENT_DAY_PATTERN = re.compile(
    r"\b(\d{1,3})\s*(?:days?|jours?|يوم|يوماً)\b",
    flags=re.IGNORECASE,
)


def normalize_language(language: str = "en") -> str:
    language = str(language or "en").lower()
    return language if language in SUPPORTED_LANGUAGES else "en"


def safe_text(value: Any) -> str:
    return str(value or "").strip()


def get_clause_text(clause: dict) -> str:
    return " ".join([
        safe_text(clause.get("clause_title") or clause.get("title")),
        safe_text(clause.get("clause_reference") or clause.get("reference")),
        safe_text(clause.get("quoted_text")),
        safe_text(clause.get("original_text")),
        safe_text(clause.get("clause_text")),
        safe_text(clause.get("explanation_simple")),
    ]).lower()


def get_clause_type(clause: dict) -> str:
    return safe_text(
        clause.get("clause_type")
        or clause.get("primary_type")
        or clause.get("type")
    ).lower()


def clause_ref(clause: dict) -> dict:
    return {
        "title": safe_text(clause.get("clause_title") or clause.get("title")),
        "reference": safe_text(clause.get("clause_reference") or clause.get("reference")),
        "clause_type": get_clause_type(clause),
    }


def has_signal(text: str, signal_name: str) -> bool:
    return any(
        signal.lower() in text
        for signal in SIGNALS.get(signal_name, [])
    )


def clause_has(clause: dict, signal_name: str, types: set[str] | None = None) -> bool:
    text = get_clause_text(clause)
    ctype = get_clause_type(clause)
    return has_signal(text, signal_name) or (types is not None and ctype in types)


def find_clauses(clauses: list[dict], signal_name: str, types: set[str] | None = None) -> list[dict]:
    return [
        clause
        for clause in clauses
        if clause_has(clause, signal_name, types)
    ]


def add_conflict(
    conflicts: list[dict],
    *,
    conflict_type: str,
    severity: str,
    message_key: str,
    language: str,
    clauses_a: list[dict],
    clauses_b: list[dict],
) -> None:
    if not clauses_a or not clauses_b:
        return

    if {id(c) for c in clauses_a} == {id(c) for c in clauses_b}:
        return

    conflicts.append({
        "type": conflict_type,
        "severity": severity,
        "message": LOCALIZED_MESSAGES[language][message_key],
        "clauses": {
            "a": [clause_ref(c) for c in clauses_a[:5]],
            "b": [clause_ref(c) for c in clauses_b[:5]],
        },
    })


def extract_payment_days(clauses: list[dict]) -> dict[int, list[dict]]:
    found: dict[int, list[dict]] = {}

    for clause in clauses:
        if not clause_has(clause, "payment_timing", {"payment", "invoice", "fees", "pricing", "late_payment"}):
            continue

        text = get_clause_text(clause)

        for match in PAYMENT_DAY_PATTERN.findall(text):
            try:
                days = int(match)
            except ValueError:
                continue

            found.setdefault(days, []).append(clause)

    return found


def extract_jurisdictions(clauses: list[dict]) -> dict[str, list[dict]]:
    found: dict[str, list[dict]] = {}

    for clause in clauses:
        if not clause_has(clause, "governing_law", {"governing_law", "jurisdiction", "venue", "arbitration", "dispute_resolution"}):
            continue

        text = get_clause_text(clause)

        for term in JURISDICTION_TERMS:
            if term in text:
                found.setdefault(term, []).append(clause)

    return found


def detect_cross_clause_conflicts(
    clauses: list[dict],
    language: str = "en",
) -> list[dict]:
    """
    Detect possible conflicts across clauses.

    Returns structured objects:
    {
      "type": str,
      "severity": "low" | "medium" | "high",
      "message": localized message,
      "clauses": {"a": [...], "b": [...]}
    }
    """

    language = normalize_language(language)
    conflicts: list[dict] = []

    if not clauses:
        return conflicts

    capped = find_clauses(clauses, "liability_cap", {"limitation_of_liability", "liability"})
    uncapped = find_clauses(clauses, "uncapped_liability", {"liability", "indemnity"})
    add_conflict(
        conflicts,
        conflict_type="liability_cap_vs_uncapped",
        severity="high",
        message_key="liability_cap_vs_uncapped",
        language=language,
        clauses_a=capped,
        clauses_b=uncapped,
    )

    notice_required = find_clauses(clauses, "notice_required", {"notice", "termination", "termination_for_cause", "termination_for_convenience"})
    without_notice = find_clauses(clauses, "without_notice", {"termination", "termination_for_cause", "termination_for_convenience"})
    add_conflict(
        conflicts,
        conflict_type="termination_notice_conflict",
        severity="medium",
        message_key="termination_notice_conflict",
        language=language,
        clauses_a=notice_required,
        clauses_b=without_notice,
    )

    exclusive = find_clauses(clauses, "exclusive", {"exclusivity"})
    non_exclusive = find_clauses(clauses, "non_exclusive", {"license", "exclusivity"})
    add_conflict(
        conflicts,
        conflict_type="exclusive_vs_nonexclusive",
        severity="high",
        message_key="exclusive_vs_nonexclusive",
        language=language,
        clauses_a=exclusive,
        clauses_b=non_exclusive,
    )

    provider_ip = find_clauses(clauses, "ip_provider_owned", {"intellectual_property", "ownership"})
    client_ip = find_clauses(clauses, "ip_client_owned_all", {"ip_assignment", "work_product", "ownership"})
    add_conflict(
        conflicts,
        conflict_type="ip_ownership_conflict",
        severity="medium",
        message_key="ip_ownership_conflict",
        language=language,
        clauses_a=provider_ip,
        clauses_b=client_ip,
    )

    consent_assignment = find_clauses(clauses, "assignment_consent_required", {"assignment"})
    unilateral_assignment = find_clauses(clauses, "assignment_allowed_unilateral", {"assignment"})
    add_conflict(
        conflicts,
        conflict_type="assignment_conflict",
        severity="medium",
        message_key="assignment_conflict",
        language=language,
        clauses_a=consent_assignment,
        clauses_b=unilateral_assignment,
    )

    auto_renewal = find_clauses(clauses, "automatic_renewal", {"automatic_renewal", "renewal"})
    expires_no_renewal = find_clauses(clauses, "expires_no_renewal", {"term", "duration", "renewal"})
    add_conflict(
        conflicts,
        conflict_type="renewal_conflict",
        severity="medium",
        message_key="renewal_conflict",
        language=language,
        clauses_a=auto_renewal,
        clauses_b=expires_no_renewal,
    )

    fixed_conf = find_clauses(clauses, "fixed_confidentiality", {"confidentiality"})
    indefinite_conf = find_clauses(clauses, "indefinite_confidentiality", {"confidentiality"})
    add_conflict(
        conflicts,
        conflict_type="confidentiality_duration_conflict",
        severity="medium",
        message_key="confidentiality_duration_conflict",
        language=language,
        clauses_a=fixed_conf,
        clauses_b=indefinite_conf,
    )

    audit_rights = find_clauses(clauses, "audit_rights", {"audit_rights"})
    no_audit = find_clauses(clauses, "no_audit", {"audit_rights"})
    add_conflict(
        conflicts,
        conflict_type="audit_conflict",
        severity="medium",
        message_key="audit_conflict",
        language=language,
        clauses_a=audit_rights,
        clauses_b=no_audit,
    )

    data_return = find_clauses(clauses, "data_return_destroy", {"data_processing", "data_protection", "privacy"})
    data_retain = find_clauses(clauses, "data_retain", {"data_processing", "data_protection", "privacy"})
    add_conflict(
        conflicts,
        conflict_type="data_return_retention_conflict",
        severity="medium",
        message_key="data_return_retention_conflict",
        language=language,
        clauses_a=data_return,
        clauses_b=data_retain,
    )

    warranty_yes = find_clauses(clauses, "warranty_affirmative", {"warranty"})
    warranty_no = find_clauses(clauses, "warranty_disclaimer", {"disclaimer", "warranty"})
    add_conflict(
        conflicts,
        conflict_type="warranty_disclaimer_conflict",
        severity="medium",
        message_key="warranty_disclaimer_conflict",
        language=language,
        clauses_a=warranty_yes,
        clauses_b=warranty_no,
    )

    service_level = find_clauses(clauses, "service_level", {"sla", "service_level"})
    exclusive_remedy = find_clauses(clauses, "exclusive_remedy", {"remedies", "sla", "service_level"})
    liability_cap = find_clauses(clauses, "liability_cap", {"limitation_of_liability", "liability"})

    if service_level and (exclusive_remedy or liability_cap):
        add_conflict(
            conflicts,
            conflict_type="service_level_remedy_conflict",
            severity="medium",
            message_key="service_level_remedy_conflict",
            language=language,
            clauses_a=service_level,
            clauses_b=(exclusive_remedy or liability_cap),
        )

    priority_terms = find_clauses(clauses, "priority_terms", {"general_provisions", "administrative"})
    if len(priority_terms) >= 2:
        conflicts.append({
            "type": "priority_of_terms_conflict",
            "severity": "medium",
            "message": LOCALIZED_MESSAGES[language]["priority_of_terms_conflict"],
            "clauses": {
                "a": [clause_ref(priority_terms[0])],
                "b": [clause_ref(c) for c in priority_terms[1:5]],
            },
        })

    jurisdictions = extract_jurisdictions(clauses)
    if len(jurisdictions) >= 2:
        items = list(jurisdictions.items())
        conflicts.append({
            "type": "governing_law_conflict",
            "severity": "high",
            "message": LOCALIZED_MESSAGES[language]["governing_law_conflict"],
            "clauses": {
                "a": [clause_ref(c) for c in items[0][1][:5]],
                "b": [clause_ref(c) for _, found in items[1:4] for c in found[:2]],
            },
            "detected_terms": [term for term, _ in items[:6]],
        })

    payment_days = extract_payment_days(clauses)
    distinct_days = sorted(payment_days)
    if len(distinct_days) >= 2:
        first = distinct_days[0]
        last = distinct_days[-1]

        if abs(last - first) >= 10:
            conflicts.append({
                "type": "payment_deadline_conflict",
                "severity": "medium",
                "message": LOCALIZED_MESSAGES[language]["payment_deadline_conflict"],
                "clauses": {
                    "a": [clause_ref(c) for c in payment_days[first][:5]],
                    "b": [clause_ref(c) for c in payment_days[last][:5]],
                },
                "detected_deadlines": distinct_days,
            })

    return dedupe_conflicts(conflicts)


def dedupe_conflicts(conflicts: list[dict]) -> list[dict]:
    seen = set()
    output = []

    for conflict in conflicts:
        key = (
            conflict.get("type"),
            tuple(
                sorted(
                    ref.get("reference", "") + ref.get("title", "")
                    for ref in conflict.get("clauses", {}).get("a", [])
                )
            ),
            tuple(
                sorted(
                    ref.get("reference", "") + ref.get("title", "")
                    for ref in conflict.get("clauses", {}).get("b", [])
                )
            ),
        )

        if key in seen:
            continue

        seen.add(key)
        output.append(conflict)

    return output
