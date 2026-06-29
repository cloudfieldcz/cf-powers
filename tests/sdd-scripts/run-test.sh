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

# --- test1: sdd-workspace --------------------------------------------------
out="$("${SCRIPTS}/sdd-workspace")"
[ "${out}" = "${WORK}/.cf-powers/sdd" ] || fail "sdd-workspace path: got '${out}'"
[ -d "${WORK}/.cf-powers/sdd" ] || fail "sdd-workspace did not create the dir"
[ "$(cat "${WORK}/.cf-powers/sdd/.gitignore")" = "*" ] || fail "sdd-workspace .gitignore not self-ignoring"
# The workspace must not show up in git status (self-ignored).
[ -z "$(git status --porcelain | grep -F '.cf-powers' || true)" ] || fail "sdd-workspace leaks into git status"
echo "PASS: test1 sdd-workspace"

# --- test2: task-brief extracts only the requested task --------------------
# Task 1's body contains a fenced "### Task 2" decoy; the fence guard must not
# treat it as a real boundary, so Task 1 extraction runs past it.
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

# Unknown task number is an error.
if "${SCRIPTS}/task-brief" plan.md 9 >/dev/null 2>&1; then fail "task-brief accepted missing task"; fi
echo "PASS: test2 task-brief"

# --- test3: review-package spans the whole BASE..HEAD range ----------------
echo one > f.txt; git add f.txt; git commit -qm "commit one"
base="$(git rev-parse HEAD)"
echo two >> f.txt; git add f.txt; git commit -qm "commit two"
echo three >> f.txt; git add f.txt; git commit -qm "commit three"
head="$(git rev-parse HEAD)"

pkg="$("${SCRIPTS}/review-package" "${base}" "${head}" | sed -n 's/^wrote \(.*\): .*/\1/p')"
grep -q "commit two" "${pkg}" || fail "review-package missing 'commit two'"
grep -q "commit three" "${pkg}" || fail "review-package missing 'commit three'"
grep -q "## Diff" "${pkg}" || fail "review-package missing diff section"
grep -q "+two" "${pkg}" || fail "review-package missing first commit's change"
# Bad base is rejected.
if "${SCRIPTS}/review-package" deadbeef "${head}" >/dev/null 2>&1; then fail "review-package accepted bad BASE"; fi
echo "PASS: test3 review-package"

echo "ALL PASS"
