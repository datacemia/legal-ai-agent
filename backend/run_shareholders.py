from dotenv import load_dotenv
load_dotenv()

import json
from pathlib import Path

from app.services.contract_agent.contract_parser import extract_text_from_docx
from app.services.contract_agent.clause_splitter import split_into_clause_objects
from app.services.contract_agent.contract_agent import ClauseAnalysisPipeline

path = next(Path("regression_docs").glob("*Shareholders*.docx"))

print("FILE:", path)

text = extract_text_from_docx(str(path))
clauses = split_into_clause_objects(text)

print("CLAUSES:", len(clauses))

result = ClauseAnalysisPipeline(
    clauses=clauses,
    language="en",
    max_clauses=60,
).run()

rows = result["clauses"]["results"]

receipt_count = 0
unsuccessful = 0
hash_mismatches = 0
post_gate = 0

for clause in rows:
    for field, receipt in (
        clause.get("validation_receipts") or {}
    ).items():
        receipt_count += 1

        if receipt.get("successful") is not True:
            unsuccessful += 1

        if (
            receipt.get("validated_text_hash")
            != receipt.get("final_text_hash")
        ):
            hash_mismatches += 1

        if receipt.get("post_gate_mutators"):
            post_gate += 1

        reasons = receipt.get("validation_reasons") or []

        if reasons:
            print()
            print("CLAUSE:", clause.get("clause_reference"))
            print("TYPE:", clause.get("clause_type"))
            print("FIELD:", field)
            print("GATE:", receipt.get("gate_result"))
            print("REASONS:", reasons)
            print(
                "BEFORE:",
                receipt.get("text_before_validation"),
            )
            print("FINAL:", clause.get(field))

Path(
    "regression_results/shareholders_local.json"
).write_text(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
        default=str,
    ),
    encoding="utf-8",
)

print()
print("RESULTS:", len(rows))
print("RECEIPTS:", receipt_count)
print("UNSUCCESSFUL:", unsuccessful)
print("HASH MISMATCHES:", hash_mismatches)
print("POST GATE MUTATIONS:", post_gate)
print("DONE")
