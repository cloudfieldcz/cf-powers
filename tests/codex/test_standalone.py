#!/usr/bin/env python3
"""Standalone installer safety and actual symlink discovery, isolated from user config."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from test_native_install import AppServer, ROOT

class Standalone(unittest.TestCase):
    def test_install_discover_uninstall_and_collision(self):
        with tempfile.TemporaryDirectory(prefix='cf-powers standalone ') as tmp:
            tmp = Path(tmp)
            project = tmp / 'project'
            project.mkdir()
            home = tmp / 'codex-home'
            home.mkdir()
            discovery = project / '.agents/skills'
            link = discovery / 'cf-powers'
            def run(action):
                return subprocess.run(['python3', str(ROOT / 'bin/codex-skills'),
                    action, '--skills-dir', str(discovery)], capture_output=True, text=True)
            for _ in range(2):
                result = run('install')
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(link.resolve(), ROOT / 'skills')
            app = AppServer(dict(os.environ, CODEX_HOME=str(home)), project)
            try:
                row = app.call('skills/list', {'cwds': [str(project)], 'forceReload': True})['data'][0]
                self.assertEqual(row['errors'], [])
                found = [s for s in row['skills'] if Path(s['path']).resolve().is_relative_to(ROOT / 'skills')]
                expected = list((ROOT / 'skills').glob('*/SKILL.md'))
                self.assertEqual(len(found), len(expected))
                for path in expected:
                    skill = next(s for s in found if s['name'] == 'cf-powers:' + path.parent.name)
                    self.assertEqual(Path(skill['path']).resolve(), path)
                runtime = (link / 'using-superpowers/references/runtime.md').resolve()
                self.assertTrue((runtime.parents[3] / 'agents/code-reviewer.md').is_file())
            finally:
                app.close()
            self.assertEqual(run('uninstall').returncode, 0)
            self.assertFalse(link.is_symlink())
            self.assertTrue((ROOT / 'skills/analysis/SKILL.md').is_file())
            link.mkdir()
            sentinel = link / 'keep.txt'
            sentinel.write_text('user data')
            for action in ['install', 'uninstall']:
                self.assertNotEqual(run(action).returncode, 0)
                self.assertEqual(sentinel.read_text(), 'user data')
            sentinel.unlink(); link.rmdir()
            link.symlink_to(tmp / 'missing')
            self.assertNotEqual(run('install').returncode, 0)
            self.assertTrue(link.is_symlink())

if __name__ == '__main__':
    unittest.main(verbosity=2)
