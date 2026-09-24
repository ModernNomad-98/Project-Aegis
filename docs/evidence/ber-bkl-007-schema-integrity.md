# BER-BKL-007 schema integrity review record

**Reading key for maintainers and reviewers:** Behavioral Eval Runner (BER)
backlog item 007 (`BER-BKL-007`) covers final record schemas. Work package
2B-1A (WP-2B-1A) was its bounded implementation; `BER-DEC` identifies the
runner decision entry that authorized it. A command-line interface (CLI)
exposes commands, and continuous integration (CI) runs automated checks.
JavaScript Object Notation (JSON) and YAML are data formats; YAML expands to
“YAML Ain't Markup Language.” The conditional DONE statement below was true
before pull request #104 merged; the dated current-reading banner gives its
later delivery status.

> **Current reading, checked 2026-09-23:** The conditional DONE wording below
> was recorded before pull request (PR) #104 merged. BER-BKL-007 (the Behavioral
> Eval Runner schema-integrity backlog item) is now **DONE** for its scoped
> offline delivery; the [BER backlog](../roadmaps/behavioral-eval-runner-backlog.md#ber-bkl-007--final-production-jsonyaml-schemas-and-schema-migration-policy)
> holds the current disposition. This evidence records the historical test
> revisions and skips, not live calibration or provider readiness. Start at the
> [evidence index](README.md) for related records.

Status: OWNER_ACCEPTED; DONE when PR #104 merges. Governing package: WP-2B-1A / BER-DEC-009,
effective after governance [PR #103](https://github.com/ModernNomad-98/Project-Aegis/pull/103)
merged at `f82a4bce770c173df6d4ddc6b920a7b35a6a63e7`.

## Scope and observed behavior

The WP-2B-1 external record loaders now reject missing and unsupported
`schema_version` values while internal constructors retain their creation
defaults. This covers attempt, aggregate, case-manifest and execution-profile
loads, including CLI record validation. Evidence verification checks the
stage-A and stage-B manifests, detached marker, final report and the report's
nested attempt/aggregate records before accepting hash-bound evidence. The
materialization verifier checks the expected record's supported version; the
budget-ledger replay checks the independent checkpoint's version. Regressions
forge self-consistent hashes and identities to prove a hash match alone cannot
make an unknown schema interpretable.

The [compatibility policy](../behavioral-eval-runner-schema-compatibility.md)
defines version dispatch, change review, older-evidence reading and a separate
reviewed conversion with original bytes and hashes preserved. It does not
change the pinned WP-2B-2 or WP-2B-3 version families.

## Verification checkpoints

| Check | Result |
| --- | --- |
| New regressions before implementation | 12 expected failures at missing/unknown version boundaries |
| Focused changed-behavior suite after correction | 76 tests, passed; 2 platform skips |
| First full BER suite in restricted sandbox | 994 tests; 12 environment errors: nested Git ownership and synthetic child termination |
| Full BER suite with command-scoped Git trust, outside sandbox | 995 tests, passed; 14 platform/capability skips, before final checkpoint/nested-record additions |
| Final full BER suite with command-scoped Git trust | 997 tests, passed; 14 platform/capability skips |
| Structural validator and BER self-check | Both passed; 184 skills, 0 warnings; 21 BER self-checks passed |
| Control-plane suite (unchanged package) | 543 tests, passed |
| Independent read-only audit | Found checkpoint and nested-report gaps; fixes reviewed, no remaining blocker |
| Local Windows PowerShell Desktop acceptance | 113 checks, passed |
| PowerShell Core acceptance | Unrun locally: `pwsh` is not installed; hosted Windows CI executes it |
| GitHub Actions on PR #104 at `7a804aa` | Linux passed (1m23s); Windows passed (2m52s); `gate-guard` failed (5s) only on protected BER paths, as its log states |
| Reconciled-main local BER suite | 997 tests passed, 14 expected skips, with checkout-scoped Git trust and the same execution mode used for the earlier process-control fixture; BER code unchanged from the audited head |

The first full-suite errors did not establish a BER code failure. The rerun
used process-local `GIT_CONFIG_COUNT` / `GIT_CONFIG_KEY_0=safe.directory` /
`GIT_CONFIG_VALUE_0` to trust only this checkout for child Git calls; no
global or repository Git configuration changed.

## Review decisions and limits

The current run schema treats `baseline_identity`, `execution_profile` and
`materialization` as free-form report objects and makes the coverage-metrics
version field optional. Requiring new nested versions there could reject
previously schema-valid `1.0.0-wp2b1` evidence. Their future shape is a
separate reviewed version decision. Budget ledger event lines are an
unversioned historical format; this package validates the versioned checkpoint
without changing the event stream.

Peter Nguyen accepted the recommendation to approve PR #104's tested final
schema shapes and merge it on 2026-09-23. BER-BKL-007 becomes DONE on that
merge, not merely because tests pass. No provider/model dispatch, measured
calibration, live execution, historical evidence rewrite, dependency install
or guard change occurred in this package. Model token and credit usage are
unknown because the runtime did not expose them.

Peter Nguyen answered "Permit this narrow exception" for PR #104's documented
guard failure on 2026-09-23 (AEGIS-APR-005). The final candidate must still
have green Linux/Windows execution and test jobs and no audit blocker. This
was separate from final schema-shape acceptance, which the owner subsequently
provided on 2026-09-23.
