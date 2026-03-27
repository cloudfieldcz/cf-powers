---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** The user manages their own branches. Verify they are on a feature branch before starting.

**IMPORTANT:** The index file is the central orchestration point. Each phase plan must be self-contained — an executor should be able to pick up any single phase file and implement it without reading other phases.

## Multi-Phase Features

When the input (analysis document) defines multiple implementation phases, create **one plan file per phase** plus an **index file**:

```
docs/plans/YYYY-MM-DD-<feature-name>-plan-index.md    ← orchestration dashboard
docs/plans/YYYY-MM-DD-<feature-name>-plan-1-<phase>.md ← phase 1 tasks
docs/plans/YYYY-MM-DD-<feature-name>-plan-2-<phase>.md ← phase 2 tasks
docs/plans/YYYY-MM-DD-<feature-name>-plan-3-<phase>.md ← phase 3 tasks
```

For simple features with only one phase, skip the index and create a single plan: `docs/plans/YYYY-MM-DD-<feature-name>-plan.md`

### Index File Structure

```markdown
# [Feature Name] — Plan Index

**Source:** `docs/plans/YYYY-MM-DD-<feature-name>.md` (design + analysis)

**Created:** YYYY-MM-DD

## Phases

| # | Phase | Plan File | Status | Dependencies |
|---|-------|-----------|--------|--------------|
| 1 | <phase name> | [plan-1-<phase>.md](./YYYY-MM-DD-<feature-name>-plan-1-<phase>.md) | ⬚ Not started | — |
| 2 | <phase name> | [plan-2-<phase>.md](./YYYY-MM-DD-<feature-name>-plan-2-<phase>.md) | ⬚ Not started | Phase 1 |
| 3 | <phase name> | [plan-3-<phase>.md](./YYYY-MM-DD-<feature-name>-plan-3-<phase>.md) | ⬚ Not started | Phase 1 |

**Status legend:** ⬚ Not started · 🔨 In progress · ✅ Complete · ⏸ Blocked

## Notes

- Phases with no dependency between them can be executed in parallel
- Each phase plan is self-contained and can be executed independently via executing-plans or subagent-driven-development
```

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] — Phase N: [Phase Name]

> **For agentic workers:** REQUIRED SUB-SKILL: Use cf-powers:subagent-driven-development (recommended) or cf-powers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this phase builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Index:** [`plan-index.md`](./YYYY-MM-DD-<feature-name>-plan-index.md)

---
```

For single-phase plans (no index), omit the **Index:** line and the "Phase N:" from the title.

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## Plan Review Loop

After writing the complete plan:

1. Dispatch plan review subagents with precisely crafted review context — never your session history. This keeps reviewers focused on the plan, not your thought process.
   - **Developer review** (always): general-purpose subagent following cf-powers:review-as-dev — verifies file paths exist or marked as new, code snippets are correct, test cases cover the right scenarios, task ordering makes sense, no gaps between analysis and plan
   - **Security review** (if plan touches auth, data handling, external APIs, trust boundaries): general-purpose subagent following cf-powers:review-as-security — verifies plan doesn't introduce security regressions, trust boundaries are maintained, input validation is included in tasks
   - **Performance review** (if plan touches DB queries, data processing, caching, search): general-purpose subagent following cf-powers:review-as-perf — verifies indexes are planned, no N+1 patterns in tasks, caching strategy is sound, algorithm choices are appropriate
   - Provide each reviewer: path to the plan document, path to analysis/spec document
2. If Issues Found: fix the issues, re-dispatch reviewer for the whole plan
3. If Approved: proceed to execution handoff

**Review loop guidance:**
- Same agent that wrote the plan fixes it (preserves context)
- If loop exceeds 3 iterations, surface to human for guidance
- Reviewers are advisory — explain disagreements if you believe feedback is incorrect

## Execution Handoff

After saving all plan files and completing plan review, offer execution choice:

**For multi-phase plans:**

**"Plans complete. Index: `docs/plans/<filename>-plan-index.md`. Which phase to start with?"**

Then for the chosen phase:

**"Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use cf-powers:subagent-driven-development
- Fresh subagent per task + two-stage review

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL:** Use cf-powers:executing-plans
- Batch execution with checkpoints for review
