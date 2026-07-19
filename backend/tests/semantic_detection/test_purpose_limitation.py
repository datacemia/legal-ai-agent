import pytest

from app.services.contract_agent.semantic_detection.purpose_limitation import detect_purpose_limitation


@pytest.mark.parametrize(
    ("language", "text"),
    [
        (
            "en",
            "Tenant shall use the Premises solely for general office and design studio purposes.",
        ),
        (
            "en",
            "Recipient may use Confidential Information only for evaluating the Transaction.",
        ),
        (
            "en",
            "The licensee shall process the data exclusively for providing the Services.",
        ),
        (
            "fr",
            "Le Preneur utilisera les Locaux exclusivement à des fins de bureaux.",
        ),
        (
            "fr",
            "Le prestataire traitera les données uniquement pour fournir les Services.",
        ),
        (
            "fr",
            "Le Destinataire ne peut utiliser les Informations Confidentielles qu'aux fins d'évaluer l'Opération.",
        ),
        (
            "fr",
            "Le Destinataire ne peut utiliser les Informations Confidentielles qu’aux fins d’évaluer l’Opération.",
        ),
        (
            "fr",
            "Le Destinataire ne peut utiliser les Informations Confidentielles qu'aux fins de l'évaluation de l'Opération.",
        ),
        (
            "ar",
            "يستخدم المستأجر المباني حصراً لأغراض المكاتب.",
        ),
        (
            "ar",
            "يعالج مقدم الخدمة البيانات فقط لغرض تقديم الخدمات.",
        ),
        (
            "ar",
            "لا يجوز للمستلم استخدام المعلومات السرية إلا لغرض تقييم الصفقة.",
        ),
    ],
)
def test_detects_purpose_limitation(language: str, text: str) -> None:
    matches = detect_purpose_limitation(text, language)

    assert len(matches) == 1
    assert matches[0].concept == "PURPOSE_LIMITATION"
    assert matches[0].language == language
    assert matches[0].confidence >= 0.95
    assert matches[0].evidence


@pytest.mark.parametrize(
    ("language", "text"),
    [
        ("en", "Purpose of this Agreement."),
        ("en", "The purpose of this section is to describe the Services."),
        ("en", "The Company develops software for healthcare purposes."),
        ("en", "The Premises may be used for commercial activities."),
        ("fr", "Objet du présent Contrat."),
        ("fr", "La présente section a pour objet de décrire les Services."),
        ("fr", "La Société développe des logiciels à des fins médicales."),
        ("fr", "Les Locaux peuvent être utilisés pour des activités commerciales."),
        ("ar", "الغرض من هذه الاتفاقية."),
        ("ar", "الغرض من هذا القسم هو وصف الخدمات."),
        ("ar", "تطور الشركة برامج لأغراض الرعاية الصحية."),
        ("ar", "يجوز استخدام المباني للأنشطة التجارية."),
    ],
)
def test_rejects_non_limiting_purpose_language(
    language: str,
    text: str,
) -> None:
    assert detect_purpose_limitation(text, language) == []


@pytest.mark.parametrize("language", ["en", "fr", "ar"])
def test_rejects_empty_text(language: str) -> None:
    assert detect_purpose_limitation("", language) == []


def test_rejects_unsupported_language() -> None:
    assert detect_purpose_limitation(
        "Tenant shall use the Premises solely for office purposes.",
        "de",
    ) == []
