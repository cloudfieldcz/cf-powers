# Claude Code operations

- Load skills with the native `Skill` tool using the `cf-powers:` namespace.
  Native registration activates the skill; do not substitute a plain file read
  for Skill invocation on Claude. Read supporting references normally.
- Dispatch with the exposed Task/Agent tool. Use registered
  `cf-powers:<role>` reviewers where called for, or `general-purpose` plus the
  specified review skill for analysis cross-checks. Give workers bounded briefs.
- Track current tasks with TodoWrite (or its exposed native successor); keep
  durable progress in the existing CF Powers ledger.
- Resume the recorded worker with the native resume/message mechanism. Use
  SendMessage for a live agent; when the runtime requires an explicit resume to
  start another turn, use that. Re-dispatch with the brief/report only if the
  original worker cannot be resumed.
- Follow the host's completion interface. Work locally while children run and
  use bounded waits when idle; queue reviews beyond available slots.
- Apply the project's applicable CLAUDE.md instructions.

## Cheaper controller for a whole plan (opt-in)

When the user asks, or says the session model is too expensive for coordination, dispatch ONE `sonnet` subagent with the plan path. It runs `cf-powers:subagent-driven-development` end to end as the controller. It returns its "Rulings I made" list verbatim, and you relay that list unsummarized.
Use this for a whole plan only. For a multi-unit job, use `cf-powers:orchestrator` instead.
Check nested-agent support and free ancestor slots first. If there is no room for the controller and its workers, run the loop in this session.

## Model tiers

Read [choosing-subagent-models](../../choosing-subagent-models/SKILL.md) before
selection. Pass the tier's alias (`haiku`, `sonnet`, `opus`) in the Agent tool's
`model` parameter; the host resolves it and enforces availability. Registered
reviewer agents pin `opus` in their frontmatter. Do not change global model
settings to implement a per-task exception.

References: [model configuration](https://code.claude.com/docs/en/model-config),
[subagent model and effort](https://code.claude.com/docs/en/sub-agents).

Claude's SessionStart hook checks the existing integrity baseline and injects
using-superpowers. This is independent of Codex's native skill discovery.
