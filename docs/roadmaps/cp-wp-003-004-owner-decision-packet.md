# CP-WP-003 and CP-WP-004 owner decision packet

**Status:** owner decision packet, prepared 2026-10-11 against `main`
`279338a938168843fabebff12acd30359a0fc414` (commit time 2026-10-11 14:54:23
-07:00). It presents **two open owner decisions** and **grants nothing**. No
option below is selected, no authority is assumed, and no budget is assumed.
Each decision needs its own separate reviewed scope and grant; this page and
its own pull request supply neither. Nothing here authorizes an account, a
credential, an authenticated inspection, a claim or reservation write, a host
contact, a provider call, spending, a deployment, or a dispatch.

**Purpose and readers.** This page is for the repository owner and the
reviewers who must decide the next two steps of control-plane work package 003
(CP-WP-003) and its later bounded integration, work package 004 (CP-WP-004).
CP means **control plane**, the resumable delivery kernel described in the
[control-plane design](../design/resumable-control-plane-v1.md). A *work
package* (WP) is a bounded delivery unit; an `AEGIS-APR-*nnn*` identifier names
an entry in the [owner approval register](../approvals/APPROVAL_REGISTER.md);
a *pull request* (PR) is a proposed repository change. Line references such as
"register L232" are line numbers in the cited file at the base commit above.

**Sources.** Every fact below is re-derived from the merged research, backlog
and governance pages listed under [Sources and verification](#sources-and-verification).
This packet adds no new research and contacts no account, service, host,
credential, or endpoint.

## Reading key

These five terms are the ones a later grant must bind. They are the
[named-candidate matrix](cp-wp-003-named-candidate-matrix.md#reading-key-and-required-result)
definitions, restated so this packet can be read on its own:

- **Grant:** the owner's scoped permission, with identity, revision, expiry,
  revocation, and permitted effect.
- **Redemption:** the one-use source transaction that lets exactly one
  authorized consumer spend a grant. A **manual consumer** is a person or
  separate tool that can initiate the same effect; it must participate in the
  same transaction boundary as the controller.
- **Freshness:** evidence that a valid-looking local checkpoint is the current
  one. An independent protected head or complete current-source reconciliation
  must reject an older restored checkpoint.
- **Receipt:** a durable answer identifying the completed claim or effect. A
  request acknowledgement, a local log, and a target outcome are different
  facts.
- **Fail closed:** with missing, stale, conflicting, or unavailable proof, the
  controller must deny dispatch and retain uncertain liability.

## 1. State at the base ref: delivered, blocked, and open

| Item | State | Evidence at the base ref |
| --- | --- | --- |
| CP-WP-001 — state, authority and recovery contract | DONE — documentation contract only | [Backlog](resumable-control-plane-backlog.md) L78: "DONE: documentation contract only, [PR #95]" |
| CP-WP-002 — offline state and recovery kernel | DONE — synthetic-only | Backlog **L79**: "DONE: synthetic-only code, [PR #99]…shared-claim repair in [PR #294]…validator marker replay fix in [PR #298]…T22 freshness-report fix in [PR #302]". Backlog L268: "All 28/28 T, 9/9 C and 22/22 F rows have tested, independently accepted coverage" and "Windows and pinned Linux 543-test suites" |
| CP-WP-003A — first offline capability proof | DONE and **CONSUMED** | Backlog L80: "DONE: synthetic failure probes, [PR #123]"; [AEGIS-APR-006](../approvals/APPROVAL_REGISTER.md#aegis-apr-006-control-plane-offline-capability-proofs-first-increment) (register L275–321) consumed by [AEGIS-APR-068](../approvals/APPROVAL_REGISTER.md#aegis-apr-068-consumption-of-the-cp-wp-003a-capability-proof-grant) (register L1858–1879) |
| CP-WP-003 — real authority, evidence and execution capability | **BLOCKED** — real source, freshness, containment, evidence and billing unselected | Backlog L81, L269, L279–282; [open-decisions register](aegis-open-decisions-2026-09-23.md) L43 |
| CP-WP-004 — one bounded real integration | **BLOCKED** — no target selected; CP-WP-003 prerequisites absent | Backlog L82, L270; open-decisions register L44, L232 |
| CP-FUT-001 — distributed ownership or hosted service | BLOCKED — out of this packet's scope | Backlog L83, L271 |
| ZT-P1 — offline role/stage transition contract | **NOT started** — needs a reviewed owner grant naming `tools/aegis_delivery_control/contracts.py` | Backlog L1688–1691 |
| P2-6 guard maintenance | DONE (PR #539 `2bb44db2`) under APR-086; grant consumed by APR-098; option (a) explicitly **not authorized** | Backlog L284–319 |
| Source-only research (named candidates; DynamoDB public contract) | COMPLETE — no source selected, nothing contacted | [Named-candidate matrix](cp-wp-003-named-candidate-matrix.md) L3; [DynamoDB public-contract inspection](cp-wp-003-dynamodb-public-contract-inspection.md) L7 |
| Gradual integration roadmap and release policy | POLICY DECISION (AEGIS-APR-102, 2026-10-02) — **grants no work; selects neither CP-WP-003 nor CP-WP-004** | Register L3160–3237; open-decisions register L239 |

**The owning open row, verbatim.** Open-decisions register
[`aegis-open-decisions-2026-09-23.md`](aegis-open-decisions-2026-09-23.md)
L232:

> Real source authority and capability proof for CP-WP-003, then selection of
> one bounded real integration for CP-WP-004; both need separate reviewed scope
> and grants.

The two per-package rows read (L43, L44):

> CP-WP-003 … The [CP backlog](resumable-control-plane-backlog.md) still blocks
> real source authority, independent freshness, containment, evidence and
> billing claims. The delivered proof grants no real dispatch.

> CP-WP-004 … No delivery target is selected. The [CP backlog](resumable-control-plane-backlog.md)
> requires CP-WP-003 prerequisites and a separately approved integration with
> exact receipt, rollback and budget terms.

The owning backlog repeats the block at L269 ("BLOCKED: separate scope/approval,
source-atomic approval claims/redemption including manual consumers, independent
monotonic anchor or complete reconciliation, verified containment/fencing,
evidence and bounded-liability accounting, and evidence-computed transition
guards (P2-6 option (a); see AEGIS-APR-086)") and L270 ("BLOCKED: chosen
integration, owner authority, idempotency/receipt/rollback semantics,
source/evidence/budget pins and proven CP-WP-003 prerequisites"), and states the
consequence at L279–282: "CP-WP-003 remains **BLOCKED**: no real source,
independent anchor/current-source ledger, selected host containment, evidence
policy, or billing authority has been selected and verified. CP-WP-004 and any
real dispatch remain blocked separately."

**This packet is not already-delivered work.** What exists is source-only
research and one consumed synthetic increment — preparation, not decisions. The
two decisions below are still open, and APR-102 itself records that the open row
"is not satisfied by this decision" while CP-WP-004's "own selection remains
open" (L239).

## 2. The synthetic boundary: what CP-WP-003A did and cannot be reused for

CP-WP-003A was the first offline capability proof. [APR-006](../approvals/APPROVAL_REGISTER.md#aegis-apr-006-control-plane-offline-capability-proofs-first-increment)
(L275–321) authorized it; [PR #123](https://github.com/ModernNomad-98/Project-Aegis/pull/123)
delivered it, merged as `c965595c3c388c94f15174d45fc3d2fa8fd073b4` from head
`d097d25cc65ebbd86cf5d5c132d772111bca690d`, changing 10 paths with 557 added
and 4 deleted lines (APR-068, register L1870–1876). The proof is real evidence
about the interface; it is not a production capability claim.

**The grant's own forbidden scope (register L306–312, verbatim):**

> At most 10 active implementation hours and 2,000 added code/test lines; zero
> task-controlled external spending. No real authority source, credential,
> customer data, provider call, deployment, real mutation, or phase advance.
> The public command-line interface stays synthetic-only. Source and host
> guarantees remain unproven until separately selected and tested.

**The grant is spent (register L1860–1861 and L1865–1867, verbatim):**

> **Event:** CONSUMED; target grant AEGIS-APR-006.
>
> **Status at recording:** AEGIS-APR-006 has no remaining use.

> **New authority:** None. This event records a past delivery and grants
> nothing. CP-WP-003 beyond this first increment, CP-WP-004 and any real
> dispatch stay blocked and need their own grants.

**Consequences that bind every option below.**

1. **The consumed one-use increment is never reused.** It cannot be extended,
   re-scoped, re-pointed at a real source, or cited as authority for an
   authenticated inspection, a claim write, a host probe, or a dispatch. A
   fresh, separately reviewed grant is required for each of those.
2. **A synthetic pass is not a real guarantee.** The [offline proof proposal](cp-wp-003-offline-proof-proposal.md)
   L97–98 states: "Passing a synthetic probe is evidence about the interface,
   not a production capability claim."
3. **No local artefact makes a real one-use claim.** The [real-authority
   decision packet](cp-wp-003-real-authority-decision-packet.md) L21 states: "A
   local journal, Git commit, PR approval, chat text or synthetic receipt alone
   cannot make a real one-use claim."
4. **Nothing has been contacted.** The [named-candidate matrix](cp-wp-003-named-candidate-matrix.md)
   records its own status at L3: "Public vendor documentation was inspected; no
   candidate account, service, host, credential, or endpoint was contacted." The
   [DynamoDB public-contract inspection](cp-wp-003-dynamodb-public-contract-inspection.md)
   records its own, differently worded status at L7: "Published AWS contracts
   were read; no account, credential, host, service endpoint, or customer data
   was accessed. This is an inference for later falsification, not a source
   selection or implementation grant."
5. **No cost is assumed.** The real-authority packet L19 states: "No $0
   operating cost is assumed." The matrix L48 states: "Pricing must be rechecked
   when a Region, account plan and test volume are known; the figures here are
   planning inputs as viewed 2026-09-25, not a quote or spend approval."

## 3. Decision D1 — CP-WP-003 real authority source, and the first authenticated read-only inspection

**Owner question:** *which approval source, account and custody arrangement
should CP-WP-003 bind — and do you separately authorize a read-only,
authenticated inspection of that source?*

This is the decision the real-authority packet describes at L9: "DynamoDB
remains the first inspection hypothesis, not a selection for execution." The
research compared the candidates; nothing is chosen.

| Option | What it means | Reason and benefit | Cost, drawback and condition |
| --- | --- | --- | --- |
| **A. DynamoDB first** (the research's first inspection hypothesis, **not** a selection) | One Amazon Web Services (AWS) account and Region; a single-Region conditional head plus `TransactWriteItems` for grant, claim and receipt | AWS documents atomic all-or-none transactions with conditional `Update`/`Put`; this is the pattern the research already inspected at the published-contract level, so the first authenticated read can test the specific limits it names | Needs a separately administered account or trusted broker, exhaustive Identity and Access Management (IAM) proof, a strongly consistent read of one complete head item or one `TransactGetItems`, and a pending-marker write-ahead protocol. A `ClientRequestToken` is idempotent for only 10 minutes, so it is a retry aid, not a durable effect identity. Reads, writes, storage, point-in-time recovery (PITR), CloudTrail data events and broker compute bill; no price is pinned here |
| **B. Firestore Native mode first** | One Google Cloud project; the same shared grant/receipt role held in Firestore documents, with server-side transactions | Transactions are atomic, retry on contention and fail offline; a readable transaction model that suits race tests | Server libraries bypass Firestore Security Rules and use IAM, so the local writer must not hold unrestricted server credentials. A retrying transaction callback cannot safely perform the target effect, and an uncertain commit still needs a stable receipt lookup. A free tier is not a $0 guarantee; project, region, volume and retention are unpinned |
| **C. Local single-owner ledger only** | Keep authority in one controlled host's ledger, with every controller and manual consumer routed through that one owner | Small offline prototype; clear local crash tests; no provider account or credential | Only viable as real authority if the **actual grant and operation** prove exclusive custody and fencing — neither is selected or proven. Restore of an older valid ledger still needs an independent anchor, and an outside consumer can otherwise reuse the same grant. This option is not available on the current evidence |
| **D. Defer the authenticated inspection** | Decide nothing now; keep researching or wait for owner, account and cost terms | Contacts nothing; leaves all options open; no spend and no credential exposure | Leaves real authority unproved and CP-WP-003/CP-WP-004 BLOCKED. Public documentation alone cannot establish this project's cross-consumer and host guarantees |

**Evidence any option must produce before it can be accepted.** This is the
requirement list, not a promise that any of it exists:

1. The exact account, Region and table (or project) identity, plus an
   independently protected table-incarnation pin such as DynamoDB's
   creation-time `TableId` — "a table name or ARN alone cannot reject deletion
   and recreation under the same name" (DynamoDB inspection L19).
2. The custody and broker principals, credential issuance, rotation,
   break-glass and trust boundary; and exhaustive IAM allow/deny and
   resource-policy tests. IAM scoping alone is not enough: "`dynamodb:LeadingKeys`
   only restricts keys; it does not enforce monotonic or append-only semantics"
   (DynamoDB inspection L42).
3. The verification read: "A strongly consistent `GetItem` of one complete head
   item, or one `TransactGetItems` for a multi-item vector, is the proposed
   verification read" (DynamoDB inspection L12).
4. The write-ahead protocol: a uniquely keyed `PENDING` record written before
   any external contact, so that "No target call occurs until a positive source
   outcome **and** a fresh current-head check establish this exact pending
   record" (DynamoDB inspection L22).
5. Race and lifecycle falsifiers: exactly one of the controller and the manual
   consumer can win one grant; revoke, expire and supersede are strictly
   ordered; and an uncertain acknowledgement is resolved by an authoritative
   marker read — never by a blind replay "after 10 minutes" (DynamoDB
   inspection L25, L33).
6. Recovery falsifiers: a restored table is "neither a current-head witness nor
   necessarily an atomic snapshot of the live transaction boundary" (DynamoDB
   inspection L15), and a replacement table must be rejected by the incarnation
   pin (L35).
7. **No claim, reservation or redemption write under any option.** The
   real-authority packet L48 is explicit for this step: "Select an exact
   candidate and obtain a separate reviewed grant before inspecting
   authenticated read-only source state or host capability facts. No claim,
   reservation or redemption write is included."

**Recommendation.** Take D1 before D2, because the owning register row orders
them that way ("Real source authority and capability proof for CP-WP-003, **then**
selection of one bounded real integration for CP-WP-004", L232). Within D1, the
real-authority packet's own sequence is (L47–50): source-only candidate research
(complete) → published-contract inspection (complete) → **select an exact
candidate and obtain a separate reviewed grant before inspecting authenticated
read-only source state** → optionally, under a further explicit grant, a
disposable test-namespace claim proof. The matrix states the same two-step rule
at its L50: "It must request a separate read-only inspection grant before
authenticated inspection, then a separate capped disposable write grant before
any claim." This packet keeps that order; it does
not reorder the steps and it does not claim the packet calls any option
"cheapest".

## 4. Decision D2 — CP-WP-004 single bounded real integration

**Owner question:** *once CP-WP-003's real prerequisites are accepted, which ONE
bounded real integration should CP-WP-004 deliver, and under what exact
idempotency, receipt, rollback, evidence and budget pins?*

**Policy context, and its boundary.** The owner's gradual integration roadmap
and release policy is recorded as [AEGIS-APR-102](../approvals/APPROVAL_REGISTER.md#aegis-apr-102-gradual-integration-roadmap-and-release-policy)
(register L3160–3237). Its event line is (L3162–3163): "**Event:** POLICY
DECISION; a policy decision only, not a GRANT. It selects a policy target and
grants no work." It covers six named integrations — Claude, Codex, DeepSeek,
Copilot, Cursor and Kimi — on five binding constraints (L3174–3200), and it
records the candidate ordering at L3202–3204: "The owner retained the existing
Claude Agent SDK bridge as the first planning candidate and Codex as the
proposed second candidate. The remaining integrations stay PARKED."

APR-102 **selects nothing here**. It says so itself (L3214): "It does not grant
Stage 4B, host proof, or CP-WP-003 and CP-WP-004 selection". The consistency note
in the open-decisions register is the binding reading (L239): "it selects
neither CP-WP-003 nor CP-WP-004"; the CP-WP-003/004 row "is not satisfied by
this decision"; and "Only the CP-WP-004 row's subject matter is touched, and
only to record that the visibility and selection policy around it is now settled
while its own selection remains open." The candidate order is planning
context for D2 — it is not a selection of the integration and it creates no
authority to build, install, contact, or spend.

One honesty note on wording, from APR-102's own evidence (register L3228–3229):
the phrase "Claude SDK bridge" "appears in no file on the default branch" —
except the register's own negative-evidence sentence that says so. This packet
therefore does not quote the phrase as a repo artefact; the first planning
candidate's in-repository identity is the offline package 4A prototype direction
named in `docs/roadmaps/aegis-setup-routing-plan.md`, exactly as APR-102
records it.

| Option | What it means | Reason and benefit | Cost, drawback and condition |
| --- | --- | --- | --- |
| **A. Claude Agent SDK bridge first** | The APR-102 first planning candidate becomes the bounded increment | Consistent with the recorded candidate order; an integration already scoped as a 4A prototype direction | APR-102 grants no work for it; the exact operation, target, host, containment, receipt and budget are all unpinned. Selection permits "only the work separately authorized for that increment" (L3188–3191) |
| **B. Draft GitHub PR target** | One bounded, reversible real target: open a draft PR as the operation, compared with local artifact export | The original packet row L352 names it: "a draft GitHub PR is a candidate reversible target for comparison with local artifact export"; reversible and already inside the repository's tooling | Needs exact target idempotency, status and receipt semantics, a rollback/cancellation rule, and host/containment proof. A GitHub approval record still cannot by itself make "an atomic one-use claim spanning a manual consumer and the controller" (real-authority packet L27) |
| **C. Local artifact export target** | One bounded export of a local artefact, with no external target | Smallest blast radius; no external provider call and no external spend | Does not prove an external target's receipt or bill; the [named-candidate matrix](cp-wp-003-named-candidate-matrix.md) L44 warns that a host/protocol proof "does not satisfy CP-WP-004's selected real delivery integration" |
| **D. Defer D2** | Decide the integration only after CP-WP-003's real prerequisites are accepted and evidenced | Matches the register's own ordering and the original packet row L352: "Decide the single integration only after CP-WP-003 evidence" | Leaves CP-WP-004 BLOCKED and delivers no integration; this is an honest option, not a failure |

**What the chosen option must pin before it is a selection.** Per the backlog
L270 and the real-authority packet L21 and L53, the owner grant must record:

1. The exact operation descriptor, target, input and effect identity — plus the
   allowed network, filesystem and process paths, bounded duration, and
   cancellation/descendant fence.
2. The target's own idempotency, status and receipt semantics, and the
   rollback or irreversibility rule.
3. Source, evidence and budget pins, including the worst-case liability cap and
   the dispute route: "Unknown amount keeps worst-case liability and slot; no
   assumed zero charge or refund" (real-authority packet L42).
4. The host and containment proof, and the evidence root, writer, readers,
   encryption/key custody, retention and redaction rule.
5. The owner's grant recording that exact scope, with its expiry or one-use
   limit, merged as a reviewed governance change before implementation.

Until then, no target is selected and no provider call is authorized. The
original packet rows still describe the work (open-decisions register L351,
L352; an ellipsis marks a cell boundary inside the row, and no punctuation is
added to the quoted cells):

> CP-WP-003: Prepare a zero-provider, synthetic capability-proof authorization
> with negative authority/race/rollback/path/process/receipt/billing probes …
> Separate reviewed CP scope and owner approval; no real adapter, deployment or
> provider call

> CP-WP-004: No delivery target selected; CP-WP-003 gates are unproven … Decide
> the single integration only after CP-WP-003 evidence; a draft GitHub PR is a
> candidate reversible target for comparison with local artifact export …
> Selection needs exact idempotency, receipt, rollback, source/evidence/budget
> pins and explicit owner authority

## 5. Named prerequisites — not decided, not granted

| Prerequisite | State | Evidence |
| --- | --- | --- |
| Evidence-computed transition guards (P2-6 option (a)) | **Entry criterion for CP-WP-003; not authorized** | Backlog L294–296: "Making the engine enforce guards computed from the checks that actually ran (option (a)) is now an entry criterion for CP-WP-003." Backlog L318–319: "Option (a), evidence-computed guards, remains an entry criterion for CP-WP-003 and is not authorized." The maintenance grant APR-086 is consumed by APR-098 |
| ZT-P1 offline role/stage transition contract | **NOT started**; needs a reviewed owner grant naming `tools/aegis_delivery_control/contracts.py` | Backlog L1688–1691 |
| CP-FUT-001 distributed ownership or hosted service | BLOCKED; out of scope for this packet | Backlog L83, L271 |
| BER separation | The Behavioral Eval Runner (BER) is a separate tool with separate approvals, data and runtime contracts; CP does not inherit BER policy by implication | Offline proof proposal L112–113; real-authority packet L41 |

These are named so the owner sees the whole chain. Naming a prerequisite grants
it nothing and starts nothing.

## 6. What this packet does not authorize

This packet authorizes **nothing**. In particular it does not authorize:

- creating, selecting or configuring an account, project, table, bucket or
  namespace;
- obtaining, rotating or using a credential, token or service identity;
- any authenticated read, inspection or host contact — including the read-only
  inspection in D1, which needs its own separate reviewed grant;
- any claim, reservation or redemption write, in a test namespace or anywhere
  else;
- any provider call, deployment, real mutation, dispatch or phase advance;
- any spending, budget, liability cap or $0 assumption;
- edits to the CP backlog, the approval register or the open-decisions
  register; and
- any reuse of the consumed AEGIS-APR-006 increment.

## 7. Recording note

Decisions D1 and D2 become real only when the owner's exact words are recorded
through separately reviewed governance changes — the
[CP backlog](resumable-control-plane-backlog.md),
the [approval register](../approvals/APPROVAL_REGISTER.md), and/or the
[open-decisions register](aegis-open-decisions-2026-09-23.md). This packet's own
pull request does not edit any of them and does not record an answer.

## Sources and verification

All quoted lines were read at the base commit
`279338a938168843fabebff12acd30359a0fc414`:

- [`docs/roadmaps/aegis-open-decisions-2026-09-23.md`](aegis-open-decisions-2026-09-23.md) — L43, L44, L232, L239, L351, L352.
- [`docs/approvals/APPROVAL_REGISTER.md`](../approvals/APPROVAL_REGISTER.md) — AEGIS-APR-006 (L275–321), AEGIS-APR-068 (L1858–1879), AEGIS-APR-102 (L3160–3237).
- [`docs/roadmaps/resumable-control-plane-backlog.md`](resumable-control-plane-backlog.md) — L78–83, L268–271, L273–282, L284–319, L1684–1691.
- [`docs/roadmaps/cp-wp-003-named-candidate-matrix.md`](cp-wp-003-named-candidate-matrix.md) — L3, L7–11, L19–22, L32–36, L40–44, L48–52.
- [`docs/roadmaps/cp-wp-003-dynamodb-public-contract-inspection.md`](cp-wp-003-dynamodb-public-contract-inspection.md) — L7, L11–15, L19–25, L33–38, L42–46.
- [`docs/roadmaps/cp-wp-003-offline-proof-proposal.md`](cp-wp-003-offline-proof-proposal.md) — L16–24, L61–69, L86–100, L104–116.
- [`docs/roadmaps/cp-wp-003-real-authority-decision-packet.md`](cp-wp-003-real-authority-decision-packet.md) — L5, L9, L15–21, L27, L37–44, L47–53.

**Certainty labels used above:** DONE, BLOCKED, CONSUMED, POLICY DECISION, NOT
started and UNPROVEN are the sources' own states, not this packet's judgement.
The option tables and the recommendation are this packet's proposal to the
owner; they are not decisions and carry no authority.
