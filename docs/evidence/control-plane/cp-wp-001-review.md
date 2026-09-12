# CP-WP-001 — reconciliation and review evidence

Date: 2026-09-12. Owner: Peter Nguyen. Repository: ModernNomad-98/Project-Aegis. Base: `57e6928d2849aa5377daf52c723b85736292585d`. Branch:
`docs/cp-wp-001-durable-state-authority-recovery`.

Scope: [design proposal](../../design/resumable-control-plane-v1.md) and [separate work-package register](../../roadmaps/resumable-control-plane-backlog.md). This record is
sanitized documentation evidence, not runtime recovery state, permission configuration or a competing approval register.

## 1. Original authorization and limits (later continuation in section 9)

Source: Peter Nguyen's original written authorization, supplied as the attachment beginning "Peter Nguyen authorizes Codex to execute CP-WP-001" on 2026-09-12. The direct human
instruction remains source evidence before any register transcription. The approval register is intentionally unchanged.

Verbatim bounded excerpts:

> Peter Nguyen authorizes Codex to execute CP-WP-001 — Durable State, Authority
> and Recovery Contract for the Project Aegis source repository.

> Exactly three created Markdown files

> Stop before merge.

The full instruction names exactly the design/backlog/evidence paths, the branch, four active hours, 1,500 added lines, USD $0 task-controlled spend (existing session, read-only
agents and hosted CI excluded), DCO commits, normal push, one PR, terminal CI monitoring and in-scope corrections. It forbids runtime/dependency/CI/BER changes,
credentials/holdouts/provider dispatch, database/deployment/release/tag/settings, merge/auto-merge/force-push and changes to unrelated untracked files. These excerpts and summary
preserve the source's scope; they do not grant anything independently.

Continuation source: Peter's 2026-09-12 written attachment beginning "Continue the already authorized CP-WP-001 work on PR #95." It requires correction of six inline findings at
`9e3db6193b47ec002f1087b21fe9a55708972544`, independent re-reviews, same-branch DCO correction commits, normal push, six evidence-backed thread replies/ resolutions, fresh
exact-head Codex review and all-check monitoring. It expressly forbids merge, another branch/PR or expansion beyond the original three files/budgets.

## 2. Initial-delivery startup reconciliation

AGENTS.md and the complete owner register were reread. The four local Role A landmarks were verified: README starts `# Project Aegis`, and catalog, validator and audit-baseline
files exist. Origin is the named GitHub repository. Both AEGIS-APR-001 and AEGIS-APR-002 remain active with no later lifecycle events; the direct task prohibits merge regardless of
standing administrator-merge scope.

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

No new-base reconciliation was needed. Existing untracked directories were identified by status only; their contents were not read or changed.

## 3. Repository sources and claim boundaries

Sources inspected directly at this base: [AGENTS.md](../../../AGENTS.md), [approval register](../../approvals/APPROVAL_REGISTER.md), [BER
backlog](../../roadmaps/behavioral-eval-runner-backlog.md), [BER successor](../../design/behavioral-eval-runner-v1-fast-track-successor.md), [BER
README](../../../tools/behavioral_eval_runner/README.md), [offline CI](../../offline-ci.md), [workflow](../../../.github/workflows/validate-skills.yml),
[CODEOWNERS](../../../.github/CODEOWNERS) and the code/tests linked in design section 2.

Current notices and inspected implementation outrank historical "nothing built" and pre-BER-DEC-008 status descriptions for IS questions; BER's current governing documents retain
their SHOULD authority. No measured calibration or live readiness is inferred from offline engineering. No evidence places this stream in BER backlog.

Relevant code observations: `pathsafe.safe_join` performs lexical joining, not its separate reparse checks; evidence final-report metadata pins BER policy and 30-day retention;
budget append/checkpoint writes are separate; approval lifecycle grader is not a consent authenticator; Windows evidence prevention and post-leader cleanup remain limited. These
are reuse boundaries, not fixes made by this package.

The three new docs fall outside the current protected-path regex but under global CODEOWNERS. Existing CI has no PR path filter; all attached checks still require terminal review.
No live branch-protection settings were inferred from local files.

## 4. Historical initial-draft reviews

The findings/verdicts below describe the initial delivery at `9e3db61`. They do not close the six later GitHub findings or validate the correction head. The prior
ready-for-owner-review handoff was superseded by the review in section 6.

Two independent read-only reviewers examined all three drafts and the current authorization. The architecture/recovery reviewer applied architecture/review guidance; the
security/authority reviewer applied threat/approval guidance and independently checked Role A and the full register. A separate read-only source audit reverified the reuse matrix.
No implementation or runtime tests were delegated.

| Finding / severity | Disposition and re-review evidence |
| --- | --- |
| A1 MAJOR — PAUSING omitted late execution/validator results | CLOSED: T10 accepts PAUSING receipts, T24 records validation observations, T07 settles with fence. Re-review required and verified that resume applies bound pass/fail through T11/T12; failure remains binding and cannot become retry-until-green. T25 now accepts PAUSING/STOPPED non-dispatch proof without reopening terminal work |
| A2 MAJOR — per-run lock insufficient for project effect/use deduplication | CLOSED: repository-scoped owner lock covers complete run catalog, all journals and effect/approval-use indexes; registration precedes intent; checkpoints carry all required histories; different-run contention tests specified |
| A3 MAJOR — routine retention could delete history needed for deduplication | CLOSED: authoritative catalog/journals/effect-use records excluded from routine cleanup pending a separately accepted compaction contract; disposable/raw artifacts retain review dates |
| S01 MEDIUM — own reservation versus exhausted one-use approval ambiguous | CLOSED: RESERVED/CONSUMED/RELEASED bound to grant/effect/intent; only owning intent recognizes reservation during fresh final check; uncertainty retained; definite non-dispatch releases only under original grant terms; T13/T25 and tests distinguish normal consumption from revocation |
| Security completeness suggestion — malformed approval history | INCLUDED: duplicate/malformed IDs, missing targets, cycles and conflicting lifecycle evidence deny affected authority |
| Source reconciliation — historical POSIX-CI comment | RESOLVED in these docs: current workflow runs Ubuntu and Windows BER checks; neither configuration nor an old comment establishes current platform guarantees |

Final architecture/recovery verdict: sound for documentation delivery; A1–A3 closed, no outstanding findings. Final security/authority verdict: approve the documentation contract;
S01 closed, no blocking findings. Both explicitly exclude implementation, merge or runtime-capability approval. Remaining platform/authentication/receipt limitations are future
entry gates, not accepted operational risk.

## 5. Historical initial-delivery validation

Results and content hashes in this section are historical, before the current six-finding correction cycle; none is asserted as validation of the new head.

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

The in-memory document audit read only the three named files and their explicitly linked local targets; it checked root-bounded existing targets and heading slugs, balanced code
fences, uniform table widths, required state/platform vocabulary, all transition/crash IDs and the 1,500-line limit. Its script was passed on stdin, not added to the repository.
These checks do not claim runtime state-machine tests.

Reviewed design SHA-256: `05f1892091c095a81816daae22003eab3fc293b8cf78351f46b92f8a908d11cb`. Reviewed backlog SHA-256:
`6d70fe63374eb03d9f93bea03467ffe1bfdda523e8af73695aef5f6775e7c5ed`. No self-hash of this evidence document is embedded.

Final staged/committed checks and the expanded evidence file receive a further scope/link/structure check before delivery. Their actual exact-head whitespace, name-status, line
count, SHA/tree, PR URL and all terminal CI results are reported in the PR body/final handoff, avoiding a self-referential commit claim. This file does not assert that unexecuted
postcommit or hosted checks have passed.

Local full BER and PowerShell platform suites were not rerun for a prose-only change; the unchanged hosted CI supplies those regression jobs. No dependency installation, browser
renderer or new validator was added. Hosted capability skips must be reported as observed; CI remains distinct from future controller evidence.

## 6. First correction cycle — a0177d5

This cycle was delivered as `a0177d556f61b9849c596604bc71d068e9bc07c0` (tree `7cb53e770511f7d3c22e9a57948ffa22095e9bd3`), 1,197 total added lines. Its three CI jobs passed, and all
six original threads received evidence replies and were resolved. Its fresh Codex review subsequently found GH7–GH9 below; these prior results do not establish that the follow-up
correction head is ready.

Startup: `git fetch origin`, current branch/head/remote, tracked/staged diffs and the complete GitHub PR/reviews/threads were read successfully. Branch remained
`docs/cp-wp-001-durable-state-authority-recovery`; local/live head was `9e3db6193b47ec002f1087b21fe9a55708972544`, tree `658932112682c9af53ff963cd404e50600f28f24`. Main remained
the base above. Tracked/staged changes were empty; status listed only the two preserved untracked directories. Role A, AGENTS.md and complete approval lifecycle were reverified. PR
was open, unmerged, auto-merge disabled. All six threads were unresolved.

Source: [Codex review at 9e3db61](https://github.com/ModernNomad-98/Project-Aegis/pull/95#pullrequestreview-5185912683), submitted 2026-09-12 08:43:54 UTC. GH1–GH6 below are local
finding references, not new issue IDs. Corrections are proposed contract requirements; their negative cases are future tests, not claims that a controller or external guarantee
exists.

| Finding / source | Corrected normative contract / negative acceptance | Disposition |
| --- | --- | --- |
| GH1 P1 [stable effect dedup](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687618) | Design CP-D08, 5.1, T03/T15/T16: key is repository UID + logical-effect ID only; immutable descriptor and durable equivalence/predecessor links; changed/repeated effect requires explicit bound new-ID approval; completed/unknown aliases cannot repeat. F01 tests revisions/runs and metadata/descriptor/new-ID bypasses | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH2 P1 [unknown-effect disposition](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687628) | CP-D04, 7.4, T17: proof-free owner choice only stops/final-fails/reports; nonexecution or reviewed safe same-key retry proof required for original-effect dispatch; compensation preserves predecessor and cannot bypass outstanding slot. F02 tests risk acceptance, new IDs, success and retry proof failures | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH3 P1 [atomic one-use authority](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687631) | CP-D09, 5.2, T03/T13/T25, C08: source-atomic claim/redemption binds exact intent/effect/expiry across all consumers; local reservation is accounting only; unsupported/ambiguous authority denies; synthetic capability cannot enable real adapter. F03 tests host/controller/manual races and missing/invalid/replayed claims | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH4 P2 [budget settlement](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687620) | CP-D10, 5.4, T10/T17–T20/T23/T25, C09: intent-owned RESERVED/CONSUMED/ADJUSTED/RELEASED/UNKNOWN_WORST_CASE_CHARGED lifecycle, atomic actual/worst-case settlement, true overrun plus fence, no uncertainty refund/reset. F04a/F04b cover every receipt/non-dispatch/cancellation/terminal/restart route and duplicate/negative accounting | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH5 P2 [checkpoint freshness](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687623) | CP-D07, 7.3, 8/8.1, T14, C07: source/export heads plus independently current monotonic anchor or complete authoritative source reconciliation; later facts/pending commits block stale import; no hash-chain/inactive-host shortcut. F05 restores older valid checkpoints after newer effects and grant consumption; absent/stale/contradictory proof denies | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH6 P2 [one outstanding operation](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995687636) | CP-D02, 5.3, T03/T10–T12, C02/C09: repository-wide slot checked/acquired atomically with intent; independent of writer lock, lifecycle and item/run; closes only with proven obligations/validation disposition. F06 tests sequential same-owner/process attempts for every outstanding disposition and crash/restart | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |

All six also update the threat model (design 9), future tests (10/10.1), and backlog acceptance/blocked later-package gates (2.2/5). Runtime verification is deferred. Independent
architecture/recovery and security/authority re-reviews each verified all six contracts and their negative families. Final verdicts: approve documentation corrections, GH1–GH6
addressed, no blocking findings. This is substantive document review closure only; actual GitHub thread resolution follows pushed-head replies.

| Correction-review finding | Verified disposition |
| --- | --- |
| R-A1 MAJOR, also confirmed by security: proven non-dispatch could free slot despite unknown claim/control bill; T25 known-billing precondition contradicted UNKNOWN branch | CLOSED after reread: 5.3 requires resolved source/control/budget obligations for BOTH release routes; T25 classifies known/unknown independently; F04a/F06 deny another item/run when no effect occurred but control billing is unknown |
| R-A2 MAJOR: safe-retry claim requirement preceded the new attempt's durable intent | CLOSED after reread: 7.4 verifies eligible authority/source and prior claim/billing disposition; new atomic claim/receipt/redemption occurs only after T03 intent; effect uncertainty does not waive budget uncertainty |
| R-A3 MAJOR: T23 existing-obligation precondition omitted contradictory bill after release closed the obligation | CLOSED after reread: T23 accepts recorded intent/effect/reservation identity including settled/RELEASED in any state, atomically adjusts true usage plus exception/fence, never advances lifecycle or reopens terminals; F04b covers it |

Final independently reviewed design working-copy SHA-256 (before line-ending normalization): `d7da89e9768da018eb7cce6b810e0aac12bb73fc17826fb0796b4fd1651e07cf`. The staged LF
representation has identical text and SHA-256 `cc497561df7e7cfb646559628d1e8ea6eec935d1d6c0b09cf77afad4ea71c08c`; the three working copies were normalized to LF before the final
scope check. Reviewed backlog SHA-256: `6a098836169c9b58878349cefc619ed257921e8b6beb59110bb94ef850bcaaee`. Primary review also preserved trustworthy-time/clock-rollback rules and
verified that contradictory post-release bills become true-usage adjustments, not discarded observations. Reviewers performed no writes or runtime tests.

| Actual correction-cycle local validation | Exit / result |
| --- | --- |
| `git diff --check` | 0; no whitespace errors; Git's existing line-ending conversion warnings are not failures |
| `python -B scripts/validate-skills.py` | 0; 184 skills valid, zero warnings; existing dependencies only |
| `python -B scripts/tests/test_validator.py` | 0; 91 gate self-test assertions passed; synthetic temporary fixtures only |
| In-memory PowerShell here-string piped to `python -B -` | 0; three UTF-8 files, 39 local links/anchors, 22 tables, 46 headings; unique T01–T25/C01–C09 definitions and valid references, CP-D/F/budget vocabulary; 1,164 lines before this evidence expansion |
| Complete correction diff and resulting content inspection | 0 for Git diff retrieval; all hunks reviewed, then focused follow-up corrections re-reviewed; no browser-rendering claim |
| In-memory Git scope/branch/base/head/index audit | 0; exact branch/base/reviewed old head, only three authorized changed paths, staged index empty before explicit staging; status only enumerated the two preserved untracked directories |

The final expanded evidence receives the same structural/scope/line-budget checks before commit. Staged/committed checks, thread replies/resolution, fresh exact-head review, final
SHA/tree and CI results are recorded in PR #95 and the handoff after normal push. No self-referential commit or old-head CI claim is made here. Full local BER/platform suites
remain skipped for prose-only work; unchanged hosted CI supplies regression evidence. F01–F06 are unexecuted future controller tests, not CI claims.

## 7. Second correction cycle — late receipts and terminal validation

Delivered as `5acf7b64781b50fca1865d4a4ba4bd20c1004452`, tree `caca8a1aaa3f1bc4c0f3023bbced6a52ba54d57c`: 1,309 added lines, all three CI jobs passed, GH7–GH9 replied/resolved. Its
next review found GH10–GH17; these results are historical.

[Fresh Codex review](https://github.com/ModernNomad-98/Project-Aegis/pull/95#pullrequestreview-5185982724) at `a0177d5`, submitted 2026-09-12 09:17:05 UTC, produced two P2 findings
and one P1. The branch/head and clean tracked/staged state were checked before these corrections; the two untracked directories remained untouched. Same three-file/1,500-line
scope, normal DCO commit/push, independent review and no-merge boundary continue to apply.

| Finding / source | Corrected normative contract / negative acceptance | Disposition |
| --- | --- | --- |
| GH7 P2 [receipt with unresolved billing](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995758075) | T17 now retains the verified receipt with UNKNOWN settlement in RECONCILIATION_REQUIRED; only settled billing/source claims permit VALIDATING (PAUSED if fenced), agreeing with 7.4/T10. F07 covers unknown-to-settled progression and denial | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH8 P2 [late terminal receipt admission](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995758079) | T23 verifies receipt identity/integrity independently of known/unknown usage classification; missing telemetry allows atomic UNKNOWN_WORST_CASE_CHARGED while terminal state/slot/fence persist. Actual charges still require authoritative proof. F08 covers admission, invalid receipts and later settlement | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |
| GH9 P1 [terminal validation settlement](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995758081) | CP-D06, 5.3, T26/T27, crash/export/threat rules: explicit non-advancing terminal validation disposition; validator intent mandatory before launch; no-start requires complete history/fence or authoritative non-launch proof, never missing result. All source/effect/usage obligations still gate slot release. F09 covers both settlement orders, uncertainty, cancellation, replay and no terminal reopen | Verified by both independent re-reviews; GitHub closure requires pushed-head evidence |

Final independent architecture/recovery and security/authority verdicts: approve the documentation corrections; GH7–GH9 closed for document review, GH1–GH6 safeguards preserved, no
blocking finding. GitHub thread closure still requires pushed evidence.

| Follow-up review finding | Verified disposition |
| --- | --- |
| R-S2 P2 — late missing telemetry could downgrade already verified usage to a smaller W | CLOSED: 5.4/T23 retain authoritative usage by reference; only authoritative correction/refund reduces it; F08 includes known A greater than W followed by missing telemetry |
| R-A4 MAJOR — validator non-launch recovery could select PLANNED and retry the completed parent | CLOSED: T17/6.2/7.4 use activity kind and check cursor; settle only validator source/budget, restore VALIDATING/PAUSED, require fresh scoped T27 authority/budget; F09 forbids parent T03 retry |
| R-A5 MAJOR — T11 omitted remaining VALIDATING for another declared required check | CLOSED: T11 retains the same operation slot and VALIDATING while declared checks remain; next operation requires all current obligations settled; F09 covers multiple checks |

The reviewers required durable validator intent before launch for no-start proof. T27 supplies that contract; T11/T12/T24/T26 preserve its usage/source accounting and bound
pass/fail observations, including UNKNOWN and pre-launch-denial paths. Tests remain future acceptance cases; no controller validation was executed by reviewers. Final reviewed
design SHA-256: `b95277548239ead4d3c25bb839939e96f5995ec4d8ab0b67bf0e3f1788742a43`. Reviewed backlog SHA-256: `e8a6adec9d242c6c99cfd04f870c00d80aab7d25ff8b7bc194c81c81a8d52db7`.

Actual local checks this cycle, all exit 0: `git diff --check`; `python -B scripts/validate-skills.py` (184 valid, zero warnings); `python -B scripts/tests/test_validator.py` (91
assertions); and the in-memory Markdown/scope audit (39 local links/anchors, 25 tables, 47 headings, unique T01–T27/C01–C09 and valid references, 1,284 lines before this evidence
expansion). The complete diff was read, including follow-up corrections; expanded evidence and the staged/committed scope receive final checks. F01–F09 remain unexecuted future
tests. Thread replies/resolution, final head/tree, fresh review and CI are recorded in PR #95 and the handoff after push; a0177d5's passing CI is historical for this cycle.

## 8. Third correction cycle — complete validation lifecycle traces

Delivered as `d2bb7aca68942ce921518cdfc71199737eedaac8`, tree `25481c0d7837f05bc636cabe88db71a22b92c19c`: 1,425 added lines, all three CI jobs passed; GH10-GH17 replied/resolved.
Fresh review then found GH18-GH21; this cycle is historical.

[Codex review at 5acf7b6](https://github.com/ModernNomad-98/Project-Aegis/pull/95#pullrequestreview-5186022401), submitted 2026-09-12 09:36:11 UTC, identified eight further
transition gaps. Tracked/ staged state was clean before correction; branch, three-file scope and user-artifact boundaries remain unchanged. Passing prior CI is not closure of these
findings.

| Finding / source | Corrected normative rule / future negative trace | Disposition |
| --- | --- | --- |
| GH10 P1 [independent check settlement](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995800088) | T11 evaluates the selected check's application guards; aggregate gates only constrain operation advancement/completion. F10: reject zero checks; apply A while B is unstarted; final pass waits on a distinct idempotent T16 finalization | Closed in independent document review; pushed reply pending |
| GH11 P2 [initial unresolved claims](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995800092) | T10 requires settled usage AND source/control claims for VALIDATING; unknown retains receipt in reconciliation. F11 denies validator contact until claim settlement | Closed in independent document review; pushed reply pending |
| GH12 P2 [non-launch state consistency](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995800096) | T17/T25 validator non-launch consistently yields BLOCKED with VALIDATING cursor pending T16, or PAUSED/reconciliation according to fence/uncertainty. F12 rejects readiness/pause/accounting detours around T16 without parent retry | Closed in independent document review; pushed reply pending |
| GH13 P1 [nonterminal contradictory receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995800104) | T23 admits unexpected/contradictory receipts in any state before ordinary routing; retains evidence/usage and fences/reconciles nonterminal work while terminal stays fixed. F13 includes another slot owner, never evicted | Closed in independent document review; pushed reply pending |
| GH14 P1 [recoverable validation slot](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995800109) | 5.3/T12 retain the unresolved recoverable check and slot through typed T16 remediation and fresh T27 launch; F14 rejects different-item dispatch and stale-attempt substitution | Closed in independent document review; pushed reply pending |
| GH15 P2 [cancellation versus delayed result](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995800116) | T26 cancellation establishes cessation/closed waiting, not absence of a produced result. Universal T24 intake preserves later bound pass/fail and usage without replacing cancellation/reopening; F15 distinguishes real contradictory proof | Closed in independent document review; pushed reply pending |
| GH16 P1 [apply retained observation once](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995800126) | T24 intake and T11/T12 APPLY_VALIDATION are distinct commands/events; atomic operation/check/attempt/observation apply key prevents duplicate application regardless of command ID. C04/C05/F16 cover denied/retried intake, apply and distinct operation finalization | Closed in independent document review; pushed reply pending |
| GH17 P2 [validation launch prerequisites](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995800136) | T27 atomically checks the selected check's declared prerequisites/gates before launch, rechecks after intent/source claim; F17 rejects missing or changed prerequisites before validator contact | Closed in independent document review; pushed reply pending |

Independent architecture/recovery and security/authority reviewers both **approve the documentation contract**, with no blocking findings remaining in their adversarial traces.
They reviewed design SHA-256 `656739099d124d5697bae6c490c305026f301d9810a9f3bde90bd904a7bc80d4` and backlog SHA-256
`13b58c977f2b8b91438630a7e57e7bcf51de4e7c8d7b050ad562918df9f06b36`. Both explicitly retained GH1-GH9 protections and traced GH10-GH17, multiple checks, unknown usage,
failure/remediation, pause/non-launch, cancellation/late evidence and crash replay. These are manual document traces, not executed controller tests.

Additional independent findings were corrected and re-reviewed:

- Architecture MAJOR: paused non-launch could bypass required recovery. T14 now
  restores BLOCKED; T16 is required. Security P2 also traced T02 readiness and T17
  accounting detours: all preserve blockers, and T27 verifies bound recovery.
- Architecture MAJOR: final pass before aggregate readiness had no later completion
  route. T11 retains BLOCKED/FINALIZING and slot; distinct T16 finalization checks
  already-applied results/gates and commits its own idempotent key/slot/cursor.
- Architecture MAJOR: zero checks stranded VALIDATING. T01/5.1 reject an empty set
  before contact; F10 covers it. C05 now explicitly includes finalization replay.

Local commands exited 0: `git diff --check`, `python -B scripts/validate-skills.py` (184 valid, zero warnings), `python -B scripts/tests/test_validator.py` (91 assertions), and the
in-memory Markdown/link/transition audit. Final evidence, staged/committed scope, DCO and hashes receive final checks before push. Future F01-F17 are unexecuted; old-head CI cannot
close current findings. Final head/tree, individual pushed replies, fresh review and exact-head CI remain PR/handoff evidence after push.

## 9. Fourth correction cycle - fences, nonexecution and validator capability

[Codex review at d2bb7ac](https://github.com/ModernNomad-98/Project-Aegis/pull/95#pullrequestreview-5186097379) submitted 2026-09-12 10:03:12 UTC identified four P1 findings.
Tracked/staged state was clean before correction; same branch, three-file scope and artifact boundaries.

| Finding / source | Normative correction / future negative case | Disposition |
| --- | --- | --- |
| GH18 P1 [final failure](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995890252) | T12/T17 commit permanent item/operation fences; T12 closes its failed check and conditionally releases the slot; T26 closes remaining checks. F18 covers single/multiple checks and crash/replay | Closed in independent document review; Resolved with pushed 7988b89 evidence; PR replies retained |
| GH19 P1 [nonexecution after handoff](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995890256) | T25 accepts exact authoritative nonexecution proof before/after handoff, covering descendants/effect paths and independent control costs. F19 rejects error-only proof and unknown billing | Closed in independent document review; Resolved with pushed 7988b89 evidence; PR replies retained |
| GH20 P1 [validator mutation](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995890258) | 5.3/T27 bind read-only pinned inputs and bounded isolated output capability; enforced subprocess/tool/network containment, unsupported denies; target repair needs its own approved effect/slot. F20 covers escape/repair | Closed in independent document review; Resolved with pushed 7988b89 evidence; PR replies retained |
| GH21 P1 [uncertainty fence clearance](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3995890260) | 6.1/T17 bind each fence to scope/reason/originating event and clear only the exact uncertainty instance its authoritative settlement proves resolved. F21 retains other/newer/pause/authority/integrity/breach/recovery fences | Closed in independent document review; Resolved with pushed 7988b89 evidence; PR replies retained |

Historical independent architecture/recovery and security/authority reviewers approved design SHA-256 `f34ec3ca1ed1841fa2f2035e05a049de171f487273eb99861647362b2506068d`. Both then
independently approved final 7988b89 design SHA-256 `a5aeee023bd2ce4cb1da1d4a3256f49e904eeaf07c4297f45892128518c84491`; reverting only the two authority-wording changes in memory
reproduced f34ec3 exactly. The normative retry/receipt/T25 text was identical. This history does not approve later corrections. Follow-ups closed T17 terminal entry, the security
P2 safe-retry dead end, and original receipt arrival before/after retry intent. T03/7.4/F02/F21 bind one-attempt exceptions; T23/T25 retain pending validation. F18-F21 table
rendering was also corrected. Local checks exited 0: `git diff --check`, `python -B scripts/validate-skills.py` (184 valid, zero warnings), `python -B
scripts/tests/test_validator.py` (91 assertions), and in-memory Markdown/link/transition checks. F01-F21 remain unexecuted future tests. Automatic approval review rejected the
PR-description update twice, applying the earlier read-only instruction and declining later attachment-based authorization. 2026-09-13 / Peter Nguyen / ACTIVE: "yes approved for
commit, push and merged". Reason: resume CP-WP-001. Allowed: commit/push/merge PR #95; runtime/out-of-scope changes forbidden. Evidence: direct chat answering the three-document
publishing request; no expiry stated. This supersedes the earlier no-merge boundary; fresh review/CI remain required before merge.

## 10. Fifth correction cycle - complete intake and validation-only reuse

[Review at 7988b89](https://github.com/ModernNomad-98/Project-Aegis/pull/95#pullrequestreview-5186926878), submitted 2026-09-12 15:19:11 UTC, found three P1 and two P2 issues. That
head/tree `7988b89cbdb26b21d1d960769e04808864cb98d7` / `5b8cddec05434e905f58957265fc69164151c955` had 1,497 added lines; all three CI jobs passed and GH1-GH21 were resolved. These
results are historical. The same three-file/line/time limits and merge-after-gates authority remain. Historical evidence paragraphs were reflowed without deleting facts.

| Finding / source | Normative correction / future negative trace | Disposition |
| --- | --- | --- |
| GH22 P1 [T25 fences](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3996642800) | T25/6.2/F21 clear only exact proven-resolved uncertainty instances, after contradiction classification; independent/parent/newer fences survive | Closed in independent document review; pushed reply pending |
| GH23 P2 [completed contradiction](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3996642803) | T25/6.2/F19 retain all-state contrary nonexecution, prior receipt/charges and integrity fence; no terminal reopen, liability release or other-slot eviction | Closed in independent document review; pushed reply pending |
| GH24 P2 [review hash binding](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3996642807) | Section 9 distinguishes historical f34ec3 and authority-only a5aeee bytes; both reviewers independently reproduced that equivalence. This cycle requires actual final design/backlog hashes and new verdicts | Final reviewed hashes/verdict recorded below; pushed reply pending |
| GH25 P1 [ceased validator](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3996642810) | Typed T24 interruption/T17/T16/T27/F09 retain the open check/slot, honest accounting and bound recovery; eligible results apply before retry; benign historical results cannot satisfy a successor; current uncertainty and mandatory policy fences remain | Closed in independent document review; pushed reply pending |
| GH26 P1 [validation-only reuse](https://github.com/ModernNomad-98/Project-Aegis/pull/95#discussion_r3996642812) | T28/5.1/6.2/F01 atomically adopt compatible final effect evidence with current checks/free slot and immutable provenance; no repeated mutation, old pass/grant/charge or terminal reopen | Closed in independent document review; pushed reply pending |

Both independent architecture/recovery and security/authority reviewers approve the final documentation; no blocking finding remains in their traced paths.
Design SHA-256: `9e5ee6fcb20269732608d0444919e64865aee41122dcd249e7a1979b691e4076`.
Backlog SHA-256: `31459a5592a5ecec6668c28a4ad9dd3b1f877037251c6340eddae0ba9238e9d8`.
Follow-up findings closed: T24 exact uncertainty clearance; result-before-cessation intake; known final failure cannot be skipped by retry; consumed recovery survives only benign historical intake.
Late mandatory policy failure retains a bound irreversible stop obligation; late uncertainty/contradiction still fences. Catalog registration also precedes adoption.
Actual local checks exited 0: `git diff --check`; `python -B scripts/validate-skills.py` (184 valid, zero warnings); `python -B scripts/tests/test_validator.py` (91 assertions).
In-memory Markdown/link/ID audit passed: 39 local links/anchors, 29 tables, 50 headings, unique T01-T28/C01-C09; final expanded evidence and staged scope receive final checks.
Complete correction diff and follow-ups were inspected. Historical prose reflow preserved facts. Final evidence content/hash is verified separately, with no self-hash embedded.
Pushed replies, fresh exact-head review, DCO/CI and final head/tree remain PR/handoff evidence after delivery; passing 7988b89 CI does not validate this correction.
F01-F21 remain unexecuted future controller cases; these document traces and repository checks establish no runtime capability.

## 11. Intentional omissions and continuation

Only the three authorized Markdown files are created. No runtime implementation, schema/policy execution, shared extraction, BER/CI/dependency change, credential or sealed-holdout
access, provider dispatch through repository code, deployment, database action, release or tag is performed. Existing artifacts/recovery/ and artifacts/reviews/ remain untouched
and unstaged. Root .gitignore stays absent.

Controller tests and real platform/authority/receipt guarantees are future work, not claimed by document checks or unchanged BER tests. Storage selection, real approval
authenticity/freshness, external idempotency/fencing, Windows prevention and distributed ownership remain blocked implementation decisions.

After successful review/CI, complete the owner-approved merge and report its result. The next owner decision is whether to authorize separately scoped CP-WP-002; no implementation
starts here.
