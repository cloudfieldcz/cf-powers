---
name: choosing-subagent-models
description: Use when dispatching any subagent - picks the model tier (mechanical / implementation / judgment) from how much judgement the task needs, instead of defaulting everything to the session model
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

Resolve these tiers with the active runtime reference. Claude maps them to
Haiku / Sonnet / Opus; Codex selects from the exposed model allowlist and sets
supported reasoning effort. A tier label is not a model ID.

**Reviews never get downgraded.** Every reviewer — code, developer, business
analyst, security, performance, plan review and analysis cross-check — uses the
judgment tier, irrespective of diff size. Inherit only when the parent is known
to provide that tier; otherwise select it explicitly. Explicit user model choices
still take precedence. If tier selection is unavailable, report that limitation
instead of silently claiming an inherited model is the top tier.

## Mapping the Work

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

When two tiers both look defensible, weigh turn count, not token price: the
cheapest model routinely takes 2-3x the turns on multi-step work and costs more
overall. Mid-tier is the floor for anything working from prose rather than from
spelled-out code.

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
