# Destination-link containment: current-head support matrix (2026-11-11)

Status: **E1.4 current-head evidence record (PROPOSED; independent review not
performed).** It re-baselines the delivered item-6 guarantee - refuse unsafe
destination links, junctions and other reparse points before any package or
record write - to the current head `701ebc7c`, and records one Windows host's
native execution of the published section 7.1 harness at that head. It is not an
acceptance, closure, enforcement, mounted-coverage, second-host, macOS, Linux or
deployment claim. Every cell that was not executed is **UNRUN** and is named in
section 8; no UNRUN cell is presented as a pass.

The historical item-6 record [destination-links-v1](destination-links-v1.md)
remains the record of the delivered change at its own head and is **not edited**
by this pass. Its run is historical evidence, not current-head evidence: it was
bound to section 7.1 at **21,977 B** while the current block is **27,748 B**.

## 1. Binding

| Item | Identity |
| --- | --- |
| Source base | `701ebc7c3cee83058afb437ad911bc9f2ca8d8cb`, tree `8b3f15b16e75ef04b93c6938f725d660b08e13c0`, merge parents `7ea22f8c` + `3016c947`; branch `impl/e14-e15-current-head-2026-11-11` |
| Page | `docs/consumer-starter-package.md`, Git blob `cc4e5ba399311422acf3d05280422727b159ad39`, **147,728 B**, sha256 `47a6b7e46dd1c16138dd8e05c6f6b09a370b60b91bf8a4b301144520993c8484` |
| P2 gate block | **6,493 B**, sha256 `fd01fce7806c74e92f0fdf877c1cb58ed7704e8f24a316cccbce91b1dd7398ea`, page lines 554-658 |
| Section 7.1 harness block | **27,748 B**, sha256 `907dc8637d91a22d3569914570436bda12fdd2562fc509a3a60093fc3ebe272f`, page lines 915-1383 |
| Section 7.1 harness as executed | **27,747 B**, sha256 `0ae99429e9563f22fcfc1c2853b074fabb500455fc0db6605e2de44e7e87f1eb` (the fenced body written to `install-starter.ps1`, i.e. the block identity minus its single trailing LF) |
| Section 7.2 exit-code table | Present as a prose table at page line 1,511; the executed codes observed here are 20, 21, 22, 23 and 24 |
| Section 7.3 transition block | **2,074 B**, sha256 `9d4ae8e80da43f5d003faf83931b7d6e3786dff633c58a7ef78f2ecfc668679d`, page lines 1595-1613 (recorded because the plan binds it; not executed by E1.4) |
| Package pin | commit `ffb040c7a363648856475280646bbd142dfabe4e`, tree `88a5aee4ad928a49c2fb945032585843ec652da7` |
| Frozen constants | `AggSha fcff1124...b699`, `AggRows 41`, `AggBytes 5420` |
| Installer provenance | item-6 merge `2a7e9c064276baad1a45fe80f7b0acbf615f822b` (tree `7514484935a5e6993700b919ee7844ee7db2764f`, parents `8c4dc764` + `d66406c1`); the executed harness is the block published at `701ebc7c` |
| Historical item-6 record | [destination-links-v1](destination-links-v1.md), **10,983 B** LF, Git blob `d5b95bdc76b600b11a3294532edd99fddb4df473`, LF sha256 `e465f41280fe26a670e394c40bfa4f3c921be919c2c7235af85ef9b2b4011346`; unmodified at this head |

"Block" means the fenced body as the page publishes it plus one trailing LF, the
same convention both historical records used. The two harness identities above
are the same bytes: the block carries one LF that the driver does not write to
the script it executes. Both are recorded so the executed artefact and the
published block can each be checked.

**Reconciliation with the plan's draft basis.** The Stage A draft cited the
item-6 record as 11,132 B / sha256 `7d63a5e3...`. That is the record's CRLF
working copy (149 lines, so 149 bytes more than the LF blob). The committed LF
blob is 10,983 B / `d5b95bdc...`, and its LF sha256 is the value above. Both
identities describe the same unmodified file; the blob is the durable identity.

## 2. Host and fixture capability

| Fact | Value |
| --- | --- |
| OS | Windows 11, NT 10.0.26200, release 25H2, 64-bit |
| PowerShell | 7.6.6 |
| Git | 2.55.0.windows.5 |
| Python (driver and validator only) | 3.14.7 |
| Administrator | **False** (no elevation, no Developer Mode, no machine-policy change) |
| Directory junction | **available**: `cmd /c mklink /J <link> <target>` succeeds unelevated; `os.path.isjunction` true; observed reparse tag `0xa0000003` |
| Dangling junction | **available**: `mklink /J` to a nonexistent target succeeds and keeps the reparse attribute |
| File symbolic link | **UNRUN**: `mklink <link> <file>` exits 1, "You do not have sufficient privilege to perform this operation." |
| Directory symbolic link | **UNRUN**: `mklink /D` exits 1 with the same privilege message |
| Other reparse tags (volume mount point, cloud placeholder, AppExecLink, WOF) | **UNRUN**: no supported unelevated way to create them on this host; only tag `0xa0000003` was created and observed |

A fixture type the host cannot create is recorded as UNRUN, never as a passing
negative case.

## 3. Support matrix (rows)

| Row | Host / lane | In scope | State | Reason |
| --- | --- | --- | --- | --- |
| R1 | Windows 11 10.0.26200, PowerShell 7.6.6, Git 2.55.0.windows.5, Python 3.14.7 | yes | **executed** | The recorded host supplied by the owner decision "execute on available Windows host now" |
| R2 | a second Windows host | no | **UNRUN** | No second host was supplied or authorised; nothing is claimed for it |
| R3 | Windows PowerShell 5.1 lane | no | **UNRUN** | Not available on this host and not authorised |
| R4 | macOS | no | **UNRUN / out of scope** | The published containment statement is Windows-scoped; no macOS host exists for this programme |
| R5 | Linux | no | **UNRUN / out of scope** | Same reason; the page's limitation statement is Windows-scoped |
| R6 | hosted Windows CI / S4 lane | no | **UNRUN / out of scope** | Delivery-stage work; it is not a substitute for native evidence and was not run |

Out-of-scope rows are stated, not omitted. Each carries the same page, P2 and
section 7.1 identities as section 1; no out-of-scope row is claimed as supported.

## 4. Fixture results (R1)

Two independent passes were executed at this head: the first produced
`native-*.json`, and the finisher pass re-ran the same drivers and reproduced
every exit and inventory (`native-*-finisher.json`). "Target after" and
"External after" are no-follow inventories (files / entries) taken immediately
before and after the command. "Record" is the record file at `-RecordPath`.

| Fixture | Case | Exit | Target after | External after | Record | Verdict |
| --- | --- | ---: | --- | --- | --- | --- |
| F1 ordinary clean target | `clean-target` | **0** | 42 files / 81 entries (41 package + record) | 0 | written | **PASS** |
| F2 linked target root | `linked-target-root` | **23** | 0, unchanged | 0, unchanged | absent | **PASS** |
| F3 linked target ancestor (junction, then real `consumer/`) | `linked-target-ancestor` | **23** | 0, unchanged | 18 files / 28 entries, unchanged | absent | **PASS** |
| F4 intermediate junction at `.claude/skills` | `intermediate-skills-junction` | **23** | 1 reparse / 2 entries, unchanged | 0, unchanged | absent | **PASS** |
| F4b intermediate junction at a skill's `references/` | `F4b-references-junction` | **23** | 1 reparse / 4 entries, unchanged | 0, unchanged | absent | **PASS** |
| F5 dangling junction | `broken-junction` | **23** | 1 reparse / 2 entries, unchanged | 0, unchanged | absent | **PASS** |
| F6 record path through a junction | `record-path-through-junction` | **23** | 1 reparse / 1 entry, unchanged | 0, unchanged | absent | **PASS** |
| F7 ordinary external record path | `ordinary-external-record` | **0** | 41 files | 1 record at the declared path | written | **PASS** |
| F8 existing linked file leaf (file symbolic link) | `existing-file-symlink-leaf` | -- | -- | -- | -- | **UNRUN** |
| F8 supplementary: directory junction at a package leaf | `existing-leaf-junction` | **23** | 1 reparse / 4 entries, unchanged | 0, unchanged | absent | **PASS (supplementary only)** |
| F9 broken / unsupported reparse point | `broken-junction` (broken) | **23** | unchanged | unchanged | absent | **PASS for a dangling junction; UNRUN for other tags** |
| F10 conflicting startup file | `F10b-conflicting-agents` | **22** | 1 file, unchanged | 0, unchanged | absent | **PASS** |
| F10 foreign material in a destination skill directory | `F10a-foreign-skill-file` | **20** | 1 file, unchanged | 0, unchanged | absent | **PASS** |
| F10 source reparse segment | `F10c-source-reparse` | **21** | 0, unchanged | 0, unchanged | absent | **PASS** |
| F11 identical resume | `F11-first-install` / `F11a` / `F11b` / `F11c` | 0 / **24** / 0 / 0 | see section 6 | unchanged | see section 6 | **PASS with the current record-guard behaviour** |

Refusal text is the published contract's, for example
`exit 23: destination reparse point (Junction -> ...\external): ...\linked-target; refusing before any write`.

## 5. What each refusal proves

Every 23 refusal above is emitted by the containment preflight, after P2 accepts
and before P6 creates a directory or copies a file, and before P9 writes the
record:

- the message names the exact path and the link type and target;
- the target inventory is byte-for-byte identical before and after (only the
  pre-existing junction entry is present);
- the external tree behind the link is unchanged, including F3's 18-file control;
- no record file exists at the declared path afterwards.

So the "before any write" claim is supported by inventories, not only by the
message. F6 additionally shows that a reparse point at `-RecordPath` is refused at
23 rather than being reported as a record problem. F7 shows the documented
caller-selected contract still works: an ordinary external record is written at
the declared path with 41 package files in the target.

## 6. Controls and the current record-guard behaviour

| Case | Exit | Observed |
| --- | ---: | --- |
| F10b conflicting `AGENTS.md` | **22** | file named, bytes preserved, no package write, no record |
| F10a foreign file in a destination skill directory | **20** | `.claude/skills/code-reviewer/notes.txt` named, bytes preserved, no record |
| F10c reparse point in the source worktree | **21** | `reparse-point source segment` named, nothing written |
| F11 first install | **0** | 42 files (41 + record); record 7,025 B, sha256 `4e2dc41341241c47c18fa9a8b55bb183673cb267ebff8efcad828d7d02650db5` |
| F11a rerun, same `-RecordPath`, no switch | **24** | `install record already exists ... nothing was written`; record byte-identical |
| F11b rerun with `-AllowExistingRecord` | **0** | record byte-identical, package files unchanged |
| F11c rerun with a second, nonexisting declared record | **0** | 43 files; second record 7,025 B, sha256 `a9ecd4f08d11c38d4d622eb580d331d5dd1f5a12b442b084289d93678498257a`; first record unchanged |

The historical item-6 record reported F11's second run as exit 0 (resume). At
this head the record guard refuses an existing `-RecordPath` with **24** unless
`-AllowExistingRecord` is passed; this record reports the current behaviour and
does not carry the older result forward.

## 7. Repository regression at this head

Command (from the worktree root):

```text
python scripts/tests/test_validator.py
```

Result: **OK: 375 gate self-test assertion(s) passed**, exit **0**. The
destination-link cases ran against the published blocks at this head:
S4-1 (clean target), S4-2 (linked target root), S4-3 (intermediate junction at
the 38th package row), S4-4 (dangling junction), S4-5 (record path through a
junction), S4-6 (ordinary external record), S4-7 (conflicting `AGENTS.md`),
S4-8 (identical resume), S4-8b and S4-10/S4-11 (existing record and
`-AllowExistingRecord`), S4-19/S4-20 (record appearing after the preflight),
S4-21/S4-23 (junction at `-RecordPath`, including one swapped in after the
preflight), and S4-12, S4-13, S4-15..S4-18 and S4-25 (record-temp and
record-path contracts) all **PASS**. S4-9, S4-14, S4-22 and S4-24 - the four
file-symbolic-link sub-cases (a leaf at the destination, a leaf at
`<record>.tmp`, the record path itself, and one swapped in after the preflight)
- are **UNRUN** with the privilege message and are not counted as passes. Six
unrelated Linux/POSIX cases are reported UNRUN in the same suite
("Linux POSIX lane unavailable" / "POSIX sh not available on this host"), so the
suite reports ten UNRUN skips in total and no failure.

The suite count is executed, not assumed: the item-6 record reported 350 at its
head and the record-guard record 361; this head reports **375**. No assertion was
removed or weakened by this pass - it changes no test.

## 8. UNRUN and limits

- **File symbolic-link leaf and file symbolic link at a record path**: creating a
  file symlink needs administrator privilege on this host; no policy was changed.
  The supplementary directory-junction-at-a-leaf fixture is not a substitute and
  is labelled supplementary.
- **Directory symbolic link**: same privilege constraint.
- **Other reparse types** (volume mount point, cloud placeholder, AppExecLink,
  WOF): not created; the check refuses any reparse attribute, but only junction
  tags `0xa0000003` were observed natively.
- **Exit 25 (atomic-write-failure / record-guard branch case)**: the required case set's exit-25 code was **NOT executed** on this host; there is no captured exit-25 observation and no claim about atomic-write-failure semantics. Disposition: **UNRUN**, not PASS. Adding a passing exit-25 case would require an authorised fault-injection/atomic-write test; none was authorised here.
- **Concurrent replacement (TOCTOU)** of a checked directory between preflight
  and copy is not detected by this record. The guarantee is the inspected,
  quiescent tree, as the page states in its limitation sections; it is not a
  security boundary and no immunity is claimed.
- **Second Windows host (R2), Windows PowerShell 5.1 (R3), macOS (R4), Linux
  (R5), hosted CI (R6)**: not run; out of scope as stated in section 3.
- **Mount/enforcement coverage (T5)**: UNKNOWN; no enforcement or mounted-coverage
  claim is made.
- **A real consumer repository and J1**: not used; every fixture is disposable.

## 9. Non-claims

No product, installer, page, test, P2, section 7.1 or section 7.3 change was made
by this pass. No E1 or E1.4 acceptance or closure is claimed. No cross-platform,
second-host or universal-containment claim is made. No enforcement claim is made.
The historical item-6 record and its block identities are unchanged and are not
presented as current evidence.

## 10. Evidence files (not committed; each identified by bytes and SHA-256)

Workspace: `_A/work-package-3/item6-matrix-2026-11-11/evidence/` (local, same
disk, outside Git). The committed record does not depend on opening these paths;
a reviewer can check a supplied copy against the identities below.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `binding-e14e15.json` | 5,908 | `2434ac9e01ca87196c20b1e9266b88c2b5ab8b0570d8148c4a154cff66cfcde9` |
| `dest_link_fixture_driver.py` (recorded item-6 driver, unchanged) | 13,633 | `dcc72b3df3d0b561475779fa617c365718c2294c45eee2c38a21b7e32359f78f` |
| `extra_fixtures.py` (F4b/F10b/F10c/F11 + capability probes) | 13,416 | `8b1f3de29adae33549bf58771cf30b1bd0dec538878d33e66bc2b1a810960e20` |
| `extra_fixtures2.py` (F10a foreign file) | 4,724 | `30abe728f5a8a1520161b62d89493c78d5aea3c618885539c3f96c5fd3f65227` |
| `measure_binding.py` | 5,280 | `b2aeeab143db18ad09c20b28bfb6f828837f1ccf60d817099ba2babde02eb78b` |
| `extract_blocks.py` | 1,823 | `604ebbbb6a18d15235f7f227e35da7e32453d71342ea16379030b4ab25fb7a86` |
| `blocks/install-mode.ps1` | 6,493 | `fd01fce7806c74e92f0fdf877c1cb58ed7704e8f24a316cccbce91b1dd7398ea` |
| `blocks/install-starter.ps1` | 27,748 | `907dc8637d91a22d3569914570436bda12fdd2562fc509a3a60093fc3ebe272f` |
| `blocks/transition-7.3.ps1` | 2,074 | `9d4ae8e80da43f5d003faf83931b7d6e3786dff633c58a7ef78f2ecfc668679d` |
| `native-f1-f8.json` (first pass) | 10,529 | `f81830f5344158aaec10ac12b24c0c81eda1c318996b9fe458279613f010bd31` |
| `native-f4b-f11.json` (first pass) | 12,705 | `6b81820336eeb9f964cc0baf1089a9942bc9f4352839bb58539ef7367710818c` |
| `native-f10a.json` (F10a, first pass) | 1,673 | `ce79fcd20e7ce3ca5c8e165a607c824267b6108fdfc617105b5e723d6e4957dd` |
| `native-f1-f8-finisher.json` (reproduction pass) | 10,525 | `f9371adeefa994aeb246b9187f1d01030f77f9503df9262f166268aee2168dd6` |
| `native-f4b-f11-finisher.json` (reproduction pass) | 12,840 | `f911e52f120a713027bf27be3d99407119ff1e0ab593b1eb43ad41b6bd631a9b` |
| `native-f10a-finisher.json` (F10a, reproduction pass) | 1,673 | `ce79fcd20e7ce3ca5c8e165a607c824267b6108fdfc617105b5e723d6e4957dd` |
| `validator-suite-current.log` | see note | suite transcript; the summary line is `OK: 375 gate self-test assertion(s) passed.` and `EXIT=0` |

`validator-suite-current.log` grows with each run and is identified by its
summary line rather than a stable byte count; the command and its result are
reproducible at this head.

## 11. Deviations recorded in this pass

- The Stage A draft's expected F11 result (second run exit 0) predates the
  record guard; the observed current behaviour is 24 without the switch and 0
  with it (section 6). This is a recorded behavioural change, not a failure.
- The draft's F8 expected a file symbolic-link result; this host cannot create
  one, so the cell is UNRUN and the directory-junction-at-a-leaf case is
  supplementary only.
- One supplementary invocation was discarded: it passed a relative `--workroot`
  to `extra_fixtures.py` and every case returned exit 1 because the extracted
  harness could not resolve the relative source path. That is a driver-invocation
  error, not an installer result; it was re-run with an absolute workroot and the
  results in section 4 come from that run. No partial output from the discarded
  invocation was retained.

## 12. Independent review (W6)

Not performed. No separate reviewer has re-derived this matrix, and T6 (the
authentication method for independent verdicts) is undefined, so this record's
disposition is **UNVERIFIED / BLOCKED** rather than verified. A reviewer must
bind to the identities in sections 1 and 10, re-count the case results and the
suite, and record its own PASS/REVISE/BLOCKED/UNRUN disposition. Nothing in this
record may be presented as independently verified before that happens.

**Recorded by:** E1.4/E1.5 finisher (DeepSeek Harness; route deepseek-flash;
serving model not observable). Local record only; no secrets.
