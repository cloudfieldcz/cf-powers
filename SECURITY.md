# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.7.x   | :white_check_mark: |
| < 1.7   | :x:       |

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
  `.claude-plugin/marketplace.json`

Out-of-scope:

- Upstream Anthropic Claude Code runtime
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
