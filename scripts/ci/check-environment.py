#!/usr/bin/env python3
"""Require the offline SDK cases to execute and report actual host capabilities."""
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import openai
import httpx2
import yaml

from tools.behavioral_eval_runner.evidence import _POSIX_EVIDENCE_ATOMIC
from tools.behavioral_eval_runner.materialize import _POSIX_NOFOLLOW_WRITE
from tools.behavioral_eval_runner.judge.calibration_transport import verify_sdk_version

verify_sdk_version()
if sys.version_info[:2] != (3, 14):
    raise RuntimeError("The reviewed CI interpreter is Python 3.14")
repo = Path(__file__).resolve().parents[2]
temp_root = Path(tempfile.gettempdir()).resolve()
if temp_root.is_relative_to(repo):
    raise RuntimeError("Synthetic fixture storage must be outside the source checkout")
print(json.dumps({
    "sdk_import_and_pin": "PASS", "openai": openai.__version__,
    "httpx2": httpx2.__version__, "pyyaml": yaml.__version__,
    "temporary_directory": str(temp_root),
    "posix_evidence_atomic": _POSIX_EVIDENCE_ATOMIC,
    "posix_nofollow_write": _POSIX_NOFOLLOW_WRITE,
    "provider_requests": "not part of this check; suites use mocked transports",
}, indent=2))
