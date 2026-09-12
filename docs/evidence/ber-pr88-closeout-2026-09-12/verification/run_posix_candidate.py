"""Run one exact committed revision in a disposable offline container checkout."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--commit", required=True)
args = parser.parse_args()
if not re.fullmatch(r"[0-9a-f]{40}", args.commit):
    parser.error("commit must be a full lowercase SHA")
repo = Path(tempfile.mkdtemp(prefix="aegis-candidate-")) / "repo"
repo.mkdir()
shutil.copytree("/source/.git", repo / ".git", ignore=shutil.ignore_patterns("worktrees"))
subprocess.run(["git", "-C", str(repo), "reset", "--hard", args.commit], check=True)
os.chdir(repo)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
print("POSIX environment:", sys.version, flush=True)
subprocess.run(["git", "show", "-s", "--format=%H %T"], check=True)
result = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tools/behavioral_eval_runner/tests", "-p", "test_*.py", "-v"])
sys.exit(result.returncode)
