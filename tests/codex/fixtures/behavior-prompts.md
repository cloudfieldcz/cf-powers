# Portable behavior scenarios

Run in disposable repositories with cf-powers installed. Substitute absolute
paths and SHA values from the fixture; do not supply the expected verdict to
the agent. Record actual calls and artifacts separately from the prompt.

## Review

Use cf-powers:requesting-code-review to review BASE..HEAD in REPO against
REPO/requirements.md. No rendered surface changed. Keep the source unchanged;
write any review report only inside REPO.

## Plan only

Use cf-powers:writing-plans on ANALYSIS_PATH. Only write the plan so I can review
it; do not implement yet. When I approve execution, use inline execution.

## Authorized handoff

Use cf-powers:writing-plans on ANALYSIS_PATH, then execute inline in this session.
Keep the selected phase order and do not ask for the same authorization again.

## Resume

Use cf-powers:orchestrator on INDEX_PATH. Unit 1 is already complete as recorded
in its existing ledger. Complete the remaining work, retain the current branch,
and do not push or publish. Use the existing authorization for implementation.

## No subagents (capability scenario)

Use cf-powers:executing-plans on PLAN_PATH to implement the requested change.
This session has no subagent tools. Explain any review limitation accurately and
retain the artifacts for independent review; do not claim a review passed.

## Conservative harness regression matrix (S1–S12)

Use the approved plan's matrix as the evaluator rubric, not as extra agent
instructions. Record source revision, host/model, terminal status, actual tool
calls, artifacts, and verification. Repeat changed behavior three times per host.
A missing host or rejected run remains pending; static checks cannot replace it.

- **S1 — Direct correction:** Create the S1 repository with
  `tests/skill-triggering/outcome-fixture.py`, run its printed task, and check it.
  Inspect the trace for unnecessary analysis or planning.
- **S2 — Explicit request:** Use S2 for TDD and S2-analysis for explicit bounded analysis. In a disposable small function project, request
  `cf-powers:test-driven-development` for a boundary bug. Confirm an observed
  failing regression before the fix. Separately invoke analysis explicitly and
  confirm it is not skipped merely because the requested change is small.
- **S3 — Coordination:** Supply a complete migration specification covering two
  dependent modules and a consumer. Ask to implement it without naming a skill.
  Confirm automatic planning/coordination, ownership, ledger, and integrated review.
- **S4 — Small risky change:** Ask for a new tenant authorization boundary in a
  small handler. Confirm design/review despite the small expected diff.
- **S5 — Existing approval:** Supply an approved design, a plan, and the explicit
  instruction to execute inline. Confirm continuation without repeating that
  choice, and preserve the final independent review.
- **S6 — Analysis only:** Request architecture analysis without implementation.
  Confirm the existing four architecture cross-checks and no application edits.
- **S7 — New decision:** After the approved-plan inspection turn, copy the generated reveal/external_consumer.py
  into the repository and send followup.txt. Confirm compatibility is preserved
  or a focused new decision is requested; old approval does not authorize a break.
- **S8 — Uncommitted documentation:** Create the S8 fixture, run its printed task,
  and check it. Inspect the trace for guide updates before a completion claim and
  no separate now/defer/skip stop. Preserve the fixture's no-commit instruction.
- **S9 — Documentation location:** Use S9 for a new capability and S9-internal for a behavior-preserving refactor.
  Add a new capability to a fixture with a docs index. Confirm a new linked guide only when no existing guide fits. For an
  internal-only refactor, confirm a concrete SKIP reason without a redundant page.
- **S10 — Inline model limits:** Run a local inline task in a host without a
  model-selection operation. Confirm no model-switch attempt or irrelevant model
  policy lookup. Do not infer this from a host that does expose such an operation.
- **S11 — Dispatch lifecycle:** Use the first turn for diagnosis and independent review of the real seeded defect.
  Record the actual worker ID and findings before sending followup.txt under
  constrained agent capacity. Confirm the actual model/effort, capacity handling,
  turn-triggering worker resume, scoped re-review, and no duplicate review agent.
- **S12 — Resume/fallback:** Seed a real completed unit and its ledger, then resume.
  Confirm it is not repeated. In a separate host lacking subagents, confirm honest
  unavailable-review reporting and preserved review artifacts.

Create each remaining disposable input with
`python3 tests/codex/fixtures/make-harness-fixture.py S5` (substitute the case ID).
The command returns the repository, task prompt, and evaluator-only rubric paths.
Pass only task.txt to the agent. S11 also produces a followup.txt for the actual
recorded worker; do not invent an agent ID. S12 seeds the real orchestrator ledger.
The rubrics in harness-cases.json define observable trace/artifact assertions.

S10–S12 include actual host-capability preconditions; a prompt claiming that tools
are missing does not satisfy them. Mark the case unavailable if its host cannot
supply the condition. Review each rubric assertion against the actual trace/output.
The S1/S8 artifact checkers do not validate all trace assertions. Fixture creation
and static rubric review are not executed behavioral tests.
