"""
Central contract taxonomy.

This module centralizes clause type metadata so the contract agent can
reuse the same signals, risk defaults, reasoning keys, and negotiation
triggers across:
- rule-based risk calibration
- clause reasoning templates
- fallback legal insight
- negotiation advice
- frontend labeling

Goal:
Reduce duplicated mappings and keep multilingual clause classification
consistent across 1000+ contracts.
"""

import re


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def build_clause_type(
    en: str,
    fr: str,
    ar: str,
    signals: list[str],
    *,
    risk_default: str = "low",
    materiality: str = "medium",
    reasoning_key: str = "general",
    critical: bool = False,
    negotiation_type: str | None = None,
    excluded_contexts: list[str] | None = None,
    description: dict | None = None,
) -> dict:
    definition = {
        "label": {
            "en": en,
            "fr": fr,
            "ar": ar,
        },
        "signals": signals,
        "risk_default": risk_default,
        "materiality": materiality,
        "reasoning_key": reasoning_key,
        "critical": critical,
        "description": description or {},
    }

    if negotiation_type:
        definition["negotiation_type"] = negotiation_type

    if excluded_contexts:
        definition["excluded_contexts"] = excluded_contexts

    return definition


CLAUSE_TYPES = {
    "payment": build_clause_type(
        "Payment",
        "Paiement",
        "الدفع",
        [
            "payment", "pay", "paid", "invoice", "fee", "fees", "pricing",
            "price", "interest", "late payment", "principal amount",
            "loan amount", "repayment", "reimbursement", "expenses",
            "expense reimbursement", "business expenses", "paid by",
            "pay or reimburse",

            "paiement", "payer", "payé", "facture", "frais", "prix",
            "intérêt", "retard de paiement", "capital", "montant du prêt",
            "remboursement", "remboursement de frais", "notes de frais",

            "الدفع", "السداد", "فاتورة", "الفاتورة", "الرسوم",
            "الأسعار", "الفائدة", "تأخر الدفع", "رأس المال",
            "مبلغ القرض", "استرداد", "تعويض المصاريف", "مصاريف",
        ],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "pricing": build_clause_type(
        "Pricing",
        "Prix",
        "التسعير",
        ["pricing", "price", "prices", "tariff", "rate", "prix", "tarif", "taux", "التسعير", "السعر", "الأسعار", "التعرفة"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "invoice": build_clause_type(
        "Invoice",
        "Facture",
        "الفاتورة",
        ["invoice", "invoicing", "billing", "facture", "facturation", "فاتورة", "الفاتورة", "الفوترة"],
        risk_default="low",
        materiality="medium",
        reasoning_key="payment",
    ),

    "tax": build_clause_type(
        "Tax",
        "Fiscalité",
        "الضريبة",
        ["tax", "taxes", "vat", "withholding tax", "fiscal", "impôt", "taxe", "tva", "retenue à la source", "ضريبة", "الضرائب", "ضريبة القيمة المضافة"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "late_payment": build_clause_type(
        "Late Payment",
        "Retard de paiement",
        "تأخر الدفع",
        ["late payment", "overdue", "past due", "default interest", "retard de paiement", "paiement en retard", "intérêts de retard", "تأخر الدفع", "الدفع المتأخر"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "refund": build_clause_type(
        "Refund",
        "Remboursement",
        "الاسترداد",
        ["refund", "refundable", "reimburse", "reimbursement", "remboursement", "remboursable", "استرداد", "قابل للاسترداد"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="payment",
    ),

    "fees": build_clause_type(
        "Fees",
        "Frais",
        "الرسوم",
        ["fees", "fee", "charges", "costs", "frais", "coûts", "charges", "الرسوم", "التكاليف"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "commission": build_clause_type(
        "Commission",
        "Commission",
        "العمولة",
        ["commission", "sales commission", "commission payment", "عمولة", "العمولة"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "royalties": build_clause_type(
        "Royalties",
        "Redevances",
        "الإتاوات",
        ["royalty", "royalties", "license fee", "redevance", "redevances", "إتاوة", "الإتاوات"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "termination": build_clause_type(
        "Termination",
        "Résiliation",
        "الإنهاء",
        [
            "termination", "terminate", "immediate termination",
            "notice period", "cure period", "default termination",
            "résiliation", "résilier", "résiliation immédiate",
            "préavis", "délai de régularisation",
            "إنهاء", "فسخ", "إنهاء فوري", "إشعار", "مهلة معالجة",
        ],
        risk_default="medium",
        materiality="high",
        reasoning_key="termination",
        critical=True,
    ),

    "term": build_clause_type(
        "Term",
        "Durée",
        "المدة",
        ["term", "contract term", "effective period", "durée", "durée du contrat", "مدة", "مدة العقد"],
        materiality="medium",
        reasoning_key="termination",
    ),

    "duration": build_clause_type(
        "Duration",
        "Durée",
        "المدة",
        ["duration", "period", "fixed term", "durée", "période", "durée déterminée", "مدة", "فترة"],
        materiality="medium",
        reasoning_key="termination",
    ),

    "renewal": build_clause_type(
        "Renewal",
        "Renouvellement",
        "التجديد",
        ["renewal", "renew", "extension", "renouvellement", "renouveler", "prolongation", "تجديد", "تمديد"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="termination",
        critical=True,
    ),

    "pricing_adjustment": build_clause_type(
        "Pricing Adjustment",
        "Ajustement tarifaire",
        "تعديل الأسعار",
        [
            "increase fees", "increase the fees", "fee increase",
            "price increase", "adjust pricing", "pricing adjustment",
            "unilaterally increase", "raise fees", "raise prices",
            "augmenter les frais", "augmentation des frais",
            "augmentation tarifaire", "ajustement tarifaire",
            "ajustement des prix", "hausse unilatérale", "unilatéralement",
            "زيادة الرسوم", "رفع الرسوم", "تعديل الأسعار", "زيادة الأسعار",
        ],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
    ),


    "automatic_renewal": build_clause_type(
        "Automatic Renewal",
        "Renouvellement automatique",
        "التجديد التلقائي",
        [
            "automatic renewal", "renews automatically", "renewing automatically",
            "auto-renewal", "shall automatically renew",
            "renouvellement automatique", "se renouvelle automatiquement",
            "se renouvelant automatiquement", "reconduction automatique",
            "تجديد تلقائي", "يتجدد تلقائيا", "يتجدد تلقائياً", "تلقائياً",
        ],
        risk_default="medium",
        materiality="high",
        reasoning_key="termination",
        critical=True,
    ),

    "termination_for_cause": build_clause_type(
        "Termination for Cause",
        "Résiliation pour motif",
        "الإنهاء لسبب",
        ["termination for cause", "for cause", "material breach", "résiliation pour motif", "faute grave", "manquement substantiel", "إنهاء لسبب", "إخلال جوهري"],
        risk_default="medium",
        materiality="high",
        reasoning_key="termination",
        critical=True,
    ),

    "termination_for_convenience": build_clause_type(
        "Termination for Convenience",
        "Résiliation de convenance",
        "الإنهاء دون سبب",
        ["termination for convenience", "without cause", "terminate at any time", "résiliation de convenance", "sans motif", "résilier à tout moment", "إنهاء دون سبب", "إنهاء في أي وقت"],
        risk_default="medium",
        materiality="high",
        reasoning_key="termination",
        critical=True,
    ),

    "cure_period": build_clause_type(
        "Cure Period",
        "Délai de correction",
        "مهلة التصحيح",
        ["cure period", "period to cure", "remedy breach", "délai de correction", "délai de régularisation", "corriger le manquement", "مهلة تصحيح", "معالجة الإخلال"],
        risk_default="low",
        materiality="medium",
        reasoning_key="termination",
    ),

    "liability": build_clause_type(
        "Liability",
        "Responsabilité",
        "المسؤولية",
        [
            "liability", "liable", "liability cap", "limitation of liability",
            "unlimited liability", "indirect damages", "consequential damages",
            "incidental damages", "punitive damages", "financial exposure",
            "responsabilité", "responsable", "plafond de responsabilité",
            "limitation de responsabilité", "responsabilité illimitée",
            "dommages indirects", "dommages consécutifs", "dommages accessoires",
            "exposition financière",
            "المسؤولية", "مسؤول", "حد المسؤولية", "مسؤولية غير محدودة",
            "الأضرار غير المباشرة", "الأضرار التبعية", "تعرض مالي",
        ],
        risk_default="medium",
        materiality="high",
        reasoning_key="liability",
        negotiation_type="liability",
        critical=True,
    ),

    "limitation_of_liability": build_clause_type(
        "Limitation of Liability",
        "Limitation de responsabilité",
        "تحديد المسؤولية",
        ["limitation of liability", "liability cap", "cap on liability", "limited liability", "limitation de responsabilité", "plafond de responsabilité", "حد المسؤولية", "تحديد المسؤولية"],
        risk_default="medium",
        materiality="high",
        reasoning_key="liability",
        critical=True,
    ),

    "limitation_of_liability_exceptions": build_clause_type(
        "Limitation of Liability Exceptions",
        "Exceptions à la limitation de responsabilité",
        "استثناءات الحد من المسؤولية",
        [
            "shall not apply to",
            "not subject to the limitation",
            "excluded from the limitation",
            "exceptions to limitation of liability",
            "carve-out from liability cap",
            "the limitation in section",
            "la limitation ne s'applique pas",
            "non soumise à la limitation",
            "exceptions à la limitation de responsabilité",
            "لا ينطبق الحد",
            "لا تخضع لحد المسؤولية",
            "استثناءات الحد من المسؤولية",
        ],
        risk_default="high",
        materiality="high",
        reasoning_key="liability",
        negotiation_type="liability",
        critical=True,
        description={
            "en": "This clause identifies situations where liability limitations do not apply and may significantly increase each party's financial exposure.",
            "fr": "Cette clause identifie les situations dans lesquelles les limitations de responsabilité ne s'appliquent pas et peuvent augmenter fortement l'exposition financière de chaque partie.",
            "ar": "يحدد هذا البند الحالات التي لا تنطبق فيها حدود المسؤولية وقد يزيد بشكل كبير من التعرض المالي لكل طرف.",
        },
    ),

    "warranty": build_clause_type(
        "Warranty",
        "Garantie",
        "الضمان",
        ["warranty", "warranties", "represents and warrants", "garantie", "garanties", "déclare et garantit", "يقر ويضمن"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
    ),

    "disclaimer": build_clause_type(
        "Disclaimer",
        "Clause de non-garantie",
        "إخلاء المسؤولية",
        ["disclaimer", "as is", "without warranty", "no warranty", "clause de non-garantie", "sans garantie", "tel quel", "إخلاء مسؤولية", "بدون ضمان"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="liability",
        critical=True,
    ),

    "penalty": build_clause_type(
        "Penalty",
        "Pénalité",
        "الغرامة",
        ["penalty", "fine", "penalties", "pénalité", "amende", "غرامة", "جزاء"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "liquidated_damages": build_clause_type(
        "Liquidated Damages",
        "Dommages-intérêts forfaitaires",
        "التعويضات المقطوعة",
        ["liquidated damages", "agreed damages", "dommages-intérêts forfaitaires", "clause pénale", "تعويضات مقطوعة", "تعويض متفق عليه"],
        risk_default="medium",
        materiality="high",
        reasoning_key="liability",
        critical=True,
    ),

    "confidentiality": build_clause_type(
        "Confidentiality",
        "Confidentialité",
        "السرية",
        ["confidentiality", "confidential information", "trade secret", "survive termination", "confidentialité", "information confidentielle", "secret commercial", "السرية", "معلومات سرية", "سر تجاري"],
        risk_default="low",
        materiality="medium",
        reasoning_key="confidentiality",
        critical=True,
    ),

    "intellectual_property": build_clause_type(
        "Intellectual Property",
        "Propriété intellectuelle",
        "الملكية الفكرية",
        [
            "intellectual property", "ip rights", "ownership", "assignment",
            "license", "invention", "patent", "work product",
            "right, title, and interest", "title and interest",
            "pre-existing tools", "methodologies and know-how",
            "propriété intellectuelle", "droits de propriété intellectuelle",
            "cession", "licence", "brevet", "création",
            "tous droits, titres et intérêts", "titre et intérêt",
            "savoir-faire préexistant",
            "الملكية الفكرية", "حقوق الملكية الفكرية", "ترخيص",
            "اختراع", "براءة اختراع",
            "الحقوق والملكية والمصلحة", "الدراية الفنية",
        ],
        risk_default="medium",
        materiality="high",
        reasoning_key="intellectual_property",
        critical=True,
    ),

    "ip_assignment": build_clause_type(
        "IP Assignment",
        "Cession de propriété intellectuelle",
        "التنازل عن الملكية الفكرية",
        ["ip assignment", "assign intellectual property", "assignment of ip", "cession de propriété intellectuelle", "cession des droits", "التنازل عن الملكية الفكرية", "نقل حقوق الملكية الفكرية"],
        risk_default="medium",
        materiality="high",
        reasoning_key="intellectual_property",
        critical=True,
    ),

    "ownership": build_clause_type(
        "Ownership",
        "Propriété",
        "الملكية",
        ["ownership", "owned by", "title to", "propriété", "appartient à", "titularité", "ملكية", "مملوك لـ"],
        risk_default="medium",
        materiality="high",
        reasoning_key="intellectual_property",
        critical=True,
    ),

    "license": build_clause_type(
        "License",
        "Licence",
        "الترخيص",
        ["license", "licence", "licensed", "right to use", "droit d'utilisation", "ترخيص", "حق الاستخدام"],
        risk_default="medium",
        materiality="high",
        reasoning_key="intellectual_property",
        critical=True,
    ),

    "work_product": build_clause_type(
        "Work Product",
        "Livrables",
        "مخرجات العمل",
        ["work product", "deliverables", "works created", "livrables", "produits du travail", "مخرجات العمل", "الأعمال المنتجة"],
        risk_default="medium",
        materiality="high",
        reasoning_key="intellectual_property",
        critical=True,
    ),

    "moral_rights": build_clause_type(
        "Moral Rights",
        "Droits moraux",
        "الحقوق المعنوية",
        ["moral rights", "waiver of moral rights", "droits moraux", "renonciation aux droits moraux", "حقوق معنوية", "التنازل عن الحقوق المعنوية"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="intellectual_property",
        critical=True,
    ),

    "data_protection": build_clause_type(
        "Data Protection",
        "Protection des données",
        "حماية البيانات",
        ["data protection", "personal data", "gdpr", "data breach", "security incident", "cybersecurity", "protection des données", "données personnelles", "violation de données", "incident de sécurité", "cybersécurité", "حماية البيانات", "البيانات الشخصية", "اختراق البيانات", "حادث أمني", "الأمن السيبراني"],
        risk_default="medium",
        materiality="high",
        reasoning_key="data",
        critical=True,
    ),

    "privacy": build_clause_type(
        "Privacy",
        "Vie privée",
        "الخصوصية",
        ["privacy", "private information", "personal information", "vie privée", "informations personnelles", "خصوصية", "معلومات شخصية"],
        risk_default="medium",
        materiality="high",
        reasoning_key="data",
        critical=True,
    ),

    "data_processing": build_clause_type(
        "Data Processing",
        "Traitement des données",
        "معالجة البيانات",
        ["data processing", "processor", "controller", "traitement des données", "sous-traitant", "responsable du traitement", "معالجة البيانات", "معالج البيانات"],
        risk_default="low",
        materiality="high",
        reasoning_key="data",
        critical=True,

        description={
            "en": "This clause defines how personal or business data may be collected, processed, stored, transferred, and protected.",
            "fr": "Cette clause définit la manière dont les données personnelles ou commerciales peuvent être collectées, traitées, stockées, transférées et protégées.",
            "ar": "يحدد هذا البند كيفية جمع البيانات الشخصية أو التجارية ومعالجتها وتخزينها ونقلها وحمايتها.",
        },
    ),

    "security": build_clause_type(
        "Security",
        "Sécurité",
        "الأمن",
        ["security", "safeguards", "security measures", "sécurité", "mesures de sécurité", "أمن", "تدابير أمنية"],
        risk_default="low",
        materiality="high",
        reasoning_key="data",
        critical=True,
    ),

    "cybersecurity": build_clause_type(
        "Cybersecurity",
        "Cybersécurité",
        "الأمن السيبراني",
        ["cybersecurity", "cyber security", "security incident", "cybersécurité", "incident de sécurité", "الأمن السيبراني", "حادث أمني"],
        risk_default="low",
        materiality="high",
        reasoning_key="data",
        critical=True,
    ),

    "sla": build_clause_type(
        "Service Level",
        "Niveau de service",
        "مستوى الخدمة",
        ["service level", "sla", "uptime", "availability", "downtime", "service credit", "niveau de service", "disponibilité", "interruption", "crédit de service", "مستوى الخدمة", "التوافر", "انقطاع الخدمة", "تعويض الخدمة"],
        risk_default="medium",
        materiality="high",
        reasoning_key="sla",
        critical=True,
    ),

    "service_level": build_clause_type(
        "Service Level",
        "Niveau de service",
        "مستوى الخدمة",
        ["service level", "sla", "uptime", "availability", "downtime", "niveau de service", "disponibilité", "مستوى الخدمة", "التوافر"],
        risk_default="medium",
        materiality="high",
        reasoning_key="sla",
        critical=True,
    ),

    "indemnity": build_clause_type(
        "Indemnity",
        "Indemnisation",
        "التعويض",
        ["indemnity", "indemnify", "hold harmless", "defend", "indemnification", "losses", "claims", "third party claims", "indemnisation", "indemniser", "tenir indemne", "défendre", "réclamations", "pertes", "تعويض", "يعوض", "الدفاع عن", "تعويضات", "مطالبات", "خسائر"],
        risk_default="medium",
        materiality="high",
        reasoning_key="indemnity",
        critical=True,
    ),

    "exclusivity": build_clause_type(
        "Exclusivity",
        "Exclusivité",
        "الحصرية",
        [
            "exclusivity", "sole provider", "sole and exclusive right to sell",
            "exclusive distributor", "exclusive dealing", "exclusive supplier",
            "exclusively engage", "exclusive rights to distribute",
            "exclusive territory", "territory",
            "exclusivité", "fournisseur unique", "distributeur exclusif",
            "fournisseur exclusif", "territoire exclusif", "territoire",
            "حصرية", "مزود وحيد", "موزع حصري", "مورد حصري", "منطقة حصرية", "منطقة",
        ],
        risk_default="medium",
        materiality="high",
        reasoning_key="exclusivity",
        critical=True,
    ),

    "restrictive_covenants": build_clause_type(
        "Restrictive Covenants",
        "Clauses restrictives",
        "القيود التعاقدية",
        [
            "non-compete", "non compete", "not compete",
            "non-solicitation", "non solicitation", "solicit employees",
            "non-dealing", "non dealing", "non-circumvention",
            "non circumvention", "exclusive dealing", "restraint of trade",
            "restrictive covenant", "customer solicitation",
            "employee solicitation", "poaching",
            "similar services to", "similar to the services to",
            "direct competitor", "direct competitors", "named competitor",
            "named competitors", "competitors of client", "competitors of company",

            "non-concurrence", "ne pas concurrencer",
            "non-sollicitation", "non sollicitation",
            "solliciter les employés", "non-détournement",
            "non détournement", "non-contournement",
            "non contournement", "exclusivité",
            "clause restrictive", "concurrents directs", "concurrents nommés",

            "عدم المنافسة", "عدم التنافس", "عدم الاستقطاب",
            "استقطاب الموظفين", "عدم التعامل", "عدم الالتفاف",
            "الحصرية", "قيد تعاقدي", "قيود تعاقدية",
            "منافسين مباشرين", "منافسين محددين",
        ],
        risk_default="medium",
        materiality="high",
        reasoning_key="restrictive_covenants",
        critical=True,
    ),

    "non_compete": build_clause_type(
        "Non-Compete",
        "Non-concurrence",
        "عدم المنافسة",
        ["non-compete", "non compete", "not compete", "restriction on competition", "non-concurrence", "ne pas concurrencer", "عدم المنافسة", "عدم التنافس"],
        risk_default="medium",
        materiality="high",
        reasoning_key="restrictive_covenants",
        critical=True,
    ),

    "post_termination_obligations": build_clause_type(
        "Post-Termination Obligations",
        "Obligations postérieures à la résiliation",
        "التزامات ما بعد الإنهاء",
        ["post-termination", "after termination", "survive termination", "après la résiliation", "survit à la résiliation", "بعد الإنهاء", "تستمر بعد الإنهاء"],
        risk_default="medium",
        materiality="high",
        reasoning_key="termination",
        critical=True,
    ),

    "remedies": build_clause_type(
        "Remedies",
        "Recours",
        "وسائل الانتصاف",
        ["remedies", "rights and remedies", "specific performance", "injunctive relief", "equitable relief", "irreparable injury", "money damages", "adequate remedy", "recours", "droits et recours", "exécution forcée", "injonction", "préjudice irréparable", "dommages-intérêts", "وسائل الانتصاف", "الحقوق ووسائل الانتصاف", "التنفيذ العيني", "أمر قضائي", "ضرر لا يمكن إصلاحه", "تعويضات مالية"],
        risk_default="medium",
        materiality="high",
        reasoning_key="liability",
        critical=True,
    ),

    "governing_law": build_clause_type(
        "Governing Law",
        "Droit applicable",
        "القانون الواجب التطبيق",
        [
            "governing law", "governed by the laws of", "state of",
            "jurisdiction", "venue", "courts",
            "droit applicable", "régi par les lois de", "juridiction",
            "tribunaux compétents", "tribunaux",
            "القانون الواجب التطبيق", "لقوانين", "الاختصاص", "المحاكم", "محكمة",
        ],
        risk_default="low",
        materiality="high",
        reasoning_key="governing_law",
        critical=True,
    ),

    "jurisdiction": build_clause_type(
        "Jurisdiction",
        "Juridiction",
        "الاختصاص القضائي",
        ["jurisdiction", "court", "courts", "venue", "juridiction", "tribunal", "tribunaux", "محكمة", "المحاكم", "الاختصاص"],
        risk_default="low",
        materiality="high",
        reasoning_key="governing_law",
        critical=True,
    ),

    "venue": build_clause_type(
        "Venue",
        "Tribunal compétent",
        "مكان الاختصاص",
        ["venue", "place of jurisdiction", "courts of", "tribunal compétent", "lieu de juridiction", "مكان الاختصاص", "محاكم"],
        risk_default="low",
        materiality="medium",
        reasoning_key="governing_law",
    ),

    "arbitration": build_clause_type(
        "Arbitration",
        "Arbitrage",
        "التحكيم",
        ["arbitration", "arbitrator", "arbitral tribunal", "arbitrage", "arbitre", "tribunal arbitral", "تحكيم", "محكم", "هيئة التحكيم"],
        risk_default="low",
        materiality="high",
        reasoning_key="governing_law",
        critical=True,
    ),

    "dispute_resolution": build_clause_type(
        "Dispute Resolution",
        "Résolution des litiges",
        "تسوية النزاعات",
        ["dispute resolution", "dispute", "mediation", "settlement", "résolution des litiges", "litige", "médiation", "règlement", "تسوية النزاعات", "نزاع", "وساطة", "تسوية"],
        risk_default="low",
        materiality="high",
        reasoning_key="governing_law",
        critical=True,
    ),

    "mediation": build_clause_type(
        "Mediation",
        "Médiation",
        "الوساطة",
        ["mediation", "mediator", "médiation", "médiateur", "وساطة", "وسيط"],
        risk_default="low",
        materiality="medium",
        reasoning_key="governing_law",
    ),

    "maintenance": build_clause_type(
        "Maintenance and Repair",
        "Maintenance et réparation",
        "الصيانة والإصلاح",
        ["maintenance", "repair", "maintenance", "réparation", "réparations", "entretien", "صيانة", "الصيانة", "إصلاح", "إصلاحات", "الإصلاحات"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="maintenance",
        critical=True,
        excluded_contexts=["service level", "sla", "uptime", "payment", "pricing", "niveau de service", "disponibilité", "paiement", "prix", "مستوى الخدمة", "الدفع", "الأسعار"],
    ),

    "repair": build_clause_type(
        "Repair",
        "Réparation",
        "الإصلاح",
        ["repair", "repairs", "réparation", "réparations", "إصلاح", "إصلاحات"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="maintenance",
    ),

    "repairs": build_clause_type(
        "Repairs",
        "Réparations",
        "الإصلاحات",
        ["repairs", "repair obligations", "réparations", "obligations de réparation", "إصلاحات", "التزامات الإصلاح"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="maintenance",
    ),

    "services": build_clause_type(
        "Services",
        "Services",
        "الخدمات",
        ["services", "service provider", "scope of work", "deliverables", "support", "implementation", "consulting", "professional services", "prestations", "assistance", "livrables", "mise en œuvre", "conseil", "خدمات", "نطاق العمل", "الدعم", "التنفيذ", "الاستشارات", "الخدمات المهنية"],
        risk_default="low",
        materiality="medium",
        reasoning_key="general",
    ),

    "support": build_clause_type(
        "Support",
        "Assistance",
        "الدعم",
        ["support", "technical support", "assistance", "support technique", "دعم", "الدعم الفني"],
        materiality="medium",
        reasoning_key="general",
    ),

    "delivery": build_clause_type(
        "Delivery",
        "Livraison",
        "التسليم",
        ["delivery", "deliver", "shipment", "livraison", "livrer", "تسليم", "شحن"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
    ),

    "acceptance": build_clause_type(
        "Acceptance",
        "Acceptation",
        "القبول",
        ["acceptance", "acceptance criteria", "accepted", "acceptation", "critères d'acceptation", "قبول", "معايير القبول"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
    ),

    "performance": build_clause_type(
        "Performance",
        "Performance",
        "الأداء",
        ["performance", "perform", "service performance", "exécution", "أداء", "تنفيذ"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
    ),

    "change_request": build_clause_type(
        "Change Request",
        "Demande de changement",
        "طلب التغيير",
        ["change request", "change order", "scope change", "demande de changement", "ordre de changement", "تغيير النطاق", "طلب تغيير"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
    ),

    "employment": build_clause_type(
        "Employment",
        "Emploi",
        "العمل",
        ["employee", "employer", "employment", "salary", "bonus", "benefits", "vacation", "executive", "employé", "employeur", "emploi", "salaire", "prime", "avantages", "congés", "موظف", "صاحب العمل", "راتب", "مكافأة", "مزايا"],
        risk_default="low",
        materiality="medium",
        reasoning_key="general",
    ),

    "compensation": build_clause_type(
        "Compensation",
        "Rémunération",
        "التعويض",
        ["compensation", "salary", "wages", "rémunération", "salaire", "أجر", "راتب", "تعويض"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "benefits": build_clause_type(
        "Benefits",
        "Avantages",
        "المزايا",
        ["benefits", "employee benefits", "health insurance", "avantages", "avantages sociaux", "assurance maladie", "مزايا", "مزايا الموظف"],
        materiality="medium",
        reasoning_key="employment",
    ),

    "vacation": build_clause_type(
        "Vacation",
        "Congés",
        "الإجازة",
        ["vacation", "paid time off", "leave", "congés", "congé payé", "إجازة", "إجازة مدفوعة"],
        materiality="medium",
        reasoning_key="employment",
    ),

    "corporate_governance": build_clause_type(
        "Corporate Governance",
        "Gouvernance d'entreprise",
        "حوكمة الشركات",
        ["board", "director", "shareholder", "approval", "consent", "voting", "corporate governance", "governance committee", "joint committee", "steering committee", "meeting quarterly", "meet quarterly", "review committee", "conseil", "administrateur", "actionnaire", "approbation", "consentement", "vote", "gouvernance", "comité de gouvernance", "comité conjoint", "comité de pilotage", "réunion trimestrielle", "مجلس الإدارة", "مدير", "مساهم", "موافقة", "تصويت", "حوكمة", "لجنة الحوكمة", "لجنة مشتركة", "اجتماع ربع سنوي"],
        materiality="medium",
        reasoning_key="general",
    ),

    "conflict_of_interest": build_clause_type(
        "Conflict of Interest",
        "Conflit d'intérêt",
        "تضارب المصالح",
        ["conflict of interest", "self dealing", "related party", "conflit d'intérêt", "partie liée", "تضارب المصالح", "طرف ذو صلة"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
    ),

    "board_approval": build_clause_type(
        "Board Approval",
        "Approbation du conseil",
        "موافقة مجلس الإدارة",
        ["board approval", "board consent", "director approval", "approbation du conseil", "consentement du conseil", "موافقة مجلس الإدارة", "موافقة المديرين"],
        materiality="medium",
        reasoning_key="general",
    ),

    "change_of_control": build_clause_type(
        "Change of Control",
        "Changement de contrôle",
        "تغيير السيطرة",
        ["change of control", "acquisition", "merger", "changement de contrôle", "acquisition", "fusion", "تغيير السيطرة", "استحواذ", "اندماج"],
        risk_default="medium",
        materiality="high",
        reasoning_key="general",
        critical=True,
    ),

    "equity_compensation": build_clause_type(
        "Equity Compensation",
        "Rémunération en actions",
        "التعويض بالأسهم",
        ["stock option", "equity compensation", "restricted stock", "vesting", "option d'achat", "rémunération en actions", "acquisition des droits", "خيارات الأسهم", "التعويض بالأسهم", "الاستحقاق"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="payment",
    ),

    "anti_dilution_preemptive_rights": build_clause_type(
        "Preemptive Rights",
        "Droits de préemption sur nouvelles émissions",
        "حقوق الأولوية في الاكتتاب",
        [
            "pro rata share", "new securities issued", "preemptive right",
            "preemptive rights", "anti-dilution", "right to purchase its pro rata",
            "participate in future issuances", "right to subscribe",

            "part au prorata", "nouveaux titres émis", "droit préférentiel de souscription",
            "droit préférentiel de souscription", "anti-dilution",
            "participer aux futures émissions", "droit de souscrire",

            "حصة نسبية", "أوراق مالية جديدة", "حق الأولوية في الاكتتاب",
            "حق الاكتتاب التفضيلي", "مكافحة التخفيف", "الحق في الاشتراك",
        ],
        risk_default="medium",
    ),

    "share_transfer_rights": build_clause_type(
        "Share Transfer Rights",
        "Droits de cession de titres",
        "حقوق نقل الأسهم",
        [
            "drag-along", "drag along", "tag-along", "tag along",
            "right of first refusal", "rofr", "transfer of shares",
            "transfer shares", "share transfer", "capital stock",
            "outstanding shares", "shareholder shall transfer",
            "cession forcée", "droit de sortie conjointe",
            "droit de préemption", "cession d'actions",
            "transfert d'actions", "actions de la société",
            "الحق في البيع المشترك", "حق الشراء الإجباري",
            "حق الأفضلية", "نقل الأسهم", "تحويل الأسهم",
        ],
        risk_default="medium",
        materiality="high",
        reasoning_key="ownership",
        critical=True,
    ),

    "investor_information_rights": build_clause_type(
        "Investor Information Rights",
        "Droits d'information de l'investisseur",
        "حقوق الاطلاع على المعلومات للمستثمر",
        [
            "information rights", "financial statements", "audited annual",
            "unaudited quarterly", "fiscal year end", "fiscal quarter end",
            "inspection rights", "books and records",
            "droits à l'information", "états financiers",
            "états financiers audités", "exercice fiscal",
            "droit d'inspection", "livres et registres",
            "حقوق الاطلاع", "القوائم المالية", "القوائم المالية المدققة",
            "نهاية السنة المالية", "حق التفتيش",
        ],
        risk_default="low",
        materiality="medium",
        reasoning_key="general",
    ),

    "trademark_branding": build_clause_type(
        "Trademark and Branding Usage",
        "Utilisation de marques et d'image de marque",
        "استخدام العلامات التجارية والهوية التجارية",
        [
            "trademark", "trade name", "trademarks", "branding",
            "brand guidelines", "logo", "co-branding",
            "publicity", "press release", "marketing material",
            "marque", "marques", "nom commercial", "image de marque",
            "charte graphique", "logo", "cobranding",
            "communiqué de presse", "matériel marketing", "publicité",
            "العلامة التجارية", "العلامات التجارية", "الاسم التجاري",
            "الهوية التجارية", "الشعار", "البيان الصحفي",
            "المواد التسويقية", "الدعاية",
        ],
        risk_default="low",
        materiality="medium",
        reasoning_key="general",
    ),

    "real_estate": build_clause_type(
        "Real Estate",
        "Immobilier",
        "العقار",
        ["lease", "tenant", "landlord", "rent", "premises", "property", "bail", "locataire", "bailleur", "locaux", "bien immobilier", "إيجار", "مستأجر", "مؤجر", "أجرة", "عقار"],
        materiality="medium",
        reasoning_key="general",
    ),

    "lease": build_clause_type(
        "Lease",
        "Bail",
        "الإيجار",
        ["lease", "rental", "tenant", "landlord", "bail", "location", "locataire", "bailleur", "إيجار", "عقد إيجار", "مستأجر", "مؤجر"],
        risk_default="medium",
        materiality="high",
        reasoning_key="general",
        critical=True,
    ),

    "rent": build_clause_type(
        "Rent",
        "Loyer",
        "الأجرة",
        ["rent", "rental payment", "loyer", "paiement du loyer", "أجرة", "إيجار"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "deposit": build_clause_type(
        "Deposit",
        "Dépôt",
        "الوديعة",
        ["deposit", "security deposit", "dépôt", "dépôt de garantie", "وديعة", "ضمان"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="payment",
    ),

    "property_use": build_clause_type(
        "Property Use",
        "Usage du bien",
        "استخدام العقار",
        ["use of premises", "permitted use", "property use", "usage des locaux", "usage autorisé", "استخدام العقار", "الاستخدام المسموح"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
    ),

    "utilities": build_clause_type(
        "Utilities",
        "Charges et services publics",
        "المرافق",
        ["utilities", "water", "electricity", "gas", "charges", "eau", "électricité", "gaz", "مرافق", "ماء", "كهرباء", "غاز"],
        materiality="medium",
        reasoning_key="payment",
    ),

    "loan_finance": build_clause_type(
        "Loan and Finance",
        "Prêt et financement",
        "القرض والتمويل",
        ["loan", "credit", "principal", "interest", "repayment", "lender", "borrower", "prêt", "crédit", "capital", "intérêt", "remboursement", "prêteur", "emprunteur", "قرض", "ائتمان", "فائدة", "سداد", "مقرض", "مقترض"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
    ),

    "loan": build_clause_type(
        "Loan",
        "Prêt",
        "القرض",
        ["loan", "credit facility", "principal", "prêt", "crédit", "قرض", "تسهيل ائتماني"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "interest": build_clause_type(
        "Interest",
        "Intérêt",
        "الفائدة",
        [
            "interest rate", "accrue interest", "late payment interest",
            "per annum", "interest per month", "interest charges",
            "taux d'intérêt", "intérêts de retard", "intérêts moratoires",
            "فائدة", "سعر الفائدة", "فوائد التأخير",
        ],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "security_interest": build_clause_type(
        "Security Interest",
        "Sûreté",
        "حق الضمان",
        ["security interest", "secured interest", "sûreté", "garantie réelle", "حق ضمان", "ضمان عيني"],
        risk_default="medium",
        materiality="high",
        reasoning_key="general",
        critical=True,
    ),

    "collateral": build_clause_type(
        "Collateral",
        "Garantie (sûreté)",
        "الضمان",
        [
            "collateral", "pledge",
            "gage", "nantissement", "sûreté", "garantie bancaire",
            "garantie de bonne fin", "garantie financière",
            "رهن", "ضمان مالي", "خطاب ضمان",
        ],
        risk_default="medium",
        materiality="high",
        reasoning_key="general",
        critical=True,
    ),

    "guarantee": build_clause_type(
        "Guarantee",
        "Cautionnement",
        "الكفالة",
        ["guarantee", "guarantor", "surety", "cautionnement", "garant", "كفالة", "ضامن"],
        risk_default="medium",
        materiality="high",
        reasoning_key="liability",
        critical=True,
    ),

    "repayment": build_clause_type(
        "Repayment",
        "Remboursement",
        "السداد",
        ["repayment", "repay", "amortization", "remboursement", "rembourser", "سداد", "إعادة السداد"],
        risk_default="medium",
        materiality="high",
        reasoning_key="payment",
        critical=True,
    ),

    "acceleration": build_clause_type(
        "Acceleration",
        "Exigibilité anticipée",
        "حلول الأجل",
        ["acceleration", "accelerate", "immediately due", "exigibilité anticipée", "exigible immédiatement", "حلول الأجل", "مستحق فوراً"],
        risk_default="medium",
        materiality="high",
        reasoning_key="termination",
        critical=True,
    ),

    "supply_distribution": build_clause_type(
        "Supply and Distribution",
        "Fourniture et distribution",
        "التوريد والتوزيع",
        ["supply", "supplier", "distribution", "distributor", "reseller", "purchase order", "delivery", "fourniture", "fournisseur", "distribution", "distributeur", "revendeur", "bon de commande", "livraison", "توريد", "مورد", "توزيع", "موزع", "طلب شراء", "تسليم"],
        materiality="medium",
        reasoning_key="general",
    ),

    "subcontracting": build_clause_type(
        "Subcontracting",
        "Sous-traitance",
        "التعاقد من الباطن",
        ["subcontracting", "subcontractor", "subcontract", "sous-traitance", "sous-traitant", "تعاقد من الباطن", "مقاول من الباطن"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
    ),

    "anti_bribery": build_clause_type(
        "Anti-Bribery",
        "Lutte contre la corruption",
        "مكافحة الرشوة",
        ["anti-bribery", "bribery", "corruption", "anti-corruption", "lutte contre la corruption", "corruption", "رشوة", "مكافحة الفساد"],
        risk_default="medium",
        materiality="high",
        reasoning_key="compliance",
        critical=True,
    ),

    "sanctions": build_clause_type(
        "Sanctions",
        "Sanctions internationales",
        "العقوبات",
        ["sanctions", "export control", "restricted party", "contrôle des exportations", "عقوبات", "رقابة الصادرات"],
        risk_default="medium",
        materiality="high",
        reasoning_key="compliance",
        critical=True,
    ),

    "compliance": build_clause_type(
        "Compliance",
        "Conformité",
        "الامتثال",
        ["compliance", "regulatory", "applicable regulations", "conformité", "réglementation", "الامتثال", "تنظيمي", "اللوائح"],
        risk_default="medium",
        materiality="high",
        reasoning_key="general",
        critical=True,
    ),

    "audit_rights": build_clause_type(
        "Audit Rights",
        "Droits d'audit",
        "حقوق التدقيق",
        ["audit rights", "right to audit", "to audit", "conduct an audit", "inspect books and records", "inspection rights", "droits d'audit", "droit d'inspection", "conduire un audit", "à auditer", "حقوق التدقيق", "حق إجراء تدقيق", "حق التفتيش", "أن يدقق"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="compliance",
    ),

    "assignment": build_clause_type(
        "Assignment",
        "Cession",
        "التنازل",
        ["assignment", "assign", "transfer of rights", "cession", "transfert de droits", "التنازل", "نقل الحقوق"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
        description={
            "en": "This clause governs whether contractual rights or obligations may be transferred to another party, and under what conditions consent is required.",
            "fr": "Cette clause encadre la possibilité de transférer les droits ou obligations contractuels à une autre partie, ainsi que les conditions de consentement applicables.",
            "ar": "ينظم هذا البند إمكانية نقل الحقوق أو الالتزامات التعاقدية إلى طرف آخر والشروط التي تتطلب الحصول على الموافقة.",
        },
    ),

    "amendment": build_clause_type(
        "Amendment",
        "Modification",
        "التعديل",
        ["amendment", "modify", "modification", "amend", "modifier", "تعديل", "يعدل"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
    ),

    "waiver": build_clause_type(
        "Waiver",
        "Renonciation",
        "التنازل",
        ["waiver", "waive", "renonciation", "renoncer", "تنازل", "يتنازل"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
    ),

    "severability": build_clause_type(
        "Severability",
        "Divisibilité",
        "قابلية الفصل",
        ["severability", "severable", "invalid provision", "divisibilité", "clause invalide", "قابلية الفصل", "بند باطل"],
        risk_default="low",
        materiality="low",
        reasoning_key="administrative",
    ),

    "entire_agreement": build_clause_type(
        "Entire Agreement",
        "Intégralité de l'accord",
        "الاتفاق الكامل",
        ["entire agreement", "whole agreement", "intégralité de l'accord", "accord complet", "الاتفاق الكامل", "كامل الاتفاق"],
        risk_default="low",
        materiality="medium",
        reasoning_key="administrative",
    ),

    "counterparts": build_clause_type(
        "Counterparts",
        "Exemplaires",
        "النُسخ",
        ["counterparts", "executed in counterparts", "exemplaires", "نسخ", "نظائر"],
        risk_default="low",
        materiality="low",
        reasoning_key="administrative",
    ),

    "notice": build_clause_type(
        "Notice",
        "Notification",
        "الإشعار",
        ["notice", "notices", "written notice", "notification", "notify", "avis", "préavis", "إشعار", "إخطار", "إبلاغ"],
        risk_default="low",
        materiality="medium",
        reasoning_key="administrative",
    ),

    "notices": build_clause_type(
        "Notices",
        "Notifications",
        "الإشعارات",
        ["notices", "notice address", "notifications", "adresse de notification", "إشعارات", "عنوان الإشعار"],
        risk_default="low",
        materiality="medium",
        reasoning_key="administrative",
    ),

    "definitions": build_clause_type(
        "Definitions",
        "Définitions",
        "التعريفات",
        ["definitions", "defined terms", "means", "définitions", "termes définis", "signifie", "تعريفات", "يقصد به", "يعني"],
        risk_default="low",
        materiality="low",
        reasoning_key="administrative",
    ),

    "administrative": build_clause_type(
        "Administrative",
        "Administratif",
        "إداري",
        ["party identification", "definitions", "headings", "headings for reference only", "titles", "section headings", "interpretation", "notice address", "for reference only", "identification des parties", "définitions", "adresse de notification", "à titre indicatif", "تعريف", "التعريفات", "عنوان الإشعار", "لأغراض مرجعية"],
        risk_default="low",
        materiality="low",
        reasoning_key="administrative",
    ),

    "force_majeure": build_clause_type(
        "Force Majeure",
        "Force majeure",
        "القوة القاهرة",
        ["force majeure", "act of god", "unforeseeable event", "cas de force majeure", "القوة القاهرة", "حدث غير متوقع"],
        risk_default="medium",
        materiality="high",
        reasoning_key="general",
        critical=True,
    ),

    "non_solicitation": build_clause_type(
        "Non-Solicitation",
        "Non-sollicitation",
        "عدم الاستقطاب",
        ["non solicitation", "non-solicitation", "solicit employees", "non-sollicitation", "solliciter les employés", "عدم الاستقطاب", "استقطاب الموظفين"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="restrictive_covenants",
    ),

    "default": build_clause_type(
        "Default",
        "Défaut",
        "الإخلال",
        ["default", "event of default", "breach", "défaut", "manquement", "إخلال", "حالة إخلال"],
        risk_default="medium",
        materiality="high",
        reasoning_key="termination",
        critical=True,
    ),

    "insurance": build_clause_type(
        "Insurance",
        "Assurance",
        "التأمين",
        ["insurance", "insured", "coverage", "assurance", "assuré", "couverture", "تأمين", "مؤمن", "تغطية"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="liability",
    ),

    "covenant": build_clause_type(
        "Covenant",
        "Engagement",
        "التعهد",
        ["covenant", "undertaking", "engagement", "obligation", "تعهد", "التزام"],
        risk_default="medium",
        materiality="medium",
        reasoning_key="general",
    ),
}


CLAUSE_PRIORITY_ORDER = [
    # Highly specific / high-impact concepts first.
    "remedies",
    "liquidated_damages",
    "penalty",
    "limitation_of_liability_exceptions",
    "limitation_of_liability",
    "liability",
    "indemnity",
    "guarantee",
    "security_interest",
    "collateral",
    "pricing_adjustment",

    "automatic_renewal",
    "termination_for_convenience",
    "termination_for_cause",
    "acceleration",
    "termination",
    "cure_period",
    "post_termination_obligations",

    "ip_assignment",
    "work_product",
    "moral_rights",
    "ownership",
    "license",
    "intellectual_property",

    "data_processing",
    "cybersecurity",
    "privacy",
    "security",
    "data_protection",

    "restrictive_covenants",
    "non_compete",
    "non_solicitation",
    "exclusivity",

    "arbitration",
    "mediation",
    "dispute_resolution",
    "governing_law",
    "jurisdiction",
    "venue",

    "late_payment",
    "tax",
    "royalties",
    "commission",
    "pricing",
    "fees",
    "refund",
    "invoice",
    "interest",
    "repayment",
    "loan",
    "payment",

    "rent",
    "deposit",
    "property_use",
    "repairs",
    "utilities",
    "lease",
    "real_estate",

    "compensation",
    "benefits",
    "vacation",
    "employment",
    "equity_compensation",
    "share_transfer_rights",
    "anti_dilution_preemptive_rights",
    "investor_information_rights",
    "trademark_branding",

    "anti_bribery",
    "sanctions",
    "compliance",
    "audit_rights",

    "change_request",
    "acceptance",
    "delivery",
    "support",
    "performance",
    "service_level",
    "sla",
    "subcontracting",
    "services",
    "supply_distribution",

    "conflict_of_interest",
    "board_approval",
    "change_of_control",
    "corporate_governance",

    "assignment",
    "amendment",
    "waiver",
    "force_majeure",
    "warranty",
    "disclaimer",
    "maintenance",
    "repair",
    "insurance",
    "default",
    "covenant",

    "term",
    "duration",
    "renewal",

    "notices",
    "notice",
    "definitions",
    "severability",
    "entire_agreement",
    "counterparts",
    "administrative",
]

CLAUSE_PRIORITY_ORDER = list(dict.fromkeys(CLAUSE_PRIORITY_ORDER))


def normalize_language(language: str) -> str:
    language = str(language or "en").lower()

    if language not in SUPPORTED_LANGUAGES:
        return "en"

    return language


def get_clause_type_definition(clause_type: str) -> dict:
    return CLAUSE_TYPES.get(
        str(clause_type or "").lower(),
        {},
    )


def get_clause_type_label(
    clause_type: str,
    language: str = "en",
) -> str:
    language = normalize_language(language)
    definition = get_clause_type_definition(clause_type)

    return definition.get(
        "label",
        {},
    ).get(
        language,
        str(clause_type or "other"),
    )


def get_clause_type_signals(clause_type: str) -> list[str]:
    definition = get_clause_type_definition(clause_type)

    return list(
        definition.get(
            "signals",
            [],
        )
    )


def get_all_critical_terms() -> list[str]:
    terms = []

    for definition in CLAUSE_TYPES.values():
        if not definition.get("critical"):
            continue

        terms.extend(
            definition.get(
                "signals",
                [],
            )
        )

    return dedupe_terms(terms)


def get_reasoning_key_for_clause_type(
    clause_type: str,
) -> str:
    definition = get_clause_type_definition(clause_type)

    return definition.get(
        "reasoning_key",
        "general",
    )


def get_risk_default_for_clause_type(
    clause_type: str,
) -> str:
    definition = get_clause_type_definition(clause_type)

    return definition.get(
        "risk_default",
        "low",
    )


def get_materiality_for_clause_type(
    clause_type: str,
) -> str:
    definition = get_clause_type_definition(clause_type)

    return definition.get(
        "materiality",
        "low",
    )


def get_excluded_contexts_for_clause_type(
    clause_type: str,
) -> list[str]:
    definition = get_clause_type_definition(clause_type)

    return list(
        definition.get(
            "excluded_contexts",
            [],
        )
    )


def dedupe_terms(terms: list[str]) -> list[str]:
    seen = set()
    output = []

    for term in terms:
        normalized = str(term or "").strip()

        if not normalized:
            continue

        lowered = normalized.lower()

        if lowered in seen:
            continue

        seen.add(lowered)
        output.append(normalized)

    return output


SIGNAL_WEIGHTS = {
    "liquidated damages": 6,
    "dommages-intérêts forfaitaires": 6,
    "تعويضات مقطوعة": 6,

    "automatic renewal": 6,
    "renouvellement automatique": 6,
    "تجديد تلقائي": 6,

    "termination for convenience": 6,
    "termination for cause": 6,
    "résiliation de convenance": 6,
    "résiliation pour motif": 6,

    "drag-along": 6,
    "drag along": 6,
    "tag-along": 6,
    "tag along": 6,
    "right of first refusal": 6,
    "droit de sortie conjointe": 6,
    "cession forcée": 6,
    "حق البيع المشترك": 6,
    "حق الشراء الإجباري": 6,

    "nantissement": 5,
    "gage": 5,
    "sûreté": 5,
    "garantie bancaire": 5,
    "خطاب ضمان": 5,
    "ضمان مالي": 5,

    "limitation of liability": 6,
    "liability cap": 6,
    "unlimited liability": 6,
    "limitation de responsabilité": 6,
    "plafond de responsabilité": 6,
    "مسؤولية غير محدودة": 6,

    "intellectual property": 5,
    "ip assignment": 6,
    "work product": 5,
    "moral rights": 5,
    "propriété intellectuelle": 5,
    "droits moraux": 5,
    "الملكية الفكرية": 5,

    "indemnity": 5,
    "indemnification": 5,
    "indemnify": 5,
    "hold harmless": 5,
    "third party claims": 5,
    "indemnisation": 5,
    "indemniser": 5,
    "تعويضات": 5,
    "مطالبات": 4,

    "rights and remedies": 5,
    "specific performance": 5,
    "injunctive relief": 5,
    "exécution forcée": 5,
    "injonction": 5,

    "non-compete": 5,
    "non compete": 5,
    "non-solicitation": 4,
    "non solicitation": 4,
    "restrictive covenant": 4,
    "non-concurrence": 5,
    "non-sollicitation": 4,
    "non sollicitation": 4,
    "عدم المنافسة": 5,
    "عدم الاستقطاب": 4,

    "arbitration": 2,
    "arbitrage": 2,
    "تحكيم": 2,

    "payment": 2,
    "pay": 2,
    "invoice": 3,
    "fee": 2,
    "fees": 2,
    "pricing": 3,
    "late payment": 4,
    "tax": 3,
    "interest": 3,
    "repayment": 3,

    "paiement": 2,
    "facture": 3,
    "frais": 2,
    "prix": 2,
    "retard de paiement": 4,
    "intérêt": 3,

    "الدفع": 2,
    "السداد": 2,
    "فاتورة": 3,
    "الرسوم": 2,
    "الفائدة": 3,
}


TYPE_SPECIFICITY_BONUS = {
    "liquidated_damages": 6,
    "automatic_renewal": 6,
    "termination_for_convenience": 6,
    "force_majeure": 6,
    "audit_rights": 4,
    "termination_for_cause": 6,
    "share_transfer_rights": 5,
    "limitation_of_liability": 5,
    "ip_assignment": 5,
    "collateral": 5,
    "pricing_adjustment": 4,
    "warranty": 5,
    "work_product": 4,
    "moral_rights": 4,
    "security_interest": 4,
    "collateral": 4,
    "guarantee": 4,
    "remedies": 4,
    "indemnity": 4,
    "intellectual_property": 4,
    "conflict_of_interest": 4,
    "assignment": 3,
    "change_of_control": 3,
    "arbitration": 3,
    "dispute_resolution": 3,
    "data_processing": 3,
    "data_protection": 3,
    "privacy": 3,
    "cybersecurity": 3,
    "restrictive_covenants": 4,
    "non_compete": 4,
    "non_solicitation": 4,
    "liability": 3,
    "termination": 3,
    "late_payment": 3,
    "notice": 2,
    "maintenance": 2,
    "payment": 0,
    "services": 0,
    "employment": 0,
    "corporate_governance": 0,
    "governing_law": 0,
    "administrative": 0,
}


TYPE_STRONG_SIGNALS = {
    "indemnity": {
        "indemnity",
        "indemnify",
        "hold harmless",
        "indemnification",
        "third party claims",
        "indemnisation",
        "indemniser",
        "tenir indemne",
        "تعويضات",
        "مطالبات",
        "خسائر",
        "يعوض",
    },
}


TYPE_CONTEXT_ANCHORS = {
    "employment": [
        "employee", "employer", "employment", "salary", "bonus",
        "benefits", "vacation", "position", "duties", "executive",
        "employé", "employeur", "emploi", "salaire", "prime",
        "avantages", "congés", "poste", "fonctions",
        "موظف", "صاحب العمل", "راتب", "مكافأة", "مزايا",
    ],
    "restrictive_covenants": [
        "non-compete", "non compete", "non-solicitation",
        "non solicitation", "restrictive covenant", "exclusive dealing",
        "restraint of trade", "customer solicitation",
        "employee solicitation", "poaching",
        "non-concurrence", "non-sollicitation", "non sollicitation",
        "clause restrictive", "exclusivité",
        "عدم المنافسة", "عدم الاستقطاب", "الحصرية", "قيود تعاقدية",
    ],
    "corporate_governance": [
        "board", "director", "shareholder", "voting", "governance",
        "committee", "board approval", "board consent",
        "conseil", "administrateur", "actionnaire", "vote",
        "gouvernance", "comité",
        "مجلس الإدارة", "مدير", "مساهم", "تصويت", "حوكمة",
    ],
    "services": [
        "master services agreement", "service agreement", "services", "service provider", "client", "scope of work", "deliverables",
        "support", "implementation", "consulting",
        "prestations", "assistance", "livrables", "mise en œuvre",
        "خدمات", "نطاق العمل", "الدعم", "التنفيذ", "الاستشارات",
    ],
    "payment": [
        "payment", "pay", "invoice", "fees", "salary", "bonus",
        "reimbursement", "expense reimbursement",
        "paiement", "payer", "facture", "frais", "salaire",
        "prime", "remboursement",
        "الدفع", "السداد", "فاتورة", "الرسوم", "راتب",
        "مكافأة", "تعويض المصاريف",
    ],
    "lease": [
        "lease", "tenant", "landlord", "rent", "premises",
        "bail", "locataire", "bailleur", "loyer", "إيجار",
        "مستأجر", "مؤجر", "أجرة",
    ],
    "loan": [
        "loan", "lender", "borrower", "principal", "interest",
        "repayment", "prêt", "prêteur", "emprunteur", "capital",
        "intérêt", "remboursement", "قرض", "مقرض", "مقترض",
        "فائدة", "سداد",
    ],
}


TYPE_CONTEXT_PENALTIES = {
    "services": TYPE_CONTEXT_ANCHORS["employment"],
    "corporate_governance": TYPE_CONTEXT_ANCHORS["employment"],
    "payment": [
        "indemnification", "indemnity", "hold harmless",
        "third party claims", "specific performance", "injunctive relief",
        "invention", "patent", "indemnisation", "tenir indemne",
        "réclamations", "exécution forcée", "injonction", "brevet",
        "تعويضات", "مطالبات", "التنفيذ العيني", "أمر قضائي",
        "اختراع", "براءة اختراع",
    ],
}


def count_context_matches(
    text: str,
    terms: list[str],
) -> int:
    normalized = str(text or "").lower()

    return sum(
        1
        for term in terms
        if re.search(r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)", normalized)
    )


def context_bonus_for_clause_type(
    text: str,
    clause_type: str,
) -> int:
    matches = count_context_matches(
        text,
        TYPE_CONTEXT_ANCHORS.get(clause_type, []),
    )

    if matches >= 3:
        return 4

    if matches == 2:
        return 2

    if matches == 1:
        return 1

    return 0


def context_penalty_for_clause_type(
    text: str,
    clause_type: str,
) -> int:
    matches = count_context_matches(
        text,
        TYPE_CONTEXT_PENALTIES.get(clause_type, []),
    )

    if matches >= 3:
        return 4

    if matches == 2:
        return 2

    if matches == 1:
        return 1

    return 0


def score_clause_type(
    text: str,
    clause_type: str,
) -> dict:
    normalized = str(text or "").lower()
    definition = CLAUSE_TYPES.get(clause_type, {})

    signals = definition.get(
        "signals",
        [],
    )

    excluded_contexts = definition.get(
        "excluded_contexts",
        [],
    )

    matched_signals = []

    if any(
        re.search(r"(?<!\w)" + re.escape(excluded.lower()) + r"(?!\w)", normalized)
        for excluded in excluded_contexts
    ):
        return {
            "type": clause_type,
            "score": 0,
            "base_score": 0,
            "context_bonus": 0,
            "context_penalty": 0,
            "signals": [],
            "excluded": True,
        }

    base_score = 0

    for signal in signals:
        signal_normalized = signal.lower()

        pattern = r"(?<!\w)" + re.escape(signal_normalized) + r"(?!\w)"

        if re.search(pattern, normalized):
            matched_signals.append(signal)
            base_score += SIGNAL_WEIGHTS.get(
                signal_normalized,
                1,
            )

    specificity_bonus = 0

    if matched_signals:
        strong_signals = TYPE_STRONG_SIGNALS.get(
            clause_type,
        )

        if strong_signals is None:
            specificity_bonus = TYPE_SPECIFICITY_BONUS.get(
                clause_type,
                0,
            )

        else:
            matched_normalized = {
                str(signal).lower()
                for signal in matched_signals
            }

            if matched_normalized & strong_signals:
                specificity_bonus = TYPE_SPECIFICITY_BONUS.get(
                    clause_type,
                    0,
                )

    context_bonus = context_bonus_for_clause_type(
        text,
        clause_type,
    )

    context_penalty = context_penalty_for_clause_type(
        text,
        clause_type,
    )

    score = max(
        0,
        base_score
        + specificity_bonus
        + context_bonus
        - context_penalty,
    )

    return {
        "type": clause_type,
        "score": score,
        "base_score": base_score,
        "specificity_bonus": specificity_bonus,
        "context_bonus": context_bonus,
        "context_penalty": context_penalty,
        "signals": dedupe_terms(matched_signals),
        "excluded": False,
    }


def detect_clause_type_candidates(
    text: str,
) -> list[dict]:
    candidates = []

    for clause_type in CLAUSE_PRIORITY_ORDER:
        candidate = score_clause_type(
            text,
            clause_type,
        )

        if candidate.get("score", 0) > 0:
            candidates.append(candidate)

    candidates.sort(
        key=lambda item: (
            item.get("score", 0),
            TYPE_SPECIFICITY_BONUS.get(item.get("type"), 0),
            -CLAUSE_PRIORITY_ORDER.index(item.get("type")),
        ),
        reverse=True,
    )

    return candidates


def select_best_clause_type(
    candidates: list[dict],
) -> str:
    if not candidates:
        return "other"

    strong_candidates = [
        candidate
        for candidate in candidates
        if candidate.get("score", 0) > 0
    ]

    if not strong_candidates:
        return "other"

    strong_candidates.sort(
        key=lambda item: (
            item.get("score", 0),
            TYPE_SPECIFICITY_BONUS.get(item.get("type"), 0),
            -CLAUSE_PRIORITY_ORDER.index(item.get("type")),
        ),
        reverse=True,
    )

    return strong_candidates[0].get(
        "type",
        "other",
    )


def detect_clause_type_from_taxonomy(text: str) -> str:
    candidates = detect_clause_type_candidates(text)

    return select_best_clause_type(candidates)


def has_clause_type_signal(
    text: str,
    clause_type: str,
) -> bool:
    candidate = score_clause_type(
        text,
        clause_type,
    )

    return candidate.get("score", 0) > 0


def detect_secondary_clause_types(
    text: str,
    limit: int = 3,
) -> list[str]:
    candidates = detect_clause_type_candidates(text)
    primary = select_best_clause_type(candidates)

    secondary = []

    for candidate in candidates:
        clause_type = candidate.get("type")

        if clause_type == primary:
            continue

        if candidate.get("score", 0) <= 0:
            continue

        secondary.append(clause_type)

        if len(secondary) >= limit:
            break

    return secondary


def detect_clause_type_labels(
    text: str,
    max_secondary: int = 3,
) -> dict:
    candidates = detect_clause_type_candidates(text)

    primary = select_best_clause_type(candidates)

    secondary = []

    for candidate in candidates:
        clause_type = candidate.get("type")

        if clause_type == primary:
            continue

        score = candidate.get("score", 0)

        if score >= 2:
            secondary.append(clause_type)

        if len(secondary) >= max_secondary:
            break

    return {
        "primary_type": primary,
        "secondary_types": secondary,
        "candidates": candidates,
    }


def is_critical_clause_text(text: str) -> bool:
    normalized = str(text or "").lower()

    return any(
        term.lower() in normalized
        for term in get_all_critical_terms()
    )



def normalize_taxonomy_role_context(
    clause_type: str,
    contract_family: str = "generic",
) -> str:
    """
    Standard international taxonomy guard.

    Restrictive covenants such as non-compete and non-solicitation are not
    automatically Employment & HR. They remain Restrictive Covenants unless
    the whole contract family is employment.
    """
    family = str(contract_family or "generic").lower().replace(" ", "_")
    ctype = str(clause_type or "other").lower().strip()

    if family != "employment" and ctype in {
        "non_compete",
        "non_solicitation",
        "restrictive_covenants",
        "post_termination_obligations",
        "conflict_of_interest",
        "exclusivity",
    }:
        return "restrictive_covenants"

    if family != "employment" and ctype in {
        "employment",
        "compensation",
        "benefits",
        "vacation",
    }:
        return "other"

    return ctype

def get_clause_type_description(
    clause_type: str,
    language: str = "en",
) -> str:
    """
    Retourne la description officielle d'un type de clause
    dans la langue demandée.
    """

    definition = CLAUSE_TYPES.get(clause_type)

    if not definition:
        return ""

    language = language if language in ("en", "fr", "ar") else "en"

    return (
        definition
        .get("description", {})
        .get(language, "")
    )
