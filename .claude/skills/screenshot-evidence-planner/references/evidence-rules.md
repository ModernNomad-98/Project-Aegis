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
entry_path, behavior_ref, candidate_id, pre_state?, post_state?}`

Field notes: `capture_mode` is `cold_fixture_direct` (clean state reached by
direct URL with seeded data, no prior UI action) or
`visible_control_transition` (defined visible control state -> action ->
exercised state). For `visible_control_transition`, `pre_state` and
`post_state` are **required** (describe the visible states with masked/
placeholder values); for `cold_fixture_direct` they are optional/not applicable.
`entry_path` is the route template + seed fixture id + persona + action TYPES
(not typed values) that reached the state. `behavior_ref` names the
checkpoint/behavior/acceptance expectation the frame proves. `candidate_id` is
the current candidate identity (build/commit/artifact token, validated as a safe
path token before path use).

**Auto-derived / human-supplied:** auto-derive everything derivable (build,
timestamp, viewport, assembled candidate id); humans supply the non-derivable
fields — checkpoint/case linkage, `capture_mode`, the `entry_path` action
sequence, `behavior_ref`, and the `pre_state`/`post_state` descriptions.
Those human-supplied fields are masked/sanitized before storage (next section).

## Capture mode and entry path

Interaction behavior evidence must show a **visible-control transition**: start
from a defined visible control state, perform the action, capture the exercised
state, and record both `pre_state` and `post_state` (required for this mode).
`cold_fixture_direct` captures are the baseline/pre-state by default and never
substitute for the transition. Every capture must be reproducible from its
`entry_path` (route template + action types); a capture whose entry path is
unknown is context, not proof.

## Metadata privacy, masking and sanitization (before storage)

Metadata is evidence and follows the masking classes above; masking is enforced
**before storage**, like frame masking.

- `entry_path`: store the route template, not raw URLs; strip or mask query
  strings/fragments (tokens, session ids, emails, names) and record action
  **types** (`clicked sort`, `selected status filter`) rather than typed values.
  If a flow types a secret or PII, record `typed <field> (masked)` — never the
  value.
- `pre_state`/`post_state`: describe states with masked/placeholder values; no
  PII, tenant data, tokens or typed secrets. M2/M3 metadata follows the restricted
  store; if it cannot be masked, it is not stored.
- `candidate_id`: derive it from the immutable build/commit/artifact identity and
  validate it against a safe path-token allowlist before it is used in archive
  paths; never derive it from user-supplied text (path-traversal risk).
- `behavior_ref`/`checkpoint_id`/`case_or_session_id`: stable ids only; never a
  raw user string.

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

Report the three lists separately. **The planner reports contamination only: it
does not move, archive, delete, overwrite or silently prune evidence files.**
Archiving or removing historical evidence requires **explicit recorded owner
authorisation** (named owner + authorization record) and is performed by the
evidence holder, not by this planner. Review completeness is not claimed while
unexpected members remain unresolved.
