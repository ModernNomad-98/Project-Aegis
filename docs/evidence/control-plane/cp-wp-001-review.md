# CP-WP-001 — reconciliation and review evidence

Date: 2026-09-12. Owner: Peter Nguyen.
Repository: ModernNomad-98/Project-Aegis.
Base: `57e6928d2849aa5377daf52c723b85736292585d`.
Branch: `docs/cp-wp-001-durable-state-authority-recovery`.

Scope: [design proposal](../../design/resumable-control-plane-v1.md) and
[separate work-package register](../../roadmaps/resumable-control-plane-backlog.md).
This record is sanitized documentation evidence, not runtime recovery state,
permission configuration or a competing approval register.

## 1. Human authorization and limits

Source: Peter Nguyen's current-session written authorization, supplied as the
attachment beginning "Peter Nguyen authorizes Codex to execute CP-WP-001" on
2026-09-12. The direct human instruction remains source evidence before any
register transcription. The approval register is intentionally unchanged.

Verbatim bounded excerpts:

> Peter Nguyen authorizes Codex to execute CP-WP-001 — Durable State, Authority
> and Recovery Contract for the Project Aegis source repository.

> Exactly three created Markdown files

> Stop before merge.

The full instruction names exactly the design/backlog/evidence paths, the branch,
four active hours, 1,500 added lines, USD $0 task-controlled spend (existing session,
read-only agents and hosted CI excluded), DCO commits, normal push, one PR, terminal
CI monitoring and in-scope corrections. It forbids runtime/dependency/CI/BER changes,
credentials/holdouts/provider dispatch, database/deployment/release/tag/settings,
merge/auto-merge/force-push and changes to unrelated untracked files. These excerpts
and summary preserve the source's scope; they do not grant anything independently.

Continuation source: Peter's 2026-09-12 written attachment beginning "Continue the
already authorized CP-WP-001 work on PR #95." It requires correction of six inline
findings at `9e3db6193b47ec002f1087b21fe9a55708972544`, independent re-reviews,
same-branch DCO correction commits, normal push, six evidence-backed thread replies/
resolutions, fresh exact-head Codex review and all-check monitoring. It expressly
forbids merge, another branch/PR or expansion beyond the original three files/budgets.

## 2. Initial-delivery startup reconciliation

AGENTS.md and the complete owner register were reread. The four local Role A
landmarks were verified: README starts `# Project Aegis`, and catalog, validator
and audit-baseline files exist. Origin is the named GitHub repository.
Both AEGIS-APR-001 and AEGIS-APR-002 remain active with no later lifecycle events;
the direct task prohibits merge regardless of standing administrator-merge scope.

| Observation / command | Actual result |
| --- | --- |
| `git status --short --untracked-files=normal` | Exit 0; only `?? artifacts/recovery/` and `?? artifacts/reviews/` at startup |
| `git branch --show-current` | Exit 0; `main` before branch creation |
| `git rev-parse HEAD` and `git rev-parse origin/main` | Exit 0; both equal base above |
| `git remote -v` | Exit 0; origin fetch/push `https://github.com/ModernNomad-98/Project-Aegis.git` |
| `git fetch origin` | Exit 0; no base change |
| `git ls-remote origin refs/heads/main refs/heads/docs/cp-wp-001-durable-state-authority-recovery` | Exit 0; main equals base, target branch absent |
| Local and remote-tracking target branch listings | Exit 0; no matching branch |
| `git rev-list --left-right --count 57e6928d2849aa5377daf52c723b85736292585d...origin/main` | Exit 0; `0 0` |
| `git diff --stat` and `git diff --cached --stat` | Exit 0; empty before writing |
| `git switch -c docs/cp-wp-001-durable-state-authority-recovery 57e6928d2849aa5377daf52c723b85736292585d` | Exit 0; exact authorized branch created |
| `Test-Path .gitignore` | False; absence documented only |

No new-base reconciliation was needed. Existing untracked directories were
identified by status only; their contents were not read or changed.

## 3. Repository sources and claim boundaries

Sources inspected directly at this base: [AGENTS.md](../../../AGENTS.md),
[approval register](../../approvals/APPROVAL_REGISTER.md),
[BER backlog](../../roadmaps/behavioral-eval-runner-backlog.md),
[BER successor](../../design/behavioral-eval-runner-v1-fast-track-successor.md),
[BER README](../../../tools/behavioral_eval_runner/README.md),
[offline CI](../../offline-ci.md),
[workflow](../../../.github/workflows/validate-skills.yml),
[CODEOWNERS](../../../.github/CODEOWNERS) and the code/tests linked in design section 2.

Current notices and inspected implementation outrank historical "nothing built"
and pre-BER-DEC-008 status descriptions for IS questions; BER's current governing
documents retain their SHOULD authority. No measured calibration or live readiness
is inferred from offline engineering. No evidence places this stream in BER backlog.

Relevant code observations: `pathsafe.safe_join` performs lexical joining, not
its separate reparse checks; evidence final-report metadata pins BER policy and
30-day retention; budget append/checkpoint writes are separate; approval lifecycle
grader is not a consent authenticator; Windows evidence prevention and post-leader
cleanup remain limited. These are reuse boundaries, not fixes made by this package.

The three new docs fall outside the current protected-path regex but under global
CODEOWNERS. Existing CI has no PR path filter; all attached checks still require
terminal review. No live branch-protection settings were inferred from local files.

## 4. Historical initial-draft reviews

The findings/verdicts below describe the initial delivery at `9e3db61`. They do
not close the six later GitHub findings or validate the correction head. The prior
ready-for-owner-review handoff was superseded by the review in section 6.

Two independent read-only reviewers examined all three drafts and the current
authorization. The architecture/recovery reviewer applied architecture/review
guidance; the security/authority reviewer applied threat/approval guidance and
independently checked Role A and the full register. A separate read-only source
audit reverified the reuse matrix. No implementation or runtime tests were delegated.

| Finding / severity | Disposition and re-review evidence |
| --- | --- |
| A1 MAJOR — PAUSING omitted late execution/validator results | CLOSED: T10 accepts PAUSING receipts, T24 records validation observations, T07 settles with fence. Re-review required and verified that resume applies bound pass/fail through T11/T12; failure remains binding and cannot become retry-until-green. T25 now accepts PAUSING/STOPPED non-dispatch proof without reopening terminal work |
| A2 MAJOR — per-run lock insufficient for project effect/use deduplication | CLOSED: repository-scoped owner lock covers complete run catalog, all journals and effect/approval-use indexes; registration precedes intent; checkpoints carry all required histories; different-run contention tests specified |
| A3 MAJOR — routine retention could delete history needed for deduplication | CLOSED: authoritative catalog/journals/effect-use records excluded from routine cleanup pending a separately accepted compaction contract; disposable/raw artifacts retain review dates |
| S01 MEDIUM — own reservation versus exhausted one-use approval ambiguous | CLOSED: RESERVED/CONSUMED/RELEASED bound to grant/effect/intent; only owning intent recognizes reservation during fresh final check; uncertainty retained; definite non-dispatch releases only under original grant terms; T13/T25 and tests distinguish normal consumption from revocation |
| Security completeness suggestion — malformed approval history | INCLUDED: duplicate/malformed IDs, missing targets, cycles and conflicting lifecycle evidence deny affected authority |
| Source reconciliation — historical POSIX-CI comment | RESOLVED in these docs: current workflow runs Ubuntu and Windows BER checks; neither configuration nor an old comment establishes current platform guarantees |

Final architecture/recovery verdict: sound for documentation delivery; A1–A3 closed,
no outstanding findings. Final security/authority verdict: approve the documentation
contract; S01 closed, no blocking findings. Both explicitly exclude implementation,
merge or runtime-capability approval. Remaining platform/authentication/receipt
limitations are future entry gates, not accepted operational risk.

## 5. Historical initial-delivery validation

Results and content hashes in this section are historical, before the current
six-finding correction cycle; none is asserted as validation of the new head.

| Actual local command/check | Exit / result |
| --- | --- |
| `git diff --check` before staging | 0; no tracked whitespace errors; new-file content inspected separately because unstaged Git diff omits untracked files |
| `python -B -c "import importlib.util; print('yaml_available=' + str(importlib.util.find_spec('yaml') is not None))"` | 0; `yaml_available=True`; existing dependency used, nothing installed |
| `python -B scripts/validate-skills.py` | 0; `OK: 184 skill(s) valid, 0 warning(s)` |
| `python -B scripts/tests/test_validator.py` | 0; `OK: 91 gate self-test assertion(s) passed.`; synthetic temporary fixtures only |
| PowerShell literal here-string piped to `python -B -` (in-memory document audit) | 0; three UTF-8 files, 38 local links/anchors, 16 tables, 39 headings, T01–T25/C01–C07 presence, 862 lines before this evidence expansion; all within scope/budget |
| Complete source/Markdown structure inspection | All three documents read; balanced fences, table column counts and heading structure checked; no browser rendering claimed |
| Semantic coverage review | T04–T10/T14/T24 pause and late results; C01–C07 crash/ack boundaries; T12 failure; T13/T25 lifecycle/intent; T15 identity; T21 contention; T18–T20 stop; T22/T23 terminal restart; reviewer-confirmed consistency |
| `gh pr list --repo ModernNomad-98/Project-Aegis --head docs/cp-wp-001-durable-state-authority-recovery --state all --json number,title,state,url` | 0; empty list before PR creation, preventing a duplicate PR |

The in-memory document audit read only the three named files and their explicitly
linked local targets; it checked root-bounded existing targets and heading slugs,
balanced code fences, uniform table widths, required state/platform vocabulary,
all transition/crash IDs and the 1,500-line limit. Its script was passed on stdin,
not added to the repository. These checks do not claim runtime state-machine tests.

Reviewed design SHA-256:
`05f1892091c095a81816daae22003eab3fc293b8cf78351f46b92f8a908d11cb`.
Reviewed backlog SHA-256:
`6d70fe63374eb03d9f93bea03467ffe1bfdda523e8af73695aef5f6775e7c5ed`.
No self-hash of this evidence document is embedded.

Final staged/committed checks and the expanded evidence file receive a further
scope/link/structure check before delivery. Their actual exact-head whitespace,
name-status, line count, SHA/tree, PR URL and all terminal CI results are reported
in the PR body/final handoff, avoiding a self-referential commit claim. This file
does not assert that unexecuted postcommit or hosted checks have passed.

Local full BER and PowerShell platform suites were not rerun for a prose-only
change; the unchanged hosted CI supplies those regression jobs. No dependency
installation, browser renderer or new validator was added. Hosted capability skips
must be reported as observed; CI remains distinct from future controller evidence.

## 6. PR #95 six-finding correction cycle

Startup: `git fetch origin`, current branch/head/remote, tracked/staged diffs and
the complete GitHub PR/reviews/threads were read successfully. Branch remained
`docs/cp-wp-001-durable-state-authority-recovery`; local/live head was
`9e3db6193b47ec002f1087b21fe9a55708972544`, tree
`658932112682c9af53ff963cd404e50600f28f24`. Main remained the base above.
Tracked/staged changes were empty; status listed only the two preserved untracked
directories. Role A, AGENTS.md and complete approval lifecycle were reverified.
PR was open, unmerged, auto-merge disabled. All six threads were unresolved.

Source: [Codex review at 9e3db61](https://github.com/ModernNomad-98/Project-Aegis/pull/95#pullrequestreview-5185912683),
submitted 2026-09-12 08:43:54 UTC. GH1–GH6 below are local finding references,
not new issue IDs. Corrections are proposed contract requirements; their negative
cases are future tests, not claims that a controller or external guarantee exists.

| Finding / source | Corrected normative contract / negative acceptance | Disposition |
| --- | --- | --- |
| GH1 P1 [stable effect dedup](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687618) | Design CP-D08, 5.1, T03/T15/T16: key is repository UID + logical-effect ID only; immutable descriptor and durable equivalence/predecessor links; changed/repeated effect requires explicit bound new-ID approval; completed/unknown aliases cannot repeat. F01 tests revisions/runs and metadata/descriptor/new-ID bypasses | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH2 P1 [unknown-effect disposition](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687628) | CP-D04, 7.4, T17: proof-free owner choice only stops/final-fails/reports; nonexecution or reviewed safe same-key retry proof required for original-effect dispatch; compensation preserves predecessor and cannot bypass outstanding slot. F02 tests risk acceptance, new IDs, success and retry proof failures | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH3 P1 [atomic one-use authority](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687631) | CP-D09, 5.2, T03/T13/T25, C08: source-atomic claim/redemption binds exact intent/effect/expiry across all consumers; local reservation is accounting only; unsupported/ambiguous authority denies; synthetic capability cannot enable real adapter. F03 tests host/controller/manual races and missing/invalid/replayed claims | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH4 P2 [budget settlement](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687620) | CP-D10, 5.4, T10/T17–T20/T23/T25, C09: intent-owned RESERVED/CONSUMED/ADJUSTED/RELEASED/UNKNOWN_WORST_CASE_CHARGED lifecycle, atomic actual/worst-case settlement, true overrun plus fence, no uncertainty refund/reset. F04a/F04b cover every receipt/non-dispatch/cancellation/terminal/restart route and duplicate/negative accounting | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH5 P2 [checkpoint freshness](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687623) | CP-D07, 7.3, 8/8.1, T14, C07: source/export heads plus independently current monotonic anchor or complete authoritative source reconciliation; later facts/pending commits block stale import; no hash-chain/inactive-host shortcut. F05 restores older valid checkpoints after newer effects and grant consumption; absent/stale/contradictory proof denies | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH6 P2 [one outstanding operation](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687636) | CP-D02, 5.3, T03/T10–T12, C02/C09: repository-wide slot checked/acquired atomically with intent; independent of writer lock, lifecycle and item/run; closes only with proven obligations/validation disposition. F06 tests sequential same-owner/process attempts for every outstanding disposition and crash/restart | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |

All six also update the threat model (design 9), future tests (10/10.1), and backlog
acceptance/blocked later-package gates (2.2/5). Runtime verification is deferred.
Independent architecture/recovery and security/authority re-reviews each verified
all six contracts and their negative families. Final verdicts: approve documentation
corrections, GH1–GH6 addressed, no blocking findings. This is substantive document
review closure only; actual GitHub thread resolution follows pushed-head replies.

| Correction-review finding | Verified disposition |
| --- | --- |
| R-A1 MAJOR, also confirmed by security: proven non-dispatch could free slot despite unknown claim/control bill; T25 known-billing precondition contradicted UNKNOWN branch | CLOSED after reread: 5.3 requires resolved source/control/budget obligations for BOTH release routes; T25 classifies known/unknown independently; F04a/F06 deny another item/run when no effect occurred but control billing is unknown |
| R-A2 MAJOR: safe-retry claim requirement preceded the new attempt's durable intent | CLOSED after reread: 7.4 verifies eligible authority/source and prior claim/billing disposition; new atomic claim/receipt/redemption occurs only after T03 intent; effect uncertainty does not waive budget uncertainty |
| R-A3 MAJOR: T23 existing-obligation precondition omitted contradictory bill after release closed the obligation | CLOSED after reread: T23 accepts recorded intent/effect/reservation identity including settled/RELEASED in any state, atomically adjusts true usage plus exception/fence, never advances lifecycle or reopens terminals; F04b covers it |

Final independently reviewed design working-copy SHA-256 (before line-ending normalization):
`d7da89e9768da018eb7cce6b810e0aac12bb73fc17826fb0796b4fd1651e07cf`.
The staged LF representation has identical text and SHA-256
`cc497561df7e7cfb646559628d1e8ea6eec935d1d6c0b09cf77afad4ea71c08c`;
the three working copies were normalized to LF before the final scope check.
Reviewed backlog SHA-256:
`6a098836169c9b58878349cefc619ed257921e8b6beb59110bb94ef850bcaaee`.
Primary review also preserved trustworthy-time/clock-rollback rules and verified
that contradictory post-release bills become true-usage adjustments, not discarded
observations. Reviewers performed no writes or runtime tests.

| Actual correction-cycle local validation | Exit / result |
| --- | --- |
| `git diff --check` | 0; no whitespace errors; Git's existing line-ending conversion warnings are not failures |
| `python -B scripts/validate-skills.py` | 0; 184 skills valid, zero warnings; existing dependencies only |
| `python -B scripts/tests/test_validator.py` | 0; 91 gate self-test assertions passed; synthetic temporary fixtures only |
| In-memory PowerShell here-string piped to `python -B -` | 0; three UTF-8 files, 39 local links/anchors, 22 tables, 46 headings; unique T01–T25/C01–C09 definitions and valid references, CP-D/F/budget vocabulary; 1,164 lines before this evidence expansion |
| Complete correction diff and resulting content inspection | 0 for Git diff retrieval; all hunks reviewed, then focused follow-up corrections re-reviewed; no browser-rendering claim |
| In-memory Git scope/branch/base/head/index audit | 0; exact branch/base/reviewed old head, only three authorized changed paths, staged index empty before explicit staging; status only enumerated the two preserved untracked directories |

The final expanded evidence receives the same structural/scope/line-budget checks
before commit. Staged/committed checks, thread replies/resolution, fresh exact-head
review, final SHA/tree and CI results are recorded in PR #95 and the handoff after
normal push. No self-referential commit or old-head CI claim is made here. Full local
BER/platform suites remain skipped for prose-only work; unchanged hosted CI supplies
regression evidence. F01–F06 are unexecuted future controller tests, not CI claims.

## 7. Intentional omissions and continuation

Only the three authorized Markdown files are created. No runtime implementation,
schema/policy execution, shared extraction, BER/CI/dependency change, credential or
sealed-holdout access, provider dispatch through repository code, deployment,
database action, release, tag or merge is performed. Existing artifacts/recovery/
and artifacts/reviews/ remain untouched and unstaged. Root .gitignore stays absent.

Controller tests and real platform/authority/receipt guarantees are future work,
not claimed by document checks or unchanged BER tests. Storage selection, real
approval authenticity/freshness, external idempotency/fencing, Windows prevention
and distributed ownership remain blocked implementation decisions.

The next owner decision is review and acceptance/merge disposition of the single
CP-WP-001 documentation PR. No later work package may start from that acceptance alone.
