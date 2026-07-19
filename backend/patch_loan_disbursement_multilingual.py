from pathlib import Path
import shutil
import sys

TARGET = Path(
    "app/services/contract_agent/"
    "semantic_source_profile.py"
)

BACKUP = TARGET.with_suffix(
    ".py.before_loan_disbursement_multilingual"
)

START_MARKER = '    _r("LOAN_PRINCIPAL_DISBURSEMENT",'
END_MARKER = '    _r("ACCELERATION_ON_DEFAULT",'

NEW_BLOCK = r'''    _r(
        "LOAN_PRINCIPAL_DISBURSEMENT",
        (
            # EN — direct disbursement of loan/facility proceeds.
            (
                r"\b(?:lender|facility\s+agent|creditor)\b"
                r".{0,120}"
                r"\b(?:shall|must|will|may)\b"
                r".{0,40}"
                r"\b(?:disburse|advance|fund|release|transfer)\b"
                r".{0,160}"
                r"\b(?:loan\s+proceeds|facility\s+proceeds|"
                r"credit\s+proceeds|principal\s+amount|"
                r"amount\s+of\s+the\s+(?:loan|facility)|"
                r"funds\s+under\s+the\s+(?:loan|facility))\b"
            ),
            # EN — proceeds/funds made available to the borrower.
            (
                r"\b(?:loan|facility|credit|financing)\b"
                r".{0,120}"
                r"\b(?:proceeds|principal|amount|funds)\b"
                r".{0,120}"
                r"\b(?:shall|must|will|may|are|is)\b"
                r".{0,50}"
                r"\b(?:be\s+)?(?:disbursed|advanced|funded|"
                r"released|transferred|made\s+available)\b"
            ),
            # EN — utilisation or drawdown funding.
            (
                r"\b(?:make|made)\s+available\b"
                r".{0,140}"
                r"\b(?:loan|facility|credit|financing)\b"
                r".{0,100}"
                r"\b(?:amount|proceeds|funds)\b"
            ),
        ),
        (
            # FR — décaissement ou versement par le prêteur.
            (
                r"\b(?:pr[eê]teur|agent\s+de\s+la\s+facilit[eé]|"
                r"cr[eé]ancier)\b"
                r".{0,120}"
                r"\b(?:doit|devra|d[eé]caissera|versera|"
                r"mettra|pourra)\b"
                r".{0,80}"
                r"\b(?:d[eé]caisser|verser|avancer|lib[eé]rer|"
                r"transf[eé]rer|mettre\s+[àa]\s+disposition|"
                r"d[eé]caissera|versera|lib[eé]rera|"
                r"transf[eé]rera)\b"
                r".{0,160}"
                r"\b(?:produit\s+du\s+pr[eê]t|"
                r"produit\s+de\s+la\s+facilit[eé]|"
                r"montant\s+principal|montant\s+en\s+principal|"
                r"montant\s+du\s+(?:pr[eê]t|cr[eé]dit)|"
                r"fonds\s+au\s+titre\s+du\s+(?:pr[eê]t|cr[eé]dit))\b"
            ),
            # FR — fonds mis à disposition.
            (
                r"\b(?:pr[eê]t|facilit[eé]|cr[eé]dit|financement)\b"
                r".{0,120}"
                r"\b(?:produit|montant|principal|fonds)\b"
                r".{0,140}"
                r"\b(?:seront|sont|doivent\s+[eê]tre|"
                r"devront\s+[eê]tre|peuvent\s+[eê]tre)\b"
                r".{0,60}"
                r"\b(?:d[eé]caiss[eé]s?|vers[eé]s?|avanc[eé]s?|"
                r"lib[eé]r[eé]s?|transf[eé]r[eé]s?|"
                r"mis\s+[àa]\s+disposition)\b"
            ),
            # FR — mise à disposition avec ordre inverse.
            (
                r"\b(?:mettre|mis|mise)\s+[àa]\s+disposition\b"
                r".{0,160}"
                r"\b(?:fonds|montant|produit)\b"
                r".{0,100}"
                r"\b(?:pr[eê]t|facilit[eé]|cr[eé]dit|financement)\b"
            ),
        ),
        (
            # AR — صرف أو تحويل مبلغ القرض/التسهيل.
            (
                r"(?:يصرف|تُصرف|تصرف|سيصرف|"
                r"يحوّل|يحول|تُحوّل|تحول|"
                r"يتيح|تتيح|يُفرج|يفرج)"
                r".{0,160}"
                r"(?:المبلغ\s+الأصلي|أصل\s+القرض|"
                r"مبلغ\s+(?:القرض|التسهيل|التمويل)|"
                r"أموال\s+(?:القرض|التسهيل|التمويل)|"
                r"حصيلة\s+(?:القرض|التسهيل|التمويل)|"
                r"عائدات\s+(?:القرض|التسهيل|التمويل))"
            ),
            # AR — instrument first, then funds are made available.
            (
                r"(?:القرض|التسهيل|الائتمان|التمويل)"
                r".{0,140}"
                r"(?:المبلغ|الأصل|الأموال|الحصيلة|العائدات)"
                r".{0,140}"
                r"(?:يتم\s+صرف|تُصرف|تصرف|"
                r"يتم\s+تحويل|تُحوّل|تحول|"
                r"تتاح|يتم\s+إتاحتها|"
                r"يتم\s+الإفراج\s+عنها)"
            ),
            # AR — funds made available under a facility.
            (
                r"(?:إتاحة|توفير|تحويل|صرف|الإفراج\s+عن)"
                r".{0,120}"
                r"(?:الأموال|المبلغ|الحصيلة|العائدات)"
                r".{0,120}"
                r"(?:بموجب|بمقتضى|في\s+إطار|لحساب)"
                r".{0,80}"
                r"(?:القرض|التسهيل|الائتمان|التمويل)"
            ),
        ),
        96,
        "loan",
        DOMAIN_CORE,
        True,
        polarity="REQUIRED",
    ),

'''

if not TARGET.exists():
    raise SystemExit(f"ERROR: target not found: {TARGET}")

source = TARGET.read_text(encoding="utf-8")

start = source.find(START_MARKER)
end = source.find(END_MARKER)

if start < 0:
    raise SystemExit(
        "ERROR: LOAN_PRINCIPAL_DISBURSEMENT block not found"
    )

if end < 0 or end <= start:
    raise SystemExit(
        "ERROR: ACCELERATION_ON_DEFAULT anchor not found"
    )

current_block = source[start:end]

if "direct disbursement of loan/facility proceeds" in current_block:
    print("PATCH STATUS: ALREADY APPLIED")
    sys.exit(0)

if current_block.count(
    "LOAN_PRINCIPAL_DISBURSEMENT"
) != 1:
    raise SystemExit(
        "ERROR: unexpected disbursement block structure"
    )

shutil.copy2(TARGET, BACKUP)

updated = source[:start] + NEW_BLOCK + source[end:]
TARGET.write_text(updated, encoding="utf-8")

print("PATCH STATUS: APPLIED")
print("TARGET:", TARGET)
print("BACKUP:", BACKUP)
