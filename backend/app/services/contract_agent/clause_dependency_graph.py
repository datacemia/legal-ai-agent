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

    dependency_rules = [
        ("termination", "payment", "Termination may be triggered by payment failure."),
        ("default", "remedies", "Default clauses often activate remedies."),
        ("liability", "data_protection", "Data protection breaches may be excluded from liability caps."),
        ("liability", "confidentiality", "Confidentiality breaches may be excluded from liability caps."),
        ("intellectual_property", "confidentiality", "IP rights may depend on confidential information handling."),
        ("service_level", "liability", "Service failures may affect liability exposure."),
        ("payment", "service_level", "Payment issues may affect service access or continuity."),
    ]

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
                if source["id"] != target["id"]:
                    append_edge_once(
                        edges,
                        source["id"],
                        target["id"],
                        reason,
                    )

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
                "payment" in combined_text
                and "termination" in combined_text
            ):
                append_edge_once(
                    edges,
                    source["id"],
                    target["id"],
                    "payment failure may trigger termination",
                )

            if (
                "liability" in combined_text
                and "confidentiality" in combined_text
            ):
                append_edge_once(
                    edges,
                    source["id"],
                    target["id"],
                    "confidentiality breach may affect liability exposure",
                )

            if (
                (
                    "data" in combined_text
                    or "data protection" in combined_text
                    or "personal data" in combined_text
                )
                and "security" in combined_text
            ):
                append_edge_once(
                    edges,
                    source["id"],
                    target["id"],
                    "data obligations may depend on security safeguards",
                )

            if (
                "breach" in combined_text
                and (
                    "remedies" in combined_text
                    or "remedy" in combined_text
                )
            ):
                append_edge_once(
                    edges,
                    source["id"],
                    target["id"],
                    "breach may activate contractual remedies",
                )

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
