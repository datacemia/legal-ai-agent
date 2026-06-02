import re
from collections import defaultdict


CATEGORY_KEYWORDS = {
    "subscriptions": [
        # Specific recurring digital services
        "netflix", "spotify", "adobe", "openai", "chatgpt",
        "hostinger", "railway", "namesilo", "aws", "google",
        "youtube", "canva", "apple.com bill", "canal+",
        "deezer", "icloud", "microsoft", "office 365",

        # General subscription wording
        "subscription", "subscriptions", "premium", "recurring",
        "membership", "monthly plan", "annual plan",
        "monthly subscription", "annual subscription",
        "renewal", "auto renewal", "auto-renewal",

        # Streaming / media subscriptions
        "streaming", "music", "video", "video streaming",
        "music streaming", "streaming service",

        # French subscription wording
        "abonnement", "abonnements", "forfait", "forfaits",
        "mensuel", "annuel", "renouvellement",
        "prélèvement abonnement", "prelevement abonnement",

        # Arabic subscription wording
        "اشتراك", "اشتراكات", "شهري", "سنوي", "تجديد",
        "كارتشا", "مايكروسوفت 365", "365 تفوسوركيام",
    ],
    "housing": [
        "rent", "rental", "landlord", "mortgage", "flat",
        "apartment", "housing", "loyer", "credit logement",
        "crédit logement", "loyer appartement", "bail",
        "hypothèque", "pret immobilier", "prêt immobilier",
        "إيجار", "كراء", "سكن", "رهن",
        "راجيإ", "مكتب", "بتكم", "المكتب", "بتكملا",
    ],
    "utilities": [
        # EN
        "electricity", "water", "internet",
        "telecom", "mobile",

        # FR
        "électricité", "electricite",
        "eau", "internet",
        "télécom", "telecom",
        "facture",

        # AR
        "كهرباء", "مياه",
        "اتصالات", "إنترنت",
        "سداد",
    ],
    "government": [
        "council tax", "tax", "hmrc", "municipal", "government",
        "impot", "impôt", "taxe", "taxes", "trésor public",
        "tresor public", "dgfip", "urssaf", "amende",
        "administration", "ضرائب", "ضريبة", "حكومة",
        "زكاة", "ةاكز", "جمارك", "كرامج", "ضريبة القيمة المضافة",
        "ةفاضملا ةميقلا ةبيرض", "القيمة المضافة", "أبشر", "رشبأ", "مقيم",
        "ميقم", "منصة", "ةصنم",
    ],
    "insurance": [
        "insurance", "assurance", "assurance maladie",
        "mutuelle", "axa", "allianz", "maif", "macif",
        "aviva", "policy", "premium insurance", "تأمين",
        "نيمأت", "تأمين طبي", "يط نيمأت", "طبي", "يبط",
    ],
    "healthcare": [
        "nhs", "prescription", "pharmacy", "pharmacie",
        "doctor", "hospital", "clinic", "medical",
        "dentist", "optical", "optician", "médecin",
        "medecin", "hôpital", "hopital", "clinique",
        "santé", "sante", "دواء", "صيدلية", "طبيب",
        "مستشفى", "صحة",
    ],
    "groceries": [
        # EN
        "grocery", "groceries", "supermarket", "hypermarket", "market",

        # FR
        "épicerie", "epicerie", "supermarché", "supermarche",
        "hypermarché", "hypermarche", "alimentaire",

        # AR
        "بقالة", "تموينات", "سوبرماركت",
    ],
    "food": [
        # EN
        "restaurant", "cafe", "coffee", "food", "meal",

        # FR
        "restaurant", "café", "cafe", "brasserie",
        "boulangerie", "snack",

        # AR
        "مطعم", "مقهى", "قهوة",
    ],
    "transport": [
        # EN
        "fuel", "gas station", "petrol", "parking",
        "taxi", "uber",

        # FR
        "carburant", "essence", "station service",
        "parking", "péage", "peage", "taxi",

        # AR
        "وقود", "بنزين", "محطة وقود",
        "مواقف", "أجرة",
    ],
    "travel": [
        "air france", "ryanair", "easyjet", "british airways",
        "emirates", "qatar airways", "hotel", "booking.com",
        "airbnb", "flight", "airport", "travel", "voyage",
        "hôtel", "hotel", "avion", "billet avion", "سفر",
        "فندق", "طيران", "مطار",
    ],
    "shopping": [
        # EN
        "pos purchase", "card purchase",
        "retail", "store", "shopping",

        # FR
        "achat carte",
        "paiement carte",
        "magasin",
        "commerce",

        # AR
        "شراء عبر نقاط بيع",
        "نقاط بيع",
        "متجر",
    ],
    "education": [
        "school", "university", "college", "tuition", "course",
        "udemy", "coursera", "edx", "formation", "école",
        "ecole", "université", "universite", "cours",
        "تعليم", "مدرسة", "جامعة", "دورة",
    ],
    "childcare": [
        "nursery", "childcare", "daycare", "crèche", "creche",
        "garderie", "school fees", "frais scolaires",
        "حضانة", "أطفال",
    ],
    "pets": [
        "pet", "pets", "veterinary", "vet", "animal",
        "vétérinaire", "veterinaire", "chien", "chat",
        "حيوان", "بيطري",
    ],
    "charity": [
        "charity", "donation", "donate", "don", "association",
        "ong", "صدقة", "تبرع",
    ],
    "savings": [
        "to savings", "savings", "livret", "livret a",
        "saving account", "compte épargne", "compte epargne",
        "épargne", "epargne", "ادخار", "توفير",
    ],
    "transfers": [
        # EN
        "transfer", "bank transfer", "wire transfer",

        # FR
        "virement", "transfert",

        # AR
        "حوالة", "تحويل",
    ],
    "business_operations": [
        "wyoming", "attorney", "llc", "legal", "company",
        "formation", "accountant", "notary", "notaire",
        "business", "professional services", "محامي", "شركة",
        "استشاري", "يراشتسا", "مورد",
        "دروم", "سداد مورد", "دروم دادس", "بوابة الدفع", "عفدلا ةباوب",
        "رسوم الدفع", "عفدلا موسر", "cloud", "cloud services",
        "aws cloud services", "خدمات سحابية", "ةيباحسلا تامدخ", "سحابية",
        "ةيباحسلا",
    ],
    "fees": [
        "fee", "fees", "frais", "commission", "charge",
        "bank charge", "overdraft fee", "late fee",
        "رسوم", "عمولة",
        "موسر", "ةلومع", "رسوم بنكية", "ةيكنب موسر",
    ],
    "cash": [
        # English
        "atm",
        "cash withdrawal",
        "withdrawal",
        "cash",
        "cash machine",
        "cashpoint",
        "cash dispenser",
        "teller",
        "counter withdrawal",
        "branch withdrawal",

        # French
        "dab",
        "gab",
        "retrait",
        "retrait espèces",
        "retrait especes",
        "retrait esp",
        "retrait d'espèces",
        "retrait d especes",
        "guichet",
        "distributeur",
        "distributeur automatique",

        # Moroccan / bank OCR common generic patterns
        "awbgab",
        "esp gab",
        "retrait esp gab",
        "gab confrere",
        "gab confrère",

        # Arabic
        "سحب",
        "سحب نقدي",
        "سحب من الصراف",
        "صراف",
        "صراف آلي",
        "الصراف الآلي",
        "نقد",
        "نقدي",
        "شباك",
    ],
    "debt": [
        "loan", "credit card", "minimum payment", "repayment",
        "debt", "collections", "prêt", "pret", "crédit",
        "credit", "remboursement prêt", "remboursement pret",
        "دين", "قرض",
        "دادس", "سداد",
    ],
}


def normalize_tokens(text: str) -> set[str]:
    return {
        token
        for token in re.split(r"[^\w\u0600-\u06FF]+", text.lower())
        if token
    }


def detect_category(description: str) -> str:
    normalized = description.lower()
    tokens = normalize_tokens(normalized)

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            keyword = keyword.lower().strip()

            if not keyword:
                continue

            # Multi-word phrase
            if " " in keyword:
                if keyword in normalized:
                    return category

            # Single word/token
            elif keyword in tokens:
                return category

    return "other"


def build_financial_charts(
    transactions: list[dict],
) -> dict:
    spending_over_time = defaultdict(float)
    income_over_time = defaultdict(float)
    net_cashflow_over_time = defaultdict(float)
    category_breakdown = defaultdict(float)
    subscription_growth = defaultdict(float)

    savings_evolution = []
    running_net = 0.0

    sorted_transactions = sorted(
        transactions,
        key=lambda tx: tx.get("date") or "9999-12-31",
    )

    for tx in sorted_transactions:
        date = tx.get("date") or "unknown"
        amount = float(tx.get("amount", 0) or 0)
        description = tx.get("description", "")

        running_net += amount

        savings_evolution.append(
            {
                "date": date,
                "amount": round(running_net, 2),
            }
        )

        net_cashflow_over_time[date] += amount

        if tx.get("type") == "expense":
            expense_amount = abs(amount)
            category = detect_category(description)

            spending_over_time[date] += expense_amount

            category_breakdown[category] += expense_amount

            if category == "subscriptions":
                subscription_growth[date] += expense_amount

        elif tx.get("type") == "income":
            income_over_time[date] += amount

    total_income = round(sum(income_over_time.values()), 2)
    total_expenses = round(sum(spending_over_time.values()), 2)

    return {
        "spending_over_time": [
            {
                "date": date,
                "amount": round(amount, 2),
            }
            for date, amount in spending_over_time.items()
        ],
        "income_over_time": [
            {
                "date": date,
                "amount": round(amount, 2),
            }
            for date, amount in income_over_time.items()
        ],
        "income_vs_expenses": {
            "income": total_income,
            "expenses": total_expenses,
            "net": round(total_income - total_expenses, 2),
        },
        "category_breakdown": [
            {
                "category": category,
                "amount": round(amount, 2),
            }
            for category, amount in sorted(
                category_breakdown.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ],
        "net_cashflow_over_time": [
            {
                "date": date,
                "amount": round(amount, 2),
            }
            for date, amount in net_cashflow_over_time.items()
        ],
        "subscription_growth": [
            {
                "date": date,
                "amount": round(amount, 2),
            }
            for date, amount in subscription_growth.items()
        ],
        "savings_evolution": savings_evolution,
    }
