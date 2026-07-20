from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class TermDurationMatch:
    concept: str
    language: str
    evidence: str
    start: int
    end: int
    confidence: float


CONCEPT: Final[str] = "TERM_DURATION"


_DURATION_UNIT_EN = r"(?:days?|weeks?|months?|years?)"
_DURATION_UNIT_FR = r"(?:jours?|semaines?|mois|ans?|années?)"
_DURATION_UNIT_AR = (
    r"(?:"
    r"يوماً|يومًا|يوما|يوم|أيام|"
    r"أسبوعاً|أسبوعًا|أسبوعا|أسبوع|أسابيع|"
    r"شهراً|شهرًا|شهرا|شهر|أشهر|"
    r"سنة|سنوات|عاماً|عامًا|عاما|عام|أعوام"
    r")"
)

_NUMBER_EN = (
    r"(?:\d+|"
    r"one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
    r"seventeen|eighteen|nineteen|twenty|thirty|forty|"
    r"fifty|sixty|seventy|eighty|ninety)"
)

_NUMBER_FR = (
    r"(?:\d+|"
    r"un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|"
    r"onze|douze|treize|quatorze|quinze|seize|vingt|trente|"
    r"quarante|cinquante|soixante)"
)

_NUMBER_AR = (
    r"(?:[0-9٠-٩]+|"
    r"واحد(?:ة)?|اثنان|اثنتان|اثنين|اثنتين|"
    r"ثلاث(?:ة)?|أربع(?:ة)?|خمس(?:ة)?|ست(?:ة)?|"
    r"سبع(?:ة)?|ثمان(?:ية)?|تسع(?:ة)?|عشر(?:ة)?|"
    r"أحد\s+عشر|إحدى\s+عشرة|اثنا\s+عشر|اثنتا\s+عشرة)"
)


# Les formes duelles arabes portent directement la quantité « deux ».
# Elles doivent donc être reconnues sans exiger un nombre cardinal séparé.
_DUAL_DURATION_AR = (
    r"(?:"
    r"يومان|يومين|"
    r"أسبوعان|أسبوعين|"
    r"شهران|شهرين|"
    r"سنتان|سنتين|"
    r"عامان|عامين"
    r")"
)


# Les motifs exigent un rattachement explicite de la durée
# au contrat, à l'accord ou à sa période initiale.
_PATTERNS: Final[dict[str, tuple[re.Pattern[str], ...]]] = {
    "en": (
        re.compile(
            rf"\b(?:initial\s+)?term\s+of\s+"
            rf"(?:this|the)\s+"
            rf"(?!(?:warranty|notice|payment|renewal|confidentiality|"
            rf"survival|cure|remedy|inspection|reporting|response|"
            rf"audit|transition)\b)"
            rf"[a-z][a-z0-9'’_-]*"
            rf"(?:\s+[a-z][a-z0-9'’_-]*){{0,5}}\s+"
            rf"(?:is|shall\s+be|will\s+be)\s+"
            rf"(?:approximately\s+|up\s+to\s+)?"
            rf"{_NUMBER_EN}(?:\s+\(\d+\))?\s+"
            rf"{_DURATION_UNIT_EN}\b",
            re.IGNORECASE,
        ),
        re.compile(
            rf"\b(?:initial\s+)?term\s+"
            rf"(?:of\s+(?:this|the)\s+(?:agreement|contract)\s+)?"
            rf"(?:is|shall\s+be|will\s+be|of)\s+"
            rf"(?:approximately\s+|up\s+to\s+)?"
            rf"(?:[a-z]+(?:[-\s][a-z]+){{0,3}}\s+)?"
            rf"(?:\(\d+\)|{_NUMBER_EN})\s+{_DURATION_UNIT_EN}\b",
            re.IGNORECASE,
        ),
        re.compile(
            rf"\b(?:initial\s+)?term\s+of\s+"
            rf"{_NUMBER_EN}\s+{_DURATION_UNIT_EN}\b",
            re.IGNORECASE,
        ),
        re.compile(
            rf"\b(?:this|the)\s+(?:agreement|contract)\s+"
            rf"(?:shall|will)\s+remain\s+"
            rf"(?:in\s+effect|in\s+force|effective)\s+"
            rf"(?:for\s+)?{_NUMBER_EN}"
            rf"(?:\s+\(\d+\))?\s+{_DURATION_UNIT_EN}\b",
            re.IGNORECASE,
        ),
        re.compile(
            rf"\b(?:this|the)\s+(?:agreement|contract)\s+"
            rf"(?:is|shall\s+be|was)\s+"
            rf"(?:entered\s+into|concluded)\s+"
            rf"for\s+(?:a\s+period\s+of\s+)?"
            rf"{_NUMBER_EN}(?:\s+\(\d+\))?\s+"
            rf"{_DURATION_UNIT_EN}\b",
            re.IGNORECASE,
        ),
        re.compile(
            rf"\b(?:contract|agreement)\s+duration\s*"
            rf"(?:is|shall\s+be|:)\s*"
            rf"{_NUMBER_EN}(?:\s+\(\d+\))?\s+"
            rf"{_DURATION_UNIT_EN}\b",
            re.IGNORECASE,
        ),
    ),
    "fr": (
        re.compile(
            rf"\b(?:la\s+)?durée\s+(?:initiale\s+)?"
            rf"du\s+présent\s+"
            rf"(?!(?:préavis|garantie|paiement|renouvellement|"
            rf"confidentialité|survie|remédiation|correction|"
            rf"inspection|audit|réponse|transition|maintenance|"
            rf"support|assistance)\b)"
            rf"[\wàâäéèêëîïôöùûüçœ'’-]+"
            rf"(?:\s+[\wàâäéèêëîïôöùûüçœ'’-]+){{0,5}}\s+"
            rf"(?:est|sera)\s+de\s+"
            rf"{_NUMBER_FR}(?:\s+\(\d+\))?\s+"
            rf"{_DURATION_UNIT_FR}\b",
            re.IGNORECASE,
        ),
        re.compile(
            rf"\b(?:durée|période)\s+(?:initiale\s+)?"
            rf"(?:du\s+présent\s+(?:accord|contrat)\s+)?"
            rf"(?:est|sera|de)\s+"
            rf"(?:[\wàâäéèêëîïôöùûüçœ'-]+"
            rf"(?:\s+[\wàâäéèêëîïôöùûüçœ'-]+){{0,3}}\s+)?"
            rf"(?:\(\d+\)|{_NUMBER_FR})\s+{_DURATION_UNIT_FR}\b",
            re.IGNORECASE,
        ),
        re.compile(
            rf"\b(?:durée|période)\s+(?:initiale\s+)?"
            rf"(?:de|est|sera|:)\s*"
            rf"{_NUMBER_FR}(?:\s+\(\d+\))?\s+"
            rf"{_DURATION_UNIT_FR}\b",
            re.IGNORECASE,
        ),
        re.compile(
            rf"\b(?:le\s+présent|ce|le)\s+(?:contrat|accord)\s+"
            rf"(?:est|sera)\s+conclu\s+"
            rf"pour\s+(?:une\s+durée\s+de\s+)?"
            rf"{_NUMBER_FR}(?:\s+\(\d+\))?\s+"
            rf"{_DURATION_UNIT_FR}\b",
            re.IGNORECASE,
        ),
        re.compile(
            rf"\b(?:le\s+présent|ce|le)\s+(?:contrat|accord)\s+"
            rf"(?:demeure|restera|reste)\s+"
            rf"(?:en\s+vigueur|applicable|valable)\s+"
            rf"(?:pendant|pour)\s+"
            rf"{_NUMBER_FR}(?:\s+\(\d+\))?\s+"
            rf"{_DURATION_UNIT_FR}\b",
            re.IGNORECASE,
        ),
        re.compile(
            rf"\bdurée\s+(?:du\s+)?(?:contrat|accord)\s*"
            rf"(?:est|sera|:)\s*"
            rf"{_NUMBER_FR}(?:\s+\(\d+\))?\s+"
            rf"{_DURATION_UNIT_FR}\b",
            re.IGNORECASE,
        ),
    ),
    "ar": (
        re.compile(
            rf"(?:مدة|فترة)\s+"
            rf"(?:(?:أولية|ابتدائية)\s+)?"
            rf"(?:قدرها\s+)?"
            rf"(?:"
            rf"{_DUAL_DURATION_AR}(?:\s*\([0-9٠-٩]+\))?"
            rf"|"
            rf"{_NUMBER_AR}(?:\s*\([0-9٠-٩]+\))?\s*"
            rf"{_DURATION_UNIT_AR}"
            rf")",
        ),
        re.compile(
            rf"(?:مدة|فترة)"
            rf"[^.;؛!?]{{0,70}}"
            rf"(?:الأولية|الابتدائية)?"
            rf"[^.;؛!?]{{0,30}}"
            rf"(?:{_NUMBER_AR}\s*)?"
            rf"(?:\([0-9٠-٩]+\)|[0-9٠-٩]+)\s*"
            rf"{_DURATION_UNIT_AR}",
        ),
        re.compile(
            rf"(?:مدة|فترة)"
            rf"[^.;؛!?]{{0,70}}"
            rf"{_NUMBER_AR}\s*"
            rf"{_DURATION_UNIT_AR}",
        ),
        re.compile(
            rf"(?:يظل|يبقى|يستمر|تظل|تبقى|تستمر)"
            rf"[^.;؛!?]{{0,50}}"
            rf"(?:هذا\s+العقد|هذه\s+الاتفاقية|العقد|الاتفاقية)"
            rf"[^.;؛!?]{{0,60}}"
            rf"(?:سارياً|ساريًا|ساريا|نافذاً|نافذًا|نافذا)"
            rf"[^.;؛!?]{{0,30}}"
            rf"(?:لمدة|مدة)\s+"
            rf"{_NUMBER_AR}(?:\s*\([0-9٠-٩]+\))?\s*"
            rf"{_DURATION_UNIT_AR}",
        ),
        re.compile(
            rf"(?:أبرم|أُبرم|يبرم|تم\s+إبرام)"
            rf"[^.;؛!?]{{0,60}}"
            rf"(?:هذا\s+العقد|هذه\s+الاتفاقية|العقد|الاتفاقية)"
            rf"[^.;؛!?]{{0,40}}"
            rf"(?:لمدة|لفترة)\s+"
            rf"{_NUMBER_AR}(?:\s*\([0-9٠-٩]+\))?\s*"
            rf"{_DURATION_UNIT_AR}",
        ),
    ),
}


# Ces motifs représentent des durées juridiques voisines qui ne constituent
# pas la durée générale du contrat. Ils restent locaux au texte examiné.
_NEGATIVE_PATTERNS: Final[dict[str, tuple[re.Pattern[str], ...]]] = {
    "en": (
        re.compile(
            r"\b(?:payment|notice|warranty|cure|remedy|inspection|"
            r"retention|reporting|response|audit|transition|renewal|"
            r"confidentiality|survival|non[-\s]compete)\s+"
            r"(?:period|term|deadline|duration)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(?:after|following)\s+(?:termination|expiration)\b",
            re.IGNORECASE,
        ),
    ),
    "fr": (
        re.compile(
            r"\b(?:paiement|préavis|garantie|remédiation|correction|"
            r"inspection|conservation|audit|réponse|transition|"
            r"renouvellement|confidentialité|survie|maintenance|"
            r"support|assistance)\b"
            r".{0,40}\b(?:délai|période|durée)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(?:délai|période|durée)\s+(?:de|du|des|d['’])?\s*"
            r"(?:paiement|préavis|garantie|remédiation|correction|"
            r"inspection|conservation|audit|réponse|transition|"
            r"renouvellement|confidentialité|survie|maintenance|"
            r"support|assistance)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(?:après|suivant|à\s+compter\s+de)\s+"
            r"(?:la\s+)?(?:résiliation|expiration)\b",
            re.IGNORECASE,
        ),
    ),
    "ar": (
        re.compile(
            r"(?:الدفع|الإخطار|الضمان|المعالجة|التصحيح|التفتيش|"
            r"الاحتفاظ|التدقيق|الاستجابة|الانتقال|التجديد|"
            r"السرية|الصيانة|الدعم|المساعدة)"
            r".{0,40}(?:مهلة|فترة|مدة)",
        ),
        re.compile(
            r"(?:مهلة|فترة|مدة)"
            r".{0,20}"
            r"(?:الدفع|الإخطار|الضمان|المعالجة|التصحيح|التفتيش|"
            r"الاحتفاظ|التدقيق|الاستجابة|الانتقال|التجديد|"
            r"السرية|الصيانة|الدعم|المساعدة)",
        ),
        re.compile(
            r"(?:بعد|عقب)\s+(?:الإنهاء|انتهاء|الفسخ)",
        ),
    ),
}


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.replace("\u200f", " ").replace("\u200e", " ")
    return re.sub(r"\s+", " ", normalized).strip()


def detect_term_duration(
    text: str,
    language: str,
) -> list[TermDurationMatch]:
    if not isinstance(text, str) or not text.strip():
        return []

    language = language.lower().strip()
    if language not in _PATTERNS:
        return []

    normalized = _normalize(text)

    if any(
        pattern.search(normalized)
        for pattern in _NEGATIVE_PATTERNS[language]
    ):
        return []

    matches: list[TermDurationMatch] = []

    for pattern in _PATTERNS[language]:
        match = pattern.search(normalized)
        if not match:
            continue

        matches.append(
            TermDurationMatch(
                concept=CONCEPT,
                language=language,
                evidence=match.group(0).strip(),
                start=match.start(),
                end=match.end(),
                confidence=0.95,
            )
        )
        break

    return matches