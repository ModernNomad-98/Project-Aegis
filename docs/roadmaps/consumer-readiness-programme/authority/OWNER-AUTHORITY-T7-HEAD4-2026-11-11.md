# OWNER AUTHORITY — T7-EQUIVALENT SCOPED FOURTH HEAD FOR PR #1016 (2026-11-11)

## Owner message (verbatim)
"I authorize ONE scoped fourth candidate head for PR #1016 under the programme's review-head exception (T7-equivalent): head 4 is permitted solely to fix B13 — reviewer independence must require distinct_from to include the PR author, the implementer, and every commit author, with a discriminating negative test — after which independent Stage D/E/F must be re-run at the new exact head. This is the final additional head, no other scope change, no plan revision, no settings/CI/provider action, and Stage G may proceed only if the new Stage F verdict is APPROVE-FOR-MERGE."

## Scope
- One additional head (head 4) on branch impl/c11a-rev2-2026-11-10 for PR #1016, solely to fix B13.
- Required fix: reviewer.independence.distinct_from must require the PR author and implementer roles (and declared commit-author identities where declared) and reject a reviewer identity matching any required role; discriminating negative test required.
- Then fresh independent Stage D/E/F at the new exact head; Stage G only on Stage F APPROVE-FOR-MERGE.
- No other scope change, no plan revision, no settings/CI/provider action.

## Implementation note
The record format has no provider commit-author identity list; the checker requires the pr-author and implementer roles and will require any declared commit-author identities under reviewer.independence.commit_authors. Commit-author identity population from provider events remains T6-UNRUN and is documented as such.

## Non-claims
This exception is not a merge approval, not design acceptance, and not authority beyond the single B13 fix head.

Recorded by: Lead (DeepSeek Harness; route deepseek-flash).
