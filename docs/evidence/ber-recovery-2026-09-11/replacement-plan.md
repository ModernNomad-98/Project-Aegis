# Replacement calibration preparation

Prepared 2026-09-11 after the owner answered "no" to access to the original
review conversation. The old computer is lost, the repository scan found no
approved input bytes, and no other surviving copy is identified. Stop pursuing
that conversation. This does not assert that every possible backup was searched.

The source code and earlier review corrections survive. The next work is a new
candidate dataset and review packet, not a reconstruction of the lost approval.
This plan is preparation only; no replacement cases or approval artifact have
been generated and no execution allowance has been renewed.

## Surviving specification

Use the existing
[candidate contract and composition validator](../../../tools/behavioral_eval_runner/judge/calibration_dataset.py),
[rubrics](../../../tools/behavioral_eval_runner/judge/rubric.py), and
[historical dataset review, section 4a](../behavioral-eval-runner-wp-2b-3-summary.md).
Their requirements establish:

| Requirement | Replacement acceptance |
| --- | --- |
| Controls | A, B, C, D, G, H, I, J, N, O; 16 cases each |
| Development | 40 cases; 2 candidate PASS and 2 candidate FAIL per control |
| Holdout | 120 distinct cases; 6 candidate PASS and 6 candidate FAIL per control |
| Critical failures | At least 40 holdout candidate FAIL cases with substantively justified CRITICAL risk |
| Adversarial coverage | At least 40 holdout injection/role-confusion cases, including at least 20 candidate PASS and 20 candidate FAIL; report each attack kind and risk overlap |
| Candidate status | Every case starts PENDING with a rationale; AI suggestions are not human-approved labels |

Counts alone are insufficient. The earlier review rejected development-derived
holdout templates, ambiguous conduct and inflated risk classifications. Preserve
those lessons: different fact patterns across splits, actual multiline previews
where required, unambiguous unauthorized-write conduct, and evidence-based risk
ratings. Use the prior normalized similarity threshold of 0.85 as a screening
check alongside semantic review, not proof of independence by itself.

## Work sequence

1. **Make the replacement reproducible.** Prepare a versioned builder, explicit
   case source and labeling guide derived from the unchanged rubrics and control
   requirements. Assign a new dataset version and item namespace. Save final
   bytes as well as construction instructions; do not promise the lost hashes
   can be reproduced. Unit-test fixtures are examples of schema use, not gold
   calibration data.
2. **Prepare the review packet.** Validate schema, exact composition, duplicate
   transcripts, cross-split similarity, label-free judge envelopes and input
   size bounds using the existing code. Include the dataset, split map, guide,
   candidate rationales, distribution/quality reports and file/semantic hashes.
   Keep holdout preparation separate from later development tuning; do not put
   holdout labels into judge requests or use them to tune after freezing.
3. **Obtain fresh label approval.** Present the complete candidate packet for
   owner review, resolve identified defects, then record a newly dated approval
   binding its exact bytes. The existing sole-human-labeler allowance remains;
   do not claim independent human labels. Old approvals stay historical.
4. **Update only the changed integration terms.** The
   [driver's pinned identities](../../../tools/behavioral_eval_runner/judge/calibration_development_driver.py)
   currently require the old dataset, guide, ZIP and approval. Update paths and
   pins only after the replacement is approved, and review the resulting source
   revision. Preserve the earlier tests and execution boundaries.
5. **Finish execution readiness separately.** Resolve any unknown historical
   accounting, verify the current machine and provider setup, and establish the
   applicable remaining allowance before any metadata or judgment request.
   Missing files do not prove unused allowance. Development ends at OWNER_WAIT;
   holdout additionally needs a reviewed execution implementation and owner
   freeze, since the current client supports development only.

## GitHub and execution storage

The owner selected GitHub for project backup and stated that the project has no
secret or personal data. Keep the replacement construction source, final review
material and continuation records durably with the project. The implementation
proposal must explicitly reconcile that direction with the older external-only
dataset rule in BER-DEC-008 decisions 24–25, including the proposed canonical
location and retention of replacement material. Record the change forward;
do not silently alter historical records or bypass the live root checks.
Public availability must also be documented when assessing holdout exposure.
Execution storage and credentials remain separate from publishing project
documentation. No new private-backup requirement is introduced here.

Unchanged provider limits, retry policy, model/SDK bindings and acceptance
thresholds remain as recorded in the final
[authorization package](../../roadmaps/behavioral-eval-runner-wp-2b-3-authorization-decision-package.md).
Only changed terms need a new disposition. This plan does not reopen the whole
project or authorize paid calls. The optional local backup ZIP is unrelated to
the missing original review ZIP and is not a dependency of this work.
