#!/usr/bin/env python3
from pathlib import Path
import re
import shutil

ROOT = Path.cwd()

WORKER_CANDIDATES = [
    ROOT / "app/workers/finance_worker.py",
    ROOT / "app/workers/finance_ai_worker.py",
    ROOT / "app/services/finance_agent/finance_worker.py",
]

EXTRACTOR_CANDIDATES = [
    ROOT / "app/services/finance_agent/transaction_extractor.py",
    ROOT / "transaction_extractor.py",
]


def backup(path):
    bak = path.with_suffix(path.suffix + ".bak.v2")
    if not bak.exists():
        shutil.copy2(path, bak)


def patch_worker(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text

    helper = '''
def normalize_signed_amounts_before_kpi(transactions):
    normalized = []
    for tx in transactions or []:
        if not isinstance(tx, dict):
            continue
        try:
            amount = float(tx.get("amount") or 0)
        except Exception:
            amount = 0.0
        if tx.get("signed_amount") is None:
            tx["signed_amount"] = amount
        if tx.get("_locked_amount") is None:
            tx["_locked_amount"] = tx["signed_amount"]
        if tx.get("locked_amount") is None:
            tx["locked_amount"] = tx["signed_amount"]
        tx_type = str(tx.get("type") or "").lower().strip()
        if not tx_type:
            if tx.get("excluded_from_financial_kpis"):
                tx["type"] = "excluded"
            elif amount > 0:
                tx["type"] = "income"
            elif amount < 0:
                tx["type"] = "expense"
            else:
                tx["type"] = "zero_amount"
        normalized.append(tx)
    return normalized


def compute_reconciliation_warning(transactions, kpi_transactions, existing_warning=None):
    total = len(transactions or [])
    kpi_count = len(kpi_transactions or [])
    excluded = max(total - kpi_count, 0)

    if total <= 0:
        return "NO_TRANSACTIONS_EXTRACTED"
    if kpi_count <= 0:
        return "NO_KPI_TRANSACTIONS"
    if excluded > max(3, int(total * 0.10)):
        return "TOO_MANY_EXCLUDED_TRANSACTIONS"
    if any(tx.get("signed_amount") is None for tx in (kpi_transactions or [])):
        return "MISSING_SIGNED_AMOUNT"

    zero_amounts = [
        tx for tx in (kpi_transactions or [])
        if float(tx.get("amount") or 0) == 0
        and not tx.get("excluded_from_financial_kpis")
    ]
    if len(zero_amounts) > max(2, int(kpi_count * 0.05)):
        return "TOO_MANY_ZERO_AMOUNT_TRANSACTIONS"

    return existing_warning
'''

    if "def normalize_signed_amounts_before_kpi(" not in text:
        if "def handle_finance_ai(" in text:
            text = text.replace("def handle_finance_ai(", helper + "\n\ndef handle_finance_ai(", 1)
        else:
            text += "\n\n" + helper + "\n"

    if "transactions = normalize_signed_amounts_before_kpi(transactions)" not in text:
        text = text.replace(
            'audit_tx_stage("TX_STAGE_2_AFTER_CANONICALIZE", transactions)',
            'transactions = normalize_signed_amounts_before_kpi(transactions)\n\n    audit_tx_stage("TX_STAGE_2_AFTER_CANONICALIZE", transactions)',
            1,
        )

    if "kpi_transactions = normalize_signed_amounts_before_kpi(kpi_transactions)" not in text:
        text = text.replace(
            'audit_tx_stage("TX_STAGE_3_KPI_TRANSACTIONS_CREATED", kpi_transactions)',
            'kpi_transactions = normalize_signed_amounts_before_kpi(kpi_transactions)\n\n    audit_tx_stage("TX_STAGE_3_KPI_TRANSACTIONS_CREATED", kpi_transactions)',
            1,
        )

    text = re.sub(
        r'\n\s*tx\.pop\("signed_amount",\s*None\)',
        '\n            # hotfix-v2: keep signed_amount for auditability',
        text,
    )
    text = re.sub(
        r"\n\s*tx\.pop\('signed_amount',\s*None\)",
        '\n            # hotfix-v2: keep signed_amount for auditability',
        text,
    )

    text = re.sub(
        r'tx\["type"\]\s*=\s*None',
        'tx["previous_type_before_exclusion"] = tx.get("type")\n            tx["type"] = tx.get("type") or "excluded"',
        text,
    )

    insertion = '''
    # hotfix-v2: ensure reconciliation warning reflects KPI safety.
    try:
        reconciliation_warning_hotfix = compute_reconciliation_warning(
            transactions,
            kpi_transactions,
            (
                reconciliation.get("warning")
                if isinstance(reconciliation, dict)
                else None
            ),
        )
        if isinstance(reconciliation, dict):
            reconciliation["excluded_transactions"] = max(
                len(transactions or []) - len(kpi_transactions or []),
                0,
            )
            reconciliation["warning"] = reconciliation_warning_hotfix
        print(
            "RECONCILIATION_WARNING_HOTFIX_V2",
            {
                "raw_transactions": len(transactions or []),
                "kpi_transactions": len(kpi_transactions or []),
                "warning": reconciliation_warning_hotfix,
            },
        )
    except Exception as exc:
        print("RECONCILIATION_WARNING_HOTFIX_V2_ERROR", str(exc))
'''

    if "RECONCILIATION_WARNING_HOTFIX_V2" not in text:
        anchors = ['print("KPI_AUDIT"', "print('KPI_AUDIT'"]
        inserted = False
        for anchor in anchors:
            idx = text.find(anchor)
            if idx != -1:
                line_start = text.rfind("\n", 0, idx)
                text = text[:line_start] + "\n" + insertion + text[line_start:]
                inserted = True
                break
        if not inserted:
            text += "\n" + insertion + "\n"

    if text != original:
        backup(path)
        path.write_text(text, encoding="utf-8")
        return True
    return False


def patch_extractor(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text

    helper = '''
def ensure_transaction_signed_amount(tx):
    if not isinstance(tx, dict):
        return tx
    if tx.get("signed_amount") is None:
        try:
            tx["signed_amount"] = float(tx.get("amount") or 0)
        except Exception:
            tx["signed_amount"] = 0.0
    if tx.get("_locked_amount") is None:
        tx["_locked_amount"] = tx["signed_amount"]
    if tx.get("locked_amount") is None:
        tx["locked_amount"] = tx["signed_amount"]
    return tx
'''

    if "def ensure_transaction_signed_amount(" not in text:
        if "def normalize_line_for_amount_detection" in text:
            text = text.replace("def normalize_line_for_amount_detection", helper + "\n\ndef normalize_line_for_amount_detection", 1)
        else:
            text += "\n\n" + helper + "\n"

    if "FINAL_TX_DEBUG" in text and "ensure_transaction_signed_amount(tx)" not in text:
        text = text.replace(
            'debug_log("FINAL_TX_DEBUG"',
            'tx = ensure_transaction_signed_amount(tx)\n        debug_log("FINAL_TX_DEBUG"',
        )
        text = text.replace(
            'print("FINAL_TX_DEBUG"',
            'tx = ensure_transaction_signed_amount(tx)\n        print("FINAL_TX_DEBUG"',
        )

    if "HOTFIX_V2_ZERO_AMOUNT_REPAIR" not in text:
        old = "return parse_terminal_amount(numbers[0], line)"
        new = '''amount = parse_terminal_amount(numbers[0], line)

    # HOTFIX_V2_ZERO_AMOUNT_REPAIR:
    # Avoid accepting 0.0 when the line contains a visible non-zero amount.
    if amount == 0 and len(numbers) >= 1:
        parsed_candidates = []
        for token in numbers:
            try:
                value = parse_terminal_amount(token, line)
                if value != 0:
                    parsed_candidates.append(value)
            except Exception:
                pass
        if parsed_candidates:
            amount = max(parsed_candidates, key=lambda x: abs(x))

    return amount'''
        if old in text:
            text = text.replace(old, new, 1)

    if text != original:
        backup(path)
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    changed = []

    for path in WORKER_CANDIDATES:
        if path.exists():
            if patch_worker(path):
                print(f"PATCHED worker: {path}")
                changed.append(path)
            else:
                print(f"UNCHANGED worker: {path}")

    for path in EXTRACTOR_CANDIDATES:
        if path.exists():
            if patch_extractor(path):
                print(f"PATCHED extractor: {path}")
                changed.append(path)
            else:
                print(f"UNCHANGED extractor: {path}")

    if not changed:
        print("No files changed. Check candidate paths.")
    else:
        print("\nChanged files:")
        for path in changed:
            print(f" - {path}")

    print("\nRun:")
    print("  python -m py_compile app/workers/finance_worker.py app/services/finance_agent/transaction_extractor.py")
    print("  git diff")
    print("  git add . && git commit -m 'finance hotfix v2 signed amount and reconciliation guards'")
    print("  git push")


if __name__ == "__main__":
    main()
