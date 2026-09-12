# PR #88 engineering closeout — 2026-09-12

This record continues the [Phase 0/1 review](../behavioral-eval-runner-phase01-review.md).
The owner authorized implementation, offline tests, commits, pushes and normal
merges, with PR #88 first, shared skill contracts second and permanent offline
Actions coverage afterward. The [audited execution plan](preflight/final-plan.md)
preserves the original estimates, independent scrutiny, scope and merge dependency.
Its pre-implementation status statements are historical, not current instructions.

## Changes and regression evidence

The twelve PR review findings are mapped to their fixes and named regressions in
the Phase 0/1 record. The closeout integrates that correction history and current
main (`000352f55b71f0c3e897a482d279d34bfaa3d66b`) through signed merge
`c7a92d208a8aec7295afa3e3188dce03a8331d0b`. PR #89's audit engine and tests are
retained; AEGIS-060 remains a retired false positive.

New evidence during this closeout justified three additions:

- Windows test fixtures now canonicalize paths when building records or using
  the guarded junction fallback. Production path verification and its character
  allowlist are unchanged. A real 8.3 destination is materialized and verified
  through both its short and canonical spellings.
- That round-trip test exposed an inherited materializer defect: an empty
  fixture or control plane had a manifest but no directory, so verification
  rejected a successfully returned record. Empty areas are now created through
  the trusted destination boundary after guarded file writes establish the root.
  Tests cover empty fixtures/control planes, a removed empty directory, a POSIX
  directory swap, and Windows creation at an absent destination. The independent
  review caught the absent-parent edge case in the first fix; its new regression
  failed before the ordering correction and then passed.
- Calibration status tests independently vary all five dataset identity fields
  and the approval-file digest. A matching synthetic pin reports APPROVED; each
  mismatched binding reports PENDING with no calls or dispatch permission.

The README now distinguishes the offline generic runner from the gated dedicated
calibration driver, and historical approval from current input availability.
No production dataset, approval, provider/model/SDK pin, cap, threshold, workflow
or shared skill contract is changed by these closeout additions.

## Preflight evidence and interpretation

The `preflight/` directory preserves the plan, commands, result metadata, logs,
fresh contract audit and initial failing runs. Original absolute paths in those
records identify the execution context; matching filenames are preserved here.
PowerShell-captured logs are normalized to UTF-8 without trailing layout spaces
for GitHub review; their test output and failure details are retained.
The helpers record the original commands and are historical reproductions, not
an unattended live-execution entry point.

The initial Windows suite had 21 failures/errors; all 21 reproduced on unchanged
main under the same sandbox. The same cases passed as the checkout owner with
canonical TEMP/TMP. This separated Git ownership and restricted process-control
behavior from two inherited fixture assumptions. Both assumptions were fixed
with short-path coverage. Initial failed logs remain evidence; a later pass does
not erase them or establish that restricted-sandbox termination works.

The first closeout pre-commit self-check rejected the new test's `ctypes`
import under the existing static-safety policy. The test now obtains the short
path through a fixed read-only Windows command with no caller-path interpolation.
The alias regression and six static-safety tests then passed, and all 21 runner
self-checks passed. No safety allowlist was widened. The original failed
pre-commit result is retained separately from final candidate verification.

The original POSIX run was at `a231bc5`, with Python 3.12.3 and a network-disabled,
unprivileged container. It is preflight evidence, not verification of this final
candidate. Final verification records must identify their actual commit/tree,
commands, environment, skips and any remaining limitations.

## Completion boundary

[Candidate verification](verification.md) records the completed full platform
suites, gates and [independent reviews](reviews.md). The PR body records the
submitted head's checks and GitHub disposition before closeout is declared
complete. The existing workflow checks
validator self-tests, skill validation and DCO; it does not run BER or contract
audit tests. Those suites require the separate recorded local verification until
the later reviewed CI change is merged.

GitHub currently requires one approving review for a normal merge. Read-only
Aegis reviews provide engineering evidence and do not impersonate that approval.
No administrator bypass or branch-protection change is authorized by this record.

All work here is offline with synthetic test inputs: zero provider requests,
zero real credentials, zero measured calibration results. Original approved
dataset/guide/approval bytes remain unavailable, and the
[replacement preparation plan](../ber-recovery-2026-09-11/replacement-plan.md)
remains open. WP-2B-3 is unfinished, OD-1 is open and WP-2B-4 remains blocked.
Windows filesystem checks retain their documented detection-only race limitation;
offline tests do not establish live operational prerequisites.
