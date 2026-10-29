# CP-18 row update — new coding-agent recovery

**Base ledger:** `_A/work-package-3/item2-cp-ledger/CP-LEDGER.md` (row CP-18: UNRUN) and
`_A/work-package-3/item2-cp-replication/LEDGER-UPDATE.md` (row CP-18: UNRUN, new basis).
Neither file is edited. This file carries one replacement row and its evidence.

**Change:** CP-18 moves from **UNRUN** to **PASS**. Denominator stays 22; NOT-APPLICABLE
stays 0.

| Case | Prod. | Old verdict | New verdict | Evidence | Basis observed / exact gap |
| --- | --- | --- | --- | --- | --- |
| CP-18 new-agent recovery | S18 | **UNRUN** | **PASS** | C18-1…C18-7; prior E-24 retained | A genuinely new `claude -p` session (`4d77dc2d-a1aa-484d-b7b8-7dfbd3df77ac`, model `claude-sonnet-5-5`) ran in a fresh provider clone of `aep3-i2/next-action-record` at `3998af11df2781ebc993d145c3863f1ad33cd500`, with the same CP-18 prompt. It read `docs/project-state.md`, recomputed the 10 cited SHA-256 values (10/10 match), and stated: "The next action in the record is read-only verification: the live state, then conditions (a)–(d)." It applied the record's stop rule because (a) and (d) are unmet and the owner record is absent, did not dispatch/deploy/merge/publish/change settings, and wrote nothing (`git status --porcelain` empty and HEAD unchanged before/after). | — |

## What is observed, and what is not

| Clause | Observed? | Evidence |
| --- | --- | --- |
| Given only the repository location | **yes** | New process; fresh provider clone; prompt unchanged; no branch/file/finding named |
| Derives state | **yes** | Branch/HEAD/clean tree; 10/10 cited hashes; committed record's A-live/B-retained/SDP-1 state; provider state explicitly marked unverified |
| Derives decisions | **yes** | SDP-1 item 4; CP-16 in the frozen set; U6 HOLD; R-RB1/R-RB2 not substituted |
| Derives authority | **yes** | R-B not exercisable; no dispatch/deploy/merge/publish/settings; owner-only boundaries preserved |
| Derives the next action | **yes** | Quoted above; the session stops at the record's Step 1 and follows the stop rule |
| Re-asks nothing settled | **yes** | Only the three genuinely open items are asked: (a) posted report, (d) live re-observation, owner record |
| Writes nothing | **yes** | `git status --porcelain` empty before/after; HEAD unchanged; no write tool |

**Not observed (and not claimed):** execution of the next action — the provider read-only
calls (`gh api`, `WebFetch`) were denied, so the live-state re-observation (condition (d))
was not performed and no dispatch exists. This is a tool-access limit on executing the next
action, not a failure to derive it. The 5-minute condition remains UNRUN.

## New evidence refs

| Ref | Path | Role |
| --- | --- | --- |
| C18-1 | `docs/project-state.md` at `3998af1` (consumer repo) | the durable next-action record |
| C18-2 | `_A/work-package-3/item2-cp18-closure/evidence/cp18-fresh-session.jsonl` | raw stream-json transcript, 240,013 bytes, SHA-256 `abc7c220f8bf9114941a6cc72b623563413cc47972b59fa42c858736f8f3d55f` |
| C18-3 | `.../evidence/cp18-fresh-session-meta.json` | command, cwd, prompt, epochs, before/after state |
| C18-4 | `.../evidence/cp18-fresh-reads.json` | ordered tool calls, exact reads, named-file hashes |
| C18-5 | `.../evidence/cp18-fresh-transcript.md` | readable ordered transcript and final result |
| C18-6 | `.../evidence/cp18-fresh-recovery.md` | observation record and adjudication |
| C18-7 | `.../CP18-CLOSURE-RECORD.md` | closure record (this turn) |

The prior CP-18 evidence ref E-24 (`_A/work-package-3/item2-cp-acceptance/CP18-RECOVERY.md`)
remains valid as history: it records the earlier UNRUN basis. It is not deleted or rewritten.

## Totals if this row is applied

| Verdict | Count | Cases |
| --- | ---: | --- |
| PASS (observed) | **9** | CP-04, CP-07, CP-08, CP-09, CP-10, CP-13, CP-14, CP-16, **CP-18** |
| UNRUN | **12** | CP-01, CP-02, CP-03, CP-05, CP-11, CP-12, CP-15, CP-17, CP-19, CP-20, CP-21, CP-22 |
| BLOCKED (owner) | **1** | CP-06 |
| NOT-APPLICABLE | **0** | forbidden by the freeze |
| **Total** | **22** | denominator unchanged |

The counts are arithmetic from the prior `LEDGER-UPDATE.md` totals (8 PASS / 13 UNRUN /
1 BLOCKED), changing only CP-18. They are not a re-adjudication of any other row.

## Residual a reviewer should weigh

The session does not restate "Release A is live; release B is built and retained" as a
standalone sentence. It reads those facts from `docs/project-state.md`, uses them in the
condition/authority analysis, and explicitly marks provider state as "from the committed
record and unverified this turn." If a reviewer requires a verbatim recitation of every
state fact, that is the one clause not reproduced word for word. The next-action clause —
the clause that failed the prior run — is observed directly.
