---
name: review-as-ba
description: Use when reviewing a technical analysis, design document, or specification from a business analyst perspective - checking requirements completeness, user workflows, edge cases, and business logic
---

# Review as Business Analyst

## Overview

Review a technical analysis or specification document from a business analyst perspective. Focus on whether the document completely and correctly captures business requirements, user workflows, and edge cases.

**Announce at start:** "I'm reviewing this document as a Business Analyst."

## Input

- Technical analysis document (typically `docs/analysis/YYYY-MM-DD-<topic>.md`)
- Original design document (if available, `docs/plans/YYYY-MM-DD-<topic>-design.md`)

## Review Checklist

### 1. Requirements Completeness
- Are all requirements from the design doc reflected in the analysis?
- Are there implied requirements that were not captured?
- Is the scope clearly defined (what is IN and OUT)?
- Are acceptance criteria clear enough to verify?

### 2. User Workflow Consistency
- Does the proposed solution cover the complete user journey?
- Are all user-facing changes described?
- Is the workflow intuitive and consistent with existing patterns?
- Are state transitions documented and complete?

### 3. Edge Cases and Error Scenarios
- What happens when things go wrong?
- Are boundary conditions addressed?
- Is error messaging user-friendly?
- Are concurrent usage scenarios considered?
- What about empty states, first-time use, data migration?

### 4. Business Logic Gaps
- Are all business rules documented?
- Are calculations/formulas correct and complete?
- Are there implicit assumptions that should be explicit?
- Do the proposed defaults make business sense?

### 5. Phase Prioritization
- Are the phases ordered by business value?
- Is there a viable MVP in phase 1?
- Can phases be delivered independently?
- Are dependencies between phases documented?

### 6. Data Integrity
- Is data migration addressed?
- Are backward compatibility concerns noted?
- What happens to existing data?
- Are there data validation rules that need to be defined?

## Output Format

Structure your review exactly like this:

```markdown
# BA Review: <topic>

## Shrnutí
[1-2 sentence overall assessment]

## Pokrytí požadavků
- ✅ [Requirement that is well covered]
- ❌ [Missing or incomplete requirement -- explain what's missing]

## Uživatelské workflow
- ✅ [Workflow that is complete and consistent]
- ❌ [Workflow gap or inconsistency]

## Nepokryté edge cases
- ❌ [Edge case 1 -- what could go wrong]
- ❌ [Edge case 2 -- boundary condition]

## Otázky k business logice
1. [Question about business rule or assumption]
2. [Clarification needed about behavior]

## Hodnocení fází
- Fáze 1: [Assessment -- is it a viable MVP?]
- Fáze 2: [Assessment -- correct priority?]

## Doporučení
1. [Actionable recommendation]
2. [Actionable recommendation]

## Verdikt
**Kvalita analýzy:** [Kompletní / Potřebuje revizi / Zásadní mezery]
**Doporučený postup:** [Pokračovat k plánování / Zapracovat feedback / Potřebuje přepracování]
```

## Key Principles

- **Be specific** -- Reference sections/tables in the analysis by name
- **Questions over assumptions** -- If something is unclear, ask rather than assume
- **Business value focus** -- Prioritize feedback that affects business outcomes
- **Constructive tone** -- Acknowledge what is done well, then identify gaps
- **Actionable feedback** -- Every concern should have a suggested resolution
