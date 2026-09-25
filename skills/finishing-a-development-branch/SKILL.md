---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

**Runtime:** Before using host tools or dispatching, read [runtime operations](../using-superpowers/references/runtime.md) and its active-host reference (once per context). Keep this skill's workflow decisions unchanged.

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 1.5.

### Step 1.5: Verify Docs in Sync

**Soft gate** — keep documentation aligned with the implementation before merging.

Invoke the `documenting-changes` skill. It walks all five doc layers (`docs/`, `README.md`, `CHANGELOG.md`, inline docstrings/JSDoc, plugin/skill metadata), maps each change to UPDATE / CREATE / SKIP, and presents the result to the user.

The user chooses **now / defer / skip**:
- **Now** → apply doc updates, then re-run tests (Step 1) before continuing.
- **Defer** → record the gap (issue, `TODO(docs)`, or note in PR body) and continue.
- **Skip** → only valid when every affected change has a one-line justification confirming no public surface or behavior changed.

Continue to Step 2 once the user has decided.

### Step 2: Determine Base Branch

Inspect the branch/worktree state with the runtime reference first. On a
host-provided detached HEAD, preserve the workspace and commits. Only present
merge/push options once an existing or explicitly authorized branch makes them
valid. If the host prevents that, hand off the exact commit/diff and workspace
state for native integration; never fabricate a branch or delete a worktree.


The base branch is whatever this work forked from — usually named in the plan, the conversation, or the branch's upstream. If it is not already known, ask: "This branch split from <your best guess> - is that correct?" Confirm before merging: merging into the wrong base is expensive to undo.

### Step 3: Present Options

Present exactly these 3 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)

Which option?
```

Present the menu exactly as written — concise, with every option coming from the list above. Discarding the work happens only in response to your human partner explicitly asking for it (see "If your human partner asks to discard the work" below). Wait for their answer; the integration decision is theirs.

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>
```

If tests fail on the merged result: stop, leave the branch in place, and investigate — nothing has been pushed, so the merge is local and recoverable.

Once the merged result is green, delete the branch:

```bash
git branch -d <feature-branch>
```

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

The PR title and body follow [Technical English](../using-superpowers/references/technical-english.md).

#### Option 3: Keep As-Is

Report: "Keeping branch <name>."

#### If your human partner asks to discard the work

This path exists only as a response to an explicit request to throw the work away. Confirm first:

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```


## Quick Reference

| Option | Merge | Push | Cleanup Branch |
|--------|-------|------|----------------|
| 1. Merge locally | ✓ | - | ✓ |
| 2. Create PR | - | ✓ | - |
| 3. Keep as-is | - | - | - |
| Discard (explicit request only) | - | - | ✓ (force) |

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

