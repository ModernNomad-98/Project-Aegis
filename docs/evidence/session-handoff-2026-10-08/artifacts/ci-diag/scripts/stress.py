"""Replicates ProtectedFileGuardTests.run_guard (scripts/tests/test_offline_ci.py)
exactly, N times, and on a cleanup OSError records what was left in the tree."""
import os, sys, subprocess, tempfile, time, json, shutil
from pathlib import Path
import yaml
REPO = Path("/home/user/Project-Aegis")
wf = yaml.load((REPO / ".github/workflows/validate-skills.yml").read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
GUARD = next(s["run"] for s in wf["jobs"]["gate-guard"]["steps"] if "gate_pattern=" in s.get("run", ""))
PATHS = sys.argv[3].split(",") if len(sys.argv) > 3 else ["tools/behavioral_eval_runner/schemas/fixture.json"]
def run_guard(paths):
    with tempfile.TemporaryDirectory(prefix="aegis-ci-guard-") as temporary:
        root = Path(temporary); repo = root / "repo"; repo.mkdir()
        def git(*args):
            return subprocess.run(["git", "-c", "user.name=Fixture", "-c",
                                   "user.email=fixture@example.invalid", *args], cwd=repo,
                                  check=True, capture_output=True)
        git("init", "--quiet")
        (repo / "README.md").write_text("fixture\n", encoding="utf-8")
        git("add", "--force", "."); git("commit", "--quiet", "-m", "fixture base")
        git("branch", "fixture-base"); git("remote", "add", "origin", str(repo))
        for path in paths:
            f = repo / path; f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text("changed fixture\n", encoding="utf-8")
        if os.environ.get("EXTRA17") == "1":
            # Two loose objects in objects/17/ make git's approximate loose
            # count 2*256 > 256, the natural geometric-repack auto trigger.
            for c in (b"pad35\n", b"pad136\n"):
                subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=repo, input=c, check=True, capture_output=True)
        git("add", "--force", "."); git("commit", "--quiet", "-m", "fixture change")
        r = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", GUARD],
                           cwd=repo, env=dict(os.environ, BASE_REF="fixture-base", RUNNER_TEMP=str(root)),
                           capture_output=True, text=True)
        assert r.returncode == 1, r.stdout + r.stderr
        return root
label, n = sys.argv[1], int(sys.argv[2])
fails = 0
for i in range(n):
    try:
        run_guard(PATHS)
    except OSError as e:
        fails += 1
        left = []
        base = Path(e.filename).parents[0] if e.filename else None
        # e.filename is the directory whose rmdir failed; list what is in it now
        try:
            for dp, dn, fn in os.walk(e.filename):
                for x in dn + fn:
                    left.append(os.path.relpath(os.path.join(dp, x), e.filename))
        except Exception as w:
            left.append(f"walk-error {w!r}")
        print(json.dumps({"label": label, "iter": i, "errno": e.errno, "filename": e.filename, "left_now": left[:30]}), flush=True)
        root = next((q for q in [Path(e.filename), *Path(e.filename).parents] if q.name.startswith("aegis-ci-guard-")), None)
        time.sleep(0.5)
        if root: shutil.rmtree(root, ignore_errors=True)
print(json.dumps({"label": label, "iterations": n, "failures": fails}), flush=True)
