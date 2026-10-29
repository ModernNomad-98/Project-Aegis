# OWNER DECISION BATCH — ANSWERS (recorded 2026-10-29 ~06:20 PDT)

**Source class:** Peter, typed directly in the Project Aegis DSH Web GUI Lead session at approximately 2026-10-29 06:20-06:21 PDT (owner message "OWNER DECISION BATCH — answers."). Recorded verbatim below; fail-closed defaults lift only where answered.

## I5: A
Publish the redacted derivative at the stated path; 148 alias lines masked; README states derivative + reason; Apache-2.0 attribution kept. Reviewer: a fresh independent agent session, designated I5-REVIEWER, different model/vendor from the export builder, not in the build chain. Reviewer verifies zero alias/username bytes in the derivative before commit; review record committed alongside.

## APR-156: YES, exactly as written
One file, one line, bound to the exact schema path and candidate head; no general waiver; no CODEOWNERS / branch protection / required-check change; fresh merger + APR receipt. Condition: the fixture matrix is shown fail-before / pass-after on the pre-change workflow, and the invalid-schema control is shown failing the suite, before Stage F.

## CP-02: A
Plan A1 §12 is the authoritative E3 allocation. Consumer records are downstream copies; any divergence is a drift finding against the consumer record, not the plan.

## CP-05: B
Revised sentence authorized: "fresh-session startup readback on the current consumer repo, Stage-0 clause removed." Record the original sentence, the revision, and the rationale (repo is no longer Stage-0-shaped) as a dated plan-revision entry; score the row as PASS or UNRUN against the revised sentence and label it "revised criterion."

## CP-06: A, but the owner needs the questions
Post the four Stage 2 owner-outcome questions inline, one line each, in the next STATUS header under OWNER DECISION REQUIRED. Owner answers all four in one reply. Until then CP-06 stays BLOCKED.

## CP-12: A
Authorize the content commit of the guard (branch aep3-i2/cp12-guard @ 8ac4f73) to consumer main via fresh merger, then the merged-main S0-S3 re-run with observed evidence. CP-12 may PASS only on the merged-main re-run, not on the branch result.

## CP-19: A
Keep the unresolved requirement. F2 is a genuine negative-case finding; CP-19 stays UNRUN; log the consumer gap in #966 (or a dedicated tracker) with the fixture reference. No R2 revision.

## CP-22: B
Fresh independent agent session, designated CP22-REVIEWER, different model/vendor from the RF-1 implementer, recorded as agent review. Runs the four rejection controls; each control must be shown able to fail.

## Browser rows: A
An independent session will run the visible halves of CP-11, CP-15, CP-17 and CP-20 against the live Pages URL and return screenshots plus observed DOM. Post the exact visible-check steps for each row inline (URL, action, expected observation, pass condition) so they can be executed verbatim. Until results land, the rows stay UNRUN.

**Operating mode:** no acknowledgement; execute; report at the anchored STATUS. Remaining owner items after this: the CP-06 questions and the browser-step list.

## CP-06 — four Stage 2 owner outcomes (owner-stated, 2026-10-29 ~06:20 PDT; verbatim, in required order)
> CP-06 — the four Stage 2 owner outcomes, in required order:
>   1. Product-spec acceptance: ACCEPTED as frozen in the case set. No additions, no reinterpretation; any gap found is a finding, not a spec change.
>   2. Prioritisation frame: risk-first. Correctness and fail-closed behavior before any feature; then the smallest reversible increment; cost evidence must be observed, never self-reported.
>   3. Roadmap uncertainty approach: explicit UNKNOWN markers. No speculative items; an item enters the roadmap only on observed evidence of need, and leaves it when the evidence does.
>   4. Commitments readiness: NOT READY beyond the frozen case set. Readiness is declared only after the CP ledger closes and the closeout is written; no external commitment before then.
> Record these as owner-stated, score CP-06 against them, PASS or FAIL on observed behavior.

**Source class:** Peter, typed directly in the Project Aegis DSH Web GUI Lead session at approximately 2026-10-29 06:20-06:22 PDT (owner message "CP-06 — the four Stage 2 owner outcomes, in required order").

## Browser rows — owner will run; window-announcement protocol (owner-stated, same message)
- Owner will run the visible checks from the inlined steps in the next STATUS header (not a posted file).
- For CP-15 and CP-20: when R-RB1 and R-RB2 dispatch under SDP-1 item 4, announce each window in the STATUS header with the deployment id and served aggregate, and HOLD the next R-step for 45 minutes so the visible check can be taken against the live release.
- Results come back as a single comment with screenshots, hashes and timestamps; rows stay UNRUN until then.


## Additional owner authorizations (2026-10-29 ~06:26 PDT, same chat batch; verbatim)

### CP-21 — AUTHORIZED
One controlled stale-run deploy dispatch as a NEGATIVE test. Expected outcome is REJECTION by the committed deploy gate with the served aggregate unchanged. Conditions: prior state re-observed within 5 min; one dispatch only; if the gate does NOT reject and the stale bundle goes live, that is CP-21 FAIL and R-RB1 fires immediately under SDP-1 item 4. Observed evidence either way.

**Recorded disposition (AEP3-I2 CP-21 agent, 2026-10-29 06:30 PDT):** the authorized dispatch was **not made** and is **unspent**. No expressible dispatch deploys a stale bundle through the committed interface — `release` is restricted to A/B, all five advertised refs carry byte-identical retained A/B trees, and a dispatch at an older ref runs that ref's older `pages.yml` rather than the committed gate. CP-21 remains **UNRUN**. Prior state re-observed 06:25:55–06:27:56 PDT (4 deployments, newest 7402685306 success; live aggregate 36bc4407… over 251 serialized bytes; main 4f31293); unchanged after the decision. Evidence: `_A/work-package-3/item2-cp21/CP21-RECORD.md` (E-34).

### CP-01 — AUTHORIZED
A fresh independent agent session, different vendor from every prior consumer session, started cold on the consumer repo with only the business prompt, recorded as the "genuinely new consumer coding session" (agent, not human). Score CP-01 on what it does, not what it reports.

### CP-12.7 — AUTHORIZED
Extend the CP-12 guard to manifest symlinks on the same branch route (branch -> independent review -> fresh-merger commit to consumer main -> merged-main re-run). PASS only on merged-main. Do not widen beyond symlink handling.

### #966 — AEP3-I9
Plan the I7 fail-closed existing-record / atomic-write gaps as AEP3-I9: Stage A/B on branch now. If every touched path is inside an ACTIVE grant (APR-140 / APR-143), proceed through merge under SDP-1a. If any path falls outside, post ONE OWNER DECISION REQUIRED with the path list and the grant needed; no new work otherwise.

### Carried advisories
Fold into #966 as a single checklist (selector row, _starter_git OSError, case-sensitive duplicates, snippet-path trimming, S4-8); no separate items, no action until AEP3-I9 picks them up.

### Skipped hosted jobs
Run the equivalent suites locally on the WSL2 host-class already authorized; record as "local run, hosted UNRUN", not as a hosted pass.

### Other UNRUN classes
Other host/OS, real consumer install J1, human approvals: UNRUN by definition; state them once in the closeout and stop listing them.

### Browser rows
Owner runs them; steps inlined in the next STATUS header. For CP-15/CP-20, announce each R-RB1/R-RB2 window in the STATUS header with deployment id + served aggregate and HOLD the next R-step 45 minutes so the check can be taken live. Results return as one comment; rows stay UNRUN until then.

### Reporting rule
Mid-hour backlog posts are not STATUS and not OWNER DECISION REQUIRED; do not post one unless asked. Act; report at the anchor.

---

## CP-01 execution receipt (appended by the CP-01 agent; not owner text)

The owner block "### CP-01 — AUTHORIZED" above (2026-10-29 ~06:26 PDT) is unchanged by this append. This receipt records only what was executed under it.

| field | value |
| --- | --- |
| Session | `01a187dc-7a82-79b1-8680-d72b53899da9` — `codex exec`, Codex CLI 0.163.0-alpha.10.2 |
| Model / vendor | `gpt-6-astra` / OpenAI. The three prior consumer sessions were `claude-sonnet-5-5` / Anthropic |
| Started | 2026-10-29T13:32:15.123Z; cwd `C:\src\_aep3_cp01_consumer`; branch `aep3-i2/startup-readback` at `338ba82` |
| Ended | 2026-10-29T13:37:10.657Z; exit 0; 9 read-only commands; 0 writes; clean tree |
| Outcome | CP-01 **PASS (observed)** — record at `_A/work-package-3/item2-cp01/CP-01-RECORD.md` |
| Residual | the "before investing in the build" ordering is not retroactively demonstrable (note N-6) |
| Effects | no push, no PR, no dispatch, no deploy, no settings change, no consumer-repository write |

## Source lines (MONITOR 6498853136 items 1-2; recorded 2026-10-29 ~07:12 PDT)

### APR-156 grant source (MONITOR item 1)
**Source: Peter, typed directly in the Project Aegis DSH Web GUI Lead session at approximately 2026-10-29 06:20-06:26 PDT.** Owner words verbatim: "APR-156: YES, exactly as written. One file, one line, bound to the exact schema path and candidate head; no general waiver; no CODEOWNERS / branch protection / required-check change; fresh merger + APR receipt. Condition: the fixture matrix is shown fail-before / pass-after on the pre-change workflow, and the invalid-schema control is shown failing the suite, before Stage F." This is a direct-session source (not a relayed reply id). Recording route: this owner-answers record plus the APR-156 register-transcription PR (in progress). The 06:59 STATUS omitted the APR-156 line; that omission is a reporting defect corrected at 07:59.

### #943 unpark source (MONITOR item 2)
**Source: Peter, typed directly in the Project Aegis DSH Web GUI Lead session at approximately 2026-10-29 06:26-06:28 PDT.** Owner words verbatim (opening): "#943 — UNPARKED. Run it to completion under APR-140 / SDP-1a; no owner merge needed." followed by the five-point order (rebase; three fixes with pre-fix failing regression tests; review dispositions 5668639539/5668668896/5669885151; fresh security-focused D + E + fresh F; limitations verbatim/no enforcement claim) and the closeout instruction. This is a direct-session source, not a relayed reply id.

### AEP3-I9 / CP-21 / CP-01 / CP-12.7 / hosted-suite authorizations source
**Source: Peter, typed directly in the Project Aegis DSH Web GUI Lead session at approximately 2026-10-29 06:26-06:28 PDT** (the same batch whose items are recorded above; "CP-21 — AUTHORIZED", "CP-01 — AUTHORIZED", "CP-12.7 — AUTHORIZED", "#966 … plan it as AEP3-I9", "Skipped hosted jobs … run the equivalent suites locally").

## Later owner decision batch (2026-10-29 ~10:05-10:07 PDT; verbatim, direct session)

**Source: Peter, typed directly in the Project Aegis DSH Web GUI Lead session at approximately 2026-10-29 10:05-10:07 PDT.**

1. **CP-21: B.** "Authorize a reviewed freshness selector on the consumer deploy gate: selected release must equal the live deployment's release, or the deploy ref must be main. On a branch; independent review; fresh-merger content commit to consumer main (owner-only merge class under SDP-1 item 6 - this is the grant). Then re-run the same negative test. Evidence required: stale bundle ACCEPTED before the selector (fail-before), REJECTED after (pass-after), served aggregate unchanged. One dispatch each; no retry."

2. **Browser rows: B.** "One new R-RB1/R-RB2 reversal pair under the SDP-1 item 4 conditional pre-grant. This time the protocol is mandatory: announce each window in the STATUS header with deployment id and served aggregate, HOLD the next step at least 45 minutes, and post the exact visible-check steps for CP-11/15/17/20 inline in that same STATUS (URL, action, expected observation, pass condition, capture). A window opened without the announce line does not count. CP-11/CP-17 steps inline now; they run before the pair."

3. **CP-09: A.** "FAIL stands; final ledger records it. Add one line to the closeout naming the gap (plan-forbidden names/PR numbers and a personal name in public commit metadata) as a future prevention item - no retroactive exception, no history rewrite."

4. **U6 condition (i): C, plus two corrections.** "a. CP-19 is rescored RUN = FAIL (13/14, F2 failing). It ran; it produced a verdict. 'UNRUN' was wrong. b. CP-22: one more reviewer cycle, hard time box 60 minutes, fresh CP22-REVIEWER, different vendor from the implementer. At the box: PASS or FAIL on whatever the controls show; UNRUN is not an outcome of a cycle that ran. U6 export proceeds when CP-21 (B) has its verdict, CP-22 has its verdict, and every non-browser row is PASS or FAIL. Browser rows state UNRUN or their result as of export time. FAIL rows are published as FAIL; that is the point of the export."

Also: "#968 rebase, #970/#971 closures: acknowledged, proceed. No acknowledgement reply; report at the anchor with the CP-11/CP-17 steps inline."

## CP-21 environment-policy grant — exact owner source (for the settings-change record)

**Source: Peter, typed directly in the Project Aegis DSH Web GUI Lead session in the turn received at approximately 2026-10-29 10:47-10:52 PDT** (verbatim head): "DECISION 1 — CP-21 environment policy: (a) APPROVED. (b) rejected — local-only evidence is not the live verdict I required. (c) rejected — a tag policy is a second mechanism to maintain and the proof does not need it." Conditions (i)-(vi) followed verbatim in the same message; also "ACTION 2 — browser rows: RUN, not skip" and "U6: after CP-21 has its verdict and browser rows are recorded (results or UNRUN as-of-export), export proceeds under condition (i)=C with no further ask."

The settings change itself (environment `github-pages`, deployment branch policy id 64714655; refs 64824653 `aep3-i2/cp12.7-manifest-symlink`, 64824654 `aep3-i2/cp21-freshness-selector` added 17:56:37Z and removed 17:58:43Z) was executed under this grant and is logged with the four readings and revert evidence in item2-cp21-exec/CP21-EXECUTION-RECORD.md and SETTINGS-CHANGE-LOG.md.
