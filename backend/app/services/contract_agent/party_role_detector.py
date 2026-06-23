ROLE_LABELS = {
    "generic": {
        "en": ("Party A", "Party B"),
        "fr": ("Partie A", "Partie B"),
        "ar": ("الطرف أ", "الطرف ب"),
    },
    "employment": {
        "en": ("Employer", "Employee"),
        "fr": ("Employeur", "Salarié"),
        "ar": ("صاحب العمل", "الموظف"),
    },
    "services": {
        "en": ("Client", "Service Provider"),
        "fr": ("Client", "Prestataire"),
        "ar": ("العميل", "مقدم الخدمة"),
    },
    "sale": {
        "en": ("Buyer", "Seller"),
        "fr": ("Acheteur", "Vendeur"),
        "ar": ("المشتري", "البائع"),
    },
    "lease": {
        "en": ("Lessor", "Lessee"),
        "fr": ("Bailleur", "Locataire"),
        "ar": ("المؤجر", "المستأجر"),
    },
    "loan": {
        "en": ("Lender", "Borrower"),
        "fr": ("Prêteur", "Emprunteur"),
        "ar": ("المقرض", "المقترض"),
    },
    "license": {
        "en": ("Licensor", "Licensee"),
        "fr": ("Concédant", "Licencié"),
        "ar": ("المرخِّص", "المرخَّص له"),
    },
    "nda": {
        "en": ("Disclosing Party", "Receiving Party"),
        "fr": ("Partie divulgatrice", "Partie réceptrice"),
        "ar": ("الطرف المفصح", "الطرف المتلقي"),
    },
}


FR_REPLACEMENTS = {
    "de la Partie contractante A": "du Client",
    "à la Partie contractante A": "au Client",
    "la Partie contractante A": "le Client",
    "La Partie contractante A": "Le Client",

    "de la Partie contractante B": "du Prestataire",
    "à la Partie contractante B": "au Prestataire",
    "la Partie contractante B": "le Prestataire",
    "La Partie contractante B": "Le Prestataire",

    "Partie contractante A": "Client",
    "Partie contractante B": "Prestataire",
}


POST_FR_FIXES = {
    "de le Client": "du Client",
    "à le Client": "au Client",

    "de le Prestataire": "du Prestataire",
    "à le Prestataire": "au Prestataire",
}


def strip_role_articles(label: str, language: str = "en") -> str:
    value = str(label or "").strip()

    if language == "fr":
        prefixes = [
            "le ", "la ", "l’", "l'",
            "Le ", "La ", "L’", "L'",
        ]

        for prefix in prefixes:
            if value.startswith(prefix):
                return value[len(prefix):].strip()

    if language == "en":
        prefixes = ["the ", "The "]

        for prefix in prefixes:
            if value.startswith(prefix):
                return value[len(prefix):].strip()

    if language == "ar":
        return value

    return value


def detect_role_family(contract_type: str = "", text: str = "") -> str:
    combined = f"{contract_type or ''} {text or ''}".lower()

    if any(x in combined for x in ["employment", "employee", "employer", "salarié", "employeur", "travail"]):
        return "employment"

    if any(x in combined for x in ["service", "services", "prestataire", "consulting", "consultant"]):
        return "services"

    if any(x in combined for x in ["sale", "purchase", "buyer", "seller", "vente", "achat"]):
        return "sale"

    if any(x in combined for x in ["lease", "tenant", "landlord", "bail", "locataire", "bailleur"]):
        return "lease"

    if any(x in combined for x in ["loan", "lender", "borrower", "prêt", "emprunteur", "مقترض"]):
        return "loan"

    if any(x in combined for x in ["license", "licence", "licensor", "licensee"]):
        return "license"

    if any(x in combined for x in ["nda", "non-disclosure", "confidentiality agreement", "accord de confidentialité"]):
        return "nda"

    return "generic"


def get_display_roles(contract_type: str = "", text: str = "", language: str = "en") -> dict:
    if language not in ["en", "fr", "ar"]:
        language = "en"

    family = detect_role_family(contract_type, text)
    party_a, party_b = ROLE_LABELS.get(family, ROLE_LABELS["generic"])[language]

    return {
        "party_a": party_a,
        "party_b": party_b,
        "family": family,
    }


def apply_display_roles(value, roles: dict, language: str = "en"):
    if isinstance(value, list):
        return [apply_display_roles(v, roles, language) for v in value]

    if isinstance(value, dict):
        return {k: apply_display_roles(v, roles, language) for k, v in value.items()}

    if not isinstance(value, str):
        return value

    a = roles.get("party_a", "Party A")
    b = roles.get("party_b", "Party B")

    replacements = {
        "en": {
            "Contracting Party A": a,
            "Contracting Party B": b,
            "Party A": a,
            "Party B": b,
        },
        "fr": {
            "Partie A": a,
            "Partie B": b,
        },
        "ar": {
            "الطرف المتعاقد أ": a,
            "الطرف المتعاقد ب": b,
            "الطرف أ": a,
            "الطرف ب": b,
        },
    }

    output = value

    if language == "fr":
        for old, new in sorted(
            FR_REPLACEMENTS.items(),
            key=lambda x: len(x[0]),
            reverse=True,
        ):
            output = output.replace(old, new)

        for old, new in replacements["fr"].items():
            output = output.replace(old, new)

        for old, new in POST_FR_FIXES.items():
            output = output.replace(old, new)

        return output

    for old, new in replacements.get(language, replacements["en"]).items():
        output = output.replace(old, new)

    return output
