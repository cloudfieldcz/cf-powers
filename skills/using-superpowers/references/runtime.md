# Runtime operations

CF Powers' workflow decisions are shared. Translate only the operation used to
carry them out. Host instructions and explicit user choices take precedence.

Read only the reference for the active host, as identified by its exposed tools
and session context (both manifests can be present on disk):

- Claude Code: [claude-code-tools.md](claude-code-tools.md)
- Codex: [codex-tools.md](codex-tools.md)

Resolve these paths from this installed file, not the project working directory.
For standalone installations, resolve filesystem symlinks to the physical checkout
before finding sibling skills, reviewer roles or the root.
The plugin root is three directories above this reference directory. Resolve
`cf-powers:<skill>` to that plugin's `skills/<skill>/SKILL.md`, and reviewer
roles to `agents/<role>.md` in the same plugin. Do not accidentally load the
upstream Superpowers copy or a same-named project skill. Pass absolute resource
paths and the selected runtime reference to clean-context children.

Standalone discovery may prefix names with the discovery folder (`cf-powers:`
on Codex 0.154.0), or expose original frontmatter names on older clients. References to `cf-powers:<skill>`
still mean the matching file in this same checkout; read it directly when that
qualified name is absent from the skill picker.

Dispatch examples in skills describe a brief, role, tier and output contract;
translate them to the actual tool schema. A `tier` is a policy label, never a
literal model ID or an extra tool argument. Each workflow that dispatches agents
requests that delegation explicitly; child implementers/reviewers do not fan out.

If subagents are unavailable, do authorized implementation inline using
executing-plans and retain its progress/checkpoints. Report independent review
as unavailable, not passed; keep artifacts for that review and do not claim
review-gated completion. Do not invent tools or enable features globally.
