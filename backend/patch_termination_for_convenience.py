from pathlib import Path

path = Path("app/services/contract_agent/semantic_source_profile.py")

text = path.read_text(encoding="utf-8")

old_1 = (
    r'r"\b(?:may|shall\s+have\s+the\s+right\s+to)\s+terminate\b'
    r'[^.;!?]{0,180}\b(?:for\s+convenience|without\s+cause|at\s+any\s+time)'
    r'\b[^.;!?]{0,220}",'
)

new_1 = (
    r'r"\b(?:may|shall\s+have\s+the\s+right\s+to)\s+terminate\b'
    r'[^.;!?]{0,180}\b(?:for\s+convenience|without\s+cause|'
    r'for\s+any\s+reason|no\s+reason|at\s+any\s+time)'
    r'\b[^.;!?]{0,220}",'
)

old_2 = (
    r'r"\bterminate\b[^.;!?]{0,180}\b'
    r'(?:for\s+convenience|without\s+cause|at\s+any\s+time)'
    r'\b[^.;!?]{0,220}",'
)

new_2 = (
    r'r"\bterminate\b[^.;!?]{0,180}\b'
    r'(?:for\s+convenience|without\s+cause|'
    r'for\s+any\s+reason|no\s+reason|at\s+any\s+time)'
    r'\b[^.;!?]{0,220}",'
)

if old_1 not in text:
    raise SystemExit("ERROR: first termination-for-convenience pattern not found")

if old_2 not in text:
    raise SystemExit("ERROR: second termination-for-convenience pattern not found")

text = text.replace(old_1, new_1, 1)
text = text.replace(old_2, new_2, 1)

path.write_text(text, encoding="utf-8")

print("PATCH APPLIED:", path)
print("Added English expressions:")
print("  - for any reason")
print("  - no reason")
