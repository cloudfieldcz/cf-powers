---
name: analysis
description: Use for non-trivial implementations involving design choices, multiple components, or unclear requirements. Explores ideas through dialogue, then produces a technical analysis with architecture, phases, risks, and cross-check reviews. SKIP for mechanical/single-file changes (Dockerfile, CI YAML, config tweak, one-liner) or when the user has already specified exactly what to build.
---

# From Idea to Technical Analysis

## Overview

A single skill that takes you from a vague idea to a reviewed technical analysis document, ready for implementation planning. Combines collaborative dialogue (understanding what to build) with rigorous technical analysis (how to build it).

**Announce at start:** "I'm using the analysis skill to turn this idea into a technical analysis."

**Output:** `docs/plans/YYYY-MM-DD-<topic>.md` — a single document containing both the design rationale and the full technical analysis.

**Output language:** English (document, dialogue, and all skill artifacts).

## The Process

### Phase 1: Understanding the Idea

**Goal:** Understand what we're building and why before writing anything.

**If the user already has a clear spec or design doc** — skip to Phase 2. Not every idea needs 20 questions.

**If the idea is vague or open-ended:**

1. Check out the current project state first (files, docs, recent commits)
2. Before asking detailed questions, assess scope: if the request describes multiple independent subsystems (e.g., "build a platform with chat, file storage, billing, and analytics"), flag this immediately. Don't spend questions refining details of a project that needs to be decomposed first.
3. If the project is too large for a single analysis, help the user decompose into sub-projects: what are the independent pieces, how do they relate, what order should they be built? Then analyze the first sub-project through the normal flow. Each sub-project gets its own analysis → plan → implementation cycle.
4. For appropriately-scoped projects, ask questions **one at a time** to refine the idea
5. Prefer **multiple choice questions** when possible, open-ended is fine too
6. Focus on: purpose, constraints, success criteria, who benefits

**Exploring approaches:**

- Propose **2-3 different approaches** with trade-offs
- Lead with your recommended option and explain why
- Let the user pick before moving on

**Validating the design direction:**

- Once you believe you understand what to build, summarize it in **200-300 words**
- Ask: "Does this capture what you have in mind?"
- Iterate until the user confirms

**Key principles for Phase 1:**
- **One question at a time** — don't overwhelm
- **YAGNI ruthlessly** — remove unnecessary features
- **Explore alternatives** — always propose 2-3 approaches before settling

**Design for isolation and clarity:**

- Break the system into smaller units that each have one clear purpose, communicate through well-defined interfaces, and can be understood and tested independently
- For each unit, you should be able to answer: what does it do, how do you use it, and what does it depend on?
- Can someone understand what a unit does without reading its internals? Can you change the internals without breaking consumers? If not, the boundaries need work.
- Smaller, well-bounded units are also easier for you to work with — you reason better about code you can hold in context at once, and your edits are more reliable when files are focused.

**Working in existing codebases:**

- Explore the current structure before proposing changes. Follow existing patterns.
- Where existing code has problems that affect the work (e.g., a file that's grown too large, unclear boundaries, tangled responsibilities), include targeted improvements as part of the design — the way a good developer improves code they're working in.
- Don't propose unrelated refactoring. Stay focused on what serves the current goal.

### Phase 2: Codebase Exploration

Before writing anything, thoroughly explore the project:

- Find all files relevant to the proposed changes
- Note specific line numbers for code that will be modified
- Understand existing patterns, data models, and service layers
- Map integration points and dependencies
- Identify what will NOT change (equally important)

### Phase 3: Write the Analysis Document

Write in English. Follow this document structure:

```markdown
# <Topic> — <Short description>

## Overview

What is being built and why.

### Why

- Motivation (bullet points)
- Business value
- Technical debt being addressed

## Current state

How things work today. Include:
- Relevant code paths with file:line references
- Data flow diagrams (ASCII or description)
- Current limitations

| Aspect | Current state | Proposed state |
|--------|---------------|----------------|
| ... | ... | ... |

## Proposed solution

### Architecture

Overall approach. Diagrams where they help.

### Database changes (if any)

Table definitions with complete DDL:

| Column | Type | Description |
|--------|------|-------------|
| ... | ... | ... |

Migration scripts, seed data.

### Service layer changes

New services, modified services. Method signatures and interfaces only — NO implementation code.
DI registration.

### UI changes (if any)

New views/pages, navigation.

### Configuration

New config values, feature flags.

## Affected files

### New files
- `path/to/file.ext` — description

### Modified files
- `path/to/file.ext:123-145` — what changes and why

### Unchanged files (important)
- `path/to/file.ext` — why no change is needed

## Implementation phases

Logical chunks, NOT micro-tasks (those belong in writing-plans).
Each phase is a coherent unit of work.
**Each phase becomes a separate plan file** in writing-plans.

### Phase 1: <Name>
- What is included
- Expected outcome
- Dependencies on other phases
- [ ] Checklist of main steps

### Phase 2: <Name>
- ...

## Risks and mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| ... | ... | ... | ... |

## Testing

### Unit tests
- List of test scenarios with expected behavior

### Integration / manual tests
- End-to-end scenarios

### Verification
- Commands to run (build, test suite)
- Grep checks for remaining hardcoded values, etc.

## Notes

Idempotence, edge cases, performance considerations, backward compatibility.

## References

- Links to relevant documentation
- Links to similar implementations in the codebase
```

### Phase 4: Validate Completeness

Before saving, verify the analysis covers all of the following:
- [ ] Problem description with rationale (Overview + Why)
- [ ] Current state analysis with file:line references (Current state)
- [ ] Proposed solution with architecture (Proposed solution)
- [ ] Database changes with full DDL (if applicable)
- [ ] All affected files listed with line references (Affected files)
- [ ] Implementation phases as logical chunks (Implementation phases)
- [ ] Risk analysis table (Risks and mitigations)
- [ ] Testing strategy with specific test cases (Testing)
- [ ] Notes on edge cases and backward compatibility (Notes)

If any section is not applicable, explicitly note "N/A" with a brief reason rather than omitting it.

### Phase 5: Save and Commit

Save the document to `docs/plans/YYYY-MM-DD-<topic>.md`. Commit to git.

### Phase 6: Dispatch Cross-Check Reviews

**REQUIRED:** After saving, dispatch four review subagents in parallel using the Task tool.
Leave their model unset so they inherit the session's default (Opus) — review is
the one tier that is never downgraded, per cf-powers:choosing-subagent-models.

**Business Analyst Review:**
```
Task tool:
  subagent_type: general-purpose
  description: "BA review of analysis"
  prompt: >
    You are a Business Analyst reviewer.
    Read and follow the cf-powers:review-as-ba skill exactly.

    Document to review: docs/plans/YYYY-MM-DD-<topic>.md

    Provide your structured review following the skill's output format.
```

**Developer Review:**
```
Task tool:
  subagent_type: general-purpose
  description: "Dev review of analysis"
  prompt: >
    You are a Developer reviewer.
    Read and follow the cf-powers:review-as-dev skill exactly.

    Document to review: docs/plans/YYYY-MM-DD-<topic>.md

    Read the actual codebase to verify all claims. Provide your structured review
    following the skill's output format.
```

**Security Review:**
```
Task tool:
  subagent_type: general-purpose
  description: "Security review of analysis"
  prompt: >
    You are a Security Engineer reviewer.
    Read and follow the cf-powers:review-as-security skill exactly.

    Document to review: docs/plans/YYYY-MM-DD-<topic>.md

    Read the actual codebase to verify security claims. Check CLAUDE.md for
    project-specific security invariants. Provide your structured review
    following the skill's output format.
```

**Performance Review:**
```
Task tool:
  subagent_type: general-purpose
  description: "Performance review of analysis"
  prompt: >
    You are a Performance Engineer reviewer.
    Read and follow the cf-powers:review-as-perf skill exactly.

    Document to review: docs/plans/YYYY-MM-DD-<topic>.md

    Read the actual schema, queries, and code to verify performance claims.
    Provide your structured review following the skill's output format.
```

### Phase 7: Incorporate Feedback

After all reviewers return:

1. Present combined feedback to the user
2. Discuss which feedback to incorporate vs. dismiss (with reasoning)
3. Update the analysis document with agreed changes
4. Save the updated version

### Phase 8: Handoff

**"Analysis is complete and has passed cross-check review. How would you like to proceed?"**

Options:
- **Create implementation plan** → Invoke `cf-powers:writing-plans`
- **Not yet** — share with team, get additional review, iterate further

## Key Principles

- **Skip what's not needed** — If the user arrives with a clear spec, skip Phase 1 dialogue and go straight to codebase exploration + analysis.
- **One question at a time** — During Phase 1, never overwhelm with multiple questions.
- **Phases, not micro-tasks** — Analysis groups work into logical phases. Micro-task breakdown belongs in writing-plans.
- **NO implementation code** — Analysis describes WHAT and WHY, not HOW in code. Do not write implementation code, function bodies, or full code blocks. Use only: method signatures, interface definitions, pseudo-code, and short illustrative snippets. Detailed code belongs in the plan phase (writing-plans skill).
- **File:line references** — Every affected file must have specific line references. Vague references are not acceptable.
- **English output** — All artifacts and dialogue produced by this skill are in English.
- **Cross-check is mandatory** — Never skip the BA + Dev + Security + Performance review dispatch.
- **Verify before writing** — Read the actual code before claiming anything about it. Do not guess file paths or line numbers.
- **YAGNI ruthlessly** — Remove unnecessary features from all designs.
