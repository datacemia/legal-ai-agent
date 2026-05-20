import re
from typing import Optional


RISK_PATTERNS = {
    "high": [
        r"\bunlimited liability\b",
        r"\bwithout (prior )?notice\b",
        r"\bsole discretion\b",
        r"\bunilateral(ly)?\b",
        r"\birrevocable\b",
        r"\bperpetual\b",
        r"\bexclusive\b",
        r"\bnon[- ]compete\b",
        r"\bliquidated damages\b",
        r"\bpenalt(y|ies)\b",
        r"\bindemnif(y|ication|ies)\b",
        r"\ball intellectual property\b",
        r"\bassigns? all rights\b",
        r"\bautomatic renewal\b",
        r"\bbinding arbitration\b",
        r"\bmandatory arbitration\b",
        r"\bexclusive arbitration\b",
        r"\bexclusively resolved by arbitration\b",
        r"\bchange of control\b.*\blump sum\b",
        r"\bchange of control\b.*\bfully vested\b",
        r"\bassigns? any and all rights\b",
        r"\birreparable injury\b",
        r"\bspecific performance\b",

        r"\bresponsabilité illimitée\b",
        r"\bsans préavis\b",
        r"\bà sa seule discrétion\b",
        r"\birrévocable\b",
        r"\bperpétuel(le)?\b",
        r"\bexclusivité\b",
        r"\bnon[- ]concurrence\b",
        r"\bpénalit(é|és)\b",
        r"\bindemnisation\b",

        r"مسؤولية غير محدودة",
        r"دون إشعار",
        r"دون إخطار",
        r"وفقًا لتقديره المطلق",
        r"غير قابل للإلغاء",
        r"دائم",
        r"حصري",
        r"عدم المنافسة",
        r"غرامة",
        r"تعويض",
        r"تحكيم إلزامي",
        r"تحكيم حصري",
        r"التجديد التلقائي",
    ],
    "medium": [
        r"\btermination\b",
        r"\bliability\b",
        r"\bconfidentiality\b",
        r"\bintellectual property\b",
        r"\bpayment delay\b",
        r"\blate payment\b",
        r"\bnotice period\b",
        r"\bgoverning law\b",
        r"\bassignment\b",
        r"\bconflict of interest\b",

        r"\brésiliation\b",
        r"\bresponsabilité\b",
        r"\bconfidentialité\b",
        r"\bpropriété intellectuelle\b",
        r"\bretard de paiement\b",
        r"\bdroit applicable\b",
        r"\bcession\b",

        r"إنهاء",
        r"فسخ",
        r"مسؤولية",
        r"سرية",
        r"الملكية الفكرية",
        r"تأخير الدفع",
        r"القانون الواجب التطبيق",
        r"التنازل",
    ],
}


LOW_RISK_PAYMENT_TERMS = {
    "salary",
    "bonus",
    "benefits",
    "vacation",
    "expense reimbursement",
}


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def find_trigger(text: str, patterns: list[str]) -> Optional[str]:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(0)
    return None


def analyze_risk(clause: str, language: str = "en") -> dict:
    text = normalize_text(clause)

    if not text:
        return {
            "risk_level": "low",
            "trigger": None,
        }

    high_trigger = find_trigger(
        text,
        RISK_PATTERNS["high"],
    )

    if high_trigger:
        return {
            "risk_level": "high",
            "trigger": high_trigger,
        }

    medium_trigger = find_trigger(
        text,
        RISK_PATTERNS["medium"],
    )

    risk_level = "low"

    if medium_trigger:
        risk_level = "medium"

    clause_type = "general"

    if any(
        term in text
        for term in LOW_RISK_PAYMENT_TERMS
    ):
        clause_type = "payment"

    has_penalty = bool(
        re.search(
            r"penalt(y|ies)|late payment|interest|liquidated damages|fine",
            text,
            flags=re.IGNORECASE,
        )
    )

    has_default_trigger = bool(
        re.search(
            r"default|non-payment|failure to pay|payment default|breach for non-payment",
            text,
            flags=re.IGNORECASE,
        )
    )

    if clause_type == "payment":
        if not has_penalty and not has_default_trigger:
            risk_level = "low"

    return {
        "risk_level": risk_level,
        "trigger": (
            high_trigger
            or medium_trigger
        ),
    }
