# Upstream Sync v6.2.0 — Phase 1: Bug Fixes

> **For agentic workers:** REQUIRED SUB-SKILL: Use cf-powers:subagent-driven-development (recommended) or cf-powers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the two upstream defects that our fork demonstrably shares: `find-polluter.sh` never finds any test files, and the Windows SessionStart hook never loads the bootstrap.

**Architecture:** Both are small, self-contained fixes ported verbatim from upstream. The `find-polluter.sh` fix arrives test-first — upstream shipped a deterministic test suite alongside it, and our copy of the script is byte-identical to the broken version, so the test is a genuine RED before the fix lands.

**Tech Stack:** Bash, `find`, Claude Code hooks JSON.

**Index:** [`plan-index.md`](./2026-07-25-upstream-sync-v6.2.0-plan-index.md)

## Global Constraints

- Upstream source of truth: `obra/superpowers` at tag **v6.2.0** (commit `3dcbd5c`), referred to as `$UPSTREAM`.
- **Fork adaptation rules** — apply to every ported line: `superpowers:` → `cf-powers:`; `.superpowers/sdd/` → `.cf-powers/sdd/`; `docs/superpowers/plans/` → `docs/plans/`; `~/.config/superpowers/` → `~/.config/cf-powers/`; `brainstorming` → `analysis`; drop every reference to `using-git-worktrees` (we do not ship it).
- **Do not adopt upstream's vendor-neutral vocabulary.** Keep the Claude Code dialect ("Task tool", "CLAUDE.md").
- Never reference a skill we do not ship: `brainstorming`, `using-git-worktrees`, `testing-anti-patterns` (after Phase 2).
- `tests/integrity/run-test.sh` fails from the first `SKILL.md` edit until Phase 5 regenerates the baseline. Expected. All other suites stay green.
- One commit per task.

---

### Task 1: `find-polluter.sh` finds test files again

Upstream issues #2008 and #2011. `find .` emits `./`-prefixed paths, so the pattern documented in the script's own usage line (`src/**/*.test.ts`) matched nothing. `wc -l` over empty input then reported `Found 1 test files`, so the script claimed to be working while running zero tests. Our copy is byte-identical to that broken version.

**Files:**
- Create: `tests/systematic-debugging/run-test.sh`
- Modify: `skills/systematic-debugging/find-polluter.sh:21-23`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: nothing later tasks rely on.

- [ ] **Step 1: Write the failing test**

Create `tests/systematic-debugging/run-test.sh`, adapted from `$UPSTREAM/tests/systematic-debugging/test-find-polluter.sh`. Our tests live at `tests/<area>/run-test.sh`, so the filename differs from upstream's; the content is the same four scenarios.

```bash
#!/usr/bin/env bash
# Tests for skills/systematic-debugging/find-polluter.sh.
#
# Guards upstream #2008/#2011: `find .` emits ./-prefixed paths, so the
# pattern in the script's own usage line matched nothing — and `wc -l` over
# empty input reported "Found 1", so the script looked like it was working.
#
# Each scenario builds a throwaway toy project under a temp dir with a stubbed
# `npm` that creates the pollution marker whenever any test runs, so the first
# test file executed is always identified as the polluter.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SCRIPT_UNDER_TEST="${REPO_ROOT}/skills/systematic-debugging/find-polluter.sh"

FAILURES=0
TEST_ROOT="$(mktemp -d)"
cleanup() { rm -rf "${TEST_ROOT}"; }
trap cleanup EXIT

pass() { echo "  [PASS] $1"; }
fail() { echo "  [FAIL] $1"; FAILURES=$((FAILURES + 1)); }

assert_contains() {
  local haystack="$1" needle="$2" description="$3"
  if printf '%s' "${haystack}" | grep -Fq -- "${needle}"; then
    pass "${description}"
  else
    fail "${description} (expected output to contain: ${needle})"
  fi
}

setup_project() {
  PROJECT="${TEST_ROOT}/project"
  rm -rf "${PROJECT}"
  mkdir -p "${PROJECT}/src/feature" "${PROJECT}/bin"
  echo "test('top')" > "${PROJECT}/src/top.test.ts"
  echo "test('nested')" > "${PROJECT}/src/feature/nested.test.ts"
  cat > "${PROJECT}/bin/npm" <<'EOF'
#!/usr/bin/env bash
touch pollution.marker
EOF
  chmod +x "${PROJECT}/bin/npm"
}

# run_polluter <pattern> — runs the script in the toy project with the stub
# npm first on PATH; captures combined output, never aborts on exit code.
run_polluter() {
  local pattern="$1"
  rm -f "${PROJECT}/pollution.marker"
  (
    cd "${PROJECT}"
    PATH="${PROJECT}/bin:${PATH}" "${SCRIPT_UNDER_TEST}" 'pollution.marker' "${pattern}" 2>&1
  ) || true
}

echo "Test: documented pattern finds nested test files (issue #2008)"
setup_project
OUTPUT="$(run_polluter 'src/**/*.test.ts')"
assert_contains "${OUTPUT}" "FOUND POLLUTER" "documented pattern runs tests and detects pollution"

echo "Test: documented pattern also finds top-level test files"
setup_project
OUTPUT="$(run_polluter 'src/**/*.test.ts')"
assert_contains "${OUTPUT}" "Found 2 test files" "src/**/*.test.ts matches src/top.test.ts and src/feature/nested.test.ts"

echo "Test: ./-prefixed pattern matches the same files"
setup_project
OUTPUT="$(run_polluter './src/**/*.test.ts')"
assert_contains "${OUTPUT}" "Found 2 test files" "leading ./ on the pattern is accepted"

echo "Test: non-matching pattern reports an honest zero"
setup_project
OUTPUT="$(run_polluter 'nomatch/**/*.test.ts')"
assert_contains "${OUTPUT}" "Found 0 test files" "empty result counts as 0, not 1"
assert_contains "${OUTPUT}" "No polluter found" "empty result exits via the clean path"

echo ""
if [ "${FAILURES}" -gt 0 ]; then
  echo "${FAILURES} test(s) failed"
  exit 1
fi
echo "All tests passed"
```

Make it executable:

```bash
chmod +x tests/systematic-debugging/run-test.sh
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `tests/systematic-debugging/run-test.sh`

Expected: FAIL — 5 of 5 assertions fail. The broken script reports `Found 1 test files`, never runs a test, and prints `No polluter found` for the patterns that should find two files.

- [ ] **Step 3: Apply the fix**

In `skills/systematic-debugging/find-polluter.sh`, replace lines 21-23:

```bash
# Get list of test files
TEST_FILES=$(find . -path "$TEST_PATTERN" | sort)
TOTAL=$(echo "$TEST_FILES" | wc -l | tr -d ' ')
```

with:

```bash
# Get list of test files (find . emits ./-prefixed paths, so accept the
# pattern written with or without a leading ./)
TEST_PATTERN="${TEST_PATTERN#./}"
# find -path can't match '**/' against zero directory levels, so a pattern
# like src/**/*.test.ts would skip src/top.test.ts; also try the pattern
# with '**/' collapsed to cover files directly under the base directory.
TEST_FILES=$(find . \( -path "./$TEST_PATTERN" -o -path "./${TEST_PATTERN//\*\*\//}" \) | sort -u)
if [ -z "$TEST_FILES" ]; then
  TOTAL=0
else
  TOTAL=$(printf '%s\n' "$TEST_FILES" | wc -l | tr -d ' ')
fi
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `tests/systematic-debugging/run-test.sh`

Expected: PASS — `All tests passed`, 5 assertions green.

- [ ] **Step 5: Commit**

```bash
git add tests/systematic-debugging/run-test.sh skills/systematic-debugging/find-polluter.sh
git commit -m "fix(systematic-debugging): find-polluter matches ./-prefixed and top-level tests"
```

---

### Task 2: Windows SessionStart hook dispatches via Git Bash

Upstream issues #1751 and #1918. Our hook command string starts with a quoted path, which breaks both shells Claude Code may hand it on Windows: PowerShell parses the leading quoted string as an expression and dies on the next bareword, and cmd.exe's `/c` quote rule drops the outer quotes when the path contains a metacharacter, so a profile directory like `C:\Users\Name(External)` truncates the command at the `(`. Either way the bootstrap silently never loads.

Declaring `shell: "bash"` makes Claude Code ≥ 2.1.81 resolve Git for Windows and run the polyglot's bash path directly, and surface an actionable install prompt when Git Bash is missing. Older versions ignore the unknown key and behave exactly as before. No effect on macOS/Linux.

**Files:**
- Modify: `hooks/hooks.json:10`
- Modify: `docs/windows/polyglot-hooks.md:7-9`, `docs/windows/polyglot-hooks.md` (hooks.json example)

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: nothing later tasks rely on.

- [ ] **Step 1: Add the `shell` key to the hook**

In `hooks/hooks.json`, add `"shell": "bash"` after the `command` line:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start",
            "shell": "bash",
            "async": false
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 2: Verify the hook still fires locally**

Run: `hooks/session-start`

Expected: the bootstrap payload on stdout — a JSON object whose `additionalContext` contains `You have superpowers.` and the full `using-superpowers` SKILL.md body. (This exercises the Unix path of the polyglot, which the `shell` key does not change.)

- [ ] **Step 3: Run the integrity suite to confirm the hook contract is intact**

Run: `tests/integrity/run-test.sh`

Expected: PASS — all three scenarios (pristine, tampered, missing baseline). No `SKILL.md` has changed yet in this phase, so the baseline still matches.

- [ ] **Step 4: Update the Windows documentation**

In `docs/windows/polyglot-hooks.md`, replace the two-line shell list under `## The Problem`:

```markdown
Claude Code runs hook commands through the system's default shell:
- **Windows**: CMD.exe
- **macOS/Linux**: bash or sh
```

with:

```markdown
Claude Code runs hook commands through a shell:
- **macOS/Linux**: bash or sh
- **Windows with Git Bash installed**: Git Bash
- **Windows without Git Bash**: PowerShell (older versions used CMD.exe)

Neither Windows fallback shell can parse our command string: PowerShell treats
a leading quoted path as a string expression and errors on the next bareword,
and CMD.exe's `/c` quoting rules strip the outer quotes when the path contains
a metacharacter such as `(`. Our hooks therefore declare `"shell": "bash"`
(supported since Claude Code 2.1.81; older versions ignore the key), which
forces the Git Bash route and, when Git Bash is absent, produces an actionable
"install Git for Windows" error instead of a shell parser failure.
```

Then add `"shell": "bash",` after the `"command":` line in that document's `hooks.json` example so the doc matches the shipped file.

- [ ] **Step 5: Commit**

```bash
git add hooks/hooks.json docs/windows/polyglot-hooks.md
git commit -m "fix(hooks): dispatch the SessionStart hook via Git Bash on Windows"
```
