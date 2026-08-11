# Behavioral Eval Runner — WP-2B-0 capability-and-evidence spike: repository-safe summary

**WP-2B-0 OWNER OUTCOME: OUTCOME B / LIMITED SCOPE — ACCEPTED.**
**EVIDENCE STATE: R1/R3 remain UNAVAILABLE/UNKNOWN; R2/R4/R5 remain INCOMPLETE/BLOCKED.**
**LIVE BEHAVIORAL EXECUTION: STILL BLOCKED. WP-2B-1: NOT AUTHORIZED BY THIS PR.**
**NEXT GOVERNANCE STEP: a separate reviewed repository authorization is required for WP-2B-1. OD-1: OPEN.**

This file is the sanitized, repository-safe closeout summary required by BER-DEC-005, corrected
after owner review. It contains no raw transcript, no personal path, no credential, no private
hostname, and no unrestricted configuration data. Raw/confidential evidence remains external
under the authorized evidence root and is described (with byte counts and SHA-256 hashes) only
in the accompanying evidence manifest. Per the binding non-circular finalization protocol, this
summary deliberately does NOT contain the final manifest hash or the finalization-marker hash.

## 1. Owner decision (recorded)

- **Owner:** Peter Nguyen
- **Decision:** OUTCOME B / LIMITED SCOPE — ACCEPTED
- **Decision date:** 2026-08-11
- **Decision time:** approximately 2026-08-11T15:05Z (minute precision only)
- **Accepted evidence dispositions (final WP-2B-0 evidence state):**
  R1 UNAVAILABLE / UNKNOWN · R2 INCOMPLETE / BLOCKED · R3 UNAVAILABLE / UNKNOWN ·
  R4 INCOMPLETE / BLOCKED · R5 INCOMPLETE / BLOCKED

Explicit statements bound to this decision:

- Outcome A was NOT established; none of the gates is claimed technically solved.
- OD-1 remains OPEN (no thresholds proposed, none ratified, no measured calibration input).
- No baseline-eligible semantic judging exists.
- No broad routing proof exists.
- No full containment proof exists.
- No Scenario A execution is authorized.
- No generic behavioral corpus execution is authorized.
- Baseline claims and CI-promotion claims remain blocked.
- WP-2B-1 is NOT authorized by this PR; a separate reviewed and merged authorization is
  required before WP-2B-1 begins.

**Accepted meaning of Outcome B / Limited Scope:** the current Claude Code control
session/host did not prove the complete pre-dispatch enforcement and containment surfaces
required for live behavioral execution. A future, separately authorized WP-2B-1 may build the
non-live runner control plane and minimum guardrails intended to own and enforce those
controls (dispatch counting, token/call budgets, timeouts, concurrency, evidence boundaries,
containment), using the recorded limitations as binding constraints. The unresolved
R1/R2/R4/R5 evidence remains binding on later live phases and must not be silently treated as
solved.

## 2. Authorization and baseline

| Item | Value |
| --- | --- |
| Authorization record | BER-DEC-005 (append-only governance log, `docs/roadmaps/behavioral-eval-runner-backlog.md` §13) |
| Authorization PR | #80 — merged 2026-08-11T13:55:40Z |
| Authorization merge SHA | `11f45f2b3fe4774f519a4153767587532e027e79` |
| Authorization merge tree SHA | `882c0b6c8d5eb906df9e7d9d8576937b4c545db7` |
| Reviewed backlog blob at merge | `3fc5230c24fcaf8cb8b77e016ea9acd41b013086` (verified equal) |
| Execution branch | `spike/behavioral-eval-runner-2b-0` |
| Execution branch base SHA | `11f45f2b3fe4774f519a4153767587532e027e79` (== authorization merge SHA) |
| Execution branch base tree SHA | `882c0b6c8d5eb906df9e7d9d8576937b4c545db7` (== authorization merge tree SHA) |
| Remote `main` at execution start and at re-finalization | `11f45f2b3fe4774f519a4153767587532e027e79` (unmoved) |
| Work package | WP-2B-0 (capability and evidence spike) |
| Execution-session ID | `BER-2B0-20260811T143734Z-a38548` (the single authorized control session; this correction ran in the SAME continuously running session) |

## 3. Timestamps

| Event | UTC |
| --- | --- |
| Control-session start | 2026-08-11T14:30:47Z |
| First evidence creation (evidence root) | 2026-08-11T14:37:34Z |
| Provisional evidence collection completed / first summary finalized | 2026-08-11T14:43:43Z |
| Provisional closeout commit pushed (see §7 deviation) | commit `a6c7159739222495a108120e3375f82f191317f9`, PR #81 opened ~2026-08-11T14:48Z |
| Owner decision (Outcome B accepted) | approximately 2026-08-11T15:05Z (minute precision) |
| Correction continuation start (same session) | 2026-08-11T15:30:36Z (verified clock read) |
| External evidence integrity re-verification | 2026-08-11T15:31Z — ALL 12 external manifest-listed artifacts MATCH (bytes + SHA-256); no reparse point in any validated chain |
| Absolute wall-clock deadline (start + 4 h) | 2026-08-11T18:30:47Z (not reached) |
| Evidence expiration (creation + 30 days) | 2026-09-10T14:37:34Z |

Intermediate timestamps inside evidence files are control-session approximations bounded by
the verified clock reads listed above.

## 4. Pre-execution safety gates (both PASSED before any write; re-run before re-finalization)

- **Physical-path check: PASS (initial and re-run).** `C:\` and `C:\temp` resolve
  unambiguously; no symlink, junction, mount, or reparse point anywhere in the validated
  chains (including every retained evidence and probe-workspace artifact at re-verification);
  volume is local Fixed NTFS (Healthy); `C:\temp` is outside every Git repository; the
  evidence root and probe workspace live directly beneath resolved `C:\temp`.
- **Encryption-at-rest check: PASS.** `Get-BitLockerVolume` is not permitted in the
  non-elevated session; the read-only Windows-native shell property
  `System.Volume.BitLockerProtection` returned code 1 = BitLocker ON (protected) for the
  volume holding `C:\temp`. No key protectors, recovery keys, or unrelated volume details
  were collected.

## 5. Authorization caps vs actual usage

| Cap (BER-DEC-005) | Authorized maximum | Actual |
| --- | --- | --- |
| Model dispatches | 20 | **0** (unchanged through this correction; no dispatch authority remains in this session) |
| Assistant turns | 60 | Self-count 36 at this re-finalization write (~38 projected through marker completion); ALL remaining turns through the hard cap are RESERVED for this final closeout; unreserved remaining: 0. Host-level turn counting is unavailable; this is a conservative control-session self-count plus reservation. |
| Concurrency | 1 | 1 (procedural; no dispatch ever in flight) |
| Probe-session duration | 15 min | n/a (no dispatches) |
| Total wall clock | 4 h | ~13 min to first evidence finalization; correction continuation began 2026-08-11T15:30:36Z, within the deadline |
| Input tokens (dispatches) | 400,000 | 0 (dispatches); control-session token use not machine-observable → UNKNOWN |
| Output tokens (dispatches) | 80,000 | 0 (dispatches); control-session token use UNKNOWN |
| Monetary | USD 5.00 ceiling | **UNKNOWN** (no in-session metering; zero dispatches; no claim of technical monetary enforcement is made) |

**Why zero dispatches:** the Phase 9 model-dispatch gate failed at its envelope condition.
Non-model R3 inspection determined that neither direct monetary reservation nor the complete
proxy envelope (dispatch/turn/concurrency/session-timeout/deadline/token ceilings) is provable
as host-enforceable BEFORE dispatch from within the authorized control session — every such
control is self-tracked or observable only after use, and BER-DEC-005 states a control that is
only observable after use is not a hard cap. The authorization's mandated consequence was
followed exactly: no model call; R3 recorded unavailable/unknown; bounded non-model report.
The owner's Outcome B decision accepts exactly this evidence state.

## 6. R1–R5 dispositions (owner-accepted as the final WP-2B-0 evidence state)

| Gate | Disposition | Basis (full detail in external raw reports, listed in the manifest) |
| --- | --- | --- |
| R1 — activation observation | **UNAVAILABLE / UNKNOWN** (backlog acceptance path 3: limitation recorded) | No activation-observation probes were authorized (envelope gate). No Tier-1 signal proven; no Tier-2 promotion attempted; candidate mechanisms (skill-invocation tool events; host hook events; output signatures) recorded as unproven hypotheses only. Ambiguity semantics preserved (`ERROR` / `AMBIGUOUS_ACTIVATION`). No broad routing claim. |
| R2 — judge calibration | **INCOMPLETE / BLOCKED** | Zero calibration dispatches. No judge pinned, no dataset versioned, no confusion matrix / false-PASS / false-FAIL / abstention / critical-split numbers exist. No OD-1 thresholds invented. Nothing baseline-eligible. |
| R3 — cost observability | **UNAVAILABLE / UNKNOWN** | Direct monetary reservation UNAVAILABLE in-session; monetary observability at best after-use; complete proxy envelope not provable pre-dispatch from a control session. Note for 2B-1: a purpose-built runner control plane owning dispatch could still implement the design's decided D3 fallback; nothing here proves that impossible — it was not provable from this session. |
| R4 — isolation / per-tool-path confinement | **INCOMPLETE / BLOCKED** | Effective per-tool-path probes did not run (gate). Non-model observations recorded: in the inspected default profile, built-in Read/Write reach multiple directory roots under permission mediation; network egress was available; an MCP surface is present; a permission-gated unsandboxed-escape parameter exists; control-plane eval-corpus inaccessibility is NOT proven (corpus is ordinary readable repo content in this profile). Per design §15/§17a broad live execution remains blocked. |
| R5 — execution-profile observability/isolation | **INCOMPLETE / BLOCKED** | Partial existence-level observability proven (managed policy absent; user-scope settings present; project/local settings absent in the clone; runtime 2.1.220; 184 shipped skills + `_template`; 7 project subagents; user-scope skills/agents/CLAUDE.md absent; auto-memory active for the control session). Isolation NOT proven; no isolation switch verified; hooks/plugins/auto-update state UNKNOWN without prohibited config dumps. Affected runs would be non-baseline-eligible per design §5e. |

## 7. PROCEDURAL SEQUENCING DEVIATION (recorded truthfully; not hidden)

- The three provisional sanitized closeout files were pushed to the public PR branch in
  commit `a6c7159739222495a108120e3375f82f191317f9` (PR #81) BEFORE Peter Nguyen recorded
  the final Outcome B owner decision.
- No raw/confidential evidence was committed; no credential, token, password, private key,
  user-profile path, raw transcript, or unrestricted configuration dump was included.
- The corrected second commit supersedes the provisional closeout bytes; the deviation does
  NOT convert the provisional artifacts into final owner-approved evidence.
- The final repository-safe bytes are those produced after the owner decision and after the
  integrity re-verification of this continuation.
- The deviation remains visible in Git history; it is not hidden, rewritten, or
  force-pushed away, and the original sequencing is NOT claimed to have been compliant.

## 8. Owner decisions — made and remaining

**Made (this record):** the aggregate WP-2B-0 outcome decision — OUTCOME B / LIMITED SCOPE
ACCEPTED — together with acceptance of the R1–R5 dispositions above.

**Remaining open:**

1. OD-1 (judge-calibration numeric thresholds) — OPEN; no measured input exists yet.
2. Authorization of WP-2B-1 (non-live runner control plane and minimum guardrails) — requires
   a separate reviewed and merged repository authorization per the work-package protocol.
3. Whether a separate backlog-status update PR is authorized (this session changed no
   R/WP/BER status, per its authority boundary).

## 9. Intentionally not done (complete list)

- No model dispatches of any kind (0 of 20), in the original spike and in this correction.
- No judge selection, no calibration dataset, no thresholds.
- No runner-core implementation, schemas, graders, or judge implementation.
- No Scenario A execution; no `evals.json` / `trigger-evals.json` execution; no corpus
  execution of any kind.
- No skill, eval, workflow, validator, AGENTS.md, CLAUDE.md, README, design, or backlog
  modification.
- No package installation; no deployment; no configuration or hook changes; no enforcement
  workaround invented or installed.
- No evidence cleanup: the external evidence root and the disposable probe workspace are
  retained intact for owner review (the probe workspace held synthetic canaries only and was
  never used by any dispatch). Cleanup remains marker-gated; expiration 2026-09-10T14:37:34Z.
- No WP-2B-1 authorization or preparation; no auto-merge; no merge; no amend; no rebase; no
  force-push; no PR comment; no reviewer request.

## 10. Evidence inventory (identifiers only; bytes/hashes in the evidence manifest)

External, confidential, under the authorized evidence root (readers: Peter Nguyen and the
single authorized control session only): `.aegis-owned-evidence.json`, `budget-ledger.json`,
`budget-ledger.sha256`, `dispatch-allocation-plan.json`, `raw/r1-activation-observation-report.md`,
`raw/r2-judge-calibration-report.md`, `raw/r3-cost-observability-report.md`,
`raw/r4-containment-inspection-report.md`, `raw/r5-execution-profile-report.md`. Disposable
probe workspace (synthetic only, unused): `.aegis-probe-workspace.json`,
`canary-read-target.txt`, `canary-write-target.txt`. Provider calls: none (zero dispatches).
At the integrity re-verification of 2026-08-11T15:31Z, every artifact above MATCHED its
recorded byte count and SHA-256; `budget-ledger.json` and `budget-ledger.sha256` were then
updated (owner decision + conservative turn accounting) and re-hashed into the corrected
manifest.

## 11. Compliance assertions

- No raw transcript is included in this repository change.
- No personal path, username, personal email address, machine name, or private hostname
  appears in the three repository-safe files.
- No credential, token, password, private key, or cookie was collected or stored anywhere.
- No unrestricted environment dump, configuration dump, or directory listing was collected;
  user-scope configuration was checked for existence only, never read.
- The validator, CI workflows, skills, evals, design, and backlog are untouched; this change
  modifies exactly the three repository-safe closeout files and nothing else.
