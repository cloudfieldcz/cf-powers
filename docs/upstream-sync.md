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

### 2026-07-25 — v6.0.3 → v6.2.0 (released as cf-powers v3.0.0)

Upstream shipped v6.1.0, v6.1.1 and v6.2.0 in this range — 70 commits.
**No new skills or agents were added**: the `SKILL.md` set is byte-identical
between v6.0.3 and v6.2.0, and upstream still has no `agents/` or `commands/`
directories. The three genuinely new files are all internals of existing
skills (`re-review-prompt.md`, `writing-good-tests.md`, and a test suite).

**Adopted:**

- **`find-polluter.sh` fix** (upstream #2008, #2011). `find .` emits
  `./`-prefixed paths, so the pattern in the script's own usage line matched
  nothing, and `wc -l` over empty input reported `Found 1`. Our copy was
  byte-identical to the broken version, so this was our bug too. Taken with
  upstream's test suite, adapted to our `tests/<area>/run-test.sh` layout.
- **Windows SessionStart hook `shell: "bash"`** (upstream #1751, #1918). A
  one-line fix for a silent total failure of the bootstrap on Windows; no-op
  on macOS/Linux, and older Claude Code ignores the unknown key. We ship the
  same polyglot `run-hook.cmd`, so we had the same exposure.
- **`writing-good-tests.md`**, replacing `testing-anti-patterns.md`. Our copy
  of the old file was byte-identical to upstream's, so a clean swap. The
  string-presence trap is the reason this one matters here: a repo that tests
  its own skills is exactly where grep-style assertions on prose look like
  tests and aren't.
- **The discard-menu removal** in `finishing-a-development-branch`. Adopted as
  a decision, not a diff — our copy diverged long ago.
- **The compression sweep.** Note that the TDD rebuttals were *folded into
  rationalization rows, not deleted*: upstream micro-tested each cut and
  found this one measurably degraded test-first behaviour (8/10 → 5/10 under
  "just write it, tests after" pressure, on both Claude and Codex). Anyone
  repeating this sweep should take the fold, never the bare deletion.
- **The `using-superpowers` bootstrap compression** — the only change in the
  repo with a recurring per-session token payoff. 116 → 73 lines.
- **The SDD restructure** — plan-scoped workspace and resume-based fix loop
  with a five-round breaker.

**Fork-specific adaptations** (where we deliberately diverge from upstream's text):

- **`.cf-powers/sdd/<plan>/`**, not `.superpowers/sdd/<plan>/`.
- **SDD Setup states our branch policy** — the human manages their own
  branches, no automatic worktrees — where upstream requires
  `using-git-worktrees`, which we do not ship. The process diagram's Setup
  node follows suit ("branch check", not "worktree").
- **The fix loop names Claude Code's `SendMessage`** and the recorded agent ID
  for resuming a live implementer, where upstream hedges with "if your harness
  cannot send another message to a live subagent". Being Claude-Code-only lets
  us be concrete.
- **`finishing-a-development-branch` keeps `gh pr create`**; upstream went
  forge-agnostic ("your forge's CLI, or the URL printed on push"). We are a
  GitHub shop and a concrete command beats a description of one.
- **`using-superpowers` keeps our Skip Flags table** (cf-powers v1.7.0), which
  upstream has no equivalent for, and keeps an H1, which upstream dropped —
  every other skill here has one and `writing-skills` mandates it.
- **The compression sweep extended to three reference files** upstream left
  alone (`condition-based-waiting.md`, `root-cause-tracing.md`,
  `testing-skills-with-subagents.md`), which carried the same unreproducible
  "2025-10-03 session" metrics as the skill bodies.

**Deliberately skipped:**

- The **vendor-neutral vocabulary rewrite**. Per standing policy.
- All **Codex work**: the `.agents/plugins/marketplace.json` manifest, the
  351-line `package-codex-plugin.sh` portal packaging script and its two test
  suites, and the hook removal/re-registration fixes.
- The **Gemini CLI removal and restoration** (removed in v6.1.0 on the news
  Google had EOLed it, reverted in v6.2.0). Net zero for us either way.
- **Pi, Antigravity and Cursor** references and their mapping tests.
- Upstream's **`docs/superpowers/specs/` and `docs/superpowers/plans/` eval
  records** for the SDD work (~3700 lines). We adopted the outcome, not the
  research trail.
- The **`brainstorming` and `using-git-worktrees` changes** — we ship neither.

**Not verified:** the subagent-behaviour suites were not run for this release
(they invoke real Claude sessions). The SDD skill body and the bootstrap both
changed substantially, so that is the outstanding gap.

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
  Interfaces block.** Structural plan improvements that pair with the SDD
  rework; adapted to our multi-phase plan template.
- **`subagent-driven-development` rewrite** (upstream v6.0.0 headline + the
  v6.0.3 Claude-Code-specific fix). One reviewer per task with two verdicts via
  a unified `task-reviewer-prompt.md` (the old `spec-reviewer-prompt.md` and
  `code-quality-reviewer-prompt.md` are removed); a single broad whole-branch
  review at the end; file-based handoff through new `scripts/task-brief`,
  `scripts/review-package`, `scripts/sdd-workspace` writing to a self-ignoring
  scratch dir; a required model per dispatch; banned severity suppression;
  read-only reviewers; a durable progress ledger; and an implementer that reads
  a brief and writes a report file with TDD evidence. Adapted to this fork:
  kept the Claude Code dialect (`Task tool`), our `docs/plans/` layout, and our
  reviewer set; used **`.cf-powers/sdd/`** instead of upstream's
  `.superpowers/sdd/`; dropped the `using-git-worktrees` integration line.
  Covered by a new `tests/sdd-scripts/run-test.sh`.

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

## Reference points

- Last fully-tracked upstream version: **v6.2.0** (synced in cf-powers v3.0.0).
- Last fully-tracked upstream version before this log started: **v5.0.7**
  (synced in cf-powers v1.4.1, commit `c107d3b`).
- Earlier syncs are recorded only in commit messages (`git log --grep upstream`).
