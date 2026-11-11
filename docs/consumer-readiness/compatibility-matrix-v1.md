# E4.1 compatibility matrix (v1) — DRAFT

**Status: DRAFT, review-scoped.** This page is a compatibility
record for the E4 docs/evidence slice, committed to the source repository for
E4 review; it is not a consumer publication. It is not a qualification report, not a
support statement, not a contract-conformance claim, not a delivery,
publication, release or install claim, and not an enforcement claim. No cell in
this page is a pass or a green result. It contains programme PR numbers,
internal record names and role identities; read the metadata warning in
section 9 before republishing anything derived from it.

**What this page is for.** It records, for each consumer mode/profile and for
the status, recovery and assurance vocabulary, what the merged repository
artifacts and the C4.1 evidence can and cannot support at the exact base
commit. It consumes the contract, the presentation design and the C4.1 matrix
**by identity**; it does not restate or re-encode their field lists or
semantics.

**Base identity for every repository citation.** Base origin/main
c5fe3adf7b64f3f583bd6ee12591afe36176d2da, tree
9d7f214c63d78721c463d972336dc1bacf0ba514 (2026-11-11T11:43:41-08:00,
merge of PR #1024). Programme records are outside this repository and are
local-only; their bytes and SHA-256 are cited, not copied.

**Cell states used here.**

| State | Meaning in this matrix |
| --- | --- |
| **SUPPORTED** | The named **artifact or interface** exists at the exact base and its own recorded checks pass. This is a narrow tooling-surface statement only. It never means a consumer profile works, a host is qualified, a contract conforms, or delivery is authorised. |
| **UNRUN** | The compatibility check or operation was not executed. The exact remaining action is named. UNRUN is never a pass. |
| **UNKNOWN** | The value is not derivable from the available evidence. The gap and its resolver are named. |

No cell state is PASS, green, qualified or ready. A cell sum would be meaningless
and is deliberately not provided.

## 1. Evidence inputs

Every row below is an input to a cell, not a claim that the input is
sufficient. "Repo" means the file is committed at the base commit; "programme"
means the record lives in the private programme records area outside this
repository.

| ID | Evidence | Identity | Retention |
| --- | --- | --- | --- |
| E-01 | Base commit / tree | c5fe3adf7b64f3f583bd6ee12591afe36176d2da / 9d7f214c63d78721c463d972336dc1bacf0ba514 | Repo; durable while history exists |
| E-02 | E4 implementation authority | E2-E4-IMPLEMENTATION-AUTHORITY-2026-11-11.md, 1,815 B / SHA-256 c96eb16aaec39bbcf7be6d4d1e1174206200a8a1f49a9379c54241b308ac6401 | Programme; local-only |
| E-03 | E2/E4 Stage A plan | E2-E4-STAGE-A-PLAN-DRAFT-2026-11-11.md, 55,297 B / SHA-256 84c41f7ee9ce4a7b26230e82cd4e178925802274d6f66c26284f3ec1cc9cccab | Programme; local-only |
| E-04 | E2/E4 Stage A capture | E2-E4-STAGE-A-CAPTURE-2026-11-11.md, 1,047 B / SHA-256 94812fd32e9aae89ae7441e7141052f43c31982f360aacb741bdb898a0d3b1da | Programme; local-only |
| E-05 | E2/E4 Stage B plan audit | E2-E4-STAGE-B-PLAN-AUDIT-2026-11-11.md, 20,719 B / SHA-256 a11b572ea24aac496d0c8e6ca3bc1afad181b2c1e977c10fd9152633de703448 | Programme; local-only |
| E-06 | Owner Fast Lane B authorization | FAST-LANE-B-AUTHORIZATION-2026-11-11.md, 796 B / SHA-256 ea40f503bf86a4d78389fb788852ba20a513764a6786876cb08c56fe4d8d6bdc | Programme; local-only |
| E-07 | C4.1 support matrix | C4-1-SUPPORT-MATRIX-2026-11-11.md, 2,095 B / SHA-256 30cb6bf933afa494d9f067caf4c8f5279aea0a82d833ac7bef306d58e87a056b | Programme; local-only |
| E-08 | C4.1 schema / validator | [tools/aegis_ops/schema.py](../../tools/aegis_ops/schema.py), 9,881 B / b1522046c688a6aa24f31a25e26696fcdcffc0fbbf67d3018f513e09edd0cb15; [pilot_metrics.py](../../tools/aegis_ops/pilot_metrics.py), 16,898 B / 1310b744170f83ddf54dac77c734f05c379876fbaf681011969072a2d0073795 | Repo |
| E-09 | C1.1a checker README | [scripts/aegis_verdict_gate/README.md](../../scripts/aegis_verdict_gate/README.md), 15,651 B / 8581b08754cfc34fa58ca9d6199248afdcda54ebfb7ad84b5af2560c3f5e6393 | Repo |
| E-10 | C1.1a field catalogue | [scripts/aegis_verdict_gate/catalogue.py](../../scripts/aegis_verdict_gate/catalogue.py), 11,441 B / e1ac14428be258f2a9e43fc0aea7335afd3f4d7caf544d38397b72cf3c6364ea | Repo |
| E-11 | C1.2-C1.4 change-state format | [docs/approvals/change-state/README.md](../approvals/change-state/README.md), 14,306 B / 883f973734e0f7a7108accffad57d08b5ab22ca8bbda99785f348a9a3dd2e71d | Repo |
| E-12 | C1.2-C1.4 producer tool | [tools/aegis_change_state/README.md](../../tools/aegis_change_state/README.md), 8,221 B / 1a5f024207bc5d8e534dda9568985dfd1415d52cb04593cf52975053a3154ddd | Repo |
| E-13 | C1.4 control boundary | [docs/design/supported-controls-boundary.md](../design/supported-controls-boundary.md), 6,755 B / 19d8d181e13e6588f007733f8a5b4ed92d508815a9054700b5b3c56a0e2dcfdd | Repo |
| E-14 | C1.4 host qualification disclosure | [docs/design/host-qualification-disclosure.md](../design/host-qualification-disclosure.md), 4,512 B / 568e084e282fc17f5a61125de48cb175701386d9fade25f225b6a22876947a82 | Repo |
| E-15 | C1.1b gate workflow (not wired) | [.github/workflows/aegis-verdict-gate.yml](../../.github/workflows/aegis-verdict-gate.yml), 9,468 B / e5ac3edfd4bf2f0d2517e821c6d51a703ef66cf29e05ac46ea80abe3be487c54; [docs/delivery-workflow.md](../delivery-workflow.md) records aegis-verdict-gate as **NOT WIRED** | Repo |
| E-16 | C2 evidence-reuse schema | [docs/conformance/evidence-reuse-v1.schema.json](../conformance/evidence-reuse-v1.schema.json), 11,850 B / b16d5e45dc2eec3ab58ce2cd2f35b372619c8472da3b132e62fd4b41b7d00f0f | Repo |
| E-17 | C3 operations guide | [docs/operations/README.md](../operations/README.md), 3,205 B / a69baf16ca5281ae212f0cf85bb2d4736908ee1d69a4f20dacda50477f111159 | Repo |
| E-18 | C3/C4 tooling README | [tools/aegis_ops/README.md](../../tools/aegis_ops/README.md), 3,480 B / eafbd730f33e4b444a952cf71d2527fac7d4bac9619e7a9cea0e78b0450f7add | Repo |
| E-19 | C4 qualification page | [docs/operations/qualification-and-pilot-metrics.md](../operations/qualification-and-pilot-metrics.md), 4,895 B / 9e9db216c4c6d8c65155e7019738bbdc1ebab0bb318cd2cebf9856bbb1e71df4 | Repo |
| E-20 | C4.2 pilot final | C4-2-PILOT-FINAL-2026-11-11.md, 1,093 B / SHA-256 76c121c807531907be04805f676df9f6336195ace72d30d34d0cdb42aa937511 | Programme; local-only |
| E-21 | C4.3 review request | C4-3-INDEPENDENT-REVIEW-REQUEST-2026-11-11.md, 2,369 B / SHA-256 a3f92a64e87f3cd1dd5c8292a96ac4adfd4b28fe2efaac04473130f920dce07d | Programme; local-only |
| E-22 | E3 item-2 ledger v5 | [docs/evidence/aep3-item2-consumer-proof-20261029/CONSOLIDATED-CP-LEDGER-V5.md](../evidence/aep3-item2-consumer-proof-20261029/CONSOLIDATED-CP-LEDGER-V5.md), 5,775 B / a95086648d020a008fe4377606c063127458241bd912a32c2c887b343162a092 | Repo |
| E-23 | E3 item-2 bounded outcome | E3-ITEM2-BOUNDED-PROOF-OUTCOME-2026-11-11.md, 1,501 B / SHA-256 656b8a8a001d8e96ad3521acd3633f9b5d3787fec8114da015d5aaf7b73e9ea2 | Programme; local-only |
| E-24 | Item-5 export receipt | ITEM5-EXPORT-RECEIPT-2026-11-11.md, 21,491 B / SHA-256 c8d3250e8a03da34774490271558d1010738d5a615e2fd7e0cc65d3614b6e02e | Programme; local-only |
| E-25 | Item-5 retrieval receipt | ITEM5-RETRIEVAL-RECEIPT-2026-11-11.md, 12,503 B / SHA-256 93f432f2de6109e028b700d71d32b2b89b37c7356392478f13c0d2b837428a65 | Programme; local-only |
| E-26 | Item-8 Stage E evidence | E1-ITEM8-STAGE-E-EVIDENCE-2026-11-11.md, 13,318 B / SHA-256 b7f0ca204709d8a89d36288e243489f59ab087f1e0d6a1047aee6684c9bf7d6e | Programme; local-only |
| E-27 | E2/E4 presentation design | E2-E4-STATUS-PRESENTATION-DESIGN-2026-11-10.md, 59,936 B / SHA-256 4a878d2599bf578c72a2879fe465c404655d79816f2bfa59e23a5974e421fa88 | Programme; local-only |
| E-28 | Implementation wave status | IMPLEMENTATION-WAVE-STATUS-2026-11-11.md, 5,917 B / SHA-256 dd87b20c388d0108477d0c73946564d35aadb2bb873339ee2c58e5a644d88fd9 | Programme; local-only |

Every programme record above is private, local-only and **not repo-durable**:
host loss would remove it, and it is not independently retrievable in the sense
required for a publication-class claim. Evidence is cited, not copied.

## 2. Version pinning (E4-AC2)

The versions below are pinned by identity. Their field lists and semantics are
owned by the cited sources and are **not restated here**. A version label is
not an acceptance: T2 (design-basis acceptance) is open.

| Item | Pinned identity | State | Source and boundary |
| --- | --- | --- | --- |
| Consumer contract schema | aegis.capability-status/v2 | **UNKNOWN** | PROPOSED; T2 open; not encoded in this repository. The plan consumes it by reference. |
| Bound verdict set | aegis.verdict-bound/v2.1 (C03-M1 delta as corrected by the v2.1 errata) | **SUPPORTED** (tooling identity) | The merged checker's single in-code projection is [catalogue.py](../../scripts/aegis_verdict_gate/catalogue.py), 62 entries; [README](../../scripts/aegis_verdict_gate/README.md) records the 560-byte canonical self-test vector 098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d. T2 still owns the design basis. |
| Display mapping | cs-map/1 (candidate) | **UNKNOWN** | Q7 open; no in-repository implementation; the presentation design is a design input, not an accepted mapping version. |
| Six consumer labels | frozen; awaiting review; budget exhausted; blocked; residual accepted; evidence reused | **SUPPORTED** (label names only) | Names are pinned by plan L342 and the presentation design (E-27). Semantics are contract-owned. The label-to-state display is UNRUN (SC-4). |
| Extension labels | no-candidate; suspended; ready-for-gate; closed/parked | **UNKNOWN** | Derived presentation labels; contract encoding is open (Q1). They are not separate contractual guarantees. |
| Overlays | stale; invalidated; unknown; bypass-recorded; enforcement NONE | **UNRUN** | Display obligations exist in the design; no display was implemented or exercised. |
| Review-head budget | v2.1 exclusive previously-published count; exception required iff used >= 3; resync/fix heads count; rename/agent/restart does not reset | **SUPPORTED** (checker semantics) | Checker README and catalogue; the display of the two budgets is UNRUN (SC-11, SC-12). |
| Plan-revision count | separate per-item count (APR-139(i)) | **SUPPORTED** (semantics) | Contract/policy by reference; no display implemented. |

**No-restatement check.** This page names version labels and presentation
labels only. It does not enumerate the contract's canonical fields and does
not define a second field list. The only in-code field projection is the merged
catalogue.py; a future page that copies the field sequence would be a defect,
not a compatibility improvement.

## 3. Mode and profile cells (E4-AC1)

The plan's modes are **A** (single agent without subagents), **B** (one
platform with subagents) and **C** (multiple platforms, bounded handoff). The
simplest no-inbox configuration is Mode A with the inbox explicitly disabled.
"Install mode" (human-only versus agent-commit) is a different axis and is
covered in the guide.

C4.1 records six configurations and **zero QUALIFIED cells**; every available
path is UNRUN, simulated_host_counted is false and T5 mounted coverage is
NOT_ASSUMED. No profile is therefore supported.

| Cell | Profile / configuration | State | C4.1 evidence | C1/C3 evidence | Limitation and remaining action |
| --- | --- | --- | --- | --- | --- |
| MP-1 | Mode A: single agent, no subagents, no inbox | **UNRUN** | E-07, row "mode A one-agent/no-inbox": UNRUN | E-09/E-10 (status tooling), E-17/E-18 (ops tooling; auditable only) | No real-host exercise and no E2.4 exercise. Run C4.1 real-host cells and the E2.4 matrix under authority. |
| MP-2 | Mode A: inbox explicitly disabled, zero associated activity | **UNRUN** | E-07, row "inbox-disabled zero activity": UNRUN | E-17/E-18, aegis.ops-inbox/v1; synthetic fixtures only | A static config is insufficient; an end-to-end disabled run plus independent confirmation is required. |
| MP-3 | Mode B: one platform with optional subagents | **UNRUN** | E-07, row "optional subagent": UNRUN | E-17/E-18 (no provider action) | No provider authority and no exercise; a provider call would need separate authority and spend approval. |
| MP-4 | Mode C: multiple platforms, bounded real handoff | **UNRUN** | E-07, row "bounded real multi-platform handoff": UNRUN | E-17/E-18 | No multi-platform proof; qualification needs retained evidence and a separate authority line. |
| MP-5 | Selected inbox when authorised | **UNRUN** | E-07, row "selected inbox when authorised": UNRUN | E-17/E-18 | Enabled inbox is out of scope; separate authority required. |
| MP-6 | Recovery and status states on a real change | **UNRUN** | E-07, row "recovery/status states": UNRUN | E-09/E-10/E-11/E-12 (formats and producers) | No durable real record and no display; synthetic fixtures are not evidence of operation. |
| MP-7 | Hosted or remote route (hosted CI, remote execution) | **UNRUN** | No C4.1 row qualifies a hosted/remote route | E-13/E-14: mounted coverage UNKNOWN; repo-side records AUDITABLE at most | T5 is not assumed; a hosted run is not a substitute for native evidence. |
| MP-8 | macOS or Linux native route | **UNRUN** | No C4.1 cell; E1 evidence is Windows-only | E-13/E-14 | No host exists for this programme; the starter package claims nothing there. |

**Profile conclusion.** There is no supported consumer profile and no
qualified mode. The only truthful profile statement today is: the local
Windows route has bounded install evidence on one host; all other profiles are
UNRUN.

## 4. Status, recovery and assurance cells (E4-AC3)

This table checks the labels and versions against the available C4.1/C1/C3
evidence. A SUPPORTED row means the named definition or tooling artifact
exists; it does not mean a consumer can see it, and it never means a verdict,
approval or enforcement.

| Cell | Compatibility item | State | Evidence | Limitation and remaining action |
| --- | --- | --- | --- | --- |
| SC-1 | aegis.verdict-bound/v2.1 is the single in-code verdict vocabulary | **SUPPORTED** (tooling) | E-09/E-10; 62 catalogue entries; 560-byte canonical vector | The design basis T2 is open; no conformance claim. |
| SC-2 | aegis.capability-status/v2 contract schema identity | **UNKNOWN** | E-03/E-27; not in repo | PROPOSED and not accepted; no encoding to check. |
| SC-3 | cs-map/1 display mapping identity | **UNKNOWN** | E-27; candidate only | Q7 open; no implementation. |
| SC-4 | Six consumer labels mapped to contract states | **UNRUN** | E-27 crosswalk; no E2.3 display | E2.3 not delivered; the design is not an exercised display. |
| SC-5 | Extension labels encoded by the contract | **UNKNOWN** | E-27 section 4; Q1 open | Derived labels only; C0 encoding decision required. |
| SC-6 | Recovery labels mapped to durable freeze/settlement/stage records | **UNRUN** | E-11/E-12; synthetic fixtures only | No real change-state record exists; provenance is UNVERIFIED (T24). |
| SC-7 | Assurance vocabulary: VERIFIED, REPORTED, UNKNOWN, UNRUN, FAIL | **SUPPORTED** (definitions) | E-09, E-13, E-14, E-22 | The definitions exist; the display mapping is UNRUN. No aggregate green. |
| SC-8 | Local versus hosted versus independent distinction | **UNKNOWN** | E-21, E-22; C4.3 UNRUN; no independent consumer evidence | No independent evidence exists; a hosted run is not independent verification. |
| SC-9 | Enforcement display: NONE or AUDITABLE at most; ENFORCED blocked | **SUPPORTED** (definition) | E-13/E-14; E-17/E-18 | Nothing is enforced; mounted coverage is UNKNOWN. |
| SC-10 | A recorded bypass is displayed as a bypass, never green | **SUPPORTED** (policy) | E-09; E-13 | No live bypass was exercised in this slice. |
| SC-11 | Two budgets are separate: review-head count and plan-revision count | **SUPPORTED** (semantics) | E-09/E-10; v2.1 exclusive count | The display of both budgets is UNRUN (SC-12). |
| SC-12 | Two-budget display and fourth-head behaviour | **UNRUN** | E-27; fixtures only | No display; 3-head/4-head cases not exercised in a consumer surface. |
| SC-13 | Evidence-reused status and decision | **UNRUN** | E-16; C2 tooling merged; no real reuse record | A synthetic schema is not a reuse decision; evidence reuse requires a real target head. |
| SC-14 | Production readiness displayed as achievable | **UNKNOWN** | E-09 (T6 UNVERIFIED+BLOCKED); E-13/E-14 | Production readiness is unreachable while T6 is undecided; no green path may be shown. |

**Status conclusion.** The vocabulary and several policy definitions exist and
are auditable, but the consumer display is not implemented and no real status
record has been exercised. All status/recovery compatibility claims that
depend on C4.1 evidence remain UNRUN.

## 5. Delivery prerequisites (E4-AC4)

This is the delivery-prerequisites record for E4.2. The guide remains DRAFT
until every applicable row is met or explicitly dispositioned by the named
owner. A row marked MET would still not authorise a publication claim by
itself.

| ID | Prerequisite | Current state | Owner | Effect on delivery |
| --- | --- | --- | --- | --- |
| DP-1 | E3 exit and T15 item-2 outcome | **NOT MET**; item-2 is 18 PASS / 3 FAIL / 1 UNRUN and not accepted (E-22, E-23) | Owner (T15-T19) and E3 owner | The assurance/limitations wording must keep the FAIL/UNRUN counts; no 22/22, no E3 closure. |
| DP-2 | C4.1 support matrix | **PRESENT but evidence-only**; 0 QUALIFIED, all cells UNRUN (E-07) | C4/C3 owner | No profile is supported; the matrix must stay UNRUN. |
| DP-3 | C4.2 pilot | **BOUNDED SHORTFALL**; 0 of 5 eligible arrivals (E-20) | C4 owner | No rate, saving, dollar or hours claim. |
| DP-4 | C4.3 independent review | **UNRUN**; no named reviewer (E-21) | Lead / AUTH-REVIEWERS | No independent C4.3 verdict exists to cite. |
| DP-5 | T2 design basis | **OPEN** | Owner | No contract conformance and no accepted version claim. |
| DP-6 | T5 mounted coverage / enforcement | **NOT ASSUMED / UNKNOWN** (E-13/E-14) | Owner | No ENFORCED or mounted-coverage claim. |
| DP-7 | T6 authentication method | **UNVERIFIED+BLOCKED** (E-09) | Owner | Production readiness remains unreachable. |
| DP-8 | T7 exception / unavailable-review authority | **OPEN / UNDEFINED** (E-11/E-12) | Owner | A cited exception cannot be honoured; real dispositions are BLOCKED. |
| DP-9 | T9 delivery/publication authority | **DOCS-ONLY IMPLEMENTATION ONLY** (E-02, E-06) | Owner / Lead | No publication, release, install or deploy claim; the guide stays DRAFT. |
| DP-10 | Q3 audience and metadata decision | **OPEN** | Owner | The docs remain review-scoped; no public metadata. |
| DP-11 | Q7 display-mapping version; Q8 assurance/visual vocabulary | **OPEN** | Owner | cs-map/1 stays a candidate; no mapping version or assurance vocabulary is accepted. |
| DP-12 | Item-5 statuses T8/T8a-c/T21 | **05-D MET; 05-G NOT MET** (E-24/E-25) | Owner / item-5 holder | No durable, source-linked or publication-classified claim; cite the limitation. |
| DP-13 | E4.3 reviewer availability | **UNRUN / not named** | Lead / owner | No independent review verdict; no PASS. |
| DP-14 | E2 dependency (status display, exercise) | **NOT DELIVERED**; E2.4 UNRUN | Experience lane | E2-dependent guide content is provisional; no UI or status display claim. |
| DP-15 | E1.6 integrated verification; T12/T13 closures | **UNRUN** (E-02, E-28) | Owner (T12/T13) | No E1 closure claim; E1.4/E1.5 records stay PROPOSED. |
| DP-16 | Accessibility standard | **PROPOSED** (candidate WCAG 2.2 AA), not exercised | Owner (Q6) | No accessibility conformance claim. |

## 6. Affected-check list (E4-AC3)

Only checks affected by this compatibility review are listed. Checks reused
from C4.1 or not applicable are recorded as UNRUN/UNKNOWN, not re-implemented.

| Check | What it tests | Result | Evidence / method |
| --- | --- | --- | --- |
| ACH-1 | Relative links and in-page anchors in the three E4 pages | **EXECUTED** | python -P scripts/ci/check-markdown-links.py over the three pages; the PR body records broken/dead counts (both must be 0). |
| ACH-2 | Structural render sanity: fences, tables, headings | **EXECUTED** | Local structural check in the E4 docs commit; PR body records the result. |
| ACH-3 | Every claim in the ledger has an evidence identity | **EXECUTED** | Full row check in [support-claims-v1](support-claims-v1.md); the PR body records the count. |
| ACH-4 | No second field list or restated contract | **EXECUTED** | Grep for canonical field sequences outside catalogue.py; none added. |
| ACH-5 | Metadata/audience classes | **EXECUTED** | Scan for personal names and plan-forbidden product names; PR numbers/internal record names present, so the pages are marked review-scoped. |
| ACH-6 | Status-vocabulary compatibility against C4.1 | **UNRUN** | C4.1 has no qualified cells; the check has no evidence to consume. |
| ACH-7 | Recovery-label compatibility against C4.1 | **UNRUN** | No real change-state records; synthetic fixtures are not evidence. |
| ACH-8 | Profile compatibility (A/B/C, no-inbox) | **UNRUN** | C4.1 cells are UNRUN; no host exercise. |
| ACH-9 | Independent review of this matrix and the guide/ledger | **UNRUN** | The E4.3 independent-review request record for this candidate (programme record, not in this repository; exact identity in the PR body) is a request, not a verdict. |

## 7. Gap and UNKNOWN register

| ID | Gap | Impact | Resolver |
| --- | --- | --- | --- |
| CM-G1 | No C4.1 QUALIFIED cell | No profile can be called supported | Real-host C4.1 evidence under T5/T9 authority |
| CM-G2 | T2 design basis open | No conformance or accepted-version claim | Owner T2 decision |
| CM-G3 | Display mapping not encoded (cs-map/1 candidate) | Cannot check label/state mapping | Q7 decision and a captured display implementation |
| CM-G4 | E2.3 display absent | Status/recovery compatibility cannot be exercised | E2 delivery under its authority |
| CM-G5 | No real change-state record | Recovery labels have no durable input | AUTH-STORE/T24 and a real change under authority |
| CM-G6 | T6 auth UNVERIFIED | Production readiness unreachable | Owner T6 decision |
| CM-G7 | T7 exception authority undefined | Unavailable-review path blocked | Owner T7 decision |
| CM-G8 | T5 mounted coverage not assumed | No enforcement/coverage claim | T5-gated qualification slice |
| CM-G9 | Item-5 05-G NOT MET | No source link or full item-5 closure | T21 + independent review/merge |
| CM-G10 | E3 item-2 not accepted (CP-09 FAIL) | No consumer-proof acceptance or 22/22 | T15-T20; CP-09 needs a new attempt |
| CM-G11 | E4.3 reviewer not named | No independent verdict | Lead/owner names a distinct reviewer |
| CM-G12 | No enforcement mechanism | Any ENFORCED claim is false | Separate T4/T5/T6/T7-gated slice |
| CM-G13 | Item-8 P3-08-01 UNRUN | Hosted schema-only proof not accepted | T14 proof acceptance / new evidence under authority |

## 8. What this matrix does not claim

- It does not qualify any host, platform, mode or profile.
- It does not claim consumer readiness, production readiness, delivery,
  installation, release, deployment or publication.
- It does not claim contract conformance; T2 is open.
- It does not claim enforcement, mounted coverage or custody.
- It does not claim item-2 acceptance, 22/22, E3 closure or E4 closure.
- It does not claim item-5 closure or durable custody; 05-G is NOT MET.
- It does not convert UNRUN or UNKNOWN to PASS, and it has no aggregate green.
- It does not authorise a provider, host, settings, CI or merge action.

## 9. Metadata and audience warning

**Do not republish this page or any derivative as consumer-facing
documentation.** It is a review record. It names programme PR numbers,
internal record identifiers and role identities that must not be copied into
public commit or artifact metadata. Requirement R8 says public commit or artifact metadata must
not carry plan-forbidden product names, PR numbers or personal names. The
audience decision Q3 is open and T9 publication authority is not granted.
Before any publication, a separate metadata-minimisation pass must remove or
replace those classes, and the owner must record the audience and channel. The
E3 item-2 CP-09 FAIL is the concrete precedent for why this warning is not
theoretical.

## 10. Maintenance and revision rule

This is compatibility matrix v1. Re-measure the base and every cited identity
at each review head; a moved head invalidates the affected cells. If a version,
label or evidence identity changes, add a dated revision or a new matrix
version; do not silently rewrite a reviewed row. No cell becomes SUPPORTED
without an evidence identity at the exact head, and no aggregation of cells is
a readiness result.
