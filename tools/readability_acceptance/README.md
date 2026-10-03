# Documentation readability acceptance index

This directory holds the missing instrument for the documentation readability
backlog in [`docs/roadmaps/aegis-documentation-readability-backlog.md`](../../docs/roadmaps/aegis-documentation-readability-backlog.md):
a per-path map from a reader page to the revision at which it was last accepted
full-page. The backlog defines a decision procedure whose only input is that map
("A larger change, meaning more than 10 changed lines on that page or any new
section, returns the page to **pending**", tracker L2484-2493), and the
repository stores the map as prose, so until now no command could produce the
pending count.

**This instrument decides nothing.** It records what sources state, with the
source location, and leaves `null` where no git-visible source states it. It does
not edit the tracker, does not accept a page, and does not replace the
independent review the rule requires.

## Files

| File | What it is |
| --- | --- |
| `acceptance-index.json` | The index: one row per reader page, with `path`, `last_acceptance_sha`, `reviewer`, `pr`, `date`, `evidence_source`, `confidence`, plus `evidence_kind`, `precision`, `note` and `alternate_acceptances`. |
| `acceptance-verdicts-stage-1.json` | Stage 1: every recorded verdict the sweep found, including the ones that name no revision. Reviewer identity and PR links are mostly absent because the sources record them in some rounds and not others; `null` means the source did not state it. |
| `stated-acceptances.json` | The per-page acceptance revisions the tracker states in words but does not store as data, each with the tracker line it was read from. `build_index.py` verifies every revision resolves and that the path exists at it. |
| `build_index.py` | Re-runnable builder: sweeps the tracker, `docs/evidence/documentation/**`, and the stated revisions, then writes the JSON files. |
| `check_index.py` | Re-runnable decision procedure: prints the bound, the no-recorded-acceptance remainder, and the undecidable set. |
| `verify_ground_truth.py` | Checks the index against the known 19-page relabel set, the generated-report and fixture exclusions, and the row-count reconciliation. |
| `scan_*.py`, `investigate_commits.py` | Diagnostics used to curate `stated-acceptances.json`. They write nothing and apply nothing; they exist so a reviewer can re-derive the curation instead of trusting it. |
| `tests/test_verify_ground_truth.py` | Runnable regression test: a failed `git diff` is an undecidable result, never 0 lines, and an absent object is not remote-contained. `.github/` is outside this change, so CI does not discover this directory yet; run it with the command below. |

## Reproduce

```bash
python -B tools/readability_acceptance/build_index.py --write
python -B tools/readability_acceptance/check_index.py            # full listing
python -B tools/readability_acceptance/check_index.py --json
python -B tools/readability_acceptance/verify_ground_truth.py --ref refs/remotes/origin/main
python -B -m unittest discover -s tools/readability_acceptance/tests -p 'test_*.py' -v
```

`check_index.py` prints a **bound plus an unknown remainder**, never one exact
pending figure:

* **provably pending** - a recorded acceptance exists and the page has drifted
  past it by more than 10 added+deleted lines, or gained a `^\+#{1,6} ` section;
* **no recorded acceptance** - the procedure cannot run at all, which is where
  the tracker's "accepted unless listed pending" convention could be hiding
  pages;
* **recorded acceptance within 10 lines** - not returned to pending by revision
  arithmetic, but *not* shown to be accepted either: the rule also says an
  unreviewed edit, however small, needs a targeted review (tracker L2497-2499),
  and git cannot see review.

## Known limits

* An acceptance record under `docs/evidence/documentation/` states one reviewed
  revision for a whole batch, so the row is `precision: "batch-level"`: the
  record binds that revision to every page it dispositions, and the binding is
  the record's own claim rather than an inference, but it is not a per-page
  re-read revision.
* Acceptances recorded only in GitHub pull-request comments are not in git and
  therefore cannot appear here.
* Pages whose acceptance revision was rewritten by a rebase are compared anyway,
  with `rebased_acceptance: true` on the row, because the trees are still
  comparable; `cannot_decide` names every page the procedure could not run for.
* A recorded acceptance revision that no `refs/remotes/**` ref contains is
  **unreachable**: a fresh clone does not hold the object, so `check_index.py`
  reports the row as `cannot_decide` (counted in
  `cannot_decide_unreachable_acceptance`) and never decides it from an object
  only the authoring clone has. Two such revisions appear in this index,
  `65bacc7d6b85` on 6 rows and `d3dcb62a335d` on 1 row; each affected row
  carries `acceptance_reachable: false` with the reason, so the bound is the
  same in a fresh clone as in the authoring mirror. `verify_ground_truth.py`
  reports the same limitation rather than measuring it, and says so as a
  mismatch. A clone with no remote-tracking refs at all therefore reports every
  recorded row this way; run it against a checkout that has the remote.
* This directory is under `tools/`, deliberately outside the gate-guard
  protected set in `.github/workflows/validate-skills.yml`.
