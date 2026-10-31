# Evidence Rules Reference

Detail file for `screenshot-evidence-planner`. Loaded on demand.

**Use:** Apply these capture and storage rules through the
[screenshot-evidence-planner workflow](../SKILL.md). `cp-id` is a checkpoint
identifier; `CP-INV-03` and `MC-INVITE-004` are illustrative catalog and case
identifiers, not universal codes. SHA means Secure Hash Algorithm and denotes
a commit identifier here; PII means personally identifiable information; PR
means pull request; and CI means continuous integration. M0–M3 are this
page's storage-sensitivity classes, defined in the masking table below.

## Checkpoint selection catalog

Evidence-worthy states (justify each against a consumer):

| State class | Why captured |
| --- | --- |
| Requirement-proving state | the visible outcome an acceptance criterion names |
| Before/after destructive action | proves confirmation + correct result |
| Permission-view difference | persona A vs persona B on the same route |
| Error/empty states under test | proves graceful handling shipped |
| Defect evidence | every filed defect gets its capture |
| Compliance-named states | whatever the obligation text actually requires |

Not evidence-worthy by default: every navigation step, every passing form,
duplicate states across viewports without a viewport-specific risk.

## Naming token table

Pattern: `<cp-id>--<route-or-case>--<persona>--<build>--<yyyymmdd-hhmmss>.png`

- `cp-id`: checkpoint id from the catalog (`CP-INV-03`) or `DEFECT-<id>`.
- `route-or-case`: kebab route (`settings-billing`) or case id (`MC-INVITE-004`).
- `persona`: role token (`admin`, `member`), never a real name/email.
- `build`: short commit SHA or build number.
- Counter-example: `Screenshot (47).png` — unlocatable, unattributable.

## Masking classes

| Class | Contents | Rule |
| --- | --- | --- |
| M0 public | verified synthetic seed data and a whole-frame inspection showing no secrets, sensitive content, or other tenant data | no masking needed after inspection — preferred path |
| M1 internal | internal test accounts, no PII | mask tokens/keys if visible |
| M2 sensitive | any real PII, financials, tenant names | block-out before storage; restricted store |
| M3 cross-tenant | any other tenant's data visible | do not store; recapture with seeded data; report as an isolation observation |

Method: opaque block-out. Blur/pixelation of text is recoverable; crop loses
context. Masking happens before the file reaches storage.

## Metadata schema (sidecar or report table)

`{capture_id, checkpoint_id, case_or_session_id, build, environment,
persona, viewport, captured_at, masked: bool, storage_class, capture_mode,
entry_path, behavior_ref, candidate_id}`

Field notes: `capture_mode` is `cold_fixture_direct` (clean state reached by
direct URL with seeded data, no prior UI action) or
`visible_control_transition` (defined visible control state -> action ->
exercised state; also record `pre_state`/`post_state`). `entry_path` is the
URL/route + seed fixture id + persona + action sequence that reached the state.
`behavior_ref` names the checkpoint/behavior/acceptance expectation the frame
proves. `candidate_id` is the current candidate identity (build/commit/artifact).

Auto-derive everything derivable (build, timestamp, viewport); humans only
supply the checkpoint/case linkage.

## Capture mode and entry path

Interaction behavior evidence must show a **visible-control transition**: start
from a defined visible control state, perform the action, capture the exercised
state (also record the pre-state when context matters). `cold_fixture_direct`
captures are the baseline/pre-state by default and never substitute for the
transition. Every capture must be reproducible from its `entry_path`; a capture
whose entry path is unknown is context, not proof.

## Storage-class matrix

| Class | Location | Retention | Access |
| --- | --- | --- | --- |
| PR artifact | CI artifact store | short (e.g. 30d) | repo access |
| Release evidence | release record/tag bundle | product policy (e.g. 1-2y) | team |
| Compliance archive | designated archive | per obligation text | restricted |
| Playwright traces | Synthetic or masked data only for evidence; separately approved sensitive transient captures follow a restricted access and deletion rule, outside the evidence store | shortest approved period | evidence access or the separately approved restricted capture access |

## Current-candidate evidence set membership

For the current candidate, the checkpoint plan defines the **expected member
list** of evidence; each capture carries the candidate's `candidate_id`.
Compare the current evidence root against that expected list:

- **expected members** — listed in the evidence-set record for this candidate;
- **unexpected members** — files under the current root that are not in the
  expected list, including stale/superseded images from an earlier candidate.
  They are **contamination, not extra coverage**; do not count them, and do not
  delete them without authorisation;
- **historical archive** — earlier-candidate evidence kept in a candidate-scoped
  archive/record with its retention class and a superseded marker.

Report the three lists separately. Membership check detects contamination; it
never deletes, overwrites or silently prunes historical evidence.
