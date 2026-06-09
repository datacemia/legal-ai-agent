from pathlib import Path

p = Path("app/services/finance_agent/transaction_extractor.py")
s = p.read_text(encoding="utf-8")

# Remove bad V10 block if present
start = s.find("# === RUNEXA_SAFE_LAYOUT_PATCH_V10 ===")
end = s.find("# === END_RUNEXA_SAFE_LAYOUT_PATCH_V10 ===")
if start != -1 and end != -1:
    end += len("# === END_RUNEXA_SAFE_LAYOUT_PATCH_V10 ===")
    s = s[:start] + "\n" + s[end:]

# Rename ONLY the first real extractor, not the final wrapper
needle = "def extract_transactions(text: str) -> list[dict]:"
if "def _runexa_core_extract_transactions(text: str) -> list[dict]:" not in s:
    first = s.find(needle)
    if first == -1:
        raise RuntimeError("Core extract_transactions not found")
    s = s[:first] + "def _runexa_core_extract_transactions(text: str) -> list[dict]:" + s[first + len(needle):]

# Force original pointer to the true core, never to a wrapper
s = s.replace(
    "_RUNEXA_ORIGINAL_EXTRACT_TRANSACTIONS = extract_transactions",
    "_RUNEXA_ORIGINAL_EXTRACT_TRANSACTIONS = _runexa_core_extract_transactions"
)

p.write_text(s, encoding="utf-8")
print("Recursion fixed safely.")
