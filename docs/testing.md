# Testing CF Powers

## Offline checks

Run from the repository root:

```bash
python3 tests/skill-triggering/test_harness.py
python3 tests/skill-triggering/test_results.py
python3 tests/skill-triggering/test_outcomes.py
bash tests/executing-plans-scripts/run-test.sh
bash tests/sdd-scripts/run-test.sh
bash tests/orchestrator-scripts/run-test.sh
bash tests/systematic-debugging/run-test.sh
bash tests/integrity/run-test.sh
bash tests/codex/run-test.sh
```

The integrity hook suite temporarily tampers with a skill and restores it; do
not run it concurrently with skill edits or baseline regeneration. Run
`bin/update-integrity` after intentional SKILL.md edits, then `bin/check-integrity`.

## Codex native integration

```bash
bash tests/codex/run-test.sh --native
```

Requires Codex CLI and Python 3.9+. Uses a committed disposable marketplace and
isolated CODEX_HOME to exercise actual installation, update, skills/list and
hooks/list. No login, model requests or global-profile edits. See
[Codex test guide](../tests/codex/README.md) for contracts and behavior scenarios.

The generic Plugin Creator validator rejects the empty hooks field; native
Codex accepts it and needs it to suppress Claude hook discovery. Keep that
compatibility decision covered by the native test.

## Claude behavior

The basic trigger/explicit-request runners and reference tests go through
`tests/claude-code/isolated-run.sh`. It passes `--plugin-dir`, `--setting-sources ""`,
and `--strict-mcp-config` with an empty MCP config. Isolated: user, project, and local
settings, CLAUDE.md files, and MCP servers. With no settings loaded, `enabledPlugins`
is not read either, so only `--plugin-dir` plugins are tested. The plugin's startup
hook still runs; `--bare` would disable it and must not be used for these tests.

Authentication, in order of use:

- Default: the active `claude` login (on macOS the OAuth token lives in the Keychain,
  so a fresh `CLAUDE_CONFIG_DIR` would be logged out).
- `CLAUDE_CODE_OAUTH_TOKEN` (from `claude setup-token`) or `ANTHROPIC_API_KEY` in the
  environment; both pass through unchanged.
- `CF_POWERS_TEST_CREDENTIALS_FILE`: path to a dedicated credentials file. Only then
  does the wrapper create a temporary `CLAUDE_CONFIG_DIR`, copy the file with mode
  0600, and delete the directory afterward.

The wrapper needs `timeout` or `gtimeout` (macOS: `brew install coreutils`).
Missing authentication is an infrastructure failure, not a skill failure.
Set `CF_POWERS_TEST_MODEL` to the same supported model for baseline and candidate.
Run:

```bash
bash tests/claude-code/run-skill-tests.sh
bash tests/skill-triggering/run-all.sh
bash tests/explicit-skill-requests/run-all.sh
```

The legacy SDD integration and specialized multi-turn scripts still have older
workflow assertions and use the caller's profile. They are diagnostic tools,
not evidence for the new isolated-runner contract. Audit their fixtures and
isolation before using them as a release gate for lifecycle changes:


```bash
bash tests/claude-code/run-skill-tests.sh --integration
```

Tests use real model sessions and can incur usage. Do not run authenticated
Claude tests through another agent without the required authorization. An old
installed version or a previous commit's green result does not verify new skills.

## Trigger and outcome evidence

`tests/skill-triggering/run-test.sh SKILL PROMPT [MAX_TURNS] [present|absent] [S1|S8]`
checks actual Skill tool events and the terminal result. Default is
3 turns and `present` for discovery probes. Exit 0 means the trigger expectation
matched and the turn completed; exit 1 is a behavioral mismatch; exit 2 is an
infrastructure/trace failure. Exit 3 means the requested trigger was observed but
the turn budget was exhausted. This is discovery evidence, not task success.
The summaries count all four outcomes separately; incomplete runs never count as
completed passes. Outcome probes such as negative S1 use 12 turns explicitly. Logs retain
stdout separately from stderr. Trigger success alone does not prove task completion.

Every basic positive trigger has a real Python/Git fixture with matching files.
Plan prompts distinguish requested planning from already-approved inline execution.
The review case uses real commits rather than placeholder SHAs.

The suite includes a negative analysis case on the real S1 correction fixture,
with an artifact check that fails if the agent does nothing. The explicit-request
runner shares the structured trace evaluator; invocation order still needs trace review. Use
[portable scenarios](../tests/codex/fixtures/behavior-prompts.md) for the complete
activation, authorization, documentation, dispatch, and resume matrix.

For executable S1/S8 outcome checks, run:

```bash
python3 tests/skill-triggering/outcome-fixture.py create /tmp/unique-empty-fixture S8
# Run the printed task in that disposable repository with the host under test.
python3 tests/skill-triggering/outcome-fixture.py check /tmp/unique-empty-fixture S8
```

The creator refuses a nonempty destination, initializes a fixture branch, and
prints the task. The checker inspects artifacts independently of the agent report.
S1 checks the exact config and absence of a plan artifact. S8 checks the public
constant, updated existing guide, and its README link. Both assert that the fixture
branch and baseline commit remain unchanged. Review the trace separately
for skill selection, redundant approvals, and authorization compliance. These
small fixtures do not validate the entire workflow or semantic correctness of prose.

Create S2–S7/S9–S12 with `python3 tests/codex/fixtures/make-harness-fixture.py CASE`.
It returns a concrete repository, task prompt, and separate evaluator rubric.
Check required host capabilities before running; inspect each observable assertion
in the resulting trace and artifacts. Creating a fixture does not pass its scenario.

Keep plugin discovery pinned to the tested snapshot, record the actual model and
client, and use separate profiles/workspaces for before/after runs. The scenario
matrix and repetitions in the approved plan remain the full behavioral gate.
Blocked or unavailable live checks are pending, never converted to passing results.

## Evidence

Skill behavior is verified through actual decisions, dispatched agents, executed
commands, test results and artifacts. Grepping skill prose is an inventory aid,
not proof that an agent follows it. Preserve the fork's behavior as the reference:
short decision-level plans, skip flags, conditional plan review, explicit-user
choices, review scope, rulings, visual verification and resume behavior.

Record the plugin commit or working-tree diff, client version, model/effort,
scenario, observed result and any limitations. The current implementation record
is [codex-verification.md](codex-verification.md). A documented test scenario is
not a completed test. Earlier maintainer-reported Claude passes apply to the
upstream-sync commit only until Claude validates this port as well.
