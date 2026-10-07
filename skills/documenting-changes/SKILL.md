---
name: documenting-changes
description: Use when implementation of a feature, fix, or refactor is finished, before claiming work complete or starting merge/PR — any change that may affect docs/, README, CHANGELOG, or inline docstrings/JSDoc
---

# Documenting Changes

## Overview

Code without matching documentation rots into "what does this do?" within weeks. Catch drift the moment implementation finishes, while the change is still in your head.

**Core principle:** When code changes, the docs that describe it must change too — or you must say why not.

**Documentation is part of the authorized change.** Perform required updates
without a separate permission stop. Keep explicit user deferrals or exclusions
visible; do not silently mark missing documentation as complete.

**Announce at start:** "I'm using the documenting-changes skill to keep docs in sync."

## When to Use

**Always run before:**
- Claiming a feature/fix is "done"
- Step 1.5 of `finishing-a-development-branch`
- Creating a PR for a feature, refactor, or bugfix

**Skip only when:**
- Pure cosmetic changes (formatting, whitespace, comment typos)
- The user has explicitly said "no docs needed for this"

## The Process

### Step 1: Inventory the Change

```bash
git diff <base>...HEAD --stat
git diff <base>...HEAD -- '*.md'   # committed documentation
git diff --stat                 # unstaged changes
git diff --cached --stat        # staged changes
git ls-files --others --exclude-standard  # untracked files
```

Read the relevant staged/unstaged diffs and untracked files, not only their names.
Use the task's actual delivery scope. Preserve unrelated user changes; do not
attribute them to this task or stage them as part of documentation updates.

Answer:
- **Public surface changed?** — API, CLI flags, config keys, env vars, schemas, slash commands, hooks, plugin manifest
- **Workflow/behavior changed?** — install steps, defaults, error messages, ordering
- **New things appeared?** — new feature, module, command, skill, script

### Step 2: Map Each Change to Doc Locations

For each change identified, walk **all five layers**:

| Layer | What to check |
|-------|---------------|
| `docs/` | Architecture, guides, references, ADRs, plans |
| `README.md` | Overview, install, quick-start, feature list (root + subdirectory READMEs) |
| `CHANGELOG.md` / release notes | Entry under current/next version |
| Inline (JSDoc, TSDoc, docstrings, Go doc comments) | Signatures, parameter docs, examples at definition sites |
| Plugin/skill metadata | `.claude-plugin/*`, `skills/*/SKILL.md` description fields, version fields |

### Step 3: Decide per Change

Technical layers (`docs/` architecture, ADRs, references, and inline docs) follow
[Technical English](../using-superpowers/references/technical-english.md). README, user guides and user-facing CHANGELOG entries keep their own voice.

Prefer the existing source of truth in `docs/`. If the repository uses another
documentation system, follow that convention. Create a new document only when no
existing guide fits, and link it from the relevant index or README. A changelog
entry or final chat reply does not replace a required persistent guide.

Each change resolves to exactly one of:

1. **UPDATE** — touches user-visible surface or modifies existing documented behavior → write the update
2. **CREATE** — entirely new feature with no existing doc home → create new file (and link from index/README)
3. **SKIP** — internal-only change → must give a one-line justification naming the specific module and confirming no public surface changed

"Internal" alone is not a justification. "Refactored cache eviction in `src/internal/cache.ts`; no exported API, config, or behavior changed" is.

### Step 4: Apply and Report

```
Documentation review for this work:

UPDATED:
- docs/architecture.md — describe new event flow
- README.md — add "MyFeature" to feature list
- CHANGELOG.md — entry for v1.6.0

CREATED:
- docs/guides/myfeature.md — usage guide for new MyFeature

INLINE:
- src/api/handler.ts — JSDoc on handleRequest() reflects new param

SKIPPED (internal-only):
- src/internal/cache.ts refactor — no public surface or behavior change

Validation: [commands/results, or a named documentation gap]
```

Apply UPDATE and CREATE decisions within the authorized scope before reporting.
Verify affected examples and links, plus the relevant repository checks.
Ask only when a material documentation/product decision is unresolved or work
would exceed existing authorization.

- **Explicit user deferral** → record the gap locally or in the handoff. Creating
  an external issue still requires authorization. Do not claim the docs are complete.
- **SKIP** → retain the specific reason; confirm existing docs remain accurate.
- **Blocked update** → name the missing document or information and report that
  part as incomplete. A summary in chat is not a substitute.

## Quick Reference

| Change type | Likely doc actions |
|-------------|-------------------|
| New public API/CLI flag | UPDATE README + CHANGELOG + inline docstring; consider docs/ guide |
| New feature (user-facing) | CREATE docs/guides/<name>.md + UPDATE README feature list + CHANGELOG |
| Behavior change of existing feature | UPDATE relevant docs/ page + CHANGELOG; check README quick-start |
| Renamed/removed export | UPDATE inline docs at new site + CHANGELOG (breaking?) + grep `docs/` for old name |
| Bugfix (no behavior change beyond fix) | CHANGELOG entry; SKIP rest with justification |
| Internal refactor | SKIP all with one-line justification per affected module |
| New skill / plugin command | CREATE SKILL.md or command doc + UPDATE plugin manifest + CHANGELOG |

## Common Mistakes

**Skipping inline docs**
- **Problem:** Function signature changed but docstring still describes old params
- **Fix:** `grep` for the symbol you changed and check the doc comment at its definition

**"I'll update docs in a follow-up PR"**
- **Problem:** Follow-up PRs for docs rarely happen; drift compounds
- **Fix:** Update in same change. If truly impossible, file an issue with a deadline before merging.

**Updating only `docs/`**
- **Problem:** `README.md` and inline docs still show old usage; users hit them first
- **Fix:** Walk all five layers every time, even if most resolve to SKIP

**Vague justification for skip**
- **Problem:** "internal change" is a label, not a reason
- **Fix:** Name the file/module and the surface that did NOT change

**New feature with no doc home**
- **Problem:** Adding a feature but updating only CHANGELOG — no place a user can learn how to use it
- **Fix:** CREATE a `docs/guides/<name>.md` and link from README, even if short

## Red Flags

- About to claim "done" without having looked at `docs/`
- Edited a function but didn't open its docstring
- Added a new feature with no entry in README or `docs/`
- "The code is self-documenting" (often true at unit level, almost never true for user-facing features or workflows)
- Skipping with no justification, or justification that just repeats "internal"

## Integration

**Called by:**
- `finishing-a-development-branch` (Step 1.5) — between test verification and presenting merge/PR options
- `verification-before-completion` — completion claims include "docs reviewed"

**Independent invocation:** Any time after a non-trivial change, even mid-work, to keep drift from accumulating.
