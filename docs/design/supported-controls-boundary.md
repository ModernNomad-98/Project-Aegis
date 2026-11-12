# Supported-controls and custody boundary (C1.2B, disclosure only)

**Status: boundary disclosure. No control is enforced, installed, qualified or
claimed as covering any route.** This page records what is *supported* in the
only sense available today - what evidence exists, who holds custody, and
which routes are not governed - and it states the maximum assurance claim this
slice can make: **AUDITABLE, at most, and NONE for any host control.**
Mounted coverage is **UNKNOWN** everywhere.

**Audience and reading key.** For Project Aegis maintainers, reviewers and consumers reading the disclosure. **C1.2B/C1.2-C1.4** are the supported-controls/custody, stage/qualification and freeze workstreams; **REV4** is the Stage A plan revision; **C0** is the programme intake findings; **B1-B2** are enforcement-design items; **C1.1a** is the verdict-gate checker store; **AUTH-STORE** is the store-custody decision; **T3/T4/T5/T6/T7/T24** are scope/settings/coverage/authentication/exception/custody decisions; **ACP/MCP** are agent-client and model-context protocol routes; **CODEOWNERS** is the repository ownership file.

**Authority.** C1.2B of the C1.2-C1.4 Stage A plan REV4 (69,918 B /
`a65fa654e59d0852759cab6693780f74b2b08b6bcf4c4c160b3834f39f208e0c`), captured as
`C12-C14-STAGE-A-CAPTURE-FINAL-2026-11-11.md` (1,081 B / `569391426f889513a415f7fb7c7e9ab495e52050cc185ceb8b7c27ef47ff90a4`)
and accepted plan-only by Stage B REV4 (12,193 B / `3318b957a3e979813c7e3458092003d7cc5b41f3d3e5f03ca987e312d410b952`). The page is
docs-only: no host access, no install, no settings/CI/required-context change,
no T5 export and no T4 identity/settings action. It is grounded in the C0
intake findings (`C0-INTAKE-FINDINGS-2026-11-10.md`, 43,074 B /
`31874a96089ec69bed5547ddf5ed63247ba829a5ba053baa59e835a0b5e65dd9`, section 6), the B1-B2 enforcement design REV2 and its errata
confirmation, and the merged C1.1a surfaces - it is not a new assessment.

## What "supported" would require

A host control is **supported** only when both of these are evidenced, not
asserted:

1. **Custody** - the constrained party cannot silently rewrite, restart,
   disable or re-point the control (the kill switch severs authority, not just
   a display).
2. **Coverage** - which tool/execution paths the control actually governs is
   known and proved (a mounted-coverage export), including the routes it does
   not govern.

Neither is proved today. The guard facility exists and is monotonic (REPORTED
from C0 section 6, not re-derived here), but the desktop composition cannot be
dumped (REPORTED: C0 intake section 6.2), so mounted coverage is UNKNOWN; and
the profile patch layer is user-writable under the constrained agent's profile
(REPORTED: C0 intake section 6.4), so custody fails for the configuration
route.

## Control matrix

Evidence classes: **VERIFIED** (re-derived this pass from a cited primary
source), **REPORTED** (asserted by a named record, not re-derived),
**UNKNOWN** (not derivable). Assurance claims are limited to NONE/AUDITABLE.

| Control | Claimed scope | Evidence available | Coverage | Custody | Bypasses | Assurance |
| --- | --- | --- | --- | --- | --- | --- |
| In-process tool guard | tool calls inside the guarded process | facility present and monotonic (REPORTED: C0 section 6); no mounted dump | **UNKNOWN** | not proved | custom executor, ACP runtimes, terminal/remote, workflow registration, subagent presets, restart re-read | **NONE** |
| Workflow policy / required contexts | repository merge path | workflow and gate-guard pattern measured at origin/main 701ebc7c; no required-context registration in this slice | partial, repository-only | repository admins can edit workflows; branch protection is a settings action | admin merge past a red gate; direct push; settings edits | **NONE** |
| Terminal / remote confinement | terminal and remote execution routes | none | **UNKNOWN** | not proved | remote/terminal routes are outside the guarded process | **NONE** |
| Profile / config custody | the constrained agent's profile and config | profile patch layer is user-writable under that profile (REPORTED: C0 section 6) | **UNKNOWN** | **fails** (write scope includes the control) | config edit + restart re-read | **NONE** |
| Counter / policy store custody | the store that counts heads/attempts | merged revision-state store is append-only + git-history only; provenance UNVERIFIED (AUTH-STORE / T24) | repository-only | **not proved** (docs/approvals is not gate-guard protected) | repository admin rewrite; a second store would duplicate the counter | **NONE** |

## Routes that are not governed

Six routes are known not to be governed by the in-process guard (REPORTED from
C0 section 6, reused by the B1-B2 coverage map, not re-derived here):

1. custom executor routes;
2. ACP runtimes;
3. terminal / remote execution;
4. workflow registration;
5. subagent presets;
6. restart re-read of configuration.

Repository-side routes are a separate class: the `gate-guard` job in
[`.github/workflows/validate-skills.yml`](../../.github/workflows/validate-skills.yml)
(L543) protects a defined set (`scripts/`, `.github/workflows/`, CODEOWNERS,
root-level importable names, `tools/behavioral_eval_runner/`, requirements
locks, agent/MCP config), with ownership recorded in
[`.github/CODEOWNERS`](../../.github/CODEOWNERS); `scripts/ci/gate_guard.py`
is not present in this tree. It does **not** protect `docs/approvals/`,
settings, branch protection or the required contexts list. The change-state store documented in
[the change-state README](../approvals/change-state/README.md) therefore has
custody by policy + append-only checker + git history only: a repository
administrator can still rewrite it. That is a recorded gap, not a claim of
protection.

## Counter and policy custody

Repo-side counters live in the append-only record store; they are re-derived
from the records and never trusted from a manifest. Any host-side counter or
policy store, if it were ever authorised, would have to be outside the party it
constrains and would have to be the **only** counter store: no duplication with
`tools/aegis_delivery_control/`, whose kernel is a synthetic,
issuer-less/offline mechanism and is not an enforcement counter. No second
ledger is created by this slice.

## Assurance vocabulary

| Claim | Meaning | Available here? |
| --- | --- | --- |
| NONE | no assurance asserted | yes (the default for every host control) |
| AUDITABLE | records and commands can be audited after the fact; nothing is prevented | yes, for the repository-side records only |
| ENFORCED | the control provably prevents the action, with proved custody and mounted coverage and independent verification | **no** - blocked |

An ENFORCED claim for any host control would require, at minimum:

- **T4** - the five custody/settings/identity preconditions (owner declined
  them for this slice);
- **T5** - a mounted host-coverage export, so the governed paths are known;
- **T6** - an authentication method (currently accepted as UNVERIFIED+BLOCKED,
  so production readiness is unreachable);
- **T7** - the general fourth-head/unavailable-review authority;
- an independent verifier distinct from the implementer, exact-head evidence,
  and a recorded scoped authority line; plus the B2 admission conditions if an
  in-session advisory were ever installed (B2 is deferred under T3).

None of that exists. Nothing in this repository may be cited as host
containment, universal prevention or enforcement.

## What this page does not do

It does not install, enable or modify a control; it does not read host state;
it does not claim coverage, custody or monotonicity as VERIFIED; it does not
convert a recorded bypass into a green label; it does not create a second store
or ledger; it does not register a required context or change settings; and it
does not qualify the host (that is the separate disclosure on
[host qualification](host-qualification-disclosure.md)).
