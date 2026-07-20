from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class PurposeLimitationMatch:
    concept: str
    language: str
    evidence: str
    start: int
    end: int
    confidence: float


CONCEPT: Final[str] = "PURPOSE_LIMITATION"

# Les motifs restent indépendants du domaine contractuel.
# Ils exigent :
# - une action d'usage ou assimilée ;
# - un marqueur exclusif ;
# - une finalité exprimée.
_PATTERNS: Final[dict[str, tuple[re.Pattern[str], ...]]] = {
    "en": (
        re.compile(
            r"\b(?:shall|must|may|will|is\s+permitted\s+to)\s+"
            r"(?:use|access|process|disclose|occupy|exploit|apply)\b"
            r".{0,180}?"
            r"\b(?:solely|only|exclusively)\s+"
            r"(?:for|to)\b.{2,160}",
            re.IGNORECASE | re.DOTALL,
        ),
        re.compile(
            r"\b(?:shall|must|may)\s+"
            r"(?:not\s+)?(?:use|access|process|disclose|occupy|exploit)\b"
            r".{0,180}?"
            r"\bfor\s+no\s+purpose\s+other\s+than\b.{2,160}",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    "fr": (
        re.compile(
            r"\b(?:devra|doit|pourra|peut|utilisera|traitera|occupera|divulguera)\b"
            r".{0,180}?"
            r"\b(?:uniquement|exclusivement|seulement)\b"
            r".{0,40}?"
            r"\b(?:pour|à\s+des\s+fins\s+(?:de|d[’'])|aux\s+fins\s+(?:de|d[’']))\b.{2,160}",
            re.IGNORECASE | re.DOTALL,
        ),
        re.compile(
            r"\b(?:ne\s+peut|ne\s+pourra|ne\s+doit|ne\s+devra)\b"
            r".{0,80}?"
            r"\b(?:utiliser|traiter|occuper|divulguer|exploiter|accéder)\b"
            r".{0,180}?"
            r"(?:"
            r"\bque\b.{0,40}?"
            r"(?:pour|à\s+des\s+fins\s+(?:de|d[’'])|aux\s+fins\s+(?:de|d[’']))"
            r"|qu[’']\s*(?:aux?\s+fins\s+(?:de|d[’'])|à\s+des\s+fins\s+(?:de|d[’']))"
            r")"
            r".{2,160}",
            re.IGNORECASE | re.DOTALL,
        ),
        re.compile(
            r"\b(?:utiliser|traiter|occuper|divulguer|exploiter|accéder)\b"
            r".{0,180}?"
            r"\b(?:aux\s+seules\s+fins\s+de|exclusivement\s+à\s+des\s+fins\s+(?:de|d[’']))\b"
            r".{2,160}",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    "ar": (
        re.compile(
            r"(?:يستخدم|تستخدم|استخدام|يعالج|تعالج|معالجة|يشغل|تشغل|يفصح|تفصح)"
            r".{0,180}?"
            r"(?:حصراً|حصرا|فقط)"
            r".{0,50}?"
            r"(?:لغرض|لأغراض|للأغراض|من\s+أجل)"
            r".{2,160}",
            re.DOTALL,
        ),
        re.compile(
            r"(?:لا\s+يجوز|لا\s+يحق)"
            r".{0,100}?"
            r"(?:استخدام|معالجة|إفشاء|الافصاح|الإفصاح|شغل|استغلال)"
            r".{0,180}?"
            r"(?:إلا|الا)"
            r".{0,50}?"
            r"(?:لغرض|لأغراض|للأغراض|من\s+أجل)"
            r".{2,160}",
            re.DOTALL,
        ),
    ),
}

# Rejets explicites pour éviter les titres, définitions et phrases descriptives.
_NEGATIVE_PATTERNS: Final[dict[str, tuple[re.Pattern[str], ...]]] = {
    "en": (
        re.compile(r"^\s*(?:purpose|objectives?)\s+of\b", re.IGNORECASE),
        re.compile(r"\bthe\s+purpose\s+of\s+(?:this|the)\b", re.IGNORECASE),
    ),
    "fr": (
        re.compile(r"^\s*(?:objet|finalité|objectif)\s+du\b", re.IGNORECASE),
        re.compile(r"\b(?:a|aura)\s+pour\s+objet\s+de\b", re.IGNORECASE),
    ),
    "ar": (
        re.compile(r"^\s*(?:الغرض|الهدف|موضوع)\s+من\b"),
        re.compile(r"(?:الغرض|الهدف)\s+من\s+(?:هذا|هذه)\b"),
    ),
}


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.replace("\u200f", " ").replace("\u200e", " ")
    return re.sub(r"\s+", " ", normalized).strip()


def detect_purpose_limitation(
    text: str,
    language: str,
) -> list[PurposeLimitationMatch]:
    if not isinstance(text, str) or not text.strip():
        return []

    language = language.lower().strip()
    if language not in _PATTERNS:
        return []

    normalized = _normalize(text)

    if any(pattern.search(normalized) for pattern in _NEGATIVE_PATTERNS[language]):
        return []

    matches: list[PurposeLimitationMatch] = []

    for pattern in _PATTERNS[language]:
        match = pattern.search(normalized)
        if not match:
            continue

        evidence = match.group(0).strip()

        matches.append(
            PurposeLimitationMatch(
                concept=CONCEPT,
                language=language,
                evidence=evidence,
                start=match.start(),
                end=match.end(),
                confidence=0.95,
            )
        )
        break

    return matches
