# The starter installer's record guard — fail closed on an existing record, write atomically

**Item:** AEP3-I9, from the #966 gaps carried by the item 7 closeout.
**Status: LOCAL CANDIDATE.** Executed on one Windows host against a disposable
target tree. Nothing here is hosted CI, and no merge claim is made.

| Field | Value |
| --- | --- |
| Change commits | `44556a91` (record guard), `75a54a92` (this evidence page), and the R1/R2 and N1/N2 fix commits on this branch, the last of which carries this revision |
| Files | `docs/consumer-starter-package.md` (+177/-48), `docs/evidence/consumer-readiness/local-starter-record-guard.md` (+158/-0), `scripts/tests/test_validator.py` (+464/-4); 3 files, +799/-52 against base `e6947039` |
| Host | Windows, PowerShell 7, Git for Windows `sh`, Python 3 |
| Model | DeepSeek V4 Flash (configured route `deepseek-flash`, DeepSeek Harness); the serving model is not observable from inside the session |

## 1. What the installer does now

The runnable block under `### 7.1` of the page gained four things:

1. `[switch]$AllowExistingRecord` — the explicit resume switch issue #966 asks for.
2. A preflight refusal, after the record-path containment walk and before the
   first directory or package write: an existing `-RecordPath` stops the run at
   **exit 24** unless that switch is passed. This removes the observed C7 outcome
   (files installed, exit 0, no receipt) instead of re-labelling it. The same
   preflight refuses, at **24**, a record path that is an existing directory or
   another non-file under `-AllowExistingRecord`, and a record path that equals or
   contains one of the 41 package outputs. It also captures
   `$recordExistedAtPreflight` (`Test-Path -PathType Leaf`), which P9 requires
   before it may keep an existing record: a record file that appears after this
   point is refused at **24** with or without the switch, never silently skipped.
   A reparse point at `-RecordPath` never reaches these checks - the containment
   walk refuses it at **23**.
3. An atomic record write: P9 creates a unique create-new temp leaf
   (`<record>.<guid>.tmp`) in the record's own directory, passes that leaf
   through `Assert-DestinationPath` (a failure stops at **25**), opens it with
   `[IO.FileMode]::CreateNew` and `[IO.FileShare]::None`, flushes it, and
   renames it into place with `[IO.File]::Move(..., $false)`. A pre-existing
   `<record>.tmp` — a regular file, a hardlink or a symlink — is therefore never
   followed, truncated or consumed. A failed write removes the temp leaf (best
   effort) and stops at **exit 25**, leaving nothing new at `-RecordPath`.
4. Directory creation for the record is inside that same `try` block, so a
   directory-creation failure is **exit 25**, not the generic PowerShell exit 1.

Codes 23, 24 and 25 are in the section 7.2 table. P9 skips a write only when
`-AllowExistingRecord` is passed **and** the record existed as a regular file at
the preflight, so the `P9: install record already present, left unchanged` line is
reachable only on that documented identical-rerun path; a record file that appears
between the preflight and P9 is refused at **24** with or without the switch and no
new record is written (the package copy has already completed by that point). The
switch does not read or verify the kept record's contents, so its "identical
install" is the caller's attestation rather than an installer check. A reparse
point at `-RecordPath` is refused by the containment walk at **23** before any
record check runs, and is never followed.

## 2. Published block identity

Block = fenced body plus one trailing LF. Extraction is by heading with the same
fence logic the validator suite and the audit use.

| Block | At `e6947039` (base) | At `9b45b86a` (pre-fix head) | At this revision | Equal |
| --- | --- | --- | --- | --- |
| P2 gate | 6,493 B, sha256 `fd01fce7806c74e92f0fdf877c1cb58ed7704e8f24a316cccbce91b1dd7398ea` | same | same | **yes** |
| Section 7.1 harness | 21,977 B, sha256 `5b0393cc40ee7d2518299cff49e25a02f77aca970a4a6ce61d8c4bb061f0a0a0` | 23,366 B, 405 LF, sha256 `d00e886c5a1fb83d436e2055633094d46f1a85d1ef4da565b66466aa30384c48` | 25,942 B, 443 LF, sha256 `9f4a085a9c210d026735a73e8fe41eed16141337b66f86270857582f95068d8c` | **changed** |

The base identities reproduce the P2 and section 7.1 values item 6 and item 7
published (`destination-links-v1.md` section 1,
`ITEM7-FINAL-RECORD.md` section 2). That is the control that the extraction reads
the delivered blocks rather than a retyped copy. Exactly **2 of 9** fenced blocks
differ from the base: block #7 (the section 7.1 harness) and block #8 (the section
7.3 operator snippet). The R1/R2 fix changed only block #7; the N1/N2 fix changed
only block #7 again (25,638 B / 438 LF at `2e9d61d6` to 25,942 B / 443 LF here),
and block #8 plus the P2 gate are byte-identical to `2e9d61d6`. The other seven
blocks, including the P2 gate, remain byte-identical to the base.

## 3. Before and after, same cases

`evidence/prefix_behaviour.py` in the item workspace runs the original three cases
against the block extracted from `origin/main`; the validator suite runs every case
against the candidate block as committed. The R1/R2 cases were also run red against
the pre-fix block at `9b45b86a` before the harness was edited. The N1/N2 cases were
run red against the pre-fix block at `2e9d61d6` with an independent watcher probe
(workspace record `item9-n1n2fix/evidence/probe.py`, which creates the record when
the target's `.claude` directory appears): the switch case exited **0** with
`left unchanged`, and the junction case exited **23** while the page said 24. The
suite's S4-12..S4-15 reproduce the same branches with a deterministic `-Sh`
stand-in that writes the record at the end-of-P8 `sh` probe, so the mid-run branch
has no timing race in CI.

| Case | Pre-fix | Candidate |
| --- | --- | --- |
| Existing `-RecordPath`, second run on a completed target | exit **0**, record and target unchanged, `P9: ... left unchanged` | exit **24**, nothing written, record byte-identical |
| The same run with `-AllowExistingRecord` | exit **1**, `A parameter cannot be found that matches parameter name 'AllowExistingRecord'` | exit **0**, record byte-identical, no package write |
| A pre-existing regular file at `<record>.tmp` | exit **0**, record written, the `.tmp` file consumed | exit **0**, record written, the `.tmp` file byte-identical |
| A hardlink at `<record>.tmp` to an external file | exit **0**, the external file overwritten with record bytes | exit **0**, the external bytes unchanged, the link intact |
| A file symlink at `<record>.tmp` | **UNRUN** on this host (no file-symlink privilege); the write would follow it | **UNRUN**: the unique create-new leaf makes the old path irrelevant |
| Record directory cannot be created (a file at an intermediate component) | exit **1**, generic `New-Item` error, no record | exit **25**, no record, no temp, 41 package files |
| A directory at `-RecordPath` with `-AllowExistingRecord` | exit **0**, 41 package files, `left unchanged`, no receipt | exit **24**, nothing written |
| `-RecordPath` equal to `<target>/AGENTS.md` | exit **0**, 41 package files, no receipt | exit **24**, nothing written |
| A record file appears after the preflight, `-AllowExistingRecord` (N1) | exit **0**, `P9: ... left unchanged`, the appearing file kept, no receipt for this run | exit **24**, `install record appeared during the run`, the appearing bytes preserved, no temp, 42 files (41 package + the appearing record) |
| The same, without the switch | exit **24** | exit **24**, same message and preservation |
| A junction at `-RecordPath` itself (N2) | exit **23** (containment walk) while the page said a non-regular-file path was 24 | exit **23** with and without the switch, outside directory empty, page states 23 |

The R1/R2 red run is retained in the fix package
(`_A/work-package-3/item9-r1r2fix/evidence/logs/`); each case fails on the
pre-fix block at the assertion shown above and passes at this revision.

## 4. Validator suite

`python -P scripts/tests/test_validator.py` at this revision: **OK: 361**
gate self-test assertion(s), exit 0 (358 at `2e9d61d6`; three assertions added).
S4-12..S4-15 in the destination-links case add the mid-run record branch without
the switch, the same branch with `-AllowExistingRecord` (N1), the junction at
`-RecordPath` plus the page's 23 statement (N2), and the file-symlink form. The
earlier record cases from the R1/R2 fix remain: the unique temp leaf, the hardlink,
the directory-creation failure, the non-file switch refusal, the package-overlap
refusal and the switch-with-no-record write. The result of each case is in the fix
package; S4-15 (file symlink at `-RecordPath`) and the earlier file-symlink case
are **UNRUN** on this host because creating a file symlink needs administrator
privilege or Developer Mode, as in item 6 and item 7.

## 5. Other checks

| Check | Command | Result |
| --- | --- | --- |
| Skills validator | `python -P scripts/validate-skills.py` | **OK: 254** skill(s) valid, 0 warning(s), exit 0 |
| Markdown links | `check-markdown-links.py` over the CI page set (`git ls-files`, fixtures excluded) | 880 pages in 3 batches: 4,162 links, 1,135 anchors, **0 broken, 0 dead**, exit 0 |
| Whitespace | `git diff --check origin/main..HEAD` | clean, exit 0 |
| DCO | `python scripts/check_dco.py --range origin/main..HEAD` | **OK: 5** commits, all signed off, exit 0 |
| PR-body bound fields | `python -P scripts/ci/check_pr_body_skills.py --body-file` | **OK**, exit 0 |

## 6. Limits and UNRUN

- **No real process kill during the P9 write was measured for this record.** The
  unique temp plus rename means a partial file at `-RecordPath` cannot exist by
  construction; a kill between the temp write and the rename can leave a uniquely
  named `<record>.<guid>.tmp` that is never read as a record. A timed kill probe
  is left to the audit rather than claimed.
- **The file-symlink collision case (S4-14) is UNRUN** for lack of the
  `SeCreateSymbolicLinkPrivilege`/Developer Mode on this host; the ordinary-file
  and hardlink collision cases (S4-12, S4-13) run and pass. **S4-15**, a file
  symbolic link at `-RecordPath`, is UNRUN for the same reason; the directory
  junction form of that reparse point (S4-14) runs and exits **23**.
- **The mid-run branch is injected through `-Sh`.** S4-12/S4-13 write the
  appearing record from a `sh` stand-in at the end of P8 rather than from a second
  concurrent process; the watcher probe recorded in the N1/N2 fix package
  reproduces the same branch independently, so the fixture is not the only
  evidence for it.
- The section 7.3 completion rule, the v1-to-v2 transition and cases C1-C8 were
  **not** re-run: this change does not alter the package list, the pin, the
  aggregate or the P2 gate, and item 7's evidence record remains the measurement of
  that transition.
- The `agent-commit` route and an external record path beyond S4-6 remain as item
  6 and item 7 recorded them.
- Hosted CI is recorded in the pull request; only the jobs that actually ran are
  claimed.

## 7. Grant route

The only changed protected path is `scripts/tests/test_validator.py` (under
`scripts/`), so the PR is an AEGIS-APR-140 candidate; the two documentation
paths are unprotected and need no exception. The mapping and the pattern probe are
in `_A/work-package-3/item9-local/I9-STAGE-A.md`.
