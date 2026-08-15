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


print(
    "RUNEXA_FINANCE_CATEGORIZATION_VERSION",
    "v5-additive-observed-other-breakdown",
)


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
        "cash deposit", "benefit payment", "benefits payment",
        "jobseeker payment", "unemployment benefit", "social security",
        "government benefit", "welfare payment",
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
        "chicken", "grill", "grilled", "takeaway",
        "poulet", "grillade", "à emporter", "a emporter",
        "دجاج", "مشويات", "وجبة سريعة",
        "restaurant", "cafe", "coffee", "food", "meal", "dining", "fast food", "pizza", "burger",
        "mcdonald", "burger king", "kfc", "subway", "starbucks", "costa", "dunkin", "shawarma",
        "talabat", "tea time",
        "café", "brasserie", "boulangerie", "snack", "repas", "resto",
        "مطعم", "مطاعم", "مقهى", "مقهي", "قهوة", "قهوه", "وجبات", "بروست", "شاورما",
        "شاورمر", "ماكدونالدز", "ستاربكس", "باسكن روبنز", "الوجبات", "مدينه النعناع",
        "شركة الوجبات", "شركه الوجبات", "بروست ساره", "كافيه",
    ],
    "transport": [
        "fuel station", "petrol station", "filling station", "service station", "fuel stn", "petrol stn",
        "station essence", "station carburant",
        "محطة بنزين", "محطة وقود",
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



STANDARD_BANK_ABBREVIATIONS = {
    # Generic banking abbreviations observed in real statements.
    # These are lexical expansions only; they do not encode bank, country,
    # currency, merchant, account holder, or transaction direction.
    "trns": "transfer",
    "xfer": "transfer",
    "xfr": "transfer",
    "pymt": "payment",
    "pmt": "payment",
    "acct": "account",
    "acc": "account",
}


def _expand_standard_bank_abbreviations(value: str) -> str:
    surface = _semantic_match_surface_without_abbreviation_expansion(value)
    tokens = surface.split()
    return " ".join(
        STANDARD_BANK_ABBREVIATIONS.get(token, token)
        for token in tokens
    )


def _semantic_match_surface_without_abbreviation_expansion(value: str) -> str:
    value = normalize_text(value)
    value = value.replace("&", " and ")
    value = re.sub(r"[./_\\-]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _semantic_match_surface(value: str) -> str:
    """
    Additive comparison surface for noisy statement descriptions.

    This is intentionally independent of bank, country, currency and merchant.
    It only normalizes punctuation/separators that PDF/OCR pipelines frequently
    vary while preserving letters, digits and Arabic text.
    """
    return _expand_standard_bank_abbreviations(value)


def _conservative_token_variants(value: str) -> set[str]:
    """
    Produce conservative lexical variants after the historical exact matcher.

    Only a trailing possessive/plural-like ``s`` is removed, and only for
    alphabetic tokens of length >= 6. This lets OCR/text variants such as
    ``sainsburys`` match an existing taxonomy token ``sainsbury`` without
    introducing bank- or merchant-specific rules.
    """
    variants: set[str] = set()

    for token in re.split(
        r"[^a-z0-9\u0600-\u06FF]+",
        _semantic_match_surface(value),
    ):
        if not token:
            continue

        variants.add(token)

        if (
            len(token) >= 6
            and token.isalpha()
            and token.endswith("s")
        ):
            variants.add(token[:-1])

    return variants


def _additive_keyword_matches(
    keyword: str,
    original: str,
) -> bool:
    """
    Secondary matcher used only after the historical classifier did not match.
    """
    keyword_surface = _semantic_match_surface(keyword)
    description_surface = _semantic_match_surface(original)

    if not keyword_surface:
        return False

    if " " in keyword_surface:
        return keyword_surface in description_surface

    description_variants = _conservative_token_variants(original)
    keyword_variants = _conservative_token_variants(keyword)

    return bool(description_variants.intersection(keyword_variants))


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

    # ADDITIVE v2 — punctuation/OCR/inflection tolerant matching.
    # Historical exact matches above always remain authoritative.
    for category in CATEGORY_PRIORITY:
        for keyword in CATEGORY_KEYWORDS.get(category, []):
            if _additive_keyword_matches(keyword, original):
                return _canonical_category(category)

    # ADDITIVE v4 — standard service-class evidence.
    #
    # A token ending in "vpn" identifies a VPN service class rather than a
    # specific merchant.  This is intentionally narrower than matching payment
    # processors such as PayPal, which remain unclassified without evidence
    # about the underlying purchase.
    semantic_surface = _semantic_match_surface(original)

    if re.search(
        r"\b[a-z0-9]{2,}vpn\b|\bvpn\s+(?:service|subscription|plan)\b",
        semantic_surface,
        flags=re.IGNORECASE,
    ):
        return "subscriptions"

    # ADDITIVE v3/v4 — standardized account-transfer phrase.
    # This path runs only after the historical taxonomy failed.  It relies on
    # generic banking-role words after abbreviation normalization.
    if re.search(
        r"\b(?:linked|internal|own)\s+account\s+transfer\b",
        semantic_surface,
        flags=re.IGNORECASE,
    ):
        return "transfers"

    # ADDITIVE v4 — named counterparty + opaque reference.
    #
    # Real bank statements often render a direct transfer as:
    #
    #   <counterparty name> <opaque alphanumeric reference>
    #
    # This rule is deliberately conservative. It requires a name-like prefix,
    # a long terminal reference containing both letters and digits, and rejects
    # card/purchase/payment-processor/service language. It does not encode any
    # institution, country, currency, person, or merchant.
    counterparty_reference_match = re.fullmatch(
        r"\s*(?:mr|mrs|ms|miss|dr)?\.?\s*"
        r"[a-z][a-z.'-]*(?:\s+[a-z][a-z.'-]*){1,4}\s+"
        r"(?=[a-z0-9]{8,16}\b)(?=[a-z0-9]*[a-z])(?=[a-z0-9]*\d)"
        r"[a-z0-9]{8,16}\s*",
        semantic_surface,
        flags=re.IGNORECASE,
    )

    counterparty_transfer_exclusions = bool(
        re.search(
            r"\b(?:card|purchase|pos|atm|cash|paypal|invoice|bill|"
            r"subscription|merchant|store|shop|restaurant|cafe|hotel|"
            r"fee|tax|loan|insurance|utility|phone|mobile|internet)\b",
            semantic_surface,
            flags=re.IGNORECASE,
        )
    )

    if (
        counterparty_reference_match
        and not counterparty_transfer_exclusions
    ):
        return "transfers"

    # Structural bank-transfer fallback.
    # Standard EN/FR/AR rule: opaque reference + bank clearing/core-system
    # metadata usually means a transfer, not an unknown merchant purchase.
    transfer_reference_like = bool(
        re.search(
            r"\b(ref|reference|beneficiary|iban|swift|bic|value\s*dt|value\s*date|"
            r"date[-\s]*time|core\s*system|via\s*core|system\s*core|"
            r"instant\s*payment|bank\s*transfer|wire\s*transfer|"
            r"virement|référence|reference|bénéficiaire|beneficiaire|"
            r"تحويل|حوالة|مرجع|مستفيد|النظام|السريع)\b",
            normalized,
            flags=re.IGNORECASE,
        )
    )
    has_bank_identifier = bool(
        re.search(
            r"\b[A-Z0-9]{8,}\b|\b[A-Z]{4,}SARI\b|\bSA\d{2}[A-Z0-9]{10,}\b",
            original.upper(),
        )
    )
    has_card_purchase_signal = bool(
        re.search(
            r"card no|pos#|mada|apple pay|google pay|purchase|"
            r"بطاقة|مدى|نقاط بيع|شراء",
            original.lower(),
        )
    )

    if transfer_reference_like and (has_bank_identifier or "core" in normalized or "system" in normalized) and not has_card_purchase_signal:
        return "transfers"

    # Generic outgoing payment to an organization/service provider.
    # Standard rule, not merchant-specific.
    if re.search(
        r"^(to|payment to|paid to|payee|beneficiary)\s+[a-z0-9]",
        normalized,
    ):
        return "business_operations"

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



def normalize_chart_date(value: object) -> str:
    s = str(value or "").strip()

    # Fix OCR/parser issue: YYYY-DD-MM -> YYYY-MM-DD
    # Example: 2024-20-06 => 2024-06-20
    m = re.match(r"^(20\d{2})-(\d{2})-(\d{2})$", s)
    if m:
        year, a, b = m.groups()
        aa = int(a)
        bb = int(b)

        if aa > 12 and 1 <= bb <= 12:
            return f"{year}-{bb:02d}-{aa:02d}"

    return s or "unknown"


def build_financial_charts(transactions: list[dict]) -> dict:
    spending_over_time = defaultdict(float)
    income_over_time = defaultdict(float)
    net_cashflow_over_time = defaultdict(float)
    category_breakdown = defaultdict(float)
    essential_breakdown = defaultdict(float)
    discretionary_breakdown = defaultdict(float)
    transfer_breakdown = defaultdict(float)
    subscription_growth = defaultdict(float)

    # ADDITIVE v5 — retain statement-specific evidence behind "Other".
    #
    # This does not recategorize any transaction and does not add merchant,
    # bank, country, currency, or statement-specific rules.  It only preserves
    # the observed rows that the historical classifier already left in
    # "other", so the UI can explain that aggregate for the current statement.
    other_observed_rows = []

    savings_evolution = []
    running_net = 0.0

    sorted_transactions = sorted(
        transactions,
        key=lambda tx: tx.get("date") or "9999-12-31",
    )

    for tx in sorted_transactions:
        date = normalize_chart_date(tx.get("date"))
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

            if category == "other":
                other_observed_rows.append(
                    {
                        "date": date,
                        "description": str(description or "").strip(),
                        "amount": round(expense_amount, 2),
                    }
                )

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

    # Deterministic display order: largest observed "Other" expense first,
    # then date and description for stable output across runs.
    other_observed_rows = sorted(
        other_observed_rows,
        key=lambda row: (
            -float(row.get("amount", 0) or 0),
            str(row.get("date") or ""),
            str(row.get("description") or ""),
        ),
    )

    # Reconcile the detail to the already-existing "Other" aggregate.  This is
    # an audit/display field only; no category or amount is changed.
    other_observed_total = round(
        sum(float(row.get("amount", 0) or 0) for row in other_observed_rows),
        2,
    )

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

        # ADDITIVE v5 — statement-specific explanation of the existing
        # "Other" aggregate. Existing consumers can ignore this key.
        "other_breakdown": {
            "amount": other_amount,
            "observed_total": other_observed_total,
            "reconciled": abs(other_observed_total - other_amount) <= 0.01,
            "transaction_count": len(other_observed_rows),
            "transactions": other_observed_rows,
            "basis": "observed_transactions_classified_as_other",
        },

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



def assess_analysis_quality_standard(transactions: list[dict]) -> dict[str, Any]:
    """International structural quality gate for bank-statement parsing.

    Validation should be based on whether transactions were extracted with a
    date, an amount and a description. A statement must not be rejected only
    because merchants are not recognized or many rows are transfers.
    """
    total = len(transactions or [])

    if total == 0:
        return {
            "status": "insufficient_data",
            "confidence": 0,
            "transaction_count": 0,
            "structure_ratio": 0,
            "other_ratio": 1,
            "category_confidence": 0,
        }

    structurally_valid = 0
    categorized_count = 0
    other_count = 0

    for tx in transactions:
        has_date = bool(tx.get("date"))
        has_amount = tx.get("amount") is not None
        has_description = bool(str(tx.get("description", "")).strip())

        if has_date and has_amount and has_description:
            structurally_valid += 1

        category = _canonical_category(
            tx.get("category") or detect_category(tx.get("description", ""))
        )

        if category != "other":
            categorized_count += 1
        else:
            other_count += 1

    structure_ratio = structurally_valid / total
    other_ratio = other_count / total
    category_confidence = categorized_count / total

    if total < 5 or structure_ratio < 0.40:
        status = "insufficient_data"
        confidence = 25
    elif total < 15 or structure_ratio < 0.70:
        status = "partial"
        confidence = 60
    else:
        status = "verified"
        confidence = 90

    if status == "verified" and category_confidence < 0.35:
        confidence = 80

    return {
        "status": status,
        "confidence": confidence,
        "transaction_count": total,
        "structure_ratio": round(structure_ratio, 4),
        "other_ratio": round(other_ratio, 4),
        "category_confidence": round(category_confidence, 4),
    }
