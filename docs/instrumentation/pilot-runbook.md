# Pilot runbook (documentation only)

> **This is not an authorisation.** No pilot, enrolment of real workflows,
> export of real data, hosting or deployment is approved by this page. It
> describes the private procedure that a separately approved pilot would follow.
> Implementing the tool and passing synthetic tests is not permission to launch.

## Roles

- **Owner** — approves the pilot, the channel and any disclosure.
- **Data steward** — issues admissions, imports exports, handles deletion and
  reviews restricted records weekly.
- **Participant** — owns the workflow, opts in and out, previews and sends
  exports, and may withdraw.
- **Maintainer reviewer** — reviews aggregates monthly against disclosure rules.

## Before any participation

1. Confirm a written collection approval, a private transport channel and a
   named steward. Email, public issues and pull-request comments are not intake.
2. Complete the privacy and security review of the channel's logs, backups,
   access paths and unavoidable metadata. If the channel cannot meet the agreed
   scope, stay local-only.
3. Prepare the consent text from [privacy-and-consent.md](privacy-and-consent.md):
   purpose, fields, recipient, retention, optional skill plane, withdrawal,
   deletion limits, missing-data limits and no public metrics.
4. Set the participant's local store outside project version control with
   user-only access. The tool enforces this where the platform allows it:
   stores, exports and the directories it creates are `0600`/`0700` on POSIX
   whatever the umask, and a path inside a Git working tree or the tool source
   tree is refused. On Windows the tool cannot set POSIX bits, so the store
   must sit in a directory whose ACL is user-only (a profile or `%TEMP%`
   directory, not a shared folder).

## Start (day 0–7)

1. The participant freezes the acceptance checklist locally and records the
   random criteria-contract reference.
2. The participant opts in with `local_report.py opt-in` and sends the steward
   the minimized start notice: random workflow reference, start day, applicable
   stages, frozen-criteria flag and criteria-contract reference.
3. The steward checks that the start is at most seven days old and the outcome
   is not known, then issues an admission with `aggregate.py issue-admission`.
   The capability secret goes to the participant privately and is never stored
   centrally.
4. The participant attaches the admission reference and records transitions as
   work proceeds.

## Reporting (by day 30 plus 7)

1. The participant reconciles the workflow, records any acceptance with its
   local evidence category (`--evidence`, default `none`), and records an
   explicit observation for day 30 when the outcome is still ongoing.
2. The participant runs `preview`, reviews the exact bytes, and then runs
   `export` with the printed SHA-256 and `--confirm`. Exports go to local disk;
   the participant sends the file through the approved private channel.
3. The steward imports it with the capability secret and records the result:
   `accepted`, `updated`, `duplicate`, `ignored` or `quarantined`.
4. A conflicting same-revision payload, an enrollment change or a rewritten
   history is quarantined for a documented correction process. It is never
   silently accepted.

## Weekly steward review

- Review restricted records only: reconciled starts, duplicate counts, late
  entries, quarantine reasons and deletions.
- Confirm every received prospective start is reconciled through day 30.
- Check that retention is pruning as specified: local 60 days, central 90 days.
- Never copy raw records into a shared or public location.

## Deletion

1. For local history, the participant runs
   `local_report.py delete-local --workflow-ref W --confirm` (or `--all
   --confirm`). This is explicit, local only and irreversible; the store file
   remains if other workflows still use it.
2. For imported data, the participant requests withdrawal through the approved
   channel with the admission capability. Withdrawal does not depend on import
   eligibility: it works after the seven-day pending admission expires and
   after the 90-day record expiry, for as long as any linked raw or quarantined
   payload is retained. The importer keeps only a capability-verification
   tombstone (random admission reference, verifier hash, random workflow
   reference) while that data exists, and deletes the tombstone with the last
   linked datum.
3. The steward runs `withdraw`; the admission or its tombstone, raw snapshots
   and quarantine copies are removed immediately, and the deletion receipt is
   issued.
4. The steward gives the participant the random, unlinkable receipt identifier.
   The receipt expires after seven days.
5. Recompute the retained cohort. The report shows the withdrawal count and the
   bias note; no linkable workflow or admission record is kept after
   withdrawal.

## Stop conditions

For this offline tool the **steward kill switch is procedural**: stop running
`import` and `report`, and restrict access to the central store. There is no
remote disable flag or hosted control, so the steward's discipline is the
control.

Stop capture, import and any publication, quarantine affected data and notify
the owner if any of these occur:

- unexpected network traffic from the reporter or importer;
- a forbidden field, identity or content appears in an export;
- deletion does not complete or leaves a linkable record;
- duplicate or conflicting revisions are mishandled;
- cohort denominators or outcomes cannot be reconciled with the received
  records;
- a suppression rule would publish a cell below the disclosure floors;
- the channel's metadata or access controls no longer meet the approved scope.

Resume only after the cause is fixed, the affected data is deleted or
quarantined, and the owner records a new approval.

## Retention schedule

| Data | Retention | Action |
| --- | --- | --- |
| Local raw store | 60 days from capture | `local_report.py purge-expired`; a participant may delete earlier with `delete-local --confirm` |
| Central raw record | 90 days from first receipt | `aggregate.py expire` |
| Quarantine payload | 90 days | `aggregate.py expire` |
| Expired-record month counters | retained with the store; no workflow or admission reference | non-linkable count per start month, so a month whose data retention deleted is never republished as complete |
| Expired admission tombstone | while linked raw or quarantine data survives | `aggregate.py expire` deletes it with the last linked datum |
| Deletion receipt | 7 days | `aggregate.py expire` |
| Approved irreversible aggregate | 365 days | not implemented; no publication authorised |

## Closure

A pilot may graduate only on measurement reliability — every synthetic
contract, privacy, metric and lifecycle test passing, no unexpected
transmission, every received start reconciled, duplicates and deletion drills
handled, unknowns reported honestly and steward workload inside the approved
budget. Low export volume means extend or stay local-only; it never means
inferring success.
