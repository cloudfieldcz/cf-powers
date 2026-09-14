#!/usr/bin/env python3
"""Offline manifest/resource contracts and observable integrity-checker behavior."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]

class PluginContracts(unittest.TestCase):
    def test_manifest_resolves_shared_tree(self):
        marketplace = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
        entries = [p for p in marketplace['plugins'] if p['name'] == 'cf-powers']
        self.assertEqual(len(entries), 1)
        source = entries[0]['source']
        self.assertEqual(source['source'], 'local')
        plugin = (ROOT / source['path']).resolve()
        self.assertEqual(plugin, ROOT)
        codex = json.loads((plugin / '.codex-plugin/plugin.json').read_text())
        claude = json.loads((plugin / '.claude-plugin/plugin.json').read_text())
        claude_market = json.loads((plugin / '.claude-plugin/marketplace.json').read_text())
        self.assertEqual(codex['name'], entries[0]['name'])
        self.assertEqual(codex['version'], claude['version'])
        self.assertEqual(codex['version'], claude_market['plugins'][0]['version'])
        # Empty object suppresses default hook discovery; absence/list/null do not.
        self.assertEqual(codex['hooks'], {})
        self.assertTrue((plugin / 'hooks/hooks.json').is_file())
        self.assertEqual((plugin / codex['skills']).resolve(), ROOT / 'skills')
        for role in ['code', 'business-analyst', 'developer', 'security', 'performance']:
            self.assertTrue((plugin / f'agents/{role}-reviewer.md').is_file())
        for ref in ['runtime', 'claude-code-tools', 'codex-tools']:
            self.assertTrue((plugin / f'skills/using-superpowers/references/{ref}.md').is_file())

class IntegrityBehavior(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='cf-powers-integrity-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'plugin with spaces'
        (self.root / 'bin').mkdir(parents=True)
        (self.root / '.claude-plugin').mkdir()
        (self.root / 'skills/demo').mkdir(parents=True)
        self.checker = self.root / 'bin/check-integrity'
        shutil.copy2(ROOT / 'bin/check-integrity', self.checker)
        self.skill = self.root / 'skills/demo/SKILL.md'
        self.skill.write_text('---\nname: demo\ndescription: Test fixture\n---\n')
        self.baseline = self.root / '.claude-plugin/integrity.sha256'
        digest = hashlib.sha256(self.skill.read_bytes()).hexdigest()
        self.baseline.write_text(f'{digest}  skills/demo/SKILL.md\n')
        self.bash = shutil.which('bash')

    def run_check(self, path=None):
        before = {str(p.relative_to(self.root)): p.read_bytes()
                  for p in self.root.rglob('*') if p.is_file()}
        env = os.environ.copy()
        if path is not None:
            env['PATH'] = str(path)
        result = subprocess.run([self.bash, str(self.checker)], cwd=self.tmp.name,
                                env=env, capture_output=True, timeout=10)
        after = {str(p.relative_to(self.root)): p.read_bytes()
                 for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after, 'checker must not mutate or repair files')
        return result.returncode

    def test_matching_from_other_cwd(self):
        self.assertEqual(self.run_check(), 0)

    def test_modified_skill_fails(self):
        self.skill.write_text('changed')
        self.assertNotEqual(self.run_check(), 0)

    def test_missing_skill_fails(self):
        self.skill.unlink()
        self.assertNotEqual(self.run_check(), 0)

    def test_missing_baseline_fails(self):
        self.baseline.unlink()
        self.assertNotEqual(self.run_check(), 0)

    def test_no_hash_utility_fails(self):
        empty = Path(self.tmp.name) / 'empty-path'
        empty.mkdir()
        self.assertNotEqual(self.run_check(empty), 0)

    def test_each_available_hash_backend(self):
        for name in ['sha256sum', 'shasum']:
            target = shutil.which(name)
            if not target:
                continue
            with self.subTest(backend=name):
                path = Path(self.tmp.name) / name
                path.mkdir()
                (path / name).symlink_to(target)
                self.assertEqual(self.run_check(path), 0)
                original = self.skill.read_bytes()
                self.skill.write_text('corrupted')
                self.assertNotEqual(self.run_check(path), 0)
                self.skill.write_bytes(original)

if __name__ == '__main__':
    unittest.main(verbosity=2)
