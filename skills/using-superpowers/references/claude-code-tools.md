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

## Model tiers

Use the policy in choosing-subagent-models. Mechanical → `haiku`, implementation
→ `sonnet`, judgment/review → `opus`. An omitted model is correct for judgment
only when the parent actually runs Opus; otherwise name `opus`. Preserve explicit
user model choices. Record the selected model or deliberate inheritance in the
brief/ledger, not an unsupported extra tool parameter.

Claude's SessionStart hook checks the existing integrity baseline and injects
using-superpowers. This is independent of Codex's native skill discovery.
