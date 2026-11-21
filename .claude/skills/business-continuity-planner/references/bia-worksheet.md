# BIA worksheet, strategy matrix and crisis-comms checklist

This worksheet carries the prompts to ask and the tables to fill. It is a
question set, not a standard: no clause text from ISO 22301, SOC 2 or any
licensed framework is reproduced here, and no threshold below is a default you
may adopt without the accountable owner stating it.

## 1. Business impact analysis prompts

Ask per process, and record the owner's answer verbatim. "Nobody said" is a
finding, not a blank to estimate.

1. What does this process deliver, and to which customer, contract or internal
   function? What breaks for them when it stops?
2. Which commitments cover it — contract, service level, support hours,
   regulatory deadline? Cite the record, not the recollection.
3. What is the impact at 1 hour, 4 hours, 1 day, 3 days and 1 week? Separate
   revenue, customer, legal or regulatory, safety, staff and reputation effects.
4. At which point does the impact become unacceptable to the owner? That point
   is the maximum tolerable downtime (MTD), and it is the owner's decision.
5. Which people are required, and how many of them are the only person who can
   do it? Which systems and data are required, and what is the manual
   substitute?
6. Which supplier or SaaS vendor sits underneath, on what contract, with what
   exit or export right?
7. When was this process last exercised, and what did the exercise show?

## 2. Impact-over-time table

One row per process. Use the owner's own wording for the consequence; do not
compress to a rating.

| Process | Delivers to | 1 hour | 4 hours | 1 day | 3 days | 1 week | MTD (owner-stated) | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  | UNDECIDED |  |

Recovery-target origin table — the anti-invention control. A target with no
source row stays UNDECIDED.

| Process or store | RTO | RPO | Source record | Source date | Derived from MTD? | Owner | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | UNDECIDED | UNDECIDED | none found | — | — |  | open question |

## 3. Continuity strategy matrix

| Dependency class | Prompt | Strategy to state | What it costs | Owner who accepts |
| --- | --- | --- | --- | --- |
| People | Who is the only person who can do this, and who is their deputy? | Cross-training, deputy pairing, succession note, cover rotation | Training hours, duplicated access, slower normal work |  |
| Workplace | If this site, network or power is unavailable, where does the work happen? | Alternate location, remote readiness, equipment and access fallback, connectivity alternative | Lease, hardware, recurring readiness checks |  |
| Suppliers and SaaS vendors | What happens on the morning the vendor is unavailable, and can the data leave? | Tiering by consequence, concentration map, exit or export terms, alternate with switching cost | Contract terms, migration effort, dual-running cost |  |
| Manual workarounds | What is done by hand while the system is down, and how is it reconciled? | Offline procedure, paper or spreadsheet record, weakened-control note, reconciliation step | Error rate, double entry, control gap during the period |  |

Every strategy row must state the control it weakens where the workaround
bypasses an approval, a limit or a record. A strategy with no owner and no cost
is a wish.

## 4. Crisis-communications checklist

- [ ] Audiences listed: customers, staff, regulators, partners — and what each
      must hear first.
- [ ] A named speaker and a named deputy for each audience (not a role with no
      person behind it).
- [ ] The approval authority for each message class stated; disclosure
      decisions that belong to legal or the owner are named as theirs.
- [ ] Status-page posture: who may publish, the first message, the update
      cadence, and the resolution message.
- [ ] Holding statements drafted that acknowledge and scope without speculating
      or blaming, each committing to a next update time.
- [ ] Regulatory and contractual notification obligations listed with the
      licensed text or contract as their source — never reconstructed from
      memory; unknown ones marked UNKNOWN with the owner who must resolve them.
- [ ] Internal channel: how staff are told, and who answers their questions.
- [ ] A post-event review step so the communication record feeds the next plan
      revision.

## 5. Ownership, review and exercise register

| Item | Owner | Cadence | Trigger that forces an early review |
| --- | --- | --- | --- |
| Plan as a whole |  |  | Reorg, merger, new product line, major supplier change |
| Each critical process |  |  | Process change, system replacement, key-person departure |
| Each supplier strategy |  |  | Contract renewal, vendor outage, price change |
| Crisis communications |  |  | Audience change, new regulator, failed notification |

| Exercise | Type | Scope | Success criteria | Evidence it must produce | Findings owner |
| --- | --- | --- | --- | --- | --- |
|  | tabletop / walkthrough / simulation |  |  |  |  |

An exercise finding becomes an owned action with a date, or a risk the owner
explicitly accepts. Silence is not acceptance.
