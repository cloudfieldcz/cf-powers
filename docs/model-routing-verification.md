# Model routing verification — 2026-09-19

Release: 2.5.2. Clients: Codex CLI 0.154.0, Claude Code 2.1.274.

## Completed

- Offline suites passed: SDD helpers, orchestrator helpers, systematic debugging,
  integrity hook (positive, tampered and missing baseline), seven Codex contracts.
- Native Codex install/update/resource discovery and standalone install/discovery/
  uninstall/collision tests passed. An initial native identity failure came from
  global standalone skills leaking into discovery despite an isolated CODEX_HOME.
  The test now checks identities across its temporary profile, including stale
  cached versions, while retaining exact installed-path and source-byte checks.
- Claude plugin and marketplace manifests passed `claude plugin validate`.
- Integrity baseline, relative model-policy links, manifest version consistency
  and `git diff --check` passed.
- Clean-context Codex agents retrieved the requested task/model/effort mappings
  from the actual policy. Baseline lacked exact mappings; updated policy covered
  planning, implementation, tests, coordination, diagnosis and review rechecks.
- Independent judgment review and scoped recheck resolved stale escalation and
  unsupported cost claims. Claude exception scenarios covered bulk renames,
  routine review under a Fable parent, difficult cross-system design, repeated
  Opus failure after narrowing, unavailable Fable, repeated Fable failure and
  explicit user choices. No material issues remained.

## Limits

A real Claude CLI policy-retrieval smoke test was attempted with Opus/high,
no tools and no session persistence. It exited before inference with
`Not logged in · Please run /login`. Claude model behavior and actual Fable
account availability/dispatch are therefore not verified. The Codex-hosted
reference checks above are not Claude runtime tests. Full authenticated Claude
behavior/triggering suites and desktop UI checks were not run for this release.
Release publication was explicitly requested by the maintainer; these limits
are recorded rather than represented as passing checks.

The local user's Codex context configuration was changed separately and is not
part of the plugin release.
