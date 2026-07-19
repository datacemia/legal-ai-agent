"""
jurisdiction_detector_international.py

International jurisdiction detector for contract analysis.

Goal:
- Work across contract families and sectors.
- Support EN / FR / AR wording.
- Detect separately:
    governing_law
    dispute_forum
    arbitration_seat
    arbitration_institution
- Cover all countries at a generic level.
- Provide stronger signals for common commercial jurisdictions and arbitration seats.
- Avoid hallucinating country-specific legal conclusions.

Important:
This detector identifies jurisdictional references in contract text.
It does not provide legal advice and does not infer governing law unless
the contract text actually supports it.
"""

import re
from typing import Any


SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


# ---------------------------------------------------------------------
# All UN member states + common commercial jurisdictions / territories.
# Generic country coverage is intentionally simple and safe.
# ---------------------------------------------------------------------

COUNTRY_ALIASES = {
    "afghanistan": ["afghanistan", "afghanistan", "أفغانستان"],
    "albania": ["albania", "albanie", "ألبانيا"],
    "algeria": ["algeria", "algérie", "الجزائر"],
    "andorra": ["andorra", "andorre", "أندورا"],
    "angola": ["angola", "angola", "أنغولا"],
    "antigua_and_barbuda": ["antigua and barbuda", "antigua-et-barbuda", "أنتيغوا وبربودا"],
    "argentina": ["argentina", "argentine", "الأرجنتين"],
    "armenia": ["armenia", "arménie", "أرمينيا"],
    "australia": ["australia", "australie", "أستراليا"],
    "austria": ["austria", "autriche", "النمسا"],
    "azerbaijan": ["azerbaijan", "azerbaïdjan", "أذربيجان"],
    "bahamas": ["bahamas", "bahamas", "الباهاما"],
    "bahrain": ["bahrain", "bahreïn", "البحرين"],
    "bangladesh": ["bangladesh", "bangladesh", "بنغلاديش"],
    "barbados": ["barbados", "barbade", "بربادوس"],
    "belarus": ["belarus", "biélorussie", "بيلاروس"],
    "belgium": ["belgium", "belgique", "بلجيكا"],
    "belize": ["belize", "belize", "بليز"],
    "benin": ["benin", "bénin", "بنين"],
    "bhutan": ["bhutan", "bhoutan", "بوتان"],
    "bolivia": ["bolivia", "bolivie", "بوليفيا"],
    "bosnia_and_herzegovina": ["bosnia and herzegovina", "bosnie-herzégovine", "البوسنة والهرسك"],
    "botswana": ["botswana", "botswana", "بوتسوانا"],
    "brazil": ["brazil", "brésil", "البرازيل"],
    "brunei": ["brunei", "brunéi", "بروناي"],
    "bulgaria": ["bulgaria", "bulgarie", "بلغاريا"],
    "burkina_faso": ["burkina faso", "burkina faso", "بوركينا فاسو"],
    "burundi": ["burundi", "burundi", "بوروندي"],
    "cabo_verde": ["cabo verde", "cape verde", "cap-vert", "الرأس الأخضر"],
    "cambodia": ["cambodia", "cambodge", "كمبوديا"],
    "cameroon": ["cameroon", "cameroun", "الكاميرون"],
    "canada": ["canada", "canada", "كندا"],
    "central_african_republic": ["central african republic", "république centrafricaine", "جمهورية أفريقيا الوسطى"],
    "chad": ["chad", "tchad", "تشاد"],
    "chile": ["chile", "chili", "تشيلي"],
    "china": ["china", "chine", "الصين"],
    "colombia": ["colombia", "colombie", "كولومبيا"],
    "comoros": ["comoros", "comores", "جزر القمر"],
    "congo": ["congo", "république du congo", "الكونغو"],
    "costa_rica": ["costa rica", "costa rica", "كوستاريكا"],
    "cote_d_ivoire": ["côte d'ivoire", "cote d'ivoire", "ivory coast", "كوت ديفوار", "ساحل العاج"],
    "croatia": ["croatia", "croatie", "كرواتيا"],
    "cuba": ["cuba", "cuba", "كوبا"],
    "cyprus": ["cyprus", "chypre", "قبرص"],
    "czech_republic": ["czech republic", "czechia", "tchéquie", "république tchèque", "التشيك"],
    "democratic_republic_of_congo": ["democratic republic of the congo", "rdc", "république démocratique du congo", "جمهورية الكونغو الديمقراطية"],
    "denmark": ["denmark", "danemark", "الدنمارك"],
    "djibouti": ["djibouti", "djibouti", "جيبوتي"],
    "dominica": ["dominica", "dominique", "دومينيكا"],
    "dominican_republic": ["dominican republic", "république dominicaine", "جمهورية الدومينيكان"],
    "ecuador": ["ecuador", "équateur", "الإكوادور"],
    "egypt": ["egypt", "égypte", "مصر"],
    "el_salvador": ["el salvador", "salvador", "السلفادور"],
    "equatorial_guinea": ["equatorial guinea", "guinée équatoriale", "غينيا الاستوائية"],
    "eritrea": ["eritrea", "érythrée", "إريتريا"],
    "estonia": ["estonia", "estonie", "إستونيا"],
    "eswatini": ["eswatini", "swaziland", "eswatini", "إسواتيني"],
    "ethiopia": ["ethiopia", "éthiopie", "إثيوبيا"],
    "fiji": ["fiji", "fidji", "فيجي"],
    "finland": ["finland", "finlande", "فنلندا"],
    "france": ["france", "french law", "droit français", "loi française", "فرنسا", "القانون الفرنسي"],
    "gabon": ["gabon", "gabon", "الغابون"],
    "gambia": ["gambia", "gambie", "غامبيا"],
    "georgia": ["georgia", "géorgie", "جورجيا"],
    "germany": ["germany", "allemagne", "german law", "droit allemand", "ألمانيا", "القانون الألماني"],
    "ghana": ["ghana", "ghana", "غانا"],
    "greece": ["greece", "grèce", "اليونان"],
    "grenada": ["grenada", "grenade", "غرينادا"],
    "guatemala": ["guatemala", "guatemala", "غواتيمالا"],
    "guinea": ["guinea", "guinée", "غينيا"],
    "guinea_bissau": ["guinea-bissau", "guinée-bissau", "غينيا بيساو"],
    "guyana": ["guyana", "guyana", "غيانا"],
    "haiti": ["haiti", "haïti", "هايتي"],
    "honduras": ["honduras", "honduras", "هندوراس"],
    "hungary": ["hungary", "hongrie", "المجر"],
    "iceland": ["iceland", "islande", "آيسلندا"],
    "india": ["india", "inde", "الهند"],
    "indonesia": ["indonesia", "indonésie", "إندونيسيا"],
    "iran": ["iran", "iran", "إيران"],
    "iraq": ["iraq", "irak", "العراق"],
    "ireland": ["ireland", "irlande", "إيرلندا"],
    "israel": ["israel", "israël", "إسرائيل"],
    "italy": ["italy", "italie", "إيطاليا"],
    "jamaica": ["jamaica", "jamaïque", "جامايكا"],
    "japan": ["japan", "japon", "اليابان"],
    "jordan": ["jordan", "jordanie", "الأردن"],
    "kazakhstan": ["kazakhstan", "kazakhstan", "كازاخستان"],
    "kenya": ["kenya", "kenya", "كينيا"],
    "kiribati": ["kiribati", "kiribati", "كيريباتي"],
    "kuwait": ["kuwait", "koweït", "الكويت"],
    "kyrgyzstan": ["kyrgyzstan", "kirghizistan", "قيرغيزستان"],
    "laos": ["laos", "laos", "لاوس"],
    "latvia": ["latvia", "lettonie", "لاتفيا"],
    "lebanon": ["lebanon", "liban", "لبنان"],
    "lesotho": ["lesotho", "lesotho", "ليسوتو"],
    "liberia": ["liberia", "libéria", "ليبيريا"],
    "libya": ["libya", "libye", "ليبيا"],
    "liechtenstein": ["liechtenstein", "liechtenstein", "ليختنشتاين"],
    "lithuania": ["lithuania", "lituanie", "ليتوانيا"],
    "luxembourg": ["luxembourg", "luxembourg", "لوكسمبورغ"],
    "madagascar": ["madagascar", "madagascar", "مدغشقر"],
    "malawi": ["malawi", "malawi", "ملاوي"],
    "malaysia": ["malaysia", "malaisie", "ماليزيا"],
    "maldives": ["maldives", "maldives", "جزر المالديف"],
    "mali": ["mali", "mali", "مالي"],
    "malta": ["malta", "malte", "مالطا"],
    "marshall_islands": ["marshall islands", "îles marshall", "جزر مارشال"],
    "mauritania": ["mauritania", "mauritanie", "موريتانيا"],
    "mauritius": ["mauritius", "maurice", "موريشيوس"],
    "mexico": ["mexico", "mexique", "المكسيك"],
    "micronesia": ["micronesia", "micronésie", "ميكرونيزيا"],
    "moldova": ["moldova", "moldavie", "مولدوفا"],
    "monaco": ["monaco", "monaco", "موناكو"],
    "mongolia": ["mongolia", "mongolie", "منغوليا"],
    "montenegro": ["montenegro", "monténégro", "الجبل الأسود"],
    "morocco": ["morocco", "maroc", "droit marocain", "القانون المغربي", "المغرب"],
    "mozambique": ["mozambique", "mozambique", "موزمبيق"],
    "myanmar": ["myanmar", "burma", "birmanie", "ميانمار"],
    "namibia": ["namibia", "namibie", "ناميبيا"],
    "nauru": ["nauru", "nauru", "ناورو"],
    "nepal": ["nepal", "népal", "نيبال"],
    "netherlands": ["netherlands", "pays-bas", "dutch law", "droit néerlandais", "هولندا", "القانون الهولندي"],
    "new_zealand": ["new zealand", "nouvelle-zélande", "نيوزيلندا"],
    "nicaragua": ["nicaragua", "nicaragua", "نيكاراغوا"],
    "niger": ["niger", "niger", "النيجر"],
    "nigeria": ["nigeria", "nigéria", "نيجيريا"],
    "north_korea": ["north korea", "corée du nord", "كوريا الشمالية"],
    "north_macedonia": ["north macedonia", "macédoine du nord", "مقدونيا الشمالية"],
    "norway": ["norway", "norvège", "النرويج"],
    "oman": ["oman", "oman", "عمان"],
    "pakistan": ["pakistan", "pakistan", "باكستان"],
    "palau": ["palau", "palaos", "بالاو"],
    "panama": ["panama", "panama", "بنما"],
    "papua_new_guinea": ["papua new guinea", "papouasie-nouvelle-guinée", "بابوا غينيا الجديدة"],
    "paraguay": ["paraguay", "paraguay", "باراغواي"],
    "peru": ["peru", "pérou", "بيرو"],
    "philippines": ["philippines", "philippines", "الفلبين"],
    "poland": ["poland", "pologne", "بولندا"],
    "portugal": ["portugal", "portugal", "البرتغال"],
    "qatar": ["qatar", "qatar", "قطر"],
    "romania": ["romania", "roumanie", "رومانيا"],
    "russia": ["russia", "russian federation", "russie", "روسيا"],
    "rwanda": ["rwanda", "rwanda", "رواندا"],
    "saint_kitts_and_nevis": ["saint kitts and nevis", "saint-christophe-et-niévès", "سانت كيتس ونيفيس"],
    "saint_lucia": ["saint lucia", "sainte-lucie", "سانت لوسيا"],
    "saint_vincent_and_the_grenadines": ["saint vincent and the grenadines", "saint-vincent-et-les-grenadines", "سانت فنسنت والغرينادين"],
    "samoa": ["samoa", "samoa", "ساموا"],
    "san_marino": ["san marino", "saint-marin", "سان مارينو"],
    "sao_tome_and_principe": ["sao tome and principe", "são tomé and príncipe", "sao tomé-et-principe", "ساو تومي وبرينسيبي"],
    "saudi_arabia": ["saudi arabia", "kingdom of saudi arabia", "arabie saoudite", "المملكة العربية السعودية", "السعودية"],
    "senegal": ["senegal", "sénégal", "السنغال"],
    "serbia": ["serbia", "serbie", "صربيا"],
    "seychelles": ["seychelles", "seychelles", "سيشل"],
    "sierra_leone": ["sierra leone", "sierra leone", "سيراليون"],
    "singapore": ["singapore", "singapour", "singapore law", "droit singapourien", "سنغافورة", "القانون السنغافوري"],
    "slovakia": ["slovakia", "slovaquie", "سلوفاكيا"],
    "slovenia": ["slovenia", "slovénie", "سلوفينيا"],
    "solomon_islands": ["solomon islands", "îles salomon", "جزر سليمان"],
    "somalia": ["somalia", "somalie", "الصومال"],
    "south_africa": ["south africa", "afrique du sud", "جنوب أفريقيا"],
    "south_korea": ["south korea", "korea", "corée du sud", "كوريا الجنوبية"],
    "south_sudan": ["south sudan", "soudan du sud", "جنوب السودان"],
    "spain": ["spain", "espagne", "spanish law", "droit espagnol", "إسبانيا", "القانون الإسباني"],
    "sri_lanka": ["sri lanka", "sri lanka", "سريلانكا"],
    "sudan": ["sudan", "soudan", "السودان"],
    "suriname": ["suriname", "suriname", "سورينام"],
    "sweden": ["sweden", "suède", "السويد"],
    "switzerland": ["switzerland", "suisse", "swiss law", "droit suisse", "geneva", "genève", "zurich", "سويسرا", "جنيف", "زيورخ"],
    "syria": ["syria", "syrie", "سوريا"],
    "tajikistan": ["tajikistan", "tadjikistan", "طاجيكستان"],
    "tanzania": ["tanzania", "tanzanie", "تنزانيا"],
    "thailand": ["thailand", "thaïlande", "تايلاند"],
    "timor_leste": ["timor-leste", "east timor", "timor oriental", "تيمور الشرقية"],
    "togo": ["togo", "togo", "توغو"],
    "tonga": ["tonga", "tonga", "تونغا"],
    "trinidad_and_tobago": ["trinidad and tobago", "trinité-et-tobago", "ترينيداد وتوباغو"],
    "tunisia": ["tunisia", "tunisie", "تونس"],
    "turkey": ["turkey", "türkiye", "turquie", "تركيا"],
    "turkmenistan": ["turkmenistan", "turkménistan", "تركمانستان"],
    "tuvalu": ["tuvalu", "tuvalu", "توفالو"],
    "uganda": ["uganda", "ouganda", "أوغندا"],
    "ukraine": ["ukraine", "ukraine", "أوكرانيا"],
    "united_arab_emirates": ["uae", "united arab emirates", "emirates", "dubai", "abu dhabi", "difc", "adgm", "émirats arabes unis", "dubai", "abou dhabi", "الإمارات", "دبي", "أبوظبي"],
    "united_kingdom": ["united kingdom", "uk", "england and wales", "english law", "london", "royaume-uni", "angleterre et pays de galles", "droit anglais", "londres", "المملكة المتحدة", "إنجلترا وويلز", "القانون الإنجليزي", "لندن"],
    "united_states": ["united states", "usa", "u.s.", "us law", "state of california", "new york", "delaware", "california", "états-unis", "droit américain", "كاليفورنيا", "نيويورك", "ديلاوير", "الولايات المتحدة"],
    "uruguay": ["uruguay", "uruguay", "أوروغواي"],
    "uzbekistan": ["uzbekistan", "ouzbekistan", "أوزبكستان"],
    "vanuatu": ["vanuatu", "vanuatu", "فانواتو"],
    "venezuela": ["venezuela", "venezuela", "فنزويلا"],
    "vietnam": ["vietnam", "viêt nam", "فيتنام"],
    "yemen": ["yemen", "yémen", "اليمن"],
    "zambia": ["zambia", "zambie", "زامبيا"],
    "zimbabwe": ["zimbabwe", "zimbabwe", "زيمبابوي"],

    # Common non-UN / special commercial jurisdictions.
    "hong_kong": ["hong kong", "hong kong sar", "hong-kong", "هونغ كونغ"],
    "taiwan": ["taiwan", "taïwan", "تايوان"],
    "macau": ["macau", "macao", "ماكاو"],
    "cayman_islands": ["cayman islands", "îles caïmans", "جزر كايمان"],
    "british_virgin_islands": ["british virgin islands", "bvi", "îles vierges britanniques", "جزر العذراء البريطانية"],
    "bermuda": ["bermuda", "bermudes", "برمودا"],
    "gibraltar": ["gibraltar", "gibraltar", "جبل طارق"],
}


LEGAL_SYSTEM_OVERRIDES = {
    "france": "civil_law",
    "morocco": "civil_law",
    "germany": "civil_law",
    "spain": "civil_law",
    "italy": "civil_law",
    "netherlands": "civil_law",
    "switzerland": "civil_law",
    "united_states": "common_law",
    "united_kingdom": "common_law",
    "ireland": "common_law",
    "canada": "mixed",
    "australia": "common_law",
    "new_zealand": "common_law",
    "singapore": "common_law",
    "hong_kong": "common_law",
    "united_arab_emirates": "mixed",
    "saudi_arabia": "mixed",
    "qatar": "mixed",
    "south_africa": "mixed",
}


ARBITRATION_INSTITUTIONS = {
    "ICC": [
        "icc", "international chamber of commerce",
        "chambre de commerce internationale",
        "غرفة التجارة الدولية",
    ],
    "LCIA": [
        "lcia", "london court of international arbitration",
        "cour internationale d'arbitrage de londres",
    ],
    "SIAC": [
        "siac", "singapore international arbitration centre",
        "centre d'arbitrage international de singapour",
    ],
    "HKIAC": [
        "hkiac", "hong kong international arbitration centre",
        "centre d'arbitrage international de hong kong",
    ],
    "DIAC": [
        "diac", "dubai international arbitration centre",
        "centre d'arbitrage international de dubai",
        "مركز دبي للتحكيم الدولي",
    ],
    "ADCCAC": [
        "adccac", "abu dhabi commercial conciliation and arbitration centre",
    ],
    "ICDR": [
        "icdr", "international centre for dispute resolution",
    ],
    "AAA": [
        "american arbitration association", "aaa",
    ],
    "UNCITRAL": [
        "uncitral", "cnudci", "الأونسيترال",
    ],
    "ICSID": [
        "icsid", "international centre for settlement of investment disputes",
        "centre international pour le règlement des différends relatifs aux investissements",
    ],
    "SCC": [
        "stockholm chamber of commerce", "scc arbitration institute",
    ],
    "CRCICA": [
        "crcica", "cairo regional centre for international commercial arbitration",
        "مركز القاهرة الإقليمي للتحكيم التجاري الدولي",
    ],
    "CMAC": [
        "moroccan court of arbitration", "cour marocaine d'arbitrage",
        "المحكمة المغربية للتحكيم",
    ],
}


GOVERNING_LAW_PATTERNS = [
    r"governed by the laws of\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",
    r"governed under the laws of\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",
    r"laws of\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)\s+shall govern",
    r"subject to the laws of\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",

    r"régi par le droit de\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",
    r"régie par le droit de\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",
    r"soumis au droit de\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",
    r"lois de\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)\s+s'appliquent",

    # AR — governing law
    r"تخضع\s+.{0,160}?\s+لقانون\s+([^\.\n،؛!?]{2,120})",
    r"تخضع\s+.{0,160}?\s+لقوانين\s+([^\.\n،؛!?]{2,120})",
    r"يخضع\s+.{0,160}?\s+لقانون\s+([^\.\n،؛!?]{2,120})",
    r"يخضع\s+.{0,160}?\s+لقوانين\s+([^\.\n،؛!?]{2,120})",
    r"تسري\s+(?:أحكام\s+)?قوانين?\s+([^\.\n،؛!?]{2,120})",
    r"يحكم\s+.{0,160}?\s+قانون\s+([^\.\n،؛!?]{2,120})",
    r"القانون\s+الواجب\s+التطبيق.*?(?:هو|:)\s*([^\.\n،؛!?]{2,120})",
]


DISPUTE_FORUM_PATTERNS = [
    # EN — prefer concrete court/forum locations before generic jurisdiction wording.
    r"(?:state\s+and\s+federal|state\s+or\s+federal)\s+courts?\s+located\s+in\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s,'’()-]{1,120})",
    r"courts?\s+located\s+in\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s,'’()-]{1,120})",
    r"courts?\s+sitting\s+in\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s,'’()-]{1,120})",
    r"(?:submit|submits|submitted|irrevocably\s+submit)\b.{0,120}\b(?:exclusive\s+)?jurisdiction\s+of\s+the\s+courts?\s+(?:of|in)\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s,'’()-]{1,120})",
    r"(?:agree|agrees)\b.{0,120}\b(?:exclusive\s+)?jurisdiction\s+of\s+the\s+courts?\s+(?:of|in)\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s,'’()-]{1,120})",
    r"exclusive\s+jurisdiction\s+of\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s,'’()-]{1,180})",
    r"submitted\s+to\s+the\s+jurisdiction\s+of\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s,'’()-]{1,180})",

    # FR — concrete court/forum locations before generic jurisdiction wording.
    r"tribunaux?\s+(?:situ[eé]s?|sis)\s+[aà]\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s,'’()-]{1,120})",
    r"tribunaux?\s+de\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s,'’()-]{1,160})",
    r"juridiction\s+exclusive\s+(?:des?|de\s+la)\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s,'’()-]{1,180})",
    r"soumis(?:e|es|s)?\s+[aà]\s+la\s+juridiction\s+de\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s,'’()-]{1,180})",

    # AR — concrete court locations first.
    r"(?:المحاكم|محاكم)\s+(?:الولائية\s+والفيدرالية|الفيدرالية\s+والولائية)"
    r"\s+الواقعة\s+في\s+([^\.\n؛!?]{2,120})",

    r"(?:المحاكم|محاكم)\s+(?:الواقعة|الكائنة|الموجودة)\s+في\s+"
    r"([^\.\n؛!?]{2,120})",

    r"الاختصاص\s+القضائي\s+الحصري\s+ل(?:لمحاكم|محاكم).*?"
    r"(?:الواقعة|الكائنة|الموجودة)\s+في\s+([^\.\n؛!?]{2,120})",

    # Generic fallbacks only after concrete patterns.
    r"الاختصاص\s+الحصري\s+(?:لمحاكم|لدى\s+محاكم)\s+([^\.\n،؛!?]{2,120})",
    r"محاكم\s+([^\.\n،؛!?]{2,120})",
    r"الاختصاص.*?لـ\s*([^\.\n،؛!?]{2,120})",
]


ARBITRATION_SEAT_PATTERNS = [
    r"seat of arbitration shall be\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",
    r"seat shall be\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",
    r"place of arbitration shall be\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",
    r"arbitration.*?in\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",

    r"siège de l'arbitrage sera\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",
    r"siège de l’arbitrage sera\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",
    r"lieu de l'arbitrage sera\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",
    r"arbitrage.*?à\s+((?:[A-Za-zÀ-ÿ\s,'-]|\.(?!\s))+)",

    r"مقر التحكيم.*?(?:هو|في|:)\s*([^\.\n،,؛]{2,80})",
    r"مكان التحكيم.*?(?:هو|في|:)\s*([^\.\n،,؛]{2,80})",
    r"التحكيم.*?في\s+([^\.\n،,؛]{2,80})",
]


def normalize_language(language: str) -> str:
    language = str(language or "en").lower().strip()
    return language if language in {"en", "fr", "ar"} else "en"


def normalize_text(text: str) -> str:
    text = str(text or "").lower()
    text = text.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", text).strip()


def clean_candidate(value: str) -> str:
    value = str(value or "").strip(" .,:;،؛\n\t")
    value = re.sub(r"\s+", " ", value)

    # Avoid runaway captures without cutting valid international names such as
    # "England and Wales", "Trinidad and Tobago", "state and federal courts",
    # "Bosnie-Herzégovine et ..." or Arabic names containing conjunctions.
    for stopper in [
        " except ", " provided that ", " subject to ", " before ",
        " under this agreement", " under the agreement",
        " sauf ", " sous réserve ", " avant ",
        " au titre du présent contrat", " aux termes du présent contrat",
        " باستثناء ", " شريطة ", " قبل ",
        " بموجب هذا الاتفاق", " بموجب الاتفاق",
        " دون اعتبار ", " دون الإخلال ", " مع عدم الإخلال ",
    ]:
        idx = value.lower().find(stopper)
        if idx > 5:
            value = value[:idx].strip()

    return value.strip(" .,:;،؛")


INVALID_CANDIDATES = {
    "a", "an", "the", "of", "in", "to", "for", "by", "and", "or",
    "le", "la", "les", "de", "du", "des", "un", "une", "et",
    "في", "من", "إلى", "على", "و",
}


INDIRECT_REFERENCE_PATTERNS = (
    r"\bsection\s+\d+(?:\.\d+)?\b",
    r"\barticle\s+\d+(?:\.\d+)?\b",
    r"\bclause\s+\d+(?:\.\d+)?\b",
    r"\bspecified\s+in\b",
    r"\bset\s+forth\s+in\b",
    r"\bprovided\s+in\b",
    r"\bsection\s+ci-dessus\b",
    r"\barticle\s+ci-dessus\b",
    r"\bpr[eé]vu(?:e|es|s)?\s+[aà]\s+l['’]article\b",
    r"\bvis[eé](?:e|es|s)?\s+[aà]\s+l['’]article\b",
    r"(?:القسم|المادة|البند)\s+\d+(?:\.\d+)?",
    r"(?:المحدد|المنصوص)\s+عليه\s+في",
)


def normalize_candidate_value(
    value: str,
    candidate_kind: str,
) -> str:
    value = clean_candidate(value)

    if candidate_kind == "dispute_forum":
        trailing_patterns = (
            r"\s+shall\s+have\s+(?:exclusive\s+)?jurisdiction\b.*$",
            r"\s+have\s+(?:exclusive\s+)?jurisdiction\b.*$",
            r"\s+(?:auront?|aura)\s+(?:la\s+)?comp[eé]tence\s+exclusive\b.*$",
            r"\s+seront?\s+seuls?\s+comp[eé]tents?\b.*$",
            r"\s+(?:حصرياً|حصريًا|حصريا)\b.*$",
            r"\s+دون\s+غيرها\b.*$",
        )

        for pattern in trailing_patterns:
            value = re.sub(
                pattern,
                "",
                value,
                flags=re.IGNORECASE,
            ).strip()

    return value.strip(" .,:;،؛")


def is_valid_candidate(
    value: str,
    candidate_kind: str = "generic",
) -> bool:
    normalized = normalize_text(value)

    if not normalized:
        return False

    if normalized in INVALID_CANDIDATES:
        return False

    if len(normalized) < 3:
        return False

    if any(
        re.search(pattern, normalized, flags=re.IGNORECASE)
        for pattern in INDIRECT_REFERENCE_PATTERNS
    ):
        return False

    # Reject candidates made only of punctuation / digits.
    if not re.search(r"[A-Za-zÀ-ÿ\u0600-\u06FF]", normalized):
        return False

    if candidate_kind == "dispute_forum":
        generic_forum_references = (
            # EN
            r"\bcompetent\s+jurisdiction\b",
            r"\bcourts?\s+of\s+competent\s+jurisdiction\b",
            r"\bappropriate\s+jurisdiction\b",
            r"\bcourts?\s+of\s+law\b",
            r"\bcompetent\s+courts?\b",

            # FR
            r"\bjuridiction\s+comp[eé]tente\b",
            r"\btribunaux?\s+comp[eé]tents?\b",
            r"\bjuridiction\s+appropri[eé]e\b",

            # AR
            r"(?:المحكمة|محكمة)\s+المختصة",
            r"(?:المحاكم|محاكم)\s+المختصة",
            r"الجهة\s+القضائية\s+المختصة",
            r"الاختصاص\s+القضائي\s+المختص",
        )

        if any(
            re.search(pattern, normalized, flags=re.IGNORECASE)
            for pattern in generic_forum_references
        ):
            return False

    return True


def _candidate_score(value: str, candidate_kind: str) -> float:
    normalized = normalize_text(value)
    score = 0.0

    country = detect_country_from_value(value)
    if country:
        score += 4.0

    if "," in value:
        score += 1.0

    word_count = len(re.findall(r"[A-Za-zÀ-ÿ\u0600-\u06FF]+", value))
    if 2 <= word_count <= 14:
        score += 1.0
    elif word_count > 24:
        score -= 3.0

    if candidate_kind == "dispute_forum":
        # Do not reward generic words such as "courts", "jurisdiction",
        # "tribunaux" or "محاكم". Those tokens can make a broad capture beat
        # a cleaner concrete location. Country/location evidence and ordered
        # pattern specificity are stronger international signals.
        pass

    elif candidate_kind == "governing_law":
        if re.search(
            r"\b(?:state|laws?|law|droit|loi|royaume|kingdom|republic)\b|"
            r"(?:قانون|قوانين|دولة|مملكة|جمهورية)",
            normalized,
            flags=re.IGNORECASE,
        ):
            score += 2.0

    elif candidate_kind == "arbitration_seat":
        if re.search(
            r"\b(?:seat|place|city|si[eè]ge|lieu|ville)\b|"
            r"(?:مقر|مكان|مدينة)",
            normalized,
            flags=re.IGNORECASE,
        ):
            score += 2.0

    return score


def find_pattern_value(
    text: str,
    patterns: list[str],
    candidate_kind: str = "generic",
) -> tuple[str | None, str | None]:
    candidates: list[tuple[float, int, int, str, str]] = []

    for pattern_index, pattern in enumerate(patterns):
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            value = normalize_candidate_value(
                match.group(1),
                candidate_kind,
            )

            if not is_valid_candidate(value, candidate_kind):
                continue

            score = _candidate_score(value, candidate_kind)

            # Pattern lists are ordered from more concrete/specific wording to
            # broader fallback wording. Reward earlier patterns so a precise
            # location capture beats a longer generic jurisdiction phrase.
            score += max(0.0, 16.0 - pattern_index * 3.0)

            candidates.append(
                (
                    score,
                    -pattern_index,
                    len(value),
                    value,
                    match.group(0),
                )
            )

    if not candidates:
        return None, None

    candidates.sort(
        key=lambda item: (
            -item[0],
            -item[1],
            -item[2],
        )
    )

    _, _, _, value, signal = candidates[0]
    return value, signal


def contains_alias(text: str, alias: str) -> bool:
    text = normalize_text(text)
    alias = normalize_text(alias)

    if not text or not alias:
        return False

    pattern = rf"(?<![\w]){re.escape(alias)}(?![\w])"
    return bool(re.search(pattern, text, flags=re.IGNORECASE))


def detect_country_from_value(value: str) -> str | None:
    normalized = normalize_text(value)

    if not normalized:
        return None

    best = None
    best_len = 0

    for country, aliases in COUNTRY_ALIASES.items():
        for alias in aliases:
            alias_norm = normalize_text(alias)
            if (
                alias_norm
                and contains_alias(normalized, alias_norm)
                and len(alias_norm) > best_len
            ):
                best = country
                best_len = len(alias_norm)

    return best


def detect_all_country_mentions(text: str) -> list[dict]:
    normalized = normalize_text(text)
    matches = []

    for country, aliases in COUNTRY_ALIASES.items():
        matched = [
            alias
            for alias in aliases
            if contains_alias(normalized, alias)
        ]

        if matched:
            matches.append({
                "country": country,
                "matched_signals": sorted(set(matched)),
                "legal_system": LEGAL_SYSTEM_OVERRIDES.get(country, "unknown"),
            })

    return matches


def detect_arbitration_institution(text: str) -> tuple[str | None, list[str]]:
    normalized = normalize_text(text)

    for institution, signals in ARBITRATION_INSTITUTIONS.items():
        matched = [
            signal
            for signal in signals
            if normalize_text(signal) in normalized
        ]

        if matched:
            return institution, matched

    return None, []


def localized_unknown(language: str) -> str:
    language = normalize_language(language)

    if language == "fr":
        return "Non spécifié"

    if language == "ar":
        return "غير محدد"

    return "Not specified"


def build_jurisdiction_notes(
    result: dict,
    language: str = "en",
) -> list[str]:
    language = normalize_language(language)
    notes = []

    if language == "fr":
        if result.get("governing_law"):
            notes.append("Le droit applicable est identifié à partir du texte contractuel.")
        else:
            notes.append("Le contrat ne précise pas clairement le droit applicable.")

        if result.get("arbitration_institution") or result.get("arbitration_seat"):
            notes.append("Le contrat contient des éléments d'arbitrage ; le siège, l'institution et les règles doivent être lus ensemble.")

        notes.append("Les effets juridiques précis dépendent du droit applicable et des règles impératives locales.")

    elif language == "ar":
        if result.get("governing_law"):
            notes.append("تم تحديد القانون الواجب التطبيق من نص العقد.")
        else:
            notes.append("لا يحدد العقد بوضوح القانون الواجب التطبيق.")

        if result.get("arbitration_institution") or result.get("arbitration_seat"):
            notes.append("يتضمن العقد عناصر تحكيم؛ يجب قراءة المقر والمؤسسة والقواعد معاً.")

        notes.append("تعتمد الآثار القانونية الدقيقة على القانون الواجب التطبيق والقواعد المحلية الآمرة.")

    else:
        if result.get("governing_law"):
            notes.append("Governing law is identified from the contract text.")
        else:
            notes.append("The contract does not clearly specify governing law.")

        if result.get("arbitration_institution") or result.get("arbitration_seat"):
            notes.append("The contract contains arbitration mechanics; seat, institution, and rules should be read together.")

        notes.append("Precise legal effects depend on governing law and mandatory local rules.")

    return notes


def detect_jurisdiction(
    text: str,
    language: str = "en",
) -> dict[str, Any]:

    language = normalize_language(language)
    normalized = normalize_text(text)

    if not normalized:
        return {
            "name": "generic",
            "legal_system": "unknown",
            "languages": [],
            "governing_law": None,
            "governing_law_country": None,
            "dispute_forum": None,
            "dispute_forum_country": None,
            "arbitration_seat": None,
            "arbitration_seat_country": None,
            "arbitration_institution": None,
            "matched_signals": [],
            "country_mentions": [],
            "confidence": "low",
            "notes": [localized_unknown(language)],
        }

    governing_law, governing_signal = find_pattern_value(
        text,
        GOVERNING_LAW_PATTERNS,
        candidate_kind="governing_law",
    )

    dispute_forum, forum_signal = find_pattern_value(
        text,
        DISPUTE_FORUM_PATTERNS,
        candidate_kind="dispute_forum",
    )

    arbitration_seat, seat_signal = find_pattern_value(
        text,
        ARBITRATION_SEAT_PATTERNS,
        candidate_kind="arbitration_seat",
    )

    institution, institution_signals = detect_arbitration_institution(text)

    governing_country = detect_country_from_value(governing_law)
    forum_country = detect_country_from_value(dispute_forum)
    seat_country = detect_country_from_value(arbitration_seat)

    country_mentions = detect_all_country_mentions(text)

    primary_country = (
        governing_country
        or seat_country
        or forum_country
        or (country_mentions[0]["country"] if country_mentions else None)
    )

    matched_signals = []

    for signal in [
        governing_signal,
        forum_signal,
        seat_signal,
        *institution_signals,
    ]:
        if signal:
            matched_signals.append(signal)

    score = 0

    if governing_law:
        score += 3

    if arbitration_seat:
        score += 2

    if dispute_forum:
        score += 2

    if institution:
        score += 2

    if country_mentions:
        score += 1

    if score >= 5:
        confidence = "high"
    elif score >= 2:
        confidence = "medium"
    else:
        confidence = "low"

    result = {
        "name": primary_country or "generic",
        "legal_system": LEGAL_SYSTEM_OVERRIDES.get(primary_country, "unknown") if primary_country else "unknown",
        "languages": [],
        "governing_law": governing_law,
        "governing_law_country": governing_country,
        "dispute_forum": dispute_forum,
        "dispute_forum_country": forum_country,
        "arbitration_seat": arbitration_seat,
        "arbitration_seat_country": seat_country,
        "arbitration_institution": institution,
        "matched_signals": matched_signals,
        "country_mentions": country_mentions,
        "confidence": confidence,
        "notes": [],
    }

    result["notes"] = build_jurisdiction_notes(result, language)

    return result


def summarize_jurisdiction_detection(
    detection: dict,
    language: str = "en",
) -> str:
    language = normalize_language(language)

    governing = detection.get("governing_law")
    seat = detection.get("arbitration_seat")
    forum = detection.get("dispute_forum")
    institution = detection.get("arbitration_institution")

    parts = []

    if language == "fr":
        if governing:
            parts.append(f"Droit applicable : {governing}.")
        if seat:
            parts.append(f"Siège de l'arbitrage : {seat}.")
        if forum:
            parts.append(f"Forum judiciaire : {forum}.")
        if institution:
            parts.append(f"Institution d'arbitrage : {institution}.")
        return " ".join(parts) or "Aucune juridiction précise n'est clairement détectée."

    if language == "ar":
        if governing:
            parts.append(f"القانون الواجب التطبيق: {governing}.")
        if seat:
            parts.append(f"مقر التحكيم: {seat}.")
        if forum:
            parts.append(f"جهة التقاضي: {forum}.")
        if institution:
            parts.append(f"مؤسسة التحكيم: {institution}.")
        return " ".join(parts) or "لم يتم تحديد ولاية قضائية واضحة."

    if governing:
        parts.append(f"Governing law: {governing}.")
    if seat:
        parts.append(f"Arbitration seat: {seat}.")
    if forum:
        parts.append(f"Dispute forum: {forum}.")
    if institution:
        parts.append(f"Arbitration institution: {institution}.")

    return " ".join(parts) or "No clear jurisdiction is detected."

def format_jurisdiction_fields(
    detection: dict,
    language: str = "en",
) -> dict:
    language = normalize_language(language)

    seat = detection.get("arbitration_seat")
    institution = detection.get("arbitration_institution")
    forum = detection.get("dispute_forum")
    governing = detection.get("governing_law")

    jurisdiction = seat or forum or governing or localized_unknown(language)

    if language == "fr":
        if seat and institution:
            note = f"Le contrat prévoit un arbitrage {institution} avec siège à {seat}."
        elif seat:
            note = f"Le contrat prévoit un arbitrage avec siège à {seat}."
        elif forum:
            note = f"Les litiges sont soumis au forum suivant : {forum}."
        elif governing:
            note = f"Le droit applicable identifié est : {governing}."
        else:
            note = "Aucune juridiction précise n'est clairement détectée."

    elif language == "ar":
        if seat and institution:
            note = f"ينص العقد على تحكيم لدى {institution} يكون مقره في {seat}."
        elif seat:
            note = f"ينص العقد على تحكيم يكون مقره في {seat}."
        elif forum:
            note = f"تُحال النزاعات إلى الجهة التالية: {forum}."
        elif governing:
            note = f"القانون الواجب التطبيق المحدد هو: {governing}."
        else:
            note = "لم يتم تحديد ولاية قضائية واضحة."

    else:
        if seat and institution:
            note = f"The agreement provides for {institution} arbitration seated in {seat}."
        elif seat:
            note = f"The agreement provides for arbitration seated in {seat}."
        elif forum:
            note = f"Disputes are submitted to the following forum: {forum}."
        elif governing:
            note = f"The identified governing law is: {governing}."
        else:
            note = "No clear jurisdiction is detected."

    return {
        "jurisdiction": jurisdiction,
        "jurisdiction_note": note,
    }