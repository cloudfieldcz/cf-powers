---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

**Runtime:** Before using host tools or dispatching, read [runtime operations](../using-superpowers/references/runtime.md) and its active-host reference (once per context). Keep this skill's workflow decisions unchanged.

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** Subagent-driven development (cf-powers:subagent-driven-development) produces significantly higher quality results. If subagents are available, prefer that skill over this one.

**For a multi-phase plan index (several phase plans under one index), prefer
cf-powers:orchestrator** — it delegates each phase to a subagent and reviews it,
so one session can drive the whole index without exhausting its context.

## The Process

### Step 0: Branch Check
1. Check current git branch: `git branch --show-current`
2. If on `main` or `master`: **STOP** — ask user to create/switch to a feature branch first
3. If on a feature branch: proceed
4. If the host provided a detached worktree: follow the runtime reference,
   preserve that workspace and its eventual integration handoff; do not create
   or switch a branch merely to satisfy this check.

### Step 1: Load and Review Plan

**For multi-phase plans (index exists):**
1. Read the **index file only** — understand phases, status, and dependencies
2. Identify the next phase to execute (first ⬚ Not started, respecting dependencies)
3. Read **only that phase's plan file** — do NOT load all phases at once
4. Review critically - identify any questions or concerns
5. If concerns: Raise them with your human partner before starting
6. If no concerns: Create native task tracking (or use the existing ledger) and proceed

**For single-phase plans:**
1. Read the plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create native task tracking (or use the existing ledger) and proceed

**Context loading principle:** Only load what you need for the current phase. If you need context from a previous phase's plan, read it on-demand, not upfront.

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each task exactly; run the red-green-commit loop yourself (cf-powers:test-driven-development) — the plan states the deliverable, contract and trap, not the steps
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use cf-powers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

**Note:** User manages their own branches. Step 0 verifies a feature branch exists — do NOT create worktrees automatically.
