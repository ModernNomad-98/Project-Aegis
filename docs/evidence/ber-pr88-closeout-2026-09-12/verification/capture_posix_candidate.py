"""Capture Docker output as UTF-8 bytes, without PowerShell stderr wrapping."""
import argparse
import json
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument("--commit", required=True)
p.add_argument("--label", required=True)
a = p.parse_args()
out = Path(__file__).resolve().parent
command = [
    "docker", "run", "--rm", "--init", "--pull", "never", "--network", "none",
    "--user", "65534:65534", "--mount",
    "type=bind,source=C:\\src\\Project Aegis\\Project-Aegis,target=/source,readonly",
    "-e", "PYTHONPATH=/source/artifacts/reviews/phase01-testdeps",
    "sha256:9bd26ad900bb5e0f4dee75839e957a89ae89c2b7ab1e76050e559790e946b948",
    "python3", "-B", "/source/artifacts/reviews/preflight-20260912/run_posix_candidate.py",
    "--commit", a.commit,
]
start = time.monotonic()
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
log = out / f"{a.label}-posix.log"
log.write_bytes(result.stdout)
record = {"commit": a.commit, "command": command, "exit_code": result.returncode,
          "seconds": round(time.monotonic()-start, 3), "log": log.name,
          "tail": result.stdout.decode("utf-8", errors="replace").splitlines()[-8:]}
(out / f"{a.label}-posix.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
print(json.dumps(record), flush=True)
raise SystemExit(result.returncode)
