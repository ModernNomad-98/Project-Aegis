# BER-BKL-009 residual host, runtime, privacy and cleanup proposal

Prepared 2026-09-25 for Project Aegis owner review. **Source-only proposal; no
operational grant.** Behavioral Eval Runner (BER) backlog item 009 remains
**PARTIALLY DELIVERED**. This page proposes how to scope the residual work; it
does not select an evidence host, attest a machine, authorize a live run, clear
publication or permit deletion. The owner's [APR-009 policy
selection](../approvals/APPROVAL_REGISTER.md#aegis-apr-009-behavioral-eval-runner-evidence-policy-selection)
already fixes a 30-day complete-bundle review clock and the Windows work
package 2B-3 (WP-2B-3) owner-plus-SYSTEM/BitLocker target. The bounded offline
proof and integration were delivered in pull requests (PRs) #139 and #257;
their one-use grants are consumed. Do not repeat those scopes or treat their
synthetic preflight as host proof.

## What remains and why it is separate

The [static source inventory](../evidence/ber-bkl-009-static-source-inventory.md)
found `OfflinePolicyWriter` in the source but no non-test production caller
that instantiates it. The existing [operator review
runbook](ber-bkl-009-operator-policy-runbook.md) inventories owned synthetic
bundles and preserves failures; it contains no deletion command. A policy
receipt records classification and hashes, but does not prove the content's
classification, a real host's access-control list (ACL), encryption or recovery
key custody. The [backlog](behavioral-eval-runner-backlog.md#ber-bkl-009--evidence-retention-access-encryption-redaction-and-deletion-policy)
and [integration review](../evidence/ber-bkl-009-policy-integration-review.md)
identify the remaining host, runtime, privacy and operator gates.

Here, **host proof** means direct, current evidence from the named machine and
exact evidence root, independently reviewed. **Runtime binding** means every
actual artifact creation and reader path uses the selected policy and checks
before semantic use. **Privacy review** means inspecting the actual content
classes and intended output for sensitive data before a judge or public
derivative sees it. **Marker-gated cleanup** means a separately authorized
operator action against only an inventoried, owned bundle whose marker, path
and hashes match. The 30-day date triggers review; it is not deletion authority.

## Choices and recommendation

| Decision | Choices and cost/trade-off | Recommendation |
| --- | --- | --- |
| Evidence source and host | Reuse the Windows WP-2B-3 root only if it is the actual source and execution path; its APR-009 target is already defined, but current ACL, encryption and custody still require proof. Selecting another host, including the paused VirtualBox Linux VM, requires its own reader/encryption mechanism and owner authority; the VM's R4/R5 Stage A setup does not select it for BER evidence. An undecided host costs planning time but avoids false attestation. | Name the exact creation sites, execution host, root and expected principals first. Make no host claim until those facts are recorded. |
| Host enforcement | A read-only host assessment can establish existing settings; changing ACL inheritance, readers, encryption or recovery-key handling changes security state and has separate review and operating cost. Owner-plus-SYSTEM is the selected Windows WP-2B-3 target, not a generic rule for another OS. | Ask for a bounded, named-host read-only proof scope first. If remediation is needed, propose its exact settings, rollback and separate authority after the findings. Unknown or contradictory facts stop. |
| Runtime binding | A narrow opt-in adapter at identified creation/read sites has a smaller compatibility surface but may expose additional writers. Broad runner rewiring might cover more paths but risks legacy bytes, schema and driver behavior. Neither should silently reuse `verify-evidence`'s hash-only success as policy acceptance. | Inventory all actual artifact writers and consumers, then bind the narrowest complete path. Require policy-aware Stage A/B verification and preserve the published `1.0.0-wp2b1` bytes and per-artifact `expiration_at` meaning. Return for a versioned decision if those bytes must change. |
| Privacy and release | Keeping raw evidence in the controlled external root limits exposure but incurs local storage and review effort. A sanitized derivative can support public review only after content-specific classification, redaction and independent release review; opaque hashes and policy references alone cannot prove safety. | Keep raw transcripts, private labels, credentials and provider output out of public Git and continuous integration (CI) artifacts. Define a minimal judge envelope and independently inspect any proposed derivative before release. Preserve originals and their hashes. |
| Cleanup | Manual, marker-gated owner review takes operator time and preserves evidence for failures. A scheduled timer would reduce routine work but can erase incomplete or disputed evidence and is outside APR-009. | Design and test a dry-run inventory first. Require an explicit later owner action for each deletion scope; preserve on missing marker, path or hash mismatch, failure, incompleteness or unresolved privacy/security review. No unattended deletion. |

The cost of retained bundles is currently **unknown**: no selected real host,
measured bundle size, run volume or storage price is recorded for this residual
scope. Any storage or operator cost comparison should use measured sizes and a
named host, then include the 30-day review period and preserved failures. The
historical 8–16 active-hour whole-item estimate cannot be carried forward:
the offline integration is delivered and the remaining work is **TBD** pending
the host, source-path inventory and separate scopes. No finite completion date
or active-work total is defensible yet. This proposal itself makes no claim
that a runtime implementation has begun.

## Bounded sequence and evidence gates

1. **Source-only decision packet.** Record the selected runtime evidence source,
   exact artifact creation and read sites (including adjacent ledgers and
   materialized files), proposed host/root, expected principals, data classes,
   intended judge/public output, and the gaps in existing checks. Include
   source revision and a changed-path/byte-compatibility plan. Reconcile the
   recorded [GitHub continuation and backup direction](../evidence/ber-recovery-2026-09-11/README.md)
   with this policy: identify which reviewed, sanitized repository records are
   recoverable from GitHub and which raw external bundles or private inputs
   remain outside it, without proposing to upload those bytes. Static code
   evidence cannot establish a host's state or actual content safety.
2. **Named-host read-only proof, under its own scope.** Verify exact physical
   path and ownership, reparse/symlink safety, effective ACL/readers and
   inheritance, encryption state and recovery-key custody without recording
   key material. Record commands, time, host identity in a protected local
   record, sanitized findings for repository review, and an independent
   reviewer. A marker assertion or `SIMULATION_ONLY` result is insufficient.
   If controls fail, stop before writing real evidence and return a separate
   remediation proposal.
3. **Runtime and privacy implementation, under a reviewed grant.** Set exact
   code/runbook paths, source baseline, hours/line/spend ceilings and rollback
   before changes. Bind each approved creation/read path to explicit
   classification, the one first-evidence clock and policy-aware verification.
   Test refusal, legacy compatibility, preserve-on-failure, judge-envelope
   minimization and redaction decisions offline. Real content and provider use
   need their own applicable authority; this proposal grants neither.
4. **Operator cleanup design and dry run, then separate deletion action.** Write
   a reviewed procedure that inventories one exact root and all Stage A/B
   artifacts and marker; compares paths, bytes and hashes; checks current host
   controls; records review date and explicit owner disposition; and dry-runs
   against owned synthetic fixtures. A deletion proposal must identify exact
   targets, independent review, rollback limits and retained sanitized audit
   record. Actual removal waits for a separate explicit owner action.
5. **Closeout.** Independently review the [twelve temporary WP-2B-0 spike
   evidence-handling terms](behavioral-eval-runner-backlog.md#minimum-phase-2b-0-spike-evidence-handling-terms-mandatory-authorization-content)
   against the final policy; record for each term whether it is absorbed or
   retired and why, without rewriting the historical spike authorization.
   Record the GitHub recovery disposition and the boundary keeping raw/private
   evidence external. Independent security/privacy review, exact-source tests
   and applicable CI should demonstrate each gate. Update BER-BKL-009 to DONE
   only when the selected host, runtime, content handling, operator procedure,
   recovery disposition and spike-term reconciliation have reviewed evidence.
   Preserve unresolved or failed bundles.

Each step can produce a useful reviewable artifact without assuming the next
step's authority. Reassess scope and estimate after the source/host choice, and
again if the host controls or actual content classes differ from the plan.

## Exact owner questions for a later authorization packet

1. Which **specific runtime source, execution host and evidence root** are in
   scope? Is the Windows WP-2B-3 root actually used, or is a different host
   proposed? What source revision and exact artifact creation/read paths must
   the implementation cover?
2. For that host, which **named principals** need read or write access to each
   artifact class? What ACL/inheritance and encryption mechanism, current
   state, verification method and recovery-key custodian are proposed? If a
   change is required, what exact settings and rollback are authorized?
3. Which **content classes and recipients** are permitted for the runtime
   bundle, judge envelope, private scoring and public derivative? Who performs
   the independent content/redaction and publication review, and what evidence
   may be sanitized into this source repository?
4. Which **exact paths, baseline, active-hour/line/spend ceilings and tests**
   would a runtime/host implementation grant cover? Does any proposed change
   alter published evidence bytes, schema or legacy caller behavior?
5. For a future cleanup action, which **exact bundle/root and hashes** may be
   removed, who reviews the dry-run inventory and failed/incomplete state, and
   what explicit owner action authorizes that removal? What is retained as a
   sanitized audit record?

These are scope and evidence questions, not a request to reconfirm APR-009's
selected 30-day policy. A later grant should be transcribed into the BER
decision log and approval register with its exact limits. This page changes
neither record and confers no inferred permission to inspect a VM or private
input, use credentials, call a provider, change host controls, publish raw
material or delete evidence.
