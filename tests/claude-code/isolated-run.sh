#!/usr/bin/env bash
# Run claude without user settings, CLAUDE.md or MCP servers. Authentication comes from the
# active login (macOS Keychain), CLAUDE_CODE_OAUTH_TOKEN, ANTHROPIC_API_KEY, or a credentials
# file in a temporary config dir when CF_POWERS_TEST_CREDENTIALS_FILE is set.
set -euo pipefail
limit=$1
shift
if command -v timeout >/dev/null 2>&1; then
    timeout_cmd=timeout
elif command -v gtimeout >/dev/null 2>&1; then
    timeout_cmd=gtimeout
else
    echo "isolated-run.sh: neither timeout nor gtimeout found (macOS: brew install coreutils)" >&2
    exit 1
fi
if [ -n "${CF_POWERS_TEST_CREDENTIALS_FILE:-}" ]; then
    test_config=$(mktemp -d "${TMPDIR:-/tmp}/cf-powers-claude-config.XXXXXX")
    trap 'rm -rf "$test_config"' EXIT
    cp "$CF_POWERS_TEST_CREDENTIALS_FILE" "$test_config/.credentials.json"
    chmod 600 "$test_config/.credentials.json"
    export CLAUDE_CONFIG_DIR="$test_config"
fi
if [ -n "${CF_POWERS_TEST_MODEL:-}" ]; then
    set -- --model "$CF_POWERS_TEST_MODEL" "$@"
fi
"$timeout_cmd" "$limit" claude \
    --setting-sources "" --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
    "$@"
