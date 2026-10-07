#!/bin/bash
# Test skill triggering with naive prompts
# Usage: ./run-test.sh <skill-name> <prompt-file>
#
# Tests whether Claude triggers a skill based on a natural prompt
# (without explicitly mentioning the skill)

set -e

SKILL_NAME="${1:-}"
PROMPT_FILE="${2:-}"
MAX_TURNS="${3:-3}"
EXPECTATION="${4:-present}"
OUTCOME_CASE="${5:-}"

if [ -z "$SKILL_NAME" ] || [ -z "$PROMPT_FILE" ]; then
    echo "Usage: $0 <skill-name> <prompt-file> [max-turns] [present|absent] [S1|S8]"
    echo "Example: $0 systematic-debugging ./test-prompts/debugging.txt"
    exit 1
fi

# Get the directory where this script lives (should be tests/skill-triggering)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Get the superpowers plugin root (two levels up from tests/skill-triggering)
PLUGIN_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

OUTPUT_DIR=$(mktemp -d "${TMPDIR:-/tmp}/cf-powers-trigger.XXXXXX")

# Read prompt from file
PROMPT=$(cat "$PROMPT_FILE")

echo "=== Skill Triggering Test ==="
echo "Skill: $SKILL_NAME"
echo "Prompt file: $PROMPT_FILE"
echo "Max turns: $MAX_TURNS"
echo "Output dir: $OUTPUT_DIR"
echo ""

# Copy prompt for reference
cp "$PROMPT_FILE" "$OUTPUT_DIR/prompt.txt"

PROJECT_DIR="$OUTPUT_DIR/project"
if [ -n "$OUTCOME_CASE" ]; then
    python3 "$SCRIPT_DIR/outcome-fixture.py" create "$PROJECT_DIR" "$OUTCOME_CASE" > "$OUTPUT_DIR/fixture-prompt.txt"
else
    python3 "$SCRIPT_DIR/prepare-fixture.py" "$PROJECT_DIR" "$SKILL_NAME"
fi

# Run Claude
LOG_FILE="$OUTPUT_DIR/claude-output.json"
cd "$PROJECT_DIR"

echo "Plugin dir: $PLUGIN_DIR"
echo "Running claude -p with naive prompt..."
status=0
bash "$SCRIPT_DIR/../claude-code/isolated-run.sh" 300 -p "$PROMPT" \
    --plugin-dir "$PLUGIN_DIR" \
    --dangerously-skip-permissions \
    --max-turns "$MAX_TURNS" \
    --output-format stream-json --verbose \
    > "$LOG_FILE" 2> "$OUTPUT_DIR/stderr.log" || status=$?

echo ""
echo "=== Results ==="

echo "Full log: $LOG_FILE"
python3 "$SCRIPT_DIR/check-result.py" "$LOG_FILE" "$SKILL_NAME" "$status" "$EXPECTATION"
if [ -n "$OUTCOME_CASE" ]; then
    python3 "$SCRIPT_DIR/outcome-fixture.py" check "$PROJECT_DIR" "$OUTCOME_CASE"
fi
