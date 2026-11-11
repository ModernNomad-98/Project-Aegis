#!/usr/bin/env python
"""Protected launcher for the aegis_verdict_gate checker.

The checker package lives under this protected scripts/ tree.  This launcher
adds exactly one directory - the protected scripts/ directory - to sys.path
and calls the package CLI main.  It performs no other environment or loader
manipulation, and the CLI arguments, output and exit codes are the package's.
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aegis_verdict_gate import __main__ as cli  # noqa: E402


if __name__ == "__main__":
    sys.exit(cli.main())
