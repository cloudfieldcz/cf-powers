---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Requesting Code Review

**Runtime:** Follow project instructions. Use native skill loading and ordinary
project reads directly. Before dispatch, resume, model selection, or shared plugin
resource resolution, read [runtime operations](../using-superpowers/references/runtime.md)
and the active-host reference once per context. Keep workflow decisions and child runtime constraints unchanged.

Dispatch cf-powers:code-reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or: git merge-base origin/main HEAD
HEAD_SHA=$(git rev-parse HEAD)
```

Use the merge-base form against main. A plain `origin/main` shows phantom deletions once main moves.

**2. If the diff touches a rendered surface, capture it:** open the affected
screen in the running app (the built-in `run` skill, or Playwright
`browser_take_screenshot`) and save the screenshot path for the package. A
diff-only reviewer has exactly the blindness a plan reviewer has — it cannot
see a screen — and it approved markup that shipped as unstyled bare text.
If you cannot capture it, the reviewer must be told to run the app itself.

**3. Dispatch code-reviewer subagent:**

Use the active runtime with the cf-powers code-reviewer role and fill the
template at `code-reviewer.md`. On Codex, pass the resolved absolute path to
`agents/code-reviewer.md` as well as the template and evidence; its frontmatter
is Claude registration metadata, while the body is the shared review role.

Dispatch it on the **judgment tier**. Inherit only when the parent is known to
provide that tier. Review is the one role that is never downgraded to a cheaper tier,
however small the diff; see cf-powers:choosing-subagent-models.

**Placeholders:**
- `{WHAT_WAS_IMPLEMENTED}` - What you just built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{DESCRIPTION}` - Brief summary
- `{UI_EVIDENCE}` - Screenshot path(s) of every screen the diff touches, or "no rendered surface changed", or "run it: <how>"

**4. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch cf-powers:code-reviewer subagent]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just review the diff myself instead of dispatching a reviewer" | You're the coordinator — reviewing the diff inline burns the context window you need to keep driving the work. Dispatch a reviewer subagent: the diff and the evaluation live in its context, and only the findings come back to you. |
| "The UI is covered by component tests, no screenshot needed" | Tests assert a testid exists. Neither the test nor a diff reader can see that the control looks like a paragraph. Capture the screen. |
| "The reviewer needs my whole session history to understand the change" | Hand it precisely crafted context, never your session's history. That keeps the reviewer on the work product, not your thought process. |

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: requesting-code-review/code-reviewer.md
