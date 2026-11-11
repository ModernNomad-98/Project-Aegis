# 39-to-41 starter transition at the current head (2026-11-11)

Status: **PROPOSED current-head evidence record** for E1.5 (programme item 7, the
exact v1 39-file to v2 41-file transition). It re-baselines the delivered
transition from the historical item-7 run to the execution head under the current
record-guard behaviour and records one Windows host's native execution. It is
execution evidence only: it is **not** a review disposition, **not** acceptance,
**not** E1/E1.5 closure, and **not** an uninstall, downgrade, arbitrary-version,
second-host, macOS, Linux, hosted, real-consumer or all-or-nothing claim. Every
cell that was not executed is named UNRUN in section 8.

The historical record
[local-starter-transition-v1-to-v2.md](local-starter-transition-v1-to-v2.md) is
unchanged and is cited only as historical evidence. It was bound to a prior page
and section 7.1 (21,977 B / `5b0393cc...`) and to the pre-record-guard
behaviour, in which C3 exited 0. That C3 result is **superseded** at this head and
is not cited as current evidence.

## 1. Binding at execution

| Item | Identity |
| --- | --- |
| Execution head | `701ebc7c3cee83058afb437ad911bc9f2ca8d8cb`, tree `8b3f15b16e75ef04b93c6938f725d660b08e13c0` |
| Base | live `origin/main` at the same commit (PR #1016 C1.1a merge); fetched immediately before the runs |
| Branch | `impl/e14-e15-current-head-2026-11-11` (docs-only evidence branch) |
| Page | [consumer-starter-package.md](../../consumer-starter-package.md), blob `cc4e5ba399311422acf3d05280422727b159ad39`, **147,728 B**, sha256 `47a6b7e46dd1c16138dd8e05c6f6b09a370b60b91bf8a4b301144520993c8484` |
| P2 gate block | **6,493 B**, sha256 `fd01fce7806c74e92f0fdf877c1cb58ed7704e8f24a316cccbce91b1dd7398ea` |
| Section 7.1 harness block | **27,748 B**, sha256 `907dc8637d91a22d3569914570436bda12fdd2562fc509a3a60093fc3ebe272f` (block index 1) |
| Section 7.2 exit-code table | prose table; the codes observed here are 20, 22, 24, 25, 31 and 23 (the record guard's 23/24/25 semantics are quoted in the cases below) |
| Section 7.3 transition block | **2,074 B**, sha256 `9d4ae8e80da43f5d003faf83931b7d6e3786dff633c58a7ef78f2ecfc668679d` |
| Record-guard behaviours at this head | exit 23 for a reparse point at or above the record path (including P9's re-check of the record leaf); exit 24 for an existing record without `-AllowExistingRecord`, a non-regular file under the switch, a record overlapping a package output, and a record file that appears after the preflight; exit 25 for a record that cannot be written atomically, with the unique same-directory temp removed best-effort; the temp name is `<record>.<guid>.tmp` and the final move is `[IO.File]::Move(temp, path, false)` |
| Package pin | `ffb040c7a363648856475280646bbd142dfabe4e`, tree `88a5aee4ad928a49c2fb945032585843ec652da7` |
| Frozen constants | `AggSha fcff1124d9d15e7d7230fd317350e0eb3b097b453bb6b911cdc1e2485525b699`, `AggRows 41`, `AggBytes 5420` |
| Historical v1 record (copied unchanged into the fixture) | `docs/consumer-install-record.md`, **6,738 B**, sha256 `31005b7b8b128ee4b800fb05d8e628056b44be460af4fc33a687b74846503f9a`, 39 rows, serialized 5,152, aggregate `0c885bcd07d62d244da06748e81f006c0f4f93b3fae3cc54f611c7c72218a5a7` |
| Adapted runner (this run) | `run_transition_current.py`, **27,512 B**, sha256 `c6de7801b92e92e3889b41fb37c8c915df345d00169eeb2afb0d2c0efe8dd5f8` |
| Fixture builder (item-7 design, reused) | `build_v1_fixture.py`, **5,705 B**, sha256 `c6e880f4af8ff21125d22773948281fa4f5f2af12916100da7c0037331e241a6` |
| Table/git helper (item-7 design, reused) | `transition_lib.py`, **4,412 B**, sha256 `732bb1bd6bf73d492a7cedd7473b450a5fd5a810a14bdb6a35fbbc8631a0ba41` |
| Raw case JSON | `current-head-cases.json`, **307,952 B**, sha256 `95ee42dd501682bbd46c91c574315d1484e01e57991e3ce34024501598cb9eb7` |
| Fixture before-state | `v1-consumer-before-state.json`, **21,546 B**, sha256 `b52d2bebd713eb251bc1c0d5399f12dc08bd3a44286cb0ddf09534f8d507f6e5` |

"Block" means the fenced body exactly as the page publishes it plus one trailing
LF. Re-measuring this head reproduced the captured-plan identities with **zero
bytes of drift** (page 147,728 / `47a6b7e4...`; P2 6,493 / `fd01fce7...`;
section 7.1 27,748 / `907dc863...`; section 7.3 2,074 / `9d4ae8e8...`; pin
`ffb040c7` / tree `88a5aee4`; constants `fcff1124...` / 41 / 5,420), and
the runner fails closed if those constants differ. No re-freeze was triggered.

Paths under `_A/` are the local evidence workspace and are not committed; every
retained file's bytes and sha256 are recorded here.

## 2. Assembled starting fixture (disclosed)

The 39-file v1 state was **assembled** from the published pinned bytes, not
replayed from a historical install:

- 39 unique rows from [local-starter-v1.md](local-starter-v1.md), each written
  from its `git cat-file` blob at pin `ffb040c7` and checked byte-for-byte
  against the published row (bytes, LF and SHA-256). No historical v1 run is
  claimed.
- The historical v1 record copied in unchanged and identity-checked: 6,738 B /
  `31005b7b...`, 39 rows, serialized 5,152, aggregate `0c885bcd...`.
- Four unrelated product files plus a harmless local config planted and hashed
  (`src/acme_app.py`, `docs/product-notes.md`, `README.md`,
  `.claude/settings.local.json`).
- Git-initialised with a local owner record and one commit:
  `ba9676e178f1f223d85803d392a565e92a2c8268`. Before-state: **44 files**,
  inventory aggregate `bf720c51dea54771e3cf509e704b72f4ce759e07c0c0d42a2b319f81922bbd41`.

The construction method is disclosed here because an assembled fixture must never
be presented as a historical run.

## 3. Pre-run preconditions

The current section 7.3 wrapper is interactive (`Read-Host -MaskInput`) and was
not executed; its preconditions were checked and recorded directly, and the
section 7.1 harness was invoked as the historical runner did. For every case:
the target is a Git repository with a local owner record; the v1 receipt exists
with 39 rows and the frozen aggregate; the v2 record path does not exist on the
initial run; `install-mode.ps1` (P2) and `install-starter.ps1` (section 7.1)
are the extracted current blocks beside each other; `-Sh` is
`C:\Program Files\Git\bin\sh.exe`; `-Mode human-only`. The runner passes
`-ModeGate` explicitly and confirms `PinCommit`, `PinTree`, `AggSha`,
`AggRows` and `AggBytes` before any case.

## 4. Case results at the current head

Every case started from a fresh copy of the assembled fixture. "Package" counts
the 41 published package paths; "pin-identical" counts those whose bytes equal the
pin blob.

| Case | Command shape | Exit | Observed |
| --- | --- | --- | --- |
| C1 valid transition, fresh record | harness, `-RecordPath docs/consumer-install-record-v2.md` | **0** | 41/41 pin-identical; delta added exactly `.claude/skills/scoped-approval-register/SKILL.md`, `.claude/skills/scoped-approval-register/references/register-format.md` and the record; no changed or removed file; old record byte-identical; commit unchanged |
| C2 conflicting selected file | one selected byte changed (`.claude/skills/code-reviewer/SKILL.md`) | **31** | conflict bytes preserved (sha re-checked), 39 present / 38 pin-identical, no record, old record unchanged |
| C3a reused old record path | `-RecordPath` = v1 record, no switch | **24** | no package write (39 present, unchanged), old record byte-identical |
| C3b reused old record path + switch | same with `-AllowExistingRecord` | **0** | 41/41 package files written; the retained 39-row v1 record is left **byte-identical at that path** and is **not** a v2 receipt |
| C4 constructed matching partial (40/41) | `register-format.md` absent, other 40 matching | **0** | resumed; added `register-format.md` + fresh 41-row record; 41/41 |
| C5 constructed divergent partial (40/41) | `register-format.md` present with divergent bytes | **31** | divergent bytes preserved; no record; not counted complete (40/41 pin-identical) |
| C6a identical completed rerun | C1 target, same record path, no switch | **24** | no file delta; record byte-identical |
| C6b identical completed rerun + switch | same with `-AllowExistingRecord` | **0** | stdout `P9: install record already present, left unchanged`; record byte-identical; no freshness implied |
| C7a stale record at the intended new path | 42-byte stale file pre-created | **24** | stale bytes preserved; no package write |
| C7b stale record + switch | same with `-AllowExistingRecord` | **0** | stale bytes preserved unchanged; **no** fresh v2 receipt is claimed |
| C8 foreign file in a selected skill directory | `.claude/skills/scoped-approval-register/notes.txt` | **20** | foreign file named and preserved; no record; no package write |
| K1 real kill at the 40/41 boundary | process suspended on observing the `references/` directory created with the 41st file absent, then terminated | **1** (killed) | observed state **40 present / 40 pin-identical**, 41st missing; rerun exit **0**, adds the missing file + fresh 41-row record, 41/41 |
| K1b real kill then divergent partial | same kill, then `.claude/skills/scoped-approval-register/SKILL.md` truncated to 0 B | **1** (killed), rerun **31** | divergent bytes preserved; no record; not complete |
| K2 real kill during the P9 record write | process suspended on the unique temp appearing, then terminated | **1** (killed) | at kill: temp `consumer-install-record-v2.md.<guid>.tmp` present, **no record at the declared path**; after kill the temp is **0 B** and is never read as a record; rerun exit **0** writes a fresh 41-row record |
| FSL file symbolic link leaf (record path) | `mklink <record> <sentinel>` | — | **UNRUN**: `You do not have sufficient privilege to perform this operation.` |
| AC agent-commit route | — | — | **UNRUN**: no authority for the agent-commit route in this slice; every accepted historical case was human-only |

The fresh C1 record is 7,025 B with 41 rows, serialized 5,420, aggregate
`fcff1124d9d15e7d7230fd317350e0eb3b097b453bb6b911cdc1e2485525b699`, source
commit `ffb040c7` and tree `88a5aee4`: it matches the frozen profile rather
than copying the v1 receipt. Its own sha256 varies per run because the record
embeds the install timestamp and tool lines; the C1 hash for this run is
`404aa815...` and is not claimed as a fixed identity.

The v1 receipt was byte-identical (`31005b7b...`) after every case, including
C3b. Product files and the fixture commit (`ba9676e1...`) were unchanged in
every case; no case created a commit.

## 5. Scope of the 39-to-41 delta

The transition adds exactly the two published paths
`.claude/skills/scoped-approval-register/SKILL.md` and
`.claude/skills/scoped-approval-register/references/register-format.md`; all 39
common rows remain pin-identical (C1/C4/K1: 41/41 pin-identical after
completion). No other file was added, changed or removed.

## 6. Acceptance-criteria mapping (execution evidence only)

| AC | State | Evidence |
| --- | --- | --- |
| E1.5-1 binding before execution, drift triggers re-freeze | **MET** | Section 1; zero-byte drift |
| E1.5-2 exact starting fixture, disclosed assembly | **MET** | Section 2; 39 rows verified at the pin; v1 record identity checked |
| E1.5-3 C1 valid transition | **MET** | 41/41; two added paths; fresh 41-row record with actual pin/aggregate; old record unchanged; commit unchanged |
| E1.5-4 C2 conflict refuses at the documented code | **MET** | 31, bytes preserved, no record |
| E1.5-5 C3 reflects the current record guard | **MET** | 24 without the switch; 0 keep-unchanged with it; the retained record is never described as a v2 receipt |
| E1.5-6 matching partial resumes, divergent refuses | **MET** | C4/K1 resume; C5/K1b refuse at 31 |
| E1.5-7 P9 interruption: no partial record at the declared path | **MET** | K2: temp observed and left 0 B, no record at the path, rerun truthful; no all-or-nothing claim |
| E1.5-8 file-symbolic-link cases PASS or explicit UNRUN | **UNRUN** | Privilege unavailable on this host |
| E1.5-9 agent-commit route PASS or explicit UNRUN | **UNRUN** | No authority for that route in this slice |
| E1.5-10 identical completed rerun | **MET** | C6a 24, C6b 0 keep-unchanged; selected bytes and records unchanged |
| E1.5-11 stale-record/foreign-file observed | **MET** | C7a/C7b stale preserved, no fresh receipt; C8 foreign preserved at 20 |
| E1.5-12 out-of-scope cases named, never claimed | **MET** | Section 8 |
| E1.5-13 consumer wording requirements-only without T2 | **MET** | Section 7 |
| E1.5-14 historical v1/v2 evidence bytes unchanged | **MET** | Cited, not edited; v1 record `31005b7b...` unchanged in every case |
| E1.5-15 independent reviewer record with T6 status | **UNRUN** | Reviewer W7 not performed; T6 undefined (section 9) |
| E1.5-16 no closure/acceptance/implementation claim | **MET** | Section 7 |

## 7. What this record does not claim

No uninstall, downgrade, other version pair, other OS, second host, concurrent
writers, external-path transition, hosted deployment or real consumer repository
claim; no all-or-nothing guarantee; no claim that the old evidence is current; no
claim of a fresh record without an actual v2 record; no claim that the retained v1
record is a v2 receipt; no contract-conforming display claim (T2 is undefined, so
consumer-facing refusal/recovery wording here is **requirements-only**); no
E1/E1.5 closure, acceptance, readiness or implementation claim. No page or test
file was edited by this slice.

## 8. UNRUN and out-of-scope

- **File symbolic link at the record path (FSL)**: administrator privilege or
  Developer Mode is unavailable; no policy was changed.
- **Agent-commit route (AC)**: not authorized in this slice.
- **Independent review (W7)**: not performed.
- Out of scope and never claimed: uninstall, downgrade, other version pairs, other
  OS or second host, concurrent writers, external-path transition, hosted
  deployment, real consumer repository or J1.
- The section 7.3 wrapper was not executed (interactive); its preconditions were
  checked and recorded as described in section 3.

## 9. Reviewer status

Reviewer **W7 is not performed** in this slice. No independent record exists, so
the disposition of this transition record is **UNVERIFIED / PROPOSED**, not
verified. T6 is undefined; a reviewer disposition cannot be called verified
without it. Nothing here is self-approval and nothing confers merge, closure or
acceptance authority.

## 10. Limits

One Windows host, point-in-time, at
`701ebc7c3cee83058afb437ad911bc9f2ca8d8cb`. Any later change to the page, the
P2/7.1/7.3 blocks, the installer, the pin or the record guard voids these cells and
requires re-measurement and re-execution of the affected cases.
