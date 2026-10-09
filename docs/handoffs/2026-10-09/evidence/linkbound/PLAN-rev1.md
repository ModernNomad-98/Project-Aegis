# LINK-BOUND-1 — bound Markdown link unwrapping without changing reports

Stage A planner: `/root/linkbound_plan`.

**SD-A: COMPLETE.** This captured plan is ready for an independent Stage B
audit. It is not a candidate implementation or a merge disposition. Source
work and publication require the coordinator's subsequent stage assignment.
The protected-file merge limitation below remains unresolved.

## Request, timing, and evidence boundary

The owner's current instruction is **"Keep working on backlogs until I get the
info"** in the Project Aegis conversation. The coordinator assigned this agent
Stage A planning only, read-only source, with no provider calls, source edits,
credentials, implementation, or PR writes. The historical requirement is
AEGIS-APR-103's owner decision: **"Grant + merge now, track the bound as a
follow-up"**, recorded at `docs/approvals/APPROVAL_REGISTER.md:3246-3250`.

- Recorded start: **2026-10-09 09:42:24 UTC**.
- Initial active-work ETA: **30–45 minutes**, supplied in the stage assignment.
- Finish and measured wall time: recorded in the adjacent `STAGE-A-RECEIPT.md`
  after this plan is finalized and hashed; active time is **not measured**.
- Planning source snapshot M: `8e11c8f4c2777265e254057ce0fa1e52f0cf03bf`.
- Local object source: `C:\src\Codex Projects\Project Aegis\cadence\impl`.
  That checkout's observed head was
  `e834ea7079060314a2bc4f4275938b1cf01e0f7d`; reads of relevant files were
  checked against M with an empty `git diff M -- <listed paths>`.
- The older source clone at `C:\src\Project Aegis\Project-Aegis` was observed
  at `f7c48212bce508512fac4d45f3aa2e43c05b59a4`, with pre-existing untracked
  `artifacts/recovery/` and `artifacts/reviews/`. It was not changed.
- **UNVERIFIED:** current GitHub main, PR state, hosted check results, bot review
  availability, and provider applicability. There was no successful network
  read. A local `git ls-tree` verification of #648 in the partial cadence clone
  unexpectedly attempted a lazy fetch; it failed to connect. The successful
  #648 blob read came earlier from the older source clone's local object store.
  Subsequent Git verification sets `GIT_NO_LAZY_FETCH=1`. This incidental failed
  attempt is disclosed; it is not live evidence or provider authorization.
  M is a pinned local planning baseline, not a claim about live main.

Source-library role was corroborated by M's README beginning `# Project Aegis`,
`docs/skills-catalog.md`, `scripts/validate-skills.py`, and
`artifacts/audits/skill-contract-audit-baseline.json`. `AGENTS.md` and the
canonical `docs/delivery-workflow.md` were read. Their seven-stage separation
and current owner instructions bind every subsequent stage.

## What changes, why, and blast radius

Replace `unwrap_links`' repeated scans and accumulated-string rebuilding with
incrementally maintained open-construct state and one assembly per output
group. Keep the current checker's supported syntax, grouping, span map,
diagnostics, counts, and exit behavior. Add focused adversarial and
compatibility tests in its existing unittest module.

At M, an unclosed link label or destination causes each continuation line to
rescan and recopy the preceding paragraph. The input is repository Markdown,
including contributor-controlled text. The checker now runs over the
repository's own pages in `validate-skills`; a long paragraph can consume the
validation job's time. No hosted timeout or attack is claimed to have occurred.

The blast radius is the preprocessing of code-blanked Markdown before `LINK`
matching and its source-line offsets. A faulty optimization could silently
hide a broken wrapped link, invent a link across a block boundary, move a
diagnostic to the wrong line, or truncate the tail while reporting success.
No application runtime, database, tenant authorization, deployment, or provider
configuration is involved.

### Exact candidate file scope

Only these two tracked files may change:

1. `scripts/ci/check-markdown-links.py` — incremental unwrap state, chunk
   assembly, and narrowly associated comments/private helpers.
2. `scripts/tests/test_markdown_links.py` — deterministic compatibility
   cases and bounded adversarial performance regressions using synthetic
   temporary data.

No additional tracked fixture is necessary: the current test file already
creates temporary Markdown files for wrap, missing-target, and line-number
cases. Existing tracked fixtures remain unchanged. This is a scope lock, not
permission to edit every function in the checker.

**Outside scope:** `.github/**`, the protected-path pattern, branch settings,
approval register, delivery policy, dependency files, docs/corpus edits,
validator code, fixture files, new commands or flags, changed output schema,
network access, and new dependencies. Also excluded are a general Markdown
parser rewrite, expanded Markdown syntax, the historical commit-message
count correction in APR-103, and separate worst cases in `LINK`,
`blank_code_spans`, or repeated `source_line_at` lookups. This plan promises a
linear bound for **unwrapping only**, not for the entire link checker on every
possible input. A newly discovered correctness defect is reported and routed
back through A/B rather than repaired opportunistically.

## PROVEN — independently observed basis

Read-only Git commands used this command prefix, abbreviated `gitM` below:

```powershell
git -c safe.directory='C:/src/Codex Projects/Project Aegis/cadence/impl' -C 'C:\src\Codex Projects\Project Aegis\cadence\impl'
```

The per-command `safe.directory` setting avoids changing repository or global
Git configuration. It is needed for this sandbox account's ownership check.

| Evidence | Command or location | Observed result |
| --- | --- | --- |
| M resolves | `gitM rev-parse --verify '8e11c8f4c2777265e254057ce0fa1e52f0cf03bf^{commit}'` | M resolves to that exact commit. |
| Unchanged checker since #648 | `gitM ls-tree M -- scripts/ci/check-markdown-links.py scripts/tests/test_markdown_links.py`, compared with `git -c safe.directory='C:/src/Project Aegis/Project-Aegis' -C 'C:\src\Project Aegis\Project-Aegis' ls-tree 33c81fdabc6e8e59a8378c2206b551fc82ff31dd -- scripts/ci/check-markdown-links.py scripts/tests/test_markdown_links.py` | Checker blob `efa65c95f5444e50867e832a688c8351cd332d2c`; test blob `21c167c25da3fbf15b0d7c9c58b58b757f42e888`, both identical at the two revisions. |
| Source of the bound | Checker at M, lines 148–171 and 220–250 | Each join calls `link_text_open(current)` or `link_target_open(current)` on a growing string; line 244 builds `head + " " + tail` again. State-only optimization would leave repeated copying. |
| Current automated reachability | Workflow blob `66cca67d0390e739190939abccae99125cb56543`, lines 219–227 | The tracked `.md` set, excluding `scripts/tests/fixtures/`, is passed to the checker in `validate-skills`. Static invocation is proven; hosted execution was not read. |
| Existing regression suite | `python -B -P scripts/tests/test_markdown_links.py` from the verified checkout with child Git ownership trust scoped to that path | `Ran 23 tests in 3.412s` / `OK`; full output captured in `BASELINE-SELFTEST.txt`. |
| Guard classification | Same workflow, `gate_pattern` at line 528 | Both candidate paths match `scripts/`. |
| Owner record | Register blob `288232321d751aae47e827d44f912f12b75323fc`, APR-103 lines 3232–3312 | Follow-up remains recorded; exact-#648 exception consumed. Search of the register for `APR-103`, `quadratic`, and `unwrap_links` found no later discharge of this bound. |

The APR-103 historical review already requested incremental state and said the
quadratic finding becomes REVISE when the checker enters corpus CI. That is
historical review evidence, not a new review verdict on M. Its old claim that
the checker was unreachable from automation does not describe M's workflow.

### Fresh synthetic baseline

`BASELINE-PROBE.py` loads the exact checker blob through local `git show M:path`
and executes it in memory. It instruments calls and concatenation sites without
changing repository code, then captures small behavior examples. For an initial
`[x` followed by N lines of 64 `a` characters:

| N | Input characters, excluding newlines | Sum of lengths offered to `link_text_open` | Sum of concatenated result lengths |
| ---: | ---: | ---: | ---: |
| 128 | 8,194 | 528,576 | 536,896 |
| 256 | 16,386 | 2,122,112 | 2,138,752 |
| 512 | 32,770 | 8,504,064 | 8,537,344 |
| 1,024 | 65,538 | 34,047,488 | 34,114,048 |
| 2,048 | 131,074 | 136,252,416 | 136,385,536 |

These are exact logical input/copy-length counts, not CPU-instruction counts.
They grow approximately fourfold for doubled input. Because no `]` exists in
this family, the rightmost-close search must inspect the growing prefix; the
repeated concatenation independently copies it. This supplies an analytic
quadratic witness as well as instrumentation.

A second untraced probe used three samples per size on Python 3.14.7 / Windows,
with the same constant-width continuations. `BASELINE-TIMING.json` records all
samples; medians in seconds were:

| N | Unclosed label `[x` | Unclosed destination `[x](` | Clean `xx` control |
| ---: | ---: | ---: | ---: |
| 4,096 | 0.285847 | 0.856907 | 0.001467 |
| 8,192 | 1.433432 | 3.477064 | 0.002699 |
| 16,384 | 5.765254 | 14.978538 | 0.005637 |

Timing is host-specific baseline evidence, not an SLA or proof of candidate
speed. No old 8.4 MB/15-minute claim was rerun. No candidate exists yet.

## Classification and validation depth

Applied `change-classification-gate`: **bug-fix + narrow refactor**, with
regression-test work. The overall change is not `qa-test-only`, because the
checker changes. It touches the security-relevant `scripts/` surface identified
by CONTRIBUTING and the protected merge-guard path set. It does not change an
access policy or the guard. Minimum floors are reproduced failure → passing
regression, and behavior preservation before/after.

Applied `risk-tiered-validation-selector`: both declared paths fall under its
`scripts/**` forced-full rule. **FULL** is the planned validation tier. This is
a planning classification of the explicit file contract; C/E must recalculate
from the actual Git diff, including renames/deletions. No live diff classifier
or new workflow enforcement is claimed.

The PR security answer, if a PR is later created, is **Yes — scripts/**. The
additional external-contribution security review follows CONTRIBUTING/MG5's
actual contributor scope. Do not extend it automatically to an agent-authored
maintainer change, and do not omit the security answer.

## Implementation design to audit before coding

1. Treat a source line/group as chunks with an accumulated effective length.
   Keep an untouched source line byte-for-byte when it consumes no continuation.
   At its first join, apply the current leading-line `rstrip`; each continuation
   keeps the existing single `QUOTE_MARKER` removal followed by the existing
   blank/block check and `strip`. Retain one ASCII joining space, precisely as
   today. Join the chunks once when the group finishes; do not rebuild the
   accumulated prefix on each continuation.
2. Maintain constant-size open-construct state while scanning only each new
   chunk. Match the existing predicates exactly: relative positions of the
   rightmost `[` and `]`; existence/location of the latest `](`; position of
   the rightmost `])`; and whether the suffix following that latest `](`
   contains `)` and/or `(`. These are the current heuristic semantics, not
   balanced-parenthesis or CommonMark semantics. A constant number of linear
   operations on each *new* fragment is allowed. No suffix/whole-prefix rescan
   may grow with the number of previously consumed lines.
3. Preserve the source span output: first `(0, original_line_number)`, then
   `(effective_prefix_length + 1, continuation_source_line)` for each join.
   Maintain the length arithmetically. Preserve every returned group and span
   tuple; leave `source_line_at` behavior unchanged.
4. Keep the current stop rules: EOF, blank/whitespace-only line, and the
   existing `BLOCK_START` matches after one quote-marker removal. The first
   line's own marker is retained. Nested quotes, headings, fences, list items,
   HTML-comment openers, leading indentation, and Unicode whitespace need
   explicit compatibility coverage; do not normalize them differently.
5. No input-size, character, paragraph, or line-count cap; no new skip category;
   no early success. APR-103 permits a loud cap as a different remedy, but this
   plan selects behavior-preserving incremental unwrapping. A cap is a plan
   change requiring A/B revision, not an implementation fallback.

For total input character count L and source-line count N, the selected design
must have **O(L + N) unwrapping time and O(L + N) output/auxiliary space**.
Each original line can be considered only a constant number of times (including
one boundary lookahead), each chunk can be scanned/copied only a constant
number of times, and every output group is assembled once. D must check that
argument against actual loops, slicing, `find/rfind`, regex calls, trimming,
and string construction. A fast benchmark alone does not establish the bound.

## Acceptance criteria

| ID | Objective criterion | Required evidence |
| --- | --- | --- |
| AC1 | The candidate changes exactly the two declared files and introduces no dependency, CLI/output contract, syntax expansion, input cap, or authority change. | Actual base-to-head name/status diff, reviewed hunk inventory, source/fixture comparison. |
| AC2 | `unwrap_links` meets the O(L + N) time and space bound, removing both accumulated-prefix rescanning and repeated rebuilding. | D's amortized code argument plus T2 scaling and timeout regressions, including an old-baseline red result. No whole-checker linearity claim. |
| AC3 | Returned merged strings and source span lists equal the old implementation on the specified compatibility matrix and deterministic generated inputs. | T1 exact tuple comparisons and unchanged existing wrap/code tests. No changed expected result accepted merely because new code differs. |
| AC4 | CLI classification, counts, diagnostic target and source line, exit status, and external-no-fetch behavior remain unchanged; large inputs still expose a real broken tail link. | T3–T5 subprocess results, exact expectations, and nonvacuity checks. |
| AC5 | The original 23 tests remain effective and pass, new relevant tests pass, and the same selected repository corpus produces the same counts and diagnostics before/after. | T6 baseline/candidate outputs, versioned corpus manifest, no fixture or corpus edits, and test nonvacuity evidence. |
| AC6 | The supplied C handoff identifies exact base/head/tree, commands, versions, local outcomes, and every unavailable check. No failed or unrun check is described as green or satisfied by timing evidence. | Immutable C handoff and D's verification of its local claims and declared limits. E/F/G records are later stage duties, not conditions that D must satisfy before those stages exist. |

**Predeclared limits at A:** no candidate head exists, so these ACs are future
implementation obligations and are not claimed MET now. AC1–AC5 and the local
part of AC6 are expected to be verifiable at D on a supplied candidate; an
unavailable mandatory local behavior test returns the plan/implementation for
revision. AC6's hosted exact-head checks, Linux execution if no authorized local
Linux environment exists, GitHub bot availability, provider-suite applicability,
PR publication/readback, and final merge are not verifiable in this Stage A
environment. Their reason is lack of a candidate/provider access and, for merge,
the known protected-path hold. D may mark only those declared portions UNRUN
with the resolving evidence named; E/F/G must carry them. A known failed guard
is a **failure**, never an UNRUN or a green result. An affirmative E disposition
does not satisfy the owner's green-only merge condition.

## Executable test plan

All data is synthetic and local. Python standard-library unit/subprocess tests
are the cheapest reliable layers for these contracts. No browser, screenshot,
live Markdown renderer, provider, database, or product E2E suite is needed for
this two-file contract. The test module remains the CI entry point at workflow
lines 178 and 327; no CI wiring is changed.

| ID / risk | Setup and action | Expected evidence | Layer / owner |
| --- | --- | --- | --- |
| T1 / semantic drift | Add table-driven calls to `unwrap_links` for empty input, one line, two/three/many lines, complete link before an open one, multiple links, label and destination continuations, stray closers, `](` and `])` order, reopened `(` suffix, spaces/tabs/Unicode whitespace, each block boundary, single/nested quote markers, and unchanged code-stripping composition. Compare merged text **and all span tuples** with frozen baseline expectations. Also generate at least 1,000 small cases with a fixed recorded seed from literal fragments covering `[`, `]`, `(`, `)`, `](`, `])`, prose, whitespace and block prefixes; compare against a frozen baseline unwrap oracle in the test module. Bound generated case size so the old oracle is cheap. | Exact equality. Independent explicit expected cases protect against copying an incorrect oracle; the frozen oracle checks compatibility over combinations. No generation from the candidate's own state machine. | Unit; C writes, D audits. |
| T2 / quadratic regression | In a child process, time only `unwrap_links` over `[x` + N copies of `a`*64, and `[x](` + N copies of `a`*64, at N=4,096/8,192/16,384. Warm up once at N=256; use median of three timed calls at each size. Record raw samples. For each shape require T(16,384) <= 6*T(4,096) + 0.05 seconds, and T(16,384) < 5 seconds. A 30-second subprocess timeout is failure, never skip/pass. The clean control confirms ordinary input remains processed. | The current captured medians violate both size-family ratio limits and the large-shape absolute limits on this host. C must actually demonstrate the new regression fails with the frozen old checker and passes with the candidate. D requires the structural O(L+N) argument too. Threshold or size changes require A/B revision with evidence, not silent widening after a failure. | Unit/performance; C writes, D rechecks, E reruns on available supported hosts. |
| T3 / silent truncation | At N=16,384, write `[x\n` + (`a`*64 + `\n`)*N + `](missing-tail.md) and [other](also-missing.md)\n`. For a second case, write `[x\n` + the same N lines + `\n[tail](missing-tail.md)\n`. Run CLI in subprocess with a 15-second test harness timeout. | First case: exit 1, broken count 2, `missing-tail.md` at line 1 and `also-missing.md` at line 16,386. Second case: exit 1, broken count 1, `missing-tail.md` at line 16,387. No lost tail. The test-harness timeout imposes no checker input cap. | CLI integration; C/D/E. |
| T4 / block/code false positives | Use the existing code fixtures plus temporary blank, heading, fence, bullet/numbered-list, quote-depth and HTML-comment boundaries; keep complete links adjacent to wraps and broken links after boundaries. | Same baseline counts and diagnostics; code mentions remain absent; source positions point to actual link openers. Existing two/three-line wrapped-twin counts remain exact. | CLI integration; C/D/E. |
| T5 / public report contract | On a small temporary mixed corpus, compare old and candidate normal output, JSON, quiet behavior and return code using the same absolute fixture paths: valid file/dir/anchor, missing target, dead anchor, external URL, site-absolute path, fragment in non-Markdown, and missing input. | Byte-equal output/exit where deterministic; identical JSON keys/counts; external references are counted without fetching. Missing input retains exit 2; broken/dead links retain exit 1. | CLI integration; C/D/E. |
| T6 / existing corpus and regression preservation | Run the original 23 cases before/after; new total is counted from the test runner. Derive a sorted tracked `.md` manifest excluding paths containing `scripts/tests/fixtures/`, matching the current workflow's predicate exactly. On Windows run bounded batches within command-line limits, using identical membership/order and targets for old/candidate. Record manifest hash, all per-batch codes/diagnostics/counts and aggregate totals. | Same selected files and identical counts/diagnostics before/after; all selected files checked once; no skipped failing batch; no fabricated fixed corpus count. Baseline failures, if any, are preserved and reported rather than edited away. | Unit + corpus integration; C/D/E. |

For the old/candidate comparison, use the pinned baseline script exported to a
synthetic scratch directory and a candidate script from the reviewed checkout;
fixture targets remain the same absolute paths. No Git network fetch is needed
to run the local old-baseline regression. A small frozen oracle is test-only;
production must not retain the quadratic code as a fallback. Tests must retain
failures if a tail scan is removed or a line map is wrong; neither total runtime
alone nor `broken: 0` alone is adequate evidence.

### Negative-path matrix

| Surface | Unauthorized | Invalid | Expired | Missing | Duplicate | Conflicting | Out-of-order |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Unwrap state and assembly | Not applicable: pure string operation, no identities/grants | T1/T2 malformed and unterminated punctuation | Not applicable: no clock/session | T1 empty/missing closer and T2 missing termination | T1 repeated punctuation/links | T1/T4 block boundary versus open state | T1 reordered closer/opener and target markers |
| CLI diagnostics | T5 external-no-fetch contract; no new network authority | T4 code-like/unsupported syntax remains baseline behavior | Not applicable: no expiry semantics | T3/T5 missing targets/inputs/anchors | T1/T5 repeated links counted per occurrence | T3/T4 adjacent link versus span ownership | T1/T4 source-line offsets preserve input order |
| Validation and publication | Protected-path hold and separate stage authority; no bypass planned | AC1 rejects scope drift | Fresh head/base/body binding required by workflow | AC6 missing runs named with resolution | One holder per PR/stage; no duplicate handoff ownership | Red guard versus green-only grant stays a hold | A→B→C→D→E→F→G; moved evidence returns to the responsible stage |

### Full-tier validation inventory for E

Use the commands and isolation rules from the candidate's
`.github/workflows/validate-skills.yml` and `docs/offline-ci.md`; collect output
under a new scratch evidence directory. Re-derive the inventory if main moves.
The current inventory includes:

- Environment/dependency verification (`python -P -m pip check`,
  `scripts/ci/check-environment.py`) using already authorized installed runtimes;
  do not silently install or fetch dependencies to make a missing environment
  appear available.
- `python -B -P scripts/tests/test_offline_ci.py`;
  `python -B -P scripts/tests/test_validator.py`;
  `python -B -P scripts/validate-skills.py`;
  `python -B -P scripts/tests/test_audit_skill_contracts.py`;
  `python -B -P scripts/tests/test_markdown_links.py`;
  the exact derived corpus run from T6.
- `python -B -m tools.behavioral_eval_runner self-check` and
  `python -B -m unittest discover -s tools/behavioral_eval_runner/tests -p 'test_*.py' -v`;
  offline Scenario A evidence acceptance using the applicable existing
  PowerShell Core/Desktop scripts. These are synthetic offline checks, not
  authorization for live BER/Stage 4B/provider runs.
- The existing setup bridge, setup-routing, and delivery-control suites where
  required by the selected full bundle; record unavailable platform/dependency
  coverage explicitly. Named existing entry points are
  `node --test tools/aegis_setup/host_bridge/bridge.test.ts`,
  `python -B -m unittest discover -s tools/aegis_setup/tests -p 'test_*.py' -v`,
  and `python -B -m unittest discover -s tools/aegis_delivery_control/tests -p 'test_*.py' -v`.
- `git diff --check`, exact changed-path review, and
  `python -B -P scripts/check_dco.py --range <base>..<head>` once commits exist.

The workflow's Windows/tools jobs are selected conditionally; do not claim
their hosted execution on a script-only diff. At E read actual job results and
record justified skips as skips. Windows and Linux executions of the changed
checker tests are required evidence before claiming cross-platform proof; if
one is unavailable, it remains a declared AC6/E gap with the required
environment named. An unrelated existing failure is reported with evidence,
not repaired by expanding this change or re-labelled a pass.

## Protected-path and authority hold

Both candidate files match the current `gate_pattern`. APR-103 was one use for
PR #648 at `33c81fdabc6e8e59a8378c2206b551fc82ff31dd`; it states consumed and
forbids extension to another PR/head/check. APR-047's standing exception names
four BER files, none of which is a candidate path here. APR-048 also says its
administrator merge grant does not waive red `gate-guard`. The owner's current
conversation condition is **"for merge, once local and github checks are green,
approved for merge"**, and the later selected disposition is **"Keep green-only
hold (recommended)"** for the existing protected-file fix.

Consequently **there is no proven merge route for LINK-BOUND-1's two-file
candidate under the current constraints**. No waiver request is part of this
plan. Do not change the guard, move code outside protected paths, reinterpret
old exceptions, claim a rerun cures a deterministic protected-path failure, or
merge red. Planning and an independently audited local candidate can be useful
backlog progress if separately assigned, while the merge remains held. An owner
decision about policy is outside this lane and cannot be fabricated from a
generic work or administrator-merge grant.

## Stage route, handoff, and stop conditions

| Stage | Distinct holder's task and required handoff |
| --- | --- |
| A | This agent supplies the captured plan, classification, baseline evidence, source/authority boundaries, and self-authored skills rows. |
| B | Astra xhigh agent independent of A audits this exact plan hash, the owner record, two-file scope, heuristic equivalence, complexity proof obligation, test thresholds, and merge hold. Post/capture SD-B against this revision. |
| C | Separate Sol high agent, only after B ACCEPT and coordinator assignment. Refresh source/base and lane ownership under applicable authority; preserve dirty roots; work in an isolated checkout. Follow the accepted plan, run baseline/new tests, sign commits if publication is authorized, and bind head/tree/base plus changed/untouched paths and raw checks. Do not invoke a MANUAL-ONLY skill absent a human invocation. |
| D | Separate Astra xhigh agent checks AC1–AC6 individually against exact head/tree/base, traces state transitions against old predicates, proves the linear unwrap bound, checks no test weakens an expectation, independently reproduces representative compatibility/performance cases, and records MET/NOT MET/declared UNRUN. |
| E | Separate Sol high agent executes the selected full validation inventory at the reviewed head; independently reads hosted checks only under provider authorization. Every gap is explicit with resolving action. No green claim for the known guard failure. |
| F | Separate Astra xhigh reviewer verifies the candidate, D/E records, exact source-authored stage rows, security answer, reconciliation witness, and current bound-field hash. Accept only the evidence actually supplied. |
| G | Separate authorized merger re-derives current head/base/body/checks and MG1–MG5. **Current expected disposition: NOT MERGED**, because the protected-file condition conflicts with green-only merge authority. No stage completion silently changes that condition. |

No agent performs two stages on this change; no two agents hold the same PR.
Each holder reports start/finish UTC and measured wall time, with active time
only if measured. The initial 30–45-minute Stage A ETA is not a source-delivery
or merge ETA. Further implementation/review estimates are **UNMEASURED** and
are supplied by their assigned holders; merge ETA is **unknown** while held.

Return to A/B if predicate semantics differ, a performance threshold needs
revision, a new tracked file is needed, a candidate introduces a cap/parser
change, protected policy changes, or current main invalidates the captured
basis. Stop a denied operation rather than retrying through another identity
or channel. Continue independent local work only within that holder's grant.

The continuation package for B is this exact plan plus `BASELINE-PROBE.py`,
`BASELINE-PROBE.json`, `BASELINE-TIMING.py`, `BASELINE-TIMING.json`, `BASELINE-SELFTEST.txt`, and
`STAGE-A-RECEIPT.md`. No source candidate, branch, PR, provider result, or merge
is produced by Stage A. No decision-ID rule is changed; SD-A through SD-G and
MG1 through MG5 remain governed by `docs/delivery-workflow.md`.

## Applied skills and self-authored rows

No installed skill owns general Stage A plan writing; that disposition is
procedural under the delivery workflow. The following skills were actually
read and applied. `ai-task-decomposer` was inspected and rejected as a fit
because this is already one small change; `systematic-debugger` was inspected
but **not invoked** because it is MANUAL-ONLY and the cause is already isolated.
The table below is a self-authored Stage A source for later exact attributed
copying; it is not a claim that any PR body has been edited.

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [change-classification-gate](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/change-classification-gate/SKILL.md) | A / `/root/linkbound_plan`, rev1 | Inspected exact checker/test/workflow surfaces; classified bug-fix plus narrow refactor; locked two candidate paths and separated implementation validation from protected-path merge authority. | PLAN-rev1.md classification, AC1–AC6, and protected-path hold; no source edits or successful provider read. An unexpected failed Git lazy-fetch attempt is disclosed in the evidence boundary. |
| [test-plan-designer](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/test-plan-designer/SKILL.md) | A / `/root/linkbound_plan`, rev1 | Mapped performance, compatibility, line-map, code/block-boundary and truncation risks to T1–T6; selected unit/CLI layers and complete negative-path matrix. | Baseline 23 tests passed; baseline instrumentation and timing reproduce growth; candidate tests and hosted results remain UNRUN because Stage A produced no candidate. |
| [risk-tiered-validation-selector](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/risk-tiered-validation-selector/SKILL.md) | A / `/root/linkbound_plan`, rev1 | Applied the scripts/** forced-full rule to the declared two-file scope and named the existing check bundle; required reclassification from the real diff at C/E. | Planned FULL tier; no new classifier enforcement or full-tier execution claimed; unavailable platform/hosted coverage declared under AC6. |

## Planning artifact hashes

These hashes bind the evidence already captured. The finalized plan's own
SHA-256 and finish receipt are recorded separately to avoid a self-referential
hash field.

| Artifact | SHA-256 |
| --- | --- |
| BASELINE-PROBE.py | `EFED9E2DFC07A7ED2243972401AD239923E90B103E95009893D8F130EEC78D4E` |
| BASELINE-PROBE.json | `2E94F763A114B6A962743352CE41207708F63CF5CC4A1B5211F8951D0ABA1E87` |
| BASELINE-TIMING.py | `CC0228071BFA105CCE90C9666FBA4E737225DA37720ECBAAD8DE7FEAC06AFDA4` |
| BASELINE-TIMING.json | `AD562652DA6122C400AFC330C4DD9E9F8223A9946B9BECFA3B062B7C70AF839B` |
| BASELINE-SELFTEST.txt | `B9B1055A2F6CB4B169B2A7E09194274383B4BC4B9B5C91F7FE04B4AF2D7CCF0A` |
