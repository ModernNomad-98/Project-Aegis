# AEGIS-APR-117 withdrawal and re-record — Phase 4 re-read lane D, batch 2, 2026-10-16

Recorded by **DeepSeek-4.1-Flash (deepseek-flash)**, keeper identity `deepseek-flash-apr117-keeper`,
an agent that ran none of the eight reads, wrote none of the eight pages, wrote none of the eight
withdrawn rows, and holds no other stage of pull request (PR) #778 — the lane D batch 2 pull
request. This is a **Stage C** recording act: Stage C is the implementation step of this
repository's seven-stage delivery workflow, and for this change it consists of appending records
rather than editing pages.

## Why these rows exist

AEGIS-APR-101 (the register entry that defines the recording-only ledger-keeper role) requires
the keeper to be a **different agent** from the page's author and accepting reviewer, and its
Scope FORBIDDEN begins 'No self-review'. Lane D's second batch appended eight
`full-page-acceptance` rows — **K-381...K-388** — whose `Reviewer` cell is
`readability-phase4-lane-d-implementer-c2`, the same agent that read the eight pages and wrote
those rows. That condition is therefore **not satisfied** for those eight rows, and the lane's own
ledger section declares it, leaving 'the disposition of that withdrawal and re-record ... to the
merge holder'. That disposition had not been performed. This record performs it on the route
**owner decision 3 of 2026-10-15** directed — **no ratification of the carry; use the
AEGIS-APR-117 route** — the same route PR #777 (lane A batch 2) and PR #787 (lane D batch 1)
already used: append withdrawal rows that cancel the same-agent rows, then append fresh acceptance
rows for the same pages **from the same evidence**, recorded by a different, eligible keeper.
**No page is re-read; the reads stand; only the recording authority changes.** All eight pages
carry a full-page verdict, so all eight end in a fresh `full-page-acceptance` row. The ledger is
never rewritten: the withdrawn rows (K-381...K-388), the withdrawal rows (K-389W, K-390W, K-391W,
K-393W, K-394W, K-395W, K-396W, K-397W) and the fresh rows (K-397...K-404) all remain physically
present in the consolidated keeper table.

*Glosses for the labels above.* **AEGIS-APR-101**: the owner-approval-register entry that created
the ledger-keeper role. **AEGIS-APR-117**: the register entry that lets the keeper cancel a wrong
recorded row by appending a withdrawal row bound to evidence. **Keeper**: the distinct agent role
that records acceptance rows. **Lane D batch 2**: the second group of eight pages assigned to the
fourth of the four re-read workstreams. **Keeper row**: one row of the consolidated acceptance
table that binds a page's acceptance to its evidence, recording agent and content hash.

## Binding method

- **Acceptance revision:** every row binds the lane's reviewed head e2a3e20b7c20ef8385b219b39c6405237163406f (the same
  revision the withdrawn rows bind; the read is not repeated).
- **Blob IDs, recomputed this round, never transcribed:** every withdrawal and fresh row's
  `Blob ID` equals `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:<page>`. All eight were re-resolved this round
  and **all eight match the withdrawn rows' cells**.
- **Original quotes:** each block's *Original quote* line is transcribed verbatim from the
  withdrawn row, whose quote the builder already validates against the lane batch record
  docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md (the evidence source of the withdrawn rows). The fresh
  rows cite **this** file as their evidence source, and each transcribed quote is bound here
  byte-for-byte, so the build-time quote check (`build_index.py`) finds both the quote and the
  revision at the built ref.
- **Withdrawal quotes:** each *Withdrawal row quote* line below is the withdrawal row's own
  quote; the `WD-D2-<n>` prefix names the withdrawal, the row it cancels and that row's
  accepting reviewer, so the cancellation stays robust to any later renumbering of the stable
  ids.
- **Evidence scope:** this file is the bound evidence for the sixteen appended rows only. It
  records no re-reading, confers no acceptance AEGIS-APR-101 does not allow the keeper to
  confer, and edits no page.

## Stable-id choice — measured against `main` and every fetched pull-request head

`build_index.py` picks a page's latest event by **string comparison of the stable id**
(`derive_reader_pages`: `if cur is None or ev[stable_id] > cur[stable_id]`). So for each page
the ids must satisfy **withdrawn < withdrawal < fresh** lexically, or the fresh row is not the
page's latest event and the page does not read as accepted.

- **Fresh block:** **K-397...K-404** — the first free contiguous eight in lane D's allocated band
  **K-381..K-480** (band table in S4 of `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md`; no
  tracked `KEEPER-ID-ALLOCATION.md` exists). Measured: band D's highest row id anywhere is
  **K-396**; K-397...K-404 occur in no keeper-table row.
- **Withdrawal block:** **K-389W, K-390W, K-391W, K-393W, K-394W, K-395W, K-396W, K-397W** — the
  first free `W`-suffixed ids above the withdrawn rows. **K-392W is skipped because a merged
  row holds it** (PR #787's withdrawal of K-392); re-using it would make the build fail loudly
  with a duplicate stable id. K-381W...K-388W are likewise already held (the lane D batch 1
  withdrawal rows), so the mirror-style ids the withdrawn rows would otherwise take are not
  available.
- **Absence measured, not assumed** — the standing rule is that new keeper ids are checked
  against every OPEN pull request, not only `main`: all sixteen ids were checked against
  `refs/remotes/origin/main` and against every fetched `refs/pull/*/head` — **1,571 refs /
  797 pull-request heads** at measurement on 2026-10-16 — and occur in no keeper-table row in
  any of them (see the id-audit section below).

## The eight pages (one block per withdrawn row; all eight end in a fresh acceptance row)

### WD-D2-1 — lane D batch 2, withdrawn row K-381, withdrawal row K-389W, fresh row K-397

- Page: docs/evidence/documentation/open-decisions-readability-2026-09-23.md
- Original keeper (accepting reviewer agent): readability-phase4-lane-d-implementer-c2
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:docs/evidence/documentation/open-decisions-readability-2026-09-23.md` (never transcribed): c47a06701f15a0a97f4f5872008f0d97848166ff
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md: LD-9 accepted: docs/evidence/documentation/open-decisions-readability-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-D2-1 withdraws K-381 (readability-phase4-lane-d-implementer-c2): LD-9 accepted: docs/evidence/documentation/open-decisions-readability-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-397, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-D2-2 — lane D batch 2, withdrawn row K-382, withdrawal row K-390W, fresh row K-398

- Page: docs/evidence/documentation/operational-guides-seven-readability-2026-09-23.md
- Original keeper (accepting reviewer agent): readability-phase4-lane-d-implementer-c2
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:docs/evidence/documentation/operational-guides-seven-readability-2026-09-23.md` (never transcribed): 98d84943913fc7cc52c3d96735e72c673c5bbee0
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md: LD-10 accepted: docs/evidence/documentation/operational-guides-seven-readability-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-D2-2 withdraws K-382 (readability-phase4-lane-d-implementer-c2): LD-10 accepted: docs/evidence/documentation/operational-guides-seven-readability-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-398, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-D2-3 — lane D batch 2, withdrawn row K-383, withdrawal row K-391W, fresh row K-399

- Page: docs/evidence/documentation/operational-proposals-five-readability-2026-09-23.md
- Original keeper (accepting reviewer agent): readability-phase4-lane-d-implementer-c2
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:docs/evidence/documentation/operational-proposals-five-readability-2026-09-23.md` (never transcribed): 5cf92ad55a628ea5568d5c6b70591104a84e99bf
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md: LD-11 accepted: docs/evidence/documentation/operational-proposals-five-readability-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-D2-3 withdraws K-383 (readability-phase4-lane-d-implementer-c2): LD-11 accepted: docs/evidence/documentation/operational-proposals-five-readability-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-399, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-D2-4 — lane D batch 2, withdrawn row K-384, withdrawal row K-393W, fresh row K-400

- Page: docs/evidence/documentation/readability-closeout-reread-2026-10-12.md
- Original keeper (accepting reviewer agent): readability-phase4-lane-d-implementer-c2
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:docs/evidence/documentation/readability-closeout-reread-2026-10-12.md` (never transcribed): 8b64260babe8846a3c75d9ea062cdf804a19a072
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md: LD-12 accepted: docs/evidence/documentation/readability-closeout-reread-2026-10-12.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-D2-4 withdraws K-384 (readability-phase4-lane-d-implementer-c2): LD-12 accepted: docs/evidence/documentation/readability-closeout-reread-2026-10-12.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-400, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-D2-5 — lane D batch 2, withdrawn row K-385, withdrawal row K-394W, fresh row K-401

- Page: docs/evidence/documentation/readability-f1f5-reread-2026-10-12.md
- Original keeper (accepting reviewer agent): readability-phase4-lane-d-implementer-c2
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:docs/evidence/documentation/readability-f1f5-reread-2026-10-12.md` (never transcribed): 68ecfd1ec0a2bbcac08854bb36f2ffd17cc0b5a5
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md: LD-13 accepted: docs/evidence/documentation/readability-f1f5-reread-2026-10-12.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-D2-5 withdraws K-385 (readability-phase4-lane-d-implementer-c2): LD-13 accepted: docs/evidence/documentation/readability-f1f5-reread-2026-10-12.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-401, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-D2-6 — lane D batch 2, withdrawn row K-386, withdrawal row K-395W, fresh row K-402

- Page: docs/evidence/documentation/readability-final3-reread-2026-10-12.md
- Original keeper (accepting reviewer agent): readability-phase4-lane-d-implementer-c2
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:docs/evidence/documentation/readability-final3-reread-2026-10-12.md` (never transcribed): 4acfb53f8963f54db0029d088bff14b519c867ca
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md: LD-14 accepted: docs/evidence/documentation/readability-final3-reread-2026-10-12.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-D2-6 withdraws K-386 (readability-phase4-lane-d-implementer-c2): LD-14 accepted: docs/evidence/documentation/readability-final3-reread-2026-10-12.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-402, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-D2-7 — lane D batch 2, withdrawn row K-387, withdrawal row K-396W, fresh row K-403

- Page: docs/evidence/documentation/readability-ledger-reread-2026-10-13.md
- Original keeper (accepting reviewer agent): readability-phase4-lane-d-implementer-c2
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:docs/evidence/documentation/readability-ledger-reread-2026-10-13.md` (never transcribed): 14b2bcf6fd7ea2d530f1c37dbf2b5ea24826b454
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md: LD-15 accepted: docs/evidence/documentation/readability-ledger-reread-2026-10-13.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-D2-7 withdraws K-387 (readability-phase4-lane-d-implementer-c2): LD-15 accepted: docs/evidence/documentation/readability-ledger-reread-2026-10-13.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-403, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-D2-8 — lane D batch 2, withdrawn row K-388, withdrawal row K-397W, fresh row K-404

- Page: docs/evidence/documentation/readability-ledger-selfcost-2026-10-13.md
- Original keeper (accepting reviewer agent): readability-phase4-lane-d-implementer-c2
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:docs/evidence/documentation/readability-ledger-selfcost-2026-10-13.md` (never transcribed): 1a70a714bcc317930cc8accb873ea642989cca5b
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md: LD-16 accepted: docs/evidence/documentation/readability-ledger-selfcost-2026-10-13.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-D2-8 withdraws K-388 (readability-phase4-lane-d-implementer-c2): LD-16 accepted: docs/evidence/documentation/readability-ledger-selfcost-2026-10-13.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-404, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

## What this act did not verify

- Whether the eight pages were truly read 'whole, line by line, as prose' — the lane reader's
  process claim is not checkable from the repository. This act verified the pages' bytes, the row
  bindings, the id absence and the builder's selection; not the act of reading.
- Whether a fresh Stage D audit, a fresh Stage E validation and a fresh Stage F review are owed:
  they **are** owed, and this file records that rather than verifying it. This act writes new
  bytes on the pull-request branch, so the Stage D ACCEPT at
  `89dd380847ca5d59027781f2ca84b3f2bbb8d0a9` is **void** for the head it produces: that
  verdict names a head this act replaces. The seven-stage requirement is not shortened — Stage E
  (validation: the applicable checks run at the new head, with their commands and output) and
  Stage F (the final independent review that names the exact 40-character head) remain owed.
- This file itself: it is a new reader page with no keeper row, so it counts pending, like every
  other evidence record before it.

