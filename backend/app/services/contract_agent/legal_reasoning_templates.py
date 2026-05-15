"""
Clause-type legal reasoning templates for contract analysis.

These templates complement domain-level reasoning by providing
specific reasoning for common clause categories:
liability, confidentiality, termination, SLA, indemnity, payment,
exclusivity, and governing law.
"""

SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


LIABILITY_NEGOTIATION = {
    "en": (
        "Consider negotiating liability caps, exclusions for indirect "
        "damages, and carve-outs for fraud, wilful misconduct, or "
        "confidentiality breaches."
    ),
    "fr": (
        "Envisager de négocier des plafonds de responsabilité, "
        "l'exclusion des dommages indirects et des exceptions en "
        "cas de fraude, faute intentionnelle ou violation de "
        "confidentialité."
    ),
    "ar": (
        "يمكن التفاوض على حدود للمسؤولية، واستبعاد الأضرار غير "
        "المباشرة، مع استثناءات لحالات الاحتيال أو الخطأ العمدي "
        "أو خرق السرية."
    ),
}


def get_language(language: str) -> str:
    language = str(language or "en").lower()

    if language not in SUPPORTED_LANGUAGES:
        return "en"

    return language


CLAUSE_REASONING_TEMPLATES = {
    "liability": {
        "signals": [
            "liability",
            "liability cap",
            "limitation of liability",
            "unlimited liability",
            "indirect damages",
            "responsabilité",
            "plafond de responsabilité",
            "limitation de responsabilité",
            "responsabilité illimitée",
            "dommages indirects",
            "المسؤولية",
            "حد المسؤولية",
            "مسؤولية غير محدودة",
            "الأضرار غير المباشرة",
        ],
        "legal_insight": {
            "en": (
                "This clause affects how financial responsibility is "
                "allocated if losses, claims, or disputes arise."
            ),
            "fr": (
                "Cette clause détermine la répartition de la "
                "responsabilité financière en cas de pertes, de "
                "réclamations ou de litiges."
            ),
            "ar": (
                "تحدد هذه المادة كيفية توزيع المسؤولية المالية عند "
                "وقوع خسائر أو مطالبات أو نزاعات."
            ),
        },
        "recommendation": {
            "en": (
                "Check whether the liability cap, exclusions, and "
                "carve-outs are clearly stated and proportionate."
            ),
            "fr": (
                "Vérifier que le plafond de responsabilité, les exclusions "
                "et les exceptions sont clairement définis et proportionnés."
            ),
            "ar": (
                "ينبغي التحقق من وضوح حد المسؤولية والاستثناءات "
                "وأن تكون متناسبة."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating liability caps, exclusions for indirect "
                "damages, and carve-outs for fraud, wilful misconduct, or "
                "confidentiality breaches."
            ),
            "fr": (
                "Envisager de négocier des plafonds de responsabilité, "
                "l'exclusion des dommages indirects et des exceptions en "
                "cas de fraude, faute intentionnelle ou violation de "
                "confidentialité."
            ),
            "ar": (
                "يمكن التفاوض على حدود للمسؤولية، واستبعاد الأضرار غير "
                "المباشرة، مع استثناءات لحالات الاحتيال أو الخطأ العمدي "
                "أو خرق السرية."
            ),
        },
    },

    "confidentiality": {
        "signals": [
            "confidentiality",
            "confidential information",
            "trade secret",
            "survive termination",
            "confidentialité",
            "information confidentielle",
            "secret commercial",
            "السرية",
            "معلومات سرية",
            "سر تجاري",
        ],
        "legal_insight": {
            "en": (
                "This clause controls how protected information may be used, "
                "shared, retained, and protected."
            ),
            "fr": (
                "Cette clause encadre l'utilisation, la communication, "
                "la conservation et la protection des informations "
                "confidentielles."
            ),
            "ar": (
                "تنظم هذه المادة كيفية استعمال المعلومات المحمية أو "
                "مشاركتها أو الاحتفاظ بها أو حمايتها."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm that the scope, permitted disclosures, duration, "
                "and return or destruction duties are clear."
            ),
            "fr": (
                "Vérifier que la portée, les divulgations autorisées, "
                "la durée et les obligations de restitution ou destruction "
                "sont claires."
            ),
            "ar": (
                "ينبغي التأكد من وضوح النطاق، وحالات الإفصاح المسموح، "
                "والمدة، وواجبات الإرجاع أو الإتلاف."
            ),
        },
        "negotiation": {
            "en": (
                "Consider limiting confidentiality duration, narrowing the "
                "scope of protected information, and adding standard "
                "disclosure exceptions."
            ),
            "fr": (
                "Envisager de limiter la durée de confidentialité, de "
                "restreindre la portée des informations protégées et "
                "d'ajouter des exceptions usuelles de divulgation."
            ),
            "ar": (
                "يمكن التفاوض على تقليص مدة السرية، وتحديد نطاق "
                "المعلومات المحمية، وإضافة استثناءات إفصاح معتادة."
            ),
        },
    },

    "termination": {
        "signals": [
            "termination",
            "terminate",
            "cure period",
            "notice period",
            "immediate termination",
            "résiliation",
            "résilier",
            "délai de régularisation",
            "préavis",
            "إنهاء",
            "فسخ",
            "مهلة معالجة",
            "إشعار",
            "إنهاء فوري",
        ],
        "legal_insight": {
            "en": (
                "This clause determines when the contract can end and "
                "whether the affected party has notice or an opportunity "
                "to cure."
            ),
            "fr": (
                "Cette clause détermine les conditions de fin du contrat "
                "et si la partie concernée bénéficie d'un préavis ou "
                "d'une possibilité de régularisation."
            ),
            "ar": (
                "تحدد هذه المادة متى يمكن إنهاء العقد وما إذا كان للطرف "
                "المتأثر حق في الإشعار أو فرصة لمعالجة الإخلال."
            ),
        },
        "recommendation": {
            "en": (
                "Review the termination triggers, notice requirements, "
                "cure periods, and post-termination obligations."
            ),
            "fr": (
                "Examiner les causes de résiliation, les exigences de "
                "préavis, les délais de régularisation et les obligations "
                "après résiliation."
            ),
            "ar": (
                "ينبغي مراجعة أسباب الإنهاء، ومتطلبات الإشعار، ومهل "
                "المعالجة، والالتزامات بعد الإنهاء."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating mutual termination rights, longer "
                "cure periods, and clear consequences after termination."
            ),
            "fr": (
                "Envisager de négocier des droits de résiliation "
                "réciproques, des délais de régularisation plus longs "
                "et des conséquences claires après résiliation."
            ),
            "ar": (
                "يمكن التفاوض على حقوق إنهاء متبادلة، ومهل معالجة أطول، "
                "وآثار واضحة بعد الإنهاء."
            ),
        },
    },

    "sla": {
        "signals": [
            "service level",
            "sla",
            "uptime",
            "availability",
            "downtime",
            "service credit",
            "niveau de service",
            "disponibilité",
            "interruption",
            "crédit de service",
            "مستوى الخدمة",
            "التوافر",
            "انقطاع الخدمة",
            "تعويض الخدمة",
        ],
        "legal_insight": {
            "en": (
                "This clause defines service performance commitments and "
                "the consequences if the provider fails to meet them."
            ),
            "fr": (
                "Cette clause définit les engagements de performance du "
                "service et les conséquences en cas de non-respect."
            ),
            "ar": (
                "تحدد هذه المادة التزامات أداء الخدمة والآثار المترتبة "
                "عند عدم الالتزام بها."
            ),
        },
        "recommendation": {
            "en": (
                "Check whether uptime targets, measurement periods, "
                "exclusions, remedies, and reporting obligations are clear."
            ),
            "fr": (
                "Vérifier que les objectifs de disponibilité, les périodes "
                "de mesure, les exclusions, les recours et les obligations "
                "de reporting sont clairs."
            ),
            "ar": (
                "ينبغي التحقق من وضوح أهداف التوافر، وفترات القياس، "
                "والاستثناءات، ووسائل المعالجة، والتقارير."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating measurable uptime commitments, service "
                "credits, incident response timelines, and termination "
                "rights for repeated failures."
            ),
            "fr": (
                "Envisager de négocier des engagements de disponibilité "
                "mesurables, des crédits de service, des délais de réponse "
                "aux incidents et un droit de résiliation en cas d'échecs "
                "répétés."
            ),
            "ar": (
                "يمكن التفاوض على التزامات توافر قابلة للقياس، وتعويضات "
                "خدمة، ومهل استجابة للحوادث، وحق الفسخ عند تكرار الإخفاق."
            ),
        },
    },

    "indemnity": {
        "signals": [
            "indemnity",
            "indemnify",
            "hold harmless",
            "defend",
            "indemnisation",
            "indemniser",
            "tenir indemne",
            "défendre",
            "تعويض",
            "يعوض",
            "الدفاع عن",
        ],
        "legal_insight": {
            "en": (
                "This clause allocates responsibility for third-party claims, "
                "defense costs, damages, or losses."
            ),
            "fr": (
                "Cette clause répartit la responsabilité liée aux réclamations "
                "de tiers, aux frais de défense, aux dommages ou aux pertes."
            ),
            "ar": (
                "تحدد هذه المادة المسؤولية عن مطالبات الغير وتكاليف الدفاع "
                "والأضرار أو الخسائر."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm which claims are covered, who controls the defense, "
                "whether notice is required, and whether liability limits apply."
            ),
            "fr": (
                "Vérifier quelles réclamations sont couvertes, qui contrôle "
                "la défense, si une notification est requise et si les limites "
                "de responsabilité s'appliquent."
            ),
            "ar": (
                "ينبغي التأكد من نوع المطالبات المشمولة، ومن يتحكم في الدفاع، "
                "وما إذا كان الإشعار مطلوباً، وهل تنطبق حدود المسؤولية."
            ),
        },
        "negotiation": {
            "en": (
                "Consider narrowing indemnified claims, requiring prompt notice, "
                "and linking indemnity exposure to liability limits."
            ),
            "fr": (
                "Envisager de restreindre les réclamations indemnisées, "
                "d'exiger une notification rapide et de lier l'indemnisation "
                "aux limites de responsabilité."
            ),
            "ar": (
                "يمكن التفاوض على تضييق نطاق المطالبات المشمولة بالتعويض، "
                "واشتراط إشعار سريع، وربط التعويض بحدود المسؤولية."
            ),
        },
    },

    "payment": {
        "signals": [
            "payment",
            "invoice",
            "fee",
            "pricing",
            "interest",
            "late payment",
            "principal amount",
            "loan amount",
            "paiement",
            "facture",
            "frais",
            "prix",
            "intérêt",
            "retard de paiement",
            "capital",
            "montant du prêt",
            "الدفع",
            "فاتورة",
            "الرسوم",
            "الأسعار",
            "الفائدة",
            "تأخر الدفع",
            "رأس المال",
            "مبلغ القرض",
        ],
        "legal_insight": {
            "en": (
                "This clause defines financial obligations, payment timing, "
                "pricing mechanics, or interest exposure."
            ),
            "fr": (
                "Cette clause définit les obligations financières, les délais "
                "de paiement, les mécanismes de prix ou l'exposition aux intérêts."
            ),
            "ar": (
                "تحدد هذه المادة الالتزامات المالية، ومواعيد الدفع، وآليات "
                "التسعير، أو التعرض للفائدة."
            ),
        },
        "recommendation": {
            "en": (
                "Check payment due dates, invoicing requirements, interest, "
                "penalties, tax treatment, and consequences of non-payment."
            ),
            "fr": (
                "Vérifier les échéances de paiement, les exigences de facturation, "
                "les intérêts, les pénalités, le traitement fiscal et les "
                "conséquences du non-paiement."
            ),
            "ar": (
                "ينبغي مراجعة آجال الدفع، ومتطلبات الفوترة، والفائدة، "
                "والجزاءات، والمعالجة الضريبية، وآثار عدم السداد."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating payment schedules, grace periods, invoice "
                "dispute procedures, and proportional late-payment remedies."
            ),
            "fr": (
                "Envisager de négocier des échéanciers de paiement, des délais "
                "de grâce, des procédures de contestation des factures et des "
                "recours proportionnés en cas de retard."
            ),
            "ar": (
                "يمكن التفاوض على جداول الدفع، وفترات السماح، وإجراءات "
                "الاعتراض على الفواتير، ووسائل معالجة متناسبة عند التأخير."
            ),
        },
    },

    "exclusivity": {
        "signals": [
            "exclusive",
            "exclusivity",
            "sole provider",
            "non-exclusive",
            "territory",
            "exclusif",
            "exclusivité",
            "fournisseur unique",
            "non exclusif",
            "territoire",
            "حصري",
            "حصرية",
            "مزود وحيد",
            "غير حصري",
            "منطقة",
        ],
        "legal_insight": {
            "en": (
                "This clause may restrict the ability to work with other "
                "partners, suppliers, customers, or territories."
            ),
            "fr": (
                "Cette clause peut limiter la capacité de travailler avec "
                "d'autres partenaires, fournisseurs, clients ou territoires."
            ),
            "ar": (
                "قد تقيد هذه المادة القدرة على التعامل مع شركاء أو موردين "
                "أو عملاء أو مناطق أخرى."
            ),
        },
        "recommendation": {
            "en": (
                "Review the exclusivity scope, territory, duration, performance "
                "conditions, and consequences of failing to meet targets."
            ),
            "fr": (
                "Examiner la portée de l'exclusivité, le territoire, la durée, "
                "les conditions de performance et les conséquences du non-respect "
                "des objectifs."
            ),
            "ar": (
                "ينبغي مراجعة نطاق الحصرية، والمنطقة، والمدة، وشروط الأداء، "
                "وآثار عدم تحقيق الأهداف."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating objective performance thresholds, carve-outs, "
                "shorter exclusivity periods, or conversion to non-exclusive rights."
            ),
            "fr": (
                "Envisager de négocier des seuils de performance objectifs, "
                "des exceptions, une durée d'exclusivité plus courte ou une "
                "conversion en droits non exclusifs."
            ),
            "ar": (
                "يمكن التفاوض على مؤشرات أداء موضوعية، واستثناءات، ومدة "
                "حصرية أقصر، أو تحويل الحق إلى غير حصري."
            ),
        },
    },

    "governing_law": {
        "signals": [
            "governing law",
            "jurisdiction",
            "venue",
            "courts",
            "droit applicable",
            "juridiction",
            "tribunaux compétents",
            "tribunaux",
            "القانون الواجب التطبيق",
            "الاختصاص",
            "المحاكم",
            "محكمة",
        ],
        "legal_insight": {
            "en": (
                "This clause identifies the legal system or forum that will "
                "govern disputes under the contract."
            ),
            "fr": (
                "Cette clause désigne le droit applicable ou le forum compétent "
                "pour les litiges liés au contrat."
            ),
            "ar": (
                "تحدد هذه المادة القانون أو الجهة القضائية المختصة بالنزاعات "
                "المتعلقة بالعقد."
            ),
        },
        "recommendation": {
            "en": (
                "Confirm that the chosen law and forum are practical, accessible, "
                "and consistent with the parties' location and transaction."
            ),
            "fr": (
                "Vérifier que le droit choisi et le forum compétent sont "
                "pratiques, accessibles et cohérents avec la localisation des "
                "parties et l'opération."
            ),
            "ar": (
                "ينبغي التأكد من أن القانون والجهة المختارة عملية وميسرة "
                "ومتناسقة مع مكان الأطراف وطبيعة المعاملة."
            ),
        },
        "negotiation": {
            "en": (
                "Consider negotiating a neutral forum, arbitration, or a venue "
                "that reduces enforcement and travel burden."
            ),
            "fr": (
                "Envisager de négocier un forum neutre, l'arbitrage ou un lieu "
                "qui réduit les contraintes d'exécution et de déplacement."
            ),
            "ar": (
                "يمكن التفاوض على جهة محايدة، أو التحكيم، أو مكان يقلل "
                "أعباء التنفيذ والتنقل."
            ),
        },
    },
}


def detect_clause_type_from_text(text: str) -> str:
    normalized = str(text or "").lower()

    best_clause_type = "general"
    best_score = 0

    for clause_type, template in CLAUSE_REASONING_TEMPLATES.items():
        score = sum(
            1 for signal in template["signals"]
            if signal.lower() in normalized
        )

        if score > best_score:
            best_score = score
            best_clause_type = clause_type

    return best_clause_type if best_score else "general"


def get_clause_reasoning(
    clause_type: str,
    language: str = "en",
) -> dict:
    language = get_language(language)
    clause_type = str(clause_type or "general").lower()

    template = CLAUSE_REASONING_TEMPLATES.get(clause_type)

    if not template:
        return {
            "clause_type": "general",
            "legal_insight": "",
            "recommendation": "",
            "negotiation": "",
        }

    return {
        "clause_type": clause_type,
        "legal_insight": template["legal_insight"].get(
            language,
            template["legal_insight"]["en"],
        ),
        "recommendation": template["recommendation"].get(
            language,
            template["recommendation"]["en"],
        ),
        "negotiation": template["negotiation"].get(
            language,
            template["negotiation"]["en"],
        ),
    }


def get_clause_reasoning_for_text(
    text: str,
    language: str = "en",
) -> dict:
    clause_type = detect_clause_type_from_text(text)

    return get_clause_reasoning(
        clause_type,
        language,
    )
def get_reasoning_for_text(
    text: str,
    language: str = "en",
) -> dict:
    return get_clause_reasoning_for_text(
        text,
        language,
    )