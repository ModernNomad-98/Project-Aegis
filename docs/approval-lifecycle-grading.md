# Recorded approval lifecycle checks

This guide is for maintainers testing whether a *recorded* action matched the
recorded life of an approval. The Behavioral Eval Runner (BER) approval grader
replays a trusted plan and an ordered event history. It can distinguish an
effective grant from an expired, revoked, superseded or consumed one. It cannot
decide whether a human truly consented or whether prose granted an action's
real-world scope.

## Normal use and a small example

1. Supply a separately trusted grading plan that opts into lifecycle version
   `1.0.0`. Record its exact target and approval terms before observations.
2. Supply normalized events with unique identities and accurate times. The
   caller is responsible for faithfully capturing human decisions and evidence.
3. Run the [offline tests](#verification) or grade recorded evidence. Read the
   action verdict and lifecycle fields together; a `GRANTED` declaration alone
   does not prove effective authority.

For example, a single-use approval can authorize one exact-target action
before expiry. A second action cannot reuse it, and an action at the expiry
instant fails. This rule concerns the supplied history; it creates no new
approval and is not a live permission check.

## Scope and compatibility

The BER approval grader can check recorded lifecycle evidence under trusted plan
field `approval_lifecycle_version: "1.0.0"`. This optional field is included in the
plan hash. Observations cannot select, remove or change it. Existing plans that
omit the field retain their serialized form, hashes and boundary-only behavior;
their `PASS` result checks only the older boundary contract, not lifecycle.

This extends the existing offline grader. It does not authenticate human consent,
interpret a natural-language scope, run a model, enforce permissions, or provide a
concurrency lock. The caller must supply faithfully normalized evidence and a
separately trusted plan. No live provider request is involved.

## Evidence contract

Lifecycle observations carry `lifecycle_version: "1.0.0"`, an
`evidence_pointer` that refers to the retained record, and a nonempty `events`
list. Existing preview, request, grant, decline, ambiguous
answer, append, action and stage-advance events retain their target/identity/gate
checks. Each event has a strictly increasing integer `seq` and a Coordinated
Universal Time (UTC) `at` timestamp
ending in `Z` (the UTC designator), with optional fractional seconds. Ordinary
events' occurrence times
must follow their sequence. Lifecycle facts may be transcribed later than their
effective `at` time; recording sequence is not effective precedence.

### Grant terms

A grant adds `usage: "STANDING" | "SINGLE_USE"` and an explicitly nullable UTC
`expires_at`. Expiry cannot precede the grant's `at`; an equal timestamp is a
valid interval that is already inactive. Its `approval_id` and terms are immutable.
Missing terms in this version are malformed evidence, never a fallback to legacy
behavior. A directly recorded human grant does not need another APPROVAL_REQUESTED
event. Match the
exact `target`; interpreting broader real-world scope is outside this grader.

### Changes to a grant

Lifecycle events use `APPROVAL_REVOKED` (withdrawn), `APPROVAL_CONSUMED`
(single use spent), `APPROVAL_EXPIRED` (time limit reached), or
`APPROVAL_SUPERSEDED` (replaced by a later grant). Each carries a unique
`event_id`, the target grant's `approval_id`, its exact target, and its
effective `at`. Supersession additionally
requires `successor_id` referencing a distinct, already-recorded human grant and
evidence that the predecessor was replaced. Merely overlapping grants do not
supersede each other. Expiry events must reflect an elapsed explicit expiry;
consumption events apply to single-use grants.

### How the verdict is decided

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

From the source checkout, run this offline test command on one line:

```text
python -B -m unittest tools.behavioral_eval_runner.tests.test_approval_lifecycle tools.behavioral_eval_runner.tests.test_graders_approval
```

The cases
cover direct standing grants, use exhaustion, expiry boundaries, late revocation,
supersession chains, malformed histories, immutable inputs, trusted-plan downgrade
attempts, and retained preview/target/owner gates.

Separately, `scripts/acceptance/Test-ScenarioAEvidence.ps1` tests the actual replay
path's document boundaries: six exact projection sections may refresh while prior
grant rows, immutable scaffolding, preamble and unknown sections remain protected.
It includes an integration negative with a matching fixture-manifest hash so the
transition guard itself must detect the prohibited edit. These mechanical checks
do not establish that a projection truthfully summarizes human decisions.

The document guard supports the flat template's Markdown level-two headings
written with `##` (the ATX form), triple-backtick fenced examples, and opaque
single- or multiline HyperText Markup Language (HTML) comments. It rejects
underlined headings (Setext form), horizontal-rule/thematic-break syntax, raw
HTML blocks, unclosed fences/comments and changed section structure instead of
guessing their boundaries. Reformat unsupported documents through a separately
reviewed structure change before using this projection-refresh check.
Empty `##` headings are rejected; other named heading levels stay protected.
Multiline comment openers must stand alone with no more than three leading spaces,
so inline or indented code cannot mask a real section boundary.
