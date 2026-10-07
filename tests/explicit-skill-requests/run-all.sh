#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../skill-triggering/suite-summary.sh"
SUITE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/cf-powers-explicit-suite.XXXXXX")
echo "Suite logs: $SUITE_DIR"
for entry in subagent-driven-development:subagent-driven-development-please systematic-debugging:use-systematic-debugging analysis:please-use-analysis subagent-driven-development:mid-conversation-execute-plan; do
    skill=${entry%%:*}
    prompt=${entry#*:}
    status=0
    bash "$SCRIPT_DIR/run-test.sh" "$skill" "$SCRIPT_DIR/prompts/$prompt.txt" 3 > "$SUITE_DIR/$prompt.log" 2>&1 || status=$?
    cat "$SUITE_DIR/$prompt.log"
    record_result "$prompt" "$status"
done
finish_summary
