# Documentation readability acceptance index

This directory holds the instrument for the documentation readability backlog
in [docs/roadmaps/aegis-documentation-readability-backlog.md](../../docs/roadmaps/aegis-documentation-readability-backlog.md):
a per-path map from a reader page to the revision at which it was last accepted
full-page. **Since the index-repair switch (D84, 2026-10-10) the official
pending count is the summary printed by `check_index.py` at the pinned ref
(AEGIS-APR-113 item 1, AEGIS-APR-114/115). This is the only page family that
publishes that figure: the ledger publishes no count of its own and cites this
index, and every other counting surface carries the same dated pointer.**

**This instrument decides nothing.** It records what the keeper fixed-format
table states, with the source location, and leaves every page without a row
pending by the no-recorded-acceptance bucket. It does not edit the tracker,
does not accept a page, and does not replace the independent review the rule
requires. `tools/readability_acceptance/` is security-relevant
"approval/evidence tooling under `tools/`" (AEGIS-APR-118); outside
contributions to it receive the additional security review.

## Files

| File | What it is |
| --- | --- |
| `acceptance-index.json` | Schema v2: the events read from the ledger consolidated keeper table (one event per row, with stable ID, event kind, revision, blob ID, quote, reviewer, evidence source, date) plus the derived per-page view. |
| `acceptance-verdicts-stage-1.json` | Stage 1: the same events as verdict rows. |
| `stated-acceptances.json` | **RETIRED as an input (D84).** The repaired builder never reads it; the prose harvester is gone. Kept for history with its purpose note updated. |
| `build_index.py` | Re-runnable builder: parses ONLY the consolidated keeper table (sentinel `<!-- acceptance-index-schema: 1 -->` in the ledger), validates every row per event kind, refuses shallow clones, enforces main-containment, and writes the two JSON files at the pinned `--ref`. |
| `check_index.py` | The official-count decision procedure: prints accepted / provably pending / no recorded acceptance / within-10 / cannot-decide buckets and the official pending count, at the pinned `--ref`. |
| `verify_ground_truth.py` | Checks the index against the 19-page relabel set, the fixture/report exclusions, the row-count reconciliation, and the six lost commits. |
| `scan_*.py`, `investigate_commits.py` | Historical diagnostics from the frozen builder; no longer inputs. They write nothing and apply nothing. |
| `tests/` | `test_verify_ground_truth.py` (failed-diff-is-never-zero and the schema-v2 format) and `test_index_schema.py` (the four prose blind spots and the three named misreadings as negative cases; per-row blob/quote/containment checks; loud malformed-row failure; lost-commit rules; shallow refusal). |

## Reproduce (rebuilds are pinned to a base ref; D73 row 8)

```bash
python -B tools/readability_acceptance/build_index.py --write --ref <pinned-sha>
python -B tools/readability_acceptance/check_index.py --ref <pinned-sha>
python -B tools/readability_acceptance/check_index.py --ref <pinned-sha> --json
python -B tools/readability_acceptance/verify_ground_truth.py --ref <pinned-sha>
python -B -m unittest discover -s tools/readability_acceptance/tests -p "test_*.py" -v
```

`build_index.py` REFUSES shallow clones and requires `refs/remotes/**` and
`refs/pull/*/head` refs. A reviewer rebuild at the same ref must produce a
byte-identical zero diff against the committed JSONs. If main moves by merge
time, the rebuild is redone at the new tip (D73 row 8). Every acceptance
revision must be contained in `refs/remotes/origin/main` (the preservation
rule the owner selected; a stronger refs namespace or tag convention remains
an owner-choice item, flagged in D84).

`check_index.py` prints every bucket and then the official pending count,
computed as provably_pending + no_recorded_acceptance + cannot_decide +
(recorded_acceptance_within_10_lines not covered by a recorded targeted-review
row). The tool states its basis; no bucket is silently collapsed.

## Known limits

* Lost-commit events (D73 row 5) are recorded, never bound, never dropped;
  their pages count as pending until re-reviewed.
* Targeted-review rows (AEGIS-APR-116) and withdrawal rows (AEGIS-APR-117)
  are schema-supported; the one-time backfill transcribed full-page
  acceptances only (lead decision 1), so none exist yet.
* Historical targeted reviews were not transcribed; transcribing them later
  is a flagged Open item (D73 row 4, D84).
