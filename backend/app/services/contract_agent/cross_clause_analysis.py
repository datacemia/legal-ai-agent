def analyze_cross_clause_risks(clauses):
    issues = []

    combined = " ".join([
        str(c.get("title", "")) + " " +
        str(c.get("clause", ""))
        for c in clauses
    ]).lower()

    if (
        "service level" in combined
        and "liability" in combined
    ):
        issues.append(
            "Service obligations should be compared against liability "
            "limitations."
        )

    if (
        "termination" in combined
        and "payment" in combined
    ):
        issues.append(
            "Termination rights may affect payment obligations or "
            "outstanding fees."
        )

    if (
        "confidentiality" in combined
        and "data" in combined
    ):
        issues.append(
            "Confidentiality obligations should align with data "
            "protection requirements."
        )

    return issues
