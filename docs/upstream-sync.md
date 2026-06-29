# Upstream Sync Log

cf-powers is a fork of [obra/superpowers](https://github.com/obra/superpowers).
This file records each time we pull changes down from upstream: when it happened,
which upstream version range it covered, what we adopted and why, and — just as
important — what we deliberately left behind.

## Standing policy

cf-powers targets **Claude Code only**. That shapes what we take:

- **We do not take vendor-neutralization.** Upstream rewrites Claude-specific
  vocabulary ("use the Task tool", "put it in CLAUDE.md", "future Claude") into
  generic phrasing ("dispatch a subagent", "your instructions file", "your
  agent") so one skill set runs on Codex/Gemini/Copilot/Kimi/Pi/Antigravity. For
  a Claude-Code-only fork that is churn at best and a small loss of precision at
  worst, so we keep the Claude dialect.
- **We skip other-harness machinery wholesale** — per-runtime tool references,
  bootstraps, manifests, and install docs for non-Claude harnesses.
- **We keep our own additions** that have no upstream equivalent: the `analysis`
  workflow, `documenting-changes`, the four `review-as-*` skills and their
  paired reviewer agents, the multi-phase plan index, and the Czech-output
  analysis dialogue.

We take, adapted to the above: genuine bug fixes, and skill-content improvements
whose value is independent of harness.

## Sync history

### 2026-06-29 — v5.0.7 → v6.0.3 (released as cf-powers v2.0.0)

Upstream shipped v5.1.0 and a major v6.0.0 (+ v6.0.1–v6.0.3) in this range.
**No new skills or agents were added** — the skill list is identical between
v5.0.7 and v6.0.3. Upstream has no `agents/` or `commands/` directories; those
are ours.

**Adopted:**

- **`systematic-debugging` — extended-thinking keyword fix** (upstream #1283).
  The bullet `"Ultrathink this"` is the exact token Claude Code scans for and
  was silently flipping every session that loaded the skill into extended
  thinking. Changed to `"Ultra-think this"`. Pure Claude Code defect; highest
  value, lowest risk item in the whole range.
- **`writing-skills` — "Match the Form to the Failure"** table and the
  **"Micro-Test Wording Before Full Scenarios"** section, plus two checklist
  items. Harness-independent guidance for skill authors (us). Taken close to
  verbatim — these are upstream's own wording-tested additions.
- **`writing-skills` — incidental fixes** consistent with the skill's own
  advice: restored the missing step 2 in the Discovery Workflow list, replaced
  two `@`-prefixed links with plain references (`@` force-loads and burns
  context), renumbered the duplicate `### 4.` heading to `### 5.`.
- **`writing-plans` — Task Right-Sizing, Global Constraints block, per-task
  Interfaces block.** Structural plan improvements that pair with the upstream
  SDD rework; adapted to our multi-phase plan template.

**Deliberately skipped:**

- The **vendor-neutral vocabulary rewrite** across all skills and the new
  `skills/using-superpowers/references/*-tools.md` per-harness tool references
  (Claude Code, Codex, Copilot, Gemini, Pi, Antigravity). Per standing policy.
- The **CSO → SDO rename** ("Claude Search Optimization" → "Skill Discovery
  Optimization"). Cosmetic for a Claude-only fork; we kept "CSO".
- All **new harness support** (Kimi Code, Pi, Antigravity) and existing-harness
  updates (Codex, OpenCode, Cursor).
- The **brainstorming visual-companion** security/robustness work — we don't
  ship the `brainstorming` skill.
- The **evals submodule migration** and Windows hook fixes.

**Deferred — decide separately:**

- The **`subagent-driven-development` rewrite** (the v6.0.0 headline): one
  reviewer per task, file-based handoff via new `task-brief` / `review-package`
  / `sdd-workspace` scripts, a required model per dispatch, banned severity
  suppression, read-only skeptical reviewers, a progress ledger, and the unified
  `task-reviewer-prompt.md`. Includes the v6.0.3 Claude-Code-specific fix moving
  scratch artifacts out of the protected `.git/` path into `.superpowers/sdd/`.
  High value but a large, divergent change against our customized SDD skill —
  port (whole or in part) as its own piece of work.

## Reference points

- Last fully-tracked upstream version before this log started: **v5.0.7**
  (synced in cf-powers v1.4.1, commit `c107d3b`).
- Earlier syncs are recorded only in commit messages (`git log --grep upstream`).
