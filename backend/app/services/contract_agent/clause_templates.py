"""
clause_templates.py

Real, fillable contract-clause wording ("draft wording"), as opposed to
market_intelligence.py (comparison) and clause_wording_library.py (guidance
on WHAT to fix). This module answers HOW the clause could actually read.

Design goals (same as the rest of the contract_agent stack):
- Works for any contract family and industry (universal fallback template).
- Supports EN / FR / AR.
- Purely additive: does not modify market_intelligence.py or
  clause_wording_library.py, only imports the shared clause-type resolver
  so all three modules stay in sync automatically.
- Never claims to be legal advice: every render is returned together with
  a disclaimer that must be surfaced to the end user.
- Placeholders use {snake_case} tokens. Unresolved placeholders are
  replaced with a clearly bracketed prompt rather than left as raw
  "{token}" text or silently dropped, so a rendered draft never looks
  finished when it is not.
"""

from app.services.contract_agent.market_intelligence import (
    normalize_clause_type,
    get_language,
)


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


DISCLAIMER = {
    "en": (
        "This wording is an automatically generated drafting starting point. "
        "It is not legal advice and must be reviewed, adapted, and validated "
        "by qualified legal counsel before use in any binding agreement."
    ),
    "fr": (
        "Ce texte constitue un point de départ rédactionnel généré "
        "automatiquement. Il ne constitue pas un avis juridique et doit "
        "être revu, adapté et validé par un conseil juridique qualifié "
        "avant toute utilisation dans un accord contraignant."
    ),
    "ar": (
        "يمثل هذا النص نقطة انطلاق للصياغة تم إنشاؤها تلقائياً. وهو لا "
        "يشكل استشارة قانونية ويجب مراجعته وتكييفه واعتماده من قبل مستشار "
        "قانوني مؤهل قبل استخدامه في أي اتفاق ملزم."
    ),
}


UNRESOLVED_PLACEHOLDER = {
    "en": "[TO BE SPECIFIED: {name}]",
    "fr": "[À PRÉCISER : {name}]",
    "ar": "[يُحدَّد لاحقاً: {name}]",
}


# ---------------------------------------------------------------------------
# Specific templates for the highest-value clause categories.
# Each entry: {"en": {"template": str, "placeholders": [str, ...]}, "fr": {...}, "ar": {...}}
# ---------------------------------------------------------------------------

CLAUSE_TEMPLATES = {
    "liability": {
        "en": {
            "template": (
                "Except in cases of {carve_outs}, {party}'s aggregate liability "
                "arising out of or relating to this Agreement shall not exceed "
                "{cap_amount}. In no event shall either party be liable for "
                "indirect, incidental, special, or consequential damages, even "
                "if advised of the possibility of such damages."
            ),
            "placeholders": ["party", "cap_amount", "carve_outs"],
        },
        "fr": {
            "template": (
                "Sauf en cas de {carve_outs}, la responsabilité globale de "
                "{party} au titre du présent Contrat ne pourra excéder "
                "{cap_amount}. En aucun cas l'une des parties ne pourra être "
                "tenue responsable des dommages indirects, accessoires, "
                "spéciaux ou consécutifs, même si elle a été informée de la "
                "possibilité de tels dommages."
            ),
            "placeholders": ["party", "cap_amount", "carve_outs"],
        },
        "ar": {
            "template": (
                "باستثناء حالات {carve_outs}، لا تتجاوز المسؤولية الإجمالية "
                "لـ{party} الناشئة عن هذا العقد أو المتعلقة به {cap_amount}. "
                "لا يجوز بأي حال من الأحوال تحميل أي من الطرفين مسؤولية "
                "الأضرار غير المباشرة أو العرضية أو الخاصة أو التبعية، حتى "
                "لو تم إخطاره بإمكانية وقوع هذه الأضرار."
            ),
            "placeholders": ["party", "cap_amount", "carve_outs"],
        },
    },

    "termination": {
        "en": {
            "template": (
                "Either party may terminate this Agreement for cause upon "
                "{cure_period} written notice to the other party if the other "
                "party materially breaches this Agreement and fails to cure "
                "such breach within the notice period. {terminating_party} may "
                "terminate this Agreement for convenience upon {notice_period} "
                "prior written notice."
            ),
            "placeholders": ["cure_period", "terminating_party", "notice_period"],
        },
        "fr": {
            "template": (
                "Chaque partie peut résilier le présent Contrat pour motif "
                "après un préavis écrit de {cure_period} adressé à l'autre "
                "partie si celle-ci commet un manquement substantiel au "
                "présent Contrat et ne remédie pas à ce manquement dans le "
                "délai imparti. {terminating_party} peut résilier le présent "
                "Contrat pour convenance moyennant un préavis écrit de "
                "{notice_period}."
            ),
            "placeholders": ["cure_period", "terminating_party", "notice_period"],
        },
        "ar": {
            "template": (
                "يجوز لأي من الطرفين إنهاء هذا العقد لسبب مشروع بموجب إشعار "
                "خطي مدته {cure_period} يوجَّه إلى الطرف الآخر إذا أخلّ هذا "
                "الأخير إخلالاً جوهرياً بالعقد ولم يعالج هذا الإخلال خلال "
                "مهلة الإشعار. يجوز لـ{terminating_party} إنهاء هذا العقد "
                "لدواعي الملاءمة بموجب إشعار خطي مسبق مدته {notice_period}."
            ),
            "placeholders": ["cure_period", "terminating_party", "notice_period"],
        },
    },

    "confidentiality": {
        "en": {
            "template": (
                "Each party shall hold the other party's Confidential "
                "Information in strict confidence and shall not disclose it "
                "to any third party except {permitted_disclosures}, for a "
                "period of {duration} following disclosure. Upon termination "
                "of this Agreement, each party shall return or destroy all "
                "Confidential Information of the other party within "
                "{return_period}."
            ),
            "placeholders": ["permitted_disclosures", "duration", "return_period"],
        },
        "fr": {
            "template": (
                "Chaque partie conservera les Informations Confidentielles de "
                "l'autre partie sous stricte confidentialité et ne les "
                "divulguera à aucun tiers, sauf {permitted_disclosures}, "
                "pendant une durée de {duration} à compter de leur "
                "divulgation. À la résiliation du présent Contrat, chaque "
                "partie restituera ou détruira toutes les Informations "
                "Confidentielles de l'autre partie dans un délai de "
                "{return_period}."
            ),
            "placeholders": ["permitted_disclosures", "duration", "return_period"],
        },
        "ar": {
            "template": (
                "يلتزم كل طرف بالحفاظ على سرية المعلومات السرية للطرف الآخر "
                "وعدم إفشائها لأي طرف ثالث باستثناء {permitted_disclosures}، "
                "لمدة {duration} من تاريخ الإفصاح. عند إنهاء هذا العقد، "
                "يلتزم كل طرف بإعادة أو إتلاف جميع المعلومات السرية للطرف "
                "الآخر خلال {return_period}."
            ),
            "placeholders": ["permitted_disclosures", "duration", "return_period"],
        },
    },

    "payment": {
        "en": {
            "template": (
                "{payer} shall pay all undisputed invoices within "
                "{payment_terms} of receipt. Any amount not paid when due "
                "shall accrue interest at a rate of {interest_rate} per "
                "annum. {payer} may withhold payment of any amount disputed "
                "in good faith, provided it notifies {payee} of the dispute "
                "within {dispute_notice_period}."
            ),
            "placeholders": ["payer", "payment_terms", "interest_rate", "payee", "dispute_notice_period"],
        },
        "fr": {
            "template": (
                "{payer} paiera toutes les factures non contestées dans un "
                "délai de {payment_terms} à compter de leur réception. Tout "
                "montant impayé à échéance portera intérêt au taux de "
                "{interest_rate} par an. {payer} pourra retenir le paiement "
                "de tout montant contesté de bonne foi, à condition d'en "
                "notifier {payee} dans un délai de {dispute_notice_period}."
            ),
            "placeholders": ["payer", "payment_terms", "interest_rate", "payee", "dispute_notice_period"],
        },
        "ar": {
            "template": (
                "يلتزم {payer} بدفع جميع الفواتير غير المتنازع عليها خلال "
                "{payment_terms} من تاريخ استلامها. يستحق على أي مبلغ لم "
                "يُدفع في موعده فائدة بمعدل {interest_rate} سنوياً. يجوز "
                "لـ{payer} حجب دفع أي مبلغ متنازع عليه بحسن نية، شريطة "
                "إخطار {payee} بالنزاع خلال {dispute_notice_period}."
            ),
            "placeholders": ["payer", "payment_terms", "interest_rate", "payee", "dispute_notice_period"],
        },
    },

    "sla": {
        "en": {
            "template": (
                "{provider} shall use commercially reasonable efforts to "
                "achieve {uptime_target} availability of the Service, "
                "measured monthly, excluding Scheduled Maintenance and events "
                "of Force Majeure. If the Service falls below {uptime_target} "
                "in any calendar month, {customer} shall be entitled to a "
                "service credit of {service_credit}."
            ),
            "placeholders": ["provider", "uptime_target", "customer", "service_credit"],
        },
        "fr": {
            "template": (
                "{provider} déploiera des efforts commercialement "
                "raisonnables pour atteindre une disponibilité du Service de "
                "{uptime_target}, mesurée mensuellement, à l'exclusion de la "
                "Maintenance Planifiée et des cas de Force Majeure. Si le "
                "Service est inférieur à {uptime_target} au cours d'un mois "
                "calendaire, {customer} aura droit à un crédit de service de "
                "{service_credit}."
            ),
            "placeholders": ["provider", "uptime_target", "customer", "service_credit"],
        },
        "ar": {
            "template": (
                "يلتزم {provider} ببذل جهود معقولة تجارياً لتحقيق توافر "
                "للخدمة بنسبة {uptime_target}، تُقاس شهرياً، باستثناء "
                "الصيانة المجدولة وحالات القوة القاهرة. وإذا انخفض توافر "
                "الخدمة عن {uptime_target} خلال أي شهر تقويمي، يحق "
                "لـ{customer} الحصول على تعويض خدمة بقيمة {service_credit}."
            ),
            "placeholders": ["provider", "uptime_target", "customer", "service_credit"],
        },
    },

    "data_privacy_security": {
        "en": {
            "template": (
                "{processor} shall process Personal Data only on documented "
                "instructions from {controller}, implement appropriate "
                "technical and organizational security measures, and notify "
                "{controller} without undue delay, and in any event within "
                "{breach_notice_period}, upon becoming aware of a Personal "
                "Data Breach. {processor} shall not engage a sub-processor "
                "without {controller}'s {subprocessor_consent}."
            ),
            "placeholders": ["processor", "controller", "breach_notice_period", "subprocessor_consent"],
        },
        "fr": {
            "template": (
                "{processor} traitera les Données Personnelles uniquement "
                "sur instructions documentées de {controller}, mettra en "
                "œuvre des mesures de sécurité techniques et organisationnelles "
                "appropriées, et notifiera {controller} sans retard "
                "injustifié, et en tout état de cause dans un délai de "
                "{breach_notice_period}, dès qu'il aura connaissance d'une "
                "violation de Données Personnelles. {processor} ne fera "
                "appel à aucun sous-traitant sans {subprocessor_consent} de "
                "{controller}."
            ),
            "placeholders": ["processor", "controller", "breach_notice_period", "subprocessor_consent"],
        },
        "ar": {
            "template": (
                "يلتزم {processor} بمعالجة البيانات الشخصية فقط بناءً على "
                "تعليمات موثقة من {controller}، وتنفيذ تدابير أمنية تقنية "
                "وتنظيمية مناسبة، وإخطار {controller} دون تأخير لا مبرر له، "
                "وفي جميع الأحوال خلال {breach_notice_period}، فور علمه "
                "بوقوع خرق للبيانات الشخصية. لا يجوز لـ{processor} "
                "الاستعانة بمعالج فرعي دون {subprocessor_consent} من "
                "{controller}."
            ),
            "placeholders": ["processor", "controller", "breach_notice_period", "subprocessor_consent"],
        },
    },

    "intellectual_property": {
        "en": {
            "template": (
                "As between the parties, {ip_owner} shall own all right, "
                "title, and interest in and to the Deliverables, including "
                "all Intellectual Property Rights therein, {carve_out}. "
                "{other_party} hereby assigns to {ip_owner} all right, "
                "title, and interest in the Deliverables upon "
                "{assignment_trigger}."
            ),
            "placeholders": ["ip_owner", "carve_out", "other_party", "assignment_trigger"],
        },
        "fr": {
            "template": (
                "Entre les parties, {ip_owner} sera propriétaire de tous les "
                "droits, titres et intérêts afférents aux Livrables, y "
                "compris tous les Droits de Propriété Intellectuelle y "
                "afférents, {carve_out}. {other_party} cède par les "
                "présentes à {ip_owner} tous les droits, titres et intérêts "
                "sur les Livrables dès {assignment_trigger}."
            ),
            "placeholders": ["ip_owner", "carve_out", "other_party", "assignment_trigger"],
        },
        "ar": {
            "template": (
                "فيما بين الطرفين، يمتلك {ip_owner} كافة الحقوق والملكية "
                "والمصالح المتعلقة بالمخرجات، بما في ذلك جميع حقوق الملكية "
                "الفكرية المرتبطة بها، {carve_out}. يتنازل {other_party} "
                "بموجب هذا لـ{ip_owner} عن كافة الحقوق والملكية والمصالح في "
                "المخرجات عند {assignment_trigger}."
            ),
            "placeholders": ["ip_owner", "carve_out", "other_party", "assignment_trigger"],
        },
    },

    "indemnification": {
        "en": {
            "template": (
                "{indemnitor} shall defend, indemnify, and hold harmless "
                "{indemnitee} from and against any third-party claims, "
                "damages, losses, and expenses (including reasonable "
                "attorneys' fees) arising out of {covered_claims}, provided "
                "that {indemnitee} promptly notifies {indemnitor} of the "
                "claim and gives {indemnitor} sole control of the defense."
            ),
            "placeholders": ["indemnitor", "indemnitee", "covered_claims"],
        },
        "fr": {
            "template": (
                "{indemnitor} défendra, indemnisera et tiendra {indemnitee} "
                "indemne de toute réclamation de tiers, dommage, perte ou "
                "dépense (y compris les honoraires d'avocat raisonnables) "
                "découlant de {covered_claims}, à condition que "
                "{indemnitee} notifie promptement {indemnitor} de la "
                "réclamation et lui confère le contrôle exclusif de la "
                "défense."
            ),
            "placeholders": ["indemnitor", "indemnitee", "covered_claims"],
        },
        "ar": {
            "template": (
                "يلتزم {indemnitor} بالدفاع عن {indemnitee} وتعويضه وإبراء "
                "ذمته من أي مطالبات أو أضرار أو خسائر أو نفقات من الغير "
                "(بما في ذلك أتعاب المحاماة المعقولة) الناشئة عن "
                "{covered_claims}، شريطة أن يقوم {indemnitee} بإخطار "
                "{indemnitor} فوراً بالمطالبة ومنحه السيطرة الكاملة على "
                "الدفاع."
            ),
            "placeholders": ["indemnitor", "indemnitee", "covered_claims"],
        },
    },

    "warranty": {
        "en": {
            "template": (
                "{warrantor} warrants that the {subject_matter} will "
                "{warranty_standard} for a period of {warranty_period} from "
                "{warranty_start}. {warrantor}'s sole obligation, and "
                "{beneficiary}'s exclusive remedy, for breach of this "
                "warranty shall be {remedy}."
            ),
            "placeholders": ["warrantor", "subject_matter", "warranty_standard", "warranty_period", "warranty_start", "beneficiary", "remedy"],
        },
        "fr": {
            "template": (
                "{warrantor} garantit que {subject_matter} {warranty_standard} "
                "pendant une durée de {warranty_period} à compter de "
                "{warranty_start}. La seule obligation de {warrantor}, et le "
                "recours exclusif de {beneficiary}, en cas de manquement à "
                "cette garantie sera {remedy}."
            ),
            "placeholders": ["warrantor", "subject_matter", "warranty_standard", "warranty_period", "warranty_start", "beneficiary", "remedy"],
        },
        "ar": {
            "template": (
                "يضمن {warrantor} أن {subject_matter} {warranty_standard} "
                "لمدة {warranty_period} اعتباراً من {warranty_start}. يكون "
                "الالتزام الوحيد لـ{warrantor}، ووسيلة الانتصاف الحصرية "
                "لـ{beneficiary}، عند الإخلال بهذا الضمان هو {remedy}."
            ),
            "placeholders": ["warrantor", "subject_matter", "warranty_standard", "warranty_period", "warranty_start", "beneficiary", "remedy"],
        },
    },

    "insurance": {
        "en": {
            "template": (
                "{party} shall maintain, at its own expense, "
                "{coverage_type} insurance with minimum coverage limits of "
                "{coverage_amount}, and shall provide {other_party} with a "
                "certificate of insurance evidencing such coverage upon "
                "request. {party} shall notify {other_party} at least "
                "{cancellation_notice} prior to any cancellation or material "
                "reduction of coverage."
            ),
            "placeholders": ["party", "coverage_type", "coverage_amount", "other_party", "cancellation_notice"],
        },
        "fr": {
            "template": (
                "{party} maintiendra, à ses frais, une assurance "
                "{coverage_type} avec des limites de couverture minimales de "
                "{coverage_amount}, et fournira à {other_party} une "
                "attestation d'assurance sur demande. {party} notifiera "
                "{other_party} au moins {cancellation_notice} avant toute "
                "annulation ou réduction substantielle de la couverture."
            ),
            "placeholders": ["party", "coverage_type", "coverage_amount", "other_party", "cancellation_notice"],
        },
        "ar": {
            "template": (
                "يلتزم {party}، على نفقته الخاصة، بالحفاظ على تأمين من نوع "
                "{coverage_type} بحد أدنى للتغطية قدره {coverage_amount}، "
                "وتزويد {other_party} بشهادة تأمين تثبت هذه التغطية عند "
                "الطلب. يلتزم {party} بإخطار {other_party} قبل "
                "{cancellation_notice} على الأقل من أي إلغاء أو تخفيض جوهري "
                "للتغطية."
            ),
            "placeholders": ["party", "coverage_type", "coverage_amount", "other_party", "cancellation_notice"],
        },
    },

    "force_majeure": {
        "en": {
            "template": (
                "Neither party shall be liable for any failure or delay in "
                "performance to the extent caused by a Force Majeure Event, "
                "provided that the affected party gives notice to the other "
                "party within {notice_period} of becoming aware of the "
                "event and uses reasonable efforts to mitigate its effects. "
                "If a Force Majeure Event continues for more than "
                "{suspension_period}, either party may terminate this "
                "Agreement upon written notice."
            ),
            "placeholders": ["notice_period", "suspension_period"],
        },
        "fr": {
            "template": (
                "Aucune partie ne sera responsable d'un manquement ou d'un "
                "retard d'exécution dans la mesure où celui-ci résulte d'un "
                "Cas de Force Majeure, à condition que la partie affectée "
                "notifie l'autre partie dans un délai de {notice_period} "
                "après avoir eu connaissance de l'événement et déploie des "
                "efforts raisonnables pour en atténuer les effets. Si un "
                "Cas de Force Majeure se poursuit pendant plus de "
                "{suspension_period}, chaque partie pourra résilier le "
                "présent Contrat par notification écrite."
            ),
            "placeholders": ["notice_period", "suspension_period"],
        },
        "ar": {
            "template": (
                "لا يتحمل أي من الطرفين مسؤولية أي إخفاق أو تأخير في "
                "التنفيذ بقدر ما يكون ناتجاً عن حدث قوة قاهرة، شريطة أن "
                "يقوم الطرف المتأثر بإخطار الطرف الآخر خلال {notice_period} "
                "من علمه بالحدث وأن يبذل جهوداً معقولة للتخفيف من آثاره. "
                "وإذا استمر حدث القوة القاهرة لأكثر من {suspension_period}، "
                "يجوز لأي من الطرفين إنهاء هذا العقد بموجب إشعار خطي."
            ),
            "placeholders": ["notice_period", "suspension_period"],
        },
    },

    "governing_law": {
        "en": {
            "template": (
                "This Agreement shall be governed by and construed in "
                "accordance with the laws of {governing_law}, without "
                "regard to its conflict of laws principles. Any dispute "
                "arising out of or relating to this Agreement shall be "
                "submitted to {dispute_forum}."
            ),
            "placeholders": ["governing_law", "dispute_forum"],
        },
        "fr": {
            "template": (
                "Le présent Contrat est régi et interprété conformément aux "
                "lois de {governing_law}, sans égard à ses principes de "
                "conflit de lois. Tout litige découlant du présent Contrat "
                "ou en relation avec celui-ci sera soumis à {dispute_forum}."
            ),
            "placeholders": ["governing_law", "dispute_forum"],
        },
        "ar": {
            "template": (
                "يخضع هذا العقد ويُفسَّر وفقاً لقوانين {governing_law}، دون "
                "اعتبار لمبادئ تنازع القوانين فيها. تُحال أي منازعة تنشأ عن "
                "هذا العقد أو تتعلق به إلى {dispute_forum}."
            ),
            "placeholders": ["governing_law", "dispute_forum"],
        },
    },

    "restrictive_covenants": {
        "en": {
            "template": (
                "During the term of this Agreement and for a period of "
                "{duration} thereafter, {restricted_party} shall not, "
                "within {territory}, {restricted_activity}, except "
                "{carve_outs}."
            ),
            "placeholders": ["duration", "restricted_party", "territory", "restricted_activity", "carve_outs"],
        },
        "fr": {
            "template": (
                "Pendant la durée du présent Contrat et pour une période de "
                "{duration} suivant celle-ci, {restricted_party} s'engage à "
                "ne pas, sur {territory}, {restricted_activity}, sauf "
                "{carve_outs}."
            ),
            "placeholders": ["duration", "restricted_party", "territory", "restricted_activity", "carve_outs"],
        },
        "ar": {
            "template": (
                "خلال مدة هذا العقد ولمدة {duration} بعد انتهائه، يلتزم "
                "{restricted_party} بعدم القيام بـ{restricted_activity} "
                "ضمن {territory}، باستثناء {carve_outs}."
            ),
            "placeholders": ["duration", "restricted_party", "territory", "restricted_activity", "carve_outs"],
        },
    },

    "assignment": {
        "en": {
            "template": (
                "Neither party may assign or transfer this Agreement, in "
                "whole or in part, without the prior written consent of the "
                "other party, except that {permitted_assignee} may assign "
                "this Agreement without consent to {permitted_transfer_scenarios}."
            ),
            "placeholders": ["permitted_assignee", "permitted_transfer_scenarios"],
        },
        "fr": {
            "template": (
                "Aucune partie ne peut céder ou transférer le présent "
                "Contrat, en tout ou partie, sans le consentement écrit "
                "préalable de l'autre partie, sauf que {permitted_assignee} "
                "peut céder le présent Contrat sans consentement dans le "
                "cadre de {permitted_transfer_scenarios}."
            ),
            "placeholders": ["permitted_assignee", "permitted_transfer_scenarios"],
        },
        "ar": {
            "template": (
                "لا يجوز لأي من الطرفين التنازل عن هذا العقد أو نقله، كلياً "
                "أو جزئياً، دون موافقة خطية مسبقة من الطرف الآخر، باستثناء "
                "أنه يجوز لـ{permitted_assignee} التنازل عن هذا العقد دون "
                "موافقة في حالات {permitted_transfer_scenarios}."
            ),
            "placeholders": ["permitted_assignee", "permitted_transfer_scenarios"],
        },
    },

    "exclusivity": {
        "en": {
            "template": (
                "During the Exclusivity Period of {duration}, "
                "{granting_party} shall not, within {scope}, "
                "{restricted_conduct}, provided that {beneficiary} achieves "
                "{performance_threshold}."
            ),
            "placeholders": ["duration", "granting_party", "scope", "restricted_conduct", "beneficiary", "performance_threshold"],
        },
        "fr": {
            "template": (
                "Pendant la Période d'Exclusivité de {duration}, "
                "{granting_party} s'engage à ne pas, dans le cadre de "
                "{scope}, {restricted_conduct}, sous réserve que "
                "{beneficiary} atteigne {performance_threshold}."
            ),
            "placeholders": ["duration", "granting_party", "scope", "restricted_conduct", "beneficiary", "performance_threshold"],
        },
        "ar": {
            "template": (
                "خلال فترة الحصرية البالغة {duration}، يلتزم "
                "{granting_party} بعدم القيام بـ{restricted_conduct} ضمن "
                "{scope}، شريطة أن يحقق {beneficiary} "
                "{performance_threshold}."
            ),
            "placeholders": ["duration", "granting_party", "scope", "restricted_conduct", "beneficiary", "performance_threshold"],
        },
    },

    "non_disparagement": {
        "en": {
            "template": (
                "Each party agrees not to make any statement, written or "
                "oral, that disparages or is likely to damage the "
                "reputation of the other party, except {legal_exceptions}, "
                "for a period of {duration} following {trigger_event}."
            ),
            "placeholders": ["legal_exceptions", "duration", "trigger_event"],
        },
        "fr": {
            "template": (
                "Chaque partie s'engage à ne faire aucune déclaration, "
                "écrite ou orale, dénigrant ou susceptible de porter "
                "atteinte à la réputation de l'autre partie, sauf "
                "{legal_exceptions}, pendant une durée de {duration} "
                "suivant {trigger_event}."
            ),
            "placeholders": ["legal_exceptions", "duration", "trigger_event"],
        },
        "ar": {
            "template": (
                "يتعهد كل طرف بعدم الإدلاء بأي تصريح، كتابي أو شفهي، يسيء "
                "إلى سمعة الطرف الآخر أو قد يضر بها، باستثناء "
                "{legal_exceptions}، لمدة {duration} بعد {trigger_event}."
            ),
            "placeholders": ["legal_exceptions", "duration", "trigger_event"],
        },
    },

    "financial_covenants": {
        "en": {
            "template": (
                "{borrower} shall maintain, as tested {testing_frequency}, "
                "a {covenant_metric} of no {covenant_direction} than "
                "{covenant_threshold}. In the event of a breach of this "
                "covenant, {borrower} shall have a cure period of "
                "{cure_period} before an Event of Default is triggered."
            ),
            "placeholders": ["borrower", "testing_frequency", "covenant_metric", "covenant_direction", "covenant_threshold", "cure_period"],
        },
        "fr": {
            "template": (
                "{borrower} maintiendra, tel que mesuré "
                "{testing_frequency}, un {covenant_metric} "
                "{covenant_direction} à {covenant_threshold}. En cas de "
                "manquement à cet engagement, {borrower} bénéficiera d'un "
                "délai de régularisation de {cure_period} avant que ne se "
                "déclenche un Cas de Défaut."
            ),
            "placeholders": ["borrower", "testing_frequency", "covenant_metric", "covenant_direction", "covenant_threshold", "cure_period"],
        },
        "ar": {
            "template": (
                "يلتزم {borrower} بالحفاظ، وفق قياس {testing_frequency}، "
                "على {covenant_metric} {covenant_direction} "
                "{covenant_threshold}. وفي حال الإخلال بهذا التعهد، يُمنح "
                "{borrower} مهلة معالجة مدتها {cure_period} قبل تفعيل حالة "
                "التعثر."
            ),
            "placeholders": ["borrower", "testing_frequency", "covenant_metric", "covenant_direction", "covenant_threshold", "cure_period"],
        },
    },

    "rent_and_escalation": {
        "en": {
            "template": (
                "{tenant} shall pay {landlord} base rent of {base_rent} per "
                "{rent_period}, payable in advance. Base rent shall "
                "increase by {escalation_rate} on each anniversary of the "
                "Commencement Date."
            ),
            "placeholders": ["tenant", "landlord", "base_rent", "rent_period", "escalation_rate"],
        },
        "fr": {
            "template": (
                "{tenant} versera à {landlord} un loyer de base de "
                "{base_rent} par {rent_period}, payable d'avance. Le loyer "
                "de base augmentera de {escalation_rate} à chaque "
                "anniversaire de la Date de Prise d'Effet."
            ),
            "placeholders": ["tenant", "landlord", "base_rent", "rent_period", "escalation_rate"],
        },
        "ar": {
            "template": (
                "يلتزم {tenant} بدفع إيجار أساسي لـ{landlord} قدره "
                "{base_rent} عن كل {rent_period}، يُدفع مقدماً. يزداد "
                "الإيجار الأساسي بنسبة {escalation_rate} في كل ذكرى سنوية "
                "لتاريخ بدء العقد."
            ),
            "placeholders": ["tenant", "landlord", "base_rent", "rent_period", "escalation_rate"],
        },
    },

    "corporate_governance": {
        "en": {
            "template": (
                "The Board shall consist of {board_composition}. "
                "{reserved_matters_holder} approval shall be required for "
                "{reserved_matters}. In the event of a deadlock, the "
                "parties shall {deadlock_mechanism}."
            ),
            "placeholders": ["board_composition", "reserved_matters_holder", "reserved_matters", "deadlock_mechanism"],
        },
        "fr": {
            "template": (
                "Le Conseil d'Administration sera composé de "
                "{board_composition}. L'approbation de "
                "{reserved_matters_holder} sera requise pour "
                "{reserved_matters}. En cas de blocage, les parties devront "
                "{deadlock_mechanism}."
            ),
            "placeholders": ["board_composition", "reserved_matters_holder", "reserved_matters", "deadlock_mechanism"],
        },
        "ar": {
            "template": (
                "يتكون مجلس الإدارة من {board_composition}. تُشترط موافقة "
                "{reserved_matters_holder} على {reserved_matters}. وفي حال "
                "حدوث جمود، يلتزم الطرفان بـ{deadlock_mechanism}."
            ),
            "placeholders": ["board_composition", "reserved_matters_holder", "reserved_matters", "deadlock_mechanism"],
        },
    },

    "severability": {
        "en": {
            "template": (
                "If any provision of this Agreement is held to be invalid "
                "or unenforceable, the remaining provisions shall continue "
                "in full force and effect, and the parties shall negotiate "
                "in good faith to replace the invalid provision with a "
                "valid one that reflects the original commercial intent as "
                "closely as possible."
            ),
            "placeholders": [],
        },
        "fr": {
            "template": (
                "Si une disposition du présent Contrat est jugée invalide "
                "ou inapplicable, les autres dispositions resteront "
                "pleinement en vigueur, et les parties négocieront de bonne "
                "foi le remplacement de la disposition invalide par une "
                "disposition valide reflétant aussi fidèlement que possible "
                "l'intention commerciale initiale."
            ),
            "placeholders": [],
        },
        "ar": {
            "template": (
                "إذا تبين أن أحد أحكام هذا العقد غير صحيح أو غير قابل "
                "للتنفيذ، تظل بقية الأحكام سارية المفعول الكامل، ويلتزم "
                "الطرفان بالتفاوض بحسن نية لاستبدال الحكم غير الصحيح بحكم "
                "صحيح يعكس النية التجارية الأصلية قدر الإمكان."
            ),
            "placeholders": [],
        },
    },
}


# ---------------------------------------------------------------------------
# Universal fallback: guarantees a draftable skeleton for ANY clause_type,
# including ones with no specific template above and ones from contract
# domains not explicitly modeled anywhere in the stack.
# ---------------------------------------------------------------------------

GENERIC_TEMPLATE = {
    "en": {
        "template": (
            "{obligated_party} shall {obligation}, subject to {conditions}. "
            "Failure to comply with this clause may result in {consequence}."
        ),
        "placeholders": ["obligated_party", "obligation", "conditions", "consequence"],
    },
    "fr": {
        "template": (
            "{obligated_party} s'engage à {obligation}, sous réserve de "
            "{conditions}. Le non-respect de cette clause peut entraîner "
            "{consequence}."
        ),
        "placeholders": ["obligated_party", "obligation", "conditions", "consequence"],
    },
    "ar": {
        "template": (
            "يلتزم {obligated_party} بـ{obligation}، مع مراعاة "
            "{conditions}. وقد يترتب على عدم الامتثال لهذا البند "
            "{consequence}."
        ),
        "placeholders": ["obligated_party", "obligation", "conditions", "consequence"],
    },
}


def get_clause_template(clause_type: str, language: str = "en") -> dict:
    """
    Return the raw template (with {placeholders}) for a clause_type.

    Always returns a usable template: a specific one for ~20 high-value
    categories, or the universal generic skeleton for anything else
    (including unknown/unlisted contract domains), so this never fails
    regardless of clause_type or contract domain.
    """
    language = get_language(language)
    normalized_type = normalize_clause_type(clause_type)

    entry = CLAUSE_TEMPLATES.get(normalized_type)

    if not entry:
        generic = GENERIC_TEMPLATE[language]
        return {
            "clause_type": normalized_type,
            "template": generic["template"],
            "placeholders": list(generic["placeholders"]),
            "specific": False,
            "disclaimer": DISCLAIMER[language],
        }

    specific = entry.get(language, entry["en"])
    return {
        "clause_type": normalized_type,
        "template": specific["template"],
        "placeholders": list(specific["placeholders"]),
        "specific": True,
        "disclaimer": DISCLAIMER[language],
    }


def render_clause_template(
    clause_type: str,
    language: str = "en",
    **values: str,
) -> dict:
    """
    Fill a clause template with provided values. Any placeholder not
    supplied in `values` is replaced with a visibly bracketed prompt
    (never left as a raw {token} and never silently dropped), so a
    rendered draft is always honest about what still needs input.
    """
    language = get_language(language)
    info = get_clause_template(clause_type, language)

    template = info["template"]
    placeholders = info["placeholders"]

    unresolved = []
    fill = {}

    for name in placeholders:
        if name in values and str(values[name]).strip():
            fill[name] = str(values[name]).strip()
        else:
            fill[name] = UNRESOLVED_PLACEHOLDER[language].format(name=name)
            unresolved.append(name)

    try:
        draft_wording = template.format(**fill)
    except (KeyError, IndexError):
        # Defensive: should not happen since fill covers all placeholders,
        # but never let a formatting edge case break the caller.
        draft_wording = template

    return {
        "clause_type": info["clause_type"],
        "draft_wording": draft_wording,
        "specific": info["specific"],
        "unresolved_placeholders": unresolved,
        "disclaimer": info["disclaimer"],
    }
