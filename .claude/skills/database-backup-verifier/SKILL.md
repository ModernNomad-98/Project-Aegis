---
name: database-backup-verifier
description: 'MANUAL-ONLY; never auto-invoke. Verify database backups would actually save you: per store, a backup exists, is non-empty, is current against the recovery point objective (RPO), is retained and encrypted as required, has an off-account copy, and is RESTORABLE, proven by a restore drill into an isolated scratch target with row-count and checksum parity and a measured restore time against the recovery time objective (RTO). Also flags dump files inside the repository or its history. Evidence mode (the default) runs read-only listings; drill mode restores only to a named non-production target after human approval, never over a source, and names credentials by variable only. CALLS PROVIDER APIS AND RESTORES DATA, so manual invocation only. Use when asked whether backups work or before a risky migration. Do NOT use to design RPO, RTO or DR (resilience-architecture-reviewer), write a migration runbook (data-migration-runbook-author), or design retention for personal data (pii-lifecycle-designer).'
disable-model-invocation: true
---

# Database Backup Verifier

**Reading key:** a **store** is one database, cluster or managed database
instance that holds data you would need back. A **backup** is a copy of a
store kept for recovery: a provider snapshot, a dump file, or continuous
log archiving. **PITR** is point-in-time recovery: restoring a store to any
moment inside a window by replaying archived change logs on top of a base
backup. The **RPO** (recovery point objective) is how much recent data the
business may lose, so the newest usable backup must be younger than it. The
**RTO** (recovery time objective) is how long the service may be down, so a
restore must finish inside it. **DR** is disaster recovery. **Retention** is
how long backups are kept before deletion. An **off-account copy** is a
backup copy held in a different cloud account, project or subscription (and
ideally region), so one compromised or deleted account does not take the
backups with it. A **restore drill** restores a real backup into a separate
**scratch target** (a new, empty, isolated, non-production instance created
only for the drill), checks it, and deletes it. **Parity** means the
restored copy matches the backup's source: same row counts per table and the
same **checksums** (a short fingerprint computed from the data, so two
copies with equal checksums hold equal data). **API** is application
programming interface. **SLO** is a service level objective (a reliability
target). A **dump file** is a database export written to a file (for
example a `.sql`, `.dump` or `.bak` file). Each check gets one verdict:
**VERIFIED** (the evidence was read and meets the requirement), **GAP** (the
evidence was read and does not meet it) or **UNVERIFIED** (the evidence
needed for a verdict could not be read, so no verdict is given).
The Phase 6 skill `resilience-architecture-reviewer` reviews RTO, RPO and
DR design; if it is not in this copy of the library, say so and ask the
owner for the recorded objectives instead.

## Purpose

Prove, store by store, that a usable backup exists and can be restored
within the agreed time, instead of trusting a "backups enabled" setting. The
deliverable is a backup verification report: for every store, a verdict on
seven checks (exists, non-empty, current against the RPO, retained as
required, encrypted, off-account copy, restore-tested), each citing the
evidence it read and where that evidence came from. When a human explicitly
asks for drill mode and approves the exact drill plan, including its
estimated cost, the report adds a restore drill record: the scratch target,
the measured restore time against the RTO, row-count and checksum parity,
and proof that the scratch copy was deleted. It also reports any dump file
found in the repository or its history, by path and commit only. Built under
owner decision D71 (roadmap row #253), from candidate 5 of the
[Phase 6 reliability batch proposal](../../../docs/roadmaps/phase6-reliability-skill-batch-proposal.md).

## Use When

- Use when: a human explicitly invokes this skill to check whether the
  backups of named stores exist, are current, are kept long enough and are
  encrypted (evidence mode, the default; read-only).
- Use when: a human explicitly invokes it to prove a backup restores, by a
  restore drill into a named, isolated, non-production scratch target
  (drill mode).
- Use when: a risky migration, cutover or data move needs "a VERIFIED backup,
  not 'backups are enabled'" as its precondition.
- Use when: someone needs to know whether a database dump was ever committed
  to the repository.
- Do NOT use when: the RTO, RPO or DR design itself must be set or reviewed
  — that is `resilience-architecture-reviewer` (see the Reading key).
  This skill checks real backups against objectives that already exist.
- Do NOT use when: the ask is the migration or data-move runbook —
  `data-migration-runbook-author`. It consumes this skill's evidence.
- Do NOT use when: the ask is rollback steps for a release —
  `rollback-runbook-author`. It may cite this report as its restore-point
  evidence.
- Do NOT use when: the ask is SLO targets, error budgets or alerting —
  `slo-reliability-architect`.
- Do NOT use when: the ask is how long personal data may be kept in
  backups, or how deletion reaches backups — `pii-lifecycle-designer`.
- Do NOT use when: the ask is a schedule of periodic audit evidence (for
  example "restore test every quarter") — `compliance-evidence-collector`.
- Do NOT use when: the ask is a reusable template for a recurring gated
  operation — `gated-deployment-prompt-template`.
- Do NOT use when: backup credentials must be stored, issued or rotated —
  `secrets-identity-hardener` *(manual-only)*.
- Do NOT use when: the service is down and data must be recovered NOW —
  that is an incident, owned by `incident-response-runbook`. This skill never
  restores into production.

## Inputs to Inspect

1. **The store inventory:** every store in scope, with its provider,
   account, region, instance identifier, and whether it is production.
2. **The recorded objectives:** the RPO and RTO per store (or per service),
   and the required retention and encryption. Missing RPO or RTO → Stop
   Conditions.
3. **Backup listings and metadata**, read-only: snapshot or dump lists with
   timestamps and sizes, PITR window, retention settings, encryption status
   and key reference, and any copies in other accounts or regions. Record
   where each listing came from (a provider API call the human authorized,
   a console export, or text the human pasted).
4. **Restore-test history:** the date, backup used, measured restore time
   and result of the last restore drill, if any.
5. **Credential references:** the environment-variable NAMES that hold the
   read-only listing credential and, for drill mode, the restore credential.
   Never read or print the values.
6. **For drill mode only:** the named scratch target (account, region,
   instance name), positive evidence that it is non-production and does not
   yet exist or is empty, the declared production identifiers to compare
   against, and the drill's estimated cost with its basis.
7. **The repository**, for the dump-file check: the working tree and its
   commit history, read locally.

## Workflow

Explicit human invocation selects this execution-capable skill; it does not
expand the allowed target or activate Task-Authorized Local Implementation
(TALI). TALI is a separate route requiring its own classification and
activation under the [skill-generation standard](../../../docs/skill-generation-standard.md#5-least-privilege--side-effects).
Use applicable existing user grants without repeated consent. Before a
state-changing command, confirm its actual files, environment and effects fit
those grants; if authority is absent, propose the operation and obtain it
before proceeding.

1. **Pin the scope and objectives.** List the stores in scope and, for
   each, its RPO, RTO, retention and encryption requirement. If any store
   has no recorded RPO or RTO, stop and hand the gap to
   `resilience-architecture-reviewer`; never invent an objective.
2. **Read the evidence (evidence mode, the default, read-only).** Run only
   listing and describe operations, using the credential named by its
   variable. Record the origin of every piece of evidence: the command or
   API and the time it ran, or "pasted by the human". Change nothing: no
   snapshot, copy, retention change or restore.
3. **Judge the seven checks per store.** Use
   [references/backup-verification-checks.md](references/backup-verification-checks.md).
   Each check is VERIFIED (evidence shown), GAP (evidence shows the
   requirement is not met) or UNVERIFIED (the evidence could not be read):
   - **Exists:** at least one backup of this store is listed.
   - **Non-empty:** its size is above zero and plausible for the store; a
     zero-byte backup is never counted as a backup.
   - **Current:** the newest usable backup, or the end of the PITR window,
     is younger than the RPO at the time of the check.
   - **Retained:** the oldest kept backup meets the retention requirement.
   - **Encrypted:** encryption is on, with the key reference (the name or
     identifier of the encryption key) named.
   - **Off-account copy:** a copy exists outside the store's own account.
   - **Restore-tested:** a restore drill of this store succeeded within the
     agreed interval, with its measured time inside the RTO.
4. **Check the repository for dump files (local, read-only).** Search the
   working tree and the full commit history for dump-like files by name and
   type. Report each hit by path and commit only; never print, open into the
   conversation, or copy its contents.
5. **Stop here unless drill mode was explicitly requested.** Deliver the
   evidence report. Drill mode needs all of: an explicit human request, a
   store whose backup evidence is not UNVERIFIED, a named scratch target
   proven non-production in step 6, and approval of the exact drill plan,
   with its estimated cost, in step 7.
6. **Pin the scratch target.** Record its account, region and instance
   name, and compare each with the declared production identifiers. It is
   non-production only on positive evidence; anything unknown or shared is
   treated as production and the drill stops. It must not exist yet, or
   must be proven empty; restoring over any existing database is refused.
   It must not be reachable from the public internet, and only the people
   or roles named in the plan may connect to it.
   Record the data origin and class: the restored copy is production data
   (backup identifier, source store, backup time, and its data class, such
   as personal or payment data), so it inherits the source's
   access limits and handling rules for as long as it exists, and the
   scratch target must sit in an account and region where that data is
   allowed to be kept.
7. **Present the drill plan and obtain approval.** State the backup to
   restore, the scratch target, the estimated cost (instance, storage and
   any cross-region or cross-account transfer, for the expected duration,
   with the currency and the basis of the estimate), the restore
   credential's variable name, the parity checks, who may access the
   scratch copy, and the deletion step with its deadline. Wait for approval
   of this exact plan. The approval must state the estimated cost; an
   approval that does not name it does not start the drill. A changed plan,
   or a cost above the approved estimate, needs fresh approval.
8. **Run the drill.** Restore the approved backup into the scratch target
   only, and time it from the restore request to a usable, connectable
   copy. If the restore fails, record the error and still delete whatever
   the attempt created.
9. **Check parity.** Compare row counts per table and checksums of agreed
   tables or columns with the backup's source at the backup's time (not
   with the live store, which has moved on since, and never by running
   queries against production). Report each mismatch by
   table; show counts and checksums, never row contents.
10. **Delete the scratch copy and prove it.** Remove the scratch instance
    and its storage without a final snapshot, and delete any snapshot,
    automated backup or export **this drill created**. Then list what the
    drill created in the scratch target to show that none of it remains.
    Both the deletion and its proof are scoped to drill-created resources:
    if the target is not a dedicated account, never remove — and never
    treat as a failure — pre-existing or unrelated resources there. The
    drill is not done until the deletion of its own resources is shown.
11. **Report** in the Output Format, including what was not done and why.

When the drill method is a real choice (for example a provider's snapshot
restore versus loading a dump file into a new instance), first define the
terms; explain each option's reason, setup and running cost (or state that
it is unknown), and case-specific pros and cons; recommend one with a reason
tied to the user's context; then ask one question. If a deciding fact is
missing, ask only for that one fact first. A chosen option is not approval
to restore.

## Output Format

```
DATABASE BACKUP VERIFICATION REPORT — <scope>
Mode: evidence (read-only) | drill (plan approved: <quote + time>, estimated cost: <amount, currency, basis>)
Objectives: <store> RPO <x> / RTO <y> / retention <z> / encryption <required?> — source <doc or owner>
Evidence origin: <store> — <command or API + time> | <console export> | <pasted by human>
Per store:
  <store> | Exists | Non-empty | Current (<newest age> vs RPO <x>) | Retained | Encrypted (<key ref>) | Off-account copy | Restore-tested (<date, time vs RTO>)
          each: VERIFIED (<evidence>) | GAP (<what is missing>) | UNVERIFIED (<why not readable>)
Drill record (drill mode only):
  Backup <id> of <store> taken <time> → scratch target <account/region/name>, proven non-production by <evidence>
  Data origin: production copy from <store> at <time>, data class <class>; access limited to <who>; not reachable from the public internet
  Restore time: <measured> vs RTO <y> → within | exceeds
  Parity: <n tables> row counts <match | mismatch list>; checksums <match | mismatch list>
  Scratch deleted: <time>; instance, storage, snapshots and backups confirmed gone by listing <evidence>; actual cost <if known>
Repository dump check: <path — commit — size> | none found (<scope searched>)
Credentials: referenced by variable name only — <VAR_NAME list>
Not done: <UNVERIFIED items, drills not requested or refused, and why>
Handoffs: <resilience-architecture-reviewer | data-migration-runbook-author | secrets-identity-hardener | pii-lifecycle-designer | incident-response-runbook>
```

## Validation Checklist

- [ ] Every store in scope has its RPO and RTO from a named source; none was
      invented.
- [ ] Evidence mode was the default and changed nothing.
- [ ] Every check carries VERIFIED, GAP or UNVERIFIED with its evidence, and
      every piece of evidence records its origin.
- [ ] No zero-byte or implausibly small backup was counted as a backup.
- [ ] Currency was judged against the RPO at the time of the check.
- [ ] A drill ran only after an explicit request and approval of the exact
      plan, and that approval stated the estimated cost.
- [ ] The scratch target was proven non-production and new or empty; no
      restore went over an existing database or into production, and its
      account and region are allowed to hold the restored data.
- [ ] Parity compared counts and checksums with the backup's source, and no
      row contents were shown.
- [ ] The scratch copy's deletion, including any final snapshot, automated
      backup or export it created, is shown by a listing.
- [ ] Dump files are reported by path and commit only; no contents printed.
- [ ] No credential value appears anywhere; only variable names.
- [ ] Any drill-method choice explained terms, costs, pros and cons, and a
      recommendation before one question.

## Safety Rules

- Production is never a restore target. A request, a variable or a default
  that points a restore at production stops the run; no approval converts
  it.
- A restore never overwrites an existing database, even a non-production
  one. Drills restore into a new or proven-empty scratch target only.
- A drill spends money and writes data, so it needs approval of the exact
  plan with its estimated cost stated; the cost is part of what is approved.
- The restored copy is production data. It keeps the source's access limits
  while it exists, and it is deleted at the end of the drill.
- Credential values are never read into the conversation, written into the
  report, or echoed in logs. Missing variables are reported by name.
- Dump files and restored rows are evidence to locate, never content to
  display.

## Gotchas

- "Backups enabled" is a setting, not evidence. A schedule can be on while
  every run fails, or the newest snapshot can be weeks old.
- A snapshot's age is not the data-loss window when PITR is on: currency is
  the end of the PITR window, and that window can silently stop advancing if
  log archiving breaks.
- Backups kept only in the store's own account are lost with that account.
  Deleting an instance can also delete its automated backups on some
  providers; treat each provider's behavior as a verification item.
- Deleting the scratch instance can leave production data behind: some
  providers take a final snapshot on deletion by default, or keep the
  instance's automated backups after it is gone. Delete without a final
  snapshot, list the snapshots and backups too, and treat each provider's
  default as a verification item.
- A backup encrypted with a key that was disabled or deleted cannot be
  restored. Name the key and check that it is still usable.
- Parity against the live store always "fails", because the live store kept
  changing. Compare with the source at the backup's time.
- Restore time grows with data size. A drill on last year's size does not
  prove this year's RTO; record the size with the measured time.
- A dump committed and later deleted still sits in the repository history.
  Removing it means rewriting history, which is outside this skill; if it
  may hold personal data, treat it as a possible exposure.

## Stop Conditions

- The skill was selected automatically rather than explicitly invoked by the
  human: do not execute it. An agent may recommend the named manual skill.
- A write, Git/network operation, database command or test side effect exceeds
  the applicable human grant: stop that operation and obtain the missing scope.
  Existing authorized operations do not need the same permission again.
- A store in scope has no recorded RPO or RTO → stop before judging it and
  hand the gap to `resilience-architecture-reviewer` (or, if that skill is not
  in this copy of the library, ask the owner for the objectives).
- The restore target is production, or its identifiers cannot be proven
  different from production → refuse the restore and report why; do not
  offer a workaround. Recovering production after an outage is an incident
  for `incident-response-runbook`.
- The restore would go over any existing database → refuse; restores go only
  into a new or proven-empty scratch target.
- The scratch target would be reachable from the public internet or by
  anyone not named in the plan, its account or region is not allowed to
  hold the source's data, or the data's class is unknown → do not start the
  drill; report which condition failed.
- The drill approval does not state the drill's estimated cost, or the
  expected cost rises above the approved estimate → do not start or continue
  the drill; present the cost and obtain approval again.
- The backup's evidence is UNVERIFIED (its listing or metadata cannot be
  read) → deliver the evidence report and refuse drill mode for that store
  until the evidence can be read.
- The drill plan changed after approval → stop and obtain approval for the
  new plan. Restoring into a scratch target, which creates a billed instance
  holding production data, is the irreversible step this skill guards.
- The scratch copy cannot be deleted, or its deletion cannot be confirmed →
  stop, report it as an open production-data copy with its location, and
  hand it to the human; do not start another drill.
- A credential value would be printed, stored or committed, or is missing →
  stop and report the variable name; custody goes to
  `secrets-identity-hardener` *(manual-only)*.

## Supporting Files

- [references/backup-verification-checks.md](references/backup-verification-checks.md)
  — the seven checks with evidence sources and verdict rules, the drill plan
  template with its cost estimate and deletion step, parity methods, and the
  repository dump-file search.
- `evals/evals.json` — behavior cases: stale backup against the RPO, drill
  with parity and deletion, production refusal, restore-over-existing
  refusal, cost-unstated refusal, zero-byte backup, dump file in history,
  missing objectives, UNVERIFIED evidence, cost overrun, changed plan,
  unconfirmed deletion, credential refusal, and manual-only silence.
- `evals/trigger-evals.json` — discrimination against
  `data-migration-runbook-author`, `compliance-evidence-collector`,
  `rollback-runbook-author`, `pii-lifecycle-designer`,
  `slo-reliability-architect`, `gated-deployment-prompt-template`,
  `incident-response-runbook` and `resilience-architecture-reviewer`.
