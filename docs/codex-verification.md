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


## Conservative harness candidate — 2026-10-07

Source baseline: `81b494e` (2.7.0). Changes remain uncommitted on
`feat/conservative-harness-improvements`. No release or version bump was made.

### Before the external Claude audit

The first candidate passed offline checks and independent static review. Those
checks did not detect the later observed implicit-TDD regression on Claude.
The user subsequently authorized live Codex tests with the current skill contents.
The earlier automatic approval rejection no longer blocks these Codex runs.

Codex CLI 0.160.1 used separate temporary profiles, project-scoped skill snapshots,
and requested model `gpt-6-sol`. Results below describe that pre-follow-up snapshot:

| Case | Observed evidence | Limit |
|---|---|---|
| S1 config | Candidate 3/3 and baseline 3/3; correct edit, no plan, no commits | Small sample; no efficiency claim |
| S8 existing guide | Candidate 3/3 and baseline 3/3; code and guide updated | Does not test implicit TDD for new logic |
| S2 explicit TDD | Skill read, failing regression, implementation, passing tests | One run; explicit request only |
| S2-analysis / S4 | Design advice without application edits | One run each |
| S3 small migration | Correct integrated behavior; no durable plan or independent review | Same omission on baseline; coordination gate not satisfied |
| S5 approved inline | Continued without repeat approval; actual independent reviewer on gpt-6-sol/high; review finding fixed | One run; baseline also completed |
| S6 architecture | Design and four actual review agents; no application edits | First run timed out at 300 s; retry completed in 493 s |
| S7 discovered consumer | Preserved legacy calls after new consumer evidence | Local commit remained blocked after resume |
| S9 public / internal | Linked docs guide for new capability; existing docs retained for internal refactor | One run each |
| S11 resume | Same diagnostic worker resumed; gpt-6-sol/high metadata; scoped feedback | Capacity/complete workflow coverage is not established by one run |
| S12 resume | Kept completed unit and finished pending code | One candidate and baseline run omitted independent review |
| S12 without agents | With agents.enabled=false, reported unavailable review and self-review | Still called unit complete; full review-gate contract is not established |

An initial attempt to disable agents with the old `multi_agent` feature flag
still exposed agents. That attempt does not count as a no-agent test. The corrected
run used `agents.enabled=false` with strict configuration validation. S10 with that
configuration fixed the typo without loading model-selection guidance.

Raw trace locations and snapshot paths are retained in the local implementation
ledger. These observations do not constitute a complete S1–S12 acceptance pass.

### External Claude audit and follow-up

The maintainer supplied a Claude Code 2.1.292 audit using the same new runners on
baseline and candidate. Its single-run trigger totals were 6/8 and 1/8 respectively.
Those totals combine fixture failures and timeouts, so they are not a task-quality
score. The email-validator trace nevertheless proves a concrete regression:
baseline loaded TDD before implementation; candidate wrote production code before
tests and never loaded TDD. This invalidates the earlier static-review confidence.

The follow-up separates work-method selection from size-based design/planning.
Production-code development and refactoring retain TDD. The analysis handoff now
requires approval of the concrete design; the prior English default is restored.
Test fixes add real repositories, isolated basic Claude profiles, separate INFRA
and INCOMPLETE results, and checks that survive Python optimization.

Three fresh Codex trials of the implicit email-validator request loaded TDD before
production edits, observed a failing test, then implemented and passed the tests.
Their snapshot precedes only the final clarification that code refactors also
select TDD. This is targeted Codex evidence, not a repeated Claude comparison.
Raw traces: `cf-auto-tdd-8slv02hy/{1,2,3}/trace.jsonl` in the local temporary root.
A subsequent current-snapshot S1 run passed 3/3 artifact checks without loading
analysis or TDD; traces are under `cf-live-routing-followup-eq3xgsa5`.

### Current local checks and remaining gate

- Trace evaluator/wrapper regressions: 12 tests.
- Outcome checker regressions: 6 tests, including optimized Python and historical default prose.
- Fixture preparation/isolation/summary checks: 3 tests.
- Integrity and Codex offline/native install/update/standalone checks passed after the skill edits.
- Hooks, manifests, model tables, core TDD and execution/review loops remain preserved.

The latest changes still need an isolated Claude before/after comparison with at
least three repetitions, plus remaining full-matrix assertions on both hosts.
The older specialized multi-turn and SDD integration scripts remain legacy tests,
not proof of the new runner isolation contract. The second session performs audit
only; this session owns edits. Do not mark the complete behavioral gate passed.
