import pytest

from app.services.contract_agent.normalized_legal_relation import (
    normalize_concept,
)
from app.services.contract_agent.semantic_source_profile import (
    extract_source_mechanisms,
)


RAW_CONCEPT = "LOAN_PRINCIPAL_DISBURSEMENT"
CANONICAL_CONCEPT = "LOAN_DISBURSEMENT"


def detected_raw_concepts(
    text: str,
    language: str,
) -> set[str]:
    mechanisms = extract_source_mechanisms(
        text,
        language=language,
    )

    return {
        str(
            mechanism.get("kind")
            or mechanism.get("concept")
            or mechanism.get("mechanism")
            or ""
        ).upper()
        for mechanism in mechanisms
    }


def detected_canonical_concepts(
    text: str,
    language: str,
) -> set[str]:
    return {
        normalize_concept(concept)
        for concept in detected_raw_concepts(
            text,
            language,
        )
    }


@pytest.mark.parametrize(
    ("language", "text"),
    [
        (
            "en",
            (
                "The lender shall disburse the principal "
                "amount of the loan to the borrower after "
                "the conditions precedent are satisfied."
            ),
        ),
        (
            "fr",
            (
                "Le prêteur décaissera le montant principal "
                "du prêt au profit de l’emprunteur après "
                "satisfaction des conditions préalables."
            ),
        ),
        (
            "ar",
            (
                "يصرف المُقرض المبلغ الأصلي للقرض إلى "
                "المقترض بعد استيفاء الشروط المسبقة."
            ),
        ),
    ],
)
def test_detects_standard_loan_disbursement(
    language: str,
    text: str,
) -> None:
    raw = detected_raw_concepts(text, language)
    canonical = detected_canonical_concepts(
        text,
        language,
    )

    assert RAW_CONCEPT in raw
    assert CANONICAL_CONCEPT in canonical


@pytest.mark.parametrize(
    ("language", "text"),
    [
        (
            "en",
            (
                "The facility proceeds will be made "
                "available to the obligor on the "
                "utilisation date."
            ),
        ),
        (
            "fr",
            (
                "Les fonds de la facilité seront mis à "
                "la disposition du débiteur à la date "
                "de tirage."
            ),
        ),
        (
            "ar",
            (
                "تتاح أموال التسهيل للمدين في تاريخ السحب."
            ),
        ),
    ],
)
def test_detects_alternative_disbursement_wording(
    language: str,
    text: str,
) -> None:
    concepts = detected_canonical_concepts(
        text,
        language,
    )

    assert CANONICAL_CONCEPT in concepts


@pytest.mark.parametrize(
    ("language", "text"),
    [
        (
            "en",
            (
                "The facility agent will transfer the "
                "loan proceeds to the designated account."
            ),
        ),
        (
            "fr",
            (
                "L’agent de la facilité transférera le "
                "produit du prêt sur le compte désigné."
            ),
        ),
        (
            "ar",
            (
                "يحول وكيل التسهيل حصيلة القرض إلى "
                "الحساب المحدد."
            ),
        ),
    ],
)
def test_detects_transfer_of_financing_proceeds(
    language: str,
    text: str,
) -> None:
    concepts = detected_canonical_concepts(
        text,
        language,
    )

    assert CANONICAL_CONCEPT in concepts


@pytest.mark.parametrize(
    ("language", "text"),
    [
        (
            "en",
            "Interest shall be payable monthly.",
        ),
        (
            "fr",
            "Les intérêts seront payables mensuellement.",
        ),
        (
            "ar",
            "تدفع الفائدة شهرياً.",
        ),
        (
            "en",
            (
                "The borrower shall repay the principal "
                "amount on the maturity date."
            ),
        ),
        (
            "fr",
            (
                "L’emprunteur remboursera le montant "
                "principal à la date d’échéance."
            ),
        ),
        (
            "ar",
            (
                "يسدد المقترض المبلغ الأصلي عند تاريخ "
                "الاستحقاق."
            ),
        ),
        (
            "en",
            (
                "The purchaser shall pay the purchase "
                "price to the seller at closing."
            ),
        ),
        (
            "fr",
            (
                "L’acquéreur versera le prix d’acquisition "
                "au vendeur à la réalisation."
            ),
        ),
        (
            "ar",
            (
                "يدفع المشتري ثمن الشراء إلى البائع "
                "عند الإقفال."
            ),
        ),
    ],
)
def test_does_not_confuse_other_payments_with_disbursement(
    language: str,
    text: str,
) -> None:
    concepts = detected_canonical_concepts(
        text,
        language,
    )

    assert CANONICAL_CONCEPT not in concepts


@pytest.mark.parametrize(
    ("language", "text"),
    [
        (
            "en",
            (
                "The lender shall disburse the principal "
                "amount of the loan. Interest shall be "
                "payable monthly."
            ),
        ),
        (
            "fr",
            (
                "Le prêteur décaissera le montant principal "
                "du prêt. Les intérêts seront payables "
                "mensuellement."
            ),
        ),
        (
            "ar",
            (
                "يصرف المقرض المبلغ الأصلي للقرض. "
                "وتدفع الفائدة شهرياً."
            ),
        ),
    ],
)
def test_disbursement_can_coexist_with_payment_frequency(
    language: str,
    text: str,
) -> None:
    raw = detected_raw_concepts(text, language)
    canonical = {
        normalize_concept(concept)
        for concept in raw
    }

    assert CANONICAL_CONCEPT in canonical
    assert "PAY_FREQUENCY" in raw
