# CP-02 — effect-by-effect grant reconciliation (actual target and authority)

**Record type:** adjudication record over existing evidence. Planning/evidence artifact only. No deploy, no
dispatch, no provider mutation, no consumer-repository write, no settings change, no ledger edit.
**Work item:** AEP#3 Item 2 (one hosted consumer journey), case CP-02 of the frozen 22.
**Adjudicated:** 2026-10-29 06:13-06:40 PDT (2026-10-29T13:13-13:40Z) by the CP-02 RECONCILIATION agent.
**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not observable.
**Canonical ledger:** not edited by this record. The proposed row replacement is CP-02-ROW-UPDATE.md.

---

## 1. The controlling decision, and what it settles

Owner decision **CP-02 = A**, recorded in _A/work-package-3/OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md
(7,239 B, SHA-256 c93c07b82f90fdb0832a8ee1ff8a97dcfdb152cdf3e091a0d4137f45e819726e, point-in-time capture), lines
11-12, verbatim:

> ## CP-02: A
> Plan A1 §12 is the authoritative E3 allocation. Consumer records are downstream copies; any divergence is a
> drift finding against the consumer record, not the plan.

Source class: Peter, typed directly in the Project Aegis DSH Web GUI Lead session, ~2026-10-29 06:20-06:21 PDT.
The question it answers (OWNER-DECISION-BATCH-2026-10-29.md, 11,704 B,
b85828a8d94d7c2649f7261017dd48acf174a96196d5da15a5d0544e36791a0f, lines 58-66) was: "Which record is the
authoritative **E3 allocation**, so the effect-to-grant reconciliation can be scored against one source?" with
option A "E3 = plan A1 §12 as written (the accepted plan is canonical)", and the fail-closed default "no E3
allocation confirmed -> CP-02 stays UNRUN".

**Two readings of "the E3 allocation", and why this record covers both.**

- Reading 1 (row): E3 is row E3 of A1 §12 - "Push of content + workflow to the public consumer repository",
  authority "Item 2 YES plus U1, in substance", state "**INFERRED — to be stated explicitly in the R-A request**".
- Reading 2 (allocation): "the E3 allocation" names the effect-by-effect allocation artifact itself (E1…E19),
  which is what CP-02's frozen acceptance text tests: "every effect names a grant or is marked NOT GRANTED /
  INFERRED" (plan v4 line 296).

This record satisfies both: §4 reconciles **all nineteen** planned effects, and §5 treats E3 (the row) in
detail, because E3 is the row A1 §12 itself says must be stated explicitly before it is relied on.

**A1 identity.** A1 is the Stage-0 record: _A/remediation/handshake/item2-consumer-plan/v4/CONSUMER-STAGE-0-v4.md,
41,024 B, 329 LF, SHA-256 4de970ee7b4f76055f10cde863a46516483c6ac978de0d54d4b4134ae30d0c26 (= ledger E-06). The
plan's own CP-02 producer column names it: "S0 (A1 §2, §8, §9, §12)". Its §12 is reproduced verbatim in
evidence/02-a1-s12-extract.md.

---

## 2. Claim boundary

1. **Adjudication from observation only.** Every grant claim below is read from a named record whose bytes this
   task hashed; every delivered effect is an identity (deployment id, run id, commit SHA, served aggregate) that
   appears in a durable record. No provider call was made by this task; the provider values are those already
   captured read-only in E-26/E-28 and the reversal records.
2. **This is not the CP-22 closeout and not an RF-1 record.** It supplies CP-02's decisive facts and the row
   replacement only.
3. **No self-review is claimed as independence.** The plan assigns CP-02 to "operator; verified by RV-1". This
   record is the operator leg; the RV-1 leg is named in §7 as open. Same handling CP-05 and CP-08 recorded.
4. **Drift findings are advisory on the record, not edits to it.** No consumer record was changed by this task.
5. **E3's marking is not upgraded.** Nothing here converts the inference into a grant; conversion would need an
   owner statement bound to the pushed SHAs, which does not exist (G-01).

---

## 3. Method and classes

For each of A1 §12's nineteen rows: take the authority and state **as written** (the allocation), then find
**what actually happened** for that effect and which record authorises it, then assign one class:

| Class | Meaning |
| --- | --- |
| **DELEGATED WRITE SCOPE** | a workspace-local effect covered by a delegated task write scope; no provider effect, no owner grant needed |
| **GRANTED (named)** | an owner/plan grant exists and is quoted; the effect was taken and is identified |
| **GRANTED (conditional)** | a standing conditional pre-grant exists; every one of its conditions is evidenced MET before the dispatch |
| **INFERRED** | A1 §12 itself marks the authority as inferred, with no separately written grant |
| **READ-ONLY / no grant needed** | public read or read-only continuation; no mutation |
| **NOT NEEDED** | the effect is explicitly not required for this proof |
| **NOT GRANTED** | no authority exists; recorded whether the effect was nevertheless taken (none was) |

Evidence keys used in the table are defined in evidence/01-source-hashes.json. Short forms: **A1** = Stage-0
record §12; **PLAN-V4**; **RA-DECISION** = owner R-A/A-13/U8 record (1c47cf27…); **RA-REQUEST** = the ask as
issued (774266e8…); **B-BUILD** (7ab8bb24…); **RB-DEPLOY** (2a623509…); **R-RB1** (2fb8d1f7…); **R-RB2**
(421cc60c…); **READINESS-A/B**; **DEPLOY-A** (6877c4a4…); **SDP-1** (5a842951…); **CP16** (583f549d…);
**PROVIDER-AFTER** (0e83e74c…); **LIVE-SUMMARY** (181f17ac…); **FREEZE** (85c773fb…).

---

## 4. The reconciliation table — 19 of 19 planned effects

| # | Planned effect (A1 §12) | A1 §12 authority / state as written | Reconciled class | Effect actually taken (observed identity) | Evidence pointer |
| --- | --- | --- | --- | --- | --- |
| E1 | Local writes in the source workspace | "the delegated task's write scope" — DONE | **DELEGATED WRITE SCOPE** | the four Stage-0 files exist (this record's A1 among them) | A1 §15; plan v4 2bca5ad1…; V4 file identities |
| E2 | Local scratch/build writes (pinned clone, staging, manifest assembly) | "the build step's ordinary local-write authority" — PLANNED | **DELEGATED WRITE SCOPE** | pinned source + consumer clone + staging + manifest assembly performed; install record aggregate fcff1124… at pin ffb040c7 | BUILD-RECORD (36f4963d…); ledger E-31 |
| E3 | Push of content + workflow to the public consumer repository | "Item 2 YES plus U1, **in substance**… There is **no separately written content grant**" — INFERRED | **INFERRED** (unconfirmed; see §5.1 and G-01) | 13 commits ee65bff → 390363f on main, 16:22-19:08 PDT 2026-10-28, owner account | evidence/05-consumer-commit-chain.txt; PLAN-V4 S5/S14; A1 §12 line 278 |
| E4 | Pages settings: enable | "U2 (executed 2026-10-28T21:00:49Z)" — DONE | **GRANTED (named)** | Pages enabled at 2026-10-28T21:00:49Z; build_type workflow, public true, status null | A1 §8, §12 E4; DEPLOY-A §6/§13 (config observed before and after) |
| E5 | Any further settings change (re-enable, visibility, domain, protection) | none — NOT GRANTED | **NOT GRANTED** (not taken) | 0 settings changes across four deployments; Pages config unchanged before/after each | DEPLOY-A §13; RB-DEPLOY §8.3; R-RB1 §5; R-RB2 §5 |
| E6 | Build run with no deployment | "Item 2 construction authority (no public release effect)" — PLANNED | **GRANTED (named)** | run 40794805183 (A build) and run 40801962008 (B build), deploy job skipped in both; B run names the owner fast-path item 3 | B-BUILD §2, §6; READINESS-A §3; DEPLOY-A §6 |
| E7 | Deploy release A | "**R-A** (U5) — not asked" — NOT GRANTED | **GRANTED (named)** — later per-ask grant | owner YES at ~18:05 PDT, conditions (a)-(e); deployment 7401326753, run 40798505740, URL 404→200 | RA-DECISION lines 5-11; DEPLOY-A §2, §6, §7 |
| E8 | Verify A (read-only fetch + browser) | "Public read; no grant needed" — PLANNED | **READ-ONLY / no grant needed** | served hashes equal M_A, aggregate 12ad18e1…867c, HEAD/GET 200; **browser half UNRUN** | DEPLOY-A §9, §10; LIVE-SUMMARY |
| E9 | Deploy release B | "**R-B** (U5)" — NOT GRANTED | **GRANTED (conditional)** — SDP-1 item 4 (a)-(d) all MET before dispatch | deployment 7402303270, run 40805535198, served aggregate 36bc4407…ba4a | SDP-1 item 4; RB-DEPLOY §2, §7, §8.4 |
| E10 | Rollback: restore retained A at the same target | "**R-RB1** (U5)" — NOT GRANTED | **GRANTED (conditional)** — SDP-1 item 4 (a)-(d) MET | deployment 7402651775, run 40808009410, served aggregate 12ad18e1…867c, no rebuild | R-RB1 §1-§5 |
| E11 | Redeploy retained B | "**R-RB2** (U5)" — NOT GRANTED | **GRANTED (conditional)** — SDP-1 item 4 (a)-(d) MET | deployment 7402685306, run 40808262509, served aggregate 36bc4407…ba4a | R-RB2 §1-§5 |
| E12 | Teardown / return to empty | "**R-EMPTY** (U5)" — "NOT GRANTED; provider primitive also UNVERIFIED" | **NOT GRANTED** (not taken) | no teardown; 4 deployments live-series ends at B; URL 200 | A1 §12 E12, §13 U7; PLAN-V4 S24b/S25; **drift D-01** |
| E13 | Fresh-agent recovery (read-only continuation) | "Read-only authority in the consumer repository" — PLANNED | **READ-ONLY / no grant needed** | CP-18 PASS: a genuinely new session in a fresh clone derived branch/HEAD/state and 10/10 cited hashes from the durable record, asked only the open items, wrote nothing | CP18-UPDATE (703ee044…) |
| E14 | Manual-only owner invocation | "**U4** — per-turn human exact-name invocation + consumer-local register entry written first" — NOT GRANTED | **NOT GRANTED** (no invocation occurred) | 0 manual-only invocations; no consumer-local authority entry exists | A1 §13 U4; SDP-1 §3 (no invocation, no entry); **drift D-03** |
| E15 | Durable evidence publication / export | "**U6** — not asked" — NOT GRANTED | **NOT GRANTED** (not taken) | the proof evidence is workspace-local; the consumer repo holds release evidence only, not the export | A1 §13 U6; CP ledger CP-22 row; DEPLOY-A §12 |
| E16 | Deletion of the repository or of Pages | "none (creation was U1/U2)" — NOT GRANTED | **NOT GRANTED** (not taken) | repository exists, Pages enabled, URL 200 | PROVIDER-AFTER; DEPLOY-A §13 |
| E17 | Read-only provider checks | "standing read access" — DONE (GETs only) | **READ-ONLY / no grant needed** | every provider fact in this record traces to a read-only capture; 0 writes by any adjudication task | PROVIDER-AFTER; LIVE-SUMMARY; RB-DEPLOY §11 |
| E18 | Plan/billing reads | "U3 not granted (no user scope)" — NOT GRANTED — and not needed | **NOT NEEDED** | no plan/billing endpoint read; budget answered by owner decision + two primary-source statements | A1 §8 (plan unreadable), §9 |
| E19 | Confirm the DELETE-Pages primitive at a disposable repository | "**none** — U1 created *this* repository and R-EMPTY covers *its* Pages" — NOT GRANTED, prerequisite U7 | **NOT GRANTED** (not taken) | no disposable repository created; primitive stays UNVERIFIED | A1 §12 E19, §13 U7; PLAN-V4 S24b |

**Counts:** DELEGATED WRITE SCOPE 2 · GRANTED (named) 3 · GRANTED (conditional) 3 · INFERRED 1 · READ-ONLY 3 ·
NOT NEEDED 1 · NOT GRANTED 6. **Total 19 of 19 reconciled; 0 unreconciled.**

---

## 5. Effects that need more than a table cell

### 5.1 E3 — the inference, and the confirmation that never happened

A1 §12 does not merely leave E3 inferred; it prescribes the exact discharge (line 278, verbatim in
evidence/02-a1-s12-extract.md): the R-A request "will state the exact commit SHAs that were already pushed (or
base..head), state that the content push was covered by Item 2 YES + U1 **by inference, not by a separately
written grant**, and ask the owner to confirm that the release decision covers exactly those SHAs (release plan
S10; finding M-01)".

The accepted plan repeats it three times: header line 6 ("the one inferred effect (E3) is confirmed in the R-A
request"), PR-03 ("an R-A grant that quotes the pushed SHAs and confirms the inferred coverage"), S10 ("Ask R-A
with … the **pushed SHAs + inference confirmation**"). The plan audit's residual observation 2 says the same.

**It was not done.** item2-ra/R-A-REQUEST.md (6,969 B, 774266e8…) contains no statement of the inference, no
effect table, no owner-confirmation request, and no "E3" outside a hex digest; its single "content push"
occurrence is a prior-state sentence. The owner's R-A answer (RA-DECISION) grants one dispatch and five
conditions; it says nothing about the content push. Therefore E3 is reconciled **as INFERRED** — the marking A1
§12 gives it — and the plan's own confirmation step is recorded as conformance gap **G-01** (DRIFT-FINDINGS.md
§B), not as a drift against a consumer record.

What the owner's CP-02=A answer adds: it fixes **which record governs the allocation** (A1 §12) and therefore
endorses the inference as the correct reading of E3. It does not perform the SHA-bound confirmation, and this
record does not pretend it does.

### 5.2 E7, E9, E10, E11 — the four dispatches, each under a different instrument

| Effect | Instrument | Shape of the grant |
| --- | --- | --- |
| E7 deploy A | R-A per-ask | one owner answer, one dispatch, conditions (a)-(e) incl. "no retry", "re-observe prior state", "report observed evidence", "not reversible by R-A", "record in the ledger/register" |
| E9 deploy B | SDP-1 item 4 | standing conditional pre-grant; (a) prior report posted 02:14:01Z, (b) gate PASS at dispatch commit + FAIL-CLOSED at pre-bundle, (c) CP-16 in the frozen set, (d) prior state re-observed 8.3 s before dispatch |
| E10 restore A | SDP-1 item 4 | same four conditions, MET at 02:43:07Z (window age 129 s) |
| E11 re-advance B | SDP-1 item 4 | same four conditions, MET at 02:45:41Z (window age 49 s) |

This is A1 §12's own rule ("A grant for one effect never covers the next") applied correctly: four dispatches,
four separately evidenced grants, 4 deployments, 6 runs, 0 retries, 0 settings changes, 0 Pages builds.

### 5.3 E12 and E14 — where the consumer record and the allocation part company

E12 and E14 are the two rows where a consumer record states an authority the authoritative allocation does not
give it. Both are recorded as drift findings (D-01 R-EMPTY, D-03 manual-only) with exact quotes and hashes in
DRIFT-FINDINGS.md. Neither effect was taken, so neither drift changes a delivered effect; both change what a
future reader would believe is pre-authorised, which is why they are recorded rather than noted.

### 5.4 The rows that are about *not* doing something

E5, E12, E15, E16, E19 are NOT GRANTED and nothing was taken. For CP-02 they matter as much as the grants: the
proof's containment claim is that the four deployments are the *whole* provider effect, and the counts in §4
(4 deployments, 6 runs, 0 builds, 0 settings changes, 0 repository deletions, 0 exports) are what makes "no
source or synthetic grant inherited" testable rather than rhetorical.

---

## 6. CP-02's frozen acceptance sentence, leg by leg

Frozen text (FREEZE, 12,392 B, 85c773fb…, line 59): "Real repository, exposure, budget and planned effects
reconcile to applicable consumer scope; no source or synthetic grant is inherited."

| Leg | Test | Observation | Evidence |
| --- | --- | --- | --- |
| **Real repository** | one provider repository, not a fixture | ModernNomad-98/aegis-consumer-proof, public, default branch main, 13 commits, admin permission held by the owner account | A1 §8; PROVIDER-AFTER .repo; commit chain |
| **Exposure** | stated visibility, world-readable, no second surface | public repository and public Pages site, one default URL, no custom domain, no second host, no second account | A1 §8 "Environment boundary"; A1 §9 visibility; DEPLOY-A §13 |
| **Budget** | no spend, no unreadable-cost exposure | no billing scope requested or granted; plan unreadable; no spend; only two provider POSTs at creation (U1/U2) and read-only GETs since | A1 §8, §9; E18 row above |
| **Target = one repository, one account, one URL** | the plan's CP-02 acceptance clause | repository + account + URL above; every deployment carries environment_url https://modernnomad-98.github.io/aegis-consumer-proof/ | PROVIDER-AFTER deployment_A/B environment_url; LIVE-SUMMARY .base |
| **Planned effects reconcile** | every effect names a grant or is marked NOT GRANTED/INFERRED | 19/19 in §4; 12 granted/read-only/not-needed/delegated, 1 inferred, 6 not granted and not taken | §4 table; evidence/01-source-hashes.json |
| **No source grant inherited** | no APR/source approval used for a consumer effect | A1 §8: "The source repository's settings, checks and approvals are **not** part of this consumer environment and confer nothing here (CP-02)"; SDP-1 §3: the record "does not carry the release authorizations… the owner gave in the same session for the source project"; SDP-1a: "this repository has no approval register entry, no approval-register grant and no merge-by-agent path" | A1 §8; SDP-1 §3, §5 (SDP-1a) |
| **No synthetic grant inherited** | no fixture/answer-key authority used | the CP-19 fixture batch is unbuilt and unrun (CP-19 UNRUN); no fixture grant appears in any dispatch record; each dispatch names an owner instrument (R-A or SDP-1 item 4) | CP ledger CP-19 row; RB-DEPLOY §2; R-RB1 §2 |

---

## 7. Verdict

**CP-02 = PASS** (operator leg). 19 of 19 planned effects are reconciled to a named grant, a conditional granted
pre-grant with its conditions evidenced, a read-only/delegated class, or an explicit NOT GRANTED / INFERRED
marking; 0 are unreconciled; the target/exposure/budget legs are observed; no source or synthetic grant is
inherited. Three drift findings are recorded against consumer records, per the owner's decision, and none of them
changes a delivered effect.

**Residual limits, stated rather than hidden:**

1. **E3 remains inferred and unconfirmed** (G-01). The marking is permitted by the frozen sentence; the plan's
   prescribed confirmation is absent and is not manufactured here.
2. **RV-1 has not verified this row.** The plan's CP-02 row reads "operator; verified by RV-1", and freeze
   roll-up rule 4 requires a reviewer independent of the actor for a PASS. This record is the operator leg only;
   CP-22's designated reviewer is the natural RV-1. Same narrow-independence handling as CP-05 (L7) and CP-08
   (N-1) — disclosed, not papered over.
3. **The drift findings are unresolved by design.** The owner's decision assigns drift findings *against the
   consumer record*; it does not authorise this task to decide precedence where a later owner instruction
   (SDP-1) says more than A1 §12 (D-01, D-03). Those are for the next STATUS, not for a silent fix.
4. **No provider call was made.** Every provider value is from a prior read-only capture; if the live site moved
   after 02:46:11Z 2026-10-29, this record would not know. The last recorded state is 4 deployments, B served.

---

## 8. What this record does not do

- It does not edit CP-LEDGER.md, LEDGER-UPDATE.md, the closeout record, the plan, the freeze, cases.json or any
  consumer record.
- It does not dispatch, deploy, roll back, unpublish, export or change a setting.
- It does not convert E3 into a grant, and it does not re-open CP-02's frozen text or the 22-case denominator.
- It does not claim RV-1 independence, CP-22 closeout, or any readiness beyond what §6 states.
