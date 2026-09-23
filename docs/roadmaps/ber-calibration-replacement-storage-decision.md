# BER replacement calibration input storage — owner decision proposal

Prepared: 2026-09-23. Status: OWNER STORAGE CHOICE RECORDED; BER-DEC amendment
pending. This is not dataset approval or execution authority. Governing package:
WP-2B-3 / BER-DEC-008. This proposal implements
the [replacement preparation plan](../evidence/ber-recovery-2026-09-11/replacement-plan.md)
only after Peter Nguyen makes the changed storage decision and its BER-DEC
amendment is reviewed and merged. It makes no provider request and does not
recreate the lost original approval.

## Verified constraint and decision

`ModernNomad-98/Project-Aegis` was **PUBLIC** when checked through GitHub on
2026-09-23. BER-DEC-008 decisions 24–25 put calibration evidence under an
external, access-controlled root outside every Git repository, with only
sanitized summaries in the source repository and 30-day evidence retention.
Peter later chose GitHub for project backup and said the project contains no
secret or personal data. The [replacement plan](../evidence/ber-recovery-2026-09-11/replacement-plan.md)
requires the changed input/source storage terms to be decided forward. Those
directions have not yet been reconciled in an authorization record.

The 160 candidate records include 120 holdout transcripts and proposed labels.
Publishing them in the public source repository would expose the holdout to
anyone, including future coding or evaluation agents with repository access.
That would weaken the sealed-holdout claim even though the records contain no
secret or personal data. GitHub backup and public disclosure are separate
choices.

**Recommended decision:** use a separate **PRIVATE** GitHub repository,
provisionally `ModernNomad-98/Project-Aegis-Calibration-Inputs`, as the durable
canonical home for replacement calibration *inputs*. Keep the public Aegis
repository limited to the builder, validation code, versioned guide if it
contains no holdout content, sanitized reports, SHA-256 hashes and a pointer
to the private input revision. Confirm the proposed repository name is
available before creation. Keep the BER-DEC-008 external execution-evidence
root and its 30-day controls for provider requests, outputs, ledgers and run
logs. No private repository or input is created by this proposal.

| Choice | Effect |
| --- | --- |
| **A. Private GitHub inputs (recommended)** | Durable GitHub history without public holdout disclosure; requires an owner-approved private repository, access list and BER-DEC amendment. |
| B. Public Aegis repository inputs | Simplest backup, but proposed labels and all holdout cases become public and a new evaluation/exposure decision is required before claiming a sealed holdout. |
| C. External-only inputs | Retains BER-DEC-008 storage terms but leaves the replacement without the requested durable GitHub backup. |

## Proposed private-input contract for choice A

- **Repository and access:** Create the named repository as private under
  `ModernNomad-98`. Peter Nguyen is the initial reader/writer. Any added
  collaborator, app, token or Actions job needs a separately recorded access
  decision. Verify private visibility and the access list before the first
  input push and before any later changed visibility or membership.
- **Canonical versioned paths:** `replacement/<version>/candidate-dataset.json`,
  `split-map.json`, `labeling-guide.md`, `quality-report.json`,
  `hash-manifest.json`, and, only after explicit owner labeling,
  `owner-label-approval.json`. Use a new version directory for each revision;
  preserve prior bytes and hashes. The construction source may be public only
  if it cannot regenerate hidden holdout transcripts or labels by itself.
- **Review status:** Every candidate label remains `PENDING` until Peter
  approves the exact dataset, guide, split map and hash manifest. A private
  commit proves persistence, not human gold-label approval. The sole-human
  labeler exception is retained without an inter-rater-independence claim.
- **Separation:** Provider requests, responses, cost/usage ledgers, credentials
  and unsanitized run evidence remain outside Git under BER-DEC-008's exact
  external root and handling controls. The private input repository must not
  become an execution-evidence sink or bypass the 30-day cleanup rule there.
- **Retention and recovery:** Keep immutable versioned input history until an
  explicit owner-reviewed deletion decision. This is a proposed change for
  input artifacts only; the execution-evidence retention remains 30 calendar
  days from first evidence creation. Document a restore check that compares
  fetched bytes with the approved manifest before any use. Git history is a
  backup location, not a signature or tamper-proof authority.
- **Exposure gate:** Before each measured development or holdout stage, verify
  the input repository is still private, the selected exact commit and hashes
  match the owner approval, and no holdout transcripts or labels have been
  copied into the public source repository, judge envelope, development tuning
  material or Actions artifacts. If exposure is discovered, stop and return
  the calibration plan to Peter; do not call the set sealed by assertion.

## Required forward record and implementation gate

After Peter chooses a storage option, a separately reviewed governance PR
must append BER-DEC-010 (or the next available ID) to the backlog, recording
the actual GitHub location, access/visibility, input retention, source pin,
evidence split, budget and stop terms. It must amend only the changed parts of
BER-DEC-008 decisions 24–25; the original entry stays immutable. The
governance PR's merge precedes any replacement input publication or provider
execution under the changed terms. The current measured calibration remains
blocked by missing approved labels, historical accounting/source reconciliation,
preflight and later holdout freeze. This proposal supplies none of those gates.

## Review questions for Peter Nguyen

1. Choose A, B or C above. If A, approve the exact private GitHub repository
   and owner-only initial access, and confirm that canonical replacement
   inputs persist there until an owner-reviewed deletion while execution
   evidence keeps its existing 30-day external retention.
2. Confirm that a public guide/builder must omit any bytes or deterministic
   seed that would reveal the hidden 120 holdout transcripts or labels. The
   candidate review packet itself stays private under A.

No choice here approves candidate labels, a provider call, a new allowance,
an installation, or the final OD-1 result.

## Owner disposition — 2026-09-23

Peter Nguyen selected option A in direct response to the PR #105 storage
question: **"Use the private GitHub input repository (recommended)"**. The
question named the public source repository, 120 holdout cases and proposed
labels, private GitHub input repository with owner-only initial access and
durable versioned inputs, and continued 30-day external execution-evidence
root. This decision accepts that storage direction; it does not itself create
the repository or approve labels, provider calls, changed source pins or an
execution allowance. Record the exact location and terms in a separately
reviewed, merged BER-DEC amendment before publishing replacement inputs.

## Implementation checkpoint — 2026-09-23

BER-DEC-010 merged in PR #106 at
`14e3f17c380dd26ddba1f27c7e041b6064509ba4`. The selected repository
`ModernNomad-98/Project-Aegis-Calibration-Inputs` was then created. GitHub
reported PRIVATE visibility, the owner account as its sole collaborator, and
Actions disabled. These facts were verified before any input push; the
repository is still empty at this checkpoint. Creation does not approve
candidate labels or satisfy an execution gate.
