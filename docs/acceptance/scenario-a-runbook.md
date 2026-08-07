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
   ("Defining the product") and empty-state `(none yet)` placeholder rows in the Decision
   log and Approvals (and `(none recorded …)` in Deviations). These placeholder rows are
   PRESERVED in every later version.
2. **Discovery recorded** — the scope decision `PS-001` (`user`) and the scope-agreement
   approval `A-001` are APPENDED after the placeholders. `A-001` freezes its allowed scope
   to immutable Decision `PS-001` (not to the mutable projection); projections are refreshed.
3. **Low-risk batch recorded** — the reversible product-definition choices (slot duration,
   multi-day navigation, link expiry, notification behavior) are FIRST appended to the
   Decision log as rationale-bearing rows `PS-002`, `PS-003`, `PS-004`, `PS-005` (attributed
   `user`), and only THEN are the mutable projections refreshed from those recorded rows.
4. **User accepts the product specification** — `PS-006` (attributed `user`) is appended,
   recording the user's acceptance of the actual spec CONTENT and anchoring it to the accepted
   artifact by its path + a SHA-256 of that artifact + the acceptance date. Approving the
   wording of a log row is not the same as accepting the spec's content.
5. **Product spec owner complete** — `PS-007` (attributed `orchestrator-via-product-spec-writer`)
   is appended; its Evidence REFERENCES the `PS-006` user acceptance and the same artifact. The
   product-spec owner is not complete until `PS-006` exists.
6. **Prioritization / roadmap / commitment readiness not applicable** — `PS-008`, `PS-009`,
   `PS-010` appended, each "not applicable (chosen over …, because …)" attributed
   `orchestrator-via-project-orchestrator`. Those four — `PS-007`, `PS-008`, `PS-009`, `PS-010`
   — are the Stage 2 exit-gate owner decisions.
7. **Stage 3 snapshot** — `SS-002` ("Design: how it will be built") appended. Scenario A
   **stops here**: there is no `SS-003`.

The fixture that encodes this exact sequence lives at
`scripts/acceptance/scenario-a-fixture/state-sequence/` as nine ordered full versions
(`00-cold-start.md` … `08-stage3-snapshot.md`). Each file is the complete
`project-state.md` **after** that step. A sibling `scripts/acceptance/scenario-a-fixture/manifest.json`
pins, PER STEP, the exact immutable IDs that must be present in each section AND a
line-ending-agnostic SHA-256 of that version (content normalized to LF before hashing, so an
autocrlf smudge cannot cause a false mismatch). The manifest also declares the SEMANTIC GATES
the harness enforces across the whole sequence: the user spec acceptance (`PS-006`) is recorded
BEFORE the product-spec owner completion (`PS-007`); the four Stage 2 owner records
(`PS-007`, `PS-008`, `PS-009`, `PS-010`) are all present BEFORE the Stage 3 snapshot (`SS-002`);
and the forbidden `SS-003` never appears. Removing a required row from every version, or editing
a fixture without updating its manifest hash, therefore FAILS the run — the append-only prefix
check alone can no longer pass an evidence sequence that silently dropped a required owner.

The manifest also pins the **accepted-spec artifact**: the `PS-006` acceptance anchors to a real
fixture, `scripts/acceptance/scenario-a-fixture/artifact/clinic-appointment-tracker-v1.md`, and the
manifest's `semantics.spec_artifact` records that file, its normalized SHA-256, the acceptance
decision id, and the in-product path. The harness recomputes the artifact's digest and FAILS if it
is missing, if the digest does not match the pin, if the pinned digest is not a well-formed
`sha256:`+64-hex value, or if the `PS-006` row does not anchor to that exact digest and path — so
the acceptance can be verified, not merely asserted.

### The property being proven

- The **immutable evidence** sections — `State snapshots`, `Decision log`, `Approvals`,
  `Deviations` — are **append-only**: no existing row is ever edited, deleted, reordered,
  or replaced; new rows are only appended at the end. Empty-state `(none yet)` placeholder
  rows are PRESERVED — the first real entry is appended AFTER the placeholder, and the
  placeholder is never dropped or replaced (schema rule 9). The harness FAILS the run if any
  previous immutable row, a placeholder included, is deleted, edited, reordered, or replaced.
- The **mutable projection** sections (`Current product summary`, `Current approved scope`,
  `Current users/roles`, `Current success definition`, `Open questions`) may be **freely
  refreshed** at checkpoints, but must never contradict the immutable records.
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

Windows PowerShell 5.1 and PowerShell 7 operating on the **same checkout bytes** produce
equivalent evidence behavior (no-BOM UTF-8 writes; byte-exact fixture copies). Each
recorded raw SHA-256 authenticates **that run's exact archived bytes** — the raw archive
hashes are not normalized, so an LF checkout and a CRLF checkout archive different bytes
and record **different raw values**. Cross-line-ending equivalence is provided by the
fixture manifest's **normalized-LF hashes** (which the harness verifies per step), not by
the raw values; the raw values remain the byte-exact evidence of what that run archived.

### Parameters

- `-KeepEvidence` — keep the work directory (disposable repo + evidence) after the run.
  Without it, a **passing** run cleans up after itself. A **failing** run always keeps its
  evidence so you can inspect it, regardless of this switch.
- `-WorkDir <path>` — **base** directory under which the run creates its own unique child
  ("scenario-a-run-…"). Must be **outside this skills repo**. The containment check first
  resolves reparse points (symlinks / Windows junctions / mount points) at **every path
  component** — not only the deepest existing one — to the PHYSICAL target BEFORE comparing paths,
  so a link whose real target is inside the skills repo is refused even when an ordinary child dir
  sits under it (e.g. `<junction-into-repo>/docs`); a lexical path comparison alone would be fooled
  into writing evidence into the repo. The harness
  NEVER deletes or recurses the base or its pre-existing contents: it creates, owns (via an
  ownership marker), and — only on a passing run and only after verifying the marker — removes
  only that child. A `-WorkDir` that already contains a `product-repo`/`evidence` directory is
  therefore safe.
- `-Manifest <path>` — override the fixture manifest (defaults to `manifest.json` beside the
  state-sequence directory); it supplies the per-step hashes + expected IDs and the semantic gates.
- `-FixtureDir <path>` — override the fixture state-sequence directory (used by the tests).
- `-LoadOnly` — define the harness functions and return without running (used by the tests).

The harness exits **0** on all-pass and **non-zero** on any failure.

### Negative / safety tests

`scripts/acceptance/Test-ScenarioAEvidence.ps1` proves the harness's guarantees:

- **Append-only** — deleting a preserved placeholder, or editing / deleting / reordering an
  immutable row, FAILS; a mutable projection-only refresh and the complete low-risk batch SUCCEED.
- **Manifest conformance (F1)** — a per-step hash mismatch (a fixture edited without updating the
  manifest), a duplicated or an unexpected immutable ID, and an unexpected fixture file all FAIL;
  and the full sequence FAILS when a required row is removed from every version — an owner
  (`PS-010`), the user acceptance (`PS-006`), or the owner completion (`PS-007`).
- **Semantic gates** — the sequence FAILS if the user acceptance (`PS-006`) or a Stage 2 owner is
  missing, or if acceptance does not precede completion; caller-owned directories are never deleted.
- **Accepted-spec artifact** — the real fixture passes; a TAMPERED artifact (digest no longer
  matches the pin), a MISSING artifact, a malformed pinned digest, a wrong pinned digest, and an
  acceptance row that fails to anchor to the digest/path all FAIL.
- **External-evidence boundary (F6/R4-3)** — a `-WorkDir` that is a symlink/junction whose PHYSICAL
  target is inside the skills repo is REJECTED, **including a path nested below such a link**
  (`<junction-into-repo>/docs`), and no run directory leaks into the repo; a normal external
  `-WorkDir` with a pre-existing `product-repo`/sentinel survives untouched. An expected-**failure**
  run (which preserves its evidence) is given a tracked `-WorkDir` so nothing leaks into system temp.
- **Fail-closed commit count (F5)** — the zero-commit check accepts only git exit 0 with exactly
  one non-negative integer `0`; a non-zero git exit, or empty / non-numeric / multi-line / negative
  / unexpectedly-positive output, all FAIL — a broken Git check never silently certifies "0 commits".

The integration cases launch the harness in a CHILD process using the **currently running
PowerShell host executable** — `pwsh` under PowerShell Core, `powershell.exe` under Windows
PowerShell — resolved from the live process rather than a hard-coded Windows-only binary, so the
suite runs under both editions (the self-check prints which host it selected). Run it the same way:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\acceptance\Test-ScenarioAEvidence.ps1"
```

Under PowerShell 7, run `pwsh -NoProfile -File "scripts/acceptance/Test-ScenarioAEvidence.ps1"`.

## How to read the evidence directory

With `-KeepEvidence` (or after a failure) the printed **evidence** path contains:

- `project-state.00.md` … `project-state.08.md` — the archived, byte-exact copy of each
  replayed version. This is the durable evidence, kept outside the product repo.
- `sha256sums.txt` — one `sha256sum`-format line per archived version
  (`<hash>  project-state.NN.md`). Verify later with, e.g.,
  `Get-FileHash -Algorithm SHA256 project-state.03.md` and compare the lower-cased hash.
- `diff.00-to-01.txt` … `diff.07-to-08.txt` — the captured `git diff --no-index` output
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
  `git ls-files --others --exclude-standard`, and at the end requires
  `git rev-list --count --all` to exit 0 AND return exactly one non-negative integer, then
  asserts that integer is **0**. A non-zero git exit or malformed count FAILS the run — it is
  never silently coerced to 0, so a broken Git check can never certify the no-commits property.
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
| AR-A-007 `(none yet)` placeholder proposed for replacement | P1 | G,D | eval `edge-immutable-history-is-append-only-placeholder-preserved` (placeholder branch); template rule 9; deterministic audit STATE-001 reports 2 semantic-review candidates on the required preserved `(none yet)` rows — human review confirms they are use-versus-mention false positives (rule 9 requires preservation, and the harness proves later records APPEND after them rather than replacing them); **harness placeholder handling** + `Test-ScenarioAEvidence.ps1` Part 7 template parity |
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

**STATE-001 disposition (human semantic review recorded).** The current generated audit
baseline **intentionally retains two `STATE-001` P0 semantic-review candidates**, anchored
to the copyable template's required preserved `(none yet)` Decision and Approval
empty-state rows (`project-state-template.md:171` and `:183`). Semantic-candidate severity
is a **prioritization signal, not mechanical proof** — the audit tool queues such readings
and has not semantically reviewed them itself. Both findings **have now been manually
reviewed by a human**: both are **false positives** of STATE-001's documented
use-versus-mention limitation, firing on **required preserved empty-state rows** —
template **rule 9 is the controlling contract** (the empty-state placeholder row is
preserved; the first real record is appended AFTER it; the placeholder is never edited
into a real record). `Test-ScenarioAEvidence.ps1` **Part 7** (cold-start placeholder
parity; no pre-populated `PS-*`/`A-*` data row) and the **append-only harness checks**
provide the deterministic regression evidence that later records append after those rows
rather than replacing them. The audit artifacts remain **unchanged** because the findings
and the detector's output are being **truthfully retained rather than suppressed**, with
this recorded disposition as the human review of record. **No behavioral proof is
claimed** by this disposition; the fresh-session Scenario A behavioral acceptance
(Control I below) remains required.

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
