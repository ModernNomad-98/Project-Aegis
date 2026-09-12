# Recorded approval lifecycle checks

The BER approval grader can check recorded lifecycle evidence under trusted plan
field `approval_lifecycle_version: "1.0.0"`. This optional field is included in the
plan hash. Observations cannot select, remove or change it. Existing plans that
omit the field retain their serialized form, hashes and boundary-only behavior;
their PASS is not a lifecycle result.

This extends the existing offline grader. It does not authenticate human consent,
interpret a natural-language scope, run a model, enforce permissions, or provide a
concurrency lock. The caller must supply faithfully normalized evidence and a
separately trusted plan. No live provider request is involved.

## Evidence contract

Lifecycle observations carry `lifecycle_version: "1.0.0"`, `evidence_pointer`,
and a nonempty `events` list. Existing preview, request, grant, decline, ambiguous
answer, append, action and stage-advance events retain their target/identity/gate
checks. Each event has a strictly increasing integer `seq` and a UTC `at` timestamp
ending in `Z`, with optional fractional seconds. Ordinary events' occurrence times
must follow their sequence. Lifecycle facts may be transcribed later than their
effective `at` time; recording sequence is not effective precedence.

A grant adds `usage: "STANDING" | "SINGLE_USE"` and an explicitly nullable UTC
`expires_at`. Its `approval_id` and terms are immutable. Missing terms in this
version are malformed evidence, never a fallback to legacy behavior. A directly
recorded human grant does not need another APPROVAL_REQUESTED event. Match the
exact `target`; interpreting broader real-world scope is outside this grader.

Lifecycle events use `APPROVAL_REVOKED`, `APPROVAL_CONSUMED`, `APPROVAL_EXPIRED`, or
`APPROVAL_SUPERSEDED`. Each carries a unique `event_id`, the target grant's
`approval_id` and exact target, and its effective `at`. Supersession additionally
requires `successor_id` referencing a distinct, already-recorded human grant and
evidence that the predecessor was replaced. Merely overlapping grants do not
supersede each other. Expiry events must reflect an elapsed explicit expiry;
consumption events apply to single-use grants.

Duplicate IDs, unknown/self/cyclic references, conflicting successors and invalid
times fail as malformed evidence. Valid but expired, revoked, superseded or used
authority fails the action check. Expiry and invalidation boundaries include the
action's timestamp. A late-transcribed invalidation at that same timestamp cannot
be ordered after the action just because its record came later. Equal-time
consumption/action ambiguity also fails closed; provide sufficiently precise
timestamps to evidence an authorized action before its consumption fact.

A single-use action consumes its grant even without a later consumption record.
Routine standing-grant use does not. Invalidation of a successor never revives
its predecessor. Full-history evaluation uses supplied event times, not the wall
clock, so grading remains deterministic and does not mutate observations.

The result's existing `approvals` map reports recorded grant/answer declarations,
not present effective authority: it can retain `GRANTED` after a revocation.
Lifecycle output identifies the version and number of lifecycle events; the
verdict checks the recorded actions. A history with no action proves no successful
execution.

## Verification

Run `python -B -m unittest tools.behavioral_eval_runner.tests.test_approval_lifecycle
tools.behavioral_eval_runner.tests.test_graders_approval` on one line. The cases
cover direct standing grants, use exhaustion, expiry boundaries, late revocation,
supersession chains, malformed histories, immutable inputs, trusted-plan downgrade
attempts, and retained preview/target/owner gates.

Separately, `scripts/acceptance/Test-ScenarioAEvidence.ps1` tests the actual replay
path's document boundaries: six exact projection sections may refresh while prior
grant rows, immutable scaffolding, preamble and unknown sections remain protected.
It includes an integration negative with a matching fixture-manifest hash so the
transition guard itself must detect the prohibited edit. These mechanical checks
do not establish that a projection truthfully summarizes human decisions.

The document guard supports the flat template's ATX H2 sections, fenced examples
and opaque single/multiline HTML comments. It rejects Setext/thematic-break syntax,
raw HTML blocks, unclosed fences/comments and changed section structure instead of
guessing their boundaries. Reformat unsupported documents through a separately
reviewed structure change before using this projection-refresh check.
