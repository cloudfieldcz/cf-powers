# Upstream Sync v6.2.0 — Phase 2: Test Guidance + Discard Menu

> **For agentic workers:** REQUIRED SUB-SKILL: Use cf-powers:subagent-driven-development (recommended) or cf-powers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the TDD reference doc `testing-anti-patterns.md` with upstream's rebuilt `writing-good-tests.md`, and stop `finishing-a-development-branch` from advertising "Discard this work" next to "Merge" on a finished, green branch.

**Architecture:** Task 1 is a clean file swap — our `testing-anti-patterns.md` is byte-identical to upstream v6.0.3 and our TDD `SKILL.md` diverges by 2 lines, so the port carries no merge risk. Task 2 is a manual edit rather than a port: our `finishing-a-development-branch` diverged from upstream long ago (we dropped the whole worktree machinery and added a docs gate), so we adopt the *decision* and the rationalization table, not the diff.

**Tech Stack:** Markdown skill documents.

**Index:** [`plan-index.md`](./2026-07-25-upstream-sync-v6.2.0-plan-index.md)

## Global Constraints

- Upstream source of truth: `obra/superpowers` at tag **v6.2.0** (commit `3dcbd5c`), referred to as `$UPSTREAM`.
- **Fork adaptation rules** — apply to every ported line: `superpowers:` → `cf-powers:`; `.superpowers/sdd/` → `.cf-powers/sdd/`; `docs/superpowers/plans/` → `docs/plans/`; `~/.config/superpowers/` → `~/.config/cf-powers/`; `brainstorming` → `analysis`; drop every reference to `using-git-worktrees` (we do not ship it).
- **Do not adopt upstream's vendor-neutral vocabulary.** Keep the Claude Code dialect ("Task tool", "CLAUDE.md").
- Never reference a skill we do not ship: `brainstorming`, `using-git-worktrees`, `testing-anti-patterns` (after Task 1).
- **No `@`-prefixed file links in skill bodies** — `@` force-loads the file and burns context on every load. Use plain markdown links.
- `tests/integrity/run-test.sh` fails from the first `SKILL.md` edit until Phase 5 regenerates the baseline. Expected. All other suites stay green.
- One commit per task.

---

### Task 1: `testing-anti-patterns.md` → `writing-good-tests.md`

Upstream rebuilt the TDD reference doc as a positive catalog and absorbed a falsifiability discipline. Two additions matter most for this repo, which tests its own skills: the **string-presence trap** (grep-style assertions on scripts, skills, and prompts counterfeit falsifiability — the observable is behavior, never text) and the **change-detector trap** (a constant assertion can fail on every intentional edit and still protect nothing).

The trigger also broadens: the old doc fired on "adding mocks or test utilities", the new one on any test writing.

**Files:**
- Create: `skills/test-driven-development/writing-good-tests.md`
- Delete: `skills/test-driven-development/testing-anti-patterns.md`
- Modify: `skills/test-driven-development/SKILL.md:206-254` (replace "Why Order Matters" with the reference pointer), `:256-270` (fold the rebuttals into rationalization rows), `:357-362` (retarget the reference section)

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `skills/test-driven-development/writing-good-tests.md` — the path Task 3 of Phase 3 must not re-reference under its old name.

- [ ] **Step 1: Port the new reference doc**

Copy the upstream file verbatim, then apply the one mechanical rename it needs:

```bash
cp "$UPSTREAM/skills/test-driven-development/writing-good-tests.md" \
   skills/test-driven-development/writing-good-tests.md
sed -i '' 's/superpowers:writing-skills/cf-powers:writing-skills/g' \
   skills/test-driven-development/writing-good-tests.md
```

- [ ] **Step 2: Verify the port is clean**

Run: `diff "$UPSTREAM/skills/test-driven-development/writing-good-tests.md" skills/test-driven-development/writing-good-tests.md`

Expected: exactly one hunk — the `superpowers:writing-skills` → `cf-powers:writing-skills` line. Nothing else.

Run: `grep -n "superpowers:\|using-git-worktrees\|@testing-anti-patterns" skills/test-driven-development/writing-good-tests.md`

Expected: no output (exit 1). No unadapted references survive.

- [ ] **Step 3: Remove the old reference doc**

```bash
git rm skills/test-driven-development/testing-anti-patterns.md
```

- [ ] **Step 4: Replace "Why Order Matters" with the reference pointer**

In `skills/test-driven-development/SKILL.md`, delete the whole `## Why Order Matters` section (lines 206-254, from the heading through `30 minutes of tests after ≠ TDD. You get coverage, lose proof tests work.`) and put this in its place:

```markdown
When writing or changing any test, read [writing-good-tests.md](writing-good-tests.md) for the rules that keep tests honest:
- Name the production change that would make the test fail — before writing it
- Assert on real behavior, never on mock behavior
- Keep test-only code in test utilities, out of production classes
- Understand a dependency's side effects before mocking it
```

**Do not simply delete the section.** Upstream measured that deleting these rebuttals outright degraded test-first behavior under "just write it, tests after" pressure (control 8/10 → treatment 5/10, corroborated on Claude and Codex). The arguments must survive as rationalization rows — that is Step 5, and it is not optional.

- [ ] **Step 5: Fold the rebuttals into the rationalization table**

In the same file, replace these five rows of the `## Common Rationalizations` table:

```markdown
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
```

and

```markdown
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
```

with the expanded forms that carry the deleted prose:

```markdown
| "I'll test after" | Tests written after pass immediately — which proves nothing. They may test the wrong thing, test the implementation instead of the behavior, or miss the edge case you forgot. You never watched it fail, so you never proved it can catch the bug. Test-first forces that failure. |
| "Tests after achieve same goals (spirit not ritual)" | Tests-after answer "what does this do?"; tests-first answer "what should this do?" Tests written after are biased by the code you already wrote — you verify the cases you remembered, not the ones you'd have discovered. Coverage without proof the tests work. |
| "Already manually tested" | Manual testing is ad-hoc: no record of what you covered, no way to re-run it when the code changes, easy to forget cases under pressure. "Worked when I tried it" ≠ comprehensive. Automated tests run the same way every time. |
| "Deleting X hours is wasteful" | Sunk cost fallacy — that time is already spent either way. The real choice: rewrite with TDD (high confidence) vs. keep it and bolt tests on after (low confidence, likely bugs). Keeping code you can't trust is the waste. |
```

```markdown
| "TDD will slow me down" | TDD IS the pragmatic path: catches bugs before commit, prevents regressions, lets you refactor without fear. "Pragmatic" shortcuts mean debugging in production — slower, not faster. |
```

- [ ] **Step 6: Retarget the reference section**

Delete the `## Testing Anti-Patterns` section (lines 357-362 — heading, the `@testing-anti-patterns.md` pointer, and its three bullets). The pointer added in Step 4 replaces it, and it sits earlier in the file where an agent hits it before writing tests rather than after.

- [ ] **Step 7: Verify no dangling references**

Run: `grep -rn "testing-anti-patterns" skills/ hooks/ tests/ README.md`

Expected: no output (exit 1). Historical mentions inside `docs/plans/2025-11-28-*.md` are a record of past work and stay as they are.

Run: `grep -n "@testing-anti-patterns\|@writing-good-tests" skills/test-driven-development/SKILL.md`

Expected: no output — the new pointer is a plain markdown link.

- [ ] **Step 8: Commit**

```bash
git add skills/test-driven-development/
git commit -m "refactor(tdd): replace testing-anti-patterns with writing-good-tests"
```

---

### Task 2: `finishing-a-development-branch` stops offering to discard

The completion menu dates from when throwing away branches was routine. Putting "Discard this work" next to "Merge" advertises destroying finished, passing work — the skill runs precisely when the work is green. Discard survives as an explicit-request-only path with the same typed-confirmation ritual.

Our copy of this skill diverged from upstream long ago: we dropped the worktree detection and cleanup machinery entirely, added Step 1.5 (`documenting-changes`), and use `gh pr create`. So this task adopts upstream's decision and rationalization table, adapted to our structure — not upstream's diff. Rows about worktree provenance do not apply to us and are omitted; our docs-gate row is added.

**Files:**
- Modify: `skills/finishing-a-development-branch/SKILL.md:53-60` (base branch), `:62-77` (menu), `:81-98` (Option 1), `:117-137` (Option 3 + discard), `:140-147` (quick reference), `:149-185` (replace Common Mistakes + Red Flags + Integration with a rationalization table)

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: nothing later tasks rely on.

- [ ] **Step 1: Firm up the base-branch step**

Replace the body of `### Step 2: Determine Base Branch` (the `git merge-base` code block and the "Or ask:" line) with:

```markdown
The base branch is whatever this work forked from — usually named in the plan, the conversation, or the branch's upstream. If it is not already known, ask: "This branch split from <your best guess> - is that correct?" Confirm before merging: merging into the wrong base is expensive to undo.
```

- [ ] **Step 2: Cut the menu to three options**

In `### Step 3: Present Options`, change `Present exactly these 4 options:` to `Present exactly these 3 options:`, delete the `4. Discard this work` line from the code block, and replace the `**Don't add explanation** - keep options concise.` line with:

```markdown
Present the menu exactly as written — concise, with every option coming from the list above. Discarding the work happens only in response to your human partner explicitly asking for it (see "If your human partner asks to discard the work" below). Wait for their answer; the integration decision is theirs.
```

- [ ] **Step 3: Handle a failing merged result**

In `#### Option 1: Merge Locally`, replace the trailing comment pair:

```bash
# If tests pass
git branch -d <feature-branch>
```

so that the bash block ends after the `<test command>` line. Then, below the closing fence, add this prose and a fresh bash block:

- Prose: `If tests fail on the merged result: stop, leave the branch in place, and investigate — nothing has been pushed, so the merge is local and recoverable.`
- Prose: `Once the merged result is green, delete the branch:`
- A bash block containing exactly: `git branch -d <feature-branch>`

- [ ] **Step 4: Convert Option 4 into an explicit-request path**

Replace the heading `#### Option 4: Discard` with:

```markdown
#### If your human partner asks to discard the work

This path exists only as a response to an explicit request to throw the work away. Confirm first:
```

and delete the now-duplicated `**Confirm first:**` line that followed it. Keep the typed-`discard` confirmation block and the `git checkout` / `git branch -D` commands exactly as they are.

- [ ] **Step 5: Relabel the quick-reference row**

In the `## Quick Reference` table, replace:

```markdown
| 4. Discard | - | - | ✓ (force) |
```

with:

```markdown
| Discard (explicit request only) | - | - | ✓ (force) |
```

- [ ] **Step 6: Replace the tail sections with a rationalization table**

Delete `## Common Mistakes`, `## Red Flags`, and `## Integration` (lines 149-185 — everything after the Quick Reference table) and put this in their place:

```markdown
## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Tests passed earlier this session" | Run the suite on the tree you are about to integrate. A green run only proves the tree it ran on. |
| "They obviously want it merged" | Integration is your human partner's decision. Present the menu and wait. |
| "They seem done with this feature — I'll offer to discard it" | The menu is complete as written. Discard happens only when your human partner asks for it in so many words. |
| "'Yeah, get rid of it' counts as confirmation" | Only the typed word `discard` authorizes deletion. |
| "Docs can follow in a separate pass" | Step 1.5 is the gate. A deferred doc gap needs a recorded owner — an issue, a `TODO(docs)`, or a line in the PR body — not a good intention. |
| "The merged-result failure is probably flaky" | A failing merged result stops everything. The branch stays put while you investigate. |
| "The base branch is obviously main" | Confirm the fork point or ask. Merging into the wrong base is expensive to undo. |
| "The push was rejected — force-push will fix it" | A rejected push means the remote moved. Investigate; force-push only on your human partner's explicit request. |
```

The `## Integration` section's content ("Called by: subagent-driven-development (Step 7), executing-plans (Step 5)") is dropped rather than relocated: both callers already name this skill at their own point of use, so the list only duplicated information the reader arrives with.

- [ ] **Step 7: Verify the menu is consistent throughout**

Run: `grep -n "4 options\|4. Discard\|Option 4" skills/finishing-a-development-branch/SKILL.md`

Expected: no output (exit 1). No stale four-option references survive anywhere in the file.

Run: `grep -c "^| " skills/finishing-a-development-branch/SKILL.md`

Expected: `13` — 4 Quick Reference rows (header, separator, and 3 options are counted separately: 1 header + 1 separator + 3 rows = 5) plus the rationalization table's 1 header + 1 separator + 8 rows. Confirm by eye that both tables are well-formed rather than trusting the count alone.

- [ ] **Step 8: Commit**

```bash
git add skills/finishing-a-development-branch/SKILL.md
git commit -m "refactor(finishing): stop offering to discard work, adopt rationalization table"
```
