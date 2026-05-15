JURISDICTION_RULES = {

    "france": {
        "signals": [
            "droit français",
            "code du travail",
            "tribunal de paris",
            "france",
            "code civil",
        ],
        "legal_system": "civil_law",
        "languages": ["fr", "en"],
        "notes": [
            "French labor law is protective of employees.",
            "Non-compete clauses are strictly regulated.",
            "Consumer protections are relatively strong.",
        ],
    },

    "morocco": {
        "signals": [
            "droit marocain",
            "royaume du maroc",
            "maroc",
            "tribunal de casablanca",
            "القانون المغربي",
        ],
        "legal_system": "civil_law",
        "languages": ["fr", "ar"],
        "notes": [
            "Moroccan contracts often combine French and Arabic legal terminology.",
            "Commercial contracts frequently rely on French civil law concepts.",
        ],
    },

    "uae": {
        "signals": [
            "uae",
            "united arab emirates",
            "dubai",
            "abu dhabi",
            "difc",
            "adgm",
            "الإمارات",
        ],
        "legal_system": "mixed",
        "languages": ["en", "ar"],
        "notes": [
            "UAE contracts may involve DIFC or ADGM common law frameworks.",
            "Employment and commercial laws vary across jurisdictions.",
        ],
    },

    "usa": {
        "signals": [
            "united states",
            "state of california",
            "new york",
            "delaware",
            "u.s.",
        ],
        "legal_system": "common_law",
        "languages": ["en"],
        "notes": [
            "US contract enforceability varies by state.",
            "Limitation of liability clauses are common in SaaS agreements.",
        ],
    },

    "uk": {
        "signals": [
            "england and wales",
            "united kingdom",
            "london court",
            "uk law",
        ],
        "legal_system": "common_law",
        "languages": ["en"],
        "notes": [
            "UK contracts frequently use detailed indemnity structures.",
            "English law is common in international commercial agreements.",
        ],
    },

}
def detect_jurisdiction(text: str) -> dict:

    normalized = str(text or "").lower()

    best_match = None
    best_score = 0

    for jurisdiction, config in JURISDICTION_RULES.items():

        score = 0

        for signal in config.get("signals", []):

            if signal.lower() in normalized:
                score += 1

        if score > best_score:
            best_score = score
            best_match = jurisdiction

    if not best_match:
        return {
            "name": "generic",
            "legal_system": "unknown",
            "languages": [],
            "notes": [],
        }

    config = JURISDICTION_RULES[best_match]

    return {
        "name": best_match,
        "legal_system": config.get("legal_system"),
        "languages": config.get("languages", []),
        "notes": config.get("notes", []),
    }