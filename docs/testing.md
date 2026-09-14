# Testing CF Powers

## Offline checks

Run from the repository root:

```bash
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

Claude executes these tests against the working-tree plugin via `--plugin-dir`,
per the maintainer's instruction. Run from an authenticated Claude environment:

```bash
bash tests/claude-code/run-skill-tests.sh
bash tests/skill-triggering/run-all.sh
bash tests/explicit-skill-requests/run-all.sh
```

The full SDD implementation integration is slower and optional for ordinary
edits, but needed when changing the actual implementation/review lifecycle:

```bash
bash tests/claude-code/run-skill-tests.sh --integration
```

Tests use real model sessions and can incur usage. Do not run authenticated
Claude tests through another agent without the required authorization. An old
installed version or a previous commit's green result does not verify new skills.

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
