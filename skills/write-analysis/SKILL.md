---
name: write-analysis
description: Use when you have a brainstorming design doc or feature idea and need a comprehensive technical analysis before writing implementation plans - creates Czech-language analysis documents with architecture, phases, risk analysis, and cross-check reviews
---

# Writing Technical Analysis Documents

## Overview

Transform brainstorming output (design doc) into a comprehensive technical analysis document. The analysis is the bridge between "what we want to build" (brainstorming) and "how to build it step by step" (writing-plans).

**Announce at start:** "I'm using the write-analysis skill to create a technical analysis."

**Input:** Design document from brainstorming (typically `docs/plans/YYYY-MM-DD-<topic>.md`) or a feature description from the user.

**Output language:** Czech (the analysis document). Code examples remain in English.

**Modifies:** The existing `docs/plans/YYYY-MM-DD-<topic>.md` — extends the brainstorming design with analysis sections. If no brainstorming doc exists, creates a new one.

## The Process

### Step 1: Understand the Input

- Read the brainstorming design doc at `docs/plans/YYYY-MM-DD-<topic>.md` (if available)
- Ask the user clarifying questions if anything is ambiguous
- Identify which parts need deeper technical investigation

### Step 2: Explore the Codebase

Before writing anything, thoroughly explore the project:
- Find all files relevant to the proposed changes
- Note specific line numbers for code that will be modified
- Understand existing patterns, data models, and service layers
- Map integration points and dependencies
- Identify what will NOT change (equally important)

### Step 3: Write the Analysis Document

Write in Czech. Follow this document structure:

```markdown
# <Topic> — <Stručný popis>

## Popis

Co se buduje a proč. Odkaz na design dokument pokud existuje.

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

- Odkaz na design dokument
- Odkazy na relevantní dokumentaci
- Odkazy na podobné implementace v codebase
```

### Step 4: Validate Completeness

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

### Step 5: Save the Document

Update the existing `docs/plans/YYYY-MM-DD-<topic>.md` — append the analysis sections after the brainstorming design content. If no brainstorming doc exists, create `docs/plans/YYYY-MM-DD-<topic>.md` from scratch.

### Step 6: Dispatch Cross-Check Reviews

**REQUIRED:** After saving, dispatch two review subagents in parallel using the Task tool.

Both agents run simultaneously (they are independent — BA reviews business aspects, Dev reviews technical aspects):

**Business Analyst Review:**
```
Task tool:
  subagent_type: general-purpose
  description: "BA review of analysis"
  prompt: >
    You are a Business Analyst reviewer.
    Read and follow the superpowers:review-as-ba skill exactly.

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
    Read and follow the superpowers:review-as-dev skill exactly.

    Document to review: docs/plans/YYYY-MM-DD-<topic>.md

    Read the actual codebase to verify all claims. Provide your structured review
    following the skill's output format.
```

### Step 7: Incorporate Feedback

After both reviewers return:

1. Present combined feedback to the user
2. Discuss which feedback to incorporate vs. dismiss (with reasoning)
3. Update the analysis document with agreed changes
4. Save the updated version

### Step 8: Handoff to Writing Plans

After feedback is incorporated:

**"Analýza je hotová a prošla cross-checkem. Chcete pokračovat vytvořením implementačního plánu?"**

- **If yes:** Invoke `superpowers:writing-plans` to create the detailed implementation plan from this analysis. The analysis document becomes the input spec for writing-plans.
- **If not yet:** The user may want to share with the team, get additional review, or iterate further.

## Key Principles

- **Phases, not micro-tasks** — Analysis groups work into logical phases. Micro-task breakdown (TDD steps, commits) belongs in writing-plans.
- **File:line references** — Every affected file must have specific line references. Vague references are not acceptable.
- **Czech output** — The analysis document is in Czech. Code examples and CLI commands stay in English.
- **Cross-check is mandatory** — Never skip the BA + Dev review dispatch.
- **Verify before writing** — Read the actual code before claiming anything about it. Do not guess file paths or line numbers.
- **Incremental validation** — For large analyses, present sections to the user as you write them and get confirmation before proceeding.
