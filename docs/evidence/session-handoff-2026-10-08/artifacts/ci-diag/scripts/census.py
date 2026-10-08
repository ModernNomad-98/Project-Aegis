"""Run the real ProtectedFileGuardTests once with TemporaryDirectory patched so
each fixture's loose objects are censused (type + fanout) just before cleanup.
Usage: python3 -I census.py <out.jsonl>"""
import importlib.util, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
OUT = open(sys.argv[1], "w")
spec = importlib.util.spec_from_file_location("toc", "/home/user/Project-Aegis/scripts/tests/test_offline_ci.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class Censused(tempfile.TemporaryDirectory):
    def __exit__(self, *exc):
        repo = Path(self.name) / "repo"
        objs = []
        if (repo / ".git/objects").is_dir():
            for d in sorted((repo / ".git/objects").glob("[0-9a-f][0-9a-f]")):
                for f in d.iterdir():
                    oid = d.name + f.name
                    t = subprocess.run(["git", "cat-file", "-t", oid], cwd=repo, capture_output=True, text=True).stdout.strip()
                    objs.append((oid, t))
            OUT.write(json.dumps({"test": CURRENT[0], "loose": len(objs),
                                  "noncommit_in_17": sum(1 for o, t in objs if o.startswith("17") and t != "commit"),
                                  "commits": sum(1 for o, t in objs if t == "commit"),
                                  "all_in_17": sum(1 for o, t in objs if o.startswith("17"))}) + "\n")
        return super().__exit__(*exc)
class NS: pass
ns = NS(); ns.__dict__.update(vars(tempfile)); ns.TemporaryDirectory = Censused
mod.tempfile = ns
CURRENT = ["?"]
class R(unittest.TextTestResult):
    def startTest(self, test): CURRENT[0] = test.id().split(".")[-1]; super().startTest(test)
suite = unittest.defaultTestLoader.loadTestsFromTestCase(mod.ProtectedFileGuardTests)
r = unittest.TextTestRunner(resultclass=R, verbosity=0).run(suite)
print("tests run", r.testsRun, "errors", len(r.errors), "failures", len(r.failures))
