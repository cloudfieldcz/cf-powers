#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "${SCRIPT_DIR}/test_contracts.py"
if [ "${1:-}" = "--native" ]; then
    python3 "${SCRIPT_DIR}/test_native_install.py"
elif [ "$#" -ne 0 ]; then
    echo "usage: $0 [--native]" >&2
    exit 2
fi
