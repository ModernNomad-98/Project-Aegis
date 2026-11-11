# C3.3 advisory review triggers and findings policy

**Status.** This is the proposal text for C3.3. The bounded normative
insertion lives in the policy of record,
[docs/delivery-workflow.md](../delivery-workflow.md#advisory-review-triggers-and-findings-policy-c33).
It is **not effective** until the change that adds it is reviewed and merged
under the repository's rule-change route. Until then it claims no policy
effect and no enforcement.

**No second policy, no second rubric.** The R3 finding-triage rubric's
normative home is the C2.1 amendment at
[docs/delivery-workflow.md](../delivery-workflow.md#r3-finding-triage-rubric).
This page and the insertion reference it; they do not duplicate its table,
classes or dispositions.

## Trigger set

| Trigger | Existing source | Advisory effect |
| --- | --- | --- |
| `pull_request_target` `opened` | `.github/workflows/deepseek-code-review.yml` | one advisory review run |
| `pull_request_target` `reopened` | same | one advisory review run |
| `pull_request_target` `synchronize` | same | one advisory review run at the new head |
| `pull_request_target` `ready_for_review` | same | one advisory review run |
| `issue_comment` `@deepseek` | same, authorised associations only | one advisory review run |
| `pull_request` `edited` | structural bound-field step | **not** a review trigger; no full pipeline re-run |

No new trigger source, scheduler, polling loop or provider call is introduced.

## Findings policy

- Advisory is **not a gate**: it is not a required context and never a green
  result. Absence/failure/usage-limit/superseded-head output never satisfies a
  mandatory review condition and never waives DCO or required validation.
- Findings are triaged under the R3 rubric by reference. The four named classes
  are examples, not an exhaustive safe list; an unmet applicable acceptance,
  authorization, security or required-validation condition stays blocking.
- No severity label (`low`, `theoretical`, `pre-existing`, `out-of-scope`,
  `follow-up`) dispositions a mandatory finding as non-blocking.
- Every disposition carries finding id, candidate head, evidence reference,
  classification, decision-maker, outcome and, for a follow-up, a backlog id.
- Carried findings remain visible in the PR triage table across heads; a later
  run that does not repeat a finding does not erase it.
- No second queue and no hidden gate.

## Trigger/yield measurement

The following fields are recordable from existing evidence for C4.2, with no
telemetry: review run id, candidate head, trigger, result or unavailable
notice, finding counts by R3 class, triaged count, fixed count,
accepted-residual/nit count and carried-finding count. They are descriptive;
no rate is a programme-completion, efficiency or dollar claim.

## Clause-by-clause preservation inventory (E2)

The E2 diff is insertion-only, 65 lines before the C2.1 section. Every clause
it could be read to affect:

| Clause | Location | Disposition | Evidence |
| --- | --- | --- | --- |
| Seven stages and stage dispositions `SD-A`-`SD-G` | [delivery-workflow.md](../delivery-workflow.md#the-seven-stages) | **kept**, no hunk | diff has no hunk |
| `MG1`-`MG5` merge conditions | [delivery-workflow.md](../delivery-workflow.md#before-merging-stage-g-entry-conditions) | **kept**; `MG3` is referenced, not restated or relaxed | diff adds a subsection after the MG block; no MG text changed |
| R3 finding-triage rubric | [delivery-workflow.md](../delivery-workflow.md#r3-finding-triage-rubric) | **kept**; referenced by link, not duplicated | diff has no hunk in the R3 table |
| Gate-passing paths and bypass recording | [delivery-workflow.md](../delivery-workflow.md#gate-passing-paths-finding-triage-and-authenticated-verdicts-c21) | **kept**, no hunk | diff has no hunk |
| Authenticated verdict consumption | [delivery-workflow.md](../delivery-workflow.md#authenticated-independent-verdict-consumption) | **kept**, no hunk | diff has no hunk |
| Required contexts and enforcement account | [delivery-workflow.md](../delivery-workflow.md#what-ci-and-branch-protection-actually-enforce-today) | **kept**; the new text explicitly registers no required context | diff text only |
| DCO | [delivery-workflow.md](../delivery-workflow.md#what-ci-and-branch-protection-actually-enforce-today) | **kept**; no waiver path added | diff text only |
| No self-approval / one active worker | [delivery-workflow.md](../delivery-workflow.md#no-self-approval-and-rule-preservation) | **kept**, no hunk | diff has no hunk |
| Exact-head invalidation | [delivery-workflow.md](../delivery-workflow.md#exact-head-invalidation) | **kept**, no hunk | diff has no hunk |
| Rule-preservation inventory for the C2 amendment | [delivery-workflow.md](../delivery-workflow.md#rule-preservation-inventory-for-this-amendment) | **kept**; this page carries the C3.3 inventory instead of editing C2's | diff has no hunk |
| Related instruments and adoption | [delivery-workflow.md](../delivery-workflow.md#adoption-and-review) | **kept**, no hunk | diff has no hunk |

**No existing clause is removed, relaxed, renamed or duplicated.** The
insertion uses the condition IDs and links, not their content.

## Approval route

The policy is effective only through the repository's rule-change route: an
independent review at the exact head, the owner's policy line (AUTH-C3-POLICY)
and a merge under separate authority. This implementer does not approve its own
text. No settings, CI, branch-protection or required-context action is
authorised by this page.

## UNRUN

The independent policy review, the rule-change approval record and the
effective-date merge are **UNRUN**. The text is a proposal until they exist.
