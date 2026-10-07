#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/suite-summary.sh"
SUITE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/cf-powers-trigger-suite.XXXXXX")
echo "Suite logs: $SUITE_DIR"
for skill in systematic-debugging test-driven-development writing-plans dispatching-parallel-agents analysis executing-plans requesting-code-review; do
    status=0
    bash "$SCRIPT_DIR/run-test.sh" "$skill" "$SCRIPT_DIR/prompts/$skill.txt" 3 > "$SUITE_DIR/$skill.log" 2>&1 || status=$?
    cat "$SUITE_DIR/$skill.log"
    record_result "$skill" "$status"
done
status=0
bash "$SCRIPT_DIR/run-test.sh" analysis "$SCRIPT_DIR/prompts/no-analysis-config.txt" 12 absent S1 > "$SUITE_DIR/no-analysis.log" 2>&1 || status=$?
cat "$SUITE_DIR/no-analysis.log"
record_result "negative analysis outcome" "$status"
finish_summary
