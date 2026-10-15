# Maintainer collaboration and scope guidance

CF Powers applies a small set of maintainer-approved collaboration and delivery rules.
The rules keep the existing language policy, workflow gates, and verification requirements.

## Behavior

- Dialogue starts with the useful point and a clear recommendation.
- The agent labels hypotheses and explains what an answer would change.
- Analysis compares real tradeoffs without a fixed number of alternatives or words.
- Designs record safe omissions and concrete conditions for revisiting them.
- Reviews connect requested changes to requirements or failure impacts.
- Verification checks representative results as well as test execution.

`using-superpowers` contains the conversation defaults in its Collaboration Defaults
section. Analysis, planning, review, and verification contain their own applicable rules.
These rules add no approval stage.

## Maintenance and verification

When scope expansion recurs, identify the responsible skill rule and add a behavioral
probe before you change it. Keep improvements within the authorized task scope.

Use the [collaboration probes](../tests/skill-triggering/collaboration-scenarios.md)
to check the behavior and its counterexamples. The
[test guide](testing.md) lists offline checks and live-run limitations.
