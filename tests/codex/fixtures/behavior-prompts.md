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
