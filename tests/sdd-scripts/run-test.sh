#!/usr/bin/env bash
# Tests for subagent-driven-development helper scripts:
#   sdd-workspace, task-brief, review-package.
#
# Each scenario runs in a throwaway git repo under a temp dir, so nothing
# touches the real working tree. Run from anywhere; resolves the scripts
# directory from $0.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SCRIPTS="${REPO_ROOT}/skills/subagent-driven-development/scripts"

WORK="$(cd "$(mktemp -d)" && pwd -P)"  # physical path; macOS /var -> /private/var
cleanup() { rm -rf "${WORK}"; }
trap cleanup EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

# Isolated git repo for the scenarios.
cd "${WORK}"
git init -q
git config user.email test@example.com
git config user.name test
git config commit.gpgsign false

# Shared plan fixture. Task 1's body contains a fenced "### Task 2" decoy; the
# fence guard must not treat it as a real boundary, so Task 1 extraction runs
# past it.
cat > plan.md <<'PLAN'
# Feature Plan

### Task 1: ALPHA work
- [ ] Step: do A
Body alpha-one.
```
### Task 2: decoy heading inside a fence
```
Body alpha-after-fence.

### Task 2: BETA work
- [ ] Step: do B
Body beta-two.

### Task 3: GAMMA work
- [ ] Step: do C
Body gamma-three.
PLAN

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

# --- test2: task-brief extracts only the requested task --------------------
# Task 1 spans past the fenced decoy, but stops at the real Task 2 heading.
b1="$("${SCRIPTS}/task-brief" plan.md 1 | sed -n 's/^wrote \(.*\): .*/\1/p')"
grep -q "ALPHA work" "${b1}" || fail "task-brief missing Task 1 heading"
grep -q "Body alpha-after-fence." "${b1}" || fail "fence guard ended Task 1 early at decoy"
grep -q "BETA work" "${b1}" && fail "task-brief leaked Task 2 into Task 1"

# Task 2 is the real heading, not the fenced decoy.
b2="$("${SCRIPTS}/task-brief" plan.md 2 | sed -n 's/^wrote \(.*\): .*/\1/p')"
grep -q "BETA work" "${b2}" || fail "task-brief missing Task 2 heading"
grep -q "Body beta-two." "${b2}" || fail "task-brief missing Task 2 body"
grep -q "ALPHA work" "${b2}" && fail "task-brief leaked Task 1 into Task 2"
grep -q "GAMMA work" "${b2}" && fail "task-brief leaked Task 3 into Task 2"

# Briefs land in the plan's own workspace, not the flat sdd root.
case "${b2}" in
  "${WORK}/.cf-powers/sdd/plan/"*) : ;;
  *) fail "task-brief wrote outside the plan workspace: ${b2}" ;;
esac

# Unknown task number is an error.
if "${SCRIPTS}/task-brief" plan.md 9 >/dev/null 2>&1; then fail "task-brief accepted missing task"; fi
echo "PASS: test2 task-brief"

# --- test3: review-package spans the whole BASE..HEAD range ----------------
echo one > f.txt; git add f.txt; git commit -qm "commit one"
base="$(git rev-parse HEAD)"
echo two >> f.txt; git add f.txt; git commit -qm "commit two"
echo three >> f.txt; git add f.txt; git commit -qm "commit three"
head="$(git rev-parse HEAD)"

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

echo "ALL PASS"
