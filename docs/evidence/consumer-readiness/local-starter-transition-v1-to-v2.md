# Consumer starter transition: v1 (39 files) to v2 (41 files)

Status: **LOCAL ACCEPTANCE PASS for the `human-only` route on one Windows host,
not independently verified from the repository; `agent-commit` and the
file-symbolic-link leaf are UNRUN.** This record covers AEP3
work item 7, "Prove the bounded 39-file to 41-file starter transition". It was
produced against the accepted Item 6 installer after PR #964 merged, so the
destination-containment preflight and the section 7.1 harness it re-extracts are
the delivered ones. It is not a claim for another host, another version pair, a
downgrade or concurrent writers; the retained UNRUN items are named in section
10.

Model: DeepSeek, configured route `deepseek-flash` (DeepSeek V4 Flash); the
serving model is not observable from inside the session, so no observed-model
claim is made.

## 1. Binding

| Item | Identity |
| --- | --- |
| Accepted main base | `2a7e9c064276baad1a45fe80f7b0acbf615f822b`, tree `7514484935a5e6993700b919ee7844ee7db2764f`, merge parents `8c4dc764` + `d66406c1` |
| Package pin | `ffb040c7a363648856475280646bbd142dfabe4e`, tree `88a5aee4ad928a49c2fb945032585843ec652da7` |
| Page before this record's change | `docs/consumer-starter-package.md`, **118,444 B**, sha256 `36547d9a906c9feec9afa337815f3ab655168b01a28256ca42609ad12d44700b` |
| Page after the section 7.3 insert and review revisions | **128,940 B**, working-file sha256 `2401ba34acd8d88fd5529859df62b20be7d877156fd27726c502528180bfbbf4` |
| Published P2 block (**unchanged**) | **6,493 B / 105 LF**, sha256 `fd01fce7806c74e92f0fdf877c1cb58ed7704e8f24a316cccbce91b1dd7398ea` |
| Section 7.1 harness (**unchanged**) | **21,977 B / 385 LF**, sha256 `5b0393cc40ee7d2518299cff49e25a02f77aca970a4a6ce61d8c4bb061f0a0a0` |
| Frozen constants | `PinCommit ffb040c7`, `PinTree 88a5aee4`, `AggSha fcff1124...b699`, `AggRows 41`, `AggBytes 5420` |
| Host | Windows 10.0.26200 (64-bit); PowerShell 7.6.6; Git 2.55.0.windows.5; Python 3.14.7 |
| Native runner | `_A/work-package-3/item7-final/evidence/scripts/run_transition.py` (local, not committed; the scripts and logs are retained in the local evidence package). This is therefore a **local, self-attested acceptance**: the committed record summarises the run, and the script manifest below lets a supplied copy be checked, but the repository alone cannot reproduce the PASS |

| Script (local) | Bytes | SHA-256 |
| --- | --- | --- |
| `run_transition.py` | 12,495 | `30c621fd1ad091f1247278ef435b2c29e3ff30c055b6c08b7edc4363af481c2f` |
| `transition_lib.py` | 4,412 | `732bb1bd6bf73d492a7cedd7473b450a5fd5a810a14bdb6a35fbbc8631a0ba41` |
| `verify_matrix.py` | 7,697 | `4f19f6d48bd28f1a08f36630400f18101522f8eb4082ac4a1bb379eaab049f03` |
| `block_identity.py` | 3,716 | `25e163df1d6264069f1dcd49f458aed56ea58397191e9d4255215226c3386d1e` |
| `verify_native.py` | 14,406 | `ee63f9e9f993f68b472667e01a05eef5501f82ff2093f1dbf638e8c55ebd4e18` |
| `kill_native.py` | 7,953 | `848602698fcbeef40b89b26e46c2f3c7c57be410a86e5cbe714c9fc5a397b450` |
| `extra_cases.py` | 4,927 | `23a64293951e58cb0562decb0b3a56aa96470bb4d271f3d7d5b73d4388692937` |
| `run_links.py` | 1,827 | `5b7cfa0273c1b0fea909e64a2bfc2c5735c405144770c8c2ca7136e63495dda9` |

These files and the logs are retained under
`_A/work-package-3/item7-final/evidence/` and are **not committed**; the hashes
and the published tables let a reviewer check that a supplied copy is the one used.


A "block" is the fenced body plus one trailing LF, the convention the earlier
install-mode and Item 6 records used. The P2 and 7.1 identities above reproduce
the Item 6 record's published values **exactly**, which is the non-circular
control that this extraction is the delivered block and not a copy.

The runner re-extracts both blocks from the ref it is given and fails closed
(`SystemExit`) unless all five constants match the frozen values. It ran
against `2a7e9c06` and did not fail closed. The check was exercised with a
local-only tamper commit (`28325e59`, not on this branch) that changed
`$AggRows` from 41 to 40: the runner exited **1** with
`post-I6 harness constants changed; re-freeze item7 before running: {... "AggRows": "40" ...}`
and ran no case.

## 2. Profile delta: same pin, 17 -> 18 skills

Both published evidence tables resolve to the **same** package pin
`ffb040c7`. Re-deriving every row from Git objects at that pin gives:

| Measure | v1 | v2 | Delta |
| --- | --- | --- | --- |
| Rows | 39 | 41 | **+2** |
| Bytes | 349,753 | 369,093 | +19,340 |
| LF bytes | 5,512 | 5,841 | +329 |
| Serialized bytes | 5,152 | 5,420 | +268 |
| Aggregate SHA-256 | `0c885bcd...a5a7` | `fcff1124...b699` | changed |
| Selected skills | 17 | 18 | **+1** |

Set delta: **removed 0, changed 0, common identical 39/39, added 2**. The added
paths already exist at the same pin:

| Added path | Blob at `ffb040c7` | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `.claude/skills/scoped-approval-register/SKILL.md` | `c317530454301c32b1bd8a39f52ed968fa9c65f2` | 11,822 | `a74d2a22579cf93f737725aa0c54197b5d496a9f33a291a93c2cf2073cd7d076` |
| `.claude/skills/scoped-approval-register/references/register-format.md` | `8a20678755798334346d16fd41f8b404ea08c9b0` | 7,518 | `ace0fb62e81df2e0a7a28822c67426d23cd0938ee6cfa7cfa6665c41e80521b6` |

Because the v1 rows are a strict subset of the v2 rows, the transition rewrites
no existing package file: the only package writes are those two additions.

## 3. Starting fixture (assembled, disclosed)

The 39-file starting state was **assembled from the published pinned bytes**,
not replayed from a historical install: each of the 39 paths was written from
`git cat-file blob` at `ffb040c7` and every hash was checked against the v1
table. The historical Stage E v1 record was copied unchanged - **6,738 B**,
sha256 `31005b7b8b128ee4b800fb05d8e628056b44be460af4fc33a687b74846503f9a`,
39 rows. Four unrelated product files were planted (`src/acme_app.py`,
`docs/product-notes.md`, `README.md`, `.claude/settings.local.json`), the
fixture was Git-initialised with local owner records and one commit
`a3bc4a9436bcd191ef5fd8abd3e9da69fa26bbc6`, giving 44 files /
356,724 B before the run. This is disclosed, not presented as a re-executed v1
install; the original v1 evidence remains the v1 record.

## 4. Procedure

The transition uses the **same accepted installer and the same P0-P9 steps**,
with the current 41-file profile and a **new, nonexisting record path**. The
prescribed procedure never passes the old record path; C3 deliberately violates
that as a negative test, and C3/C7 exit 0 without satisfying the completion
rule. The clarification is published as
section 7.3 of `docs/consumer-starter-package.md`; P2 and section 7.1 are
byte-identical to the accepted main (section 1).

Command shape for each case (disposable copy of the fixture):

```text
pwsh -NoProfile -File <extracted-install-starter.ps1> -Src <pinned-worktree>
  -Tgt <case> -Sh 'C:\Program Files\Git\bin\sh.exe' -Mode human-only
  -OwnerAuthorization '<fixture owner statement>' -ModeGate <extracted-install-mode.ps1>
  -RecordPath <case>\docs\consumer-install-record-v2.md
```

## 5. Native transition results

All six cases ran against `2a7e9c06` with the extracted blocks. "Added" and
"changed" compare complete before/after file inventories (SHA-256 per file;
`.git` excluded).

| Case | Exit | Observed |
| --- | --- | --- |
| C1 - valid transition, fresh record | **0** | 41 package files; added exactly the two package files plus the new record; 0 removed, 0 changed; new record **41 rows, 7,025 B**, sha256 `d6db86a31c07e00b6f41cf0323ef5eeedb05740821ed0a1648bd959bbd246820`; old record hash unchanged; fixture commit and local Git config unchanged (config file sha256 `c4454039...f433`, `git config --local --list` identical) |
| C2 - conflicting selected file | **31** | `existing installed file differs from the pinned source: .claude/skills/code-reviewer/SKILL.md`; conflicting bytes preserved; no package write (empty delta); no record written; old record unchanged |
| C3 - reused old record path | **0** | 41 package files installed; `P9: install record already present, left unchanged`; the old record is still 39 rows / 6,738 B and unchanged; no "record written" claim |
| C4 - constructed matching partial (40/41) | **0** | resumed; added `register-format.md` and the fresh record; 41 package files; record 41 rows |
| C5 - constructed divergent partial (40/41) | **31** | `register-format.md` refused as a pin mismatch; divergent bytes preserved; no record written; no package write |
| C6 - identical completed rerun | **0** | no file delta; the existing 41-row record is left unchanged (same sha256 as C1) |

### 5.1 Additional refusal and stale-record cases

Two cases that the review asked to be explicit about were executed natively:

| Case | Exit | Observed |
| --- | --- | --- |
| C7 - stale record already at the new path | **0** | 41 package files installed; the stale 31-byte file was **left unchanged** (`P9: install record already present, left unchanged`); the new receipt was **not** produced. This is the observed footgun the page warns about: completion needs the 41-row / 5,420-serialized-byte / destination check in sections 9.1-9.2, not just exit 0 |
| C8 - foreign file in a selected skill directory | **20** | `.claude/skills/code-reviewer/notes.md` named on stderr, bytes preserved, no record, no package write |

Kill during P9 itself (a partial record at the new path) is **UNRUN**; the
stale-record consequence is what C7 observes. Atomic record write and a
fail-closed refusal of an existing `-RecordPath` would be installer changes
outside this documentation item and are not claimed.

The C1 record's parsed rows equal the published v2 path set in ordinal order,
and its rows independently aggregate to
`fcff1124d9d15e7d7230fd317350e0eb3b097b453bb6b911cdc1e2485525b699` over 5,420
serialized bytes - matching both its own header and the published value.

A 63-check assertion record over the case JSON, record text, real-kill runs and
published tables (`verify_native.py`) is **63/63 PASS**, including: the 39 published v1 paths are
byte-identical at the destination after C1; the four product files, the old
record, the commit and the local Git config are unchanged; C3 adds exactly the
two package files but produces no v2 receipt; C4's starting state is exactly 40
package files; C5 writes nothing.

## 6. Real process-kill interruption

The interruption method is a real process kill, not a simulated flag: the
runner starts the published harness, polls the destination, and calls
`TerminateProcess` when the defined boundary is reached. Three observed
outcomes cover both the matching and the divergent interruption case:

| Boundary | Kill result | Partial state | Rerun (unchanged command) |
| --- | --- | --- | --- |
| **40 of 41 package files** | process exit 1; observed count 40 | all 40 present package files byte-identical to the pin | exit 0; added `register-format.md` + the fresh record; final 41 files; record 41 rows / 5,420 bytes / published aggregate |
| 41 of 41, before P9 record write | process exit 1; observed count 41 | 41 files, all pin-identical; no record | exit 0; added only the fresh record; record 41 rows |
| **real divergent partial** | process exit 1; the last file existed at **0 bytes** | 41 paths present; `register-format.md` mismatched the pin (0 B vs 7,518 B); no record | exit **31**: `existing installed file differs from the pinned source: .../register-format.md`; bytes preserved; no record, no package write |

The 40/41 all-matching row is the acceptance case for an interrupted
**matching** copy. The third row is the interrupted **divergent** copy produced
by a real kill (not by C5's constructed state): the truncated file was detected
and preserved, and the run could not be counted complete. No rollback is claimed
and none occurred; each partial state is reported as it was found.

## 7. Destination-link containment (Item 6 fixture, re-executed)

Rather than invent a link fixture, this acceptance re-ran Item 6's accepted
repo test `test_consumer_install_destination_links` in
`scripts/tests/test_validator.py` at this head. It extracts the published P2
and 7.1 blocks itself and builds real `mklink /J` junctions:

| Fixture | Result |
| --- | --- |
| S4-1 ordinary clean target | exit 0; 41 package files + declared record |
| S4-2 linked target root | exit **23**, names the junction, external tree unchanged |
| S4-3 intermediate junction at the 38th package row | exit **23** before the first package write |
| S4-4 dangling junction | exit **23**, no traversal |
| S4-5 record path through a junction | exit **23** before any package or record write |
| S4-6 ordinary external record path | exit 0, record at the declared path |
| S4-7 conflicting `AGENTS.md` control | exit **22**, bytes unchanged |
| S4-8 identical resume | exit 0 with a **different** declared record path; 41 package files and the first record preserved; second record written |
| S4-9 file symbolic-link leaf | **UNRUN**: creating a file symlink needs administrator privilege on this host |

The full S4 test result is the table above; the validator suite summary is in
section 9. The
contract itself is Item 6's and is cited, not duplicated:
[destination-links-v1](destination-links-v1.md).

## 8. Historical bytes preserved

The v1 record Git blob `f16e720894a27f75d74ae188c6365f242dd9eb63` and the v2
record Git blob `dd63e7690ddca7d305949b11c1cbf7bfbdd28d1e` are unchanged at every
pin where each exists, including the accepted main. These are **Git object IDs**,
not working-file SHA-256 values; C1's generated v2 file hash `d6db86a3...` is a
different object (the committed example record's bytes). No v1 path is removed or
modified by the v2 profile, so v1 history is preserved by construction rather
than by a migration step.

## 9. Gates at the recorded head

| Check | Result |
| --- | --- |
| `python scripts/tests/test_validator.py` | **OK: 350** gate self-test assertion(s), exit 0; 7 UNRUN skips (six Linux-lane cases and S4-9 file-symlink) |
| `python scripts/validate-skills.py` | **OK: 254** skill(s) valid, 0 warning(s), exit 0 |
| Markdown link corpus (`check-markdown-links.py`) | **OK: 878** pages checked in 3 batches, exit 0 |
| `git diff --check` | clean (no whitespace errors) |
| DCO on the commits | signed off; verified with `scripts/check_dco.py` over `origin/main..HEAD` |
| PR-body bound fields (`check_pr_body_skills.py`) | OK on the draft and on the live body read back |

Hosted CI at `1b63544b`, `8fc806d3`, `844a1261`, `47336d06`, `79529ede` and
`9108cd51` completed with **all required checks green**: `gate-guard`, `validate-skills`, `changes` and both review-switch
jobs. Four DeepSeek review rounds and one Codex round posted 41 advisory findings;
all were read and dispositioned in the PR body. The documentation
findings are fixed in the commit that carries this record; the installer-
behaviour requests (atomic record write, a new fail-closed code for an existing
record path, testing `agent-commit`) are recorded as out of scope / **UNRUN**
rather than claimed. `tools-tests-linux`, `tools-tests-windows` and
`windows-offline-checks` were **skipped** by design for a docs-only change and
are UNRUN, never passes. This acceptance is bound to the page **working-file** sha256
`2401ba34...bf4` and the installer at `2a7e9c06`; a later page edit invalidates
it and requires a rerun. The commit that carries this record re-triggers CI;
that later run is delivery-stage evidence and is not claimed here.

## 10. UNRUN and limits

- **Other operating systems**, a second Windows host, a real consumer repository
  and J1 - not run here. Hosted CI itself ran at `1b63544b`, `8fc806d3`,
  `844a1261`, `47336d06`, `79529ede` and `9108cd51` (all required checks green);
  the commit carrying this record re-runs it.
- **Concurrent writers** and replacement of a checked directory between
  preflight and write - not covered; the guarantee is the inspected quiescent
  tree (sections 1.3 and 12 of the page).
- **Downgrade, arbitrary future versions, and other version pairs** - out of
  scope; this record proves only 39 -> 41 at the recorded pin.
- **File symbolic-link leaf** - UNRUN on this host (administrator privilege);
  only directory junctions were exercised natively.
- **Kill during the P9 record write** - UNRUN; a partial record at the new path
  would be left unchanged by a rerun (C7 observes the stale-record outcome).
  Atomic record writing is not implemented.
- **`agent-commit` transition route** - UNRUN; every accepted case used
  `human-only`. P2's identity contract is unchanged and not re-proven here.
- **A fail-closed refusal of an existing `-RecordPath`** - not implemented; the
  documented operator check and C7 are the current state. The installer-side
  remediation is tracked as [issue #966](https://github.com/ModernNomad-98/Project-Aegis/issues/966).
- **Review, CI and merge** - delivery-stage work; a PR is opened, not merged.
  Skipped or pending jobs are never counted as passes. Advisory review
  findings are dispositioned in the PR body, not silently absorbed.

## 11. Reproduction

From `_A/work-package-3/item7-final/evidence` (local, not committed):

```text
python scripts/verify_matrix.py --repo ../repo --history-pin 2a7e9c064276baad1a45fe80f7b0acbf615f822b --out-json matrix-verification-newmain.json --out-md matrix-generated-newmain.md
python scripts/block_identity.py --repo ../repo --ref 2a7e9c064276baad1a45fe80f7b0acbf615f822b --out-json blocks-main.json --out-dir blocks-main
python scripts/run_transition.py --repo ../repo --ref 2a7e9c064276baad1a45fe80f7b0acbf615f822b --fixture ../../item7-local/evidence/work/v1-consumer --work work/transition --force
python scripts/verify_native.py
python scripts/kill_native.py --repo ../repo --tools work/transition/tools --src work/pin-src --fixture ../../item7-local/evidence/work/v1-consumer --work work/process-kill-40 --ref 2a7e9c064276baad1a45fe80f7b0acbf615f822b --threshold 40
```

## 12. Aegis skills applied

| Skill and source revision | Actor / role | Purpose | How applied | Result, evidence, and limitations |
| --- | --- | --- | --- | --- |
| `change-classification-gate` - `.claude/skills/change-classification-gate/SKILL.md` at `2a7e9c06` | DeepSeek (deepseek-flash), item-7 final-acceptance agent | Classify and lock the delivered change | Classified the committed change as **docs-only** (one page section plus this record); declared scope to those two paths and confirmed the diff touches nothing else; no approval-required class, no workflow or skill change | Diff is 2 files, docs only; validation floor (links/rendering + review) met by the gates in section 9; the local fixture/runner is qa-test-only evidence outside the repository |
| `risk-tiered-validation-selector` - `.claude/skills/risk-tiered-validation-selector/SKILL.md` at `2a7e9c06` | DeepSeek (deepseek-flash), item-7 final-acceptance agent | Select validation depth from the changed file set | Classified changed paths: `docs/consumer-starter-package.md` and `docs/evidence/consumer-readiness/local-starter-transition-v1-to-v2.md` -> docs-only; no never-docs-only path (workflow, script, lockfile, agent-instruction, schema) is touched; aggregate tier = docs-only, but the repository's full validator suite was run anyway | No forced-full path in the final diff; the full suite result is in section 9. The temporary local scripts are not committed and do not raise the delivered tier |
| `release-readiness-reviewer` - `.claude/skills/release-readiness-reviewer/SKILL.md` at `2a7e9c06` | DeepSeek (deepseek-flash), item-7 final-acceptance agent | Evidence-not-vibes acceptance check | Built section 5-9 as an evidence table: every accepted case cites a command exit, an inventory hash, or an explicit UNRUN; verified the accepted installer identity (P2 and 7.1 block hashes) rather than assuming the merge | All nine work-item acceptance rows have native evidence or an explicit UNRUN; the destination-link row reuses Item 6's accepted test; review/CI/merge are delivery-stage UNRUN, not passes |

The work-item acceptance rows, mapped: exact starting fixture -> section 3;
valid transition -> C1; new receipt -> C1 (C6 only retains an existing
record on an identical rerun); product preservation -> C1;
conflicting selected file -> C2; reused old record path -> C3; interrupted
matching copy -> C4 and the real matching kill in section 6; interrupted
conflicting copy -> the real divergent kill in section 6 (C5 is the
deterministic constructed variant); identical completed rerun -> C6.
