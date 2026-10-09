# CP-WP-003 planning corrections — independent Stage B audit, revision 1

**SD-B: REVISE**, bound exclusively to `PLAN-rev1.md` SHA-256 `3296d09a382837aee265a71a951406b8f526fc58355bbe949c014ae9fee8bdd5`.

Auditor: `/root/rowpolicy_backlog`, Stage B only. This agent did not author Stage A and takes no later stage of this change. Initial estimate: 15–25 active minutes. First measured start: 2026-10-09 16:56:28 UTC. Active time is not separately measured.

## Required revision

**R1 — Include the mandatory pre-PR structural validator in the finite validation plan.**

The plan's validation commands at lines 99–105 list scope, whitespace, Markdown links and the focused synthetic test/trace, but omit `python -B -P scripts/validate-skills.py`. Current `CONTRIBUTING.md:84–89` requires the validator to pass with exit 0 before any PR. The plan's later statement that hosted `validate-skills` will run does not schedule this explicit pre-PR check. The classification skill's links/rendering floor does not displace the repository requirement.

Minimal repair: add `python -B -P scripts/validate-skills.py` to the candidate-check list, require exit 0 before PR publication and retained output in C's handoff, and include that check in AC4 or an explicit referenced check list. No new test, dependency installation, additional source path or broader test suite is requested. If the required validator cannot run, report the actual limitation and return to the coordinator under the existing workflow; do not publish under an inferred waiver.

This is the sole blocking finding. It is a plan completeness issue, not evidence of a source defect. Return a new captured plan revision for independent Stage B re-audit before C starts.

## Independent evidence and reconciliation

Live `main` was observed twice during this audit using `gh api repos/ModernNomad-98/Project-Aegis/branches/main --jq .commit.sha`; both returned `625fc66711eaf7b3ee788cbc2dff98f05f147c1c` (M). The earlier pinned GitHub tree and register responses were re-used as immutable content after this current ref check. The complete register has 121 defining entries, maximum 121, no duplicates. I inspected its preamble, complete APR-086/098/099 sections, and all subsequent references to those IDs. No later option-(a) authorization is present in that history.

Source checkout: `C:/src/Codex Projects/Project Aegis/route002/impl`. Its origin is `https://github.com/ModernNomad-98/Project-Aegis.git`; README begins `# Project Aegis`, and all three other AGENTS-required source landmarks exist. Source `git status --short` was empty before and after the independent test. Git reads used process-local `-c safe.directory=...` and `--no-optional-locks`; persistent Git configuration was not modified.

| Pinned object | Verified Git identity |
| --- | --- |
| Backlog at M and source checkout | `2b0e2976680097d9771e6aa6294f3468c261561a` |
| Decision packet at M and source checkout | `dc147668bf4396efdf435a113a413f84b18a40a7` |
| Entire tools tree at M and source checkout | `629fc1c4a44013c908e44a7bb8639496cb652f08` |
| Current register at M | `7ee0e822398382101900c79aea9962b540a86c57` |
| Canonical delivery workflow at M | `720a858083f67a4fb91648517a0a918c68cd1d4b` |
| CI workflow at M | `66cca67d0390e739190939abccae99125cb56543` |

**C1, IS conflict — historical proposed assertion versus actual test execution.**

The backlog's historical note at 321–331 recommends asserting that run-2 readiness blockers include `OPERATION_SLOT_OCCUPIED`. Current `test_guard_traceability.py:282–306` calls the inherited `test_t02_repository_slot_in_another_run_blocks_readiness` at line 283. In `test_storage.py:10783–10818`, that helper asserts BLOCKED at 10807 and the exact blocker at 10818. `storage.py:24776–24777` checks PLANNED before the later occupied-slot branch at 24899–24904. Actual source and independently observed execution govern this IS question under source-of-truth precedence rule 2; the dated historical note remains intact.

I independently executed the existing `GuardGapTests.test_t03_occupied_slot_denies_other_run_intent` with a new in-memory `sys.settrace` observer, rather than running the planner's output-writing trace script. The observer recorded the explicit assertion, PLANNED denial and all six lines 24899–24904 in the later branch, filtered to request run-2. The single offline synthetic case passed in 36.291 seconds. Observed output:

```json
{"exceptions": [["DispatchDenied", "T03 requires durable PLANNED state"]], "planned_denial_executed": true, "readiness_assertion_executed": true, "slot_branch_lines_reached": [], "success": true, "testsRun": 1}
```

The larger traced runtime is not a benchmark. The observer resolves paths on events and therefore adds overhead. The result proves this focused test's path only. It does not prove universal branch unreachability or live authority. The proposed addition makes that distinction correctly and leaves the second receipt-accounting finding historical and unverified.

**C2, SHOULD discrepancy — omitted prerequisite in the decision packet.**

Backlog line 269 includes evidence-computed transition guards in CP-WP-003's entry criteria; lines 294–296 and 317–319 preserve this condition and its ungranted status. Main APR-086 at 2585–2594 makes option (a) an entry criterion and expressly does not grant it. APR-098 at 2952–2965 consumes APR-086 while preserving that ungranted condition. APR-099's correction is limited to an unrelated prose clause and does not grant this option. The complete decision packet's missing-proof table omits this requirement. Current canonical owner records govern this SHOULD question under precedence rule 3. The added row correctly restores the existing prerequisite to the packet without selecting a source, granting work, or equating authenticated inspection with dispatch.

## Scope, authority and preservation review

The exact two-path scope is sufficient:

1. `docs/roadmaps/resumable-control-plane-backlog.md`: one dated insertion after the complete historical paragraph ending at current line 331.
2. `docs/roadmaps/cp-wp-003-real-authority-decision-packet.md`: one dated table row after the billing row.

The plan requires all earlier content to remain in order and unchanged. Additions-only diff evidence must be checked against actual base bytes; a successful `diff --check` alone does not prove preservation. No new approval-register entry is needed to repeat the existing APR-086/098 requirement. Neither their consumed implementation authority nor standing delivery mechanics authorizes runtime work. This audit approves no source edit or real CP activity.

Classification **docs-only** is appropriate after inspecting the actual targets and proposed additions: no new behavior, permission, approval rule, guard requirement, agent instruction or executable artifact is introduced. Database/schema impact and external spend are zero for the proposed documentary scope. Both paths are outside the current protected-path pattern and CONTRIBUTING's listed security-review surfaces. Actual changed files and the PR security answer must still be verified by later holders.

The links/rendering/review floor is specified, and the existing focused test supports the new factual sentence without adding a test. All seven stages remain distinct. Immutable C head/tree/base, D's per-criterion assessment, E's actual output, F's skills/security/witness/hash and G's independent gates are retained. Nothing in the plan permits a stage to review or merge its own work.

## Acceptance-criteria review

Compound criteria are decomposed below into observable parts without dropping or silently rewriting any condition. These verdicts concern testability, not whether implementation is MET.

### AC1 — TESTABLE

> AC1 — Exactly the two named source paths change, through additions at the stated anchors. Every pre-existing byte/text segment remains intact and in order. No approval register, code, test, workflow, generated artifact or agent instruction changes.

Observable parts: exact path-set equality, zero removed/replaced prior bytes and insertions at the two named locations. Threshold: exactly two paths and no historical-content mutation. Evidence: base/head blob comparison, exact diff and insertion-boundary inspection. The anchors are present and unambiguous. No rewrite needed.

### AC2 — TESTABLE

> AC2 — The backlog identifies the inherited helper and its existing BLOCKED/OPERATION_SLOT_OCCUPIED assertions; distinguishes the durable-state denial from the later commit_intent slot branch; and says this focused test does not independently prove that branch. It neither requests a duplicate assertion as outstanding work nor claims universal unreachability.

Observable parts: complete bounded factual explanation and absence of the two prohibited overclaims. Threshold: statements agree with named source and the focused trace. Evidence: exact prose review plus the helper/assertion/denial sites and trace output. The independent run above confirms the premises. No rewrite needed.

### AC3 — TESTABLE

> AC3 — The packet states the existing evidence-computed transition-guard prerequisite and links backlog, APR-086 and APR-098; records the maintenance grant consumed and option (a) ungranted; keeps CP-WP-003/004 and real dispatch blocked. No scope, prerequisite or grant is silently added, removed or rewritten.

Observable parts: the specified row, three references, lifecycle statement and retained blocked posture. Threshold: agreement with current canonical owner records and no new permission or prerequisite. Evidence: exact row/readback, links and comparison against pinned APR/backlog text. No rewrite needed.

### AC4 — NEEDS-REWRITE (R1 only)

> AC4 — The repository offline Markdown checker reports zero broken links and zero dead anchors for both documents; new blocks render coherently; git diff --check passes. The named functions and assertion/denial sites still exist, and the focused synthetic test at validation confirms the factual claim.

The listed outcomes are testable: zero broken/dead links, zero diff-check errors, retained named sites and the specified trace facts, with Markdown preview/readback for formatting. Missing from the plan's overall check set is the required pre-PR structural validator. Add it here or link AC4 to a finite check list that includes its exit-0 requirement and captured output. No arbitrary new numeric threshold or owner choice is needed.

### AC5 — TESTABLE

> AC5 — Stage C's handoff names immutable head, tree and base, accepted plan hash, check output, two-path scope proof and rule-preservation inventory. Stage D resolves each AC individually against those objects.

Observable parts: every named field resolves and matches C's exact candidate, and D records a result for each criterion. Threshold: no missing/wrong object, hash, output or preservation evidence. Evidence: immutable Git object reads and the handoff/per-criterion audit. This is a reviewable artifact requirement, not a claim of completed implementation. No rewrite needed.

Summary: **4 TESTABLE; 1 NEEDS-REWRITE; 0 UNTESTABLE.**

Completeness classes were considered against this documentary scope. Negative cases (wrong helper/denial claim, duplicate assertion, omitted lifecycle state, extra files), boundaries (exact insertion sites and prior byte preservation), permission (no newly granted runtime/source/host work), error recovery (failed or unavailable checks returned with evidence) and state/timing (fresh main, exact candidate and distinct A–G holders) are addressed. No product-behavior gap or new owner decision is needed for these two corrections.

**Advisory clarification, not a second blocking finding:** line 93 says AC1–AC5 cannot be marked MET at Stage A because the candidate does not yet exist. That statement is true at planning time and does not expressly waive D. For clarity, rev2 can say that all five must be MET at the immutable C/D candidate and that this plan declares no genuine candidate-stage UNRUN exception. Canonical SD-D at `docs/delivery-workflow.md:131` governs; an unavailable required candidate check must not become an accidental blanket exemption. The plan's D paragraph already requires each AC to be assessed against the candidate.

## Checks, inputs and limitations

- Exact plan SHA-256 independently matched before and after review: `3296d09a382837aee265a71a951406b8f526fc58355bbe949c014ae9fee8bdd5`.
- Planner trace script SHA-256: `77745e933888f933dabed3f87fd6b9e1587b7f55e5c58133cd1cf5f8f04eab73`.
- Planner trace-result SHA-256: `948e8a45ff0d3422fa180ba957d0c3cc2cf0480daf5eafadd5a017c54a50d227`.
- Inspected that script and result; did not execute it because it rewrites the planner's evidence file. Independent execution used inline Python with `-B -P`, temporary synthetic fixtures and no retained test-output file.
- Fresh source status after that run remained empty. No full suite, hosted job or PR was run/created by this audit. The mandatory validator is identified as future C/publication evidence, not claimed passed here.
- The plan's CI sentence is read in its stated PR-publication context. `gate-guard` is PR-event-only; no push-job success is implied. Actual check results and path skips remain future observations.

PROVEN: current source identities; complete two-file historical/additive scope; existing readiness assertion and actual durable-state denial in one synthetic case; preserved existing ungranted prerequisite and packet omission; testable correction criteria except the missing repository-required validation item; clean inspected source after audit.

UNVERIFIED: original owner UI evidence outside the current source records; actual future candidate, H/tree/base and changed-source check results; rendering of future additions; direct slot-branch denial; receipt-accounting branch claim; real authority/freshness/host/evidence/billing guarantees; implementation of evidence-computed guards; full-suite/hosted CI and merge readiness. These gaps are not passed checks.

Intentionally not done: source edits, commits, pushes, PR comments/reviews/publication, provider or real-account access, credentials, real dispatch, merge, and any later delivery stage. Only the assigned scratch audit artifact was written. The source plan and planner evidence were preserved.

## Skills actually applied and stage handoff

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| acceptance-criteria-reviewer | CP docs correction Stage B round 1 / `/root/rowpolicy_backlog` | Read SKILL and criteria-review-sheet; quoted/decomposed AC1–AC5 and checked outcomes, thresholds, evidence and scope-relevant negative/boundary/permission/error cases. | Four TESTABLE, AC4 NEEDS-REWRITE for missing mandatory pre-PR validator; no implementation MET claim. |
| source-of-truth-reconciler | CP docs correction Stage B round 1 / `/root/rowpolicy_backlog` | Applied source precedence to historical assertion advice versus independent code/trace evidence and missing packet prerequisite versus APR-086/098; retained historical context and authority limits. | Both proposed corrections are evidence-backed; no normative choice or runtime authority created; details above. |
| change-classification-gate | CP docs correction Stage B round 1 / `/root/rowpolicy_backlog` | Read SKILL and classification matrix; inspected both target files, actual proposed additions, CONTRIBUTING and protected/CI paths. | Docs-only, exact two-path lock, links/rendering/review plus repository-required validator; no database or permission change. |

The skill procedures support this independent audit. Stage B's disposition itself follows `docs/delivery-workflow.md` SD-B. No MANUAL-ONLY skill was applied. Prior SD-A's captured scope and the canonical SD/MG rules remain binding; this audit changes no rule and records no owner approval.

Next: the original planner addresses R1 in a new immutable plan revision; a distinct-from-A Stage B auditor re-audits it. C must wait for an affirmative audit on that revision. This reviewer remains Stage B only.

Finish: 2026-10-09 17:00:56 UTC. Elapsed measured wall interval from 16:56:28 UTC: 268.9 seconds. Active time was not measured; wall time is an imperfect comparison with the 15–25 active-minute estimate.
