from pathlib import Path

p = Path("app/services/finance_agent/transaction_extractor.py")
s = p.read_text(encoding="utf-8")

start = s.find('    raw = normalize_arabic_digits(str(text or ""))\n    if (\n        "325,458" in raw')
end = s.find("\n    cleaned_summary = {}", start)

if start == -1 or end == -1:
    raise RuntimeError("Hardcoded ANB summary block not found")

generic = '''    raw = normalize_arabic_digits(str(text or ""))

    # Generic ANB Arabic summary parser.
    # Layout:
    # amount + opening balance label
    # amount + closing balance label
    # negative amount + total debit label
    # amount + total credit label
    anb_summary = _runexa_extract_anb_summary_generic(raw)
    if anb_summary:
        original_summary = anb_summary

'''

s = s[:start] + generic + s[end:]

insert_anchor = "def extract_transactions(text: str) -> list[dict]:"
idx = s.find(insert_anchor)
if idx == -1:
    raise RuntimeError("extract_transactions anchor not found")

helper = r'''
def _runexa_extract_anb_summary_generic(text):
    import re

    raw = normalize_arabic_digits(str(text or ""))

    # ANB signal. Supports normal Arabic, pdfplumber Arabic presentation forms,
    # English fallback, and account/IBAN pattern for this ANB layout family.
    if not any(marker in raw for marker in [
        "البنك العربي الوطني",
        "ANB",
        "Arab National Bank",
        "anb.com.sa",
        "SA323040",
        "ملخص الحساب",
        "ﺏﺎﺴﺤﻟﺍ ﺺﺨﻠﻣ",
    ]):
        return {}

    money_re = r"-?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})|-?\d+(?:\.\d{1,2})?"

    lines = [" ".join(x.split()) for x in raw.splitlines() if " ".join(x.split())]

    def money_from_line(line):
        vals = re.findall(money_re, line)
        if not vals:
            return None
        try:
            return parse_amount(vals[0])
        except Exception:
            return None

    summary = {}

    # Works with both logical Arabic text and Arabic presentation-form text,
    # because we also rely on the stable order of the first summary block.
    for i, line in enumerate(lines[:120]):
        val = money_from_line(line)
        if val is None:
            continue

        # Normal Arabic labels.
        if "الرصيد الافتتاحي" in line or "ﻲﺣﺎﺘﺘﻓﻻﺍ" in line:
            summary["opening_balance"] = abs(val)
            continue

        if "رصيد الإغلاق" in line or "ﻕﻼﻏﻹﺍ" in line:
            summary["ending_balance"] = abs(val)
            continue

        if "إجمالي الخصم" in line or "ﻢﺼﺨﻟﺍ" in line:
            summary["withdrawals"] = abs(val)
            continue

        if "إجمالي المبلغ الدائن" in line or "ﻦﺋﺍﺪﻟﺍ" in line:
            summary["deposits"] = abs(val)
            continue

    # Positional fallback for ANB pdfplumber RTL presentation text.
    if not {"opening_balance", "ending_balance", "withdrawals", "deposits"} <= set(summary):
        block_vals = []
        for line in lines[:80]:
            if any(label in line for label in [
                "ﻲﺣﺎﺘﺘﻓﻻﺍ",
                "ﻕﻼﻏﻹﺍ",
                "ﻢﺼﺨﻟﺍ",
                "ﻦﺋﺍﺪﻟﺍ",
                "الرصيد",
                "إجمالي",
            ]):
                val = money_from_line(line)
                if val is not None:
                    block_vals.append(val)

        if len(block_vals) >= 4:
            summary.setdefault("opening_balance", abs(block_vals[0]))
            summary.setdefault("ending_balance", abs(block_vals[1]))
            summary.setdefault("withdrawals", abs(block_vals[2]))
            summary.setdefault("deposits", abs(block_vals[3]))

    required = ["opening_balance", "ending_balance", "withdrawals", "deposits"]
    if all(k in summary for k in required):
        print("ANB_GENERIC_SUMMARY_EXTRACTED", summary)
        return summary

    return {}

'''

s = s[:idx] + helper + "\n" + s[idx:]

p.write_text(s, encoding="utf-8")
print("Generic ANB summary patch installed")
