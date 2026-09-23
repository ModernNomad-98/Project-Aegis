# Seven operational guides: current-reading correction

Date: 2026-09-23. Edit start: 21:08:20 UTC. Base: `37c018d166f0647703b4a0f7009ae0ca4c5e32b0`
(merged pull request #169). Prior smaller screen estimate: 2–4 active hours;
this bounded seven-page correction estimate: 4–8 active hours. The selected
overall backlog estimate at planning time was 175–394 active hours.
These are active-work estimates. Draft freeze: 21:11:42 UTC; observed
start-to-freeze wall time: 3 minutes 22 seconds, excluding independent review.

## Scope and source reconciliation

This batch edits the seven listed guides and this evidence note. It does not
change a decision entry, approval, runtime, test, fixture, host, private input,
or provider boundary. Original proposal, grant, table, and threshold text stays
in place; added first-screen notes distinguish a dated snapshot from current
delivery and point to the owning backlog or evidence.

| Guide | Current fact used by the new reading note | Historical text retained |
| --- | --- | --- |
| BER replacement storage decision | Its own implementation checkpoint records BER-DEC-010 merge in PR #106, private owner-only input repository creation and PENDING packet; the [BER backlog](../../roadmaps/behavioral-eval-runner-backlog.md) remains the authority route. | Pending-amendment proposal, alternatives, questions and conditions. |
| Selected-host capability proposal | The [open-decision index](../../roadmaps/aegis-open-decisions-2026-09-23.md) records a disposable POSIX direction without a named host or proof. | Stage A/B proposal and R4/R5 proof criteria. |
| Holdout execution scope | The [BER backlog](../../roadmaps/behavioral-eval-runner-backlog.md) records WP-2B-3 authorized but incomplete; the private candidate packet remains pending. | Exact proposed branch, file scope and execution gates. |
| CP-WP-003 offline proof proposal | The [CP backlog](../../roadmaps/resumable-control-plane-backlog.md) and [CP-WP-003A review](../control-plane/cp-wp-003a-review.md) record AEGIS-APR-006 / PR #123 synthetic delivery; real CP-WP-003 remains blocked. | Proposed first-increment grant and negative-proof matrix. |
| BER fast-track successor | The [BER backlog](../../roadmaps/behavioral-eval-runner-backlog.md) records WP-2B-3 authorized and incomplete; WP-2B-4 blocked. | Original design status and phase-map history. |
| Semantic-review rubric | The [runner guide](../../../tools/behavioral_eval_runner/README.md) documents the offline runner; measured/live proof remains gated. | Original twelve-question rubric and coverage protocol. |
| AEGIS-060+ register | The current first-screen disposition rejects AEGIS-060; sections 3–5 are the older 184-skill baseline. | Candidate analysis, counts, dedup map and historical remediation sequence. |

## Validation and closeout

At the local draft checkpoint, a relative-link and heading-anchor check
covered 45 links in these eight pages with zero failures. The first pass
treated a valid directory link as a file and was corrected before the passing
rerun. `python scripts/validate-skills.py` reported 185 valid skills and zero
warnings; this checks skill structure, not arbitrary Markdown content.
`git diff --check` passed. The seven existing guides have additive first-screen
notes only; no original proposal or table line was removed. Independent
read-only review is pending at this draft checkpoint.

No provider calls, real host probes, private-input reads or credential access
were part of this batch.
