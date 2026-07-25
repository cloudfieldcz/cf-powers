# Upstream Sync v6.2.0 — Phase 3: Compression Sweep

> **For agentic workers:** REQUIRED SUB-SKILL: Use cf-powers:subagent-driven-development (recommended) or cf-powers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove recap sections, fabricated metrics, and benefits-selling prose aimed at a reader who has already invoked the skill; fold every load-bearing argument into a rationalization-table row or move it to its point of use.

**Architecture:** Three tasks grouped by risk. Task 1 is pure deletion of content that persuades nobody (the reader already invoked the skill) — the only additions are two pointers that move to their point of use. Task 2 converts two "Integration" listings into rationalization tables. Task 3 touches `using-superpowers`, which is injected into **every session**, so it is separated: its compression is the only change here with a measurable per-session token payoff, and the only one that must preserve our fork-specific Skip Flags table.

**Tech Stack:** Markdown skill documents.

**Index:** [`plan-index.md`](./2026-07-25-upstream-sync-v6.2.0-plan-index.md)

## Global Constraints

- Upstream source of truth: `obra/superpowers` at tag **v6.2.0** (commit `3dcbd5c`), referred to as `$UPSTREAM`.
- **Fork adaptation rules** — apply to every ported line: `superpowers:` → `cf-powers:`; `.superpowers/sdd/` → `.cf-powers/sdd/`; `docs/superpowers/plans/` → `docs/plans/`; `~/.config/superpowers/` → `~/.config/cf-powers/`; `brainstorming` → `analysis`; drop every reference to `using-git-worktrees` (we do not ship it).
- **Do not adopt upstream's vendor-neutral vocabulary.** Keep the Claude Code dialect ("Task tool", "Skill tool", "TodoWrite", "CLAUDE.md").
- **Never delete a behaviour-shaping argument without relocating it.** Upstream measured one such deletion degrading behaviour (TDD, handled in Phase 2). Deletions here are limited to fabricated metrics, self-congratulation, and recaps that restate the skill's own body.
- **Preserve every fork-specific addition**: the Skip Flags table in `using-superpowers`, the docs gate in `finishing-a-development-branch`, the `analysis` workflow, and all four `review-as-*` skills.
- `tests/integrity/run-test.sh` fails from the first `SKILL.md` edit until Phase 5 regenerates the baseline. Expected. All other suites stay green.
- One commit per task.

---

### Task 1: Drop social proof, fabricated metrics, and recaps

Six skills carry sections written to sell the skill to a reader who has already invoked it. The metrics in them ("First-time fix rate: 95% vs 40%", "From 24 failure memories") were never measured in this fork and cannot be reproduced; they read as authority while carrying no information the body doesn't already give.

Two pointers move rather than die: `systematic-debugging`'s verification reference moves into Phase 4 Step 3, where the agent is standing when it needs it.

**Files:**
- Modify: `skills/dispatching-parallel-agents/SKILL.md:158`, `:160-166`, `:175-182`
- Modify: `skills/verification-before-completion/SKILL.md:10`, `:108-116`, `:133-139`
- Modify: `skills/receiving-code-review/SKILL.md:207-213`
- Modify: `skills/writing-skills/SKILL.md:681-689`
- Modify: `skills/writing-plans/SKILL.md:175-181`
- Modify: `skills/systematic-debugging/SKILL.md:10`, `:190`, `:285-296`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: nothing later tasks rely on.

- [ ] **Step 1: `dispatching-parallel-agents` — drop Key Benefits, Real-World Impact, and the time-saved boast**

Delete the `**Time saved:** 3 problems solved in parallel vs sequentially` line (line 158), the entire `## Key Benefits` section (lines 160-166), and the entire `## Real-World Impact` section (lines 175-182, through `- Zero conflicts between agent changes`). The file now ends with the `## Verification` list.

- [ ] **Step 2: `verification-before-completion` — drop the moralizing opener, Why This Matters, and The Bottom Line**

Delete line 10 (`Claiming work is complete without verification is dishonesty, not efficiency.`) and the blank line after it, so `## Overview` leads with `**Core principle:** Evidence before claims, always.`

Delete the entire `## Why This Matters` section (lines 108-116) and the entire `## The Bottom Line` section (lines 133-139). The file now ends with the `## When To Apply` list.

The Iron Law, the Gate Function, and the Rationalization Prevention section already carry every rule these sections restated.

- [ ] **Step 3: `receiving-code-review` — drop The Bottom Line**

Delete the entire `## The Bottom Line` section (lines 207-213). The file now ends with `## GitHub Thread Replies`.

- [ ] **Step 4: `writing-skills` — drop The Bottom Line**

Delete the entire `## The Bottom Line` section (lines 681-689). The file now ends with `**Optimize for this flow** - put searchable terms early and often.`

`## The Iron Law (Same as TDD)` and `## RED-GREEN-REFACTOR for Skills` already state the discipline this section recapped.

- [ ] **Step 5: `writing-plans` — drop the Remember block**

Delete the entire `## Remember` section (lines 175-181). Every line in it is already a rule in `## No Placeholders`, `## Task Structure`, or `## Bite-Sized Task Granularity`.

This also removes an internal contradiction: the block instructed plan authors to "Reference relevant skills with @ syntax", while `writing-skills` warns that `@` force-loads the referenced file and burns context on every load.

- [ ] **Step 6: `systematic-debugging` — drop the opener and Real-World Impact, relocate the verification pointer**

Delete line 10 (`Random fixes waste time and create new bugs. Quick patches mask underlying issues.`) and the blank line after it, so `## Overview` leads with the core principle.

In Phase 4 Step 3 (`3. **Verify Fix**`), add a fourth bullet after `- Issue actually resolved?`:

```markdown
   - Use the `cf-powers:verification-before-completion` skill before claiming success
```

Then delete the `**Related skills:**` block at the end of `## Supporting Techniques` (its two bullets and the blank line before them) and the entire `## Real-World Impact` section. The file now ends with the `condition-based-waiting.md` bullet.

The TDD pointer that block carried is not lost — Phase 4 Step 1 already names `cf-powers:test-driven-development` at the exact moment a failing test is needed.

- [ ] **Step 7: Verify nothing else referenced the deleted sections**

Run: `grep -rn "Real-World Impact\|## Key Benefits\|## The Bottom Line" skills/`

Expected: exactly one hit — `skills/writing-skills/SKILL.md:135:## Real-World Impact (optional)`. That is a heading inside the **SKILL.md template** that `writing-skills` offers to skill authors, not a section of our own, and it stays.

Run: `grep -rn "@testing-anti-patterns\|@writing-good-tests\|with @ syntax" skills/`

Expected: no output (exit 1).

- [ ] **Step 8: Commit**

```bash
git add skills/dispatching-parallel-agents/SKILL.md skills/verification-before-completion/SKILL.md \
        skills/receiving-code-review/SKILL.md skills/writing-skills/SKILL.md \
        skills/writing-plans/SKILL.md skills/systematic-debugging/SKILL.md
git commit -m "refactor(skills): drop social proof and recap sections, relocate pointers"
```

---

### Task 2: Convert Integration listings to rationalization tables

`requesting-code-review` and `executing-plans` each end with an "Integration" section listing which workflows call them. Both callers already name these skills at their own point of use, so the listing tells the reader something they arrived knowing. In `requesting-code-review` the space is better spent on the two rationalizations that actually cost sessions: reviewing the diff inline instead of dispatching, and dumping session history on the reviewer.

**Files:**
- Modify: `skills/requesting-code-review/SKILL.md:9`, `:77-90`
- Modify: `skills/executing-plans/SKILL.md:82-88`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: nothing later tasks rely on.

- [ ] **Step 1: Trim the `requesting-code-review` opener**

Replace line 9:

```markdown
Dispatch cf-powers:code-reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history. This keeps the reviewer focused on the work product, not your thought process, and preserves your own context for continued work.
```

with:

```markdown
Dispatch cf-powers:code-reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history.
```

The dropped clause is not lost — it becomes the second rationalization row in Step 2, where an agent hits it mid-rationalization instead of in an opening paragraph.

- [ ] **Step 2: Replace Integration with Common Rationalizations**

Replace the entire `## Integration with Workflows` section (lines 77-90, through `- Review when stuck`) with:

```markdown
## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just review the diff myself instead of dispatching a reviewer" | You're the coordinator — reviewing the diff inline burns the context window you need to keep driving the work. Dispatch a reviewer subagent: the diff and the evaluation live in its context, and only the findings come back to you. |
| "The reviewer needs my whole session history to understand the change" | Hand it precisely crafted context, never your session's history. That keeps the reviewer on the work product, not your thought process. |
```

Keep the `## Red Flags` section that follows, and the closing `See template at: requesting-code-review/code-reviewer.md` line.

- [ ] **Step 3: Fold the `executing-plans` Integration section**

Delete the `## Integration` section's heading and its `**Required workflow skills:**` list (lines 82-86), keeping the note that follows it as a plain closing paragraph under `## Remember`:

```markdown
**Note:** User manages their own branches. Step 0 verifies a feature branch exists — do NOT create worktrees automatically.
```

Both named skills already appear at their point of use: `writing-plans` produces the plan this skill loads in Step 1, and `finishing-a-development-branch` is named in Step 5.

**Do not** adopt upstream's parallel change here, which inserts `use superpowers:using-git-worktrees to create one or verify the existing one` as a new Step 1. We do not ship that skill, and the note above states our fork's opposite policy deliberately.

- [ ] **Step 4: Verify the tables are well-formed and no dangling references remain**

Run: `grep -n "^## " skills/requesting-code-review/SKILL.md skills/executing-plans/SKILL.md`

Expected: `requesting-code-review` shows `When to Request Review`, `How to Request`, `Example`, `Common Rationalizations`, `Red Flags` — no `Integration with Workflows`. `executing-plans` shows `Overview`, `The Process`, `When to Stop and Ask for Help`, `When to Revisit Earlier Steps`, `Remember` — no `Integration`.

Run: `grep -rn "using-git-worktrees" skills/`

Expected: no output (exit 1). We never ship a reference to a skill we don't have.

- [ ] **Step 5: Commit**

```bash
git add skills/requesting-code-review/SKILL.md skills/executing-plans/SKILL.md
git commit -m "refactor(skills): trim Integration listings, add review rationalization table"
```

---

### Task 3: Compress the `using-superpowers` bootstrap

This skill is injected into **every session** by `hooks/session-start`, so its size is paid continuously — it is the only skill in the repo where byte count is a recurring cost rather than a one-off load. Upstream replaced the graphviz flowchart with the prose it encoded and folded the standalone precedence section into the closing paragraph.

Our copy carries a fork-specific **Skip Flags** table (added in cf-powers v1.7.0) that upstream has no equivalent for. It is behaviour-shaping in the opposite direction from Red Flags — it stops agents forcing skills onto mechanical one-liners — and it survives this task untouched.

**Files:**
- Modify: `skills/using-superpowers/SKILL.md:5`, `:15`, `:18-32`, `:36-60`, `:96-116`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: the compressed bootstrap whose hash Phase 5 records in the integrity baseline.

- [ ] **Step 1: Adopt the two micro-tested wording changes**

Line 5: `If you were dispatched as a subagent to execute a specific task, skip this skill.` → replace `skip` with `ignore` (upstream's wording; "skip" reads as a deferral, "ignore" as a full stop).

Line 15: `This is not negotiable. This is not optional. You cannot rationalize your way out of this.` → `This is not negotiable. You cannot rationalize your way out of this.`

- [ ] **Step 2: Replace the flowchart with the prose it encoded**

Replace lines 36-60 — the `## The Rule` heading, its paragraph, and the whole ```` ```dot ```` block — with:

```markdown
## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — including clarifying questions, exploring the codebase, or checking files. Even a 1% chance a skill might apply means you invoke it to check. If it turns out wrong for the situation, you don't have to use it.

Then announce "Using [skill] to [purpose]" and follow the skill exactly. If it has a checklist, create a TodoWrite todo per item.
```

The diagram encoded exactly these two sentences as nine nodes and eight edges. Nothing behavioural is lost, and the graphviz block was the single largest block in the file.

- [ ] **Step 3: Fold Instruction Priority and How to Access Skills into their points of use**

Delete the `## Instruction Priority` section (lines 18-26) and the `## How to Access Skills` section (lines 28-32), along with the standalone `# Using Skills` heading (line 34) that only existed to separate them from the rule. `## The Rule` becomes the first section after the `<EXTREMELY-IMPORTANT>` block.

The one Claude-Code-specific instruction worth keeping moves into `## The Rule`, appended after the announce paragraph:

```markdown
Use the `Skill` tool to load a skill — never the Read tool on a skill file, which loads the text without activating the skill.
```

The precedence rules move to `## User Instructions` in Step 5.

- [ ] **Step 4: Compress Skill Priority and drop Skill Types**

Replace the `## Skill Priority` section (lines 96-105) with:

```markdown
## Skill Priority

When multiple skills apply, process skills come first — they set the approach, then implementation skills carry it out.

- "Let's build X" → cf-powers:analysis first, then implementation skills.
- "Fix this bug" → cf-powers:systematic-debugging first, then domain skills.
```

Delete the `## Skill Types` section (lines 106-112). The rigid-vs-flexible distinction stays available to skill authors — `writing-skills` has its own `## Skill Types` section — and each skill already states which it is.

- [ ] **Step 5: Rewrite User Instructions to carry the precedence rules**

Replace the `## User Instructions` section (lines 114-116) with:

```markdown
## User Instructions

User instructions (CLAUDE.md, AGENTS.md, direct requests) take precedence over skills, which in turn override default system behavior. If CLAUDE.md says "don't use TDD" and a skill says "always use TDD," follow the user. Only skip a skill's workflow when your human partner has explicitly told you to.

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
```

- [ ] **Step 6: Verify the bootstrap still contains everything load-bearing**

Run: `grep -n "^## \|^# \|Skip Flags\|Red Flags" skills/using-superpowers/SKILL.md`

Expected sections in order: `# Using Superpowers` (or the existing H1), `## The Rule`, `## Red Flags`, `## Skip Flags`, `## Skill Priority`, `## User Instructions`. Both flag tables present.

Run: `grep -c "^| " skills/using-superpowers/SKILL.md`

Expected: `20` — Red Flags (1 header + 11 rows) and Skip Flags (1 header + 7 rows). Separator lines start `|---` and do not match `^| `. This task changes neither table, so the count must be **identical** to before the edit; any other number means a table row was collateral damage. Confirm by eye that both tables are intact.

Run: `wc -l skills/using-superpowers/SKILL.md`

Expected: roughly 85-95 lines, down from 116. Record the actual number for the changelog.

- [ ] **Step 7: Confirm the hook still injects the compressed bootstrap**

Run: `hooks/session-start | head -20`

Expected: the JSON payload, with `additionalContext` containing `You have superpowers.` and the compressed skill body. The integrity check inside the hook **will fail** at this point because the baseline still holds the pre-compression hash — the expected output at this step is the fail-closed alert, and Phase 5 Step 1 is what clears it.

- [ ] **Step 8: Commit**

```bash
git add skills/using-superpowers/SKILL.md
git commit -m "refactor(using-superpowers): compress the per-session bootstrap"
```
