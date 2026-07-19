from pathlib import Path

path = Path("app/services/contract_agent/normalized_legal_relation.py")
text = path.read_text(encoding="utf-8")

concept_old = '"TRANSITION_SERVICE_OBLIGATION": "TRANSITION_PLAN",'
concept_new = '''"TRANSITION_SERVICE_OBLIGATION": "TRANSITION_PLAN",

    # Governance
    "RESERVED_MATTERS_CONSENT": "RESERVED_MATTER",'''

if '"RESERVED_MATTERS_CONSENT"' not in text:
    text = text.replace(concept_old, concept_new)

action_old = '"TAG_ALONG_RIGHT": "PARTICIPATE_IN_SALE",'
action_new = '''"TAG_ALONG_RIGHT": "PARTICIPATE_IN_SALE",

    # Governance
    "RESERVED_MATTER": "OBTAIN_REQUIRED_CONSENT",'''

if '"RESERVED_MATTER": "OBTAIN_REQUIRED_CONSENT"' not in text:
    text = text.replace(action_old, action_new)

path.write_text(text, encoding="utf-8")

print("✓ RESERVED_MATTERS_CONSENT mapping added")
