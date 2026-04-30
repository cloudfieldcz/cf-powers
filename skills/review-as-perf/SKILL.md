---
name: review-as-perf
description: Use when reviewing a technical analysis, design document, or specification from a performance perspective - checking missing indexes, N+1 queries, algorithm complexity, memory usage, caching strategy, and scalability
---

# Review as Performance Engineer

## Overview

Review a technical analysis or specification document from a performance engineer perspective. Focus on whether the proposed solution will perform well under realistic load — checking database access patterns, algorithm complexity, memory usage, caching, and scalability.

**Announce at start:** "I'm reviewing this document as a Performance Engineer."

## Input

- Design + analysis document (typically `docs/plans/YYYY-MM-DD-<topic>.md`)
- The actual codebase (read relevant files to verify performance claims)

## Review Checklist

### 1. Database Access Patterns (DO THIS FIRST)

**CRITICAL:** This is the most common source of performance problems. Read the actual schema and queries.

- Are indexes defined for all columns used in WHERE, JOIN, ORDER BY, and GROUP BY?
- Are there N+1 query patterns? (loading related entities in a loop)
- Are queries fetching only needed columns, or SELECT *?
- Are there missing composite indexes for multi-column lookups?
- Are there full table scans on large tables?
- Are LIKE queries with leading wildcards used on unindexed columns?
- Are pagination queries efficient (keyset vs offset)?
- Are there unnecessary JOINs or subqueries that could be simplified?
- Are transaction scopes minimal (not holding locks longer than necessary)?

### 2. Algorithm and Data Structure Complexity

- Are there O(n²) or worse algorithms where O(n log n) or O(n) exists?
- Are there nested loops over large collections?
- Are there linear searches where a hash lookup would work?
- Are data structures appropriate for the access pattern? (list vs set vs map)
- Are there unnecessary copies of large data structures?
- Is sorting done efficiently and only when needed?

### 3. Memory and Resource Usage

- Are there unbounded collections that grow with input size?
- Are large objects held in memory longer than necessary?
- Is streaming used for large data sets, or is everything loaded at once?
- Are resources (connections, file handles, streams) properly closed/disposed?
- Are there potential memory leaks from event listeners, caches, or circular references?
- Is object allocation minimized in hot paths?

### 4. Caching Strategy

- Is caching applied where data is read frequently and changes rarely?
- Are cache invalidation rules correct and complete?
- Is there risk of serving stale data?
- Are cache key designs efficient (not too broad, not too narrow)?
- Is cache size bounded to prevent memory issues?
- Are cache hit/miss ratios measurable?

### 5. Network and I/O

- Are external calls batched where possible instead of one-by-one?
- Are there unnecessary serialization/deserialization round-trips?
- Is compression used for large payloads?
- Are connections pooled and reused?
- Are there appropriate timeouts on all external calls?
- Is there potential for thundering herd problems?

### 6. Scalability Concerns

- Does the design scale linearly with data growth?
- Are there bottlenecks that become single points of contention?
- Are background jobs/workers properly parallelized?
- Is the solution stateless or does it require sticky sessions?
- What happens at 10x current data volume? 100x?

### 7. Concurrency and Contention

- Are there lock contention points under concurrent access?
- Are database transactions competing for the same rows?
- Are there shared resources that become bottlenecks?
- Is optimistic vs pessimistic locking chosen appropriately?

## Output Format

Structure your review exactly like this:

```markdown
# Performance Review: <topic>

## Summary
[1-2 sentence performance assessment]

## Database access patterns
- ✅ [Well-indexed query pattern]
- CRITICAL: [Missing index — describe query, table size, expected impact]
- HIGH: [N+1 query pattern — describe loop, suggest eager loading/batch query]

## Algorithm complexity
- ✅ [Appropriate algorithm choice]
- HIGH: [Suboptimal algorithm — describe complexity, suggest alternative]
- MEDIUM: [Unnecessary work — describe and suggest optimization]

## Memory and resources
- ✅ [Efficient resource usage]
- HIGH: [Unbounded collection or memory leak risk — describe scenario]
- MEDIUM: [Opportunity to use streaming instead of loading all]

## Caching
- ✅ [Appropriate caching strategy]
- MEDIUM: [Missing cache opportunity — describe access pattern]
- MEDIUM: [Cache invalidation risk — describe staleness scenario]

## Network and I/O
- ✅ [Efficient I/O pattern]
- HIGH: [Unbatched external calls — describe N+1 HTTP/API pattern]
- MEDIUM: [Missing connection pooling or compression]

## Scalability
- ✅ [Scales well with data growth]
- HIGH: [Bottleneck at scale — describe what breaks at 10x/100x]

## Performance questions
1. [Question about expected data volume or access pattern]
2. [Clarification about load characteristics]

## Recommendations
1. [Actionable performance recommendation — priority order]
2. [Actionable performance recommendation]

## Verdict
**Performance assessment:** [OK / Needs optimization / Critical issues]
**Recommended next step:** [Proceed to planning / Incorporate feedback / Requires redesign of performance-critical parts]
```

## Severity Levels

- **CRITICAL** — Missing index on high-traffic query, O(n²) on large dataset, unbounded memory growth
- **HIGH** — N+1 queries, suboptimal algorithms, missing batching, scalability bottleneck
- **MEDIUM** — Missing cache opportunity, unnecessary work, optimization potential
- **LOW** — Minor efficiency improvement, premature optimization candidate

## Key Principles

- **Verify against code** — Read the actual schema, queries, and code; don't trust the analysis claims
- **Data-driven** — Reference table sizes, query frequency, and expected growth where possible
- **Indexes first** — Missing indexes are the #1 performance killer; check them first
- **Measure before optimizing** — Flag clear anti-patterns, but don't suggest micro-optimizations without evidence
- **Pragmatic** — A simple O(n²) on 20 items is fine; the same on 100k items is not
- **Scalability mindset** — Consider not just current load, but realistic growth scenarios
