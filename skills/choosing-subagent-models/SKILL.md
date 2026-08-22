---
name: choosing-subagent-models
description: Use when dispatching any subagent - picks the model tier (Haiku / Sonnet / Opus) from how much judgement the task needs, instead of defaulting everything to the session model
---

# Choosing Subagent Models

Every dispatch carries an explicit model. Pick the tier from how much the task
has to *decide*, not from how important it feels.

**Core principle:** a large model on a mechanical task is wasted latency; a
small model on a review is a missed defect. Match the tier to the judgement
required.

## The Tiers

| Tier | `model` | Use for |
|---|---|---|
| **Haiku** | `"haiku"` | Completely mechanical, no thinking required |
| **Sonnet** | `"sonnet"` | Mechanical or simple work with the shape already decided |
| **Opus** (default) | omit `model` — inherits the session default | Review of any kind, and work with an open question in it |

**Reviews never get downgraded.** Leave `model` unset on a reviewer dispatch so it
inherits the session default, which is Opus here; the mistake to avoid is naming a
cheaper tier to save time. If the session itself is running on something cheaper,
name `"opus"` on the reviewer explicitly — inheriting is only right while the
default is the top tier. Every reviewer dispatch — `cf-powers:code-reviewer`,
`cf-powers:developer-reviewer`, `cf-powers:business-analyst-reviewer`,
`cf-powers:security-reviewer`, `cf-powers:performance-reviewer`, plan review,
analysis cross-check — runs on Opus. Review is where judgement pays: a green
test suite has repeatedly shipped defects that review caught.

## Mapping the Work

**Haiku**
- apply a named rename across a listed set of files
- fix stale line references, delete a listed set of dead lines
- mechanical locale / JSON / config edits
- run a fixed list of commands and report the output

**Sonnet**
- comment and docstring cleanups
- a documentation unit written against a finished plan
- a single-file implementation whose shape the plan already fixed
- transcription-plus-testing: the plan text contains the code to write
- writing a subordinate plan whose index already fixed its scope

**Opus**
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

## Always Set It Explicitly

An omitted model inherits the session's model. For a reviewer that is exactly
right — the session default is Opus. For anything mechanical it is the whole
problem: the tiering only saves anything if you name Haiku or Sonnet where they
belong. So make the tier a deliberate decision on every dispatch, and let it
default only when the answer really is Opus.

## Red Flags

| Thought | Reality |
|---|---|
| "Opus is safer, I'll just use it everywhere" | Then the tiering does nothing — the session default is already Opus, so 'not deciding' means paying it every time. Safety belongs in the review tier, not the implementer tier. |
| "This is important, so it needs the big model" | Importance is not difficulty. A critical rename is still a rename. |
| "Cheapest tier for everything, it's a bulk edit" | If it works from prose or needs a judgement call, Haiku will burn more turns than it saves. |
| "It's only a small diff, Sonnet can review it" | Reviews stay on Opus. Diff size does not change who is qualified to judge it. |
| "The same round failed, retry as-is" | A stuck loop needs a tier bump or fresh eyes, never an identical retry. |
