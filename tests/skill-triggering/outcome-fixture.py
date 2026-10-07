"""Create disposable S1/S8 fixtures; check artifacts independently of agent reports."""
import argparse
import ast
from pathlib import Path
import re
import subprocess


def create(root, case):
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise ValueError('fixture destination must be empty')
    instructions = 'Use English for test responses. Keep this feature branch. Do not commit or publish. Verify changed behavior.\n'
    files = {'AGENTS.md': instructions, 'CLAUDE.md': instructions}
    if case == 'S1':
        files['sample.ini'] = '[client]\ntimeout = 10\n'
        prompt = 'Change timeout from 10 to 20 in sample.ini. This is a known local configuration correction. Verify the contents.'
    else:
        files.update({
            'client.py': 'DEFAULT_TIMEOUT = 10\n',
            'README.md': '# Client\n\nSee [configuration](docs/configuration.md).\n',
            'docs/configuration.md': '# Configuration\n\nThe default timeout is 10 seconds.\n',
        })
        prompt = 'Change the public client default timeout from 10 seconds to 20 seconds. Complete the change and verify it.'
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    for args in [('init', '-q', '-b', 'fixture/harness'), ('add', '.'),
                 ('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                  'commit', '-qm', 'Baseline fixture')]:
        subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True)
    baseline = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True)
    (root / '.git/cf-powers-baseline').write_text(baseline)
    print(prompt)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(root, case):
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True)
    require(head == (root / '.git/cf-powers-baseline').read_text(), 'fixture commits changed')
    branch = subprocess.check_output(['git', '-C', str(root), 'branch', '--show-current'], text=True).strip()
    require(branch == 'fixture/harness', 'fixture branch changed')
    changed = subprocess.check_output(['git', '-C', str(root), 'diff', 'HEAD', '--name-only'], text=True).splitlines()
    if case == 'S1':
        require((root / 'sample.ini').read_text() == '[client]\ntimeout = 20\n', 'wrong config')
        require(not list(root.glob('docs/plans/*.md')), 'unnecessary plan artifact')
        require('sample.ini' in changed, 'expected uncommitted config change')
    else:
        tree = ast.parse((root / 'client.py').read_text())
        values = [ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                  and any(isinstance(target, ast.Name) and target.id == 'DEFAULT_TIMEOUT'
                          for target in node.targets)]
        require(values == [20], 'wrong default')
        guide = (root / 'docs/configuration.md').read_text().lower()
        require(re.search(r'default timeout\s*(?:is|:|=)\s*[`*]*20\b', guide),
                'guide must identify the current default timeout as 20')
        require('docs/configuration.md' in (root / 'README.md').read_text(), 'guide is not linked')
        require({'client.py', 'docs/configuration.md'} <= set(changed), 'expected uncommitted code and guide changes')
    print(f'PASS: {case} artifact checks; trace/review assertions remain separate')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['create', 'check'])
    parser.add_argument('directory', type=Path)
    parser.add_argument('case', choices=['S1', 'S8'])
    args = parser.parse_args()
    try:
        (create if args.action == 'create' else check)(args.directory, args.case)
    except (OSError, ValueError, AssertionError, SyntaxError, subprocess.CalledProcessError) as error:
        print(f'FAIL: {error}')
        raise SystemExit(1)
