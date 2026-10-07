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
selection. Mapping: mechanical → `haiku`, implementation → `sonnet` (Sonnet 5.5),
judgment/review → `opus` (Opus 5.5). For judgment work explicitly select `opus`;
inherit only when the actual parent model is the selected target. Under a Fable
parent, select `opus` explicitly unless the user asked for Fable subagents.

For a requested Fable dispatch, verify availability in the current host/account
and use the provider's exact ID (`claude-fable-5-1` on the Anthropic API). Use
`fable` only after you verify that the alias resolves to the intended version.
Claude Code requires v2.1.257 or later for this model. Use only parameters
exposed by the active Task/Agent schema; do not assume it accepts every CLI option.
Supported subagent definitions can set `model` and `effort: high`; if the active
dispatch cannot set effort, use verified inheritance or report the limitation.
Check the actual selected model/effort, including host substitutions (for
example in `/tasks`), and record it in the brief/ledger. Explicit user choices
and organization restrictions take precedence. Do not change global model
settings to implement a per-task exception.

References: [model configuration](https://code.claude.com/docs/en/model-config),
[subagent model and effort](https://code.claude.com/docs/en/sub-agents).

Claude's SessionStart hook checks the existing integrity baseline and injects
using-superpowers. This is independent of Codex's native skill discovery.
