# Required-governance contract v1 — contract, resolver, receipts and packaging closure

**Status:** normative design page for the P0-GOV C1 implementation (WS2 "Required Governance Discovery and Execution Gates"). **Schema:** `aegis.governance-contract/1` plus `aegis.context-receipt/1`, `aegis.governance-adoption/1`, `aegis.admission-decision/1`. **Tool:** `tools/aegis_preflight/governance.py` (read-only resolver/validator, second verb family) and the read-only dependency-consumption mode of `tools/distributed_payload verify --check-dependencies`. **Plan of record:** `PLAN-OF-RECORD-P0-GOV-r3.md` (190,556 B / sha256 `0A5F8A65C2BEF4EFAEACED0262A78EFFDA36121333A0EB6BC1B57583881A1A40`), Stage B r3 ACCEPT (`EC106437...`). **Base:** `b2666f97b91335a72a5e7e6456e8c251c3ee09c3`.

**Assurance:** auditable, deterministic, read-only tooling and repository content. This page and the artifacts it describes are **guidance plus local checks**, not runtime enforcement, not an approval, not a merge gate and not a second policy. On the observed host no repository-installable hook or interception facility exists (plan section 8); a claim of runtime enforcement from these files would be false.

## 1. Problem this closes

An agent can consume an Aegis skill without discovering the governance that governs the work. The copied starter carries the startup files and skills but deliberately not the source workflow, register or approval semantics; the installed DeepSeek Harness does not discover `.claude/skills`; and an individually exported skill has no declarative statement of the governance it requires. The C1 implementation adds one versioned, machine-readable contract that binds the authoritative documents by identity, declares applicability, lifecycle and adoption, resolves the dependency offline, and records typed receipts whose bound inputs can be re-derived and invalidated.

It does **not** change any authoritative document, create approval, add a register or backlog, wire CI, or enforce at runtime.

## 2. Artifact layout

```
docs/governance/
  payload/                                    <- packaging root: exactly the six packaged entries
    required-governance-contract.v1.json      <- schema aegis.governance-contract/1
    rule-projection.v1.json                   <- committed deterministic mapping/classifier
    schemas/governance-contract-v1.schema.json
    schemas/context-receipt-v1.schema.json
    schemas/adoption-record-v1.schema.json
    schemas/admission-decision-v1.schema.json
  governance-payload.source.json              <- generated-manifest source claim (outside payload root)
  governance-payload.dependencies.json        <- packaging entry->entry edges (outside payload root)
  governance-payload.manifest.json            <- generated committed manifest (outside payload root)
  inputs/governance-inventory.json            <- governed generation input (task-33 inventory, outside payload root)
docs/design/required-governance-contract-v1.md  <- this page (deliberately NOT packaged)
tools/aegis_preflight/governance.py            <- resolver/validator/receipt/admission + render verbs
tools/aegis_preflight/tests/{test_governance.py,test_rule_projection.py,fixtures/governance/**}
tools/distributed_payload/verify.py + __main__.py  <- read-only verify --check-dependencies mode
tools/distributed_payload/tests/test_dependency_closure.py
tools/governance-dependencies.json            <- per-skill packaging dependency declaration
```

The design page is not a payload entry because it lives outside `docs/governance/payload/`; the unchanged packaging tool collects exactly the entries under that root, so the page can never become an entry and determinism holds.

## 3. The contract

Required top-level fields (strict schema; unknown fields at every object level are rejected):

| Field | Meaning |
| --- | --- |
| `schema`, `contract_id`, `contract_version` | `aegis.governance-contract/1`, `aegis.required-governance`, SemVer (`1.0.0`). |
| `source` | Declared repository/commit/tree plus `generated_by`. The commit is the base the authoritative identities were measured at; it is **not** the enclosing commit (no circularity). |
| `summary` | Plain-language statement of what the contract requires and does not enforce. |
| `roles` | `source-library` and `consumer`: required documents, conditional documents with a closed condition name, exclusions with a reason, `adoption_required`, permitted entry routes. |
| `documents` | The 27 authoritative Tier 1/2/3 records with doc_id, path, role scope, tier, bytes/LF/SHA-256, authority class, lifecycle state, read depth and rule citations. |
| `entry_routes` | Five route families; seven route ids (session-boundary expands to resume/compaction/handoff). Each record carries triggers, resolution inputs, fail-closed behaviour, required evidence and a supported-host scope label. |
| `dependency_graph` | The **resolution/applicability** graph (nodes: doc id, route route-id family, skill entrypoint; edges to doc ids with class required/conditional/optional/maintainer-only). |
| `rule_applicability` | 187 records: direct inventory fields copied byte-for-byte plus six derived fields produced only by the committed projection. |
| `conflicts` | The inventory's twelve document-level conflicts with normalized status, the documents named in evidence and (currently empty) rule-level attachments. An unresolved **rule-level** conflict blocks resolution; a document-level conflict is surfaced. |
| `lifecycle` | Contract-level status/review date/migration rule/rollback rule. |
| `local_adoption` | Consumer adoption record schema, record paths, required fields and the invalidation inputs. |
| `host_boundary` | Observed host identity with an explicit claim label; unsupported-host fail-closed behaviour; data-exit disclosures. |
| `enforcement_claims` | One claim object (`GUIDANCE-ONLY` here) with named surfaces, bypass analysis and UNRUN items. A `HOST-PLUGIN` claim requires a composition hash and evidence; it cannot be asserted by text alone. |
| `trust`, `non_claims` | Authoritative inputs, non-authoritative inputs, the re-derivation rule and the explicit non-claims. |

### 3.1 Deterministic projection (direct vs derived)

Direct fields are imported unchanged from the task-33 inventory: rule_id, anchor, class, dimension, lifecycle, consumer adoption status and consumer effect. The derived fields are produced **only** by `docs/governance/payload/rule-projection.v1.json`:

| Derived field | Rule |
| --- | --- |
| `source_document` | Total table over the inventory's source strings; the primary is the first document named by the source cell and every combined row also lists its secondary documents for citation. An unmapped source fails the build; no default is applied. |
| `applies_to_roles` | Base table by inventory class (portable classes reach both roles; source-only/action-permission/historical/ambiguous reach the source role) plus a committed per-rule override table for the thirteen portable exceptions. An unmapped class fails the build. |
| `authority_action` | Mechanical: class == action-permission (17 rules), never authored by hand. |
| `enforcement_class`, `enforcement_ref` | Closed classifier over the inventory's descriptive Enforcement text with a fixed precedence: a leading procedural/negative marker means GUIDANCE-ONLY; then required-context language means CI-REQUIRED; then host-enforcement language means HOST-ENFORCED; then structural-check language means CI-STRUCTURAL; otherwise GUIDANCE-ONLY. The classifier version and its full output are committed in the projection file and re-run by the projection test. |

The classifier is **descriptive of the inventory's own text**. A named surface is never complete enforcement of a rule, and the contract publishes no aggregate "how many rules are machine-enforced" tally (the withdrawn r1 48/125/14 split is not reproduced anywhere).

## 4. Resolver algorithm

`governance resolve` (read-only) performs, in order:

1. **Validate the contract structure** — strict schema, role profiles (required/conditional/excluded disjoint; consumer adoption required), five route families / seven route ids, graph node kinds, conditional-rule vocabulary, duplicate-edge and cycle detection. A malformed graph or a cycle is a hard failure; nothing is traversed past it.
2. **Resolve the role/route.** The route id must be permitted for the role. The role profile contributes required documents, conditionally-included documents (a closed six-name condition vocabulary evaluated from caller-supplied booleans) and exclusions with reasons.
3. **Traverse the resolution graph** from `route:<id>` and `route_family:<family>`. Required edges add targets; conditional edges add only when their named condition holds; optional edges are advisory; maintainer-only targets are never added. Cycles and unresolvable required edges block.
4. **Re-derive document identities** from the checkout: bytes, LF and raw SHA-256 must equal the contract records. Missing or changed required documents block with the exact doc_id/path; a superseded/withdrawn document is excluded with the lifecycle reason.
5. **Apply local adoption** for the consumer role: an absent, malformed, contract-mismatched or revoked adoption record means not-adopted/withdrawn and blocks dependent work; the source role is its own authoritative set and requires no consumer adoption.
6. **Compute the rule set.** A rule is resolved when the role is in its derived `applies_to_roles`, its lifecycle is in force, its source document is in the resolved document set and (for consumers) its adoption status is adopted-by-copy or the adoption record explicitly adopts it. Everything else is recorded as an exclusion with a reason — never silently dropped.
7. **Surface conflicts.** A document-level conflict affecting resolved documents is recorded, not resolved. A conflict that attaches at least two resolved rule ids blocks with both anchors and never picks a winner.
8. **Record the session-boundary typing** inferred from the route and hash the resolved set into a deterministic digest.

Status is `RESOLVED` only when no finding is FAIL/BLOCKED; otherwise `BLOCKED` with the inputs named. A resolution is an observation, never authority.

## 5. Context receipt and admission

### 5.1 Receipt

A receipt (`aegis.context-receipt/1`) records one observation: receipt id, observation type, route id/family, UTC time, task and authority reference, target and role evidence, host/session facts (null where the host does not expose them), instruction baseline, contract identity (version, sha256, source commit, approved upstream pin, lifecycle state, verifier identity), the packaging-manifest binding (manifest bytes/LF/sha256, path outside the payload root, detached binding ref/hash, the build/verify/check-manifest commands and exit codes, the Stage A feasibility reference and whether C1 dependency consumption was used), the resolved documents with read status, local adoption state, nested/local policy files, resolved rules, exclusions, an invalidation digest, integrity status, limitations and non-claims.

**Observation typing is part of the record:** a session-boundary route must carry its matching type (`resume`/`compaction`/`handoff`); a non-boundary route carries `fresh-start` or `protected-operation`. An old receipt keeps its old type and is never edited to refresh.

### 5.2 Invalidation

The invalidation digest is SHA-256 over the ordered, normalized list of bound inputs (`kind`, `path`, `bytes`, `sha256`): the contract, every resolved document, the adoption record, nested/local policy files, the role evidence, the host profile digest where available, and the task/authority reference. Any of the contract bytes/version, a required-document hash, the approved upstream pin, the target or role, the adoption record, a nested policy hash, the host build/profile digest or session boundary invalidates without re-observation. Receipts are never edited in place; a new observation produces a new receipt and the old one is kept as evidence of the old observation.

### 5.3 Admission

An admission decision (`aegis.admission-decision/1`) is a record of a recheck at admission time, not a prompt and not a durable permission. For each protected operation class the resolver: re-reads the bound inputs and compares the digest; rechecks role/target identity; refuses a source-library authority reference for consumer work; compares the contract sha256 and the approved pin; blocks a pre-boundary receipt after a resume/compaction/handoff; rechecks the adoption record (withdrawn blocks, malformed blocks); verifies that every required document still matches authoritative bytes; and denies a claimed active host gate without composition evidence. Outcomes are `ALLOW`, `DENY` or `BLOCKED` with a closed reason code and the differing inputs. Read-only diagnostic access remains allowed with the missing or stale source named — and no decision denies anything at the host level; it records guidance plus evidence.

## 6. Entry routes

Five families, seven route ids: source-checkout; copied-starter; external-skill; standalone-export; session-boundary (resume, compaction, handoff). For every route: the target repository and role determine applicability, the contract version/pin is explicit, resolved identities are recorded, exclusions are explicit, an old receipt is old, adoption is local, source authority never transfers, and a missing dependency blocks dependent work while diagnostics stay allowed. The route records in the contract state each family's triggers, inputs, fail-closed behaviour, evidence and supported-host scope.

## 7. Packaging closure (unchanged tool + one C1 mode)

The payload root contains exactly the six entries and the manifest is generated **outside** it. The exact unchanged-tool commands are:

```
python -m tools.distributed_payload build --root docs/governance/payload --package-id aegis.required-governance --package-version 1.0.0 --source docs/governance/governance-payload.source.json --dependencies docs/governance/governance-payload.dependencies.json --out docs/governance/governance-payload.manifest.json
python -m tools.distributed_payload verify --manifest docs/governance/governance-payload.manifest.json --target docs/governance/payload --json
python -m tools.distributed_payload check-manifest --manifest docs/governance/governance-payload.manifest.json
```

C1 adds the read-only consumption mode `verify --check-dependencies`: it consumes the manifest's declared entry->entry edges and reports duplicates (exact or conflicting class), cycles, class/scope contradictions (a maintainer-only edge naming a distributed entry), conditional edges without a rule, and required/conditional/optional targets absent from the target tree. It adds findings only; `manifest.py`, schema v1 and the three existing verbs are unchanged, and verify still never repairs. The two graphs are separate: the **packaging graph** is entry->entry and is owned by the distributed-payload manifest; the **resolution/applicability graph** uses logical ids (docs, routes, skill entrypoints) and is owned by `governance.py`; neither is emitted into the other's artifact.

**Non-circular binding.** The manifest lists payload hashes; no payload entry contains the manifest hash; a detached binding records manifest bytes/LF/sha256, contract sha256, source commit/tree, the three commands and exit codes, and a UTC timestamp. A receipt records the contract hash and that detached binding identity.

## 8. Migration, rollback and consumer adoption (specification only)

- **Migration:** a new contract version is adopted by recording the new contract id/version/sha256 in the consumer's adoption record; a source edit to any bound document requires re-generation, a contract_version bump and a re-derived manifest. Receipts observed under an older contract remain old observations.
- **Rollback:** restore the previous committed payload bytes and manifest and supersede the new contract version in the record; a rollback never restores revoked authority and never silently deletes consumer-local policy. The resolver exposes a deterministic rollback record shape and its triggers (false admission, broken install, unusable restoration, owner withdrawal).
- **Consumer adoption:** the consumer route is a copy route, not a source-role grant. The consumer's own adoption record (owner/authorised-agent authority, contract binding, explicit adopted/rejected rule ids, installation pin and manifest hash, effective/revocation fields, review date) is required; a missing or revoked record means not-adopted/withdrawn. Source register entries never authorize consumer work.
- **OpsFlow** and any live consumer rollout are **separate governed outcomes**: this page is a specification and performs no OpsFlow edit, memory edit or settings change. Adding the contract bytes to the starter install closure (starter v3) is likewise a separate governed outcome (O12); the live copied-starter route is UNRUN.

## 9. Host boundary and enforcement honesty

The observed host is DeepSeek Harness Desktop 0.2.2-rc.1 with app.asar sha256 `5FA8A6B2...`; its host claim label in the contract is `OBSERVED-IDENTITY-ONLY` — the installation identity was observed, but no host gate, hook, interception or review-independence mechanism is active for repository governance. All other hosts are UNSUPPORTED-UNVERIFIED. Enforcement claims are limited to `GUIDANCE-ONLY` repository content plus the named auditable local checks; bypass routes (direct effects inside run_code, alternate launchers, GUI/remote/ACP bridges, host-user configuration edits, subprocess effects, local receipt/session-log mutation, default-on provider upload) are disclosed and not closed by repository content. A host-profile plugin/wrapper is the separate owner choice O15; until one is provisioned and evidenced, live-host cases 09/10/11/16/22/25 remain UNRUN and case 25 cannot pass.

## 10. Determinism and non-circularity

- Contract, projection, governance-dependency declaration and manifest are rendered from committed inputs; the test suite asserts the committed bytes are byte-identical to a fresh render and that two renders are identical.
- The contract never embeds its own sha256, the manifest sha256, the enclosing commit hash, a timestamp or an absolute host path. The projection's derived output is generated, never hand-edited; a mismatch fails validation.
- The source identity in `governance-payload.source.json` and in the contract is the measured planning base `b2666f97`, not the enclosing commit.
- The governed inventory (task-33, raw 473,586 B / 8,008 LF / 8,008 CR / sha256 `902E443A...`) is committed **LF-normalized** because the repository's `.gitattributes` text policy (text=auto eol=lf) normalizes text files on commit: committed identity 465,578 B / 8,008 LF / sha256 `FCDC04B3...`, with the raw source identity recorded beside it in the projection. The conversion is CRLF->LF only and leaves the JSON semantics unchanged; both identities are pinned in code, the projection and the detached binding, and any change is refused until a deliberate, reviewed regeneration.

## 11. File and change discipline

New files: the six payload entries, the three packaging inputs/manifest, the governed inventory copy, `docs/design/required-governance-contract-v1.md`, `tools/aegis_preflight/governance.py`, the resolver/render tests and governance fixtures, `tools/distributed_payload/tests/test_dependency_closure.py` and the `tools/governance-dependencies.json` declaration. Modified files: `tools/aegis_preflight/__main__.py` (dispatch of the second verb family) and `models.py` (shared vocabularies and result records); `tools/distributed_payload/verify.py` and `__main__.py` (read-only dependency consumption and its flag); the two component READMEs. `manifest.py`, manifest schema v1 and PF-01..PF-10 semantics are unchanged.

Not touched by C1: CI workflows, `scripts/**`, `.claude/agents/**`, the approval register and revision-state store, `README.md`, the source pin, and the surfaces held by PR #1095 (`.claude/skills/**`, `AGENTS.md`, `CLAUDE.md`, `docs/consumer-starter-package.md`, `tools/skills-manifest.json`). The pointer/rule-text edits the plan assigns to `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `docs/delivery-workflow.md` and the consumer pages are **deferred**: the held ones wait for PR #1095, and the rest are C2 documentation work; see the C1 evidence record for the held/deferred list.

A later contract change is a reviewed change: edit the authoritative input, bump `contract_version` (SemVer; a breaking change is a new major-version file with v1 retained), re-render the contract/projection/declaration, rebuild the manifest with the unchanged command, and re-run the test suites and the gate-guard protected-path measurement.

## 12. Non-claims

This page is not an approval, not a grant, not a merge gate, not runtime enforcement, not a host qualification, not consumer readiness, not a second register/backlog/policy, and not evidence of reading comprehension or obedience. A clean verification, a receipt and a resolver ALLOW are records of a check, never authority. The live-host cases and the OpsFlow route remain UNRUN.
