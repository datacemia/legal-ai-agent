"""
clause_wording_library.py

Universal safer-alternative wording library.

Goals:
- Works across contract families, sectors, and jurisdictions.
- Supports EN / FR / AR.
- Gives cautious, generic fallback wording.
- Does not provide jurisdiction-specific legal advice.
"""

SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def get_language(language: str = "en") -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


WORDING_LIBRARY = {
    "liability": {
        "en": (
            "A safer alternative is to define a clear liability cap, specify excluded damages, "
            "and state any carve-outs such as fraud, wilful misconduct, confidentiality breaches, "
            "data protection breaches, payment obligations, or indemnity obligations."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir un plafond de responsabilité clair, "
            "à préciser les dommages exclus et à indiquer les exceptions telles que la fraude, "
            "la faute intentionnelle, les violations de confidentialité, les violations de données, "
            "les obligations de paiement ou d’indemnisation."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد سقف واضح للمسؤولية، وبيان الأضرار المستثناة، "
            "وتوضيح الاستثناءات مثل الاحتيال أو الخطأ العمدي أو خرق السرية أو خرق حماية البيانات "
            "أو التزامات الدفع أو التعويض."
        ),
    },

    "pricing": {
        "en": (
            "A safer alternative is to fix pricing for a defined initial period, permit adjustment "
            "no more than once per year, tie any increase to an objective, verifiable index or "
            "documented cost basis, and cap the maximum annual increase."
        ),
        "fr": (
            "Une alternative plus sûre consiste à fixer les prix pour une période initiale définie, "
            "à limiter les ajustements à une fois par an au maximum, à indexer toute hausse sur un "
            "indice objectif et vérifiable ou une base de coûts documentée, et à plafonner la hausse "
            "annuelle maximale."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تثبيت الأسعار لفترة أولية محددة، والسماح بالتعديل مرة واحدة "
            "في السنة كحد أقصى، وربط أي زيادة بمؤشر موضوعي وقابل للتحقق أو أساس تكلفة موثق، "
            "وتحديد سقف أقصى للزيادة السنوية."
        ),
    },

    "moral_rights": {
        "en": (
            "A safer alternative is to limit any moral rights waiver to the extent strictly necessary "
            "and permitted under applicable law, preserve the right to be identified as author where "
            "legally required, and require the assignee's consent before any modification that would "
            "harm the creator's reputation."
        ),
        "fr": (
            "Une alternative plus sûre consiste à limiter toute renonciation aux droits moraux à ce "
            "qui est strictement nécessaire et permis par le droit applicable, à préserver le droit "
            "à la paternité lorsque la loi l’exige, et à exiger le consentement du cessionnaire avant "
            "toute modification susceptible de nuire à la réputation du créateur."
        ),
        "ar": (
            "البديل الأكثر أماناً هو قصر أي تنازل عن الحقوق المعنوية على ما هو ضروري ومسموح به "
            "بموجب القانون المعمول به، والحفاظ على الحق في نسب العمل عند اقتضاء القانون ذلك، "
            "واشتراط موافقة المتنازل له قبل أي تعديل قد يضر بسمعة المُبدع."
        ),
    },

    "work_product": {
        "en": (
            "A safer alternative is to separate background IP retained by the creating party from "
            "newly created deliverables, define the ownership transfer timing (e.g. upon full payment "
            "rather than upon creation), specify any license the creating party retains for its own "
            "background tools, and state post-termination usage rights."
        ),
        "fr": (
            "Une alternative plus sûre consiste à distinguer la propriété intellectuelle préexistante "
            "conservée par la partie créatrice des livrables nouvellement créés, à définir le moment "
            "du transfert de propriété (par exemple au paiement intégral plutôt qu’à la création), à "
            "préciser toute licence conservée par la partie créatrice sur ses outils préexistants, et "
            "à indiquer les droits d’usage après résiliation."
        ),
        "ar": (
            "البديل الأكثر أماناً هو الفصل بين الملكية الفكرية السابقة التي تحتفظ بها الجهة المُنشئة "
            "والمخرجات المُستحدثة، وتحديد توقيت نقل الملكية (كأن يكون عند السداد الكامل بدلاً من "
            "لحظة الإنشاء)، وتوضيح أي ترخيص تحتفظ به الجهة المُنشئة لأدواتها السابقة، وبيان حقوق "
            "الاستخدام بعد انتهاء العقد."
        ),
    },

    "termination": {
        "en": (
            "A safer alternative is to define termination triggers, notice periods, cure rights, "
            "effective dates, accrued rights, transition duties, and post-termination obligations."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir les causes de résiliation, les préavis, "
            "les droits de régularisation, les dates d’effet, les droits acquis, les obligations "
            "de transition et les obligations post-résiliation."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد أسباب الإنهاء ومدد الإشعار وحقوق المعالجة "
            "وتاريخ النفاذ والحقوق المكتسبة وواجبات الانتقال والالتزامات بعد الإنهاء."
        ),
    },

    "automatic_renewal": {
        "en": (
            "A safer alternative is to require affirmative renewal consent rather than automatic renewal, "
            "or if automatic renewal is retained, to cap the number of renewal cycles, fix the renewal "
            "term length, set a clear non-renewal notice deadline well before expiry, and specify whether "
            "pricing carries over unchanged or is subject to adjustment at each renewal."
        ),
        "fr": (
            "Une alternative plus sûre consiste à exiger un consentement exprès au renouvellement plutôt "
            "qu'un renouvellement automatique, ou, si le renouvellement automatique est conservé, à plafonner "
            "le nombre de cycles de renouvellement, à fixer la durée du renouvellement, à établir une date "
            "limite claire de notification de non-renouvellement bien avant l'échéance, et à préciser si les "
            "tarifs restent inchangés ou peuvent être ajustés à chaque renouvellement."
        ),
        "ar": (
            "البديل الأكثر أماناً هو اشتراط موافقة صريحة على التجديد بدلاً من التجديد التلقائي، أو في حال "
            "الإبقاء على التجديد التلقائي، تحديد سقف لعدد دورات التجديد، وتثبيت مدة التجديد، ووضع موعد "
            "نهائي واضح لإشعار عدم التجديد قبل انتهاء المدة بوقت كافٍ، وتوضيح ما إذا كانت الأسعار تبقى "
            "دون تغيير أو تخضع للتعديل عند كل تجديد."
        ),
    },

    "confidentiality": {
        "en": (
            "A safer alternative is to define Confidential Information, exclusions, permitted disclosures, "
            "security duties, survival period, and return or destruction obligations."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir les informations confidentielles, les exclusions, "
            "les divulgations autorisées, les obligations de sécurité, la durée de survie et les obligations "
            "de restitution ou destruction."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تعريف المعلومات السرية والاستثناءات والإفصاحات المسموح بها "
            "وواجبات الأمن ومدة البقاء وواجبات الإرجاع أو الإتلاف."
        ),
    },

    "confidentiality_general": {
        "en": (
            "A safer alternative is to state the non-disclosure obligation clearly, name who it binds "
            "(the receiving party and its representatives), require at least the same level of protection "
            "for any authorized sub-disclosure, and specify the standard of care expected (e.g. the same "
            "care used for the receiving party's own confidential information, but no less than reasonable care)."
        ),
        "fr": (
            "Une alternative plus sûre consiste à énoncer clairement l'obligation de non-divulgation, à "
            "préciser qui elle engage (la partie réceptrice et ses représentants), à exiger un niveau de "
            "protection au moins équivalent pour toute sous-divulgation autorisée, et à préciser le niveau "
            "de soin attendu (par exemple le même soin que celui appliqué à ses propres informations "
            "confidentielles, sans être inférieur à un soin raisonnable)."
        ),
        "ar": (
            "البديل الأكثر أماناً هو النص بوضوح على التزام عدم الإفصاح، وتحديد الأطراف الملزمة به (الطرف "
            "المتلقي وممثلوه)، واشتراط مستوى حماية مماثل على الأقل لأي إفصاح فرعي مصرح به، وتحديد معيار "
            "العناية المتوقع (كالعناية المطبقة على معلوماته السرية الخاصة، على ألا يقل عن العناية المعقولة)."
        ),
    },

    "confidentiality_use_restriction": {
        "en": (
            "A safer alternative is to define the permitted purpose narrowly and precisely, state that "
            "Confidential Information may not be used for any other purpose (including competitive analysis "
            "or independent development based on it), and clarify whether internal evaluation, benchmarking, "
            "or affiliate use falls within or outside the permitted purpose."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir la finalité autorisée de manière étroite et "
            "précise, à préciser que les Informations Confidentielles ne peuvent être utilisées à aucune "
            "autre fin (y compris l'analyse concurrentielle ou le développement indépendant fondé sur ces "
            "informations), et à clarifier si l'évaluation interne, le benchmarking ou l'usage par des "
            "affiliés entre dans le périmètre de la finalité autorisée."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد الغرض المصرح به بدقة وضيق، والنص على عدم جواز استخدام المعلومات "
            "السرية لأي غرض آخر (بما في ذلك التحليل التنافسي أو التطوير المستقل بناءً عليها)، وتوضيح ما إذا "
            "كان التقييم الداخلي أو المقارنة المرجعية أو استخدام الشركات التابعة يدخل ضمن الغرض المصرح به."
        ),
    },

    "confidentiality_exclusions": {
        "en": (
            "A safer alternative is to keep the standard four exclusions (public without breach, already "
            "known, independently developed, lawfully received from a third party) but require the "
            "receiving party to bear the burden of proving an exclusion applies, and to require prompt "
            "written notice before relying on the independent-development or already-known exclusions."
        ),
        "fr": (
            "Une alternative plus sûre consiste à conserver les quatre exclusions usuelles (information "
            "publique sans faute, déjà connue, développée indépendamment, reçue légitimement d'un tiers), "
            "tout en faisant peser sur la partie réceptrice la charge de prouver qu'une exclusion "
            "s'applique, et en exigeant une notification écrite rapide avant de se prévaloir des exclusions "
            "de développement indépendant ou de connaissance préalable."
        ),
        "ar": (
            "البديل الأكثر أماناً هو الإبقاء على الاستثناءات القياسية الأربعة (المعلومات العامة دون خطأ، "
            "المعروفة مسبقاً، المطورة بشكل مستقل، المستلمة بشكل قانوني من طرف ثالث)، مع تحميل الطرف المتلقي "
            "عبء إثبات انطباق أي استثناء، واشتراط إخطار كتابي فوري قبل الاعتماد على استثناءي التطوير "
            "المستقل أو المعرفة المسبقة."
        ),
    },

    "confidentiality_duration": {
        "en": (
            "A safer alternative is to set a defined survival period for the confidentiality obligations "
            "(commonly two to five years after disclosure or after termination), while carving out an "
            "indefinite survival period specifically for trade secrets for as long as they remain protectable "
            "as such under applicable law."
        ),
        "fr": (
            "Une alternative plus sûre consiste à fixer une durée de survie définie pour les obligations de "
            "confidentialité (généralement de deux à cinq ans à compter de la divulgation ou de la "
            "résiliation), tout en prévoyant une durée de survie illimitée spécifiquement pour les secrets "
            "commerciaux tant qu'ils demeurent protégeables comme tels au regard du droit applicable."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد مدة بقاء محددة لالتزامات السرية (عادة من سنتين إلى خمس سنوات من "
            "تاريخ الإفصاح أو الإنهاء)، مع النص على مدة بقاء غير محددة خصيصاً للأسرار التجارية طالما ظلت "
            "قابلة للحماية بهذه الصفة بموجب القانون المعمول به."
        ),
    },

    "payment": {
        "en": (
            "A safer alternative is to specify invoice timing, payment due dates, taxes, disputed invoices, "
            "late-payment interest, suspension rights, and consequences of non-payment."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser le calendrier de facturation, les échéances de paiement, "
            "les taxes, les factures contestées, les intérêts de retard, les droits de suspension et les conséquences "
            "du non-paiement."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد مواعيد الفوترة والاستحقاق والضرائب والفواتير المتنازع عليها "
            "وفوائد التأخير وحقوق التعليق وآثار عدم الدفع."
        ),
    },

    "sla": {
        "en": (
            "A safer alternative is to define measurable service levels, measurement periods, exclusions, "
            "reporting duties, service credits, escalation rights, and remedies for repeated failures."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir des niveaux de service mesurables, les périodes de mesure, "
            "les exclusions, les obligations de reporting, les crédits de service, les droits d’escalade et les recours "
            "en cas d’échecs répétés."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد مستويات خدمة قابلة للقياس وفترات القياس والاستثناءات "
            "والتقارير وتعويضات الخدمة وحقوق التصعيد ووسائل المعالجة عند تكرار الإخفاق."
        ),
    },

    "data_privacy_security": {
        "en": (
            "A safer alternative is to clarify processing instructions, security standards, audit rights, "
            "incident notification timelines, subprocessor controls, deletion or return duties, and liability treatment."
        ),
        "fr": (
            "Une alternative plus sûre consiste à clarifier les instructions de traitement, les standards de sécurité, "
            "les droits d’audit, les délais de notification d’incident, le contrôle des sous-traitants, les obligations "
            "de suppression ou restitution et le traitement de la responsabilité."
        ),
        "ar": (
            "البديل الأكثر أماناً هو توضيح تعليمات المعالجة ومعايير الأمن وحقوق التدقيق ومهل الإخطار بالحوادث "
            "وضوابط المعالجين الفرعيين وواجبات الحذف أو الإرجاع ومعالجة المسؤولية."
        ),
    },

    "data_privacy_security_instructions": {
        "en": (
            "A safer alternative is to require that processing occurs strictly on documented instructions, "
            "list the specific exceptions where applicable law requires otherwise, and require the processor to "
            "promptly inform the controller if an instruction appears to infringe applicable data protection law."
        ),
        "fr": (
            "Une alternative plus sûre consiste à exiger que le traitement s'effectue strictement sur instructions "
            "documentées, à lister les exceptions spécifiques où le droit applicable impose le contraire, et à "
            "exiger que le sous-traitant informe rapidement le responsable si une instruction semble enfreindre le "
            "droit applicable en matière de protection des données."
        ),
        "ar": (
            "البديل الأكثر أماناً هو اشتراط أن تتم المعالجة حصراً بناءً على تعليمات موثقة، وتحديد الاستثناءات "
            "المحددة التي يفرض فيها القانون المعمول به خلاف ذلك، واشتراط قيام المعالج بإبلاغ المسؤول فوراً إذا بدا "
            "أن أحد التعليمات يخالف قانون حماية البيانات المعمول به."
        ),
    },

    "data_privacy_security_personnel_confidentiality": {
        "en": (
            "A safer alternative is to require a written confidentiality commitment from every person authorized "
            "to process personal data, confirm this obligation survives termination of their role, and limit access "
            "to personal data strictly to those with a genuine need to know."
        ),
        "fr": (
            "Une alternative plus sûre consiste à exiger un engagement de confidentialité écrit de la part de "
            "chaque personne autorisée à traiter les données personnelles, à confirmer que cette obligation "
            "survit à la cessation de leurs fonctions, et à limiter l'accès aux données personnelles strictement "
            "aux personnes ayant un besoin réel d'en connaître."
        ),
        "ar": (
            "البديل الأكثر أماناً هو اشتراط التزام كتابي بالسرية من كل شخص مصرح له بمعالجة البيانات الشخصية، "
            "وتأكيد استمرار هذا الالتزام بعد انتهاء مهامه، وقصر الوصول إلى البيانات الشخصية حصراً على من لديهم "
            "حاجة فعلية للاطلاع عليها."
        ),
    },

    "data_privacy_security_subprocessors": {
        "en": (
            "A safer alternative is to require prior specific written authorization for each subprocessor rather "
            "than a general authorization, set a defined objection period, and require the same data protection "
            "obligations to flow down contractually to every subprocessor."
        ),
        "fr": (
            "Une alternative plus sûre consiste à exiger une autorisation écrite spécifique préalable pour chaque "
            "sous-traitant ultérieur plutôt qu'une autorisation générale, à fixer un délai d'objection défini, et "
            "à exiger que les mêmes obligations de protection des données soient répercutées contractuellement sur "
            "chaque sous-traitant ultérieur."
        ),
        "ar": (
            "البديل الأكثر أماناً هو اشتراط إذن كتابي محدد مسبق لكل معالج فرعي بدلاً من إذن عام، وتحديد مهلة "
            "اعتراض محددة، واشتراط سريان نفس التزامات حماية البيانات تعاقدياً على كل معالج فرعي."
        ),
    },

    "data_privacy_security_security_measures": {
        "en": (
            "A safer alternative is to specify concrete technical and organizational measures (e.g. encryption "
            "standard, access controls, pseudonymization where applicable) rather than a generic 'appropriate "
            "measures' standard, and require periodic review as risks evolve."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser des mesures techniques et organisationnelles concrètes "
            "(par exemple le standard de chiffrement, les contrôles d'accès, la pseudonymisation le cas échéant) "
            "plutôt qu'un standard générique de 'mesures appropriées', et à exiger une revue périodique à mesure "
            "que les risques évoluent."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد تدابير تقنية وتنظيمية ملموسة (مثل معيار التشفير، ضوابط الوصول، إخفاء "
            "الهوية عند الاقتضاء) بدلاً من معيار عام غير محدد لـ'التدابير المناسبة'، واشتراط مراجعة دورية مع "
            "تطور المخاطر."
        ),
    },

    "data_privacy_security_subject_rights": {
        "en": (
            "A safer alternative is to set a concrete response timeline for the processor's assistance, clarify "
            "whether the processor may charge for extensive requests, and require the processor to forward any "
            "direct request from a data subject to the controller without responding to it independently."
        ),
        "fr": (
            "Une alternative plus sûre consiste à fixer un délai de réponse concret pour l'assistance du "
            "sous-traitant, à préciser si le sous-traitant peut facturer les demandes volumineuses, et à exiger "
            "que le sous-traitant transmette toute demande directe d'une personne concernée au responsable sans y "
            "répondre lui-même."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد مهلة استجابة ملموسة لمساعدة المعالج، وتوضيح ما إذا كان يجوز للمعالج "
            "تحصيل رسوم عن الطلبات الموسعة، واشتراط قيام المعالج بإحالة أي طلب مباشر من صاحب البيانات إلى "
            "المسؤول دون الرد عليه بشكل مستقل."
        ),
    },

    "data_privacy_security_breach_notification": {
        "en": (
            "A safer alternative is to keep the notification window short and clearly triggered (from becoming "
            "aware, not from confirming), require a specified minimum content for the notification (nature of the "
            "breach, categories and approximate number affected, likely consequences, measures taken), and commit "
            "to ongoing updates as the investigation progresses."
        ),
        "fr": (
            "Une alternative plus sûre consiste à conserver un délai de notification court et clairement "
            "déclenché (dès la prise de connaissance, et non dès la confirmation), à exiger un contenu minimal "
            "spécifié pour la notification (nature de la violation, catégories et nombre approximatif de personnes "
            "concernées, conséquences probables, mesures prises), et à s'engager à fournir des mises à jour "
            "continues à mesure que l'enquête progresse."
        ),
        "ar": (
            "البديل الأكثر أماناً هو الإبقاء على مهلة إخطار قصيرة ومحددة بوضوح (من لحظة العلم، لا من لحظة "
            "التأكيد)، واشتراط حد أدنى محدد من المحتوى للإخطار (طبيعة الخرق، فئات الأشخاص المتأثرين وعددهم "
            "التقريبي، العواقب المحتملة، التدابير المتخذة)، والالتزام بتقديم تحديثات مستمرة مع تقدم التحقيق."
        ),
    },

    "data_privacy_security_deletion_return": {
        "en": (
            "A safer alternative is to give the controller an explicit election between deletion and return "
            "(rather than leaving it to the processor), set a concrete deadline for completing deletion or return, "
            "and require written certification of deletion once complete."
        ),
        "fr": (
            "Une alternative plus sûre consiste à accorder au responsable un choix explicite entre suppression et "
            "restitution (plutôt que de le laisser au sous-traitant), à fixer un délai concret pour l'achèvement "
            "de la suppression ou de la restitution, et à exiger une attestation écrite de suppression une fois "
            "celle-ci effectuée."
        ),
        "ar": (
            "البديل الأكثر أماناً هو منح المسؤول خياراً صريحاً بين الحذف والإرجاع (بدلاً من تركه للمعالج)، "
            "وتحديد مهلة ملموسة لإتمام الحذف أو الإرجاع، واشتراط شهادة كتابية بالحذف بعد إتمامه."
        ),
    },

    "data_privacy_security_audit": {
        "en": (
            "A safer alternative is to define the audit scope and required advance notice, cap frequency absent a "
            "breach, allow the processor to satisfy the obligation through a recognized third-party certification "
            "report where equivalent, and keep audit findings confidential."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir le périmètre de l'audit et le préavis requis, à plafonner "
            "la fréquence en l'absence de violation, à permettre au sous-traitant de satisfaire cette obligation "
            "au moyen d'un rapport de certification tiers reconnu lorsqu'il est équivalent, et à garder les "
            "conclusions de l'audit confidentielles."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد نطاق التدقيق والإشعار المسبق المطلوب، وتحديد سقف لتكرار التدقيق في "
            "غياب أي خرق، والسماح للمعالج بالوفاء بهذا الالتزام عبر تقرير شهادة معتمدة من طرف ثالث عند تكافؤه، "
            "والحفاظ على سرية نتائج التدقيق."
        ),
    },

    "intellectual_property": {
        "en": (
            "A safer alternative is to separate background IP from newly created deliverables, define license scope, "
            "ownership transfer timing, permitted use, moral rights treatment, and post-termination rights."
        ),
        "fr": (
            "Une alternative plus sûre consiste à distinguer la propriété intellectuelle préexistante des livrables créés, "
            "à définir la portée de la licence, le moment du transfert, l’usage autorisé, le traitement des droits moraux "
            "et les droits après résiliation."
        ),
        "ar": (
            "البديل الأكثر أماناً هو فصل الملكية الفكرية السابقة عن المخرجات الجديدة، وتحديد نطاق الترخيص "
            "وتوقيت نقل الملكية والاستخدام المسموح ومعالجة الحقوق المعنوية والحقوق بعد الإنهاء."
        ),
    },

    "assignment": {
        "en": (
            "A safer alternative is to require consent for material assignments while allowing defined exceptions "
            "for affiliates, reorganizations, mergers, or asset sales, subject to notice and continued responsibility."
        ),
        "fr": (
            "Une alternative plus sûre consiste à exiger le consentement pour les cessions importantes, tout en permettant "
            "des exceptions définies pour les affiliés, réorganisations, fusions ou ventes d’actifs, sous réserve d’un préavis "
            "et du maintien de la responsabilité."
        ),
        "ar": (
            "البديل الأكثر أماناً هو اشتراط الموافقة على التنازلات الجوهرية، مع السماح باستثناءات محددة "
            "للشركات التابعة أو إعادة التنظيم أو الاندماج أو بيع الأصول، بشرط الإشعار واستمرار المسؤولية."
        ),
    },

    "restrictive_covenants": {
        "en": (
            "A safer alternative is to limit the restriction to legitimate business interests, define the restricted activity, "
            "duration, territory, affected persons, exceptions, and proportional remedies."
        ),
        "fr": (
            "Une alternative plus sûre consiste à limiter la restriction aux intérêts commerciaux légitimes, à définir "
            "l’activité restreinte, la durée, le territoire, les personnes concernées, les exceptions et les recours proportionnés."
        ),
        "ar": (
            "البديل الأكثر أماناً هو قصر القيد على المصالح التجارية المشروعة، وتحديد النشاط المقيد والمدة "
            "والنطاق والأشخاص المعنيين والاستثناءات ووسائل المعالجة المتناسبة."
        ),
    },

    "governing_law": {
        "en": (
            "A safer alternative is to specify governing law, forum, dispute escalation steps, language, costs, interim relief, "
            "and enforcement mechanics in a clear and practical manner."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser le droit applicable, le forum, les étapes d’escalade des litiges, "
            "la langue, les coûts, les mesures provisoires et les modalités d’exécution de manière claire et pratique."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد القانون الواجب التطبيق والاختصاص وخطوات تصعيد النزاع واللغة "
            "والتكاليف والتدابير المؤقتة وآليات التنفيذ بطريقة واضحة وعملية."
        ),
    },

    "force_majeure": {
        "en": (
            "A safer alternative is to define covered events precisely, require prompt notice, impose "
            "mitigation duties, and specify a maximum suspension period after which either party may terminate."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir précisément les événements couverts, à exiger une "
            "notification rapide, à imposer des obligations d’atténuation et à préciser une durée maximale de "
            "suspension au-delà de laquelle chaque partie peut résilier."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد الأحداث المشمولة بدقة، واشتراط إخطار فوري، وفرض واجبات التخفيف، "
            "وتحديد مدة قصوى للتعليق يجوز بعدها لأي طرف الإنهاء."
        ),
    },

    "warranty": {
        "en": (
            "A safer alternative is to state warranties precisely, define their duration, list exclusions and "
            "disclaimers clearly, and specify the exclusive remedies available if a warranty is breached."
        ),
        "fr": (
            "Une alternative plus sûre consiste à énoncer précisément les garanties, à définir leur durée, à "
            "lister clairement les exclusions et exonérations, et à préciser les recours exclusifs disponibles "
            "en cas de manquement à une garantie."
        ),
        "ar": (
            "البديل الأكثر أماناً هو النص على الضمانات بدقة، وتحديد مدتها، وسرد الاستثناءات والإخلاءات بوضوح، "
            "وتحديد وسائل الانتصاف الحصرية المتاحة عند الإخلال بالضمان."
        ),
    },

    "indemnification": {
        "en": (
            "A safer alternative is to define indemnified claims precisely, set a cap aligned with the "
            "liability clause, specify notice and defense procedures, and clarify how indemnification "
            "interacts with insurance recovery."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir précisément les réclamations indemnisées, à fixer un "
            "plafond cohérent avec la clause de responsabilité, à préciser les procédures de notification et "
            "de défense, et à clarifier l’articulation entre l’indemnisation et le recouvrement d’assurance."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد المطالبات المشمولة بالتعويض بدقة، وتحديد سقف متوافق مع بند "
            "المسؤولية، وتوضيح إجراءات الإخطار والدفاع، وبيان كيفية تفاعل التعويض مع استرداد التأمين."
        ),
    },

    "insurance": {
        "en": (
            "A safer alternative is to specify required coverage types and minimum limits, require evidence "
            "of coverage, address additional insured status, and define the consequences and notice period "
            "for any lapse."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser les types de couverture exigés et les montants "
            "minimaux, à exiger une preuve de couverture, à traiter le statut d’assuré additionnel et à "
            "définir les conséquences et le délai de notification en cas d’interruption."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد أنواع التغطية المطلوبة والحدود الدنيا، واشتراط تقديم دليل على "
            "التغطية، ومعالجة صفة المؤمَّن الإضافي، وتحديد آثار ومهلة الإخطار في حال انقطاع التغطية."
        ),
    },

    "audit_rights": {
        "en": (
            "A safer alternative is to limit audit scope and frequency, require reasonable advance notice, "
            "keep findings confidential, and allocate costs based on the outcome of the audit."
        ),
        "fr": (
            "Une alternative plus sûre consiste à limiter la portée et la fréquence des audits, à exiger un "
            "préavis raisonnable, à garder les constatations confidentielles, et à répartir les coûts en "
            "fonction du résultat de l’audit."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تقييد نطاق وتكرار التدقيق، واشتراط إشعار مسبق معقول، والحفاظ على سرية "
            "النتائج، وتوزيع التكاليف بناءً على نتيجة التدقيق."
        ),
    },

    "change_of_control": {
        "en": (
            "A safer alternative is to define what constitutes a change of control, require timely notice, "
            "and specify whether the counterparty may object, consent, or terminate, and on what timeline."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir ce qui constitue un changement de contrôle, à "
            "exiger une notification en temps utile, et à préciser si la contrepartie peut s’y opposer, y "
            "consentir ou résilier, et selon quel délai."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد ما يشكل تغييراً في السيطرة، واشتراط إشعار في الوقت المناسب، "
            "وتوضيح ما إذا كان يجوز للطرف الآخر الاعتراض أو الموافقة أو الإنهاء، وضمن أي مهلة."
        ),
    },

    "subcontracting": {
        "en": (
            "A safer alternative is to require prior consent for material subcontracting, retain the primary "
            "party's responsibility for subcontractor performance, and flow down key contractual obligations "
            "to subcontractors."
        ),
        "fr": (
            "Une alternative plus sûre consiste à exiger un consentement préalable pour toute sous-traitance "
            "importante, à maintenir la responsabilité de la partie principale pour la performance du "
            "sous-traitant, et à répercuter les obligations contractuelles clés sur les sous-traitants."
        ),
        "ar": (
            "البديل الأكثر أماناً هو اشتراط الموافقة المسبقة على التعاقد الجوهري من الباطن، والإبقاء على "
            "مسؤولية الطرف الأصلي عن أداء المتعاقد من الباطن، ونقل الالتزامات التعاقدية الجوهرية إلى "
            "المتعاقدين من الباطن."
        ),
    },

    "anti_bribery_compliance": {
        "en": (
            "A safer alternative is to reference recognized anti-bribery and compliance standards, require "
            "ongoing certification, and provide for immediate termination and cooperation duties if a "
            "violation occurs."
        ),
        "fr": (
            "Une alternative plus sûre consiste à faire référence à des normes anti-corruption et de "
            "conformité reconnues, à exiger une certification continue, et à prévoir la résiliation immédiate "
            "et des obligations de coopération en cas de violation."
        ),
        "ar": (
            "البديل الأكثر أماناً هو الإشارة إلى معايير معترف بها لمكافحة الرشوة والامتثال، واشتراط تصديق "
            "مستمر، والنص على الإنهاء الفوري وواجبات التعاون في حال حدوث مخالفة."
        ),
    },

    "export_control": {
        "en": (
            "A safer alternative is to include representations of sanctions and export-control compliance, "
            "require prompt notice of any change in status, and allow suspension or termination if a party "
            "becomes restricted."
        ),
        "fr": (
            "Une alternative plus sûre consiste à inclure des déclarations de conformité aux sanctions et aux "
            "contrôles à l’exportation, à exiger une notification rapide de tout changement de statut, et à "
            "permettre la suspension ou la résiliation si une partie devient soumise à des restrictions."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تضمين إقرارات بالامتثال للعقوبات وضوابط التصدير، واشتراط إخطار فوري بأي "
            "تغيير في الوضع، والسماح بالتعليق أو الإنهاء إذا أصبح أحد الطرفين خاضعاً لقيود."
        ),
    },

    "notices": {
        "en": (
            "A safer alternative is to specify permitted delivery methods including electronic means, define "
            "when notice is deemed received, and require prompt updates if contact details change."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser les modes de transmission autorisés, y compris les "
            "moyens électroniques, à définir le moment où la notification est réputée reçue, et à exiger une "
            "mise à jour rapide en cas de changement des coordonnées."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد وسائل التسليم المسموح بها بما في ذلك الوسائل الإلكترونية، وتحديد "
            "متى يُعتبر الإشعار مستلماً، واشتراط التحديث الفوري عند تغيير بيانات الاتصال."
        ),
    },

    "entire_agreement": {
        "en": (
            "A safer alternative is to state clearly which documents form the entire agreement, "
            "whether prior representations, negotiations, and understandings are superseded, and "
            "whether any exhibits or referenced policies are incorporated by reference."
        ),
        "fr": (
            "Une alternative plus sûre consiste à indiquer clairement quels documents constituent l’intégralité "
            "de l’accord, si les déclarations, négociations et accords antérieurs sont remplacés, et si des "
            "annexes ou politiques référencées sont incorporées par référence."
        ),
        "ar": (
            "البديل الأكثر أماناً هو التوضيح بدقة ما هي الوثائق التي تشكل الاتفاق الكامل، وما إذا كانت "
            "الإقرارات والمفاوضات والتفاهمات السابقة قد حلّت محلها، وما إذا كانت أي ملاحق أو سياسات "
            "مُشار إليها مدرجة بالإحالة."
        ),
    },

    "amendment": {
        "en": (
            "A safer alternative is to require that amendments be in writing and signed by authorized "
            "representatives of both parties, distinguish a formal amendment from a mere waiver or course "
            "of dealing, and specify whether electronic signatures satisfy the writing requirement."
        ),
        "fr": (
            "Une alternative plus sûre consiste à exiger que les modifications soient écrites et signées par "
            "des représentants autorisés des deux parties, à distinguer une modification formelle d'une simple "
            "renonciation ou d'un usage établi entre les parties, et à préciser si les signatures électroniques "
            "satisfont à l'exigence d'écrit."
        ),
        "ar": (
            "البديل الأكثر أماناً هو اشتراط أن تكون التعديلات مكتوبة وموقّعة من ممثلين مفوضين لكلا الطرفين، "
            "والتمييز بين التعديل الرسمي ومجرد التنازل أو التعامل المعتاد بين الطرفين، وتوضيح ما إذا كانت "
            "التوقيعات الإلكترونية تفي بمتطلب الكتابة."
        ),
    },

    "severability": {
        "en": (
            "A safer alternative is to state that invalidity of one provision does not affect the rest of the "
            "contract, and that the parties will negotiate a replacement provision reflecting the original intent."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser que l’invalidité d’une disposition n’affecte pas le "
            "reste du contrat, et que les parties négocieront une disposition de remplacement reflétant "
            "l’intention initiale."
        ),
        "ar": (
            "البديل الأكثر أماناً هو النص على أن بطلان أحد الأحكام لا يؤثر على بقية العقد، وأن الطرفين "
            "سيتفاوضان على حكم بديل يعكس النية الأصلية."
        ),
    },

    "waiver": {
        "en": (
            "A safer alternative is to state expressly that any waiver must be in writing and signed, and that "
            "a single waiver does not constitute a waiver of future breaches."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser expressément que toute renonciation doit être écrite "
            "et signée, et qu’une renonciation ponctuelle ne vaut pas renonciation pour des manquements futurs."
        ),
        "ar": (
            "البديل الأكثر أماناً هو النص صراحة على أن أي تنازل يجب أن يكون مكتوباً وموقعاً، وأن التنازل مرة "
            "واحدة لا يشكل تنازلاً عن مخالفات مستقبلية."
        ),
    },

    "third_party_rights": {
        "en": (
            "A safer alternative is to state clearly that the contract confers no rights on third parties, "
            "subject to any express exceptions such as affiliates or indemnified parties."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser clairement que le contrat ne confère aucun droit à "
            "des tiers, sous réserve d’exceptions expresses telles que les affiliés ou les parties indemnisées."
        ),
        "ar": (
            "البديل الأكثر أماناً هو التوضيح بدقة أن العقد لا يمنح أي حقوق للغير، مع مراعاة أي استثناءات صريحة "
            "مثل الشركات التابعة أو الأطراف المستفيدة من التعويض."
        ),
    },

    "survival": {
        "en": (
            "A safer alternative is to list explicitly which clauses survive termination, such as "
            "confidentiality, liability, indemnification, and payment obligations, and for what duration."
        ),
        "fr": (
            "Une alternative plus sûre consiste à énumérer explicitement les clauses qui survivent à la "
            "résiliation, telles que la confidentialité, la responsabilité, l’indemnisation et les obligations "
            "de paiement, ainsi que leur durée."
        ),
        "ar": (
            "البديل الأكثر أماناً هو سرد الأحكام التي تستمر بعد الإنهاء بشكل صريح، مثل السرية والمسؤولية "
            "والتعويض والتزامات الدفع، ولأي مدة."
        ),
    },

    "most_favored_nation": {
        "en": (
            "A safer alternative is to define the comparison group and metrics precisely, set a reasonable "
            "verification mechanism, and limit the remedy to a prospective price or term adjustment rather "
            "than retroactive liability."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir précisément le groupe de comparaison et les "
            "critères, à prévoir un mécanisme de vérification raisonnable, et à limiter le recours à un "
            "ajustement prospectif du prix ou des conditions plutôt qu’à une responsabilité rétroactive."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد مجموعة المقارنة والمعايير بدقة، وتوفير آلية تحقق معقولة، وقصر "
            "وسيلة الانتصاف على تعديل مستقبلي للسعر أو الشروط بدلاً من المسؤولية بأثر رجعي."
        ),
    },

    "exclusivity": {
        "en": (
            "A safer alternative is to limit exclusivity to a defined scope, territory, and duration, tie it "
            "to measurable performance thresholds, and specify the consequences if those thresholds are not met."
        ),
        "fr": (
            "Une alternative plus sûre consiste à limiter l’exclusivité à une portée, un territoire et une "
            "durée définis, à la lier à des seuils de performance mesurables, et à préciser les conséquences "
            "en cas de non-atteinte de ces seuils."
        ),
        "ar": (
            "البديل الأكثر أماناً هو قصر الحصرية على نطاق وإقليم ومدة محددة، وربطها بحدود أداء قابلة "
            "للقياس، وتوضيح العواقب في حال عدم بلوغ هذه الحدود."
        ),
    },

    "pricing_adjustment": {
        "en": (
            "A safer alternative is to tie adjustments to an objective, published index or formula, set a "
            "fixed frequency, require advance notice, and cap the maximum increase per adjustment period."
        ),
        "fr": (
            "Une alternative plus sûre consiste à lier les ajustements à un indice ou une formule objective "
            "et publiée, à fixer une fréquence déterminée, à exiger un préavis, et à plafonner l’augmentation "
            "maximale par période d’ajustement."
        ),
        "ar": (
            "البديل الأكثر أماناً هو ربط التعديلات بمؤشر أو معادلة موضوعية ومنشورة، وتحديد وتيرة ثابتة، "
            "واشتراط إشعار مسبق، ووضع حد أقصى للزيادة لكل فترة تعديل."
        ),
    },

    "publicity": {
        "en": (
            "A safer alternative is to require prior written consent for any public announcement or use of "
            "the other party's name, logo, or trademarks, with narrow exceptions for legally required "
            "disclosures."
        ),
        "fr": (
            "Une alternative plus sûre consiste à exiger un consentement écrit préalable pour toute annonce "
            "publique ou utilisation du nom, du logo ou des marques de l’autre partie, avec des exceptions "
            "limitées pour les divulgations légalement requises."
        ),
        "ar": (
            "البديل الأكثر أماناً هو اشتراط الموافقة الخطية المسبقة على أي إعلان عام أو استخدام لاسم الطرف "
            "الآخر أو شعاره أو علاماته التجارية، مع استثناءات محدودة للإفصاحات المطلوبة قانوناً."
        ),
    },

    "non_disparagement": {
        "en": (
            "A safer alternative is to make the obligation mutual, define what constitutes disparagement, "
            "set a reasonable duration, and expressly exclude truthful statements made in legal or "
            "regulatory proceedings."
        ),
        "fr": (
            "Une alternative plus sûre consiste à rendre l’obligation réciproque, à définir ce qui constitue "
            "un dénigrement, à fixer une durée raisonnable, et à exclure expressément les déclarations "
            "véridiques faites dans le cadre de procédures judiciaires ou réglementaires."
        ),
        "ar": (
            "البديل الأكثر أماناً هو جعل الالتزام متبادلاً، وتحديد ما يشكل إساءة، وتحديد مدة معقولة، "
            "واستبعاد صراحة التصريحات الصادقة التي تُقدَّم في إجراءات قضائية أو تنظيمية."
        ),
    },

    "financial_covenants": {
        "en": (
            "A safer alternative is to define covenant calculations precisely, set realistic thresholds with "
            "headroom, provide a cure period before default is triggered, and specify graduated consequences "
            "for a breach."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir précisément le calcul des engagements, à fixer des "
            "seuils réalistes avec une marge, à prévoir un délai de régularisation avant le déclenchement du "
            "défaut, et à préciser des conséquences graduées en cas de manquement."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد طريقة حساب التعهدات بدقة، ووضع حدود واقعية مع هامش، وتوفير مهلة "
            "معالجة قبل تفعيل حالة التعثر، وتحديد عواقب متدرجة عند المخالفة."
        ),
    },

    "events_of_default": {
        "en": (
            "A safer alternative is to list default triggers precisely, provide reasonable cure periods for "
            "non-monetary defaults, limit cross-default scope, and tie acceleration to material and "
            "continuing defaults."
        ),
        "fr": (
            "Une alternative plus sûre consiste à énumérer précisément les événements de défaut, à prévoir "
            "des délais de régularisation raisonnables pour les défauts non monétaires, à limiter la portée "
            "du défaut croisé, et à lier l’accélération à des défauts substantiels et persistants."
        ),
        "ar": (
            "البديل الأكثر أماناً هو سرد أحداث التعثر بدقة، وتوفير مهل معالجة معقولة للتعثرات غير النقدية، "
            "وتقييد نطاق التعثر المتبادل، وربط التسريع بالتعثرات الجوهرية والمستمرة."
        ),
    },

    "security_collateral": {
        "en": (
            "A safer alternative is to describe the secured assets precisely, complete all perfection "
            "formalities, clarify priority among creditors, and define clear conditions for release of the "
            "security."
        ),
        "fr": (
            "Une alternative plus sûre consiste à décrire précisément les actifs garantis, à accomplir toutes "
            "les formalités de constitution, à clarifier la priorité entre créanciers, et à définir des "
            "conditions claires de mainlevée de la garantie."
        ),
        "ar": (
            "البديل الأكثر أماناً هو وصف الأصول المضمونة بدقة، واستكمال جميع إجراءات إتمام الضمان، وتوضيح "
            "الأولوية بين الدائنين، وتحديد شروط واضحة للإفراج عن الضمان."
        ),
    },

    "conditions_precedent": {
        "en": (
            "A safer alternative is to list each condition precisely, set a clear satisfaction deadline, "
            "specify who may waive a condition, and state whether failure to satisfy a condition allows "
            "termination without liability."
        ),
        "fr": (
            "Une alternative plus sûre consiste à énumérer précisément chaque condition, à fixer une date "
            "limite claire de réalisation, à préciser qui peut renoncer à une condition, et à indiquer si le "
            "non-accomplissement d’une condition permet une résiliation sans responsabilité."
        ),
        "ar": (
            "البديل الأكثر أماناً هو سرد كل شرط بدقة، وتحديد مهلة واضحة لتحققه، وتوضيح من يجوز له التنازل "
            "عن الشرط، وبيان ما إذا كان عدم تحقق الشرط يسمح بالإنهاء دون مسؤولية."
        ),
    },

    "purchase_price_adjustment": {
        "en": (
            "A safer alternative is to define the adjustment mechanism and calculation methodology "
            "precisely, set a clear dispute-resolution procedure for disagreements, and cap the adjustment "
            "within a reasonable range."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir précisément le mécanisme d’ajustement et la "
            "méthodologie de calcul, à prévoir une procédure claire de règlement des différends, et à "
            "plafonner l’ajustement dans une fourchette raisonnable."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد آلية التعديل ومنهجية الحساب بدقة، وتوفير إجراء واضح لتسوية "
            "الخلافات، ووضع سقف للتعديل ضمن نطاق معقول."
        ),
    },

    "title_and_risk_of_loss": {
        "en": (
            "A safer alternative is to specify the precise point of title and risk transfer, address "
            "retention of title until payment, and allocate responsibility for loss or damage during transit "
            "and storage."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser le moment exact du transfert de propriété et de "
            "risque, à traiter la réserve de propriété jusqu’au paiement, et à répartir la responsabilité en "
            "cas de perte ou de dommage pendant le transport et le stockage."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد اللحظة الدقيقة لانتقال الملكية والمخاطر، ومعالجة الاحتفاظ "
            "بالملكية حتى الدفع، وتوزيع المسؤولية عن الفقدان أو التلف أثناء النقل والتخزين."
        ),
    },

    "delivery_and_acceptance": {
        "en": (
            "A safer alternative is to define objective acceptance criteria, set a reasonable inspection "
            "period, specify the process for rejecting non-conforming deliverables, and provide a clear cure "
            "or replacement remedy."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir des critères d’acceptation objectifs, à fixer un "
            "délai d’inspection raisonnable, à préciser la procédure de rejet des livrables non conformes, et "
            "à prévoir un recours clair de régularisation ou de remplacement."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد معايير قبول موضوعية، وتحديد فترة فحص معقولة، وتوضيح إجراء رفض "
            "المخرجات غير المطابقة، وتوفير وسيلة انتصاف واضحة للمعالجة أو الاستبدال."
        ),
    },

    "use_and_occupancy": {
        "en": (
            "A safer alternative is to define the permitted use precisely, address exclusivity if relevant, "
            "require compliance with applicable zoning and building rules, and specify remedies for "
            "unauthorized use."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir précisément l’usage autorisé, à traiter "
            "l’exclusivité le cas échéant, à exiger le respect des règles d’urbanisme et de construction "
            "applicables, et à préciser les recours en cas d’usage non autorisé."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد الاستخدام المسموح به بدقة، ومعالجة الحصرية عند الاقتضاء، "
            "واشتراط الامتثال لقواعد التنظيم العمراني والبناء المعمول بها، وتحديد وسائل الانتصاف عند "
            "الاستخدام غير المصرح به."
        ),
    },

    "maintenance_and_repairs": {
        "en": (
            "A safer alternative is to allocate maintenance and repair responsibilities clearly between the "
            "parties, set response-time standards for repairs, and specify remedies if neglect causes damage "
            "or loss of use."
        ),
        "fr": (
            "Une alternative plus sûre consiste à répartir clairement les responsabilités d’entretien et de "
            "réparation entre les parties, à fixer des normes de délai d’intervention, et à préciser les "
            "recours si une négligence cause un dommage ou une perte d’usage."
        ),
        "ar": (
            "البديل الأكثر أماناً هو توزيع مسؤوليات الصيانة والإصلاح بوضوح بين الطرفين، وتحديد معايير زمنية "
            "للاستجابة للإصلاحات، وتوضيح وسائل الانتصاف إذا تسبب الإهمال بضرر أو فقدان الاستخدام."
        ),
    },

    "rent_and_escalation": {
        "en": (
            "A safer alternative is to tie rent escalation to an objective published index or a fixed "
            "schedule, set a reasonable review frequency, and itemize any additional charges separately from "
            "base rent."
        ),
        "fr": (
            "Une alternative plus sûre consiste à lier l’indexation du loyer à un indice objectif publié ou "
            "à un calendrier fixe, à fixer une fréquence de révision raisonnable, et à détailler séparément "
            "les charges additionnelles du loyer de base."
        ),
        "ar": (
            "البديل الأكثر أماناً هو ربط زيادة الإيجار بمؤشر موضوعي منشور أو جدول ثابت، وتحديد وتيرة مراجعة "
            "معقولة، وتفصيل أي رسوم إضافية بشكل منفصل عن الإيجار الأساسي."
        ),
    },

    "corporate_governance": {
        "en": (
            "A safer alternative is to define board composition and appointment rights clearly, list "
            "reserved matters requiring enhanced approval, and include a defined deadlock-resolution "
            "mechanism such as escalation or mediation."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir clairement la composition du conseil et les droits "
            "de nomination, à lister les matières réservées nécessitant une approbation renforcée, et à "
            "inclure un mécanisme défini de résolution des blocages tel que l’escalade ou la médiation."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد تكوين مجلس الإدارة وحقوق التعيين بوضوح، وسرد المسائل المحفوظة "
            "التي تتطلب موافقة معززة، وتضمين آلية محددة لحل الجمود مثل التصعيد أو الوساطة."
        ),
    },

    "corporate_governance_committee": {
        "en": (
            "A safer alternative is to define the meeting frequency, required attendees, standing agenda "
            "items, performance metrics to be reviewed, ownership of resulting action items, an escalation "
            "path for unresolved issues, and a requirement to keep written minutes."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir la fréquence des réunions, les participants requis, "
            "les points permanents à l’ordre du jour, les indicateurs de performance à examiner, "
            "la responsabilité des points d’action qui en résultent, une voie d’escalade pour les questions "
            "non résolues, et l’obligation de conserver un procès-verbal écrit."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد وتيرة الاجتماعات، والحضور المطلوب، وبنود جدول الأعمال الثابتة، "
            "ومؤشرات الأداء الواجب مراجعتها، والمسؤولية عن بنود العمل الناتجة، ومسار تصعيد للمسائل غير "
            "المحلولة، والالتزام بالاحتفاظ بمحضر مكتوب للاجتماع."
        ),
    },

    "share_transfer_restrictions": {
        "en": (
            "A safer alternative is to define the right-of-first-refusal process clearly, balance tag-along "
            "and drag-along thresholds fairly, set a reasonable lock-up period, and permit transfers to "
            "affiliates without triggering the full process."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir clairement le processus de préemption, à équilibrer "
            "les seuils de sortie conjointe et forcée, à fixer une période d’incessibilité raisonnable, et à "
            "permettre les cessions aux affiliés sans déclencher la procédure complète."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد إجراء حق الأولوية في الشراء بوضوح، وتحقيق التوازن في حدود حقوق "
            "المرافقة والإجبار في البيع، وتحديد فترة حظر تصرف معقولة، والسماح بالتنازلات للشركات التابعة "
            "دون تفعيل الإجراء الكامل."
        ),
    },

    "anti_dilution_preemptive_rights": {
        "en": (
            "A safer alternative is to specify the anti-dilution formula precisely, define the triggering "
            "events narrowly, and set a clear and time-bound process for exercising pre-emptive rights."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser la formule anti-dilution avec exactitude, à "
            "définir étroitement les événements déclencheurs, et à prévoir un processus clair et limité dans "
            "le temps pour l’exercice des droits préférentiels."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد صيغة مكافحة التخفيف بدقة، وتضييق تعريف الأحداث المحفزة، وتوفير "
            "إجراء واضح ومحدد بمهلة زمنية لممارسة حقوق الأولوية."
        ),
    },

    "liquidation_preference": {
        "en": (
            "A safer alternative is to define the preference multiple and seniority ranking clearly, specify "
            "whether the preference is participating or non-participating, and address treatment "
            "consistently across sale, merger, and liquidation scenarios."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir clairement le multiple de préférence et le rang de "
            "priorité, à préciser si la préférence est participative ou non participative, et à traiter de "
            "manière cohérente les scénarios de cession, fusion et liquidation."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد مضاعف الأفضلية وترتيب الأولوية بوضوح، وتوضيح ما إذا كانت "
            "الأفضلية مشاركة أو غير مشاركة، ومعالجة سيناريوهات البيع والاندماج والتصفية بشكل متسق."
        ),
    },

    "independent_contractor_status": {
        "en": (
            "A safer alternative is to state clearly that no employment, agency, or partnership relationship "
            "is created, allocate tax and social-security responsibility to the contractor, and avoid "
            "contractual terms that resemble employee control."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser clairement qu’aucune relation d’emploi, de mandat "
            "ou de partenariat n’est créée, à attribuer la responsabilité fiscale et de sécurité sociale au "
            "prestataire, et à éviter des termes contractuels ressemblant à un contrôle de type salarié."
        ),
        "ar": (
            "البديل الأكثر أماناً هو النص بوضوح على عدم نشوء علاقة عمل أو وكالة أو شراكة، وإسناد المسؤولية "
            "الضريبية والضمان الاجتماعي إلى المتعاقد، وتجنب الشروط التعاقدية التي تشبه سيطرة صاحب العمل على "
            "الموظف."
        ),
    },

    "key_personnel": {
        "en": (
            "A safer alternative is to name key personnel explicitly, require approval before replacement, "
            "and provide a reasonable transition period and remedy if a key person becomes unavailable."
        ),
        "fr": (
            "Une alternative plus sûre consiste à désigner explicitement le personnel clé, à exiger une "
            "approbation avant tout remplacement, et à prévoir une période de transition raisonnable et un "
            "recours en cas d’indisponibilité d’une personne clé."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تسمية الموظفين الرئيسيين صراحة، واشتراط الموافقة قبل الاستبدال، "
            "وتوفير فترة انتقالية معقولة ووسيلة انتصاف في حال عدم توفر أحد الأفراد الرئيسيين."
        ),
    },

    "exit_transition": {
        "en": (
            "A safer alternative is to define transition-out obligations precisely, require good-faith "
            "knowledge transfer and data return, and specify the duration, scope, and pricing of "
            "post-termination transition assistance."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir précisément les obligations de sortie, à exiger un "
            "transfert de connaissances et une restitution des données de bonne foi, et à préciser la durée, "
            "la portée et la tarification de l’assistance de transition post-résiliation."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد التزامات الخروج بدقة، واشتراط نقل المعرفة وإرجاع البيانات بحسن "
            "نية، وتحديد مدة ونطاق وتسعير مساعدة الانتقال بعد الإنهاء."
        ),
    },

    "cross_border_data_transfer": {
        "en": (
            "A safer alternative is to specify the legal transfer mechanism relied upon, list the "
            "jurisdictions involved, and include audit and notice rights consistent with applicable "
            "data-protection requirements."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser le mécanisme juridique de transfert utilisé, à "
            "lister les juridictions concernées, et à inclure des droits d’audit et de notification "
            "conformes aux exigences applicables en matière de protection des données."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد الآلية القانونية للنقل المعتمدة، وسرد الولايات القضائية "
            "المعنية، وتضمين حقوق تدقيق وإخطار متوافقة مع متطلبات حماية البيانات المعمول بها."
        ),
    },

    "tax": {
        "en": (
            "A safer alternative is to state clearly whether prices are tax-inclusive or exclusive, "
            "allocate withholding tax responsibility, include gross-up language where needed, and "
            "require cooperation on tax documentation."
        ),
        "fr": (
            "Une alternative plus sûre consiste à préciser clairement si les prix incluent ou "
            "excluent les taxes, à répartir la responsabilité de la retenue à la source, à inclure "
            "une clause de majoration si nécessaire, et à exiger une coopération sur les documents "
            "fiscaux."
        ),
        "ar": (
            "البديل الأكثر أماناً هو التوضيح بدقة ما إذا كانت الأسعار شاملة أو غير شاملة "
            "للضرائب، وتوزيع مسؤولية ضريبة الاستقطاع، وتضمين صياغة التعويض الضريبي عند الحاجة، "
            "واشتراط التعاون بشأن المستندات الضريبية."
        ),
    },

    "employment_terms": {
        "en": (
            "A safer alternative is to define compensation and benefits precisely, state working "
            "conditions clearly, and align duties with objective, measurable performance "
            "expectations."
        ),
        "fr": (
            "Une alternative plus sûre consiste à définir précisément la rémunération et les "
            "avantages, à préciser clairement les conditions de travail, et à aligner les fonctions "
            "sur des attentes de performance objectives et mesurables."
        ),
        "ar": (
            "البديل الأكثر أماناً هو تحديد التعويض والمزايا بدقة، وتوضيح ظروف العمل بوضوح، "
            "ومواءمة المهام مع توقعات أداء موضوعية وقابلة للقياس."
        ),
    },
}


GENERAL_WORDING = {
    "en": (
        "A safer alternative is to clarify the scope, objective standards, notice requirements, "
        "exceptions, remedies, and proportional limits so the clause remains enforceable and balanced."
    ),
    "fr": (
        "Une alternative plus sûre consiste à clarifier la portée, les critères objectifs, "
        "les exigences de notification, les exceptions, les recours et les limites proportionnées "
        "afin que la clause reste applicable et équilibrée."
    ),
    "ar": (
        "البديل الأكثر أماناً هو توضيح النطاق والمعايير الموضوعية ومتطلبات الإخطار "
        "والاستثناءات ووسائل الانتصاف والحدود المتناسبة حتى يبقى البند قابلاً للتنفيذ ومتوازناً."
    ),
}


def normalize_clause_type(clause_type: str) -> str:
    value = str(clause_type or "general").lower().strip()

    aliases = {
        "limitation_of_liability": "liability",
        "limitation_of_liability_exceptions": "liability",
        "termination_for_convenience": "termination",
        "termination_for_cause": "termination",
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
        "notice": "notices",
        "communications": "notices",
        "notice_provision": "notices",
        "delivery": "delivery_and_acceptance",
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
        "finance_lending": "financial_covenants",
        "real_estate": "use_and_occupancy",
        "suspension": "termination",
        "business_continuity": "force_majeure",
        "open_source": "intellectual_property",
        "escrow": "intellectual_property",
        "transition_assistance": "exit_transition",
        "employment_hr": "employment_terms",
    }

    return aliases.get(value, value)


def get_safer_alternative(
    clause_type: str,
    language: str = "en",
) -> str:
    language = get_language(language)
    normalized_type = normalize_clause_type(clause_type)

    wording = WORDING_LIBRARY.get(normalized_type)

    if not wording:
        return GENERAL_WORDING[language]

    return wording.get(language, wording["en"])
