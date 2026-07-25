# Changelog

All notable changes to cf-powers will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.0.0] — 2026-07-25

Selective sync from upstream [obra/superpowers](https://github.com/obra/superpowers)
v6.0.3 → v6.2.0 (70 commits, upstream releases v6.1.0, v6.1.1 and v6.2.0).
**No new skills or agents appeared upstream** — the `SKILL.md` set is
byte-identical between v6.0.3 and v6.2.0, and upstream still has no `agents/`
or `commands/` directories. Only the Claude-Code-relevant changes were adopted;
all Codex/Gemini/Pi/Antigravity/Cursor work and the vendor-neutral vocabulary
rewrite were deliberately skipped. See [docs/upstream-sync.md](docs/upstream-sync.md)
for the full record and rationale.

The major bump is for the SDD helper scripts: `review-package` gained a leading
`PLAN_FILE` argument and `sdd-workspace` now requires one, so any direct caller
breaks.

### Added
- **`skills/test-driven-development/writing-good-tests.md`** — replaces
  `testing-anti-patterns.md`. Rebuilt as a positive catalog and absorbs a
  falsifiability discipline: name the production change that would fail the
  test, derive expectations independently of the code under test, and close
  with a mutation check. Two traps are named with a hard stop in the gate
  function — the **string-presence trap** (grep-style assertions on scripts,
  skills and prompts counterfeit falsifiability; the observable is behaviour,
  never text) and the **change-detector trap** (a constant assertion can fail
  on every intentional edit and still protect nothing).
- **`skills/subagent-driven-development/re-review-prompt.md`** — scoped
  re-review template. Verdicts each prior finding ADDRESSED / NOT ADDRESSED,
  inspects only the fix diff, and routes out-of-scope observations to the
  ledger so they cannot extend the loop. Read-only, model required.
- **SDD five-round circuit breaker and controller adjudication** — park with a
  ruling, or STOP as `BLOCKED` when a finding is load-bearing. Every ruling is
  a ledger entry.
- **`tests/systematic-debugging/run-test.sh`** — four scenarios over
  `find-polluter.sh` in throwaway toy projects with a stubbed `npm`.
- **Rationalization tables** in `finishing-a-development-branch` (8 rows) and
  `requesting-code-review` (2 rows).

### Changed
- **SDD workspace is plan-scoped** (**breaking**). `sdd-workspace PLAN_FILE`
  resolves `.cf-powers/sdd/<plan-basename>/`; `review-package` takes
  `PLAN_FILE` as its first argument; the ledger names its plan on line 1; the
  workspace is deleted once the final review is clean. The flat directory had
  no plan identity and no end-of-life, so a follow-up plan in the same working
  tree could read the previous plan's ledger as its own progress — upstream
  observed this in the wild, and measured 6–13 tool calls of cross-plan git
  forensics per resume even when controllers correctly refused the stale
  ledger. The `.gitignore` moves up to `.cf-powers/sdd/`, covering every plan.
- **SDD fix loop resumes the implementer.** A round is one fix dispatch plus
  one scoped re-review. Rounds 1-3 resume the original implementer via
  `SendMessage` (context intact); rounds 4-5 dispatch fresh on a more capable
  model. `SKILL.md` is reorganized by lifecycle. Previously the loop had no
  termination condition at all.
- **`finishing-a-development-branch` no longer offers to discard your work.**
  The skill runs when the work is finished and green, so "Discard this work"
  next to "Merge" advertised destroying it. Discard survives as an
  explicit-request-only path with the same typed-`discard` ritual. Also:
  confirm the base branch before merging, and stop on a failing merged result.
- **`using-superpowers` bootstrap compressed**, 116 → 73 lines and 5583 → 4132
  bytes (−26%). It is injected into every session, so its size is a recurring
  cost. The graphviz flowchart encoded exactly two sentences as nine nodes and
  eight edges and is now those sentences; Instruction Priority folded into
  User Instructions. Both flag tables survive untouched, including our
  fork-specific Skip Flags table.
- **Compression sweep across 9 skills** — recaps, benefits-selling prose, and
  metrics this fork never measured are gone. Load-bearing arguments were
  relocated, not deleted: TDD's "Why Order Matters" rebuttals became
  Common Rationalizations rows because upstream measured outright deletion
  degrading test-first behaviour under pressure (8/10 → 5/10, on both Claude
  and Codex), and `systematic-debugging`'s verification pointer moved into
  Phase 4 Step 3 where the agent stands when it needs it.
- **`hooks/hooks.json` declares `"shell": "bash"`** on the SessionStart hook.
  The Windows docs' canonical `hooks.json` example was also realigned with the
  shipped file — it still showed `session-start.cmd` and a `resume` matcher.

### Fixed
- **`find-polluter.sh` finds test files again.** `find .` emits `./`-prefixed
  paths, so the pattern in the script's own usage line (`src/**/*.test.ts`)
  matched nothing — and `wc -l` over empty input then reported
  `Found 1 test files`, so the script claimed to be working while running zero
  tests. Also matches `**/` collapsed, so a test directly under the base
  directory is no longer silently skipped. (upstream #2008, #2011)
- **The Windows SessionStart hook loads the bootstrap again.** The command
  string starts with a quoted path, which broke both shells Claude Code may
  hand it: PowerShell parsed the quoted string as an expression and died on
  the next bareword, and cmd.exe's `/c` quote rule dropped the outer quotes
  when the path contained a metacharacter, truncating at a `(` in a profile
  path. Either way the bootstrap silently never loaded. Claude Code ≥ 2.1.81
  resolves `shell: "bash"` to Git for Windows; older versions ignore the key.
  (upstream #1751, #1918)

### Removed
- `skills/test-driven-development/testing-anti-patterns.md` (superseded).
- `spec-reviewer`-era trailing note in `task-reviewer-prompt.md`; the fix loop
  owns that behaviour now.
- Recap and social-proof sections: `The Bottom Line` from
  `receiving-code-review`, `writing-skills` and `verification-before-completion`;
  `Real-World Impact` and `Key Benefits` from `dispatching-parallel-agents`;
  `Why This Matters` from `verification-before-completion`; `Real-World Impact`
  from `systematic-debugging` and from three reference files
  (`condition-based-waiting.md`, `root-cause-tracing.md`,
  `testing-skills-with-subagents.md`); `Remember` from `writing-plans`, which
  also removes its instruction to use `@` syntax — a contradiction with
  `writing-skills`, which warns `@` force-loads the file on every load.
- `Integration` listings from `requesting-code-review`, `executing-plans`,
  `finishing-a-development-branch` and `subagent-driven-development`. Every
  named skill already appears at its point of use.

### Testing
Offline suites green: `tests/sdd-scripts/run-test.sh`,
`tests/systematic-debugging/run-test.sh`, `tests/integrity/run-test.sh`.

The subagent-behaviour suites (`tests/subagent-driven-dev/`,
`tests/claude-code/`, `tests/skill-triggering/`,
`tests/explicit-skill-requests/`) invoke real Claude sessions and **were not
run** for this release. The SDD skill body and the `using-superpowers`
bootstrap both changed substantially, so those suites are the outstanding
verification gap.

## [2.0.0] — 2026-06-29

Selective sync from upstream [obra/superpowers](https://github.com/obra/superpowers)
v5.1.0 → v6.0.3 (our last sync was v5.0.7). No new skills or agents appeared
upstream in that range. Only the Claude-Code-relevant changes were adopted;
the multi-harness work and vendor-neutral vocabulary rewrite were deliberately
skipped. See [docs/upstream-sync.md](docs/upstream-sync.md) for the full record
and rationale.

The headline is the **subagent-driven-development rewrite** — a breaking change
for anyone dispatching the old reviewer prompt files (hence the major bump).

### Changed
- **`subagent-driven-development` rewritten** (upstream v6.0.0 + the v6.0.3
  Claude Code fix), adapted to this fork:
  - One reviewer per task with two verdicts (spec compliance + code quality)
    via a single new `task-reviewer-prompt.md`, replacing the separate
    `spec-reviewer-prompt.md` and `code-quality-reviewer-prompt.md` (both
    removed — **breaking** if you dispatched them directly).
  - A single broad whole-branch review at the end (reuses
    `requesting-code-review`'s `code-reviewer.md`) instead of re-reviewing
    every task.
  - File-based handoff: new `scripts/task-brief`, `scripts/review-package`,
    and `scripts/sdd-workspace` write task text, review diffs, and a progress
    ledger to a self-ignoring `.cf-powers/sdd/` directory in the working tree
    — not under `.git/`, which Claude Code denies agent writes to. (We use
    `.cf-powers/sdd/`, not upstream's `.superpowers/sdd/`.)
  - Every dispatch must name its model explicitly (an omitted model silently
    inherits the session's most expensive one); a pre-flight plan review; the
    controller may no longer tell a reviewer what to ignore or pre-rate
    severity; reviewers are read-only; a durable progress ledger lets a
    compacted controller resume instead of re-running finished tasks.
  - `implementer-prompt.md` now reads a task brief, writes a detailed report
    to a file, returns a <15-line summary, and carries TDD red/green evidence.
  - Kept the Claude Code dialect (`Task tool (general-purpose)`) and our
    `docs/plans/` layout; dropped the upstream `using-git-worktrees`
    integration line (we manage branches ourselves).
- `tests/sdd-scripts/run-test.sh` added — covers `sdd-workspace`,
  `task-brief` (incl. the code-fence guard), and `review-package`
  (multi-commit range) in throwaway git repos.

### Fixed
- `systematic-debugging`: the redirection bullet read `"Ultrathink this"`, the
  exact keyword Claude Code scans for — it silently switched every session that
  loaded the skill into extended thinking. A hyphen (`"Ultra-think this"`)
  breaks the keyword while keeping the text readable. (upstream #1283)
- `writing-skills`: the Discovery Workflow list skipped step 2; restored
  "Searches skills". Replaced two `@`-prefixed file links with plain references
  (the skill's own guidance warns `@` force-loads files and burns context).
  Fixed the duplicate `### 4.` heading (Cross-Referencing is now `### 5.`).

### Added
- `writing-skills`: **Match the Form to the Failure** — a table for picking the
  right kind of guidance (prohibition vs. positive recipe vs. structural slot vs.
  conditional) based on the baseline failure type, with a scope note on the
  Bulletproofing section. **Micro-Test Wording Before Full Scenarios** — a cheap
  per-wording verification step (no-guidance control, 5+ reps, manual reads)
  before committing to full pressure scenarios. Two matching checklist items.
- `writing-plans`: **Task Right-Sizing** guidance, a **Global Constraints** block
  in the plan header template (project-wide rules copied verbatim), and a
  per-task **Interfaces** block (consumes/produces contracts for implementers who
  see only their own task).

## [1.8.0] — 2026-05-18

### Added
- SHA-256 integrity baseline for every `skills/*/SKILL.md` file
  (`.claude-plugin/integrity.sha256`).
- `bin/update-integrity` helper that regenerates the baseline by
  discovering every `skills/<name>/SKILL.md` and hashing it.
- `tests/integrity/run-test.sh` covering positive, tampered, and
  missing-baseline paths.
- `SECURITY.md` describing the supported versions, reporting channel,
  scope, and threat model.

### Changed
- `hooks/session-start` now verifies the integrity baseline before
  injecting `using-superpowers/SKILL.md` into the session context. On any
  failure (missing baseline, mismatched hash, no hash utility) the hook
  emits a `<security-alert>` block instead of injecting unverified skill
  content (fail-closed).
- Release procedure documented in [README.md](README.md#releasing): the
  baseline must be regenerated before bumping the version.

## [1.7.0] — 2026-05-17

Last release before the integrity baseline work. See git history for
prior changes.
