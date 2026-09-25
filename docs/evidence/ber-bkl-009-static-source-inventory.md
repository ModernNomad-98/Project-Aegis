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
