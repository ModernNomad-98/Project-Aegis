# Scenario A — acceptance-evidence runbook

This runbook explains how to produce and read the acceptance evidence for **Scenario A**
of the beginner-flow `docs/project-state.md` discipline, and maps the Scenario A defects
**AR-A-001 … AR-A-021** to the deterministic checks, skill evals, contract assertions, and
acceptance-harness tests that cover them (matrix at the end).

## What Scenario A is

Scenario A is the **clean "simple MVP" flow** through the beginner front door
(`project-orchestrator`): one non-developer, one small maintenance-company/clinic MVP, one
bounded first release, **no deadline and no delivery commitment**. It exercises the
project-state journey from cold start to the start of design:

1. **Cold start** — the file is created with the first State snapshot `SS-001`
   ("Defining the product") and empty-state Decision log / Approvals / Deviations.
2. **Discovery recorded** — the scope decision `PS-001` (a business decision, `user`) and
   the scope-agreement approval `A-001` are appended; projections are refreshed.
3. **Low-risk batch recorded** — reversible product-definition details are folded into the
   **mutable projections** (no new immutable rows).
4. **Product spec complete** — `PS-002` appended.
5. **Prioritization / roadmap / commitment readiness not applicable** — `PS-003`, `PS-004`,
   `PS-005` appended, each "not applicable (chosen over …, because …)" attributed
   `orchestrator-via-project-orchestrator`. These four DECISION entries are the Stage 2
   exit gate.
6. **Stage 3 snapshot** — `SS-002` ("Design: how it will be built") appended. Scenario A
   **stops here**: there is no `SS-003`.

The fixture that encodes this exact sequence lives at
`scripts/acceptance/scenario-a-fixture/state-sequence/` as eight ordered full versions
(`00-cold-start.md` … `07-stage3-snapshot.md`). Each file is the complete
`project-state.md` **after** that step.

### The property being proven

- The **immutable evidence** sections — `State snapshots`, `Decision log`, `Approvals`,
  `Deviations` — are **append-only**: no existing row is ever edited, deleted, reordered,
  or replaced; new rows are only added at the end. (Empty-state scaffolding rows may be
  dropped exactly once, when the first real evidence row arrives.)
- The **mutable projection** sections (`Current product summary`, `Current approved scope`,
  `Current users/roles`, `Current success definition`, `Open questions`) may be **freely
  refreshed** at checkpoints.
- The acceptance **evidence is stored OUTSIDE** the disposable product repo, and the
  product repo is **never committed to** for evidence.

## How to run the harness

Prerequisites: **git** on `PATH`, and either **Windows PowerShell 5.1** or **PowerShell 7**.
The harness creates a throwaway git repo and an evidence directory under your system temp
folder (outside this skills repo) and cleans them up on success.

### PowerShell 7 (`pwsh`)

```powershell
pwsh -NoProfile -File "scripts/acceptance/Invoke-ScenarioAEvidence.ps1" -KeepEvidence
```

### Windows PowerShell 5.1 (`powershell.exe`)

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\acceptance\Invoke-ScenarioAEvidence.ps1" -KeepEvidence
```

Both editions produce byte-identical evidence (no-BOM UTF-8 writes; byte-exact fixture
copies), so the recorded SHA-256 values match across editions and machines.

### Parameters

- `-KeepEvidence` — keep the work directory (disposable repo + evidence) after the run.
  Without it, a **passing** run cleans up after itself. A **failing** run always keeps its
  evidence so you can inspect it, regardless of this switch.
- `-WorkDir <path>` — root directory to create the disposable repo + evidence under. Must
  be **outside this skills repo** (the harness refuses otherwise). Defaults to a fresh
  unique directory under the system temp folder.

The harness exits **0** on all-pass and **non-zero** on any failure.

## How to read the evidence directory

With `-KeepEvidence` (or after a failure) the printed **evidence** path contains:

- `project-state.00.md` … `project-state.07.md` — the archived, byte-exact copy of each
  replayed version. This is the durable evidence, kept outside the product repo.
- `sha256sums.txt` — one `sha256sum`-format line per archived version
  (`<hash>  project-state.NN.md`). Verify later with, e.g.,
  `Get-FileHash -Algorithm SHA256 project-state.03.md` and compare the lower-cased hash.
- `diff.00-to-01.txt` … `diff.06-to-07.txt` — the captured `git diff --no-index` output
  between consecutive versions (the visible append/refresh at each step).
- `evidence-log.txt` — one ISO-8601-timestamped `PASS`/`FAIL` line per step plus a final
  `RUN RESULT` line. Each step line records whether the file was untracked, the diff
  exit-code interpretation, the append-only result (including which immutable rows were
  added), and the version's SHA-256.

## `git diff --no-index` exit-code semantics

The harness compares consecutive archived versions with `git diff --no-index --unified=0`.
`--no-index` makes git a plain two-file comparator whose exit code is the signal:

| Exit | Meaning | Harness treatment |
|------|---------|-------------------|
| `0`  | files identical | **unexpected** — consecutive versions must differ (flagged) |
| `1`  | files differ | **SUCCESS** of the comparison — this is what we expect |
| `>1` | git error | failure |

**Exit code 1 is not a script failure.** Each replayed version is expected to differ from
the one before it, so "differences found" (exit 1) is the success signal. The harness
captures git's exit code as data (stderr is redirected to a file, never `2>&1`), so a
non-zero git exit never becomes a terminating PowerShell error. The append-only property
is proven independently by parsing the immutable sections — the diff is the human-readable
record of what changed, not the pass/fail oracle.

## Evidence is external and uncommitted

- The disposable product repo only ever holds `docs/project-state.md` as an **untracked**
  file — the harness never runs `git add` or `git commit`. It verifies untracked status
  with **both** `git status --short --untracked-files=all` and
  `git ls-files --others --exclude-standard`, and asserts at the end that
  `git rev-list --count --all` is **0**.
- Every evidence artifact is written into the **external** evidence directory, never inside
  this skills repo. The harness refuses to run if its work directory resolves to a path
  inside the skills repo.

## Defect-to-test matrix — AR-A-001 … AR-A-021

Every defect maps to at least one deterministic check, skill eval, contract assertion,
acceptance-harness test, or fresh-session behavioral step. Behavioral evals are
specifications; the fresh-session Scenario A rerun (below) is the behavioral proof and is
required before any defect is called behaviorally resolved. Evals below live in
`project-orchestrator/evals/evals.json` unless noted; contract references are to
`project-orchestrator/SKILL.md`, `.../references/project-state-template.md`, and
`.../references/recording-and-authority.md`.

| Defect | P | Control | Test / evidence |
|---|---|---|---|
| AR-A-001 fresh app repo called the skills library | P2 | A | eval `edge-consumer-repo-not-skills-library`; contract Inputs-to-Inspect §2 + Gotcha "Calling the product repo the skills library"; fresh-session step 1 |
| AR-A-002 friendly alias instead of exact skill name | P2 | B | contract Capability 2 (exact backticked name; arrow only for a real invocation); evals `edge-stage2-classification-is-no-invocation`, `edge-no-prejudge-of-later-stage2-owners` |
| AR-A-003 two business questions in one turn | P1 | B | contract Capability 3 (≤1 decision question); evals `edge-low-risk-decisions-batch-to-one-checkpoint`, `positive-cold-vague-idea` |
| AR-A-004 unrelated approvals bundled | P1 | F,C | eval `should-not-batch-high-risk-actions`; `recording-and-authority.md` §1 (never-batched list) |
| AR-A-005 append-only history proposed for rewrite | P1 | G | eval `edge-immutable-history-is-append-only-placeholder-preserved`; template rules 2/§mutability; deterministic audit STATE-002/003; **harness append-only check** |
| AR-A-006 scope agreement → build authority | P0 | C | eval `should-not-treat-scope-acceptance-as-build-authority`; `recording-and-authority.md` §2; deterministic audit **APPR-002 1→0** on the template |
| AR-A-007 `(none yet)` placeholder proposed for replacement | P1 | G,D | eval `edge-immutable-history-is-append-only-placeholder-preserved` (placeholder branch); template rule 9; deterministic audit STATE-001 (clean); **harness placeholder handling** |
| AR-A-008 stage claimed before snapshot recorded | P1 | D,H | eval `edge-recorded-stage-lags-until-snapshot-appended`; contract Inputs §2 + template awaiting-record; **harness SS-003-absent check** |
| AR-A-009 ellipses in "exact" previews | P1 | D | eval `edge-exact-preview-is-byte-for-byte-no-ellipsis`; contract Capability 4 (byte-for-byte) + `recording-and-authority.md` §3 |
| AR-A-010 discovery exited before durable brief recorded | P1 | D,H | eval `edge-stage1-durable-before-stage2`; contract Capability 2 Stage 1 + Inputs §2 |
| AR-A-011 decision missing "chosen over …, because …" | P1 | D | contract Capability 3 + template rule 6; eval `should-not-treat-business-answer-as-write-approval` |
| AR-A-012 repeated an invalid corrected proposal | P1 | D | eval `should-not-repeat-a-rejected-proposal`; `recording-and-authority.md` §3 (proposal fingerprint) |
| AR-A-013 proposed an already-recorded decision | P1 | D | eval `should-not-repropose-an-already-recorded-decision`; `recording-and-authority.md` §3 (already-recorded scan) |
| AR-A-014 miscounted remaining questions | P2 | B,D | eval `edge-low-risk-decisions-batch-to-one-checkpoint` (checklist-count assertion); contract Capability 3 + `recording-and-authority.md` §3 |
| AR-A-015 spec review + permission-to-proceed bundled | P1 | C,F | evals `should-not-treat-scope-acceptance-as-build-authority`, `edge-recorded-stage-lags-until-snapshot-appended`; `recording-and-authority.md` §2 |
| AR-A-016 later Stage 2 owners pre-judged | P1 | E | eval `edge-no-prejudge-of-later-stage2-owners`; `edge-stage2-owner-ledger-in-progress`; contract Stage 2 (one at a time) |
| AR-A-017 classification not marked no-skill-invoked | P1 | E | evals `edge-stage2-classification-is-no-invocation`, `edge-no-prejudge-of-later-stage2-owners`; contract WHAT HAPPENS NEXT forms |
| AR-A-018 per-answer preview/approval/append ceremony | P1 | F | eval `edge-low-risk-decisions-batch-to-one-checkpoint`; `recording-and-authority.md` §1 (risk-tiered batch) |
| AR-A-019 acceptance assumed tracked files / empty diffs | P1 | H | **`Invoke-ScenarioAEvidence.ps1`** — untracked enumeration (`git status --short --untracked-files=all` + `git ls-files --others --exclude-standard`) and `git diff --no-index` exit-1 handling; this runbook |
| AR-A-020 no per-append external evidence | P1 | H | **`Invoke-ScenarioAEvidence.ps1`** — external copy + SHA-256 + prior-vs-current comparison + pass/fail log per append; no commits in the disposable repo |
| AR-A-021 stale projection contradicts spec/log | P1 | G | eval `edge-stale-projection-refreshed-before-completion`; template §mutability + conflict rule; deterministic audit **STATE-005 2→0** on the template |

**Live PR findings (also covered):** stage detection inspects the recorded owner gate →
eval `edge-resume-spec-recorded-but-owners-missing-stays-stage2`; terminal result awaits
record → template awaiting-record + eval `edge-stage2-terminal-result-awaits-recording`;
`COMMIT-ABLE` + `HUMAN DECISION REQUIRED` reachable → commitments evals
`readiness-commitable-does-not-require-human-decision`,
`should-not-equate-commitable-with-committed`; ROUTE-003 honest branch-aware →
`scripts/tests/test_audit_skill_contracts.py::test_route003_branch_aware`.

## Fresh-session behavioral acceptance (Control I) — required

The evals and the harness are specifications and deterministic evidence; they are **not** a
behavioral run of the orchestrator. Before AR-A-001 … AR-A-021 are called **behaviorally
resolved**, run Scenario A end-to-end in a **brand-new acceptance repository** and a **fresh
Claude session**, confirming:

1. a fresh consumer repository (a product, not the skills library);
2. no implementation permission is granted;
3. the requirements conversation asks **one** business question per turn;
4. low-risk answers accumulate in a visible **pending batch**;
5. **one** exact batch approval records the logical checkpoint;
6. the product spec is produced and **separately** accepted;
7. the product-spec terminal result is **recorded** (previewed → approved → appended);
8. prioritization is **independently** classified;
9. the roadmap is **independently** classified;
10. commitment readiness is **independently** classified;
11. every classification explicitly says **no skill invoked**;
12. the exit gate stays **BLOCKED** while any result awaits recording;
13. the exit gate becomes **MET** only after every owner result is recorded;
14. Stage 3 is proposed **separately**;
15. **no** package install, code, network action, Git commit, push, or implementation
    occurs.

The clean Scenario A experience does **not** require a separate diary approval after every
ordinary product answer (Control F). This runbook and its harness do not, and cannot,
substitute for that fresh-session rerun.
