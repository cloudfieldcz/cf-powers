---
name: using-superpowers
description: Use at session start to select relevant workflows, including automatic coordination for complex work and direct execution for mechanical tasks.
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

# Using Superpowers

## Activation precedence

1. Follow explicit user and project instructions, subject to host instructions.
2. Select work-method skills from the action, not task size. Load TDD before
   developing or refactoring production code, debugging before diagnostic work, review
   before evaluating a requested change, and parallel-dispatch guidance before delegation.
   A clear request already establishes that trigger; do not postpone it until exploration succeeds.
3. Select analysis, planning, and orchestration from design uncertainty, dependencies,
   coordination needs, and risk. A fully specified migration can still need coordination.
4. Use the direct path only for mechanical changes without new logic or unresolved
   behavior: a literal config edit, a non-code rename, a prose typo, or documentation.
   Production-code refactors retain the TDD skill's scope and exceptions.

A small function is still new logic. It requires TDD even when its specification
is complete and no analysis document is needed. Tests written after production
code do not satisfy TDD. A literal config edit is not production code and needs no TDD.
Explicit user or project exceptions still apply.

Explicit skill requests remain binding. Missing inputs may prevent completing the
workflow, but do not erase a clear request to debug, review, or develop behavior.
Read enough to locate the work after loading its applicable work-method skill.
Size-based exceptions never waive TDD, verification, documentation, or review gates
required by the selected workflow. Resume existing plans under their recorded
workflow and completion gates, even when the remaining task is small.

**Runtime:** Follow project instructions. Use native skill loading and ordinary
project reads directly. Before dispatch, resume, model selection, or shared plugin
resource resolution, read [runtime operations](references/runtime.md) and the
active-host reference once per context.

## The Rule

**Apply the activation precedence before the first action of the relevant type.**
For development, debugging, review, or delegation, load the applicable work-method
skill before doing that work. A routine file listing to locate the project is not
permission to implement new logic without TDD. For size-dependent workflows, inspect
only enough context to establish their trigger before entering the workflow.

Then announce "Using [skill] to [purpose]" and follow the skill exactly. If it has a checklist, create a native todo per item (or track it in the existing ledger).

Use the active runtime's skill-loading mechanism from [runtime operations](references/runtime.md). Claude uses its native Skill tool; Codex can read the resolved skill file when that is its exposed mechanism.

## Red Flags

These thoughts mean STOP—you're rationalizing past a skill that applies:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions about non-trivial work are tasks. Check for skills. |
| "I need more context first" | Work-method skills load before the action. Inspection decides only size-based ceremony. |
| "Let me explore the codebase first" | A request to develop, debug, review or delegate loads its skill first. Exploration comes after. |
| "I can check git/files quickly" | Read-only checks can size analysis or planning. They never delay a work-method skill. |
| "Let me gather information first" | The request itself is the trigger. Load the skill, then gather information. |
| "This doesn't need a formal skill" | If a skill clearly applies, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action on non-trivial work = task. Check for skills. |
| "I'll just do this one thing first" | Check BEFORE doing anything non-trivial. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Skip Flags

These flags skip unnecessary design/planning ceremony only. They never bypass
a work-method skill whose action trigger applies:

| Thought | Reality |
|---------|---------|
| "This is one mechanical file write without new logic" | Apply the literal change and verify it; new behavior still requires TDD. |
| "The known mechanical change is fully specified" | Execute it directly; a larger specified migration can still need coordination. |
| "No design choices or coordination needs remain" | No design or planning workflow is needed; keep the applicable quality checks. |
| "It's a literal config tweak or typo" | Edit and verify it. A one-line logic change still requires its work-method skill. |
| "It's a direct factual question" | Answer it. Skills are for *doing*, not chatting. |
| "Read-only exploration of one file/path" | Read it and report. Skills don't gate looking. |
| "Routine git/shell I've been authorized for" | Run it. The skill rules cover *judgment*, not muscle memory. |

**How the two tables relate:** Red Flags catches rationalizing *away* from skills that apply. Skip Flags catches rationalizing *into* skills that don't. Both errors waste the user's time. If no work-method trigger applies and a task matches Skip Flags, name it in one short sentence ("going direct — single config file, no design choices") and proceed. If the user disagrees, they'll redirect.

## Skill Priority

When multiple skills apply, process skills come first — they set the approach, then implementation skills carry it out.

- New or changed code behavior → cf-powers:test-driven-development before implementation.
- "Let's build X" with unresolved design → cf-powers:analysis before implementation.
- A specified change with dependent units → planning or orchestration as needed.
- "Fix this bug" requiring investigation → cf-powers:systematic-debugging first.
- A known mechanical correction → the direct path, with relevant verification.

## Comments in Code You Write

A comment earns its place only by saying what the line cannot: a non-local coupling, a
refusal the code implies but never names, why the obvious simpler version is wrong. Cut
the rest — restating the code, narrating the flow, background, section banners, ALL-CAPS
emphasis, a module docstring that tells the feature's story. Long rationale belongs in the
project's docs, where it can be found and maintained. Past roughly one comment line per ten
lines of code you are writing prose. The surrounding file is not the standard: write the
new comment short even where the one above it runs six lines.

## Technical English

Comments, docstrings, commit messages, PR descriptions, analyses, plans and technical
docs follow the writing rules of Simplified Technical English (ASD-STE100). Each sentence
carries one statement in at most 25 words, in active voice with a named actor. Use the
imperative for instructions, one term for one thing, and full verb forms. These rules
change how a sentence reads, not how many there are. Scope and examples:
[technical-english.md](references/technical-english.md).

## User Instructions

User instructions (CLAUDE.md, AGENTS.md, direct requests) take precedence over skills, subject to the host's system and developer instructions. If CLAUDE.md says "don't use TDD" and a skill says "always use TDD," follow the user. Once selected, follow the skill's workflow. The direct-path rules decide whether a workflow applies; they do not waive its safeguards.

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
