import re
from typing import Optional


RISK_PATTERNS = {
    "high": [
        # Truly high-risk patterns: strong exposure, severe imbalance, or major control shift.
        r"\bunlimited liability\b",
        r"\bunlimited indemnit(y|ies)\b",
        r"\buncapped liability\b",
        r"\buncapped indemnif(y|ication|ies)\b",
        r"\bwithout (prior )?notice\b.*\b(terminate|termination|suspend|suspension)\b",
        r"\bterminate\b.*\bwithout (prior )?notice\b",
        r"\bsuspend\b.*\bwithout (prior )?notice\b",
        r"\bsole discretion\b.*\b(amend|modify|change|terminate|suspend)\b",
        r"\bunilateral(ly)?\b.*\b(amend|modify|change|terminate|suspend)\b",
        r"\bliquidated damages\b",
        r"\bpenalt(y|ies)\b.*\b(non[- ]payment|breach|default|delay|late)\b",
        r"\ball intellectual property\b",
        r"\bassigns? all rights\b",
        r"\bassigns? any and all rights\b",
        r"\bchange of control\b.*\blump sum\b",
        r"\bchange of control\b.*\bfully vested\b",

        r"\bresponsabilité illimitée\b",
        r"\bresponsabilité non plafonnée\b",
        r"\bindemnisation illimitée\b",
        r"\bsans préavis\b.*\b(résilier|résiliation|suspendre|suspension)\b",
        r"\b(résilier|suspendre)\b.*\bsans préavis\b",
        r"\bà sa seule discrétion\b.*\b(modifier|résilier|suspendre)\b",
        r"\bmodification unilatérale\b",
        r"\brésiliation unilatérale\b.*\bsans préavis\b",
        r"\bpénalit(é|és)\b.*\b(retard|défaut|manquement|non-paiement)\b",
        r"\bcession de tous les droits\b",
        r"\bcession de l'ensemble des droits\b",

        r"مسؤولية غير محدودة",
        r"مسؤولية غير مقيدة",
        r"تعويض غير محدود",
        r"دون إشعار.*(إنهاء|فسخ|تعليق)",
        r"(إنهاء|فسخ|تعليق).*دون إشعار",
        r"وفقًا لتقديره المطلق.*(تعديل|إنهاء|فسخ|تعليق)",
        r"تعديل.*من جانب واحد",
        r"غرامة.*(تأخير|إخلال|تقصير|عدم الدفع)",
        r"التنازل عن جميع الحقوق",
    ],
    "medium": [
        # Medium-risk signals: legally meaningful, but not automatically high.
        r"\btermination\b",
        r"\bterminate\b",
        r"\bliability\b",
        r"\bindemnif(y|ication|ies)\b",
        r"\bpayment delay\b",
        r"\blate payment\b",
        r"\bnotice period\b",
        r"\bconflict of interest\b",
        r"\barbitration\b",
        r"\bgoverning law\b",
        r"\bjurisdiction\b",
        r"\bassignment\b",
        r"\bautomatic renewal\b",
        r"\bnon[- ]compete\b",
        r"\bnon[- ]solicitation\b",
        r"\bexclusive\b",
        r"\bconfidentiality\b",
        r"\bintellectual property\b",
        r"\bdata protection\b",
        r"\bpersonal data\b",
        r"\bsecurity incident\b",
        r"\baudit\b",
        r"\binsurance\b",
        r"\bservice level\b",
        r"\buptime\b",
        r"\bservice credit\b",

        r"\brésiliation\b",
        r"\brésilier\b",
        r"\bresponsabilité\b",
        r"\bindemnisation\b",
        r"\bretard de paiement\b",
        r"\bpréavis\b",
        r"\bconflit d['’]intérêt\b",
        r"\barbitrage\b",
        r"\bdroit applicable\b",
        r"\bjuridiction\b",
        r"\bcession\b",
        r"\brenouvellement automatique\b",
        r"\bnon[- ]concurrence\b",
        r"\bnon[- ]sollicitation\b",
        r"\bexclusif\b",
        r"\bexclusivité\b",
        r"\bconfidentialité\b",
        r"\bpropriété intellectuelle\b",
        r"\bprotection des données\b",
        r"\bdonnées personnelles\b",
        r"\bincident de sécurité\b",
        r"\baudit\b",
        r"\bassurance\b",
        r"\bniveau de service\b",
        r"\bdisponibilité\b",
        r"\bcrédit de service\b",

        r"إنهاء",
        r"فسخ",
        r"مسؤولية",
        r"تعويض",
        r"تأخير الدفع",
        r"إشعار",
        r"تعارض المصالح",
        r"تضارب المصالح",
        r"تحكيم",
        r"القانون الواجب التطبيق",
        r"اختصاص",
        r"تنازل",
        r"تجديد تلقائي",
        r"عدم المنافسة",
        r"عدم الاستقطاب",
        r"حصري",
        r"الحصرية",
        r"سرية",
        r"الملكية الفكرية",
        r"حماية البيانات",
        r"البيانات الشخصية",
        r"حادث أمني",
        r"تدقيق",
        r"تأمين",
        r"مستوى الخدمة",
        r"التوافر",
        r"تعويض الخدمة",
    ],
}


LOW_RISK_PAYMENT_TERMS = {
    # Generic commercial payment terms that are not risky by themselves.
    "salary",
    "bonus",
    "benefits",
    "vacation",
    "expense reimbursement",
    "invoice",
    "fee",
    "fees",
    "payment",
    "price",
    "purchase price",
    "service fee",
    "subscription fee",
    "rent",
    "royalty",
    "commission",

    "salaire",
    "prime",
    "avantages",
    "congés",
    "remboursement de frais",
    "facture",
    "paiement",
    "prix",
    "honoraires",
    "frais",
    "loyer",
    "redevance",
    "commission",

    "راتب",
    "مكافأة",
    "مزايا",
    "إجازة",
    "تعويض المصاريف",
    "فاتورة",
    "الدفع",
    "ثمن",
    "رسوم",
    "إيجار",
    "إتاوة",
    "عمولة",
}


SIGNAL_PATTERNS = [
    r"\bindemnif(y|ication|ies)\b",
    r"\bindemnity\b",
    r"\barbitration\b",
    r"\bautomatic renewal\b",
    r"\bnon[- ]compete\b",
    r"\bnon[- ]solicitation\b",
    r"\bexclusive\b",
    r"\bliability\b",
    r"\bconfidentiality\b",
    r"\bgoverning law\b",
    r"\bjurisdiction\b",
    r"\bassignment\b",
    r"\bintellectual property\b",
    r"\bdata protection\b",
    r"\bpersonal data\b",
    r"\bsecurity incident\b",
    r"\baudit\b",
    r"\binsurance\b",
    r"\bservice level\b",
    r"\bservice credit\b",
    r"\btermination\b",

    r"\bindemnisation\b",
    r"\barbitrage\b",
    r"\brenouvellement automatique\b",
    r"\bnon[- ]concurrence\b",
    r"\bnon[- ]sollicitation\b",
    r"\bexclusif\b",
    r"\bexclusivité\b",
    r"\bresponsabilité\b",
    r"\bconfidentialité\b",
    r"\bdroit applicable\b",
    r"\bjuridiction\b",
    r"\bcession\b",
    r"\bpropriété intellectuelle\b",
    r"\bprotection des données\b",
    r"\bdonnées personnelles\b",
    r"\bincident de sécurité\b",
    r"\baudit\b",
    r"\bassurance\b",
    r"\bniveau de service\b",
    r"\bcrédit de service\b",
    r"\brésiliation\b",

    r"تعويض",
    r"تحكيم",
    r"تجديد تلقائي",
    r"عدم المنافسة",
    r"عدم الاستقطاب",
    r"حصري",
    r"الحصرية",
    r"مسؤولية",
    r"سرية",
    r"القانون الواجب التطبيق",
    r"اختصاص",
    r"تنازل",
    r"الملكية الفكرية",
    r"حماية البيانات",
    r"البيانات الشخصية",
    r"حادث أمني",
    r"تدقيق",
    r"تأمين",
    r"مستوى الخدمة",
    r"تعويض الخدمة",
    r"إنهاء",
    r"فسخ",
]


RISK_FACTOR_PATTERNS = {
    "uncapped_financial_exposure": [
        r"\bunlimited liability\b",
        r"\buncapped liability\b",
        r"\bunlimited indemn",
        r"\bresponsabilité illimitée\b",
        r"\bresponsabilité non plafonnée\b",
        r"\bindemnisation illimitée\b",
        r"مسؤولية غير محدودة",
        r"تعويض غير محدود",
    ],
    "termination_or_suspension_without_notice": [
        r"\bwithout (prior )?notice\b.*\b(terminate|termination|suspend|suspension)\b",
        r"\b(terminate|suspend)\b.*\bwithout (prior )?notice\b",
        r"\bsans préavis\b.*\b(résilier|résiliation|suspendre|suspension)\b",
        r"\b(résilier|suspendre)\b.*\bsans préavis\b",
        r"دون إشعار.*(إنهاء|فسخ|تعليق)",
        r"(إنهاء|فسخ|تعليق).*دون إشعار",
    ],
    "unilateral_control": [
        r"\bsole discretion\b.*\b(amend|modify|change|terminate|suspend)\b",
        r"\bunilateral(ly)?\b.*\b(amend|modify|change|terminate|suspend)\b",
        r"\bà sa seule discrétion\b.*\b(modifier|résilier|suspendre)\b",
        r"\bmodification unilatérale\b",
        r"وفقًا لتقديره المطلق.*(تعديل|إنهاء|فسخ|تعليق)",
        r"تعديل.*من جانب واحد",
    ],
    "broad_ip_transfer": [
        r"\ball intellectual property\b",
        r"\bassigns? all rights\b",
        r"\bassigns? any and all rights\b",
        r"\bcession de tous les droits\b",
        r"\bcession de l'ensemble des droits\b",
        r"التنازل عن جميع الحقوق",
    ],
    "penalty_or_liquidated_damages": [
        r"\bliquidated damages\b",
        r"\bpenalt(y|ies)\b.*\b(non[- ]payment|breach|default|delay|late)\b",
        r"\bpénalit(é|és)\b.*\b(retard|défaut|manquement|non-paiement)\b",
        r"غرامة.*(تأخير|إخلال|تقصير|عدم الدفع)",
    ],
}


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = str(text).lower()
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def find_trigger(text: str, patterns: list[str]) -> Optional[str]:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(0)
    return None


def find_all_signals(text: str) -> list[str]:
    signals = []

    for pattern in SIGNAL_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            signals.append(pattern)

    return signals


def detect_risk_factors(text: str) -> list[str]:
    factors = []

    for factor, patterns in RISK_FACTOR_PATTERNS.items():
        if find_trigger(text, patterns):
            factors.append(factor)

    return factors


def is_non_exclusive_context(text: str) -> bool:
    return bool(
        re.search(
            r"\bnon[- ]exclusive\b|\bnon exclusif\b|غير حصري",
            text,
            flags=re.IGNORECASE,
        )
    )


def is_low_risk_payment_context(text: str) -> bool:
    has_payment_term = any(
        term in text
        for term in LOW_RISK_PAYMENT_TERMS
    )

    if not has_payment_term:
        return False

    has_penalty = bool(
        re.search(
            r"penalt(y|ies)|late payment|interest|liquidated damages|fine|"
            r"default|non-payment|failure to pay|payment default|"
            r"breach for non-payment|"
            r"pénalit(é|és)|retard de paiement|intérêt|défaut de paiement|"
            r"غرامة|تأخير الدفع|فائدة|عدم الدفع|إخلال بالدفع",
            text,
            flags=re.IGNORECASE,
        )
    )

    return not has_penalty


def calibrate_risk_level(
    text: str,
    high_trigger: Optional[str],
    medium_trigger: Optional[str],
    risk_factors: list[str],
) -> str:
    if risk_factors:
        return "high"

    if high_trigger:
        return "high"

    if medium_trigger:
        return "medium"

    return "low"


def analyze_risk(clause: str, language: str = "en") -> dict:
    text = normalize_text(clause)

    if not text:
        return {
            "risk_level": "low",
            "trigger": None,
            "signals": [],
            "risk_factors": [],
        }

    high_trigger = find_trigger(
        text,
        RISK_PATTERNS["high"],
    )

    medium_trigger = find_trigger(
        text,
        RISK_PATTERNS["medium"],
    )

    risk_factors = detect_risk_factors(text)

    risk_level = calibrate_risk_level(
        text=text,
        high_trigger=high_trigger,
        medium_trigger=medium_trigger,
        risk_factors=risk_factors,
    )

    # Payment clauses with ordinary commercial terms should not be raised
    # unless there is a penalty, default, interest, suspension, or similar remedy.
    if is_low_risk_payment_context(text):
        if not risk_factors:
            risk_level = "low"

    # Avoid treating non-exclusive rights as exclusivity risk.
    if is_non_exclusive_context(text):
        signals = [
            pattern
            for pattern in find_all_signals(text)
            if pattern not in {
                r"\bexclusive\b",
                r"\bexclusif\b",
                r"حصري",
            }
        ]
    else:
        signals = find_all_signals(text)

    return {
        "risk_level": risk_level,
        "trigger": high_trigger or medium_trigger,
        "signals": signals,
        "risk_factors": risk_factors,
    }
