---
name: review-as-security
description: Use when reviewing a technical analysis, design document, or specification from a security perspective - checking attack vectors, trust boundaries, authentication, data integrity, and fail-safe behavior
---

# Review as Security Engineer

## Overview

Review a technical analysis or specification document from a security engineer perspective. Focus on whether the proposed solution correctly handles trust boundaries, input validation, authentication, data integrity, and fail-safe behavior.

**Announce at start:** "I'm reviewing this document as a Security Engineer."

## Input

- Design + analysis document (typically `docs/plans/YYYY-MM-DD-<topic>.md`)
- The actual codebase (read relevant files to verify security claims)
- CLAUDE.md security-related sections (if project defines security invariants, they are absolute)

## Review Checklist

### 1. Security Invariant Compliance (DO THIS FIRST)

**CRITICAL:** Check if the project defines security invariants in CLAUDE.md. If so, verify every proposed change against them. Any violation is automatically CRITICAL.

Read the actual code paths affected by the proposed changes.

### 2. Attack Surface Analysis

- Can an attacker poison caches or shared state? (TOCTOU between validation and use)
- Can an attacker bypass validation? (race conditions, partial inputs, encoding tricks)
- Can an attacker serve or receive different data than what was validated? (hash/integrity verification)
- Can an attacker manipulate external responses? (TLS verification, redirect following, DNS rebinding)
- Can an attacker trigger denial of service? (large payloads, zip/tar bombs, unbounded allocations)
- Can an attacker exploit processing of untrusted input? (injection, deserialization, path traversal)

### 3. Trust Boundary Analysis

- Map all trust boundaries (client-server, service-to-service, internal-external, user-admin)
- Verify input validation at each boundary
- Check that data from untrusted sources is never used unsanitized
- Verify outputs from external services are validated before acting on them
- Check inter-process/inter-service channel security

### 4. Authentication and Authorization

- Are API endpoints properly authenticated?
- Is authorization checked at every access point (not just at the UI level)?
- Are credentials stored and transmitted securely?
- Is the UI protected against CSRF, XSS, session hijacking?
- Are there privilege escalation paths?
- Is the principle of least privilege followed?

### 5. Data Integrity and Cryptography

- Is sensitive data encrypted at rest and in transit?
- Are hashes/signatures verified end-to-end where needed?
- Are TLS certificates validated for external connections?
- Is there protection against downgrade attacks?
- Are cryptographic primitives used correctly (no custom crypto, proper key management)?

### 6. Secrets and Sensitive Data

- Are secrets excluded from logs and error messages?
- Are API keys, tokens, and credentials properly scoped?
- Is sensitive data masked in user-facing output?
- Are secrets managed through proper secret management (not hardcoded)?

### 7. Fail-Safe Behavior

- Do failures fail safe (deny by default) or fail open? Is the choice appropriate?
- What happens when external dependencies are unreachable?
- Are there timeouts on all external calls?
- Is there circuit-breaking for repeated failures?
- Are error messages safe (no stack traces, internal paths, or secrets leaked)?

## Output Format

Structure your review exactly like this:

```markdown
# Security Review: <topic>

## Shrnutí
[1-2 sentence security posture assessment]

## Bezpečnostní invarianty
- ✅ [Invariant maintained — cite evidence]
- CRITICAL: [Invariant violated — cite code, describe attack]
(If project has no defined invariants, note "Projekt nedefinuje explicitní bezpečnostní invarianty v CLAUDE.md")

## Plocha útoku
- HIGH: [Attack vector — scenario, impact, remediation]
- MEDIUM: [Defense-in-depth gap — describe and suggest improvement]

## Trust boundaries
- ✅ [Boundary with proper validation]
- HIGH: [Boundary with insufficient validation — describe risk]

## Autentizace a autorizace
- ✅ [Properly secured access point]
- HIGH: [Missing or insufficient auth check]

## Integrita dat a kryptografie
- ✅ [Correct integrity check]
- MEDIUM: [Missing or weak check]

## Tajné údaje a citlivá data
- ✅ [Properly handled secrets]
- HIGH: [Exposed or mishandled secret — describe risk]

## Chování při selhání
- ✅ [Correct fail-safe behavior]
- MEDIUM: [Missing timeout or circuit breaker]

## Bezpečnostní otázky
1. [Question about security design decision]
2. [Clarification about threat model assumption]

## Doporučení
1. [Actionable security recommendation — priority order]
2. [Actionable security recommendation]

## Verdikt
**Bezpečnostní posouzení:** [V pořádku / Potřebuje zlepšení / Kritické nedostatky]
**Doporučený postup:** [Pokračovat k plánování / Zapracovat feedback / Vyžaduje bezpečnostní redesign]
```

## Severity Levels

- **CRITICAL** — Security invariant violation or directly exploitable vulnerability
- **HIGH** — Significant security weakness that needs fixing before deployment
- **MEDIUM** — Defense-in-depth improvement
- **LOW** — Hardening suggestion

## Key Principles

- **Verify against code** — Always read the actual files; don't trust the analysis claims
- **Think like an attacker** — For each component, ask "how would I abuse this?"
- **Specific attack scenarios** — Don't say "could be vulnerable"; describe the exact attack path
- **Prioritize by exploitability** — Real risks over theoretical concerns
- **Defense in depth** — One control failing shouldn't compromise the system
- **Project invariants are sacred** — If CLAUDE.md defines security invariants, any violation is CRITICAL
