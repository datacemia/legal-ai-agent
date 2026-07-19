#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


TARGET = Path(
    "app/services/contract_agent/semantic_source_profile.py"
)

PATCH_BEGIN = "# BEGIN PATCH HIGH_FAILURES_MULTILANG_V1"
PATCH_END = "# END PATCH HIGH_FAILURES_MULTILANG_V1"


PATCH = r'''
# BEGIN PATCH HIGH_FAILURES_MULTILANG_V1
#
# Conservative international semantic augmentation.
#
# Design requirements:
# - generic across contract domains;
# - unified EN / FR / AR behavior;
# - cumulative legal conditions rather than isolated keywords;
# - additive only: existing mechanisms are never removed or replaced;
# - evidence-grounded;
# - idempotent mechanism insertion.
#

import re as _hf_re


_HF_WS_RE = _hf_re.compile(r"\s+")


def _hf_normalize_text(value):
    return _HF_WS_RE.sub(" ", str(value or "")).strip()


def _hf_search(pattern, text):
    return _hf_re.search(
        pattern,
        text,
        flags=_hf_re.IGNORECASE | _hf_re.UNICODE,
    )


def _hf_has(pattern, text):
    return _hf_search(pattern, text) is not None


def _hf_evidence(pattern, source_text):
    match = _hf_search(pattern, source_text)

    if match is None:
        return []

    return [{
        "text": match.group(0),
        "start": match.start(),
        "end": match.end(),
    }]


def _hf_existing_mechanism_kinds(profile):
    kinds = set()

    for key in (
        "ranked_material_mechanisms",
        "material_mechanisms",
        "mechanisms",
    ):
        values = profile.get(key) or []

        if not isinstance(values, list):
            continue

        for value in values:
            if isinstance(value, dict):
                kind = value.get("kind")

                if kind:
                    kinds.add(str(kind))

            elif isinstance(value, str):
                kinds.add(value)

    return kinds


def _hf_append_ranked_mechanism(
    profile,
    *,
    kind,
    evidence,
    semantic_role=None,
    candidate_primary_type=None,
    polarity=None,
    procedural_state=None,
):
    if kind in _hf_existing_mechanism_kinds(profile):
        return

    mechanisms = profile.get("ranked_material_mechanisms")

    if not isinstance(mechanisms, list):
        mechanisms = []
        profile["ranked_material_mechanisms"] = mechanisms

    mechanism = {
        "kind": kind,
        "semantic_role": semantic_role,
        "candidate_primary_type": candidate_primary_type,
        "primary_eligible": False,
        "polarity": polarity,
        "procedural_state": procedural_state,
        "source_evidence": evidence or [],
        "confidence": 0.97,
        "detection_source": "HIGH_FAILURES_MULTILANG_V1",
    }

    mechanisms.append(mechanism)


def _hf_detect_preemptive_right(source_text):
    """
    International pre-emptive / subscription right.

    Required cumulative structure:
    1. legal right or entitlement;
    2. acquisition or subscription;
    3. proportional or pro-rata allocation;
    4. newly issued securities.
    """
    text = _hf_normalize_text(source_text)

    right = _hf_has(
        r"""
        (?:
            \bright\s+to\b
            |
            \bentitled\s+to\b
            |
            \bshall\s+have\s+the\s+right\b
            |
            \bdroit\s+(?:de|d['’])\b
            |
            \baura\s+le\s+droit\b
            |
            \best\s+en\s+droit\b
            |
            يحق\s+ل
            |
            له\s+الحق
            |
            يكون\s+له\s+الحق
        )
        """,
        text,
    )

    acquisition = _hf_has(
        r"""
        (?:
            \bpurchas(?:e|ing)\b
            |
            \bsubscrib(?:e|ing)\b
            |
            \bacquir(?:e|ing)\b
            |
            \bacheter\b
            |
            \bacqu[eé]rir\b
            |
            \bsouscrire\b
            |
            شراء
            |
            اكتساب
            |
            الاكتتاب
        )
        """,
        text,
    )

    proportional = _hf_has(
        r"""
        (?:
            \bpro[\s-]?rata\b
            |
            \bproportion(?:al|ate)\b
            |
            \bproportionnelle?\b
            |
            \bau\s+prorata\b
            |
            \bquote-part\b
            |
            حصة(?:ه|ها|هم|هن)?\s+التناسبية
            |
            بنسبة\s+تتناسب
            |
            على\s+أساس\s+نسبي
        )
        """,
        text,
    )

    new_securities = _hf_has(
        r"""
        (?:
            \bnew(?:ly)?\s+(?:issued\s+)?securit(?:y|ies)\b
            |
            \bnew(?:ly)?\s+(?:issued\s+)?shares?\b
            |
            \bfuture\s+issuances?\b
            |
            \bnouveaux?\s+titres?\b
            |
            \btitres?\s+nouvellement\s+[ée]mis\b
            |
            \bnouvelles?\s+actions?\b
            |
            أوراق\s+مالية\s+جديدة
            |
            أسهم\s+جديدة
            |
            إصدارات?\s+جديدة
        )
        """,
        text,
    )

    if not (
        right
        and acquisition
        and proportional
        and new_securities
    ):
        return None

    evidence_pattern = r"""
        (?:
            right\s+to.{0,120}pro[\s-]?rata.{0,120}
            (?:new|issued).{0,40}(?:securities|shares)
            |
            droit.{0,120}(?:quote-part|prorata|proportionnelle?).{0,120}
            (?:nouveau|nouveaux|nouvelle|nouvelles).{0,40}
            (?:titre|titres|action|actions)
            |
            يحق.{0,120}(?:حصة|بنسبة).{0,120}
            (?:أوراق\s+مالية\s+جديدة|أسهم\s+جديدة|إصدارات?\s+جديدة)
        )
    """

    return _hf_evidence(evidence_pattern, text) or [{
        "text": text,
        "start": 0,
        "end": len(text),
    }]


def _hf_detect_appointment_right(source_text):
    """
    Generic appointment or designation right.

    Applies to boards, committees, representatives, experts,
    arbitrators and similar legally defined roles.
    """
    text = _hf_normalize_text(source_text)

    appointment = _hf_has(
        r"""
        (?:
            \bdesignat(?:e|ed|es|ing)\b
            |
            \bappoint(?:ed|s|ing)?\b
            |
            \bnominat(?:e|ed|es|ing)\b
            |
            \bselected\s+by\b
            |
            \bd[eé]sign[ée]s?\s+par\b
            |
            \bnomm[ée]s?\s+par\b
            |
            \bchoisi(?:e|s|es)?\s+par\b
            |
            يعين(?:ه|ها|هم|هن)?
            |
            يعيّن(?:ه|ها|هم|هن)?
            |
            يُعي[َّ]?ن
            |
            يسمي(?:ه|ها|هم|هن)?
            |
            يتم\s+تعيين
        )
        """,
        text,
    )

    role = _hf_has(
        r"""
        (?:
            \bdirectors?\b
            |
            \bboard\s+members?\b
            |
            \bcommittee\s+members?\b
            |
            \brepresentatives?\b
            |
            \bmanagers?\b
            |
            \bofficers?\b
            |
            \bexperts?\b
            |
            \barbitrators?\b
            |
            \badministrateurs?\b
            |
            \bmembres?\b
            |
            \brepr[eé]sentants?\b
            |
            \bdirigeants?\b
            |
            \bexperts?\b
            |
            \barbitres?\b
            |
            أعضاء
            |
            عضو
            |
            مدير
            |
            مديرين
            |
            ممثل
            |
            ممثلين
            |
            خبير
            |
            محكم
        )
        """,
        text,
    )

    appointer = _hf_has(
        r"""
        (?:
            \bby\s+the\b
            |
            \bby\s+(?:an?|each)\b
            |
            \bpar\s+l['’]\b
            |
            \bpar\s+les?\b
            |
            \bpar\s+un(?:e)?\b
            |
            يعين(?:ه|ها|هم|هن)?
            |
            يعيّن(?:ه|ها|هم|هن)?
            |
            من\s+قبل
            |
            يسمي(?:ه|ها|هم|هن)?
        )
        """,
        text,
    )

    if not (appointment and role and appointer):
        return None

    evidence_pattern = r"""
        (?:
            (?:designated|appointed|nominated|selected)\s+by
            |
            (?:désigné|désignés|désignée|désignées|
               nommé|nommés|nommée|nommées|
               choisi|choisis|choisie|choisies)\s+par
            |
            يعين(?:ه|ها|هم|هن)?
            |
            يعيّن(?:ه|ها|هم|هن)?
            |
            من\s+قبل
        )
    """

    return _hf_evidence(evidence_pattern, text) or [{
        "text": text,
        "start": 0,
        "end": len(text),
    }]


def _hf_detect_tag_participation(source_text):
    """
    Participation in a transfer on equivalent terms.

    All three conditions are required:
    - sale or transfer;
    - beneficiary participation;
    - same/equivalent terms.
    """
    text = _hf_normalize_text(source_text)

    transfer = _hf_has(
        r"""
        (?:
            \btransfer(?:red|s|ring)?\b
            |
            \bsale\b
            |
            \bsell(?:ing|s)?\b
            |
            \bdisposal\b
            |
            \bcession\b
            |
            \bc[eé]der\b
            |
            \bvente\b
            |
            تحويل
            |
            تنازل
            |
            بيع
        )
        """,
        text,
    )

    participation = _hf_has(
        r"""
        (?:
            \bparticipat(?:e|es|ed|ing)\s+in\b
            |
            \bjoin\s+(?:in\s+)?(?:the|such)\s+sale\b
            |
            \bparticiper\s+[àa]\b
            |
            \bprendre\s+part\s+[àa]\b
            |
            المشاركة\s+في
            |
            الانضمام\s+إلى
        )
        """,
        text,
    )

    same_terms = _hf_has(
        r"""
        (?:
            \bon\s+the\s+same\s+terms\b
            |
            \bon\s+equivalent\s+terms\b
            |
            \bunder\s+the\s+same\s+conditions\b
            |
            \baux\s+m[eê]mes\s+conditions\b
            |
            \bselon\s+les\s+m[eê]mes\s+modalit[eé]s\b
            |
            بنفس\s+الشروط
            |
            بالشروط\s+نفسها
            |
            بذات\s+الشروط
        )
        """,
        text,
    )

    if not (transfer and participation and same_terms):
        return None

    evidence_pattern = r"""
        (?:
            participat(?:e|es|ed|ing).{0,100}
            (?:same|equivalent)\s+(?:terms|conditions)
            |
            participer.{0,100}
            (?:mêmes\s+conditions|mêmes\s+modalités)
            |
            المشاركة.{0,100}
            (?:بنفس\s+الشروط|بالشروط\s+نفسها|بذات\s+الشروط)
        )
    """

    return _hf_evidence(evidence_pattern, text) or [{
        "text": text,
        "start": 0,
        "end": len(text),
    }]


def _hf_detect_reserved_matter_consent(source_text):
    """
    Generic reserved-matter consent or veto structure.

    Required:
    - prohibition/restriction on an obligated actor;
    - absence-of-consent formulation;
    - prior consent or approval;
    - at least one governed corporate, financial or material act.
    """
    text = _hf_normalize_text(source_text)

    prohibition = _hf_has(
        r"""
        (?:
            \bshall\s+not\b
            |
            \bmay\s+not\b
            |
            \bmust\s+not\b
            |
            \bshall\s+not\s+be\s+permitted\b
            |
            \bne\s+pourra\b
            |
            \bne\s+peut\b
            |
            \bne\s+devra\s+pas\b
            |
            \bil\s+est\s+interdit\b
            |
            لا\s+يجوز
            |
            لا\s+يحق
            |
            يمتنع\s+عن
        )
        """,
        text,
    )

    without_consent = _hf_has(
        r"""
        (?:
            \bwithout\b.{0,50}\bconsent\b
            |
            \bwithout\b.{0,50}\bapproval\b
            |
            \bsans\b.{0,50}\bconsentement\b
            |
            \bsans\b.{0,50}\bautorisation\b
            |
            دون.{0,50}موافقة
            |
            بدون.{0,50}موافقة
            |
            دون.{0,50}إذن
        )
        """,
        text,
    )

    prior = _hf_has(
        r"""
        (?:
            \bprior\b.{0,30}\b(?:written\s+)?(?:consent|approval)\b
            |
            \bconsentement\b.{0,30}\bpr[eé]alable\b
            |
            \bautorisation\b.{0,30}\bpr[eé]alable\b
            |
            \bpr[eé]alable\b.{0,30}\bconsentement\b
            |
            موافقة.{0,30}مسبقة
            |
            موافقة.{0,30}خطية
            |
            إذن.{0,30}مسبق
        )
        """,
        text,
    )

    governed_action = _hf_has(
        r"""
        (?:
            \bamend\b
            |
            \bauthori[sz]e\b
            |
            \bissue\b
            |
            \bincur\b
            |
            \bindebtedness\b
            |
            \bmerge\b
            |
            \bacquir(?:e|ing)\b
            |
            \bdispose\b
            |
            \bsell\b
            |
            \btransfer\b
            |
            \bbudget\b
            |
            \bdividend\b
            |
            \brelated[-\s]party\b
            |
            \bmodify\b
            |
            \bmodifier\b
            |
            \bcr[eé]er\b
            |
            \b[eé]mettre\b
            |
            \bcontracter\b
            |
            \bendettement\b
            |
            \bfusion\b
            |
            \bacquisition\b
            |
            \bc[eé]der\b
            |
            \bbudget\b
            |
            \bdividende\b
            |
            تعديل
            |
            إصدار
            |
            إنشاء
            |
            تحمل\s+مديونية
            |
            اقتراض
            |
            اندماج
            |
            استحواذ
            |
            بيع
            |
            تحويل
            |
            ميزانية
            |
            أرباح
        )
        """,
        text,
    )

    if not (
        prohibition
        and without_consent
        and prior
        and governed_action
    ):
        return None

    evidence_pattern = r"""
        (?:
            (?:shall\s+not|may\s+not|must\s+not)
            .{0,100}
            without.{0,60}(?:prior\s+)?(?:written\s+)?(?:consent|approval)
            |
            (?:ne\s+pourra|ne\s+peut|ne\s+devra\s+pas)
            .{0,100}
            sans.{0,60}(?:consentement|autorisation).{0,40}préalable
            |
            لا\s+يجوز.{0,120}
            دون.{0,60}موافقة.{0,40}(?:مسبقة|خطية)
        )
    """

    return _hf_evidence(evidence_pattern, text) or [{
        "text": text,
        "start": 0,
        "end": len(text),
    }]


def _hf_augment_profile(profile, source_text, language=None):
    if not isinstance(profile, dict):
        return profile

    preemptive_evidence = _hf_detect_preemptive_right(source_text)

    if preemptive_evidence:
        _hf_append_ranked_mechanism(
            profile,
            kind="PREEMPTIVE_RIGHT",
            evidence=preemptive_evidence,
            semantic_role="PREEMPTIVE_SUBSCRIPTION_RIGHT",
            candidate_primary_type="anti_dilution_preemptive_rights",
            polarity="RIGHT",
        )

    appointment_evidence = _hf_detect_appointment_right(source_text)

    if appointment_evidence:
        _hf_append_ranked_mechanism(
            profile,
            kind="APPOINTMENT_RIGHT",
            evidence=appointment_evidence,
            semantic_role="APPOINTMENT_OR_DESIGNATION",
            candidate_primary_type="governance",
            polarity="RIGHT",
        )

    tag_evidence = _hf_detect_tag_participation(source_text)

    if tag_evidence:
        _hf_append_ranked_mechanism(
            profile,
            kind="PARTICIPATION_OPTION",
            evidence=tag_evidence,
            semantic_role="PARTICIPATE_IN_SALE",
            candidate_primary_type="governance",
            polarity="OPTION",
        )

        _hf_append_ranked_mechanism(
            profile,
            kind="SAME_TERMS_RIGHT",
            evidence=tag_evidence,
            semantic_role="EQUIVALENT_TRANSFER_TERMS",
            candidate_primary_type="governance",
            polarity="RIGHT",
        )

    consent_evidence = _hf_detect_reserved_matter_consent(
        source_text
    )

    if consent_evidence:
        _hf_append_ranked_mechanism(
            profile,
            kind="INVESTOR_CONSENT_RIGHT",
            evidence=consent_evidence,
            semantic_role="RESERVED_MATTER_CONSENT",
            candidate_primary_type="governance",
            polarity="CONSENT_RIGHT",
            procedural_state="PRIOR_APPROVAL",
        )

        _hf_append_ranked_mechanism(
            profile,
            kind="RESERVED_MATTER",
            evidence=consent_evidence,
            semantic_role="GOVERNED_RESERVED_ACTION",
            candidate_primary_type="governance",
            polarity="RESTRICTION",
            procedural_state="CONSENT_REQUIRED",
        )

    return profile


# Wrap the existing public function without changing its original logic.
_hf_original_build_semantic_source_profile = (
    build_semantic_source_profile
)


def build_semantic_source_profile(
    source_text,
    language=None,
    *args,
    **kwargs,
):
    profile = _hf_original_build_semantic_source_profile(
        source_text,
        language=language,
        *args,
        **kwargs,
    )

    return _hf_augment_profile(
        profile,
        source_text,
        language=language,
    )


# END PATCH HIGH_FAILURES_MULTILANG_V1
'''


def main() -> int:
    if not TARGET.exists():
        print(f"ERROR: target file not found: {TARGET}")
        return 2

    original = TARGET.read_text(encoding="utf-8")

    if PATCH_BEGIN in original:
        print("PATCH ALREADY PRESENT")
        print("TARGET:", TARGET)
        return 0

    if "def build_semantic_source_profile" not in original:
        print(
            "ERROR: build_semantic_source_profile() "
            "not found in target"
        )
        return 3

    backup = TARGET.with_suffix(
        TARGET.suffix + ".before_high_failures_multilang_v1"
    )

    if not backup.exists():
        shutil.copy2(TARGET, backup)

    patched = original.rstrip() + "\n\n" + PATCH.strip() + "\n"

    TARGET.write_text(
        patched,
        encoding="utf-8",
    )

    print("=" * 78)
    print("MULTILINGUAL SEMANTIC PATCH APPLIED")
    print("=" * 78)
    print("TARGET :", TARGET)
    print("BACKUP :", backup)
    print("PATCH  : HIGH_FAILURES_MULTILANG_V1")
    print()
    print("Added conservative recognition for:")
    print("- PREEMPTIVE_RIGHT")
    print("- APPOINTMENT_RIGHT")
    print("- PARTICIPATION_OPTION")
    print("- SAME_TERMS_RIGHT")
    print("- INVESTOR_CONSENT_RIGHT")
    print("- RESERVED_MATTER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
