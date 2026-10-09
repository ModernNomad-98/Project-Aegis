# CIFIX-GREEN-ROUTE — independent Stage B supplement audit

**SD-B: REVISE** on captured `DECISION-SUPPLEMENT.md` SHA-256 **ab3e9fa1edb1a52b2e10a1894d26daa0d68f4eadfb72022720cec88ff46e91a2**. This is a decision-packet verdict only. It supplies no prototype/platform PASS, source implementation authority, installation grant or merge verdict.

Auditor: `/root/pr682_policy_adversarial`, distinct from the supplement author `/root/pr682_policy_supplement`. The auditor previously performed a read-only adversarial investigation; it authored neither this supplement nor the historical Stage A packet. Assigned write scope: this file only. Stage B's plan-level ACCEPT/REVISE and hash binding are procedural under `docs/delivery-workflow.md`; `acceptance-criteria-reviewer` supplies the criterion testability analysis only.

## Required corrections

### R1 — Define the F3 actor and comparison point (supplement line 53)

F2 permits only the broker to update main, but F3 presently has “another permitted actor” change main. The F3 output then requires “both refs unchanged,” without distinguishing the deliberately injected base advance from a forbidden merge. A conforming serialized broker could fail the literal test merely because the setup deliberately changed a ref.

Split the cases: (a) an unauthorized actor's attempted main update must itself be denied; (b) a separately authorized broker update serializes before the pending candidate and invalidates its old B/T tuple; (c) an actor permitted to edit PR metadata retargets the PR without changing H. Record ref snapshots immediately before releasing each attempted merge, after any permitted setup injection. The denied merge must cause no further ref change; do not require an authorized setup change never to have happened. Preserve zero wrong-destination or wrong-B/T merges.

This is a test-oracle correction, not a finding that the proposed broker currently works or a request to weaken exclusive update control.

### R2 — Specify every F6 denial outcome and its enforcing layer (line 56)

F6 names stale and dismissed review attempts, but the result clause expressly covers only missing/rejected reviews and a valid approval. Current GitHub protection has stale-dismissal and last-push checks disabled. An old native approval can therefore remain on the PR without satisfying the proposed exact-candidate authorization.

Explicitly require denial for each listed invalid state, including stale head-bound evidence and dismissed approval. Separate native review-count enforcement from the evaluator/broker's exact-candidate review binding. A stale native approval that still counts under GitHub must not release the broker. Require a new, valid independent approval for the tested candidate before the positive case; do not silently turn on new review settings or lower the count.

### R3 — Give the 120-minute exercise an honest exit vocabulary (lines 67 and 73)

The proposed owner question promises an independently reviewed “viable/not-viable decision.” Offline work cannot establish the hosted controls, and the capped exercise may exhaust time before resolving the cutoff, reviewer or platform model. A binary outcome creates pressure to label an incomplete result viable or to overstate a no-go.

Define three exits: **ready for separately authorized hosted proof**, **not viable under the selected constraints**, or **inconclusive/unfinished at the 120 aggregate-active-minute cap**. A favorable offline result must never mean a working all-green route, production readiness or permission to continue automatically. At the cap, retain evidence and unresolved items and stop; no automatic extension or promised hosted proposal when prerequisites remain unavailable. These are outcome clarifications; the 120-minute limit itself is acceptable as a proposed resource cap rather than a completion estimate.

No new owner answer is needed to repair this decision packet. Return it to its author for these narrow clarifications and recapture its hash.

## Decision-packet criteria

| ID | Result | Evidence / limit |
| --- | --- | --- |
| S1 Current facts, closed status and source hashes | MET | Fresh GETs and independent byte hashes agree with the supplement; details below. |
| S2 Current authority and green-only hold | MET | Current-main register preamble, APR002/013 and APR120/121 are consistent with planning authority and the retained hold. The contextual “do it” follows the proposal to prepare a separately reviewed policy plan; no particular broker installation, credential or settings delta was presented or selected. |
| S3 Unproven broker constraints remain explicit | MET | Lines 26–43 accurately distinguish an attestation from merge-time control; personal-repository, retarget, revocation, stale-token and native-review limitations are clearly disclosed. |
| S4 F1–F8 falsifiability and evidence placement | NOT MET | R1 and R2 leave two test outcomes ambiguous. F4's absent owner cutoff is correctly disclosed as a future prerequisite, not a tested control. |
| S5 Cost, timeboxes, owner choice, scope and stops | NOT MET | Scope boundaries and resource caps are concrete, but R3 must prevent a binary offline feasibility claim when hosted proof remains UNRUN. |

## Criterion testability review

This review treats each numbered F row as a future proof gate, not an executed result. Compound attempts within a row are individually named below and share the same pass/fail oracle only where that oracle is explicit. **5 TESTABLE, 2 NEEDS-REWRITE, 1 UNTESTABLE pending its expressly deferred owner decision.** Every F1–F8 runtime result remains **UNRUN**.

| Gate | Verdict | Observable outcome, threshold and evidence |
| --- | --- | --- |
| F1 | TESTABLE as a future gate | Exact valid tuple accepted; each single-field invalid tuple, wrong identity and copied/shared-H authorization denied. Offline traces prove parser/state behavior only; hosted wrong-App and candidate-success attempts must produce zero unauthorized merges. Future protocol fixtures must name exact inputs. |
| F2 | TESTABLE as a future gate | Only the authorized broker PR operation succeeds; broker direct push and all disallowed actors fail with unchanged refs. Requires actual public User-owned disposable repository, rule readback and operation/ref logs. App UI actions are tested through the actual APIs available to that identity, not an imaginary App browser login. |
| F3 | NEEDS-REWRITE | Actor permissions and ref baseline are ambiguous; R1 provides a falsifiable split and comparison point. |
| F4 | UNTESTABLE until the deferred cutoff decision | A timestamped trace can test a chosen cutoff, but this revision deliberately chooses none. Eventual owner question: what event makes a revocation effective, and are already-dispatched operations pending/too late? Research can model alternatives; none becomes an accepted operating rule from this audit. This explicit deferral is appropriate for a decision packet. |
| F5 | TESTABLE as a future gate | At most one authorized merge/use; unresolved operation keeps its reservation; old writer is unable to update refs after real authority transfer. Offline ledger traces plus hosted retained-token/fencing attempts are required; a new local epoch alone cannot pass. |
| F6 | NEEDS-REWRITE | Every invalid review state needs an explicit denial result and native versus evaluator enforcement attribution; see R2. |
| F7 | TESTABLE as a future gate | Real positive candidate obtains retained required-check success; malicious candidate stays blocked. Existing negative protection tests and Linux/Windows coverage remain. Exact candidate/test inventory must be frozen in the later hosted plan. |
| F8 | TESTABLE as a future gate | Failure/recovery exercises produce zero fail-open merges; recovery dependency, operator availability and measured usage records exist. There is no promised availability target; inability to recover safely can remain a documented hold. |

The exact reviewed F1–F8 wording is retained in the source at the captured hash, lines 51–58, and reproduced in the appendix. No criterion is marked runtime MET here.

Completeness checked: negative, permission, state/timing, failure and recovery classes are represented. Input resource boundaries (oversized/malformed receipts, API pagination/rate-limit failure and authentication-channel denial) are not detailed in this supplement's hardest-constraint screen. They remain future protocol/test-plan gaps, covered at a high level by the historical T2/T6/T8 model; they do not justify widening this two-hour exercise or inventing limits. Any later executable plan must make their chosen limits explicit. No production tenant-data boundary is in scope.

## Fresh state and evidence

Read-only GitHub commands used the fixed repository `ModernNomad-98/Project-Aegis`. Source contents were pinned to M, not accepted from a mutable branch name alone.

| Evidence | Observed result |
| --- | --- |
| `GET git/ref/heads/main` | M `625fc66711eaf7b3ee788cbc2dff98f05f147c1c` |
| `GET pulls/682` | closed, merged=false, H `a33aa2a620589d2e0412521e6a0ee1ba3594c97f`, base ref main, recorded B `5228977920ee479e1fe1ec6b8d56f8fc24c14947` |
| `GET pulls/683` | merged=true, merged_at 2026-10-09T15:53:09Z, merge `a4fb1445ea92ff6df469627ea9e10f769d69d830` |
| `GET commits/H/check-runs` | changes and validate-skills success; gate-guard 113518470282 failure; three advisory checks skipped |
| `GET commits/M/check-runs` | five success; gate-guard skipped |
| `GET commits/H/check-suites` | GitHub Actions completed/failure; Supabase/Vercel/Claude queued/null |
| `GET pulls/682/reviews` | zero |
| `GET branches/main/protection` | required gate-guard and validate-skills, both app_id 15368; strict=false; enforce_admins=false; approving count 1; stale-dismissal/last-push false |
| `GET rulesets`, `GET rules/branches/main` | [] and [] |
| `GET repository` | ID 1291303476, public, owner type User |
| pinned workflow contents | blob `66cca67d0390e739190939abccae99125cb56543`; byte SHA-256 `38fddc4c66bea51e466b6cabbe9a27e5e8a9d8a0bfc94e20b93a6c720a8e4a0e` |
| pinned register contents | blob `7ee0e822398382101900c79aea9962b540a86c57`; byte SHA-256 `d3dfd86df8ad6441938a3df788fd0bc1f1efa70e6cf1df2fde3d1061a567380e`; 121 headings, 121 unique IDs |
| original DECISION-PLAN.md | SHA-256 `43a98e8eeee8cad392197c97dab244025333653f79ba56e1f5514bb2dc7acd1b` |
| original investigative AUDIT.md | SHA-256 `d550e55cab06e62aa9149d86e0b4f1e27742adbca826df8ad2c46be51b57e15e` |

The pinned workflow still rejects any protected match, including scripts/ and workflows/. The earlier actual job-log read in this audit lane named the test path and exit 1; this Stage B turn refreshed check conclusion and exact workflow bytes without rerunning the job. #682 file count/size and fixture context were directly inspected during the immediately preceding independent investigation; no new source review or runtime rerun is claimed here.

The register's historical exact-H exception remains subject to its later green-only condition. The supplement correctly treats closure as neither delivery nor consumption. A changed-head continuation cannot spend APR120 as if it named a replacement head. The current planning instruction needs no repeated consent, while the still-undefined installed App, settings, review actor and revocation choices have no grant in this packet.

## Platform and proportionality assessment

Official primary documentation was freshly reopened during Stage B:

- [Ruleset layering](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets): overlapping rulesets and classic protection aggregate. This supports testing separate updater and check restrictions; it does not prove a working installation.
- [Rules REST schema](https://docs.github.com/en/rest/repos/rules): repository rulesets support Integration and User actors, PR-only branch bypass, and creation/update/deletion rules. Exact actor IDs, targeting, exclusions and `update_allows_fetch_and_merge` must be frozen and tested later.
- [Merge REST API](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request): documented merge requests pin head SHA, not expected base ref/SHA/tree. Async acceptance is not completed enforcement or merge; delayed/unknown results require reconciliation.
- [Merge queue availability](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request-with-a-merge-queue): organization-owned repositories are the documented eligible ownership. User ownership prevents treating queues as an available shortcut here.

The separate-App/exclusive-broker design remains a hypothesis. Wrong-App checks, candidate-controlled Actions, a PR retarget, an unacknowledged revocation, a stale token after failover and a missing native review are distinct boundaries. The supplement does not merge them into one false “green means authorized” claim.

A 120-minute rejection screen is a defensible proposed spending cap for identifying a no-go early. It is smaller in scope than the old 4–8-hour prototype exercise, not an evidence-backed claim that the same work became faster. The provisional four-hour hosted cap is likewise a limit, not a proof or promise of F1–F8 completion. Money and ongoing operating costs remain unknown and require a later finite proposal. The judgment that a permanent service is disproportionate for this isolated 28-line fix is reasonable; it is not a measured return-on-investment claim.

## Skills, authority and limits

- `acceptance-criteria-reviewer` and its criteria-review sheet: assessed outcomes, thresholds, evidence and missing decision inputs; did not edit the source criteria.
- `human-approval-boundary`: matched the current contextual instruction and register to planning versus future settings/credential/merge actions.
- `scoped-approval-register` and register-format reference: distinguished historical ACTIVE wording from effective permission and the later APR121 condition; recorded no grant.
- `threat-modeler` and threat catalog: challenged retarget, revocation, actor isolation, crash/failover and recovery controls without asserting a live exploit.

The latter skills were read and applied earlier in this audit lane and reused with fresh source/authority evidence; they were not claimed as newly read during this Stage B turn. The local source-library role and clean H clone were corroborated during the independent investigation. No other agent's work was reverted. This artifact is the only authorized new write. No source edit, Git mutation, PR comment, reviewer trigger, settings change, App creation, credential read, provider call or hosted experiment occurred.

Initial assigned ETA: 20–30 active minutes. First measured checkpoint: **2026-10-09 16:53:21 UTC**. Actual dispatch/start and active time were not measured. Completion and readback timing are appended below; wall time is an imperfect comparison with the active ETA.

## Appendix — exact captured F1–F8

| Gate | Concrete attempt and required observable result | Required evidence / stop |
| --- | --- | --- |
| F1 Independent authorization | Candidate replaces its verifier with success; copy a grant across repo/PR; mutate H, base ref/B, tree, paths, deletion/mode, policy, expiry/revocation/use individually. Wrong App emits the same check name; create a second PR at the same H. | Offline positive exact tuple passes and every mutation denies; hosted wrong-App/candidate success cannot permit merge. Stop on any unauthorized success. |
| F2 Exclusive update path | With all normal checks green, ordinary writer, administrator session, other App and broker each attempt UI/API merge and direct/ref update. Broker attempts direct main push. | On a disposable **public User-owned** repo, only authorized broker PR merge succeeds; broker direct push and other actors fail without changing any ref. Read back all active rule IDs/bypass modes and classic protection. A config screenshot or local mock cannot pass this gate. |
| F3 Base retarget and base advance | Pause after final authorization read; another permitted actor retargets to an existing non-main branch or changes main; then release the request. Repeat with new/renamed destinations and shared H. | Zero wrong-destination/wrong-B/T merges; denied attempts leave both refs unchanged. Prove confinement covers every branch pattern and every main writer. If prevention depends on eventual event delivery or another GET, stop. |
| F4 Revocation and expiry | Schedule revoke/expiry before reservation, before dispatch, during a delayed request and after server acceptance. Stop the check publisher after success. | Timestamped trace proves the explicitly selected cutoff, zero dispatch after acknowledged pre-cutoff revocation, and honest pending/too-late results for in-flight work. An owner-unaccepted cutoff or claim of cancellability without a primitive stops the route. |
| F5 Crash, retry and stale leader | Crash at each reservation/dispatch/result boundary; drop response; start a second leader; retain an old token; replay request and webhook. | At most one authorized merge/use; ambiguous operation remains locked; old process cannot update refs after authority transfer. Hosted token/fencing evidence is required in addition to offline ledger tests. If only voluntary process behavior fences a live token, stop. |
| F6 Native and independent review | Try zero review, author/same-account review, stale or dismissed review, requested changes, then a valid independent approval for the exact candidate. | Native missing/rejected review blocks; valid independent approval can release only with every other gate. Separately retain A–G holder separation and bound review receipts. No bypass of reviews hidden in the broker ruleset. |
| F7 All-green bootstrap and regression | In the isolated repo, install denied-by-default external enforcement first, then submit the actual protected policy candidate and a malicious variant. Exercise current protected-path, rename/case/symlink/import-isolation tests plus real Linux/Windows checks. | Legitimate candidate obtains genuine success for retained required checks and selected external check; malicious variant remains blocked. Preserve original failed records; no duplicate-status substitution, skip/continue-on-error or direct push. Production grant must follow, never precede this proof. |
| F8 Recovery and cost | Simulate service/key-store failure, lost ledger and bad policy version; exercise read-only reconciliation and the proposed denial-first recovery sequence. | No fail-open merge; operator/reviewer availability, recovery dependencies and measured work/usage are recorded. Recovery that needs removing the independent check while the permissive guard remains deployed fails. |


## Audit completion

Completed at 2026-10-09 16:57:31.384 UTC; measured checkpoint-to-completion wall time 04:10.384. Active time was not separately measured. The 20–30-minute active ETA therefore has no measured active-time comparison. The written audit was read back, including its exact F1–F8 appendix; the reviewed supplement remained at the captured hash. No runtime gate was executed.

