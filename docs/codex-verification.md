# Codex port verification — 2026-09-14

Version: 2.5.0, based on upstream-sync commit `3ae09eb`.
Release authorized by the maintainer on 2026-09-14; outstanding checks remain
listed below and are not represented as passed.
The maintainer's earlier Claude pass applies to `3ae09eb`. It does not cover
this port. Source policy: preserve cf-powers behavior, adapt runtime mechanics.

## Completed

| Check | Result / evidence |
|---|---|
| Existing offline suites | PASS: sdd-scripts, orchestrator-scripts, systematic-debugging, integrity (positive, tampered and missing-baseline hook behavior). |
| New Codex contracts | PASS: 7 unittest cases; manifests resolve the shared tree, integrity checker is read-only and fails on corruption/missing inputs/utility; both available hash backends exercised. |
| Real native installation | PASS on macOS, Codex CLI 0.154.0: local marketplace install into a temporary CODEX_HOME from a committed snapshot of the working tree. |
| Installed skill/resource discovery | PASS via a fresh App Server: all 20 source skills resolve from the installation cache under cf-powers names; reviewer roles and runtime references match source. |
| Hook suppression | PASS: actual hooks/list returns zero hooks and no errors with Claude hooks/hooks.json present in the installed plugin. |
| Native update | PASS: install a new committed fixture version, restart App Server, verify updated skill bytes, matching integrity and no duplicate skill identities. |
| Upstream coexistence | PASS: installed actual upstream v6.3.0 and cf-powers together in a temporary profile; distinct prefixed skill identities, cf-powers source bytes preserved, zero hooks. Only upstream's local marketplace locator was adapted for the fixture. |
| Metadata | PASS: all 20 skills pass frontmatter validation; native Codex accepts the manifest. |
| Independent review forward-test | PASS in the current Codex agent runtime: clean-context reviewer dispatch with absolute role/template/runtime paths, gpt-6-astra/high. Reviewer catches the fixture's missing out-of-range validation although its two existing tests pass; no source edits. |
| One-task SDD forward-test | PASS in the current Codex agent runtime: clean-context gpt-5.6-sol/medium worker, independent gpt-6-astra/high task and final reviewers. Two regression tests fail before the fix; all four tests pass afterward. Both reviews approve; authorized keep-branch finish and workspace cleanup complete. |
| Port review | One branch-guard regression identified in writing-plans and fixed: retain feature-branch/main restriction while allowing host-provided detached worktrees. No other concrete findings reported by the independent reviewer. |

Reproduce native/offline checks with `bash tests/codex/run-test.sh --native` and
shared suite commands in [testing.md](testing.md). The test profile and Git
repositories are temporary; the user's actual Codex installation/configuration
were not changed. These checks make no authenticated model requests.

For the review forward-test, use `tests/codex/fixtures/make-review-fixture.py`.
The scenario has apply_discount(total, percent), a documented 0..100 range and
passing tests for valid values. Actual reviewer reproduced -1 and 101 returning
values instead of raising ValueError. Only its review report was written.
The evaluator used the source skill paths in a clean Codex subagent context;
this validates execution separately from the native installation test. It is
not a claim that a fresh CLI model session or desktop UI was exercised.

For the SDD scenario, generate the same disposable fixture with `--with-plan`.
The worker implemented range rejection and committed only fixture code/tests
as `c226932717cb29bdab1c3f37659bf2e51b0d2669`. The controller retained
`fixture/review` as authorized, resolved the task review's unchanged-requirement
and branch-state verification warnings, and completed the final review and
finish verification. No fixes were requested by reviewers, so this scenario
does not exercise review fix rounds, escalation, or rulings.

## Validator compatibility

The installed Plugin Creator ingestion validator rejects any `hooks` field.
This repo intentionally retains upstream's `hooks: {}` rather than removing
it: Codex CLI 0.154.0 installs this native manifest successfully, and its actual
App Server reports zero registered hooks. The general validator is therefore
not green; the consumer-specific regression test is authoritative for this
compatibility manifest. No other plugin-validation failures were reported.

## Remaining release validation

- Claude must run the behavior/triggering suites against this changed plugin.
- Fresh CLI model session: implicit skill activation and all four analysis
  review perspectives, preserving user choices and short/conditional planning.
- Full SDD fix-loop escalation, two-unit orchestrator restart, no-subagent and
  restricted-nesting scenarios; helpers passing alone do not prove those flows.
- Model-driven selection with upstream Superpowers installed too; native
  coexistence/discovery itself already passed.
- Desktop UI installation/picker/update. The tested App Server is its backend;
  API-level verification is not a visual UI test.
- Linux native/client verification; Windows and IDE installation are not claimed.

See [tests/codex/README.md](../tests/codex/README.md) for reproducible scenarios.
Do not mark unexecuted scenarios as passed or publish a fully validated release
solely on the offline/install results above.

## Standalone IDE installation follow-up

Version 2.5.1 adds `bin/codex-skills`. On macOS with Codex
0.154.0, an isolated project discovery directory loads all 20 skills through
the symlink with `cf-powers:` identities. Real paths resolve shared reviewer
resources. Repeated install, uninstall preserving source, unrelated directory
and broken-symlink collision checks pass. Run
`python3 -B tests/codex/test_standalone.py` (also included in `--native`).

This verifies the shared discovery backend, not a VS Code UI session or its
subagent availability. The installer defaults to the documented user discovery
directory; the automated test uses the equivalent project-scoped directory to
avoid modifying the user's profile. No normal-profile installation was made.
