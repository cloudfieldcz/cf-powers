# CF Powers

Skills plugin for Claude Code and Codex that guides your AI coding agent through a structured development workflow — from idea to implementation.

Based on [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent, extended with technical analysis workflow and cross-check review agents.

Codex support is implemented for native plugin installation. CLI 0.154.0
installation, update and skill/hook discovery are verified; the full behavioral
regression and desktop UI checks are tracked in the
[verification record](docs/codex-verification.md). See the
[design](docs/codex-support.md) for the shared workflow and runtime boundaries.

## Quick Start

See the **[installation guide](docs/installation.md)** for choosing between CLI
plugins and VS Code standalone skills, updates, removal and troubleshooting.

### Claude Code

```bash
# 1. Register the marketplace
/plugin marketplace add cloudfieldcz/cf-powers

# 2. Install the plugin
/plugin install cf-powers@cf-powers

# 3. Verify — you should see cf-powers commands in the list
/help
```

The Claude plugin activates through its SessionStart hook.

### Codex CLI

From a local checkout containing this version:

```bash
codex plugin marketplace add /absolute/path/to/cf-powers
codex plugin add cf-powers@cf-powers
```

Start a fresh session. Use `/skills` or `$` and choose
`cf-powers:analysis`, `cf-powers:writing-plans`, `cf-powers:executing-plans`
or `cf-powers:orchestrator`. Skills can also activate from matching requests.
Codex 0.154.0 additionally imports the Claude command wrappers as
`cf-powers:source-command-*` skills; the canonical entry points above are stable.

For installation directly from GitHub, use
`codex plugin marketplace add https://github.com/cloudfieldcz/cf-powers.git`
instead of the local path.

### Codex in VS Code (standalone skills)

The IDE extension supports standalone skills, but currently does not support
plugins. Install the shared skill tree from a complete checkout (macOS/Linux,
Python 3):

```bash
git clone https://github.com/cloudfieldcz/cf-powers.git ~/.codex/cf-powers
python3 ~/.codex/cf-powers/bin/codex-skills install
```

For an existing checkout, run `python3 bin/codex-skills install` there instead.
The installer creates `~/.agents/skills/cf-powers` pointing to that checkout's
`skills/` directory and refuses to overwrite unrelated files. Keep the complete
checkout: skills also use its reviewer definitions and helper scripts.

Reload VS Code and start a new Codex chat. Type `$` or `/skills` and select
`cf-powers:analysis`, `cf-powers:writing-plans`, or `cf-powers:orchestrator`.
Codex 0.154.0 prefixes these with the discovery folder name; older clients may
show the plain skill names. This discovery route also works in CLI.
Use one installation route per environment to avoid duplicate entries; standalone
upstream Superpowers shares some names, so avoid enabling both standalone trees.
Available subagent tools depend on the host; missing independent review is
reported explicitly, never treated as passed.

Update with `git -C ~/.codex/cf-powers pull --ff-only`, then start a new session.
Uninstall with `python3 ~/.codex/cf-powers/bin/codex-skills uninstall`; the checkout
is retained. With Remote SSH, WSL or a dev container, install in the environment
where the Codex extension runs.

This follows upstream's earlier clone-and-symlink installation. See
[OpenAI standalone skill discovery](https://learn.chatgpt.com/docs/build-skills)
and [IDE plugin limitations](https://learn.chatgpt.com/docs/plugins).

### Codex App

Install from the cf-powers repo marketplace using the App's supported marketplace
flow (team/workspace GitHub import where applicable), then open a fresh session
and choose the cf-powers skills. The CLI/App Server integration is verified;
manual desktop UI verification remains pending. This is a repo plugin, not a
listing in OpenAI's public catalog.

Both runtimes share the same workflow decisions, reviews and ledgers. Codex uses
native skill discovery with **no SessionStart hook or per-session hash check**;
run `bin/check-integrity` manually to verify the shipped SKILL.md baseline.
See [SECURITY.md](SECURITY.md) for the integrity boundary. The plugin does not
edit global model settings or install custom roles into your profile.

## Workflow

Every feature starts the same way:

```
/analyse  →  /write-plan  →  execute
    ↓
 idea → dialogue → analysis
    ↓
 BA + Dev cross-check
```

1. **`/analyse`** — From idea to technical analysis in one step. Explores the idea through dialogue, then produces a full technical analysis (Czech output): architecture, DB changes, affected files, phases, risks, testing. Automatically dispatches BA and Developer reviewers for cross-check.
2. **`/write-plan`** — Break the analysis into vertical-slice units and decision-level tasks; the implementer runs the TDD loop.
3. **Execute** — Run the plan via subagent-driven development, or `/orchestrate` for a multi-phase index.

What happens at step 3 depends on the size of the feature:

### Simple Feature (single phase)

When the analysis contains one logical phase, `/write-plan` produces a single plan file:

```
docs/plans/YYYY-MM-DD-feature-plan.md
```

You execute it in one go — either with **subagent-driven development** (in the current session) or by opening a new session with **executing-plans** (batch execution with checkpoints).

### Multi-Phase Feature

When the analysis defines multiple implementation phases, `/write-plan` produces one plan file per phase plus an index:

```
docs/plans/YYYY-MM-DD-feature-plan-index.md      ← orchestration dashboard
docs/plans/YYYY-MM-DD-feature-plan-1-models.md    ← phase 1
docs/plans/YYYY-MM-DD-feature-plan-2-services.md  ← phase 2
docs/plans/YYYY-MM-DD-feature-plan-3-ui.md        ← phase 3
```

You then execute the whole index with **`/orchestrate`**: one session acts as the orchestrator, delegates each phase to a subagent, reviews every phase on the judgment tier (Opus on Claude), updates the index and keeps a run ledger — so six phases do not exhaust one context window. The ledger makes a resume in a fresh session free.

You can still execute phases one at a time by hand if you prefer; the index file tracks overall progress either way.

### Orchestrating Work Without a Plan

`/orchestrate` is not limited to plan indexes. Any job that splits into units a subagent can own end to end runs the same way — a migration across 23 handlers, a batch of failing suites, an audit over a codebase, a translation pass. When no work list exists, the orchestrator scouts one, writes it to its run workspace, and then delegates, reviews and ledgers unit by unit.

## Skills

| Skill | When it activates |
|-------|-------------------|
| **analysis** | Non-trivial work with design choices — from idea to technical analysis |
| **review-as-ba** | Cross-check analysis from business analyst perspective |
| **review-as-dev** | Cross-check analysis from developer perspective |
| **writing-plans** | When you need a step-by-step implementation plan |
| **executing-plans** | Batch execution with human checkpoints |
| **subagent-driven-development** | Fast parallel execution with two-stage review |
| **orchestrator** | Any job too big for one session — plan index, migration, bug batch, audit; delegates each unit to subagents |
| **choosing-subagent-models** | Before any dispatch — picks a mechanical / implementation / judgment tier for the active runtime |
| **test-driven-development** | During implementation (RED-GREEN-REFACTOR) |
| **systematic-debugging** | When encountering bugs or test failures |
| **verification-before-completion** | Before claiming work is done |
| **requesting-code-review** | After completing tasks |
| **receiving-code-review** | When processing review feedback |
| **dispatching-parallel-agents** | When facing independent parallel tasks |
| **documenting-changes** | After implementation, before merge/PR — keep docs in sync with code |
| **finishing-a-development-branch** | When ready to merge or create a PR |
| **writing-skills** | When creating new skills |
| **using-superpowers** | Injected automatically at session start |

## Updating

Claude Code:

```bash
/plugin update cf-powers
```

Codex: refresh a Git marketplace with `codex plugin marketplace upgrade`, then
run `codex plugin add cf-powers@cf-powers` and start a fresh session. For a local
marketplace, update the checkout first. Changed plugin content needs a new
manifest version to avoid reusing an old cached installation.

Run offline and native installation checks with
`bash tests/codex/run-test.sh --native`; it uses an isolated temporary profile.

## Releasing

The SessionStart hook fail-closes if `.claude-plugin/integrity.sha256`
does not match the on-disk skill files. That means **any release that
touches `skills/*/SKILL.md` must refresh the baseline before tagging**,
otherwise installed clients will see a `<security-alert>` block instead
of the `using-superpowers` skill content after `/plugin update`.

Release checklist:

1. Land all skill changes on `main`.
2. Run `bin/update-integrity` and commit
   `.claude-plugin/integrity.sha256` if it changed.
3. Bump `version` in **all three**
   [.claude-plugin/plugin.json](.claude-plugin/plugin.json),
   [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json), and
   [.codex-plugin/plugin.json](.codex-plugin/plugin.json)
   following [SemVer](https://semver.org/) (skill additions/removals
   = minor; behavior fixes = patch). Claude Code reads `plugin.json`
   when deciding whether `/plugin update` has new content — if only
   `marketplace.json` is bumped, clients silently skip the update.
4. Update [CHANGELOG.md](CHANGELOG.md) — move the `[Unreleased]`
   entries under the new version heading with today's date.
5. Run `tests/integrity/run-test.sh` to confirm the hook still passes
   on a clean tree.
6. Run `bin/check-integrity` and `bash tests/codex/run-test.sh --native`.
   Complete the behavior/UI checks recorded in [docs/testing.md](docs/testing.md)
   for both runtimes; record client versions and actual results.
7. Commit, tag `vX.Y.Z`, push tag when the release is authorized.

If you forget step 2, end users get a fail-closed session on the next
update. Recovery is to ship a follow-up release with the regenerated
baseline.

## Credits

This project is a fork of [Superpowers](https://github.com/obra/superpowers) by [Jesse Vincent](https://github.com/obra). The original project provides the core skills library (TDD, debugging, collaboration patterns) and the plugin architecture. We added the `analysis` workflow with BA/Developer cross-check agents.

What we pull down from upstream — when, what, and what we deliberately skip — is recorded in [docs/upstream-sync.md](docs/upstream-sync.md).

## License

MIT — see [LICENSE](LICENSE) for details.
