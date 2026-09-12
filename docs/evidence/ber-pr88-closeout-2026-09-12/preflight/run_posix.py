"""Run committed correction tests in a disposable, network-disabled container."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

repo = Path(tempfile.mkdtemp(prefix="aegis-preflight-")) / "repo"
repo.mkdir()
shutil.copytree("/source/.git", repo / ".git", ignore=shutil.ignore_patterns("worktrees"))
subprocess.run(["git", "-C", str(repo), "reset", "--hard", "a231bc5db820c89467b32dbec533adf01eb56676"], check=True)
os.chdir(repo)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
print("POSIX environment:", sys.version, flush=True)
subprocess.run(["git", "rev-parse", "HEAD"], check=True)
result = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tools/behavioral_eval_runner/tests", "-p", "test_*.py", "-v"])
sys.exit(result.returncode)
