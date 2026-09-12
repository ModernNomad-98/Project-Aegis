"""Capture declared offline checks for the PR88 planning preflight."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument("--repo", required=True)
p.add_argument("--label", required=True)
p.add_argument("--suite", action="store_true")
p.add_argument("--suite-python")
a = p.parse_args()
repo = Path(a.repo).resolve()
out = Path(__file__).resolve().parent
commands = [
    [sys.executable, "-B", "scripts/tests/test_validator.py"],
    [sys.executable, "-B", "scripts/validate-skills.py"],
    [sys.executable, "-B", "scripts/tests/test_audit_skill_contracts.py"],
    [sys.executable, "-B", "-m", "tools.behavioral_eval_runner", "self-check"],
    [sys.executable, "-B", "scripts/check_dco.py", "--range", "origin/main..HEAD"],
    ["git", "diff", "--check"],
]
if a.suite:
    commands.append([a.suite_python or sys.executable, "-B", "-m", "unittest", "discover", "-s", "tools/behavioral_eval_runner/tests", "-p", "test_*.py", "-v"])
results = []
for index, command in enumerate(commands):
    start = time.monotonic()
    log = out / f"{a.label}-{index}.log"
    with log.open("wb") as output:
        result = subprocess.run(command, cwd=repo, stdout=output, stderr=subprocess.STDOUT)
    record = {"command": command, "exit_code": result.returncode, "seconds": round(time.monotonic()-start, 3), "log": str(log), "tail": log.read_text(encoding="utf-8", errors="replace").splitlines()[-7:]}
    results.append(record)
    print(json.dumps(record), flush=True)
(out / f"{a.label}-results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
raise SystemExit(any(record["exit_code"] for record in results))
