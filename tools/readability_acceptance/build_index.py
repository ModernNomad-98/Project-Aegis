#!/usr/bin/env python3
"""Build the per-path documentation readability acceptance index.

WHY THIS EXISTS
---------------
`docs/roadmaps/aegis-documentation-readability-backlog.md` defines a decision
procedure - "A larger change, meaning more than 10 changed lines on that page or
any new section, returns the page to pending" - whose only input is a per-path
mapping

    reader page -> the revision at which it was last accepted full-page

and the repository does not store that mapping in machine-readable form. It is
prose: inside the tracker, inside the page-level acceptance records under
`docs/evidence/documentation/`, and (for some pages) in GitHub pull-request
comments that are not in git at all. This script harvests the git-visible part
of that prose into `acceptance-index.json` so that the decision procedure can be
run over it by `tools/readability_acceptance/check_index.py`.

WHAT THIS SCRIPT DOES NOT DO
----------------------------
It decides nothing. It does not accept a page, re-review a page, or edit the
tracker. It records what a source states, with the source location, and leaves
`null` for every page whose acceptance no git-visible source states. Where a
source gives a verdict but names no revision, the revision stays `null` with
`confidence: "unknown"`; it is never bound to "the nearest commit". `unknown` is
a measurement result, not a defect: it is why the pending count is a bound plus
an unknown remainder rather than one exact figure.

PRECISION
---------
Two bindings appear in the index and they are not equally strong:

* `page-level`   - the statement names this specific page and a revision.
* `batch-level`  - an acceptance record states one exact reviewed revision in
  its head and dispositions many pages in a table; the record's own claim is
  that those pages were reviewed at that revision, so the binding is the
  record's, not an inference - but it is a batch binding.

USAGE
-----
    python -B tools/readability_acceptance/build_index.py --write
    python -B tools/readability_acceptance/build_index.py --report
    python -B tools/readability_acceptance/build_index.py --rows <path>
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

INDEX_REL = "tools/readability_acceptance/acceptance-index.json"
STAGE1_REL = "tools/readability_acceptance/acceptance-verdicts-stage-1.json"
STATED_REL = "tools/readability_acceptance/stated-acceptances.json"
TRACKER_REL = "docs/roadmaps/aegis-documentation-readability-backlog.md"
EVIDENCE_DIR_REL = "docs/evidence/documentation"

# The one class the tracker defines positively (owner decision, 2026-09-28).
GENERATED_REPORTS = ("docs/audits/skill-contract-audit-baseline.md",)

# Fixture class rule, tracker L2458-2459: the fixture paths are under `scripts/`,
# except the reader-facing `scripts/tests/fixtures/README.md`.
FIXTURE_PREFIX = "scripts/"
FIXTURE_EXCEPTIONS = ("scripts/tests/fixtures/README.md",)

# Reachability rule for a recorded acceptance revision. `refs/remotes/**` is this
# clone's record of the remote's refs, so an object no remote-tracking ref
# contains is exactly an object a fresh clone lacks - it may be a dangling
# pre-rebase object, or one held only by a local tag no remote has. Such a row is
# annotated rather than decided, because deciding it from the local object makes
# the answer a property of the authoring clone instead of the repository.
REMOTE_REFS = "refs/remotes/"
REACHABILITY_RULE = (
    "an acceptance revision is usable only when a remote-tracking ref "
    "(refs/remotes/**) contains it; that is exactly the object set a fresh "
    "clone of the remote has"
)
REACHABILITY_PROBE = ("git for-each-ref --contains <sha> "
                      "--format=%(refname) refs/remotes/")
UNREACHABLE_ROW_REASON = (
    "no refs/remotes/** ref contains this revision, so a fresh clone does not "
    "hold the object; check_index.py reports the row as cannot_decide rather "
    "than deciding it from an object only the authoring clone has"
)

# Rule citations, pinned to the tracker revision named in `source_revision`.
# check_index.py re-reads these lines so a tracker edit cannot silently
# invalidate the citations.
RULE_LINES = {
    "reader_page_default": [103, 104],
    "new_page_pending": [320, 324],
    "acceptance_criteria": [2376, 2397],
    "full_page_acceptance_event": [2478, 2482],
    "targeted_edit_rule": [2484, 2493],
    "refinements": [2495, 2502],
    "net_difference": [2504, 2510],
    "generated_reports": [2512, 2521],
    "targeted_edit_cannot_confer": [2569, 2569],
    "targeted_edit_scope": [22, 26],
    "fixture_rule": [2458, 2459],
}

SHA_RE = re.compile(r"`([0-9a-f]{7,40})`")
BACKTICKED_RE = re.compile(r"`([^`\n]+)`")
BARE_SHA_RE = re.compile(r"(?<![0-9a-zA-Z])([0-9a-f]{7,40})(?![0-9a-zA-Z])")
MD_LINK_RE = re.compile(r"\]\(([^)\s]+?\.md)(?:#[^)]*)?\)")

ACCEPT_RE = re.compile(
    r"(?i)\b("
    r"corrected and accepted|accepted unchanged|re-?accepted|"
    r"accepted|accepts|accept\b"
    r")"
)
RETENTION_RE = re.compile(
    r"(?i)\bkeep(s|ing)?\b[^.]{0,40}?\bacceptance\b"
)

PATH_HINTS = (
    ".claude/skills/",
    ".claude/agents/",
    "docs/",
    "tools/",
    "scripts/",
    "artifacts/",
)


def git(*args: str, root: Path | None = None) -> str:
    proc = subprocess.run(
        ["git", "-C", str(root or REPO_ROOT), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed:\n{proc.stderr.strip()}")
    return proc.stdout


def tracked_markdown(ref: str, root: Path) -> list[str]:
    out = git("ls-tree", "-r", "--name-only", ref, root=root)
    return sorted(line for line in out.splitlines() if line.endswith(".md"))


def classify(paths: list[str]) -> dict[str, list[str]]:
    fixtures = [
        p for p in paths
        if p.startswith(FIXTURE_PREFIX) and p not in FIXTURE_EXCEPTIONS
    ]
    reports = [p for p in paths if p in GENERATED_REPORTS]
    reader = [p for p in paths if p not in set(fixtures) | set(reports)]
    return {"reader": reader, "generated_reports": reports, "fixtures": fixtures}


def resolve_sha(token: str, root: Path) -> str | None:
    proc = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--verify", "--quiet",
         f"{token}^{{commit}}"],
        capture_output=True, text=True,
    )
    sha = proc.stdout.strip()
    return sha if (proc.returncode == 0 and sha) else None


class Repo:
    """Cache over the git queries the harvester needs."""

    def __init__(self, ref: str, root: Path) -> None:
        self.ref = ref
        self.root = root
        self._sha_cache: dict[str, str | None] = {}
        self._date_cache: dict[str, str] = {}
        self._touch_cache: dict[str, str | None] = {}
        self._ls_cache: dict[str, set[str]] = {}
        self._log_cache: dict[str, bool] = {}
        self._contained_cache: dict[str, bool] = {}

    def sha(self, token: str) -> str | None:
        if token not in self._sha_cache:
            self._sha_cache[token] = resolve_sha(token, self.root)
        return self._sha_cache[token]

    def date(self, sha: str) -> str:
        if sha not in self._date_cache:
            self._date_cache[sha] = git(
                "show", "-s", "--format=%ad", "--date=short", sha, root=self.root
            ).strip()
        return self._date_cache[sha]

    def tree(self, ref: str) -> set[str]:
        if ref not in self._ls_cache:
            self._ls_cache[ref] = set(
                git("ls-tree", "-r", "--name-only", ref, root=self.root).splitlines()
            )
        return self._ls_cache[ref]

    def touches(self, sha: str, path: str) -> bool:
        key = f"{sha}:{path}"
        if key not in self._log_cache:
            out = git("log", "-1", "--format=%H", sha, "--", path, root=self.root)
            self._log_cache[key] = bool(out.strip())
        return self._log_cache[key]

    def exists_at(self, sha: str, path: str) -> bool:
        """Whether the path is present in the tree at that revision."""
        key = f"exists:{sha}:{path}"
        if key not in self._log_cache:
            proc = subprocess.run(
                ["git", "-C", str(self.root), "cat-file", "-e",
                 f"{sha}:{path}"],
                capture_output=True, text=True,
            )
            self._log_cache[key] = proc.returncode == 0
        return self._log_cache[key]

    def remote_contained(self, sha: str) -> bool:
        """Whether a fresh clone of the remote would hold this object."""
        if sha not in self._contained_cache:
            proc = subprocess.run(
                ["git", "-C", str(self.root), "for-each-ref", "--contains", sha,
                 "--format=%(refname)", REMOTE_REFS],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            self._contained_cache[sha] = (proc.returncode == 0
                                          and bool(proc.stdout.strip()))
        return self._contained_cache[sha]

    def last_touch(self, path: str) -> str | None:
        if path not in self._touch_cache:
            out = git("log", "-1", "--format=%H", self.ref, "--", path,
                      root=self.root).strip()
            self._touch_cache[path] = out or None
        return self._touch_cache[path]


class Candidate:
    __slots__ = ("path", "sha", "evidence", "kind", "verdict", "date",
                 "reviewer", "pr", "note")

    def __init__(self, path: str, sha: str | None, evidence: str, kind: str,
                 verdict: str, pr: int | None = None, note: str = "") -> None:
        self.path = path
        self.sha = sha
        self.evidence = evidence
        self.kind = kind
        self.verdict = verdict
        self.pr = pr
        self.note = note
        self.date: str | None = None
        self.reviewer: str | None = None

    def to_json(self) -> dict:
        return {
            "path": self.path,
            "sha": self.sha,
            "date": self.date,
            "evidence_source": self.evidence,
            "kind": self.kind,
            "verdict": self.verdict,
            "reviewer": self.reviewer,
            "pr": self.pr,
            "note": self.note,
        }


def extract_pr(text: str) -> int | None:
    m = re.search(r"(?i)\bPRs?\s*#(\d+)", text)
    return int(m.group(1)) if m else None


def is_plausible_path(raw: str) -> bool:
    if not raw.endswith(".md") or " " in raw:
        return False
    if raw.startswith(("http", "#", "...", "<")):
        return False
    return True


def normalise_path(raw: str, tracked: set[str]) -> str | None:
    candidate = raw[2:] if raw.startswith("./") else raw
    if candidate in tracked:
        return candidate
    for hint in PATH_HINTS:
        if f"{hint}{candidate}" in tracked:
            return f"{hint}{candidate}"
    return None


def clause_links(clause: str, tracked: set[str]) -> list[str]:
    """Tracked page paths named in one clause, in order of appearance."""
    found: list[tuple[int, str]] = []
    for m in BACKTICKED_RE.finditer(clause):
        raw = m.group(1).strip()
        if is_plausible_path(raw):
            path = normalise_path(raw, tracked)
            if path:
                found.append((m.start(), path))
    for m in MD_LINK_RE.finditer(clause):
        path = normalise_path(m.group(1), tracked)
        if path:
            found.append((m.start(), path))
    first: dict[str, int] = {}
    for pos, path in found:
        first.setdefault(path, pos)
    return [p for p, _ in sorted(first.items(), key=lambda kv: kv[1])]


def sentence_split(text: str) -> list[str]:
    parts = re.split(r"(?<=[.;:])\s+(?=[A-Z(\[`*])", text)
    return [p for p in parts if p.strip()]


def verdict_in(text: str) -> str | None:
    m = ACCEPT_RE.search(text)
    if m:
        return m.group(1).lower()
    m = RETENTION_RE.search(text)
    if m:
        return m.group(0).lower()
    return None


def sha_after_verdict(clause: str, repo: Repo) -> tuple[str | None, str]:
    """The revision a clause binds, preferring one stated after the verdict."""
    m = ACCEPT_RE.search(clause) or RETENTION_RE.search(clause)
    span = m.end() if m else 0
    tail, head = clause[span:], clause[:span]
    for segment, where in ((tail, "after-verdict"), (head, "before-verdict")):
        for regex in (SHA_RE, BARE_SHA_RE):
            last: str | None = None
            for mm in regex.finditer(segment):
                full = repo.sha(mm.group(1))
                if full:
                    last = full
            if last:
                return last, where
    return None, "no-revision-stated"


def harvest_evidence(repo: Repo, tracked: set[str]) -> tuple[list[Candidate], list[str]]:
    """Sweep docs/evidence/documentation/ for page-level acceptance records.

    An acceptance record states its exact reviewed revision in its opening
    paragraph ("from the exact merged pull request (PR) #208 commit `<sha>`",
    "The exact base is the #214 merge `<sha>`") and dispositions the pages it
    reviewed in a table. Binding that stated revision to a listed page is the
    record's own claim, so the row is `batch-level`, not an inference.
    """
    candidates: list[Candidate] = []
    notes: list[str] = []
    evidence_root = repo.root / EVIDENCE_DIR_REL
    for md in sorted(evidence_root.glob("*.md")):
        rel = f"{EVIDENCE_DIR_REL}/{md.name}"
        text = md.read_text(encoding="utf-8", errors="replace")
        head = "\n".join(text.splitlines()[:20])
        shas: list[str] = []
        for token in SHA_RE.findall(head) + BARE_SHA_RE.findall(head):
            full = repo.sha(token)
            if full and full not in shas and repo.tree(full) & tracked:
                shas.append(full)
        pr = extract_pr(head)
        rows = 0
        for lineno, line in enumerate(text.splitlines(), start=1):
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            paths: list[str] = []
            for raw in BACKTICKED_RE.findall(cells[0]):
                if is_plausible_path(raw):
                    resolved = normalise_path(raw, tracked)
                    if resolved:
                        paths.append(resolved)
            verdict = verdict_in(" ".join(cells[1:]))
            if not paths or not verdict:
                continue
            rows += 1
            for path in paths:
                if shas and not repo.exists_at(shas[0], path):
                    # The record names a page that did not exist at the
                    # revision it states, so the record's stated revision is
                    # not this page's acceptance revision. Record nothing
                    # rather than bind a revision that cannot be right.
                    continue
                cand = Candidate(
                    path=path, sha=shas[0] if shas else None,
                    evidence=f"{rel}:{lineno}", kind="evidence-record-batch",
                    verdict=verdict, pr=pr,
                )
                if not shas:
                    cand.note = "record states a disposition but no revision"
                candidates.append(cand)
        if rows:
            notes.append(f"{rel}: {rows} disposition row(s), revision "
                         f"{shas[0][:12] if shas else 'UNSTATED'}")
    return candidates, notes


TRACKER_ROW_RE = re.compile(r"^\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")


def harvest_tracker(repo: Repo, tracked: set[str]) -> tuple[list[Candidate], list[str]]:
    """Sweep the tracker for acceptance statements that name a page and a revision."""
    candidates: list[Candidate] = []
    notes: list[str] = []
    text = (repo.root / TRACKER_REL).read_text(encoding="utf-8", errors="replace")

    for lineno, line in enumerate(text.splitlines(), start=1):
        is_row = bool(TRACKER_ROW_RE.match(line))
        if is_row:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            scopes = [(cell, cell) for cell in cells]
        else:
            scopes = [(line, sentence) for sentence in sentence_split(line)]
        for scope, clause in scopes:
            verdict = verdict_in(clause)
            if not verdict:
                continue
            paths = clause_links(clause, tracked)
            if not paths:
                continue
            sha, where = sha_after_verdict(clause, repo)
            pr = extract_pr(clause)
            for path in paths:
                if sha and not repo.exists_at(sha, path):
                    # The statement's revision predates the page, so it cannot
                    # be that page's acceptance; record the verdict without a
                    # revision instead of a revision that is provably wrong.
                    cand = Candidate(
                        path=path, sha=None,
                        evidence=f"{TRACKER_REL}:{lineno}",
                        kind="tracker-row-cell" if is_row else "tracker-sentence",
                        verdict=verdict, pr=pr,
                        note=(f"statement names revision {sha[:12]}, but this path "
                              f"does not exist at it; revision not bound"),
                    )
                    candidates.append(cand)
                    continue
                cand = Candidate(
                    path=path, sha=sha, evidence=f"{TRACKER_REL}:{lineno}",
                    kind="tracker-row-cell" if is_row else "tracker-sentence",
                    verdict=verdict, pr=pr,
                )
                if sha is None:
                    cand.note = "statement records a verdict without a revision"
                elif not repo.touches(sha, path):
                    cand.note = (f"revision {sha[:12]} ({where}) does not touch "
                                 f"this path - binding needs review")
                candidates.append(cand)
    notes.append(f"tracker: {len(candidates)} page/revision statement(s)")
    return candidates, notes


def newest_first(repo: Repo, cands: list[Candidate]) -> list[Candidate]:
    for cand in cands:
        cand.date = repo.date(cand.sha) if cand.sha else None
    return sorted(
        cands,
        key=lambda c: (c.date or "", c.sha or "", c.evidence),
        reverse=True,
    )


def load_stated(repo: Repo, tracked: set[str]) -> tuple[list[Candidate], list[str]]:
    """Read the curated per-page acceptance revisions and verify them.

    The verification is mechanical and reported, never silently repaired: a row
    whose revision does not resolve, or whose path is not tracked, is dropped
    with a note rather than kept on trust.
    """
    candidates: list[Candidate] = []
    notes: list[str] = []
    data = json.loads((repo.root / STATED_REL).read_text(encoding="utf-8"))
    for row in data["rows"]:
        path = row["path"]
        if path not in tracked:
            notes.append(f"STATED DROPPED (path not tracked): {path}")
            continue
        sha = repo.sha(row["sha"])
        if not sha:
            notes.append(f"STATED DROPPED (revision unresolved): {path} "
                         f"`{row['sha']}`")
            continue
        if not repo.exists_at(sha, path):
            notes.append(f"STATED DROPPED (path absent at that revision): {path} "
                         f"`{row['sha']}`")
            continue
        cand = Candidate(
            path=path, sha=sha,
            evidence=f"{data['source_file']}:{row['tracker_line']}",
            kind=row["kind"], verdict="accepted", pr=row.get("pr"),
        )
        if not repo.touches(sha, path):
            cand.note = (f"revision {sha[:12]} does not itself modify this path; "
                         f"the tracker still names it as the revision at which "
                         f"the page is accepted")
        candidates.append(cand)
    notes.append(f"stated-acceptances.json: {len(candidates)} row(s) verified")
    return candidates, notes


def verify_rule_lines(root: Path) -> list[str]:
    """Report whether each cited rule line range still exists in the tracker."""
    lines = (root / TRACKER_REL).read_text(
        encoding="utf-8", errors="replace").splitlines()
    problems = []
    for name, (start, end) in RULE_LINES.items():
        if end > len(lines):
            problems.append(f"{name}: lines {start}-{end} beyond end of file")
    return problems


def build(ref: str, root: Path) -> dict:
    repo = Repo(ref, root)
    paths = tracked_markdown(ref, root)
    classes = classify(paths)
    tracked = set(paths)

    ev, ev_notes = harvest_evidence(repo, tracked)
    tr, tr_notes = harvest_tracker(repo, tracked)
    st, st_notes = load_stated(repo, tracked)
    all_cands = ev + tr + st

    by_path: dict[str, list[Candidate]] = {}
    for cand in all_cands:
        by_path.setdefault(cand.path, []).append(cand)

    rows = []
    unreachable: dict[str, int] = {}
    for path in classes["reader"]:
        cands = newest_first(repo, by_path.get(path, []))
        best = cands[0] if cands else None
        alternates = [
            {
                "last_acceptance_sha": c.sha,
                "date": c.date,
                "evidence_source": c.evidence,
                "evidence_kind": c.kind,
                "pr": c.pr,
                "note": c.note,
            }
            for c in cands[1:4]
            if c.sha and c.kind == "tracker-audit-table"
        ]
        row = {
            "path": path,
            "last_acceptance_sha": best.sha if best else None,
            "reviewer": best.reviewer if best else None,
            "pr": best.pr if best else None,
            "date": best.date if best else None,
            "evidence_source": best.evidence if best else None,
            "confidence": "recorded" if (best and best.sha) else "unknown",
            "acceptance_verdict_recorded": bool(best),
            "evidence_kind": best.kind if best else None,
            "precision": (
                "page-level: the statement names this page and a revision"
                if best and best.kind in ("tracker-row-cell", "tracker-sentence",
                                          "tracker-row", "tracker-audit-table")
                else "batch-level: the record binds its stated revision to every "
                     "page it dispositions" if best and
                best.kind == "evidence-record-batch"
                else None
            ),
            "note": best.note if best else
                    "no git-visible source records a full-page acceptance",
            "alternate_acceptances": alternates,
        }
        sha = row["last_acceptance_sha"]
        if sha and not repo.remote_contained(sha):
            row["acceptance_reachable"] = False
            row["acceptance_unreachable_reason"] = UNREACHABLE_ROW_REASON
            unreachable[sha] = unreachable.get(sha, 0) + 1
        rows.append(row)

    recorded = [r for r in rows if r["confidence"] == "recorded"]
    unknown = [r for r in rows if r["confidence"] == "unknown"]
    verdict_only = [r for r in rows if r["acceptance_verdict_recorded"]
                    and not r["last_acceptance_sha"]]
    notes = ev_notes + tr_notes + st_notes
    if unreachable:
        notes.append(
            "UNREACHABLE acceptance revision(s), contained by no "
            f"{REMOTE_REFS}** ref so a fresh clone does not hold the object: "
            + ", ".join(f"{sha[:12]} x{count}"
                        for sha, count in sorted(unreachable.items())))
    return {
        "reader_pages": rows,
        "candidates": [c.to_json() for c in newest_first(repo, all_cands)],
        "acceptance_reachability": {
            "rule": REACHABILITY_RULE,
            "probe": REACHABILITY_PROBE,
            "rows_annotated": sum(unreachable.values()),
            "unreachable_revisions": [
                {"sha": sha, "rows": count}
                for sha, count in sorted(unreachable.items())
            ],
        },
        "counts": {
            "tracked_markdown": len(paths),
            "generated_reports": len(classes["generated_reports"]),
            "fixtures": len(classes["fixtures"]),
            "reader_pages": len(classes["reader"]),
            "rows_emitted": len(rows),
            "recorded": len(recorded),
            "unknown": len(unknown),
            "verdict_recorded_without_revision": len(verdict_only),
            "harvest_candidates": len(all_cands),
            "evidence_candidates": len(ev),
            "tracker_candidates": len(tr),
            "stated_candidates": len(st),
        },
        "notes": notes,
        "class_membership": {
            "generated_reports": classes["generated_reports"],
            "fixture_count": len(classes["fixtures"]),
            "fixture_exceptions": list(FIXTURE_EXCEPTIONS),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build the documentation readability acceptance index."
    )
    ap.add_argument("--repo", default=str(REPO_ROOT))
    ap.add_argument("--ref", default="HEAD")
    ap.add_argument("--write", action="store_true",
                    help="rewrite the index data file")
    ap.add_argument("--report", action="store_true",
                    help="print one line per reader page")
    ap.add_argument("--rows", metavar="PATH",
                    help="print the harvested candidates for one page path")
    ap.add_argument("--candidates", action="store_true",
                    help="print every harvested candidate with its note")
    args = ap.parse_args()

    root = Path(args.repo).resolve()
    data = build(args.ref, root)
    counts = data["counts"]
    print(json.dumps(counts, indent=2))
    for note in data["notes"]:
        print(f"  {note}")

    if args.report:
        for row in data["reader_pages"]:
            sha = row["last_acceptance_sha"] or "-"
            print(f"{row['confidence']:9} {sha[:12]:12} "
                  f"{row['evidence_source'] or '-':72} {row['path']}")
    if args.rows:
        for row in data["reader_pages"]:
            if row["path"] == args.rows:
                print(json.dumps(row, indent=2))
        for cand in data["candidates"]:
            if cand["path"] == args.rows:
                print(json.dumps(cand))
    if args.candidates:
        for cand in data["candidates"]:
            print(f"{cand['date'] or '-':10} {(cand['sha'] or '-')[:12]:12} "
                  f"{cand['kind']:22} {cand['evidence_source']:66} "
                  f"{cand['path']}")
            if cand["note"]:
                print(f"           note: {cand['note']}")
    if args.write:
        out = root / INDEX_REL
        payload = {
            "schema": "aegis.documentation-acceptance-index/1",
            "source_revision": git("rev-parse", args.ref, root=root).strip(),
            "source_repository": "ModernNomad-98/Project-Aegis",
            "rule_text_file": TRACKER_REL,
            "rules": RULE_LINES,
            "acceptance_reachability": data["acceptance_reachability"],
            "counts": counts,
            "class_membership": data["class_membership"],
            "reader_pages": data["reader_pages"],
        }
        out.write_text(
            json.dumps(payload, indent=2, sort_keys=False) + "\n",
            encoding="utf-8", newline="\n",
        )
        print(f"wrote {out.relative_to(root)} ({len(data['reader_pages'])} rows)")

        verdicts = {
            "schema": "aegis.documentation-acceptance-index.verdicts/1",
            "purpose": (
                "Stage 1 of the acceptance index: the recorded verdicts, which "
                "do NOT include the reviewer identity or the PR link for most "
                "rows, because the tracker records those in some rounds and not "
                "in others. A null reviewer/pr here means the source did not "
                "state it, not that no review happened."
            ),
            "source_revision": payload["source_revision"],
            "rule_text_file": TRACKER_REL,
            "rules": RULE_LINES,
            "counts": counts,
            "candidates": data["candidates"],
        }
        stage1 = root / STAGE1_REL
        stage1.write_text(
            json.dumps(verdicts, indent=2, sort_keys=False) + "\n",
            encoding="utf-8", newline="\n",
        )
        print(f"wrote {stage1.relative_to(root)} "
              f"({len(data['candidates'])} candidates)")

    problems = verify_rule_lines(root)
    if problems:
        print("RULE CITATION PROBLEMS:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
