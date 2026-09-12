"""Rerun exactly the failed Windows cases to classify baseline/environment causes."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument("--repo", required=True)
p.add_argument("--label", required=True)
p.add_argument("--canonical-temp", action="store_true")
a = p.parse_args()
out = Path(__file__).resolve().parent
original = (out / "corrections-6.log").read_text(encoding="utf-8", errors="replace")
cases = re.findall(r"^(?:ERROR|FAIL): [^\n]*\(([^)]+)\)", original, flags=re.MULTILINE)
cases = list(dict.fromkeys(cases))
env = os.environ.copy()
if a.canonical_temp:
    temp = out / (a.label + "-temp")
    temp.mkdir(exist_ok=True)
    env["TEMP"] = str(temp.resolve())
    env["TMP"] = str(temp.resolve())
code = "import sys,unittest; sys.path.insert(0,'tools/behavioral_eval_runner/tests'); unittest.main(module=None,argv=['unittest', '-v', *sys.argv[1:]])"
start = time.monotonic()
r = subprocess.run([sys.executable, "-B", "-c", code, *cases], cwd=a.repo, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
log = out / (a.label + ".log")
log.write_bytes(r.stdout)
record = {"cases": cases, "repo": a.repo, "python": sys.executable, "canonical_temp": a.canonical_temp, "exit_code": r.returncode, "seconds": round(time.monotonic()-start,3), "log": str(log), "tail": r.stdout.decode("utf-8",errors="replace").splitlines()[-8:]}
(out / (a.label + ".json")).write_text(json.dumps(record,indent=2),encoding="utf-8")
print(json.dumps(record),flush=True)
raise SystemExit(r.returncode)
