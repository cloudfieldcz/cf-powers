# Upstream Sync v6.0.3 → v6.2.0 — Plan Index

**Source:** Comparison of `obra/superpowers` v6.0.3 (our last sync, cf-powers v2.0.0)
against v6.2.0 (upstream HEAD, commit `3dcbd5c`, released 2026-07-23).

**Created:** 2026-07-25

**Scope decision:** No new skills or agents appeared upstream in this range — the
`SKILL.md` set is byte-identical between v6.0.3 and v6.2.0, and upstream still has no
`agents/` or `commands/` directories. This sync therefore adopts **fixes and skill-content
improvements only**, in four tiers of increasing effort, plus a release phase.

## Phases

| # | Phase | Plan File | Status | Dependencies |
|---|-------|-----------|--------|--------------|
| 1 | Bug fixes (T1) | [plan-1-bugfixes.md](./2026-07-25-upstream-sync-v6.2.0-plan-1-bugfixes.md) | ⬚ Not started | — |
| 2 | Test guidance + discard menu (T2) | [plan-2-content.md](./2026-07-25-upstream-sync-v6.2.0-plan-2-content.md) | ⬚ Not started | — |
| 3 | Compression sweep (T3) | [plan-3-compression.md](./2026-07-25-upstream-sync-v6.2.0-plan-3-compression.md) | ⬚ Not started | — |
| 4 | SDD restructure (T4) | [plan-4-sdd.md](./2026-07-25-upstream-sync-v6.2.0-plan-4-sdd.md) | ⬚ Not started | — |
| 5 | Release | [plan-5-release.md](./2026-07-25-upstream-sync-v6.2.0-plan-5-release.md) | ⬚ Not started | Phases 1-4 |

**Status legend:** ⬚ Not started · 🔨 In progress · ✅ Complete · ⏸ Blocked

## Notes

- Phases 1-4 touch disjoint file sets and have no dependency between them — they can be
  executed in any order or in parallel. Phase 5 must run last: it regenerates the
  SHA-256 integrity baseline over every `skills/*/SKILL.md`, so any earlier phase that
  lands after it invalidates the baseline.
- **`tests/integrity/run-test.sh` will fail from the first `SKILL.md` edit until Phase 5
  regenerates the baseline.** This is expected, not a regression. Every other test suite
  must stay green throughout.
- Phase 4 changes the signatures of all three SDD helper scripts (`review-package` gains
  a leading `PLAN_FILE` argument). That is a breaking change for anyone invoking them
  directly, which is what makes this release a major version bump.

## Upstream reference

The phases cite upstream files verbatim. To recreate the reference checkout:

```bash
git clone https://github.com/obra/superpowers.git /tmp/superpowers-v6.2.0
git -C /tmp/superpowers-v6.2.0 checkout v6.2.0
```

Phase files refer to this checkout as `$UPSTREAM`.
