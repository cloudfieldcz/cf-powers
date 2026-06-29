# Changelog

All notable changes to cf-powers will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
