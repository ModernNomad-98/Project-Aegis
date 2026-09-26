# BER-BKL-009 evidence source inventory

This is a **static source inventory** for the Project Aegis owner and reviewers
planning the remaining Behavioral Eval Runner (BER) evidence-policy work.
`BER-BKL-009` is the runner's backlog item for evidence retention, access,
encryption, redaction and deletion. This inventory describes the source tree
at merge `69be30a3a71d21c70f13a6b20d7da5e15e023d17`
(pull request #267). Read it with the [owning backlog item](../roadmaps/behavioral-eval-runner-backlog.md#ber-bkl-009--evidence-retention-access-encryption-redaction-and-deletion-policy),
the [selected policy](../approvals/APPROVAL_REGISTER.md#aegis-apr-009-behavioral-eval-runner-evidence-policy-selection),
and the [synthetic integration review](ber-bkl-009-policy-integration-review.md).
BER-BKL-009 is **partially delivered**. This page is not a host assessment,
implementation grant, privacy approval, publication clearance or cleanup plan.
Stage A is the input-evidence snapshot; Stage B is the final-evidence bundle
with the final report and manifest. A detached marker binds Stage B to the
completed bundle.

## What was inspected

Only tracked source and existing documentation were read. The inventory did
not start the runner, inspect an evidence root, access the paused VirtualBox
virtual machine (VM), read private inputs, call a provider, change access or
encryption settings, or delete anything. Function references below describe
available code paths; they do not prove that a production caller uses them.
The table covers policy-bound bundle creation and its adjacent read and host
checks. It is **not** an inventory of every BER file writer: budget ledgers,
materialized fixtures and calibration records follow separate code paths.

| Source site | Current behavior and limit |
| --- | --- |
| [`evidence.py`](../../tools/behavioral_eval_runner/evidence.py), `EvidenceWriter.finalize_input_evidence` and `finalize_final_bundle` | Write the two-stage bundle and detached finalization marker. Legacy callers keep their existing serialized format; policy-bound stage transitions require the internal policy token and checks. This writer does not establish an operating-system reader list or encryption. |
| [`evidence_policy.py`](../../tools/behavioral_eval_runner/evidence_policy.py), `OfflinePolicyWriter.finalize_input` and `finalize_final` | Opt-in, synthetic local writer requires an explicit classification decision and versioned access-policy reference for each input, final artifact and report. It records one writer-stamped first-evidence time and a complete-bundle review date 30 consecutive 24-hour periods later. The policy receipts are ordinary hashed manifest artifacts; this is metadata and byte verification, not proof that content was redacted or a host was secured. |
| [`evidence_policy.py`](../../tools/behavioral_eval_runner/evidence_policy.py), `verify_policy_input` and `verify_policy_bundle`; [`evidence.py`](../../tools/behavioral_eval_runner/evidence.py), `verify_local_bundle` | `verify_policy_input` checks the Stage A receipt and classifications and returns its recorded review date; it does **not** check whether that date has passed. `verify_policy_bundle` checks the complete Stage A/B chain and final marker, then refuses an active-bundle acceptance at or after the review date. Inconsistent bundles fail closed and remain in place. The opt-in `verify_local_bundle(require_policy=True)` mode refuses a missing policy receipt; lower-level legacy hash verification is not a policy check. |
| [`evidence_policy_preflight.py`](../../tools/behavioral_eval_runner/evidence_policy_preflight.py), `evaluate_synthetic_host_facts` | Checks caller-supplied path, ownership, access-control list (ACL), inheritance, encryption and recovery-key assertions. It makes no operating-system query. Complete assertions yield `SIMULATION_ONLY`; unknown or conflicting facts yield `STOP`. Neither outcome is selected-host attestation. |
| [`evidence.py`](../../tools/behavioral_eval_runner/evidence.py), `JudgeInputGate`; [`judge/envelope.py`](../../tools/behavioral_eval_runner/judge/envelope.py), envelope construction | The gate verifies the Stage A manifest before reading a listed artifact and rehashes bytes when read. The envelope builder uses this gate and a closed allowed-key set. This source-level read boundary does not itself select the reader's operating-system principal, prove host access control, or authorize a provider request. |
| [`cli.py`](../../tools/behavioral_eval_runner/cli.py), `verify-evidence` command | Calls the lower-level Stage A and final-bundle integrity verifiers. Its `verified` result describes those requested integrity checks; it is not a BER-BKL-009 policy or host attestation. Another CLI path constructs `JudgeInputGate` for local envelope work. |
| [`judge/calibration_development_driver.py`](../../tools/behavioral_eval_runner/judge/calibration_development_driver.py), `verify_evidence_root` and development driver | Separately scoped work-package 2B-3 (WP-2B-3) code requires an exact ownership marker, rejects reparse ancestors and checks that its marker records encryption as verified. That marker check does not prove the underlying ACL, encryption state or recovery-key custody afresh, and it does not connect this driver to `OfflinePolicyWriter`. The future live entry remains gated by its own BER decisions. |

The non-test source search at this revision finds `OfflinePolicyWriter` defined
inside `evidence_policy.py`, but no non-test caller that instantiates it for a
production run. This is a static finding, not a claim that every possible
external caller has been examined. The existing [operator review runbook](../roadmaps/ber-bkl-009-operator-policy-runbook.md)
covers synthetic inventory and owner review; it contains no deletion command.

## Source-to-runtime decision packet (rechecked at `9b85140d`)

This source recheck identifies the **call sites to choose from**, not an actual
runtime execution or host. A writer creates bytes; a reader consumes them. An
evidence *root* is the directory containing one bundle, while a *manifest* is
the list of files and hashes that a verifier checks. The selected host and root
remain unknown for the residual work.

| Path and source site | Bytes created or consumed | Boundary for a later scope |
| --- | --- | --- |
| [`evidence.py`](../../tools/behavioral_eval_runner/evidence.py), `EvidenceWriter.finalize_input_evidence` / `finalize_final_bundle` | Writes Stage A artifacts and input manifest; then the final report, Stage B artifacts and manifest, and detached marker. `verify_input_evidence`, `verify_final_bundle`, and `verify_local_bundle` read them. | The writer is called by the opt-in `OfflinePolicyWriter`, but the non-test tree has no production instantiation of either writer. Identify a real producer before proposing a binding. |
| [`evidence_policy.py`](../../tools/behavioral_eval_runner/evidence_policy.py), `OfflinePolicyWriter` / `verify_policy_input` / `verify_policy_bundle` | Writes `policy/stage-a.json` and `policy/stage-b.json` receipts through the underlying writer; reads receipts, manifests, artifacts and marker for policy verification. | Synthetic integration exists. A real producer and each intended consumer must opt into policy-aware verification; a receipt does not attest content or host settings. |
| [`cli.py`](../../tools/behavioral_eval_runner/cli.py), `verify-evidence` / `build-judge-envelope` | `verify-evidence` calls lower-level hash/bundle readers. The envelope path constructs `JudgeInputGate`, which checks active policy on a policy-claimed Stage A root before reading permitted artifacts; [`judge/envelope.py`](../../tools/behavioral_eval_runner/judge/envelope.py) builds the restricted envelope. | Hash-only CLI success must not be reported as policy acceptance. Future consumers need the same policy-aware gate before semantic use. The envelope command emits metadata only and does not dispatch. |
| [`budget.py`](../../tools/behavioral_eval_runner/budget.py), `BudgetLedger._append_event` / `_write_checkpoint` | With a `store_path`, writes append-only event lines and a separate terminal checkpoint; `BudgetLedger.load` reads both. | This accounting pair is outside the Stage A/B writer. Decide whether a selected run root contains it and whether it belongs to the complete runtime bundle. |
| [`materialize.py`](../../tools/behavioral_eval_runner/materialize.py), `materialize` / `_write_under_destination` | Writes materialized fixture files and its record beneath a caller-selected destination; the [`cli.py`](../../tools/behavioral_eval_runner/cli.py) `materialize` command supplies that destination. | A materialization destination is not automatically the evidence root. Map whether and how those source bytes enter a selected run's Stage A manifest. |
| [`judge/calibration_development_driver.py`](../../tools/behavioral_eval_runner/judge/calibration_development_driver.py), `create_genesis` / `finalize` | At its fixed WP-2B-3 Windows root, writes a run manifest, canonical `runs/wp2b3-development-ledger-v1.jsonl` (through [`calibration_ledger.py`](../../tools/behavioral_eval_runner/judge/calibration_ledger.py)) and `runs/wp2b3-development-result-summary-v1.json`. On reopen, the driver reads the manifest and ledger and checks whether the summary exists. | These are separate calibration ledger/summary writers, not `EvidenceWriter` calls. The hardcoded root does not establish that it is the BER-BKL-009 runtime bundle or that its current host controls are verified. |

**Compatibility boundary.** The published WP-2B-1 evidence family is
`1.0.0-wp2b1`. Its existing Stage A/B bytes, hashes, detached marker, legacy
caller behavior and per-artifact `expiration_at` (based on each artifact's own
creation time) must remain interpretable. The policy receipt adds a separate
first-evidence **bundle review date**; it does not rewrite old artifacts or turn
their individual timestamps into a deletion instruction. The [schema
compatibility policy](../behavioral-eval-runner-schema-compatibility.md) requires
a versioned reader and separately reviewed derivative if published field meaning
or accepted bytes change. A narrow opt-in binding has less compatibility work,
but only covers the paths explicitly attached to it; broad rewiring may cover
more producers, with greater migration and regression cost. **Recommend mapping
the actual producers and readers first, then selecting the smallest complete
binding**, because the non-test writer call gap prevents a justified code scope
today. Engineering hours remain unestimated until that map and a host exist;
neither option has an approved external spend.

**Recovery boundary.** The [September 11 recovery record](ber-recovery-2026-09-11/README.md)
uses GitHub for *source-library continuation and backup*: reviewed source,
sanitized decisions and public-safe summaries are recoverable from Git history.
That does not make GitHub a backup for raw Stage A/B bundles, provider output,
private calibration inputs, local environments, wheel binaries or the local
recovery ZIP. The [selected policy](../roadmaps/ber-bkl-009-evidence-policy-decision.md)
keeps raw runtime evidence in an external controlled root and versioned private
inputs in their separate owner-only repository. A future recovery plan must
identify the named external store, measured bundle size and run volume, backup
retention and restore test before quoting storage or upkeep cost. Uploading raw
bytes to this public repository would expose material whose content has not
been independently reviewed; it is not proposed here.

**Next owner decisions.** Select the actual producer(s), consumers, execution
host and exact root; name the host principals and encryption/recovery-key
custodian; classify each created content class and intended judge/public
recipient; then approve exact implementation paths, version handling and
hour/line/spend bounds. A read-only host assessment can test existing controls
with low change risk but takes operator time. Remediation changes ACL or
encryption state and needs its own settings, rollback and authority. Deletion
remains a separate later action after a marker/path/hash dry run and explicit
owner disposition. Until those choices are made, a static inventory cannot
establish host safety, privacy clearance, complete runtime coverage or a finite
remaining ETA.

## Unresolved connections and decisions

1. **Choose the runtime evidence source and host.** Name the exact creation
   sites and selected host before binding the opt-in policy to a real run.
   The paused VirtualBox Linux VM is only the separate R4/R5 Stage A candidate;
   its setup approval does not make it the BER-BKL-009 evidence host or permit a
   probe or source transfer.
2. **Prove host controls on that host.** Independently establish root ownership,
   exact paths, allowed readers, ACL/inheritance, encryption and recovery-key
   custody. The Windows WP-2B-3 owner-plus-SYSTEM (the built-in Windows service
   account) and BitLocker target in
   [APR-009](../approvals/APPROVAL_REGISTER.md#aegis-apr-009-behavioral-eval-runner-evidence-policy-selection)
   applies to that Windows root. Another host needs its own reviewed reader
   and encryption decision. A synthetic preflight result or marker assertion
   cannot replace host verification.
3. **Bind runtime and content handling.** Identify each real artifact creation
   and reader path, assign content-specific sensitivity and redaction decisions,
   and ensure the right consumers use policy-bound verification. Independently
   review actual content before any external sharing or public derivative.
4. **Design operator cleanup separately.** Keep failed or incomplete bundles;
   a reached review date is only a review trigger. Any future deletion needs an
   exact root and hash inventory, marker and physical-path checks, privacy and
   security review, a reviewed procedure, and a separate explicit owner action.

The one synthetic integration grant, [APR-023](../approvals/APPROVAL_REGISTER.md#aegis-apr-023-bounded-synthetic-evidence-policy-integration),
was consumed by pull request #257. The session's commit/push/merge approval
does not enlarge that grant. The remaining host, runtime, privacy and cleanup
work needs a new bounded scope and applicable owner authority. The current
[forecast](../roadmaps/aegis-backlog-forecast.md#start-here--current-reading)
therefore leaves this residual unestimated; it does not convert the former
8–16-hour whole-item estimate into a promise.
