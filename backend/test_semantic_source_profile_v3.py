from app.services.contract_agent.semantic_source_profile import (
    UNKNOWN,
    build_semantic_source_profile,
    canonicalize_pipeline_type,
)

CASES = [
    ("en_financial", "The Company shall provide financial statements within 30 days after each quarter.", "financial_reporting"),
    ("fr_financial", "La Société doit fournir les états financiers dans un délai de 30 jours après chaque trimestre.", "financial_reporting"),
    ("ar_financial", "يجب على الشركة تقديم القوائم المالية خلال 30 يومًا بعد كل ربع سنة.", "financial_reporting"),
    ("en_liability", "The total liability of the Supplier shall not exceed the fees paid under this Agreement.", "liability"),
    ("fr_liability", "La responsabilité totale du Prestataire est limitée au montant payé au titre du Contrat.", "liability"),
    ("ar_liability", "تكون المسؤولية الإجمالية للمورد محدودة بالمبالغ المدفوعة بموجب العقد.", "liability"),
    ("en_conf", "The Recipient shall keep all Confidential Information in strict confidence.", "confidentiality"),
    ("fr_conf", "Le Destinataire doit garder les informations strictement confidentielles.", "confidentiality"),
    ("ar_conf", "يلتزم المستلم بالحفاظ على سرية المعلومات بشكل صارم.", "confidentiality"),
    ("en_renewal", "This Agreement shall automatically renew for successive one-year periods.", "renewal"),
    ("fr_renewal", "Le Contrat se renouvelle automatiquement pour des périodes successives d'un an.", "renewal"),
    ("ar_renewal", "يتجدد هذا العقد تلقائيًا لفترات متتالية مدتها سنة واحدة.", "renewal"),
    ("control_only", "The Contractor shall not act without prior written consent of the Company.", UNKNOWN),
    ("en_governance", "The board of directors shall consist of five directors appointed under this Agreement.", "governance"),
    ("en_payment", "The Client shall pay the monthly fee within 30 days after receipt of invoice.", "payment"),
    ("en_termination", "Either party may terminate this Agreement upon thirty days written notice.", "termination"),
    ("broad_narrow_abstain", ("This section describes the parties, background, operational framework, schedules, exhibits, "
        "general administration, reporting context, contacts, definitions, and miscellaneous arrangements. "
        "The Supplier shall pay a fee. Additional provisions address implementation and coordination."), UNKNOWN),
]

def main():
    failures = []
    for name, text, expected in CASES:
        profile = build_semantic_source_profile(text)
        actual = profile["primary_type"]
        if actual != expected:
            failures.append((name, expected, actual, profile.get("abstention_reason"), profile.get("dominance_scores")))
        print(name, "=>", actual, profile["confidence"], profile["abstained"])
    assert canonicalize_pipeline_type("limitation_of_liability") == "liability"
    assert canonicalize_pipeline_type("corporate_governance") == "governance"
    assert not failures, failures
    print(f"PASS: {len(CASES)}/17 semantic adjudication cases")

if __name__ == "__main__":
    main()
