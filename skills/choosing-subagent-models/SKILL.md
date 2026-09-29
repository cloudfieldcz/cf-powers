---
name: choosing-subagent-models
description: Use when selecting a model or reasoning effort for a workflow, or before dispatching any subagent
---

# Choosing Subagent Models

**Runtime:** Before using host tools or dispatching, read [runtime operations](../using-superpowers/references/runtime.md) and its active-host reference (once per context). Keep this skill's workflow decisions unchanged.

Every dispatch carries a deliberate model selection. Pick the tier from how much the task
has to *decide*, not from how important it feels.

**Core principle:** a large model on a mechanical task is wasted latency; a
small model on a review is a missed defect. Match the tier to the judgement
required.

## The Tiers

| Tier | Use for |
|---|---|
| **Mechanical** | Completely mechanical, no thinking required |
| **Implementation** | Simple work with the shape already decided |
| **Judgment** (default) | Review of any kind, and work with an open question in it |

Claude resolves these tiers to Haiku / Sonnet / Opus through its runtime
reference. Claude Fable runs only on an explicit user request. For Codex, the
task-specific defaults below take precedence over generic tier examples here and
in other workflows. A tier label is not a model ID.

## Claude models

| Tier | Model |
|---|---|
| Mechanical | Haiku (the `haiku` alias; a newer Haiku replaces 4.5 when it ships) |
| Implementation | Sonnet 5.5 |
| Judgment | Opus 5.5 |
| On explicit user request only | Fable 5.1 |

Select Fable only when the user names it for the task or the session. Task
difficulty, repeated Opus failure, repository size and review scope do not
select Fable. When Opus repeatedly fails the same acceptance criteria, narrow
the task, change the approach or surface the unresolved decision to the user.
This replaces a workflow's "one tier up" step when the stuck worker already ran
on Opus. You may tell the user that Fable is an option; do not dispatch it until they ask.
A Fable parent session does not select Fable for its children. Select Opus
explicitly unless the user asked for Fable subagents.

For a requested Fable dispatch, verify the exact model, account/provider
availability and supported effort in the Claude runtime reference. Record the
actual model and effort. If Fable is unavailable, report the limitation and
continue on Opus. Never claim that Fable ran when the host substituted another
model.

## Codex defaults — single source of truth

These are workflow recommendations, not benchmark results or guaranteed savings
against a weekly usage limit. Do not add volatile pricing multipliers.

| Work | Tier | Model | Reasoning effort |
|---|---|---|---|
| Analysis of a bounded feature | Judgment | `gpt-6-sol` | `high` |
| Architecture across systems, analysis with unresolved architecture | Complex judgment | `gpt-6-astra` | `high` |
| Main implementation plan | Judgment | `gpt-6-sol` | `medium`; `high` with major decisions still open |
| Breakdown of an already-decided phase | Implementation | `gpt-6-sol` | `medium` |
| Routine programming from a plan | Implementation | `gpt-6-sol` | `medium` |
| Complex implementation with interfaces and invariants already decided | Implementation | `gpt-6-sol` | `high` |
| New decisions about transactions, concurrency or permissions | Complex judgment | `gpt-6-astra` | `high` |
| Routine test writing | Implementation | `gpt-6-sol` | `medium` |
| Design of difficult race/crash/security tests | Complex judgment | `gpt-6-astra` | `high` |
| Running specified tests, collecting results, codegen | Mechanical | `gpt-6-luna` | `low` |
| Mechanical edits, renames, precisely specified documentation | Mechanical | `gpt-6-luna` | `low`–`medium` |
| All reviews, including security reviews and rechecks | Judgment | `gpt-6-sol` | `high` |
| Coordination of decided tasks | Implementation | `gpt-6-sol` | `medium` |
| Coordination involving design decisions | Judgment | `gpt-6-sol` | `high` |
| Routine debugging, including an initially unknown root cause | Judgment | `gpt-6-sol` | `high` |
| Diagnosis requiring complex reasoning across systems, concurrency or security boundaries | Complex judgment | `gpt-6-astra` | `high` |

`gpt-6-sol` is the Codex default. Use `gpt-6-astra` only for the complex-judgment
rows, or when `gpt-6-sol` repeatedly failed the same acceptance criteria after
the task was narrowed.

Start routine diagnosis on `gpt-6-sol`. An unknown root cause alone does not
justify `gpt-6-astra`. Select Astra when evidence shows complex interactions
across systems, concurrency or security boundaries, or when the repeated-failure
rule above applies.

Explicit user model/effort choices take precedence. Before selecting, verify the
models and supported effort values exposed by the current host; this table does
not establish availability. Within a range, use the lower effort for fully
specified work and the higher effort for remaining complexity or major decisions.
Use `xhigh` for a specific difficult problem; `max`/`ultra` are exceptional,
never automatic defaults. If a model or effort is unavailable, follow the
runtime fallback, record the limitation and preserve the required tier.

This table neither requires delegation nor authorizes unsupported changes to
the current session model. Apply it when the host supports selection; otherwise
continue authorized work on the current model and disclose the limitation.

Give each child a narrow task, necessary instructions, relevant file paths and
an output contract. Use a clean context rather than automatically passing the
whole history. Scope rechecks to the findings, changes and relevant regression
evidence. After repeated failure, escalate the model or narrow the task; never
repeat the same unsuccessful approach unchanged. If already at the highest
available tier, narrow the task rather than automatically raising effort.

**Reviews never get downgraded.** Every reviewer — code, developer, business
analyst, security, performance, plan review and analysis cross-check — uses the
judgment tier, irrespective of diff size: Opus on Claude, `gpt-6-sol`/`high` on
Codex. Inherit only when the parent is known
to provide that tier; otherwise select it explicitly. Explicit user model choices
still take precedence. If tier selection is unavailable, report that limitation
instead of silently claiming an inherited model is the top tier.

## Generic tier examples (Claude; Codex uses the table above)

**Mechanical**
- apply a named rename across a listed set of files
- fix stale line references, delete a listed set of dead lines
- mechanical locale / JSON / config edits
- run a fixed list of commands and report the output

**Implementation**
- comment and docstring cleanups
- a documentation unit written against a finished plan
- a single-file implementation whose shape the plan already fixed
- transcription-plus-testing: the plan text contains the code to write
- writing a subordinate plan whose index already fixed its scope

**Judgment**
- every reviewer agent, plan review, analysis
- an implementation unit whose predicate, contract or security boundary is
  still an open question
- multi-file coordination, debugging an unknown root cause, architecture
- the final whole-branch review
- fix-loop escalation after a lower tier got stuck (always at least one tier up)

## The Deciding Question

> Does this task require *deciding* anything, or only *executing* decisions
> already made?

Executing only → drop a tier. Still deciding → keep the tier.

For tasks not covered by the Codex table, choose by unresolved decisions and
validate the selection against observed results. Do not infer cost or quota
savings from a tier label. For Claude, the implementation tier remains the
floor for work from prose rather than spelled-out code.

## Make the Selection Explicit

Choose the tier deliberately on every dispatch. Record the actual model and
supported reasoning effort (Codex), or deliberate inheritance, in the brief or
ledger. The mechanical and implementation tiers save work only when they select
an appropriate cheaper model; review remains at the judgment tier. Use the
runtime reference for available parameters and the no-routing fallback.

## Red Flags

| Thought | Reality |
|---|---|
| "The judgment tier is safer, I'll just use it everywhere" | Then the tiering does nothing — 'not deciding' means paying the judgment tier every time. Safety belongs in the review tier, not the implementer tier. |
| "This is important, so it needs the big model" | Importance is not difficulty. A critical rename is still a rename. |
| "Cheapest tier for everything, it's a bulk edit" | If it works from prose or needs a judgement call, the mechanical tier will burn more turns than it saves. |
| "It's only a small diff, the implementation tier can review it" | Reviews stay on the judgment tier. Diff size does not change who is qualified to judge it. |
| "The same round failed, retry as-is" | A stuck loop needs a tier bump or fresh eyes, never an identical retry. |
