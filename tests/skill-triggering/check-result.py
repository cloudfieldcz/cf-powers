"""Check Claude stream-json discovery evidence, not implementation correctness."""
import argparse
import json
from pathlib import Path


def evaluate(path, skill, status, expectation):
    if status not in (0, 1):
        reason = 'timeout' if status in (124, 137) else f'process exited {status}'
        return 2, f'INFRA: {reason}'
    try:
        events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    except (OSError, ValueError) as error:
        return 2, f'INFRA: unreadable or malformed trace: {error}'
    if not events or any(not isinstance(event, dict) for event in events):
        return 2, 'INFRA: missing or invalid events'
    invoked = set()
    for event in events:
        message = event.get('message')
        if event.get('type') != 'assistant' or not isinstance(message, dict):
            continue
        content = message.get('content')
        if not isinstance(content, list):
            continue
        for block in content:
            if (isinstance(block, dict) and block.get('type') == 'tool_use'
                    and block.get('name') == 'Skill' and isinstance(block.get('input'), dict)):
                name = block['input'].get('skill')
                if isinstance(name, str):
                    invoked.add(name)
    found = any(name == skill or name.endswith(':' + skill) for name in invoked)
    results = [event for event in events if event.get('type') == 'result']
    terminal = results[0] if len(results) == 1 and results[0] == events[-1] else None
    if (terminal and terminal.get('subtype') == 'error_max_turns'
            and expectation == 'present' and found):
        return 3, f'INCOMPLETE: trigger {skill} observed; turn budget exhausted, task outcome unverified'
    if (terminal and terminal.get('subtype') == 'error_max_turns'
            and expectation == 'present' and status in (0, 1)):
        return 1, f'FAIL: trigger {skill} expected present; not observed before turn budget exhausted'
    if status:
        return 2, f'INFRA: process exited {status}'
    if (not terminal or terminal.get('subtype') != 'success'
            or terminal.get('is_error') is not False):
        return 2, 'INFRA: missing successful terminal result'
    passed = found == (expectation == 'present')
    return (0 if passed else 1), (
        f'{"PASS" if passed else "FAIL"}: trigger {skill} expected {expectation}; '
        f'observed {sorted(invoked)}. Task outcome requires separate verification.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log', type=Path)
    parser.add_argument('skill')
    parser.add_argument('status', type=int)
    parser.add_argument('expectation', choices=['present', 'absent'])
    args = parser.parse_args()
    code, message = evaluate(args.log, args.skill, args.status, args.expectation)
    print(message)
    raise SystemExit(code)
