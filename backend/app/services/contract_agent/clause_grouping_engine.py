from app.services.contract_agent.legal_ontology import (
    detect_legal_domains,
)


def normalize_text(text: str) -> str:
    return " ".join(
        str(text or "").lower().strip().split()
    )


DOMAIN_TERMS = {
    "termination": [
        # EN
        "termination", "terminate", "terminated", "without cause",
        "for cause", "good reason", "non-renewal", "expiry",
        "expiration", "notice period", "cure period", "breach",
        "default",
        # FR
        "résiliation", "résilier", "fin du contrat",
        "non-renouvellement", "expiration", "préavis",
        "délai de correction", "manquement", "défaut",
        # AR
        "إنهاء", "فسخ", "انتهاء", "عدم التجديد",
        "إشعار", "مهلة تصحيح", "إخلال", "الإخلال", "تقصير",
    ],
    "compensation_payment": [
        # EN
        "payment", "pay", "salary", "fee", "fees", "bonus",
        "compensation", "expenses", "reimbursement", "invoice",
        "interest", "commission", "price", "pricing", "remuneration",
        # FR
        "paiement", "salaire", "honoraires", "frais", "prime",
        "rémunération", "remboursement", "facture", "intérêt",
        "commission", "prix",
        # AR
        "دفع", "الدفع", "راتب", "أتعاب", "رسوم", "مكافأة",
        "تعويض", "سداد", "فاتورة", "فائدة", "عمولة", "ثمن", "السعر",
    ],
    "confidentiality_data": [
        # EN
        "confidential", "confidentiality", "non-disclosure",
        "trade secret", "proprietary information", "personal data",
        "data protection", "privacy", "security",
        # FR
        "confidentiel", "confidentialité", "non-divulgation",
        "secret commercial", "données personnelles",
        "protection des données", "vie privée", "sécurité",
        # AR
        "سري", "سرية", "عدم الإفصاح", "سر تجاري",
        "معلومات سرية", "بيانات شخصية", "حماية البيانات",
        "الخصوصية", "الأمن",
    ],
    "liability_indemnity_insurance": [
        # EN
        "liability", "liable", "indemnity", "indemnification",
        "indemnify", "insurance", "warranty", "damages",
        "limitation of liability",
        # FR
        "responsabilité", "responsable", "indemnité",
        "indemnisation", "indemniser", "assurance", "garantie",
        "dommages", "limitation de responsabilité",
        # AR
        "مسؤولية", "مسؤول", "تعويض", "تأمين", "ضمان",
        "أضرار", "حد المسؤولية",
    ],
    "governance_approval_control": [
        # EN
        "board", "chairman", "director", "governance", "approval",
        "consent", "control", "authority", "decision", "vote", "voting",
        # FR
        "conseil", "président", "administrateur", "gouvernance",
        "approbation", "consentement", "contrôle", "autorité",
        "décision", "vote",
        # AR
        "مجلس الإدارة", "رئيس", "مدير", "حوكمة", "موافقة",
        "رضا", "سيطرة", "سلطة", "قرار", "تصويت",
    ],
    "dispute_jurisdiction_arbitration": [
        # EN
        "dispute", "claim", "jurisdiction", "venue",
        "governing law", "arbitration", "court", "litigation",
        "attorney fees",
        # FR
        "litige", "réclamation", "juridiction", "compétence",
        "droit applicable", "arbitrage", "tribunal", "contentieux",
        "frais d'avocat",
        # AR
        "نزاع", "مطالبة", "اختصاص", "القانون الواجب التطبيق",
        "تحكيم", "محكمة", "تقاضي", "أتعاب المحاماة",
    ],
    "ip_ownership_license": [
        # EN
        "intellectual property", "ip", "ownership", "license",
        "licence", "assignment", "copyright", "trademark",
        "patent", "work product",
        # FR
        "propriété intellectuelle", "propriété", "licence",
        "cession", "droit d'auteur", "marque", "brevet", "livrable",
        # AR
        "ملكية فكرية", "ملكية", "ترخيص", "تنازل",
        "حقوق النشر", "علامة تجارية", "براءة", "منتج العمل",
    ],
    "performance_service_obligations": [
        # EN
        "obligation", "shall", "must", "service", "performance",
        "deliverable", "service level", "sla", "availability",
        "maintenance", "support",
        # FR
        "obligation", "doit", "service", "performance", "livrable",
        "niveau de service", "disponibilité", "maintenance", "support",
        # AR
        "التزام", "يلتزم", "يجب", "خدمة", "أداء", "مخرج",
        "مستوى الخدمة", "توفر", "صيانة", "دعم",
    ],
}


MIN_GROUP_CONFIDENCE = 0.55
SECONDARY_GROUP_THRESHOLD = 0.72


def build_clause_groups(clauses: list[dict]) -> dict:
    buckets: dict[str, list[dict]] = {}

    seen_titles = set()

    for clause in clauses:
        title = str(
            clause.get("title")
            or clause.get("clause_title")
            or ""
        )

        reference = str(
            clause.get("clause_reference")
            or clause.get("reference")
            or ""
        )

        body = " ".join([
            str(clause.get("quoted_text") or ""),
            str(clause.get("original_text") or ""),
            str(clause.get("clause_text") or ""),
            str(clause.get("explanation_simple") or ""),
        ])

        scores = score_groups(
            title=title,
            reference=reference,
            body=body,
        )

        primary_group = max(
            scores,
            key=scores.get,
        )

        best_score = float(
            scores[primary_group]
        )

        if best_score < MIN_GROUP_CONFIDENCE:

            text = " ".join([
                title,
                reference,
                body,
            ])

            ontology_domains = detect_legal_domains(text)

            if ontology_domains:
                primary_group = ontology_domains[0]

            else:
                primary_group = "other"

        secondary_groups = []

        primary_score = float(
            scores.get(
                primary_group,
                0,
            )
        )

        for name, score in scores.items():

            if name == primary_group:
                continue

            if primary_score <= 0:
                continue

            similarity = (
                score / primary_score
            )

            if similarity >= SECONDARY_GROUP_THRESHOLD:
                secondary_groups.append(name)

        normalized = normalize_text(title)

        if normalized in seen_titles:
            continue

        seen_titles.add(normalized)

        clause["primary_group"] = primary_group
        clause["secondary_groups"] = secondary_groups

        buckets.setdefault(
            primary_group,
            [],
        ).append(clause)

    return {
        "groups": [
            {
                "name": name,
                "count": len(items),
                "clauses": items,
            }
            for name, items in buckets.items()
            if items
        ]
    }


def score_groups(
    title: str,
    reference: str = "",
    body: str = "",
) -> dict[str, int]:

    title_text = str(title or "").lower()
    reference_text = str(reference or "").lower()
    body_text = str(body or "").lower()

    return {
        name: (
            score_terms(title_text, terms) * 3
            + score_terms(reference_text, terms) * 2
            + score_terms(body_text, terms)
        )
        for name, terms in DOMAIN_TERMS.items()
    }


def score_terms(
    text: str,
    terms: list[str],
) -> int:
    return sum(
        1
        for term in terms
        if term in text
    )
