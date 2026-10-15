# Collaboration probe evidence — 2026-10-15

Base: `072fa00dc3b119a3ce3b8dad8821bd1e05ab58ad`.
Candidate: the uncommitted maintainer-guidance change based on that commit.
Host: Codex App exposed collaboration agents; CLI discovery was not exercised.
Model: `gpt-6-sol`, high reasoning, for both baseline and candidate.

Two clean-context agents read the actual skill files before producing responses.
Each agent handled several scenarios in one context. The five clarification variants
are wording probes, not five isolated statistical repetitions. No application ran.
The parent manually inspected all outputs. Prompts and expectations are in
[collaboration-scenarios.md](collaboration-scenarios.md).

## Baseline finding

All five clarification responses presented choices without an explicit working hypothesis.
They also classified the hypothetical broader scope as architectural before clarification.
The CSV, minimal-control, and authorization/vault scenarios already produced acceptable
recommendations. Their candidate runs check preservation, not a newly fixed failure.

## Actual clarification outputs

### Daily report

Baseline:
> I’m treating this as architectural for now because a global report would cross the current account boundary. Existing reports are account-bound. Should each account receive its own daily report, or should one report aggregate all accounts?

Candidate:
> I’m provisionally treating the daily report as account-bound because the existing reports are. Should it cover one account or all accounts? That answer determines the query scope and whether broader authorization is needed.

### Export

Baseline:
> I’m treating this as architectural for now because exporting everyone’s records would cross the current ownership boundary. Existing exports are scoped to the caller’s records. Should this export include only the caller’s records, or all records?

Candidate:
> I’m provisionally treating the export as limited to the requester’s own data, matching the current code. Should it export only their data or all data? The answer changes the data selection and required authorization.

### Notification

Baseline:
> I’m treating this as architectural for now because team delivery would change the current recipient boundary. Existing notifications are per user. Should each user receive their own notification, or should one notification go to the team?

Candidate:
> I’m provisionally treating the notification as going to one user, matching the current code. Should it go only to that user or to the whole team? The answer changes recipient selection and permission checks.

### Archive

Baseline:
> I’m treating this as architectural for now because an archive across projects would change the current project boundary. Existing archives are per project. Should this archive contain one project or all projects?

Candidate:
> I’m provisionally treating the archive as limited to one project, matching the current code. Should it include that project or all projects? The answer changes what data is collected and who may request it.

### Metrics

Baseline:
> I’m treating this as architectural for now because global metrics would cross the current tenant boundary. Existing metrics are tenant-scoped. Should the new metric remain per tenant, or aggregate across tenants?

Candidate:
> I’m provisionally treating the metrics as tenant-scoped, matching the current code. Should they cover one tenant or all tenants? The answer changes aggregation and access control across tenants.

## Other candidate outputs

CSV:
> I’m using the analysis skill. This is a bounded change: the existing serializer already meets the requirements, so I would connect the route to it and test the route’s response and access checks. That is the proposed design; implementation waits for approval unless you have already approved this exact scope.

Dropdown:
> I’m using the writing-plans skill. Use the existing searchable control for the 30 items, preserving keyboard use and an empty-results state. Omit the plugin framework because there is only one current source. Revisit it when a second real source needs a different integration.

Review:
> Reject removal of export access checks: it would expose data outside the requester’s authorization. Use the managed vault that already meets the requirements; a custom vault adds security and maintenance work without a stated benefit. I would verify both claims against the actual code before issuing a formal review verdict.

Verification:
> No completion claim yet. Run the full report flow on an authorized, known invoice set and compare its line items and total with an independently calculated expected result. If the environment or suitable data is unavailable, report that verification gap.

## Scope of evidence

The candidate demonstrated provisional hypotheses, meaningful clarification, safe
scope reduction, and refusal to claim unverified completion. Its analysis dialogue
remained English. The verification prompt had no baseline run.
Counterexamples received a rule-level assessment, not separate execution.
Correction handling, humor, full review formatting, persisted plan structure,
native plugin loading, and Claude behavior remain outside these probes.

All offline commands listed in `docs/testing.md` passed. The integrity hook's three
cases passed after baseline regeneration. `bin/check-integrity` and `git diff --check`
also passed. These checks do not establish live plugin behavior.
