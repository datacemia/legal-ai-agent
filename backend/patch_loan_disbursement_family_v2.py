from pathlib import Path
import shutil
import sys


TARGET = Path(
    "app/services/contract_agent/"
    "semantic_source_profile.py"
)

BACKUP = TARGET.with_suffix(
    ".py.before_loan_disbursement_family_v2"
)

START_MARKER = '    _r(\n        "LOAN_PRINCIPAL_DISBURSEMENT",'
END_MARKER = '    _r("ACCELERATION_ON_DEFAULT",'

NEW_BLOCK = r'''    _r(
        "LOAN_PRINCIPAL_DISBURSEMENT",
        (
            # EN — financier actively provides financing proceeds.
            (
                r"\b(?:lender|creditor|facility\s+agent|"
                r"finance\s+party|funding\s+party)\b"
                r".{0,120}?"
                r"\b(?:(?:shall|must|will|may)\s+)?"
                r"(?:disburse|advance|fund|release|transfer|"
                r"make\s+available)\b"
                r".{0,160}?"
                r"\b(?:principal\s+amount|loan\s+proceeds|"
                r"facility\s+proceeds|credit\s+proceeds|"
                r"financing\s+proceeds|"
                r"amount\s+of\s+the\s+(?:loan|facility|credit)|"
                r"funds\s+under\s+the\s+(?:loan|facility|credit))\b"
            ),
            # EN — financing amount or proceeds are provided.
            (
                r"\b(?:principal\s+amount|loan\s+proceeds|"
                r"facility\s+proceeds|credit\s+proceeds|"
                r"financing\s+proceeds|"
                r"funds\s+(?:of|under)\s+the\s+"
                r"(?:loan|facility|credit|financing))\b"
                r".{0,140}?"
                r"\b(?:shall|must|will|may|is|are)\b"
                r".{0,50}?"
                r"\b(?:be\s+)?(?:disbursed|advanced|funded|"
                r"released|transferred|made\s+available)\b"
            ),
            # EN — generic availability of financing funds.
            (
                r"\b(?:make|makes|made)\s+available\b"
                r".{0,140}?"
                r"\b(?:principal\s+amount|proceeds|funds)\b"
                r".{0,100}?"
                r"\b(?:loan|facility|credit|financing)\b"
            ),
        ),
        (
            # FR — acteur financier + verbe conjugué ou modal + infinitif.
            (
                r"\b(?:pr[eê]teur|cr[eé]ancier|"
                r"agent\s+de\s+la\s+facilit[eé]|"
                r"agent\s+du\s+cr[eé]dit|partie\s+financi[eè]re)\b"
                r".{0,120}?"
                r"(?:"
                r"(?:doit|devra|pourra|s'engage\s+[àa])"
                r".{0,40}?"
                r"(?:d[eé]caisser|verser|avancer|lib[eé]rer|"
                r"transf[eé]rer|mettre\s+[àa]\s+disposition)"
                r"|"
                r"(?:d[eé]caisse(?:ra|nt)?|verse(?:ra|nt)?|"
                r"avance(?:ra|nt)?|lib[eé]re(?:ra|nt)?|"
                r"transf[eè]re(?:ra|nt)?|"
                r"met(?:tra|tront)\s+[àa]\s+disposition)"
                r")"
                r".{0,160}?"
                r"\b(?:montant\s+principal|"
                r"montant\s+en\s+principal|"
                r"produit\s+du\s+pr[eê]t|"
                r"produit\s+de\s+la\s+facilit[eé]|"
                r"produit\s+du\s+cr[eé]dit|"
                r"fonds\s+du\s+(?:pr[eê]t|cr[eé]dit|financement)|"
                r"montant\s+du\s+(?:pr[eê]t|cr[eé]dit|financement))\b"
            ),
            # FR — fonds ou produit du financement + voix passive.
            (
                r"\b(?:fonds|produit|montant|principal)\b"
                r".{0,80}?"
                r"\b(?:du|de\s+la|des)\b"
                r".{0,40}?"
                r"\b(?:pr[eê]t|facilit[eé]|cr[eé]dit|financement)\b"
                r".{0,140}?"
                r"\b(?:sera|seront|doit\s+[eê]tre|"
                r"doivent\s+[eê]tre|devra\s+[eê]tre|"
                r"devront\s+[eê]tre|pourra\s+[eê]tre|"
                r"pourront\s+[eê]tre)\b"
                r".{0,50}?"
                r"\b(?:d[eé]caiss[eé]s?|vers[eé]s?|avanc[eé]s?|"
                r"lib[eé]r[eé]s?|transf[eé]r[eé]s?|"
                r"mis(?:es)?\s+[àa]\s+disposition)\b"
            ),
            # FR — mise à disposition exprimée avant l'objet financier.
            (
                r"\b(?:mettre|mettra|mettront|mis|mise|mises)"
                r"\s+[àa]\s+disposition\b"
                r".{0,160}?"
                r"\b(?:fonds|produit|montant|principal)\b"
                r".{0,100}?"
                r"\b(?:pr[eê]t|facilit[eé]|cr[eé]dit|financement)\b"
            ),
        ),
        (
            # AR — active disbursement, transfer or availability.
            (
                r"(?:يصرف|سيصرف|تصرف|تُصرف|"
                r"يحول|يحوّل|سيحول|تحول|تُحوّل|"
                r"يتيح|سيتيح|يوفر|سيوفر|"
                r"يفرج|يُفرج)"
                r".{0,160}?"
                r"(?:المبلغ\s+الأصلي|أصل\s+القرض|"
                r"مبلغ\s+(?:القرض|التسهيل|الائتمان|التمويل)|"
                r"أموال\s+(?:القرض|التسهيل|الائتمان|التمويل)|"
                r"حصيلة\s+(?:القرض|التسهيل|الائتمان|التمويل)|"
                r"عائدات\s+(?:القرض|التسهيل|الائتمان|التمويل))"
            ),
            # AR — passive availability or transfer of financing funds.
            (
                r"(?:تتاح|ستتاح|تُتاح|"
                r"تتوفر|ستتوفر|"
                r"تُصرف|تصرف|"
                r"تُحوّل|تحول|"
                r"يتم\s+(?:صرف|تحويل|إتاحة|توفير|الإفراج\s+عن))"
                r".{0,100}?"
                r"(?:الأموال|المبلغ|المبالغ|الحصيلة|العائدات)"
                r".{0,100}?"
                r"(?:القرض|التسهيل|الائتمان|التمويل)"
            ),
            # AR — financing instrument first, followed by funding action.
            (
                r"(?:القرض|التسهيل|الائتمان|التمويل)"
                r".{0,120}?"
                r"(?:المبلغ|المبالغ|الأموال|الحصيلة|العائدات)"
                r".{0,140}?"
                r"(?:تتاح|تُتاح|تُصرف|تصرف|تُحوّل|تحول|"
                r"يتم\s+(?:صرف|تحويل|إتاحة|توفير|الإفراج\s+عن))"
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

current = source[start:end]

if "acteur financier + verbe conjugué" in current:
    print("PATCH STATUS: ALREADY APPLIED")
    sys.exit(0)

if current.count("LOAN_PRINCIPAL_DISBURSEMENT") != 1:
    raise SystemExit(
        "ERROR: unexpected semantic rule structure"
    )

shutil.copy2(TARGET, BACKUP)

updated = source[:start] + NEW_BLOCK + source[end:]
TARGET.write_text(updated, encoding="utf-8")

print("PATCH STATUS: APPLIED")
print("TARGET:", TARGET)
print("BACKUP:", BACKUP)
