"""
clause_interactions.py

Cross-clause legal reasoning: detects tensions, dependencies, or
reinforcing effects BETWEEN pairs of clauses present in the same
contract, instead of reasoning on each clause in isolation.

Also provides optional, non-binding jurisdiction caveats: general
informational notes on how enforceability commonly varies by
jurisdiction. These are explicitly NOT legal advice and are phrased as
general considerations, not conclusions about any specific contract.

Design goals (same as the rest of the contract_agent stack):
- Works for any contract family and industry.
- Supports EN / FR / AR.
- Purely additive: does not modify market_intelligence.py,
  clause_wording_library.py, or clause_templates.py; only imports the
  shared clause-type resolver so all modules stay in sync.
- Silence is an acceptable, honest answer: if two clause types have no
  known documented interaction, nothing is returned for that pair
  rather than fabricating a generic-sounding but meaningless insight.
  Jurisdiction caveats, by contrast, always return something (a
  general "verify locally" fallback) since the person explicitly asked
  about a jurisdiction and deserves a substantive answer either way.
"""

from app.services.contract_agent.market_intelligence import (
    normalize_clause_type,
    get_language,
)


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


# ---------------------------------------------------------------------------
# Pairwise clause interactions.
# Keys are frozensets of two normalized clause_type strings (order-independent).
# ---------------------------------------------------------------------------

def _pair(a: str, b: str) -> frozenset:
    return frozenset({a, b})


CLAUSE_INTERACTIONS = {
    _pair("liability", "indemnification"): {
        "severity": "high",
        "insight": {
            "en": (
                "The liability cap and the indemnification obligation should "
                "be reconciled: if indemnification is left uncapped or is not "
                "expressly made subject to the liability cap, it can "
                "effectively bypass that cap and reintroduce unlimited "
                "exposure through the back door."
            ),
            "fr": (
                "Le plafond de responsabilité et l'obligation d'indemnisation "
                "doivent être mis en cohérence : si l'indemnisation reste non "
                "plafonnée ou n'est pas expressément soumise au plafond de "
                "responsabilité, elle peut en pratique contourner ce plafond "
                "et réintroduire une exposition illimitée par une autre voie."
            ),
            "ar": (
                "يجب التوفيق بين حد المسؤولية والتزام التعويض: فإذا بقي "
                "التعويض غير محدود أو لم يُخضع صراحة لحد المسؤولية، فقد "
                "يتجاوز هذا الحد فعلياً ويعيد إدخال تعرض غير محدود من باب آخر."
            ),
        },
    },

    _pair("liability", "insurance"): {
        "severity": "medium",
        "insight": {
            "en": (
                "The liability cap should be checked against available "
                "insurance coverage: a cap set well below the insured amount "
                "may leave recoverable insurance proceeds unused, while a cap "
                "set above coverage limits can leave residual exposure "
                "uninsured."
            ),
            "fr": (
                "Le plafond de responsabilité doit être comparé à la "
                "couverture d'assurance disponible : un plafond fixé bien "
                "en dessous du montant assuré peut laisser inutilisée une "
                "indemnisation recouvrable, tandis qu'un plafond supérieur "
                "aux limites de couverture peut laisser une exposition "
                "résiduelle non assurée."
            ),
            "ar": (
                "يجب مقارنة حد المسؤولية بالتغطية التأمينية المتاحة: فحد "
                "أقل بكثير من المبلغ المؤمَّن قد يترك تعويضاً قابلاً "
                "للاسترداد دون استخدام، بينما حد أعلى من حدود التغطية قد "
                "يترك تعرضاً متبقياً دون تأمين."
            ),
        },
    },

    _pair("liability", "warranty"): {
        "severity": "medium",
        "insight": {
            "en": (
                "Warranty remedies and the liability cap can conflict if the "
                "warranty section provides its own uncapped remedy (such as "
                "replacement or refund) that is not explicitly stated to be "
                "the parties' sole and exclusive remedy subject to the "
                "liability limitations elsewhere in the contract."
            ),
            "fr": (
                "Les recours de garantie et le plafond de responsabilité "
                "peuvent entrer en conflit si la clause de garantie prévoit "
                "son propre recours non plafonné (remplacement, "
                "remboursement) sans préciser expressément qu'il constitue "
                "le recours exclusif des parties, soumis aux limitations de "
                "responsabilité prévues ailleurs dans le contrat."
            ),
            "ar": (
                "قد تتعارض وسائل انتصاف الضمان مع حد المسؤولية إذا نص بند "
                "الضمان على وسيلة انتصاف خاصة به غير محدودة (كالاستبدال أو "
                "استرداد الثمن) دون النص صراحة على أنها الوسيلة الحصرية "
                "الخاضعة لحدود المسؤولية المنصوص عليها في موضع آخر من العقد."
            ),
        },
    },

    _pair("indemnification", "insurance"): {
        "severity": "medium",
        "insight": {
            "en": (
                "Indemnification obligations and insurance requirements "
                "should be aligned: the required insurance should reasonably "
                "cover the scope of indemnified claims so the indemnifying "
                "party is not left personally exposed for risks it agreed to "
                "cover but did not actually insure."
            ),
            "fr": (
                "Les obligations d'indemnisation et les exigences "
                "d'assurance doivent être alignées : l'assurance requise "
                "devrait raisonnablement couvrir le périmètre des "
                "réclamations indemnisées, afin que la partie indemnisante "
                "ne reste pas personnellement exposée pour des risques "
                "qu'elle a accepté de couvrir sans les assurer réellement."
            ),
            "ar": (
                "يجب مواءمة التزامات التعويض مع متطلبات التأمين: ينبغي أن "
                "تغطي التغطية التأمينية المطلوبة بشكل معقول نطاق المطالبات "
                "المشمولة بالتعويض، حتى لا يبقى الطرف الملتزم بالتعويض "
                "معرضاً شخصياً لمخاطر وافق على تغطيتها دون تأمينها فعلياً."
            ),
        },
    },

    _pair("termination", "survival"): {
        "severity": "medium",
        "insight": {
            "en": (
                "Termination rights should be read together with the "
                "survival clause: obligations the parties intend to outlast "
                "the contract (confidentiality, payment, liability, IP, "
                "dispute resolution) must be expressly listed as surviving, "
                "or termination may be read as extinguishing them entirely."
            ),
            "fr": (
                "Les droits de résiliation doivent être lus conjointement "
                "avec la clause de survie : les obligations que les parties "
                "entendent voir perdurer après le contrat (confidentialité, "
                "paiement, responsabilité, propriété intellectuelle, "
                "règlement des litiges) doivent être expressément listées "
                "comme survivantes, sous peine que la résiliation soit "
                "interprétée comme les éteignant entièrement."
            ),
            "ar": (
                "يجب قراءة حقوق الإنهاء مقترنة ببند الاستمرارية: "
                "الالتزامات التي يرغب الطرفان في استمرارها بعد العقد "
                "(السرية، الدفع، المسؤولية، الملكية الفكرية، تسوية "
                "النزاعات) يجب سردها صراحة كالتزامات مستمرة، وإلا فقد "
                "يُفسَّر الإنهاء على أنه ينهيها بالكامل."
            ),
        },
    },

    _pair("confidentiality", "survival"): {
        "severity": "medium",
        "insight": {
            "en": (
                "If confidentiality is not expressly listed in the survival "
                "clause, its duration set within the confidentiality clause "
                "itself may be undermined or create ambiguity as to whether "
                "it continues to apply after termination."
            ),
            "fr": (
                "Si la confidentialité n'est pas expressément listée dans la "
                "clause de survie, la durée fixée dans la clause de "
                "confidentialité elle-même peut être remise en cause ou "
                "créer une ambiguïté quant à sa poursuite après résiliation."
            ),
            "ar": (
                "إذا لم تُدرج السرية صراحة في بند الاستمرارية، فقد تتأثر "
                "المدة المحددة في بند السرية نفسه أو ينشأ غموض حول استمرار "
                "سريانها بعد الإنهاء."
            ),
        },
    },

    _pair("data_privacy_security", "indemnification"): {
        "severity": "high",
        "insight": {
            "en": (
                "Data-breach costs (regulatory fines, notification costs, "
                "credit monitoring, third-party claims) can be very large; "
                "check whether the indemnification clause explicitly covers "
                "data-security incidents and whether that indemnity is "
                "subject to, carved out of, or exceeds the general liability "
                "cap."
            ),
            "fr": (
                "Les coûts liés à une violation de données (amendes "
                "réglementaires, coûts de notification, surveillance de "
                "crédit, réclamations de tiers) peuvent être très élevés ; "
                "vérifier si la clause d'indemnisation couvre explicitement "
                "les incidents de sécurité des données et si cette "
                "indemnisation est soumise au plafond général de "
                "responsabilité, en est exclue, ou le dépasse."
            ),
            "ar": (
                "قد تكون تكاليف خرق البيانات (الغرامات التنظيمية، تكاليف "
                "الإخطار، مراقبة الائتمان، مطالبات الغير) كبيرة جداً؛ يجب "
                "التحقق مما إذا كان بند التعويض يغطي صراحة حوادث أمن "
                "البيانات وما إذا كان هذا التعويض خاضعاً لحد المسؤولية "
                "العام أو مستثنى منه أو يتجاوزه."
            ),
        },
    },

    _pair("data_privacy_security", "liability"): {
        "severity": "high",
        "insight": {
            "en": (
                "Many data-protection regimes impose fines and liabilities "
                "that cannot be capped or excluded by private agreement; "
                "confirm the liability clause does not purport to limit "
                "exposure for data-protection breaches beyond what "
                "applicable law permits."
            ),
            "fr": (
                "De nombreux régimes de protection des données imposent des "
                "amendes et responsabilités qui ne peuvent être plafonnées "
                "ou exclues par accord privé ; vérifier que la clause de "
                "responsabilité ne prétend pas limiter l'exposition pour les "
                "violations de protection des données au-delà de ce que la "
                "loi applicable permet."
            ),
            "ar": (
                "تفرض العديد من أنظمة حماية البيانات غرامات ومسؤوليات لا "
                "يمكن تحديدها أو استبعادها باتفاق خاص؛ يجب التأكد من أن بند "
                "المسؤولية لا يحاول تحديد التعرض عن مخالفات حماية البيانات "
                "بما يتجاوز ما يسمح به القانون المعمول به."
            ),
        },
    },

    _pair("intellectual_property", "indemnification"): {
        "severity": "medium",
        "insight": {
            "en": (
                "Check whether IP infringement claims by third parties are "
                "explicitly covered by the indemnification clause (an "
                "\"IP indemnity\") and whether that indemnity is carved out "
                "of the general liability cap, since IP infringement "
                "exposure is often treated as a heightened risk category."
            ),
            "fr": (
                "Vérifier si les réclamations de tiers pour contrefaçon de "
                "propriété intellectuelle sont explicitement couvertes par "
                "la clause d'indemnisation (une « indemnisation PI ») et si "
                "cette indemnisation est exclue du plafond général de "
                "responsabilité, la contrefaçon étant souvent traitée comme "
                "une catégorie de risque aggravée."
            ),
            "ar": (
                "يجب التحقق مما إذا كانت مطالبات الغير المتعلقة بانتهاك "
                "الملكية الفكرية مشمولة صراحة ببند التعويض (\"تعويض "
                "الملكية الفكرية\") وما إذا كان هذا التعويض مستثنى من حد "
                "المسؤولية العام، إذ غالباً ما يُعامل التعرض لانتهاك "
                "الملكية الفكرية كفئة مخاطر مشددة."
            ),
        },
    },

    _pair("exclusivity", "restrictive_covenants"): {
        "severity": "medium",
        "insight": {
            "en": (
                "Exclusivity and restrictive covenants can stack to create a "
                "combined restriction broader than either clause alone; "
                "review the total restricted scope, territory, and duration "
                "across both clauses together, as enforceability is often "
                "assessed on their cumulative effect."
            ),
            "fr": (
                "L'exclusivité et les engagements restrictifs peuvent se "
                "cumuler pour créer une restriction globale plus large que "
                "chaque clause prise isolément ; examiner le périmètre, le "
                "territoire et la durée restreints au total sur les deux "
                "clauses, l'applicabilité étant souvent appréciée au regard "
                "de leur effet cumulé."
            ),
            "ar": (
                "قد تتراكم الحصرية والتعهدات التقييدية لتُنشئ قيداً إجمالياً "
                "أوسع من كل بند على حدة؛ يجب مراجعة النطاق والإقليم والمدة "
                "الإجمالية عبر البندين معاً، إذ غالباً ما تُقيَّم قابلية "
                "التنفيذ بناءً على أثرهما التراكمي."
            ),
        },
    },

    _pair("assignment", "change_of_control"): {
        "severity": "medium",
        "insight": {
            "en": (
                "Check whether a change of control is treated as a deemed "
                "assignment under the assignment clause; if not explicitly "
                "addressed, a change of control may bypass assignment "
                "consent requirements entirely, undermining their purpose."
            ),
            "fr": (
                "Vérifier si un changement de contrôle est traité comme une "
                "cession réputée au sens de la clause de cession ; à défaut "
                "de traitement explicite, un changement de contrôle peut "
                "contourner entièrement les exigences de consentement à la "
                "cession, en compromettant l'objectif."
            ),
            "ar": (
                "يجب التحقق مما إذا كان تغيير السيطرة يُعامل كتنازل "
                "مفترض بموجب بند التنازل؛ فإن لم يُعالج ذلك صراحة، فقد "
                "يتجاوز تغيير السيطرة متطلبات الموافقة على التنازل بالكامل، "
                "مما يقوض الغرض منها."
            ),
        },
    },

    _pair("share_transfer_restrictions", "change_of_control"): {
        "severity": "medium",
        "insight": {
            "en": (
                "Share-transfer restrictions (right of first refusal, "
                "tag-along, drag-along) and change-of-control provisions can "
                "overlap at the holding-company level; confirm which regime "
                "governs an indirect transfer through a parent entity to "
                "avoid a gap or a double-trigger."
            ),
            "fr": (
                "Les restrictions de cession d'actions (préemption, sortie "
                "conjointe, sortie forcée) et les clauses de changement de "
                "contrôle peuvent se chevaucher au niveau de la société "
                "holding ; confirmer quel régime s'applique à un transfert "
                "indirect via une entité mère afin d'éviter une lacune ou un "
                "double déclenchement."
            ),
            "ar": (
                "قد تتداخل قيود نقل الأسهم (الأولوية في الشراء، المرافقة، "
                "الإجبار في البيع) مع أحكام تغيير السيطرة على مستوى الشركة "
                "القابضة؛ يجب تأكيد النظام الذي يحكم النقل غير المباشر عبر "
                "كيان أم لتجنب وجود فجوة أو تفعيل مزدوج."
            ),
        },
    },

    _pair("termination", "exit_transition"): {
        "severity": "medium",
        "insight": {
            "en": (
                "Termination triggers should be cross-checked against the "
                "exit/transition clause: transition assistance obligations "
                "are often conditioned on termination \"without cause\" or "
                "expiry, and may not automatically apply to termination for "
                "the other party's breach unless expressly stated."
            ),
            "fr": (
                "Les causes de résiliation doivent être recoupées avec la "
                "clause de sortie/transition : les obligations d'assistance "
                "à la transition sont souvent conditionnées à une "
                "résiliation « sans motif » ou à l'expiration, et peuvent ne "
                "pas s'appliquer automatiquement à une résiliation pour "
                "manquement de l'autre partie sauf mention expresse."
            ),
            "ar": (
                "يجب مقارنة أسباب الإنهاء ببند الخروج/الانتقال: غالباً ما "
                "تكون التزامات المساعدة الانتقالية مشروطة بالإنهاء \"دون "
                "سبب\" أو بالانقضاء، وقد لا تنطبق تلقائياً على الإنهاء "
                "بسبب إخلال الطرف الآخر ما لم يُنص على ذلك صراحة."
            ),
        },
    },

    _pair("payment", "events_of_default"): {
        "severity": "high",
        "insight": {
            "en": (
                "Confirm whether late or missed payment automatically "
                "triggers an Event of Default (with acceleration and "
                "cross-default consequences) or whether it is treated more "
                "leniently under the payment clause alone (interest, cure "
                "period); the two clauses should be consistent on this point."
            ),
            "fr": (
                "Confirmer si un retard ou défaut de paiement déclenche "
                "automatiquement un Cas de Défaut (avec exigibilité "
                "anticipée et conséquences de défaut croisé) ou s'il est "
                "traité plus souplement au titre de la seule clause de "
                "paiement (intérêts, délai de régularisation) ; les deux "
                "clauses doivent être cohérentes sur ce point."
            ),
            "ar": (
                "يجب التأكد مما إذا كان التأخر أو الإخفاق في الدفع يفعّل "
                "تلقائياً حالة تعثر (مع تسريع وآثار تعثر متبادل) أم يُعامل "
                "بمرونة أكبر بموجب بند الدفع وحده (فوائد، مهلة معالجة)؛ "
                "يجب أن يكون البندان متسقين في هذه النقطة."
            ),
        },
    },

    _pair("security_collateral", "events_of_default"): {
        "severity": "high",
        "insight": {
            "en": (
                "Enforcement of security/collateral is normally triggered "
                "by an Event of Default; confirm the default triggers are "
                "precise enough to avoid premature or disputed enforcement "
                "action against pledged assets."
            ),
            "fr": (
                "La réalisation des sûretés/garanties est normalement "
                "déclenchée par un Cas de Défaut ; confirmer que les "
                "événements de défaut sont suffisamment précis pour éviter "
                "une action d'exécution prématurée ou contestée sur les "
                "actifs nantis."
            ),
            "ar": (
                "عادة ما يُفعَّل تنفيذ الضمانات/الرهون بموجب حالة تعثر؛ "
                "يجب التأكد من أن أحداث التعثر محددة بدقة كافية لتجنب "
                "إجراء تنفيذ سابق لأوانه أو متنازع عليه على الأصول المرهونة."
            ),
        },
    },

    _pair("most_favored_nation", "pricing_adjustment"): {
        "severity": "medium",
        "insight": {
            "en": (
                "An MFN clause and a pricing-adjustment clause can interact "
                "unexpectedly: a routine index-based price increase under "
                "the adjustment clause could trigger an MFN comparison and "
                "obligation if not expressly excluded from the MFN scope."
            ),
            "fr": (
                "Une clause NPF et une clause d'ajustement tarifaire peuvent "
                "interagir de façon inattendue : une hausse de prix "
                "ordinaire fondée sur un indice au titre de la clause "
                "d'ajustement pourrait déclencher une comparaison et une "
                "obligation NPF si elle n'est pas expressément exclue du "
                "périmètre de la clause NPF."
            ),
            "ar": (
                "قد يتفاعل بند الدولة الأولى بالرعاية مع بند تعديل الأسعار "
                "بشكل غير متوقع: فزيادة سعرية روتينية قائمة على مؤشر بموجب "
                "بند التعديل قد تفعّل مقارنة والتزاماً بموجب بند الدولة "
                "الأولى بالرعاية ما لم تُستثنَ صراحة من نطاقه."
            ),
        },
    },

    _pair("governing_law", "restrictive_covenants"): {
        "severity": "medium",
        "insight": {
            "en": (
                "Enforceability of restrictive covenants (non-compete, "
                "non-solicit) varies significantly by jurisdiction; the "
                "chosen governing law should be checked against where the "
                "restricted party actually operates, since some "
                "jurisdictions will apply local mandatory rules regardless "
                "of the contractual choice of law."
            ),
            "fr": (
                "L'applicabilité des engagements restrictifs (non-"
                "concurrence, non-sollicitation) varie fortement selon la "
                "juridiction ; le droit applicable choisi doit être confronté "
                "au lieu d'exercice réel de la partie restreinte, certaines "
                "juridictions appliquant des règles impératives locales "
                "indépendamment du choix contractuel de loi."
            ),
            "ar": (
                "تختلف قابلية تنفيذ التعهدات التقييدية (عدم المنافسة، عدم "
                "الاستقطاب) اختلافاً كبيراً بحسب الولاية القضائية؛ يجب "
                "مقارنة القانون المختار بمكان ممارسة الطرف المقيد فعلياً، "
                "إذ تطبق بعض الولايات القضائية قواعد آمرة محلية بصرف النظر "
                "عن اختيار القانون التعاقدي."
            ),
        },
    },

    _pair("liability", "force_majeure"): {
        "severity": "low",
        "insight": {
            "en": (
                "Check that the liability clause does not inadvertently "
                "override the force majeure excuse (or vice versa): a "
                "delay or failure excused under force majeure should not "
                "simultaneously trigger liability exposure under a separate, "
                "broadly worded liability clause."
            ),
            "fr": (
                "Vérifier que la clause de responsabilité ne neutralise pas "
                "involontairement l'excuse de force majeure (ou "
                "inversement) : un retard ou manquement excusé par la force "
                "majeure ne devrait pas déclencher simultanément une "
                "exposition au titre d'une clause de responsabilité "
                "distincte et largement rédigée."
            ),
            "ar": (
                "يجب التحقق من أن بند المسؤولية لا يُبطل عن غير قصد عذر "
                "القوة القاهرة (أو العكس): فالتأخير أو الإخفاق المعذور "
                "بالقوة القاهرة لا ينبغي أن يفعّل في الوقت ذاته تعرضاً "
                "للمسؤولية بموجب بند مسؤولية منفصل وواسع الصياغة."
            ),
        },
    },
}


def get_clause_interactions(
    clause_types: list,
    language: str = "en",
) -> list:
    """
    Given the list of clause_type values detected in a contract, return
    the documented interactions among every pair present.

    Honest by design: if a pair has no documented interaction, nothing is
    returned for it. This function never fabricates a generic-sounding
    insight just to have something to say about every pair.
    """
    language = get_language(language)

    normalized = sorted({
        normalize_clause_type(ct)
        for ct in (clause_types or [])
        if ct
    })

    results = []
    seen_pairs = set()

    for i, a in enumerate(normalized):
        for b in normalized[i + 1:]:
            key = _pair(a, b)
            if key in seen_pairs:
                continue
            seen_pairs.add(key)

            entry = CLAUSE_INTERACTIONS.get(key)
            if not entry:
                continue

            results.append({
                "clause_types": sorted([a, b]),
                "severity": entry.get("severity", "medium"),
                "insight": entry["insight"].get(
                    language,
                    entry["insight"]["en"],
                ),
            })

    return results


# ---------------------------------------------------------------------------
# Jurisdiction caveats: general, non-binding informational notes.
# These are NOT legal advice and do not assert the state of law for any
# specific contract; they flag general considerations to verify locally.
# ---------------------------------------------------------------------------

JURISDICTION_CAVEATS = {
    "US": {
        "en": (
            "In the United States, enforceability of clauses such as "
            "non-competes, liquidated damages, and limitation of liability "
            "varies significantly by state; several states restrict or "
            "void certain restrictive covenants or penalty-like provisions."
        ),
        "fr": (
            "Aux États-Unis, l'applicabilité de clauses telles que la "
            "non-concurrence, les dommages-intérêts forfaitaires et la "
            "limitation de responsabilité varie fortement selon l'État ; "
            "plusieurs États restreignent ou annulent certains engagements "
            "restrictifs ou clauses assimilables à des pénalités."
        ),
        "ar": (
            "في الولايات المتحدة، تختلف قابلية تنفيذ بنود مثل عدم "
            "المنافسة والتعويضات المتفق عليها مسبقاً وتحديد المسؤولية "
            "اختلافاً كبيراً بحسب الولاية؛ وتقيّد عدة ولايات أو تبطل بعض "
            "التعهدات التقييدية أو الأحكام الشبيهة بالغرامات."
        ),
    },
    "UK": {
        "en": (
            "In the United Kingdom, penalty clauses may be unenforceable if "
            "they do not reflect a genuine attempt to estimate loss, and "
            "restrictive covenants are assessed for reasonableness in scope, "
            "duration, and legitimate business interest."
        ),
        "fr": (
            "Au Royaume-Uni, les clauses pénales peuvent être inapplicables "
            "si elles ne reflètent pas une tentative réelle d'estimer le "
            "préjudice, et les engagements restrictifs sont appréciés au "
            "regard de leur caractère raisonnable (portée, durée, intérêt "
            "commercial légitime)."
        ),
        "ar": (
            "في المملكة المتحدة، قد تكون بنود الغرامة غير قابلة للتنفيذ "
            "إذا لم تعكس محاولة حقيقية لتقدير الضرر، وتُقيَّم التعهدات "
            "التقييدية من حيث معقولية النطاق والمدة والمصلحة التجارية "
            "المشروعة."
        ),
    },
    "EU": {
        "en": (
            "In France and many other EU jurisdictions, excessive penalty "
            "clauses may be reduced by a judge, and consumer- or employee-"
            "protection rules can override certain contractual terms "
            "regardless of the parties' agreement."
        ),
        "fr": (
            "En France et dans de nombreuses autres juridictions de l'UE, "
            "les clauses pénales excessives peuvent être réduites par le "
            "juge, et les règles de protection des consommateurs ou des "
            "salariés peuvent primer sur certaines stipulations "
            "contractuelles indépendamment de l'accord des parties."
        ),
        "ar": (
            "في فرنسا والعديد من دول الاتحاد الأوروبي الأخرى، يجوز للقاضي "
            "تخفيض بنود الغرامة المفرطة، ويمكن لقواعد حماية المستهلك أو "
            "الموظف أن تسمو على بعض الشروط التعاقدية بصرف النظر عن اتفاق "
            "الطرفين."
        ),
    },
    "MA": {
        "en": (
            "In Morocco, contracts are generally governed by the Code des "
            "Obligations et Contrats (DOC); certain clauses affecting "
            "public order or mandatory labor and consumer protections "
            "cannot be waived by private agreement."
        ),
        "fr": (
            "Au Maroc, les contrats sont généralement régis par le Code des "
            "Obligations et Contrats (DOC) ; certaines clauses touchant à "
            "l'ordre public ou aux protections impératives du travail et du "
            "consommateur ne peuvent être écartées par convention privée."
        ),
        "ar": (
            "في المغرب، تخضع العقود عموماً لقانون الالتزامات والعقود؛ "
            "ولا يجوز الاتفاق على استبعاد بعض البنود المتعلقة بالنظام "
            "العام أو الحماية الآمرة للعمل والمستهلك."
        ),
    },
    "AE": {
        "en": (
            "In the United Arab Emirates, mainland contracts are generally "
            "subject to UAE Civil Code, while contracts within free zones "
            "such as DIFC or ADGM may instead be governed by their own "
            "common-law-based regulations; confirm which regime applies."
        ),
        "fr": (
            "Aux Émirats arabes unis, les contrats conclus sur le "
            "territoire principal sont généralement soumis au Code civil "
            "fédéral, tandis que les contrats conclus dans des zones "
            "franches telles que le DIFC ou l'ADGM peuvent relever de leurs "
            "propres réglementations de type common law ; il convient de "
            "confirmer le régime applicable."
        ),
        "ar": (
            "في الإمارات العربية المتحدة، تخضع العقود في البر الرئيسي "
            "عموماً للقانون المدني الاتحادي، بينما قد تخضع العقود في "
            "المناطق الحرة مثل مركز دبي المالي العالمي أو سوق أبوظبي "
            "العالمي لأنظمتها الخاصة القائمة على القانون العام؛ يجب تأكيد "
            "النظام المعمول به."
        ),
    },
    "SA": {
        "en": (
            "In Saudi Arabia, contracts are subject to Sharia principles and "
            "applicable regulations; interest-based (riba) terms typically "
            "require restructuring, and certain penalty or liability "
            "provisions are assessed for compatibility with those principles."
        ),
        "fr": (
            "En Arabie saoudite, les contrats sont soumis aux principes de "
            "la charia et à la réglementation applicable ; les clauses "
            "fondées sur l'intérêt (riba) nécessitent généralement une "
            "restructuration, et certaines clauses pénales ou de "
            "responsabilité sont appréciées au regard de leur compatibilité "
            "avec ces principes."
        ),
        "ar": (
            "في المملكة العربية السعودية، تخضع العقود لمبادئ الشريعة "
            "والأنظمة المعمول بها؛ وتتطلب الشروط القائمة على الفائدة "
            "(الربا) عادة إعادة هيكلة، وتُقيَّم بعض بنود الغرامة أو "
            "المسؤولية من حيث توافقها مع هذه المبادئ."
        ),
    },
}

GENERIC_JURISDICTION_CAVEAT = {
    "en": (
        "Enforceability and interpretation of contractual clauses vary by "
        "jurisdiction. This information is general in nature and does not "
        "constitute legal advice; verify specific requirements with "
        "qualified local counsel."
    ),
    "fr": (
        "L'applicabilité et l'interprétation des clauses contractuelles "
        "varient selon la juridiction. Cette information est de nature "
        "générale et ne constitue pas un avis juridique ; il convient de "
        "vérifier les exigences spécifiques auprès d'un conseil juridique "
        "local qualifié."
    ),
    "ar": (
        "تختلف قابلية تنفيذ البنود التعاقدية وتفسيرها بحسب الولاية "
        "القضائية. هذه المعلومات ذات طابع عام ولا تشكل استشارة قانونية؛ "
        "يجب التحقق من المتطلبات المحددة لدى مستشار قانوني محلي مؤهل."
    ),
}


def get_jurisdiction_caveat(jurisdiction: str, language: str = "en") -> str:
    """
    Return a general, non-binding informational caveat for a jurisdiction.

    Always returns something usable: a specific caveat for a handful of
    commonly requested jurisdictions, or a generic "verify locally"
    caveat for any other jurisdiction string (including unknown, empty,
    or misspelled ones), so this never fails regardless of input.
    """
    language = get_language(language)
    key = str(jurisdiction or "").upper().strip()

    entry = JURISDICTION_CAVEATS.get(key)
    if not entry:
        return GENERIC_JURISDICTION_CAVEAT[language]

    return entry.get(language, entry["en"])


def list_supported_jurisdictions() -> list:
    return sorted(JURISDICTION_CAVEATS.keys())
