---
name: review-as-dev
description: Use when reviewing a technical analysis, design document, or specification from a developer perspective - checking technical feasibility, architecture, integration points, and performance/security
---

# Review as Developer

## Overview

Review a technical analysis or specification document from a senior developer perspective. Focus on whether the proposed solution is technically sound, feasible, and addresses architecture, performance, and security concerns.

**Announce at start:** "I'm reviewing this document as a Developer."

## Input

- Technical analysis document (typically `docs/analysis/YYYY-MM-DD-<topic>.md`)
- The actual codebase (read relevant files to verify claims in the analysis)

## Review Checklist

### 1. Code Verification (DO THIS FIRST)

**CRITICAL:** Do not trust the analysis at face value. Read the actual codebase to verify:
- Are the file:line references accurate?
- Do the claimed existing patterns actually exist in the code?
- Are the "files WITHOUT changes" truly unaffected?
- Is the proposed approach compatible with the actual code?

### 2. Technical Feasibility
- Is the proposed architecture realistic?
- Are the technology choices appropriate?
- Are there simpler alternatives that were not considered?
- Do the estimated phases seem realistic?

### 3. Architecture Concerns
- Does the solution fit the existing architecture?
- Are SOLID principles respected?
- Is the separation of concerns appropriate?
- Are there coupling issues or circular dependencies?
- Is the DI registration plan correct?

### 4. Missing Technical Details
- Are database indexes defined for query patterns?
- Are transaction boundaries specified?
- Is concurrency handling addressed?
- Are connection/resource lifetimes correct?
- Are migrations reversible?

### 5. Integration Points
- Are all integration points identified?
- Are API contracts (method signatures) complete?
- Will existing callers break?
- Are backward compatibility concerns addressed?
- Is the "files WITHOUT changes" section accurate?

### 6. Performance and Security
- Are there N+1 query risks?
- Is caching strategy appropriate?
- Are there potential memory issues (large data sets)?
- Is input validation sufficient?
- Are authorization checks in place?
- Are sensitive data handled correctly?

## Output Format

Structure your review exactly like this:

```markdown
# Dev Review: <topic>

## Shrnutí
[1-2 sentence overall technical assessment]

## Architektura
- ✅ [Sound architectural decision]
- ❌ [Architecture concern -- explain why and suggest alternative]

## Technické mezery
- ❌ [Missing technical detail -- what needs to be specified]
- ❌ [Incorrect assumption -- what the code actually does at file:line]

## Integrační rizika
- ❌ [Integration point that may break]
- ❌ [Missing API contract detail]

## Výkon / Bezpečnost
- ❌ [Performance concern with suggested mitigation]
- ❌ [Security concern with suggested fix]

## Ověření proti kódu
- ✅ [Verified: file:line reference is accurate]
- ❌ [Incorrect: file:line actually does X, not Y as claimed]

## Technické otázky
1. [Question about implementation approach]
2. [Clarification about technical decision]

## Doporučení
1. [Actionable technical recommendation]
2. [Actionable technical recommendation]

## Verdikt
**Technická kvalita:** [V pořádku / Drobné problémy / Zásadní problémy]
**Doporučený postup:** [Pokračovat k plánování / Zapracovat feedback / Potřebuje přepracování architektury]
```

## Key Principles

- **Verify against code** -- Always read the actual files referenced in the analysis
- **Specific references** -- Use file:line when pointing out issues
- **Pragmatic** -- Focus on real risks, not theoretical perfection
- **Alternative proposals** -- When flagging an issue, suggest a better approach
- **Security mindset** -- Think about what could go wrong in production
