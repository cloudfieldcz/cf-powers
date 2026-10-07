import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent


class HarnessTests(unittest.TestCase):
    def test_summary_distinguishes_infrastructure_and_incomplete(self):
        for statuses, expected in [('0', 0), ('2', 2), ('3', 3), ('0 1 2 3', 1)]:
            result = subprocess.run(['bash', '-c',
                'source "$1"; shift; for rc in "$@"; do record_result fixture "$rc"; done; finish_summary',
                'test', str(HERE / 'suite-summary.sh'), *statuses.split()], capture_output=True, text=True)
            self.assertEqual(result.returncode, expected)
            self.assertIn('Infrastructure errors:', result.stdout)
            self.assertIn('Incomplete after trigger:', result.stdout)

    def test_trigger_repositories_have_real_inputs(self):
        for skill in ('analysis', 'systematic-debugging', 'test-driven-development',
                      'writing-plans', 'executing-plans', 'requesting-code-review', 'dispatching-parallel-agents'):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / 'repo'
                subprocess.run(['python3', str(HERE / 'prepare-fixture.py'), str(root), skill], check=True)
                self.assertTrue((root / 'CLAUDE.md').is_file())
                if skill in ('writing-plans', 'executing-plans'):
                    self.assertTrue((root / 'requirements.md').is_file())
                    self.assertEqual((root / 'docs/plans/validation-plan.md').is_file(), skill == 'executing-plans')
                if skill == 'requesting-code-review':
                    count = subprocess.check_output(['git', '-C', str(root), 'rev-list', '--count', 'HEAD'], text=True)
                    self.assertEqual(count.strip(), '2')
                if skill in ('systematic-debugging', 'dispatching-parallel-agents'):
                    result = subprocess.run(['python3', '-m', 'unittest', 'discover'], cwd=root, capture_output=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(b'FAILED', result.stderr)

    def test_claude_profile_is_isolated_and_cleaned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'user-profile'
            source.mkdir()
            (source / 'CLAUDE.md').write_text('UNRELATED USER INSTRUCTIONS')
            (source / 'settings.json').write_text('{"additionalDirectories":["/unrelated"]}')
            binary = root / 'claude'
            binary.write_text('''#!/usr/bin/env python3
import json,os,sys
from pathlib import Path
config=Path(os.environ['CLAUDE_CONFIG_DIR'])
Path(os.environ['CF_TEST_CAPTURE']).write_text(json.dumps({'args':sys.argv[1:],'config':str(config),'files':list(p.name for p in config.iterdir())}))
''')
            binary.chmod(0o755)
            capture = root / 'capture.json'
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ['PATH'],
                       CLAUDE_CONFIG_DIR=str(source), CF_TEST_CAPTURE=str(capture),
                       CF_POWERS_TEST_MODEL='test-model')
            env.pop('CF_POWERS_TEST_CREDENTIALS_FILE', None)
            subprocess.run(['bash', str(HERE.parent / 'claude-code/isolated-run.sh'), '10', '-p', 'literal $(not-a-command)'], env=env, check=True)
            observed = json.loads(capture.read_text())
            self.assertEqual(observed['config'], str(source))
            self.assertIn('--strict-mcp-config', observed['args'])
            self.assertEqual(observed['args'][observed['args'].index('--setting-sources') + 1], '')
            self.assertEqual(observed['args'][-1], 'literal $(not-a-command)')
            self.assertEqual((source / 'CLAUDE.md').read_text(), 'UNRELATED USER INSTRUCTIONS')
            credentials = root / 'credentials.json'
            credentials.write_text('{}')
            env['CF_POWERS_TEST_CREDENTIALS_FILE'] = str(credentials)
            subprocess.run(['bash', str(HERE.parent / 'claude-code/isolated-run.sh'), '10', '-p', 'x'], env=env, check=True)
            observed = json.loads(capture.read_text())
            self.assertNotEqual(observed['config'], str(source))
            self.assertEqual(observed['files'], ['.credentials.json'])
            self.assertFalse(Path(observed['config']).exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
