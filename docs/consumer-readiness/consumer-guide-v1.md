# Consumer guide (v1) — DRAFT

**Status: DRAFT — not delivered, not published as a consumer guide, not a
release, installation or support commitment.** This is the E4.2 consumer-guide
draft, committed to the source repository for E4 review. It stays DRAFT
until the delivery prerequisites in
[compatibility-matrix-v1](compatibility-matrix-v1.md) section 5 are met or
explicitly dispositioned, and until an independent E4.3 review is recorded.
Reading it does not authorise an install, a provider call, a publication or a
merge.

**Who should read it.** A reader deciding whether the current local Aegis
route is usable today, and an independent reviewer checking whether the guide
is honest about what is not proven. The guide is a review draft, not a
consumer publication; section 9 explains the metadata warning.

**Reading key.** **Role A** is the Project Aegis source repository; **Role B**
is your own consumer/product repository, which copies Aegis files into its
workspace. **J1** is the first consumer journey the starter package supports.
**UNRUN** means not executed and never a pass. **PR** is a pull request; **CI**
is continuous integration; **SHA** is a Git object identifier or a SHA-256
digest, named where it is used. **T2**, **T5**, **T6**, **T7** and **T9** are
owner decisions recorded in the programme records; their current states are
summarised in section 10.

## 1. At a glance

| Question | Honest answer today | Evidence |
| --- | --- | --- |
| Is there a documented install route? | Yes, a provisional local route for one measured Windows host, defined by the v2 starter package. It is not consumer readiness. | [Starter package](../consumer-starter-package.md); [local-starter-v2 evidence](../evidence/consumer-readiness/local-starter-v2.md) |
| Is any consumer mode or profile supported? | No. Every C4.1 profile cell is UNRUN and there are 0 QUALIFIED cells. | [Compatibility matrix](compatibility-matrix-v1.md) section 3; C4.1 record cited there |
| Can I see a supported status or recovery display? | No. The status display (E2.3) is not delivered, and status/recovery compatibility is UNRUN. | Matrix sections 2 and 4 |
| Is anything enforced? | No. Host-control assurance is NONE; repository-side records are AUDITABLE at most; mounted coverage is UNKNOWN; ENFORCED is blocked. | [Control boundary](../design/supported-controls-boundary.md); [host qualification](../design/host-qualification-disclosure.md) |
| Is the consumer proof accepted? | No. E3 item-2 is 18 PASS / 3 FAIL / 1 UNRUN of 22 and is not accepted; CP-09 FAIL stands for this attempt. | [Ledger v5](../evidence/aep3-item2-consumer-proof-20261029/CONSOLIDATED-CP-LEDGER-V5.md) |
| Is item-5 closed? | No. 05-D is MET on the owner-authorised private route; 05-G is NOT MET. No source link, no off-device custody. | Programme records cited in [support-claims-v1](support-claims-v1.md) |
| Is item-8 P3-08-01 proven? | No. The schema annotation is merged, but P3-08-01 remains UNRUN. | Programme record cited in the claims ledger |
| Are costs known? | No. Setup time, agent time, owner attention and dollar cost are UNKNOWN; the pilot had 0 eligible cases. | Section 8; C4.2 record cited in the claims ledger |

If any row above reads like a limitation rather than a feature, that is the
intended reading. The limitations are part of the guide, not fine print.

## 2. Prerequisites and entry path

### 2.1 One entry path, no second application

The only documented entry path is the existing consumer starter package
procedure, sections 6 to 9 of
[consumer-starter-package.md](../consumer-starter-package.md): record the host,
prove the target is a consumer repository, state the install mode and verify
the identity records, clone at the pinned commit, copy the allow-listed files,
verify the closure, and write the install record. There is no second
application, onboarding system, dashboard or installer. The E2 work that would
polish this path is not delivered; treat the current path as the E1-era route.

### 2.2 Prerequisites

These are observed on one measured Windows host. They are a checklist, not a
promise that another host behaves the same way. Every prerequisite is meant to
report MET, UNMET or UNKNOWN with a reason and a permitted next action; when it
cannot, the procedure refuses instead of guessing.

| Prerequisite | Why it is required | Current evidence |
| --- | --- | --- |
| Git 2.x with access to the source repository | The package is copied from a clone, and both identity checks use Git. | Measured: git 2.55.0.windows.5 |
| An LF checkout of the pinned commit | Every pin and the aggregate are computed over LF bytes; a CRLF checkout changes the bytes. | The repository pins LF; one host measured, no second host |
| A POSIX sh invoked by absolute path | The startup gate's presence and owner check are POSIX sh snippets; naming sh is not enough. | Measured absolute Git sh path on one host; a bare sh was absent |
| PowerShell 7 for the scripted procedure | The published harness is a script whose control flow is its exit codes. | Measured 7.6.6; PowerShell 5.1 was not used for the scripted route |
| A host coding agent that reads AGENTS.md / CLAUDE.md | The J1 journey runs in the host agent. | Measured with DeepSeek Harness (deepseek-flash); not the only possible host, but the only measured one |
| A git-initialised product repository (Role B) with a human owner | The install target; the owner record is local Git configuration. | One fixture repository; a fresh repository may have zero commits |
| Python, Node or any package manager | Not required by the consumer install. | Deliberately not used |

The full prerequisite discussion, including the measured host details, is in
[consumer-starter-package.md](../consumer-starter-package.md) section 6. The
guide does not repeat the host-verification commands; use the package page.

### 2.3 Before any write: owner record and install mode

The procedure requires an explicit install mode, stated by the owner:

| Install mode | What it means | What it does not mean |
| --- | --- | --- |
| human-only | The owner makes their own commits. The install makes no commit and changes no Git identity. | It is not a relaxed agent check and it does not prove who supplied the answer. |
| agent-commit | An agent will commit. The effective author and committer must be valid non-owner identities. | It does not grant publication, merge or provider authority. |

An invalid, empty, padded or unrecognised mode is refused (exit 43) after
normalisation and before any comparison or record. An agent-commit attempt
under the owner identity is refused (exit 42). The selected mode is written to
the install record; the record is evidence of identity, not a signature.

### 2.4 Host scope

The measured evidence is one Windows 11 host, one OS build and one consumer
fixture. macOS and Linux are unvalidated and the package claims nothing there.
A second Windows host is UNRUN. A hosted CI run is not a substitute for native
evidence.

## 3. Modes, profiles and capabilities

### 3.1 Operating modes

The plan names three operating modes. They describe the consumer's operating
shape, not an assurance level.

| Mode | Meaning | Current support state | What is actually evidenced |
| --- | --- | --- | --- |
| A | Single agent, no subagents, no inbox | **UNRUN** | Bounded install evidence on one host; no C4.1 real-host cell; no E2.4 exercise |
| B | One platform with optional subagents | **UNRUN** | No provider authority and no exercise; a provider call needs separate authority and spend approval |
| C | Multiple platforms with a bounded handoff | **UNRUN** | No multi-platform proof; a qualification slice would need retained evidence and separate authority |

The simplest no-inbox configuration is Mode A with the inbox explicitly
disabled. Its zero-activity property is UNRUN: a static configuration is not
enough; an end-to-end disabled run plus independent confirmation is required.

### 3.2 Install modes versus operating modes

Do not conflate the two axes. Human-only and agent-commit are install-time
identity choices. Modes A, B and C are operating shapes. Neither axis grants
authority or support.

### 3.3 Capabilities

| Capability | Current state | Evidence and limitation |
| --- | --- | --- |
| Copy the fixed starter package | Available as a documented, bounded local route | 41 files / 18 skills; one host; J1 only |
| Explicit mode selection and refusal | Implemented in the published procedure | Exit 42/43; the mode is an owner statement, not a verified identity |
| Destination-link containment | Implemented for the inspected, quiescent tree | Directory junctions exercised; file and directory symbolic links and other reparse tags UNRUN; race not detectable |
| Install-record atomic write | Implemented | Exit 25; a partial receipt is not left at the record path |
| Status display | Not delivered | E2.3 and E4.1 status compatibility UNRUN |
| Recovery display | Not delivered | E1.4/E1.5 evidence exists, but the consumer display is UNRUN |
| Optional subagents or providers | Optional only | No exercise and no provider authority; never required |
| Optional inbox | Optional only | Disabled zero activity is UNRUN; enabled inbox is out of scope |
| Verdict/readiness checker | Auditable tooling only | Read-only; not enforcement; not a required context; production readiness blocked by T6 |
| Change-state producers | Auditable tooling only | 87 tests; no real record committed; provenance UNVERIFIED (T24) |
| Operations tooling | Auditable tooling only | Read-only validation of supplied facts across seven record families; real settlements, inbox runs and pilot cases UNRUN |
| Host enforcement | Not available | NONE for host controls; AUDITABLE at most for repository-side records; ENFORCED blocked |

### 3.4 Optional components and no staffing prerequisite

Subagents, additional providers and the inbox are optional. Single-agent
operation remains useful and carries the same honest assurance limits. There
is no Nemesis dependency, no mandatory additional vendor or subscription, and
no mandatory extra staffing. Missing mandatory independent approval stays
BLOCKED and is not replaced by CI, a green check, a label or a merge.

## 4. Assurance classes: what the labels mean

| Label | Meaning | What it does not mean |
| --- | --- | --- |
| VERIFIED | Re-derived in the pass from a cited primary source | It does not mean independent review or acceptance |
| REPORTED | Asserted by a named record, not re-derived in this pass | It does not become VERIFIED by repetition |
| UNKNOWN | Not derivable from the available evidence | It does not mean "probably fine"; the resolver must be named |
| UNRUN | Not executed | It is never a pass, a partial pass or a simulated result |
| FAIL | Executed and failed | It stands; a later attempt needs new evidence, not a softer label |
| AUDITABLE | Records and commands can be audited after the fact; nothing is prevented | It is not enforcement or custody |
| NONE | No assurance asserted | It is the default for host controls |
| ENFORCED | The control provably prevents the action with proved custody and mounted coverage | **Blocked**: it cannot be claimed today |

The local, hosted and independent distinctions are kept separate. A local
install record is not hosted evidence, a hosted CI run is not native
verification, and self-review is not independent review. No aggregate green or
score exists; counts must keep their denominator, and a recorded bypass is
displayed as a bypass.

## 5. Named UNRUNs, FAILs and limitations

This section names the limitations a consumer or reviewer is most likely to
misread. The full claim-to-evidence binding is in
[support-claims-v1](support-claims-v1.md).

### 5.1 E1 and the starter package

- The v2 starter was installed on one measured Windows host; that is bounded
  local evidence, not consumer readiness, hosted readiness or J1 acceptance.
- The E1.4 and E1.5 current-head records are PROPOSED evidence records, not
  acceptance or E1 closure. Their unexecuted rows (second host, macOS, Linux,
  file and directory symbolic links, other reparse tags, some exit-code
  branches) are UNRUN.
- E1.6 integrated verification is UNRUN. T12 and T13 closures are owner-held
  and UNRUN. E1.2 and E1.3 closure is also UNRUN and owner-held.
- No E1 closure is claimed anywhere in this guide.

### 5.2 E3 item-2: not accepted

E3 item-2 is **18 PASS / 3 FAIL / 1 UNRUN / 0 BLOCKED**, denominator 22. The
three FAILs are CP-03, CP-09 and CP-19; CP-17 is the UNRUN. CP-22 PASS is
matrix/closeout integrity only, not 22/22 acceptance. CP-09 is permanent for
this attempt: a public consumer commit metadata breach stands, and prevention
is the only remedy. The structural ceiling for this attempt is 21/22; full
22/22 would require a new consumer-proof attempt under separate authority. The
current attempt is **not accepted**, item-2 remains open, and no E3 closure or
E4 conformance claim follows from it.

### 5.3 Item-5: 05-D MET, 05-G NOT MET

The private preservation export contains 78 files / 310,293 B and was
independently retrieved (05-D MET on the owner-authorised private-destination
route). **05-G is NOT MET**: no authorised source-documentation link to the
verified export and retrieval report exists, and the source-doc change needs
T21 plus independent review and merge. The destination is on the same local
volume as the source: no off-device replication, independent backup or restore
test is evidenced. Do not describe item-5 as closed, durable, source-linked,
publication-classified or independently retrievable in the publication sense.

### 5.4 Item-8: P3-08-01 UNRUN

The schema annotation change merged, and the hosted evidence was captured, but
P3-08-01 remains **UNRUN**. It is not accepted, not closed and not a pass. Do
not cite the merged annotation as proof of P3-08-01.

### 5.5 C1, C2, C3 and C4

- C1.1a: a read-only checker exists and is auditable. It is not enforcement,
  not a required context, and production readiness is unreachable while T6 is
  UNVERIFIED+BLOCKED.
- C1.2-C1.4: producer/format/validator tooling exists (87 tests), but no real
  change-state record is committed and store provenance is UNVERIFIED (T24).
  The C1.3 host-side row is UNRUN. C1.4 qualification is UNRUN.
- C1.1b: Stage 1/2 is merged, but aegis-verdict-gate is **NOT WIRED** as a
  required context; Stage 3 is blocked on T4/T6/T24/T7.
- C2: the preflight/evidence-reuse policy and tooling are merged; no real
  evidence-reuse record is claimed.
- C3: the operations tooling is auditable and synthetic-only; real
  settlements, stage records, inbox runs, reviewer replacements and pilot
  cases are UNRUN.
- C4.1: six configurations, 0 QUALIFIED cells, all UNRUN; simulated hosts are
  not counted and T5 mounted coverage is not assumed.
- C4.2: 0 of 5 eligible pilot arrivals; the result is a bounded shortfall, not
  a five-case result. No rate, saving, dollar or hours claim.
- C4.3: independent review is UNRUN; no reviewer is named.

### 5.6 Open owner decisions and other limits

- T2 design basis is open: no contract conformance and no accepted version.
- T5 mounted coverage is not assumed: no enforcement or coverage claim.
- T6 authentication is UNVERIFIED+BLOCKED: production readiness is unreachable.
- T7 exception/unavailable-review authority is open: real dispositions are
  blocked.
- T9 grants docs-only implementation, not publication, release, install or
  deployment.
- The display mapping version cs-map/1 is a candidate; Q7 is open.
- Accessibility is proposed as WCAG 2.2 AA and has not been exercised; no
  accessibility conformance claim is made.
- The measured route is Windows-only; macOS, Linux and a second Windows host
  are UNRUN.

## 6. Recovery and refusal

### 6.1 Install refusal codes

The published procedure stops at a refusal; it does not warn and continue.
These codes are from
[consumer-starter-package.md](../consumer-starter-package.md) section 7.2.

| Code | Meaning | What to do next |
| --- | --- | --- |
| 1 | Prerequisite failure: no Git sh, missing source/target, or sh did not answer | Fix the prerequisite; nothing was written |
| 20 | Foreign material in a destination skill directory | Remove or relocate the foreign file; nothing was overwritten |
| 21 | Unsafe or missing source path | Inspect the path; nothing was written |
| 22 | Startup-file conflict | Reconcile the differing file; existing bytes are unchanged |
| 23 | Unsafe destination path: junction, symbolic link or other reparse point | Do not follow it; choose a plain path; refused before package or record writes |
| 24 | Install-record path cannot be used | Use a new regular-file path; an existing record is not overwritten |
| 25 | Install record could not be written atomically | The package copy may be complete but no record was written; fix the record path and resume deliberately |
| 30 | Closure, count or eval-material failure | Inspect the named path or count; do not edit pins to make it pass |
| 31 | Pin or byte mismatch, including a CRLF checkout | Restore an LF checkout at the pinned commit; do not normalise the pins |
| 32 | Missing sibling dependency | Install or restore the named sibling; do not improvise a substitute |
| 40 | Wrong repository role | You are not in the intended Role B target; stop and re-check |
| 41 | Owner record missing | Record the owner in local Git configuration as documented |
| 42 | Commit identity missing or owner-matching on agent-commit | Use a valid non-owner agent identity; do not bypass the check |
| 43 | Install mode or owner authorization not stated, empty or unrecognised | State human-only or agent-commit explicitly; nothing was written |

### 6.2 Recovery rules

- An identical rerun must be distinguishable from the initial run. Do not
  describe a rerun as a first install.
- An existing install record is refused, not overwritten. If you need a new
  receipt, choose a new record path or use the documented resume switch
  deliberately.
- Interruption is recoverable without inventing history: record the exact
  command, exit code, message and the state it left behind.
- A failed or partial result is evidence. A softened retelling is not.
- Do not repair a failed check by editing a pin, a selector row, a frozen
  constant or a historical record.

### 6.3 Status and recovery display

The shared consumer labels are **frozen**, **awaiting review**, **budget
exhausted**, **blocked**, **residual accepted** and **evidence reused**, with
presentation extensions **no-candidate**, **suspended**, **ready-for-gate** and
**closed/parked**, and overlays **stale**, **invalidated**, **unknown**,
**bypass-recorded** and **enforcement NONE**. These are presentation labels
derived from contract states; they are not separate guarantees.

Today there is **no implemented consumer status display**. The E2.3 surface is
not delivered, and the E4.1 compatibility cells for status and recovery are
UNRUN. Until a display exists and is independently reviewed, read the
authoritative records directly and do not treat a badge, a SHA-bearing
comment, a fix commit, green CI, a label or a merge as approval.

Every state must show exactly one permitted next action with its actor,
authority, precondition and reference, or "none" with the responsible
authority. The UI may display, copy or link; it may not create, clear, advance,
suspend or reopen a state, and it may not approve, merge, waive, accept risk or
clear a block.

### 6.4 If you are blocked

A missing mandatory independent approval is displayed as BLOCKED. CI, an
automated review, a label or a green head is an input, not an approval. Do not
substitute a self-review or a weaker check. Find the authoritative record that
names the unmet condition and the authority that can unblock it; if that
authority is UNKNOWN, say so and stop.

## 7. Support matrix (summary)

This is a summary only; the per-cell evidence and limitations are in
[compatibility-matrix-v1](compatibility-matrix-v1.md).

| Mode / configuration | Support state | C4.1 cell | What you can rely on |
| --- | --- | --- | --- |
| Mode A, single agent, no inbox | **UNRUN** | UNRUN | Only the bounded local install route described above; no consumer support |
| Mode A, inbox disabled | **UNRUN** | UNRUN | A static setting is not evidence; zero-activity run is required |
| Mode B, one platform, optional subagents | **UNRUN** | UNRUN | Optional components only; no exercise, no provider authority |
| Mode C, multiple platforms | **UNRUN** | UNRUN | Nothing; no multi-platform proof |
| Selected inbox when authorised | **UNRUN** | UNRUN | Nothing; out of scope |
| Recovery/status states | **UNRUN** | UNRUN | Read the authoritative records directly; no display |
| macOS / Linux | **UNRUN** | No cell | Nothing; Windows-only evidence |
| Hosted/remote route | **UNRUN** | No cell | Nothing; T5 not assumed |

**No consumer profile is supported.** The only SUPPORTED statements in the
matrix are narrow tooling-surface statements about existing artifacts, not
statements about a consumer's mode.

## 8. Costs and burden

| Cost or burden | State | Source and boundary |
| --- | --- | --- |
| Setup time on your host | **UNKNOWN** | No measured consumer setup duration; lane-day estimates are engineering ranges, not consumer cost |
| Agent time | **UNKNOWN** | Not instrumented; the pilot had no eligible cases |
| Owner attention and review waits | **UNKNOWN** | Not separable or measured; the work includes real review waits |
| Dollar cost | **UNKNOWN** | No measured invoice or spend; do not infer one from lane-days |
| Ongoing maintenance | **UNKNOWN** | No longitudinal evidence |
| Mandatory vendor or subscription | **NONE** | Subagents, additional providers and the inbox are optional |

The qualitative burden is real: the route has prerequisites, several manual
steps, a host-agent dependency and review waits. C4.2 measured 0 of 5 eligible
arrivals, so there is no rate, saving, dollar, hours-to-delay or
programme-completion figure to quote. Do not convert a lane-day estimate into
a dollar or calendar promise.

## 9. Metadata and publication warning

**Do not republish this guide, or a derivative, as consumer-facing
documentation.** It is a review draft. It contains programme PR numbers,
internal record identifiers and role identities that must not be copied into
public commit or artifact metadata. Requirement R8 says public commit or artifact metadata must
not carry plan-forbidden product names, PR numbers or personal names. The
audience decision Q3 is open, T9 publication authority is not granted, and the
guide is DRAFT. Before any publication, run a metadata-minimisation pass that
removes or replaces those classes and record the audience and channel.

This is not a hypothetical risk. The E3 item-2 CP-09 FAIL is exactly a public
consumer commit metadata breach involving plan-forbidden names and a personal
name; it stands for that attempt and cannot be repaired retroactively.

## 10. What would change this guide

| Prerequisite or decision | Current state | Owner | Effect on this guide |
| --- | --- | --- | --- |
| E3 exit / T15 item-2 | 18/3/1, not accepted | Owner (T15-T19) | Keeps the FAIL/UNRUN limitations; no 22/22 |
| C4.1 support matrix | Evidence-only, 0 qualified | C4/C3 owner | All profile cells stay UNRUN |
| C4.2 pilot | 0/5, bounded shortfall | C4 owner | No economics |
| C4.3 independent review | UNRUN | Lead / AUTH-REVIEWERS | No independent C4.3 verdict |
| T2 design basis | Open | Owner | No conformance or accepted version |
| T5 mounted coverage | Not assumed | Owner | No enforcement claim |
| T6 authentication | UNVERIFIED+BLOCKED | Owner | Production readiness unreachable |
| T7 exception authority | Open | Owner | Real unavailable-review dispositions blocked |
| T9 publication authority | Docs-only implementation; no publication | Owner / Lead | Guide stays DRAFT; no publication |
| Q3 audience / Q7 mapping / Q8 assurance vocabulary | Open | Owner | Review-scoped; cs-map/1 candidate; no accepted assurance vocabulary |
| E1.6, T12/T13 | UNRUN | Owner | No E1 closure |
| E2.3 / E2.4 | Not delivered / UNRUN | Experience lane | E2-dependent content provisional |
| E4.3 independent review | UNRUN, no reviewer | Lead / owner | No review verdict |

## 11. Evidence index and non-claims

The full evidence index, with bytes and SHA-256 for every cited record and its
retention status, is in [support-claims-v1](support-claims-v1.md). The main
repository sources used here are:

- [consumer-starter-package.md](../consumer-starter-package.md)
- [local-starter-v2.md](../evidence/consumer-readiness/local-starter-v2.md)
- [local-starter-transition-current-head-v1.md](../evidence/consumer-readiness/local-starter-transition-current-head-v1.md)
- [destination-links-support-matrix-v1.md](../evidence/consumer-readiness/destination-links-support-matrix-v1.md)
- [CONSOLIDATED-CP-LEDGER-V5.md](../evidence/aep3-item2-consumer-proof-20261029/CONSOLIDATED-CP-LEDGER-V5.md)
- [supported-controls-boundary.md](../design/supported-controls-boundary.md)
- [host-qualification-disclosure.md](../design/host-qualification-disclosure.md)
- [change-state README](../approvals/change-state/README.md)
- [aegis_change_state README](../../tools/aegis_change_state/README.md)
- [aegis_verdict_gate README](../../scripts/aegis_verdict_gate/README.md)
- [aegis_ops README](../../tools/aegis_ops/README.md)
- [qualification-and-pilot-metrics.md](../operations/qualification-and-pilot-metrics.md)

**Non-claims.** This guide does not claim consumer readiness, production
readiness, contract conformance, enforcement, mounted coverage, custody,
delivery, installation, release, deployment or publication. It does not claim
E1/E3/E4 closure, item-2 acceptance, 22/22, item-5 closure, item-8 P3-08-01
acceptance, or any supported consumer profile. It does not convert UNRUN or
UNKNOWN to PASS. It does not authorise a provider call, host action, settings
change or merge.

## 12. E4 acceptance-criteria coverage (for reviewers)

| Criterion | Where this guide covers it |
| --- | --- |
| E4-AC5 guide coverage and honesty | Sections 2 (prerequisites/entry), 3 (modes/capabilities), 4 (assurance), 5 (named UNRUNs/FAILs), 6 (recovery), 7 (support matrix), 8 (costs), 9 (metadata), 3.4 (optional/no Nemesis) |
| E4-AC6 claims ledger binding | [support-claims-v1](support-claims-v1.md), one evidence identity per claim |
| E4-AC8 metadata/audience constraints | Section 9; review-scoped marking; no personal names in these pages |
| E4-AC10 no delivery/publication overclaim | Status block, section 11 non-claims, section 10 prerequisites |
| E4-AC7 evidence index and retention honesty | Evidence index in [support-claims-v1](support-claims-v1.md); local-only records named as not repo-durable |
| E4-AC1/AC2/AC3/AC4 compatibility and prerequisites | [compatibility-matrix-v1](compatibility-matrix-v1.md) sections 1-5 |
| E4-AC9 independent final review | E4.3 request (programme record, not in this repository) — a request, not a verdict |
| E4-AC11/AC12 scope confinement and exact-head evidence | PR body and the E4.3 request; the diff is the three new consumer-readiness pages |
