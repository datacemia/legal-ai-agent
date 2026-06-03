"""
Runexa Financial Categorization Engine
International standard taxonomy - English / French / Arabic

Goals:
- Reduce "other" by using a layered classifier.
- Keep categories stable and internationally understandable.
- Work with noisy bank PDF/OCR descriptions in EN/FR/AR.
- Avoid mixing transfers, debt, fees, taxes and real consumption.

Public functions kept compatible with previous code:
- detect_category(description: str) -> str
- build_financial_charts(transactions: list[dict]) -> dict
"""

import re
import unicodedata
from collections import defaultdict
from typing import Any


CATEGORY_LABELS = {
    "income": {"en": "Income", "fr": "Revenus", "ar": "الدخل"},
    "housing": {"en": "Housing", "fr": "Logement", "ar": "السكن"},
    "utilities": {"en": "Utilities", "fr": "Services", "ar": "الخدمات"},
    "groceries": {"en": "Groceries", "fr": "Courses", "ar": "البقالة والتموين"},
    "food_dining": {"en": "Food & Dining", "fr": "Restaurants & cafés", "ar": "المطاعم والمقاهي"},
    "transport": {"en": "Transport", "fr": "Transport", "ar": "النقل"},
    "travel": {"en": "Travel", "fr": "Voyage", "ar": "السفر"},
    "shopping": {"en": "Shopping", "fr": "Achats", "ar": "التسوق"},
    "healthcare": {"en": "Healthcare", "fr": "Santé", "ar": "الصحة"},
    "insurance": {"en": "Insurance", "fr": "Assurance", "ar": "التأمين"},
    "education": {"en": "Education", "fr": "Éducation", "ar": "التعليم"},
    "childcare": {"en": "Childcare", "fr": "Garde d'enfants", "ar": "رعاية الأطفال"},
    "pets": {"en": "Pets", "fr": "Animaux", "ar": "الحيوانات الأليفة"},
    "government_taxes": {"en": "Government & Taxes", "fr": "Gouvernement & taxes", "ar": "الجهات الحكومية والضرائب"},
    "debt_loans": {"en": "Debt & Loans", "fr": "Dettes & prêts", "ar": "القروض والديون"},
    "transfers": {"en": "Transfers", "fr": "Virements", "ar": "التحويلات"},
    "savings_investments": {"en": "Savings & Investments", "fr": "Épargne & investissements", "ar": "الادخار والاستثمار"},
    "subscriptions": {"en": "Subscriptions", "fr": "Abonnements", "ar": "الاشتراكات"},
    "business_operations": {"en": "Business Expenses", "fr": "Dépenses professionnelles", "ar": "مصاريف الأعمال"},
    "fees": {"en": "Bank Fees", "fr": "Frais bancaires", "ar": "الرسوم البنكية"},
    "cash": {"en": "Cash Withdrawal", "fr": "Retrait espèces", "ar": "السحب النقدي"},
    "charity": {"en": "Charity & Donations", "fr": "Dons", "ar": "التبرعات والزكاة"},
    "other": {"en": "Other", "fr": "Autres", "ar": "أخرى"},
}


CATEGORY_ALIASES = {
    "food": "food_dining",
    "government": "government_taxes",
    "debt": "debt_loans",
    "savings": "savings_investments",
}


CATEGORY_PRIORITY = [
    "income",
    "debt_loans",
    "savings_investments",
    "transfers",
    "fees",
    "government_taxes",
    "utilities",
    "subscriptions",
    "insurance",
    "healthcare",
    "groceries",
    "food_dining",
    "transport",
    "travel",
    "housing",
    "education",
    "childcare",
    "pets",
    "charity",
    "business_operations",
    "cash",
    "shopping",
]


CATEGORY_KEYWORDS = {
    "income": [
        "salary", "payroll", "wage", "income", "deposit salary", "employer", "bonus",
        "transfer - credit", "salary transfer", "salary transfer cdd",
        "salaire", "paie", "revenu", "virement salaire", "rémunération", "remuneration",
        "راتب", "رواتب", "ايداع رواتب", "إيداع رواتب", "دخل", "مكافأة", "مكافاه", "بدل",
        "/payroll/", "samasari",
    ],
    "housing": [
        "rent", "rental", "landlord", "mortgage", "flat", "apartment", "housing", "property",
        "loyer", "bail", "logement", "appartement", "crédit logement", "credit logement",
        "hypothèque", "hypotheque", "prêt immobilier", "pret immobilier",
        "إيجار", "ايجار", "كراء", "سكن", "رهن", "عقار", "شقة", "شقه",
        "راجيإ", "بتكملا", "المكتب",
    ],
    "utilities": [
        "electricity", "water", "internet", "telecom", "mobile", "phone", "broadband", "gas bill",
        "utility", "utilities", "bill payment", "sadad",
        "électricité", "electricite", "eau", "internet", "télécom", "telecom", "mobile",
        "facture", "factures", "gaz", "sfr", "orange", "free mobile", "bouygues",
        "كهرباء", "الكهرباء", "مياه", "المياه", "اتصالات", "الاتصالات", "إنترنت", "انترنت",
        "الجوال", "الهاتف", "فاتورة", "مدفوعات سداد", "شركة المياه", "شركه المياه",
        "اتصالات السعوديه", "الاتصالات السعودية", "stc", "zain", "mobily",
    ],
    "groceries": [
        "grocery", "groceries", "supermarket", "hypermarket", "market", "mart", "mini market",
        "carrefour", "lidl", "aldi", "tesco", "sainsbury", "asda", "walmart", "costco",
        "al meera", "meera", "lulu", "danube",
        "épicerie", "epicerie", "supermarché", "supermarche", "hypermarché", "hypermarche",
        "alimentaire", "auchan", "leclerc", "intermarché", "intermarche", "monoprix", "casino",
        "بقالة", "بقاله", "تموينات", "سوبرماركت", "سوبر ماركت", "تموين", "ماركت", "هايبر",
        "الدانو", "الدانوب", "بنده", "باندا", "كارفور", "العثيم", "لولو", "تموينات السابله",
        "مون مارت", "moon mart",
    ],
    "food_dining": [
        "restaurant", "cafe", "coffee", "food", "meal", "dining", "fast food", "pizza", "burger",
        "mcdonald", "burger king", "kfc", "subway", "starbucks", "costa", "dunkin", "shawarma",
        "talabat", "tea time",
        "café", "brasserie", "boulangerie", "snack", "repas", "resto",
        "مطعم", "مطاعم", "مقهى", "مقهي", "قهوة", "قهوه", "وجبات", "بروست", "شاورما",
        "شاورمر", "ماكدونالدز", "ستاربكس", "باسكن روبنز", "الوجبات", "مدينه النعناع",
        "شركة الوجبات", "شركه الوجبات", "بروست ساره", "كافيه",
    ],
    "transport": [
        "fuel", "gas station", "petrol", "parking", "taxi", "uber", "bolt", "lyft", "careem",
        "train", "metro", "bus", "toll", "car wash", "vehicle", "auto repair", "garage", "mechanic",
        "woqod", "qatar fuel",
        "carburant", "essence", "station service", "parking", "péage", "peage", "taxi", "garage",
        "وقود", "بنزين", "محطة وقود", "محطه وقود", "محطه نفط", "محطة نفط", "مواقف",
        "أجرة", "اجرة", "سيارات", "سياره", "كريم", "اوبر", "بترول", "نفط", "ورشه", "ورشة",
        "شركة بترول", "شركه بترول", "محطه", "محطة",
    ],
    "travel": [
        "air france", "ryanair", "easyjet", "british airways", "emirates", "qatar airways",
        "saudia", "flynas", "hotel", "booking.com", "airbnb", "flight", "airport", "travel",
        "trip", "airline", "resort", "hostel", "visa application",
        "voyage", "hôtel", "hotel", "avion", "billet avion", "aéroport", "aeroport", "vacances",
        "سفر", "مصاريف سفر", "فندق", "طيران", "مطار", "رحلة", "رحله", "حجز", "الخطوط", "فلاي ناس",
        "فندق اطياف",
    ],
    "shopping": [
        "naps purchase", "cbq purchase", "electron auth", "pos purchase", "card purchase",
        "retail", "store", "shopping", "shop", "mall", "fashion", "clothes", "clothing",
        "electronics", "amazon", "aliexpress", "shein", "temu", "ikea",
        "achat carte", "paiement carte", "magasin", "commerce", "boutique", "mode", "vêtements", "vetements",
        "شراء عبر نقاط بيع", "نقاط بيع", "شراء", "متجر", "محل", "مول", "تسوق", "الكترونيات", "ملابس",
    ],
    "healthcare": [
        "nhs", "prescription", "pharmacy", "doctor", "hospital", "clinic", "medical", "dentist",
        "optical", "optician", "health", "laboratory", "lab test",
        "pharmacie", "médecin", "medecin", "hôpital", "hopital", "clinique", "santé", "sante",
        "dentiste", "optique", "laboratoire",
        "دواء", "صيدلية", "صيدليات", "طبيب", "مستشفى", "مستشفي", "صحة", "صحه", "مختبر",
        "زهره", "زهرة", "صيدليات زهره", "صيدليات زهرة",
    ],
    "insurance": [
        "insurance", "assurance", "policy", "premium insurance", "mutual", "axa", "allianz", "maif",
        "macif", "aviva", "geico", "state farm", "progressive",
        "assurance maladie", "mutuelle", "cotisation assurance",
        "تأمين", "تامين", "نيمأت", "تأمين طبي", "تامين طبي", "طبي", "يبط",
    ],
    "education": [
        "school", "university", "college", "tuition", "course", "udemy", "coursera", "edx",
        "training", "academy", "bookstore", "stationery",
        "formation", "école", "ecole", "université", "universite", "cours", "frais scolaires",
        "تعليم", "مدرسة", "مدرسه", "جامعة", "جامعه", "دورة", "دوره", "تدريب", "قرطاسية", "قرطاسيه",
    ],
    "childcare": [
        "nursery", "childcare", "daycare", "creche", "crèche", "garderie", "school fees",
        "حضانة", "حضانه", "أطفال", "اطفال", "روضة", "روضه",
    ],
    "pets": [
        "pet", "pets", "veterinary", "vet", "animal", "dog", "cat", "petshop",
        "vétérinaire", "veterinaire", "chien", "chat", "animalerie",
        "حيوان", "حيوانات", "بيطري", "قطط", "كلاب",
    ],
    "government_taxes": [
        "council tax", "tax", "hmrc", "municipal", "government", "customs", "fine", "traffic fine",
        "vat", "value added tax", "administration",
        "impot", "impôt", "taxe", "taxes", "trésor public", "tresor public", "dgfip", "urssaf", "amende",
        "administration", "douane", "tva",
        "ضرائب", "ضريبة", "حكومة", "حكومي", "زكاة", "زكاه", "جمارك", "ضريبة القيمة المضافة",
        "القيمة المضافة", "أبشر", "ابشر", "مقيم", "منصة", "المخالفات", "المخالفات المروريه",
        "المخالفات المرورية", "مرور", "غرامة", "غرامه", "ضريبه القيمه المضافه",
        "ةفاضملا ةميقلا ةبيرض", "ةاكز", "كرامج", "رشبأ", "ميقم", "ةصنم",
    ],
    "debt_loans": [
        "loan", "credit card", "minimum payment", "repayment", "debt", "collections", "installment",
        "personal loan", "mortgage payment", "finance payment", "loan repayment", "loan repayment - princ",
        "card bill payment",
        "prêt", "pret", "crédit", "credit", "remboursement prêt", "remboursement pret", "mensualité",
        "دين", "قرض", "تمويل", "قسط", "اقساط", "أقساط", "سداد قرض", "خصم قسط", "قرض شخصي",
        "نمطم طلسهلي", "للمقفونطع",
    ],
    "transfers": [
        "transfer", "bank transfer", "wire transfer", "instant transfer", "internal transfer", "external transfer",
        "remittance", "p2p", "family transfer", "friends", "beneficiary", "thirdparty transfer", "funds transfer",
        "virement", "transfert", "versement", "bénéficiaire", "beneficiaire", "virement instantané",
        "حوالة", "حواله", "تحويل", "تحويلات", "حواله فوريه", "حوالة فورية", "محليه صادره",
        "محلية صادرة", "تحويل لافراد الاسره", "تحويل الي الاهل", "الأهل والأصدقاء", "الاهل والاصدقاء",
        "benbk", "rembk",
    ],
    "savings_investments": [
        "to savings", "savings", "saving account", "investment", "brokerage", "stock", "stocks", "etf",
        "mutual fund", "pension", "retirement", "crypto", "coinbase", "binance", "trading",
        "livret", "livret a", "compte épargne", "compte epargne", "épargne", "epargne", "placement",
        "bourse", "investissement", "retraite",
        "ادخار", "توفير", "استثمار", "استثمارات", "محفظة", "محفظه", "أسهم", "اسهم", "تداول", "تقاعد",
    ],
    "subscriptions": [
        "netflix", "spotify", "adobe", "openai", "chatgpt", "hostinger", "railway", "namesilo",
        "aws", "google", "youtube", "canva", "apple.com bill", "apple.com/bill", "apple.com",
        "itunes", "canal+", "deezer", "icloud", "microsoft", "office 365", "dropbox", "notion", "github",
        "figma", "zoom", "slack",
        "subscription", "subscriptions", "premium", "recurring", "membership", "monthly plan", "annual plan",
        "monthly subscription", "annual subscription", "renewal", "auto renewal", "auto-renewal",
        "streaming", "music streaming", "video streaming", "saas",
        "abonnement", "abonnements", "forfait", "forfaits", "mensuel", "annuel", "renouvellement",
        "prélèvement abonnement", "prelevement abonnement",
        "اشتراك", "اشتراكات", "شهري", "سنوي", "تجديد", "عضوية", "عضويه",
        "كارتشا", "مايكروسوفت 365", "365 تفوسوركيام",
    ],
    "business_operations": [
        "wyoming", "attorney", "llc", "legal", "company", "accountant", "notary", "business",
        "professional services", "supplier", "vendor", "invoice", "cloud services", "aws cloud services",
        "notaire", "entreprise", "société", "societe", "comptable", "fournisseur", "facturation",
        "محامي", "شركة", "شركه", "استشاري", "مورد", "فاتورة مورد", "بوابة الدفع", "رسوم الدفع",
        "خدمات سحابية", "سحابية", "يراشتسا", "دروم", "دادس مورد", "دروم دادس", "عفدلا ةباوب",
        "عفدلا موسر", "ةيباحسلا تامدخ", "ةيباحسلا",
    ],
    "fees": [
        "fee", "fees", "bank fee", "bank charge", "commission", "charge", "overdraft fee", "late fee",
        "service charge", "transfer fee", "atm fee", "transfer charge",
        "frais", "commission", "frais bancaires", "frais de tenue", "frais virement",
        "رسوم", "عمولة", "عموله", "رسوم بنكية", "رسوم تحويل", "خصم ضريبه", "عكس رسوم",
        "موسر", "ةلومع", "ةيكنب موسر",
    ],
    "cash": [
        "naps atm", "atm", "cash withdrawal", "withdrawal", "cash", "cash machine", "cashpoint", "cash dispenser",
        "teller", "counter withdrawal", "branch withdrawal",
        "dab", "gab", "retrait", "retrait espèces", "retrait especes", "retrait esp",
        "retrait d'espèces", "retrait d especes", "guichet", "distributeur", "distributeur automatique",
        "awbgab", "esp gab", "retrait esp gab", "gab confrere", "gab confrère",
        "سحب", "سحب نقدي", "سحب من الصراف", "صراف", "صراف آلي", "الصراف الآلي", "نقد", "نقدي", "شباك",
    ],
    "charity": [
        "charity", "donation", "donate", "nonprofit", "ngo", "zakat", "waqf",
        "don", "association", "ong", "caritatif",
        "صدقة", "صدقه", "تبرع", "تبرعات", "زكاة", "زكاه", "وقف", "جمعية", "جمعيه",
    ],
}


MERCHANT_CATEGORY_OVERRIDES = {
    "talabat": "food_dining",
    "tea time": "food_dining",
    "starbucks": "food_dining",
    "mcdonald": "food_dining",
    "ماكدونالدز": "food_dining",
    "ستاربكس": "food_dining",
    "شاورمر": "food_dining",
    "al meera": "groceries",
    "meera": "groceries",
    "lulu": "groceries",
    "danube": "groceries",
    "woqod": "transport",
    "qatar fuel": "transport",
    "apple.com/bill": "subscriptions",
    "apple.com bill": "subscriptions",
    "apple.com": "subscriptions",
    "itunes": "subscriptions",
    "youtube": "subscriptions",
    "google youtube": "subscriptions",
    "netflix": "subscriptions",
    "spotify": "subscriptions",
    "openai": "subscriptions",
    "chatgpt": "subscriptions",
    "hostinger": "subscriptions",
    "railway": "subscriptions",
    "aws": "business_operations",
    "google cloud": "business_operations",
    "amazon": "shopping",
    "uber": "transport",
    "careem": "transport",
    "booking.com": "travel",
    "airbnb": "travel",
    "loan repayment": "debt_loans",
    "salary transfer": "income",
}


GENERIC_PAYMENT_WORDS = [
    r"\bapple\s*pay\b", r"\bgoogle\s*pay\b", r"\bsamsung\s*pay\b",
    r"\bmada\b", r"\bvisa\b", r"\bmastercard\b", r"\bamex\b",
    r"شراء عبر نقاط بيع", r"نقاط بيع", r"مدي اثير", r"مدى أثير",
]


def strip_accents(text: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(char)
    )


def normalize_text(text: str) -> str:
    """Normalize multilingual bank text without destroying merchant/category signals."""
    if text is None:
        return ""

    text = str(text).lower()
    text = strip_accents(text)

    text = re.sub(r"\*+", " ", text)
    text = re.sub(r"\b\d{8,}\b", " ", text)
    text = re.sub(r"\b(?:ref|reference|مرجع|رقم الشاشه|screen|city|vat chrg)[:\s\w-]*", " ", text)

    for pattern in GENERIC_PAYMENT_WORDS:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)

    text = re.sub(r"[^a-z0-9\u0600-\u06FF+.'&/ -]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_tokens(text: str) -> set[str]:
    return {
        token
        for token in re.split(r"[^a-z0-9\u0600-\u06FF]+", normalize_text(text))
        if token
    }


def _canonical_category(category: str) -> str:
    return CATEGORY_ALIASES.get(category, category)


def _keyword_matches(keyword: str, normalized: str, tokens: set[str]) -> bool:
    keyword = normalize_text(keyword)
    if not keyword:
        return False

    if " " in keyword or "/" in keyword or "+" in keyword or "." in keyword:
        return keyword in normalized

    return keyword in tokens


def detect_category(description: str) -> str:
    """
    Layered deterministic classifier.

    1) Merchant overrides
    2) Priority-based multilingual keyword taxonomy
    3) Safe generic purchase fallback -> shopping
    4) other
    """
    original = "" if description is None else str(description)
    normalized = normalize_text(original)
    tokens = normalize_tokens(original)

    for merchant, category in MERCHANT_CATEGORY_OVERRIDES.items():
        if normalize_text(merchant) in normalized:
            return _canonical_category(category)

    for category in CATEGORY_PRIORITY:
        for keyword in CATEGORY_KEYWORDS.get(category, []):
            if _keyword_matches(keyword, normalized, tokens):
                return _canonical_category(category)

    lowered_original = original.lower()
    if re.search(
        r"pos purchase|card purchase|naps purchase|cbq purchase|electron auth|"
        r"paiement carte|achat carte|شراء عبر نقاط بيع|نقاط بيع|مدي اثير|مدى أثير",
        lowered_original,
    ):
        return "shopping"

    return "other"


def detect_category_details(description: str) -> dict[str, Any]:
    category = detect_category(description)
    return {
        "category": category,
        "labels": CATEGORY_LABELS.get(category, CATEGORY_LABELS["other"]),
        "normalized_description": normalize_text(description),
    }


def get_category_label(category: str, language: str = "en") -> str:
    category = _canonical_category(category)
    labels = CATEGORY_LABELS.get(category, CATEGORY_LABELS["other"])
    return labels.get(language, labels["en"])


def category_is_cashflow_neutral(category: str) -> bool:
    return _canonical_category(category) in {"transfers", "savings_investments"}


def build_financial_charts(transactions: list[dict]) -> dict:
    spending_over_time = defaultdict(float)
    income_over_time = defaultdict(float)
    net_cashflow_over_time = defaultdict(float)
    category_breakdown = defaultdict(float)
    essential_breakdown = defaultdict(float)
    discretionary_breakdown = defaultdict(float)
    transfer_breakdown = defaultdict(float)
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
        tx_type = tx.get("type")

        running_net += amount
        savings_evolution.append({"date": date, "amount": round(running_net, 2)})
        net_cashflow_over_time[date] += amount

        if tx_type == "expense":
            expense_amount = abs(amount)
            category = detect_category(description)

            spending_over_time[date] += expense_amount
            category_breakdown[category] += expense_amount

            if category == "subscriptions":
                subscription_growth[date] += expense_amount

            if category in {
                "housing", "utilities", "groceries", "healthcare", "insurance",
                "debt_loans", "fees", "government_taxes",
            }:
                essential_breakdown[category] += expense_amount
            elif category in {"transfers", "savings_investments"}:
                transfer_breakdown[category] += expense_amount
            else:
                discretionary_breakdown[category] += expense_amount

        elif tx_type == "income":
            income_over_time[date] += amount

    total_income = round(sum(income_over_time.values()), 2)
    total_expenses = round(sum(spending_over_time.values()), 2)
    total_transfers_savings = round(sum(transfer_breakdown.values()), 2)
    adjusted_consumption = round(total_expenses - total_transfers_savings, 2)
    other_amount = round(category_breakdown.get("other", 0.0), 2)
    other_ratio = round((other_amount / total_expenses) * 100, 2) if total_expenses else 0.0

    def as_series(mapping: defaultdict) -> list[dict]:
        return [{"date": date, "amount": round(amount, 2)} for date, amount in mapping.items()]

    def as_category_series(mapping: defaultdict) -> list[dict]:
        return [
            {
                "category": category,
                "label_en": get_category_label(category, "en"),
                "label_fr": get_category_label(category, "fr"),
                "label_ar": get_category_label(category, "ar"),
                "amount": round(amount, 2),
            }
            for category, amount in sorted(mapping.items(), key=lambda item: item[1], reverse=True)
        ]

    return {
        "spending_over_time": as_series(spending_over_time),
        "income_over_time": as_series(income_over_time),
        "income_vs_expenses": {
            "income": total_income,
            "expenses": total_expenses,
            "net": round(total_income - total_expenses, 2),
            "transfers_and_savings": total_transfers_savings,
            "adjusted_consumption": adjusted_consumption,
            "adjusted_net_after_consumption": round(total_income - adjusted_consumption, 2),
        },
        "category_breakdown": as_category_series(category_breakdown),
        "essential_breakdown": as_category_series(essential_breakdown),
        "discretionary_breakdown": as_category_series(discretionary_breakdown),
        "transfer_breakdown": as_category_series(transfer_breakdown),
        "quality_metrics": {
            "other_amount": other_amount,
            "other_ratio_percent": other_ratio,
            "target_other_ratio_percent": 5.0,
            "needs_ai_recategorization_pass": other_ratio > 5.0,
        },
        "net_cashflow_over_time": as_series(net_cashflow_over_time),
        "subscription_growth": as_series(subscription_growth),
        "savings_evolution": savings_evolution,
    }


if __name__ == "__main__":
    samples = [
        "03-Sep-23 ELECTRON AUTH 891390 APPLE.COM/BILL ITUNES.COM 149.99 3,377.41",
        "07-Sep-23 NAPS PURCHASE AL MEERA 72.14 1,879.33",
        "12-Sep-23 FUNDS TRANSFER Bilel bouzidi 1,250.00 313.00",
        "SALARY TRANSFER CDD 6760.00",
        "ايداع رواتب القوات البريه الملكيه السعوديه /PAYROLL/",
        "Pay Apple - شراء عبر نقاط بيع ستاربكس RIYADH",
    ]

    for sample in samples:
        print(sample, "=>", detect_category_details(sample))
