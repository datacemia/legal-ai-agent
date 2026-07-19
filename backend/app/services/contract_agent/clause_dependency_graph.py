DEPENDENCY_REASONS = {
    "liability_data_protection": {
        "en": "Data protection breaches may be excluded from liability caps.",
        "fr": "Les violations de protection des données peuvent être exclues des plafonds de responsabilité.",
        "ar": "قد تُستثنى خروقات حماية البيانات من حدود المسؤولية.",
    },
    "liability_confidentiality": {
        "en": "Confidentiality breaches may be excluded from liability caps.",
        "fr": "Les violations de confidentialité peuvent être exclues des plafonds de responsabilité.",
        "ar": "قد تُستثنى خروقات السرية من حدود المسؤولية.",
    },
    "ip_confidentiality": {
        "en": "IP rights may depend on confidential information handling.",
        "fr": "Les droits de propriété intellectuelle peuvent dépendre du traitement des informations confidentielles.",
        "ar": "قد تعتمد حقوق الملكية الفكرية على كيفية التعامل مع المعلومات السرية.",
    },
    "service_liability": {
        "en": "Service failures may affect liability exposure.",
        "fr": "Les défaillances de service peuvent affecter l'exposition à la responsabilité.",
        "ar": "قد تؤثر إخفاقات الخدمة على مدى التعرض للمسؤولية.",
    },
    "payment_service": {
        "en": "Payment issues may affect service access or continuity.",
        "fr": "Les problèmes de paiement peuvent affecter l'accès au service ou sa continuité.",
        "ar": "قد تؤثر مشاكل الدفع على الوصول إلى الخدمة أو استمراريتها.",
    },
    "payment_failure_termination": {
        "en": "Payment failure may trigger termination.",
        "fr": "Un défaut de paiement peut entraîner la résiliation.",
        "ar": "قد يؤدي التخلف عن الدفع إلى الإنهاء.",
    },
    "confidentiality_liability": {
        "en": "Confidentiality breach may affect liability exposure.",
        "fr": "Une violation de confidentialité peut affecter l'exposition à la responsabilité.",
        "ar": "قد يؤثر خرق السرية على مدى التعرض للمسؤولية.",
    },
    "data_security": {
        "en": "Data obligations may depend on security safeguards.",
        "fr": "Les obligations relatives aux données peuvent dépendre des mesures de sécurité.",
        "ar": "قد تعتمد الالتزامات المتعلقة بالبيانات على الضمانات الأمنية.",
    },
}


def _reason(key: str, language: str = "en") -> str:
    entry = DEPENDENCY_REASONS.get(key, {})
    return entry.get(language, entry.get("en", ""))


def append_edge_once(
    edges: list[dict],
    source_id: int,
    target_id: int,
    reason: str,
) -> None:
    source = {
        "id": source_id,
    }

    target = {
        "id": target_id,
    }

    existing = any(
        edge["from"] == source["id"]
        and edge["to"] == target["id"]
        for edge in edges
    )

    if existing:
        return

    edges.append({
        "from": source["id"],
        "to": target["id"],
        "reason": reason,
    })


MAX_OUTBOUND_EDGES = 6


def build_clause_dependency_graph(clauses: list[dict], language: str = "en") -> dict:
    if language not in {"en", "fr", "ar"}:
        language = "en"

    nodes = []
    edges = []

    for idx, clause in enumerate(clauses):
        title = clause.get("clause_title", "") or clause.get("title", "")
        clause_type = clause.get("clause_type", "other")

        nodes.append({
            "id": idx,
            "title": title,
            # Article/section reference (e.g. "8.1" vs "8.4"), so a
            # downstream renderer can disambiguate two distinct clauses
            # that happen to share the same title -- without this, edges
            # from two different "Limitation de responsabilité" clauses
            # render as visually identical, indistinguishable duplicates
            # even though they are genuinely separate graph nodes.
            "reference": clause.get("clause_reference", ""),
            "type": clause_type,
            "risk_level": clause.get("risk_level", "low"),
        })

    explicit_payment_failure_terms = [
        "failure to pay",
        "non-payment",
        "unpaid",
        "payment default",
        "défaut de paiement",
        "non-paiement",
        "impayé",
        "التخلف عن الدفع",
        "عدم السداد",
        "متأخرات",
    ]

    dependency_rules = [
        ("liability", "data_protection", _reason("liability_data_protection", language)),
        ("liability", "confidentiality", _reason("liability_confidentiality", language)),
        ("intellectual_property", "confidentiality", _reason("ip_confidentiality", language)),
        ("service_level", "liability", _reason("service_liability", language)),
        ("payment", "service_level", _reason("payment_service", language)),
    ]

    edge_count_by_node = {}

    for source_type, target_type, reason in dependency_rules:
        source_nodes = [
            node for node in nodes
            if node["type"] == source_type
        ]

        target_nodes = [
            node for node in nodes
            if node["type"] == target_type
        ]

        for source in source_nodes:
            for target in target_nodes:
                if source["id"] == target["id"]:
                    continue

                source_id = source["id"]
                count = edge_count_by_node.get(source_id, 0)

                if count >= MAX_OUTBOUND_EDGES:
                    continue

                before_count = len(edges)

                append_edge_once(
                    edges,
                    source_id,
                    target["id"],
                    reason,
                )

                if len(edges) > before_count:
                    edge_count_by_node[source_id] = count + 1

    for source in nodes:
        source_clause = clauses[source["id"]]

        source_text = (
            source_clause.get("clause_text", "")
            or source_clause.get("original_text", "")
            or source_clause.get("quoted_text", "")
            or source_clause.get("clause_title", "")
            or source_clause.get("title", "")
            or ""
        ).lower()

        for target in nodes:
            if source["id"] == target["id"]:
                continue

            source_id = source["id"]
            count = edge_count_by_node.get(source_id, 0)

            if count >= MAX_OUTBOUND_EDGES:
                continue

            target_clause = clauses[target["id"]]

            target_text = (
                target_clause.get("clause_text", "")
                or target_clause.get("original_text", "")
                or target_clause.get("quoted_text", "")
                or target_clause.get("clause_title", "")
                or target_clause.get("title", "")
                or ""
            ).lower()

            combined_text = f"{source_text} {target_text}"

            if (
                "termination" in combined_text
                and any(
                    term in combined_text
                    for term in explicit_payment_failure_terms
                )
            ):
                before_count = len(edges)

                append_edge_once(
                    edges,
                    source_id,
                    target["id"],
                    _reason("payment_failure_termination", language),
                )

                if len(edges) > before_count:
                    edge_count_by_node[source_id] = count + 1

                continue

            if (
                "liability" in combined_text
                and "confidentiality" in combined_text
            ):
                before_count = len(edges)

                append_edge_once(
                    edges,
                    source_id,
                    target["id"],
                    _reason("confidentiality_liability", language),
                )

                if len(edges) > before_count:
                    edge_count_by_node[source_id] = count + 1

                continue

            if (
                (
                    "data" in combined_text
                    or "data protection" in combined_text
                    or "personal data" in combined_text
                )
                and "security" in combined_text
            ):
                before_count = len(edges)

                append_edge_once(
                    edges,
                    source_id,
                    target["id"],
                    _reason("data_security", language),
                )

                if len(edges) > before_count:
                    edge_count_by_node[source_id] = count + 1

                continue

    deduped_edges = []
    seen_edges = set()

    for edge in edges:
        key = (
            edge.get("from"),
            edge.get("to"),
            edge.get("reason"),
        )

        if key in seen_edges:
            continue

        seen_edges.add(key)
        deduped_edges.append(edge)

    return {
        "nodes": nodes,
        "edges": deduped_edges,
        "edges_count": len(deduped_edges),
    }