# BER WP-2B-3 owner decision chain — WP-2B-3/4/5/6/7, R2 and OD-1

**Status: owner decision-chain page for review, 2026-10-11 (Stage C revision 2,
the seven Codex findings triaged at Stage D applied). This page grants
nothing.** Every gate below is separately authorized, separately evidenced and
separately recorded. Reading this page, or merging the pull request that adds
it, approves no label, selects no execution source, renews no allowance,
authorizes no host or provider step, unseals no holdout, and ratifies no owner
decision. Its only job is to place the open owner decisions in one order, with
the evidence each one needs before it can be taken.

Prepared 2026-10-11 against `origin/main`
`279338a938168843fabebff12acd30359a0fc414` (2026-10-11 14:54 -07:00).

**Citation convention, and per-cited-line identity.** Short names used below:
**register** = [open decisions register](aegis-open-decisions-2026-09-23.md);
**backlog** = [BER backlog](behavioral-eval-runner-backlog.md);
**measurement packet** = [measurement prerequisite decision
packet](ber-wp2b3-measurement-prerequisite-decision-packet.md);
**APR register** = [APPROVAL_REGISTER](../approvals/APPROVAL_REGISTER.md);
**reconciliation v4** =
[step-0 reconciliation v4](../reconciliation/step-0-reconciliation-v4.md).
Line references name each file's lines at the baseline above. The Stage B audit
of this packet's plan (SD-B ACCEPT, findings F-1/F-2/F-3) re-read every cited
**line**, not every cited **file**, at that baseline; the two files a sibling
lane touched carried unrelated appends outside the cited ranges, so identity is
claimed per cited line. **Certainty labels** used below: *confirmed* = quoted
from a cited repository line or resolved by a command; *inferred* = follows
from confirmed lines but is not itself written down; *unknown* = no public
source states it; **UNVERIFIABLE-FROM-PUBLIC-CLONE** = the object lives in the
owner-only private repository and cannot be resolved from the public clone.

**Reading key for delivery terms.** Behavioral Eval Runner (BER) is the
evaluation tool. WP-2B-3 is its numbered measured-calibration work package —
the Measured Judge Calibration and Owner Decision One (OD-1) Ratification Gate.
**Development** is the 40-case characterization stage; the **sealed holdout**
is the separate 120-case one-pass measurement; `OWNER_WAIT` is the mandatory
pause between them (measurement packet L5). A **source pin** is an exact
reviewed Git commit and tree, not a branch name; an **allowance** is the
verified unused portion of the existing call, token and dollar ceilings, not a
new budget; a **selected-host preflight** verifies the actual machine, evidence
root, identity and provider controls before any request (measurement packet
L5). `JUDGE_ERROR` is an unsuccessful judge outcome, not a passing verdict.
OD-1 is the owner's later disposition of the measured result. R1–R5 are the
Phase 2B-0 evidence gates (backlog L393–L685).

## 1. The chain at a glance

The measured-calibration chain has seven gates, in this order; the host ladder
H runs beside gates 1–3 but substitutes for none of them, and nothing below
gate 4 is authorized by completing H.

| # | Gate | Owner decision | Current status |
| --- | --- | --- | --- |
| G1 | Private candidate labels | Approve the exact bytes, labels, split and hashes of 160 pending private candidates | PENDING (register L40, L233; measurement packet L15) |
| G2 | Live execution source | Select the exact audited source commit **and tree** | Not selected; the offline head is not a live source (measurement packet L16) |
| G3 | Remaining allowance | Reconcile historical usage and permit dispatch within the recorded caps | Unreconciled; assume zero residual until reconciled (register L349) |
| G4 | Selected host and provider preflight | Authorize the preflight, and the one read-only model-availability request once G3 settles | Not authorized (measurement packet L18) |
| G5 | Measured development, then `OWNER_WAIT` | Authorize the 40-case development stage | Not authorized (measurement packet L19) |
| G6 | Holdout freeze | Freeze every BER-DEC-008 decision-35 field, source pin and reconciled allowance | Not frozen (measurement packet L20) |
| G7 | One measured holdout and OD-1 | Execute the 120 holdout identities once; ratify or explicitly decline OD-1 | OD-1 OPEN, never ratified (backlog L2139, L2175–L2181) |
| H | Host / R4 / R5 ladder | Fix the Stage A host-phase time ceiling and disposition Stage A; confirm or stop Stage B | Stage A grant merged; no public receipt found, so the probe's execution state is unverified; Stage B authorized, bounded, in flight (backlog L3974–L4048; reconciliation v4 L4406–L4434) |

**Recommended order (mirrors the measurement packet's own):** G1 → G2 → G3 →
G4, then G5, G6, G7; the host ladder H runs in parallel with G1–G3 and is not a
substitute for any of them. The measurement packet states the reason as
"the recommended order retires the cheapest uncertainty first" (measurement
packet L31, *confirmed*).

**Honesty statement.** This packet is not already-delivered work. WP-2B-3 is
AUTHORIZED but not DONE (backlog L1079–L1090, L1254–L1255); all seven gates
above remain open except the offline synthetic-support increment (backlog
L1092–L1112); OD-1 is open (backlog L2139); R2 is BLOCKED (backlog L472–L476);
no public Stage A probe receipt exists in `docs/evidence/` on the baseline, and
absence from the repository does not establish that no probe command ran — the
grant places raw receipts in an external evidence root, so the probe's
execution state is **unverified** until those artifacts are checked; Stage B is
authorized and recorded but not an R4/R5 proof (backlog L4040–L4048;
reconciliation v4 L4406–L4434). The owner work that remains is exactly the
chain this page presents.

## 2. The seven measured-calibration gates

Each gate is a separate owner decision with its own evidence. Every gate below
carries a defer/stop option, so declining to decide is always available and is
never treated as consent.

### G1 — Private candidate labels

**Owner question:** approve the exact private candidate packet, request a new
immutable version, or decline or defer the review?

The register records the open item as "Semantic review and exact-byte approval
of the 160 pending private candidates; this index does not inspect them"
(register L233, *confirmed*), and the replacement-labels row as "records 160
pending candidates. Owner semantic review and exact-byte label approval remain
open; this index does not inspect or approve private inputs" (register L40,
*confirmed*). The measurement packet puts the same decision first: "Peter
Nguyen can **inspect and dispose the private candidate PR #1** at exact commit
`6beba11e83e5e8a1655f33302e40959ecc6067e5` (approve its exact labels, guide,
split and hashes; request a new version; or decline it), or defer that review"
(measurement packet L9, *confirmed*). The packet's own boundary sentence
follows: "Reading or accepting this public packet is not dataset approval"
(measurement packet L9, *confirmed*).

| Option | What it means | Cost, risk, or rejection reason |
| --- | --- | --- |
| A. Approve the exact bytes | Owner records approval of the exact dataset, guide, split and SHA-256s in the private `owner-label-approval.json` | Requires the full semantic and exact-byte review first; "A changed byte needs a new version and owner review" (measurement packet L15, *confirmed*) |
| B. Request a new immutable version | Repairs a disputed label, case or split before it can bias measurement | "Requires a new immutable input version, fresh hashes and renewed owner review; shifts all dependent source/freeze pins" (measurement packet L28, *confirmed*) |
| C. Decline the candidate | Stops the replacement-input path | Leaves WP-2B-3 without an approved dataset; "No provider spend should occur during that review" (measurement packet L28, *confirmed*) |
| D. Defer the review | Keeps every later gate closed | Costs schedule, not correctness: G2–G7 all remain blocked behind it. This is a real option, not a stall |

**Evidence each option needs:** all 160 transcripts, proposed PASS/FAIL labels
and rationales, risk tags, split map, labeling guide, quality report, manifest
and source cards in the owner-only repository
`ModernNomad-98/Project-Aegis-Calibration-Inputs`; the verified 40 development
/ 120 sealed split, per-control balance, critical and adversarial quotas,
semantic independence, and the exact private commit and file/SHA-256 hashes
(measurement packet L15, *confirmed*). The public sanitized checkpoint records
opaque identities only — it lists the candidate dataset semantic SHA-256, the
dataset file SHA-256, the split-map semantic SHA-256, the labeling-guide file
SHA-256 and the quality-report file SHA-256, plus "160 distinct records; 40
development / 120 holdout" and a "Full offline judgment input bound" of
"Maximum 5,040 against the 8,000 ceiling; no provider call" (candidate summary
L45–L53, *confirmed*). Those are screening results, "not gold labels"
(measurement packet L15, *confirmed*). The literal count of 160 candidate files
and the private commit `6beba11e…` **cannot be resolved from this public
clone** — `git cat-file -t 6beba11e83e5e8a1655f33302e40959ecc6067e5` fails
with "could not get object info" locally, which is expected because the object
lives in the private repository: **UNVERIFIABLE-FROM-PUBLIC-CLONE** (audit
finding F-2). The 160 figure is re-cited, not re-derived. The owner may be the
sole gold-label authority, and the honesty rule is explicit: "do not claim two
independent labels if only one person reviewed" (measurement packet L15,
*confirmed*).

### G2 — Live execution source

**Owner question:** select the exact audited live execution source — commit and
tree — by a separate owner-reviewed BER-DEC amendment, keep BER-DEC-008's
original baseline, or defer?

The measurement packet requires the owner to "Identify the audited source
commit **and Git tree** for both development and holdout, reconcile intervening
normative BER changes, and explicitly select the execution branch/clone and any
change from BER-DEC-008's original baseline" (measurement packet L16,
*confirmed*). It states the offline code's identity precisely: the
implementation head `bf72d391831c9c6c30eedd295d07a2ff32b47fe4`, tree
`cd4f944406ac79884de204f4d1e135e444316383`, and merge
`fa37c0e545dfd096e8327ca5357b0dfc6e2f8bb5` "identify reviewed offline code,
**not** an approved live source" (measurement packet L16, *confirmed*). All
three hashes resolve in this clone (*confirmed*: `git cat-file -t` /
`git merge-base --is-ancestor fa37c0e5 origin/main`). BER-DEC-010 "preserved
the original measured-execution branch and baseline" and BER-DEC-012 "selected
no live source"; therefore "An offline merge or moving `main` cannot silently
replace either" (measurement packet L16, *confirmed*). The register's source
row likewise says a "reviewed execution source" remains a prerequisite and that
"[n]o provider metadata or judgment request, dependency install or new source
pin follows from this proposal" (register L41, L349, *confirmed*).

| Option | What it means | Cost, risk, or rejection reason |
| --- | --- | --- |
| A. Name the audited commit and tree | A separate owner-reviewed BER-DEC amendment fixes the development and holdout source pins | Needs a full audit of the named revision against intervening normative BER changes, plus private input commit, dataset, guide and split hashes pinned into the execution record |
| B. Keep the BER-DEC-008 baseline | No amendment; the original measured-execution branch and baseline stay the candidate | Must still be proven to be a reviewed live source with an audited tree; the offline PR does not become one, and the original baseline may not carry the delivered offline support |
| C. Defer | Every later gate stays closed | Costs schedule only; no source risk is incurred |

**Evidence each option needs:** the exact source commit **and** Git tree for
development and holdout; reconciled normative BER changes; the private input
commit and dataset/guide/split hashes; and proof that the offline head is not
being used as the live source (measurement packet L16, *confirmed*). The
private input pins are **UNVERIFIABLE-FROM-PUBLIC-CLONE**.

### G3 — Remaining allowance and price

**Owner question:** reconcile authoritative historical provider usage and
permit dispatch within the remaining headroom, assume zero available and stop,
or defer?

The measurement packet requires the owner to "Recover authoritative historical
provider usage and reservations, including uncertain attempts, and reconcile
the single durable ledger before granting dispatch" (measurement packet L17,
*confirmed*), and states the binding caps (see §5 below). Two boundaries are
stated verbatim in the sources. First: "Missing old evidence does not prove
zero use. Unknown or exhausted headroom, unavailable telemetry, or materially
changed price stops all metadata and judgment calls until the owner resolves
it. No allowance is renewed by candidate or offline-support delivery"
(measurement packet L17, *confirmed*). Second, the operational posture: the
register's own recommendation is to "[o]perationally assume **zero available
residual allowance** until independently reconciled, without changing the
historical grant" (register L349, *confirmed*).

| Option | What it means | Cost, risk, or rejection reason |
| --- | --- | --- |
| A. Reconcile, then authorize within remaining headroom | Reconciliation alone permits no dispatch: it records the remaining allowance against a current price, and dispatch stays prohibited until G4 and G5 separately pass | Requires authoritative historical usage including uncertain attempts; a provider-side project spend limit at or below the ceiling; and a stop-before-exceed rule. An unresolved or exhausted headroom stops it |
| B. Assume zero available and stop | No dispatch is attempted | Safest and always available; leaves the calibration unmeasured and OD-1 open |
| C. Defer | Accounting is done later | Costs schedule; no spend risk |

**Evidence each option needs:** authoritative historical usage and reservations
including uncertain attempts; remaining headroom shown against the lifetime
maxima quoted in §5; a rechecked current provider price with the worst
permitted path recomputed against the cap; and a recorded provider-side project
spend limit plus stop-before-exceed rule (measurement packet L17, *confirmed*).
No dollar figure beyond the recorded caps is asserted on this page: the
recorded USD $158 path is "historical pricing math, not a quote for today"
(measurement packet L17, *confirmed*), and this page fabricates no price.

### G4 — Actual selected-host and provider preflight

**Owner question:** authorize the selected-host and provider preflight — and,
once G3 settles, the one authorized read-only model-availability request — or
defer?

The measurement packet requires verification of "the chosen host identity,
exact audited checkout, execution account, encrypted external evidence
volume/root, access controls, ownership marker, private repository visibility
and hash restore, process-scoped dedicated service-account credential,
dedicated project, model access, `openai` 3.0.0 integrity,
`api.openai.com:443` TLS path without unapproved proxy, retention posture, and
stop/cleanup controls under BER-DEC-008/010" (measurement packet L18,
*confirmed*), and it states the stop rule: "A missing or unverifiable
host/evidence/credential/provider fact stops live execution" (measurement
packet L18, *confirmed*). It also names the older candidate platform honestly:
the "owner-selected disposable VirtualBox Linux guest is still a **candidate**:
installer boot is recorded, but guest configuration and selected-host proof are
not. Its proposed offline Stage A capability probe needs its own grant; generic
Linux CI is not host proof" (measurement packet L18, *confirmed*) — that
VirtualBox sentence is a dated statement of the platform under consideration in
2026-09-25 and is superseded on the platform question by the 2026-10-10 WSL2
decision recorded in §3 below; the host-proof requirement it states is not
superseded.

| Option | What it means | Cost, risk, or rejection reason |
| --- | --- | --- |
| A. Authorize the preflight, on whichever live host the owner has separately selected | Host identity, evidence root, credential custody, provider project and TLS path are verified on the selected host before any dispatch | G4 stays host-agnostic: no source selects a measured-execution host yet, so the owner's selection of the live host is a separate decision before this option can be taken; on a host other than the current Windows root it also needs APR-009's own verified mechanism and access decision (APR register L419–L421, *confirmed*). It requires every listed fact to be present and verifiable, and the one read-only model-availability request to wait for G3; no Stage A result substitutes for it |
| B. Defer | No host or provider step occurs | Leaves G5–G7 closed; costs schedule only |

**Evidence each option needs:** the full preflight fact list quoted above, plus
Stage A receipts where available (measurement packet L18, *confirmed*). Two
decisions separate here: selecting the live host, and authorizing this
preflight on it. APR-126 selects WSL2 only for the Stage A candidate, and "A
different selected host requires its own verified mechanism and access
decision" (APR register L419–L421, *confirmed*); selecting the live host is
its own decision, and taking this gate does not make it. Stage A's capability
observation "could support a **Stage A capability observation only** — 'not a
production isolation claim, permission for provider calls, or a BER baseline
result'" (backlog L3989–L3992; APR register L5469–L5472, *confirmed*, the
capability-observation honesty line verbatim).

### G5 — Measured development, then `OWNER_WAIT`

**Owner question:** authorize the 40-case development stage under the ledger,
with a mandatory stop at `OWNER_WAIT`, or stop?

The measurement packet scopes it: "Run only the 40 approved development
identities through the pinned judge and durable ledger, with no sealed holdout
access. Preserve attempts, token and spend accounting, errors and exact
output/reasoning-token distribution. Stop at `OWNER_WAIT`; present the
distribution, incomplete/`JUDGE_ERROR` outcomes, and proposed safety margin to
Peter" (measurement packet L19, *confirmed*). Its stop row is equally explicit:
"No automatic transition from development to holdout; no retry for a semantic
miss or incomplete response; no tuning against holdout cases" (measurement
packet L19, *confirmed*).

| Option | What it means | Cost, risk, or rejection reason |
| --- | --- | --- |
| A. Authorize development to `OWNER_WAIT` | Produces the characterization distribution the freeze decision reads | Spends against the reconciled allowance and requires the G3 and G4 facts to hold; the stage cannot touch the sealed holdout |
| B. Stop before development | Nothing is spent; no distribution exists | Leaves G6 and G7 without their input and OD-1 open |

**Evidence each option needs before authorizing:** the G3 and G4 facts must
hold — the reconciled ledger and the passed selected-host/credential/provider
preflight; the development distribution does not exist yet, and nothing more is
asked of the owner at this authorization (measurement packet L18–L19,
*confirmed*). **Evidence the later G6 decision needs at `OWNER_WAIT`:** the
development distribution, the incomplete/`JUDGE_ERROR` outcomes, and a proposed
safety margin, produced by the authorized run and presented there at
`OWNER_WAIT`; the stop option produces no distribution (measurement packet L19,
*confirmed*).

### G6 — Holdout freeze

**Owner question:** freeze all BER-DEC-008 decision-35 fields, the source pins
and the reconciled allowance before unsealing — or stop?

The measurement packet requires the owner to "independently freeze and hash
**all** BER-DEC-008 [decision 35](behavioral-eval-runner-backlog.md#ber-dec-008)
fields before unsealing: provider and model snapshot; endpoint; SDK/transport
version; system policy; rubric contracts; verdict schema; dataset; split map;
labels; reasoning effort; final holdout `max_output_tokens` within
**8,192–25,000**; retention settings; thresholds; retry policy; and call, token
and dollar caps", and to "bind the audited development and holdout source
heads/trees, exact private input commit and hashes, development manifest and
summary digest, and reconciled remaining allowance" (measurement packet L20,
*confirmed*). Its stop row: "Any missing or mismatched freeze field, source
pin, cap, or evidence digest denies dispatch. A post-hoc change creates a new
versioned attempt and needs a new sealed holdout or explicit owner
authorization" (measurement packet L20, *confirmed*).

| Option | What it means | Cost, risk, or rejection reason |
| --- | --- | --- |
| A. Freeze all fields, pins and allowance | A complete freeze makes the run eligible for the separate G7 execution decision — the freeze itself authorizes no execution, and the holdout stays unsealed until G7 is separately granted | Any later change voids the attempt and needs a new sealed holdout; the freeze must be complete, not partial |
| B. Stop | No unsealing occurs | Leaves OD-1 without its measured input; the 120 identities stay sealed |

**Evidence each option needs:** the complete freeze field list quoted above,
the audited source heads/trees, the exact private input commit and hashes, the
development manifest and summary digest, and the reconciled allowance
(measurement packet L20, *confirmed*). The private input commit and hashes are
**UNVERIFIABLE-FROM-PUBLIC-CLONE**; the freeze record must carry them as
recorded private facts, not as claims this page can check.

### G7 — One measured holdout and OD-1

**Owner question:** after one measured holdout pass, ratify OD-1 on the
measured result, explicitly decline it, or defer?

The register records the outstanding state as "Historical accounting, exact
reviewed live execution source, private label approval, host proof and an
explicit call/token/dollar cap remain prerequisites. **No measured result or
OD-1 ratification exists**" (register L41, *confirmed*). The backlog records
OD-1 as "OWNER DECISION REQUIRED **DURING 2B-0**", covering "the initial
acceptance thresholds (accuracy/agreement, false-PASS rate, false-FAIL rate,
abstention rate) **and the separate critical false-PASS threshold**, together
with the measured calibration result, before the judge produces any
baseline-eligible semantic verdict" (backlog L2146–L2150, *confirmed*), and
then records that the during-2B-0 timing was missed: "**Post-2B-0 status
(2026-08-11): OPEN — not completed during 2B-0.**" (backlog L2154,
*confirmed*). The post-authorization note is the operative one: "OD-1 is
ratified or explicitly declined by Peter Nguyen only after the measured
sealed-holdout evidence is reviewed (backlog §7 WP-2B-3; BER-DEC-008 OD-1
terms)" (backlog L2179–L2181, *confirmed*); the current reconciliation line
reads "OD-1 remains OPEN for measured-result ratification" (backlog L2139,
*confirmed*).

The measurement packet's stop row is binding on the outcome: "A threshold miss
means calibration not accepted and OD-1 stays open; no retry-until-green,
baseline-eligible semantic verdict, Scenario A live suite, or WP-2B-4
authorization follows. An uncertain interrupted pass cannot be restarted
automatically" (measurement packet L21, *confirmed*).

| Option | What it means | Cost, risk, or rejection reason |
| --- | --- | --- |
| A. Ratify OD-1 on the measured result | Unblocks R2 and, with the other WP-2B-4 dependencies, the later live phase | Only available if every pre-registered threshold is met on the one measured pass; ratification of a miss is not an option the sources leave open |
| B. Explicitly decline | Records calibration as not accepted and keeps OD-1 open | Leaves R2 BLOCKED (backlog L472–L476) and WP-2B-4 blocked; it is the honest disposition on a miss |
| C. Defer | No disposition is recorded | Leaves OD-1 open; costs schedule only |

**Evidence each option needs:** the full confusion matrix, denominators, the
adversarial injection subset, all six pre-registered BER-DEC-008 thresholds,
judge identity, usage and cost, the evidence inventory, and only a sanitized
public summary (measurement packet L21, *confirmed*). The six thresholds are
BER-DEC-008 decisions 11–16 and the freeze fields are decision 35 (backlog
L3364–L3366, L3485, *confirmed* per the Stage B audit).

## 3. The host / R4 / R5 ladder (H)

The host ladder is a platform decision, a setup grant, a probe grant and a
model-driven authorization — not a live-host proof. It runs in parallel with
G1–G3 and completes none of them.

**Platform decision and setup (2026-10-10).** APR-126 records the owner's
approval of "ONE agent-assisted disposable WSL2 Ubuntu 24.04 distribution
setup", with the platform decision quoted as "**WSL2 selected** for the
candidate; the existing VirtualBox VM is **NOT deleted** — deletion requires
separate approval plus operator confirmation; the VM stays untouched and
unverified" (APR register L5367–L5384, *confirmed*). Its Scope FORBIDDEN is
explicit that the grant "does not authorize BER Stage A or Stage B tests,
source transfer into the distribution, provider/model calls, private inputs,
credentials in chat or source, paid services, production use, changes to
Windows security or hypervisor features, any action against the VirtualBox VM
(deletion, modification, power-state change), WSL distribution deletion
(`wsl --unregister Ubuntu-24.04` IS deletion and requires a separate owner
approval plus operator confirmation), or evidence deletion", and adds "A
separate BER-DEC grant is required before even the offline Stage A host probe"
(APR register L5396–L5404, *confirmed*). APR-127 records the platform
supersession of APR-028's VirtualBox choice with "**New authority:** None" and
leaves "the VirtualBox VM ... **intact, untouched and unverified**" (APR
register L5414–L5434, *confirmed*).

**Probe grant (merged).** APR-128 records the owner's "go" of 2026-10-10 for
"ONE offline BER R4/R5 Stage A host probe on the named WSL2 distribution",
scoped to the distro alias `aegis-ber-stage-a-wsl`, user `peternguyen` and
scratch root `/home/peternguyen/aegis-stage-a` (mode 700), offline, with the
five required POSIX test IDs pinned (APR register L5438–L5472, *confirmed*).
Its Scope FORBIDDEN repeats the deletion rule — "DELETION — of the distro or
the VirtualBox VM — which requires the owner's separate approval plus operator
confirmation (the owner's 2026-10-10 rule, quoted)" — and adds "A separate
authorization is required before any Stage B model-driven proof" (APR register
L5473–L5481, *confirmed*). BER-DEC-016 is its decision-log entry: owner
**"go"**, effective only on merge of the reviewed governance PR, with the probe
"a separate, later host phase that runs only under the merged grant" (backlog
L3974–L3982, *confirmed*); ONE probe, "consumed when the host phase completes
its receipts" (backlog L4040–L4042, *confirmed*); the exact commit and tree
"fixed at host-phase start from the then-current `origin/main`, recorded in
the host-phase receipt before any probe command" (backlog L4002–L4004,
*confirmed*). The grant is merged on the baseline: commit `b65bd3fc`
("docs: BER Stage A offline host probe grant - APR-128 + BER-DEC-016 (D89)",
2026-10-10 13:33:28 -07:00) is an ancestor of `origin/main` `279338a9`
(*confirmed* by `git merge-base --is-ancestor`). **No public Stage A probe
receipt exists in `docs/evidence/` on the baseline** (*confirmed* by the Stage B
audit's `git ls-tree` absence check, audit evidence (6)) — public absence does
not establish that no probe command ran, because the grant places raw receipts
in the external evidence root; the execution state stays **unverified** until
that root is checked (APR register L5438–L5491, *confirmed*).

**Stage B (model-driven), authorized 2026-10-11.** D94 in reconciliation v4
records the owner's Q2 selection with "start on all these" plus the standing
blanket pre-approval, and bounds the run: "ONE bounded run class — three
synthetic Scenario-A-shaped prompts executed via the session harness's current
model route (no new provider account, no credentials stored anywhere)", on the
named distro only, with BER source refreshed to the Stage B base pin
`26bfc772`, "a 60-minute ceiling, the runner's NON-LIVE construction
respected — the live-dispatch gate's deterministic `LIVE_DISPATCH_DISABLED`
denial is invoked and observed per prompt, never worked around — no deletion,
no package installs, no network beyond the harness provider route"
(reconciliation v4 L4406–L4422, *confirmed*). The honesty line every Stage B
artifact carries is "a capability observation ONLY — NOT a production isolation
claim, NOT a BER baseline result"; "No new APR is created"; and "The lane adds
NO repository code" (reconciliation v4 L4410, L4422–L4434, *confirmed*). D94's
commit `b4e4c16b` is an ancestor of `origin/main` (*confirmed*).

**Two stale-by-supersession register rows, flagged and not edited.** Register
L234 records the open item "Disposable Linux VM — Whether and when to resume
the paused VirtualBox setup; a Stage A host probe needs its own grant", dated
by the row's last re-check at 2026-09-30 (register L234, L237, *confirmed*).
That row is stale in part: the platform decision is now the 2026-10-10 WSL2
decision — **platform decision (APR-126/127)**, with **the probe grant now
merged (APR-128 + BER-DEC-016)** — while the VirtualBox VM itself "remains
intact, untouched and unverified" and its deletion is expressly not authorized
(APR register L5421–L5423, L5478–L5480, *confirmed*). The same split applies to
register L42's "No Stage A probe ... is authorized or recorded" and to register
L350's "then authorize its bounded offline probe" recommendation wording: the
*authorization* half is superseded by APR-128/BER-DEC-016; the *host proof*
half is not — the WSL2 distribution is the selected **candidate** platform, and
"no selected-host capability proof exists" (register L350, *confirmed*).
**Correcting or annotating any register row is a register edit and needs its
own grant; this page therefore only flags the staleness.**

**What the ladder does not do.** Neither Stage A nor Stage B is an R4/R5
live-host proof. R4 ("effective per-tool-path confinement proven for the
selected live host, including control-plane corpus inaccessibility") and R5
("execution-profile observability and isolation proven for the selected live
host, or an explicit owner-approved narrower live claim scope ...") remain
WP-2B-4 dependencies (backlog L1264–L1268, *confirmed*). Passing Stage A could
support only the capability observation quoted above; a skipped required POSIX
case "is an unmet proof, not a pass" (backlog L4014–L4015, *confirmed*).

**Owner decisions still open on this ladder:**

| Option | What it means | Cost, risk, or rejection reason |
| --- | --- | --- |
| A. Fix the Stage A host-phase time ceiling and run the probe | The merged APR-128/BER-DEC-016 grant is executed under its own receipts | The exact ceiling value "is fixed by the owner at host-phase authorization and recorded in the host-phase receipt before any probe command runs" (backlog L4026–L4030, *confirmed*); a required POSIX skip or any stop rule ends it as `NON_BASELINE` or `UNAVAILABLE`, "not a partial pass" (backlog L4036–L4039) |
| B. Disposition Stage A, and separately confirm or stop Stage B | Stage A's disposition is reviewed on its own; Stage B continues under its own recorded authorization, with no Stage A-first ordering | D94 imposes no Stage A precondition on Stage B's continuation — its start is unconditional (reconciliation v4 L4406–L4434) — and stopping Stage B is available and costs only the capability observation |
| C. Defer | Nothing further runs | Costs schedule only; G1–G7 are unaffected in either direction |

## 4. Downstream prerequisites (named, not decided here)

These are named so the chain is readable end to end. None is granted by this
page, and none follows from any choice made above.

**WP-2B-4** is "**Status:** BLOCKED — separate first-live phase; NOT authorized
by BER-DEC-007. Unblocks only when every dependency below exists, including a
separate reviewed and merged WP-2B-4 authorization with a live-token budget, a
live external evidence root, evidence-handling and retention terms, and live
stop conditions" (backlog L1239–L1242, *confirmed*). Its six dependencies are
enumerated as ALL of: (1) WP-2B-1 DONE (PR #83) and WP-2B-2 DONE (PR #85, merge
`b84e43ad`) — *satisfied* — and WP-2B-3 DONE, "which remains UNMET (WP-2B-3 is
AUTHORIZED by merged BER-DEC-008, not DONE)"; (2) "a truthful R1
activation-identifying mechanism or an explicitly owner-approved bounded
activation claim scope sufficient for Scenario A's claims"; (3) R2 measured
calibration completed and OD-1 ratified through WP-2B-3; (4) R4 proven for the
selected live host; (5) R5 proven for the selected live host, or an explicit
owner-approved narrower live claim scope that "defines exactly what remains
unobservable and excludes affected runs from baseline claims"; and (6) "a
separate reviewed and merged WP-2B-4 authorization with live-token budget, live
external evidence root, evidence terms, and stop conditions" (backlog
L1251–L1269, *confirmed*). The trigger is equally explicit: "WP-2B-4 may not be
authorized while R1, R2/OD-1, R4, or R5 remains unresolved for the selected
live execution profile" (backlog L1270–L1272, *confirmed*).

**WP-2B-5/6/7** are BACKLOG, and each "requires its own owner phase
authorization". WP-2B-5 (generic corpus execution) is **Status: BACKLOG** with
dependencies "WP-2B-4 DONE; the 2B-0 gate resolved to outcome A or an
owner-approved limitation ...; owner authorization for WP-2B-5", and its own
note that "WP-2B-5 remains BACKLOG and separately owner-authorized" (backlog
L1311–L1342, *confirmed*). WP-2B-6 (scheduling, cost, quarantine and cadence)
depends on "WP-2B-5 DONE; owner authorization for WP-2B-6" and requires "OD-3
ratification if still pending" (backlog L1366–L1399, *confirmed*). WP-2B-7
(advisory CI and operator workflow) depends on "WP-2B-6 DONE; owner
authorization for WP-2B-7", is "the SOLE owner of actual advisory CI
integration", and its promotion remains separate: "WP-2B-7 implements advisory
CI only, and a separate later owner decision is still required to promote the
lane; nothing in this phase activates blocking CI" (backlog L1409–L1456,
*confirmed*), with "the separate later promotion decision — pending OD-2
ratification and the durable human promotion approval under the DECIDED §17
criteria" (backlog L1453–L1456, *confirmed*).

**Other named owner decisions:** OD-2 (minimum promotion coverage threshold;
owner decision required before CI promotion), OD-3 (risk-class-aware
operations, consumed by WP-2B-6), and OD-4 (a future authenticity decision)
are later gates than OD-1 (backlog L2139–L2141, *confirmed*). **BER-BKL-009
residual:** the evidence policy is selected — APR-009 chose the 30-calendar-day
complete-bundle policy from first evidence creation, with "owner plus
operating-system SYSTEM access and host-verified BitLocker encryption" for the
current Windows WP-2B-3 root and "A different selected host requires its own
verified mechanism and access decision" (APR register L402–L435, *confirmed*).
The residual remains open: "Real-host access, encryption, privacy and operator
cleanup remain unscoped" (register L39, *confirmed*), and "[t]his decision
grants no automatic deletion, additional reader, provider call, holdout access,
or measured result" (APR register L426–L431, *confirmed*).

## 5. Budget caps, as the measurement packet states them

The only figures this page carries are the recorded caps. They are quoted, not
recomputed, and no price or spend projection is asserted: "Recheck current
provider price and recompute the worst permitted path against the cap; the
recorded USD $158 path is historical pricing math, not a quote for today"
(measurement packet L17, *confirmed*).

> Show remaining headroom against BER-DEC-008's lifetime maxima: **200 judgment
> attempts including retries; one read-only model-availability request; 201
> total external requests; 8,000 input tokens per judgment; USD $175 total and
> USD $175 per day**.

— measurement packet L17, *confirmed*; independently corroborated by BER-DEC-008
decisions 17–20 in the backlog (L3371–L3381, *confirmed* per the Stage B audit).
The delivery deadlines are caps, not estimates: "Active execution has
BER-DEC-008's 90-minute development, four-hour holdout and six-hour package
deadlines, excluding `OWNER_WAIT`; these are caps, **not an ETA**"
(measurement packet L27, *confirmed*). "No total ETA follows from the
active-execution caps: owner review, authorization, host setup, queue, and
failure/revision time are unbounded here" (measurement packet L31,
*confirmed*). The recorded operational posture is zero assumed residual until
reconciliation (register L349, *confirmed*), and the recorded offline input
bound already measured for the candidate packet is "Maximum 5,040 against the
8,000 ceiling; no provider call" (candidate summary L53, *confirmed* —
evidence from the candidate preparation, not a live measurement).

## 6. What nothing in this page authorizes

Explicit no-grant list. This page, and the pull request that adds it,
authorize **none** of the following:

- **No provider call, metadata request or judgment request.** "No allowance is
  renewed by candidate or offline-support delivery" (measurement packet L17).
- **No budget, spend or dollar authority.** No allowance is created, renewed,
  extended or reconciled here; the caps are quoted, not granted.
- **No private label approval.** The 160 candidates remain PENDING (register
  L233) and "Reading or accepting this public packet is not dataset approval"
  (measurement packet L9).
- **No live execution source selection.** The offline head and tree "identify
  reviewed offline code, **not** an approved live source" (measurement packet
  L16).
- **No host probe, host phase, or selected-host proof.** Stage A runs only
  under the already-merged APR-128/BER-DEC-016 grant and only after the owner
  fixes the host-phase ceiling; this page grants no host step, and Stage A or
  Stage B is not an R4/R5 live-host proof.
- **No holdout unseal and no OD-1 ratification.** OD-1 stays open (backlog
  L2139); "no retry-until-green, baseline-eligible semantic verdict, Scenario A
  live suite, or WP-2B-4 authorization follows" (measurement packet L21).
- **No WP-2B-4, WP-2B-5, WP-2B-6 or WP-2B-7 authorization**, and no promotion
  of the advisory CI lane.
- **No register, backlog or approval-register edit.** This page edits no
  governance record; see §7.
- **No deletion of anything** — not the paused VirtualBox VM, not the WSL2
  distribution. "DELETION — of the distro or the VirtualBox VM — ... requires
  the owner's separate approval plus operator confirmation (the owner's
  2026-10-10 rule, quoted)" (APR register L5478–L5480).
- **No new private-input access, credential use, dependency installation, or
  unsanctioned network step.**
- **No claim that previous work is already delivered.** WP-2B-3 is AUTHORIZED,
  not DONE, and its measured calibration remains undelivered. The delivered
  support increments recorded in the backlog are the offline synthetic-support
  increment (backlog L1092–L1112, delivered by PR #249 at `fa37c0e5`), the
  merged engineering corrections and recovery documentation from PR #88
  together with the shared contracts and permanent offline CI of PRs #90/#91
  (backlog L1081–L1085), BER-DEC-014 with the selected-precheck aggregate
  correction delivered by PR #374 (backlog L1122–L1135), and BER-DEC-015 with
  the non-executed-aggregate correction delivered by PR #535 (backlog
  L1146–L1161); WP-2B-3 itself stays AUTHORIZED, not DONE (backlog
  L1254–L1255).

## 7. Recording note

Any owner answer that must persist — for G1–G7, for the host ladder, or for any
downstream item — goes through its own separately reviewed governance pull
request, not through this page's pull request. The registers that would carry
it are the [BER backlog](behavioral-eval-runner-backlog.md) decision log
(BER-DEC entries), the [APPROVAL_REGISTER](../approvals/APPROVAL_REGISTER.md),
and the [open decisions
register](aegis-open-decisions-2026-09-23.md). This page's pull request is
docs-only, adds exactly one file, and edits none of them. The register rows
flagged as stale in §3 stay exactly as written until a separately authorized
register edit changes them.

A host-phase execution (a Stage A probe run, a Stage B run) is likewise not
part of this page or its pull request: those are host-phase actions under their
own grants (APR-128 for Stage A; the D94 record for Stage B), each with its own
receipts and its own evidence split. If this page were ever to quote the private
candidate contents, that would violate BER-DEC-010's public/execution evidence
separation (backlog L3587–L3595); it therefore quotes only opaque identities,
sanitized hashes and public line references.

## 8. Provenance and precision notes

- **Baseline:** prepared against `origin/main`
  `279338a938168843fabebff12acd30359a0fc414` (2026-10-11 14:54 -07:00).
  Post-2026-10-10 commits, including D94 (`b4e4c16b`) and the merged Stage A
  grant (BER-DEC-016 / APR-128, `b65bd3fc`), are ancestors of that baseline
  (*confirmed* by `git merge-base --is-ancestor`).
- **Plan audit:** the packet's plan was accepted with three named findings:
  F-1 (a file-level byte-identity sentence that is true only per cited line),
  F-2 (private-repository objects unresolvable from the public clone), F-3 (a
  parenthetical that grouped the platform decision with the probe grant). This
  page applies all three: it claims **per-cited-line** identity (§ top), marks
  private facts **UNVERIFIABLE-FROM-PUBLIC-CLONE** (G1, G2, G6), and splits the
  platform decision from the probe grant (§3).
- **Not re-derived:** the private candidate count (160) and the private commit
  `6beba11e…` are re-cited from the measurement packet and the sanitized
  checkpoint, not verified locally — the object is not in the public clone.
- **No fabricated figures:** no dollar price, spend projection, elapsed time or
  throughput number appears beyond the quoted caps and the recorded offline
  input bound.
- **No-grant posture verified:** every gate above carries a defer/stop option
  with a real cost, and every "does not authorize" item in §6 traces to a cited
  source line.

## 9. Sources

- [BER backlog and decision log](behavioral-eval-runner-backlog.md) — R1–R5
  (L393–L685), WP-2B-3 (L1072–L1232), WP-2B-4 (L1233–L1310), WP-2B-5/6/7
  (L1311–L1462), OD-1–OD-4 (L2139–L2184), BER-DEC-008 (L3364–L3485), BER-DEC-010
  (L3552+), BER-DEC-016 (L3974–L4048).
- [Open decisions register](aegis-open-decisions-2026-09-23.md) — BER rows
  L39–L42, "Still open for the owner" L224–L241, decision table L345–L352.
- [Measurement prerequisite decision
  packet](ber-wp2b3-measurement-prerequisite-decision-packet.md) — L5, L9,
  L15–L21, L27, L31.
- [Holdout execution scope proposal](ber-wp2b3-holdout-execution-scope.md) —
  the live execution proposal referenced by register L41.
- [Sanitized candidate checkpoint](../evidence/ber-replacement-candidate-1-summary.md)
  — L23–L31, L45–L54.
- [Offline holdout review](../evidence/ber-wp2b3-holdout-offline-review.md) —
  the delivered offline increment.
- [APPROVAL_REGISTER](../approvals/APPROVAL_REGISTER.md) — APR-009 (L402–L435),
  APR-126 (L5367–L5412), APR-127 (L5414–L5434), APR-128 (L5438–L5491).
- [Step-0 reconciliation v4](../reconciliation/step-0-reconciliation-v4.md) —
  D94 (L4406–L4434), D95 (L4436–L4454).
- [Selected-host capability decision](ber-selected-host-capability-decision.md),
  [WSL2 Stage A setup proposal](ber-wsl2-stage-a-setup-proposal.md),
  [VM setup record](ber-virtualbox-stage-a-setup-proposal.md),
  [authorization decision
  package](behavioral-eval-runner-wp-2b-3-authorization-decision-package.md),
  [BKL-009 evidence policy](ber-bkl-009-evidence-policy-decision.md),
  [BKL-009 residual cleanup
  proposal](ber-bkl-009-residual-host-runtime-privacy-cleanup-proposal.md),
  [replacement storage decision](ber-calibration-replacement-storage-decision.md).
