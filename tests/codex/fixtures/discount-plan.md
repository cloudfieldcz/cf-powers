# Discount range validation

**Goal:** Enforce the existing discount percentage contract.
**Analysis:** [requirements.md](requirements.md)
**Architecture:** Keep the current pure function and unittest suite.

## Global Constraints

- Preserve valid 0..100 behavior and the apply_discount(total, percent) interface.
- No UI changes, dependencies, push, branch switches or publication.
- Keep the current branch as-is after completion; this integration choice is already made.

### Task 1: Reject invalid percentages

- [ ] **Delivers:** Percentages outside 0..100 raise ValueError.
**Files:** Modify discount.py and test_discount.py.
**Interfaces:** apply_discount(total, percent) -> discounted total; ValueError outside the range.
**Decisions:** Existing requirements.md is binding; retain the pure function.
**Trap:** Existing tests cover only valid percentages and pass before the fix.
**Verify:** python3 -B -m unittest discover -v, with negative and over-100 test cases.
