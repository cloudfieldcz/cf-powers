# Codex verification

## Automated checks

From the plugin root:

```bash
bash tests/codex/run-test.sh
bash tests/codex/run-test.sh --native
```

The offline suite validates marketplace/resource contracts and runs the integrity
checker on matching, tampered, missing-file, missing-baseline and missing-utility
fixtures. It verifies both available hash backends and that checks do not mutate
files. Requires Bash and Python 3.9+.

`--native` additionally requires Codex CLI (tested on 0.154.0). It copies the
working tree into a committed temporary marketplace, installs with a temporary
CODEX_HOME, and asks a fresh App Server for `skills/list` and `hooks/list`.
It checks all source skills, role/reference resources, identity uniqueness and
zero hooks, then installs an updated committed fixture and checks again. It
makes no model requests and never installs into your real profile. This tests
the desktop's backend API, not the desktop UI.

The shared Plugin Creator validator currently rejects the `hooks` field. We
retain `hooks: {}` intentionally, as upstream v6.3.0 does; native installation
and hooks/list verify the actual consumer accepts it and suppresses auto-discovery.
Do not remove the field just to satisfy that unrelated ingestion validator.

## Behavioral checks

These need actual model sessions. Claude runs its own regression tests; do not
interpret the earlier upstream-sync test pass as a pass for this Codex port.
Run Codex checks in fresh sessions with the installed plugin. Record the client
version, plugin version and source commit/diff, selected model/effort, actual
calls and report paths. Keep fixtures disposable; do not publish anything.

Create a deterministic review fixture:

```bash
python3 tests/codex/fixtures/make-review-fixture.py
```

It prints a disposable repository, base and head SHAs. Ask Codex to use
`cf-powers:requesting-code-review` on that range against requirements.md, without
fixing it. The reviewer must independently notice missing rejection of percentages
outside 0–100, despite the valid-input tests passing. Source files stay unchanged.
Use `--with-plan` to also create plan.md for an SDD implementation scenario.
Then run cf-powers:subagent-driven-development on that absolute plan path, with
the explicit instruction to retain the branch and not push/publish. Use a fresh
fixture so the implementation reviewer does not inherit a previous verdict.

Use these additional scenarios (acceptance is behavior, not exact wording):

| Scenario | Expected evidence |
|---|---|
| Plain bug report | Appropriate installed cf-powers skill loads without manual bootstrap. |
| Direct analysis | Runtime reference loads; BA/dev/security/performance reviewers return their own reports, queueing within capacity. |
| Direct plan request | Decision-level plan; conditional review; no implementation for a plan-only request. |
| Already-authorized execution | Preserves chosen method/order without asking for the same permission again. |
| SDD repair | Same worker identity receives a turn-triggering follow-up and appends covering tests before re-review. |
| Orchestrator restart | Two units run sequentially; after restarting following unit 1, only unit 2 is dispatched. |
| Reduced capability | No unsupported call; independent review explicitly unavailable; preserve unreviewed artifacts. |
| Limited nesting | Parent runs SDD controller loop when another controller would exhaust the slots. |
| Model override | User's choice is retained; Codex never receives an Anthropic alias or a tier label as model ID. |
| Git state | Feature branch, existing worktree and detached HEAD retain user work and valid handoff. |
| Coexistence | With upstream Superpowers installed too, cf-powers invocations resolve this plugin's own files. |
| Desktop UI | Plugin and skills appear after native installation/restart; verify update in the actual App UI. |

See [the current verification record](../../docs/codex-verification.md) for the
checks actually performed. A documented scenario is not a passing result.

Standalone discovery: `python3 -B tests/codex/test_standalone.py` exercises the
installer with a temporary project discovery directory and fresh App Server.
It checks all source skills, role resolution, repeat install, uninstall and
collision protection. This is included in `run-test.sh --native`; it does not
claim visual verification inside VS Code.
