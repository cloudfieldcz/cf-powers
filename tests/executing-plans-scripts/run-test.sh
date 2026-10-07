#!/usr/bin/env bash
# Tests for executing-plans helper scripts: task-start, task-done.
#
# Each scenario runs in a throwaway git repo under a temp dir. Scripts run
# through bash, as the skill instructs.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
EP="${REPO_ROOT}/skills/executing-plans/scripts"

WORK="$(cd "$(mktemp -d)" && pwd -P)"  # physical path; macOS /var -> /private/var
cleanup() { rm -rf "${WORK}"; }
trap cleanup EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

cd "${WORK}"
git init -q
git config user.email test@example.com
git config user.name test
git config commit.gpgsign false

cat > plan.md <<'PLAN'
# Plan

### Task 1: First thing
Do the first thing.

### Task 2: Second thing
Do the second thing.
PLAN
git add plan.md; git commit -qm fixture
base="$(git rev-parse HEAD)"
ws="${WORK}/.cf-powers/sdd/plan"

# --- test1: task-start -------------------------------------------------------
rc=0; bash "${EP}/task-start" plan.md >/dev/null 2>&1 || rc=$?
[ "${rc}" -eq 2 ] || fail "task-start without a task number exit ${rc}, want 2"
out="$(bash "${EP}/task-start" plan.md 1)"
case "${out}" in *"brief: ${ws}/task-1-brief.md"*) : ;; *) fail "task-start brief path: ${out}" ;; esac
case "${out}" in *"base: ${base}"*) : ;; *) fail "task-start BASE: ${out}" ;; esac
[ -s "${ws}/task-1-brief.md" ] || fail "task-start wrote no brief"
echo "PASS: test1 task-start"

# --- test2: task-done records a passing task ---------------------------------
echo x > work.txt; git add work.txt; git commit -qm "task 1"
head="$(git rev-parse HEAD)"
out="$(bash "${EP}/task-done" ./plan.md 1 "${base}" -- sh -c 'echo "Ran 3 tests"; echo OK')"
ledger="${ws}/progress.md"
expected="Task 1: complete (commits ${base:0:7}..${head:0:7}, tests: sh -c 'echo \"Ran 3 tests\"; echo OK' → OK)"
grep -qF "${expected}" "${ledger}" || fail "task-done ledger line missing: $(cat "${ledger}")"
case "${out}" in *OK*) : ;; *) fail "task-done did not print the tail: ${out}" ;; esac
[ -s "${ws}/task-1-tests.log" ] || fail "task-done kept no log"
# The header comes from the plan-path marker, not from the spelling used.
[ "$(head -n 1 "${ledger}")" = "# SDD ledger — plan: plan.md" ] || fail "ledger header: $(head -n 1 "${ledger}")"
echo "PASS: test2 task-done success"

# --- test3: a failing run records nothing ------------------------------------
rc=0
out="$(bash "${EP}/task-done" plan.md 2 "${base}" -- sh -c 'echo "FAILED (errors=1)"; exit 1' 2>&1)" || rc=$?
[ "${rc}" -ne 0 ] || fail "task-done succeeded on a failing command"
grep -q "Task 2: complete" "${ledger}" && fail "task-done recorded a failing task"
case "${out}" in *FAILED*) : ;; *) fail "task-done hid the failing output: ${out}" ;; esac
echo "PASS: test3 failing run"

# --- test4: refuses an empty range or a non-ancestor BASE (exit 3) -----------
rc=0; bash "${EP}/task-done" plan.md 2 "${head}" -- true >/dev/null 2>&1 || rc=$?
[ "${rc}" -eq 3 ] || fail "HEAD==BASE exit ${rc}, want 3"
git checkout -q -b side "${base}"
echo s > s.txt; git add s.txt; git commit -qm side
rc=0; bash "${EP}/task-done" plan.md 2 "${head}" -- true >/dev/null 2>&1 || rc=$?
[ "${rc}" -eq 3 ] || fail "non-ancestor BASE exit ${rc}, want 3"
grep -q "Task 2: complete" "${ledger}" && fail "task-done recorded a refused range"
git checkout -q - 
echo "PASS: test4 range guards"

# --- test5: the test command gets no stdin -----------------------------------
echo y >> work.txt; git add work.txt; git commit -qm "task 2"
out="$(echo piped | bash "${EP}/task-done" plan.md 2 "${head}" -- sh -c 'if read -r l; then echo "STDIN:$l"; else echo EOF; fi')"
case "${out}" in *EOF*) : ;; *) fail "test command read stdin: ${out}" ;; esac
echo "PASS: test5 stdin closed"

# --- test6: scripts work via bash with exec bits stripped (copy only) --------
NOX="${WORK}/noexec/executing-plans/scripts"
mkdir -p "${NOX}" "${WORK}/noexec/subagent-driven-development"
cp "${EP}"/task-start "${EP}"/task-done "${NOX}/"
cp -R "${REPO_ROOT}/skills/subagent-driven-development/scripts" "${WORK}/noexec/subagent-driven-development/"
chmod -x "${NOX}"/* "${WORK}"/noexec/subagent-driven-development/scripts/*
out="$(bash "${NOX}/task-start" plan.md 2)"
case "${out}" in *"brief: "*"task-2-brief.md"*) : ;; *) fail "task-start via bash without +x: ${out}" ;; esac
b2="$(git rev-parse HEAD)"
echo z >> work.txt; git add work.txt; git commit -qm "task 2b"
bash "${NOX}/task-done" plan.md 2 "${b2}" -- true >/dev/null || fail "task-done via bash without +x failed"
echo "PASS: test6 no exec bit"

echo "ALL PASS"
