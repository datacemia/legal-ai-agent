"""
test_isolation_full_chain_v2.py

Version corrigee : analyze_contract_clauses() retourne un dict (pas une
liste), avec la vraie liste de clauses dans results["clauses"]["results"].

Usage:
    python test_isolation_full_chain_v2.py
"""

from app.services.text_cleaner import clean_text
from app.services.contract_agent.pii_redactor import redact_sensitive_data
from app.services.contract_agent.clause_splitter import split_into_clauses
from app.services.contract_agent.contract_agent import analyze_contract_clauses

TEST_TEXT = """EXECUTIVE EMPLOYMENT AGREEMENT

This Executive Employment Agreement (the "Agreement") is entered into as of July 6, 2026, between Ironvale Biosciences Inc., a Delaware corporation (the "Company"), and Dr. Elena Marchetti, an individual (the "Executive"), pursuant to which the Company agrees to employ Executive as Chief Scientific Officer.

**"****Cause****"** means Executive's conviction of a felony, willful misconduct materially injurious to the Company, or continued failure to perform material duties after written notice and a thirty (30) day cure period.

**"****Good Reason****"** means a material diminution in Executive's title, duties, or base salary, or relocation of Executive's principal office by more than fifty (50) miles, in each case without Executive's consent.

# 1. POSITION AND DUTIES

1.1 Executive shall serve as Chief Scientific Officer, reporting to the Chief Executive Officer, and shall devote substantially full business time to the Company's affairs.

# 2. COMPENSATION

2.1 The Company shall pay Executive an annual base salary of $410,000, payable in accordance with the Company's standard payroll practices, subject to annual review by the Board.
"""

cleaned = clean_text(TEST_TEXT)
redacted = redact_sensitive_data(cleaned)
clauses = split_into_clauses(redacted)

print(f"Clauses apres decoupage ({len(clauses)}):")
for c in clauses:
    print(f"  - {c[:70]!r}")

print()
print("Appel de analyze_contract_clauses() (vrais appels IA)...")
pipeline_result = analyze_contract_clauses(
    clauses,
    language="en",
    party_roles={"party_a": "Company", "party_b": "Executive", "family": "generic"},
)

print()
print("Cles du dict retourne:", list(pipeline_result.keys()))

clause_list = pipeline_result.get("clauses", {}).get("results", [])
print()
print(f"{len(clause_list)} clause(s) analysee(s):")
for r in clause_list:
    print(f"  clause_reference={r.get('clause_reference')!r:10}  clause_title={r.get('clause_title')!r}")

print()
found_11 = any(r.get("clause_reference") == "1.1" for r in clause_list)
if found_11:
    print("✅ '1.1' SURVIT jusqu'au resultat final via ce chemin direct.")
else:
    print("❌ '1.1' NE SURVIT PAS. Detail de l'entree concernee:")
    import json
    for r in clause_list:
        if "Position" in str(r.get("clause_title", "")):
            print(json.dumps(r, indent=2, ensure_ascii=False)[:2500])