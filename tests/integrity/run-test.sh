#!/usr/bin/env bash
# F-00 integrity verification test for hooks/session-start.
# Three scenarios:
#   1. Positive — pristine repo, baseline matches → SKILL.md injected.
#   2. Tampered — SKILL.md modified → fail-closed alert, no SKILL.md content.
#   3. Missing baseline — integrity.sha256 absent → fail-closed alert.
#
# Restores all state via trap. Run from anywhere; resolves repo root from $0.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
HOOK="${REPO_ROOT}/hooks/session-start"
SKILL="${REPO_ROOT}/skills/using-superpowers/SKILL.md"
BASELINE="${REPO_ROOT}/.claude-plugin/integrity.sha256"

BACKUP_SKILL="$(mktemp)"
BACKUP_BASELINE="$(mktemp)"
cp "${SKILL}" "${BACKUP_SKILL}"
cp "${BASELINE}" "${BACKUP_BASELINE}"

cleanup() {
    cp "${BACKUP_SKILL}" "${SKILL}" 2>/dev/null || true
    cp "${BACKUP_BASELINE}" "${BASELINE}" 2>/dev/null || true
    rm -f "${BACKUP_SKILL}" "${BACKUP_BASELINE}"
}
trap cleanup EXIT

export CLAUDE_PLUGIN_ROOT="${REPO_ROOT}"

pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*" >&2; exit 1; }

# --- Test 1: Positive path -------------------------------------------------
out=$(bash "${HOOK}")
echo "${out}" | grep -q "EXTREMELY_IMPORTANT" || fail "test1 positive: missing EXTREMELY_IMPORTANT"
echo "${out}" | grep -q "security-alert" && fail "test1 positive: unexpected security-alert"
pass "test1 positive path"

# --- Test 2: Tampered SKILL.md ---------------------------------------------
echo "# tamper" >> "${SKILL}"
out=$(bash "${HOOK}")
echo "${out}" | grep -q "security-alert" || fail "test2 tampered: missing security-alert"
echo "${out}" | grep -q "EXTREMELY_IMPORTANT" && fail "test2 tampered: unexpected EXTREMELY_IMPORTANT"
cp "${BACKUP_SKILL}" "${SKILL}"
pass "test2 tampered path"

# --- Test 3: Missing baseline ----------------------------------------------
rm -f "${BASELINE}"
out=$(bash "${HOOK}")
echo "${out}" | grep -q "security-alert" || fail "test3 missing-baseline: missing security-alert"
echo "${out}" | grep -q "EXTREMELY_IMPORTANT" && fail "test3 missing-baseline: unexpected EXTREMELY_IMPORTANT"
cp "${BACKUP_BASELINE}" "${BASELINE}"
pass "test3 missing-baseline path"

echo "ALL PASS"
