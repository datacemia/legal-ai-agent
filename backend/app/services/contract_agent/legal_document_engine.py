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
    line = str(line or "").strip()

    # Strip a leading markdown heading marker ("#", "##", ...) before
    # further normalization. Every contract test document in this
    # pipeline uses markdown-style section headers ("# 1. DEFINITIONS",
    # "# 3. الرسوم والتجديد التلقائي"...), but every numbered-heading
    # pattern in detect_heading_level() anchors on a digit at the very
    # start of the line ("^\d+..."). A leading "#" made every such
    # header completely invisible to heading detection -- regardless of
    # language -- silently discarding the section's real title and
    # letting its content get mis-partitioned into the wrong node
    # (orphaned onto the previous section, or picking up a title
    # extracted from elsewhere in the body instead of its own heading).
    line = re.sub(r"^#+\s*", "", line)

    return re.sub(r"\s+", " ", line)


# Known unnumbered structural headings, matched independent of letter
# case, shared by is_document_title_or_cover_line() and
# detect_heading_level(). Covers common closing/opening sections that
# routinely appear without a section number in any of the three
# languages (e.g. "SIGNATURES", "التوقيعات").
_STRUCTURAL_HEADING_TERMS = [
    "signatures", "signature", "in witness whereof",
    "en foi de quoi",
    "التوقيعات", "التوقيع",
    "definitions", "définitions", "التعاريف",
    "recitals", "préambule", "الديباجة", "تمهيد",
    "exhibits", "annexes", "الملاحق",
]


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



def is_document_title_or_cover_line(line: str) -> bool:
    normalized = normalize_line(line)
    lowered = normalized.lower()

    if not normalized:
        return True

    # A line that starts with a numbered-heading marker ("1.", "2)",
    # "3.1"...) is a section heading, never a genuine document cover
    # title -- a contract's own title line ("MASTER SERVICES
    # AGREEMENT") never begins with a section number. Without this
    # early exemption, a short, all-caps numbered heading like "2. FEES
    # AND AUTO-RENEWAL" was being misclassified as a document title by
    # the uppercase-ratio heuristic below and silently discarded before
    # ever reaching detect_heading_level() -- an entire section's
    # content then gets orphaned onto whatever node preceded it. This
    # affects any language where section headings are conventionally
    # styled distinctly (all-caps in English, for instance), not just
    # Arabic.
    if re.match(r"^\d+(\.\d+)*[\.\)]\s+\S", normalized):
        return False

    # Known unnumbered structural headings (Signatures, Definitions...)
    # are never a genuine document cover title either, and must be
    # exempted HERE too, not just in detect_heading_level(). Without
    # this, an English/French all-caps heading like "SIGNATURES"
    # satisfies the uppercase-ratio "looks like a title" heuristic below
    # and gets swallowed by THIS function first -- detect_heading_level()
    # never even runs on it, so its own case-agnostic recognition of the
    # exact same term (needed for Arabic, which cannot satisfy the
    # uppercase heuristic at all) never gets a chance to help. Confirmed
    # in testing: a trailing "SIGNATURES" heading caused the entire
    # preceding clause to be discarded downstream after its text merged
    # with the un-recognized heading -- in English, not just Arabic.
    if normalized.strip(" :.-–—").lower() in _STRUCTURAL_HEADING_TERMS:
        return False

    words = normalized.split()

    operative_terms = [
        "shall", "must", "may", "means", "includes", "entitled",
        "liable", "terminate", "pay", "notify", "process",
        "obligation", "right",
        "doit", "peut", "signifie", "comprend", "autorisé",
        "responsable", "résilier", "payer", "notifier", "traiter",
        "obligation", "droit",
        "يلتزم", "يجب", "يجوز", "يعني", "يشمل", "مسؤول",
        "إنهاء", "دفع", "إخطار", "معالجة", "التزام", "حق",
    ]

    alpha_count = sum(
        c.isalpha()
        for c in normalized
    )

    uppercase_ratio = (
        sum(
            c.isupper()
            for c in normalized
            if c.isalpha()
        )
        / max(1, alpha_count)
    )

    looks_like_title = (
        uppercase_ratio > 0.70
        or normalized.istitle()
    )

    if (
        len(words) <= 12
        and looks_like_title
        and not any(term in lowered for term in operative_terms)
    ):
        return True

    document_title_patterns = [
        r".*\bagreement\b$",
        r".*\bcontract\b$",
        r".*\bmaster services agreement\b$",
        r".*\bservice agreement\b$",
        r".*\bemployment agreement\b$",
        r".*\blease agreement\b$",
        r".*\blicense agreement\b$",
        r".*\bcontrat\b$",
        r".*\baccord\b$",
        r".*اتفاقية$",
        r".*عقد$",
    ]

    if (
        len(words) <= 12
        and looks_like_title
        and any(
            re.match(pattern, lowered)
            for pattern in document_title_patterns
        )
    ):
        return True

    return False


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


def _term_present(term: str, text: str) -> bool:
    """
    Word-boundary-aware presence check, used by detect_semantic_parent()
    for both the category-key check and the associated-term check.
    Avoids substring collisions such as "support" matching inside
    "supported" -- the exact real bug that caused an unrelated Governing
    Law clause to be misattached under a Non-Compete clause purely
    because its boilerplate ("...provisions herein are supported by
    adequate consideration...") happened to contain that substring.
    """
    if not term or not text:
        return False

    return bool(re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text))


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
        "payment": [
            "salary",
            "bonus",
            "benefits",
            "expenses",
            "reimbursement",
            "payment",
            "invoice",
            "fees",
            "pricing",
            "tax",
            "commission",
            "royalties",
            "salaire",
            "prime",
            "avantages",
            "frais",
            "remboursement",
            "paiement",
            "facture",
            "prix",
            "taxe",
            "commission",
            "redevances",
            "راتب",
            "مكافأة",
            "مزايا",
            "مصاريف",
            "سداد",
            "دفع",
            "فاتورة",
            "رسوم",
            "ضريبة",
            "عمولة",
        ],
        "confidentiality": [
            "confidential information",
            "trade secret",
            "non-disclosure",
            "confidentialité",
            "secret commercial",
            "non-divulgation",
            "معلومات سرية",
            "سرية",
            "عدم الإفصاح",
        ],
        "services": [
            "service level",
            "service levels",
            "support",
            "maintenance",
            "delivery",
            "acceptance",
            "performance",
            "sla",
            "availability",
            "uptime",
            "niveau de service",
            "assistance",
            "maintenance",
            "livraison",
            "acceptation",
            "performance",
            "disponibilité",
            "مستوى الخدمة",
            "الدعم",
            "الصيانة",
            "التسليم",
            "القبول",
            "الأداء",
            "التوافر",
        ],
        "liability": [
            "cap",
            "liability cap",
            "limitation",
            "limitation of liability",
            "indemnity",
            "indemnification",
            "damages",
            "insurance",
            "warranty",
            "remedies",
            "plafond",
            "limitation de responsabilité",
            "indemnisation",
            "dommages",
            "assurance",
            "garantie",
            "recours",
            "حد",
            "حد المسؤولية",
            "تعويض",
            "أضرار",
            "تأمين",
            "ضمان",
            "وسائل الانتصاف",
        ],
        "data protection": [
            "personal data",
            "data processing",
            "processor",
            "controller",
            "subprocessor",
            "security incident",
            "security measures",
            "privacy",
            "cybersecurity",
            "données personnelles",
            "traitement des données",
            "sous-traitant",
            "responsable du traitement",
            "incident de sécurité",
            "mesures de sécurité",
            "vie privée",
            "cybersécurité",
            "بيانات شخصية",
            "معالجة البيانات",
            "معالج البيانات",
            "حادث أمني",
            "تدابير أمنية",
            "الخصوصية",
            "الأمن السيبراني",
        ],
        "intellectual property": [
            "license",
            "assignment",
            "ownership",
            "deliverables",
            "work product",
            "invention",
            "patent",
            "copyright",
            "trademark",
            "moral rights",
            "licence",
            "cession",
            "propriété",
            "livrables",
            "invention",
            "brevet",
            "droit d'auteur",
            "marque",
            "droits moraux",
            "ترخيص",
            "تنازل",
            "ملكية",
            "مخرجات العمل",
            "اختراع",
            "براءة",
            "حقوق النشر",
            "علامة تجارية",
            "حقوق معنوية",
        ],
        "dispute resolution": [
            "arbitration",
            "mediation",
            "governing law",
            "jurisdiction",
            "venue",
            "court",
            "litigation",
            "arbitrage",
            "médiation",
            "droit applicable",
            "juridiction",
            "tribunal",
            "contentieux",
            "تحكيم",
            "وساطة",
            "القانون الواجب التطبيق",
            "اختصاص",
            "محكمة",
            "تقاضي",
        ],
        "restrictive covenants": [
            "non-compete",
            "non compete",
            "non-solicitation",
            "non solicitation",
            "non-dealing",
            "non-circumvention",
            "exclusivity",
            "exclusive dealing",
            "non-concurrence",
            "non-sollicitation",
            "non sollicitation",
            "exclusivité",
            "عدم المنافسة",
            "عدم الاستقطاب",
            "عدم الالتفاف",
            "الحصرية",
        ],
        "governance": [
            "board",
            "director",
            "shareholder",
            "approval",
            "consent",
            "committee",
            "governance",
            "audit",
            "compliance",
            "conseil",
            "administrateur",
            "actionnaire",
            "approbation",
            "consentement",
            "comité",
            "gouvernance",
            "audit",
            "conformité",
            "مجلس الإدارة",
            "مدير",
            "مساهم",
            "موافقة",
            "لجنة",
            "حوكمة",
            "تدقيق",
            "امتثال",
        ],
        "force majeure": [
            "force majeure", "act of god", "natural disaster", "pandemic", "war", "strike",
            "cas de force majeure", "catastrophe naturelle", "pandémie", "grève",
            "القوة القاهرة", "كارثة طبيعية", "جائحة", "حرب", "إضراب",
        ],
        "tax": [
            "tax", "vat", "gst", "withholding", "tax invoice",
            "impôt", "tva", "retenue à la source", "facture fiscale",
            "ضريبة", "القيمة المضافة", "اقتطاع", "فاتورة ضريبية",
        ],
        "warranties": [
            "warranty", "representation", "merchantability", "fitness for purpose",
            "garantie", "déclaration", "aptitude à l'usage",
            "ضمان", "إقرار", "ملاءمة للغرض",
        ],
        "renewal": [
            "renewal", "automatic renewal", "extension term",
            "renouvellement", "reconduction automatique",
            "تجديد", "تجديد تلقائي",
        ],
        "suspension": [
            "suspension", "suspend services", "access suspension",
            "suspendre les services", "تعليق", "تعليق الخدمات",
        ],
        "business continuity": [
            "business continuity", "disaster recovery", "backup", "restore",
            "continuité d'activité", "reprise après sinistre",
            "استمرارية الأعمال", "التعافي من الكوارث",
        ],
        "publicity": [
            "press release", "public announcement", "use of name",
            "communiqué de presse", "annonce publique",
            "بيان صحفي", "إعلان عام",
        ],
        "severability": [
            "severability", "invalid provision", "unenforceable",
            "divisibilité", "clause invalide",
            "قابلية الفصل", "حكم غير قابل للتنفيذ",
        ],
        "survival": [
            "survive termination", "post-termination",
            "survie", "post-résiliation",
            "استمرار بعد الإنهاء",
        ],
        "amendment": [
            "amendment", "change order", "written modification",
            "avenant", "modification",
            "تعديل", "أمر تغيير",
        ],
        "waiver": [
            "waiver", "failure to enforce",
            "renonciation", "défaut d'exercice",
            "تنازل", "عدم ممارسة الحق",
        ],
        "assignment": [
            "assignment", "delegate", "novation",
            "cession", "déléguer",
            "تنازل", "تفويض",
        ],
        "insurance": [
            "insurance", "coverage", "policy",
            "assurance", "couverture",
            "تأمين", "تغطية",
        ],
        "export control": [
            "export control", "sanctions", "embargo",
            "contrôle des exportations", "sanctions",
            "ضوابط التصدير", "عقوبات",
        ],
        "open source": [
            "open source", "copyleft", "third-party software",
            "logiciel libre", "logiciel tiers",
            "برنامج مفتوح المصدر", "برنامج طرف ثالث",
        ],
        "escrow": [
            "escrow", "source code escrow",
            "séquestre", "séquestre de code source",
            "ضمان الكود", "إيداع",
        ],
        "transition assistance": [
            "transition assistance", "exit assistance", "handover",
            "assistance de transition", "assistance à la sortie",
            "مساعدة انتقالية", "مساعدة الخروج",
        ],
    }

    for parent in reversed(previous_nodes):
        parent_normalized = normalize_title(parent.title)

        for parent_key, child_terms in semantic_parent_terms.items():
            # Word-boundary-aware matching, not naive substring
            # containment. Confirmed real bug: the term "support" (from
            # the "services" category) matched as a substring inside
            # "supported" in a Governing Law clause's boilerplate
            # ("...non-compete provisions herein are SUPPORTed by
            # adequate consideration..."), causing that clause to be
            # semantically misattached under an unrelated Non-Compete
            # clause instead of its own Governing Law section -- purely
            # because of a coincidental substring match, not any genuine
            # topical relationship. This affects every category key and
            # term in this dictionary, in any of the three languages, so
            # the fix is applied generically rather than special-casing
            # "support".
            if _term_present(parent_key, parent_normalized) and any(
                _term_present(term, child)
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

    if line.isupper() and 4 <= len(line) <= 120 and len(line.split()) <= 10:
        return 1, "", 0.65

    # Known unnumbered structural headings, matched independent of
    # letter case. The isupper() fallback above gives English/French
    # ALL-CAPS headings (e.g. "SIGNATURES") a way to be recognized even
    # without a section number -- but scripts with no letter case at all
    # (Arabic) can never satisfy isupper(), so an unnumbered heading like
    # "التوقيعات" was silently invisible to heading detection. Left
    # unrecognized, its text gets merged into whatever clause precedes
    # it, which can then be wrongly discarded downstream by unrelated
    # content filters (e.g. a signature-block filter matching "التوقيعات"
    # inside what is otherwise a legitimate substantive clause). A short,
    # explicit list covers the common closing/opening sections that
    # routinely appear without a number in any of the three languages.
    if line.strip(" :.-–—").lower() in _STRUCTURAL_HEADING_TERMS:
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

    # Semantic matching is only consulted as a FALLBACK when structure
    # alone provides no parent at all (parent is None) -- it must never
    # override an already-valid structural match. Confirmed real bug:
    # a spurious category-keyword coincidence (a payment-related word
    # mentioned only in passing within an otherwise unrelated clause,
    # matched against another equally incidental payment-related word
    # in a much later clause) was overriding the correct, unambiguous
    # structural parent determined by document order and heading level,
    # misattaching a clause under a completely unrelated earlier one and
    # leaving its rightful parent section orphaned.
    if parent is None:
        semantic_parent = detect_semantic_parent(
            node.title,
            previous_nodes,
        )

        # Strictly deeper level required (not >=): a genuine parent-child
        # relationship always has the child deeper than the parent.
        # Confirmed real bug: in a header-less, flattened context (e.g.
        # re-splitting already-split clause strings joined back together
        # without their original section headers), every clause ends up
        # at the same level with no structural parent at all, so this
        # fallback gets consulted for every single one of them -- and a
        # spurious category-keyword coincidence (two same-level clauses
        # each mentioning an unrelated word from the same broad category,
        # like "payment" and "fees") was misattaching one clause as a
        # "child" of another same-level sibling, silently dropping the
        # wrongly-demoted clause's own entry.
        if (
            semantic_parent
            and node.level > semantic_parent.level
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
        if is_document_title_or_cover_line(line):
            continue

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
    min_length: int = 25,
) -> list[dict]:

    clauses = []

    def walk(node: LegalNode):
        own_text = node.text.strip()

        # A node that HAS children but captured no substantive text of
        # its own (own_text empty) is a pure organizational section
        # header -- e.g. "3. FEES AND AUTO-RENEWAL" immediately followed
        # by "3.1 Client shall pay...", with nothing captured directly
        # under the header itself before its first sub-heading began.
        # Without this check, every such header produced its own
        # separate, near-empty clause entry (title only, frequently with
        # no clean clause number attached) IN ADDITION to its child's
        # own entry -- duplicating every section built this way.
        # Confirmed on both English and Arabic test contracts. A node
        # with children that DOES have genuine text of its own (a real
        # clause that also happens to introduce numbered sub-items) is
        # unaffected and still gets its own entry as before.
        is_pure_section_header = bool(node.children) and not own_text

        if not is_pure_section_header:
            has_dot = bool(node.number) and "." in node.number

            # Each "\n"-separated segment in own_text corresponds to one
            # original source paragraph accumulated after this node's own
            # heading line (see stack[-1].text += "\n" + line above) --
            # by construction, every such paragraph is something that
            # could be its own numbered item, since it is literally a
            # separate line in the source, distinct from the clause's
            # own heading line.
            own_text_segments = [
                s.strip() for s in own_text.split("\n") if s.strip()
            ]

            if has_dot:
                # This node's own number is already specific (e.g.
                # "2.1"), so its own title alone is independently
                # substantial content -- keep it as its own entry, and
                # treat EVERY accumulated paragraph as a candidate
                # separate, positionally-numbered sub-clause (e.g. "2.2",
                # "2.3", ...) rather than folding the first one into this
                # node's own text. Confirmed real case: a clause like
                # "2.1 The Company shall pay a base salary..." followed
                # by an unnumbered "[Executive] shall be eligible for an
                # annual bonus..." paragraph -- the bonus provision is a
                # genuinely separate item that lost its own "2.2" number
                # during text extraction, not a continuation of 2.1.
                content = node.title.strip()
                extra_segments = own_text_segments
            else:
                # A bare section-level number (e.g. "1", no dot) has no
                # meaningful standalone content on its own (the section
                # heading alone is normally too short to pass
                # min_length) -- its first accumulated paragraph is
                # combined into the inferred "N.1" entry alongside the
                # heading, and only FURTHER paragraphs beyond that one
                # are split out as additional positionally-numbered
                # entries.
                primary_text = own_text_segments[0] if own_text_segments else ""
                extra_segments = own_text_segments[1:]
                content = "\n".join(
                    part for part in [node.title, primary_text] if part
                ).strip()

            if len(content) >= min_length:
                clause_number = node.number

                # A bare section-level number (e.g. "1", no dot) that
                # ALSO carries substantive own_text is a section header
                # whose immediately-following sentence has no explicit
                # sub-clause number of its own in the source text --
                # confirmed real cause: some source documents number a
                # lone first sub-clause via the word processor's
                # auto-numbering (list styling) rather than typing "1.1"
                # as literal text, and plain-text extraction from such
                # documents does not preserve auto-generated list
                # numbers, only the paragraph's own typed content.
                # Reporting the bare "1" as this clause's reference is
                # ambiguous and collides with the section heading
                # itself; inferring "1.1" (this section's first,
                # implicit sub-clause) gives it a specific, usable
                # reference consistent with how sibling sections in the
                # same document number their own sub-clauses.
                if (
                    clause_number
                    and not has_dot
                    and own_text
                ):
                    clause_number = f"{clause_number}.1"

                clauses.append({
                    "id": node.id,
                    "title": node.title,
                    "text": content,
                    "level": node.level,
                    "depth": node.depth,
                    "number": clause_number,
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

                if (
                    extra_segments
                    and clause_number
                    and "." in clause_number
                ):
                    base_prefix, _, last_part_str = clause_number.rpartition(".")

                    if base_prefix and last_part_str.isdigit():
                        last_part = int(last_part_str)

                        for offset, segment in enumerate(extra_segments, start=1):
                            if len(segment) < min_length:
                                continue

                            inferred_number = f"{base_prefix}.{last_part + offset}"

                            clauses.append({
                                "id": f"{node.id}_extra_{offset}",
                                "title": segment[:80],
                                "text": segment,
                                "level": node.level,
                                "depth": node.depth,
                                "number": inferred_number,
                                "parent_id": node.parent_id,
                                "parent_clause_id": node.parent_clause_id,
                                "semantic_parent": node.semantic_parent,
                                "section_path": node.section_path,
                                "lineage": node.lineage,
                                "children": [],
                                # Slightly lower confidence than a
                                # directly-detected heading: this entry
                                # is inferred from paragraph boundaries,
                                # not an explicit number in the source.
                                "confidence": round(node.confidence * 0.8, 2),
                            })

        for child in node.children:
            walk(child)

    for node in nodes:
        walk(node)

    return clauses


def flatten_legal_tree_to_clauses(
    nodes: list[LegalNode],
    min_length: int = 25,
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
