# Privacy and consent

The reporter is built so that a consenting participant can report the progress
of **one workflow** without handing over their project, their prompts, their
output or their identity.

## The allowlist

The export is a closed schema: `additionalProperties` is false at every level,
and every string must match one of a fixed enum, a day-precision date
(`YYYY-MM-DD`) or a random reference (`wf-`, `exp-`, `adm-`, `evt-`,
`crit-` followed by 32 lowercase hex characters). Anything else is rejected
before it can be stored or imported.

| Field class | Allowed values |
| --- | --- |
| `schema` | `workflow-outcomes-v1` only |
| `capture_tier` | `self_report` only; `host_recorded` needs a new validated adapter and fails closed |
| `status` | `ongoing`, `delivered`, `failed`, `abandoned`, `unknown` |
| Stage status | `not_started`, `in_progress`, `complete`, `not_applicable`, `unknown` |
| Acceptance | `not_assessed`, `self_reported_pass`, `self_reported_fail`, `independent_attested_pass`, `independent_attested_fail` |
| Evidence | `none`, `local_checklist`, `local_test_record`, `local_review_record` |
| Event kind | `status`, `stage`, `acceptance`, `scope_change`, `observation` |

Keys that could smuggle content or identity — `prompt`, `output`, `code`,
`project_name`, `repository`, `path`, `url`, `account`, `email`, `user`,
`host`, `device`, `sha256`, `content_hash`, `reason`, `notes`, `comment` and
similar — are rejected with their own error code at any nesting depth, so a
leak is loud rather than merely "unknown field". Duplicate JSON keys, invalid
UTF-8 and payloads over 64 KiB are rejected before parsing.

## Pseudonymous, not anonymous

A random `workflow_ref` is generated locally and is never derived from a
machine, account, project or start date. It links that workflow's successive
exports so a revision can update an earlier record and a duplicate can be
recognised. That makes the record **pseudonymous**: it does not name a person,
but it is a stable handle for one workflow.

The tool makes no anonymity claim. A file's minimized JSON does not make its
transport anonymous: an approved private channel may still expose the sender's
address, IP or account metadata. Before any real external transfer, the
ingress, proxy, CDN, application and security logs, backups and access paths
must be inspected, and unavoidable metadata disclosed. Email, public issues and
pull-request comments are never raw-data intake.

## Consent

Default off. Before a workflow is opted in, the participant is told:

- the purpose (learn whether observed workflows reach delivery), the exact
  fields, the recipient and the retention periods;
- that reporting is optional and declining changes no normal Aegis behaviour;
- that the sample is opt-in and cannot establish population adoption;
- that missing reports, withdrawal and self-report bias limit the results;
- that the skill-usage plane is separate and separately consented;
- how to disable capture, delete local history and withdraw imported data;
- that already published irreversible aggregates cannot be retracted.

New recipients, purposes or fields require fresh consent and, for a schema
change, a new dataset version with migration tests and a comparability note.

## Withdrawal and deletion

- Disabling capture stops recording immediately and removes unsent exports.
- A participant who has the admission capability can ask the steward to delete
  the linked raw data. Withdrawal removes the admission, the raw snapshots and
  the deletion verifier; nothing that links back to the workflow or the
  admission is retained.
- Deletion is immediate in this implementation, which satisfies the seven-day
  obligation. The only surviving artefact is a random, unlinkable deletion
  receipt with its own seven-day expiry, so the participant can confirm the
  deletion happened.
- Withdrawal changes the denominator. The report shows a non-linkable
  withdrawal count and states the bias; historical original-cohort success is
  not reconstructable after deletion without a separately approved safe
  aggregate design.
- Losing the capability secret means deletion cannot reliably locate the data.
  That is disclosed before consent; no identity is collected for recovery.

## Retention

- Local raw reporter data: **60 days from capture**, then pruned by the local
  tool.
- Central-model minimized raw records: **90 days from first receipt**, never
  reset by a retry or an update.
- Quarantined contract-valid payloads kept for correction: **90 days**.
- Deletion receipts: **7 days**.
- Approved irreversible aggregates: **365 days** (not implemented here; no
  aggregation is published).
- No raw backups. Adding backups would require a bounded expiry and
  delete-on-restore approval before collection.

Reports produced after a record's retention expiry are suppressed or explicitly
marked incomplete; retention is never silently extended.

## Limits that cannot be fixed by the contract

Opt-in selection, invisible local starts, self-report truthfulness, deliberately
fabricated new workflows, withdrawal-induced denominator change, transport
metadata and sparse-cell differencing all remain limits. They are disclosed, not
eliminated.
