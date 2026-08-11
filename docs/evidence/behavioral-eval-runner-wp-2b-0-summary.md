# Behavioral Eval Runner — WP-2B-0 capability-and-evidence spike: repository-safe summary

**Final spike status: EVIDENCE-BOUNDED NON-MODEL REPORT — INCOMPLETE / BLOCKED (zero model
dispatches). Awaiting independent evidence review and the owner's manual decision.**

This file is the sanitized, repository-safe closeout summary required by BER-DEC-005. It
contains no raw transcript, no personal path, no credential, no private hostname, and no
unrestricted configuration data. Raw/confidential evidence remains external under the
authorized evidence root and is described (with byte counts and SHA-256 hashes) only in the
accompanying evidence manifest. Per the binding non-circular finalization protocol, this
summary deliberately does NOT contain the final manifest hash or the finalization-marker hash.

## 1. Authorization and baseline

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
| Remote `main` at execution start | `11f45f2b3fe4774f519a4153767587532e027e79` (unmoved) |
| Work package | WP-2B-0 (capability and evidence spike) |
| Execution-session ID | `BER-2B0-20260811T143734Z-a38548` (the single authorized control session) |

## 2. Timestamps

| Event | UTC |
| --- | --- |
| Control-session start | 2026-08-11T14:30:47Z |
| First evidence creation (evidence root) | 2026-08-11T14:37:34Z |
| Evidence collection completed / summary finalized | 2026-08-11T14:43:43Z (verified clock read) |
| Absolute wall-clock deadline (start + 4 h) | 2026-08-11T18:30:47Z (not reached) |
| Evidence expiration (creation + 30 days) | 2026-09-10T14:37:34Z |

Intermediate timestamps inside evidence files are control-session approximations bounded by
the verified clock reads listed above.

## 3. Pre-execution safety gates (both PASSED before any write)

- **Physical-path check: PASS.** `C:\` and `C:\temp` resolved unambiguously; no symlink,
  junction, mount, or reparse point anywhere in the chain; volume is local Fixed NTFS
  (Healthy); `C:\temp` is outside every Git repository; the evidence root and probe workspace
  were created directly beneath resolved `C:\temp` and re-validated (reparse-free) after
  creation.
- **Encryption-at-rest check: PASS.** `Get-BitLockerVolume` is not permitted in the
  non-elevated session; the read-only Windows-native shell property
  `System.Volume.BitLockerProtection` returned code 1 = BitLocker ON (protected) for the
  volume holding `C:\temp`. No key protectors, recovery keys, or unrelated volume details
  were collected.

## 4. Authorization caps vs actual usage

| Cap (BER-DEC-005) | Authorized maximum | Actual |
| --- | --- | --- |
| Model dispatches | 20 | **0** |
| Assistant turns | 60 | 26 at evidence finalization (self-counted; no host turn counter). Closeout turns after finalization are additional and reported in the closeout PR. |
| Concurrency | 1 | 1 (procedural; no dispatch ever in flight) |
| Probe-session duration | 15 min | n/a (no dispatches) |
| Total wall clock | 4 h | ~13 min to evidence finalization |
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

## 5. R1–R5 dispositions (prepared for owner ratification)

| Gate | Disposition | Basis (full detail in external raw reports, listed in the manifest) |
| --- | --- | --- |
| R1 — activation observation | **UNAVAILABLE / UNKNOWN** (backlog acceptance path 3: limitation recorded) | No activation-observation probes were authorized (envelope gate). No Tier-1 signal proven; no Tier-2 promotion attempted; candidate mechanisms (skill-invocation tool events; host hook events; output signatures) recorded as unproven hypotheses only. Ambiguity semantics preserved (`ERROR` / `AMBIGUOUS_ACTIVATION`). No broad routing claim. |
| R2 — judge calibration | **INCOMPLETE / BLOCKED** | Zero calibration dispatches. No judge pinned, no dataset versioned, no confusion matrix / false-PASS / false-FAIL / abstention / critical-split numbers exist. No OD-1 thresholds invented. Nothing baseline-eligible. |
| R3 — cost observability | **UNAVAILABLE / UNKNOWN** | Direct monetary reservation UNAVAILABLE in-session; monetary observability at best after-use; complete proxy envelope not provable pre-dispatch from a control session. Note for 2B-1: a purpose-built runner control plane owning dispatch could still implement the design's decided D3 fallback; nothing here proves that impossible — it was simply not provable from this session. |
| R4 — isolation / per-tool-path confinement | **INCOMPLETE / BLOCKED** | Effective per-tool-path probes did not run (gate). Non-model observations recorded: in the inspected default profile, built-in Read/Write reach multiple directory roots under permission mediation; network egress was available; an MCP surface is present; a permission-gated unsandboxed-escape parameter exists; control-plane eval-corpus inaccessibility is NOT proven (corpus is ordinary readable repo content in this profile). Per design §15/§17a broad live execution remains blocked. |
| R5 — execution-profile observability/isolation | **INCOMPLETE / BLOCKED** | Partial existence-level observability proven (managed policy absent; user-scope settings present; project/local settings absent in the clone; runtime 2.1.220; 184 shipped skills + `_template`; 7 project subagents; user-scope skills/agents/CLAUDE.md absent; auto-memory active for the control session). Isolation NOT proven; no isolation switch verified; hooks/plugins/auto-update state UNKNOWN without prohibited config dumps. Affected runs would be non-baseline-eligible per design §5e. |

## 6. Aggregate recommendation

**INCOMPLETE / BLOCKED.** Outcome A is unavailable (no proven activation mechanism, no proven
boundary, no proven confinement, no isolatable profile, no measured calibration). Outcome B
(limited scope) is not recommended by this session because the evidence gathered is
non-model-only; whether any narrower scope is acceptable is precisely the owner's call, not
this report's. **Only Peter Nguyen can decide the final WP-2B-0 outcome.**

## 7. Owner decisions required

1. Ratification (or rejection) of the R1–R5 dispositions above.
2. The aggregate WP-2B-0 outcome decision: outcome A / outcome B (limited scope) / no-go /
   incomplete-blocked, per design §17a item 10.
3. OD-1 remains open with no measured input (no thresholds proposed; none invented).
4. Whether any narrower scope or retry under a different enforcement surface (e.g., a
   runner-owned dispatch process, per the R3 report's 2B-1 note) should be separately
   authorized — resumption requires a new reviewed and merged authorization (the single
   authorized control session rule).
5. Whether a separate backlog-status update PR is authorized (this session changed no
   R/WP/BER status, per its authority boundary).

## 8. Intentionally not done (complete list)

- No model dispatches of any kind (0 of 20): no R4/R5 probes, no R1 activation probes, no R2
  calibration calls — mandated by the envelope determination.
- No judge selection, no calibration dataset, no thresholds.
- No runner-core implementation, schemas, graders, or judge implementation.
- No Scenario A execution; no `evals.json` / `trigger-evals.json` execution; no corpus
  execution of any kind.
- No skill, eval, workflow, validator, AGENTS.md, CLAUDE.md, README, design, or backlog
  modification.
- No package installation; no deployment; no configuration or hook changes; no enforcement
  workaround invented or installed.
- No evidence cleanup: the external evidence root and the disposable probe workspace are
  retained intact for owner review (probe workspace was created, held synthetic canaries
  only, and was never used by any dispatch). Cleanup remains marker-gated and deferred to
  owner review; expiration 2026-09-10T14:37:34Z.
- No WP-2B-1 authorization or preparation; no auto-merge; no merge.

## 9. Evidence inventory (identifiers only; bytes/hashes in the evidence manifest)

External, confidential, under the authorized evidence root (readers: Peter Nguyen and the
single authorized control session only): `.aegis-owned-evidence.json`, `budget-ledger.json`,
`budget-ledger.sha256`, `dispatch-allocation-plan.json`, `raw/r1-activation-observation-report.md`,
`raw/r2-judge-calibration-report.md`, `raw/r3-cost-observability-report.md`,
`raw/r4-containment-inspection-report.md`, `raw/r5-execution-profile-report.md`. Disposable
probe workspace (synthetic only, unused): `.aegis-probe-workspace.json`,
`canary-read-target.txt`, `canary-write-target.txt`. Provider calls: none (zero dispatches).

## 10. Compliance assertions

- No raw transcript is included in this repository change.
- No personal path, username, personal email address, machine name, or private hostname
  appears in the three repository-safe files.
- No credential, token, password, private key, or cookie was collected or stored anywhere.
- No unrestricted environment dump, configuration dump, or directory listing was collected;
  user-scope configuration was checked for existence only, never read.
- The validator, CI workflows, skills, evals, design, and backlog are untouched; this change
  adds exactly three new repository-safe files and modifies nothing.
