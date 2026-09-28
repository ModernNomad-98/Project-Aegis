---
name: acceptance-criteria-reviewer
description: 'Review acceptance criteria that already exist, in a spec, ticket or user story, for testability, completeness and ambiguity: each criterion must name an observable outcome, a pass or fail threshold and the evidence that will prove it; missing negative, boundary and permission cases are listed; vague words ("fast", "works", "user-friendly") are flagged with a suggested concrete rewrite for the author to accept. Per-criterion verdict TESTABLE, NEEDS-REWRITE or UNTESTABLE, with one question to the owner where intent is unclear; rewrites nothing silently and invents no requirement. Use when a story or spec arrives for build or test and nobody has checked that its criteria can be verified, or before turning criteria into a test plan. Do NOT use to write the spec (product-spec-writer), elicit unclear requirements (requirements-gathering-facilitator), plan the tests (test-plan-designer), write manual cases (manual-test-case-creator), or gate a release on evidence (release-readiness-reviewer).'
---

# Acceptance Criteria Reviewer

**Reading key:** Acceptance criteria are the conditions a feature must meet
to count as done. A user story is a short "as a <role>, I want <goal>"
statement of a need; a ticket is a work item in a tracker. Quality assurance
(QA) checks behavior against the criteria. Given/when/then is a common
criterion shape: a starting state, an action, and the expected result.

## Purpose

Criteria that cannot be checked are the cheapest defect to fix and the most
expensive to find late: a tester plans around "should load fast", an
engineer builds to a different reading of "works", and the disagreement
surfaces at release. This skill reads acceptance criteria someone else
wrote, in a spec, ticket or user story, and returns a per-criterion verdict
(TESTABLE, NEEDS-REWRITE or UNTESTABLE) with the reason, the missing
observable outcome, threshold or evidence, and a suggested rewrite the author
may accept. It lists the negative, boundary and permission cases the set
does not cover as gaps for the owner to decide, and asks one question where
intent is unclear. It reads and reports only: it never edits the source
document, never invents a requirement, and never decides whether work is
done. Built under owner decision D68 (2026-09-28) from catalog item #226;
the definition-of-done check (#227) stays with `release-readiness-reviewer`.

## Use When

- Use when: a story, ticket or spec arrives for build or test and nobody has
  checked that its acceptance criteria can be verified.
- Use when: someone asks "are these acceptance criteria any good?", "can QA
  test this story?" or "what is missing from these criteria?".
- Use when: criteria are about to become a test plan or manual cases and the
  planner needs to know which ones are safe to plan against.
- Use when: a criterion set from another team, a customer or an older spec
  must be checked before it is accepted into a sprint.
- Do NOT use when: no criteria exist yet and the job is to write the spec —
  that is `product-spec-writer`, which writes criteria and already checks its
  own. This skill reviews criteria written elsewhere or earlier.
- Do NOT use when: the requirement itself is unclear, contested or
  solution-first — that is `requirements-gathering-facilitator`; reviewing
  criteria for an undecided requirement only polishes a guess.
- Do NOT use when: the criteria are checked and the ask is what to test, at
  which layer, with what data — that is `test-plan-designer`. This skill
  answers "can these be verified?", not "how will we verify them?".
- Do NOT use when: the ask is step-by-step manual cases from the criteria —
  that is `manual-test-case-creator`.
- Do NOT use when: the ask is "is this story done?" or "is this ready to
  ship?" — the definition-of-done evidence gate is `release-readiness-reviewer`;
  the finished-work report is `ai-closeout-reporter`, and an after-the-fact
  process check is `agent-governance-audit`.

## Inputs to Inspect

1. The criteria themselves, verbatim, with their source (spec path, ticket
   id, story text). No criteria → Stop Conditions.
2. The requirement or story they belong to: the user, the goal and any
   stated non-goals. Criteria are judged against the intent they serve, not
   in isolation.
3. The product spec (`product-spec-writer` output) or requirements brief
   (`requirements-gathering-facilitator` output) when one exists, to separate
   an unclear criterion from an undecided requirement.
4. Existing definitions the criteria lean on: roles and permissions
   (`authorization-matrix-designer` output), error codes
   (`error-taxonomy-designer` output), service levels or latency budgets, and
   glossary terms. A criterion that says "per the latency budget" is only
   testable if that budget exists.
5. Observed behavior, when the feature already exists in code or a running
   build, only to detect a contradiction between criteria and behavior; it
   is not a reason to rewrite the criteria to match the code.

## Workflow

1. **Collect and number the criteria.** Quote each verbatim with a stable id
   (AC1, AC2 …). Split compound criteria ("user can upload and share a file")
   into their parts and say so; never merge or drop one silently.
2. **Check each criterion for the three testable parts.** An observable
   outcome (what a tester sees, queries or measures), a pass or fail
   threshold (the value, state or count that separates pass from fail), and
   the evidence that will prove it (a test result, log line, screenshot,
   metric or record). Name every missing part.
3. **Flag vague and unfalsifiable wording.** Words such as "fast", "works",
   "user-friendly", "intuitive", "secure", "appropriate", "etc." and "as
   expected" have no threshold. For each, propose a concrete rewrite built
   only from facts in the inputs; where the threshold is unknown, leave a
   visible placeholder (`<p95 under ? ms>`) and ask the owner, never pick a
   number. The vague-word catalog and rewrite patterns are in
   [references/criteria-review-sheet.md](references/criteria-review-sheet.md).
4. **Assign one verdict per criterion.**
   - **TESTABLE:** all three parts present; state the evidence that will
     prove it.
   - **NEEDS-REWRITE:** the intent is clear but a part is missing or vague;
     give the suggested rewrite for the author to accept.
   - **UNTESTABLE:** no observable outcome can be derived without a product
     decision (the intent itself is unclear), or the criterion describes an
     internal design choice rather than behavior. Pair it with the one
     question that would unblock it.
5. **Check completeness across the set.** For the behavior the story covers,
   list which classes have no criterion: negative (invalid input, missing
   data, expired or duplicate items), boundary (limits, empty, maximum
   sizes), permission (wrong role, other tenant, signed-out user), and error
   or recovery behavior. Report each as a GAP with the question the owner
   must answer. A gap is not a requirement: never write the missing criterion
   as if it were agreed.
6. **Check consistency.** Criteria that contradict each other, the story's
   goal or a stated non-goal get ONE owner question naming both sides; do
   not guess which one wins. A contradiction between criteria and the
   observed behavior of existing code goes to `source-of-truth-reconciler`.
7. **Ask at most one question per unclear item, and rank them.** The owner
   gets the smallest set of questions that unblocks the most criteria,
   blocking questions first. If a product choice is needed, define the terms,
   explain each viable option's user benefit, drawbacks and cost or
   uncertainty, recommend one with a reason tied to the story, and ask one
   atomic question. The answer is the owner's decision, not this skill's.
8. **Deliver the review** in the Output Format and name the next owner:
   `test-plan-designer` for TESTABLE criteria, the author for NEEDS-REWRITE,
   the product owner for UNTESTABLE items and gaps. Cross-tenant and
   wrong-role gaps that need a security test suite are noted for
   `multi-tenant-security-tester` *(manual-only)*, which a person must invoke
   by name.

## Output Format

```
ACCEPTANCE CRITERIA REVIEW — <story / spec / ticket id>
Source:     <path or ticket id; criteria quoted verbatim below>
Intent:     <user, goal and non-goals the criteria serve, as stated>
Summary:    <n> TESTABLE · <n> NEEDS-REWRITE · <n> UNTESTABLE · <n> GAPS
Criteria:
  AC<n> "<verbatim text>"
        Verdict:  TESTABLE | NEEDS-REWRITE | UNTESTABLE
        Outcome:  <observable outcome, or MISSING>
        Threshold:<pass/fail value or state, or MISSING>
        Evidence: <what will prove it, or MISSING>
        Why:      <the specific problem, quoting the vague word if any>
        Suggested rewrite (author to accept): <given/when/then, placeholders
                  visible where the owner must supply a value | none>
Gaps (not requirements; owner to decide):
  GAP<n> <negative | boundary | permission | error class> — <behavior not
        covered> — question: <one question>
Contradictions: <AC ids + the conflicting statements + one question | none>
Owner questions (ranked, blocking first):
  Q<n> <question> — unblocks <AC/GAP ids>
Next: TESTABLE → test-plan-designer · NEEDS-REWRITE → author ·
      UNTESTABLE and gaps → product owner
Not changed: the source document; every rewrite above is a suggestion.
```

For an owner product choice inside a question, include the defined terms,
the options with reasons, benefits, drawbacks and cost or unknowns, and the
recommendation with its reason before the one question.

## Validation Checklist

- [ ] Every criterion is quoted verbatim with an id; compound criteria were
      split and the split is stated.
- [ ] Every criterion has exactly one verdict with a specific reason;
      TESTABLE items name their evidence.
- [ ] Every NEEDS-REWRITE item has a suggested rewrite built only from facts
      in the inputs, with unknown thresholds left as visible placeholders.
- [ ] Every UNTESTABLE item carries one question that would unblock it.
- [ ] Negative, boundary, permission and error classes were each checked;
      each uncovered class is a GAP with a question, not a new criterion.
- [ ] Contradictions name both sides and ask one question; none was resolved
      by guessing.
- [ ] The source document was not edited, and the report says so.
- [ ] No verdict about whether the work is done or ready to ship was given.

## Gotchas

- A criterion can be precise and still untestable: "the system uses a queue"
  describes design, not behavior. Ask what the user would observe.
- "Works as expected" and "same as today" hide the expectation. Unless the
  current behavior is written down somewhere the tester can read, it is
  NEEDS-REWRITE.
- Inventing thresholds feels helpful and is the main failure mode: a
  reviewer who writes "under 200 ms" has made a product decision. Leave the
  placeholder and ask.
- Gap lists grow into a requirements rewrite. Report the class and the
  question; the owner decides whether it becomes a criterion.
- Criteria copied from a spec that `product-spec-writer` produced are usually
  good; the value is in tickets and stories edited after the spec, where
  criteria drift.
- Permission gaps are the ones most often missing and most costly in a
  multi-tenant product; check them even when the story does not mention
  roles.
- A criterion that only a production metric can prove (for example a
  conversion rate) is testable after release, not before; say which, so the
  planner does not block on it.

## Stop Conditions

- No acceptance criteria are supplied or findable → stop and ask for them;
  if none exist, hand the job to `product-spec-writer` (or
  `requirements-gathering-facilitator` if the requirement itself is unclear).
  A review cannot start from a feature name.
- Asked to edit the ticket, spec or story in place ("just fix the criteria")
  → refuse the write; return the suggested rewrites for the author to accept
  and change nothing.
- Asked to fill a gap or pick a threshold as if it were agreed → refuse;
  report it as a gap or placeholder with the owner question.
- Criteria contradict each other or the stated goal → stop short of a
  verdict on those items and ask the owner one question; do not choose.
- Criteria contradict the observed behavior of existing code → route to
  `source-of-truth-reconciler` before reviewing against either.
- Asked whether the story is done, merged-ready or ready to release → out of
  scope; hand off to `release-readiness-reviewer`.

## Supporting Files

- [references/criteria-review-sheet.md](references/criteria-review-sheet.md)
  — the three-part testability check, the vague-word catalog with rewrite
  patterns, the completeness classes with prompt questions, and worked
  verdict examples.
- `evals/evals.json` — behavior cases: the mixed-verdict happy path, missing
  failure and permission classes reported as gaps, the "just fix the
  ticket" refusal, and contradicting criteria answered with one question.
- `evals/trigger-evals.json` — discrimination against `product-spec-writer`
  (write vs review), `requirements-gathering-facilitator`,
  `test-plan-designer` (review vs plan), `manual-test-case-creator` and
  `release-readiness-reviewer` ("is this story done?").
