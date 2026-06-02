from collections import defaultdict


CATEGORY_KEYWORDS = {
    "subscriptions": [
        "netflix", "spotify", "adobe", "openai", "chatgpt",
        "hostinger", "railway", "namesilo", "aws", "google",
        "youtube", "canva", "apple.com bill", "subscription",
        "premium", "recurring", "abonnement", "abonnements",
        "canal+", "deezer", "icloud", "microsoft", "office 365",
        "اشتراك", "اشتراكات",
    ],
    "housing": [
        "rent", "rental", "landlord", "mortgage", "flat",
        "apartment", "housing", "loyer", "credit logement",
        "crédit logement", "loyer appartement", "bail",
        "hypothèque", "pret immobilier", "prêt immobilier",
        "إيجار", "كراء", "سكن", "رهن",
    ],
    "utilities": [
        "water", "electricity", "internet", "telecom", "orange",
        "inwi", "maroc telecom", "gas", "british gas",
        "thames water", "edf", "sfr", "fiber", "fibre",
        "utility", "utilities", "free mobile", "engie",
        "engie gaz", "bpay electricity", "eau", "électricité",
        "electricite", "gaz", "wifi", "mobile", "phone",
        "téléphone", "telephone", "فواتير", "كهرباء", "ماء",
        "غاز", "إنترنت", "هاتف",
    ],
    "government": [
        "council tax", "tax", "hmrc", "municipal", "government",
        "impot", "impôt", "taxe", "taxes", "trésor public",
        "tresor public", "dgfip", "urssaf", "amende",
        "administration", "ضرائب", "ضريبة", "حكومة",
    ],
    "insurance": [
        "insurance", "assurance", "assurance maladie",
        "mutuelle", "axa", "allianz", "maif", "macif",
        "aviva", "policy", "premium insurance", "تأمين",
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
        "tesco", "sainsburys", "sainsbury", "carrefour",
        "lidl", "aldi", "monoprix", "intermarche",
        "intermarché", "supermarket", "grocery", "groceries",
        "carrefour city", "marché local", "marche local",
        "épicerie", "epicerie", "supermarché", "supermarche",
        "asda", "morrisons", "waitrose", "auchan", "casino",
        "bim", "marjane", "aswak", "بقالة", "سوبرماركت",
    ],
    "food": [
        "restaurant", "cafe", "coffee", "glovo", "uber eats",
        "deliveroo", "just eat", "pret", "pret a manger",
        "costa", "mcdonald", "kfc", "burger", "pizza",
        "pub", "bar", "food", "order", "boulangerie",
        "bistrot", "café", "cafe terrasse", "bakery",
        "takeaway", "meal", "snack", "مطعم", "قهوة",
        "مقهى", "طعام", "وجبة",
    ],
    "transport": [
        "uber trip", "taxi", "careem", "fuel", "train",
        "rail", "national rail", "trainline", "tfl",
        "contactless london", "transport", "sncf", "sncf connect",
        "péage", "peage", "vinci", "bus", "metro", "métro",
        "tram", "parking", "essence", "diesel", "carburant",
        "shell", "bp", "totalenergies", "نقل", "وقود",
        "قطار", "تاكسي",
    ],
    "travel": [
        "air france", "ryanair", "easyjet", "british airways",
        "emirates", "qatar airways", "hotel", "booking.com",
        "airbnb", "flight", "airport", "travel", "voyage",
        "hôtel", "hotel", "avion", "billet avion", "سفر",
        "فندق", "طيران", "مطار",
    ],
    "shopping": [
        "amazon", "shein", "zara", "mall", "shop", "store",
        "marketplace", "paypal payment", "paypal", "card purchase",
        "retail", "electronics", "jb hi-fi", "jbhifi",
        "fnac", "décathlon", "decathlon", "boulanger",
        "darty", "ikea", "apple store", "google store",
        "achat", "achats", "boutique", "magasin", "تسوق",
        "متجر", "شراء",
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
        "own account", "internal transfer",
        "transfer between accounts", "virement interne",
        "transfer", "osko transfer", "bank transfer",
        "wise transfer", "faster payment", "virement",
        "virement famille", "virement reçu", "virement recu",
        "remboursement ami", "transfer received",
        "payment from", "payment to", "حوالة", "تحويل",
    ],
    "business_services": [
        "wyoming", "attorney", "llc", "legal", "company",
        "formation", "accountant", "notary", "notaire",
        "business", "professional services", "محامي", "شركة",
    ],
    "fees": [
        "fee", "fees", "frais", "commission", "charge",
        "bank charge", "overdraft fee", "late fee",
        "رسوم", "عمولة",
    ],
    "cash": [
        "atm", "cash withdrawal", "withdrawal", "dab",
        "retrait", "retrait espèces", "retrait especes",
        "guichet", "سحب", "نقد",
    ],
    "debt": [
        "loan", "credit card", "minimum payment", "repayment",
        "debt", "collections", "prêt", "pret", "crédit",
        "credit", "remboursement prêt", "remboursement pret",
        "دين", "قرض",
    ],
}


def detect_category(description: str) -> str:
    normalized = description.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
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
