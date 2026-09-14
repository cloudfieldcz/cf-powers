# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 2.4.x (Claude Code) | :white_check_mark: |
| 2.5.x (Claude Code + Codex) | :white_check_mark:; validation coverage in [verification record](docs/codex-verification.md) |
| Older releases | Upgrade to a maintained release |

## Reporting a vulnerability

For security issues, please use one of the following channels:

- **GitHub Security Advisories** (preferred):
  https://github.com/cloudfieldcz/cf-powers/security/advisories/new
- **Email:** valda@cloudfield.cz

Please do not file public issues for security-sensitive reports.

## Disclosure timeline

- T+0:  Acknowledge receipt (within 72h)
- T+14: Initial assessment and severity rating
- T+90: Coordinated disclosure window (negotiable)

## Scope

In-scope:

- `hooks/session-start` (SessionStart hook injecting skill content into the
  model session context)
- `bin/update-integrity` and `.claude-plugin/integrity.sha256` (skill
  integrity baseline tooling)
- `skills/*/SKILL.md` (skill content loaded by the agent)
- Plugin manifest files: `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`,
  `.agents/plugins/marketplace.json`
- `bin/check-integrity` (read-only baseline verification)
- Runtime references and reviewer definitions distributed with the plugin

Out-of-scope:

- Upstream Anthropic Claude Code and OpenAI Codex runtimes
- Third-party skills installed by the user outside this plugin
- Issues in the upstream `obra/superpowers` project unless they reproduce in
  this plugin's distributed artifacts

## Threat model (summary)

`hooks/session-start` automatically injects the contents of
`skills/using-superpowers/SKILL.md` into every session's model context as
an `<EXTREMELY_IMPORTANT>` block. The user does not see this content and
does not explicitly invoke it. That makes those files a high-value target
for silent modification — both on disk after install and during the
release pipeline.

The current control (`.claude-plugin/integrity.sha256`, verified by the
hook before injection) is a drift-detection mechanism: it catches
post-install corruption, accidental edits, encoding changes after a
`git pull`, and partial updates. It does **not** defend against an
attacker who can also modify the baseline file in the same checkout — a
fully signed-release model would be required for that, which this plugin
does not yet ship.


## Codex integrity boundary

Codex uses native skill discovery. Its manifest explicitly declares `hooks: {}`
to suppress auto-discovery of the Claude hook. There is no automatic startup
hash check in Codex and installing through a marketplace does not run our
checker. `bin/check-integrity` provides read-only verification for release checks
and troubleshooting; only `bin/update-integrity` refreshes the baseline.

The existing baseline covers `skills/*/SKILL.md`. It does not cover supporting
references, scripts or `agents/*.md`, on either runtime. Do not interpret a green
baseline check as verification of every distributed file or as a signature.
Claude's existing hook and fail-closed injection behavior are unchanged.
