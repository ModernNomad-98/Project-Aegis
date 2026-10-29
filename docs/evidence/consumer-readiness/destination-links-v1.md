# Destination link containment: native before/after evidence (2026-10-28)

Status: **Item 6 evidence record** for the owner-requested package work item
"Refuse unsafe destination links before installation writes". It records one
Windows host's native execution of the published section 7.1 harness before and
after the change, plus the repo regression that re-executes the published block.
It is not a consumer-readiness, second-host, macOS, Linux or deployment claim.
Every retained UNRUN is named in section 7.

## 1. Binding

| Item | Identity |
| --- | --- |
| Source base | `8c4dc7641a3f7e06613c6464cc10a9f234746bd3`, tree `822bce87b2b877b30e4aa223c3c4216070306741`, branch `aep3-i6/destination-link-containment` |
| Page before | `docs/consumer-starter-package.md`, **112,205 B**, sha256 `e5221836e8b5ea6f2b136f2e5c9a53e9a485de822ab11e77a7c5ceebda871627` |
| Page after (this revision) | **118,444 B**, sha256 `36547d9a906c9feec9afa337815f3ab655168b01a28256ca42609ad12d44700b` |
| Section 7.1 block before | **19,076 B / 321 LF**, sha256 `435c7b64db3cfb8df0645525422bc6781e60108a24f46c1327f997c516c91a6c` (the block the page published at the base) |
| Section 7.1 block after | **21,977 B / 385 LF**, sha256 `5b0393cc40ee7d2518299cff49e25a02f77aca970a4a6ce61d8c4bb061f0a0a0` |
| P2 block (unchanged) | **6,493 B / 105 LF**, sha256 `fd01fce7806c74e92f0fdf877c1cb58ed7704e8f24a316cccbce91b1dd7398ea` |
| Native fixture driver (local only) | `_A/work-package-3/item6-local/evidence/dest_link_fixture_driver.py`, **13,633 B**, sha256 `dcc72b3df3d0b561475779fa617c365718c2294c45eee2c38a21b7e32359f78f` |
| Raw before run | `evidence/pre-fix.json` (local), **11,333 B** |
| Raw after run | `evidence/post-fix.json` (local), **10,481 B** |

"Block" means the fenced body exactly as the page publishes it plus one trailing
LF, the same extraction convention the earlier install-mode record used. The
before block reproduces that record's published identity byte for byte, which is
the non-circular control for the extraction.

Paths under `_A/` are the local work area and are not committed; the commands
and outputs are reproduced here so this record does not depend on opening them.

## 2. Host and fixture capability

| Fact | Value |
| --- | --- |
| OS | Windows, 10.0.26200 (64-bit) |
| PowerShell 7 | 7.6.6 |
| Git | 2.55.0.windows.5 |
| Python (validator and driver only) | 3.14.7 |
| Directory junction | **available**: `cmd /c mklink /J <link> <target>` succeeds without elevation; `Get-Item` reports `LinkType=Junction`, `Attributes=Directory, ReparsePoint`; `fsutil reparsepoint query` reports tag `0xa0000003` (Mount Point) |
| Dangling junction | **available**: `mklink /J` to a path that does not exist succeeds; `Test-Path` returns true and `[IO.File]::GetAttributes` still returns `Directory, ReparsePoint` |
| File symbolic link | **UNRUN**: `mklink <link> <file>` returns 1 with "You do not have sufficient privilege to perform this operation." Developer mode is not enabled and no machine policy was changed |
| Directory symbolic link | **UNRUN**: `New-Item -ItemType SymbolicLink` returns "Administrator privilege required for this operation." |

A fixture type the host cannot create is recorded as UNRUN, never as a passing
negative case.

## 3. Before state: what the published harness accepted

Command (from `_A/work-package-3/item6-local`):

```text
python evidence/dest_link_fixture_driver.py --repo repo --label pre-fix   --rev 8c4dc7641a3f7e06613c6464cc10a9f234746bd3 --out evidence/pre-fix.json
```

Each fixture is a disposable zero-commit consumer repository (owner record and
commit identity both `Peter Nguyen <263130032+ModernNomad-98@users.noreply.github.com>`),
a worktree of `ffb040c7` as the source, and a fresh external directory outside
the target. "Files" excludes `.git` and never follows a reparse point.

| Fixture | Exit | Target after | External after | Result |
| --- | --- | --- | --- | --- |
| Ordinary clean target | 0 | 42 files (41 + record) | empty | expected success |
| Linked target root (`-Tgt` is a junction) | **0** | junction | **0 -> 41 files** | **gap**: every package file written into the external directory |
| Linked target ancestor (junction then real `consumer/`) | **0** | 41 files | 18 -> 59 files | **gap**: 41 package files written outside the nominal path |
| Intermediate junction at `.claude/skills` | **0** | 3 files (2 startup + record) | **0 -> 39 files** | **gap**: 39 skill files written outside |
| Dangling junction at `.claude/skills` | **1** | unchanged | empty | not a pass: raw PowerShell "Could not find a part of the path" |
| Record path through a junction | **0** | 41 package files | **0 -> 1 record** | **gap**: record written through the link |
| Ordinary external `-RecordPath` | 0 | 41 files | 1 record | allowed, as documented |
| Directory junction at a package leaf (`SKILL.md`) | **1** | unchanged | empty | not a pass: raw "Access to the path ... is denied." |
| File symbolic-link leaf | **UNRUN** | - | - | fixture unavailable on this host |

So the reproduced pre-fix behaviour is exactly the documented limitation: the
source chain was checked, the destination chain was not, and a link could
redirect writes outside the target - while returning exit 0 in three independent
topologies. A broken link and a junction at a leaf were refused only by an
unhandled PowerShell error (exit 1), not by the documented contract.

## 4. After state: refusal before any write

Command:

```text
python evidence/dest_link_fixture_driver.py --repo repo --label post-fix   --page repo/docs/consumer-starter-package.md --out evidence/post-fix.json
```

| Fixture | Exit | Target after | External after | stderr (abridged) |
| --- | --- | --- | --- | --- |
| Ordinary clean target | 0 | 42 files (41 + record) | empty | - |
| Linked target root | **23** | unchanged | unchanged (empty) | `destination reparse point (Junction -> ...external): ...linked-target; refusing before any write` |
| Linked target ancestor | **23** | unchanged | 18 files, unchanged | `destination reparse point (Junction -> ...external): ...ancestor; ...` |
| Intermediate junction at `.claude/skills` | **23** | 2 entries, unchanged | unchanged (empty) | `destination reparse point (Junction -> ...external): ....claudeskills; ...` |
| Dangling junction at `.claude/skills` | **23** | 2 entries, unchanged | unchanged (empty) | `destination reparse point (Junction -> ...externalmissing): ....claudeskills; ...` |
| Record path through a junction | **23** | 1 junction entry, unchanged | unchanged (empty) | `destination reparse point (Junction -> ...external): ...record-link; ...` |
| Ordinary external `-RecordPath` | 0 | 41 package files | 1 record at the declared path | - |
| Directory junction at a package leaf (`SKILL.md`) | **23** | unchanged | unchanged (empty) | `destination reparse point (Junction -> ...external): ...SKILL.md; ...` |
| File symbolic-link leaf | **UNRUN** | - | - | "You do not have sufficient privilege to perform this operation." |

The refusal in every linked case happens before P6 creates a directory or copies
a file and before P9 writes the record. The external inventories and the
internal inventories are identical before and after. The clean target and the
ordinary external record still succeed.

## 5. Acceptance mapping

| Required fixture | This run |
| --- | --- |
| Ordinary clean target | **Pass native**: exit 0, exactly 41 package files plus the declared record; external directory empty |
| Linked target root or existing ancestor | **Pass native**: exit 23 in both topologies; target and external inventories unchanged |
| Intermediate destination junction/link | **Pass native**: junction at `.claude/skills` and at one skill's `references/` both exit 23 before the first package write; the earlier package paths are absent afterwards |
| Existing linked file leaf | **UNRUN for a symbolic-link leaf** (administrator privilege unavailable). Supplementary: a directory junction at `AGENTS.md`/`SKILL.md` is refused at 23 without touching its target. This does not establish the symbolic-link-file case |
| Broken link or unsupported reparse point | **Pass native**: dangling `Junction` exits 23 with no traversal; no other reparse type can be created on this host |
| Install-record path through a link | **Pass native**: exit 23; 41 package files absent and the external directory unchanged |
| Explicit ordinary external record path | **Pass native**: exit 0, record at the declared external path, 41 package files in the target |
| Source-link and conflicting-file controls | Conflicting `AGENTS.md` still exits **22** with its bytes unchanged (repo test S4-7). The source-chain checks are byte-identical to the base block; no source-link fixture was re-run (**UNRUN** for source-link, see section 7) |
| Identical resume | **Pass in the repo test** S4-8: a second run exits 0, preserves the 41 package files and the first record, and writes the second declared record |

## 6. Regression harness

`scripts/tests/test_validator.py` gains
`test_consumer_install_destination_links`. It extracts the published P2 and
section 7.1 blocks exactly, builds the same junction fixtures with `mklink /J`,
asserts exit 23 with unchanged no-follow inventories, and keeps the clean
target, external-record, conflicting-`AGENTS.md` and resume controls. Assertions
are only added; none is removed or weakened. Run against the base page with
`STARTER_DOC` pointed at those bytes, the test fails on its first containment
assertion ("the published harness has no destination containment preflight";
local `evidence/red-before-test.log`). Against the fixed page the full Windows
suite is **OK: 350** (baseline **342**), exit 0; S4-1..S4-8 pass and S4-9 records
the file-symlink UNRUN. The first full-suite run failed at S4-8 because the test
compared an unfiltered baseline; the assertion was corrected to compare the 41
package rows rather than the record files, and the suite was re-run.

## 7. UNRUN and limits

- **File symbolic-link leaf**: creating a file symlink needs administrator
  privilege on this host; no policy was changed. The directory-junction-at-a-leaf
  supplementary fixture is not a substitute and is labelled accordingly.
- **Directory symbolic link**: same privilege constraint; only `Junction`
  reparse points (`0xa0000003`) were exercised.
- **Other reparse types** (mount point on a volume, cloud placeholder, AppExecLink)
  were not created; the check refuses any reparse attribute, but only junction
  tags were observed natively.
- **Concurrent replacement** of a checked directory between preflight and copy is
  not detected. The guarantee is the inspected, quiescent tree; this is stated in
  sections 1.3 and 12 of the page and is not presented as a security boundary.
- **Linux, macOS, a second Windows host, GitHub-hosted CI, a real consumer
  install and J1** were not run. CI and review are delivery-stage work, not this
  local preparation item.
