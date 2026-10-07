"""Create the concrete Python repository used by a basic trigger probe."""
import argparse
from pathlib import Path
import subprocess

SKILLS = ('analysis', 'systematic-debugging', 'test-driven-development',
          'writing-plans', 'executing-plans', 'requesting-code-review',
          'dispatching-parallel-agents')


def create(root, skill):
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise ValueError('fixture destination must be empty')
    rules = 'Use English for test responses. Keep fixture/trigger. Local commits are allowed; do not publish. Use Python unittest.\n'
    files = {'AGENTS.md': rules, 'CLAUDE.md': rules,
             'README.md': '# Fixture\n\nPython standard library only. Run python3 -m unittest discover -v.\n'}
    if skill == 'systematic-debugging':
        files.update({'parser.py': 'def parse(data):\n    return data["value"]\n',
                      'test_parser.py': 'import unittest\nfrom parser import parse\nclass ParserTests(unittest.TestCase):\n    def test_nested_value(self):\n        self.assertEqual(parse({"node": {"value": 7}}), 7)\n'})
    elif skill in ('writing-plans', 'executing-plans'):
        files['requirements.md'] = '# Approved design\n\nImplement is_valid_email(value) in email_validator.py: nonempty local part, @, and dot in domain. Add cli.py reading one argument and returning exit 0 for valid input, 1 otherwise. Use unittest. No dependencies.\n'
        if skill == 'executing-plans':
            files['docs/plans/validation-plan.md'] = '# Email validation\n\n**Analysis:** [requirements](../../requirements.md)\n\n## Global Constraints\nStandard library only. Preserve the specified exit codes.\n\n## Review Focus\nEmpty local part and missing domain dot.\n\n### Task 1: Validate email\n- [ ] **Delivers:** is_valid_email(value) returns bool.\n**Files:** email_validator.py, test_email_validator.py\n**Interfaces:** is_valid_email(value: str) -> bool\n**Verify:** python3 -m unittest discover -v with valid and invalid addresses.\n\n### Task 2: Expose CLI\n- [ ] **Delivers:** cli.py calls the validator.\n**Files:** cli.py, test_cli.py\n**Interfaces:** consumes is_valid_email.\n**Verify:** python3 -m unittest discover -v; CLI exit codes 0 and 1.\n'
    elif skill == 'analysis':
        files['handler.py'] = 'def can_access(actor, tenant):\n    return True\n'
    elif skill == 'requesting-code-review':
        files['requirements.md'] = '# Contract\n\nis_valid_email checks a nonempty local part, an @, and a dot in the domain.\n'
    elif skill == 'dispatching-parallel-agents':
        files['tests/__init__.py'] = ''
        for module, function, expression, expected in (
            ('login', 'redirect', '"/wrong"', '"/home"'),
            ('users', 'list_users', 'None', '[]'),
            ('button', 'label', '""', '"Save"'),
            ('dates', 'utc_hour', '12 + 2', '10'),
        ):
            files[module + '.py'] = f'def {function}():\n    return {expression}\n'
            files[f'tests/test_{module}.py'] = f'import unittest\nfrom {module} import {function}\nclass Tests(unittest.TestCase):\n    def test_result(self):\n        self.assertEqual({function}(), {expected})\n'
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    def git(*args):
        subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture',
                        '-c', 'user.email=fixture@example.invalid', *args], check=True, capture_output=True)
    git('init', '-q', '-b', 'fixture/trigger')
    git('add', '.')
    git('commit', '-qm', 'Fixture contract')
    if skill == 'requesting-code-review':
        (root / 'email_validator.py').write_text('def is_valid_email(value):\n    return "@" in value\n')
        git('add', 'email_validator.py')
        git('commit', '-qm', 'Implement email validator')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('skill', choices=SKILLS)
    args = parser.parse_args()
    create(args.directory, args.skill)
