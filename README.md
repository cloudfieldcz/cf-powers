# CF Powers

Skills plugin for Claude Code that guides your AI coding agent through a structured development workflow — from idea to implementation.

Based on [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent, extended with technical analysis workflow and cross-check review agents.

## Quick Start

```bash
# 1. Register the marketplace
/plugin marketplace add cloudfieldcz/cf-powers

# 2. Install the plugin
/plugin install cf-powers@cf-powers

# 3. Verify — you should see cf-powers commands in the list
/help
```

That's it. The plugin activates automatically on every session.

## Workflow

```
/brainstorm  →  /write-analysis  →  /write-plan  →  execute
                     ↓
              BA + Dev cross-check
```

1. **`/brainstorm`** — Refine your idea through questions. Produces a design document.
2. **`/write-analysis`** — Turn the design into a full technical analysis (Czech output): architecture, DB changes, affected files, phases, risks, testing. Automatically dispatches BA and Developer reviewers for cross-check.
3. **`/write-plan`** — Break the analysis into bite-sized TDD implementation tasks.
4. **Execute** — Run the plan via subagent-driven development or batch execution.

## Skills

| Skill | When it activates |
|-------|-------------------|
| **brainstorming** | Before any creative work |
| **write-analysis** | After brainstorming, before implementation planning |
| **review-as-ba** | Cross-check analysis from business analyst perspective |
| **review-as-dev** | Cross-check analysis from developer perspective |
| **writing-plans** | When you need a step-by-step implementation plan |
| **executing-plans** | Batch execution with human checkpoints |
| **subagent-driven-development** | Fast parallel execution with two-stage review |
| **test-driven-development** | During implementation (RED-GREEN-REFACTOR) |
| **systematic-debugging** | When encountering bugs or test failures |
| **verification-before-completion** | Before claiming work is done |
| **requesting-code-review** | After completing tasks |
| **receiving-code-review** | When processing review feedback |
| **dispatching-parallel-agents** | When facing independent parallel tasks |
| **using-git-worktrees** | When you need an isolated workspace |
| **finishing-a-development-branch** | When ready to merge or create a PR |
| **writing-skills** | When creating new skills |
| **using-superpowers** | Injected automatically at session start |

## Updating

```bash
/plugin update cf-powers
```

## Credits

This project is a fork of [Superpowers](https://github.com/obra/superpowers) by [Jesse Vincent](https://github.com/obra). The original project provides the core skills library (TDD, debugging, collaboration patterns) and the plugin architecture. We added the `write-analysis` workflow with BA/Developer cross-check agents.

## License

MIT — see [LICENSE](LICENSE) for details.
