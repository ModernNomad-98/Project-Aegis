# Aegis delivery control plane

The **delivery control plane** is a safety kernel for continuing a long-running
engineering task after a pause, crash or uncertain external effect. It is for
Project Aegis maintainers building controlled delivery workflows. Its job is
to decide, from durable facts, whether a proposed next operation still has
valid authority, budget, identity and evidence. The shipped package is an
**offline synthetic kernel**: it demonstrates those decisions with fake
authorities and targets, not with GitHub, a model provider or a production
deployment. Its kernel decisions stay offline and synthetic; exactly one
opt-in, read-only command, `ci-durations` (`--allow-network`), additionally
reads public GitHub run metadata and never writes or dispatches anything.

For example, if a synthetic target accepts a change but the controller crashes
before receiving the receipt, the controller must not assume the change failed
and send it again. It retains the outstanding operation and budget liability,
then reconciles the target's durable receipt. If the evidence is missing or
contradictory, further dispatch stays blocked. This is the problem the kernel
is designed to solve.

Control-plane work package 003A (CP-WP-003A) added offline negative capability
probes in `capabilities.py` and tests. The dispatch coordinators reject a
lookalike authority or target before committing an intent. Passing synthetic
source, freshness, containment, owned-path, evidence or accounting probes
does not authorize a real route; `require_real_dispatch` always denies it. A
selected source and host, independent freshness proof, actual evidence and
billing policy remain open work-package 003 gates.

## Boundary

The [control-plane design](../../docs/design/resumable-control-plane-v1.md)
defines the full intended system. The
[backlog](../../docs/roadmaps/resumable-control-plane-backlog.md) separates
delivered synthetic behavior from real source, host and integration gates.
**Control-plane work package 002** delivered the offline state and recovery
kernel. **Work package 003A** delivered a bounded offline capability-proof
increment; it did not establish a real authority source or host. These numbers
name work packages, not runtime versions.

## How a controlled operation works

1. **Accept an exact plan.** The kernel binds a repository, source revision,
   item, policy and validation checks to one immutable operation identity.
2. **Check authority and reserve capacity.** A synthetic issuer grants a
   one-use capability. The kernel verifies its current status, reserves a
   bounded budget and occupies one repository-wide outstanding operation slot.
3. **Commit intent before contact.** A transaction records permission use,
   budget liability, the operation intent and its expected target identity.
   The synthetic adapter may contact its target only after that commit.
4. **Record receipts and validation.** The synthetic target and validator keep
   separate durable ledgers. A receipt or validator result is checked against
   the exact operation, then applied once. An uncertain result retains the
   slot and worst-case liability until authoritative reconciliation.
5. **Recover conservatively.** After restart, the kernel replays its events,
   checks hashes and source freshness, and preserves fences from pauses,
   revocations, stop requests or conflicting observations. It never converts
   an unknown effect into permission to retry.

The lifecycle includes explicit pause, resume, stop and finalization routes.
Design identifiers such as `T03` (transition 03, dispatch intent) and `T27`
(transition 27, validator intent) refer to rows in the
[design transition table](../../docs/design/resumable-control-plane-v1.md);
they are not commands a user should type.

Each transition row also lists guards: named preconditions such as
`no_fence` or `budget_available` that the design requires before the
transition commits. In `engine.py` that list is an advisory catalog. The
engine denies an unknown transition, a disallowed state pair or event variant,
and any change to a terminal state, but every production caller reports the
full guard list as satisfied, so the engine's guard comparison never denies a
production call. The checks that decide whether a guard holds are inline in
`storage.py` and the authority and contract checks it calls.
[`tests/test_guard_traceability.py`](tests/test_guard_traceability.py) pins
that calling pattern and maps each transition-guard pair to its inline check
and to a test that is denied when the guard fails.

## What the package files do

**Reading key:** SQLite is the embedded database engine that stores local
state in a file. SHA-256 (Secure Hash Algorithm 256-bit) is a digest of bytes:
it helps detect changes against a trusted value, but does not itself grant
authority or prove the source is fresh.

| File | Responsibility |
| --- | --- |
| `contracts.py` | Define typed operation, event, permission, budget and result records; reject malformed or ambiguous inputs. |
| `engine.py` | Hold the transition table and deny a transition, state pair or event variant it does not list. Its guard lists are an advisory catalog; `storage.py` enforces them. |
| `storage.py` | Keep an append-only event chain and transactionally owned projections in a repository-scoped SQLite database. |
| `authority.py` | Verify and redeem synthetic issuer permissions; a local permission is not a real external approval. |
| `adapters.py` | Provide the synthetic execution and validator targets with separate durable receipt ledgers. There are no real adapters. |
| `dispatch.py` | Coordinate permission, intent and synthetic target contact order; compare a returned receipt with the exact committed operation before intake. |
| `evidence.py` | Canonicalize a synthetic evidence record, create a new evidence file and return its SHA-256 hash. Receipt and authority checks occur in the dispatch, authority and storage paths. |
| `owned_paths.py` | Resolve the user-state root and reject unsafe links, ownership and path substitutions. |
| `cli.py` | Provide a read-only command-line interface for capabilities, status, verification and the CI-run duration reader. No lifecycle mutation command is exposed. |
| `ci_durations.py` | Read one public GitHub Actions run's per-job durations and coverage: conclusion-first job state, honest `not_recorded`/`not_applicable` tokens and a head-bound status marker. Offline unless `--allow-network` is given. |

The kernel allows one outstanding synthetic operation per repository. The
operation slot remains occupied while an effect, validator or accounting
obligation is unresolved. Event replay is checked against the stored sequence,
predecessor hashes and identity bindings before projections are trusted.

## Read-only commands

From the Project Aegis source checkout, this command reports what the local
package can actually do without opening a state database:

```powershell
python -m tools.aegis_delivery_control --repository-id example-project capabilities
```

`status` reads the repository's local state if it exists. It does **not**
establish that the state is fresh against an independent source:

```powershell
python -m tools.aegis_delivery_control --repository-id example-project status
```

`verify` compares the stored state with an independently supplied freshness
vector and checks synthetic issuer evidence. It requires both a vector file
containing exactly `repository_id`, `catalog_head` and `run_heads`, and a
separate file containing the synthetic issuer key under
`synthetic_issuer_key_hex`. These are test inputs, not production credentials.
Both files are JavaScript Object Notation (JSON). In the expected vector,
`repository_id` must match the command's repository identity, `catalog_head`
is the independently expected catalog revision, and `run_heads` maps each run
identifier to its independently expected head. The separate key file has
exactly `synthetic_issuer_key_hex`, a hexadecimal synthetic issuer key from
the same offline test authority. The
[command-line test fixture](tests/test_dispatch.py) shows the two JSON shapes
and obtains their values from a synthetic setup; `verify --help` lists the
required file arguments. That fixture exercises the command shape, not an
independent freshness proof. Do not derive the expected vector from the state
being checked when making a freshness claim, or substitute a real credential.
Create both files from an
independently trusted synthetic fixture before using these ordinary path
examples:

```powershell
python -m tools.aegis_delivery_control --repository-id example-project verify --expected-vector .\vector.json --authority-key-file .\synthetic-key.json
```

Verification denies a missing database, mismatched identity or head, malformed
input, unsafe path, or unavailable source fact. A state file's own contents
cannot prove its freshness. The command changes no run's lifecycle state; it
does not repair or advance a run, though opening the state file may apply a
pending schema migration.


## ci-durations: read the duration of one CI run (read-only)

`ci-durations` answers one question honestly: *what did each job of this
GitHub Actions run actually do, and may I call it green?* It reads one run
and its jobs through the GitHub REST API, prints a fixed evidence report to
standard output, and writes nothing. It is the one command in this package
that can reach the network, and only when you ask for it:

```powershell
python -m tools.aegis_delivery_control --repository-id example-project ci-durations --run-id 38198781208 --allow-network --candidate 4d5ccb0b38369812bef198b7083d113d559ad387 --format table
```

The **offline form** replays a `{"<url>": <payload>}` fixture map of the two
endpoints the reader calls (`.../actions/runs/<id>` and its `/jobs`). A
fixture always wins over `--allow-network`, and the fixture path constructs
no transport and opens no socket. The test module is the fixture's source of
truth, so an operator can emit one and replay it:

```powershell
python -m tools.aegis_delivery_control --repository-id example-project ci-durations --run-id 38198781208 --fixture tools/aegis_delivery_control/tests/fixtures/run-38198781208.json --candidate 4d5ccb0b38369812bef198b7083d113d559ad387 --now 2026-10-12T04:00:00Z
```

`--show-identity` prints the command's fixed identity block (read-only true,
one host, no mutating verb, no artifact download) as JSON and exits 0.

### Boundary of this one command

- **One host, with no override.** The only contactable host is
  `api.github.com`; no argument selects another, so a GitHub Enterprise
  deployment is out of scope for this reader. The live transport also
  **refuses any redirect that changes scheme or host**, so a 3xx response
  cannot move the read - or the `--token-env` bearer token - to a second host.
- **Opt-in, read-only, no token required.** Live reads require
  `--allow-network`. No POST, PUT, PATCH or DELETE is ever issued, no file is
  written, no artifact is downloaded and `gh` is never invoked. `--token-env
  GH_TOKEN` names an environment variable (never the token itself) and is
  applied only to `api.github.com`, to lift the anonymous rate limit.
- **Never auto-run.** No workflow, schedule, hook or wrapper calls it; a
  person or an agent runs it deliberately. FAST SAVE never triggers it.

### Exit codes and the status marker

| Exit | Marker | Meaning |
| --- | --- | --- |
| 0 | `COMPLETE` | Evidence printed; the run is green and `--candidate` equals the run head. |
| 1 | `STALE`, `INCOMPLETE` or `UNBOUND` | Evidence printed, but nothing is certified: the candidate differs, a required field is missing, or no `--candidate` was supplied. |
| 2 | (none) | Refused or unresolvable input: no `--fixture` and no `--allow-network`, an unknown workflow, no run for the head, a malformed fixture, a missing artifact directory, or an `--attempt N` the run payload cannot confirm. |
| 3 | (none) | Transport or API failure: HTTP status, timeout or malformed JSON. |
| 4 | `FAILED` | Evidence printed, but the run or an executed job is not green. |

**Exit 0 is a green, head-bound claim - not merely "the report is complete".**
`--candidate` is required for it: without a candidate the marker is `UNBOUND`
and the exit code is 1. The candidate must also **bind**: if the run payload
records no usable `head_sha`, `candidate_status` is `unresolvable`, the
reason carries `candidate_status=unresolvable`, and the exit code is 1. The
reader never rounds a missing, skipped or red value up to a pass: a skipped
job is `not_applicable` whatever its timestamp window looks like (-1 s, 0 s or
absent), an unrecorded value is the literal token `not_recorded` and never
zero, an executed job that is not `success` is never green, and a missing
roster job is a reported `roster_delta`.

Two further gaps force `INCOMPLETE` (exit 1) rather than a pass:

- **A required job the event makes unconditional was skipped.** On a
  `pull_request` run `gate-guard` is unconditional and branch-protected, so a
  skipped `gate-guard` yields `required-job-skipped:gate-guard`. On a push the
  same skip is the lawful event filter and stays green. A skipped `changes` is
  always lawful: `changes` is the path filter itself.
- **The jobs list was truncated.** If the API advertises a `total_count`
  larger than the jobs actually read, the report says `jobs-truncated`,
  `jobs_truncated` is `true`, and `roster_delta` names `truncated-jobs-page`.
  Later pages are fetched while the advertised total demands them.

`--attempt N` **selects or refuses**: when the run payload reports a different
`run_attempt` (or none), the command exits 2 with the mismatch named, instead
of silently reporting attempt 1 for every request.

### Worked example (run 38198781208, push, head 4d5ccb0b, attempt 1)

| job | state | conclusion | duration_s | exit_code | coverage |
| --- | --- | --- | --- | --- | --- |
| changes | executed | success | 7 | not_recorded | demonstrated |
| validate-skills | executed | success | 109 | not_recorded | demonstrated |
| gate-guard | skipped | skipped | not_applicable | not_recorded | not_selected |
| windows-offline-checks | executed | success | 224 | not_recorded | demonstrated |
| tools-tests-linux | executed | success | 132 | not_recorded | demonstrated |
| tools-tests-windows | executed | success | 229 | not_recorded | demonstrated |

`STATUS: COMPLETE (exit 0)`. `gate-guard` is skipped because it is a
pull-request-only job on a push run. A GitHub job record carries a
*conclusion*, never a process exit code, so `exit_code` stays `not_recorded`
unless you also pass `--artifact-dir` with the extracted
`record-check.py` artifacts. Each record is then used only for the job whose
**real uploaded artifact name** contained it
(`offline-checks-linux-<run>-<attempt>` maps to `validate-skills`,
`offline-checks-windows-...` to `windows-offline-checks`,
`tools-tests-linux-...` and `tools-tests-windows-...` to their same-named
jobs; `changes` and `gate-guard` upload nothing), and only when the record
binds to the run head. One uploaded directory holds **many** records - the
`offline-checks-linux` artifact alone is fed by every recorded step of that
job - so the whole per-job set is reported in `exit_codes` with its
provenance, and the singular `exit_code` is filled only when every bound
record agrees on one code; otherwise it reads `not_applicable` rather than
promoting one arbitrary record to the job.

On a `pull_request` run the binding field is **`pr_head_sha`**, not
`checkout_sha`: GitHub checks out a synthetic merge commit that no contributor
signed, and the workflow records the pull request head separately
(`AEGIS_PR_HEAD_SHA`). On a push the checkout *is* the head, so
`checkout_sha` binds. Both fields are listed in the provenance, and an
unrecognised directory is reported as `not_mapped`, never guessed at.

### Step-level prerequisites

The two pull-request-only steps of the `validate-skills` job - `Verify DCO
sign-off on every commit` and `pr-body-skills-check` - are reported under
`step_details` with the state the API actually returned for them: `executed`
on a `pull_request` run, `skipped` on a push, and `not_recorded` when the
payload does not carry the step. Only genuinely skipped steps appear in
`step_skipped`, so a pull-request report never claims a validation gap the
workflow does not have.

## Storage and current guarantees

State lives outside the repository checkout in a user-local directory:

- Windows: the operating system's LocalAppData known folder, then
  `ProjectAegis/control-plane/<repository-hash>/state.sqlite3`.
- Linux: the `XDG_STATE_HOME` environment variable selects the user-state
  directory when set; otherwise use
  `$HOME/.local/state/project-aegis/control-plane/<repository-hash>/state.sqlite3`.

The database uses SQLite transactions, rollback journaling and
`synchronous=FULL`, SQLite's request to sync transaction writes to storage.
The process-crash tests do not prove physical power-loss durability. A stable
operating-system lock excludes cooperating writers. The synthetic target and
validator each have their own SQLite
ledger, so a restarted controller can reconcile an accepted effect or result
without issuing it again. Checked paths reject unsafe links and ownership;
unsupported path guarantees close dispatch.

Tests establish process-crash and transaction-rollback behavior for the
supported local fixtures. They do not prove power-loss durability of a disk,
real source-atomic approval across other consumers, independent monotonic
freshness, real-host process containment, a production evidence access policy,
or billing reconciliation. Those remain later gates. A successful synthetic
test never authorizes an external side effect.

## Tests and further reading

The focused offline suite runs without a real target or provider:

```powershell
python -m unittest discover -s tools/aegis_delivery_control/tests -p "test_*.py" -v
```

Record the exact revision, platform and skips with results. The
[work package 002 review](../../docs/evidence/control-plane/cp-wp-002-codex-handoff.md)
contains the accepted transition, crash and recovery evidence. The
[work package 003A proposal](../../docs/roadmaps/cp-wp-003-offline-proof-proposal.md)
explains the delivered synthetic proof boundary. The
[backlog](../../docs/roadmaps/resumable-control-plane-backlog.md) is the
current status source for any real integration claim.

## Role/stage transition contract (ZT-P1)

Work package ZT-P1 adds an **offline synthetic role/stage transition
contract** to this kernel. The contract is `RoleStageContract` in
`contracts.py`, with a single version constant `ZT_P1_CONTRACT_VERSION`
(currently `1`) that appears in every emitted evidence envelope. It declares
the effective roles, the permitted role-to-stage transitions, the required
evidence per transition, and the stop/terminal semantics that a later
supervisor validates against.

The corresponding evaluated predicates are:

- `authority.validate_role_stage_contract` and
  `authority.validate_role_stage_transition` — block a presented effective
  role, contract version, or role-to-stage transition that does not match the
  contract (the mismatch-blocks rule), including a transition that would widen
  the real-dispatch refusal.
- `authority.validate_grant_lifecycle` — blocks an expired, revoked or
  consumed grant, and a replayed approval.
- `evidence.build_versioned_evidence_envelope` and
  `evidence.verify_versioned_evidence_envelope` — the versioned envelope of the
  design's §4.8(1); malformed and duplicate envelopes are rejected.
- `owned_paths.lease_is_exclusive` and `owned_paths.generation_is_current` —
  the one-lease-per-workflow and generation-fencing predicates.

**Honesty requirement:** this contract and its predicates are **offline and
synthetic and grant nothing**. A passing synthetic probe is not real
authority, and no real route is authorized. `require_real_dispatch` still
always denies a real dispatch, and the new checks may only narrow, never
widen, that refusal.
