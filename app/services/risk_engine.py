RISK_KEYWORDS = {
    "en": {
        "high": [
            "penalty",
            "liquidated damages",
            "indemnify",
            "indemnification",
            "exclusive",
            "non-compete",
            "non compete",
            "irrevocable",
            "perpetual",
            "all intellectual property",
            "without notice"
        ],
        "medium": [
            "termination",
            "liability",
            "confidentiality",
            "intellectual property",
            "payment delay"
        ]
    },
    "fr": {
        "high": [
            "pénalité",
            "dommages",
            "indemniser",
            "exclusivité",
            "non-concurrence"
        ],
        "medium": [
            "résiliation",
            "responsabilité",
            "confidentialité"
        ]
    },
    "ar": {
        "high": [
            "غرامة",
            "تعويض",
            "حصري",
            "عدم المنافسة"
        ],
        "medium": [
            "إنهاء",
            "مسؤولية",
            "سرية"
        ]
    }
}


def analyze_risk(clause: str, language: str = "en") -> dict:
    clause_lower = clause.lower()

    keywords = RISK_KEYWORDS.get(language, RISK_KEYWORDS["en"])

    for word in keywords["high"]:
        if word in clause_lower:
            return {
                "risk_level": "high",
                "trigger": word
            }

    for word in keywords["medium"]:
        if word in clause_lower:
            return {
                "risk_level": "medium",
                "trigger": word
            }

    return {
        "risk_level": "low",
        "trigger": None
    }