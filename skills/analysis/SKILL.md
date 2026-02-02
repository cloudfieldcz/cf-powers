---
name: analysis
description: MANDATORY before any implementation. Explores ideas through dialogue, then produces comprehensive technical analysis (Czech) with architecture, phases, risk analysis, and cross-check reviews.
---

# From Idea to Technical Analysis

## Overview

A single skill that takes you from a vague idea to a reviewed technical analysis document, ready for implementation planning. Combines collaborative dialogue (understanding what to build) with rigorous technical analysis (how to build it).

**Announce at start:** "I'm using the analysis skill to turn this idea into a technical analysis."

**Output:** `docs/plans/YYYY-MM-DD-<topic>.md` — a single document containing both the design rationale and the full technical analysis.

**Output language:** Czech (the document). Code examples and CLI commands remain in English.

## The Process

### Phase 1: Understanding the Idea

**Goal:** Understand what we're building and why before writing anything.

**If the user already has a clear spec or design doc** — skip to Phase 2. Not every idea needs 20 questions.

**If the idea is vague or open-ended:**

1. Check out the current project state first (files, docs, recent commits)
2. Ask questions **one at a time** to refine the idea
3. Prefer **multiple choice questions** when possible, open-ended is fine too
4. Focus on: purpose, constraints, success criteria, who benefits

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

### Phase 2: Codebase Exploration

Before writing anything, thoroughly explore the project:

- Find all files relevant to the proposed changes
- Note specific line numbers for code that will be modified
- Understand existing patterns, data models, and service layers
- Map integration points and dependencies
- Identify what will NOT change (equally important)

### Phase 3: Write the Analysis Document

Write in Czech. Follow this document structure:

```markdown
# <Topic> — <Stručný popis>

## Popis

Co se buduje a proč.

### Proč

- Motivace (bullet points)
- Business hodnota
- Technický dluh který se řeší

## Aktuální stav

Jak věci fungují dnes. Zahrňte:
- Relevantní code paths s file:line referencemi
- Data flow diagramy (ASCII nebo popis)
- Současná omezení

| Aspekt | Současný stav | Navrhovaný stav |
|--------|--------------|-----------------|
| ... | ... | ... |

## Návrh řešení

### Architektura

Celkový přístup. Diagramy kde to pomáhá.

### Databázové změny (pokud jsou)

Definice tabulek s kompletním DDL:

| Sloupec | Typ | Popis |
|---------|-----|-------|
| ... | ... | ... |

Migrační skripty, seed data.

### Změny v servisní vrstvě

Nové služby, upravené služby. Signatury metod.
DI registrace.

### Změny v UI (pokud jsou)

Nové views/stránky, navigace.

### Konfigurace

Nové config hodnoty, feature flagy.

## Dotčené soubory

### Nové soubory
- `cesta/k/souboru.ext` — popis

### Upravené soubory
- `cesta/k/souboru.ext:123-145` — co se mění a proč

### Soubory BEZ změn (důležité)
- `cesta/k/souboru.ext` — proč není třeba měnit

## Implementační fáze

Logické celky, NE micro-tasky (ty patří do writing-plans).
Každá fáze je koherentní kus práce.
**Každá fáze se stane separátním plan souborem** při writing-plans.

### Fáze 1: <Název>
- Co je zahrnuto
- Očekávaný výsledek
- Závislosti na jiných fázích
- [ ] Checklist hlavních kroků

### Fáze 2: <Název>
- ...

## Rizika a mitigace

| Riziko | Dopad | Pravděpodobnost | Mitigace |
|--------|-------|-----------------|----------|
| ... | ... | ... | ... |

## Testování

### Unit testy
- Seznam testovacích scénářů s očekávaným chováním

### Integrační / manuální testy
- End-to-end scénáře

### Verifikace
- Příkazy ke spuštění (build, test suite)
- Grep kontroly na zbylé hardcoded hodnoty apod.

## Poznámky

Idempotence, edge cases, výkonnostní úvahy, zpětná kompatibilita.

## Reference

- Odkazy na relevantní dokumentaci
- Odkazy na podobné implementace v codebase
```

### Phase 4: Validate Completeness

Before saving, verify the analysis covers all of the following:
- [ ] Problem description with rationale (Popis + Proč)
- [ ] Current state analysis with file:line references (Aktuální stav)
- [ ] Proposed solution with architecture (Návrh řešení)
- [ ] Database changes with full DDL (if applicable)
- [ ] All affected files listed with line references (Dotčené soubory)
- [ ] Implementation phases as logical chunks (Implementační fáze)
- [ ] Risk analysis table (Rizika a mitigace)
- [ ] Testing strategy with specific test cases (Testování)
- [ ] Notes on edge cases and backward compatibility (Poznámky)

If any section is not applicable, explicitly note "N/A" with a brief reason rather than omitting it.

### Phase 5: Save and Commit

Save the document to `docs/plans/YYYY-MM-DD-<topic>.md`. Commit to git.

### Phase 6: Dispatch Cross-Check Reviews

**REQUIRED:** After saving, dispatch two review subagents in parallel using the Task tool.

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

### Phase 7: Incorporate Feedback

After both reviewers return:

1. Present combined feedback to the user
2. Discuss which feedback to incorporate vs. dismiss (with reasoning)
3. Update the analysis document with agreed changes
4. Save the updated version

### Phase 8: Handoff

**"Analýza je hotová a prošla cross-checkem. Jak chcete pokračovat?"**

Options:
- **Create implementation plan** → Invoke `cf-powers:writing-plans`
- **Create isolated worktree first** → Invoke `cf-powers:using-git-worktrees`, then `cf-powers:writing-plans`
- **Not yet** — share with team, get additional review, iterate further

## Key Principles

- **Skip what's not needed** — If the user arrives with a clear spec, skip Phase 1 dialogue and go straight to codebase exploration + analysis.
- **One question at a time** — During Phase 1, never overwhelm with multiple questions.
- **Phases, not micro-tasks** — Analysis groups work into logical phases. Micro-task breakdown belongs in writing-plans.
- **File:line references** — Every affected file must have specific line references. Vague references are not acceptable.
- **Czech output** — The analysis document is in Czech. Code examples and CLI commands stay in English.
- **Cross-check is mandatory** — Never skip the BA + Dev review dispatch.
- **Verify before writing** — Read the actual code before claiming anything about it. Do not guess file paths or line numbers.
- **YAGNI ruthlessly** — Remove unnecessary features from all designs.
