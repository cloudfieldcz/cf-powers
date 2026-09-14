# Codex support design

Status: implemented in 2.5.0; validation coverage is
tracked in [codex-verification.md](codex-verification.md). Based on cf-powers
`3ae09eb` (upstream backports complete; Claude test pass reported by maintainer).

## Outcome and scope

Install cf-powers in Codex App and CLI and use the same analysis → plan →
execution → review workflow as Claude Code, including our custom orchestrator.
Keep Claude working. The first release targets local macOS/Linux environments;
Windows and IDE standalone installation need their own validation before being
advertised. No new application, MCP server or second copy of the skills.

Upstream already supports both Codex App and CLI. This is an adaptation of its
integration, not a new integration design from scratch. Pin reference material
to [upstream v6.3.0](https://github.com/obra/superpowers/tree/v6.3.0), commit
`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`. The later dev tree `5940bd8`
adds no further changes to those Codex integration files.

## Behavioral source of truth — maintainer requirement

**The behavior of cf-powers at `3ae09eb` is authoritative on both runtimes.**
Upstream supplies Codex integration mechanics only. Start every skill edit from
our version; never replace a skill or reviewer body with its upstream counterpart.
Translate how an operation is performed, preserving when it happens, why it
happens, its scope and its stopping conditions.

In particular, retain our skip flags, analysis workflow and review perspectives,
short decision-level plans and vertical slices, conditional plan review, visual
verification, model-tier intent, SDD rulings and fix-loop limits, orchestrator
ledgers/resume, and the user's existing authorization and branch choices. Do not
import upstream's extra approval stages, mandatory worktrees, brainstorming
workflow or different review cadence as part of this port.

Each changed instruction must have a concrete runtime-compatibility reason.
If a host limitation prevents equivalent behavior, document that specific
limitation and the fallback; do not quietly redefine the shared workflow.
Behavioral redesigns require a separate scope decision, not a porting cleanup.

Validate parity using the same scenarios against our Claude behavior and the
Codex port: compare decisions, handoffs, review scope and artifacts rather than
exact wording or tool names. Upstream behavior is not the acceptance oracle.

## Upstream reuse decisions

| Upstream source (v6.3.0) | Decision for cf-powers |
|---|---|
| `.codex-plugin/plugin.json` | Adapt native manifest: `name: cf-powers`, `skills: ./skills/`, explicit `hooks: {}`, Cloudfield metadata. Omit upstream icons/legal URLs and optional fields we cannot supply accurately. |
| `.agents/plugins/marketplace.json` | Adapt the single-repo marketplace. Use `name: cf-powers`, a same-repo local source `{source: local, path: ./}` per current official docs; validate on the target clients. |
| `skills/using-superpowers/SKILL.md` | Reuse platform-reference routing. Keep our skip flags and analysis entry point; remove the blanket prohibition on reading a skill file on Codex. |
| `skills/using-superpowers/references/codex-tools.md` | Adapt dispatch, follow-up, waiting and environment detection. Current host tool definitions override copied examples; see below. |
| Shared skill vocabulary | Adopt action-based wording only where a Claude tool/model prevents Codex execution. Retain our v2.4 planning, verification, branch and ledger behavior. |
| `tests/codex/test-marketplace-manifest.sh` | Adapt schema/name/path and empty-hook-object checks to `tests/codex/run-test.sh`; supplement with real installation evidence. |
| `scripts/package-codex-plugin.sh` and its archive tests | Defer: repo marketplace installation carries the whole plugin. A later portal archive must include our `agents/` and own metadata. |
| `scripts/sync-to-codex-plugin.sh` | Skip: it manages a fork of the official plugin repository, pushes a branch and opens a PR. We distribute from cloudfieldcz/cf-powers. |
| `docs/porting-to-a-new-harness.md` | Use the shared-content/thin-adapter principle. Its universal SessionStart requirement is stale for Codex: upstream's actual manifest explicitly disables hooks. |

The upstream packager requires a previous official package to seed every
`skills/*/agents/openai.yaml`, and archives an allowlist that excludes our root
reviewer definitions. Those are distribution-specific assumptions, not Codex
runtime requirements. Do not introduce that dependency into our first release.

## Installation contract

One repository, one shared `skills/`, two native plugin manifests. Codex installs
through its own marketplace mechanism; no bootstrap CLI, global skill symlinks,
agent-role installation or automatic edits to user configuration. Existing
Claude commands and hook configuration remain available to Claude.

Current docs support same-repository local plugin sources, with paths relative
to the marketplace root. [Marketplace formats](https://learn.chatgpt.com/docs/enterprise/plugin-management)

For CLI development, document this explicit opt-in configuration, then select
cf-powers in `/plugins` and start a fresh session:

```toml
[marketplaces.cf-powers]
source_type = "local"
source = "/absolute/path/to/cf-powers"
```

For distribution, use `source_type = "git"` with source
`https://github.com/cloudfieldcz/cf-powers.git` and an optional tested release
`ref`. Desktop/team installation uses the supported marketplace import flow;
record the exact tested UI steps and client version during implementation.
Do not promise inclusion in OpenAI's public catalog.
[Marketplace configuration](https://learn.chatgpt.com/docs/config-file/config-reference)

Codex entry points are the installed skills: `analysis`, `writing-plans`,
`executing-plans`, `orchestrator`. Document picker-based invocation (`$`/`/skills`
in CLI); resolve the installed cf-powers identity rather than an unrelated skill
with the same short name. Claude `/analyse`, `/write-plan`, `/execute-plan` and
`/orchestrate` commands are unchanged. Codex 0.154.0 also imports their wrappers
as `cf-powers:source-command-*` skills; the canonical skill names above remain
the documented Codex entry points. Test with upstream Superpowers also
installed to catch namespace ambiguity. [Skills](https://learn.chatgpt.com/docs/build-skills)

## Shared runtime contract

The shared `skills/using-superpowers/references/runtime.md` routes to
`claude-code-tools.md` and the adapted upstream `codex-tools.md`. These are instruction references, not a new executable
adapter framework. Select the runtime from the host's exposed tools and context,
not merely the presence of both manifests in the installed directory.

Every directly invoked workflow that depends on runtime behavior links to the
active reference at its point of use. Do not rely solely on `using-superpowers`:
Codex loads skills on demand, and clean-context workers skip the general
bootstrap. Resolve reference and role paths from the installed skill location;
pass absolute paths in dispatch briefs, never assume the consumer's cwd is the
plugin checkout.

| Operation | Claude Code | Codex contract |
|---|---|---|
| Load a skill | Native `Skill` tool | Native skill facility, or read the resolved `SKILL.md` when that is the exposed mechanism. |
| Track progress | Native todos | Available planning tool; durable progress remains in our existing ledger. |
| Dispatch | Native task/agent tool and registered reviewer type | Exposed spawn tool, isolated context, bounded brief and selected model/effort. |
| Continue a worker | Native resume/message mechanism | Turn-triggering follow-up, e.g. `followup_task`; passive messaging alone does not wake an idle child. |
| Wait | Native task completion | Event-driven bounded waits, useful local work first, periodic reconciliation and user updates within host limits. |
| Project rules | Applicable `CLAUDE.md` | Applicable `AGENTS.md` and host instructions. |

Upstream's current text says full-history forks allow model overrides; the host
contract in this audit forbids those overrides. Use isolated forks when selecting
model/effort, and follow the actual schema. Likewise, do not insist on obsolete
feature flags or `close_agent` where those are absent. Runtime instructions and
user authorization take precedence over the skill. [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

## Reviews and model routing

Keep the bodies in `agents/{code,developer,business-analyst,security,performance}-reviewer.md`
as the shared role definitions. Claude continues to register them natively.
A Codex generic reviewer reads the role body from its absolute plugin path;
Claude frontmatter is registration metadata, not a Codex configuration. Pass
the relevant review skill/template, scope, base/head SHAs, evidence and report
path. No global custom-role setup is required.

`choosing-subagent-models` owns the routing policy. Common prose uses three tiers:
mechanical, implementation, judgment. Claude maps these to Haiku/Sonnet/Opus.
Codex maps them once per run to the available presets: lightest suitable model
for mechanical work, capable middle tier for decided implementation, highest
available judgment tier for review/architecture. Record actual model and effort
with each dispatch. Follow explicit user model choices; if the host exposes no
safe tier mapping, inherit the parent and report that cost tiering is unavailable.
Never send Anthropic aliases to Codex or silently assume the parent is top-tier.

Keep reviews independent and source files read-only (review reports may be
written to their assigned workspace). Preserve the existing four analysis
review seats, per-task combined SDD review and final branch review. Queue read-only
reviews when slots are scarce; a four-slot environment cannot necessarily run
four children at once. Never run concurrent writers in the same working tree.

Orchestrator phase controllers may delegate SDD tasks; leaf implementers and
reviewers may not delegate. Account for occupied ancestor slots. When nesting is
unavailable, the parent runs the phase's SDD controller loop itself. If there are
no subagents at all, execute authorized work inline and explicitly mark independent
review as unavailable; never claim equivalent review coverage or a clean review.

## Git and integrity

Preserve the human-managed branch policy and `.cf-powers/sdd/` and
`.cf-powers/orchestrator/` artifact contracts. Detect an existing linked worktree
and detached HEAD separately. Detached HEAD is not by itself proof that Git
writes are prohibited. Use actual permissions; do not create/delete worktrees,
change branches or force a push just to fit a copied upstream recipe. When
integration is unavailable, keep artifacts and provide a handoff with exact state.

**Implemented boundary: hookless Codex, matching upstream.** Explicit
`hooks: {}` prevents accidental Claude-hook discovery. Retain the existing
baseline and Claude startup check. Provide a read-only `bin/check-integrity` command
for release validation and optional troubleshooting; keep
`bin/update-integrity` as the explicit baseline mutation. This verifies the
current SKILL.md scope only, not every prompt/reference/role file.

Codex receives native-discovered skills without a per-session hash check. State
that difference in SECURITY.md and the install guide. Marketplace installation
does not automatically run our checker. Extending the hash coverage or adding a
Codex hook is separate work; neither is necessary to reproduce upstream's model.

## Acceptance evidence

| Check | Observable outcome |
|---|---|
| cf-powers behavioral parity | The same scenarios preserve our skip flags, short plans, conditional review, authorization, rulings, visual evidence and resume decisions; every difference is explained by an actual host limitation. |
| Fresh App and CLI install | cf-powers is listed; all shipped skills resolve from the installed copy; a plain debugging request activates the appropriate skill without manual bootstrap. |
| Direct workflow invocation | analysis, plan and orchestrator load their runtime references even when using-superpowers was not loaded first. |
| Claude regression | Hook injects once with matching baseline; existing commands, skip flags and runtime actions continue working. |
| Hook isolation | Codex registers no Claude hook and gets no integrity-alert or duplicate bootstrap from it. |
| Review roles | All four analysis perspectives return scoped reports; code review catches an injected defect without editing source. |
| SDD fix round | Worker implements a small fixture, reviewer catches a defect, same worker resumes and produces passing evidence. |
| Orchestration/resume | Two sequential units complete; restart after the first resumes only unfinished work from the ledger; limited slots do not deadlock. |
| Model selection | Actual dispatch arguments use allowed Codex models/effort; explicit user choices survive; no Anthropic alias leaks. |
| Reduced capabilities | No-subagent/nesting limitations produce an honest inline fallback, no invented tools or independent-review claim. |
| Plan handoff | Plan-only stops; already-authorized execution preserves method/order without another permission question. |
| Git environments | Normal branch, existing worktree and detached HEAD retain user work and report valid integration options. |
| Install/update identity | Test local development install and update from a committed fixture; no duplicate skills after restart, including coexistence with upstream. |
| Integrity checker | Matching tree succeeds; modified skill, missing baseline or missing hash utility fails; check does not rewrite anything. |

Offline tests validate executable helpers and packaging contracts. Behavior tests
inspect actual actions/artifacts/transcripts, not string presence in skill prose.
Record tested client versions, selected models and the plugin commit used.
Claude executes its behavioral regression tests, per the maintainer's instruction;
Codex behavior is verified in fresh Codex sessions. The current verification record distinguishes completed live checks from
remaining scenarios.

First dual-runtime release: **2.5.0**. Keep both plugin manifests and the Claude
marketplace version aligned and refresh hashes for each release. The maintainer
authorized this release with the verification coverage documented above; README
reports implemented support and remaining validation without claiming full
regression coverage.
