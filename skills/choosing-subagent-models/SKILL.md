---
name: choosing-subagent-models
description: Use before dispatching a subagent or performing a supported model or reasoning-effort selection. Inline work without a selection operation does not require this skill.
---

# Choosing Subagent Models

**Runtime:** Follow project instructions. Use native skill loading and ordinary
project reads directly. Before dispatch, resume, model selection, or shared plugin
resource resolution, read [runtime operations](../using-superpowers/references/runtime.md)
and the active-host reference once per context. Keep workflow decisions and child runtime constraints unchanged.

Pick the tier from how much the task has to *decide*, not from how important it feels.
Judgment is the default. Drop a tier when the task only executes decisions that are
already made. That drop is the purpose of this skill: a judgment-tier model on a
mechanical task wastes latency and quota.

## The Tiers

| Tier | Use for | Claude | Codex |
|---|---|---|---|
| **Mechanical** | Completely mechanical, no thinking required | `haiku` | `gpt-6-luna`, `low`–`medium` |
| **Implementation** | Work with the shape already decided | `sonnet` | `gpt-6-sol`, `medium` |
| **Judgment** (default) | Review of any kind, and work with an open question in it | `opus` | `gpt-6-sol`, `high` |
| **Complex judgment** (Codex only) | Architecture across systems; new transaction, concurrency or permission decisions; difficult race/crash/security tests; diagnosis across systems or security boundaries | `opus` | `gpt-6-astra`, `high` |

Claude aliases resolve to the newest model of each family. Pass the alias, not a
versioned name. The host enforces its own model and effort allowlist. Never pass a
Claude alias to Codex.

On Claude, a dispatch without `model` inherits the parent model. Inherit for judgment
work only when the parent runs Opus. Set `model` explicitly for every lower tier.

Select Fable only when the user names it for the task or the session. A Fable parent
does not select Fable for its children; select `opus` for them.

On Codex, start routine debugging on `gpt-6-sol`/`high`, also when the root cause is
unknown. Select `gpt-6-astra` when evidence shows complex interactions, or when Sol
repeatedly failed the narrowed task. Use the lower effort of a range for fully
specified work. Use `xhigh` for one specific difficult problem; `max` is never automatic.

Explicit user model and effort choices take precedence. If the host exposes no model
selection, continue on the current model and report that tier routing is unavailable.
This skill does not require delegation.

## Reviews Never Get Downgraded

Every reviewer — code, developer, business analyst, security, performance, plan review
and analysis cross-check — uses the judgment tier, irrespective of diff size. The
registered cf-powers reviewer agents pin `opus` in their frontmatter. A general-purpose
reviewer gets `opus` explicitly unless the parent runs Opus. On Codex, select
`gpt-6-sol`/`high`.

## Examples

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

## The Deciding Question

> Does this task require *deciding* anything, or only *executing* decisions
> already made?

Executing only → drop a tier. Still deciding → keep the tier. For Claude, the
implementation tier is the floor for work from prose rather than spelled-out code.

## Escalation

After repeated failure, move one tier up or narrow the task. Never repeat the same
unsuccessful approach unchanged. At the top tier, narrow the task, change the approach
or surface the unresolved decision to the user. You may tell the user that Fable is an
option; do not dispatch it until they ask.

## Make the Selection Explicit

Give each child a narrow task, necessary instructions, relevant file paths and an
output contract, in a clean context. Record the selected model (and effort on Codex),
or deliberate inheritance, in the brief or ledger.

## Red Flags

| Thought | Reality |
|---|---|
| "The parent is Opus, I'll just inherit" | Inheritance is a judgment-tier dispatch. For executing-only work, set the lower tier. |
| "The judgment tier is safer, I'll just use it everywhere" | Then the tiering does nothing. Safety belongs in the review tier, not the implementer tier. |
| "This is important, so it needs the big model" | Importance is not difficulty. A critical rename is still a rename. |
| "Cheapest tier for everything, it's a bulk edit" | If it works from prose or needs a judgement call, the mechanical tier will burn more turns than it saves. |
| "It's only a small diff, the implementation tier can review it" | Reviews stay on the judgment tier. Diff size does not change who is qualified to judge it. |
| "The same round failed, retry as-is" | A stuck loop needs a tier bump or fresh eyes, never an identical retry. |
