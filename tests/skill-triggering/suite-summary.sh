#!/usr/bin/env bash
PASSED=0
FAILED=0
INFRA=0
INCOMPLETE=0

record_result() {
    case "$2" in
        0) PASSED=$((PASSED + 1)); echo "PASS: $1" ;;
        1) FAILED=$((FAILED + 1)); echo "FAIL: $1" ;;
        3) INCOMPLETE=$((INCOMPLETE + 1)); echo "INCOMPLETE: $1 (trigger observed; task not completed)" ;;
        *) INFRA=$((INFRA + 1)); echo "INFRA: $1 (exit $2)" ;;
    esac
}

finish_summary() {
    echo "Passed: $PASSED"
    echo "Failed: $FAILED"
    echo "Infrastructure errors: $INFRA"
    echo "Incomplete after trigger: $INCOMPLETE"
    if [ "$FAILED" -gt 0 ]; then return 1; fi
    if [ "$INFRA" -gt 0 ]; then return 2; fi
    if [ "$INCOMPLETE" -gt 0 ]; then return 3; fi
    return 0
}
