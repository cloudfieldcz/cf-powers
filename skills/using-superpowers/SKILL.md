---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

# Using Superpowers

**Runtime:** Before using host tools or dispatching, read [runtime operations](references/runtime.md) and its active-host reference (once per context). Keep this skill's workflow decisions unchanged.

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — including clarifying questions, exploring the codebase, or checking files. Even a 1% chance a skill might apply means you invoke it to check. If it turns out wrong for the situation, you don't have to use it.

Then announce "Using [skill] to [purpose]" and follow the skill exactly. If it has a checklist, create a native todo per item (or track it in the existing ledger).

Use the active runtime's skill-loading mechanism from [runtime operations](references/runtime.md). Claude uses its native Skill tool; Codex can read the resolved skill file when that is its exposed mechanism.

## Red Flags

These thoughts mean STOP—you're rationalizing past a skill that applies:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions about non-trivial work are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill clearly applies, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action on non-trivial work = task. Check for skills. |
| "I'll just do this one thing first" | Check BEFORE doing anything non-trivial. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Skip Flags

These thoughts mean GO DIRECT—forcing a skill here is overhead, not discipline:

| Thought | Reality |
|---------|---------|
| "This is one mechanical file write" | Add the file. No skill triage needed. |
| "User specified exactly what to do" | Execute it. They don't need design dialogue. |
| "No design choices involved" | No `analysis`. No `writing-plans`. Just do it. |
| "It's a single config tweak / one-liner" | Edit it. A skill check costs more than the task. |
| "It's a direct factual question" | Answer it. Skills are for *doing*, not chatting. |
| "Read-only exploration of one file/path" | Read it and report. Skills don't gate looking. |
| "Routine git/shell I've been authorized for" | Run it. The skill rules cover *judgment*, not muscle memory. |

**How the two tables relate:** Red Flags catches rationalizing *away* from skills that apply. Skip Flags catches rationalizing *into* skills that don't. Both errors waste the user's time. If a task matches Skip Flags clearly, name it in one short sentence ("going direct — single config file, no design choices") and proceed. If the user disagrees, they'll redirect.

## Skill Priority

When multiple skills apply, process skills come first — they set the approach, then implementation skills carry it out.

- "Let's build X" → cf-powers:analysis first, then implementation skills.
- "Fix this bug" → cf-powers:systematic-debugging first, then domain skills.

## Comments in Code You Write

A comment earns its place only by saying what the line cannot: a non-local coupling, a
refusal the code implies but never names, why the obvious simpler version is wrong. Cut
the rest — restating the code, narrating the flow, background, section banners, ALL-CAPS
emphasis, a module docstring that tells the feature's story. Long rationale belongs in the
project's docs, where it can be found and maintained. Past roughly one comment line per ten
lines of code you are writing prose. The surrounding file is not the standard: write the
new comment short even where the one above it runs six lines.

## User Instructions

User instructions (CLAUDE.md, AGENTS.md, direct requests) take precedence over skills, subject to the host's system and developer instructions. If CLAUDE.md says "don't use TDD" and a skill says "always use TDD," follow the user. Only skip a skill's workflow when your human partner has explicitly told you to.

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
