from app.services.finance_agent.transaction_extractor import (
    looks_like_debit_description,
    looks_like_credit_description,
    looks_like_neutral_inbound_transfer,
)

def check(desc, expected):
    debit = looks_like_debit_description(desc)
    credit = looks_like_credit_description(desc)
    neutral_income = looks_like_neutral_inbound_transfer(desc, 100)

    if expected == "expense":
        assert debit and not credit, desc
    elif expected == "income":
        assert credit or neutral_income, desc
        assert not debit, desc

def test_expense_markers():
    check("PRLV SEPA EDF", "expense")
    check("PAIEMENT CB CARREFOUR", "expense")
    check("Direct Debit TELSTRA", "expense")
    check("Transfer to xx1234", "expense")
    check("ATM withdrawal", "expense")

def test_income_markers():
    check("Salary payment", "income")
    check("Direct Credit ATO", "income")
    check("Transfer from HAMZAN", "income")
    check("VIR DGFIP SCBCM MINEFI", "income")
    check("VIR AKTO", "income")
    check("VIR CIAMT", "income")
    check("VRST REF06036A07 BILLET", "income")
