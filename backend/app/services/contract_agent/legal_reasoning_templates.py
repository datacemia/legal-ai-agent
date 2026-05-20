"""
Clause-type legal reasoning templates for contract analysis.

These templates complement domain-level reasoning by providing
specific reasoning for common clause categories:
liability, confidentiality, termination, SLA, indemnity, payment,
exclusivity, and governing law.
"""

from app.services.contract_agent.legal_ontology import (
    detect_legal_domains,
)


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


BOILERPLATE_CLAUSES = {
    "headings",
    "notices",
    "governing law",
    "employment agreement",
}


GENERIC_LEGAL_INSIGHTS = {
    "This clause creates contractual obligations or operational requirements that should be reviewed in the context of the overall agreement.",
    "This clause creates contractual obligations.",
}


GENERIC_RECOMMENDATIONS = {
    "Confirm that the clause is consistent with the commercial intent, operational process, and overall risk allocation.",
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
            "confidentiality obligations",
            "confidential information",
            "non-disclosure",
            "nda",
            "proprietary information",
            "post-employment obligations",
            "trade secret",
            "survive termination",
            "confidentialité",
            "obligations de confidentialité",
            "information confidentielle",
            "secret commercial",
            "السرية",
            "التزامات السرية",
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

    "general": {
        "signals": [],

        "legal_insight": {
            "en": (
                "This clause creates contractual obligations or operational "
                "requirements that should be reviewed in the context of the "
                "overall agreement."
            ),
            "fr": (
                "Cette clause crée des obligations contractuelles ou "
                "opérationnelles qui doivent être examinées dans le contexte "
                "global du contrat."
            ),
            "ar": (
                "تنشئ هذه المادة التزامات تعاقدية أو تشغيلية ينبغي "
                "مراجعتها ضمن السياق العام للعقد."
            ),
        },

        "recommendation": {
            "en": (
                "Confirm that the clause is consistent with the commercial "
                "intent, operational process, and overall risk allocation."
            ),
            "fr": (
                "Vérifier que cette clause est cohérente avec l'objectif "
                "commercial, les processus opérationnels et la répartition "
                "globale des risques."
            ),
            "ar": (
                "ينبغي التأكد من توافق هذه المادة مع الهدف التجاري "
                "والإجراءات التشغيلية والتوزيع العام للمخاطر."
            ),
        },

        "negotiation": {
            "en": "",
            "fr": "",
            "ar": "",
        },
    },
}



RISK_REASON_TEMPLATES = {
    "termination": [
        {
            "risk_pattern": [
                "without cause",
                "sans motif",
                "دون سبب",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause grants unilateral termination rights without "
                    "requiring objective justification, which may expose the "
                    "affected party to sudden contract loss or reduced bargaining leverage."
                ),
                "fr": (
                    "La clause accorde un droit de résiliation unilatérale sans "
                    "justification objective, ce qui peut exposer la partie concernée "
                    "à une rupture soudaine du contrat ou à une perte de pouvoir de négociation."
                ),
                "ar": (
                    "يمنح هذا البند حق الإنهاء من جانب واحد دون اشتراط مبرر موضوعي، "
                    "مما قد يعرّض الطرف المتأثر لفقدان العقد بشكل مفاجئ أو إضعاف موقفه التفاوضي."
                ),
            },
        },
        {
            "risk_pattern": [
                "immediate termination",
                "terminate immediately",
                "résiliation immédiate",
                "إنهاء فوري",
                "فسخ فوري",
            ],
            "risk_level": "high",
            "legal_consequence": {
                "en": (
                    "The clause allows immediate termination, so the absence or "
                    "shortness of notice and cure protections may create operational "
                    "or financial exposure."
                ),
                "fr": (
                    "La clause permet une résiliation immédiate ; l'absence ou la "
                    "brièveté du préavis et des possibilités de régularisation peut "
                    "créer une exposition opérationnelle ou financière."
                ),
                "ar": (
                    "يسمح هذا البند بالإنهاء الفوري، ولذلك فإن غياب الإشعار أو "
                    "مهلة المعالجة قد يخلق تعرضاً تشغيلياً أو مالياً."
                ),
            },
        },
        {
            "risk_pattern": [
                "cure period",
                "notice period",
                "délai de régularisation",
                "préavis",
                "مهلة معالجة",
                "إشعار",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause includes procedural safeguards such as notice or "
                    "a cure period, but the timing, required detail, and consequences "
                    "should still be reviewed carefully."
                ),
                "fr": (
                    "La clause prévoit des garanties procédurales comme un préavis "
                    "ou un délai de régularisation, mais les délais, le niveau de détail "
                    "requis et les conséquences doivent être examinés attentivement."
                ),
                "ar": (
                    "يتضمن البند ضمانات إجرائية مثل الإشعار أو مهلة المعالجة، "
                    "لكن يجب مراجعة المدة والتفاصيل المطلوبة والآثار المترتبة بعناية."
                ),
            },
        },
    ],
    "payment": [
        {
            "risk_pattern": [
                "late payment",
                "interest",
                "penalty",
                "retard de paiement",
                "intérêt",
                "pénalité",
                "تأخر الدفع",
                "فائدة",
                "غرامة",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause may impose financial consequences for delayed or failed "
                    "payment, so deadlines, interest, penalties, tax treatment, and "
                    "dispute rights should be clear."
                ),
                "fr": (
                    "La clause peut imposer des conséquences financières en cas de retard "
                    "ou défaut de paiement ; les échéances, intérêts, pénalités, traitement "
                    "fiscal et droits de contestation doivent être clairs."
                ),
                "ar": (
                    "قد يفرض هذا البند آثاراً مالية عند التأخر أو الإخفاق في الدفع، "
                    "لذلك يجب توضيح الآجال والفوائد والغرامات والمعالجة الضريبية وحقوق الاعتراض."
                ),
            },
        },
    ],
    "confidentiality": [
        {
            "risk_pattern": [
                "survive termination",
                "after termination",
                "thereafter",
                "survie",
                "après résiliation",
                "بعد الإنهاء",
                "تظل",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The confidentiality obligation may continue after the agreement ends, "
                    "so duration, scope, exceptions, and permitted disclosures should be "
                    "clearly defined."
                ),
                "fr": (
                    "L'obligation de confidentialité peut se poursuivre après la fin du contrat ; "
                    "la durée, la portée, les exceptions et les divulgations autorisées doivent "
                    "être clairement définies."
                ),
                "ar": (
                    "قد تستمر التزامات السرية بعد انتهاء العقد، لذلك يجب تحديد المدة والنطاق "
                    "والاستثناءات وحالات الإفصاح المسموح بها بوضوح."
                ),
            },
        },
    ],
    "liability": [
        {
            "risk_pattern": [
                "unlimited liability",
                "responsabilité illimitée",
                "مسؤولية غير محدودة",
            ],
            "risk_level": "high",
            "legal_consequence": {
                "en": (
                    "The clause may create uncapped financial exposure, which can exceed "
                    "the contract value and materially increase legal or commercial risk."
                ),
                "fr": (
                    "La clause peut créer une exposition financière non plafonnée, susceptible "
                    "de dépasser la valeur du contrat et d'accroître fortement le risque juridique "
                    "ou commercial."
                ),
                "ar": (
                    "قد يخلق هذا البند تعرضاً مالياً غير محدود قد يتجاوز قيمة العقد ويزيد "
                    "المخاطر القانونية أو التجارية بشكل كبير."
                ),
            },
        },
        {
            "risk_pattern": [
                "indirect damages",
                "consequential damages",
                "dommages indirects",
                "أضرار غير مباشرة",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause affects recovery of indirect or consequential losses, so exclusions "
                    "and carve-outs should be checked against the transaction risk."
                ),
                "fr": (
                    "La clause affecte la réparation des dommages indirects ou consécutifs ; les "
                    "exclusions et exceptions doivent être vérifiées au regard du risque de l'opération."
                ),
                "ar": (
                    "يؤثر هذا البند على التعويض عن الأضرار غير المباشرة أو التبعية، لذلك يجب "
                    "مراجعة الاستثناءات وفقاً لمخاطر المعاملة."
                ),
            },
        },
    ],
    "indemnity": [
        {
            "risk_pattern": [
                "defend",
                "hold harmless",
                "third-party claims",
                "défendre",
                "tenir indemne",
                "réclamations de tiers",
                "الدفاع عن",
                "مطالبات الغير",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause may require one party to cover defense costs or third-party claims, "
                    "so notice, control of defense, settlement rights, and liability limits should "
                    "be reviewed."
                ),
                "fr": (
                    "La clause peut imposer la prise en charge des frais de défense ou des réclamations "
                    "de tiers ; il faut vérifier l'avis, le contrôle de la défense, les transactions "
                    "et les limites de responsabilité."
                ),
                "ar": (
                    "قد يفرض هذا البند تحمل تكاليف الدفاع أو مطالبات الغير، لذلك يجب مراجعة الإشعار "
                    "والسيطرة على الدفاع وحقوق التسوية وحدود المسؤولية."
                ),
            },
        },
    ],
    "sla": [
        {
            "risk_pattern": [
                "uptime",
                "availability",
                "service credit",
                "disponibilité",
                "crédit de service",
                "التوافر",
                "تعويض الخدمة",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause defines measurable service commitments, so measurement periods, "
                    "exclusions, credits, reporting, and repeated-failure remedies should be clear."
                ),
                "fr": (
                    "La clause définit des engagements de service mesurables ; les périodes de mesure, "
                    "exclusions, crédits, reporting et recours en cas d'échecs répétés doivent être clairs."
                ),
                "ar": (
                    "يحدد هذا البند التزامات خدمة قابلة للقياس، لذلك يجب توضيح فترات القياس "
                    "والاستثناءات والتعويضات والتقارير ووسائل المعالجة عند تكرار الإخفاق."
                ),
            },
        },
    ],
    "exclusivity": [
        {
            "risk_pattern": [
                "exclusive",
                "exclusivity",
                "sole provider",
                "exclusif",
                "exclusivité",
                "حصري",
                "حصرية",
            ],
            "risk_level": "medium",
            "legal_consequence": {
                "en": (
                    "The clause may restrict work with alternative partners, suppliers, customers, "
                    "or territories, so duration, scope, performance conditions, and carve-outs "
                    "should be reviewed."
                ),
                "fr": (
                    "La clause peut limiter le recours à d'autres partenaires, fournisseurs, clients "
                    "ou territoires ; la durée, la portée, les conditions de performance et les exceptions "
                    "doivent être vérifiées."
                ),
                "ar": (
                    "قد يقيّد هذا البند التعامل مع شركاء أو موردين أو عملاء أو مناطق بديلة، لذلك يجب "
                    "مراجعة المدة والنطاق وشروط الأداء والاستثناءات."
                ),
            },
        },
    ],
    "governing_law": [
        {
            "risk_pattern": [
                "arbitration",
                "jurisdiction",
                "venue",
                "arbitrage",
                "juridiction",
                "tribunaux",
                "تحكيم",
                "اختصاص",
                "محكمة",
            ],
            "risk_level": "low",
            "legal_consequence": {
                "en": (
                    "The clause determines where and how disputes are resolved, so enforceability, "
                    "cost, language, and practical access to the forum should be checked."
                ),
                "fr": (
                    "La clause détermine où et comment les litiges seront résolus ; il faut vérifier "
                    "l'exécution, le coût, la langue et l'accès pratique au forum."
                ),
                "ar": (
                    "يحدد هذا البند مكان وطريقة حل النزاعات، لذلك يجب مراجعة قابلية التنفيذ والتكلفة "
                    "واللغة وسهولة الوصول إلى الجهة المختصة."
                ),
            },
        },
    ],
}


def get_contextual_risk_reasoning(
    clause_type: str,
    text: str,
    language: str = "en",
) -> dict:
    language = get_language(language)
    normalized = str(text or "").lower()

    for template in RISK_REASON_TEMPLATES.get(clause_type, []):
        risk_pattern = [
            str(signal).lower()
            for signal in template.get("risk_pattern", [])
        ]

        if any(signal in normalized for signal in risk_pattern):
            return {
                "clause_type": clause_type,
                "risk_level": template.get("risk_level", "medium"),
                "legal_insight": template["legal_consequence"].get(
                    language,
                    template["legal_consequence"].get("en", ""),
                ),
                "contextual_reasoning": True,
            }

    return {}

def normalize_clause_title(
    title: str,
) -> str:

    normalized = str(title or "").lower().strip()

    replacements = {
        "termination for cause":
            "termination",

        "constructive termination":
            "termination",

        "termination without cause":
            "termination",

        "confidentiality obligations":
            "confidentiality",

        "governing law":
            "governing_law",

        "notices":
            "general",

        "expense reimbursement":
            "payment",

        "change of control":
            "termination",
    }

    for source, target in replacements.items():
        if source in normalized:
            return target

    return normalized.replace(" ", "_")


def detect_clause_type_from_text(
    text: str,
    title: str = "",
) -> str:

    normalized_clause_title = normalize_clause_title(
        title
    )

    if normalized_clause_title in CLAUSE_REASONING_TEMPLATES:
        return normalized_clause_title

    normalized_text = str(text or "").lower()
    normalized_title = str(title or "").lower()

    # only first 500 chars matter
    intro_text = normalized_text[:500]

    best_clause_type = "general"
    best_score = 0

    for clause_type, template in CLAUSE_REASONING_TEMPLATES.items():

        signals = [
            s.lower()
            for s in template["signals"]
        ]

        title_score = sum(
            5
            for signal in signals
            if signal in normalized_title
        )

        intro_score = sum(
            2
            for signal in signals
            if signal in intro_text
        )

        # full body is intentionally weak
        body_score = sum(
            0.25
            for signal in signals
            if signal in normalized_text
        )

        total_score = (
            title_score
            + intro_score
            + body_score
        )

        if total_score > best_score:
            best_score = total_score
            best_clause_type = clause_type

    # avoid weak accidental matches
    if best_score < 3:

        ontology_domains = detect_legal_domains(
            text
        )

        if ontology_domains:
            return ontology_domains[0]

        return "general"

    return best_clause_type


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
    title: str = "",
) -> dict:
    clause_type = detect_clause_type_from_text(
        text,
        title=title,
    )

    base_reasoning = get_clause_reasoning(
        clause_type,
        language,
    )

    contextual_reasoning = get_contextual_risk_reasoning(
        clause_type,
        text,
        language,
    )

    if contextual_reasoning:
        base_reasoning["legal_insight"] = contextual_reasoning.get(
            "legal_insight",
            base_reasoning.get("legal_insight", ""),
        )
        base_reasoning["risk_level"] = contextual_reasoning.get(
            "risk_level",
            base_reasoning.get("risk_level", "medium"),
        )
        base_reasoning["contextual_reasoning"] = True
    else:
        base_reasoning["contextual_reasoning"] = False

    normalized_title = str(title or "").lower().strip()

    if normalized_title in BOILERPLATE_CLAUSES:
        base_reasoning["recommendation"] = ""

    if (
        base_reasoning.get("legal_insight")
        ==
        base_reasoning.get("recommendation")
    ):
        base_reasoning["recommendation"] = ""

    legal_insight = str(
        base_reasoning.get(
            "legal_insight",
            "",
        )
    ).strip()

    if legal_insight in GENERIC_LEGAL_INSIGHTS:
        base_reasoning["legal_insight"] = ""

    recommendation = str(
        base_reasoning.get(
            "recommendation",
            "",
        )
    ).strip()

    if recommendation in GENERIC_RECOMMENDATIONS:
        base_reasoning["recommendation"] = ""

    return base_reasoning
def get_reasoning_for_text(
    text: str,
    language: str = "en",
    title: str = "",
) -> dict:
    return get_clause_reasoning_for_text(
        text=text,
        language=language,
        title=title,
    )