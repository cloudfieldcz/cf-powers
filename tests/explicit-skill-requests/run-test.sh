#!/bin/bash
# Test explicit skill requests (user names a skill directly)
# Usage: ./run-test.sh <skill-name> <prompt-file>
#
# Tests whether Claude invokes a skill when the user explicitly requests it by name
# (without using the plugin namespace prefix)
#
# Uses a disposable project and claude-code/isolated-run.sh (no user settings, CLAUDE.md or MCP;
# authentication from the active login or the variables documented in docs/testing.md).

set -e

SKILL_NAME="${1:-}"
PROMPT_FILE="${2:-}"
MAX_TURNS="${3:-3}"

if [ -z "$SKILL_NAME" ] || [ -z "$PROMPT_FILE" ]; then
    echo "Usage: $0 <skill-name> <prompt-file> [max-turns]"
    echo "Example: $0 subagent-driven-development ./prompts/subagent-driven-development-please.txt"
    exit 1
fi

# Get the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Get the superpowers plugin root (two levels up)
PLUGIN_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

OUTPUT_DIR=$(mktemp -d "${TMPDIR:-/tmp}/cf-powers-explicit.XXXXXX")

# Read prompt from file
PROMPT=$(cat "$PROMPT_FILE")

echo "=== Explicit Skill Request Test ==="
echo "Skill: $SKILL_NAME"
echo "Prompt file: $PROMPT_FILE"
echo "Max turns: $MAX_TURNS"
echo "Output dir: $OUTPUT_DIR"
echo ""

# Copy prompt for reference
cp "$PROMPT_FILE" "$OUTPUT_DIR/prompt.txt"

# Create a minimal project directory for the test
PROJECT_DIR="$OUTPUT_DIR/project"
mkdir -p "$PROJECT_DIR/docs/plans"
printf '%s\n' 'Use English for test responses. Read only this fixture and the plugin under test. Do not publish.' > "$PROJECT_DIR/CLAUDE.md"

# Create a dummy plan file for mid-conversation tests
cat > "$PROJECT_DIR/docs/plans/auth-system.md" << 'EOF'
# Auth System Implementation Plan

## Task 1: Add User Model
Create user model with email and password fields.

## Task 2: Add Auth Routes
Create login and register endpoints.

## Task 3: Add JWT Middleware
Protect routes with JWT validation.
EOF

# Run Claude with isolated environment
LOG_FILE="$OUTPUT_DIR/claude-output.json"
cd "$PROJECT_DIR"

echo "Plugin dir: $PLUGIN_DIR"
echo "Running claude -p with explicit skill request..."
echo "Prompt: $PROMPT"
echo ""

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
python3 "$SCRIPT_DIR/../skill-triggering/check-result.py" "$LOG_FILE" "$SKILL_NAME" "$status" present
# Invocation order and implementation outcomes require trace review; this checks discovery only.
