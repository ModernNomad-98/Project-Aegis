# CP-02 — proposed row update (canonical ledger NOT edited)

**Record type:** row replacement proposal for the canonical CP ledger. This task did not edit
_A/work-package-3/item2-cp-ledger/CP-LEDGER.md (21,278 B, 9f3d4f369b7b57be1071f93d92802feea38735da98e409c70b03da50837d7f3d),
nor LEDGER-UPDATE.md, nor the closeout record, nor any plan/freeze/cases file.
**Basis:** CP-02-RECONCILIATION.md (this directory); owner decision CP-02 = A
(OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md, c93c07b8…, lines 11-12).
**Verdict proposed:** **PASS** (operator leg; RV-1 leg open — see §4).

---

## 1. The row as it stands (CP-LEDGER.md line 59, verbatim)

> | CP-02 target and authority | S0; S10 | **UNRUN** | E-06, E-17 | Target, URL and exposure are observed; the frozen row also requires **every planned effect reconciled to a grant or marked NOT GRANTED/INFERRED**, and no independent effect-to-grant reconciliation exists in this evidence set | an effect-by-effect reconciliation against A1 §12 and the R-A/R-B requests |

The gap it names is exactly what this task produced, and the owner has since supplied the missing authority
decision. Both halves of the "closes with" cell are now discharged except the RV-1 reviewer leg.

## 2. Replacement row (drop-in, same six columns)

| Case | Prod. | Verdict | Ev. | Basis observed / exact gap | Closes with |
| --- | --- | --- | --- | --- | --- |
| CP-02 target and authority | S0; S10 | **PASS** | E-06, E-17, E-18, E-19, E-30, E-16, E-22, E-28, E-26 | Owner decision CP-02 = A (2026-10-29 ~06:20 PDT) makes A1 §12 the authoritative allocation. 19/19 planned effects reconciled in item2-cp02/CP-02-RECONCILIATION.md §4: 2 delegated write scope (E1, E2), 3 granted-named (E4, E6, E7), 3 granted-conditional with all four SDP-1 item 4 conditions evidenced before dispatch (E9 8.3 s, E10 129 s, E11 49 s), 3 read-only (E8, E13, E17), 1 not-needed (E18), 1 **INFERRED** (E3, unconfirmed — conformance gap G-01), 6 **NOT GRANTED** and not taken (E5, E12, E14, E15, E16, E19). One repository / one account / one URL observed (ModernNomad-98/aegis-consumer-proof; https://modernnomad-98.github.io/aegis-consumer-proof/); budget leg met with no billing scope and no spend; no source or synthetic grant inherited (A1 §8, SDP-1 §3/SDP-1a, no fixture grant in any dispatch record). 4 deployments / 6 runs / 0 Pages builds / 0 settings changes bound the total provider effect. 3 drift findings recorded against consumer records (D-01 R-EMPTY pre-granted without U7; D-02 A.md points at a request that lacks the grant; D-03 manual-only standing permission vs per-turn U4) — none changes a delivered effect | — (RV-1 verification of this row open; see §4). Findings: item2-cp02/DRIFT-FINDINGS.md |

Evidence-ref note: the row keeps the ledger's existing refs (E-06 A1 §12; E-17 R-B deploy) and adds the reversal,
B-build, readiness, CP-16 and provider refs this reconciliation actually reads. All eleven were re-hashed here and
match the ledger's register (evidence/06-verification.txt §1).

## 3. Totals if this row is applied

Arithmetic from the last recorded totals (item2-cp05-revision/CP-05-ROW-UPDATE.md §5: **10 PASS / 11 UNRUN /
1 BLOCKED**), changing **only** CP-02. Not a re-adjudication of any other row.

| Verdict | Before | After | Cases after |
| --- | ---: | ---: | --- |
| PASS (observed) | 10 | **11** | CP-02, CP-04, CP-05 (revised criterion), CP-07, CP-08, CP-09, CP-10, CP-13, CP-14, CP-16, CP-18 |
| UNRUN | 11 | **10** | CP-01, CP-03, CP-11, CP-12, CP-15, CP-17, CP-19, CP-20, CP-21, CP-22 |
| BLOCKED (owner) | 1 | **1** | CP-06 |
| NOT-APPLICABLE | 0 | **0** | forbidden by the freeze |
| **Total** | 22 | **22** | denominator unchanged |

**Two live caveats for whoever applies this.** (1) CP-06 was answered by the owner at 2026-10-29 ~06:20-06:22 PDT
(four Stage 2 outcomes recorded in the answers record), so the BLOCKED count may move independently of this row;
the arithmetic above deliberately does not anticipate it. (2) CP-12 and CP-22 have owner authorisations in flight
(CP-12 = A merge + merged-main re-run; CP-22 = B designated reviewer) and remain UNRUN until their own records
land. Neither is read by this row.

## 4. The RV-1 leg, stated plainly

Plan v4 line 296 assigns CP-02 to "operator; verified by RV-1", and freeze roll-up rule 4 says "PASS requires at
least one accessible hashed evidence entry **and** a reviewer who is independent of the actor; self-review is not a
pass." This record supplies the operator leg and eleven hashed, accessible evidence entries. **It is not RV-1.**
The natural home for that verification is the CP-22 reviewer designated under CP-22 = B, whose brief already
requires opening and hashing the decisive files.

Precedent for scoring this way, disclosed rather than copied silently: CP-05 was scored PASS with its L7 note
("not an RV-5 verification… the formal RV-5 review remains open"), and CP-08 with note N-1 ("contextual
independence within one harness"). If the closeout requires RV-1 to precede the row, CP-02 is PASS-pending-RV-1 —
not an evidence-free PASS, and not UNRUN.

## 5. Downstream edits the ledger would need (listed, not made)

If the row is applied, the canonical ledger needs four consequential edits, all mechanical:

1. **§2 Totals** — PASS 5 -> 11 (or 10 -> 11 if applied after CP-05), UNRUN 14 -> 10 (or 11 -> 10), and the
   case lists in those two rows.
2. **§3 row** — the replacement row in §2 above.
3. **§5 "Why the other seventeen are not PASS"** — the group row "Needs an unassembled record | CP-02, CP-09,
   CP-22" loses CP-02 and its single-reason sentence needs rewording to "CP-09, CP-22".
4. **§7 Postable STATUS block** — the PASS and UNRUN lists, and the "Next closable without owner or browser" line,
   which currently starts with the CP-19 fixture batch and should now note CP-02 as closed.

Also, if the drift findings are to travel with the ledger, add one line to §8 ("What this task did not do") of the
*next* ledger revision: three drift findings against consumer records recorded in item2-cp02/DRIFT-FINDINGS.md,
none of which was closed by editing a consumer file.

## 6. What this update does not do

- It does not edit any canonical file, any plan, the freeze, cases.json, or any consumer record.
- It does not convert E3 into a grant (G-01 stays open), does not close D-01/D-02/D-03, and does not claim CP-22.
- It does not touch CP-12, CP-19, CP-22, CP-06 or the browser rows, whose states stand exactly as their own
  records leave them.
