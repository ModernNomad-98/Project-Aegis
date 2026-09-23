# Behavioral Eval Runner offline evidence-policy review

Here, BER-BKL-009A means Behavioral Eval Runner backlog item 009, offline
increment A; WP-2B-1B is its bounded work package; APR-012 and BER-DEC-011
are the matching owner approval and runner decision records.

Prepared 2026-09-23 for work package WP-2B-1B under the merged
[APR-012 grant](../approvals/APPROVAL_REGISTER.md) and
[BER-DEC-011 decision](../roadmaps/behavioral-eval-runner-backlog.md).
Implementation branch: `feat/ber-bkl-009a-offline-policy`, based directly on
grant merge `7e8f0c1067ee0a2e963520bf735a4b7b907a991f`. Record the eventual
reviewed implementation head and hosted checks in the PR; this local record
does not claim a merged implementation.

## What the synthetic proof checks

The opt-in writer requires an explicit, content-bound classification decision
for every caller artifact and the final report. It rejects caller-supplied
creation times, empty Stage A inputs, unversioned access-policy references,
mixed retention and missing citations. The first Coordinated Universal Time
(UTC) value is minted by the writer before its first policy artifact write.
A Stage A receipt and Stage B receipt are ordinary hash-listed artifacts.
Each is created with an exclusive file claim and verified without replacing
its bytes. The final manifest binds the Stage B receipt, and the detached
marker binds that final manifest and report.
The verifier checks those links and a single complete-bundle review date:
first writer event plus 30 consecutive 24-hour periods. The marker remains
outside its manifest. Expiry causes a fail-closed review signal, never
automatic deletion; failed and incomplete files remain available.
Stage A refuses any preexisting root content before writing. Stage B checks
filesystem path aliases and preexisting targets before writing. The policy
verifier compares each separately read manifest, receipt, report and marker
snapshot to the hashes established by the base verifier, and checks the
writer/verifier clock order. A failed or interrupted claim remains in place;
another writer cannot reset the first clock or replace the final stage.

This new policy date is **distinct from** existing `expiration_at` fields,
which retain their per-artifact meaning and byte shape. The policy does not
change the published `1.0.0-wp2b1` manifest, report or marker fields. Golden
hashes in `test_evidence.py` were captured by running the same fixed synthetic
fixture against the exact pre-policy grant-base `evidence.py` object
`bfb35cd1aee6cddd239c32377c8388871a0d6633`.

## Local verification

| Check | Observed result |
| --- | --- |
| Focused policy and evidence tests | 52 tests passed, 2 expected platform skips; exit 0 after independent-audit corrections. |
| Skill validator | 185 skills valid, zero warnings. |
| Diff whitespace check | `git diff --check` passed locally. |
| Full offline Behavioral Eval Runner suite | Corrected candidate: 1,022 tests passed, 14 expected skips, exit 0 under repository-owner context. The earlier sandbox-user run had 12 environment errors: Git rejected the worktree's owner identity and one synthetic process-tree kill lacked permission. |
| Independent architecture/security review | Astra re-audit found no remaining code blocker after the eight corrected findings, including both writer races. Root final review remains. |
| Exact-head Linux/Windows Actions | Pending implementation PR. |

Negative fixtures cover receipt-only Stage A, final-report omission, matched
invalid metadata enums, repeated writer reset and interleaved Stage A/B writers,
Windows case-alias overwrite,
receipt/report swaps across verification reads, writer/verifier chronology,
missing or rehashed first time, noncanonical and altered policy bytes,
omitted classification decisions, mixed retention, unbound or missing marker,
substituted run, expired or incomplete bundle, timezone normalization and a
month boundary. The tests use synthetic content and owned temporary
directories only.

## Remaining gates and limits

This is an offline internal-consistency proof, not independent attestation of
an operating-system clock against an actor able to rewrite every bundle file.
On capable Portable Operating System Interface (POSIX) hosts the claim uses
retained no-follow directory handles; on Windows its reparse checks detect
existing unsafe paths but cannot prevent
a mid-operation ancestor swap. No selected-host guarantee is claimed.
A citable decision reference and content hash do not prove the content was
actually redacted; publication still requires human privacy review. No real
host, an owner-plus-Windows-SYSTEM-service-account access-control list, disk encryption, recovery-key
custody, private input, provider use, live driver wiring or marker-gated
operator cleanup is implemented or claimed. BER-BKL-009 remains PARTIALLY
DELIVERED. Any requirement to reinterpret a published `expiration_at` field
or add a deadline field to the marker requires a separate versioned schema
decision and stops this increment.

The previous full evidence-policy implementation estimate was 8–16 active
hours. This bounded increment was estimated at 4–8 active hours, capped at
8. The selected backlog total at start was 175–394 active hours. Active-only
time was not instrumented. The first new implementation file was created at
2026-09-23 17:41:37 UTC; the work-start instant before that was not captured.
At the 18:13:55 UTC local completion checkpoint, observed wall time since
that file creation was 32 minutes 18 seconds, including test waits. Added
code/test lines total 971, below the 1,000-line grant cap.
