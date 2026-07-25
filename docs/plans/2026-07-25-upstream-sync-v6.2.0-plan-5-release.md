# Upstream Sync v6.2.0 — Phase 5: Release

> **For agentic workers:** REQUIRED SUB-SKILL: Use cf-powers:subagent-driven-development (recommended) or cf-powers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Regenerate the SHA-256 integrity baseline over the edited skills, record the sync, and ship cf-powers v3.0.0.

**Architecture:** Two tasks. Task 1 restores the integrity invariant — every `skills/*/SKILL.md` edit in Phases 1-4 invalidated the baseline, and the SessionStart hook fails closed until it is regenerated, so this is the change that makes the plugin loadable again. Task 2 is the paper trail: changelog, sync log, version bumps.

**Why a major version:** `review-package` gained a leading `PLAN_FILE` argument and `sdd-workspace` gained a required one. Anyone invoking those scripts directly breaks. Under semver that is a major bump: 2.0.0 → 3.0.0.

**Tech Stack:** Bash, JSON manifests, Markdown.

**Index:** [`plan-index.md`](./2026-07-25-upstream-sync-v6.2.0-plan-index.md)

## Global Constraints

- **Runs last.** Phases 1-4 must all be committed before this phase starts. Any `SKILL.md` edit landing after Task 1 invalidates the baseline again.
- Version bumps land in **both** `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — they must never disagree.
- Changelog format follows Keep a Changelog; the project follows semver.
- Record what was **deliberately skipped**, not only what was adopted. The sync log's value is in the decisions it preserves.
- The subagent-behaviour suites were not exercised in Phase 4 — say so in the changelog rather than implying full coverage.
- One commit per task.

---

### Task 1: Regenerate the integrity baseline

`hooks/session-start` verifies every `skills/*/SKILL.md` against `.claude-plugin/integrity.sha256` and fails closed on mismatch — it refuses to inject the bootstrap and prints an alert instead. Phases 1-4 edited 11 skill files, so the plugin currently fails closed on every session start. This task is what makes it load again.

**Files:**
- Modify: `.claude-plugin/integrity.sha256` (regenerated, 18 lines)

**Interfaces:**
- Consumes: every `SKILL.md` edit from Phases 1-4.
- Produces: a baseline matching the working tree, which `tests/integrity/run-test.sh` asserts.

- [ ] **Step 1: Confirm the baseline is currently stale**

Run: `tests/integrity/run-test.sh`

Expected: FAIL on the positive scenario — the pristine-repo case cannot inject `SKILL.md` because the recorded hashes no longer match. This is the state Phases 1-4 deliberately left behind; if this test **passes** here, no skill was edited and something went wrong earlier.

- [ ] **Step 2: Verify every skill edit was intentional before blessing it**

Run: `git diff --stat main -- skills/`

Expected: exactly the files the four phases claimed —
`skills/test-driven-development/SKILL.md`, `writing-good-tests.md` (new), `testing-anti-patterns.md` (deleted),
`skills/finishing-a-development-branch/SKILL.md`,
`skills/dispatching-parallel-agents/SKILL.md`, `skills/verification-before-completion/SKILL.md`,
`skills/receiving-code-review/SKILL.md`, `skills/writing-skills/SKILL.md`, `skills/writing-plans/SKILL.md`,
`skills/systematic-debugging/SKILL.md` + `find-polluter.sh`,
`skills/requesting-code-review/SKILL.md`, `skills/executing-plans/SKILL.md`,
`skills/using-superpowers/SKILL.md`,
`skills/subagent-driven-development/` (SKILL.md, 3 prompts, 3 scripts).

Anything else in that list is an unintended edit — investigate before regenerating. The baseline is a security control; regenerating it blesses whatever is on disk, so this check is the control's real gate.

- [ ] **Step 3: Regenerate**

Run: `bin/update-integrity`

Expected: the script reports the baseline written, covering 18 skills (the count is unchanged — this sync added and removed no skills).

- [ ] **Step 4: Verify the invariant is restored**

Run: `tests/integrity/run-test.sh`

Expected: PASS — all three scenarios: pristine (injects `SKILL.md`), tampered (fail-closed alert, no skill content), missing baseline (fail-closed alert).

Run: `hooks/session-start | head -5`

Expected: the JSON payload with `additionalContext` containing `You have superpowers.` — the bootstrap loads again.

- [ ] **Step 5: Run every offline suite**

Run: `tests/sdd-scripts/run-test.sh && tests/systematic-debugging/run-test.sh && tests/integrity/run-test.sh`

Expected: `ALL PASS`, `All tests passed`, and the three integrity scenarios green — in that order, all three exiting 0.

- [ ] **Step 6: Commit**

```bash
git add .claude-plugin/integrity.sha256
git commit -m "chore(security): regenerate integrity baseline for the v6.2.0 sync"
```

---

### Task 2: Changelog, sync log, version bump

**Files:**
- Modify: `CHANGELOG.md` (new `[3.0.0]` section under `[Unreleased]`)
- Modify: `docs/upstream-sync.md` (new sync-history entry, updated reference point)
- Modify: `.claude-plugin/plugin.json:4` (version)
- Modify: `.claude-plugin/marketplace.json:12` (version)

**Interfaces:**
- Consumes: the completed work of Phases 1-4 and Task 1.
- Produces: the released v3.0.0.

- [ ] **Step 1: Write the changelog entry**

Add a `## [3.0.0] — 2026-07-25` section under `## [Unreleased]` in `CHANGELOG.md`, following the existing v2.0.0 entry's shape: a lead paragraph naming the upstream range, then `### Added` / `### Changed` / `### Fixed` / `### Removed` subsections.

The lead paragraph must state: selective sync from `obra/superpowers` v6.0.3 → v6.2.0; **no new skills or agents appeared upstream** (the `SKILL.md` set is byte-identical between those tags); only Claude-Code-relevant changes adopted; the Codex/Gemini/Pi/Antigravity/Cursor work and the vendor-neutral vocabulary rewrite deliberately skipped; pointer to `docs/upstream-sync.md`.

Content to cover, by subsection:

- **Added** — `writing-good-tests.md` (replacing `testing-anti-patterns.md`), `re-review-prompt.md`, `tests/systematic-debugging/run-test.sh`, the SDD five-round breaker and adjudication rules, rationalization tables in `finishing-a-development-branch` and `requesting-code-review`.
- **Changed** — the SDD plan-scoped workspace and resume-based fix loop (**breaking**: `review-package` takes `PLAN_FILE` first, `sdd-workspace` requires it); `finishing-a-development-branch` no longer offers to discard work; the `using-superpowers` bootstrap compressed (state the actual before/after line count measured in Phase 3 Task 3 Step 6); the compression sweep across 8 skills; `hooks/hooks.json` declares `shell: "bash"`.
- **Fixed** — `find-polluter.sh` matching (upstream #2008/#2011, with the "Found 1 test files" symptom named); the Windows SessionStart hook (#1751/#1918).
- **Removed** — `skills/test-driven-development/testing-anti-patterns.md`; the recap/social-proof sections; `Integration` listings from `requesting-code-review`, `executing-plans`, `finishing-a-development-branch`, and `subagent-driven-development`.

State plainly that the subagent-behaviour suites (`tests/subagent-driven-dev/`, `tests/claude-code/`, `tests/skill-triggering/`, `tests/explicit-skill-requests/`) were **not run** — they invoke real Claude sessions — and that the offline suites (sdd-scripts, systematic-debugging, integrity) are green.

- [ ] **Step 2: Record the sync decisions**

Add a `### 2026-07-25 — v6.0.3 → v6.2.0 (released as cf-powers v3.0.0)` entry to the `## Sync history` section of `docs/upstream-sync.md`, above the existing 2026-06-29 entry. Follow that entry's shape: a framing paragraph, an **Adopted:** list, and a **Deliberately skipped:** list.

The framing paragraph must record that upstream shipped v6.1.0, v6.1.1 and v6.2.0 in this range (70 commits) and that **no new skills or agents were added** — the `SKILL.md` set is byte-identical between v6.0.3 and v6.2.0, and upstream still has no `agents/` or `commands/` directories.

**Adopted** — each with its one-line rationale: the two bug fixes; `writing-good-tests.md`; the discard-menu removal; the compression sweep (noting the TDD rebuttals were *folded into rationalization rows, not deleted*, because upstream measured deletion degrading behaviour 8/10 → 5/10); the bootstrap compression; the SDD restructure.

**Fork-specific adaptations** worth recording separately, because they are where we diverged from the upstream text on purpose:
- `.cf-powers/sdd/<plan>/` instead of `.superpowers/sdd/<plan>/`.
- The SDD Setup section states our branch policy (the human manages branches, no automatic worktrees) where upstream requires `using-git-worktrees`.
- The fix loop names Claude Code's `SendMessage` for resuming a live implementer, where upstream hedges with "if your harness cannot send another message to a live subagent".
- `finishing-a-development-branch` keeps `gh pr create`; upstream went forge-agnostic. We are a GitHub shop and the concrete command is more useful than a description of one.
- `using-superpowers` keeps our Skip Flags table, which upstream has no equivalent for.

**Deliberately skipped** — the vendor-neutral vocabulary rewrite; all Codex work (marketplace manifest, `package-codex-plugin.sh`, portal packaging, hook removal); the Gemini CLI removal-and-restoration; Pi/Antigravity/Cursor references and tests; upstream's `docs/superpowers/specs/` and `docs/superpowers/plans/` eval records; the `brainstorming` and `using-git-worktrees` changes (we ship neither).

Finally, update the `## Reference points` section: the last fully-tracked upstream version is now **v6.2.0**, synced in cf-powers v3.0.0.

- [ ] **Step 3: Bump the version in both manifests**

In `.claude-plugin/plugin.json`, change `"version": "2.0.0"` to `"version": "3.0.0"`.

In `.claude-plugin/marketplace.json`, change the `"version": "2.0.0"` inside the `plugins[0]` entry to `"version": "3.0.0"`.

- [ ] **Step 4: Verify the manifests agree and stay valid JSON**

```bash
python3 -c "
import json
p = json.load(open('.claude-plugin/plugin.json'))['version']
m = json.load(open('.claude-plugin/marketplace.json'))['plugins'][0]['version']
assert p == m == '3.0.0', f'version mismatch: plugin={p} marketplace={m}'
print('both manifests at', p)
"
```

Expected: `both manifests at 3.0.0`. A non-zero exit means the two files disagree — the failure mode this check exists to catch.

- [ ] **Step 5: Mark the index complete**

In `docs/plans/2026-07-25-upstream-sync-v6.2.0-plan-index.md`, set every row's Status to `✅ Complete`.

- [ ] **Step 6: Final verification before claiming done**

Run: `tests/sdd-scripts/run-test.sh && tests/systematic-debugging/run-test.sh && tests/integrity/run-test.sh`

Expected: all three green, exit 0.

Run: `grep -rn "superpowers:" skills/ | grep -v "cf-powers:" | grep -v "using-superpowers"`

Expected: no output (exit 1) — no unadapted upstream skill references anywhere.

Run: `git status --porcelain`

Expected: no output — everything committed.

- [ ] **Step 7: Commit**

```bash
git add CHANGELOG.md docs/upstream-sync.md .claude-plugin/plugin.json \
        .claude-plugin/marketplace.json docs/plans/2026-07-25-upstream-sync-v6.2.0-plan-index.md
git commit -m "v3.0.0: selective upstream sync (obra/superpowers v6.0.3 → v6.2.0)"
```
