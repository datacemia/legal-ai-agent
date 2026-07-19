"""
test_isolation_full_chain.py

Test isole plus complet : appelle la chaine complete d'analyse de clauses
(pas seulement le decoupage) directement, en cout-circuitant tout job/
worker/cache eventuel, pour voir si "1.1" survit jusqu'au resultat final
quand on appelle le code Python directement.

Usage:
    python test_isolation_full_chain.py
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

print("=" * 78)
print("ETAPE 1 - clean_text()")
print("=" * 78)
cleaned = clean_text(TEST_TEXT)
print("OK, longueur:", len(cleaned))

print()
print("=" * 78)
print("ETAPE 2 - redact_sensitive_data()")
print("=" * 78)
redacted = redact_sensitive_data(cleaned)
idx = redacted.find("POSITION")
print("Extrait autour de la section 1:")
print(repr(redacted[max(0, idx - 20):idx + 200]))

print()
print("=" * 78)
print("ETAPE 3 - split_into_clauses()")
print("=" * 78)
clauses = split_into_clauses(redacted)
print(f"{len(clauses)} clause(s) produite(s):")
for c in clauses:
    print(f"  - {c[:70]!r}")

print()
print("=" * 78)
print("ETAPE 4 - analyze_contract_clauses() -- LA CHAINE COMPLETE, AVEC APPELS IA REELS")
print("=" * 78)
print("(Ceci va faire de vrais appels a l'IA -- peut prendre quelques secondes)")

results = analyze_contract_clauses(
    clauses,
    language="en",
    party_roles={"party_a": "Company", "party_b": "Executive", "family": "generic"},
)

print()
print(f"{len(results)} resultat(s) final(aux):")
for r in results:
    print(f"  clause_reference={r.get('clause_reference')!r:10}  clause_title={r.get('clause_title')!r}")

print()
found_11 = any(r.get("clause_reference") == "1.1" for r in results)
if found_11:
    print("✅ '1.1' SURVIT jusqu'au resultat final via ce chemin direct.")
    print("   -> Le bug doit se situer dans l'infrastructure job/worker")
    print("      (mise en cache, une autre version du code executee par le worker, etc.)")
else:
    print("❌ '1.1' NE SURVIT PAS. Voici le detail complet du resultat concerne :")
    for r in results:
        if "Position" in str(r.get("clause_title", "")):
            import json
            print(json.dumps(r, indent=2, ensure_ascii=False)[:2000])

print()
print("=" * 78)
print("Copie-colle la sortie complete ci-dessus dans la conversation.")
print("=" * 78)