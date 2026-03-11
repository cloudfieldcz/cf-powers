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

> **For Claude:** REQUIRED SUB-SKILL: Use cf-powers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this phase builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Index:** [`plan-index.md`](./YYYY-MM-DD-<feature-name>-plan-index.md)

---
```

For single-phase plans (no index), omit the **Index:** line and the "Phase N:" from the title.

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## DEV Review Before Execution

**REQUIRED:** After saving all plan files (index + all phases), dispatch a Developer Review:

```
Agent tool:
  subagent_type: cf-powers:developer-reviewer
  description: "Dev review of implementation plan"
  prompt: >
    Review the implementation plan for completeness and technical correctness.

    Index file: docs/plans/YYYY-MM-DD-<feature-name>-plan-index.md
    Phase files: [list all phase files]

    Verify:
    - All file paths exist or are clearly marked as new
    - Code snippets are syntactically correct
    - Test cases cover the right scenarios
    - Task ordering and dependencies make sense
    - No gaps between analysis and plan

    Provide structured feedback.
```

Incorporate feedback before offering execution options.

## Execution Handoff

After saving all plan files and completing DEV review, offer execution choice:

**For multi-phase plans:**

**"Plans complete. Index: `docs/plans/<filename>-plan-index.md`. Which phase to start with?"**

Then for the chosen phase:

**"Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use cf-powers:subagent-driven-development
- Stay in this session
- Fresh subagent per task + code review

**If Parallel Session chosen:**
- Guide them to open new session
- **REQUIRED SUB-SKILL:** New session uses cf-powers:executing-plans
