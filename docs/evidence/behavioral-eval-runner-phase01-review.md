# BER Phase 0/1 — PR #88 reconciliation and local corrections

Review date: 2026-09-10. Local work is based on PR #88 head
`ac9e1cdb020f4efb7a52e5ea606c3b329fb486e2`, whose authorization base remains
`1c3e4931329179d9a3f9cc9ec1bb93020378c043` (PR #87). GitHub rechecked during
this review: PR #88 open at that same head; all 12 threads unresolved and not
outdated. Local corrections do not resolve remote review threads.

This is the resumed, owner-approved Phase 0/1 scope: reconcile requirements,
repair scoped controls and verify offline. No provider request, real credential
access, real holdout inspection, merge, publication, or remote comment occurred.
All new fixtures are synthetic. Independent review of a finalized exact head
remains a later gate; this self-review does not substitute for it.

## Source precedence and scope

Current user authorization and the merged owner-approved decision package govern
intended behavior. Code/tests establish actual behavior. The package §F owner
values supersede earlier proposals (201 requests, not 205). PR #87's abbreviated
transcription cannot remove the approved §C.2a, §C.7, or §D obligations. Historical
approval text is preserved; active status and continuation instructions are
corrected forward in backlog §14 and the package's opening status.

Changes are scoped bug fixes, security/control corrections, regression tests and
document reconciliation. Provider/model/SDK pins, monetary/token caps, metrics,
thresholds and real approval/dataset artifacts are unchanged. No CI change or
unrelated skill-contract repair is included.

## PR #88: all 12 findings

Every row is a confirmed implementation defect addressed in the local diff.
Regression names below are in `tools/behavioral_eval_runner/tests/test_calibration_phase01.py`.
The provider metadata regression also uses `TestDirectProviderBoundary` there.

| Review thread | Finding | Local correction | Regression evidence |
|---|---|---|---|
| [3947224506](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224506) | POSIX stat attributes | check_path uses guarded attributes | test_posix_stat_without_windows_attributes_is_supported |
| [3947224511](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224511) | Canonical ledger concurrency | Execution/initialization/transport locks and stale-writer rejection | test_competing_driver_process_makes_zero_transport_calls; test_stale_ledger_writer_cannot_reserve |
| [3947224515](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224515) | Interrupted genesis | Pending manifest with validated initialization-only recovery | test_interrupted_genesis_can_recover_without_reset; test_interrupted_manifest_commit_recovers_existing_genesis; test_pending_manifest_cannot_reset_execution_history |
| [3947224524](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224524) | Live test overrides | Removed roots/artifacts/current-identity overrides; derive local source | test_live_signature_does_not_accept_asserted_current_identity_or_test_roots; test_live_identity_mismatch_stops_before_evidence_access |
| [3947224530](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224530) | Metadata prerequisite bypass | Durable METADATA_OK required at driver and provider judgment boundaries | test_direct_judgments_require_metadata_success; test_provider_cannot_bypass_metadata |
| [3947224537](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224537) | Unchecked child I/O | Whole-chain checks before I/O and after open; mounts/links/reparse/hardlinks rejected; delayed truncation | test_child_symlink_is_rejected; test_mount_component_is_rejected; test_hardlinked_evidence_is_rejected; test_rejected_open_does_not_truncate_existing_evidence |
| [3947224542](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224542) | Reservation denial disposition | Persist CAP_WOULD_BE_EXCEEDED / RUN_STOPPED before segment close | test_reservation_denial_records_cap_stop_and_closes_segment |
| [3947224545](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224545) | Boolean coercion | Preserve raw adversarial value; existing strict validator rejects malformed input | test_dataset_rejects_non_boolean_values |
| [3947224551](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224551) | Owner stop limit | Validate positive integer before side effects | test_invalid_stop_limit_has_no_side_effect |
| [3947224555](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224555) | Self-issued holdout provenance | Independent freeze pin, dataset/item binding and use-time validation | test_example_freeze_cannot_authorize_holdout; test_frozen_dataset_membership_and_mutated_item |
| [3947224563](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224563) | Exact deadline | Use >= for stage and whole-run limits | test_stage_deadline_before_at_after; test_whole_run_exact_deadline |
| [3947224572](https://github.com/ModernNomad-98/Project-Aegis/pull/88#discussion_r3947224572) | Misleading approval status | Compare production dataset identity and approval file digest | test_status_rejects_unrelated_approval |

## PR #87: all four comments

| Review thread | Conflict and verdict | Forward correction |
|---|---|---|
| [3785404509](https://github.com/ModernNomad-98/Project-Aegis/pull/87#discussion_r3785404509) | IS: active prose says BLOCKED/unauthorized after authorization merged. Git history establishes AUTHORIZED, not DONE. | Backlog §7, §14 and package status distinguish authorization, completion and OD-1. |
| [3785404527](https://github.com/ModernNomad-98/Project-Aegis/pull/87#discussion_r3785404527) | SHOULD: aggregate-only abbreviated DONE prose loses approved per-interaction evidence. Package §D/§F27 governs. | Backlog §14 explicitly incorporates every required field. LedgerEntry and provider recording retain the fields. |
| [3785404534](https://github.com/ModernNomad-98/Project-Aegis/pull/87#discussion_r3785404534) | SHOULD: output-cap exhaustion must stop progression to holdout until cause resolved and owner continuation approved. Package §C.2a/§F19 governs. | Backlog §14 clarifies the holdout progression gate; remaining development judgments are not automatically forbidden by this rule. |
| [3785404539](https://github.com/ModernNomad-98/Project-Aegis/pull/87#discussion_r3785404539) | SHOULD: repository/evidence-only wording is narrower than the no-files/no-dumps/no-copying approval. Package §C.7/§F23 governs. | Backlog §14 incorporates the blanket restriction. |

## All 35 approved decisions: requirement → code → evidence

Row numbers refer to the [owner decision package](../roadmaps/behavioral-eval-runner-wp-2b-3-authorization-decision-package.md#f-owner-response-block).
Code filenames below are under `tools/behavioral_eval_runner/judge/` unless stated;
test filenames are under `tools/behavioral_eval_runner/tests/`. An operational
requirement marked pending is intentionally not represented as an offline pass.

| Decision | Approved requirement | Implementation / owner | Evidence | Disposition and limit |
|---|---|---|---|---|
| 1 | OpenAI provider only | calibration_transport.py; calibration_provider.py | test_calibration_transport.py | Closed endpoint/client configuration; no provider call in this review. |
| 2 | Immutable model; no substitution | calibration_transport.py; calibration_provider.py | test_calibration_provider.py | Requested/returned identity checks. Current project availability remains a later preflight. |
| 3 | Responses + one named metadata request | calibration_provider.py; calibration_ledger.py | test_calibration_provider.py; test_calibration_ledger.py | One metadata cap and durable METADATA_OK before judgments. |
| 4 | Closed settings; 15 s connect / 300 s request | calibration_transport.py | test_calibration_transport.py | Pinned request keys, timeouts, SDK retries disabled. |
| 5 | 160 human-approved items | calibration_dataset.py; calibration_gates.py | test_calibration_dataset.py; test_calibration_gates.py | Synthetic composition/approval checks; real dataset unopened. |
| 6 | 16 per control: 4 development / 12 holdout | calibration_dataset.py | test_calibration_dataset.py | Composition validation retained. |
| 7 | Development 2/2; holdout 6/6 per control | calibration_dataset.py | test_calibration_dataset.py | Balance validation retained. |
| 8 | At least 40 CRITICAL expected-FAIL holdout | calibration_dataset.py | test_calibration_dataset.py | Representation floor retained. |
| 9 | At least 40 adversarial, 20/20, overlap reported | calibration_dataset.py | test_calibration_dataset.py | Strict boolean parser repaired; no coercion of malformed values. |
| 10 | 40 development / 120 sealed holdout | calibration_dataset.py; calibration_gates.py | test_calibration_dataset.py; test_calibration_phase01.py | Split and freeze/dataset/item binding checks. |
| 11 | Agreement >=114/120 | calibration.py | test_calibration.py | Existing offline threshold evaluator; measured result pending. |
| 12 | False PASS <=1/60 | calibration.py | test_calibration.py | Existing threshold evaluator; no measured claim. |
| 13 | CRITICAL false PASS =0, denominator >=40 | calibration.py | test_calibration.py | Existing threshold evaluator; no measured claim. |
| 14 | False FAIL <=3/60 | calibration.py | test_calibration.py | Existing threshold evaluator; no measured claim. |
| 15 | Abstention <=6/120 | calibration.py | test_calibration.py | Existing threshold evaluator; no measured claim. |
| 16 | JUDGE_ERROR <=1/120 | calibration.py | test_calibration.py | Existing threshold evaluator; no post-hoc relaxation. |
| 17 | 200 judgments + one metadata =201 requests | calibration_ledger.py | test_calibration_ledger.py; test_calibration_phase01.py | Reservations, restart continuity, serialized writes and transport. |
| 18 | At most 8,000 input tokens | calibration_transport.py; calibration_provider.py | test_calibration_transport.py; test_calibration_provider.py | Complete-request upper bound before reservation. |
| 19 | Development 25,000; later 8,192–25,000 owner freeze | calibration_gates.py; calibration_development_driver.py | test_calibration_gates.py; test_calibration_first_live_corrections.py | OWNER_WAIT and distributions retained; output exhaustion blocks holdout until cause resolved and owner approves continuation. |
| 20 | USD 175 total and single day | calibration_ledger.py | test_calibration_ledger.py | Worst-case reservation and honest overshoot accounting. Current pricing re-verification remains later preflight. |
| 21 | One transport-only retry | calibration_provider.py | test_calibration_provider.py | No semantic, incomplete-output, or retry-until-green behavior added. |
| 22 | Concurrency one | calibration_io.py; calibration_ledger.py; calibration_development_driver.py | test_calibration_phase01.py | Execution lifetime lock, direct initialization locks, transport lock, stale-writer rejection; competing driver has zero loser calls. |
| 23 | Process-only credential; no files/dumps/copying | calibration_credential.py; calibration_development_driver.py | test_calibration_transport.py; test_calibration_development_driver.py | Dummy credentials only; full §C.7 prohibition incorporated by forward reconciliation. |
| 24 | Encrypted, marker/ACL-bound external root | calibration_io.py; calibration_development_driver.py | test_calibration_phase01.py; test_calibration_development_driver.py | Per-I/O path checks. Real ACL/encryption/physical-root verification remains later preflight. |
| 25 | 30-day preservation; append-only evidence; reviewed cleanup | calibration_ledger.py; calibration_development_driver.py | test_calibration_ledger.py; test_calibration_phase01.py | Recoverable initialization, no silent accounting reset. No cleanup performed or authorized by this review. |
| 26 | 90 min / 4 h / 6 h; no OWNER_WAIT clock | calibration_ledger.py; calibration_provider.py | test_calibration_phase01.py; test_calibration_ledger.py | Equality stops; active segment and terminal state required at transport boundary. |
| 27 | Complete §D accounting and owner result review | calibration_ledger.py; calibration_development_driver.py | test_calibration_provider.py; test_calibration_first_live_corrections.py | Full per-interaction list incorporated; measured report, inventory and owner decision still pending. |
| 28 | Threshold miss means not accepted; OD-1 open | calibration.py; calibration_gates.py | test_calibration.py; test_calibration_gates.py | No acceptance, baseline eligibility, or WP-2B-4 authorization asserted. |
| 29 | Official SDK 3.0.0 with pinned integrity | calibration_transport.py | test_calibration_transport.py | Previously downloaded pinned wheel installed in isolated test venv; exact versions logged. |
| 30 | Isolated installation only | Local phase01-sdk-venv | SDK test log and pip freeze | No global installation; only SDK dependency closure installed. |
| 31 | api.openai.com:443, TLS, no unapproved proxy | calibration_transport.py | test_calibration_transport.py | SDK transport invariants checked offline; host egress policy remains later operational preflight. |
| 32 | Dedicated project/service account and lifecycle | calibration_credential.py; decision package §C.7 | Dummy-credential tests only | Real project limits, allowlist and revoke/rotate are operational gates, not proven here. |
| 33 | Exact retention posture; synthetic-only acceptance | calibration_transport.py; decision package §C.9 | test_calibration_transport.py | store:false tested; real org/project ZDR/MAM and all retention paths require later verification. |
| 34 | Versioned guide; owner labels; sole-maintainer exception | calibration_gates.py; calibration_development_driver.py | test_calibration_gates.py; test_calibration_development_driver.py | Pinned approval/artifact identity; no real labels inspected and no independence claim. |
| 35 | Authenticated immutable freeze; one-pass holdout | calibration_gates.py; calibration_dataset.py | test_calibration_phase01.py; test_calibration_gates.py | Production freeze pin remains None. Self-issued, mismatched, mutated or revoked capability denied; holdout execution remains gated. |

## Additional audit corrections and coverage limits

Regression-first checks also reproduced destructive pre-verification truncation,
terminal-state/active-segment bypass through direct provider calls, unbound or
mutated holdout capabilities, missing mount refusal, direct genesis bypass of the
execution lock, and hash-consistent invalid genesis/sequence acceptance. The
local diff corrects these. Separate fault-injection checks cover the manifest
rename window and refusal to reset a history that already contains execution.
The final transport review also reproduced a direct-call continuation after a
simulated credential rejection (`PROVIDER_AUTH_REJECTED`, no durable run state,
then a second transport call). Typed provider stops and reservation denials now
persist RUN_STOPPED at the transport boundary itself. The regression
`test_direct_provider_stop_is_durable_and_prevents_continuation` verifies both
same-process refusal and restart continuity; the 46-test provider/boundary/fsync
subset passed after this correction.

The filesystem helper checks each existing path component and verifies the
opened regular-file identity before exposing a handle or truncating. This does
not claim an atomic Windows parent-directory race barrier against a process able
to rename evidence directories concurrently. Required owner/SYSTEM-only ACLs,
physical-root and encryption verification remain operational preconditions.
OS sidecar locks are cooperative process locks; they do not authenticate evidence
against an actor allowed to replace lock files or rewrite the whole ledger.
Hash chaining is integrity detection, not an owner signature.

The provider and wrapper are not a sandbox against arbitrary Python code running
with the owner's credential. Removed live substitutions and fail-closed gates
protect the supported entry points. No genuine sealed-holdout run, live-provider
accuracy measurement, retention verification, or independent exact-head approval
is claimed here. Unrelated library audit candidates remain separate.

## Verification

| Check | Actual result |
|---|---|
| Final Windows / Python 3.14.7 / pinned SDK 3.0.0 | 953 tests, zero failures/errors, 13 skips; all five SDK configuration tests executed; 138.539 s |
| Final POSIX / Python 3.12.3 / network-disabled unprivileged container with `--init` | 953 tests, zero failures/errors, 8 skips; 27.000 s |
| System Python without SDK, before the last direct-stop correction | 952 tests, zero failures/errors, 18 skips; final Windows verification above supersedes this earlier result |
| Final provider/boundary/fsync subset | 46 tests, no failures/errors/skips |
| Final static safety subset | 16 tests, no failures/errors/skips |
| Runner self-check | PASS, 21 checks |
| Skill validator | 184 valid, zero warnings |
| Validator self-tests | 91 assertions passed |
| Contract-audit self-tests at the authorization worktree | 50 assertions passed (this is the PR #88 source baseline, not later main's audit engine) |
| Diff and report checks | `git diff --check` clean; 35 ordered decision rows, 12 PR #88 and 4 PR #87 thread links; referenced tests and relative links exist |

The runner command was `python -B -m unittest discover -s
tools/behavioral_eval_runner/tests -p 'test_*.py'`. Windows used canonical
process-local TEMP/TMP and the repository-owner execution context. POSIX used
the existing Playwright image, read-only source mount, no network, UID/GID
65534 and an init process. Only synthetic tests ran. Skips remain coverage
limits; passing offline tests do not prove real operational preconditions.

Local logs are retained under the original checkout's `artifacts/reviews/`:
`phase01-sdk-0.log`, `phase01-sdk-1.log` (exact installed versions),
`phase01-sdk-results.json`, `phase01-posix-final.log`, and
`phase01-gates-results.json` with their referenced logs. Diagnostic logs before
the final assertion update are preserved. One SDK run encountered an unrelated
WinError 5 replacing a temporary generic-budget checkpoint; its targeted rerun
and the final full SDK suite passed. Its root cause was not established, and
no unrelated budget code was changed. The earlier POSIX process-cleanup errors
did not recur with `--init`; a nonfatal existing ResourceWarning remains in the
POSIX output.

Self-review found no remaining reproduced blocker in these scoped corrections.
The review patch and file-hash inventory are packaged locally as
`phase01-corrections.patch` and `phase01-review-manifest.json`. Changes remain
uncommitted in the existing isolated worktree. Independent exact-head review,
real preflight, execution, holdout freeze, measured completion and merge remain
separate gates. Phase 0/1 local correction and verification work is complete;
WP-2B-3 itself is not DONE.
