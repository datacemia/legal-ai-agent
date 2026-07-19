"""
test_isolation_1_1.py

Test isole, a executer directement sur le serveur reel, pour determiner
sans ambiguite si split_into_clauses() (avec les fichiers reellement
deployes) separe correctement "1.1" de l'en-tete "1. POSITION AND DUTIES".

Usage:
    python test_isolation_1_1.py
"""

from app.services.contract_agent.clause_splitter import split_into_clauses

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
print("TEST D'ISOLATION - split_into_clauses() directement, sans le reste du pipeline")
print("=" * 78)

clauses = split_into_clauses(TEST_TEXT)

print(f"\nNombre de clauses produites : {len(clauses)}\n")

for i, c in enumerate(clauses, 1):
    preview = c[:80].replace("\n", " \\n ")
    print(f"  {i}. {preview!r}")

print()
found_11 = any(c.strip().startswith("1.1") for c in clauses)

if found_11:
    print("✅ '1.1' EST correctement separee comme sa propre clause.")
    print("   -> Le bug n'est PAS dans split_into_clauses() sur ce serveur.")
    print("   -> Le probleme se situe ailleurs dans le pipeline")
    print("      (extract_text, redact_sensitive_data, ou un autre fichier).")
else:
    print("❌ '1.1' N'EST PAS separee correctement.")
    print("   -> Le bug EST bien dans split_into_clauses() (ou une fonction")
    print("      qu'elle appelle) sur ce serveur precisement.")
    print("   -> Cela confirme un ecart entre le fichier reellement execute")
    print("      ici et celui teste par Claude.")

print()
print("=" * 78)
print("Copie-colle la sortie complete ci-dessus dans la conversation.")
print("=" * 78)