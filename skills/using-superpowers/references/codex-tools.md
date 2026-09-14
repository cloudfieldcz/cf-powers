# Codex operations

Adapted from obra/superpowers v6.3.0; the actual host tool schema wins over
examples here. CF Powers keeps its own workflow and review decisions.

## Skills and roles

Codex discovers installed skills natively. Use its skill-loading facility when
exposed; otherwise read the resolved SKILL.md. There is no requirement for a
Claude `Skill` tool. Resolve cf-powers resources as described in runtime.md.
Directly invoked skills load this reference without relying on SessionStart.

Codex does not register our Claude agent frontmatter. Spawn a generic child and
give it the absolute `agents/<role>.md` path, the required review skill/template,
scope and evidence. Tell it to follow the role's body (frontmatter is Claude
metadata), read the actual source and write only its assigned review report.
Role names: code-reviewer, business-analyst-reviewer, developer-reviewer,
security-reviewer, performance-reviewer. Do not install global custom agents.

Use applicable AGENTS.md and host instructions for project rules. Use the
exposed planning tool for todos, or the existing run ledger when none is exposed.

## Dispatch and model selection

- Use the exposed spawn tool (for example `spawn_agent`), with a clean context:
  `fork_turns: "none"` where supported. Supply absolute brief, report, role and
  runtime-reference paths, the task directory and binding constraints.
- Follow choosing-subagent-models: resolve mechanical / implementation / judgment
  tiers once per run against the host's available models and their documented
  capabilities. Use a light model for mechanical edits, a capable middle tier
  for decided implementation, and the strongest available judgment tier for
  architecture and every review. Never pass `haiku`, `sonnet` or `opus` to Codex.
- Name both model and reasoning effort when the tool supports overrides; validate
  both against its allowlist. Preserve explicit user choices. Record actual
  selections in the brief/ledger. Full-history forks may prohibit overrides;
  use isolated forks instead of relying on upstream's full-history example.
- If no safe mapping or override is available, inherit the parent and report
  that tier routing is unavailable. Do not invent model IDs or claim inheritance
  means top-tier review. No silent downgrade to satisfy a failing spawn.

## Continuation and capacity

Send open findings to the recorded worker with a turn-triggering operation
(`followup_task` when exposed). `send_message` alone does not start a turn for
an idle agent. On a different tool generation, use its documented resume
operation. Only create a replacement when the worker cannot be resumed; give it
the brief and existing report. Preserve SDD's five-round loop and escalation.

Work locally while children run. When idle, use event-driven bounded waits
(`wait_agent` where exposed), respecting host limits on waits and user updates.
Reconcile live agents after a timeout or a missing result. Do not busy-poll or
wait indefinitely without reporting progress. Close children only if the host
exposes a close operation; do not fabricate `close_agent`.

Count occupied ancestor and child slots. Queue read-only reviews when capacity
is exhausted. Keep writers sequential in one working tree. A phase controller
may dispatch SDD workers; a leaf worker/reviewer must not delegate. If nested
agents are unavailable or capacity cannot support a phase controller plus its
worker, run the SDD controller loop in the parent, without dispatching an extra
controller. If subagents are entirely unavailable, use runtime.md's explicit
reduced-capability fallback and preserve the unreviewed artifacts.

## Git environments

Read `git branch --show-current`, `git rev-parse --git-dir` and
`git rev-parse --git-common-dir` to distinguish branch, detached HEAD and linked
worktree. Resolve paths before comparing them. Detached HEAD alone does not
prove Git writes are forbidden. Keep the existing user-managed branch policy:
use an already-provided worktree, never create/remove one automatically.

On detached HEAD, preserve work and report the commit (or uncommitted diff if
commits are blocked). For integration, use only actions authorized and supported
by the host. If naming a branch is needed, request that specific choice or use
an already-authorized name; do not switch away from or delete the workspace.
When sandbox permissions prevent integration, provide the exact state for the
user's native handoff. Do not offer a merge/push command requiring a branch
that does not exist.

## Bootstrap and integrity

The Codex manifest intentionally declares `hooks: {}` so it cannot discover
Claude's hooks/hooks.json. Native-discovered skills have no per-session hash
check. `bin/check-integrity` is an optional read-only check and a release gate;
Codex installation does not automatically run it. It checks SKILL.md files only.
