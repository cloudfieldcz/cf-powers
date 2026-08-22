#!/usr/bin/env bash
# Tests for the orchestrator helper script: orchestrator-workspace.
#
# Each scenario runs in a throwaway git repo under a temp dir, so nothing
# touches the real working tree. Run from anywhere; resolves the scripts
# directory from $0.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SCRIPTS="${REPO_ROOT}/skills/orchestrator/scripts"

WORK="$(cd "$(mktemp -d)" && pwd -P)"  # physical path; macOS /var -> /private/var
cleanup() { rm -rf "${WORK}"; }
trap cleanup EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

cd "${WORK}"
git init -q
git config user.email test@example.com
git config user.name test
git config commit.gpgsign false

echo "# Plan Index" > big-thing-index.md
echo "# Other Index" > other-index.md

# --- test1: a file argument scopes the workspace to that file's basename ----
out="$("${SCRIPTS}/orchestrator-workspace" big-thing-index.md)"
[ "${out}" = "${WORK}/.cf-powers/orchestrator/big-thing-index" ] \
    || fail "file arg path: got '${out}'"
[ -d "${WORK}/.cf-powers/orchestrator/big-thing-index" ] || fail "run dir not created"
# The .gitignore sits one level up, covering every run's workspace at once.
[ "$(cat "${WORK}/.cf-powers/orchestrator/.gitignore")" = "*" ] \
    || fail ".gitignore not self-ignoring"
[ -z "$(git status --porcelain | grep -F '.cf-powers' || true)" ] \
    || fail "workspace leaks into git status"

# --- test2: a second job gets its own directory ----------------------------
# A run must never be able to read another run's ledger.
echo "ledger one" > "${WORK}/.cf-powers/orchestrator/big-thing-index/run.md"
out2="$("${SCRIPTS}/orchestrator-workspace" other-index.md)"
[ "${out2}" = "${WORK}/.cf-powers/orchestrator/other-index" ] \
    || fail "second job path: got '${out2}'"
[ ! -e "${out2}/run.md" ] || fail "second job sees the first job's ledger"

# --- test3: a bare slug works for a job with no file behind it -------------
out3="$("${SCRIPTS}/orchestrator-workspace" auth-helper-migration)"
[ "${out3}" = "${WORK}/.cf-powers/orchestrator/auth-helper-migration" ] \
    || fail "bare slug path: got '${out3}'"
[ -d "${out3}" ] || fail "bare-slug run dir not created"

# --- test4: the same argument is idempotent, contents survive --------------
echo "ledger three" > "${out3}/run.md"
out4="$("${SCRIPTS}/orchestrator-workspace" auth-helper-migration)"
[ "${out4}" = "${out3}" ] || fail "not idempotent: '${out4}' != '${out3}'"
[ "$(cat "${out3}/run.md")" = "ledger three" ] || fail "re-resolve clobbered the ledger"

# --- test5: traversal and empty names are rejected -------------------------
for bad in "../escape" "a/b" ".." "." ""; do
    if out5="$("${SCRIPTS}/orchestrator-workspace" "${bad}" 2>/dev/null)"; then
        fail "accepted unsafe name '${bad}' → '${out5}'"
    fi
done
[ ! -e "${WORK}/.cf-powers/escape" ] || fail "traversal created a dir outside the base"

# --- test6: wrong arity is a usage error ----------------------------------
if "${SCRIPTS}/orchestrator-workspace" >/dev/null 2>&1; then
    fail "accepted zero arguments"
fi
if "${SCRIPTS}/orchestrator-workspace" a b >/dev/null 2>&1; then
    fail "accepted two arguments"
fi

echo "ALL PASS"
