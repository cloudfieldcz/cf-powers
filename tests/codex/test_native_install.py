#!/usr/bin/env python3
"""Real Codex CLI/App Server install/update/discovery, without auth or model calls.

Copies the working tree into a committed temporary marketplace and uses an
isolated CODEX_HOME. Never installs into the user's profile.
"""
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[2]

class AppServer:
    def __init__(self, env, cwd):
        self.errors = tempfile.TemporaryFile(mode='w+')
        self.process = subprocess.Popen(['codex', 'app-server', '--stdio'], env=env,
            cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=self.errors, text=True)
        self.messages = queue.Queue()
        self.next_id = 0
        threading.Thread(target=self.read, daemon=True).start()
        try:
            self.call('initialize', {'clientInfo': {'name': 'cf-powers-test', 'version': '1.0'},
                                    'capabilities': {'experimentalApi': True}})
            self.process.stdin.write('{"method":"initialized"}\n')
            self.process.stdin.flush()
        except BaseException:
            self.close()
            raise

    def read(self):
        for line in self.process.stdout:
            self.messages.put(json.loads(line))
        self.messages.put(None)

    def call(self, method, params):
        self.next_id += 1
        self.process.stdin.write(json.dumps({'id': self.next_id, 'method': method, 'params': params}) + '\n')
        self.process.stdin.flush()
        while True:
            item = self.messages.get(timeout=30)
            if item is None:
                self.errors.seek(0)
                raise RuntimeError('App Server exited: ' + self.errors.read())
            if item.get('id') == self.next_id:
                if 'error' in item:
                    raise RuntimeError(item['error'])
                return item['result']

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()
        self.process.stdin.close()
        self.process.stdout.close()
        self.errors.close()

class NativeInstall(unittest.TestCase):
    def test_committed_install_update_and_discovery(self):
        self.assertIsNotNone(shutil.which('codex'), '--native requires Codex CLI')
        with tempfile.TemporaryDirectory(prefix='cf-powers-native-') as tmp:
            tmp = Path(tmp)
            source, home, project = tmp / 'marketplace', tmp / 'home', tmp / 'project'
            home.mkdir(); project.mkdir()
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns('.git', '.cf-powers', '__pycache__'))
            env = dict(os.environ, CODEX_HOME=str(home))
            def run(*args):
                result = subprocess.run(args, cwd=project, env=env, capture_output=True,
                                        text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return result.stdout
            def commit(message):
                run('git', '-C', str(source), 'add', '.')
                run('git', '-C', str(source), '-c', 'user.name=CF Powers Test',
                    '-c', 'user.email=test@example.invalid', 'commit', '-qm', message)
            run('git', '-C', str(source), 'init', '-q', '-b', 'fixture/install')
            commit('Install fixture')
            print(run('codex', '--version').strip())
            run('codex', 'plugin', 'marketplace', 'add', str(source))
            install = json.loads(run('codex', 'plugin', 'add', 'cf-powers@cf-powers', '--json'))
            installed = Path(install['installedPath'])
            self.assertTrue(installed.is_relative_to(home.resolve()))
            self.assertNotEqual(installed, source)
            run('bash', str(installed / 'bin/check-integrity'))
            self.check_discovery(env, project, installed, source)

            # Exercise the consumer update, not merely edits in a source checkout.
            changed_skill = source / 'skills/systematic-debugging/SKILL.md'
            changed_skill.write_text(changed_skill.read_text() + '\n<!-- update fixture -->\n')
            manifest_path = source / '.codex-plugin/plugin.json'
            manifest = json.loads(manifest_path.read_text())
            manifest['version'] = '99.0.0-test.1'
            manifest_path.write_text(json.dumps(manifest))
            run('bash', str(source / 'bin/update-integrity'))
            commit('Update fixture')
            update = json.loads(run('codex', 'plugin', 'add', 'cf-powers@cf-powers', '--json'))
            updated = Path(update['installedPath'])
            self.assertEqual(update['version'], manifest['version'])
            self.assertEqual((updated / 'skills/systematic-debugging/SKILL.md').read_bytes(), changed_skill.read_bytes())
            run('bash', str(updated / 'bin/check-integrity'))
            self.check_discovery(env, project, updated, source)
            print('PASS: native fresh install, cached resources, zero hooks, update and fresh-server discovery')

    def check_discovery(self, env, project, installed, source):
        app = AppServer(env, project)
        try:
            result = app.call('skills/list', {'cwds': [str(project)], 'forceReload': True})
            row = result['data'][0]
            self.assertEqual(row['errors'], [])
            # CODEX_HOME isolates plugins, but native ~/.agents/skills discovery
            # still includes the user's standalone installation. Check identities
            # across this test profile (including stale cached versions), not
            # unrelated global skills with the same namespace.
            profile = Path(env['CODEX_HOME']).resolve()
            skills = [s for s in row['skills']
                      if s['name'].startswith('cf-powers:')
                      and Path(s['path']).resolve().is_relative_to(profile)]
            names = [s['name'] for s in skills]
            self.assertEqual(len(names), len(set(names)), 'duplicate identities after install/update')
            for path in (source / 'skills').glob('*/SKILL.md'):
                name = f'cf-powers:{path.parent.name}'
                skill = next(s for s in skills if s['name'] == name)
                self.assertTrue(Path(skill['path']).is_relative_to(installed))
                self.assertEqual(Path(skill['path']).read_bytes(), path.read_bytes())
            for path in (source / 'agents').glob('*.md'):
                self.assertEqual((installed / 'agents' / path.name).read_bytes(), path.read_bytes())
            for path in (source / 'skills/using-superpowers/references').glob('*.md'):
                self.assertEqual((installed / path.relative_to(source)).read_bytes(), path.read_bytes())
            hooks = app.call('hooks/list', {'cwds': [str(project)]})['data'][0]
            self.assertEqual(hooks['errors'], [])
            self.assertEqual(hooks['hooks'], [], 'Claude hook must not be discovered by Codex')
        finally:
            app.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)
