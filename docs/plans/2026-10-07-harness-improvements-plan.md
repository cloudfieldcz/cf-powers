# CF Powers — conservative harness improvements

**Status:** Implementation prepared; offline validation passed. Full live behavioral validation remains pending.
**Goal:** Remove activation and handoff conflicts while preserving the proven workflow safeguards.
**Analysis:** [Audit and requirements](2026-10-07-harness-audit.md).
**Baseline:** `81b494e` (2.7.0).

> Execution was authorized by the user on 2026-10-07 and performed inline.
> Release and publication remain outside this task. Live test approval limits are recorded below.

## Global Constraints

- Preserve automatic workflows for complex work; do not make the skill collection explicit-only.
- Keep skill names, hooks, integrity boundary, manifests, model defaults, reviewer tiers, helpers, and ledger formats.
- Preserve TDD, architecture cross-checks, unit/task/final reviews, fix loops, UI checks, and resume behavior.
- Keep the five-layer documentation check; persistent docs must accompany changed documented behavior.
- Honor existing authorization without bypassing new material decisions or project branch policy.
- Apply narrow edits in sequence. Stop expanding scope when a change needs a new policy decision.
- Compare against the restored baseline, not the reverted rewrite. No major-version bump is planned.

## Review Focus

- A mechanical-task exception must not suppress tests, documentation, risk review, or explicit skill requests.
- A complex but fully specified migration still needs coordination.
- Continuing authorization must not turn an analysis-only request into implementation.
- Moving a model lookup must not lower reviewer capability or lose child runtime instructions.
- Uncommitted public changes must update the correct guide, not only the changelog.

### Task 1: Establish behavior fixtures and baseline

- [ ] **Delivers:** Reproducible positive, negative, and safeguard scenarios before instruction edits.
**Files:** `tests/skill-triggering/run-test.sh:47`, `tests/skill-triggering/run-all.sh`,
`tests/skill-triggering/prompts/`, `tests/codex/fixtures/behavior-prompts.md`, `docs/testing.md`.
**Decisions:** Keep trigger detection as one signal. Distinguish timeout/process failure from behavioral failure and successful completion.
Add small disposable outcome fixtures and assertions for the scenario matrix below. Preserve existing suites and their purpose.
**Trap:** A successful Skill call followed by a failed process is not a successful task.
**Verify:** Parser fixtures cover success, failed process, timeout, malformed/missing output, and a false positive from quoted tool text.
Record current behavior on both hosts before claiming an improvement. Unavailable live runs remain explicitly pending.

### Task 2: Resolve activation precedence without changing workflow internals

- [ ] **Delivers:** Ordinary work takes the existing direct path; substantive work still selects the existing workflow automatically.
**Files:** `skills/using-superpowers/SKILL.md:11`, `:24`, `:48`, `:68`;
trigger descriptions in `skills/analysis/SKILL.md:3` and `skills/writing-plans/SKILL.md:3`; `README.md:100`.
**Decisions:** Replace the universal 1% instruction with explicit precedence and observable complexity signals.
Limit edits to routing, descriptions, and conflicting examples. Keep SessionStart and all downstream workflow bodies.
**Trap:** "User specified exactly what to do" can describe a large migration; it removes design uncertainty, not coordination needs.
**Verify:** S1–S4 below, including implicit activation on both hosts and unchanged explicit skill invocation.

### Task 3: Preserve authorization and finish documentation within scope

- [ ] **Delivers:** Approved work continues; required docs reach their persistent destination without redundant permission prompts.
**Files:** `skills/analysis/SKILL.md:39`, `:65`, `:82`, `:374`;
`skills/writing-plans/SKILL.md:217`; `skills/documenting-changes/SKILL.md:14`, `:31`, `:55`, `:68`;
`skills/finishing-a-development-branch/SKILL.md:42`, `:66`; relevant command descriptions under `commands/`.
**Decisions:** Reuse existing approval only when its design, scope, and execution choice match.
Keep questions for unresolved material decisions. Keep external/destructive authorization separate.
Preserve UPDATE/CREATE/SKIP and all five doc layers. Include committed, staged, unstaged, and untracked delivery scope.
Prefer an existing `docs/` guide; create and link a new guide when needed, respecting repository conventions.
**Trap:** A top-level exception is insufficient if examples and finishing prompts still command an unconditional stop.
**Verify:** S5–S9 below. A missing required guide stays a documented gap; a user can explicitly defer it.

### Task 4: Reduce irrelevant runtime loading while preserving model policy

- [ ] **Delivers:** Inline work avoids inapplicable model setup; real dispatch still carries all required policy and context.
**Files:** `skills/using-superpowers/references/runtime.md:7`, `codex-tools.md:23`, `claude-code-tools.md:1`
(the latter two share the same reference directory); runtime preambles in affected skills;
`skills/choosing-subagent-models/SKILL.md:3`, `:8`; only affected dispatch template preambles.
**Decisions:** Make model policy loading conditional on a supported selection/dispatch operation.
Keep existing model recommendations and reviewer tiers. Load the active host reference once per context when required.
Keep absolute resource paths, project instructions, lifecycle mapping, capacity checks, and capability fallback available to children.
**Trap:** Removing a parent lookup must not remove a child's constraints or silently permit a lower-tier review.
**Verify:** S10–S12. Inspect actual selected models, inherited context, calls, and review artifacts; do not infer them from template prose.

### Task 5: Review, document, and validate the combined change

- [ ] **Delivers:** Small reviewed patch with accurate user docs and evidence for each preserved safeguard.
**Files:** `README.md:100`, `docs/testing.md`, `docs/codex-verification.md`, `CHANGELOG.md`,
`.claude-plugin/integrity.sha256`; changed skill references and templates identified by Tasks 2–4.
**Decisions:** Fix README's route, language, and reviewer drift. Keep installation and security behavior unchanged.
Refresh integrity after final skill edits. Release/version changes belong to a separately authorized release.
**Verify:** Run the commands below and an independent review of the combined diff, including linked templates.
Resolve material findings and verify fixes. Record remaining client/UI/behavior limits explicitly.

## Scenario matrix

| ID | Input | Required evidence |
|---|---|---|
| S1 | Known one-line config correction | Direct change, relevant verification, no analysis artifact |
| S2 | Explicit analysis or TDD request | Requested workflow retained, including its safeguards |
| S3 | Fully specified dependent migration, no skill name | Automatic coordination, ownership, ledger, integrated review |
| S4 | Small new authorization boundary | Analysis/review retained despite small diff |
| S5 | Approved design and chosen inline execution | Continue without repeat approval; final independent review remains |
| S6 | Analysis only | Design and current architecture cross-check; no implementation |
| S7 | Newly discovered breaking API choice | Surface the decision; prior authorization is not expanded |
| S8 | Uncommitted public config change | Existing docs guide updated, examples correct, no doc-only permission loop |
| S9 | New documented capability or internal-only fix | Linked new docs page for the former; accurate SKIP reason for the latter |
| S10 | Inline task without model-selection capability | No irrelevant selection attempt; no invented override |
| S11 | Delegated task, occupied slots, and scoped fix | Current model policy, bounded capacity, correct resume, review evidence |
| S12 | Interrupted run or missing subagents | No repeated completed work; unmet independent review reported honestly |

Use the same fixtures and models for before/after comparisons. Repeat each changed behavior at least three times per host.
All safeguard scenarios must pass. Report quality first, then interventions, tool calls, loaded context, latency, and tokens when available.
No efficiency claim is valid without comparable measurements. A skipped run is not a pass.
If a host is unavailable, keep the candidate as a reviewable draft and leave Task 5's behavioral validation incomplete.
Report passing offline checks separately. Complete authorized live checks before declaring the candidate validated for both hosts.

## Plan review

An independent read-only reviewer checked the audit and plan against the baseline on 2026-10-07.
The reviewer approved the plan with no must-fix findings. Two clarifications were incorporated:
the existing CREATE rule already requires a documentation link, and unavailable live checks leave behavioral validation incomplete.
This review validates the proposal; it does not validate future implementation or model behavior.

## Verification and rollout

Run these helper suites:

```bash
bash tests/sdd-scripts/run-test.sh
bash tests/executing-plans-scripts/run-test.sh
bash tests/orchestrator-scripts/run-test.sh
bash tests/systematic-debugging/run-test.sh
```

Run `bash tests/integrity/run-test.sh` separately from skill edits; it temporarily changes tracked fixtures.
Run `bash tests/codex/run-test.sh --native` and the affected Claude behavior suites documented in `docs/testing.md`.
Use disposable repositories and isolated profiles; never alter the user's global settings for an evaluation.

Tasks are sequential because their assertions and routing rules overlap. Keep each task's diff reviewable and separately reversible.
If a candidate weakens a safeguard or misses a complex trigger, revise or revert that candidate before continuing.
Do not merge skills, remove hooks, relax review gates, or replace model policy as part of this plan.


## Implementation handoff — 2026-10-07

Implementation changes are prepared on `feat/conservative-harness-improvements`.
Completion boxes remain open until the full live acceptance gate is satisfied.

The first static review missed an implicit-TDD regression later demonstrated by
the external Claude audit. Follow-up changes now distinguish work-method triggers
from size-based planning, retain TDD for code/refactors, and require approval of
the specific design. The basic Claude runners now use real repositories and an
isolated config, and report INFRA and incomplete-trigger outcomes separately.

The user authorized live Codex payload transfer. The six S1/S8 comparison runs
passed, and targeted follow-up implicit TDD passed 3/3 on Codex. Broader probes
also recorded limitations; they are not a full matrix pass. The Claude recheck
must use the new isolated runner and repeated baseline/candidate trials.

See [verification record](../codex-verification.md) for exact coverage and limits.
No release, version bump, merge, or publication was performed.
