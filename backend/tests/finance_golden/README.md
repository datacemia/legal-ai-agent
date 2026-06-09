
Finance golden regression.

Valider un relevé:
python tools/finance_golden_runner.py --statement tests/finance_golden/bank_001.txt --expected tests/finance_golden/bank_001.expected.json --update

Tester un relevé:
python tools/finance_golden_runner.py --statement tests/finance_golden/bank_001.txt --expected tests/finance_golden/bank_001.expected.json

Rejouer tous les relevés validés:
python tools/finance_golden_runner.py --all tests/finance_golden
