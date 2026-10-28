# Consumer-readiness evidence - starter package v2, one native host (2026-10-28)

Status: **Stage E validation evidence record** for the v2 consumer starter package (41
files / 18 skills) in docs/consumer-starter-package.md. It records **one native run, on
one verified Windows host**, of the published prerequisite, copy and verify route, plus
disposable integrity-refusal fixtures and a fresh-context reading of the installed
lifecycle material. It is written **after** the run, from that run's captured artifacts.
It is not a readiness, completion, production, second-host or J1-acceptance claim;
section 9 states the boundary and section 8 keeps every UNRUN item.

Claim labels: **OBSERVED** = quoted from this run's own command output or artifacts;
**UNRUN** = not executed, with the exact remaining action named - never a pass;
**UNVERIFIED** = not checked by the run or by this record.

## 1. Binding

| Item | Identity |
| --- | --- |
| Plan of record | four-priority plan, section 3 (S1-1...S1-6), Item 1: consumer starter dependency completion |
| Validated definition | docs/consumer-starter-package.md at candidate head 750767b731820782e1c1535230a2ef3b78ec4ea7, tree a5260b0d0c2cac86f1f8f2612647ac4a4cba16d7 |
| PR base | aa4ae348fa33a50383fb5b79272b6b9aa663c8c0 |
| Branch / worktree | item1/consumer-starter-deps; C:/src/Project Aegis/_A/remediation/handshake/four-priority-item1; clean before and after every command |
| Stage D audit | item1-audit/ITEM1-STAGE-D-AUDIT.md and item1-audit-r2/ITEM1-STAGE-D-REAUDIT.md (working material under _A/, not committed); the re-audit accepted 750767b7 and left S1-3...S1-5 UNRUN |
| Historical v1 record | docs/evidence/consumer-readiness/local-starter-v1.md: 38,376 B / 370 LF, sha256 340a3ac60029b07cb3fb9a8f9890792a2d85d3da40c4ec50abde0c0a6c422813; the blob is identical at base aa4ae348 and head 750767b7 (both git cat-file blob = f16e720894a27f75d74ae188c6365f242dd9eb63) and this change does not touch it |
| This record | added by the Stage E commit on top of 750767b7; it names the validated head, not its own commit, so no self-referential hash is embedded |
| Raw material | _A/remediation/handshake/item1-stage-e/ (logs, fixture JSON, install-record copy): working evidence outside this change, hashed in section 10 |

## 2. Host, tools and permissions (measured in this run)

| Fact | OBSERVED value | How measured |
| --- | --- | --- |
| OS | Microsoft Windows 11 Business 25H2, version 10.0.26200, build 26200, UBR 9711, AMD64 | Get-CimInstance Win32_OperatingSystem; Windows NT CurrentVersion UBR |
| Run window | 2026-10-28, started 14:01:23 PDT (21:01:23Z); the install completed at 14:02:22 PDT; the refusal and lifecycle fixtures ran 14:03-14:08 PDT. Repository gates were run after this record was drafted, so this row is a start and sequence record, not a finish time | host clock samples; active time was not separately instrumented |
| PowerShell 7 | 7.6.6 | $PSVersionTable.PSVersion.ToString() |
| Git | 2.55.0.windows.5 | git --version |
| POSIX sh | C:/Program Files/Git/bin/sh.exe; C:/Program Files/Git/usr/bin/sh.exe also exists | P0 candidate probe; & <path> -c 'echo ok' printed ok, exit 0 |
| Python | 3.14.7 at C:/Python314/python.exe | used only for independent verification, never by the install |
| Network | github.com reachable; git ls-remote --heads origin main returned aa4ae348fa33a50383fb5b79272b6b9aa663c8c0 | read-only, used by the P3 clone |
| Host agent / model | DeepSeek Harness session, configured route deepseek-flash (DeepSeek V4 Flash); the serving model is not observable | session identity; no observed-model claim |
| Fresh consumer-context reader (S1-5) | Claude Code 2.1.311, headless print mode, default configured model; the serving model is not observable | claude --version; the session's own confirmation |
| Consumer destination | C:/temp/aegis-item1-consumer-20261028-140123, outside the repository; git-initialised; synthetic owner record; unrelated files planted before the run | P1/P2 probes and file inventory |
| Source clone | C:/temp/aegis-src-20261028-140123, cloned from github.com per P3 | git rev-parse and status |

The install ran with the ambient token; no step requested or received elevation.
Elevation state was not separately measured in this run. The host's Windows PowerShell
5.1 was not exercised.

## 3. Source and installed identities (independently re-derived)

The P3 clone was made with the published command and proven before any copy:

    git clone --no-checkout -c core.autocrlf=false -c core.eol=lf https://github.com/ModernNomad-98/Project-Aegis.git C:/temp/aegis-src-20261028-140123
    git -C C:/temp/aegis-src-20261028-140123 checkout --detach ffb040c7a363648856475280646bbd142dfabe4e

OBSERVED: HEAD ffb040c7a363648856475280646bbd142dfabe4e; tree
88a5aee4ad928a49c2fb945032585843ec652da7; git status --porcelain empty; zero
w/crlf entries under AGENTS.md, CLAUDE.md and .claude/skills. The pin is not the
PR base aa4ae348; one selected file differs between them (see the package page).

The 41 installed files were re-hashed from the destination bytes and compared
with git cat-file blob at the pin, not with the page's table alone. OBSERVED:

- 41 files / 18 skill directories / 39 skill files + 2 startup files.
- 369,093 bytes and 5,841 LF bytes total; zero CR bytes in all 41 files.
- Aggregate fcff1124d9d15e7d7230fd317350e0eb3b097b453bb6b911cdc1e2485525b699 over
  5,420 serialized bytes for 41 rows, computed from the installed bytes with the
  section 9.2 serialization (path, TAB, bytes, TAB, LF, TAB, sha256, LF; ordinal
  order; UTF-8 no BOM). Every installed byte sequence was byte-identical to the
  pinned blob.
- Install record: 6,816 B, sha256
  e21e657ea3ba9d021f1f7a6a0b24502e756ecbb04ecd60797df1d38ab64dee5b; 41 table
  rows, ordinal order, each row equal to the independent computation, plus the
  published aggregate line.
- Destination inventory: 48 files = the 41 package files + the install record +
  the 6 unrelated files planted before the run.

The 41 rows, in the aggregate's ordinal order:

| Path (consumer-relative) | Bytes | LF | SHA-256 |
| --- | --- | --- | --- |
| .claude/skills/agent-startup-context-gate/SKILL.md | 21084 | 336 | a157d30d5b8eac48243906d2e46716e6bc37a0591e648b062a0430f7da3c35ee |
| .claude/skills/agent-startup-context-gate/references/context-source-checklist.md | 3325 | 59 | 79383159c3b45357eb9a236eb0d984b784f35362f5ac40ce1f6083c3acfb8563 |
| .claude/skills/agent-startup-context-gate/references/shared-local-resource-coordination.md | 16797 | 297 | b3cc865f02d2a1042252939d21eb7c27805fe48b7e0637de70c361be99fee9a8 |
| .claude/skills/ai-sdlc-operating-model/SKILL.md | 9650 | 167 | 604e4d5aee14a88ec124a369fd4f7600d049e42bfef49f780cf858086426682e |
| .claude/skills/ai-sdlc-operating-model/references/stage-gate-map.md | 5596 | 65 | 9f17997c2a0d5fdd68138e9620a1f1c07060a93022974e710a6f62f6a1d901f8 |
| .claude/skills/architecture-designer/SKILL.md | 8491 | 158 | a6f56df1da1ed960d057290c905766fcd1a8266cd7cb13a0185d095ab342ec33 |
| .claude/skills/architecture-designer/references/architecture-artifacts.md | 3110 | 66 | e5c6d07ffb1479f7e048b41f515f2131f40480027836dbfe594d280262b0891e |
| .claude/skills/change-classification-gate/SKILL.md | 7185 | 141 | 08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996 |
| .claude/skills/change-classification-gate/references/classification-matrix.md | 3781 | 49 | 0362e2eebc11b1a7d35282c8deec6d29021433f847782965e08ceac43906c7b4 |
| .claude/skills/code-reviewer/SKILL.md | 9404 | 165 | 6238b67b7b90fcbb26fcc45300562efa9e290a9d3870548e37bedaabbc76449a |
| .claude/skills/code-reviewer/references/severity-rubric.md | 5151 | 86 | 017c223f84cb49a57211e5d1096b9e9210a135c51419db1ea423ef05f26fb491 |
| .claude/skills/domain-modeler/SKILL.md | 7031 | 129 | 4001c1edff7ed32025f31e4d69c656ad2610a2fd0a12aade2fb25adc49e09c37 |
| .claude/skills/domain-modeler/references/domain-artifacts.md | 3737 | 77 | eb62149495d685c8f3fa6475da65d94d15ca0dce6714d9af37a7a64974426535 |
| .claude/skills/human-approval-boundary/SKILL.md | 8301 | 146 | 4efcb7251333c9da12b1d1909c4a7e0d7c09de73220e230519cceadb6af648a8 |
| .claude/skills/human-approval-boundary/references/consumer-manual-only-policy.md | 3764 | 35 | cd719096fef8fc2f4384122709f882265f62d38b9e9359647a57e27c03d8f33d |
| .claude/skills/phased-work-handoff-designer/SKILL.md | 10070 | 175 | 12e0caf60ec50d75b6370292e027b3926caddeecd2c77cd51a58d33e817984d4 |
| .claude/skills/phased-work-handoff-designer/references/handoff-sheet.md | 2433 | 80 | d976510390adc6aec332bc3b19b80ece7692e2ec1e9025108a0b9340307e09fe |
| .claude/skills/plan-audit-reviewer/SKILL.md | 7353 | 72 | e055fce01fc55371c331ce71af4b0721397d78ec1ba2ca2fe013899846b1af86 |
| .claude/skills/plan-audit-reviewer/references/plan-audit-checklist.md | 2299 | 25 | 27928bd205d5b5a4c57caacce72b481c2b9841f5b8ce01e97c9da18c97550fb3 |
| .claude/skills/plan-of-record-author/SKILL.md | 6244 | 71 | 86d2d6e3d52ad96d9f165041a6219c0d0bbce39d1c352b523f0c4ad2dd697634 |
| .claude/skills/plan-of-record-author/references/plan-of-record-package.md | 1973 | 25 | a2509f23892bf16eb43bbe1130bc4ac5eb2221bb5f529252e141c34290e492be |
| .claude/skills/product-spec-writer/SKILL.md | 13519 | 234 | a8fef31f8992436dd2fb75cf9575b293373dda45362fa950481573299d1185cc |
| .claude/skills/product-spec-writer/references/product-spec-sheet.md | 3940 | 111 | 1452cb673884eb106f73a2e0221a17de1d1fd9b30b2c87b841355f7e4fc8c993 |
| .claude/skills/project-orchestrator/SKILL.md | 42794 | 494 | 3ef1f0ba8b350385aaf5b0a2929c38d2e3f24c176875635129fa139ef22f0584 |
| .claude/skills/project-orchestrator/references/project-state-template.md | 22454 | 357 | 902f982e9b1314f644aa341319c129757c5461c606edbda8264943c5de4e22d5 |
| .claude/skills/project-orchestrator/references/recording-and-authority.md | 10024 | 180 | bdcf2bb67f27f8b617566f7c44cd9d3223cc064baa2f4a73b2856398db7cdaa1 |
| .claude/skills/release-readiness-reviewer/SKILL.md | 10663 | 192 | 9d1cd8091385e537f823c6b8d78be4b180f2599fc354129ec8f735389dd5d305 |
| .claude/skills/release-readiness-reviewer/references/readiness-evidence.md | 3645 | 48 | d03ee7b15768ee0498024bedbce58a98f9d2c8201cb6be23128be9e8bccc71ca |
| .claude/skills/requirements-gathering-facilitator/SKILL.md | 16061 | 271 | db5c6795ae85bbf07faa5a791702e76edf09a0305399600f56d34975029b8c37 |
| .claude/skills/requirements-gathering-facilitator/references/elicitation-sheet.md | 6524 | 174 | fbd4f381627d19b6f406458644fb27305cdb5169c5b3e9f6f66c1779378aea7b |
| .claude/skills/scoped-approval-register/SKILL.md | 11822 | 193 | a74d2a22579cf93f737725aa0c54197b5d496a9f33a291a93c2cf2073cd7d076 |
| .claude/skills/scoped-approval-register/references/register-format.md | 7518 | 136 | ace0fb62e81df2e0a7a28822c67426d23cd0938ee6cfa7cfa6665c41e80521b6 |
| .claude/skills/screenshot-evidence-planner/SKILL.md | 10878 | 183 | b0910f9003a3479d7753f4da608dfd9b275ab8ca5d0157c7adb8e5d8813a8c1f |
| .claude/skills/screenshot-evidence-planner/references/evidence-rules.md | 3389 | 66 | d7a06498ddfcb31798efa5d35f966121ec089b31882805b7bb4b73ac7b9f85d7 |
| .claude/skills/tech-spec-writer/SKILL.md | 10865 | 191 | cd1ee59dc53452de93404ceb2c1afdea49f64d2a1576dd1ba3621d93da3806f5 |
| .claude/skills/tech-spec-writer/references/tech-spec-sheet.md | 2935 | 72 | d7c7757942fc9a9e954fa241d595c95339b20f9c531eab8a00572550f4c99323 |
| .claude/skills/test-plan-designer/SKILL.md | 9662 | 158 | beba751405cd1cccc7dd1a3c5c9f26a833dc192e4ca08a8eb163d8db333713ba |
| .claude/skills/test-plan-designer/references/qa-scenario-extensions.md | 2450 | 32 | 16058d2721a57c3e74c8175b9c627307a50a3f5678e311a44cf51b599b32ef4b |
| .claude/skills/test-plan-designer/references/test-plan-template.md | 5256 | 77 | d2561d221cf018875f5b044284e0dc0f3476a42741a7818af83d765896e70e53 |
| AGENTS.md | 25228 | 231 | 02628bd7a224ec8dbb1534baccbc18fe1f805b225f644d49b0003b1d42d862fc |
| CLAUDE.md | 2687 | 17 | 760afd104f1b058cfe08dac6cf2648c5391eace1db5e7cd86ee7ed6cd8cafb6c |
| **Total: 41 files** | **369093** | **5841** | fcff1124d9d15e7d7230fd317350e0eb3b097b453bb6b911cdc1e2485525b699 |

## 4. S1-3 native copy - OBSERVED, exit 0

Procedure executed, in order, against the isolated consumer destination above:

- P0: recorded $PSVersionTable.PSVersion.ToString() = 7.6.6; git --version =
  2.55.0.windows.5; resolved sh = C:/Program Files/Git/bin/sh.exe and confirmed
  & <path> -c 'echo ok' printed ok (exit 0).
- P1: from the destination, the four-landmark probe returned count = 0, so the
  target is Role B (consumer/product repository), not the library.
- P2: git config --local --get aegis.ownerName and aegis.ownerEmail both present
  (synthetic fixture values, deliberately not the real owner); git var
  GIT_AUTHOR_IDENT and GIT_COMMITTER_IDENT resolved to DeepSeek V4 Flash
  <deepseek-v4-flash@users.noreply.github.com>, which does not match the owner
  record; the documented exit 41/42 stops were therefore not triggered.
- P3: clone, checkout and proof as quoted in section 3.
- P4-P9: the harness block was extracted mechanically from the page, not retyped:
  lines 672-967 (the fenced block whose first line is param(), 17,305 B / 294 LF,
  sha256 78f8a2f93bb46f274d6bc59027e69108bd1ebd416b9b0661d521a69c5753bf86), saved as
  install-starter.ps1 and run as written:

    pwsh -NoProfile -File install-starter.ps1 -Src C:\temp\aegis-src-20261028-140123 -Tgt C:\temp\aegis-item1-consumer-20261028-140123 -Sh 'C:\Program Files\Git\bin\sh.exe' -RecordPath C:\temp\aegis-item1-consumer-20261028-140123\docs\consumer-install-record.md

OBSERVED stdout (complete), stderr empty, exit code 0:

    P8: count_check=PASS installed=41 extra=0
    P8: manifest_pins=PASS 18/18
    P8: source_pins=PASS 23/23
    P8: siblings=PASS absent=0
    P8: forbidden=PASS none
    P9: rows=41 serialized_bytes=5420 aggregate=fcff1124d9d15e7d7230fd317350e0eb3b097b453bb6b911cdc1e2485525b699 (matches the published value)
    P9: install record written: C:\temp\aegis-item1-consumer-20261028-140123\docs\consumer-install-record.md
    OK: 41 installed files; closure, pins, siblings, eval and aggregate checks passed

Install-record header, quoted (owner values are not recorded):

    # Consumer install record - starter package v2
    - Source: ModernNomad-98/Project-Aegis at commit ffb040c7a363648856475280646bbd142dfabe4e (tree 88a5aee4ad928a49c2fb945032585843ec652da7), detached HEAD, clean.
    - Installed: 2026-10-28T14:02:22-07:00
    - Tools: PowerShell 7.6.6; git version 2.55.0.windows.5; sh C:\Program Files\Git\bin\sh.exe
    - Owner record: present on both keys (values not recorded)
    - Rows: 41; serialized bytes: 5420; aggregate: fcff1124d9d15e7d7230fd317350e0eb3b097b453bb6b911cdc1e2485525b699
    - Result: P5-P8 exit 0. A later mismatch in any row is a stop, not a warning.

**Independent verification (Python, separate from the harness).** The page's
section 2.3 table was parsed for the 41 paths and byte/LF values; each installed
file was hashed and compared with git cat-file blob at the pin; the aggregate was
recomputed from the installed bytes; the record's 41 rows were compared row by
row. OBSERVED: 41/41 rows match the page and the pin, totals 369,093 B / 5,841 LF,
aggregate and 5,420 serialized bytes match, record row order is ordinal, 0 extra
files inside the installed skill directories, and all 6 unrelated destination
files retain their pre-run bytes and SHA-256. The unrelated set is: README.md,
.gitignore, notes/unrelated.txt, .claude/settings.json,
.claude/skills/my-own-skill/SKILL.md and src/app.py.

**Collision and resume.** A second run on the completed destination, with the
same -RecordPath, exited 0; stdout included "P9: install record already present,
left unchanged" and the same P8/P9 lines. A SHA-256 map of all 48 destination
files taken before and after the re-run was identical (48/48), so the re-run
neither corrupted the install nor rewrote the record. A differing pre-existing
packaged file and a foreign file are refused in section 5, not silently
overwritten.

## 5. S1-4 integrity refusals - OBSERVED in disposable fixtures

Destination fixtures are copies of the completed consumer tree. Source fixtures
are linked git worktrees of the pinned clone; the mutated tracked path was marked
update-index --assume-unchanged so the P3 clean-status gate does not pre-empt the
downstream check under test. That technique is disclosed here: it simulates bytes
that diverged after the clone's identity was proven, and lets the P5/P8 checks be
observed directly. Every case started with the 6 unrelated files present, and each
case's unrelated files kept identical bytes and SHA-256. No case wrote or rewrote
an install record.

| # | Case and fixture change | Exit | Exact refusal (stderr) | Files written | Unrelated files |
| --- | --- | --- | --- | --- | --- |
| 1 | Changed destination byte: appended one byte to .claude/skills/code-reviewer/references/severity-rubric.md | 31 | exit 31: existing installed file differs from the pinned source: .claude/skills/code-reviewer/references/severity-rubric.md | 0 added, 0 changed | unchanged |
| 2 | Evaluation-answer contamination: .claude/skills/test-plan-designer/evals/evals.json added | 20 | exit 20: existing skill directory holds a file outside the package: .claude/skills/test-plan-designer/evals/evals.json | 0 | unchanged |
| 3 | Conflicting startup bytes: one byte appended to AGENTS.md | 22 | exit 22: startup file differs: <fixture>/AGENTS.md | 0; the conflicting AGENTS.md bytes were left as planted, never overwritten | unchanged |
| 4 | Foreign non-package file: .claude/skills/plan-of-record-author/references/extra.md added | 20 | exit 20: existing skill directory holds a file outside the package: .claude/skills/plan-of-record-author/references/extra.md | 0 | unchanged |
| 5 | Changed source byte: one byte appended to the pinned severity-rubric.md (assume-unchanged) | 31 | exit 31: aggregate e5be10ad15ae2c943aee48feceac2c11033ae188724121827742e48a15c00a1d does not match the published fcff1124d9d15e7d7230fd317350e0eb3b097b453bb6b911cdc1e2485525b699 | 41 (the copy completed before verification), no record | unchanged |
| 6 | Missing required reference: register-format.md deleted from the source clone (assume-unchanged) | 21 | exit 21: missing source file: <fixture>/.../scoped-approval-register/references/register-format.md | 0 | unchanged |
| 7 | Malformed manifest, invalid JSON: tools/skills-manifest.json replaced with a non-JSON string (assume-unchanged) | 1 | ConvertFrom-Json: Conversion from JSON failed ... Invalid character after parsing property name ... (PowerShell terminating error; no record) | 41, no record | unchanged |
| 8 | Malformed manifest, wrong shape: {"skills":"not-an-array"} (assume-unchanged) | 31 | exit 31: no unique manifest entry for agent-startup-context-gate | 41, no record | unchanged |
| 9 | Identical re-run (collision/resume) | 0 | P9: install record already present, left unchanged | 0 changed; 48/48 files identical | unchanged |

Notes on the intended reasons, including one honest limitation:

- Cases 1, 3 and 4 are refused by the P5 destination pre-checks before any copy;
  each names the exact offending file and leaves the destination unchanged.
- Case 2 is evaluation-answer contamination. It is refused as foreign material
  in an installed skill directory (exit 20) by P5, which runs before P7. The
  published P7 eval scan (exit 30) is not reachable for a destination-only
  fixture, because P5 already refuses the same file; no claim is made that P7
  itself ran in this case. The outcome is still fail-closed and the file is
  named.
- Case 5 shows why the aggregate is the independent anchor: the source-side pin
  comparison would compare the destination with the same changed clone, so only
  the published aggregate detects the divergence. It exits 31 (no file is named
  by this check) and writes no record.
- Case 7 is syntactically invalid JSON. The harness does not wrap this parse in
  a documented Stop-Step, so PowerShell exits 1 with the JSON parser error; it
  still fails closed and writes no record. Case 8 uses valid JSON with a wrong
  shape and produces the documented exit 31 naming the skill with no unique
  manifest entry. Both are recorded as observed rather than converted to a
  PASS of a specific code.
- Case 6 is refused before any write; the target kept only its unrelated files.

## 6. S1-5 authority and lifecycle - OBSERVED in a fresh isolated consumer context

A disposable fixture at C:/temp/aegis-item1-authority-20261028-140123 contains the
installed scoped-approval-register material copied from the completed consumer
tree (SKILL.md 11,822 B / 193 LF, sha256
a74d2a22579cf93f737725aa0c54197b5d496a9f33a291a93c2cf2073cd7d076;
references/register-format.md 7,518 B / 136 LF, sha256
ace0fb62e81df2e0a7a28822c67426d23cd0938ee6cfa7cfa6665c41e80521b6) and four
synthetic, explicitly non-authorizing histories. Each case states a proposed
action time of 2026-10-02T12:00:00Z and a hypothetical append to
docs/fixture-target.md (sha256 feb3242bd9ddb767a7faceee7af8c2f10a836cf63aa9c8aee4bc733e89c0b9c6).
No real approval exists, and no external operation was possible or attempted.

The reading was performed by a **fresh Claude Code 2.1.311 headless session** with
the fixture as its working directory, no prior conversation, only Read/Glob/Grep
allowed, no network, and explicit instructions not to read outside the fixture and
not to create, edit or delete anything. Its own confirmation states that it read
only README.md, the four case files and the two installed lifecycle files, created,
edited and deleted nothing, and used no network. A SHA-256 map of the fixture's 8
files taken before and after the reading is identical; the target file remains
FIXTURE-TARGET and was not written.

| Case | Synthetic history | Effective status at the action time | Authorized by the history? | Action |
| --- | --- | --- | --- | --- |
| 1 Valid scope | APR-201 GRANT, ACTIVE, scope = one append to the named path at the named SHA-256 during 2026-10-02, one use, expiry 2026-10-03 | effectively ACTIVE if it were a real grant; path, content, hash, time, expiry and use limit match; no lifecycle event | Yes in the modeled sense only; the record is synthetic and authorizes nothing real | No action performed |
| 2 Late-recorded revocation | APR-202 GRANT; APR-203 REVOKED target APR-202, effective 2026-10-02T08:00:00Z, recorded 2026-10-03T09:00:00Z | REVOKED at the action time (effective time governs, not the later transcription) | No | Refuse / no action |
| 3 Malformed target | APR-204 GRANT; APR-205 REVOKED with target "APR-204?" (not a valid reference to an existing GRANT) | UNRESOLVED | No | Refuse / no action; request a fresh unambiguous human grant |
| 4 Duplicate ID | Two different GRANT records both numbered APR-206 | UNRESOLVED | No | Refuse / no action; request a fresh unambiguous human grant |

The exact rule text quoted by the reader, matched to the installed reference:

- Case 2: "Establish applicability by evidenced effective time, including
  late-recorded facts", "Invalidation is terminal for that grant", and
  "Reauthorization requires a NEW grant ID and a new human decision".
- Cases 3 and 4: "Missing targets, duplicate IDs, self-links, cycles or
  contradictory events make affected authority unresolved; do not use those
  records to authorize action", plus "An annotation does not repair or validate
  malformed history" and "Further authority requires a separately evidenced human
  grant with a fresh unambiguous ID; never edit old bytes".
- Case 1: "Only effectively ACTIVE grants can cover an action. Match actual
  allowed scope, environment, target, limits and applicable prohibitions", with
  the status test "A grant begins ACTIVE only if supported by the actual human
  decision". The reader noted the synthetic evidence line and therefore made no
  real-permission claim.

**Limitation, stated rather than hidden:** the reader took the target's SHA-256
from the case text; it did not read docs/fixture-target.md, so the hash match is
not independently re-derived by the reader. The lifecycle distinction (valid,
late-recorded revocation, malformed target, duplicate ID) is the observation this
case records; the content hash is a field the installed procedure requires and the
fixture supplies.

## 7. S1-6 record and claims alignment

- This record is the v2 evidence record named by plan section 3 (S1-6). It was
  written after the native run and contains the run's actual commands, host,
  inputs, outputs and exit codes; it does not repeat the hosted J1 proof, which
  remains out of scope.
- The historical v1 record is byte-unchanged: 38,376 B / 370 LF, sha256
  340a3ac60029b07cb3fb9a8f9890792a2d85d3da40c4ec50abde0c0a6c422813; its git blob is
  f16e720894a27f75d74ae188c6365f242dd9eb63 at both aa4ae348 and 750767b7.
- The package page and the two READMEs are edited in the same Stage E commit only
  where they said the v2 native checks were UNRUN or pointed the v2 selection at
  the v1 record. No selector row, byte, LF, SHA-256, aggregate, harness constant
  or test behaviour is changed by that commit; the pinned values and
  scripts/tests/test_validator.py are untouched.

## 8. Retained UNRUN register (never a pass)

| # | Item | Why UNRUN here | Exact remaining action |
| --- | --- | --- | --- |
| U-1 | macOS and Linux native install | this run is Windows only; the page claims nothing there | run the same procedure on a verified macOS/Linux host |
| U-2 | A second Windows host or build | one host, one OS build (26200 UBR 9711) | repeat on another verified host and record its tool versions |
| U-3 | Hosted CI (validate-skills jobs, tools-tests-linux, tools-tests-windows, windows-offline-checks) | no push and no PR edit were made, so no hosted run exists at this commit | the Stage F/pr merge route runs them; skipped jobs are UNRUN, not passes |
| U-4 | The J1 journey itself (requirements through local delivery) | S1-3...S1-6 cover the install and its lifecycle material, not the journey; the v1 record's J1 rows remain as recorded there | a separate J1 acceptance run on a consumer repository |
| U-5 | Negative prerequisite branches exit 40 (wrong repository), exit 41 (missing owner record), exit 42 (owner-matching commit identity) | not re-executed in this v2 run; the prerequisite layer and its code are unchanged, and the same host ran these branches in the v1 record | re-run P1/P2 negative branches against a v2 consumer if that layer changes |
| U-6 | P7 eval scan's own exit 30 | a destination eval file is refused earlier by P5 exit 20; the published harness offers no hook to inject material between copy and P7 | a fixture that adds the eval material between P6 and P7, or a harness change; not claimed as run |
| U-7 | Reparse-point source-path leg | no junction or symbolic-link fixture was created in this run | run on a host that permits creating a reparse point, with the user's approval |
| U-8 | Windows PowerShell 5.1 script-load refusal | this run used PowerShell 7.6.6 only | run the 5.1 load probe on a host with the documented policy |
| U-9 | Serving-model identity | not observable from inside the run | none; the configured route is recorded |
| U-10 | Active-time split | wall clock was sampled; active time was not separately instrumented | none; no duration is invented |
| U-11 | Real external operations under any synthetic history | synthetic histories cannot authorize real operations, and none was attempted or possible | a real operation needs a real human grant, outside this test |

## 9. Claim boundary and limits

- **One host, one run, one clone, one consumer fixture.** Windows 11 build 26200
  UBR 9711 with PowerShell 7.6.6, Git 2.55.0.windows.5 and the absolute Git sh.
  It says nothing about macOS, Linux, another Windows build, a hosted runner or a
  second consumer tree.
- **Not a readiness or completion claim.** The package's own page still claims
  only the local J1 baseline; this record does not claim consumer readiness,
  production readiness, hosted deployment, live-model evaluation, CI-green
  equivalence or "complete native consumer testing".
- **Install integrity, not the journey.** The 41 selected files were copied and
  verified; the J1 journey, its skills' runtime behaviour beyond the lifecycle
  reading, and any real consumer product are outside this run.
- **The aggregate is an identity anchor, not a signature.** It is checked
  fail-closed against the published value, but a clone that reproduces those bytes
  would also reproduce the aggregate; P3's commit/tree proof is the second anchor.
- **All numbers are derived by scripts from bytes**, not typed from prose: the
  page table, git cat-file blob at the pin, the installed record and the
  independent recomputation.
- **Synthetic histories are non-authorizing.** Section 6 records a reading
  exercise only; it created no authority and performed no action.

## 10. Recording note and raw artifacts

Written 2026-10-28 by the Stage E validation agent (DeepSeek V4 Flash, configured
route deepseek-flash @ deepseek-account, DeepSeek Harness; the serving model is
not observable). The agent did not implement Item 1 and did not write the v2
definition; it ran the published route, the refusal fixtures and the fresh-context
reading, then wrote this record and the claim-alignment edits.

The raw material is under _A/remediation/handshake/item1-stage-e/ and is not part
of this change. Key artifacts: the raw/logs/ set (preflight, install, rerun,
refusal, authority-reading and repository-gate logs); raw/fixtures/install-starter.ps1 (extracted
harness, 17,305 B, sha256 78f8a2f9...); raw/fixtures/install-record-run1.md
(6,816 B, sha256 e21e657e...); raw/fixtures/install-verify.json; the case-*.json
refusal records; raw/fixtures/authority-before.json and authority-after.json;
raw/fixtures/authority-prompt.txt and raw/logs/08-authority-reading.log.
