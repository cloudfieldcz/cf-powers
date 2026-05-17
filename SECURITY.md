# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.7.x   | :white_check_mark: |
| < 1.7   | :x:       |

## Reporting a vulnerability

Tento projekt je fork pre účely SSDLC remediácie. Pre reportovanie
zraniteľnosti:

- **Email:** <doplniť bezpečnostný kontakt>
- **GitHub Security Advisories:** povolené pre tento repo
  (https://github.com/qb-bp/cf-superpowers/security/advisories/new)
- **Encryption:** PGP key fingerprint <doplniť alebo odstrániť>

## Disclosure timeline

- T+0: Acknowledge receipt (do 72h)
- T+14: Initial assessment + severity rating
- T+90: Coordinated disclosure window (negotiable)
- Hall of Fame: opt-in pre reportujúcich

## Scope

In-scope:
- `lib/skills-core.js` a jeho subroutines
- `hooks/` adresár (SessionStart hook + helper scripts)
- `skills/*/SKILL.md` integrity / prompt injection patterns
- Plugin manifest (`.claude-plugin/*.json`) parsing

Out-of-scope:
- Upstream Anthropic Claude Code runtime
- Third-party skills nainštalované používateľom mimo tento plugin

## Threat model

Skrátená verzia: `docs/security-model.md` (TBD per remediation 30-8).

## Known security gaps

Sledované v `docs/audits/SSDLC-Audit-v1.1.2.md`. Status v
`docs/remediation/README.md`.