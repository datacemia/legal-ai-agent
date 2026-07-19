REQUIRED_FIELD_ALIASES = {
    "summary": [
        "summary",
        "executive_summary",
        "summary_data",
        "contract_summary",
        "global_summary",
    ],
    "clauses": [
        "clauses",
        "clause_results",
        "analysis",
    ],
    "risk_score": [
        "risk_score",
        "global_risk_score",
        "overall_risk_score",
        "risk",
    ],
    "simplified_version": [
        "simplified_version",
        "simplified",
        "plain_language_summary",
    ],
}


def get_first_available(
    data: dict,
    aliases: list[str],
):
    for key in aliases:
        if key in data:
            return data.get(key)
    return None


def is_empty_value(value) -> bool:
    return value in [None, "", [], {}]


def get_clause_text(clause: dict) -> str:
    if not isinstance(clause, dict):
        return ""

    return " ".join([
        str(clause.get("title", "")),
        str(clause.get("clause_title", "")),
        str(clause.get("original_text", "")),
        str(clause.get("quoted_text", "")),
        str(clause.get("clause_text", "")),
        str(clause.get("text", "")),
    ]).lower()


GENERIC_TYPE_KEYWORDS = {
    "payment": [
        "payment", "salary", "bonus", "fee", "fees", "price",
        "compensation", "invoice", "pay", "reimburse", "rent",
        "royalty", "commission", "subscription",
        "paiement", "salaire", "prime", "prix", "facture",
        "loyer", "redevance", "commission",
        "الدفع", "السداد", "الأجر", "الراتب", "المبلغ",
        "فاتورة", "إيجار", "رسوم", "عمولة",
    ],
    "termination": [
        "terminate", "termination", "expire", "breach", "notice",
        "cure period", "renewal",
        "résiliation", "expiration", "rupture", "préavis",
        "délai de régularisation",
        "إنهاء", "فسخ", "انتهاء", "إخلال", "إشعار", "تجديد",
    ],
    "confidentiality": [
        "confidential", "secret", "non-disclosure",
        "confidentiel", "confidentialité", "secret",
        "سري", "سرية", "معلومات سرية", "عدم الإفصاح",
    ],
    "liability": [
        "liability", "indemnify", "indemnity", "damages", "claim",
        "limitation of liability",
        "responsabilité", "indemnisation", "dommages",
        "مسؤولية", "تعويض", "أضرار", "مطالبة",
    ],
    "governing_law": [
        "governing law", "jurisdiction", "laws of", "arbitration",
        "mediation", "court",
        "droit applicable", "juridiction", "arbitrage", "tribunal",
        "القانون الواجب", "الاختصاص", "القانون", "تحكيم", "محكمة",
    ],
    "intellectual_property": [
        "intellectual property", "copyright", "patent",
        "invention", "license", "licence", "deliverables",
        "propriété intellectuelle", "brevet", "licence", "livrables",
        "الملكية الفكرية", "براءة", "ترخيص", "مخرجات العمل",
    ],
    "corporate_governance": [
        "board of directors", "shareholder", "voting",
        "fiduciary", "director", "approval", "consent",
        "conseil d'administration", "actionnaire", "approbation",
        "consentement",
        "مجلس الإدارة", "المساهم", "تصويت", "موافقة",
    ],
    "data_protection": [
        "personal data", "data protection", "data processing",
        "security incident", "data breach", "subprocessor",
        "privacy",
        "données personnelles", "protection des données",
        "traitement des données", "incident de sécurité",
        "violation de données", "sous-traitant",
        "البيانات الشخصية", "حماية البيانات", "معالجة البيانات",
        "حادث أمني", "اختراق البيانات", "الخصوصية",
    ],
    "service_level": [
        "service level", "uptime", "availability", "service credit",
        "support", "maintenance", "incident response",
        "niveau de service", "disponibilité", "crédit de service",
        "support", "maintenance",
        "مستوى الخدمة", "التوافر", "تعويض الخدمة", "الدعم", "الصيانة",
    ],
    "services_operations": [
        "services", "scope of work", "statement of work",
        "deliver", "performance", "change request",
        "services", "périmètre", "énoncé des travaux",
        "livraison", "performance",
        "الخدمات", "نطاق العمل", "بيان العمل", "التسليم", "الأداء",
    ],
    "assignment": [
        "assignment", "assign", "transfer", "delegate",
        "cession", "céder", "transfert", "déléguer",
        "تنازل", "نقل", "تفويض",
    ],
    "audit": [
        "audit", "inspection", "records", "books",
        "audit", "inspection", "registres",
        "تدقيق", "تفتيش", "سجلات",
    ],
    "insurance": [
        "insurance", "policy", "coverage", "insured",
        "assurance", "police", "couverture", "assuré",
        "تأمين", "وثيقة التأمين", "تغطية", "مؤمن عليه",
    ],
    "real_estate": [
        "lease", "rent", "premises", "tenant", "landlord",
        "deposit", "property",
        "bail", "loyer", "locaux", "locataire", "bailleur",
        "dépôt",
        "إيجار", "أجرة", "عقار", "مستأجر", "مؤجر", "وديعة",
    ],
    "finance_lending": [
        "loan", "credit", "borrower", "lender", "interest",
        "collateral", "security interest",
        "prêt", "crédit", "emprunteur", "prêteur", "intérêt",
        "garantie", "sûreté",
        "قرض", "ائتمان", "مقترض", "مقرض", "فائدة", "ضمان",
    ],
    "restrictive_covenants": [
        "non-compete", "non compete", "non-solicitation",
        "exclusive", "exclusivity",
        "non-concurrence", "non-sollicitation", "exclusivité",
        "عدم المنافسة", "عدم الاستقطاب", "الحصرية",
    ],
}


GENERIC_UNSUPPORTED_PHRASES = [
    "could lead to disputes",
    "potential disputes",
    "may lead to disputes",
    "may create uncertainty",
    "could create uncertainty",
    "may limit options",
    "could favor one party",
    "could disadvantage",
    "should be reviewed carefully",
    "important legal or commercial obligations",
    "operational or legal obligations",
    "review with counsel",

    "pourrait entraîner des litiges",
    "risques potentiels",
    "peut créer une incertitude",
    "peut limiter les options",
    "devrait être examiné attentivement",
    "obligations juridiques ou commerciales importantes",

    "قد يؤدي إلى نزاعات",
    "قد يخلق غموضاً",
    "قد يحد من الخيارات",
    "ينبغي مراجعته بعناية",
    "التزامات قانونية أو تجارية مهمة",
]


CONTRACT_KEYWORDS = [
    "contract", "agreement", "party", "parties", "clause",
    "payment", "termination", "liability", "governing law",
    "confidentiality", "obligations", "effective date",

    "contrat", "accord", "partie", "parties", "clause",
    "paiement", "résiliation", "responsabilité",
    "droit applicable", "confidentialité", "obligations",

    "العقد", "عقد", "الطرف", "الأطراف", "المادة", "البند",
    "الدفع", "السداد", "الفسخ", "إنهاء", "الالتزام",
    "القانون", "المسؤولية", "السرية",
]


STRONG_CONTRACT_KEYWORDS = [
    "this agreement", "the parties agree", "terms and conditions",
    "effective date", "governing law", "whereas",

    "le présent contrat", "les parties conviennent",
    "conditions générales", "date d'effet", "droit applicable",

    "اتفق الطرفان", "بموجب هذا العقد", "تاريخ السريان",
    "الشروط والأحكام", "القانون الواجب التطبيق",
]


STRUCTURE_KEYWORDS = [
    "section", "article", "clause", "schedule", "exhibit",
    "whereas", "signature",

    "section", "article", "clause", "annexe", "préambule",
    "signature",

    "المادة", "البند", "الملحق", "التمهيد", "التوقيع",
]


def extract_clauses(result: dict) -> list:
    clauses = get_first_available(
        result,
        REQUIRED_FIELD_ALIASES["clauses"],
    )

    if isinstance(clauses, list):
        return clauses

    if isinstance(clauses, dict):
        if isinstance(clauses.get("results"), list):
            return clauses.get("results")

        if isinstance(clauses.get("clauses"), dict):
            nested_results = clauses.get("clauses", {}).get("results", [])
            if isinstance(nested_results, list):
                return nested_results

        if isinstance(clauses.get("items"), list):
            return clauses.get("items")

    return []


def has_required_field(
    result: dict,
    logical_field: str,
) -> bool:
    value = get_first_available(
        result,
        REQUIRED_FIELD_ALIASES.get(logical_field, [logical_field]),
    )

    return not is_empty_value(value)


def get_result_text(result: dict) -> str:
    return str(
        result.get("text", "")
        or result.get("full_text", "")
        or result.get("raw_text", "")
        or result.get("contract_text", "")
        or ""
    )


def validate_contract_result(result: dict) -> dict:
    issues = []
    score = 100

    if not isinstance(result, dict):
        return {
            "valid": False,
            "score": 0,
            "issues": ["Result must be a dictionary"],
        }

    for field in REQUIRED_FIELD_ALIASES:
        if not has_required_field(result, field):
            issues.append(f"Missing field: {field}")
            score -= 8

    contract_score = (
        result.get("contract_quality_score")
        if result.get("contract_quality_score") is not None
        else result.get("contract_score")
    )

    if (
        contract_score is not None
        and not isinstance(contract_score, int)
    ):
        issues.append("contract score must be integer")
        score -= 10

    clauses = extract_clauses(result)
    clauses_count = len(clauses)

    if clauses_count == 0:
        issues.append("No clauses extracted")
        score -= 20

    weak_detail_count = 0

    for clause in clauses:
        if not isinstance(clause, dict):
            continue

        combined = " ".join([
            str(clause.get("explanation_simple", "")),
            str(clause.get("recommendation", "")),
            str(clause.get("negotiation_advice", "")),
            str(clause.get("legal_insight", "")),
            str(clause.get("market_comparison", "")),
            str(clause.get("safer_alternative", "")),
        ]).lower()

        if any(term in combined for term in GENERIC_UNSUPPORTED_PHRASES):
            weak_detail_count += 1

    if weak_detail_count >= 5:
        issues.append(
            f"Too many generic or unsupported clause analyses: {weak_detail_count}"
        )
        score -= min(25, weak_detail_count * 4)

    elif weak_detail_count:
        issues.append(
            f"Generic or unsupported clause analysis: {weak_detail_count}"
        )
        score -= min(15, weak_detail_count * 5)

    summary_value = get_first_available(
        result,
        REQUIRED_FIELD_ALIASES["summary"],
    )

    summary = str(summary_value or "")

    if len(summary.strip()) < 40:
        issues.append("Summary too short")
        score -= 10

    text = get_result_text(result)

    if (
        len(text.strip()) < 500
        and clauses_count < 3
    ):
        issues.append("Very little text extracted")
        score -= 30

    if result.get("is_probably_contract") is False:
        issues.append("Document does not look like a contract")
        score -= 40

    empty_detail_count = 0

    for clause in clauses:
        if not isinstance(clause, dict):
            continue

        has_details = clause.get("has_details")

        combined_details = " ".join([
            str(clause.get("explanation_simple", "")),
            str(clause.get("legal_insight", "")),
            str(clause.get("recommendation", "")),
            str(clause.get("negotiation_advice", "")),
        ]).lower()

        has_strong_detail = any([
            clause.get("legal_insight"),
            clause.get("recommendation"),
            clause.get("negotiation_advice"),
            clause.get("market_comparison"),
            clause.get("safer_alternative"),
        ])

        if (
            has_details
            and clause.get("risk_level") != "low"
            and not has_strong_detail
        ):
            empty_detail_count += 1

        if (
            not has_strong_detail
            and any(
                phrase in combined_details
                for phrase in GENERIC_UNSUPPORTED_PHRASES
            )
        ):
            empty_detail_count += 1

    if empty_detail_count:
        issues.append(f"Weak clause details: {empty_detail_count}")
        score -= min(20, empty_detail_count * 5)

    semantic_mismatch_count = 0

    for clause in clauses:
        if not isinstance(clause, dict):
            continue

        clause_type = str(
            clause.get("clause_type", "")
            or clause.get("type", "")
        ).lower()

        keywords = GENERIC_TYPE_KEYWORDS.get(clause_type)

        if not keywords:
            continue

        clause_text = get_clause_text(clause)

        if clause_text and not any(
            keyword in clause_text
            for keyword in keywords
        ):
            semantic_mismatch_count += 1

    if semantic_mismatch_count:
        issues.append(
            f"Possible clause type mismatches: {semantic_mismatch_count}"
        )
        score -= min(15, semantic_mismatch_count * 3)

    score = max(0, min(score, 100))

    return {
        "valid": score >= 75,
        "score": score,
        "issues": issues,
    }


def is_probably_contract(text: str) -> bool:
    text = str(text or "").lower()

    keyword_score = sum(
        1
        for keyword in CONTRACT_KEYWORDS
        if keyword in text
    )

    strong_score = sum(
        1
        for keyword in STRONG_CONTRACT_KEYWORDS
        if keyword in text
    )

    structure_score = sum(
        1
        for keyword in STRUCTURE_KEYWORDS
        if keyword in text
    )

    return (
        keyword_score >= 3
        or (
            strong_score >= 1
            and structure_score >= 1
        )
        or (
            keyword_score >= 2
            and structure_score >= 2
        )
    )

# ---------------------------------------------------------------------------
# International validation extensions
# ---------------------------------------------------------------------------
# Privacy-first: these keywords validate legal coverage only. They do not
# reconstruct, infer, restore, request, or output real identities or personal data.

INTERNATIONAL_GENERIC_TYPE_KEYWORDS = {
    "force_majeure": [
        "force majeure", "act of god", "natural disaster", "unforeseeable event",
        "beyond reasonable control", "pandemic", "epidemic", "war", "strike",
        "cas de force majeure", "cas fortuit", "catastrophe naturelle",
        "événement imprévisible", "hors du contrôle raisonnable", "pandémie",
        "épidémie", "guerre", "grève",
        "القوة القاهرة", "حدث غير متوقع", "خارج السيطرة المعقولة",
        "كارثة طبيعية", "جائحة", "وباء", "حرب", "إضراب",
    ],
    "tax": [
        "tax", "taxes", "vat", "gst", "withholding", "gross-up",
        "tax invoice", "sales tax", "duties", "levies",
        "impôt", "impôts", "taxe", "tva", "retenue à la source",
        "majoration fiscale", "facture fiscale", "droits", "prélèvements",
        "ضريبة", "ضرائب", "القيمة المضافة", "اقتطاع", "استقطاع",
        "تعويض ضريبي", "فاتورة ضريبية", "رسوم", "جبايات",
    ],
    "warranties": [
        "warranty", "warranties", "representation", "representations",
        "representations and warranties", "as is", "disclaimer of warranty",
        "fitness for purpose", "merchantability", "defect warranty",
        "garantie", "garanties", "déclaration", "déclarations",
        "déclarations et garanties", "en l'état", "exclusion de garantie",
        "aptitude à l'usage", "vice",
        "ضمان", "ضمانات", "إقرار", "إقرارات",
        "الإقرارات والضمانات", "كما هو", "استبعاد الضمان",
        "ملاءمة للغرض", "عيب",
    ],
    "renewal": [
        "renewal", "automatic renewal", "auto-renewal", "renewal term",
        "extension term", "successive terms", "non-renewal",
        "renouvellement", "reconduction automatique",
        "période de renouvellement", "durée de renouvellement",
        "non-renouvellement",
        "تجديد", "تجديد تلقائي", "مدة التجديد",
        "فترات متتالية", "عدم التجديد",
    ],
    "suspension": [
        "suspension", "suspend", "suspend services", "service suspension",
        "reinstatement", "restore service", "access suspension",
        "suspendre", "suspendre les services", "rétablissement",
        "restaurer le service",
        "تعليق", "يعلق", "تعليق الخدمات", "استئناف الخدمة",
        "إعادة الخدمة", "تعليق الوصول",
    ],
    "business_continuity": [
        "business continuity", "disaster recovery", "bcp", "drp",
        "backup", "restore", "recovery time objective", "rto",
        "recovery point objective", "rpo", "contingency plan",
        "continuité d'activité", "reprise après sinistre",
        "sauvegarde", "restauration", "plan de continuité",
        "خطة استمرارية الأعمال", "استمرارية الأعمال",
        "التعافي من الكوارث", "نسخ احتياطي", "استعادة", "خطة طوارئ",
    ],
    "publicity": [
        "publicity", "press release", "public announcement", "use of name",
        "logo", "trademark in marketing", "case study", "reference customer",
        "publicité", "communiqué de presse", "annonce publique",
        "utilisation du nom", "logo", "étude de cas", "référence client",
        "دعاية", "بيان صحفي", "إعلان عام", "استخدام الاسم",
        "الشعار", "دراسة حالة", "عميل مرجعي",
    ],
    "severability": [
        "severability", "invalid provision", "unenforceable provision",
        "severed", "valid substitute", "remaining provisions",
        "divisibilité", "clause invalide", "clause inapplicable",
        "séparée", "disposition de remplacement",
        "قابلية الفصل", "حكم غير صحيح", "حكم غير قابل للتنفيذ",
        "فصل الحكم", "حكم بديل", "باقي الأحكام",
    ],
    "survival": [
        "survival", "survive termination", "survive expiry",
        "post-termination obligations", "continue after termination",
        "survie", "survivent à la résiliation",
        "obligations postérieures à la résiliation",
        "continuer après la résiliation",
        "استمرار", "تستمر بعد الإنهاء", "تستمر بعد الانقضاء",
        "التزامات ما بعد الإنهاء",
    ],
    "amendment": [
        "amendment", "amendments", "modified only in writing",
        "change order", "variation", "written modification",
        "modification", "avenant", "modifié uniquement par écrit",
        "ordre de modification", "changement",
        "تعديل", "تعديلات", "لا يعدل إلا كتابة",
        "أمر تغيير", "تغيير كتابي",
    ],
    "waiver": [
        "waiver", "no waiver", "failure to enforce",
        "delay in exercising", "waive", "single waiver",
        "renonciation", "absence de renonciation",
        "défaut d'exercice", "retard dans l'exercice", "renoncer",
        "تنازل", "عدم التنازل", "عدم ممارسة الحق",
        "التأخر في ممارسة الحق", "يتنازل",
    ],
    "export_control": [
        "export control", "sanctions", "trade sanctions",
        "restricted party", "embargo", "anti-boycott", "dual use",
        "contrôle des exportations", "sanctions", "embargo",
        "partie restreinte", "double usage",
        "ضوابط التصدير", "عقوبات", "حظر",
        "طرف مقيد", "استخدام مزدوج",
    ],
    "open_source": [
        "open source", "copyleft", "oss", "third-party software",
        "source code", "software component",
        "logiciel libre", "logiciel tiers", "code source",
        "برنامج مفتوح المصدر", "كود مفتوح", "كود المصدر",
        "برنامج طرف ثالث",
    ],
    "escrow": [
        "escrow", "source code escrow", "deposit materials",
        "release condition",
        "séquestre", "séquestre de code source",
        "dépôt", "condition de libération",
        "ضمان الكود", "إيداع", "مواد مودعة", "شرط الإفراج",
    ],
    "transition_assistance": [
        "transition assistance", "exit assistance", "handover",
        "migration", "knowledge transfer", "wind-down",
        "assistance de transition", "assistance à la sortie",
        "transfert de connaissances", "migration", "remise",
        "مساعدة انتقالية", "مساعدة الخروج",
        "نقل المعرفة", "ترحيل", "تسليم انتقالي",
    ],
}


INTERNATIONAL_CONTRACT_KEYWORDS = [
    "force majeure", "warranty", "warranties", "tax", "taxes",
    "assignment", "notice", "arbitration", "data processing",
    "service level", "insurance", "renewal", "suspension",
    "business continuity", "disaster recovery", "severability",
    "survival", "amendment", "waiver", "export control",
    "sanctions", "open source", "escrow", "transition assistance",

    "force majeure", "garantie", "garanties", "impôt", "taxe",
    "cession", "notification", "arbitrage", "traitement des données",
    "niveau de service", "assurance", "renouvellement", "suspension",
    "continuité d'activité", "reprise après sinistre", "divisibilité",
    "survie", "avenant", "renonciation", "contrôle des exportations",
    "sanctions", "logiciel libre", "séquestre", "assistance de transition",

    "القوة القاهرة", "ضمان", "ضمانات", "ضريبة", "ضرائب",
    "تنازل", "إشعار", "تحكيم", "معالجة البيانات",
    "مستوى الخدمة", "تأمين", "تجديد", "تعليق",
    "استمرارية الأعمال", "التعافي من الكوارث", "قابلية الفصل",
    "استمرار", "تعديل", "تنازل", "ضوابط التصدير",
    "عقوبات", "برنامج مفتوح المصدر", "إيداع", "مساعدة انتقالية",
]


INTERNATIONAL_STRONG_CONTRACT_KEYWORDS = [
    "this agreement", "the parties agree", "governing law",
    "data processing agreement", "service level agreement",
    "force majeure", "representations and warranties",

    "le présent contrat", "les parties conviennent", "droit applicable",
    "accord de traitement des données", "accord de niveau de service",
    "force majeure", "déclarations et garanties",

    "بموجب هذا العقد", "اتفق الطرفان", "القانون الواجب التطبيق",
    "اتفاقية معالجة البيانات", "اتفاقية مستوى الخدمة",
    "القوة القاهرة", "الإقرارات والضمانات",
]


def _merge_unique(base: list, extra: list) -> list:
    return list(dict.fromkeys([*base, *extra]))


def _extend_international_validator_keywords() -> None:
    for clause_type, keywords in INTERNATIONAL_GENERIC_TYPE_KEYWORDS.items():
        GENERIC_TYPE_KEYWORDS[clause_type] = _merge_unique(
            GENERIC_TYPE_KEYWORDS.get(clause_type, []),
            keywords,
        )

    CONTRACT_KEYWORDS[:] = _merge_unique(
        CONTRACT_KEYWORDS,
        INTERNATIONAL_CONTRACT_KEYWORDS,
    )

    STRONG_CONTRACT_KEYWORDS[:] = _merge_unique(
        STRONG_CONTRACT_KEYWORDS,
        INTERNATIONAL_STRONG_CONTRACT_KEYWORDS,
    )


_extend_international_validator_keywords()

