# Anonymized improvement log

Entries are numbered U-* for owner-raised and A-* for build-session-raised. Identifying detail is removed: no product name, owner name, accounts, repository or file names, dates, prices, devices or vendors. Context: the owner directed a multi-stage delivery programme; a self-described experience level was not recorded in the session, so it is not asserted here. This file is never sent anywhere; passing it on is the owner's decision and action.

## U-1 — Working scope (owner-raised)
- Stage: discover/preflight. Category: helpers and workspace.
- Problem: the delivery assistant searched locations outside the project repository while looking for missing evidence; the owner limited scope to the project repository and asked to be told about anything else.
- Suggested improvement: limit evidence searches to declared paths and require explicit owner permission for broader search.
- Still open for the framework: yes.

## U-2 — Parallel work and cost (owner-raised)
- Stage: build/deliver. Category: parallel work, cost and platform.
- Problem: the work was being executed serially; the owner asked for parallel work in separate working trees, cost-efficient merging, and grouping of small fixes.
- Suggested improvement: make one working tree per independent delivery unit a default, and state the cost default at intake.
- Still open for the framework: yes.

## U-3 — Merge authority changed mid-flight (owner-raised)
- Stage: deliver. Category: approvals.
- Problem: two owner statements conflicted about whether the assistant could merge; a clarification question was needed before any merge.
- Suggested improvement: record merge authority as a decision with an explicit change protocol.
- Still open for the framework: yes.

## U-4 — Missing evidence delivery (owner-raised)
- Stage: discover/preflight. Category: records.
- Problem: expected evidence locations were empty; the owner had to supply the package, and the task had been blocked before that.
- Suggested improvement: record how evidence will be delivered, and check the delivery folder before declaring a block.
- Still open for the framework: yes.

## A-1 — Completion check satisfied by a neighbouring marker
- Stage: plan. Category: accuracy.
- Problem: a completion check could pass because a different item's note sat within one line; an independent audit rejected it and the plan was revised.
- Suggested improvement: require a marker on the item's own line and make the check machine-verifiable.
- Still open for the framework: yes.

## A-2 — Final-review document was a pre-publication draft
- Stage: deliver. Category: records.
- Problem: the review document described an unpublished state while the public work item was already live with reviews and checks.
- Suggested improvement: produce that document only after the public work item exists, or require live-fact fields.
- Still open for the framework: yes.

## A-3 — No per-stage skill-use record existed
- Stage: build/validate. Category: records.
- Problem: the required skill-use table needed one self-authored row per stage; most stages had not written one, and rows had to be collected late.
- Suggested improvement: make the self-authored row a stage-exit deliverable.
- Still open for the framework: yes.

## A-4 — A pinned line was split by a legitimate edit
- Stage: validate. Category: review and testing.
- Problem: an edit placed a note inside a sentence that an automated check pins as a contiguous string; two required checks failed until the note was moved.
- Suggested improvement: document pinned substrings where edits happen, or compare text with markup stripped.
- Still open for the framework: yes.

## A-5 — A known-failing non-required check blocks the merge condition
- Stage: deliver. Category: review and testing.
- Problem: an automated check fails on every work item because of a known defect in its own test, while the merge rule requires all applicable checks green.
- Suggested improvement: fix the defect, or mark the job expected-fail/skip with a visible reason.
- Still open for the framework: yes.

## A-6 — An owner question was lost to a tool timeout
- Stage: any. Category: questions.
- Problem: a structured question to the owner timed out before an answer was captured.
- Suggested improvement: persist interactive questions before waiting for an answer.
- Still open for the framework: yes.

## A-7 — Long validation dominate elapsed time
- Stage: validate. Category: cost and platform.
- Problem: the main self-test takes many minutes and several agents took tens of minutes.
- Suggested improvement: cache or parallelise long checks and start them early.
- Still open for the framework: yes.

## A-8 — Worked well: independent stage agents found real defects
- Stage: validate/review. Category: review and testing.
- What worked: separate agents found completion-check gaming, stale documents, contradictions, a pinned-line break and missing records before anything merged.
- Keep: the different-agent stage separation.

## A-9 — Worked well: resume preserved prior state
- Stage: discover. Category: records.
- What worked: the saved checkpoint's revision, preserved unrelated file and identity records all matched on resume; nothing was lost or redone.
- Keep: the preservation checklist and the do-not-delete rule.

## A-10 — Unknown working tree appeared
- Stage: build. Category: helpers and workspace.
- Problem: a working tree not created by the assistant appeared and had to be investigated and preserved.
- Suggested improvement: save/resume should list and label working trees created by other sessions.
- Still open for the framework: yes.

## A-11 — Resume asserted teammates that were not present
- Stage: discover. Category: helpers and workspace.
- Problem: the saved state described a helper roster that did not exist after resume.
- Suggested improvement: record verified helper availability instead of an assumed roster.
- Still open for the framework: yes.

## A-12 — Repeated automated reviews multiplied the disposition work
- Stage: review. Category: review and testing.
- Problem: several automated reviews across successive revisions produced a large duplication burden in the final record.
- Suggested improvement: keep one review per revision head and deduplicate findings across revisions.
- Still open for the framework: yes.
