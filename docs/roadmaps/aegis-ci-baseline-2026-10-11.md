# Aegis CI baseline and bottleneck observations (2026-10-11)

**Status: observation record only — it changes nothing and grants nothing.** This
page records the continuous-integration (CI) baseline of
`ModernNomad-98/Project-Aegis` as observed on 2026-10-11: the six jobs of the
repository's only workflow, their triggers, path filters, required or advisory
status and measured durations; the branch-protection settings; three
evidence-backed top bottlenecks plus the ranked remainder; the MG1-MG5
enforcement status; and the method by which every figure here can be
re-derived. It edits no workflow, script, tool, dependency file or index, and it
authorizes no CI change, no protected-path change, no branch-protection change
and no merge.

**Who should read it.** Any agent or human planning, reviewing or approving a CI
change on this repository. It is the baseline a future optimisation claim is
measured against, and §8(b) states what such a claim must carry before it is
believed.

**Reading key.** **CI** is continuous integration: the automated checks that run
on a proposed change. A **pull request (PR)** proposes a change; its **head** is
its newest commit, and a **check** is one CI job's result on that head. **DCO**
is the Developer Certificate of Origin, enforced here as a `Signed-off-by:`
trailer on every commit of a PR (CONTRIBUTING.md L266-274). **Required** means a
check registered in branch protection, so a normal merge is blocked until it
passes; **advisory** means visible coverage that blocks nothing mechanically
(offline-ci.md L53-60). A **path filter** decides whether a job runs, from the
list of paths the change touches. **UNKNOWN** means not measured, **UNRUN** means
not run, and **skipped** means the filter did not select the job — a skipped or
unrun job is never a pass (offline-ci.md L41-51, L62-67, L229-236). File paths
below are relative to the repository root; `.github/workflows/validate-skills.yml`
is the one workflow, so its bare line citations are written `L…`.

**Bound facts and dates (provenance).**

- Repository facts here — every file and line citation — were read at head
  `5ad973a2d8ef5908021deea9861ac57bd9f72292` (`origin/main` at authoring time; tree
  `40452161058d0d7539b19c7a0da979729e78c418`). Line numbers are those of that tree; a
  later head may move them.
- Live GitHub facts (job durations, branch protection) were re-derived from the
  GitHub API on 2026-10-11 17:09:36 PDT (2026-10-12T00:09:36Z) with an authenticated `gh`
  CLI. They are dated observations, not maintained state.
- Session evidence (outside this repository): the Stage A plan
  `_resume-2026-10-09/evidence/p0/P0A-A1-PLAN.md` (sha256
  `4cdc03d5fe0d67e111f83ce4e6469fa0e136a650ccc284db821179f3e28b9a0b`) and its
  independent audit `_resume-2026-10-09/evidence/p0/P0A-A1-AUDIT-B.md` (sha256
  `1ab348270d0dc25cac71365e5f36b2142fecf0fbb446d9729fc741140ed4553e`), which
  accepted the plan (SD-B ACCEPT) and whose findings F1-F6 are folded in here
  (§8(b), §8(c), §3, §5, §7); and the source reconciliation
  `_resume-2026-10-09/evidence/p0/F0-source-authority-reconciliation.md` (F0),
  whose same-day live measurements this page re-derived rather than copied.
- This page's own commit cannot be cited inside its own bytes — see §8(c). Its
  head, tree and base are recorded in the Stage C handoff and the pull request.

## S2. Baseline inventory — the six jobs

One workflow exists at this head: [`.github/workflows/validate-skills.yml`](../../.github/workflows/validate-skills.yml)
(verified by listing `.github/workflows/`: one file). Its workflow name is
`validate-skills` (L6). Its two events are deliberately asymmetric (decision D60):
`pull_request` with types `opened`, `synchronize`, `reopened`, `edited` targeting `main`,
and `push` to `main` (L8-23). The push event is a detection lane, not a gate: it
runs after the merge and cannot block anything (L11-15).

| Job | Runner | Trigger | Path filter | Merge role | Timeout | Measured duration | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `changes` | ubuntu-latest | every PR to `main` and every push to `main` | none — it computes the flags the advisory jobs consume | not registered as required | 5 min | 8 s (run `38184781825` @ `6ea8a723`) | L57-104 |
| `validate-skills` | ubuntu-latest | every PR to `main` and every push to `main` | none (unconditional) | **required** (branch protection) | 15 min | 111 s (same run) | L106-283 |
| `gate-guard` | ubuntu-latest | pull requests only | none (unconditional, PR-only) | **required** (branch protection) | 5 min | skipped on push runs; runs on every PR | L484-561 |
| `windows-offline-checks` | windows-latest | `needs: [changes]`; runs when the event is a push or the offline flag is true | offline = `tools/` or `requirements-ci.in` / `requirements-ci.txt` | advisory (not registered) | 20 min | 241 s (same run) | L285-370 |
| `tools-tests-linux` | ubuntu-latest | `needs: [changes]`; push or tools flag true | tools = `tools/` only | advisory (not registered) | 15 min | 100 s (same run) | L378-426 |
| `tools-tests-windows` | windows-latest | `needs: [changes]`; push or tools flag true | tools = `tools/` only | advisory (not registered) | 20 min | 165 s (same run) | L428-482 |

The second measured run is in §5. How the filter is computed (L81-104): on a PR
the `changes` job diffs the PR against its base with a three-dot
`git diff --no-renames --name-only` and sets `offline` true when a path matches
`tools/` or one of the two root lock files, and `tools` true when a path matches
`tools/`; on a push to `main` both flags are forced true (L86-88), so the
post-merge run selects all three advisory jobs. `validate-skills` and
`gate-guard` have no path filter and no `needs:` — they run unconditionally on
their events (offline-ci.md L41-51).

Consequences this page depends on:

- A change touching only `docs/`, skill files or the workflow itself runs
  `changes` + `validate-skills` + `gate-guard` on its PR and skips the three
  advisory jobs. Two steps inside `validate-skills` are PR-only: the DCO check
  (L260-267) and the PR-body bound-field check (L269-274).
- On a push to `main`, `gate-guard` is skipped (its `if:` at L493 admits pull
  requests only) while the three advisory jobs run: the full suite minus the
  guard, which is the post-merge detection lane (offline-ci.md L62-67).
- Each advisory job declares `needs: [changes]` (L288, L379, L429), so it is also
  skipped when `changes` itself fails, times out or is cancelled; check
  `changes` first to tell the two cases apart (offline-ci.md L236).
- Record a skipped job as **skipped**, never as passed (offline-ci.md L41-51).
  `not applicable` is a different status, permitted only where a condition's own
  scope clause says so (delivery-workflow.md L226-231).

Both gate jobs run with a read-only token (`permissions: contents: read`, L25-26,
L383-384, L433-434), and both advisory tools jobs also pin
`persist-credentials: false` on checkout (L389-391, L439-441) — §4.

## S3. Branch protection and required checks

Settings read live (authenticated) on 2026-10-11 17:09:36 PDT with:

```text
gh api repos/ModernNomad-98/Project-Aegis/branches/main/protection --jq '{required_status_checks: {contexts: .required_status_checks.contexts, strict: .required_status_checks.strict}, enforce_admins: .enforce_admins.enabled, reviews: {dismiss_stale_reviews: .required_pull_request_reviews.dismiss_stale_reviews, require_last_push_approval: .required_pull_request_reviews.require_last_push_approval, required_approving_review_count: .required_pull_request_reviews.required_approving_review_count}, allow_force_pushes: .allow_force_pushes.enabled, allow_deletions: .allow_deletions.enabled}'
```

Output (one line, verbatim):

```text
{"allow_deletions":false,"allow_force_pushes":false,"enforce_admins":false,"required_status_checks":{"contexts":["gate-guard","validate-skills"],"strict":false},"reviews":{"dismiss_stale_reviews":false,"require_last_push_approval":false,"required_approving_review_count":1}}
```

| Setting | Value | What it means for a merge |
| --- | --- | --- |
| Required status contexts | `gate-guard`, `validate-skills` | Only these two checks block a normal merge mechanically. The three advisory jobs do not (offline-ci.md L53-60, L119-122). |
| `strict` (branch up to date) | `false` | The platform does not require the head to be rebased on the latest `main`. |
| `enforce_admins` | `false` | Repository administrators can merge past a red required check (delivery-workflow.md L642-643). |
| `required_approving_review_count` | `1` | A normal merge asks for one approving review. |
| `dismiss_stale_reviews` | `false` | A new commit does not dismiss an existing approval. |
| `require_last_push_approval` | `false` | The last push does not need a fresh approval either. |
| `allow_force_pushes`, `allow_deletions` | `false`, `false` | `main` cannot be force-pushed or deleted through these API settings. |

The last three rows are why the repository's exact-head rule is procedural: the
platform will not invalidate a verdict when a head moves
(delivery-workflow.md L407-411).

**Authentication limit — recorded, not hidden.** Branch-protection data is not
public: an unauthenticated read returns HTTP 401, which the independent Stage B
audit of this page's plan observed (AUDIT-B item 8), so re-deriving these rows
requires an authenticated `gh` (or token) with repository access. Stage C read
them that way at 2026-10-11 17:09:36 PDT; the values matched F0's earlier authenticated read of
2026-10-11 16:37 PDT, with `require_last_push_approval` recorded here in addition.
Re-verify at the head being merged: branch protection can change with no commit
to this repository.

## S4. Dependencies, isolation and evidence plumbing

**Dependencies are a complete hash lock, not a version range.** `validate-skills`
installs `requirements-ci.txt` with
`pip install --require-hashes --only-binary :all: --no-deps -r requirements-ci.txt`
and then runs `pip check` (L142-146), recording the resolved set through the
recorder (L148-149). A file whose hash is not in the lock fails the install, no
source distribution is built and nothing outside the lock is resolved
(offline-ci.md L124-140). The lock's `openai` hashes must equal the
`AUTHORIZED_SDK_*` constants in
`tools/behavioral_eval_runner/judge/calibration_transport.py`, and
[`scripts/tests/test_offline_ci.py`](../../scripts/tests/test_offline_ci.py) enforces that — an
SDK bump must update the constants and the lock together (offline-ci.md
L134-140). The lock's input `requirements-ci.in` is deliberately not protected:
editing it changes nothing in CI until the protected lock is regenerated
(offline-ci.md L244-246).

**Interpreters are pinned.** Python `3.14` (L122-134, with the reasoning: `3.x`
silently followed the runner image) and Node `24` for the setup host-bridge
callback tests (L400-402; the same pins on Windows, L448-454). Both verification
lanes use full Git history, because some Behavioral Eval Runner fixtures verify
historical commits (offline-ci.md L126-127).

**Import and executable isolation.** Every script run and every `python -m pip`
call in the workflow uses `python -P`, so a module a PR adds beside a gate
script cannot shadow the standard library or the YAML parser and rewrite an exit
status (L28-36). The commands that legitimately need the checkout root on
`sys.path` (`-m tools.behavioral_eval_runner`, `-m unittest`) cannot take `-P`
and rely instead on the guard protecting every root-level importable name
(L34-36). On Windows, `NoDefaultCurrentDirectoryInExePath: '1'` (L50-53) turns off
the `CreateProcess` working-directory search, so a root `git.exe` or `python.exe`
added by a PR cannot run in place of the real tool (L45-49).

**Gate/tools isolation.** The gate jobs run only code the guard protects; the
tools suites — PR-controlled code outside that set — run on their own runners
with a read-only token and no persisted credentials, sharing no runner,
environment file, `PATH` or checkout with the gates (L38-43, L372-377, L389-391,
L439-441). A step in a gate job could otherwise write `$GITHUB_ENV` or rewrite a
gate script before it ran.

**Evidence plumbing.** [`scripts/ci/record-check.py`](../../scripts/ci/record-check.py) runs
an existing command once, streams its combined output, preserves the raw log
bytes and writes a JSON record holding the label, the command, `checkout_sha`,
dirty state, `event_sha`, the PR head SHA, Python/platform and key package
versions, the native exit code and the elapsed seconds (record-check.py L61-68,
L85-89). It refuses to overwrite an earlier log or record with the same label
(L52-54) and never retries or reinterprets the command (docstring L1-2;
offline-ci.md L195-201). Each verification job uploads its logs and records on
success or failure under a unique OS/run/attempt name, with **14-day
retention** and `if: always()` (L276-283, L363-370, L475-482); the upload action
is pinned to `actions/upload-artifact` v7.0.1 commit
`043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` (offline-ci.md L203-210).

## S5. Measured durations

Two successful push runs on `main`, re-read from the GitHub API on 2026-10-11 17:09:36 PDT
(durations are seconds between each job's `started_at` and `completed_at`; a
skipped job reports an inverted window, which is how `gate-guard` appears on a
push run):

**Footnote, 2026-10-12 — the skipped-window sentence above is over-general.**
A skipped job's timestamp window is not always inverted. The measured set over
the live payloads the A2 audit read is **{−1 s, 0 s, absent}** — skipped
windows of negative, zero, or absent duration — and a 0-second window would
render as an executed job with a duration of 0 s if state were derived from the
window. The rule that follows is **conclusion-first**: `conclusion=skipped`
means skipped with no duration, whatever the window says; the window is used
only for executed jobs. The `gate-guard` instance above stays true and no
figure in the table changes. Recorded as the page-level follow-up required by
`P0A-A2-AUDIT-B-rev2.md` R3.

**Correction to this footnote, 2026-10-12 (Stage C2 repair; Codex finding
`4252843353`, Stage D item F-A).** The footnote first read "skipped windows of
both signs and of zero". That clause was false: the set stated above holds a
negative window, a zero window and an absent window, and **no positive
window**. The sentence now reads "skipped windows of negative, zero, or absent
duration", which is the contract the reader already carries —
`tools/aegis_delivery_control/ci_durations.py` L11-14: "A skipped job carries
`not_applicable` whatever its window looks like (-1 s, 0 s, null or absent)."
The conclusion-first rule, the `gate-guard` instance and every figure above are
unchanged.

| Run ID | Event | Head | `changes` | `validate-skills` | `gate-guard` | `windows-offline-checks` | `tools-tests-linux` | `tools-tests-windows` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `38184781825` | push (post-merge) | `6ea8a723ee90346f2e7203229b5103f4c25d58d2` | 8 s | 111 s | skipped (PR-only) | 241 s | 100 s | 165 s |
| `38182969797` | push (post-merge) | `f41a29525b36c9c0c95099e20b63289ad17710ae` | 4 s | 109 s | skipped (PR-only) | 243 s | 147 s | 168 s |

Run windows: `38184781825` 23:34:19Z → 23:38:32Z and `38182969797` 23:05:41Z →
23:09:53Z. Measurement tool and method:

- `gh api repos/ModernNomad-98/Project-Aegis/actions/runs/<run_id>` → head SHA,
  event, status and conclusion.
- `gh api 'repos/ModernNomad-98/Project-Aegis/actions/runs/<run_id>/jobs?per_page=100'`
  → each job's `started_at` and `completed_at`; every figure above is the
  difference between them.
- `gh api repos/ModernNomad-98/Project-Aegis/actions/runs/<run_id>/timing` →
  billable minutes. It returned no billable rows for these two runs when read,
  so billed time is **UNKNOWN** here.
- These endpoints are readable without a token on this public repository: the
  independent Stage B audit re-read both runs unauthenticated and matched these
  figures, and Stage C re-read them authenticated and matched again.

**UNKNOWN, each with what would resolve it.**

- The distribution of PR-run latencies (queue plus run) — no PR-triggered run
  has been sampled for latency here; resolve by sampling PR runs over a fixed
  window.
- The flake rate — the repository documents the signature (every job cancelled
  at the same instant, at durations matching none of the jobs' own timeouts →
  re-run the workflow on the same head; L63-66, offline-ci.md L229-236) but no
  frequency has been measured; resolve by a census of cancelled-at-once runs
  over a fixed window.
- The wall time of the full suite reproduced locally — the hosted figures above
  have no local counterpart at this head; resolve by running the local set in
  the hash-locked environment (§8(a)) through the recorder.
- Billed CI time — see the `timing` row above.

## S6. Ranked bottlenecks (evidence, or UNKNOWN)

The top three, each with its evidence:

1. **The five merge-gate conditions (MG1-MG5) are 100% procedural.** The
   repository's own enforcement split records `Enforced by: Nothing` for each of
   them (delivery-workflow.md L653-657), and the platform settings that would
   partially cover head moves and administrator bypass are off:
   `enforce_admins: false` (L642-643) and `dismiss_stale_reviews: false`
   (L407-411). Consequence: "all checks green at the exact head, the final
   review posted and accepted there, the automated-review wait honoured" rests
   entirely on agent discipline; the receipt that records it is a record, not a
   gate (L207-234).
2. **Every CI-improvement change is itself blocked by the guard it aims to
   improve.** The protected-path pattern (L545) matches `.github/workflows/` and
   `scripts/`, so a change to the pipeline or its tooling lands red on the
   required `gate-guard` check and needs a one-time exact-head owner exception
   each time (CONTRIBUTING.md L45-56; the only standing exception covers four
   named Behavioral Eval Runner files). The lock file and the workflow are
   protected too, so every Dependabot bump carries the same friction
   (offline-ci.md L159-165). CI velocity is structurally capped at one owner
   decision per protected change.
3. **Windows and tools coverage is advisory on pull requests.**
   `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows` are
   not registered required checks (offline-ci.md L53-60, L119-122) and run only
   when the path filter selects them (L288-289, L379-380, L429-430); measured at
   241 s / 100 s / 165 s on run `38184781825` (§5). A Windows-only or
   `tools/`-only regression can merge green and is caught, if at all, by the
   post-merge push lane (L8-15, L86-88).

Ranked after the top three:

4. **Dependency bumps each need an owner exception** — the lock file and the
   workflow are protected paths, one friction event per Dependabot PR
   (offline-ci.md L159-165).
5. **The documented infrastructure-flake signature forces re-runs** — all jobs
   cancelled at once at durations matching none of their own timeouts (L63-66;
   offline-ci.md L231-233), and a cancelled run is not a pass. Frequency:
   **UNKNOWN** (resolver in §5).
6. **Local reproduction requires the hash-locked environment** — the validator
   and the CI self-tests fail closed without the pinned dependencies
   (offline-ci.md L325-349; F0 reproduced that failure at `6ea8a72`). The cost
   of a full local mirror is **UNKNOWN**: the hosted per-job numbers in §5 are
   not local wall time.
7. **UNKNOWN items**, restated here so the ranking is complete: the hosted
   PR-run latency distribution, the flake rate, the automated review's (MG3)
   latency, and whether the advisory jobs' status has in fact let reds merge in
   practice. None is measured. What would resolve each: a PR-run latency
   sample; a cancelled-run census; per-head automated-review timestamps; and a
   review of merged PRs whose post-merge push run went red.

## S7. MG1-MG5 enforcement status

The normative merge-gate block is delivery-workflow.md L294-335; the
repository's own enforcement measurement is its procedural-requirements table at
L645-668. This page repeats the **status and the pointers**, not the
requirements — a derived list carries identifiers, statuses and pointers only
(L236-243):

| ID | Normative definition (pointer) | Enforced by (the repository's own row) |
| --- | --- | --- |
| MG1 | delivery-workflow.md L294-305 | `Nothing` — L653 |
| MG2 | delivery-workflow.md L306-307 | `Nothing` — L654 |
| MG3 | delivery-workflow.md L308-314 | `Nothing` — L655 |
| MG4 | delivery-workflow.md L315-324 | `Nothing` — L656 |
| MG5 | delivery-workflow.md L325-335 | `Nothing` — L657 |

The same table also records `Nothing` for exact-head invalidation (L658) and for
the audited plan being bound to a captured revision (L659).

**Receipt vocabulary, and what a change of this class may write.** The receipt's
shape and vocabulary are at delivery-workflow.md L207-234: a status table keyed
to the `MG` identifiers plus the `SD-F` template answer, carrying identifiers,
statuses and pointers only; `not applicable` is permitted only where a
condition's own scope clause says so, recorded by linking to the condition
(L226-231). For a change that touches no `tools/` path and neither lock file —
this page's own class — the three advisory jobs are recorded as **`skipped`** with
the path-filter citation (offline-ci.md L41-51), never as passed. MG5's
outside-contribution scope is stated at CONTRIBUTING.md L253-258 and
AGENTS.md L73-74; a receipt may take MG5 as `not applicable` only on that clause.

Two further recorded facts. The check that would assert the PR body's
reconciliation-witness block is `recorded as open, not present` (delivery-workflow.md
L704-706). And the coordinator's recorded precedent for an automated review
result that exists only at a superseded head is at
`FAST-CHECKPOINT-2026-10-11D.md` L18 — L17 at the Stage B audit's read; the
checkpoint gained one line at L14 at 17:04:40 PDT on 2026-10-11 — with the
stricter normative rendering at delivery-workflow.md L308-314 recorded as
literally unmet in each receipt.

## S8. Re-derivation method, future-claim criteria, honesty

### S8(a) — Method: how every figure here is re-derived

1. **Get the bytes.** Clone or fetch the repository and check out a named head;
   record `git rev-parse HEAD` and `git rev-parse HEAD^{tree}`. On Windows, fetch
   with `-c http.sslBackend=openssl` when the platform TLS backend fails.
2. **Read the workflow.** `.github/workflows/validate-skills.yml` at that head;
   confirm it is the only file in `.github/workflows/`. Every `L…` citation in
   §2 and §4 resolves there: job names, timeouts, `if:` conditions, the two flag
   regexes and the protected-path pattern (L545) are the load-bearing lines.
3. **Re-read the durations.** The two `gh api` endpoints in §5; a job's seconds
   are `completed_at` minus `started_at`. No token is needed for these on this
   public repository.
4. **Re-read branch protection.** The `gh api` command in §3, authenticated —
   the endpoint returns 401 without a token. Compare the JSON, not a rendered
   settings page.
5. **Reproduce the local set in the hash-locked environment.** Create an
   isolated Python 3.14 environment, then
   `python -m pip install --require-hashes --only-binary :all: --no-deps -r requirements-ci.txt`
   and `python -m pip check`; then the recorded commands (offline-ci.md L325-349).
   The three that matter for this page:
   - gate isolation: `python -P scripts/ci/record-check.py ci-tests -- python -P scripts/tests/test_offline_ci.py`;
   - skill validation: `python -P scripts/validate-skills.py` (at this head it
     prints `OK: 205 skill(s) valid, 0 warning(s)` and exits 0);
   - the PR-body bound-field checker against its fixtures:
     `python -P scripts/ci/check_pr_body_skills.py --body-file <file> --author <login>`
     (a good body exits 0, a bad body 1, a bot author 0).
   Record each through [`scripts/ci/record-check.py`](../../scripts/ci/record-check.py) so the
   result is bound to `checkout_sha`, dirty state, `event_sha`, the PR head SHA,
   the native exit code and the elapsed seconds (record-check.py L61-68).
6. **Mind the retention window.** Uploaded artifacts live 14 days (L276-283;
   offline-ci.md L203-210), so re-deriving a specific run's raw logs after that
   window needs a new run; the run and job metadata used in §5 outlives the
   artifacts, and that metadata is what §5 cites.
7. **Walk one figure end to end (worked example).** The
   `windows-offline-checks` row of §5, run `38184781825`:
   - `gh api repos/ModernNomad-98/Project-Aegis/actions/runs/38184781825` →
     `"head_sha":"6ea8a723ee90346f2e7203229b5103f4c25d58d2"`, `"event":"push"`,
     `"conclusion":"success"`.
   - `gh api 'repos/ModernNomad-98/Project-Aegis/actions/runs/38184781825/jobs?per_page=100'`
     → the `windows-offline-checks` row reads
     `completed|success|2026-10-11T23:34:31Z|2026-10-11T23:38:32Z`; the
     difference is 241 s.
   - Cross-check on run `38182969797`: `2026-10-11T23:05:49Z` →
     `2026-10-11T23:09:52Z` = 243 s.
   A Stage D walk should reproduce a **duration row from §5** like this one;
   the branch-protection rows are deliberately not the walked figure because
   they need a token.

### S8(b) — What a future optimisation claim must carry (relay-derived criteria)

**Non-exhaustiveness label (mandatory): relay-derived criteria; the directive's
verbatim success-criteria list prevails; completeness pending owner verbatim
text.** The criteria below come from the directive fragments relayed to this
effort (`FAST-CHECKPOINT-2026-10-11D.md` L17) and from the repository's own
rules. They are a record, not an authorization mechanism: no future increment is
relieved of its own plan and independent review by citing them, and every
requirement below is subordinate to the directive's own wording.

| Relayed directive goal | Evidence a claim must carry before it is believed |
| --- | --- |
| Reliability | Before/after measured durations with run IDs at a comparable workload, plus green required checks at the head that carries the change. |
| Accurate coverage | The required-check set is unchanged, or the owner's branch-protection decision is cited; skipped jobs are recorded as skipped, never as passed (offline-ci.md L41-51). |
| Faster where safe | Duration evidence measured as in §5 **and** gate isolation still intact — `scripts/tests/test_offline_ci.py` green (§8(a) step 5). |
| Less waste | A concrete removed or avoided run, with before/after evidence for the run that no longer happens. |
| Clear usable evidence | Every figure carries its command and output, or a run ID that resolves (§8(a)). |
| Safe continuation | No protected path weakened; no auto-merge armed (forbidden — AGENTS.md L120; the standing grants' scope); the change stays inside its recorded grants. |

Binding on every such claim: negative tests and real tool-call traces accompany
the acceptance evidence (the directive's sequence step 5, as relayed); a claim
that lacks evidence is labelled **UNVERIFIED**, never implied; no percentage is
invented; and the intended future consumer of this page is the F2a CI evidence
reader — independently callable, read-only, never auto-run by FAST SAVE — whose
mechanics beyond that description are **UNKNOWN**.

Stage D check note: applying the independent plan audit's finding F1, the
acceptance criterion AC9 requires **both** the label above and the gap mapping
in §8(c) to be present.

### S8(c) — Intentionally not recorded / UNKNOWN, gap mapping, revision

Intentionally not recorded, or UNKNOWN:

- The distribution of PR-run latencies — **UNKNOWN**; resolver: sample
  PR-triggered runs over a fixed window.
- The flake rate — **UNKNOWN**; resolver: a census of cancelled-at-once runs
  over a fixed window.
- The automated review's (MG3) latency — **UNKNOWN**; resolver: per-head review
  timestamps. The recorded superseded-head precedent and its literal-unmet
  bookkeeping are cited in §7.
- Live re-verification at later heads — this page's live facts are dated
  2026-10-11 17:09:36 PDT and are deliberately not maintained; re-derive with §8(a).
- The directive's verbatim text. It is not on `main` (F0 §5 records zero
  matches for its markers at `6ea8a72`), so the success-criteria list is
  relayed, not quoted; the owner or coordinator can supply the verbatim text.
- Whether the advisory jobs' status has in fact let reds merge in practice —
  **UNKNOWN**; resolver: review merged PRs whose post-merge push run went red.
- Billed CI time — the `timing` endpoint returned no billable rows for the two
  sampled runs (§5).
- Branch-protection facts without a token — §3 records the 401 found by the
  independent audit and the authenticated re-read made here.

**Gap mapping (audit F1).** The relay that §8(b) derives from did not include
the directive's verbatim success-criteria list. Mapping each relayed goal to the
criterion it serves, and naming what the relay cannot establish:

| Relayed goal in §8(b) | Directive success criterion it serves | What is unverifiable from the relay |
| --- | --- | --- |
| Reliability | baseline plus reproduced bottlenecks | whether the verbatim list adds further reliability criteria |
| Accurate coverage | no lost coverage; honest failure and skip reporting | "no lost coverage" is inferred from the required-check set and the skip rules, not quoted |
| Faster where safe | comparative measurements; preserved gate isolation | the directive's exact comparative-measurement wording |
| Less waste | (no relayed criterion identified) | whether the directive names waste reduction explicitly |
| Clear usable evidence | correct source bindings; actual CI results on the final candidate | the directive's exact binding and final-candidate wording |
| Safe continuation | independent review; regression and negative tests | whether independent review is stated as a per-increment requirement |

Until the owner's verbatim text is supplied, this mapping is the honest
statement of what the relay could and could not support; no criterion above is
claimed to be the directive's own wording.

**Revision record.** This page is revision 1, authored 2026-10-11 from base head
`5ad973a2d8ef5908021deea9861ac57bd9f72292`. Its own commit SHA cannot appear in
its own bytes: a file's content determines its hash, so a page cannot carry the
hash of the revision that contains it, and this increment is constrained to one
commit. The head SHA, the tree it resolves to, the base and the pull-request
number are recorded in the Stage C handoff record and in the pull request; a
later increment may add the merged pull-request number here.

**Dated cross-reference — 2026-10-12: the instrument §8(b) requires now exists.** This
page stays bound to head `5ad973a2d8ef5908021deea9861ac57bd9f72292`, and its line-number
citations stay bound to that tree (a later head may move them). §8(b) states what a future
optimisation claim measured against this baseline must carry; the read-only reader that
produces the per-run and per-job durations such a claim needs now exists: **`ci-durations`**
in `tools/aegis_delivery_control` (PR #740, merge `7fbc2335`, the current `main` head),
documented in the tool's README. This block changes no figure on this page, adds no
criterion, and **grants no CI change, no protected-path change, no branch-protection change
and no merge**.

## Footnote, 2026-10-12 — the artifact pin this page cites has moved to v7.0.2

**Appended, never rewritten.** The S4 paragraph above is the dated 2026-10-11 observation and its bytes
are untouched, exactly as the ledger rule requires (dated snapshots are never rewritten; a factual
defect found in a dated section is recorded as a note like this one, ledger L2760). This note corrects
the citation forward.

**What was stale.** Lines 188-189 above read `actions/upload-artifact` v7.0.1 commit
`043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` (offline-ci.md L203-210). PR #743 (`81081ca4`, parents
`ce865c91` / `af49536c`) bumped all four upload steps in `.github/workflows/validate-skills.yml` to
**v7.0.2**, commit `cf430e030ddbb5b0abf93d22962f4752f3646cd9`, and updated no documentation; the
second surface, `docs/offline-ci.md` L207-208, was corrected in the same change that appends this note.

**The current pins, measured.** `git grep -n upload-artifact -- .github/workflows` returns exactly four
lines, at `.github/workflows/validate-skills.yml` L278, L365, L421 and L477, each
`actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9  # v7.0.2`; and
`git grep -n -e v7.0.1 -e 043fb46d -- docs/offline-ci.md` now returns nothing.

**Scope.** This note records a citation correction on a live page and nothing else. The dated
2026-10-11 measurements on this page — the durations, the skipped-window footnote and every figure in
S5 — are unchanged and are not re-measured here. No workflow file was edited by this change: the pin
in `.github/workflows/validate-skills.yml` was already correct.
