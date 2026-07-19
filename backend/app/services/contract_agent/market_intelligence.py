"""
market_intelligence.py

Universal market-intelligence fallbacks for contract clauses.

Goals:
- Works for any contract family and industry.
- Supports EN / FR / AR.
- Uses clause_type only, not hard-coded contract-specific logic.
- Provides safe, cautious market comparison language.
"""

SUPPORTED_LANGUAGES = {"en", "fr", "ar"}

# === PRODUCER_AWARE_MULTI_CANDIDATE_COMPAT_V1 ===
# Direct canonical entries are preserved before compatibility aliases;
# legal_reasoning_templates selects market_comparison per producer field.


def get_language(language: str = "en") -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


MARKET_INTELLIGENCE = {
    "liability": {
        "practice": "commonly_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Liability clauses are common in commercial contracts, but caps, "
                "exclusions, carve-outs, and uncapped liabilities are frequently negotiated."
            ),
            "fr": (
                "Les clauses de responsabilité sont courantes dans les contrats commerciaux, "
                "mais les plafonds, exclusions, exceptions et responsabilités non plafonnées "
                "sont fréquemment négociés."
            ),
            "ar": (
                "تعد بنود المسؤولية شائعة في العقود التجارية، لكن حدود المسؤولية "
                "والاستثناءات والحالات غير المحدودة غالباً ما تكون محل تفاوض."
            ),
        },
    },

    "termination": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Termination clauses are common, but notice periods, cure rights, unilateral "
                "termination rights, and post-termination effects vary significantly."
            ),
            "fr": (
                "Les clauses de résiliation sont courantes, mais les préavis, droits de "
                "régularisation, droits unilatéraux et effets post-résiliation varient fortement."
            ),
            "ar": (
                "تعد بنود الإنهاء شائعة، لكن مدد الإشعار وحقوق المعالجة والإنهاء "
                "من جانب واحد وآثار ما بعد الإنهاء تختلف بشكل كبير."
            ),
        },
    },

    "confidentiality": {
        "practice": "very_common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Confidentiality clauses are very common. Market practice usually focuses on "
                "scope, exclusions, permitted disclosures, survival period, and return or destruction duties."
            ),
            "fr": (
                "Les clauses de confidentialité sont très courantes. La pratique porte souvent "
                "sur la portée, les exclusions, les divulgations autorisées, la durée de survie "
                "et les obligations de restitution ou destruction."
            ),
            "ar": (
                "تعد بنود السرية شائعة جداً. وتركز الممارسة عادة على النطاق "
                "والاستثناءات والإفصاحات المسموح بها ومدة البقاء وواجبات الإرجاع أو الإتلاف."
            ),
        },
    },

    "payment": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Payment clauses are standard, but payment timing, invoice disputes, interest, "
                "taxes, suspension rights, and late-payment consequences are often negotiated."
            ),
            "fr": (
                "Les clauses de paiement sont standards, mais les délais, contestations de facture, "
                "intérêts, taxes, droits de suspension et conséquences du retard sont souvent négociés."
            ),
            "ar": (
                "تعد بنود الدفع قياسية، لكن مواعيد الدفع واعتراضات الفواتير والفوائد "
                "والضرائب وحقوق التعليق وآثار التأخير غالباً ما تكون محل تفاوض."
            ),
        },
    },

    "sla": {
        "practice": "commonly_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Service-level clauses are common in service and technology contracts. Market practice "
                "varies on uptime targets, exclusions, service credits, reporting, and repeated-failure remedies."
            ),
            "fr": (
                "Les clauses de niveau de service sont courantes dans les contrats de services "
                "et de technologie. La pratique varie selon les objectifs de disponibilité, exclusions, "
                "crédits de service, reporting et recours en cas d’échecs répétés."
            ),
            "ar": (
                "تعد بنود مستوى الخدمة شائعة في عقود الخدمات والتقنية. وتختلف الممارسة "
                "بحسب نسب التوافر والاستثناءات وتعويضات الخدمة والتقارير ووسائل المعالجة عند تكرار الإخفاق."
            ),
        },
    },

    "data_privacy_security": {
        "practice": "commonly_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Data, privacy, and security clauses are common where information or systems are involved. "
                "Market practice varies on processing instructions, security standards, audit rights, "
                "incident notice, subprocessors, deletion, and liability treatment."
            ),
            "fr": (
                "Les clauses relatives aux données, à la confidentialité et à la sécurité sont courantes "
                "lorsque des informations ou systèmes sont concernés. La pratique varie selon les instructions "
                "de traitement, standards de sécurité, droits d’audit, notifications d’incident, sous-traitants, "
                "suppression et responsabilité."
            ),
            "ar": (
                "تعد بنود البيانات والخصوصية والأمن شائعة عندما تكون المعلومات أو الأنظمة معنية. "
                "وتختلف الممارسة بحسب تعليمات المعالجة ومعايير الأمن وحقوق التدقيق والإخطار بالحوادث "
                "والمعالجين الفرعيين والحذف ومعالجة المسؤولية."
            ),
        },
    },

    "intellectual_property": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Intellectual-property clauses are frequently negotiated, especially around ownership, "
                "background IP, deliverables, license scope, transfer timing, and residual rights."
            ),
            "fr": (
                "Les clauses de propriété intellectuelle sont fréquemment négociées, notamment concernant "
                "la propriété, les éléments préexistants, les livrables, la portée des licences, le moment "
                "du transfert et les droits résiduels."
            ),
            "ar": (
                "تكون بنود الملكية الفكرية غالباً محل تفاوض، خصوصاً فيما يتعلق بالملكية "
                "والحقوق السابقة والمخرجات ونطاق الترخيص وتوقيت النقل والحقوق المتبقية."
            ),
        },
    },

    "assignment": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Assignment clauses commonly restrict transfers without consent, while allowing limited exceptions "
                "for affiliates, reorganizations, mergers, or asset sales."
            ),
            "fr": (
                "Les clauses de cession limitent souvent les transferts sans consentement, avec des exceptions "
                "pour les affiliés, réorganisations, fusions ou ventes d’actifs."
            ),
            "ar": (
                "غالباً ما تقيد بنود التنازل نقل الحقوق أو الالتزامات دون موافقة، مع استثناءات "
                "محدودة للشركات التابعة أو إعادة التنظيم أو الاندماج أو بيع الأصول."
            ),
        },
    },

    "restrictive_covenants": {
        "practice": "often_sensitive",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Restrictive covenants are often sensitive and heavily context-dependent. Duration, territory, "
                "restricted activity, affected persons, and legitimate business justification are commonly negotiated."
            ),
            "fr": (
                "Les engagements restrictifs sont souvent sensibles et dépendent fortement du contexte. La durée, "
                "le territoire, les activités restreintes, les personnes concernées et la justification commerciale "
                "sont généralement négociés."
            ),
            "ar": (
                "تعد التعهدات التقييدية حساسة وغالباً ما تعتمد على السياق. وتكون المدة والنطاق "
                "والأنشطة المقيدة والأشخاص المعنيون والمبرر التجاري عادة محل تفاوض."
            ),
        },
    },

    "governing_law": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Governing-law and forum clauses are standard, but parties often negotiate neutrality, convenience, "
                "enforcement practicality, cost, language, and dispute-resolution process."
            ),
            "fr": (
                "Les clauses de droit applicable et de forum sont standards, mais les parties négocient souvent "
                "la neutralité, la praticité, l’exécution, les coûts, la langue et le processus de règlement des litiges."
            ),
            "ar": (
                "تعد بنود القانون الواجب التطبيق والاختصاص قياسية، لكن الأطراف غالباً ما تتفاوض "
                "على الحياد والملاءمة وسهولة التنفيذ والتكلفة واللغة وآلية تسوية النزاعات."
            ),
        },
    },

    "force_majeure": {
        "practice": "standard",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Force majeure clauses are standard and typically excuse non-performance caused by events "
                "beyond a party's reasonable control. Market practice varies on the definition of covered "
                "events, notice requirements, mitigation duties, and the point at which prolonged force "
                "majeure allows termination."
            ),
            "fr": (
                "Les clauses de force majeure sont standards et excusent généralement l’inexécution causée "
                "par des événements échappant au contrôle raisonnable d’une partie. La pratique varie selon "
                "la définition des événements couverts, les exigences de notification, les obligations "
                "d’atténuation et le seuil à partir duquel une force majeure prolongée permet la résiliation."
            ),
            "ar": (
                "تعد بنود القوة القاهرة قياسية وتُعفي عادة من عدم التنفيذ الناتج عن أحداث خارجة عن السيطرة "
                "المعقولة للطرف. وتختلف الممارسة بحسب تعريف الأحداث المشمولة ومتطلبات الإخطار وواجبات "
                "التخفيف والحد الذي يسمح عنده استمرار القوة القاهرة بالإنهاء."
            ),
        },
    },

    "warranty": {
        "practice": "commonly_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Warranty clauses are common and often the subject of negotiation, particularly around scope, "
                "duration, exclusions, disclaimers of implied warranties, and the remedies available for a breach."
            ),
            "fr": (
                "Les clauses de garantie sont courantes et souvent négociées, notamment quant à leur portée, "
                "leur durée, les exclusions, les exclusions de garanties implicites et les recours disponibles "
                "en cas de manquement."
            ),
            "ar": (
                "تعد بنود الضمان شائعة وغالباً ما تكون محل تفاوض، خصوصاً فيما يتعلق بالنطاق والمدة والاستثناءات "
                "واستبعاد الضمانات الضمنية ووسائل الانتصاف المتاحة عند الإخلال."
            ),
        },
    },

    "indemnification": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Indemnification clauses are common in commercial contracts and are frequently negotiated "
                "regarding scope of covered claims, caps, exclusions, procedure for claims, and interaction "
                "with liability limitations and insurance."
            ),
            "fr": (
                "Les clauses d’indemnisation sont courantes dans les contrats commerciaux et souvent négociées "
                "quant à la portée des réclamations couvertes, les plafonds, les exclusions, la procédure de "
                "réclamation et l’articulation avec les limitations de responsabilité et l’assurance."
            ),
            "ar": (
                "تعد بنود التعويض شائعة في العقود التجارية وغالباً ما تكون محل تفاوض فيما يتعلق بنطاق "
                "المطالبات المشمولة والحدود القصوى والاستثناءات وإجراءات المطالبة والعلاقة مع حدود المسؤولية "
                "والتأمين."
            ),
        },
    },

    "insurance": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Insurance clauses are common where risk allocation matters, and market practice varies on "
                "required coverage types, minimum amounts, certificates of insurance, additional insured "
                "status, and consequences of a coverage lapse."
            ),
            "fr": (
                "Les clauses d’assurance sont courantes lorsque la répartition des risques est importante, et "
                "la pratique varie selon les types de couverture exigés, les montants minimaux, les attestations "
                "d’assurance, le statut d’assuré additionnel et les conséquences d’une interruption de couverture."
            ),
            "ar": (
                "تعد بنود التأمين شائعة عندما يكون توزيع المخاطر مهماً، وتختلف الممارسة بحسب أنواع التغطية "
                "المطلوبة والحد الأدنى للمبالغ وشهادات التأمين وصفة المؤمَّن الإضافي وآثار انقطاع التغطية."
            ),
        },
    },

    "audit_rights": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Audit rights are common in commercial and services contracts, and market practice varies on "
                "scope, frequency, advance notice, confidentiality of findings, and allocation of audit costs."
            ),
            "fr": (
                "Les droits d’audit sont courants dans les contrats commerciaux et de services, et la pratique "
                "varie selon la portée, la fréquence, le préavis, la confidentialité des constatations et la "
                "répartition des coûts d’audit."
            ),
            "ar": (
                "تعد حقوق التدقيق شائعة في العقود التجارية وعقود الخدمات، وتختلف الممارسة بحسب النطاق "
                "والتكرار ومهلة الإشعار المسبق وسرية النتائج وتوزيع تكاليف التدقيق."
            ),
        },
    },

    "change_of_control": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Change-of-control provisions are common, particularly in longer-term or strategic contracts, "
                "and market practice varies on whether a change of control triggers notice, consent, or "
                "termination rights."
            ),
            "fr": (
                "Les clauses de changement de contrôle sont courantes, notamment dans les contrats à long terme "
                "ou stratégiques, et la pratique varie selon qu’un changement de contrôle déclenche une "
                "obligation de notification, de consentement ou un droit de résiliation."
            ),
            "ar": (
                "تعد بنود تغيير السيطرة شائعة، خصوصاً في العقود طويلة الأمد أو الاستراتيجية، وتختلف الممارسة "
                "بحسب ما إذا كان تغيير السيطرة يستوجب الإشعار أو الموافقة أو يمنح حق الإنهاء."
            ),
        },
    },

    "subcontracting": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Subcontracting clauses are common in service and supply contracts, and market practice varies "
                "on whether consent is required, the level of continued responsibility for subcontracted work, "
                "and flow-down obligations."
            ),
            "fr": (
                "Les clauses de sous-traitance sont courantes dans les contrats de services et de fourniture, "
                "et la pratique varie selon l’exigence de consentement, le niveau de responsabilité maintenue "
                "pour les travaux sous-traités et les obligations répercutées."
            ),
            "ar": (
                "تعد بنود التعاقد من الباطن شائعة في عقود الخدمات والتوريد، وتختلف الممارسة بحسب اشتراط "
                "الموافقة ومستوى استمرار المسؤولية عن الأعمال المتعاقد عليها من الباطن والالتزامات المنقولة "
                "إلى الباطن."
            ),
        },
    },

    "anti_bribery_compliance": {
        "practice": "standard",
        "negotiability": "low",
        "comparison": {
            "en": (
                "Anti-bribery and compliance clauses are increasingly standard in commercial contracts, and "
                "market practice varies on the compliance standards referenced, certification requirements, "
                "audit rights, and termination remedies for violations."
            ),
            "fr": (
                "Les clauses anti-corruption et de conformité sont de plus en plus standards dans les contrats "
                "commerciaux, et la pratique varie selon les normes de conformité visées, les exigences de "
                "certification, les droits d’audit et les recours en résiliation en cas de violation."
            ),
            "ar": (
                "أصبحت بنود مكافحة الرشوة والامتثال معياراً شائعاً بشكل متزايد في العقود التجارية، وتختلف "
                "الممارسة بحسب معايير الامتثال المرجعية ومتطلبات التصديق وحقوق التدقيق ووسائل الانتصاف "
                "بالإنهاء عند المخالفة."
            ),
        },
    },

    "export_control": {
        "practice": "standard",
        "negotiability": "low",
        "comparison": {
            "en": (
                "Export control and sanctions clauses are increasingly common where cross-border trade or "
                "technology transfer is involved, and market practice varies on representations, ongoing "
                "compliance duties, and remedies for a sanctioned-party event."
            ),
            "fr": (
                "Les clauses de contrôle des exportations et de sanctions sont de plus en plus courantes "
                "lorsque des échanges transfrontaliers ou des transferts de technologie sont concernés, et la "
                "pratique varie selon les déclarations, les obligations de conformité continue et les recours "
                "en cas d’événement lié à une partie sanctionnée."
            ),
            "ar": (
                "أصبحت بنود ضوابط التصدير والعقوبات شائعة بشكل متزايد عندما تكون التجارة العابرة للحدود أو "
                "نقل التقنية معنية، وتختلف الممارسة بحسب الإقرارات وواجبات الامتثال المستمر ووسائل الانتصاف "
                "في حال ظهور طرف خاضع للعقوبات."
            ),
        },
    },

    "notices": {
        "practice": "standard",
        "negotiability": "low",
        "comparison": {
            "en": (
                "Notice clauses are standard and largely administrative, though market practice varies on "
                "permitted delivery methods, deemed receipt timing, and designated addresses or contacts."
            ),
            "fr": (
                "Les clauses de notification sont standards et largement administratives, bien que la pratique "
                "varie selon les modes de transmission autorisés, le moment de la réception réputée et les "
                "adresses ou contacts désignés."
            ),
            "ar": (
                "تعد بنود الإشعار قياسية وإدارية إلى حد كبير، إلا أن الممارسة تختلف بحسب وسائل التسليم "
                "المسموح بها وتوقيت اعتبار الاستلام والعناوين أو جهات الاتصال المحددة."
            ),
        },
    },

    "entire_agreement": {
        "practice": "standard",
        "negotiability": "low",
        "comparison": {
            "en": (
                "Entire agreement clauses are standard boilerplate, and market practice varies mainly on "
                "whether prior representations, side letters, or course of dealing are expressly excluded "
                "or preserved."
            ),
            "fr": (
                "Les clauses d’intégralité de l’accord sont des clauses standards, et la pratique varie "
                "principalement selon que les déclarations antérieures, lettres annexes ou pratiques "
                "antérieures sont expressément exclues ou préservées."
            ),
            "ar": (
                "تعد بنود اكتمال الاتفاق بنوداً قياسية معتادة، وتختلف الممارسة أساساً بحسب ما إذا كانت "
                "الإقرارات السابقة أو الرسائل الملحقة أو التعاملات السابقة مستبعدة صراحة أو محفوظة."
            ),
        },
    },

    "severability": {
        "practice": "standard",
        "negotiability": "low",
        "comparison": {
            "en": (
                "Severability clauses are standard boilerplate intended to preserve the remainder of a "
                "contract if one provision is found unenforceable, with limited variation across market practice."
            ),
            "fr": (
                "Les clauses de divisibilité sont des clauses standards destinées à préserver le reste du "
                "contrat si une disposition est jugée inapplicable, avec des variations limitées selon la "
                "pratique du marché."
            ),
            "ar": (
                "تعد بنود قابلية الفصل بنوداً قياسية معتادة تهدف إلى الحفاظ على بقية العقد في حال تبين أن "
                "أحد الأحكام غير قابل للتنفيذ، مع تباين محدود في ممارسات السوق."
            ),
        },
    },

    "waiver": {
        "practice": "standard",
        "negotiability": "low",
        "comparison": {
            "en": (
                "No-waiver clauses are standard boilerplate providing that a failure to enforce a right does "
                "not waive it, with limited variation across market practice."
            ),
            "fr": (
                "Les clauses de non-renonciation sont des clauses standards prévoyant qu’un défaut d’exercice "
                "d’un droit ne vaut pas renonciation à celui-ci, avec des variations limitées selon la pratique "
                "du marché."
            ),
            "ar": (
                "تعد بنود عدم التنازل بنوداً قياسية معتادة تنص على أن عدم ممارسة حق ما لا يعني التنازل عنه، "
                "مع تباين محدود في ممارسات السوق."
            ),
        },
    },

    "third_party_rights": {
        "practice": "standard",
        "negotiability": "low",
        "comparison": {
            "en": (
                "No-third-party-beneficiary clauses are standard boilerplate limiting enforceable rights to "
                "the contracting parties, with limited variation across market practice."
            ),
            "fr": (
                "Les clauses excluant les tiers bénéficiaires sont des clauses standards limitant les droits "
                "exécutoires aux seules parties contractantes, avec des variations limitées selon la pratique "
                "du marché."
            ),
            "ar": (
                "تعد بنود استبعاد المستفيد من الغير بنوداً قياسية معتادة تقصر الحقوق القابلة للتنفيذ على "
                "الأطراف المتعاقدة، مع تباين محدود في ممارسات السوق."
            ),
        },
    },

    "survival": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Survival clauses are common and specify which obligations continue after termination or "
                "expiry, with market practice varying on the scope and duration of surviving provisions."
            ),
            "fr": (
                "Les clauses de survie sont courantes et précisent quelles obligations perdurent après la "
                "résiliation ou l’expiration, la pratique variant selon la portée et la durée des dispositions "
                "survivantes."
            ),
            "ar": (
                "تعد بنود الاستمرارية شائعة وتحدد الالتزامات التي تستمر بعد الإنهاء أو الانتهاء، وتختلف "
                "الممارسة بحسب نطاق ومدة الأحكام المستمرة."
            ),
        },
    },

    "most_favored_nation": {
        "practice": "commonly_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Most-favored-nation (MFN) clauses are less common outside pricing-sensitive sectors, and "
                "market practice varies on the scope of comparison, verification mechanisms, and the remedy "
                "if a more favorable term is found."
            ),
            "fr": (
                "Les clauses de la nation la plus favorisée (NPF) sont moins courantes en dehors des secteurs "
                "sensibles aux prix, et la pratique varie selon la portée de la comparaison, les mécanismes "
                "de vérification et le recours applicable si une condition plus favorable est constatée."
            ),
            "ar": (
                "تعد بنود الدولة الأولى بالرعاية أقل شيوعاً خارج القطاعات الحساسة للأسعار، وتختلف الممارسة "
                "بحسب نطاق المقارنة وآليات التحقق ووسيلة الانتصاف في حال وجود شرط أكثر تفضيلاً."
            ),
        },
    },

    "exclusivity": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Exclusivity clauses are frequently negotiated and heavily context-dependent, with market "
                "practice varying on scope, duration, territory, carve-outs, and performance thresholds "
                "required to maintain exclusivity."
            ),
            "fr": (
                "Les clauses d’exclusivité sont fréquemment négociées et dépendent fortement du contexte, la "
                "pratique variant selon la portée, la durée, le territoire, les exceptions et les seuils de "
                "performance requis pour maintenir l’exclusivité."
            ),
            "ar": (
                "تعد بنود الحصرية محل تفاوض متكرر وتعتمد بشدة على السياق، وتختلف الممارسة بحسب النطاق "
                "والمدة والإقليم والاستثناءات وحدود الأداء المطلوبة للحفاظ على الحصرية."
            ),
        },
    },

    "pricing_adjustment": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Pricing-adjustment clauses are common in longer-term contracts, and market practice varies "
                "on the adjustment index or method, frequency, notice requirements, and any caps on increases."
            ),
            "fr": (
                "Les clauses d’ajustement tarifaire sont courantes dans les contrats de longue durée, et la "
                "pratique varie selon l’indice ou la méthode d’ajustement, la fréquence, les exigences de "
                "notification et les éventuels plafonds d’augmentation."
            ),
            "ar": (
                "تعد بنود تعديل الأسعار شائعة في العقود طويلة الأمد، وتختلف الممارسة بحسب مؤشر أو طريقة "
                "التعديل والتكرار ومتطلبات الإخطار وأي حدود قصوى للزيادات."
            ),
        },
    },

    "publicity": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Publicity clauses are common, particularly where brand or reputation is involved, and market "
                "practice varies on whether prior written consent is required for public announcements, use "
                "of trademarks or logos, and case-study or reference rights."
            ),
            "fr": (
                "Les clauses de publicité sont courantes, notamment lorsque la marque ou la réputation est "
                "concernée, et la pratique varie selon l’exigence d’un consentement écrit préalable pour les "
                "annonces publiques, l’utilisation des marques ou logos, et les droits de référence ou "
                "d’étude de cas."
            ),
            "ar": (
                "تعد بنود الدعاية شائعة، خصوصاً عندما تكون العلامة التجارية أو السمعة معنية، وتختلف الممارسة "
                "بحسب اشتراط الموافقة الخطية المسبقة على الإعلانات العامة واستخدام العلامات التجارية أو "
                "الشعارات وحقوق الإشارة كمرجع أو دراسة حالة."
            ),
        },
    },

    "non_disparagement": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Non-disparagement clauses are common, especially in settlement, employment, and exit-related "
                "contracts, and market practice varies on scope, mutuality, duration, and exceptions for legal "
                "proceedings or regulatory disclosures."
            ),
            "fr": (
                "Les clauses de non-dénigrement sont courantes, notamment dans les contrats de transaction, "
                "d’emploi et de départ, et la pratique varie selon la portée, la réciprocité, la durée et les "
                "exceptions pour les procédures judiciaires ou divulgations réglementaires."
            ),
            "ar": (
                "تعد بنود عدم الإساءة شائعة، خصوصاً في عقود التسوية والعمل وإنهاء الخدمة، وتختلف الممارسة "
                "بحسب النطاق والتبادلية والمدة والاستثناءات المتعلقة بالإجراءات القضائية أو الإفصاحات "
                "التنظيمية."
            ),
        },
    },

    "financial_covenants": {
        "practice": "standard",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Financial covenants are standard in lending and investment agreements, and market practice "
                "varies on the specific ratios or thresholds used, testing frequency, cure periods, and "
                "consequences of a breach."
            ),
            "fr": (
                "Les engagements financiers sont standards dans les contrats de prêt et d’investissement, et "
                "la pratique varie selon les ratios ou seuils utilisés, la fréquence des tests, les délais de "
                "régularisation et les conséquences d’un manquement."
            ),
            "ar": (
                "تعد التعهدات المالية قياسية في عقود الإقراض والاستثمار، وتختلف الممارسة بحسب النسب أو "
                "الحدود المستخدمة وتكرار الاختبار ومهل المعالجة وعواقب المخالفة."
            ),
        },
    },

    "events_of_default": {
        "practice": "standard",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Events-of-default clauses are standard in finance contracts, and market practice varies on "
                "the triggers included, grace or cure periods, cross-default provisions, and acceleration or "
                "enforcement remedies."
            ),
            "fr": (
                "Les clauses de cas de défaut sont standards dans les contrats de financement, et la pratique "
                "varie selon les événements déclencheurs inclus, les délais de grâce ou de régularisation, "
                "les clauses de défaut croisé et les recours d’accélération ou d’exécution."
            ),
            "ar": (
                "تعد بنود حالات التعثر قياسية في عقود التمويل، وتختلف الممارسة بحسب الأحداث المحفزة المدرجة "
                "ومهل السماح أو المعالجة وأحكام التعثر المتبادل ووسائل التسريع أو التنفيذ."
            ),
        },
    },

    "security_collateral": {
        "practice": "standard",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Security and collateral clauses are standard where financing or credit risk is involved, and "
                "market practice varies on the assets pledged, perfection requirements, priority ranking, and "
                "release conditions."
            ),
            "fr": (
                "Les clauses de sûretés et garanties sont standards lorsque le financement ou le risque de "
                "crédit est concerné, et la pratique varie selon les actifs nantis, les exigences de "
                "constitution, le rang de priorité et les conditions de mainlevée."
            ),
            "ar": (
                "تعد بنود الضمانات والرهون قياسية عندما يكون التمويل أو مخاطر الائتمان معنية، وتختلف "
                "الممارسة بحسب الأصول المرهونة ومتطلبات الإتمام وترتيب الأولوية وشروط الإفراج."
            ),
        },
    },

    "conditions_precedent": {
        "practice": "standard",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Conditions-precedent clauses are standard in financing, investment, and acquisition "
                "agreements, and market practice varies on the specific conditions required, waiver rights, "
                "and the consequence of a condition not being satisfied."
            ),
            "fr": (
                "Les clauses de conditions suspensives sont standards dans les contrats de financement, "
                "d’investissement et d’acquisition, et la pratique varie selon les conditions spécifiques "
                "requises, les droits de renonciation et la conséquence du non-accomplissement d’une "
                "condition."
            ),
            "ar": (
                "تعد بنود الشروط الواقفة قياسية في عقود التمويل والاستثمار والاستحواذ، وتختلف الممارسة "
                "بحسب الشروط المحددة المطلوبة وحقوق التنازل وأثر عدم تحقق أحد الشروط."
            ),
        },
    },

    "purchase_price_adjustment": {
        "practice": "commonly_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Purchase-price-adjustment clauses are common in sale and acquisition agreements, and market "
                "practice varies on the adjustment mechanism (such as working-capital or earn-out structures), "
                "calculation methodology, dispute procedures, and payment timing."
            ),
            "fr": (
                "Les clauses d’ajustement du prix d’achat sont courantes dans les contrats de vente et "
                "d’acquisition, et la pratique varie selon le mécanisme d’ajustement (tel que le fonds de "
                "roulement ou les compléments de prix), la méthodologie de calcul, les procédures de "
                "contestation et le calendrier de paiement."
            ),
            "ar": (
                "تعد بنود تعديل سعر الشراء شائعة في عقود البيع والاستحواذ، وتختلف الممارسة بحسب آلية "
                "التعديل (مثل رأس المال العامل أو هياكل الدفعات الإضافية) ومنهجية الحساب وإجراءات النزاع "
                "وتوقيت الدفع."
            ),
        },
    },

    "title_and_risk_of_loss": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Title and risk-of-loss clauses are common in sale and supply agreements, and market practice "
                "varies on the point at which title and risk transfer, retention-of-title arrangements, and "
                "treatment of loss or damage in transit."
            ),
            "fr": (
                "Les clauses de transfert de propriété et de risque sont courantes dans les contrats de vente "
                "et de fourniture, et la pratique varie selon le moment du transfert de propriété et de "
                "risque, les clauses de réserve de propriété et le traitement des pertes ou dommages en "
                "transit."
            ),
            "ar": (
                "تعد بنود انتقال الملكية والمخاطر شائعة في عقود البيع والتوريد، وتختلف الممارسة بحسب لحظة "
                "انتقال الملكية والمخاطر وترتيبات الاحتفاظ بالملكية ومعالجة الفقدان أو التلف أثناء النقل."
            ),
        },
    },

    "delivery_and_acceptance": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Delivery and acceptance clauses are common in supply and services contracts, and market "
                "practice varies on delivery timelines, inspection rights, acceptance criteria, and remedies "
                "for rejected goods or deliverables."
            ),
            "fr": (
                "Les clauses de livraison et d’acceptation sont courantes dans les contrats de fourniture et "
                "de services, et la pratique varie selon les délais de livraison, les droits d’inspection, "
                "les critères d’acceptation et les recours en cas de rejet des biens ou livrables."
            ),
            "ar": (
                "تعد بنود التسليم والقبول شائعة في عقود التوريد والخدمات، وتختلف الممارسة بحسب مواعيد "
                "التسليم وحقوق الفحص ومعايير القبول ووسائل الانتصاف عند رفض البضائع أو المخرجات."
            ),
        },
    },

    "use_and_occupancy": {
        "practice": "standard",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Use-and-occupancy clauses are standard in lease agreements, and market practice varies on "
                "permitted use restrictions, exclusivity of use, compliance with zoning or building rules, "
                "and consequences of unauthorized use."
            ),
            "fr": (
                "Les clauses d’usage et d’occupation sont standards dans les contrats de bail, et la pratique "
                "varie selon les restrictions d’usage autorisé, l’exclusivité d’usage, la conformité aux "
                "règles d’urbanisme ou de construction et les conséquences d’un usage non autorisé."
            ),
            "ar": (
                "تعد بنود الاستخدام والإشغال قياسية في عقود الإيجار، وتختلف الممارسة بحسب قيود الاستخدام "
                "المسموح به وحصرية الاستخدام والامتثال لقواعد التنظيم العمراني أو البناء وعواقب الاستخدام "
                "غير المصرح به."
            ),
        },
    },

    "maintenance_and_repairs": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Maintenance-and-repair clauses are common in lease and equipment agreements, and market "
                "practice varies on which party bears responsibility for routine maintenance, structural "
                "repairs, and the consequences of neglect."
            ),
            "fr": (
                "Les clauses d’entretien et de réparation sont courantes dans les contrats de bail et "
                "d’équipement, et la pratique varie selon la partie responsable de l’entretien courant, des "
                "réparations structurelles, et les conséquences d’une négligence."
            ),
            "ar": (
                "تعد بنود الصيانة والإصلاح شائعة في عقود الإيجار والمعدات، وتختلف الممارسة بحسب الطرف "
                "المسؤول عن الصيانة الروتينية والإصلاحات الهيكلية وعواقب الإهمال."
            ),
        },
    },

    "rent_and_escalation": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Rent and escalation clauses are common in lease agreements, and market practice varies on "
                "the base rent, escalation index or fixed percentage, review frequency, and treatment of "
                "additional charges such as service fees."
            ),
            "fr": (
                "Les clauses de loyer et d’indexation sont courantes dans les contrats de bail, et la "
                "pratique varie selon le loyer de base, l’indice d’indexation ou le pourcentage fixe, la "
                "fréquence de révision et le traitement des charges additionnelles telles que les frais de "
                "service."
            ),
            "ar": (
                "تعد بنود الإيجار وزيادته شائعة في عقود الإيجار، وتختلف الممارسة بحسب الإيجار الأساسي "
                "ومؤشر أو نسبة الزيادة الثابتة وتكرار المراجعة ومعالجة الرسوم الإضافية مثل رسوم الخدمة."
            ),
        },
    },

    "corporate_governance": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Corporate-governance clauses are frequently negotiated in shareholder and investment "
                "agreements, and market practice varies on board composition and appointment rights, voting "
                "thresholds, reserved matters, and deadlock resolution mechanisms."
            ),
            "fr": (
                "Les clauses de gouvernance d’entreprise sont fréquemment négociées dans les pactes "
                "d’actionnaires et contrats d’investissement, et la pratique varie selon la composition du "
                "conseil et les droits de nomination, les seuils de vote, les matières réservées et les "
                "mécanismes de résolution des blocages."
            ),
            "ar": (
                "تعد بنود الحوكمة المؤسسية محل تفاوض متكرر في اتفاقيات المساهمين والاستثمار، وتختلف "
                "الممارسة بحسب تكوين مجلس الإدارة وحقوق التعيين وحدود التصويت والمسائل المحفوظة وآليات حل "
                "الجمود."
            ),
        },
    },

    "share_transfer_restrictions": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Share-transfer clauses are frequently negotiated in shareholder agreements, and market "
                "practice varies on rights of first refusal, tag-along and drag-along rights, lock-up "
                "periods, and permitted transfers to affiliates."
            ),
            "fr": (
                "Les clauses de cession d’actions sont fréquemment négociées dans les pactes d’actionnaires, "
                "et la pratique varie selon les droits de préemption, les droits de sortie conjointe et "
                "forcée, les périodes d’incessibilité et les cessions autorisées aux affiliés."
            ),
            "ar": (
                "تعد بنود نقل الأسهم محل تفاوض متكرر في اتفاقيات المساهمين، وتختلف الممارسة بحسب حقوق "
                "الأولوية في الشراء وحقوق المرافقة والإجبار في البيع وفترات حظر التصرف والتنازلات المسموح "
                "بها للشركات التابعة."
            ),
        },
    },

    "anti_dilution_preemptive_rights": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Anti-dilution and pre-emptive rights clauses are frequently negotiated in investment "
                "agreements, and market practice varies on the anti-dilution formula (such as full ratchet "
                "or weighted average), triggering events, and the scope of pre-emptive participation rights."
            ),
            "fr": (
                "Les clauses anti-dilution et de droits préférentiels de souscription sont fréquemment "
                "négociées dans les contrats d’investissement, et la pratique varie selon la formule "
                "anti-dilution (telle que le ratchet intégral ou la moyenne pondérée), les événements "
                "déclencheurs et la portée des droits de participation préférentielle."
            ),
            "ar": (
                "تعد بنود مكافحة التخفيف وحقوق الأولوية في الاكتتاب محل تفاوض متكرر في عقود الاستثمار، "
                "وتختلف الممارسة بحسب صيغة مكافحة التخفيف (مثل الراتشيت الكامل أو المتوسط المرجح) والأحداث "
                "المحفزة ونطاق حقوق المشاركة التفضيلية."
            ),
        },
    },

    "liquidation_preference": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Liquidation-preference clauses are frequently negotiated in investment agreements, and "
                "market practice varies on the preference multiple, participation rights, seniority ranking "
                "among share classes, and treatment on a sale, merger, or liquidation event."
            ),
            "fr": (
                "Les clauses de préférence de liquidation sont fréquemment négociées dans les contrats "
                "d’investissement, et la pratique varie selon le multiple de préférence, les droits de "
                "participation, le rang de priorité entre catégories d’actions et le traitement en cas de "
                "cession, fusion ou liquidation."
            ),
            "ar": (
                "تعد بنود أفضلية التصفية محل تفاوض متكرر في عقود الاستثمار، وتختلف الممارسة بحسب مضاعف "
                "الأفضلية وحقوق المشاركة وترتيب الأولوية بين فئات الأسهم والمعاملة عند البيع أو الاندماج أو "
                "التصفية."
            ),
        },
    },

    "independent_contractor_status": {
        "practice": "standard",
        "negotiability": "low",
        "comparison": {
            "en": (
                "Independent-contractor clauses are standard in consulting and services agreements, and "
                "market practice varies mainly on the specificity of language addressing misclassification "
                "risk, tax responsibility, and the absence of an employment relationship."
            ),
            "fr": (
                "Les clauses de statut d’entrepreneur indépendant sont standards dans les contrats de conseil "
                "et de services, et la pratique varie principalement selon la précision du langage traitant "
                "du risque de requalification, de la responsabilité fiscale et de l’absence de relation de "
                "travail."
            ),
            "ar": (
                "تعد بنود صفة المتعاقد المستقل قياسية في عقود الاستشارات والخدمات، وتختلف الممارسة أساساً "
                "بحسب دقة الصياغة المتعلقة بمخاطر إعادة التصنيف والمسؤولية الضريبية وغياب علاقة العمل."
            ),
        },
    },

    "key_personnel": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Key-personnel clauses are common in services and outsourcing agreements, and market practice "
                "varies on the process for designating key individuals, replacement and approval rights, and "
                "remedies if a key person departs."
            ),
            "fr": (
                "Les clauses de personnel clé sont courantes dans les contrats de services et "
                "d’externalisation, et la pratique varie selon le processus de désignation des personnes "
                "clés, les droits de remplacement et d’approbation, et les recours en cas de départ d’une "
                "personne clé."
            ),
            "ar": (
                "تعد بنود الموظفين الرئيسيين شائعة في عقود الخدمات والتعهيد، وتختلف الممارسة بحسب إجراء "
                "تحديد الأفراد الرئيسيين وحقوق الاستبدال والموافقة ووسائل الانتصاف في حال مغادرة أحدهم."
            ),
        },
    },

    "exit_transition": {
        "practice": "commonly_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Exit and transition clauses are common in outsourcing and managed-services agreements, and "
                "market practice varies on transition-out assistance, knowledge transfer, data return, and "
                "the duration and cost of post-termination support."
            ),
            "fr": (
                "Les clauses de sortie et de transition sont courantes dans les contrats d’externalisation et "
                "de services gérés, et la pratique varie selon l’assistance de sortie, le transfert de "
                "connaissances, la restitution des données, et la durée et le coût du support "
                "post-résiliation."
            ),
            "ar": (
                "تعد بنود الخروج والانتقال شائعة في عقود التعهيد والخدمات المدارة، وتختلف الممارسة بحسب "
                "مساعدة الخروج ونقل المعرفة وإرجاع البيانات ومدة وتكلفة الدعم بعد الإنهاء."
            ),
        },
    },

    "cross_border_data_transfer": {
        "practice": "commonly_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": (
                "Cross-border data-transfer clauses are increasingly common where data moves between "
                "jurisdictions, and market practice varies on the transfer mechanism used, such as standard "
                "contractual clauses, adequacy reliance, or binding corporate rules, and related notice and "
                "audit rights."
            ),
            "fr": (
                "Les clauses de transfert transfrontalier de données sont de plus en plus courantes lorsque "
                "des données circulent entre juridictions, et la pratique varie selon le mécanisme de "
                "transfert utilisé, tel que les clauses contractuelles types, la reconnaissance d’adéquation "
                "ou les règles d’entreprise contraignantes, ainsi que les droits de notification et d’audit "
                "associés."
            ),
            "ar": (
                "أصبحت بنود نقل البيانات عبر الحدود شائعة بشكل متزايد عندما تنتقل البيانات بين الولايات "
                "القضائية، وتختلف الممارسة بحسب آلية النقل المستخدمة، مثل البنود التعاقدية القياسية أو "
                "الاعتماد على قرار الكفاية أو القواعد المؤسسية الملزمة، وحقوق الإخطار والتدقيق المرتبطة بها."
            ),
        },
    },

    "tax": {
        "practice": "standard",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Tax clauses are standard in commercial contracts, and market practice varies on "
                "whether prices are tax-inclusive or exclusive, withholding tax treatment, gross-up "
                "obligations, and responsibility for tax documentation."
            ),
            "fr": (
                "Les clauses fiscales sont standards dans les contrats commerciaux, et la pratique "
                "varie selon que les prix incluent ou excluent les taxes, le traitement de la retenue "
                "à la source, les obligations de majoration et la responsabilité des documents fiscaux."
            ),
            "ar": (
                "تعد البنود الضريبية قياسية في العقود التجارية، وتختلف الممارسة بحسب ما إذا كانت "
                "الأسعار شاملة أو غير شاملة للضرائب، ومعالجة ضريبة الاستقطاع، والتزامات التعويض "
                "الضريبي، ومسؤولية المستندات الضريبية."
            ),
        },
    },

    "employment_terms": {
        "practice": "standard",
        "negotiability": "medium",
        "comparison": {
            "en": (
                "Employment-terms clauses are standard in employment agreements, and market practice "
                "varies on compensation structure, benefits, working conditions, and the specificity "
                "of duties and performance expectations."
            ),
            "fr": (
                "Les clauses de conditions d’emploi sont standards dans les contrats de travail, et la "
                "pratique varie selon la structure de rémunération, les avantages, les conditions de "
                "travail et la précision des fonctions et attentes de performance."
            ),
            "ar": (
                "تعد بنود شروط العمل قياسية في عقود العمل، وتختلف الممارسة بحسب هيكل التعويض "
                "والمزايا وظروف العمل ودقة المهام وتوقعات الأداء."
            ),
        },
    },
}


GENERAL_MARKET_COMPARISON = {
    "en": (
        "Comparable clauses are commonly seen across commercial contracts, but market practice "
        "varies depending on the transaction type, sector, bargaining position, jurisdiction, "
        "scope, duration, remedies, and exceptions."
    ),
    "fr": (
        "Des clauses comparables sont courantes dans les contrats commerciaux, mais la pratique "
        "du marché varie selon le type d’opération, le secteur, le pouvoir de négociation, "
        "la juridiction, la portée, la durée, les recours et les exceptions."
    ),
    "ar": (
        "تظهر بنود مماثلة بشكل شائع في العقود التجارية، لكن ممارسات السوق تختلف بحسب "
        "نوع المعاملة والقطاع ومركز التفاوض والاختصاص والنطاق والمدة ووسائل الانتصاف والاستثناءات."
    ),
}



# ---------------------------------------------------------------------------
# Direct canonical market entries for source-grounded taxonomy types
# ---------------------------------------------------------------------------
MARKET_INTELLIGENCE.update({
    "loan": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": "Loan provisions are frequently negotiated clause by clause, with practice varying according to the specific credit obligation, trigger, metric, timing, and remedy addressed.",
            "fr": "Les dispositions de prêt sont fréquemment négociées clause par clause, la pratique variant selon l'obligation de crédit, le déclencheur, l'indicateur, le calendrier et le recours précisément concernés.",
            "ar": "غالباً ما تُفاوض أحكام القروض مادةً بمادة، وتختلف الممارسة بحسب الالتزام الائتماني المحدد وسببه ومؤشره وتوقيته ووسيلة المعالجة المعنية.",
        },
    },
    "collateral": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": "Collateral provisions are frequently negotiated around the secured assets, secured obligations, priority, release mechanics, and enforcement trigger.",
            "fr": "Les sûretés sont fréquemment négociées quant aux actifs grevés, aux obligations garanties, au rang, aux mécanismes de mainlevée et au déclencheur de réalisation.",
            "ar": "غالباً ما تكون أحكام الضمانات العينية محل تفاوض بشأن الأصول المضمونة والالتزامات المضمونة والأولوية وآليات الإفراج وسبب التنفيذ.",
        },
    },
    "guarantee": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": "Guarantees are frequently negotiated around the guaranteed obligations, cap, duration, demand procedure, defenses, and release.",
            "fr": "Les garanties sont fréquemment négociées quant aux obligations garanties, au plafond, à la durée, à la procédure d'appel, aux moyens de défense et à la libération.",
            "ar": "غالباً ما تكون الكفالات محل تفاوض بشأن الالتزامات المكفولة والحد الأقصى والمدة وإجراءات المطالبة والدفوع والانتهاء.",
        },
    },
    "services": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": "Service-obligation clauses are common, with practice varying according to the specific duty, responsible party, stated standard, timing, and remedy.",
            "fr": "Les clauses d'obligations de service sont courantes, la pratique variant selon l'obligation précise, la partie responsable, le standard prévu, le calendrier et le recours.",
            "ar": "تعد بنود التزامات الخدمة شائعة، وتختلف الممارسة بحسب الواجب المحدد والطرف المسؤول والمعيار المنصوص عليه والتوقيت ووسيلة المعالجة.",
        },
    },
    "covenant": {
        "practice": "commonly_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": "Continuing covenants are commonly negotiated around objective standards, materiality, duration, compliance mechanics, cure rights, and breach consequences.",
            "fr": "Les engagements continus sont couramment négociés quant aux critères objectifs, à la matérialité, à la durée, aux modalités de conformité, aux droits de régularisation et aux conséquences du manquement.",
            "ar": "تكون التعهدات المستمرة عادة محل تفاوض بشأن المعايير الموضوعية والجوهرية والمدة وآليات الامتثال وحقوق المعالجة وآثار الإخلال.",
        },
    },
    "penalty": {
        "practice": "commonly_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": "Penalty and charge provisions are commonly negotiated around the trigger, calculation, cap, cumulative effect, and proportionality.",
            "fr": "Les pénalités et frais sont couramment négociés quant au déclencheur, au calcul, au plafond, à l'effet cumulatif et à la proportionnalité.",
            "ar": "تكون أحكام الجزاءات والرسوم عادة محل تفاوض بشأن سبب الاستحقاق وطريقة الاحتساب والحد والأثر التراكمي والتناسب.",
        },
    },
    "employment": {
        "practice": "commonly_negotiated",
        "negotiability": "medium",
        "comparison": {
            "en": "Employment terms are commonly negotiated according to the specific duty, benefit, restriction, trigger, duration, and consequence addressed.",
            "fr": "Les conditions d'emploi sont couramment négociées selon l'obligation, la prestation, la restriction, le déclencheur, la durée et la conséquence précisément concernés.",
            "ar": "تكون شروط العمل عادة محل تفاوض بحسب الواجب أو الميزة أو القيد أو السبب أو المدة أو الأثر المحدد في المادة.",
        },
    },
    "dispute_resolution": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": "Dispute-resolution clauses are standard, but escalation steps, forum, seat or venue, procedural rules, language, and interim relief are commonly negotiated.",
            "fr": "Les clauses de règlement des litiges sont standards, mais les étapes d'escalade, le forum, le siège ou lieu, les règles de procédure, la langue et les mesures provisoires sont couramment négociés.",
            "ar": "تعد بنود تسوية النزاعات قياسية، لكن مراحل التصعيد والجهة والمقر أو المكان والقواعد الإجرائية واللغة والتدابير المؤقتة غالباً ما تكون محل تفاوض.",
        },
    },
    "automatic_renewal": {
        "practice": "common",
        "negotiability": "medium",
        "comparison": {
            "en": "Automatic-renewal clauses are common, with market practice varying on renewal length, advance notice, non-renewal windows, and separately controlled renewal changes.",
            "fr": "Les clauses de renouvellement automatique sont courantes, la pratique variant selon la durée de renouvellement, le préavis, la fenêtre de non-renouvellement et les changements de renouvellement soumis à des contrôles distincts.",
            "ar": "تعد بنود التجديد التلقائي شائعة، وتختلف الممارسة بحسب مدة التجديد والإشعار المسبق ونافذة عدم التجديد والتغييرات المرتبطة بالتجديد والخاضعة لضوابط مستقلة.",
        },
    },
    "share_transfer_rights": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": "Share-transfer rights are frequently negotiated around the transfer trigger, affected shares, participation scope, notice, price parity, and completion mechanics.",
            "fr": "Les droits de transfert d'actions sont fréquemment négociés quant au déclencheur, aux actions concernées, à la participation, à la notification, à l'égalité de prix et aux modalités de réalisation.",
            "ar": "غالباً ما تكون حقوق نقل الأسهم محل تفاوض بشأن سبب النقل والأسهم المعنية ونطاق المشاركة والإشعار وتكافؤ السعر وآليات الإتمام.",
        },
    },
    "anti_dilution_preemptive_rights": {
        "practice": "frequently_negotiated",
        "negotiability": "high",
        "comparison": {
            "en": "Anti-dilution and preemptive-right provisions are frequently negotiated around covered issuances, formulas, exclusions, notice, and exercise periods.",
            "fr": "Les clauses anti-dilution et de droits préférentiels sont fréquemment négociées quant aux émissions couvertes, aux formules, aux exclusions, à la notification et aux délais d'exercice.",
            "ar": "غالباً ما تكون أحكام مكافحة التخفيف وحقوق الأولوية محل تفاوض بشأن الإصدارات المشمولة والصيغ والاستثناءات والإشعار ومهل الممارسة.",
        },
    },
})


def normalize_clause_type(clause_type: str) -> str:
    value = str(clause_type or "general").lower().strip()

    # Preserve a direct canonical entry before applying compatibility aliases.
    # This prevents canonical taxonomy types such as automatic_renewal,
    # compliance, collateral, or dispute_resolution from being widened when
    # a dedicated market entry already exists.
    if value in MARKET_INTELLIGENCE:
        return value

    aliases = {
        "limitation_of_liability": "liability",
        "limitation_of_liability_exceptions": "liability",
        "termination_for_convenience": "termination",
        "termination_for_cause": "termination",
        "automatic_renewal": "termination",
        "renewal": "termination",
        "service_level": "sla",
        "services_operations": "sla",
        "data_processing": "data_privacy_security",
        "data_protection": "data_privacy_security",
        "privacy": "data_privacy_security",
        "security": "data_privacy_security",
        "cybersecurity": "data_privacy_security",
        "confidential_information": "confidentiality",
        "non_solicitation": "restrictive_covenants",
        "non_compete": "restrictive_covenants",
        "intellectual_property_rights": "intellectual_property",
        "ip_assignment": "intellectual_property",
        "ownership": "intellectual_property",
        "assignment_of_deliverables": "intellectual_property",
        "dispute_resolution": "governing_law",
        "arbitration": "governing_law",
        "jurisdiction": "governing_law",
        "venue": "governing_law",
        "act_of_god": "force_majeure",
        "hardship": "force_majeure",
        "unforeseeable_circumstances": "force_majeure",
        "excuse_of_performance": "force_majeure",
        "warranties": "warranty",
        "representations_and_warranties": "warranty",
        "product_warranty": "warranty",
        "fitness_for_purpose": "warranty",
        "quality_warranty": "warranty",
        "indemnity": "indemnification",
        "hold_harmless": "indemnification",
        "defense_and_indemnification": "indemnification",
        "insurance_requirements": "insurance",
        "coverage_requirements": "insurance",
        "required_insurance": "insurance",
        "audit": "audit_rights",
        "inspection_rights": "audit_rights",
        "right_to_audit": "audit_rights",
        "records_and_audit": "audit_rights",
        "change_in_control": "change_of_control",
        "ownership_change": "change_of_control",
        "control_change": "change_of_control",
        "subcontractors": "subcontracting",
        "delegation_of_duties": "subcontracting",
        "use_of_subcontractors": "subcontracting",
        "anti_corruption": "anti_bribery_compliance",
        "compliance": "anti_bribery_compliance",
        "code_of_conduct": "anti_bribery_compliance",
        "fcpa": "anti_bribery_compliance",
        "bribery": "anti_bribery_compliance",
        "sanctions": "export_control",
        "trade_compliance": "export_control",
        "export_controls": "export_control",
        "sanctioned_parties": "export_control",
        "notice_clause": "notices",
        "communications": "notices",
        "notice_provision": "notices",
        "entire_agreement_clause": "entire_agreement",
        "integration_clause": "entire_agreement",
        "merger_clause": "entire_agreement",
        "whole_agreement": "entire_agreement",
        "severability_clause": "severability",
        "partial_invalidity": "severability",
        "invalidity": "severability",
        "no_waiver": "waiver",
        "waiver_clause": "waiver",
        "non_waiver": "waiver",
        "no_third_party_beneficiaries": "third_party_rights",
        "third_party_beneficiary": "third_party_rights",
        "third_party_rights_clause": "third_party_rights",
        "survival_clause": "survival",
        "surviving_obligations": "survival",
        "post_termination_survival": "survival",
        "mfn": "most_favored_nation",
        "most_favoured_nation": "most_favored_nation",
        "best_price_guarantee": "most_favored_nation",
        "exclusive_dealing": "exclusivity",
        "sole_source": "exclusivity",
        "exclusive_supply": "exclusivity",
        "price_adjustment": "pricing_adjustment",
        "fee_adjustment": "pricing_adjustment",
        "price_escalation": "pricing_adjustment",
        "indexation": "pricing_adjustment",
        "press_release": "publicity",
        "public_announcement": "publicity",
        "trademark_use": "publicity",
        "marketing_rights": "publicity",
        "non_disparagement_clause": "non_disparagement",
        "no_disparagement": "non_disparagement",
        "mutual_non_disparagement": "non_disparagement",
        "affirmative_covenants": "financial_covenants",
        "negative_covenants": "financial_covenants",
        "leverage_ratio": "financial_covenants",
        "financial_ratios": "financial_covenants",
        "default_clause": "events_of_default",
        "cross_default": "events_of_default",
        "acceleration": "events_of_default",
        "security_interest": "security_collateral",
        "collateral": "security_collateral",
        "pledge": "security_collateral",
        "lien": "security_collateral",
        "guarantee_and_security": "security_collateral",
        "closing_conditions": "conditions_precedent",
        "conditions_to_closing": "conditions_precedent",
        "drawdown_conditions": "conditions_precedent",
        "working_capital_adjustment": "purchase_price_adjustment",
        "earn_out": "purchase_price_adjustment",
        "price_true_up": "purchase_price_adjustment",
        "risk_of_loss": "title_and_risk_of_loss",
        "transfer_of_title": "title_and_risk_of_loss",
        "retention_of_title": "title_and_risk_of_loss",
        "delivery_terms": "delivery_and_acceptance",
        "acceptance_testing": "delivery_and_acceptance",
        "goods_acceptance": "delivery_and_acceptance",
        "permitted_use": "use_and_occupancy",
        "occupancy_clause": "use_and_occupancy",
        "repair_obligations": "maintenance_and_repairs",
        "upkeep": "maintenance_and_repairs",
        "rent_review": "rent_and_escalation",
        "rent_escalation": "rent_and_escalation",
        "base_rent": "rent_and_escalation",
        "board_composition": "corporate_governance",
        "voting_rights": "corporate_governance",
        "reserved_matters": "corporate_governance",
        "right_of_first_refusal": "share_transfer_restrictions",
        "tag_along": "share_transfer_restrictions",
        "drag_along": "share_transfer_restrictions",
        "lock_up": "share_transfer_restrictions",
        "anti_dilution": "anti_dilution_preemptive_rights",
        "preemptive_rights": "anti_dilution_preemptive_rights",
        "full_ratchet": "anti_dilution_preemptive_rights",
        "liquidation_rights": "liquidation_preference",
        "preference_stack": "liquidation_preference",
        "contractor_classification": "independent_contractor_status",
        "no_employment_relationship": "independent_contractor_status",
        "named_personnel": "key_personnel",
        "staffing_clause": "key_personnel",
        "transition_out": "exit_transition",
        "exit_assistance": "exit_transition",
        "reverse_transition": "exit_transition",
        "international_data_transfer": "cross_border_data_transfer",
        "data_transfer_mechanism": "cross_border_data_transfer",
        "standard_contractual_clauses": "cross_border_data_transfer",
        "scc": "cross_border_data_transfer",
        "security_measures": "data_privacy_security",
        "security_incident_notification": "data_privacy_security",
        "subprocessor_engagement": "data_privacy_security",
        "return_or_destruction": "data_privacy_security",
        "service_availability": "sla",
        "uptime_commitment_and_service_credits": "sla",
        "ownership_of_deliverables": "intellectual_property",
        "moral_rights_waiver": "intellectual_property",

        # Generic / fallback cleanup
        "other": "general",
        "general": "general",

        # Data / privacy / security (space-separated and long-form variants)
        "security incident notification": "data_privacy_security",
        "subprocessor engagement": "data_privacy_security",
        "data processing": "data_privacy_security",
        "return or destruction of personal data and confidential information": "data_privacy_security",

        # SLA / services (space-separated variants)
        "service availability": "sla",
        "uptime commitment and service credits": "sla",

        # IP (space-separated variants)
        "intellectual property rights": "intellectual_property",
        "ownership of deliverables": "intellectual_property",
        "assignment of deliverables": "intellectual_property",
        "moral rights waiver": "intellectual_property",

        # Liability (space-separated variants)
        "limitation of liability": "liability",
        "limitation of liability exceptions": "liability",

        # Termination (space-separated variants)
        "termination for convenience": "termination",
        "termination for cause": "termination",
        "term and renewal": "termination",
        "term_and_renewal": "termination",

        # Restrictive covenants (hyphen/space variants)
        "non-solicitation": "restrictive_covenants",
        "non solicitation": "restrictive_covenants",

        # Assignment (identity mapping)
        "assignment": "assignment",

        # legal_reasoning_templates.py compatibility: map reviewer's clause_type
        # keys (used as CLAUSE_REASONING_TEMPLATES / DOMAIN_TO_REASONING_TYPE
        # values) to the closest existing category so they get specific market
        # intelligence instead of falling back to the generic response.
        # NOTE: "services_operations" already maps to "sla" above.
        "governance_compliance": "corporate_governance",
        "finance_lending": "financial_covenants",
        "real_estate": "use_and_occupancy",
        "suspension": "termination",
        "business_continuity": "force_majeure",
        "amendment": "entire_agreement",
        "open_source": "intellectual_property",
        "escrow": "intellectual_property",
        "transition_assistance": "exit_transition",
        "employment_hr": "employment_terms",
    }

    return aliases.get(value, value)


def get_market_intelligence(
    clause_type: str,
    language: str = "en",
) -> dict:
    language = get_language(language)
    normalized_type = normalize_clause_type(clause_type)

    item = MARKET_INTELLIGENCE.get(normalized_type)

    if not item:
        return {
            "market_comparison": GENERAL_MARKET_COMPARISON[language],
            "market_practice": "standard",
            "market_benchmark": "common",
            "negotiability": "medium",
            "market_confidence": 0.65,
        }

    return {
        "market_comparison": item["comparison"].get(
            language,
            item["comparison"]["en"],
        ),
        "market_practice": item.get("practice", "standard"),
        "market_benchmark": item.get("practice", "common"),
        "negotiability": item.get("negotiability", "medium"),
        "market_confidence": 0.85,
    }


def get_market_comparison(
    clause_type: str,
    language: str = "en",
) -> str:
    return get_market_intelligence(
        clause_type,
        language,
    ).get("market_comparison", "")
