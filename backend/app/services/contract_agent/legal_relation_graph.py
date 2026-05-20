from app.services.contract_agent.legal_ontology import (
    detect_legal_domains,
    detect_relation_triggers,
    detect_relation_consequences,
    get_trigger_consequences,
)


CONCEPT_TERMS = {
    "termination_event": [
        "termination", "terminate", "terminated", "résiliation", "résilier",
        "إنهاء", "فسخ",
    ],
    "notice_requirement": [
        "notice", "written notice", "notice period", "préavis", "avis écrit",
        "إشعار", "إشعار كتابي",
    ],
    "disability": [
        "disability", "incapacity", "invalidity", "incapacité", "invalidité",
        "عجز", "إعاقة",
    ],
    "death": [
        "death", "deceased", "décès", "mort", "وفاة", "موت",
    ],
    "good_reason": [
        "good reason", "for good reason", "motif légitime", "cause légitime",
        "سبب وجيه", "سبب مشروع",
    ],
    "voluntary_termination": [
        "voluntary termination", "resignation", "démission", "résiliation volontaire",
        "استقالة", "إنهاء طوعي",
    ],
    "without_cause": [
        "without cause", "sans motif", "دون سبب",
    ],
    "for_cause": [
        "for cause", "cause", "pour motif", "لسبب",
    ],
    "compensation_payment": [
        "salary", "bonus", "compensation", "benefits", "payment", "reimbursement",
        "salaire", "prime", "rémunération", "avantages", "paiement", "remboursement",
        "راتب", "مكافأة", "تعويض", "مزايا", "دفع", "سداد",
    ],
    "performance_goal": [
        "goal", "performance", "achievement", "factor", "objective",
        "objectif", "performance", "réalisation", "facteur",
        "هدف", "أداء", "إنجاز", "عامل",
    ],
    "confidentiality": [
        "confidential", "confidentiality", "trade secret", "proprietary information",
        "confidentialité", "secret commercial", "معلومات سرية", "سرية",
    ],
    "post_employment": [
        "post-employment", "post employment", "after termination", "thereafter",
        "survive", "survival", "après emploi", "après résiliation", "survie",
        "بعد انتهاء", "بعد الإنهاء", "تظل",
    ],
    "ip_ownership": [
        "intellectual property", "ownership", "license", "assignment",
        "propriété intellectuelle", "propriété", "licence", "cession",
        "ملكية فكرية", "ملكية", "ترخيص", "تنازل",
    ],
    "liability_protection": [
        "liability", "indemnity", "insurance", "warranty",
        "responsabilité", "indemnisation", "assurance", "garantie",
        "مسؤولية", "تعويض", "تأمين", "ضمان",
    ],
}


LEGAL_ROLES = {
    "disability": "trigger_event",
    "death": "trigger_event",
    "good_reason": "trigger_event",
    "payment_default": "breach_trigger",
    "notice_requirement": "procedural_requirement",
    "termination_event": "legal_consequence",
    "compensation_payment": "legal_consequence",
    "performance_goal": "condition",
    "confidentiality": "continuing_obligation",
    "post_employment": "temporal_scope",
    "ip_ownership": "rights_allocation",
    "liability_protection": "risk_allocation",
}

ALLOWED_RELATIONS = [
    ("trigger_event", "legal_consequence"),
    ("procedural_requirement", "legal_consequence"),
    ("breach_trigger", "legal_consequence"),
    ("condition", "legal_consequence"),
    ("continuing_obligation", "temporal_scope"),
    ("rights_allocation", "continuing_obligation"),
    ("continuing_obligation", "risk_allocation"),
]


DISPLAY_GROUPS = {
    "performance_service_obligations": "Performance & Duties",
    "governance_approval_control": "Governance & Control",
    "compensation_payment": "Compensation",
    "termination": "Termination",
    "ip_ownership_license": "Intellectual Property",
    "other": "General",
}


DEPENDENCY_TRIGGERS = {
    "termination": [
        "salary",
        "bonus",
        "benefits",
        "compensation",
        "equity",
    ],

    "payment": [
        "termination",
        "performance",
        "cause",
    ],

    "liability": [
        "damages",
        "claims",
        "breach",
    ],

    "confidentiality": [
        "breach",
        "injunctive relief",
    ],
}


def build_legal_relation_graph(
    clauses: list[dict],
) -> dict:
    nodes = []
    edges = []
    groups = {}

    indexed = []

    for index, clause in enumerate(clauses):
        title = str(
            clause.get("title")
            or clause.get("clause_title")
            or f"Clause {index + 1}"
        )

        text = " ".join([
            title,
            str(clause.get("quoted_text") or ""),
            str(clause.get("original_text") or ""),
            str(clause.get("clause_text") or ""),
        ]).lower()

        concepts = detect_concepts(
            title,
            text,
        )

        roles = detect_roles(concepts)

        domains = detect_legal_domains(text)

        all_triggers = []
        all_consequences = []

        for domain in domains:

            all_triggers.extend(
                detect_relation_triggers(
                    text,
                    domain,
                )
            )

            all_consequences.extend(
                detect_relation_consequences(
                    text,
                    domain,
                )
            )

        node_id = f"clause_{index}"

        nodes.append({
            "id": node_id,
            "title": title,
            "risk_level": clause.get("risk_level", "low"),
            "clause_type": clause.get("clause_type", "other"),
            "concepts": concepts,
            "roles": roles,
            "domains": domains,
            "relation_triggers": list(dict.fromkeys(all_triggers)),
            "relation_consequences": list(dict.fromkeys(all_consequences)),
        })

        indexed.append({
            "index": index,
            "title": title,
            "text": text,
            "concepts": concepts,
            "roles": roles,
            "source_type": clause.get("clause_type", "other"),
        })

        for concept in concepts:
            group_name = DISPLAY_GROUPS.get(
                concept,
                concept,
            )

            groups.setdefault(
                group_name,
                [],
            ).append(node_id)

    add_relation_edges(
        indexed,
        edges,
    )

    directional_edges = build_directional_edges(nodes)

    return {
        "nodes": nodes,
        "edges": (
            edges
            + directional_edges
        ),
        "groups": groups,
    }


def detect_concepts(
    title: str,
    text: str,
) -> list[str]:
    title_text = str(title or "").lower()
    body_text = str(text or "").lower()

    concepts = []

    for concept, terms in CONCEPT_TERMS.items():
        title_hit = contains_any(title_text, terms)
        body_hit = contains_any(body_text, terms)

        if title_hit:
            concepts.append(concept)
            continue

        # Body-only concepts are weaker: accept only structural concepts.
        if body_hit and concept in {
            "post_employment",
            "performance_goal",
            "liability_protection",
        }:
            concepts.append(concept)

    return concepts


def detect_roles(
    concepts: list[str],
) -> list[str]:
    roles = []

    for concept in concepts:
        role = LEGAL_ROLES.get(concept)

        if role and role not in roles:
            roles.append(role)

    return roles


def relation_allowed(
    source_roles: set[str],
    target_roles: set[str],
) -> bool:
    return any(
        source_role in source_roles
        and target_role in target_roles
        for source_role, target_role in ALLOWED_RELATIONS
    )


def add_relation_edges(
    indexed_clauses: list[dict],
    edges: list[dict],
) -> None:

    seen = set()

    for source in indexed_clauses:
        for target in indexed_clauses:
            if source["index"] == target["index"]:
                continue

            relation = detect_relation(
                source,
                target,
            )

            if not relation:
                continue

            edge_key = (
                source["index"],
                target["index"],
                relation["type"],
            )

            if edge_key in seen:
                continue

            seen.add(edge_key)

            edges.append({
                "from": f"clause_{source['index']}",
                "to": f"clause_{target['index']}",
                "type": relation["type"],
                "reason": relation["reason"],
                "confidence": relation["confidence"],
            })


def detect_relation(
    source: dict,
    target: dict,
) -> dict | None:

    source_concepts = set(source.get("concepts", []))
    target_concepts = set(target.get("concepts", []))

    source_roles = set(source.get("roles", []))
    target_roles = set(target.get("roles", []))

    if not relation_allowed(
        source_roles,
        target_roles,
    ):
        source_type = str(
            source.get("source_type", "")
        ).lower()

        target_text = " ".join([
            str(target.get("title", "")),
            str(target.get("text", "")),
        ]).lower()

        if source_type in DEPENDENCY_TRIGGERS:
            for trigger in DEPENDENCY_TRIGGERS[source_type]:
                if trigger in target_text:
                    return {
                        "type": "semantic_dependency",
                        "reason": (
                            f"{source_type.title()} may affect "
                            f"{trigger} obligations."
                        ),
                        "confidence": 0.75,
                    }

        return None

    if (
        "notice_requirement" in source_concepts
        and "termination_event" in target_concepts
    ):
        return {
            "type": "notice_dependency",
            "reason": "Termination depends on notice requirements.",
            "confidence": 0.9,
        }

    if (
        "disability" in source_concepts
        and "termination_event" in target_concepts
        and "voluntary_termination" not in target_concepts
        and "good_reason" not in target_concepts
        and "without_cause" not in target_concepts
        and "for_cause" not in target_concepts
    ):
        return {
            "type": "termination_trigger",
            "reason": "Disability may trigger termination rights.",
            "confidence": 0.9,
        }

    if (
        "death" in source_concepts
        and "termination_event" in target_concepts
        and "voluntary_termination" not in target_concepts
        and "good_reason" not in target_concepts
    ):
        return {
            "type": "termination_trigger",
            "reason": "Death may trigger termination consequences.",
            "confidence": 0.9,
        }

    if (
        "good_reason" in source_concepts
        and "compensation_payment" in target_concepts
    ):
        return {
            "type": "compensation_trigger",
            "reason": "Good Reason may trigger compensation or benefit consequences.",
            "confidence": 0.85,
        }

    if (
        "performance_goal" in source_concepts
        and "compensation_payment" in target_concepts
        and (
            "bonus" in target["title"].lower()
            or "incentive" in target["title"].lower()
            or "prime" in target["title"].lower()
            or "مكافأة" in target["title"].lower()
        )
    ):
        return {
            "type": "performance_dependency",
            "reason": "Bonus compensation depends on defined performance goals.",
            "confidence": 0.9,
        }

    if (
        "confidentiality" in source_concepts
        and "post_employment" in target_concepts
    ):
        return {
            "type": "post_employment_obligation",
            "reason": "Confidentiality may continue after the relationship ends.",
            "confidence": 0.85,
        }

    if (
        "ip_ownership" in source_concepts
        and "confidentiality" in target_concepts
    ):
        return {
            "type": "information_rights_dependency",
            "reason": "IP or ownership rights may depend on confidential information handling.",
            "confidence": 0.8,
        }

    if (
        "confidentiality" in source_concepts
        and "liability_protection" in target_concepts
    ):
        return {
            "type": "liability_exception",
            "reason": "Confidentiality breaches may affect liability or indemnity exposure.",
            "confidence": 0.8,
        }

    return None


def contains_any(
    text: str,
    terms: list[str],
) -> bool:
    return any(
        term in text
        for term in terms
    )
def build_directional_edges(
    nodes: list,
) -> list:

    edges = []

    for source in nodes:

        source_domains = set(
            source.get("domains", [])
        )

        source_triggers = set(
            source.get(
                "relation_triggers",
                [],
            )
        )

        if not source_triggers:
            continue

        for target in nodes:

            if source["id"] == target["id"]:
                continue

            target_domains = set(
                target.get("domains", [])
            )

            shared_domains = (
                source_domains
                & target_domains
            )

            if not shared_domains:
                continue

            target_consequences = set(
                target.get(
                    "relation_consequences",
                    [],
                )
            )

            if not target_consequences:
                continue

            shared_terms = set()

            for trigger in source_triggers:

                mapped_consequences = set(
                    get_trigger_consequences(trigger)
                )

                overlap = (
                    mapped_consequences
                    & target_consequences
                )

                shared_terms.update(overlap)

            shared_trigger_count = len(shared_terms)

            if (
                len(shared_domains) < 1
                or shared_trigger_count < 1
            ):
                continue

            score = (
                shared_trigger_count * 4
                + len(shared_domains)
            )

            if score < 5:
                continue

            edges.append({
                "from": source["id"],
                "to": target["id"],
                "domains": list(shared_domains),
                "shared_terms": list(shared_terms),
                "relation_type": "trigger_consequence",
                "score": score,
            })

    return edges


