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
| `check_index.py` | The official-count decision procedure: prints accepted / provably pending / no recorded acceptance / within-10 / cannot-decide / withdrawn-pending-re-review / partial-disposition buckets and the official pending count, at the pinned `--ref`. A latest withdrawal is never an acceptance, and an active partial disposition is decided before the withdrawal bucket. |
| `partial-dispositions.json` | Schema 1: the instrument-level partial-disposition record. One row per page: the page, `"partial"`, the cancelling `withdrawal_id` and `withdrawal_revision`, the evidence source and a fixed 40-hex `evidence_ref`, the verbatim `quote`, and the reviewer/date attribution from the keeper row. It records a gap, never an acceptance, and it is validated through the builder's own `find_table`/`validate_rows`. |
| `verify_ground_truth.py` | Checks the index against the 19-page relabel set, the fixture/report exclusions, the row-count reconciliation, and the six lost commits. |
| `scan_*.py`, `investigate_commits.py` | Historical diagnostics from the frozen builder; no longer inputs. They write nothing and apply nothing. |
| `tests/` | `test_verify_ground_truth.py` (failed-diff-is-never-zero and the schema-v2 format), `test_index_schema.py` (the four prose blind spots and the three named misreadings as negative cases; per-row blob/quote/containment checks; loud malformed-row failure; lost-commit rules; shallow refusal) and `test_check_index.py` (a fabricated zero-drift withdrawal is never accepted, with a mutation control that runs the base checker on the same case; the active-partial precedence; an inactive disposition moves no count; every sidecar error exits 2; the C4 identities on the committed index). |

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
withdrawn_pending_rereview + partial_disposition_pending +
(recorded_acceptance_within_10_lines not covered by a recorded targeted-review
row). The tool states its basis; no bucket is silently collapsed.

A page whose latest recorded keeper event is a **withdrawal** (AEGIS-APR-117)
is never an acceptance: it is classified into `withdrawn_pending_rereview`
before reachability and drift, so neither a zero drift nor a reachable
revision can turn a cancellation into an acceptance. A **partial
disposition** recorded in `partial-dispositions.json` is decided **before**
the withdrawal bucket: a withdrawal **with** an ACTIVE disposition is
`partial_disposition_pending`, and **without** one it is
`withdrawn_pending_rereview`. A disposition is active only when the page has
no index row, or when the index's effective event is that withdrawal at that
revision; a disposition on a page the index records as an acceptance is
INACTIVE, prints as declared but not applied, and changes no count, so a
stale disposition can never demote an accepted page. The two buckets are
disjoint — `withdrawn + partial` equals the number of latest-withdrawal pages
— so no page is counted twice. A malformed or unreadable record, an unknown
disposition, a duplicate page, an unreadable evidence source, an
`evidence_ref` that is not a fixed 40-hex commit contained in
`refs/remotes/origin/main`, a quote that is not verbatim at that ref, or a
`withdrawal_id` that is not exactly one withdrawal row for that page makes
the checker exit 2 with the reason; a misconfigured `--partial-dispositions`
path fails the same way instead of silently disabling the feature.

## Known limits

* Lost-commit events (D73 row 5) are recorded, never bound, never dropped;
  their pages count as pending until re-reviewed.
* Targeted-review rows (AEGIS-APR-116) and withdrawal rows (AEGIS-APR-117)
  are schema-supported; the one-time backfill transcribed full-page
  acceptances only (lead decision 1), so none exist yet.
* Historical targeted reviews were not transcribed; transcribing them later
  is a flagged Open item (D73 row 4, D84).
* **The docstring's accepted sentence is narrower than the code, and this
  change does not close that gap.** At main, 10 accepted pages rest on
  `targeted-review` rows (AEGIS-APR-116) although the docstring requires a
  `full-page-acceptance` row; this change removes the four withdrawal
  acceptances and leaves the targeted-review divergence disclosed here, with
  no count movement caused by that disclosure.
* **A withdrawal's revision is stored in the generated view's
  `last_acceptance_sha` field.** For a withdrawal that field holds the
  cancelling row's revision, not an acceptance; the checker ignores it for a
  withdrawal. Renaming it would change generated content, which belongs to the
  separate rebuild (AEGIS-APR-115), not to this instrument change.
* **A partial disposition is instrument-level.** The ledger's four event
  kinds have no partial kind (the consolidated contract names
  `full-page-acceptance`, `targeted-review`, `withdrawal` and
  `lost-commit`), so a partial verdict is recorded beside the checker and
  bound to the keeper row's evidence rather than as a fifth keeper kind. No
  keeper row is added, edited or re-typed by that record.

## Official count reference (pinned)

A durable citation point, recorded by D96 (2026-10-11) — NOT the live
figure. The live figure remains `check_index.py` run at the current ref;
this section pins one historical reading so later readers can cite it
without re-deriving it, and later rebuilds at newer refs supersede it.

- **Pinned ref:** `408e4d6a2046b37afe7912e9c8643474df7ab037` ("fix: LF-pinned
  writer and APR-125 CONSUMED ID (SD-D REVISE round 2)"; an ancestor of
  origin/main).
- **The six labeled numbers at that ref:** reader pages **631** / accepted
  on recorded review **50** / provably pending **4** / no recorded
  acceptance **564** / recorded acceptance within 10 lines **7** /
  cannot-decide **6** — **official pending count 581**.
- **Computation method** (this README's formula above): provably_pending +
  no_recorded_acceptance + cannot_decide + (within-10 not covered by a
  recorded targeted-review row).
- **Exact re-derivation command** (full clone; refs/remotes + refs/pull
  heads fetched):

  ```bash
  python -B tools/readability_acceptance/check_index.py --ref 408e4d6a2046b37afe7912e9c8643474df7ab037
  ```

- **Provenance:** the six numbers above were re-derived byte-for-byte by
  Stage C of the Q4 durable-acceptance-refs lane at the implementation base
  before this section was appended (recorded in D96).
