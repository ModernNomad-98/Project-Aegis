# Consumer install, verify, repair and upgrade lifecycle - v1 design

**Status:** design-first page for the **Consumer install / verify / repair / upgrade lifecycle** slice of the Aegis Maturity Package item **Consumer Packaging Manifest and Read-Only Verification** (plan row P-11; closure CL-15). **Base:** main `e99fa451cbd214a3155e07330436b3c87907e78a`, tree `f83e3153b6a107a38cae5f068b8c17690e084745`. **Scope:** this page plus new executable preservation tests. **It adds no verb, no installer code and no capability.** No install target is exercised by this slice, and the consumer install record remains **UNRUN**.

**Reading key.** *Role A* is the Project Aegis source library; *Role B* is a consumer/product repository that copies Aegis files into its workspace. **UNRUN** means not executed, with the exact remaining action named; it is never a pass. *Fail-closed* means the operation refuses and leaves the previous state intact. *Preservation invariant* is a property that must hold after every accepted, refused or interrupted operation.

## 1. Purpose and non-goals

The read-only verifier slice is merged (`docs/design/distributed-payload-manifest-v1.md`; `tools/distributed_payload/`). It answers "do these payload bytes match this manifest?" and deliberately does nothing else. The remaining lifecycle questions - what a consumer may install, what a refusal looks like, what happens when a run is interrupted, and how an install is upgraded - had no single design page. This page supplies it.

**In scope:** the lifecycle model (states and transitions), the accepted and refused path for each of install / verify / repair / upgrade, the preservation invariants that make skill loss impossible by construction, the negative and interruption cases, and executable tests for the cases the shipped code can actually decide.

**Out of scope, deliberately:**

- no installer, updater, repair or prune command is written or executed here;
- no consumer repository is chosen and no consumer install record is produced (that requires the owner target decision referenced by plan row P-11's route; closure CL-16 tracks the owner record);
- no change to `docs/consumer-starter-package.md` (the documented procedure this page reasons about is read-only input);
- no claim about macOS or Linux behaviour, no CI wiring, and no approval, merge or delivery.

## 2. Verified starting state

Every row is a fact checked at the base commit, with its evidence. Rows marked *documentary* are claims read from a repository document that this slice did not execute.

| # | Fact | Evidence |
| --- | --- | --- |
| F1 | The payload tool has exactly three verbs: `build`, `verify`, `check-manifest`. There is no install, repair, upgrade, uninstall, prune, cleanup or approve verb, and an unknown verb exits 2. | `tools/distributed_payload/__main__.py:93-123`; asserted by `tests/test_manifest.py::test_a09_cli_exposes_only_three_verbs` and by N-2 below. |
| F2 | `verify` opens target files read-only, has no write/delete/move/rename/chmod operation against the target, and reports findings instead of repairing them. | `tools/distributed_payload/verify.py:3-13`, `:121-123`, `:168-321`; asserted by `tests/test_verify.py::test_i04_no_mutation_for_clean_and_findings_runs` and N-3/N-4 below. |
| F3 | The only report write is an explicit `--report-out` destination outside the target root and outside the declared package directories; it is written to a same-directory temporary file, fsynced, then renamed over the destination, and the temporary file is removed in a `finally` block. | `verify.py:126-165`; interruption cases I-1/I-2 below. |
| F4 | A manifest build refuses an output path inside the payload root and validates before writing; the manifest is not part of any target tree. | `__main__.py:30-38`, `:56-62`; `manifest.py:469-484`. |
| F5 | The repository ships no installer, updater, repair or prune script at any path. | Filesystem search over the base tree for `install*` / `*install*.ps1` / `*install*.py` returned no hit; the only install surface is the documented procedure in F6. |
| F6 | `docs/consumer-starter-package.md` *documents* a Windows PowerShell 7 install procedure (P0-P9): it writes exactly 41 files (18 skill directories, `AGENTS.md`, `CLAUDE.md`) plus a consumer install record, and every check stops rather than warning and continuing. (documentary) | `docs/consumer-starter-package.md:454-465`, `:1511-1530`. |
| F7 | That documented procedure's exit codes are: 1 prerequisite, 20 foreign material, 21 unsafe source, 22 startup-file conflict, 23 unsafe destination, 24 unusable record path, 25 record not written atomically, 30 closure/count/eval material, 31 pin or byte mismatch, 32 missing sibling dependency, 40 wrong repository role, 41 owner record missing, 42 commit identity missing/owner-matching on the agent-commit route, 43 install mode or authorization unstated/unrecognised. (documentary) | `docs/consumer-starter-package.md:1513-1530`. |
| F8 | The documented v1->v2 transition re-runs the same procedure with a new record path: there is no updater, no downgrade engine and no in-place substitution of the old record; an already-existing skill directory carrying foreign material is refused at 20 and a differing byte at 31, before any write. (documentary) | `docs/consumer-starter-package.md:1532-1564`, `:1571-1587`. |
| F9 | The consumer install record is the consumer's own artifact, written by that documented procedure, with one row per installed file and a computed aggregate; this slice neither writes one nor runs the procedure. | `docs/consumer-starter-package.md:1923-1944`; plan row P-11 route ("actual consumer installation requires P-20 target decision"). |
| F10 | At the base commit, `docs/design/consumer-install-verify-repair-v1.md` does not exist (this page creates it); the closure re-derivation is in section 10. | Official closure form `captures/closures.ps1` CL-15; candidate-scoped re-derivation in section 10. |

## 3. Terms

| Term | Meaning in this page |
| --- | --- |
| **install** | Materialising the declared package files into a Role B target and writing a consumer install record. Documented (F6-F8), not executed in this slice. |
| **verify** | Read-only comparison of a target tree against a manifest; reports `ABSENT`, `CHANGED`, `CHANGED_TYPE`, `UNRECOGNIZED`. Implemented (F1-F3). |
| **repair** | Writing into the target to remove a finding (restoring a missing file, overwriting drifted bytes, deleting unrecognized content). **Not implemented in v1; refused by construction.** |
| **upgrade** | Moving from one package profile version to another. In v1 this is *only* a fresh install run with a new record path (F8); `verify` never performs it. |
| **consumer install record** | The receipt the documented procedure writes at a new path inside the consumer repository (default `docs/consumer-install-record.md`), recording mode, host, file set and aggregate (F9). |
| **skill loss** | Any removal, hiding, truncation, overwrite or unreadable replacement of a skill file, or a skill directory that stops being discoverable. |
| **preservation invariant** | A property that must be true after an accepted, refused or interrupted operation; each is numbered PI-n in section 7. |

## 4. Lifecycle model

States describe the *target*, not the caller's intent. Transitions are labelled with the operation that causes them and the authority it needs.

| State | Meaning |
| --- | --- |
| **S0 absent** | The target has none of the declared package files. |
| **S1 installed, unverified** | The declared files are present but no verify run has been recorded against this manifest. |
| **S2 verified clean** | A verify run over this target and manifest returned exit 0 (a findings state, not an approval). |
| **S3 verified with findings** | A verify run returned exit 1; findings are reported and nothing was repaired. |
| **S4 refused / blocked** | The last operation was refused (wrong role, unsafe path, unusable record, identity, etc.); the target is unchanged by that attempt. |
| **S5 upgraded** | A new profile version and a new install record were installed by a fresh run; the previous record is retained byte-unchanged. |

Transitions:

| From -> to | Operation | Authority required |
| --- | --- | --- |
| S0 -> S1 | install (documented procedure) | Owner-stated mode + owner authorization + identity rules (F6-F8); **not exercised here** |
| S1 -> S1 | install rerun with an existing record (`-AllowExistingRecord`) | operator-attested identical rerun; the record is left unchanged and its contents are not re-read (F7, code 25/24 semantics) |
| S1/S3 -> S2 | verify (clean) | none beyond running the read-only verifier |
| S1/S2 -> S3 | verify (findings) | none; findings are not repaired |
| S2/S3 -> S4 | any refused operation | the refusal itself; target unchanged |
| S1..S3 -> S5 | upgrade = fresh install run with a **new** record path | a **new** owner authorization for this transition; a v1 authorization is not reused (F8) |
| S3 -> S2 | *not available in v1* | would require repair, which v1 refuses; the accepted remedy is a fresh install run (S5) with conflict checks |
| any -> any | crash / interruption | no transition is claimed; section 9 states the crash windows |

**Verify never changes lifecycle state.** It is an observation: a clean run is exit 0 and a findings run is exit 1, and both leave the target byte-identical (F2, N-3). Only the documented install procedure creates S1/S5, and only a fresh install (not verify) can replace package bytes.

## 5. Accepted paths

### 5.1 Verify - accepted and implemented

Preconditions: a valid manifest (schema `aegis.distributed-payload-manifest/1`); an existing target directory; a target path chain with no symlink/reparse point; if `--report-out` is used, a regular-file destination outside the target root and outside the declared package directories.

Accepted outcome: exit 0 when every declared entry matches on `bytes`, `lf`, `sha256_raw` and `sha256_normalized`, and no content inside declared package directories is undeclared. Exit 1 is likewise an *accepted run* - it reports findings; it is never a repair and never an approval (F1-F3). The report carries no `approved`, `qualified` or verdict field (`tests/test_verify.py::test_a22_no_authority_artifact_in_output`).

### 5.2 Install - accepted path, documented and not exercised here

Preconditions follow the documented procedure (F6-F8): a Role B target (P1 must not see all four source-package landmarks); an explicit `-Mode` and the owner's exact authorizing words; a valid owner record and, on the `agent-commit` route, a parsable non-owner effective author and committer; a pinned source clone; a new record path that is a regular-file destination outside the package outputs and inside the target.

Accepted outcome: exit 0, the 41 declared files present, the consumer install record written at the chosen new path. **This slice does not run that procedure and does not produce that record** (section 11).

### 5.3 Repair - no accepted path in v1

Repair is not implemented anywhere in the repository (F1, F5). The verifier reports a finding and stops (F2); its own output says `repair: none` (`__main__.py:83`). There is no accepted repair path, no `--fix`, no `--force` and no implicit repair on a findings run.

The accepted remedy for S3 is **not** repair: it is either (a) a consumer-side decision to restore files from the pinned source, or (b) a fresh install run, which refuses foreign material (20), startup-file conflicts (22) and byte drift (31) before writing (F8). Adding a repair verb would require its own reviewed design, because it is the first operation that would write into a target.

### 5.4 Upgrade - accepted only as a fresh install with a new record

The accepted upgrade path is a re-run of the documented procedure with a new profile version and a **new** record path; the previous record is retained byte-unchanged (F8). There is no updater, no downgrade engine and no in-place record substitution. A target holding a foreign file in a selected skill directory is refused at 20, and a differing byte at 31, before any write (F8). `verify` never upgrades: a v2 manifest against a v1 target reports the new entries as `ABSENT` and leaves the target untouched (N-5).

## 6. Refused paths

Refusals are the lifecycle's safety surface: each one is fail-closed, and each leaves a stated state untouched.

### 6.1 Verify refusals (implemented, measured by N-3/N-6/N-7/N-9)

| Refusal | Observable | What stays unchanged |
| --- | --- | --- |
| Manifest unreadable, not JSON, unsupported schema, unknown/missing field, bad digest, unsafe path, duplicate, dependency error, manifest self-reference | `ManifestError`; CLI exit 2 | target bytes, and (with `--report-out`) no report is written |
| Target missing or not a directory | `ManifestError` (`target_missing` / `target_not_directory`); exit 2 | nothing is created |
| Target path chain contains a symlink/reparse point | `ManifestError` (`unsafe_target`); exit 2 | nothing is read through the link, nothing written |
| An entry's path component is a reparse point | finding `CHANGED_TYPE` and exit 1; the link is never followed | the link and its target are untouched |
| `--report-out` inside the target root, inside a declared package directory, equal to the manifest, an existing non-file, or under a missing parent | `ManifestError` (`unsafe_report_path`); exit 2 | no report, no overwrite of any skill or manifest byte |

### 6.2 Install refusals (documentary, F6-F8; not exercised here)

| Code | Refusal | Preservation effect stated by the document |
| --- | --- | --- |
| 1 | Prerequisite failure (no usable shell, missing source/target) | nothing written; the documented shell probe at the end of P8 is the one case stated as occurring after the 41 files are written, with no record |
| 20 | Foreign material in a destination skill directory | the exact offending file; nothing overwritten |
| 21 | Unsafe or missing source path | nothing written |
| 22 | Startup-file conflict (`AGENTS.md`/`CLAUDE.md` differ) | existing bytes unchanged |
| 23 | Unsafe destination path (junction/symlink/reparse point) | refused before any package or record write; a link swapped in later is still refused at 23 and no record is written |
| 24 | Record path cannot be used (exists, non-file, overlaps a package output, appeared after preflight) | refused before any package or record write; no new record |
| 25 | Record could not be written atomically | the unique temp file is removed; no partial receipt is readable; the message states the 41 package files are already written |
| 30 | Closure, count or eval-material failure | stops before/at the check; no repair |
| 31 | Pin or byte mismatch (including CRLF) | the exact file; existing bytes unchanged |
| 32 | Missing sibling dependency | the installed skill and the absent sibling; nothing written |
| 40 | Wrong repository role (all four source-package landmarks present) | nothing written |
| 41 | Owner record missing or incomplete | nothing written |
| 42 | Commit identity missing/owner-matching on the `agent-commit` route | nothing written |
| 43 | Install mode or owner authorization unstated, empty or unrecognised | nothing written; no package file copied |

### 6.3 Repair and upgrade refusals

| Attempt | Refusal | Evidence |
| --- | --- | --- |
| `install`, `repair`, `upgrade`, `uninstall`, `prune`, `cleanup`, `approve` as a payload-tool verb | argparse rejects the choice; exit 2; nothing is written anywhere | F1; N-2 |
| Verify with an expectation that a missing file be restored | the file is reported `ABSENT` and is not created | F2; N-4 |
| Verify with an expectation that drifted bytes be rewritten | the entry is reported `CHANGED`; drifted bytes remain | F2; N-4 |
| Verify with an expectation that unrecognized content be deleted | `UNRECOGNIZED` is reported and the bytes remain | F2; N-4 |
| Upgrade of a v1 target to a v2 manifest by running `verify` | the v2-only entries are reported `ABSENT`; no directory or file is created | N-5 |
| Upgrade with an existing record path | documented exit 24 before any package or record write | F7/F8 (documentary) |

## 7. Preservation invariants

### 7.1 Enforced by shipped code (measurable here)

- **PI-1 (no destructive operation in the verifier).** `verify.py` contains no `os.remove`, `os.unlink`, `os.rename`, `os.chmod`, `shutil` or `rmtree` operation against the target (F2; also asserted by the pre-existing test suite). The only `Path.replace` is the report temp-file rename outside the target (F3).
- **PI-2 (read-only target access).** Every target file is opened `"rb"` (`verify.py:121-123`); no target file is opened for writing, and no directory is created inside the target.
- **PI-3 (findings are observations).** A findings run leaves the target byte-identical; `UNRECOGNIZED` content is reported, never adopted, never deleted (`verify.py:252-290`; N-3/N-4).
- **PI-4 (declared scope only).** The verifier never claims ownership of the whole target: unrecognized scanning is confined to declared package directories, and content outside them is ignored (`verify.py:252-255`; pre-existing test `test_a16`).
- **PI-5 (report cannot overwrite a skill or the manifest).** `--report-out` is refused inside the target root, inside a declared package directory, at the manifest path, at an existing non-file, or under a missing parent (F3; N-6).
- **PI-6 (no partial record).** A report write goes to a unique same-directory temp file, is fsynced, then renamed; the temp is removed in a `finally` block, so an interruption leaves either no report or the previous complete report - never a partially written one (F3; I-1/I-2).
- **PI-7 (fail-closed refusal).** Every verify refusal occurs before any write; invalid input is rejected before target bytes are read beyond containment preflight (F2, F3; N-7/N-9).
- **PI-8 (no new write surface).** This design adds no verb, no flag and no code path that writes to a target. The design page and tests are the only additions (section 12).

### 7.2 Asserted by the documented install procedure (documentary; UNRUN here)

- **PI-9 (additive copy).** The procedure copies declared files into the target and refuses every conflict rather than overwriting: foreign material (20), startup-file conflict (22), byte drift (31), unsafe destination (23). It does not move, rename or delete skill bytes (F6-F8).
- **PI-10 (atomic receipt).** The install record is written create-new and atomically; on failure the temp file is removed and no partial receipt remains (25). An existing record is left unchanged, and its contents are not re-read (24 semantics) (F7).
- **PI-11 (record retention on upgrade).** A v1->v2 transition uses a new record path; the previous record is retained byte-unchanged, and the transition requires its own authorization (F8).

### 7.3 Why no skill loss is possible by construction

To lose a skill, some operation must delete, move, rename, truncate, hide or overwrite a skill file, or make its directory undiscoverable. Enumerate every write surface in the shipped package and the documented procedure:

1. **`build`** writes one manifest file at the operator-named `--out` and refuses a destination inside the payload root (`__main__.py:30-38`; F4). The guard constrains only the payload root and knows nothing about consumer trees: a consumer file - a skill file included - named directly as `--out` would be replaced. That direct call is an operator command outside the documented procedure (the first limit below), and the documented procedure never calls `build` against a consumer tree.
2. **`verify`** writes nothing unless `--report-out` names a destination; that destination is refused inside the target and inside package directories, and it is written atomically outside the target (F3, PI-5/PI-6).
3. **`check-manifest`** writes nothing; it prints a detached identity (F1).
4. **The documented install procedure** copies declared files only, refuses every conflict class before writing, and writes its record at a new path with create-new atomic semantics (F6-F8, PI-9/PI-10).
5. **There is no other verb, script or flag** in the repository that writes into a consumer tree (F1, F5).

No enumerated operation contains a delete, prune, move, rename or in-place package overwrite of skill bytes; every operation that could damage a skill is either absent (repair/prune/uninstall/upgrade-in-place) or refused before writing (20/22/23/31). A crash cannot leave a half-written skill: the copy is additive and the only non-additive write (the receipt) is atomic. Therefore, **within the enumerated surfaces, skill loss is not reachable by construction** - not merely "not observed". N-2/N-4/N-5/N-6/N-10 exercise the refusal and interruption paths and assert skill bytes and the skill file set are unchanged; I-1/I-2 exercise the receipt write.

**Limits of that claim (stated so it is not overread):**

- It covers the shipped package and the documented procedure. It says nothing about a third-party tool, an operator command run outside the procedure, a filesystem failure, or an OS-level deletion.
- The install procedure itself is **UNRUN** in this slice, so PI-9/PI-10/PI-11 are documentary invariants, not measured ones. Only the verifier invariants (PI-1..PI-8) are executable and were executed here.
- "No skill loss" is not "no skill drift": drift is detectable (exit 1) but is not repaired, and the design intentionally does not claim a repair capability.

## 8. Negative cases (executable)

These cases are implemented in the new module `tools/distributed_payload/tests/test_install_lifecycle.py` with fixtures under `tools/distributed_payload/tests/fixtures/lifecycle/`. Every target is materialised in a unique temporary directory; no repository file is written and no install target is touched. The last row (H-1) is a harness regression, not a lifecycle case: it keeps the executable suite from writing into the repository.

| ID | Case | Expected | Test |
| --- | --- | --- | --- |
| N-1 | The design page states the accepted paths, refused paths, preservation invariants, negative and interruption cases, and the UNRUN install record | page exists and carries the required contract terms | `test_n01_design_page_states_the_lifecycle_contract` |
| N-2 | Each lifecycle verb (`install`, `repair`, `upgrade`, `uninstall`, `prune`, `cleanup`, `approve`) is requested with plausible arguments | exit 2, `invalid choice`, target byte-identical, no install record created | `test_n02_lifecycle_verbs_are_absent_and_refuse_without_writing` |
| N-3 | A clean consumer-shaped package (skills under `.claude/skills/`) is verified | exit 0, no findings, `repair_available` false, mode `read-only`, target byte-identical | `test_n03_verify_accepts_a_clean_consumer_package_read_only` |
| N-4 | A skill file is deleted, another is drifted, a foreign file is added | exit 1 with `ABSENT` + `CHANGED` + `UNRECOGNIZED`; missing stays missing, drifted bytes stay drifted, foreign bytes preserved; target byte-identical | `test_n04_drifted_skill_tree_reports_and_never_repairs` |
| N-5 | A v2 manifest (one extra skill) is verified against a v1 target | only the new entries are `ABSENT`; no directory or file created; target byte-identical | `test_n05_upgrade_candidate_is_absent_and_never_materialised` |
| N-6 | `--report-out` names an existing skill file or a path inside the skill tree | exit 2, `unsafe_report_path`, skill bytes unchanged, no report created | `test_n06_report_destination_in_skill_tree_is_refused` |
| N-7 | The manifest is invalid but a report path is supplied | exit 2, no report written, skill bytes unchanged | `test_n07_invalid_manifest_refuses_before_touching_skills` |
| N-8 | The target root does not exist | `ManifestError` (`target_missing`), nothing created | `test_n08_missing_target_is_refused_without_creating_it` |
| N-9 | A report destination is a directory, the manifest itself, or under a missing parent | `ManifestError` (`unsafe_report_path`); nothing overwritten | `test_n09_report_destination_edge_cases_are_refused` |
| N-10 | Every refused lifecycle attempt is run against one skill-bearing target | the skill file set and every skill byte are unchanged after all attempts | `test_n10_refused_attempts_cannot_lose_a_skill` |
| H-1 | The harness's own CLI subprocess call and its scratch tree are exercised | the child command carries `-B`, so no bytecode is written under the repository; the scratch tree exists, is writable, and is 0o700 off Windows | `test_run_cli_passes_dash_b_to_the_cli_subprocess` |

## 9. Interruption cases

A crash is not a lifecycle transition. The question for each window is only: *what may exist afterwards, and is any skill byte at risk?*

| ID | Crash window | May exist afterwards | Invariant | Executable? |
| --- | --- | --- | --- | --- |
| I-1 | During the report write, before the rename (`fsync` interrupted) | no report at the destination; a same-directory temp file that the `finally` block removes | PI-6; target untouched | yes - `test_i01_interrupted_report_write_leaves_no_partial_record` |
| I-2 | During the report rename (rename fails) | the previous complete report, byte-unchanged; no temp left | PI-6; target untouched | yes - `test_i02_interrupted_report_rename_preserves_previous_record` |
| I-3 | During a verify read, before any report | nothing written; target unchanged | PI-2/PI-3 | pre-existing `test_a08_interrupted_verify_leaves_no_corruption` (process kill) |
| I-4 | During the documented install copy, before the receipt (documentary) | some declared files copied, no receipt; the run is resumable and every conflict is refused on the retry | PI-9/PI-10 | **UNRUN** - no install target exercised |
| I-5 | Between install copy and receipt write (documentary) | 41 files present, no receipt (codes 1/24/25 state that scope explicitly) | PI-10 | **UNRUN** |
| I-6 | During the receipt write (documentary) | the temp file removed; no partial receipt; previous record unchanged if one existed | PI-10 | **UNRUN** |

The I-1/I-2 tests are deterministic: they interrupt the write in-process rather than racing a process kill, so they do not depend on host timing.

## 10. Executable evidence and closure

Run from the candidate root:

    python -B -m unittest discover -s tools/distributed_payload/tests -p test_*.py -v

The pre-existing suite is 37 tests (3 host-limited skips); this slice adds **thirteen** new test methods in one new module - the twelve contract cases (N-1..N-10 and I-1/I-2) plus the harness-hygiene regression (H-1) - so the expected total is **50** tests with the same 3 skips. The observed result is recorded in the lane receipt, not in this page.

**CL-15 re-derivation.** The official closure form is `Test-Path -LiteralPath "$C/docs/design/consumer-install-verify-repair-v1.md"` where `$C` is the frozen main checkout (`captures/closures.ps1`, CL-15). Re-derived at this candidate, the same predicate is:

    Test-Path -LiteralPath "<candidate>/docs/design/consumer-install-verify-repair-v1.md"

and it returns `True` at the candidate. The official form still returns `False` at the frozen `main` checkout until this design page is delivered and merged; that is expected and is not a candidate failure.

## 11. Explicit non-claims and UNRUN register

- **No install target was exercised.** No consumer repository was chosen, created or written.
- **The consumer install record remains UNRUN.** No `docs/consumer-install-record.md` was produced; the target decision that would allow one is the owner gate referenced by P-11's route (CL-16 tracks the owner record).
- The documented install procedure (F6-F8) was **read, not executed**; PI-9/PI-10/PI-11 and I-4/I-5/I-6 are documentary and UNRUN.
- macOS and Linux behaviour is UNRUN; one Windows host is the measured environment.
- `mode` enforcement remains UNRUN (declared in the manifest, not compared).
- The verifier is offline and stdlib-only; no network, credentials or provider calls occur in this slice.
- A clean verify run is a findings state, not an approval, qualification or merge authority. This page grants no authority to install, merge, publish or release.
- No installer, updater, repair or prune code exists in this slice, and none is claimed.

## 12. Change discipline

- **No new verb without its own design and review.** Repair is the first operation that would write into a consumer target; it must not be added as a flag on `verify`. Its design would have to state, at minimum: what it may overwrite, how it proves it is not destroying consumer content, how it behaves on an interrupted write, and how it preserves unrecognized content.
- **Upgrade stays "a fresh install with a new record"** until a separately reviewed updater design exists (F8).
- **The install record stays opt-in and owner-gated.** A record is evidence of a run, not an approval, and this slice produces none.
- **Tests are additive.** New fixtures use a neutral `skills/` layout under `tools/distributed_payload/tests/fixtures/lifecycle/` and are materialised into `.claude/skills/` only inside temporary target directories. No nested `.claude/skills/` tree is committed to the repository: the skill validator treats a tracked nested tree as a hard error (`scripts/validate-skills.py:1546-1570`, `:1633-1639`), and the fixture layout keeps the root skills tree the only one.

## 13. Traceability

| Reference | Relationship |
| --- | --- |
| Plan row P-11 | This page and the new tests are its design-first slice; CL-15 is its closure. |
| `docs/design/distributed-payload-manifest-v1.md` | Normative design of the manifest and read-only verifier this page builds on; unchanged. |
| `docs/consumer-starter-package.md` | The documented install, exit-code and v1->v2 transition procedure this page reasons about; unchanged and not executed. |
| `tools/distributed_payload/` | The shipped tool whose read-only guarantees PI-1..PI-8 describe; unchanged code. |
| `docs/roadmaps/aegis-maturity-package.md` | Readable item name "Consumer Packaging Manifest and Read-Only Verification" and the program's preservation boundaries. |

**Timestamp:** 2026-11-08 (design-first slice; commands, test counts and hashes are recorded in the lane receipt, not in this page).
