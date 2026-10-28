# Human-only installation: explicit install mode, native before/after evidence (2026-10-28)

Status: **Item 3 evidence record** for the owner-requested four-priority plan
(section 5, "Finish human-only installation without relaxing agent checks"). It
records one Windows host's native execution of the published P2 install-mode step
and the section 7.1 harness, before and after the change, plus the source
regression that re-executes the published procedure. It is not a
consumer-readiness, second-host, J1 acceptance or deployment claim. Every
retained UNRUN is named in section 7.

## 1. Binding

| Item | Identity |
| --- | --- |
| Source base | `482ba165a790c3a172d00771fa23474764dd916e`, tree `c8a251e21189aeb7ffb7621e380469a34f5a1f42`, branch `item3/human-only-install` |
| Plan | `_A/remediation/handshake/PLAN-HANDOFF-FOUR-PRIORITIES-2026-10-28.md` section 5 (independently audited: ACCEPT) |
| Procedure page, before | `docs/consumer-starter-package.md` at the base, **91,779 B**, sha256 `b9c015e5fec171e8a1b8328dbc4389195ecd7761cbb18302b639e96abbcdef4c` |
| Before P2 block | **657 B / 11 lines**, sha256 `ee0fb37aca29b3eada063eadf71b5c7c49c26ae1a6359f5fb69ff6d0fecc1a28` |
| Before section 7.1 block | **17,305 B / 294 LF**, sha256 `78f8a2f93bb46f274d6bc59027e69108bd1ebd416b9b0661d521a69c5753bf86` |
| After P2 block | **5,284 B / 91 LF**, sha256 `88db8dcce5245e458dfcca794a8c9dc03b1f2a89397643ddfd482f507376694d` |
| After section 7.1 block | **18,905 B / 318 LF**, sha256 `e63ca4a79577acbe1830d8efe36cde808d7a8b38be1e4529c7f5c31fbeb7e21d` |
| Extraction wrapper | `extract-block.ps1`, **1,798 B**, sha256 `159f9af86b05e752b903b1be0e4225a96e2aac892665452d2edd105554f8e047`; it reads the fence body plus one trailing LF and reports the span, size, LF count and hash |
| Retained v1 walkthrough wrapper | `install-step.ps1` from the v1 validation raw material, **14,477 B**, sha256 `1eb9174d87b68900671320666a8377be2bf81e5dbaa20ab54f56b9daeb1a7636`; its P2 branch is the implementation the v1 evidence record ran |
| Raw before log | `before-native.log`, **1,631 B**, sha256 `4c56aa012ba116b43bac325d88fcec5ab3ca83049d9789561bf2b77d128484cf` |
| Raw after log | `after-native.log`, **11,746 B**, sha256 `5747d4591a94b1a5821d35df9a2f91191e2d0f08f0d022eff44ab071f7834025` |

The extraction check is non-circular: run against the unmodified page, the
wrapper reproduces the page's own published v2 measurement of the section 7.1
block byte for byte (**17,305 B / 294 LF**, sha256 `78f8a2f9…bf86`). The same
wrapper then produces the before and after identities above.

The raw logs live under `_A/remediation/handshake/item3/` beside this work. Every
decisive command line and its output is reproduced below, so the record does not
depend on opening that folder.

## 2. Host and tools (measured in the run)

| Fact | Value |
| --- | --- |
| OS | Windows 11 Business, 10.0.26200 (UBR 9711), 64-bit |
| PowerShell 7 | **7.6.6** (`$PSVersionTable.PSVersion`) |
| Git | **2.55.0.windows.5** |
| POSIX `sh` | `C:\Program Files\Git\bin\sh.exe`; `& <path> -c 'echo ok'` printed `ok` |
| Python | 3.14.7 (validator self-tests only; the consumer install runs no Python) |
| Host agent | DeepSeek Harness, model **DeepSeek V4 Flash**; the evidence was produced by this agent, not by a human typing the procedure |

## 3. Before-state: the published procedure and its human-only stop (native)

Three native observations on the unmodified page. The fixture is a zero-commit
consumer repository whose **owner record and commit identity are the same solo
owner** (`Peter Nguyen` / `263130032+ModernNomad-98@users.noreply.github.com`) —
the normal solo-consumer case.

### B1 — the published P2 block, executed as written: no stop

The block is extracted verbatim and executed with only the documented `$TGT`
variable supplied; the wrapper adds no behaviour.

```text
COMMAND  pwsh -NoProfile -File before/b1-run-published-block-as-written.ps1
           -Tgt <solo-owner fixture> -Block before/P2-before.txt
RESULT   reached_end=yes block_stopped=no exit=0 (no exit statement executed)
EXIT     0
```

The exit-42 condition exists only in the block's comments (its last two lines);
the executable bytes never evaluate it. This is the plan's finding that P2
contains procedure comments rather than a complete standalone installer.

### B2 — the retained v1 walkthrough P2: exit 42

The wrapper the v1 evidence record used for this step (identity above) is run
unchanged against the same fixture:

```text
COMMAND  pwsh -NoProfile -File .../validation/raw/scripts/install-step.ps1 -Step P2
           -TGT <solo-owner fixture>
OUTPUT   author=Peter Nguyen <263130032+ModernNomad-98@users.noreply.github.com>
         committer=Peter Nguyen <263130032+ModernNomad-98@users.noreply.github.com>
         Git reports this repository's author and committer as
         "Peter Nguyen <263130032+ModernNomad-98@users.noreply.github.com>", which is
         the recorded owner. Should the agent commit under a different identity for
         this repository, or will you commit yourself?
EXIT     42
FILES    0
```

This reproduces the documented human-only dead end natively: a solo owner whose
Git identity is their own owner record cannot pass P2, although the decided
policy (package section 8.3) says the owner may commit as themselves. The
wrapper prints the v1 question wording; the documented stop condition and its
exit code are the ones in the page.

### B3 — the current copy harness: exit 0, so it cannot prove the branch fixed

The section 7.1 harness is extracted and run against the same solo-owner fixture
and a pinned source checkout (`ffb040c7`):

```text
COMMAND  pwsh -NoProfile -File before/harness-before.ps1
           -Src <pinned clone> -Tgt <solo-owner fixture> -Sh <Git sh>
           -RecordPath <fixture>/docs/consumer-install-record.md
OUTPUT   P8: count_check=PASS installed=41 extra=0
         P8: manifest_pins=PASS 18/18
         P8: source_pins=PASS 23/23
         P8: siblings=PASS absent=0
         P8: forbidden=PASS none
         P9: rows=41 serialized_bytes=5420 aggregate=fcff1124…b699
         P9: install record written: <fixture>/docs/consumer-install-record.md
         OK: 41 installed files; closure, pins, siblings, eval and aggregate checks passed
EXIT     0
EFFECT   42 files (41 package + record), 0 commits, 6,271 ms
```

The copy succeeds while the documented prerequisite would stop the same owner at
42. That is the plan's statement that the separate P5-P9 copy harness does not
enforce P2, and a successful copy run cannot prove this branch is fixed.

### Reconciliation

The stop **is** reproducible natively, but only through the walkthrough
implementation: the published P2 block is not executable as written (B1). The
record therefore does not invent a failing executable; it freezes the published
bytes, the retained v1 wrapper's bytes and its actual exit 42, and reports the
gap between the published comments and any runnable procedure as the defect the
change closes.

## 4. The change

- **P2 now publishes a runnable gate**, `install-mode.ps1`, saved from the P2
  block. It takes `-Tgt`, `-Mode` and `-OwnerAuthorization`; it reads the two
  identity records and states the mode; it writes nothing, makes no commit and
  runs no `git config` write. Exit codes: **0** accepted, **1** target unusable,
  **41** owner record missing, **42** identity missing/unparsable or an
  `agent-commit` attempt under the owner identity, **43** install mode or owner
  authorization missing, empty or unrecognised.
- **The section 7.1 harness runs the gate first.** It takes `-Mode`,
  `-OwnerAuthorization` and an optional `-ModeGate`, invokes the gate as a child
  process before it reads a source pin or writes a file, and exits with the
  gate's code. The install record now records the accepted mode and what it did
  or did not authorize.
- **The agent route is unchanged in effect**: an effective owner identity on
  `agent-commit` still exits 42 with the resolved values and exactly one
  question; a missing identity still exits 42; a missing owner still exits 41
  with the section 8.2 text.
- **The startup gate is untouched.** No file under `.claude/skills/` changed; the
  gate's own presence/owner check still exits 1 for an agent commit under the
  owner identity, and a `human-only` install makes no commit at all.
- **A later agent commit is re-gated** in the page's section 8.3: the same
  procedure must accept `agent-commit` with current authority, an effective
  non-owner identity and the mandatory provenance step, and every agent commit
  carries a DCO `Signed-off-by` trailer.

## 5. After-state: the six required observations (native)

Commands and results below are quoted from `after-native.log`. Unless stated,
the fixture is a disposable zero-commit Git repository; "files" counts every file
outside `.git`; "config" is the `git config --local --list` snapshot.

| ID and plain-English case | Observed result |
| --- | --- |
| **S3-1** — a valid human-only install succeeds with no agent commit or identity change | Gate exit **0**: `P2: mode=human-only owner_match=yes identity=not-recorded install_commit=none identity_mutation=none`; config hash unchanged; 0 commits; 0 files. Full harness exit **0**: 41 installed files, 18/18 manifest pins, 23/23 source pins, published aggregate, **42 files** including a **7,025 B** record, **0 commits**, config hash byte-identical, record's mode lines present and the owner's name/email absent from the record |
| **S3-2** — an authorized explicit non-owner agent route preserves the measured identity in an isolated fixture commit | Gate exit **0**: `P2: mode=agent-commit owner_match=no identity=Aegis Agent (DeepSeek V4 Flash) <agent@example.invalid>`; `git var GIT_AUTHOR_IDENT` starts with the same identity; an isolated `git commit -s` records `author=Aegis Agent (DeepSeek V4 Flash) <agent@example.invalid>`, the same committer, `Signed-off-by: …`, and the owner record still reads `Owner Person` |
| **S3-3** — owner identity used by an agent is refused before commit | Gate exit **42**, prints `author=…`, `committer=…` and the one question `Will an agent commit in this repository, or will you commit yourself?`; **0 commits**, **0 files**, config unchanged |
| **S3-4** — missing owner, unclear mode or malformed values refuse before package writes | Missing owner: exit **41** with the section 8.2 text, 0 files. No `-Mode`: exit **43**, 0 files. `-Mode human_only`: exit **43**, 0 files. No `-OwnerAuthorization`: exit **43**, 0 files; config and commit count unchanged. Malformed effective identity (`GIT_AUTHOR_DATE=not-a-date`): exit **42**, 0 files. The full harness with no `-Mode`: exit **43**, **0 files**, **0 commits** |
| **S3-5** — a later agent-commit proposal after a human-only install is re-gated | On the installed `human-only` tree with the owner identity: exit **42**, no commit. After the human states the distinct agent identity, the same gate exits **0**; a later signed commit carries that identity. The check itself makes no commit |
| **S3-6** — restoring the old contradictory branch makes the behavioral test fail | The published block contains exactly one mode branch, `if ($ownerMatch -and ($Mode -ceq 'agent-commit'))`. Replacing it with the old unconditional `if ($ownerMatch)` leaves the block parseable; the same human-only fixture then exits **42**, with 0 files and 0 commits, while the published block exits 0 on an identical fixture |

### Decisive output (quoted)

```text
S3-1 gate    P2: mode=human-only owner_match=yes identity=not-recorded
             install_commit=none identity_mutation=none                      EXIT 0
S3-1 harness P8: count_check=PASS installed=41 extra=0
             P8: manifest_pins=PASS 18/18
             P8: source_pins=PASS 23/23
             P9: rows=41 serialized_bytes=5420 aggregate=fcff1124…b699
             OK: 41 installed files; …                                     EXIT 0
             OBSERVED config_hash_before = config_hash_after_install
             OBSERVED commits_after_install=0  files_after_install=42  record_bytes=7025
             RECORD  - Install mode: human-only (owner-stated; …)
                     - Agent commit: none made by this install; no Git identity was written. …
             RECORD contains owner email: False   contains owner name: False
S3-2 gate    P2: mode=agent-commit owner_match=no
             identity=Aegis Agent (DeepSeek V4 Flash) <agent@example.invalid> EXIT 0
S3-2 commit  author=Aegis Agent (DeepSeek V4 Flash) <agent@example.invalid>
             committer=Aegis Agent (DeepSeek V4 Flash) <agent@example.invalid>
             Signed-off-by: Aegis Agent (DeepSeek V4 Flash) <agent@example.invalid>
S3-3 gate    author=Owner Person <owner@example.invalid>
             committer=Owner Person <owner@example.invalid>
             Git reports this repository's author and committer as "Owner Person
             <owner@example.invalid>", which is the recorded owner. Will an agent
             commit in this repository, or will you commit yourself?          EXIT 42
             OBSERVED commits_after=0  files_after=0  config_hash_unchanged=True
S3-4         exit 41 (missing owner); exit 43 (no mode); exit 43 (human_only);
             exit 43 (no authorization); exit 42 (malformed identity);
             harness exit 43 with files_after_harness_refusal=0
S3-5         installed tree + owner identity → EXIT 42, commits_after_refusal=0;
             distinct agent identity → EXIT 0; gate made no commit
S3-6         OBSERVED old_branch_matches=1; mutated block on the same fixture → EXIT 42
```

## 6. Source regression

Added to the existing dispatcher in `scripts/tests/test_validator.py` (protected;
AEGIS-APR-140 applies, and no existing assertion is removed or weakened):

- `test_consumer_install_mode_gate` (**S3-1** human-only success, **S3-2**
  non-owner route with a fixture commit, **S3-3** owner refusal, **S3-4** the four
  refusal classes, **S3-5** re-gating, **S3-6** old-branch mutation).
- `test_consumer_install_mode_native` (full published harness: human-only install
  with the record, the installed-tree re-gate, and a no-mode harness refusal with
  0 files).

The oracle is the published procedure itself: both fenced blocks are extracted
from the page and executed with `pwsh`, and the S3-6 control is the published
block with the old branch restored — not a second implementation and not a
keyword matcher. The harness's "before package writes" property is behavioral:
with no `-Mode` the harness exits 43 rather than the pin-check exit 31 it would
produce if pin checks ran first, on a dummy source directory.

Availability policy: an absent `pwsh`/Git/`sh` or a clone without the pinned
commit is UNRUN — a required failure on Linux (`AssertionError`), an explicit
`REQUIRED_SKIPS` entry on other hosts, never a pass. Linux closure therefore
remains nonzero when the case cannot run.

Local execution of this change (Windows, this host): both tests **9 PASS, 0
SKIP**; the full suite is recorded in section 9.

## 7. Retained UNRUN

| Item | Why it is UNRUN | Exact remaining action |
| --- | --- | --- |
| A Linux or macOS native run of the Windows-specific procedure | This record's host is Windows only; the procedure is documented as Windows PowerShell 7 specific | Run the same extracted blocks and harness on a capable POSIX host and record its own host facts |
| A real interactive owner session stating the mode | The fixtures pass the owner's words as literals; the gate cannot verify who typed them (a decision procedure, not a boundary) | Have a human run P2 in a real session and record the answer; no automation can prove authorship |
| A real consumer repository and the J1 journey | This item changes the installation prerequisite; it does not run J1 | Execute J1 in a fresh consumer repository and record the Stage 0/1 result |
| The 9 Stage E acceptance rows | They were UNRUN before this change and are not converted by it | As listed in [local-starter-v2](local-starter-v2.md) |
| The v2 negative fixtures (changed byte, eval material, conflicting `AGENTS.md`, missing reference) | P5-P8 bytes are unchanged by this item; they were last executed for the pre-revision block | Re-run them if a future change touches P5-P8 |
| CI execution of this branch and any push, PR, merge or deployment | None was performed or is authorized here | Open the PR under the source's stages; CI runs the new cases on Linux and Windows |

## 8. Limits

- One host, one run. These are native observations on the named Windows host, not
  a second-host, cross-platform or consumer-readiness claim.
- The mode is an owner statement. The gate requires the mode and the owner's
  words and refuses ambiguity, but it cannot prove who supplied them; the page
  keeps that disclosure (`docs/consumer-starter-package.md`, section 1.3).
- The gate is not a security boundary and is not a hook. Installing these files
  ships behaviour and a check, not enforcement.
- The install record stores the mode and the owner record's presence only; it
  never stores the owner's name, email or a hash of them. S3-1 asserts this.
- No Git identity is written anywhere in the changed procedure; the harness and
  the gate only read.

## 9. Validator and repository checks (this work)

| Check | Command | Result |
| --- | --- | --- |
| Validator self-tests (full suite) | `python -P scripts/tests/test_validator.py` | **OK: 303 gate self-test assertion(s) passed; exit 0** (9 of them the new install-mode cases) |
| Skill validator | `python -P scripts/validate-skills.py` | **exit 0**, `OK: 254 skill(s) valid, 0 warning(s)` |
| Markdown link check on the changed pages | `python -P scripts/ci/check-markdown-links.py <pages>` | **exit 0**, 3 files / 97 links checked / 0 broken / 0 dead |
| Whitespace / conflict markers | `git diff --check` | **clean** |
| DCO sign-off on the candidate commit | `python -P scripts/check_dco.py --range <base>..<head>` | **OK: 1 commit(s) checked, all signed off or exempt** |

```text
$ python -P scripts/tests/test_validator.py
...
  PASS  S3-1: human-only with owner-matching identity exits 0, with 0 commits, 0 files written and byte-identical local Git config
  PASS  S3-2: agent-commit exits 0 for the measured non-owner identity, and an isolated fixture commit carries that author and committer plus Signed-off-by
  PASS  S3-3: agent-commit under the owner identity exits 42 before any commit, with the resolved values, one question and 0 files written
  PASS  S3-4: missing owner (41), absent/malformed mode and missing authorization (43) and a malformed effective identity (42) all refuse with 0 package files
  PASS  S3-5: after a human-only acceptance a later agent-commit proposal is re-gated: exit 42 under the owner identity, exit 0 only after the explicit distinct identity, and no commit is made by the check
  PASS  S3-6: restoring the old unconditional owner-match branch makes the same human-only fixture fail (exit 42) while the published branch exits 0
  PASS  S3-1: the published harness completes a human-only install with 41 files, the mode in the record, 0 commits and byte-identical config
  PASS  S3-5: on the installed human-only tree, a later agent-commit proposal exits 42 and creates no commit
  PASS  S3-4: the published harness with no -Mode exits 43 before reading a source pin, with 0 package files and 0 commits

SKIPPED: 6 test(s) (UNRUN, not passes)
UNRUN: 6 required readiness case(s) did not run on this platform (non-Linux UNRUN; Linux gate remains nonzero on skip)
OK: 303 gate self-test assertion(s) passed.
```

## 10. Skills applied

| Skill and source revision | Actor / role | Purpose | How applied | Result, evidence and limitations |
| --- | --- | --- | --- | --- |
| `agent-startup-context-gate` at `482ba16` | DeepSeek V4 Flash / Item 3 implementer | Establish the source role and the scope of the change | Read the skill and `AGENTS.md`; confirmed the source landmarks, branch and base before acting | Source role verified; no consumer authority inferred |
| `source-of-truth-reconciler` at `482ba16` | Same implementer | Reconcile the published page, the retained v1 walkthrough and the plan's claims | Compared the page's P2 comments with the retained wrapper and the copy harness; re-ran all three natively | The plan's dependency claim (copy harness cannot prove the branch) reproduced; no stale pass reused |
| `plan-of-record-author` / `plan-audit-reviewer` (plan only) | Separate plan and audit agents | Bind the acceptance criteria used here | Read section 5 and the six observations; implemented against them | Implementation scope matches the accepted S3-1..S3-6 set |
