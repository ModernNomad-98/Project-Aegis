#!/usr/bin/env python
"""Protected test runner for the moved aegis_verdict_gate suite.

Adds only the protected scripts/ directory and this tests directory to
sys.path, discovers test_*.py with unittest, and returns nonzero on failure.
No network access is used.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parents[1]
for directory in (SCRIPTS_DIR, TESTS_DIR):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))


def main() -> int:
    suite = unittest.TestLoader().discover(str(TESTS_DIR), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
