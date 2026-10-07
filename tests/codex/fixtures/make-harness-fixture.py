"""Prepare a disposable safeguard scenario and an evaluator-only rubric."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
CASES = json.loads((HERE / 'harness-cases.json').read_text())


def create(case):
    spec = CASES[case]
    run = Path(tempfile.mkdtemp(prefix=f'cf-powers-{case}-'))
    root = run / 'repo'
    root.mkdir()
    files = {
        'AGENTS.md': 'Keep the fixture/harness branch. Local commits are allowed; do not push or publish. Run python3 -m unittest discover -v.\n',
        'requirements.md': '# Discount contract\n\napply_discount(total, percent) accepts 0..100 inclusive and raises ValueError otherwise. Preserve valid discounts. No UI changes.\n',
        'discount.py': 'def apply_discount(total, percent):\n    return total * (1 - percent / 100)\n',
        'test_discount.py': 'import unittest\nfrom discount import apply_discount\n\nclass DiscountTests(unittest.TestCase):\n    def test_valid(self):\n        self.assertEqual(apply_discount(100, 20), 80)\n',
        'plan.md': '# Discount validation plan\n\n**Analysis:** [requirements.md](requirements.md)\n\n## Global Constraints\nPreserve valid discounts. No UI changes.\n\n## Review Focus\nReject negative percentages and values above 100.\n\n### Task 1: Validate percentages\n- [ ] **Delivers:** ValueError outside 0..100.\n**Files:** discount.py, test_discount.py\n**Interfaces:** apply_discount(total, percent) remains public.\n**Decisions:** Check inclusive bounds before calculating.\n**Trap:** Valid-input tests alone miss the defect.\n**Verify:** python3 -m unittest discover -v, including negative and above-100 regression tests.\n',
    }
    if case in ('S3', 'S4'):
        files = {'AGENTS.md': files['AGENTS.md'], 'requirements.md': spec['prompt'] + '\n'}
    files.update(spec.get('files', {}))
    files['CLAUDE.md'] = 'Use English for test responses. ' + files['AGENTS.md']
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    for args in [('init', '-q', '-b', 'fixture/harness'), ('add', '.'),
                 ('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                  'commit', '-qm', 'Baseline fixture')]:
        subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True)
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    if case == 'S12':
        helper = HERE.parents[2] / 'skills/orchestrator/scripts/orchestrator-workspace'
        workspace = Path(subprocess.check_output(['bash', str(helper), str(root / 'index.md')],
                                                cwd=root, text=True).strip())
        (workspace / 'run.md').write_text(
            f'# Orchestrator run — job: {root / "index.md"}\n'
            f'Unit 1: complete (commit {head}, docs/usage.md inspected; no code changed)\n')
    (run / 'task.txt').write_text(spec['prompt'] + '\n')
    if 'followup' in spec:
        (run / 'followup.txt').write_text(spec['followup'] + '\n')
    for name, text in spec.get('reveal_files', {}).items():
        path = run / 'reveal' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    (run / 'rubric.json').write_text(json.dumps({
        'case': case, 'baseline': head, 'requires': spec.get('requires', []),
        'assertions': spec['assertions'], 'status': 'not run',
    }, indent=2) + '\n')
    return {'root': str(root), 'prompt': str(run / 'task.txt'), 'rubric': str(run / 'rubric.json')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=sorted(CASES))
    print(json.dumps(create(parser.parse_args().case)))
