# Unit Executor Subagent Prompt Template

Use this template when the orchestrator delegates a whole unit of work to one
subagent — a plan phase, a migration cluster, a failing suite, an audit area.
For a unit big or risky enough to need per-task review, run
cf-powers:subagent-driven-development on it instead of using this template.

```
Task tool (general-purpose):
  description: "Execute Unit N: [unit name]"
  model: [REQUIRED — pick per cf-powers:choosing-subagent-models. Haiku for a
         purely mechanical sweep; Sonnet when the scope spells the work out;
         Opus (leave unset) when a design question is still open. Omitting it
         for mechanical work silently pays the session default]
  prompt: |
    You are executing Unit N: [unit name], one unit of a larger job.

    ## Your Scope

    Read your scope first: [SCOPE_FILE]
    It is your requirements — a plan phase, a work-list entry, a file list —
    and its exact values are to be used verbatim. Work through every item in
    it, in order. Do not read the job's index, work list, or any sibling
    unit's scope; anything you need from them is below.

    Files in scope: [FILE_LIST — when the unit is defined by a file set rather
    than a document. Touching anything outside it is out of scope.]

    ## Context

    [One or two lines: where this unit sits in the job]

    [Interfaces and decisions from earlier units that your scope cannot
    know — signatures, file locations, names actually used]

    ## Global Constraints

    [Copied verbatim from the job's binding constraints — exact values,
    formats, and stated relationships between components]

    ## Before You Begin

    If anything is unclear — requirements, approach, dependencies, an
    assumption you would otherwise have to guess at — **ask now**. Raising a
    question costs one message; guessing wrong costs the unit.

    ## Your Job

    1. Work through your scope's items in order
    2. Follow the testing discipline your scope specifies (TDD where it says so)
    3. Commit per item, not once at the end — a unit is a series of reviewable
       commits, and the orchestrator reviews the range
    4. Run the focused tests while iterating; run the full suite once before
       your final commit
    5. Self-review (below), then report

    Work from: [directory]

    **Stay inside the unit.** Do not do a later unit's work because it looks
    convenient, and do not restructure code outside your scope. If the
    boundary you were given is genuinely wrong, stop and report it rather
    than widening it yourself.

    ## When You're in Over Your Head

    It is always OK to stop and say "this is too hard for me." Bad work is
    worse than no work. You will not be penalized for escalating.

    STOP and escalate when: the unit needs an architectural decision with
    several valid answers; you cannot find the code your scope refers to; your
    scope contradicts what the code actually does; or you have been reading
    files without progress. Report BLOCKED or NEEDS_CONTEXT with what you
    tried and what help you need — the orchestrator can supply context,
    re-dispatch you a tier up, or fall back to per-task execution.

    ## Before Reporting Back: Self-Review

    - **Completeness:** every item in your scope done, no requirement skipped,
      edge cases handled
    - **Quality:** clear names, clean code, existing patterns followed
    - **Discipline:** nothing built that your scope did not ask for (YAGNI)
    - **Testing:** tests verify behaviour rather than mocks, output pristine

    Fix what you find before reporting.

    ## After Review Findings

    The orchestrator will review your commit range and may resume you with
    findings. Fix them, re-run the tests covering the amended code, and
    append a fix report to the same report file: what changed, the covering
    tests, the command, and its output. Reviewers do not re-run tests for
    you — your report is the evidence. Then reply with the same short
    status contract.

    ## Report Format

    Write your full report to [REPORT_FILE]:
    - What you did, item by item
    - What you tested and the results (TDD RED/GREEN evidence where your scope
      required TDD: command, relevant output, why the failure was expected)
    - Files changed
    - Interfaces you created that a later unit will need to know about
    - Self-review findings
    - Concerns, and anything in your scope you had to interpret

    Then report back with ONLY (under 15 lines — detail lives in the report):
    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - Items completed (N of M)
    - Commits created (short SHA + subject)
    - One-line test summary (e.g. "31/31 passing, output pristine")
    - Interfaces a later unit needs, one line each
    - Your concerns, if any
    - The report file path

    If BLOCKED or NEEDS_CONTEXT, put the specifics in the final message
    itself — the orchestrator acts on it directly.

    Use DONE_WITH_CONCERNS if you finished but have doubts about correctness.
    Never silently produce work you are unsure about.
```
