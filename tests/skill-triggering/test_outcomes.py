from pathlib import Path
import subprocess
import tempfile
import unittest

FIXTURE = Path(__file__).with_name('outcome-fixture.py')


class OutcomeTests(unittest.TestCase):
    def run_fixture(self, action, root, case):
        return subprocess.run(['python3', str(FIXTURE), action, str(root), case],
                              capture_output=True, text=True)

    def test_config_outcome_requires_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'repo'
            self.assertEqual(self.run_fixture('create', root, 'S1').returncode, 0)
            self.assertEqual(self.run_fixture('check', root, 'S1').returncode, 1)
            (root / 'sample.ini').write_text('[client]\ntimeout = 20\n')
            self.assertEqual(self.run_fixture('check', root, 'S1').returncode, 0)
            (root / 'docs/plans').mkdir(parents=True)
            (root / 'docs/plans/unnecessary.md').write_text('plan')
            self.assertEqual(self.run_fixture('check', root, 'S1').returncode, 1)

    def test_public_change_requires_persistent_guide(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'repo'
            self.assertEqual(self.run_fixture('create', root, 'S8').returncode, 0)
            (root / 'client.py').write_text('DEFAULT_TIMEOUT = 20\n')
            self.assertEqual(self.run_fixture('check', root, 'S8').returncode, 1)
            (root / 'docs/configuration.md').write_text('The default timeout is 20 seconds.\n')
            self.assertEqual(self.run_fixture('check', root, 'S8').returncode, 0)

    def test_creation_preserves_existing_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'keep').write_text('user data')
            self.assertNotEqual(self.run_fixture('create', root, 'S1').returncode, 0)
            self.assertEqual((root / 'keep').read_text(), 'user data')

    def test_checks_survive_python_optimization(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'repo'
            self.assertEqual(self.run_fixture('create', root, 'S1').returncode, 0)
            result = subprocess.run(['python3', '-O', str(FIXTURE), 'check', str(root), 'S1'],
                                    capture_output=True)
            self.assertEqual(result.returncode, 1)

    def test_guide_can_describe_previous_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'repo'
            self.assertEqual(self.run_fixture('create', root, 'S8').returncode, 0)
            (root / 'client.py').write_text('DEFAULT_TIMEOUT = 20\n')
            (root / 'docs/configuration.md').write_text('The default timeout is 20 seconds. Previously it was 10 seconds.\n')
            self.assertEqual(self.run_fixture('check', root, 'S8').returncode, 0)
            (root / 'docs/configuration.md').write_text('The default timeout is 10 seconds. Previously it was 20 seconds.\n')
            self.assertEqual(self.run_fixture('check', root, 'S8').returncode, 1)

    def test_public_change_must_remain_uncommitted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'repo'
            self.assertEqual(self.run_fixture('create', root, 'S8').returncode, 0)
            (root / 'client.py').write_text('DEFAULT_TIMEOUT = 20\n')
            (root / 'docs/configuration.md').write_text('The default timeout is 20 seconds.\n')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture',
                            '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Unauthorized'], check=True)
            self.assertEqual(self.run_fixture('check', root, 'S8').returncode, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
