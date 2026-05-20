#!/usr/bin/env bash

set -e

CONTRACT_DIR="C:/Users/rachi/legal-ai-agent/backend/generated_contracts"
OUTPUT_DIR="quality_runs"

mkdir -p "$OUTPUT_DIR"

echo "==============================================="
echo "ENTERPRISE CONTRACT AGENT QUALITY TEST SUITE"
echo "==============================================="

TOTAL=0
SUCCESS=0
FAILURES=0

for file in "$CONTRACT_DIR"/*; do

    if [[ ! -f "$file" ]]; then
        continue
    fi

    filename=$(basename "$file")
    name="${filename%.*}"

    echo ""
    echo "------------------------------------------------"
    echo "TESTING: $filename"
    echo "------------------------------------------------"

    rm -rf debug_output

    python test_contract_quality.py "$file" \
        > "$OUTPUT_DIR/${name}_output.txt" 2>&1 || true

    if grep -q "VALID: True" "$OUTPUT_DIR/${name}_output.txt"; then
        VALID="TRUE"
    else
        VALID="FALSE"
    fi

    SCORE=$(grep "QUALITY SCORE:" "$OUTPUT_DIR/${name}_output.txt" | tail -1 | awk '{print $3}')

    if [[ -z "$SCORE" ]]; then
        SCORE="0"
    fi

    echo "VALID: $VALID"
    echo "SCORE: $SCORE"

    cp -r debug_output "$OUTPUT_DIR/${name}_debug_output" 2>/dev/null || true

    TOTAL=$((TOTAL + 1))

    if [[ "$VALID" == "TRUE" ]]; then
        SUCCESS=$((SUCCESS + 1))
    else
        FAILURES=$((FAILURES + 1))
    fi
done

echo ""
echo "==============================================="
echo "FINAL RESULTS"
echo "==============================================="
echo "TOTAL FILES: $TOTAL"
echo "SUCCESS: $SUCCESS"
echo "FAILURES: $FAILURES"

echo ""
echo "Reports saved in:"
echo "$OUTPUT_DIR"