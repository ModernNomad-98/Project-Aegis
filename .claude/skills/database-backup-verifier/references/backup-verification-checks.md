# Backup verification checks, drill plan and dump-file search

Supporting reference for `database-backup-verifier`. Terms follow the skill's
Reading key: RPO is the recovery point objective, RTO the recovery time
objective, PITR point-in-time recovery, and API an application programming
interface.

Provider behavior (snapshot types, PITR windows, what happens to automated
backups when an instance is deleted, cross-account copy support, restore
pricing) changes over time and differs by provider and plan. Treat every
provider-specific claim as a **verification item**: cite the provider
document you checked and its date, or mark the claim UNVERIFIED.

## 1. The seven checks

Each check gets exactly one verdict:

| Verdict | Meaning |
| --- | --- |
| VERIFIED | The evidence was read and meets the requirement. Cite it. |
| GAP | The evidence was read and does not meet the requirement. Say what is missing. |
| UNVERIFIED | The evidence could not be read (no access, no listing, no history). Say why. A drill is refused for a store whose backup evidence is UNVERIFIED. |

| Check | Evidence to read (read-only) | VERIFIED when | Common GAP |
| --- | --- | --- | --- |
| Exists | Snapshot or backup list for the store; dump-file listing in the backup bucket | At least one backup of this exact store is listed | Backups belong to a different or deleted instance |
| Non-empty | Size of the newest backup; size history | Size is above zero and within a plausible range of recent backups and the store's size | Zero-byte file; size suddenly far smaller than usual |
| Current | Newest backup time, or end of the PITR window, and the check time | Age at check time is below the RPO | Newest backup older than the RPO; PITR window stopped advancing |
| Retained | Oldest kept backup; retention setting; lifecycle rules on the backup bucket | Oldest kept backup meets the retention requirement | Retention shorter than required; lifecycle rule deletes early |
| Encrypted | Encryption flag and key reference on the backup and its copies | Encryption on, key named, and the key is enabled and usable | Unencrypted copy; key disabled or scheduled for deletion |
| Off-account copy | Copies in another account, project or subscription (and region) | A current copy exists outside the store's own account | All copies live in the same account as the store |
| Restore-tested | Last drill record: date, backup used, measured time, parity result | A drill succeeded within the agreed interval and its time is inside the RTO | Never tested; last test too old; measured time above the RTO |

Record **evidence origin** for every row: the command or API call and its
time, a console export and who made it, or "pasted by the human". Evidence
pasted by the human is reported as such; it is not re-labelled as observed.

Judge currency at the time of the check, and state that time. A backup that
was current yesterday can be a GAP today.

## 2. Drill plan template

A drill is proposed, approved and then run. Present the plan in this shape
and wait for approval of this exact plan:

```
RESTORE DRILL PLAN — <store>
Backup to restore: <backup id>, taken <time>, size <size>
Scratch target: <account / project> / <region> / <new instance name>
  Non-production evidence: <identifiers compared with the production list>
  Exists already? <no | yes, proven empty by <evidence>>
Data origin: production copy of <store> at <backup time>
Access to scratch copy: <named people or roles only>
Estimated cost: <amount> <currency> for about <duration>
  Basis: <instance class × hours, storage size × duration, transfer size, source of prices and date>
Restore credential: <VAR_NAME> (value never printed)
Timing: from restore request to first successful connection
Parity checks: row counts for <tables>; checksums for <tables or columns>
Deletion: delete instance and storage by <deadline>; confirm by listing
Stop if: cost rises above the estimate, the target is not empty, or deletion cannot be confirmed
```

The approval must quote or clearly accept the estimated cost. "Go ahead"
without the cost, or approval of an earlier plan with a different cost,
does not start the drill.

## 3. Parity methods

Compare the restored copy with the backup's source **at the backup's time**,
never with the live store.

- **Row counts:** count rows per table in the restored copy. The reference
  counts come from a count taken at backup time, the backup's own metadata,
  or a second restore of the same backup. Say which.
- **Checksums:** compute an ordered aggregate hash per table or per agreed
  column set (for example a hash over primary keys and an updated-at column)
  on the restored copy, and compare with the same computation on the
  reference. Use the same query on both sides and show it.
- **Scope:** for very large stores, agree a sample (named tables, key
  ranges) in the drill plan. A sample result is reported as a sample, not as
  full parity.
- **Show numbers only:** counts, checksums and table names. Never rows.

## 4. Repository dump-file search (local, read-only)

Search both the working tree and the history. Report path, commit and size;
never print or open the file's contents into the conversation.

- File names and extensions that often hold dumps: `.sql`, `.dump`, `.bak`,
  `.backup`, `.sql.gz`, `.tar` or `.gz` next to database names, `.sqlite`,
  `.db`, and files whose names contain `dump` or `backup`.
- History: list every path ever added with those patterns, for example with
  `git log --all --diff-filter=A --name-only` filtered by pattern, and
  record the first commit that added each one.
- Large binary blobs in history can also be dumps; list their paths and
  sizes for a human to check.
- A hit is reported, not removed. Removing it from history is a history
  rewrite, a destructive operation outside this skill. If the file may hold
  personal or customer data, say it may be an exposure so the human can
  decide whether it is an incident.

## 5. After the drill

- Delete the scratch instance and its storage, then list them again and show
  that they are gone.
- Record the measured restore time with the data size at the time; a later,
  larger store needs a new drill.
- If deletion fails or cannot be confirmed, stop, report the open copy of
  production data and where it is, and do not start another drill.
