# AEP#3 — OWNER DECISIONS APPLIED (2026-10-28 ~20:05 PDT)

Source: Peter, typed directly in the DSH Web GUI Lead session. Applies to AEP3-I1..I8 only.

## 1. Combined audit: YES (conditions)
- For diffs confined to test files and docs/evidence: ONE fresh independent audit covers implementation + validation in a single round.
- Conditions: auditor has not seen the author's work; auditor re-runs the suite; proves every new/changed test can fail against the pre-fix code.
- Any item touching a workflow, validator source, or skill file returns to separate Stage D + E.
- Applies to: AEP3-I3 (after current separate Stage E completes, the Stage F is folded where eligible), AEP3-I4, AEP3-I6, AEP3-I7. AEP3-I8 (workflow) stays separate D+E. AEP3-I5 (evidence only) may use combined.

## 2. Browser rows
- CP-11 / CP-17 / CP-20 accepted as **UNRUN — no browser session supplied by owner**. Record exactly this wording; not deferred, not pending. They do not block Item 2 closeout; the closeout states them UNRUN.

## 3. U6 pre-grant (conditional)
- Publish the source evidence + guide PR via fresh merger WHEN ALL: (i) every non-browser CP row is RUN with a recorded PASS or FAIL; (ii) the R-series has reached its planned end state with observed evidence; (iii) the Item 2 closeout is written.
- Any condition unmet = HOLD, no ask. No separate owner question required when all three hold.

## 4. WSL2 host-class: YES with labeling
- Docker-on-WSL2 uid 1000 counts as a non-root Linux host for affected acceptance rows.
- Record host class each row as: "non-root Linux (WSL2/Docker, uid 1000)" - not bare-metal.
- If a row depends on something the container cannot provide (capabilities, systemd, bind-mount permission semantics), that row is UNRUN with the reason - never PASS.

## 5. Numbering (binding)
- Morning Items 1-4 keep bare labels; every AEP#3 item is **AEP3-I<n>** everywhere from now on.
- Decision log append-only; no two entries share D. D124 = SDP-1 adoption. AEP#3 closeouts take next free D numbers; full D121->current mapping in _A/work-package-3/CLOSEOUT-NUMBERING.md and in the 20:59 STATUS.
- AEP#3 owner source: Peter, typed directly in the DSH Web GUI Lead session ~2026-10-28 18:21-18:23 PDT; exact wording recorded in OWNER-DECISION-PARALLEL-NUMBERING-2026-10-28.md and cited in the STATUS header.