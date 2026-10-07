import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

CHECKER = Path(__file__).with_name('check-result.py')
CALL = {'type': 'assistant', 'message': {'content': [
    {'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'cf-powers:analysis'}}]}}
SUCCESS = {'type': 'result', 'subtype': 'success', 'is_error': False}


class ResultTests(unittest.TestCase):
    def check(self, events, expected, status=0, expectation='present'):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / 'trace.jsonl'
            log.write_text('\n'.join(json.dumps(e) for e in events) + '\n')
            result = subprocess.run(['python3', str(CHECKER), str(log),
                                     'analysis', str(status), expectation],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            label = {0: 'PASS:', 1: 'FAIL:', 2: 'INFRA:', 3: 'INCOMPLETE:'}[expected]
            self.assertIn(label, result.stdout)
            return result.stdout

    def test_successful_invocation(self):
        self.check([CALL, SUCCESS], 0)

    def test_plain_skill_name(self):
        call = {'type': 'assistant', 'message': {'content': [
            {'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'analysis'}}]}}
        self.check([call, SUCCESS], 0)

    def test_missing_invocation(self):
        self.check([SUCCESS], 1)

    def test_negative_trigger(self):
        self.check([SUCCESS], 0, expectation='absent')
        self.check([CALL, SUCCESS], 1, expectation='absent')

    def test_quoted_tool_call_does_not_count(self):
        quote = {'type': 'assistant', 'message': {'content': [
            {'type': 'text', 'text': json.dumps(CALL)}]}}
        self.check([quote, SUCCESS], 1)

    def test_process_failure_after_invocation(self):
        self.assertIn('INFRA', self.check([CALL, SUCCESS], 2, status=1))

    def test_timeout_after_invocation(self):
        self.assertIn('timeout', self.check([CALL], 2, status=124))

    def test_truncated_output(self):
        self.check([CALL], 2)
        self.check([], 2)

    def test_host_error(self):
        self.check([CALL, {'type': 'result', 'subtype': 'error_during_execution',
                          'is_error': True}], 2)

    def test_trigger_confirmed_but_turn_budget_exhausted(self):
        budget = {'type': 'result', 'subtype': 'error_max_turns', 'is_error': True}
        self.check([CALL, budget], 3, status=1)
        self.check([budget], 1, status=1)
        self.check([budget], 1, status=0)
        self.check([CALL, budget], 2, status=124)
        self.check([budget], 2, status=1, expectation='absent')

    def test_malformed_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / 'trace.jsonl'
            log.write_text('not json\n')
            result = subprocess.run(['python3', str(CHECKER), str(log), 'analysis', '0', 'absent'],
                                    capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn(b"INFRA:", result.stdout)

    def test_runner_preserves_process_failure_and_separates_stderr(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / 'bin'
            bin_dir.mkdir()
            for name, script in {
                'claude': '#!/bin/sh\ncat "$CF_TEST_TRACE"\necho warning >&2\nexit "$CF_TEST_STATUS"\n',
                'timeout': '#!/bin/sh\nshift\nexec "$@"\n',
            }.items():
                path = bin_dir / name
                path.write_text(script)
                path.chmod(0o755)
            log = root / 'source.jsonl'
            log.write_text(json.dumps(CALL) + '\n' + json.dumps(SUCCESS) + '\n')
            prompt = root / 'prompt.txt'
            prompt.write_text('fixture')
            for status, expected in [(0, 0), (1, 2), (124, 2)]:
                env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'],
                           TMPDIR=str(root), CF_TEST_TRACE=str(log), CF_TEST_STATUS=str(status))
                runners = [CHECKER.with_name('run-test.sh'),
                           CHECKER.parent.parent / 'explicit-skill-requests/run-test.sh']
                for runner in runners:
                    result = subprocess.run(['bash', str(runner), 'analysis', str(prompt)],
                                            env=env, capture_output=True, text=True)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                if status == 0:
                    log.write_text(json.dumps(SUCCESS) + '\n')
                    result = subprocess.run(['bash', str(runners[0]), 'analysis', str(prompt),
                                             '12', 'absent', 'S1'], env=env,
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1, 'No-op agent must fail the outcome check')
                    log.write_text(json.dumps(CALL) + '\n' + json.dumps(SUCCESS) + '\n')



if __name__ == '__main__':
    unittest.main(verbosity=2)
