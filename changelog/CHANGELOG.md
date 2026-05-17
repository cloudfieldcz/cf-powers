# Changelog

All notable changes to cf-superpowers will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] — security remediation track

### Security
- Forked from `cloudfieldcz/cf-powers` v1.7.0 for security remediation per
  SSDLC audit v1.1.2 (`docs/audits/SSDLC-Audit-v1.1.2.md`).
- F-00 (CRITICAL): SHA-256 integrity baseline + fail-closed verification for
  `skills/using-superpowers/SKILL.md` in SessionStart hook. Baseline at
  `.claude-plugin/integrity.sha256`; helper `bin/update-integrity`. Tests in
  `tests/integrity/run-test.sh`.

## [Fork baseline] — 2026-05-17

Initial fork point. Identical to upstream `cf-powers@31551ad`.