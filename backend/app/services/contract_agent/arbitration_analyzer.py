"""
arbitration_analyzer.py

Point 4 (Arbitration Analysis): recognizing that arbitration exists is not
enough. This module deterministically extracts the mechanics of an
arbitration clause so the reasoning engine cannot silently skip a field.

Extracted mechanics include:
- seat / place of arbitration
- institution
- arbitration rules
- governing law if stated near arbitration or generally
- language
- arbitrator count
- mandatory pre-arbitration steps
- cost allocation
- confidentiality
- emergency arbitrator
- interim measures
- consolidation
- expedited procedure
- appeal waiver / final and binding language
- court interim relief carve-out

International scope:
- English
- French
- Arabic
"""

import re
from typing import Iterable


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


INSTITUTIONS = {
    "ICC": r"\bICC\b|International Chamber of Commerce|Chambre de Commerce Internationale|غرفة التجارة الدولية",
    "LCIA": r"\bLCIA\b|London Court of International Arbitration|Cour internationale d'arbitrage de Londres",
    "AAA": r"\bAAA\b|American Arbitration Association",
    "ICDR": r"\bICDR\b|International Centre for Dispute Resolution|International Center for Dispute Resolution",
    "SIAC": r"\bSIAC\b|Singapore International Arbitration Centre|Singapore International Arbitration Center|Centre d'arbitrage international de Singapour",
    "HKIAC": r"\bHKIAC\b|Hong Kong International Arbitration Centre|Hong Kong International Arbitration Center|Centre d'arbitrage international de Hong Kong",
    "UNCITRAL": r"\bUNCITRAL\b|CNUDCI|الأونسيترال",
    "CEDR": r"\bCEDR\b|Centre for Effective Dispute Resolution",
    "JAMS": r"\bJAMS\b",
    "DIAC": r"\bDIAC\b|Dubai International Arbitration Centre|Dubai International Arbitration Center|مركز دبي للتحكيم الدولي",
    "ADCCAC": r"\bADCCAC\b|Abu Dhabi Commercial Conciliation and Arbitration Centre|Abu Dhabi Commercial Conciliation and Arbitration Center",
    "ADGM": r"\bADGM\b|Abu Dhabi Global Market",
    "DIFC-LCIA": r"\bDIFC[- ]LCIA\b|DIFC LCIA",
    "CRCICA": r"\bCRCICA\b|Cairo Regional Centre for International Commercial Arbitration|Cairo Regional Center for International Commercial Arbitration|مركز القاهرة الإقليمي للتحكيم التجاري الدولي",
    "SCC": r"\bSCC\b|Stockholm Chamber of Commerce|SCC Arbitration Institute",
    "ICSID": r"\bICSID\b|International Centre for Settlement of Investment Disputes|International Center for Settlement of Investment Disputes",
    "CIETAC": r"\bCIETAC\b|China International Economic and Trade Arbitration Commission",
    "VIAC": r"\bVIAC\b|Vienna International Arbitral Centre|Vienna International Arbitration Centre",
    "DIS": r"\bDIS\b|German Arbitration Institute|Deutsche Institution für Schiedsgerichtsbarkeit",
    "PCA": r"\bPCA\b|Permanent Court of Arbitration|Cour permanente d'arbitrage",
    "CMAC": r"\bCMAC\b|Moroccan Court of Arbitration|Cour Marocaine d'Arbitrage|المحكمة المغربية للتحكيم",
}


RULE_PATTERNS = [
    (r"ICC Rules(?: of Arbitration)?", "ICC Rules"),
    (r"LCIA Rules", "LCIA Rules"),
    (r"SIAC Rules", "SIAC Rules"),
    (r"HKIAC Rules", "HKIAC Rules"),
    (r"UNCITRAL Arbitration Rules", "UNCITRAL Arbitration Rules"),
    (r"AAA Rules", "AAA Rules"),
    (r"ICDR Rules", "ICDR Rules"),
    (r"DIAC Rules", "DIAC Rules"),
    (r"CRCICA Rules", "CRCICA Rules"),
    (r"SCC Rules", "SCC Rules"),
    (r"ICSID Convention|ICSID Rules", "ICSID Rules"),
    (r"CIETAC Rules", "CIETAC Rules"),
    (r"VIAC Rules", "VIAC Rules"),
    (r"DIS Rules", "DIS Rules"),
    (r"PCA Rules", "PCA Rules"),
    (r"règlement d'arbitrage de la CCI", "ICC Rules"),
    (r"règlement de la CCI", "ICC Rules"),
    (r"règlement d'arbitrage", "arbitration rules"),
    (r"قواعد التحكيم", "arbitration rules"),
    (r"قواعد غرفة التجارة الدولية", "ICC Rules"),
]


ARBITRATOR_COUNT_PATTERNS = [
    (r"\bsole arbitrator\b", "1 (sole arbitrator)"),
    (r"\bone\s*\(1\)\s*arbitrator\b", "1"),
    (r"\bone arbitrator\b", "1"),
    (r"\bthree\s*\(3\)\s*arbitrators\b", "3"),
    (r"\bthree arbitrators\b", "3"),
    (r"\bpanel of three\b", "3"),

    (r"\barbitre unique\b", "1 (sole arbitrator)"),
    (r"\bun\s*\(1\)\s*arbitre\b", "1"),
    (r"\bun arbitre\b", "1"),
    (r"\btrois\s*\(3\)\s*arbitres\b", "3"),
    (r"\btrois arbitres\b", "3"),

    (r"محكم منفرد", "1 (sole arbitrator)"),
    (r"محكم واحد", "1"),
    (r"محكماً واحداً", "1"),
    (r"ثلاثة محكمين", "3"),
    (r"ثلاثة\s*\(?3\)?\s*محكمين", "3"),
]


PRE_ARBITRATION_STEP_PATTERNS = [
    (r"good faith negotiation", "good-faith negotiation"),
    (r"\bmediation\b", "mediation"),
    (r"senior executives?", "escalation to senior executives"),
    (r"executive escalation", "executive escalation"),
    (r"amicable settlement", "amicable settlement"),
    (r"cooling[- ]off period", "cooling-off period"),

    (r"négociation de bonne foi", "good-faith negotiation"),
    (r"\bmédiation\b", "mediation"),
    (r"cadres dirigeants|dirigeants supérieurs", "escalation to senior executives"),
    (r"règlement amiable", "amicable settlement"),
    (r"période de réflexion", "cooling-off period"),

    (r"مفاوضات بحسن نية", "good-faith negotiation"),
    (r"الوساطة", "mediation"),
    (r"كبار المسؤولين التنفيذيين", "escalation to senior executives"),
    (r"تسوية ودية", "amicable settlement"),
    (r"فترة تهدئة", "cooling-off period"),
]


COST_PATTERNS = [
    (r"each party shall bear its own costs", "each party bears own costs"),
    (r"each party.{0,40}own (costs|fees|expenses)", "each party bears own costs"),
    (r"costs?.{0,40}shared equally", "costs shared equally"),
    (r"prevailing party", "prevailing-party fee shifting"),
    (r"losing party.{0,40}(bear|pay)", "losing-party pays"),

    (r"chaque partie supporte ses propres (frais|coûts)", "each party bears own costs"),
    (r"chaque partie.{0,40}ses propres frais", "each party bears own costs"),
    (r"(frais|coûts).{0,40}répartis? à parts égales", "costs shared equally"),
    (r"partie succombante", "losing-party pays"),

    (r"يتحمل كل طرف تكاليفه الخاصة", "each party bears own costs"),
    (r"يتحمل كل طرف.{0,30}تكاليفه", "each party bears own costs"),
    (r"تُقسم التكاليف بالتساوي", "costs shared equally"),
    (r"تقسم التكاليف بالتساوي", "costs shared equally"),
    (r"الطرف الخاسر", "losing-party pays"),
]


CONFIDENTIALITY_PATTERNS = [
    r"arbitration.{0,120}confidential",
    r"confidential.{0,120}arbitration",
    r"proceedings.{0,80}confidential",
    r"sentence arbitrale.{0,80}confidentielle",
    r"arbitrage.{0,120}confidentiel",
    r"confidentialité.{0,120}arbitrage",
    r"إجراءات التحكيم.{0,80}سرية",
    r"التحكيم.{0,120}سري",
    r"سرية.{0,120}التحكيم",
]


BOOLEAN_FEATURE_PATTERNS = {
    "emergency_arbitrator": [
        r"emergency arbitrator",
        r"emergency arbitration",
        r"arbitre d'urgence",
        r"arbitrage d'urgence",
        r"محكم الطوارئ",
        r"تحكيم طارئ",
    ],
    "interim_measures": [
        r"interim measures?",
        r"provisional measures?",
        r"conservatory measures?",
        r"injunctive relief",
        r"mesures provisoires",
        r"mesures conservatoires",
        r"référé",
        r"تدابير مؤقتة",
        r"تدابير تحفظية",
        r"أمر قضائي",
    ],
    "consolidation": [
        r"consolidat(?:e|ion)",
        r"joinder",
        r"jonction",
        r"consolidation",
        r"ضم الدعاوى",
        r"توحيد الإجراءات",
    ],
    "expedited_procedure": [
        r"expedited procedure",
        r"expedited arbitration",
        r"fast[- ]track arbitration",
        r"procédure accélérée",
        r"arbitrage accéléré",
        r"إجراءات معجلة",
        r"تحكيم معجل",
    ],
    "appeal_waiver": [
        r"final and binding",
        r"waive.{0,40}appeal",
        r"no appeal",
        r"définitive et obligatoire",
        r"renoncent.{0,40}appel",
        r"sans appel",
        r"نهائي وملزم",
        r"التنازل عن الاستئناف",
        r"غير قابل للاستئناف",
    ],
    "court_interim_relief": [
        r"court.{0,80}interim relief",
        r"court.{0,80}injunctive relief",
        r"courts?.{0,80}provisional measures",
        r"tribunal.{0,80}mesures provisoires",
        r"tribunaux.{0,80}mesures conservatoires",
        r"محكمة.{0,80}تدابير مؤقتة",
        r"القضاء.{0,80}تدابير تحفظية",
    ],
}


GOVERNING_LAW_PATTERNS = [
    r"governed by the laws of\s+([A-Za-zÀ-ÿ\s,.'-]{2,80})",
    r"laws of\s+([A-Za-zÀ-ÿ\s,.'-]{2,80})\s+shall govern",
    r"subject to the laws of\s+([A-Za-zÀ-ÿ\s,.'-]{2,80})",
    r"régi par le droit de\s+([A-Za-zÀ-ÿ\s,.'-]{2,80})",
    r"régie par le droit de\s+([A-Za-zÀ-ÿ\s,.'-]{2,80})",
    r"soumis au droit de\s+([A-Za-zÀ-ÿ\s,.'-]{2,80})",
    r"يخضع.*?لقوانين\s+([^\.\n،,؛]{2,80})",
    r"القانون الواجب التطبيق.*?(?:هو|:)\s*([^\.\n،,؛]{2,80})",
]


ARBITRATION_TRIGGER_WORDS = [
    "arbitr",
    "arbitral tribunal",
    "arbitral award",
    "binding arbitration",
    "final and binding",
    "sentence arbitrale",
    "tribunal arbitral",
    "arbitrage",
    "حكم التحكيم",
    "هيئة التحكيم",
    "التحكيم",
    "محكم",
]


def normalize_language(language: str) -> str:
    language = str(language or "en").lower().strip()
    return language if language in SUPPORTED_LANGUAGES else "en"


def clean_capture(value: str) -> str:
    value = str(value or "").strip(" .,:;،؛\n\t")
    value = re.sub(r"\s+", " ", value)

    stoppers = [
        " under ", " pursuant ", " in accordance ", " before ",
        " sauf ", " conformément ", " avant ",
        " بموجب ", " وفقاً ", " قبل ",
    ]

    lowered = value.lower()
    for stopper in stoppers:
        idx = lowered.find(stopper)
        if idx > 3:
            value = value[:idx].strip(" .,:;،؛")
            break

    return value


def _search_any(text: str, patterns: Iterable[tuple[str, str]]) -> list:
    hits = []

    for pattern, label in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            if label not in hits:
                hits.append(label)

    return hits


def _search_boolean(text: str, patterns: list[str]) -> bool:
    return any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in patterns
    )


def _extract_with_patterns(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = clean_capture(match.group(1))
            if value:
                return value
    return None


def _extract_seat(text: str) -> str | None:
    patterns = [
        r"seat of arbitration shall be\s+([A-ZÀ-Ÿ][A-Za-zÀ-ÿ,\s.'-]{2,80}?)(?:\.|,|;|\n)",
        r"seat shall be\s+([A-ZÀ-Ÿ][A-Za-zÀ-ÿ,\s.'-]{2,80}?)(?:\.|,|;|\n)",
        r"place of arbitration shall be\s+([A-ZÀ-Ÿ][A-Za-zÀ-ÿ,\s.'-]{2,80}?)(?:\.|,|;|\n)",
        r"arbitration.{0,50}(?:in|at)\s+([A-ZÀ-Ÿ][A-Za-zÀ-ÿ,\s.'-]{2,80}?)(?:\.|,|;|\n)",

        r"si[eè]ge de l['’]arbitrage (?:sera|est)\s+(?:à\s+)?([A-ZÀ-Ÿ][A-Za-zÀ-ÿ,\s.'-]{2,80}?)(?:\.|,|;|\n)",
        r"lieu de l['’]arbitrage (?:sera|est)\s+(?:à\s+)?([A-ZÀ-Ÿ][A-Za-zÀ-ÿ,\s.'-]{2,80}?)(?:\.|,|;|\n)",
        r"arbitrage.{0,50}à\s+([A-ZÀ-Ÿ][A-Za-zÀ-ÿ,\s.'-]{2,80}?)(?:\.|,|;|\n)",

        r"مقر التحكيم\s+(?:في|هو|:)\s+([\u0600-\u06FF\s،]{2,80})",
        r"مكان التحكيم\s+(?:في|هو|:)\s+([\u0600-\u06FF\s،]{2,80})",
        r"التحكيم.{0,50}في\s+([\u0600-\u06FF\s،]{2,80})",
    ]

    return _extract_with_patterns(text, patterns)


def _extract_language(text: str) -> str | None:
    patterns = [
        r"language of (?:the )?arbitration shall be\s+([A-Za-zÀ-ÿ]+)",
        r"arbitration shall be conducted in\s+([A-Za-zÀ-ÿ]+)",
        r"langue de l['’]arbitrage (?:sera|est)\s+(?:l['e]?\s*)?([A-Za-zÀ-ÿ]+)",
        r"l['’]arbitrage sera conduit en\s+([A-Za-zÀ-ÿ]+)",
        r"لغة التحكيم\s+(?:هي|ستكون|:)\s+([\u0600-\u06FF]+)",
        r"تجرى إجراءات التحكيم باللغة\s+([\u0600-\u06FF]+)",
    ]

    return _extract_with_patterns(text, patterns)


def _extract_rules(text: str) -> list[str]:
    return _search_any(text, RULE_PATTERNS)


def _extract_governing_law(text: str) -> str | None:
    return _extract_with_patterns(text, GOVERNING_LAW_PATTERNS)


def _detect_institutions(text: str) -> list[str]:
    institutions_found = [
        name
        for name, pattern in INSTITUTIONS.items()
        if re.search(pattern, text, re.IGNORECASE)
    ]

    return institutions_found or []


def _detect_confidential_proceedings(text: str) -> bool:
    return _search_boolean(text, CONFIDENTIALITY_PATTERNS)


def _detect_features(text: str) -> dict:
    return {
        key: _search_boolean(text, patterns)
        for key, patterns in BOOLEAN_FEATURE_PATTERNS.items()
    }


def has_arbitration_trigger(contract_text: str) -> bool:
    lowered = str(contract_text or "").lower()

    return any(
        trigger.lower() in lowered
        for trigger in ARBITRATION_TRIGGER_WORDS
    )


def analyze_arbitration(contract_text: str) -> dict | None:
    """
    Returns None if no arbitration clause is detected.

    Otherwise returns a dict of every mechanic found, plus a list of
    mechanics that are notably ABSENT and should not be assumed.
    """
    if not contract_text:
        return None

    if not has_arbitration_trigger(contract_text):
        return None

    arbitrator_count = None

    for pattern, label in ARBITRATOR_COUNT_PATTERNS:
        if re.search(pattern, contract_text, re.IGNORECASE):
            arbitrator_count = label
            break

    features = _detect_features(contract_text)

    result = {
        "present": True,
        "seat": _extract_seat(contract_text),
        "institution": _detect_institutions(contract_text) or None,
        "rules": _extract_rules(contract_text),
        "governing_law": _extract_governing_law(contract_text),
        "language": _extract_language(contract_text),
        "arbitrator_count": arbitrator_count,
        "pre_arbitration_steps": _search_any(
            contract_text,
            PRE_ARBITRATION_STEP_PATTERNS,
        ),
        "cost_allocation": _search_any(
            contract_text,
            COST_PATTERNS,
        ),
        "confidential_proceedings": _detect_confidential_proceedings(contract_text),
        "emergency_arbitrator": features["emergency_arbitrator"],
        "interim_measures": features["interim_measures"],
        "consolidation": features["consolidation"],
        "expedited_procedure": features["expedited_procedure"],
        "appeal_waiver": features["appeal_waiver"],
        "court_interim_relief": features["court_interim_relief"],
    }

    missing = []

    if not result["seat"]:
        missing.append("seat")

    if not result["institution"]:
        missing.append("institution")

    if not result["rules"]:
        missing.append("rules")

    if not result["governing_law"]:
        missing.append("governing_law")

    if not result["arbitrator_count"]:
        missing.append("number_of_arbitrators")

    if not result["language"]:
        missing.append("language")

    if not result["pre_arbitration_steps"]:
        missing.append("mandatory_pre_arbitration_steps")

    if not result["cost_allocation"]:
        missing.append("cost_allocation")

    result["undefined_mechanics"] = missing

    return result


def _join(values: list | None, fallback: str) -> str:
    if not values:
        return fallback
    return ", ".join(str(v) for v in values)


def build_arbitration_hint(
    analysis: dict | None,
    language: str = "en",
) -> str:
    language = normalize_language(language)

    if analysis is None:
        if language == "fr":
            return "Aucune clause d'arbitrage détectée."
        if language == "ar":
            return "لم يتم اكتشاف شرط تحكيم."
        return "No arbitration clause detected."

    if language == "fr":
        not_specified = "NON SPÉCIFIÉ DANS LE TEXTE"
        none_found = "AUCUN ÉLÉMENT TROUVÉ"

        lines = [
            "MÉCANISMES D'ARBITRAGE EXTRAITS DU TEXTE "
            "(couvrir explicitement TOUS ces éléments ; ne pas seulement indiquer qu'un arbitrage existe) :"
        ]
        lines.append(f"- Siège : {analysis.get('seat') or not_specified}")
        lines.append(f"- Institution : {_join(analysis.get('institution'), not_specified)}")
        lines.append(f"- Règles : {_join(analysis.get('rules'), not_specified)}")
        lines.append(f"- Droit applicable : {analysis.get('governing_law') or not_specified}")
        lines.append(f"- Langue : {analysis.get('language') or not_specified}")
        lines.append(f"- Nombre d'arbitres : {analysis.get('arbitrator_count') or not_specified}")
        lines.append(f"- Étapes préalables obligatoires : {_join(analysis.get('pre_arbitration_steps'), none_found)}")
        lines.append(f"- Répartition des coûts : {_join(analysis.get('cost_allocation'), not_specified)}")
        lines.append(f"- Procédure confidentielle : {'oui' if analysis.get('confidential_proceedings') else 'non indiqué'}")
        lines.append(f"- Arbitre d'urgence : {'oui' if analysis.get('emergency_arbitrator') else 'non indiqué'}")
        lines.append(f"- Mesures provisoires : {'oui' if analysis.get('interim_measures') else 'non indiqué'}")
        lines.append(f"- Consolidation / jonction : {'oui' if analysis.get('consolidation') else 'non indiqué'}")
        lines.append(f"- Procédure accélérée : {'oui' if analysis.get('expedited_procedure') else 'non indiqué'}")
        lines.append(f"- Renonciation à l'appel / sentence définitive : {'oui' if analysis.get('appeal_waiver') else 'non indiqué'}")
        lines.append(f"- Recours judiciaire provisoire : {'oui' if analysis.get('court_interim_relief') else 'non indiqué'}")

        if analysis.get("undefined_mechanics"):
            lines.append(
                "\nMécanismes NON précisés dans le texte : "
                + ", ".join(analysis["undefined_mechanics"])
                + ". Les signaler dans confidence_notes / negotiation_priorities ; "
                  "ne pas supposer par défaut une institution, un siège ou un nombre d'arbitres."
            )

        return "\n".join(lines)

    if language == "ar":
        not_specified = "غير محدد في النص"
        none_found = "لم يتم العثور على شيء"

        lines = [
            "آليات التحكيم المستخرجة من النص "
            "(يجب تغطية كل هذه العناصر صراحةً؛ لا تكتفِ بذكر وجود التحكيم):"
        ]
        lines.append(f"- المقر: {analysis.get('seat') or not_specified}")
        lines.append(f"- المؤسسة: {_join(analysis.get('institution'), not_specified)}")
        lines.append(f"- القواعد: {_join(analysis.get('rules'), not_specified)}")
        lines.append(f"- القانون الواجب التطبيق: {analysis.get('governing_law') or not_specified}")
        lines.append(f"- اللغة: {analysis.get('language') or not_specified}")
        lines.append(f"- عدد المحكمين: {analysis.get('arbitrator_count') or not_specified}")
        lines.append(f"- الخطوات السابقة للتحكيم: {_join(analysis.get('pre_arbitration_steps'), none_found)}")
        lines.append(f"- توزيع التكاليف: {_join(analysis.get('cost_allocation'), not_specified)}")
        lines.append(f"- سرية الإجراءات: {'نعم' if analysis.get('confidential_proceedings') else 'غير مذكور'}")
        lines.append(f"- محكم الطوارئ: {'نعم' if analysis.get('emergency_arbitrator') else 'غير مذكور'}")
        lines.append(f"- التدابير المؤقتة: {'نعم' if analysis.get('interim_measures') else 'غير مذكور'}")
        lines.append(f"- ضم الإجراءات: {'نعم' if analysis.get('consolidation') else 'غير مذكور'}")
        lines.append(f"- الإجراءات المعجلة: {'نعم' if analysis.get('expedited_procedure') else 'غير مذكور'}")
        lines.append(f"- التنازل عن الاستئناف / الحكم النهائي: {'نعم' if analysis.get('appeal_waiver') else 'غير مذكور'}")
        lines.append(f"- اللجوء إلى القضاء للتدابير المؤقتة: {'نعم' if analysis.get('court_interim_relief') else 'غير مذكور'}")

        if analysis.get("undefined_mechanics"):
            lines.append(
                "\nآليات غير محددة في نص العقد: "
                + ", ".join(analysis["undefined_mechanics"])
                + ". يجب إدراجها في confidence_notes / negotiation_priorities؛ "
                  "ولا يجب افتراض مؤسسة أو مقر أو عدد محكمين بشكل تلقائي."
            )

        return "\n".join(lines)

    not_specified = "NOT SPECIFIED IN TEXT"
    none_found = "NONE FOUND"

    lines = [
        "ARBITRATION MECHANICS EXTRACTED FROM TEXT "
        "(cover ALL of these explicitly; do not just note that arbitration exists):"
    ]
    lines.append(f"- Seat: {analysis.get('seat') or not_specified}")
    lines.append(f"- Institution: {_join(analysis.get('institution'), not_specified)}")
    lines.append(f"- Rules: {_join(analysis.get('rules'), not_specified)}")
    lines.append(f"- Governing law: {analysis.get('governing_law') or not_specified}")
    lines.append(f"- Language: {analysis.get('language') or not_specified}")
    lines.append(f"- Number of arbitrators: {analysis.get('arbitrator_count') or not_specified}")
    lines.append(f"- Mandatory pre-arbitration steps: {_join(analysis.get('pre_arbitration_steps'), none_found)}")
    lines.append(f"- Cost allocation: {_join(analysis.get('cost_allocation'), not_specified)}")
    lines.append(f"- Confidential proceedings: {'yes' if analysis.get('confidential_proceedings') else 'not stated'}")
    lines.append(f"- Emergency arbitrator: {'yes' if analysis.get('emergency_arbitrator') else 'not stated'}")
    lines.append(f"- Interim measures: {'yes' if analysis.get('interim_measures') else 'not stated'}")
    lines.append(f"- Consolidation / joinder: {'yes' if analysis.get('consolidation') else 'not stated'}")
    lines.append(f"- Expedited procedure: {'yes' if analysis.get('expedited_procedure') else 'not stated'}")
    lines.append(f"- Appeal waiver / final award: {'yes' if analysis.get('appeal_waiver') else 'not stated'}")
    lines.append(f"- Court interim relief carve-out: {'yes' if analysis.get('court_interim_relief') else 'not stated'}")

    if analysis.get("undefined_mechanics"):
        lines.append(
            "\nMechanics NOT specified in the contract text: "
            + ", ".join(analysis["undefined_mechanics"])
            + ". Report these as confidence_notes / negotiation_priorities gaps — "
              "do not assume a default institution, seat, rules, or arbitrator count."
        )

    return "\n".join(lines)
