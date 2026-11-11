"""Shared synthetic-fixture helpers for the aegis_ops tests.

No real PR, identity, secret, network payload or clock value is used.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"


def load(name: str) -> dict:
    with (FIXTURES / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fixture_names() -> list:
    return sorted(path.name for path in FIXTURES.glob("*.json"))


def run_cli(*args: str, cwd: pathlib.Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "tools.aegis_ops", *args],
        capture_output=True,
        text=True,
        cwd=str(cwd or ROOT),
    )
