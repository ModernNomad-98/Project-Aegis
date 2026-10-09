# LINK-BOUND-1 — independent Stage B audit of PLAN-rev1

**SD-B: ACCEPT** for the captured plan whose SHA-256 is
`82D2BC9B440C00C7A6AAF044C393CBCD8CAD509213D99BF14F168C9E35CF459C`.

Auditor: `/root/linkbound_b`, independent of Stage A planner
`/root/linkbound_plan`. This accepts a bounded implementation plan. It does not
assert that an implementation exists, that any candidate passes, or that a
protected-file merge is authorized. **The green-only merge hold remains.**

## Binding, scope, and timing

- Plan: `C:\src\Codex Projects\Project Aegis\linkbound\PLAN-rev1.md`.
- Stage A receipt SHA-256:
  `C8B9258ECDE7279D4C0D147CF0AFC704BCC1EAAE758A730360805C9E921CC746`.
- Pinned local planning baseline M:
  `8e11c8f4c2777265e254057ce0fa1e52f0cf03bf`.
- Observed cadence checkout HEAD:
  `e834ea7079060314a2bc4f4275938b1cf01e0f7d`.
- Audit start: **2026-10-09 09:56:55.5502608 UTC**, captured by
  `Get-Date -AsUTC -Format o` before reading the plan.
- Initial assigned estimate: **20–35 active minutes**. Active time is not
  measured. Finish and wall duration are in the final timing section below.
- Authority for this stage: the coordinator's explicit bounded independent
  plan audit assignment; source and provider access remain read-only, with no
  provider calls. Only scratch audit artifacts under `linkbound` are written.

## Findings

**No blocking plan deficiency found.** The two-file scope, exact baseline
compatibility contract, separate structural complexity proof, adversarial
regressions, and explicit protected-file hold make the plan implementable and
independently adjudicable. The six criteria are TESTABLE as future engineering
obligations; none is claimed MET by this Stage B audit.

The following are implementation and review cautions already required by the
accepted plan, not added scope or waived requirements:

1. Keep the existing heuristic even where it differs from a balanced Markdown
   parser. In particular, an opening parenthesis anywhere after the latest
   `](` can keep destination state open after a later `)`. The current helper's
   prose is less precise than its actual predicate. The baseline function and
   exact oracle are the behavior source for this optimization.
2. Removing prefix rescans without removing repeated prefix assembly does not
   meet AC2. D must inspect the actual slicing, searches, trimming, regexes,
   and string construction, including helpers called from the loop.
3. Timing ratios are regression evidence, not an asymptotic proof or a portable
   runtime guarantee. The plan requires both timing and a structural argument,
   and requires A/B revision before changing sizes or thresholds. A harness
   timeout is a failed regression, not a skip or an input cap.
4. Preserve actual CLI output in T5. For example, current `--quiet` sends
   both diagnostics and summary through `_Null`; the implementation must not
   opportunistically change that behavior to match a help-text interpretation.
5. Hosted Windows/tools jobs are conditionally skipped for this script-only
   diff under the inspected workflow. An observed skip cannot prove candidate
   execution on Windows; local Windows evidence and actual Linux evidence must
   be distinguished as the plan requires.

## Independently re-derived repository and authority evidence

All Git commands in this audit used `GIT_NO_LAZY_FETCH=1`. Commands reading the
cadence checkout also used a per-command
`-c safe.directory=C:/src/Codex Projects/Project Aegis/cadence/impl`; the older
clone used its corresponding per-command safe path. No Git configuration was
written. No provider command, escalation, or implicit-fetch attempt occurred
in this audit.

Source-library role is corroborated by the README's `# Project Aegis` heading
and the presence of `docs/skills-catalog.md`, `scripts/validate-skills.py`, and
`artifacts/audits/skill-contract-audit-baseline.json`. The source checkout's
`AGENTS.md` and canonical `docs/delivery-workflow.md` were inspected. There is
no `AGENTS.md` at the scratch workspace root; the attempted read reported that
absence, and source instructions were read from the verified clone.

`git ls-tree M -- <paths>` resolved these immutable objects:

| Path | Blob at M |
| --- | --- |
| `scripts/ci/check-markdown-links.py` | `efa65c95f5444e50867e832a688c8351cd332d2c` |
| `scripts/tests/test_markdown_links.py` | `21c167c25da3fbf15b0d7c9c58b58b757f42e888` |
| `.github/workflows/validate-skills.yml` | `66cca67d0390e739190939abccae99125cb56543` |
| `docs/approvals/APPROVAL_REGISTER.md` | `288232321d751aae47e827d44f912f12b75323fc` |
| `docs/delivery-workflow.md` | `720a858083f67a4fb91648517a0a918c68cd1d4b` |

`git diff M -- AGENTS.md README.md docs/approvals/APPROVAL_REGISTER.md
docs/delivery-workflow.md scripts/ci/check-markdown-links.py
scripts/tests/test_markdown_links.py .github/workflows/validate-skills.yml`
was empty. The older clone's local
`git ls-tree 33c81fdabc6e8e59a8378c2206b551fc82ff31dd --
scripts/ci/check-markdown-links.py scripts/tests/test_markdown_links.py`
returned the same two checker/test blobs. Thus the inspected worktree code is
the captured M behavior and the historical #648 behavior for those paths.

APR-103, register lines 3232–3312, records the owner's decision to track this
bound, describes the quadratic `unwrap_links` witness, prefers incremental
state, and says its exact-#648 exception is consumed. A full-file search for
`APR-103`, `quadratic`, `unwrap_links`, and the #648 head found no later
discharge of this bound in the inspected register. Its historical statement
that corpus CI did not invoke the checker has become stale: workflow lines
219–227 now derive tracked Markdown, exclude the fixture substring, enforce
the 600-file floor, and invoke the checker on the selected set.

The exact `gate_pattern` at workflow line 528 contains `scripts/`. Both
allowlisted candidate paths match. The guard exits 1 when any matching path is
present (lines 530–542). APR-047's four eligible paths (register lines
1250–1254) are BER reporting/aggregation files, not either candidate path;
its forbidden scope preserves separate decisions for other protected files.
APR-048 lines 1317–1321 expressly does not waive a red guard. The current
owner's green-only condition therefore has no proven satisfied merge route
for this plan. **ACCEPT does not consume, revive, or widen an old exception.**

## Complexity and compatibility audit

The current loop at checker lines 223–246 repeatedly calls predicates on
`current`, then executes `current = head + " " + tail`. For a constant-width
unclosed label, the no-`]` rightmost-close search must revisit the growing
prefix; rebuilding that prefix independently repeats work proportional to its
length. The sum over N continuations is quadratic for that family.

The proposed design can attain **O(L + N) time and O(L + N) space for
`unwrap_links`**, using the conventional unit-cost string-index/RAM model:

- The rightmost `[` and `]`, latest `](`, rightmost `])`, and suffix
  parenthesis-presence flags contain all information used by the existing
  predicates. A constant-size state updated over each new fragment suffices;
  no nesting stack or rescan of an old suffix is needed.
- The inserted ASCII space prevents `](` or `])` from forming across a join
  boundary. The first successful join removes only trailing whitespace from
  the first line. That whitespace contains none of the predicate markers.
  Subsequent tails are stripped and nonempty, so later joins do not require
  removing trailing content from previously accumulated chunks.
- Offsets must be based on the effective trimmed prefix length, not the raw
  original line length. Each span entry is appended once, with the same
  `(effective_length + 1, continuation_line)` value as the baseline. The
  joining space remains on the preceding span until that next offset.
- Each line is consumed once and can additionally be inspected as a boundary
  lookahead once. Quote removal, strip operations, and the existing anchored
  block regex are linear or bounded on the newly inspected line. A constant
  number of such operations costs O(L + N).
- One final join per group copies each retained character and separator a
  constant number of times. Chunk lists, groups, and source span lists occupy
  O(L + N) aggregate storage.

This is a feasibility argument for the design, not a proof of unwritten code.
D must establish these properties in the candidate. The plan correctly
excludes whole-checker bounds: `LINK`, code-span processing, and repeated
`source_line_at` searches can have separate costs.

Independent direct calls recorded ten baseline examples in
`STAGE-B-PROBE.json`, including:

- `['  [x \t', '  y \t', 'z](none.md)  ']` becomes
  `['  [x y z](none.md)']` with spans `[(0,1),(5,2),(7,3)]`.
- A line consuming no continuation retains trailing tabs/spaces.
- A single quote marker is removed from a continuation; a nested quote still
  stops the group after the first marker is removed.
- A heading followed by Unicode whitespace and a numbered list using a
  Unicode digit both stop a group. Four leading ASCII spaces before `#` do
  not match this baseline block-boundary rule.
- `['[a](t(x', 'y)', 'end']` remains one group under the current suffix
  heuristic, even after `y)`.

T1 already calls for these classes, including exact span lists and a frozen
baseline oracle. No expected output should be regenerated from the candidate.

## Test-plan audit and independent checks

The two allowed source paths are sufficient: synthetic temporary files avoid
tracked fixtures or corpus edits; a small frozen baseline oracle fits in the
existing test module. Scope excludes changes to CI, policy, dependencies,
output, CLI flags, parser syntax, and guards. This is **bug-fix + narrow
refactor**, not a test-only or docs-only change. `scripts/**` selects **FULL**
under the inspected selector's rules artifact. This classifies the planned
paths; C/E must classify the actual diff again.

| Check | Independent result and relevance |
| --- | --- |
| Original test suite | `python -B -P scripts/tests/test_markdown_links.py`: **23 tests in 3.477s, OK**. Per-process Git ownership trust was inherited by the existing tracked-fixture subprocess; no repository configuration changed. AST enumeration independently found 23 `test_` methods. |
| T2 captured timing arithmetic | All recorded medians equal the median of their three samples. Label T(16384)=5.7652537 exceeds 6*T(4096)+0.05=1.7650844 and 5 seconds. Destination T(16384)=14.9785379 exceeds 5.1914396 and 5 seconds. Both old families are red under the prescribed thresholds on the captured host. The complete timing suite was not redundantly rerun; C still owes an actual old-regression red run. |
| T3 joined large tail | At N=16384, independently ran the current CLI in a 15-second child timeout. Exit **1**, broken **2**; `missing-tail.md` line **1**, `also-missing.md` line **16386**. Wall sample **5.7992541s**; stderr empty. |
| T3 blank-boundary tail | At N=16384, exit **1**, broken **1**; `missing-tail.md` line **16387**. Wall sample **4.9819067s**; stderr empty. |
| Corpus selection | Independently derived sorted tracked `.md` paths excluding the exact substring `scripts/tests/fixtures/`: **619 unique paths** at the inspected checkout. LF-terminated manifest SHA-256: `d477b804aa9ead2e050b38322acae1e5c679e162c2af0f8a15900766247b46e6`. This is an audit observation, not a future fixed expected count; T6 must derive the candidate manifest again. |
| Evidence binding | Recomputed plan, receipt, and all five Stage A evidence hashes; each matches its captured value. Both new B probe files were read back and hashed. |

T1's explicit examples plus independently frozen oracle avoid a generated test
that merely restates the new state machine. T2 would reject the recorded old
behavior, while the required structural proof catches a fast small-input
implementation that still has quadratic growth. T3 asserts actual broken
targets and exact source lines, preventing a silent size cap or lost tail from
passing as zero problems. T4 preserves code and block exclusions. T5 compares
normal/JSON/quiet modes and nonzero errors on identical fixture paths. T6
requires the same selected corpus, every batch, and unchanged original tests;
neither an empty selection nor a lost failing batch is an acceptable pass.
These are sufficient nonvacuity obligations for this bounded plan.

The workflow self-test entry points are lines 178 and 327. Corpus CI is
lines 219–227. Linux `validate-skills` is unconditional; Windows/offline is
conditional on `tools/` or the CI requirements files (lines 94–103, 271–275),
and tools jobs are conditional on `tools/` (lines 361–364 and 411–414). The
plan correctly requires actual job evidence and distinguishes a skip from a
pass. Its full local validation inventory names existing commands; this audit
does not claim to have executed that full bundle.

## Acceptance criteria review

Each quoted criterion retains its original ID. Compound obligations are
assessed together below; none is silently dropped or replaced. Summary:
**6 TESTABLE, 0 NEEDS-REWRITE, 0 UNTESTABLE, 0 blocking gaps**.

| ID and verbatim criterion | Verdict; observable threshold and evidence |
| --- | --- |
| AC1: The candidate changes exactly the two declared files and introduces no dependency, CLI/output contract, syntax expansion, input cap, or authority change. | **TESTABLE.** Exact two-path name/status set plus reviewed hunks, unchanged fixture/corpus comparison, and T1/T5 contract evidence. Any extra tracked path or excluded behavior change fails. |
| AC2: `unwrap_links` meets the O(L + N) time and space bound, removing both accumulated-prefix rescanning and repeated rebuilding. | **TESTABLE.** A structural amortized argument must account for every operation and allocation, supported by the explicit T2 thresholds and old-baseline red result. Timing alone cannot satisfy it. |
| AC3: Returned merged strings and source span lists equal the old implementation on the specified compatibility matrix and deterministic generated inputs. | **TESTABLE.** Exact tuple equality on T1's named matrix and at least 1,000 bounded fixed-seed cases against the frozen baseline; unchanged existing wrap/code expectations. Any difference fails. |
| AC4: CLI classification, counts, diagnostic target and source line, exit status, and external-no-fetch behavior remain unchanged; large inputs still expose a real broken tail link. | **TESTABLE.** T3 exact target/line/count/exit results independently corroborated above; T4/T5 exact expectations and mode comparisons cover the remaining contract. No successful network fetch is needed. |
| AC5: The original 23 tests remain effective and pass, new relevant tests pass, and the same selected repository corpus produces the same counts and diagnostics before/after. | **TESTABLE.** Baseline 23-method inventory/run, unchanged assertions, new test count/output, nonvacuity controls, versioned manifest, and complete before/after batch evidence. Pre-existing corpus failures must be preserved and disclosed. |
| AC6: The supplied C handoff identifies exact base/head/tree, commands, versions, local outcomes, and every unavailable check. No failed or unrun check is described as green or satisfied by timing evidence. | **TESTABLE.** Git object resolution and immutable handoff content either supply the named fields and honest dispositions or fail. Local tests cannot become undeclared UNRUN at D. The plan explicitly declares which hosted/platform portions cannot be established locally and names later E/F/G duties. |

Negative, boundary, error/recovery, state/order, and permission classes were
checked. The plan names malformed punctuation, absent closers, empty and large
inputs, conflicting block state, missing targets/inputs, duplicate links, and
out-of-order markers. User/tenant authorization and expiry are inapplicable to
the pure string operation, and the plan says why. Its external-no-fetch and
stage-authority boundaries cover the actual permission surface. No new product
choice or threshold is invented by this audit.

## PROVEN and UNVERIFIED boundary

**PROVEN here:** exact plan/receipt binding; local source and historical blob
identity; current local corpus invocation and protected-path classification;
consumed exception limits; baseline 23-test pass; direct compatibility probes;
large-tail target/line/count results; recorded timing threshold arithmetic;
testability and feasibility of this plan.

**UNVERIFIED here:** live GitHub main/head/base/checks, any candidate behavior or
performance, Linux execution, cross-platform proof, full validation bundle,
automated-review availability, provider-suite applicability, PR publication,
and merge. No implementation exists in this audit. A prospective guard
failure is a known deterministic policy consequence of the stated file set;
no hosted failure is fabricated. Any actual failed guard remains failed.

The Stage A planner disclosed one failed implicit fetch. This auditor made no
such attempt. One synthetic probe initially used Windows' default text
encoding and failed with `UnicodeDecodeError` reading the UTF-8 workflow;
rerunning that scratch probe with explicit UTF-8 succeeded. No source file
changed. Git status emitted permission warnings about the user's global
ignore file; the cadence checkout had no status entries and the older clone
reported only its pre-existing untracked `artifacts/recovery/` and
`artifacts/reviews/`.

## Changed artifacts and next handoff

Only these scratch audit artifacts were created:

- `linkbound/STAGE-B-AUDIT-rev1.md` (this verdict).
- `linkbound/STAGE-B-PROBE.json`, SHA-256
  `C77067106800A53AED5CB060E0C4AB0AC55A53F9DE3F8011D20B564E2D92DB93`.
- `linkbound/STAGE-B-TAIL-PROBE.json`, SHA-256
  `0FF64BEF1D5376FEC3277DA1C7A120AC1208872FDFF8E5422EEFB39382CB9C50`.

Source files, fixtures, Git configuration, branches, commits, PRs, credentials,
and external systems were not changed. Synthetic tail fixtures were removed
by their temporary-directory context manager.

The coordinator may assign the accepted plan to a distinct Sol high Stage C
holder within the existing owner authority. That holder must verify the exact
base and lane, preserve unrelated work, follow the two-file allowlist, and
produce the immutable C handoff. A changed baseline, required threshold
change, parser/behavior change, additional file, or policy change returns to
A/B as the plan says. This Stage B holder must not implement, validate as E,
review as D/F, or merge this same change.

## Self-authored skills rows

The rows below are exact source rows for an authorized editor to copy with
attribution. They claim no PR-body write. `test-plan-designer` was read for
context but was not invoked to rewrite the existing plan; no MANUAL-ONLY skill
was invoked.

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [acceptance-criteria-reviewer](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/acceptance-criteria-reviewer/SKILL.md) | B / `/root/linkbound_b`, rev1 | Reviewed AC1–AC6 verbatim for observable outcomes, thresholds, evidence, boundaries and contradictions; independently checked baseline semantics and large-tail diagnostics without rewriting criteria. | 6 TESTABLE, no blocking gap; SD-B ACCEPT bound to plan SHA-256 82D2BC9B440C00C7A6AAF044C393CBCD8CAD509213D99BF14F168C9E35CF459C. Candidate, hosted and cross-platform results remain unverified. |
| [change-classification-gate](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/change-classification-gate/SKILL.md) | B / `/root/linkbound_b`, rev1 | Re-derived bug-fix plus narrow refactor classification, two-path scope, protected guard matches, consumed APR-103 limits, and APR-047/048 exclusions. | Plan scope accepted; no additional source path or authority granted; green-only protected-file merge hold retained. |
| [risk-tiered-validation-selector](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/risk-tiered-validation-selector/SKILL.md) | B / `/root/linkbound_b`, rev1 | Checked scripts/** forced-full rule, named local inventory, actual workflow entry points and conditional Windows/tools selection; required actual-diff reclassification later. | Planned FULL tier accepted; original 23 tests passed here; full bundle, candidate and hosted execution not claimed. |

## Final timing

Finish: **2026-10-09T10:04:09.908809+00:00**. Measured elapsed wall time: **434.359 seconds**
(**7 minutes 14.359 seconds**). Active time was not measured. This
wall duration is an imperfect comparison with the original **20–35 active-minute**
estimate; it is not a measured active-work result or a future delivery ETA.
