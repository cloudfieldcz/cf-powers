# CF Powers — conservative harness audit

**Baseline:** `81b494e`, version 2.7.0, clean working tree before this audit.
**Date:** 2026-10-07.
**Scope:** Audit and planning only. The earlier broad rewrite was reverted.
**Next:** [Implementation plan](2026-10-07-harness-improvements-plan.md).

## Outcome and constraints

Preserve the proven Superpowers workflows while removing instruction conflicts and redundant host setup.
Complex work must still activate workflows automatically. Explicit invocation remains available.
The user requested smaller changes and concrete safeguards, including persistent documentation in `docs/`.

This audit proposes incremental edits, not a replacement framework or a new major release.
It does not establish that shorter skills improve correctness, latency, or token use.

## Method and evidence limits

Inspect entry skills, execution handoffs, runtime adapters, documentation rules, hooks, and relevant tests.
Treat contradictions as static findings. Treat their possible effect on model behavior as a hypothesis until tested.
Do not reuse results from the reverted rewrite as evidence for this baseline.

Checks run against this baseline:
- `bash bin/check-integrity`: passed.
- `bash tests/codex/run-test.sh`: seven offline tests passed.

No fresh live Claude/Codex behavioral comparison or desktop/IDE validation ran during this audit.
No runtime files, skills, hooks, manifests, or model defaults were changed.

## Findings

### F1 — Activation rules conflict

**Evidence:** `skills/using-superpowers/SKILL.md:11`, `:24`, `:48`, `:62`, and `:68`.
The skill requires invocation at a 1% relevance threshold and before exploration.
Its Skip Flags permit direct edits and read-only exploration. Generic priority examples can select analysis or debugging again.
`skills/analysis/SKILL.md:3` and `skills/writing-plans/SKILL.md:3` already contain mechanical-task exclusions.

**Proposal:** Establish one precedence order: explicit user/project instruction, substantive workflow trigger, then mechanical-task exception.
An exception skips irrelevant process, not tests, documentation, or a requested workflow.
Judge complexity by unresolved decisions, dependency coordination, and risk; file count alone is insufficient.
Keep automatic discovery, the Claude startup hook, and the existing skills.

**Preserve:** Automatic analysis for unresolved design, debugging discipline, and explicit skill requests.
**Validate:** A known config fix stays direct; a specified multi-unit migration still receives coordination without a skill name.

### F2 — Authorization continuity is inconsistent

**Evidence:** `skills/analysis/SKILL.md:39`, `:65`; `skills/writing-plans/SKILL.md:222`, `:227`, `:233`.
Analysis requires a new approval on every path. Planning says to preserve authorization, then presents mandatory-looking choice prompts.
`skills/finishing-a-development-branch/SKILL.md:68` and `:80` require a fixed integration menu even when a choice may already exist.

**Proposal:** Honor approval already given for the same concrete design, execution mode, and scope.
A broad implementation request does not settle newly discovered product decisions or compatibility tradeoffs.
Ask when an unresolved material decision requires the user; do not repeat a choice already supplied.
Use dependency order when it unambiguously determines the next phase.

**Preserve:** Design validation, analysis-only boundaries, project branch policy, and authorization for destructive or external actions.
**Validate:** Approved plan plus chosen inline execution continues; analysis-only requests stop; new breaking contracts still surface a decision.

### F3 — Documentation can stall or miss the actual change

**Evidence:** `skills/documenting-changes/SKILL.md:14`, `:31`, `:43`, `:68`, `:90`;
`skills/finishing-a-development-branch/SKILL.md:42`.
The five-layer inventory is useful. The unconditional now/defer/skip question adds a separate stop for routine documentation work.
The example `git diff <base>...HEAD` covers committed work, not staged, unstaged, or untracked changes.
The CREATE rule already requires an index/README link at `skills/documenting-changes/SKILL.md:63`.
It does not explicitly prefer an existing guide as the source of truth before creating a new page.

**Proposal:** Keep all five layers and UPDATE/CREATE/SKIP decisions.
Inspect the actual delivery scope, including uncommitted files when present.
Perform required documentation updates within existing implementation authorization.
Update the existing guide in `docs/`; create and link a document only when no suitable guide exists.
Honor another documentation system when the repository explicitly uses one.
User-requested deferral remains possible and must be recorded. Never silently substitute chat or changelog for the guide.

**Preserve:** Automatic documentation checks, inline contracts, changelog conventions, and explicit omission reasons.
**Validate:** A new config option updates the guide before any commit; an internal fix needs no invented page.

### F4 — Runtime routing includes avoidable policy loading

**Evidence:** `skills/using-superpowers/references/runtime.md:7`;
`skills/using-superpowers/references/codex-tools.md:28`;
`skills/analysis/SKILL.md:8`, `:10`; `skills/writing-plans/SKILL.md:8`, `:10`.
Entry skills require runtime references before host operations. The Codex adapter routes inline work through model-selection guidance.
The adapter already has sound lifecycle handling at `codex-tools.md:43`, capacity handling at `:56`, and fallback handling in `runtime.md:33`.
The model policy already states that it cannot switch an unsupported current session model.

**Proposal:** Separate dispatch-time model selection from inline work where no model-selection operation exists.
Load the active-host reference once per context when a host-specific operation needs it.
Keep a short entry-point reminder of project instructions and resource resolution; do not require a full adapter before ordinary file reads.
Children must still receive required runtime constraints and absolute resources.

**Preserve:** Existing model IDs, reviewer judgment tier, explicit user overrides, clean briefs, bounded waits, capacity limits, and honest fallback.
**Validate:** Inline work avoids irrelevant model lookup; actual dispatch still follows the existing model policy and supported tool schema.
**Limit:** Expected context savings are unmeasured. Do not introduce new native agent registration or global settings in this patch.

### F5 — Trigger tests do not establish successful outcomes

**Evidence:** `tests/skill-triggering/run-test.sh:47` and `:59`; `docs/testing.md:55`;
`tests/codex/fixtures/behavior-prompts.md:1`.
The trigger runner tolerates process failure and can pass after detecting a skill call in the log.
That is useful discovery evidence, but it cannot prove completion or preserved safeguards.
Existing portable scenarios cover review, plan-only, authorized handoff, resume, and unavailable subagents.

**Proposal:** Retain these suites. Add outcome assertions, negative-trigger cases, and explicit infrastructure-failure reporting.
Use the same fixtures on both hosts. Record correctness and safeguards before comparing overhead.
Do not describe a written scenario, static text check, or successful install as a live behavioral pass.

### F6 — README describes older behavior

**Evidence:** `README.md:102` and `:112` versus `skills/analysis/SKILL.md:23`, `:46`, and `:286`.
README says every feature starts identically, describes Czech output, and names only BA/Developer cross-checks.
The skill has three routes, specifies English artifacts, and requires four architecture reviewers.

**Proposal:** Correct the guide to match the preserved workflow, including small-task exclusions and the four-reviewer architecture path.
Keep conversation language subject to user instructions. Record implementation-era changes in the changelog when they land.

## Safeguards that stay

| Safeguard | Current source | Decision |
|---|---|---|
| Design routes and architecture cross-check | `skills/analysis/SKILL.md:46`, `:286` | Preserve |
| Decision-level plans, exact interfaces, Review Focus | `skills/writing-plans/SKILL.md:98`, `:130`, `:186` | Preserve |
| TDD and required suite checks | `skills/test-driven-development/SKILL.md`; execution workflows | Preserve |
| Task review, scoped fixes, bounded escalation, final review | `skills/subagent-driven-development/SKILL.md:291`, `:378`, `:453` | Preserve |
| Inline final independent review | `skills/executing-plans/SKILL.md:161` | Preserve |
| Unit ownership, one writer, unit/final review | `skills/orchestrator/SKILL.md:155`, `:174`, `:192`, `:262` | Preserve |
| Durable identity, resume, rulings, helper formats | SDD/execution/orchestrator ledgers and scripts | Preserve |
| Five-layer documentation inventory | `skills/documenting-changes/SKILL.md:43` | Preserve and close gaps |
| Visual evidence and honest verification | `skills/verification-before-completion/SKILL.md:43` | Preserve |
| Integrity boundary and installation routes | `hooks/session-start`, `SECURITY.md`, manifests | Preserve |

## Alternatives and recommendation

1. **Recommended:** Resolve F1–F6 through small, independently measured edits. Keep workflow internals and native adapters largely intact.
2. **Documentation only:** Correct README and add tests first. Lowest behavior risk, but existing instruction conflicts remain.
3. **Broad rewrite:** Consolidate skills, remove bootstrap, replace model policy, or reduce reviews. Defer; current evidence does not justify it.

A later progressive-disclosure experiment may move one self-contained reference after tracing actual loading.
Do not move every checklist or orphan existing worker/reviewer templates. No target line-count reduction is required.

## External guidance

OpenAI recommends specific triggers and progressive disclosure, and warns against excessive recipes.
This supports contextual loading; it does not establish that CF Powers' safeguards should be removed.
See [OpenAI guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

Both hosts document native subagents and configuration. Local adapter behavior still depends on exposed capabilities and client versions.
See [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and
[Claude subagents](https://code.claude.com/docs/en/sub-agents).
