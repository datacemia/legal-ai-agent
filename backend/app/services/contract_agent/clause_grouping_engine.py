from app.services.contract_agent.legal_ontology import (
    detect_legal_domains,
)


def normalize_text(text: str) -> str:
    return " ".join(
        str(text or "").lower().strip().split()
    )


DOMAIN_TERMS = {
    "commercial_finance": [
        "payment", "pricing", "invoice", "tax", "late payment", "refund",
        "expense", "fees", "commission", "bonus", "royalties",
        "paiement", "prix", "facture", "taxe", "retard de paiement",
        "remboursement", "frais", "commission", "prime",
        "الدفع", "السعر", "فاتورة", "ضريبة", "رسوم", "عمولة", "مكافأة",
    ],

    "contract_lifecycle": [
        "term", "duration", "renewal", "termination", "notice", "default",
        "cure period", "expiration", "non-renewal",
        "durée", "renouvellement", "résiliation", "préavis", "défaut",
        "délai de correction", "expiration",
        "المدة", "التجديد", "إنهاء", "فسخ", "إشعار", "إخلال",
    ],

    "liability_risk": [
        "liability", "limitation of liability", "indemnity", "insurance",
        "warranty", "damages", "penalty", "force majeure",
        "responsabilité", "limitation de responsabilité", "indemnisation",
        "assurance", "garantie", "dommages", "pénalité", "force majeure",
        "المسؤولية", "حد المسؤولية", "تعويض", "تأمين", "ضمان",
        "أضرار", "غرامة", "القوة القاهرة",
    ],

    "ip_licensing": [
        "intellectual property", "ip", "ownership", "license", "assignment",
        "copyright", "trademark", "patent", "work product", "invention",
        "propriété intellectuelle", "licence", "cession", "droit d'auteur",
        "marque", "brevet", "livrable", "invention",
        "الملكية الفكرية", "ترخيص", "تنازل", "حقوق النشر", "علامة تجارية",
        "براءة", "اختراع",
    ],

    "data_confidentiality": [
        "confidentiality", "confidential", "non-disclosure", "trade secret",
        "personal data", "data protection", "privacy", "security",
        "confidentialité", "confidentiel", "non-divulgation",
        "secret commercial", "données personnelles", "protection des données",
        "vie privée", "sécurité",
        "السرية", "سري", "عدم الإفصاح", "بيانات شخصية", "حماية البيانات",
        "الخصوصية", "الأمن",
    ],

    "employment_hr": [
        "employment", "employee", "employer", "salary", "benefits",
        "vacation", "non-compete", "non-solicitation", "conflict of interest",
        "emploi", "employé", "employeur", "salaire", "avantages",
        "congés", "non-concurrence", "non-sollicitation", "conflit d'intérêt",
        "العمل", "الموظف", "صاحب العمل", "راتب", "مزايا", "إجازة",
        "عدم المنافسة", "عدم الاستقطاب",
    ],

    "services_operations": [
        "services", "service level", "sla", "support", "maintenance",
        "delivery", "acceptance", "performance", "change request",
        "services", "niveau de service", "support", "maintenance",
        "livraison", "acceptation", "performance",
        "الخدمات", "مستوى الخدمة", "الدعم", "الصيانة", "التسليم",
        "القبول", "الأداء",
    ],

    "governance_compliance": [
        "assignment", "change of control", "compliance", "anti-bribery",
        "sanctions", "governance", "subcontracting", "audit",
        "cession", "changement de contrôle", "conformité", "sanctions",
        "gouvernance", "sous-traitance", "audit",
        "التنازل", "تغيير السيطرة", "الامتثال", "العقوبات", "الحوكمة",
        "التعاقد من الباطن", "التدقيق",
    ],

    "real_estate": [
        "lease", "rent", "deposit", "premises", "property", "repairs",
        "utilities", "tenant", "landlord",
        "bail", "loyer", "dépôt", "locaux", "bien immobilier",
        "réparations", "charges", "locataire", "bailleur",
        "إيجار", "أجرة", "وديعة", "عقار", "إصلاحات", "مستأجر", "مؤجر",
    ],

    "finance_lending": [
        "loan", "interest", "collateral", "guarantee", "repayment",
        "acceleration", "borrower", "lender",
        "prêt", "intérêt", "garantie", "remboursement", "exigibilité",
        "emprunteur", "prêteur",
        "قرض", "فائدة", "ضمان", "سداد", "مقترض", "مقرض",
    ],

    "dispute_resolution": [
        "dispute", "governing law", "jurisdiction", "venue", "arbitration",
        "mediation", "court", "litigation",
        "litige", "droit applicable", "juridiction", "tribunal",
        "arbitrage", "médiation", "contentieux",
        "نزاع", "القانون الواجب التطبيق", "اختصاص", "محكمة",
        "تحكيم", "وساطة", "تقاضي",
    ],

    "general_provisions": [
        "parties", "party", "definitions", "interpretation", "notices",
        "assignment", "entire agreement", "amendment", "severability",
        "waiver", "counterparts",

        "parties", "définitions", "interprétation", "notifications",
        "cession", "intégralité de l'accord", "modification",
        "divisibilité", "renonciation", "exemplaires",

        "الأطراف", "طرف", "التعاريف", "التفسير", "الإشعارات",
        "التنازل", "الاتفاق الكامل", "التعديل", "قابلية الفصل",
    ],
}


GROUP_LABELS = {
    "commercial_finance": {
        "en": "Commercial & Finance",
        "fr": "Commercial et finance",
        "ar": "الشروط التجارية والمالية",
    },
    "contract_lifecycle": {
        "en": "Contract Lifecycle",
        "fr": "Cycle de vie du contrat",
        "ar": "دورة حياة العقد",
    },
    "liability_risk": {
        "en": "Liability & Risk",
        "fr": "Responsabilité et risques",
        "ar": "المسؤولية والمخاطر",
    },
    "ip_licensing": {
        "en": "IP & Licensing",
        "fr": "Propriété intellectuelle et licences",
        "ar": "الملكية الفكرية والتراخيص",
    },
    "data_confidentiality": {
        "en": "Data & Confidentiality",
        "fr": "Données et confidentialité",
        "ar": "البيانات والسرية",
    },
    "employment_hr": {
        "en": "Employment & HR",
        "fr": "Emploi et ressources humaines",
        "ar": "العمل والموارد البشرية",
    },
    "services_operations": {
        "en": "Services & Operations",
        "fr": "Services et opérations",
        "ar": "الخدمات والعمليات",
    },
    "governance_compliance": {
        "en": "Governance & Compliance",
        "fr": "Gouvernance et conformité",
        "ar": "الحوكمة والامتثال",
    },
    "real_estate": {
        "en": "Real Estate",
        "fr": "Immobilier",
        "ar": "العقارات",
    },
    "finance_lending": {
        "en": "Finance & Lending",
        "fr": "Financement et crédit",
        "ar": "التمويل والإقراض",
    },
    "dispute_resolution": {
        "en": "Dispute Resolution",
        "fr": "Règlement des litiges",
        "ar": "تسوية النزاعات",
    },
    "general_provisions": {
        "en": "General Provisions",
        "fr": "Dispositions générales",
        "ar": "أحكام عامة",
    },
}


MIN_GROUP_CONFIDENCE = 0.55
SECONDARY_GROUP_THRESHOLD = 0.72


def build_clause_groups(clauses: list[dict], language: str = "en") -> dict:
    buckets: dict[str, list[dict]] = {}

    seen_titles = set()

    for clause in clauses:
        title = str(
            clause.get("title")
            or clause.get("clause_title")
            or ""
        )

        normalized_title = normalize_text(title)

        if normalized_title in {
            "parties",
            "party",
            "article 1 - parties",
            "article 1 parties",
            "les parties",
            "الأطراف",
        }:
            primary_group = "general_provisions"
            secondary_groups = []

        else:
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
                    primary_group = "general_provisions"

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

        normalized = normalized_title

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
                "name": GROUP_LABELS.get(name, {}).get(language, name),
                "key": name,
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
