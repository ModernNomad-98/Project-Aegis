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

## 2. Startup reconciliation

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

## 4. Review findings and dispositions

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

## 5. Validation evidence

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

## 6. Intentional omissions and continuation

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
