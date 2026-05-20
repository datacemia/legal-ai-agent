import re
from dataclasses import dataclass, field


@dataclass
class LegalNode:
    id: str
    title: str
    text: str = ""
    level: int = 1
    number: str = ""
    parent_id: str | None = None
    parent_clause_id: str | None = None
    confidence: float = 0.0
    depth: int = 1
    section_path: list[str] = field(default_factory=list)
    semantic_parent: str | None = None
    children: list = field(default_factory=list)
    lineage: list[str] = field(default_factory=list)


def normalize_line(line: str) -> str:
    return re.sub(r"\s+", " ", str(line or "").strip())


def normalize_title(title: str) -> str:
    title = normalize_line(title).lower()

    title = re.sub(
        r"^(article|section|clause)\s+\d+\s*[-:.–—]?\s*",
        "",
        title,
        flags=re.IGNORECASE,
    )

    title = re.sub(
        r"^(المادة|البند|الفقرة)\s*\d*\s*[-:.–—]?\s*",
        "",
        title,
    )

    title = re.sub(
        r"^\d+(\.\d+)*\s*[).:-]?\s*",
        "",
        title,
    )

    title = re.sub(
        r"^\(([a-z]|[ivxlcdm]+)\)\s*",
        "",
        title,
        flags=re.IGNORECASE,
    )

    return title.strip(" -–—:.").strip()


def title_contains_parent(
    child_title: str,
    parent_title: str,
) -> bool:
    child = normalize_title(child_title)
    parent = normalize_title(parent_title)

    if not child or not parent:
        return False

    if child == parent:
        return False

    if len(parent) < 4:
        return False

    return parent in child


def detect_semantic_parent(
    child_title: str,
    previous_nodes: list[LegalNode],
) -> LegalNode | None:
    for parent in reversed(previous_nodes):
        if title_contains_parent(
            child_title,
            parent.title,
        ):
            return parent

    child = normalize_title(child_title)

    semantic_parent_terms = {
        "termination": [
            "without cause",
            "for cause",
            "good reason",
            "voluntary termination",
            "non-renewal",
            "death",
            "disability",
            "notice",
            "date of termination",
            "résiliation",
            "sans motif",
            "pour motif",
            "décès",
            "incapacité",
            "préavis",
            "إنهاء",
            "فسخ",
            "وفاة",
            "عجز",
            "إشعار",
        ],
        "compensation": [
            "salary",
            "bonus",
            "benefits",
            "expenses",
            "reimbursement",
            "payment",
            "salaire",
            "prime",
            "avantages",
            "frais",
            "remboursement",
            "paiement",
            "راتب",
            "مكافأة",
            "مزايا",
            "مصاريف",
            "سداد",
            "دفع",
        ],
        "confidentiality": [
            "confidential information",
            "trade secret",
            "non-disclosure",
            "post-employment",
            "confidentialité",
            "secret commercial",
            "non-divulgation",
            "معلومات سرية",
            "سرية",
            "عدم الإفصاح",
        ],
    }

    for parent in reversed(previous_nodes):
        parent_normalized = normalize_title(parent.title)

        for parent_key, child_terms in semantic_parent_terms.items():
            if parent_key in parent_normalized and any(
                term in child
                for term in child_terms
            ):
                return parent

    return None


def detect_heading_level(line: str) -> tuple[int, str, float]:
    line = normalize_line(line)

    patterns = [
        (1, r"^(article|section|clause)\s+(\d+)", 0.9),
        (1, r"^(المادة|البند|الفقرة)\s*(\d+)", 0.9),
        (1, r"^(\d+)[\.\)]\s+", 0.8),
        (2, r"^(\d+\.\d+)[\.\)]?\s+", 0.85),
        (3, r"^\(([a-z])\)\s+", 0.75),
        (3, r"^\(([ivxlcdm]+)\)\s+", 0.7),
    ]

    for level, pattern, confidence in patterns:
        match = re.search(pattern, line, re.IGNORECASE)

        if match:
            number = match.group(2) if len(match.groups()) >= 2 else match.group(1)
            return level, number, confidence

    if line.isupper() and 4 <= len(line) <= 120:
        return 1, "", 0.65

    return 0, "", 0.0


def attach_node_to_parent(
    node: LegalNode,
    stack: list[LegalNode],
    root_nodes: list[LegalNode],
    previous_nodes: list[LegalNode],
) -> None:

    while stack and stack[-1].level >= node.level:
        stack.pop()

    parent = stack[-1] if stack else None

    semantic_parent = detect_semantic_parent(
        node.title,
        previous_nodes,
    )

    if (
        semantic_parent
        and node.level >= semantic_parent.level
        and semantic_parent.id != node.id
    ):
        parent = semantic_parent

    if parent:
        node.parent_id = parent.id
        node.parent_clause_id = parent.id
        node.semantic_parent = parent.title
        node.depth = parent.depth + 1
        node.lineage = parent.lineage + [parent.title]
        node.section_path = parent.section_path + [node.title]
        parent.children.append(node)
    else:
        node.depth = 1
        node.section_path = [node.title]
        root_nodes.append(node)

    stack.append(node)
    previous_nodes.append(node)


def build_legal_document_tree(text: str) -> list[LegalNode]:
    lines = [
        normalize_line(line)
        for line in str(text or "").splitlines()
        if normalize_line(line)
    ]

    nodes: list[LegalNode] = []
    stack: list[LegalNode] = []
    previous_nodes: list[LegalNode] = []
    node_counter = 0

    for line in lines:
        level, number, confidence = detect_heading_level(line)

        if confidence >= 0.65:
            node_counter += 1

            node = LegalNode(
                id=f"node_{node_counter}",
                title=line,
                level=level,
                number=number,
                confidence=confidence,
            )

            attach_node_to_parent(
                node=node,
                stack=stack,
                root_nodes=nodes,
                previous_nodes=previous_nodes,
            )

        else:
            if stack:
                stack[-1].text += ("\n" + line)

            else:
                node_counter += 1

                node = LegalNode(
                    id=f"node_{node_counter}",
                    title="Document Preamble",
                    text=line,
                    level=1,
                    confidence=0.3,
                    depth=1,
                    section_path=["Document Preamble"],
                )

                nodes.append(node)
                stack.append(node)
                previous_nodes.append(node)

    return nodes


def flatten_legal_tree_to_clause_objects(
    nodes: list[LegalNode],
    min_length: int = 80,
) -> list[dict]:

    clauses = []

    def walk(node: LegalNode):
        content = "\n".join(
            part for part in [
                node.title,
                node.text.strip(),
            ]
            if part
        ).strip()

        if len(content) >= min_length:
            clauses.append({
                "id": node.id,
                "title": node.title,
                "text": content,
                "level": node.level,
                "depth": node.depth,
                "number": node.number,
                "parent_id": node.parent_id,
                "parent_clause_id": node.parent_clause_id,
                "semantic_parent": node.semantic_parent,
                "section_path": node.section_path,
                "lineage": node.lineage,
                "children": [
                    child.id
                    for child in node.children
                ],
                "confidence": node.confidence,
            })

        for child in node.children:
            walk(child)

    for node in nodes:
        walk(node)

    return clauses


def flatten_legal_tree_to_clauses(
    nodes: list[LegalNode],
    min_length: int = 80,
) -> list[str]:

    clause_objects = flatten_legal_tree_to_clause_objects(
        nodes,
        min_length=min_length,
    )

    return [
        clause["text"]
        for clause in clause_objects
    ]


def parse_legal_document_objects(text: str) -> list[dict]:
    tree = build_legal_document_tree(text)

    return flatten_legal_tree_to_clause_objects(tree)


def parse_legal_document(text: str) -> list[str]:
    tree = build_legal_document_tree(text)

    return flatten_legal_tree_to_clauses(tree)
