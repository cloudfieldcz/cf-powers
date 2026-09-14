---
name: writing-plans
description: Use when you have a spec for a non-trivial task with non-obvious sequencing, multiple coordinated files, or unclear ordering of steps. SKIP when the task is mechanical (add one file, edit a config, one-liner) or when the implementation order is obvious from the request.
---

# Writing Plans

## Overview

A plan records **decisions the implementer cannot cheaply re-derive**: the order that keeps the tree green, the files two units both touch, the exact contract between units (names, signatures, payload shapes), values copied verbatim from the spec, and the specific trap in this codebase that will bite them. Everything the implementer would arrive at on their own by reading the surrounding code is **transcription**. Cut it.

Assume a skilled developer who knows almost nothing about our toolset or problem domain and who runs cf-powers:test-driven-development on their own. The plan tells them what to build and what must not be got wrong; it does not do the work for them in Markdown.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** The user manages their own branches. Verify they are on a feature branch before starting.

**IMPORTANT:** The index file is the central orchestration point. Each unit plan must be self-contained — an executor should be able to pick up any single plan file and implement it without reading other plans.

## Plan Budget

A plan is shorter than the code it describes: **at most a third of the production lines you expect the unit to add.** A unit that will add ~200 lines of code gets a **30-60 line** plan. Count before you save.

**Stop rule:** if your plan is longer than the diff will be, you are writing the implementation twice. Stop and cut it.

**Why:** a plan that contains the code is the implementation written once in Markdown and again in the editor by the same model, then deleted before the squash. One feature of 2 370 production lines carried 7 716 lines of plans — the largest line item on its branch, and none of it shipped.

## Units Are Vertical Slices

A unit (one plan file — a "phase" in the index) is a **user-visible capability end to end**: its validation, storage, endpoint and UI together, not a layer. The layers of one capability are reviewed and shipped together, so they are planned together.

**The split test:** if two units cannot be worked by two agents at the same time because they touch the same files, they are one unit. A shared-file table in a plan index is not a coordination aid — it is proof the split was wrong. Merge and re-plan.

**Default low.** Prefer 3 units over 12. Each extra unit costs a plan document, a review pass, a dispatch, a verdict and a status commit; split only where it buys real parallelism or a genuinely separate review gate. **Why:** a twelve-unit index split by layer (validation / columns / GraphQL / boot API / theme / context / page / …) had to list four groups of units sharing files. Nothing ran concurrently, and the split bought twelve rounds of overhead for what was three slices of work.

The analysis document's phases are a proposal, not the unit list. Apply the split test to them before creating plan files.

## Multi-Phase Features

When the work has more than one unit, create **one plan file per unit** plus an **index file**:

```
docs/plans/YYYY-MM-DD-<feature-name>-plan-index.md    ← orchestration dashboard
docs/plans/YYYY-MM-DD-<feature-name>-plan-1-<phase>.md ← phase 1 tasks
docs/plans/YYYY-MM-DD-<feature-name>-plan-2-<phase>.md ← phase 2 tasks
docs/plans/YYYY-MM-DD-<feature-name>-plan-3-<phase>.md ← phase 3 tasks
```

For a single-unit feature, skip the index and create a single plan: `docs/plans/YYYY-MM-DD-<feature-name>-plan.md`

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

- Phases with no dependency between them can be executed in parallel; if two phases share a file, they are one phase
- Each phase plan is self-contained and can be executed independently via executing-plans or subagent-driven-development
- Status cells are updated inside the phase's own last commit or once per batch — never in a commit of their own
```

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

## Task Granularity

A task is the smallest deliverable a fresh reviewer could reject while approving its neighbour. Fold setup, configuration, scaffolding and documentation into the task whose deliverable needs them.

A task states five things: what it delivers, which files, the contract it produces for later tasks, how it is verified, and the trap. Nothing else. Red-green-commit is the implementer's loop and already lives in cf-powers:test-driven-development — a plan does not enumerate "write the failing test / run it / implement / run / commit" per task. Those five lines, repeated twelve times, are the bulk of every oversized plan.

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] — Phase N: [Phase Name]

> **For agentic workers:** REQUIRED SUB-SKILL: Use cf-powers:subagent-driven-development (recommended) or cf-powers:executing-plans to implement this plan task-by-task. Tasks use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this phase builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Analysis:** [`YYYY-MM-DD-<feature-name>.md`](./YYYY-MM-DD-<feature-name>.md) — the design this plan implements

**Index:** [`plan-index.md`](./YYYY-MM-DD-<feature-name>-plan-index.md)

## Global Constraints

[The spec's project-wide requirements — version floors, dependency limits,
naming and copy rules, platform requirements — one line each, with exact
values copied verbatim from the spec. Every task's requirements implicitly
include this section.]

---
```

For single-phase plans (no index), omit the **Index:** line and the "Phase N:" from the title. Keep the **Analysis:** line either way — the plan argues from the analysis, so the analysis travels with it. Executors read both, and cf-powers:subagent-driven-development resolves plan conflicts against the analysis rather than guessing. A plan whose analysis is unreachable makes every conflict a coin flip.

## Task Structure

````markdown
### Task N: [Component Name]

- [ ] **Delivers:** [one sentence — the capability this task adds, as the user or the next task sees it]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact function names, parameter
  and return types. A task's implementer sees only their own task; this
  block is how they learn the names and types neighboring tasks use.]

**Decisions:** [only what is non-obvious and expensive to get wrong — a
schema, a migration, a limit or regex copied from the spec, a security
constraint. Code appears here only when a sentence cannot carry it.]

**Trap:** [the one thing in this codebase that will bite, e.g. "`TerraButton`
is a bare primitive; callers must add their own button chrome"]

**Verify:** `pytest tests/exact/path/to/test.py -v` green; [the spec
behaviour to check by hand]. If this task changes a rendered surface, the
last line is always: *open the affected screen in the running app and look
at it (screenshot).* This line is never folded away or delegated to a test.
````

## No Placeholders

Every task must contain what an engineer needs to act. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Similar to Task N" (state it again — the engineer may be reading tasks out of order)
- References to types, functions, or methods not defined in any task's Interfaces block

**Code belongs in a plan only where the choice is non-obvious and getting it wrong is expensive:** a schema, a migration, a cross-unit contract, a security constraint, an exact regex or limit from the spec. Never paste a component body, a test body, or a function the implementer will write anyway.

The replacement for a code block is the exact file, the exact signature, and the decision. `validate_branding_asset(kind, data) -> None, raises BrandingRefusal(code)` is a contract. Forty lines of its body is transcription.

## Plan Review

Review happens on code, once. A plan gets a review only when it draws a shape that is expensive to reverse after implementation starts: **if no task's Decisions block introduces a DB schema or migration, a public API or payload shape, or a cross-unit contract, skip the plan review entirely** and go to Execution Handoff.

When one of those is present: one reviewer, one pass, narrow scope. Dispatch a single general-purpose subagent with [plan-document-reviewer-prompt.md](plan-document-reviewer-prompt.md), giving it the plan path and the analysis path — never your session history.

The only findings it may return are ones **expensive or irreversible to discover later**:
- a DB schema or migration shape other units will build on
- a public API, payload or cross-unit contract shape
- an ordering that would leave the tree red, or a dependency the index has backwards
- two units that write the same files
- a spec requirement silently dropped from every task

Everything else — whether a test will pass, whether markup renders, naming, wording — the implementer finds out in one command and code review catches for free. A plan reviewer reasoning about it is guessing.

**One iteration.** Fix what came back; do not re-dispatch. If the reviewer returns more than ~3 must-fix items, the plan is too detailed, not too thin — cut it rather than grow it.

**Security review** (cf-powers:review-as-security) only where a trust boundary is drawn for the first time: a new endpoint's authz, a new upload path, a new external input. Not because the feature "touches data". No performance review of a document — performance is measured on code.

## Anti-patterns

**Reviewing the document instead of the code.** One branch ran three reviewers over its plans for up to three rounds each. The result: whole commits whose only content was edits to plan files; a destructive "reset all branding" button nobody had asked for, proposed as a review finding and inserted into a plan; and explicit approval of `<TerraButton style={{ color: "var(--danger)" }}>` on a primitive whose docstring says callers must supply their own look — which shipped as an unstyled scrap of red text a human found the next morning. A reviewer reading a document cannot see a rendered screen. It spent its budget where it was blind and approved what it could not check.

## Execution Handoff

After saving all plan files and completing any applicable plan review, link
the saved plan (or index) and summarize the decisions the user needs to see.
Preserve any execution method and phase order the user already supplied.
If execution is already authorized, continue using those choices; do not ask
for the same authorization again. If the user requested only a plan, deliver
it for review and wait for an execution request. Ask only for a missing choice
that matters to the handoff.

**For multi-phase plans when the starting phase has not been chosen:**

**"Plans complete. Please review the [index](docs/plans/<filename>-plan-index.md). Which phase should we start with?"**

**When no execution method has already been supplied:**

**"Plan saved: [plan](docs/plans/<filename>.md). Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use cf-powers:subagent-driven-development
- Fresh subagent per task + per-task review (spec + quality) + broad whole-branch review at the end

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL:** Use cf-powers:executing-plans
- Batch execution with checkpoints for review
