# LINK-BOUND-1 — independent local implementation audit

**SD-D: REVISE.** The local code review found no implementation defect in the
supplied tree, and AC1–AC5 are MET for that tree. AC6 is **NOT MET** because no
candidate commit H exists. This report is local audit evidence, not an
affirmative formal Stage D exit or permission to enter Stage E.

Auditor: `/root/linkbound_d_local`, independent of A, B and C. This assignment
permits a source-read-only audit and synthetic offline probes, with scratch
reports outside the repository. No provider, signing, PR or merge action was
performed. Initial ETA: **25–45 active minutes**. Recorded start:
**2026-10-09 10:15:11 UTC**. Finish and wall duration are in the final timing
section. Active time was not measured.

## Exact reviewed objects and inputs

Repository/worktree: `C:\src\Codex Projects\Project Aegis\linkbound\impl`.
The README heading and three source-package landmarks establish the Aegis
source-library role. `AGENTS.md` and `docs/delivery-workflow.md` were read.

| Object or artifact | Independently verified identity |
| --- | --- |
| Local base M and current HEAD | `8e11c8f4c2777265e254057ce0fa1e52f0cf03bf` |
| M's tree, **not** candidate tree | `785ae6aac5ee884751c1da4911c7bebe8d6c7cf8` |
| Candidate tree T | `64d2cf8a83fb22b7d4aef49d4f17e2c5ce3a5191` |
| Candidate commit H | **Absent**; HEAD still resolves to M |
| Candidate checker blob | `ac76863be5f6a9cbb93fbeaa9d59472ac1e2fc4c` |
| Candidate test blob | `5483c58441962370f8b18f40d106bc044a272bfc` |
| Baseline checker blob | `efa65c95f5444e50867e832a688c8351cd332d2c` |
| Accepted `PLAN-rev1.md` SHA-256 | `82D2BC9B440C00C7A6AAF044C393CBCD8CAD509213D99BF14F168C9E35CF459C` |
| B `STAGE-B-AUDIT-rev1.md` SHA-256 | `8CE748F2C9368A684D50242E020EEFDD7E3C590B45E48ECC976ABECABAC1BFE7` |
| C `STAGE-C-HANDOFF.md` SHA-256 | `6972F0CB51370AA0942311B11656EFBB94BB81855A3F338715EEB72F04F69772` |
| `CANDIDATE.patch` SHA-256 | `117D9F124D519F58492888D2CCEE44C37C82872CFFD67E45CB00958A8D193A63` |

The staged name/status set is exactly two modifications:

- `scripts/ci/check-markdown-links.py`: +64/-5.
- `scripts/tests/test_markdown_links.py`: +205/-1.

`git cat-file -t T` returned `tree`; `git diff --cached --exit-code T --`
returned 0 with no diff. Thus the existing immutable tree and the index have
the same content, without rerunning `git write-tree` or modifying the index.
`git diff --name-status` showed no unstaged change. The reverse cached patch
check and staged whitespace check passed. The same state was reobserved after
all probes; only the two intended staged paths remain. A tree identifies
content but does **not** identify a candidate commit or satisfy the workflow's
head requirement.

All Git object reads set `GIT_NO_LAZY_FETCH=1`. The command prefix was:

```powershell
git -c safe.directory='C:/src/Codex Projects/Project Aegis/linkbound/impl' --no-optional-locks -C 'C:\src\Codex Projects\Project Aegis\linkbound\impl'
```

No Git configuration was written. The independent Python probe applies the
same ownership trust via process-local `GIT_CONFIG_COUNT/KEY_0/VALUE_0` so the
unchanged fixture test's child Git read can run. Runtime versions observed:
**Python 3.14.7**, **Git 2.55.0.windows.5**, on Windows.

## Finding and disposition

**D-1 — workflow blocker: immutable implementation head is missing.**
`docs/delivery-workflow.md:130` says SD-C COMPLETE requires the commit SHA,
its resolved tree and base; `:42–54` makes an affirmative predecessor the next
stage's entry condition; `:181` carries the head, tree and base into D. The C
handoff's opening status, `SD-C: LOCAL CANDIDATE COMPLETE; NO COMMIT OR PR`,
honestly describes useful local work but is not a normative SD-C COMPLETE.
The unchanged HEAD and different candidate tree reproduce the gap.

Failure scenario: treating T as H would allow an audit to flow onward without
the fixed commit/base diff the canonical rule requires. **Remediation:** carry
`SD-C: INCOMPLETE` while H is absent. In an appropriately authorized environment
where the signer is available, C can create a commit for the reviewed T, record
H/T/M and signature/DCO evidence, and supply a corrected handoff. D must then
reobserve H's tree and base and issue a fresh head-bound disposition. A changed
tree or base needs corresponding re-audit; this local report is not silently
rebound. No request to bypass GPG permissions, use an unsigned substitute,
change configuration or call a provider is made by this report.

The inability to sign is reported by C as keyring permission failures; I did
not access the keyring or repeat that attempt. **H's absence is independently
proven; the detailed GPG failure is C-reported evidence.** No other code-review
finding was established in the two-file diff. The protected-path merge hold
below is a separate known gate, not an implementation defect.

## Acceptance criteria

The following keeps all six accepted criterion texts and assesses the supplied
local candidate. `MET` here binds to T/M; it is not an assertion that an H-based
formal stage exists.

| ID and accepted criterion | Result and evidence |
| --- | --- |
| **AC1:** The candidate changes exactly the two declared files and introduces no dependency, CLI/output contract, syntax expansion, input cap, or authority change. | **MET for T/M.** Git reports exactly the two allowlisted paths; all hunks and surrounding callers were reviewed. Production additions are private state plus unwrap assembly. CLI, resolver/reporting, code stripping, patterns, fixtures, corpus, dependencies, policies and workflow are unchanged. The test-only checker override supports the declared baseline regression. Formal base-to-H binding remains absent under AC6. |
| **AC2:** `unwrap_links` meets the O(L + N) time and space bound, removing both accumulated-prefix rescanning and repeated rebuilding. | **MET for T.** Structural argument below covers all scans, allocations and loop advances. Candidate T2 passed unchanged thresholds. Independently rerunning the same new T2 on the exact old blob failed on the label ratio and destination timeout. The bound applies to unwrap only. |
| **AC3:** Returned merged strings and source span lists equal the old implementation on the specified compatibility matrix and deterministic generated inputs. | **MET for T.** Candidate T1's explicit expectations and 1,200 fixed-seed cases passed; frozen oracle was compared with the baseline source. Independent probes compared 55,987 punctuation strings and 5,000 seeded line sets with the actual old module. Every merged string and span tuple matched. Existing wrap/code cases remain unchanged and passed. |
| **AC4:** CLI classification, counts, diagnostic target and source line, exit status, and external-no-fetch behavior remain unchanged; large inputs still expose a real broken tail link. | **MET for T.** All T3–T5 tests passed, including 16,384 continuation lines, exact broken counts 2/1 and diagnostic lines 1/16386/16387. Old/new normal, JSON, quiet and missing-input reports were reproduced byte-for-byte. Static review confirms external targets still take the unchanged non-fetch branch. Tail-discard and incorrect-line scratch mutants both failed the large-tail test. |
| **AC5:** The original 23 tests remain effective and pass, new relevant tests pass, and the same selected repository corpus produces the same counts and diagnostics before/after. | **MET for T.** All 23 original test method ASTs are identical; baseline 23 and candidate 29 tests passed independently. Captured seven-batch evidence was verified against raw files and the exact 619-path manifest; no corpus/fixture edits. One complete 90-file batch was independently rerun. See the explicit distinction between verified captured evidence and reruns below. |
| **AC6:** The supplied C handoff identifies exact base/head/tree, commands, versions, local outcomes, and every unavailable check. No failed or unrun check is described as green or satisfied by timing evidence. | **NOT MET.** The handoff honestly records M/T, commands, versions, outcomes and limitations, but candidate H is absent. This is a missing mandatory local artifact, not one of A's declared hosted/platform gaps. D cannot ACCEPT. The named hosted/platform checks remain separately UNRUN as declared at A. |

## Code argument: heuristic equivalence and complexity

Relevant candidate anchors: `_OpenLinkState` at checker `:174–216`; unchanged
old predicates at `:148–171`; unwrap at `:229–309`; caller and diagnostic
mapping at `:377–385`. The checker still applies `strip_code` before unwrap,
then uses the same `LINK.finditer`, path/anchor classification and line lookup.

**State invariant.** After every `add(text)`, `last_open` and `last_close` are
the rightmost `[` and `]` positions of the accumulated group. `last_target` is
the rightmost `](` position, and `last_closed_target` the rightmost `])`.
`previous` retains the previous character across chunk calls, so a marker
straddling two calls is handled. On a new `](`, both suffix flags reset after
processing its `(`. This excludes the marker's opening parenthesis from the
suffix, exactly as old `line[line.rfind("](")+2:]` does. Subsequent `(` and `)`
set the corresponding flags until the next marker. Before any `](`, flags
cannot affect the result because `last_target >= 0` guards them.

Consequently `open()` is the disjunction of the unchanged two old predicates:
rightmost `[` after rightmost `]`, or an existing latest target marker with
rightmost `[` after rightmost `])` and either no suffix `)` or a suffix `(`.
This intentionally preserves the old heuristic's unusual reopened-parenthesis
behavior; it does not reinterpret it as balanced Markdown syntax. The
independent predicate enumeration uses six characters `[]()a `, lengths 0–6,
and single-character `add` calls, checking marker adjacency across chunks.

**Whitespace and group invariant.** Initial `rstrip` can remove whitespace but
no punctuation used in those predicates. It therefore preserves the open/closed
answer even though the untrimmed original is returned when no join occurs.
On a join, the same one quote marker is removed; the same blank/block test
runs; the tail has the same `strip`; exactly one ASCII space is appended.
Every appended tail is nonempty and has no trailing whitespace, so the old
next-iteration `current.rstrip()` was a no-op and need not be repeated.
Maintained `length + 1` is precisely the previous effective prefix length
plus the joining space. The unchanged `(0, source_line)` and each appended
span therefore agree with the old implementation.

**Time.** Let L be total source characters and N the number of input lines.
`index` advances once for each consumed source line; every line becomes either
a group head or one continuation. A rejected boundary can be inspected once
as a lookahead and once as the next head. Each first-line `rstrip`, quote-marker
substitution, blank `strip`, accepted tail `strip`, anchored `BLOCK_START`
match and `state.add` scans only that line or new fragment a bounded number of
times. The fixed anchored regexes have no nested ambiguous repetition; their
digit/whitespace scan remains linear in the examined line. No growing prefix
is passed to `find`, `rfind`, slicing, regex or trimming inside the continuation
loop. `open()` and length/span updates are constant work under the standard
index-arithmetic model. Appends are amortized constant work. Each group is
assembled by one `join`, copying its chunks once. Joining spaces contribute
at most O(N). Total unwrap work is therefore **O(L+N)**.

**Space.** The state holds a constant number of scalar values. Chunks, spans
and output groups have O(N) entries and O(L+N) aggregate characters; trimming
and quote removal create at most a constant number of copies of each line.
Peak auxiliary plus output space is **O(L+N)**. The old quadratic oracle exists
only in the test module and is used on bounded small cases. Production has no
quadratic fallback or cap. This proof says nothing about the separate `LINK`
matcher, code blanker or repeated `source_line_at` searches.

## Independent executions and evidence integrity

The exact reusable audit driver is `STAGE-D-PROBE.py`. Run from
`C:\src\Codex Projects\Project Aegis`:

```powershell
python -B linkbound/STAGE-D-PROBE.py static
python -B linkbound/STAGE-D-PROBE.py semantic
python -B linkbound/STAGE-D-PROBE.py corpus
python -B linkbound/STAGE-D-PROBE.py old-red
python -B linkbound/STAGE-D-PROBE.py suite
python -B linkbound/STAGE-D-PROBE.py mutants
```

Every driver command returned 0, meaning its asserted expected result held.
The old regression and two mutant child runs returned **1**, as intended;
their failures are preserved in raw files and not described as candidate
failures or as skipped tests. No heavy workload was launched in parallel with
the performance measurements. The driver exports the old checker directly
from local M and verifies its Git blob identity; it does not use the copied
test oracle as independent truth.

| Run | Observed outcome |
| --- | --- |
| Candidate `python -B -P scripts/tests/test_markdown_links.py -v` | **29 tests OK**, runner 6.497 s, measured subprocess wall 6.626302 s. Includes all six new methods and original 23. |
| Baseline `CheckerReportTests SlugTests FixtureTree -v`, with test-only `AEGIS_LINK_CHECKER` pointing to exported old checker | **23 tests OK**, runner 3.311 s, subprocess wall 3.437032 s. The baseline export has the original checker basename so `SlugTests` imports that module correctly. |
| Original test integrity | AST comparison: **23 of 23 original test methods identical**, including assertions and decorators; no original method deletion or skip. Actual diff contains only import/setup support plus six new methods. |
| New T2 against baseline | **Exit 1: failures=1, errors=1**, runner 52.002 s. Open label N=16384 median **5.7436569 s**, permitted ratio value **1.8209996 s**; it also exceeds the 5 s absolute bound. The destination child exceeded its unchanged **30 s timeout**, an error rather than a skip. Raw open-label samples and traceback retained. |
| Independent state/semantic probes | **55,987 predicate strings** equal old predicate answers; **5,000** line sets at seed **20261009** equal old merged strings and all spans. Candidate's separate 1,200 cases use seed 103648. |
| Tail-loss scratch mutant | Replacing only appended tail content with empty text yields `broken: 0`, exit 0. T3 rejects it at test `:188` because exit 1 is required. |
| Wrong-map scratch mutant | Replacing only continuation source line with 1 leaves two broken links but reports the second at line 1. T3 rejects it at test `:191` because line 16386 is required. |
| Same-path mixed CLI | Old/new bytes and exit equal: normal/JSON/quiet exit **1**; nonexistent input exit **2**. JSON counts are files 1, checked 5, anchors 2, broken 1, dead 1, external 1, skipped 2. |
| Independently rerun corpus sample | First 90 manifest paths, both exit **0**, identical raw output SHA-256 `050e5d1c80d51ad609a50d19672cd0589b09d349c48027b5cd78fa41155a3601`; 117 checked links, 2 anchors, 0 broken/dead, 16 external, 0 other skips. |

The predeclared T2 sizes, three-sample medians, warmup, ratio/absolute limits
and timeout were not weakened. T3 asserts real broken-tail diagnostics rather
than just fast completion. Existing code/fence, two/three-line wrap, adjacent
link and quote tests remain effective. No migration, dependency, configuration,
workflow or authority change appears in the diff. No separate accepted ADR
covering this pure helper was identified in the plan/source evidence reviewed;
the accepted plan and current helper contracts are the applicable design basis.

### The 619-file claim

This audit **did not rerun the whole seven-batch corpus**; that would duplicate
the captured C work without resolving another code risk. Instead it verified:

1. Current `git ls-files -z '*.md'`, sorted and excluding paths containing
   `scripts/tests/fixtures/`, reproduces the stored manifest byte-for-byte.
   There are **619 unique paths**, SHA-256
   `d477b804aa9ead2e050b38322acae1e5c679e162c2af0f8a15900766247b46e6`.
2. The comparison script partitions that list into six batches of 90 and one
   of 79, with identical ordered absolute targets for old and new; no hidden
   filter or successful-only aggregation exists.
3. Each of the seven raw old/new report pairs is byte-identical, agrees with
   its recorded hash/length, has empty captured stderr and recorded exit 0.
   The report summaries contain **90/90/90/90/90/90/79 files** respectively.
4. Summing those summaries gives **619 files, 3,231 checked links, 877 anchors,
   0 broken links, 0 dead anchors, 1,811 external skips, 0 other skips**.
5. The source diff contains no corpus or fixture edit, and an independent run
   of the first complete batch reproduces C's bytes exactly.

Thus the full result is **verified captured C execution evidence**, with a
representative fresh reproduction. It is not seven newly rerun D batches or
hosted CI proof. Commands, per-batch summaries, hashes and fresh results are
in `D-evidence/corpus.json` and `comparison/`.

## Classification and remaining limits

Applied `change-classification-gate`: **bug fix + narrow refactor**, with the
two-file scope locked. The old-failure/new-pass and preservation floors are
satisfied locally. Applied `risk-tiered-validation-selector` against the
actual staged paths: each matches its `scripts/**` forced-full rule, so the
aggregate is **FULL**. The full bundle remains a later Stage E responsibility;
this audit is not Stage E and does not claim its execution.

Both paths match `.github/workflows/validate-skills.yml:528` through
`scripts/`; the guarded branch at `:534–542` exits 1 for matches. This is a
static policy consequence, **not a newly observed hosted failure**. APR-103 at
`docs/approvals/APPROVAL_REGISTER.md:3232–3312` is consumed and explicitly does
not cover another PR/head/check. The owner's green-only merge condition still
holds. No local performance result changes that authority or supplies a merge
route.

**PROVEN in this audit:** input artifact identities; exact local M/T/index
relationship and two-path scope; unchanged original test bodies; local old-red
and candidate-green regressions; the structural unwrap bound; representative
semantic/CLI/corpus equivalence; full captured corpus manifest/report integrity;
mutation nonvacuity; and the lack of a candidate H.

**UNRUN / UNVERIFIED and resolving evidence:**

- Candidate signature and DCO: require an authorized C commit H and subsequent
  verification, including `scripts/check_dco.py --range M..H`.
- Fresh GitHub main/PR head/base, Actions/checks/statuses, bot availability and
  provider applicability: require separately authorized current provider reads
  once a PR/head exists. No provider was called here.
- Linux/platform coverage: requires the reviewed candidate's tests on an
  available authorized environment or named CI job; Windows-only observations
  do not prove cross-platform behavior.
- Full Stage E bundle: environment/pip checks, offline-CI/validator/skill-contract
  suites, selected corpus execution, BER self-check/unit tests, offline Scenario
  A evidence acceptance, setup bridge/setup routing/delivery-control tests,
  DCO and applicable hosted jobs remain E's task after valid C/D handoffs.
  C's validator summary was read but that validator was not independently
  rerun by D; no claim of a full-tier pass is made.
- PR publication/readback, final F review/metadata and G merge: no PR exists
  in the supplied handoff, and these stages were not performed. Their fresh
  evidence and existing authority requirements remain intact.

A's explicitly declared hosted/platform gaps can remain UNRUN. **Missing H
is not one of those permitted gaps:** it is the AC6 NOT MET and chain-entry
blocker. This report changes no SD-A/SD-B decision or MG1–MG5 condition.

## Artifact inventory and continuation

Only scratch files outside `impl` were written: this audit,
`STAGE-D-PROBE.py`, and `D-evidence/` (baseline export, two synthetic mutants,
JSON records, raw stdout/stderr). Repository source/index/config, baseline
objects, candidate tree, branch refs and external systems were not changed.

Minor audit-command issues were corrected without changing permissions: an
initial read looked for an absent AGENTS.md at the scratch parent instead of
the actual checkout; one PowerShell call required quoting `HEAD^{tree}`; and
the guard was located in `validate-skills.yml`, not a separate guessed workflow
filename. Git status/diff also warns that the user's global ignore file is
unreadable. Successful corrected commands and exact path checks provide the
evidence above. No command was retried through another identity or provider.

| Scratch evidence | SHA-256 |
| --- | --- |
| `STAGE-D-PROBE.py` | `C28D3A1C9A698898FAAB66F4F7BAEF244D61D675534010234A98278B99F25FAA` |
| `D-evidence/static.json` | `1559F946A0413098F2585910BC20427A816D9ABEBDFE9161B41F7A72E93A6033` |
| `D-evidence/semantic.json` | `F4534502B26379C9824B0A9F720892859E56C11C139A642F3EDADA85EB7D65B9` |
| `D-evidence/suite.json` | `539F0DA2256BAD1775ABB3B95B785020B6B20ED6771FFD14B206CA8C032EEED0` |
| `D-evidence/old-red.json` | `0E0CD951BD27BA3E2AFD619A1F46817300D36B0D7CAA59141430526889992F7F` |
| `D-evidence/mutants.json` | `15E8484AF3F6C0F091051EF04A5062CA19C40E94B5DEDEF25A66C274029EE8C0` |
| `D-evidence/corpus.json` | `C6CCB403E70CF49817D657D9F97F7717CCC3BF46256E7974F54C054AAEF56C14` |

**Continuation:** return to C for immutable-head completion; retain this local
review evidence. Once H exists, rederive H/T/M, scope and relevant validation
binding before a fresh D disposition. Do not enter formal E/F/G on this report.
No source revision is requested on the evidence found, and no held merge is
authorized.

## Self-authored skills rows

These are exact D source rows for future attributed copying. No PR body was
written. `code-reviewer` applies to the Python tooling diff, not skill-content
review. No MANUAL-ONLY skill was invoked.

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [code-reviewer](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/code-reviewer/SKILL.md) | D local / `/root/linkbound_d_local`, round 1 | Reviewed actual staged two-file Python diff and callers; proved state/assembly bound, checked preservation and unchanged original tests, independently reran baseline/candidate and mutation probes. | No source defect found at tree `64d2cf8a83fb22b7d4aef49d4f17e2c5ce3a5191`; AC1–AC5 MET locally. SD-D REVISE because AC6 lacks candidate commit H; no formal D acceptance or hosted claim. |
| [change-classification-gate](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/change-classification-gate/SKILL.md) | D local / `/root/linkbound_d_local`, round 1 | Reclassified actual script/test paths as bug fix plus narrow refactor; verified exact allowlist, old-red/new-green floor and behavior preservation; retained protected-path limits. | Two staged modifications only; original 23 and candidate 29 tests pass; old T2 fails as intended. No policy, corpus, dependency, provider or merge action. |
| [risk-tiered-validation-selector](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/risk-tiered-validation-selector/SKILL.md) | D local / `/root/linkbound_d_local`, round 1 | Applied scripts/** forced-full rule separately to both actual paths and carried the accepted real E check inventory forward without claiming its execution. | FULL remains required at E after C/H and D completion; hosted, Linux, signature/DCO and full-bundle evidence remain unavailable or unrun. |

## Final timing

Recorded start: **2026-10-09 10:15:11 UTC**. Finish: **2026-10-09 10:22:48 UTC**.
Measured wall interval between recorded timestamps: **457 seconds**.
Active time was **not measured**. This wall interval is an imperfect comparison
with the initial **25–45 active-minute** ETA. The finished report's SHA-256 is
recorded in `STAGE-D-LOCAL-RECEIPT.json` and the final handoff, avoiding a
self-referential report hash.
