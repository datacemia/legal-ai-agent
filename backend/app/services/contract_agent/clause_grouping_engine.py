from app.services.contract_agent.legal_ontology import (
    detect_legal_domains,
)


def normalize_text(text: str) -> str:
    return " ".join(
        str(text or "").lower().strip().split()
    )


# Universal, contract-family-neutral clause grouping taxonomy.
# This file intentionally avoids treating restrictive covenants
# as Employment/HR by default, because non-compete, non-solicitation,
# non-circumvention and exclusivity clauses appear across many
# commercial contract families internationally.
DOMAIN_TERMS = {
    "commercial_finance": [
        # EN
        "payment", "payments", "pricing", "price", "invoice", "tax",
        "late payment", "refund", "expense", "fees", "fee",
        "commission", "bonus", "royalties", "royalty", "interest",
        "service credits", "service credit", "credit note",
        # FR
        "paiement", "prix", "facture", "taxe", "retard de paiement",
        "remboursement", "frais", "commission", "prime", "redevance",
        "intérêt", "avoirs", "crédit de service",
        # AR
        "الدفع", "السعر", "فاتورة", "ضريبة", "رسوم", "عمولة",
        "مكافأة", "فائدة", "إتاوة", "ائتمان الخدمة", "رصيد الخدمة",
    ],

    "contract_lifecycle": [
        # EN
        "term", "duration", "renewal", "automatic renewal", "termination",
        "notice", "default", "cure period", "expiration", "non-renewal",
        "termination for cause", "termination for convenience",
        # FR
        "durée", "renouvellement", "renouvellement automatique",
        "résiliation", "préavis", "défaut", "délai de correction",
        "expiration", "non-renouvellement",
        # AR
        "المدة", "التجديد", "التجديد التلقائي", "إنهاء", "فسخ",
        "إشعار", "إخلال", "مهلة تصحيح", "انتهاء", "عدم التجديد",
    ],

    "liability_risk": [
        # EN
        "liability", "limitation of liability", "liability cap",
        "indemnity", "indemnification", "insurance", "warranty",
        "damages", "penalty", "liquidated damages", "force majeure",
        "hold harmless", "consequential damages", "gross negligence",
        "willful misconduct",
        # FR
        "responsabilité", "limitation de responsabilité",
        "plafond de responsabilité", "indemnisation", "assurance",
        "garantie", "dommages", "pénalité", "dommages-intérêts",
        "force majeure", "faute lourde", "faute intentionnelle",
        # AR
        "المسؤولية", "حد المسؤولية", "تعويض", "تأمين", "ضمان",
        "أضرار", "غرامة", "القوة القاهرة", "الإهمال الجسيم",
        "سوء السلوك المتعمد",
    ],

    "ip_licensing": [
        # EN
        "intellectual property", "ip", "ownership", "license", "licence",
        "assignment", "copyright", "trademark", "patent", "work product",
        "deliverables", "invention", "moral rights", "source code",
        # FR
        "propriété intellectuelle", "licence", "cession", "droit d'auteur",
        "marque", "brevet", "livrable", "livrables", "invention",
        "droits moraux", "code source",
        # AR
        "الملكية الفكرية", "ترخيص", "تنازل", "حقوق النشر",
        "علامة تجارية", "براءة", "اختراع", "المخرجات", "الحقوق المعنوية",
        "الشفرة المصدرية",
    ],

    "data_confidentiality": [
        # EN
        "confidentiality", "confidential", "non-disclosure", "trade secret",
        "personal data", "data protection", "privacy", "security incident",
        "security", "processor", "controller", "subprocessor",
        "data processing", "gdpr", "personal information",
        # FR
        "confidentialité", "confidentiel", "non-divulgation",
        "secret commercial", "données personnelles", "protection des données",
        "vie privée", "incident de sécurité", "sécurité", "sous-traitant",
        "responsable du traitement", "traitement des données",
        # AR
        "السرية", "سري", "عدم الإفصاح", "بيانات شخصية", "حماية البيانات",
        "الخصوصية", "حادث أمني", "الأمن", "معالج البيانات",
        "المتحكم", "المعالج الفرعي", "معالجة البيانات",
    ],

    "restrictive_covenants": [
        # EN
        "non-compete", "non compete", "noncompetition", "non-competition",
        "non-solicitation", "non solicitation", "non-solicit",
        "non-dealing", "non dealing", "non-circumvention",
        "non circumvention", "exclusive dealing", "exclusivity",
        "exclusive arrangement", "restraint of trade", "poaching",
        "customer solicitation", "employee solicitation",
        "post-termination restriction", "restrictive covenant",
        # FR
        "non-concurrence", "non concurrence", "non-sollicitation",
        "non sollicitation", "non détournement", "non-contournement",
        "exclusivité", "clause restrictive", "restriction post-contractuelle",
        "débauchage", "sollicitation de clients", "sollicitation des employés",
        # AR
        "عدم المنافسة", "عدم الاستقطاب", "عدم الالتفاف", "الحصرية",
        "قيد تعاقدي", "قيود تعاقدية", "استقطاب العملاء", "استقطاب الموظفين",
        "قيود ما بعد انتهاء العقد",
    ],

    "employment_hr": [
        # EN — true HR/employment terms only
        "employment", "employment agreement", "employment contract",
        "employee", "employer", "salary", "wages", "benefits",
        "vacation", "leave", "working hours", "disciplinary",
        "promotion", "retirement", "severance", "termination of employment",
        "bonus plan", "payroll",
        # FR
        "emploi", "contrat de travail", "employé", "employeur",
        "salarié", "salaire", "avantages", "congés", "temps de travail",
        "licenciement", "indemnité de départ", "paie",
        # AR
        "العمل", "عقد عمل", "الموظف", "صاحب العمل", "راتب",
        "مزايا", "إجازة", "ساعات العمل", "فصل", "تعويض نهاية الخدمة",
        "كشوف الرواتب",
    ],

    "services_operations": [
        # EN
        "services", "service level", "sla", "uptime", "availability",
        "support", "maintenance", "delivery", "acceptance", "performance",
        "change request", "statement of work", "sow", "service credits",
        "remediation", "incident report", "deliver the services",
        # FR
        "services", "niveau de service", "disponibilité", "support",
        "maintenance", "livraison", "acceptation", "performance",
        "demande de changement", "cahier des charges", "crédits de service",
        "remédiation", "rapport d'incident",
        # AR
        "الخدمات", "مستوى الخدمة", "توفر الخدمة", "الجاهزية", "الدعم",
        "الصيانة", "التسليم", "القبول", "الأداء", "طلب تغيير",
        "رصيد الخدمة", "معالجة الخلل", "تقرير الحادث",
    ],

    "governance_compliance": [
        # EN
        "compliance", "anti-bribery", "anti bribery", "sanctions",
        "governance", "committee", "subcontracting", "audit", "audit rights",
        "policies", "regulatory", "framework", "controls", "code of conduct",
        # FR
        "conformité", "anti-corruption", "sanctions", "gouvernance",
        "comité", "sous-traitance", "audit", "droits d'audit",
        "réglementaire", "contrôles", "code de conduite",
        # AR
        "الامتثال", "مكافحة الرشوة", "العقوبات", "الحوكمة", "لجنة",
        "التعاقد من الباطن", "التدقيق", "حقوق التدقيق", "تنظيمي",
        "ضوابط", "مدونة السلوك",
    ],

    "corporate": [
        # EN
        "board", "director", "shareholder", "member", "equity", "shares",
        "voting", "capital", "company", "merger", "acquisition",
        "change of control", "affiliate", "subsidiary", "joint venture",
        # FR
        "conseil d'administration", "administrateur", "actionnaire",
        "membre", "capital", "société", "fusion", "acquisition",
        "changement de contrôle", "filiale", "coentreprise",
        # AR
        "مجلس الإدارة", "مدير", "مساهم", "عضو", "أسهم", "تصويت",
        "رأس المال", "شركة", "اندماج", "استحواذ", "تغيير السيطرة",
        "شركة تابعة", "مشروع مشترك",
    ],

    "real_estate": [
        # EN
        "lease", "rent", "deposit", "premises", "property", "repairs",
        "utilities", "tenant", "landlord", "lessor", "lessee",
        # FR
        "bail", "loyer", "dépôt", "locaux", "bien immobilier",
        "réparations", "charges", "locataire", "bailleur",
        # AR
        "إيجار", "أجرة", "وديعة", "عقار", "إصلاحات", "مستأجر", "مؤجر",
    ],

    "finance_lending": [
        # EN
        "loan", "interest", "collateral", "guarantee", "repayment",
        "acceleration", "borrower", "lender", "security interest",
        "financing", "credit facility",
        # FR
        "prêt", "intérêt", "garantie", "remboursement", "exigibilité",
        "emprunteur", "prêteur", "sûreté", "financement", "crédit",
        # AR
        "قرض", "فائدة", "ضمان", "سداد", "مقترض", "مقرض",
        "ضمان عيني", "تمويل", "تسهيلات ائتمانية",
    ],

    "dispute_resolution": [
        # EN
        "dispute", "governing law", "jurisdiction", "venue", "arbitration",
        "mediation", "court", "litigation", "tribunal", "icc", "aaa",
        "seat of arbitration",
        # FR
        "litige", "droit applicable", "juridiction", "tribunal",
        "arbitrage", "médiation", "contentieux", "siège de l'arbitrage",
        # AR
        "نزاع", "القانون الواجب التطبيق", "اختصاص", "محكمة",
        "تحكيم", "وساطة", "تقاضي", "هيئة التحكيم", "مقر التحكيم",
    ],

    "general_provisions": [
        # EN
        "parties", "party", "definitions", "interpretation", "notices",
        "entire agreement", "amendment", "severability", "waiver",
        "counterparts", "signatures", "headings",
        # FR
        "parties", "définitions", "interprétation", "notifications",
        "intégralité de l'accord", "modification", "divisibilité",
        "renonciation", "exemplaires", "signatures", "titres",
        # AR
        "الأطراف", "طرف", "التعاريف", "التفسير", "الإشعارات",
        "الاتفاق الكامل", "التعديل", "قابلية الفصل", "التنازل",
        "التوقيعات", "العناوين",
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
    "restrictive_covenants": {
        "en": "Restrictive Covenants",
        "fr": "Clauses restrictives",
        "ar": "القيود التعاقدية",
    },
    "employment_hr": {
        "en": "Restrictive Covenants & Personnel",
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
    "corporate": {
        "en": "Corporate & Ownership",
        "fr": "Société et gouvernance capitalistique",
        "ar": "الشركات والملكية",
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


PARTIES_TITLES = {
    "parties",
    "party",
    "article 1 - parties",
    "article 1 parties",
    "les parties",
    "الأطراف",
}


# Some domain terms are legally stronger than generic body matches.
# These explicit title rules prevent terms like "employee" inside a
# non-solicitation clause from making the whole clause Employment/HR.
TITLE_PRIORITY_RULES = {
    "restrictive_covenants": [
        "non-compete", "non compete", "non-solicitation", "non solicitation",
        "non-circumvention", "non circumvention", "non-dealing", "exclusivity",
        "restrictive covenant", "non-concurrence", "non-sollicitation",
        "non sollicitation", "عدم المنافسة", "عدم الاستقطاب", "الحصرية",
    ],
    "services_operations": [
        "service level", "service levels", "uptime", "availability",
        "support", "maintenance", "services and service levels",
        "niveau de service", "disponibilité", "مستوى الخدمة", "توفر الخدمة",
    ],
    "data_confidentiality": [
        "data protection", "data processing", "security incident",
        "security measures", "subprocessor", "confidentiality",
        "protection des données", "traitement des données",
        "incident de sécurité", "confidentialité", "حماية البيانات",
        "معالجة البيانات", "حادث أمني", "السرية",
    ],
    "liability_risk": [
        "liability", "limitation of liability", "indemnification",
        "indemnity", "insurance", "responsabilité", "indemnisation",
        "المسؤولية", "تعويض",
    ],
    "dispute_resolution": [
        "dispute", "arbitration", "mediation", "governing law",
        "jurisdiction", "litige", "arbitrage", "médiation", "نزاع", "تحكيم",
    ],
    "employment_hr": [
        "employment", "employment duties", "compensation", "salary",
        "benefits", "vacation", "termination of employment",
        "contrat de travail", "salaire", "congés", "عقد عمل", "راتب",
    ],
}



GROUP_PRIORITY = [
    "liability_risk",
    "data_confidentiality",
    "services_operations",
    "commercial_finance",
    "ip_licensing",
    "contract_lifecycle",
    "governance_compliance",
    "dispute_resolution",
    "finance_lending",
    "corporate",
    "real_estate",
    "restrictive_covenants",
    "employment_hr",
    "general_provisions",
]


def normalize_language(language: str) -> str:
    language = str(language or "en").lower().strip()

    if language in {"en", "fr", "ar"}:
        return language

    return "en"


def safe_group_label(
    name: str,
    language: str = "en",
) -> str:
    language = normalize_language(language)

    labels = GROUP_LABELS.get(name, {})

    return (
        labels.get(language)
        or labels.get("en")
        or name
    )


def stable_best_group(
    scores: dict[str, int],
) -> str:
    if not scores:
        return "general_provisions"

    best_score = max(scores.values())

    candidates = [
        group
        for group, score in scores.items()
        if score == best_score
    ]

    if len(candidates) == 1:
        return candidates[0]

    for group in GROUP_PRIORITY:
        if group in candidates:
            return group

    return sorted(candidates)[0]


def build_clause_groups(
    clauses: list[dict],
    language: str = "en",
    party_roles: dict | None = None,
) -> dict:
    language = normalize_language(language)

    role_family = ""
    if isinstance(party_roles, dict):
        role_family = str(party_roles.get("family") or "").lower().strip()

    is_employment_contract = role_family == "employment"

    buckets: dict[str, list[dict]] = {}
    seen_titles = set()

    for clause in clauses:
        if not isinstance(clause, dict):
            continue

        clause = dict(clause)

        title = str(
            clause.get("title")
            or clause.get("clause_title")
            or ""
        )

        normalized_title = normalize_text(title)

        if normalized_title in PARTIES_TITLES:
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

            primary_group, secondary_groups = classify_clause_group(
                title=title,
                reference=reference,
                body=body,
            )

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
                "name": safe_group_label(name, language),
                "key": name,
                "count": len(items),
                "clauses": items,
            }
            for name, items in buckets.items()
            if items
        ]
    }


def classify_clause_group(
    title: str,
    reference: str = "",
    body: str = "",
) -> tuple[str, list[str]]:
    title_text = normalize_text(title)
    reference_text = normalize_text(reference)
    body_text = normalize_text(body)
    full_text = " ".join([title_text, reference_text, body_text])

    priority_group = detect_priority_group_from_title(title_text)

    scores = score_groups(
        title=title,
        reference=reference,
        body=body,
    )

    if priority_group:
        primary_group = priority_group
    else:
        primary_group = stable_best_group(scores)

        best_score = float(
            scores[primary_group]
        )

        if best_score < MIN_GROUP_CONFIDENCE:
            ontology_domains = detect_legal_domains(full_text)

            if ontology_domains:
                primary_group = normalize_ontology_domain(
                    ontology_domains[0]
                )
            else:
                primary_group = "general_provisions"

    secondary_groups = build_secondary_groups(
        scores=scores,
        primary_group=primary_group,
    )

    return primary_group, secondary_groups


def detect_priority_group_from_title(title_text: str) -> str | None:
    if not title_text:
        return None

    for group, terms in TITLE_PRIORITY_RULES.items():
        if any(term in title_text for term in terms):
            return group

    return None


def normalize_ontology_domain(domain: str) -> str:
    value = normalize_text(domain).replace(" ", "_")

    aliases = {
        "data_privacy": "data_confidentiality",
        "privacy": "data_confidentiality",
        "data_protection": "data_confidentiality",
        "confidentiality": "data_confidentiality",
        "ip": "ip_licensing",
        "intellectual_property": "ip_licensing",
        "licensing": "ip_licensing",
        "liability": "liability_risk",
        "risk": "liability_risk",
        "employment": "employment_hr",
        "hr": "employment_hr",
        "restrictive_covenant": "restrictive_covenants",
        "restrictive_covenants": "restrictive_covenants",
        "post_termination_restrictions": "restrictive_covenants",
        "services": "services_operations",
        "operations": "services_operations",
        "dispute": "dispute_resolution",
        "dispute_resolution": "dispute_resolution",
        "commercial": "commercial_finance",
        "finance": "commercial_finance",
    }

    return aliases.get(value, value if value in DOMAIN_TERMS else "general_provisions")


def build_secondary_groups(
    scores: dict[str, int],
    primary_group: str,
) -> list[str]:
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

        similarity = score / primary_score

        if similarity >= SECONDARY_GROUP_THRESHOLD:
            secondary_groups.append(name)

    return secondary_groups


def score_groups(
    title: str,
    reference: str = "",
    body: str = "",
) -> dict[str, int]:
    title_text = normalize_text(title)
    reference_text = normalize_text(reference)
    body_text = normalize_text(body)

    return {
        name: (
            score_terms(title_text, terms) * 4
            + score_terms(reference_text, terms) * 2
            + score_terms(body_text, terms)
        )
        for name, terms in DOMAIN_TERMS.items()
    }


def score_terms(
    text: str,
    terms: list[str],
) -> int:
    normalized_terms = [normalize_text(term) for term in terms]

    return sum(
        1
        for term in normalized_terms
        if term and term in text
    )
