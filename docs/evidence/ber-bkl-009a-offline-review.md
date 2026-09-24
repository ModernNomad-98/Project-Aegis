# Behavioral Eval Runner offline evidence-policy review

## Current reading — 2026-09-24

This note helps maintainers review what the bounded synthetic evidence-policy
proof checks and what it leaves open. Its premerge test and guard entries below
are dated preparation evidence. [Pull request (PR) #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
merged as `b4b1195d6162728ffc37d22d038a08e3722db7c0` after Linux and Windows
passed and the owner approved its one-time protected guard exception, now
consumed by [approval-register entry APR-015](../approvals/APPROVAL_REGISTER.md#aegis-apr-015-consumption-of-pr-139-exception).
The offline increment is delivered; Behavioral Eval Runner backlog item 009
(BER-BKL-009) still needs separately scoped
real-host access, encryption, privacy and operator cleanup controls.

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
for every caller artifact and the final report. Stage A is the hash-verified
input bundle; Stage B is the final report and verification bundle. The writer
rejects caller-supplied creation times, empty Stage A inputs,
unversioned access-policy references,
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
| Focused policy and evidence tests | 54 tests run, 52 passed, 2 expected platform skips; exit 0 after independent-audit corrections. |
| Skill validator | 185 skills valid, zero warnings. |
| Diff whitespace check | `git diff --check` passed locally. |
| Full offline Behavioral Eval Runner suite | Current correction: 1,024 tests run, 14 expected skips, exit 0 under repository-owner context. The sandbox-user run had 12 environment errors: Git rejected the worktree's owner identity and one synthetic process-tree kill lacked permission. |
| Independent architecture/security review | Astra re-audit found no remaining code blocker after the eight corrected findings, including both writer races. Root final review remains. |
| Exact-head Linux/Windows Actions | Pending on corrected PR #139 head. |

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

## Integration verification — 2026-09-24

Pull request (PR) #139 was updated locally with already-merged main revisions
`754fc7a02f85c1f05dc32b4bbd70c1b616979b50` (PR #208) and
`f1bfaece5b68551f75e910470becd17ed61ccb7e` (PR #209). The local integration
head is `9cd78be746f81803824bf642258664ba652c9a27`. Both merge commits carry
a Developer Certificate of Origin sign-off. Neither operation publishes the
branch or merges PR #139 into main.

The single conflict was in the backlog's work-package status paragraph. The
resolution retains main's explanation of the effective grant and pending
PR #139 guard decision, together with this implementation's dated checkpoint.
At that checkpoint, the complete `tools/behavioral_eval_runner/` subtree, including its tests and
README, was identical to reviewed implementation commit
`8928383f0838e2d99ee3a89c44b98b7aba7f1c9b`. The PR then changed only its
seven authorized paths and added 971 code/test lines, leaving 29 below the cap.

| Local command or check | Observed result |
| --- | --- |
| `python -B scripts/validate-skills.py` | 185 skills valid, zero warnings; exit 0 before and after the PR #209 integration. |
| `python -B scripts/tests/test_validator.py` | 91 gate self-test assertions passed; exit 0. |
| `python -B -m tools.behavioral_eval_runner self-check` | All 21 checks passed; live dispatch disabled; exit 0. |
| `python -B -m unittest tools.behavioral_eval_runner.tests.test_evidence_policy tools.behavioral_eval_runner.tests.test_evidence` | 52 tests run, two expected platform skips; exit 0. |
| `python -B -m unittest discover -s tools/behavioral_eval_runner/tests -p 'test_*.py'` | 1,022 tests run in 171.815 seconds, 14 expected skips; exit 0 under repository-owner context. |
| Conflict, scope and whitespace checks | No unresolved conflict; seven authorized PR paths; `git diff --check` passed. |
| Local file links in this record and the backlog | All 79 checked targets resolved. |

The test commands above ran on the resolved PR #208 working tree committed as
`27078574d90805b16dcf39b42a9af226eac3c28f`. PR #209 then brought in only
documentation changes; the unchanged runner subtree was verified again and
skill validation was repeated. This records the tested content precisely; it
does not claim a fresh full-suite run or hosted checks on the later commit.
Independent read-only review of the integrated head and this evidence update
found no blocker at that checkpoint: seven authorized paths, unchanged runner files, 971 added
code/test lines, 79 resolving local file links, and 185 valid skills with no
warnings. Exact-head Linux/Windows Actions remain a delivery gate. The
PR-specific protected-file disposition remains pending, and the earlier
real-host and policy limitations still apply.

This integration started at 2026-09-24 00:25:31 UTC. At the 00:33:07 UTC local
checkpoint, observed wall time was 7 minutes 36 seconds, including test and
Git waits. The previous and revised integration estimates are both 0.5–1
active hour; active-only time was not instrumented. The published selected
backlog estimate at start was 150–394 active hours. At the 00:36:44 UTC
post-review checkpoint, observed wall time was 11 minutes 13 seconds.
Publication and any eventual PR merge timing must be recorded separately.

## Path-identity correction — 2026-09-24

The later PR #139 review reproduced two policy defects. The receipt recorded
normalized artifact paths while Stage A and B passed original path spellings
to the writer; a backslash input could leave a claimed receipt and manifest
before failing verification. The policy also accepted case aliases of the
input manifest, final manifest and marker on case-sensitive hosts. The writer
now uses the validated normalized path in both stages and reserves those
control names by casefolded identity before the first write. Synthetic tests
cover both stages and prewrite rejection. These corrections do not change the
legacy manifest, report or marker schema.

On this corrected candidate, the focused command above ran **54 tests, 52
passed, 2 expected platform skips**. The complete offline runner suite ran
**1,024 tests, 1,010 passed, 14 expected skips** under repository-owner
context. Both exited zero. A sandbox-user full run reported 12 environment
errors from Git ownership and synthetic process-tree permissions; it is not
counted as passing. Two independent read-only Sol reviews accepted the code
and tests. The seven authorized PR paths remain unchanged; added code/test
lines total **993 of 1,000**, leaving 7. Exact-head hosted CI and the
PR-specific protected-file guard disposition remain pending.
