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


def build_clause_dependency_graph(clauses: list[dict]) -> dict:
    nodes = []
    edges = []

    for idx, clause in enumerate(clauses):
        title = clause.get("clause_title", "") or clause.get("title", "")
        clause_type = clause.get("clause_type", "other")

        nodes.append({
            "id": idx,
            "title": title,
            "type": clause_type,
            "risk_level": clause.get("risk_level", "low"),
        })

    explicit_payment_failure_terms = [
        "failure to pay",
        "non-payment",
        "unpaid",
        "payment default",
    ]

    dependency_rules = [
        ("liability", "data_protection", "Data protection breaches may be excluded from liability caps."),
        ("liability", "confidentiality", "Confidentiality breaches may be excluded from liability caps."),
        ("intellectual_property", "confidentiality", "IP rights may depend on confidential information handling."),
        ("service_level", "liability", "Service failures may affect liability exposure."),
        ("payment", "service_level", "Payment issues may affect service access or continuity."),
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
                    "payment failure may trigger termination",
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
                    "confidentiality breach may affect liability exposure",
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
                    "data obligations may depend on security safeguards",
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
    }
