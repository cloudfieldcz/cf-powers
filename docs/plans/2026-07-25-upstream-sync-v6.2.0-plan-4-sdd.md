# Upstream Sync v6.2.0 — Phase 4: SDD Restructure

> **For agentic workers:** REQUIRED SUB-SKILL: Use cf-powers:subagent-driven-development (recommended) or cf-powers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adopt upstream v6.2.0's two structural SDD changes — a plan-scoped workspace, and a resume-based fix loop with a five-round circuit breaker and controller adjudication.

**Architecture:** Three tasks in dependency order. Task 1 changes the helper scripts' contract (test-first, since we have a fast offline suite for them). Task 2 ports the prompt templates that the new loop dispatches. Task 3 rewrites `SKILL.md` around the new lifecycle, and depends on both — it documents the script signatures from Task 1 and links the template from Task 2.

**Why this matters:** `.cf-powers/sdd/` had no plan identity and no end-of-life, so a follow-up plan in the same working tree could read the previous plan's ledger as its own progress. Upstream observed this in the wild. Their baseline evals found controllers *did* refuse foreign ledgers, but paid 6-13 tool calls of cross-plan git forensics per resume; plan-scoping makes the answer structural instead of a judgement call. The fix loop previously had no termination condition at all — a task could loop indefinitely on a finding the implementer could not see.

**Tech Stack:** Bash, git, Markdown prompt templates.

**Index:** [`plan-index.md`](./2026-07-25-upstream-sync-v6.2.0-plan-index.md)

## Global Constraints

- Upstream source of truth: `obra/superpowers` at tag **v6.2.0** (commit `3dcbd5c`), referred to as `$UPSTREAM`.
- **Fork adaptation rules** — apply to every ported line: `superpowers:` → `cf-powers:`; `.superpowers/sdd/` → `.cf-powers/sdd/`; `docs/superpowers/plans/` → `docs/plans/`; `~/.config/superpowers/` → `~/.config/cf-powers/`; `brainstorming` → `analysis`; drop every reference to `using-git-worktrees` (we do not ship it).
- **Do not adopt upstream's vendor-neutral vocabulary.** Keep the Claude Code dialect: `Task tool (general-purpose)` for dispatch, `TodoWrite` for todos, `SendMessage` for resuming a live subagent.
- **Workspace path is `.cf-powers/sdd/<plan-basename>/`** — never `.superpowers/`. `.gitignore` lives at `.cf-powers/sdd/.gitignore`, one level above the per-plan directories.
- **Every dispatch names its model explicitly.** An omitted model silently inherits the session's most expensive one. This rule predates this phase and must survive it.
- **Five rounds maximum per task**, then controller adjudication. Adjudicating earlier is pre-judging under another name.
- `tests/integrity/run-test.sh` fails from the first `SKILL.md` edit until Phase 5 regenerates the baseline. Expected. `tests/sdd-scripts/run-test.sh` must be green at the end of every task in this phase.
- The subagent-behaviour suites (`tests/subagent-driven-dev/`, `tests/claude-code/`, `tests/skill-triggering/`, `tests/explicit-skill-requests/`) invoke real Claude sessions and cost real money and minutes. They are **out of scope for this phase** — do not run them; note in the changelog that they were not exercised.
- One commit per task.

---

### Task 1: Plan-scope the helper scripts

`sdd-workspace` gains a required `PLAN_FILE` argument and resolves `<repo-root>/.cf-powers/sdd/<plan-basename>/`. `task-brief` passes its plan through. `review-package` gains `PLAN_FILE` as its **first** argument, shifting `BASE` and `HEAD` right by one — a breaking change to the script's contract.

**Files:**
- Modify: `tests/sdd-scripts/run-test.sh` (all three scenarios)
- Modify: `skills/subagent-driven-development/scripts/sdd-workspace`
- Modify: `skills/subagent-driven-development/scripts/task-brief:6-8`, `:24`
- Modify: `skills/subagent-driven-development/scripts/review-package:7-29`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `sdd-workspace PLAN_FILE` → prints `<repo-root>/.cf-powers/sdd/<plan-basename>`; `task-brief PLAN_FILE N [OUTFILE]` → unchanged signature, plan-scoped output; `review-package PLAN_FILE BASE HEAD [OUTFILE]` → prints `wrote <path>: <n> commit(s), <n> bytes`. Task 3 documents exactly these signatures.

- [ ] **Step 1: Write the failing tests**

In `tests/sdd-scripts/run-test.sh`, the plan fixture currently sits inside test2 but all three scenarios now need it. **Move** the existing `cat > plan.md <<'PLAN' … PLAN` heredoc and its two comment lines verbatim — do not retype it, it contains fenced-decoy lines whose exact bytes are the point of the fence-guard assertion — from test2 up to immediately after the `git config commit.gpgsign false` line, and retitle the comment:

```
# Shared plan fixture. Task 1's body contains a fenced "### Task 2" decoy; the
# fence guard must not treat it as a real boundary, so Task 1 extraction runs
# past it.
```

Then replace the whole `# --- test1: sdd-workspace` block with the plan-scoped version:

```bash
# --- test1: sdd-workspace is plan-scoped -----------------------------------
out="$("${SCRIPTS}/sdd-workspace" plan.md)"
[ "${out}" = "${WORK}/.cf-powers/sdd/plan" ] || fail "sdd-workspace path: got '${out}'"
[ -d "${WORK}/.cf-powers/sdd/plan" ] || fail "sdd-workspace did not create the plan dir"
# The .gitignore sits one level up, covering every plan's workspace at once.
[ "$(cat "${WORK}/.cf-powers/sdd/.gitignore")" = "*" ] || fail "sdd-workspace .gitignore not self-ignoring"
# The workspace must not show up in git status (self-ignored).
[ -z "$(git status --porcelain | grep -F '.cf-powers' || true)" ] || fail "sdd-workspace leaks into git status"

# A second plan gets its own directory — it can never read the first's ledger.
cat > other-plan.md <<'PLAN'
# Other Plan
PLAN
out2="$("${SCRIPTS}/sdd-workspace" other-plan.md)"
[ "${out2}" = "${WORK}/.cf-powers/sdd/other-plan" ] || fail "second plan path: got '${out2}'"
[ "${out2}" != "${out}" ] || fail "two plans shared one workspace"

# The plan file is required, and must exist.
if "${SCRIPTS}/sdd-workspace" >/dev/null 2>&1; then fail "sdd-workspace accepted no PLAN_FILE"; fi
if "${SCRIPTS}/sdd-workspace" nope.md >/dev/null 2>&1; then fail "sdd-workspace accepted a missing plan file"; fi
echo "PASS: test1 sdd-workspace"
```

In test2, delete the now-duplicated `cat > plan.md` heredoc and its comment, keeping every assertion. Then add one assertion after the Task 2 checks, verifying briefs land in the plan's directory:

```bash
# Briefs land in the plan's own workspace, not the flat sdd root.
case "${b2}" in
  "${WORK}/.cf-powers/sdd/plan/"*) : ;;
  *) fail "task-brief wrote outside the plan workspace: ${b2}" ;;
esac
```

In test3, change the `review-package` invocations to the new signature and assert the output path is plan-scoped:

```bash
pkg="$("${SCRIPTS}/review-package" plan.md "${base}" "${head}" | sed -n 's/^wrote \(.*\): .*/\1/p')"
grep -q "commit two" "${pkg}" || fail "review-package missing 'commit two'"
grep -q "commit three" "${pkg}" || fail "review-package missing 'commit three'"
grep -q "## Diff" "${pkg}" || fail "review-package missing diff section"
grep -q "+two" "${pkg}" || fail "review-package missing first commit's change"
case "${pkg}" in
  "${WORK}/.cf-powers/sdd/plan/review-"*) : ;;
  *) fail "review-package wrote outside the plan workspace: ${pkg}" ;;
esac
# Bad base is rejected.
if "${SCRIPTS}/review-package" plan.md deadbeef "${head}" >/dev/null 2>&1; then fail "review-package accepted bad BASE"; fi
# A missing plan file is rejected.
if "${SCRIPTS}/review-package" nope.md "${base}" "${head}" >/dev/null 2>&1; then fail "review-package accepted a missing plan file"; fi
# The old two-argument form must not silently work.
if "${SCRIPTS}/review-package" "${base}" "${head}" >/dev/null 2>&1; then fail "review-package accepted the old BASE HEAD form"; fi
echo "PASS: test3 review-package"
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `tests/sdd-scripts/run-test.sh`

Expected: FAIL at the first assertion — `FAIL: sdd-workspace path: got '/…/.cf-powers/sdd'`. The current script ignores arguments and returns the flat path.

- [ ] **Step 3: Rewrite `sdd-workspace`**

Replace the entire contents of `skills/subagent-driven-development/scripts/sdd-workspace` with:

```bash
#!/usr/bin/env bash
# Resolve and ensure the working-tree directory SDD uses for one plan's
# short-lived artifacts: task briefs, implementer reports, review packages,
# and the progress ledger. Print the plan directory's absolute path.
#
# One directory per plan (.cf-powers/sdd/<plan-basename>/) so a follow-up
# plan in the same working tree can never read or overwrite another plan's
# artifacts. A stale ledger misread as current progress makes controllers
# skip whole task sequences — plan-scoping removes that failure structurally.
#
# The workspace lives in the working tree (not under .git/) because Claude Code
# treats .git/ as a protected path and denies agent writes there — which blocks
# an implementer subagent from writing its report file. A self-ignoring
# .gitignore at .cf-powers/sdd/ keeps every plan's workspace out of
# `git status` and out of accidental commits without modifying any tracked file.
#
# Single source of truth for the workspace location, so task-brief and
# review-package cannot drift to different directories.
#
# Usage: sdd-workspace PLAN_FILE
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: sdd-workspace PLAN_FILE" >&2
  exit 2
fi

plan=$1
[ -f "$plan" ] || { echo "no such plan file: $plan" >&2; exit 2; }

slug=$(basename "$plan" .md)
[ -n "$slug" ] && [ "$slug" != "." ] && [ "$slug" != ".." ] \
  || { echo "cannot derive a workspace name from: $plan" >&2; exit 2; }

root=$(git rev-parse --show-toplevel)
base="$root/.cf-powers/sdd"
dir="$base/$slug"
mkdir -p "$dir"
printf '*\n' > "$base/.gitignore"
cd "$dir" && pwd
```

- [ ] **Step 4: Pass the plan through `task-brief`**

In `skills/subagent-driven-development/scripts/task-brief`, update the usage comment (lines 7-8):

```bash
# Default OUTFILE: <repo-root>/.cf-powers/sdd/<plan-basename>/task-<N>-brief.md
# (per plan and per worktree; concurrent runs of the SAME plan in the same
# working tree share it).
```

and pass the plan to the workspace resolver (line 24):

```bash
  dir=$("$(cd "$(dirname "$0")" && pwd)/sdd-workspace" "$plan")
```

- [ ] **Step 5: Add `PLAN_FILE` to `review-package`**

In `skills/subagent-driven-development/scripts/review-package`, replace the usage comment (lines 7-8):

```bash
# Usage: review-package PLAN_FILE BASE HEAD [OUTFILE]
# Default OUTFILE: <repo-root>/.cf-powers/sdd/<plan-basename>/review-<base7>..<head7>.diff
```

and replace the argument handling (lines 12-29) with:

```bash
if [ $# -lt 3 ] || [ $# -gt 4 ]; then
  echo "usage: review-package PLAN_FILE BASE HEAD [OUTFILE]" >&2
  exit 2
fi

plan=$1
base=$2
head=$3
[ -f "$plan" ] || { echo "no such plan file: $plan" >&2; exit 2; }

git rev-parse --verify --quiet "$base" >/dev/null || { echo "bad BASE: $base" >&2; exit 2; }
git rev-parse --verify --quiet "$head" >/dev/null || { echo "bad HEAD: $head" >&2; exit 2; }

if [ $# -eq 4 ]; then
  out=$4
else
  dir=$("$(cd "$(dirname "$0")" && pwd)/sdd-workspace" "$plan")
  out="$dir/review-$(git rev-parse --short "$base")..$(git rev-parse --short "$head").diff"
fi
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `tests/sdd-scripts/run-test.sh`

Expected: PASS — `PASS: test1 sdd-workspace`, `PASS: test2 task-brief`, `PASS: test3 review-package`, `ALL PASS`.

- [ ] **Step 7: Commit**

```bash
git add tests/sdd-scripts/run-test.sh skills/subagent-driven-development/scripts/
git commit -m "feat(sdd)!: plan-scoped workspace, review-package takes PLAN_FILE first"
```

---

### Task 2: Port the prompt templates

The fix loop needs a scoped re-review template — a reviewer that verdicts each prior finding ADDRESSED / NOT ADDRESSED and inspects only the fix diff, rather than re-reading the whole task. The implementer template gains the resume contract, and the task reviewer's placeholder list picks up the new `review-package` signature.

**Files:**
- Create: `skills/subagent-driven-development/re-review-prompt.md`
- Modify: `skills/subagent-driven-development/implementer-prompt.md` (the `## After Review Findings` section)
- Modify: `skills/subagent-driven-development/task-reviewer-prompt.md` (the `[DIFF_FILE]` placeholder and the trailing fix-dispatch note)

**Interfaces:**
- Consumes: the `review-package PLAN_FILE BASE HEAD` signature from Task 1.
- Produces: `re-review-prompt.md` — the path Task 3's SKILL.md links from the fix loop.

- [ ] **Step 1: Port the re-review template**

```bash
cp "$UPSTREAM/skills/subagent-driven-development/re-review-prompt.md" \
   skills/subagent-driven-development/re-review-prompt.md
```

Then apply the fork adaptations. The file needs no `superpowers:` rename (it has none), but confirm the `review-package PLAN_FILE FIX_BASE HEAD` reference is present in the `[DIFF_FILE]` placeholder — that is the new signature from Task 1.

- [ ] **Step 2: Verify the port**

Run: `diff "$UPSTREAM/skills/subagent-driven-development/re-review-prompt.md" skills/subagent-driven-development/re-review-prompt.md`

Expected: no output — a clean verbatim copy.

Run: `grep -n "superpowers:\|\.superpowers/\|using-git-worktrees" skills/subagent-driven-development/re-review-prompt.md`

Expected: no output (exit 1).

Run: `grep -n "MODEL — REQUIRED\|read-only\|Out-of-Scope Observations" skills/subagent-driven-development/re-review-prompt.md`

Expected: all three present — the required-model rule, the read-only constraint, and the out-of-scope escape hatch that stops the loop from extending itself.

- [ ] **Step 3: Give the implementer the resume contract**

In `skills/subagent-driven-development/implementer-prompt.md`, replace the `## After Review Findings` body:

```markdown
    If a reviewer finds issues and you fix them, re-run the tests that cover
    the amended code and append the results to your report file. Reviewers
    will not re-run tests for you — your report is the test evidence.
```

with:

```markdown
    If the task review finds issues, you will be resumed with the findings.
    Fix them, re-run the tests that cover the amended code, and append a fix
    report to your report file: what you changed, the covering tests you
    ran, the command, and the output. Reviewers will not re-run tests for
    you — your report is the test evidence. Then reply with the same short
    status contract as your first report.
```

- [ ] **Step 4: Update the task reviewer's placeholder and trailing note**

In `skills/subagent-driven-development/task-reviewer-prompt.md`, update the `[DIFF_FILE]` placeholder text to the new signature:

```markdown
- `[DIFF_FILE]` — REQUIRED: the path the controller wrote the review
  package to (`scripts/review-package PLAN_FILE BASE HEAD` prints the unique
  path it wrote; the package never enters the controller's context)
```

Then delete the two trailing lines after the **Reviewer returns:** paragraph:

```markdown
A fix dispatch can address spec gaps and quality findings together;
re-review after fixes covers both verdicts.
```

The fix loop in SKILL.md now owns that behaviour, and the scoped re-review template describes it precisely.

- [ ] **Step 5: Verify template cross-references**

Run: `grep -rn "review-package" skills/subagent-driven-development/*.md`

Expected: every occurrence reads `review-package PLAN_FILE …`. No bare `review-package BASE HEAD` survives.

- [ ] **Step 6: Commit**

```bash
git add skills/subagent-driven-development/re-review-prompt.md \
        skills/subagent-driven-development/implementer-prompt.md \
        skills/subagent-driven-development/task-reviewer-prompt.md
git commit -m "feat(sdd): add scoped re-review template, resume contract for implementers"
```

---

### Task 3: Restructure `SKILL.md` around the lifecycle

The skill is reorganized by lifecycle — Setup, The Task Loop (dispatch → report → review → fix loop → complete), Final Review, Finish — and its Red Flags / Advantages / Integration sections convert to the house rationalization table. The fix loop gains resume semantics, the five-round breaker, and adjudication rules.

**Files:**
- Modify: `skills/subagent-driven-development/SKILL.md` (full restructure)

**Interfaces:**
- Consumes: the script signatures from Task 1 and `re-review-prompt.md` from Task 2.
- Produces: nothing later tasks rely on.

- [ ] **Step 1: Port the restructured skill**

```bash
cp "$UPSTREAM/skills/subagent-driven-development/SKILL.md" \
   skills/subagent-driven-development/SKILL.md
```

- [ ] **Step 2: Apply the mechanical fork renames**

```bash
F=skills/subagent-driven-development/SKILL.md
sed -i '' \
  -e 's/superpowers:/cf-powers:/g' \
  -e 's|\.superpowers/sdd|.cf-powers/sdd|g' \
  -e 's|docs/superpowers/plans|docs/plans|g' \
  -e 's|~/\.config/superpowers/|~/.config/cf-powers/|g' \
  -e 's/brainstorm first/analyse first/g' \
  "$F"
```

Then verify nothing was missed:

```bash
grep -n "superpowers" "$F"
```

Expected: no output (exit 1).

- [ ] **Step 3: Replace the worktree Setup line with our branch policy**

Upstream's `## Setup` opens by requiring `using-git-worktrees`, which we do not ship. Replace:

```markdown
Ensure the work happens in an isolated workspace: use
cf-powers:using-git-worktrees to create one or verify the existing one.
Never start implementation on a main/master branch without your human
partner's explicit consent.
```

with our fork's policy — the user manages their own branches:

```markdown
Verify the work is on a feature branch before dispatching anything. Your
human partner manages their own branches; do not create worktrees
automatically. Never start implementation on a main/master branch without
their explicit consent.
```

- [ ] **Step 4: Name Claude Code's resume mechanism in the fix loop**

Upstream hedges rounds 1-3 with "If your harness cannot send another message to a live subagent". We are Claude-Code-only and can name the mechanism. Replace:

```markdown
**Rounds 1-3 — resume the original implementer.** Send it the open findings
verbatim. Its context is intact: it knows the task, the code, and its own
choices. If your harness cannot send another message to a live subagent,
dispatch a fresh implementer carrying the brief path, the report-file path,
and the findings — the report file is the persistent memory either way.
```

with:

```markdown
**Rounds 1-3 — resume the original implementer.** Send it the open findings
verbatim with SendMessage, addressed to the agent ID you recorded at
dispatch. Its context is intact: it knows the task, the code, and its own
choices. If that agent is gone — a compacted or restarted session loses the
handle — dispatch a fresh implementer carrying the brief path, the
report-file path, and the findings; the report file is the persistent memory
either way.
```

- [ ] **Step 5: Confirm the fix-loop machinery survived the port intact**

Run: `grep -n "Fix round\|R = 5\|five-round\|Five rounds\|breaker\|BLOCKED\|parked" skills/subagent-driven-development/SKILL.md`

Expected: the five-round cap, the breaker, the `BLOCKED` ledger line, and the parked-with-ruling path all present.

Run: `grep -n "re-review-prompt.md\|task-reviewer-prompt.md\|implementer-prompt.md\|code-reviewer.md" skills/subagent-driven-development/SKILL.md`

Expected: all four templates linked. `code-reviewer.md` must resolve to `../requesting-code-review/code-reviewer.md`.

Run: `grep -c "review-package PLAN_FILE" skills/subagent-driven-development/SKILL.md`

Expected: `4` or more — the task review, each fix round's scoped re-review, the final whole-branch review, and the final fix wave all call it with the plan file.

- [ ] **Step 6: Verify every referenced path exists**

```bash
for f in implementer-prompt.md task-reviewer-prompt.md re-review-prompt.md \
         scripts/sdd-workspace scripts/task-brief scripts/review-package; do
  test -e "skills/subagent-driven-development/$f" || echo "MISSING: $f"
done
test -e skills/requesting-code-review/code-reviewer.md || echo "MISSING: code-reviewer.md"
```

Expected: no output. Every link target exists.

- [ ] **Step 7: Confirm the removed sections are gone and nothing dangles**

Run: `grep -n "^## " skills/subagent-driven-development/SKILL.md`

Expected: `Overview`, `When to Use`, `Setup`, `Model Selection`, `The Task Loop`, `Final Review`, `Finish`, `Common Rationalizations`, `Example Workflow` — with no `Advantages`, `Red Flags`, `Integration`, `File Handoffs`, `Durable Progress`, or `Prompt Templates` sections (all folded into the lifecycle sections).

Run: `tests/sdd-scripts/run-test.sh`

Expected: PASS — `ALL PASS`. The scripts are untouched by this task; this confirms Task 1 still holds.

- [ ] **Step 8: Commit**

```bash
git add skills/subagent-driven-development/SKILL.md
git commit -m "refactor(sdd)!: lifecycle restructure with resume-based fix loop and five-round breaker"
```
