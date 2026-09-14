#!/usr/bin/env python3
"""Create a disposable review/fix fixture. Outputs root, base and head as JSON."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--with-plan", action="store_true", help="include the SDD implementation scenario")
args = parser.parse_args()

root = Path(tempfile.mkdtemp(prefix="cf-powers-review-"))
def git(*args):
    return subprocess.check_output(
        ["git", "-c", "user.name=CF Powers Test", "-c", "user.email=test@example.invalid", *args],
        cwd=root, text=True,
    ).strip()
git("init", "-q", "-b", "fixture/review")
(root / "requirements.md").write_text(
    "# Discount calculation\n\n"
    "apply_discount(total, percent) returns the discounted total. "
    "Percent must be between 0 and 100 inclusive; values outside that range "
    "raise ValueError. No rendered surface changes.\n"
)
git("add", ".")
git("commit", "-qm", "Document discount contract")
base = git("rev-parse", "HEAD")
(root / "discount.py").write_text(
    "def apply_discount(total, percent):\n"
    "    return total * (1 - percent / 100)\n"
)
(root / "test_discount.py").write_text(
    "import unittest\nfrom discount import apply_discount\n\n"
    "class DiscountTests(unittest.TestCase):\n"
    "    def test_valid_discount(self):\n"
    "        self.assertEqual(apply_discount(100, 20), 80)\n"
    "    def test_boundaries(self):\n"
    "        self.assertEqual(apply_discount(100, 0), 100)\n"
    "        self.assertEqual(apply_discount(100, 100), 0)\n"
)
git("add", ".")
git("commit", "-qm", "Implement discount calculation")
if args.with_plan:
    (root / "plan.md").write_bytes((Path(__file__).parent / "discount-plan.md").read_bytes())
print(json.dumps({"root": str(root), "base": base, "head": git("rev-parse", "HEAD")}))
