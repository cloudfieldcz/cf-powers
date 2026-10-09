---
name: executing-plans
description: Use when executing an implementation plan in the current session as the implementer yourself - the user chose inline execution, or no subagent tool is available
---

# Executing Plans

**Runtime:** Follow project instructions. Use native skill loading and ordinary
project reads directly. Before dispatch, resume, model selection, or shared plugin
resource resolution, read [runtime operations](../using-superpowers/references/runtime.md)
and the active-host reference once per context. Keep workflow decisions and child runtime constraints unchanged.

You implement every task of the plan yourself, in this session. There is no
implementer subagent and no reviewer per task. One fresh reviewer checks the
whole branch at the end.

**Announce at start:** "I'm using the executing-plans skill to implement this plan inline."

**Why inline:** cf-powers:subagent-driven-development pays for a fresh
implementer and a fresh reviewer on every task. Inline execution pays for one
context (yours) and one final reviewer. It gives up the fresh context and the
second reader per task. This skill replaces them: the brief is the
requirement, the ledger is your memory, the task's `Verify:` line is the
per-task gate, and the final reviewer is the second reader.

**Narration:** between tool calls, narrate at most one short line. The ledger
and the tool results carry the record.

**Continuous execution:** Do not pause to check in with the user between
tasks. Execute all tasks without stopping. The only reasons to stop are the
four stops below, or all tasks complete.

**Rulings, not stalls.** Decide conflicts, ambiguities and plan defects
yourself. The analysis document is the binding authority, the plan is its
argument, and your judgement settles what neither answers. Record every
decision in the ledger as `Ruling: <what you decided> — <why> — <what it costs
if wrong>`, and continue. A deviation from the plan without a ledgered ruling
is a decision made in secret.

Four things stop you, and only these: an irreversible or destructive
operation; a security-sensitive action; a side effect outside this repository
that norms say you ask about first (a merge, a push to a shared branch, a
publish); and a plan so broken that every path forward is a guess. For those,
stop and ask.

## When to Use

- The user chose inline execution at the cf-powers:writing-plans handoff.
- The host has no subagent tool. Never fabricate a dispatch. Run the plan here.
- The tasks are mostly independent, as for cf-powers:subagent-driven-development.

A plan with exact interfaces and decisions makes inline execution transcription
plus testing. A mid-tier session model can do it. The judgment tier is necessary
only for the final review, which this skill dispatches separately.

Prefer cf-powers:subagent-driven-development when the user wants a review gate
on every task, or when the plan is so long that its last tasks will run on a
compacted context. The ledger makes a long inline run recoverable, but the last
tasks get the least of your context.

**For a multi-phase plan index (several phase plans under one index), use
cf-powers:orchestrator.** It delegates each phase and keeps one session's
context sufficient for the whole index. This skill executes one plan file.

## Step 0: Branch Check

1. Run `git branch --show-current`.
2. On `main` or `master`: **STOP**. Ask the user to create or switch to a
   feature branch, unless they already explicitly authorized work there.
3. On a feature branch: continue.
4. In a host-provided detached worktree: follow the runtime reference. Keep that
   workspace and its integration handoff. Do not create or switch a branch only
   to satisfy this check.

The user manages their own branches. Do not create worktrees.

## Setup

Conversation memory does not survive compaction. An inline executor that
loses its place implements again tasks whose commits already exist. Track
progress in the ledger, not only in todos. The workspace and the ledger are
the same as in cf-powers:subagent-driven-development, so the user can change
executors in the middle of a plan and the new executor resumes from the ledger.

Script paths in this skill are relative to this skill's directory. Always
run a bundled script through `bash`: packagers can remove the execute bit.

- Run `bash ../subagent-driven-development/scripts/sdd-workspace PLAN_FILE`.
  It prints the plan's git-ignored workspace
  (`<repo-root>/.cf-powers/sdd/<plan-basename>/`). On a name collision it is a
  sibling named `<basename>-<parent>[-N]`. Use the printed path. Another plan's
  directory is never yours to read or write.
- Read `<workspace>/progress.md` if it exists. If its first line names your
  plan file, a task with a `Task <N>: complete` line is DONE: do not do it
  again. Resume at the first task without that line. A task whose last ledger
  line is a fix round already has commits. Resume from `git log`. Do not redo it. After compaction, trust
  the ledger and `git log` over your recollection. A ledger that names a
  different plan file belongs to another plan: leave it and start a new one.
- A new ledger starts with the line `# SDD ledger — plan: <plan file path>`.
  `task-done` writes it from the path recorded in `<workspace>/plan-path`, so
  every spelling of one plan gives the same line.
- `git clean -fdx` deletes the workspace. If that happens, recover from `git log`.

Read the plan once. Note its Global Constraints and Review Focus, and create a
todo per task. Read the **Analysis** that the plan header names. Conflicts in
the plan resolve against it. If the analysis is unreachable, write a ledger
note: rulings without it are provisional.

**REQUIRED SUB-SKILL:** load cf-powers:test-driven-development before Task 1.
It governs every task.

Before Task 1, scan the Interfaces blocks. For every task that consumes what an
earlier task produces, write one ledger row: the two tasks, the produced name
against the consumed name, and what you found. If no task shares anything,
write `Pre-flight: no shared interfaces`. Rule on each conflict and record the
ruling beside its row.

## The Task Loop

Every tool result stays in your context for the rest of the session. Send long
test output to a file in the workspace and read its tail. Read a brief, not the
whole plan. Chain the final commit and `task-done` in one tool call, never in
separate calls.

1. **Take the task.** Run `bash scripts/task-start PLAN_FILE N`. It prints the brief path and BASE. Read the brief, also
   for a task you remember: the brief has the exact values. Mark the todo
   in_progress.
2. **Build it with TDD.** The plan gives Delivers, Files, Interfaces,
   Decisions, Trap and Verify. It does not list steps. Run the red-green-commit
   loop yourself. Watch each test fail before you write the code. A test that
   passes before the code exists is a finding about the test. Where the plan
   leaves a choice open, make a reasonable one. When the code is wrong, use
   cf-powers:systematic-debugging. When the plan is wrong (it contradicts the
   analysis, or an interface does not match the earlier task), make the
   smallest change that satisfies the analysis. Record it as
   `Task <N>: Ruling: <finding> — <decision and why> — <cost if wrong>`.
   Later tasks that touch the same interface read the ruling from the ledger.
3. **Meet the `Verify:` line.** The task is complete only when all of these
   are true, with evidence from this session:
   - The command in `Verify:` passed. Step 4 runs it through `task-done`, so
     that run is the evidence. Do not run it twice.
   - You checked each by-hand behavior that `Verify:` names.
   - If the task changes a rendered surface, you opened the affected screen in
     the running app and looked at a screenshot. A test does not replace this.
   - Every deviation from the brief has a `Ruling:` line in the ledger.

   **REQUIRED SUB-SKILL:** cf-powers:verification-before-completion governs the claim.
4. **Commit and record it.** Run
   `git commit … && bash scripts/task-done PLAN_FILE N BASE -- <Verify command>`
   in one call. Pass a `Verify:` command that contains `&&` or pipes as
   `bash -c '…'`. `task-done` runs the command, keeps the full output in the
   workspace and prints the tail. Only on success does it append
   `Task <N>: complete (commits <base7>..<head7>, tests: <command> → <result>)`.
   A failed run records nothing. If BASE..HEAD is empty or BASE is not an
   ancestor of HEAD, it exits 3 and records nothing. Then mark the todo
   complete. A task can have several commits. BASE is the start of its range,
   never `HEAD~1`.

## Final Review

Run `bash ../subagent-driven-development/scripts/review-package PLAN_FILE MERGE_BASE HEAD`
(MERGE_BASE is the commit the branch started from, for example
`git merge-base main HEAD`).

**With a subagent tool:** dispatch one reviewer on the judgment tier
(cf-powers:choosing-subagent-models) with cf-powers:requesting-code-review's
[code-reviewer.md](../requesting-code-review/code-reviewer.md). Give it the
package path, the plan and analysis paths, the plan's Review Focus lines
verbatim, and a pointer to the ledger's `Ruling:` lines. Name the model
explicitly. Do not skip this review, and do not replace it with your own read
of the diff.

**Without a subagent tool:** read code-reviewer.md and do that review yourself
against the package, as a separate pass after the last task. Write
`Final review: self-review (independent review unavailable)` to the ledger.
Say in your final message that independent review is unavailable, not passed,
and keep the package for a later independent review.

Re-grade each finding by its effect on a person who uses the software, not by
the label. Then:

- **Critical and Important:** fix them yourself in ONE pass. For each fix,
  write a test that reproduces the finding, watch it fail, make it pass, then
  run the whole suite. Record
  `Final: fixed <finding> — <test> RED→GREEN, suite <N>/<N>`. There is no
  re-review and no second pass.
- **A finding you decide not to fix** is a ruling:
  `Final: Ruling: <finding> — <why the code stands> — <cost if wrong>`.
- **Minor:** do not fix. Record `Final: minor (deferred): <one-liner>`.

## Finish

Before you delete anything, copy into your final message every ledger line
that contains `Ruling:` under "Rulings I made", in order, each with its cost if
wrong. Copy every `minor (deferred)` line under "Deferred minors". Both lists
are exhaustive.

When the fixes are committed, delete this plan's workspace
(`rm -rf <workspace>`). The git history is the record now. Leave sibling
directories alone.

Use cf-powers:finishing-a-development-branch.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I remember what Task N says" | You remember a summary. The brief has the exact values. Read it. |
| "The test will fail, skip watching it" | A test you never saw fail proves nothing. |
| "The test passes, skip the screenshot" | A test does not see a rendered screen. The `Verify:` line says look. |
| "The plan is wrong here, I will just do the right thing" | Do it and ledger the ruling. |
| "I will write the ledger lines later" | Compaction does not wait. One line per task. Chain `task-done` after the commit. |
| "Let me check in before the next task" | Only the four stops stop you. |
| "I read my own diff, the final reviewer is redundant" | Same author, same blind spots. It is the only fresh context this run buys. |
| "I will fix the minors too" | Ledger them. The user decides. |
