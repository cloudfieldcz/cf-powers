# Changelog

All notable changes to cf-powers will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.8.0] — 2026-05-18

### Added
- SHA-256 integrity baseline for every `skills/*/SKILL.md` file
  (`.claude-plugin/integrity.sha256`).
- `bin/update-integrity` helper that regenerates the baseline by
  discovering every `skills/<name>/SKILL.md` and hashing it.
- `tests/integrity/run-test.sh` covering positive, tampered, and
  missing-baseline paths.
- `SECURITY.md` describing the supported versions, reporting channel,
  scope, and threat model.

### Changed
- `hooks/session-start` now verifies the integrity baseline before
  injecting `using-superpowers/SKILL.md` into the session context. On any
  failure (missing baseline, mismatched hash, no hash utility) the hook
  emits a `<security-alert>` block instead of injecting unverified skill
  content (fail-closed).
- Release procedure documented in [README.md](README.md#releasing): the
  baseline must be regenerated before bumping the version.

## [1.7.0] — 2026-05-17

Last release before the integrity baseline work. See git history for
prior changes.
