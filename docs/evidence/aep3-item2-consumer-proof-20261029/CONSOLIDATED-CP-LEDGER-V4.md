# AEP3-I2 CONSOLIDATED CP LEDGER — v4 (CP-21 PASS; 2026-10-29 11:07 PDT)

Frozen denominator: 22 ordered IDs; case_set_sha256 48a28ba1... (R1; CP-05 counts only against case_set_sha256_R2 c39360cf...). NOT-APPLICABLE = 0.

| Case | Verdict | Basis / residual |
|---|---|---|
| CP-01 | PASS | owner-authorized Codex (OpenAI gpt-6-astra) fresh session; residual N-6 (pre-build ordering not retroactively showable; owner defined the run as the closing observation) |
| CP-02 | PASS | 19/19 effects reconciled + RV-1 verification; drifts D-01/D-02/D-03 recorded; G-01 E3 INFERRED; drift correction merged consumer `a598f3b` |
| CP-03 | **FAIL** | executed pre-registered N1 installer control exited 0 and healed 40->41; two clauses unsatisfied; independent semantic review earlier PASS is superseded by the control evidence (round-6/7 reviewers accepted FAIL) |
| CP-04 | PASS | install collisions observed (0/22/0, tree_before==tree_after) |
| CP-05 | PASS (revised criterion, R2 only) | owner CP-05=B revision R2-CP05; observed at 338ba82 and currency-closed at 3998af1; countable against case_set_sha256_R2 only; label 'revised criterion' |
| CP-06 | PASS | four Stage 2 owner outcomes recorded PS-001..PS-004 in order; CP-06-RECORD a55bd45e... |
| CP-07 | PASS | 20/20 owner/content paths reachable + hash-equal; routing quoted; manual-only triggers recorded before invocation |
| CP-08 | PASS | plan accepted by non-author on exact hashes |
| CP-09 | **FAIL** | public consumer commit metadata contains plan-forbidden product names/PR numbers and a personal full name; owner CP-09=A: FAIL stands; prevention item recorded; no retroactive exception/history rewrite |
| CP-10 | PASS | non-author reviews + dispositions |
| CP-11 | UNRUN | browser visible halves; owner browser decision=B (new pair protocol) |
| CP-12 | PASS | merged consumer main 4f31293; merged-main re-run PASS; CP-12.8 independent review PASS; CP-12.6/.7 later work |
| CP-13 | PASS | workflow bytes dispatch-only, choice inputs, pinned actions, scoped permissions |
| CP-14 | PASS | pre-push empty-target record + invariant; A restorable |
| CP-15 | UNRUN | browser A-window half; windows closed; owner browser=B (new reversal pair) |
| CP-16 | PASS | exact Release B observed (aggregate 36bc4407...) |
| CP-17 | UNRUN | external browser journey; owner browser=B |
| CP-18 | PASS | durable next-action record + fresh-session derivation |
| CP-19 | **FAIL (run)** | owner rescore: RUN=FAIL, 13/14, F2-late-revocation failing; owner CP-19=A keeps the unresolved requirement; gap logged #966; no R2 revision |
| CP-20 | UNRUN | browser count-disappears/returns half; windows closed; owner browser=B |
| CP-21 | **PASS** | owner CP-21=B; selector merged to consumer main `f3ec2cff`; live negative test under owner-authorized temporary env policy change (policy id 64714655, exactly 2 named refs added at 17:56:37Z, restored byte-identical by 17:58:43Z, 2m06s < 60-min deadline, no retry): **D1 fail-before** run 40926181149 SUCCESS accepted A (deployment 7420139651, aggregate 12ad18e1...); **D2 pass-after** run 40926362502 FAILURE `freshness_selector_refused reason=selected_release_differs_from_live selected_release=B live_release=A`, upload/publish skipped, served A unchanged; restore run 40926519791 SUCCESS B (deployment 7420187769), served B byte-identical to the 17:56:09Z snapshot. Pass-after-from-main determination: not possible (main fast path allows any release; no out-of-choice value). Settings change withheld from consumer docs register only until the owner-authorized commit lands. |
| CP-22 | **PASS** | final cycle rev-8 + fresh Anthropic claude-opus-5-5 reviewer: 22/22 ACCEPT, controls 5/5 rejected, clean baseline; signed gate MET; CP-22-ROW-UPDATE.md |

**Totals: PASS 15 / FAIL 3 (CP-03, CP-09, CP-19) / UNRUN 4 (CP-11, CP-15, CP-17, CP-20) / BLOCKED 0.** Arithmetic: 15+3+4=22.

Non-browser rows: **all PASS or FAIL** (CP-09/CP-19/CP-03 FAIL; all others PASS including CP-21 PASS and CP-22 PASS). U6 condition (i) per owner C is therefore **satisfied**: CP-21 has a verdict, CP-22 has a verdict, every non-browser row is PASS or FAIL. Browser rows (CP-11/CP-15/CP-17/CP-20) state UNRUN or their result as of export time; FAIL rows publish as FAIL. U6 export may proceed with no further ask; it is being prepared and will carry the single-window browser results or UNRUN-as-of-export.

**Evidence:** item2-cp21-exec/ (CP21-EXECUTION-RECORD, SETTINGS-CHANGE-LOG, CP-21-ROW-UPDATE PASS, 57 artifacts), item2-cp21-merge/, item2-cp21-selector/, item2-cp22-final/, item2-cp02/, item2-cp05-revision/, item2-cp06/, item2-cp12-merge/, item2-cp12.8-review/, item2-cp01/, item2-cp22-final/ (RF1-DRAFT-v8 9b595c24...), item2-cp19-fix/, item2-cp21-selector/, CP-19-CP-09-OWNER-CORRECTIONS.md (40e5b420...), owner answers record 36495683...