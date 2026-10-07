---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

**Runtime:** Follow project instructions. Use native skill loading and ordinary
project reads directly. Before dispatch, resume, model selection, or shared plugin
resource resolution, read [runtime operations](../using-superpowers/references/runtime.md)
and the active-host reference once per context. Keep workflow decisions and child runtime constraints unchanged.

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

Invoke `documenting-changes` and keep its five-layer inventory and UPDATE/CREATE/SKIP decisions.
Apply required updates within existing authorization. Update the persistent guide
in `docs/` or the project's established system, and link any new document.
Report changed paths, verification, and justified skips. Preserve an explicit
user deferral as an open documentation gap; do not ask again for routine updates.

Continue once required updates are verified or an explicit deferral is recorded.
If an update is blocked, report the gap instead of claiming documentation is complete.

### Step 2: Determine Base Branch

Inspect the branch/worktree state with the runtime reference first. On a
host-provided detached HEAD, preserve the workspace and commits. Only present
merge/push options once an existing or explicitly authorized branch makes them
valid. If the host prevents that, hand off the exact commit/diff and workspace
state for native integration; never fabricate a branch or delete a worktree.


The base branch is whatever this work forked from — usually named in the plan, the conversation, or the branch's upstream. If it is not already known, ask: "This branch split from <your best guess> - is that correct?" Confirm before merging: merging into the wrong base is expensive to undo.

### Step 3: Present Options

If an integration choice and target are already authorized, execute that choice
after verification and the project's branch-policy checks. Otherwise present these three options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)

Which option?
```

When no choice is already authorized, present this menu concisely and wait for
the answer. The integration decision is the user's. Discard work only on an explicit
request, following the separate confirmation step below.

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
| "They obviously want it merged" | Integration is your human partner's decision. Without an authorized choice, present the menu and wait. |
| "They seem done with this feature — I'll offer to discard it" | The menu is complete as written. Discard happens only when your human partner asks for it in so many words. |
| "'Yeah, get rid of it' counts as confirmation" | Only the typed word `discard` authorizes deletion. |
| "Docs can follow in a separate pass" | Step 1.5 is the gate. A deferred doc gap needs a recorded owner and a local record or handoff note. Create an external issue only when authorized. |
| "The merged-result failure is probably flaky" | A failing merged result stops everything. The branch stays put while you investigate. |
| "The base branch is obviously main" | Confirm the fork point or ask. Merging into the wrong base is expensive to undo. |
| "The push was rejected — force-push will fix it" | A rejected push means the remote moved. Investigate; force-push only on your human partner's explicit request. |

