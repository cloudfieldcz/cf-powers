#!/usr/bin/env bash
# Test: subagent-driven-development skill
# Verifies that the skill is loaded and follows correct workflow
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "=== Test: subagent-driven-development skill ==="
echo ""

# Test 1: Verify skill can be loaded
echo "Test 1: Skill loading..."

output=$(run_claude "What is the subagent-driven-development skill? Describe its key steps briefly." 180)

if assert_contains "$output" "subagent-driven-development\|Subagent-Driven Development\|Subagent Driven" "Skill is recognized"; then
    : # pass
else
    exit 1
fi

if assert_contains "$output" "Load Plan\|read.*plan\|extract.*tasks" "Mentions loading plan"; then
    : # pass
else
    exit 1
fi

echo ""

# Test 2: Verify the task review carries both verdicts
# Since v2.0.0 there is ONE reviewer per task returning TWO verdicts, so there
# is no ordering between them — the separate spec-reviewer and
# code-quality-reviewer prompts were deleted. Assert both verdicts are required.
echo "Test 2: Task review verdicts..."

output=$(run_claude "In the subagent-driven-development skill, how many reviewers review each task, and which verdicts must the task review report?" 180)

if assert_contains "$output" "spec.*[Cc]ompliance\|[Ss]pec compliance" "Reports spec compliance verdict"; then
    : # pass
else
    exit 1
fi

if assert_contains "$output" "quality" "Reports quality verdict"; then
    : # pass
else
    exit 1
fi

if assert_contains "$output" "both\|two verdicts\|one review\|single review\|same review\|one reviewer\|single reviewer" "Both verdicts from one task review"; then
    : # pass
else
    exit 1
fi

echo ""

# Test 3: Verify self-review is mentioned
echo "Test 3: Self-review requirement..."

output=$(run_claude "Does the subagent-driven-development skill require implementers to do self-review? What should they check?" 180)

if assert_contains "$output" "self-review\|self review" "Mentions self-review"; then
    : # pass
else
    exit 1
fi

if assert_contains "$output" "completeness\|Completeness" "Checks completeness"; then
    : # pass
else
    exit 1
fi

echo ""

# Test 4: Verify plan is read once
echo "Test 4: Plan reading efficiency..."

output=$(run_claude "In subagent-driven-development, how many times should the controller read the plan file? When does this happen?" 180)

if assert_contains "$output" "once\|one time\|single" "Read plan once"; then
    : # pass
else
    exit 1
fi

# Assert the behaviour (read before any task is dispatched), not the section
# name — v3.0.0 renamed this phase from "Step 1"/"Load Plan" to "Setup", and a
# pattern matching only the old vocabulary is a change detector.
if assert_contains "$output" "[Ss]etup\|Step 1\|beginning\|start\|Load Plan\|before.*[Tt]ask 1\|before.*dispatch" "Read before dispatching any task"; then
    : # pass
else
    exit 1
fi

echo ""

# Test 5: Verify the task reviewer is skeptical
echo "Test 5: Task reviewer mindset..."

output=$(run_claude "What is the task reviewer's attitude toward the implementer's report in subagent-driven-development?" 180)

if assert_contains "$output" "not trust\|don't trust\|skeptical\|verify.*independently\|suspiciously" "Reviewer is skeptical"; then
    : # pass
else
    exit 1
fi

if assert_contains "$output" "read.*code\|inspect.*code\|verify.*code" "Reviewer reads code"; then
    : # pass
else
    exit 1
fi

echo ""

# Test 6: Verify review loops
echo "Test 6: Review loop requirements..."

output=$(run_claude "In subagent-driven-development, what happens if a reviewer finds issues? Is it a one-time review or a loop?" 180)

if assert_contains "$output" "loop\|again\|repeat\|until.*approved\|until.*compliant" "Review loops mentioned"; then
    : # pass
else
    exit 1
fi

if assert_contains "$output" "implementer.*fix\|fix.*issues" "Implementer fixes issues"; then
    : # pass
else
    exit 1
fi

echo ""

# Test 7: Verify task text is handed over as a brief file
# Inverted at v3.0.0: v2.0.0 replaced pasted task text with a file handoff
# (scripts/task-brief), because pasted text stays resident in the controller's
# context for the whole session. The implementer reads its brief; what it must
# never be handed is the whole plan file.
echo "Test 7: Task context provision..."

output=$(run_claude "In subagent-driven-development, how does the controller give the implementer its task text? Name the mechanism." 180)

if assert_contains "$output" "brief\|task-brief" "Uses a task brief"; then
    : # pass
else
    exit 1
fi

if assert_contains "$output" "file\|path" "Brief is handed over as a file"; then
    : # pass
else
    exit 1
fi

if assert_not_contains "$output" "whole plan\|entire plan\|full plan file" "Doesn't hand over the whole plan"; then
    : # pass
else
    exit 1
fi

echo ""

# Test 8: Verify branch check requirement
echo "Test 8: Branch check requirement..."

output=$(run_claude "What workflow skills are required before using subagent-driven-development? List any prerequisites or required skills." 180)

if assert_contains "$output" "branch\|feature.branch\|main" "Mentions branch verification"; then
    : # pass
else
    exit 1
fi

echo ""

# Test 9: Verify main branch warning
echo "Test 9: Main branch red flag..."

output=$(run_claude "In subagent-driven-development, is it okay to start implementation directly on the main branch?" 180)

if assert_contains "$output" "worktree\|feature.*branch\|not.*main\|never.*main\|avoid.*main\|don't.*main\|consent\|permission" "Warns against main branch"; then
    : # pass
else
    exit 1
fi

echo ""

echo "=== All subagent-driven-development skill tests passed ==="
