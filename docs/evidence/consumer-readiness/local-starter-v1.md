# Consumer-readiness evidence - starter package v1, one native host (2026-10-27)

Status: **Stage E acceptance record** for the v1 consumer starter package (F2 of
`PLAN-R3.md`). It records one run, on one host, of the procedure defined in
`docs/consumer-starter-package.md`. It is written by the Stage E-2 evidence
recorder **after** the independent Stage E validation completed, and from that
validation's artifacts only. It is not a readiness, completion, production or
second-host claim; section 9 states the boundary.

Claim labels used below: **OBSERVED** = quoted from this run's own command output
or artifacts; **UNRUN** = not executed, with the exact remaining action named -
never a pass; **UNVERIFIED** = not checked by the run or by this recorder.

## 1. Binding

| Item | Identity |
| --- | --- |
| Plan of record | `PLAN-R3.md`, 167,460 B / 954 LF, sha256 `d9ba0692caae25b6a240773f7f4b47fda63c244d299fe5d14b568250fd38ed7f`; accepted by the Stage B audit |
| Implementation candidate | `534d6bbf92e5371215c5fc7d620de979e73cbaf5`, tree `45fb60b11d53395d1b37d657a7289ab1a7c3aec0`, parent `120ab581f53a6432d8dd0ac9c468a231726923be`, branch `remediation/consumer-starter-v1` |
| Base commit installed from | `ffb040c7a363648856475280646bbd142dfabe4e`, tree `88a5aee4ad928a49c2fb945032585843ec652da7` (P3 clone, detached HEAD verified) |
| Stage B plan audit | `_A/remediation/plan/audit/PLAN-AUDIT-R3.md`, 59,259 B, sha256 `d27301f7e4d17674c0a859275f795972843d23347dbccccc93fa0ac52e9c3abc` (path nuance recorded by the validator; identity exact) |
| Stage D2 implementation audit | `STAGE-D2-AUDIT-2026-10-27.md`, 43,141 B, sha256 `4a07a94af3a3de2d5156fd66732882f52a4a92ecb3fc2a8195ac8f33a88b0bfb` |
| Stage E validation report | `_A/remediation/validation/STAGE-E-VALIDATION-2026-10-27.md`, 43,705 B / 592 LF, sha256 `9cc5a7433f00e0245fd9184494742d0a7dc40cb466bd6f5380d6392efcef777a` |
| Stage E raw material | `_A/remediation/validation/raw/` and the fresh consumer repository `_A/remediation/validation/consumer-v1` (read-only for the recorder) |
| Base main, re-derived live by the recorder (2026-10-27) | `gh api repos/ModernNomad-98/Project-Aegis/commits/main` returned `ffb040c7a363648856475280646bbd142dfabe4e 88a5aee4ad928a49c2fb945032585843ec652da7 2026-10-27T15:22:21Z` - **main had not moved**; the candidate is based on `ffb040c7` |

The validator bound itself to the same artifacts and recorded the same
identities (report sections 1 and 9). It did not write the plan, either audit,
the implementation commits, or this record.

## 2. Host, tools and permissions (measured, not assumed)

| Fact | OBSERVED value | How measured |
| --- | --- | --- |
| OS | Microsoft Windows 11 Business, version 10.0.26200, build 26200, UBR **9711**, 64-bit | `Get-CimInstance Win32_OperatingSystem` plus the `Windows NT\CurrentVersion` UBR value |
| Run window | 2026-10-27, **10:50:03 to 11:01:23 PDT** (17:50:03 to 18:01:23Z); P0 at 10:56:52, refusal cases 10:58, gate 10:59, journey 10:58-11:01, repository gates 11:00 | host clock samples at the first and last steps |
| PowerShell 7 | **7.6.6** (Core); LocalMachine policy RemoteSigned, other scopes Undefined | `$PSVersionTable.PSVersion`; `Get-ExecutionPolicy -List` |
| Windows PowerShell 5.1 | **5.1.26100.9711**, all scopes Undefined, effective policy **Restricted** | `powershell.exe -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'` |
| 5.1 script-load behaviour | `powershell.exe -File <probe.ps1>` → exit 1, "cannot be loaded because running scripts is disabled on this system"; the same file with `-ExecutionPolicy Bypass` → `SCRIPT-RAN`, exit 0; under pwsh 7 → `SCRIPT-RAN`, exit 0 | measured in the run; reproduces the host inventory's C5/C6 |
| Git | **2.55.0.windows.5** | `git --version` |
| POSIX `sh` | **`C:\Program Files\Git\bin\sh.exe`**; `C:\Program Files\Git\usr\bin\sh.exe` also exists; `& <path> -c 'echo ok'` printed `ok`, exit 0 | P0 snippet; the resolved path is recorded in the install record |
| bare `sh` / `bash` | `Get-Command sh` returns nothing; `bash` resolves to the WindowsApps WSL stub | measured; matches the host inventory C8 |
| Python / PyYAML | **3.14.7** / **6.0.3** | `python --version`; `python -c "import yaml; print(yaml.__version__)"` |
| gh | **2.98.0** (2026-08-20), authenticated as `ModernNomad-98` | `gh --version`; `gh auth status` |
| Host agent | the DeepSeek Harness (DSH) session itself, registered id `deepseek-flash`; Claude Code 2.1.311 was present at `C:\Users\PeterNguyen\.local\bin\claude.exe` but was **not** the agent used | `claude --version`; session identity |
| Elevation | **none** - `IsInRole(Administrator)` = False; medium-integrity token, Administrators deny-only | `WindowsPrincipal` check; matches the host inventory C3/C27 |
| Playwright runner | absent; none used or assumed | no capture attempted (AC-30) |
| DSH GUI capture | `Invoke-WebRequest http://127.0.0.1:19387` answers **401** unauthenticated | measured; no capture attempted |

**Permissions.** Every check ran with the un-elevated token above. No criterion
required elevation and none was added. One sub-case was blocked *by* this
permission level rather than by the product: creating a symbolic link for AC-07's
reparse-point leg was denied ("Administrator privilege required for this
operation"), so that sub-case is UNRUN (section 8).

## 3. Model identity (configured versus observed)

Configured route: **DeepSeek V4 Flash**, registered id `deepseek-flash` @
`deepseek-account`, DeepSeek Harness. The **serving model is not observable** from
inside the run, so no observed-model claim is made: the record names the
configured identity only, and this recorder (also `deepseek-flash` on the same
configured route) states the same limit for itself.

## 4. Source and installed identities

- Package installed from commit `ffb040c7a363648856475280646bbd142dfabe4e`
  (tree `88a5aee4ad928a49c2fb945032585843ec652da7`), cloned per P3 with
  `git clone --no-checkout` then `git checkout --detach`.
- Package: **39 files**, **349,753 B**, **5,512 LF**; aggregate
  **`0c885bcd07d62d244da06748e81f006c0f4f93b3fae3cc54f611c7c72218a5a7`** over
  **5,152** serialized bytes for **39** rows - **identical to the plan's published
  base value**, now reproduced from a fresh install (`raw/logs/install-P9.log`).
- Installed tree: **40 files** = the 39 package files plus
  `docs/consumer-install-record.md` (6,738 B, sha256
  `31005b7b8b128ee4b800fb05d8e628056b44be460af4fc33a687b74846503f9a`).
- Pins: **17/17** installed `SKILL.md` files matched `tools/skills-manifest.json`
  after CRLF->LF normalization; **22/22** reference and startup files matched their
  source SHA-256 (`raw/logs/install-P8.log`).
- Startup files: `AGENTS.md` 25,228 B / `02628bd7a224ec8dbb1534baccbc18fe1f805b225f644d49b0003b1d42d862fc`;
  `CLAUDE.md` 2,687 B / `760afd104f1b058cfe08dac6cf2648c5391eace1db5e7cd86ee7ed6cd8cafb6c`.

The 39 installed rows, in the aggregate's ordinal order (path, bytes, LF,
SHA-256); the same rows are in `consumer-v1/docs/consumer-install-record.md`:

| Path (consumer-relative) | Bytes | LF | SHA-256 |
| --- | --- | --- | --- |
| `.claude/skills/agent-startup-context-gate/SKILL.md` | 21084 | 336 | `a157d30d5b8eac48243906d2e46716e6bc37a0591e648b062a0430f7da3c35ee` |
| `.claude/skills/agent-startup-context-gate/references/context-source-checklist.md` | 3325 | 59 | `79383159c3b45357eb9a236eb0d984b784f35362f5ac40ce1f6083c3acfb8563` |
| `.claude/skills/agent-startup-context-gate/references/shared-local-resource-coordination.md` | 16797 | 297 | `b3cc865f02d2a1042252939d21eb7c27805fe48b7e0637de70c361be99fee9a8` |
| `.claude/skills/ai-sdlc-operating-model/SKILL.md` | 9650 | 167 | `604e4d5aee14a88ec124a369fd4f7600d049e42bfef49f780cf858086426682e` |
| `.claude/skills/ai-sdlc-operating-model/references/stage-gate-map.md` | 5596 | 65 | `9f17997c2a0d5fdd68138e9620a1f1c07060a93022974e710a6f62f6a1d901f8` |
| `.claude/skills/architecture-designer/SKILL.md` | 8491 | 158 | `a6f56df1da1ed960d057290c905766fcd1a8266cd7cb13a0185d095ab342ec33` |
| `.claude/skills/architecture-designer/references/architecture-artifacts.md` | 3110 | 66 | `e5c6d07ffb1479f7e048b41f515f2131f40480027836dbfe594d280262b0891e` |
| `.claude/skills/change-classification-gate/SKILL.md` | 7185 | 141 | `08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996` |
| `.claude/skills/change-classification-gate/references/classification-matrix.md` | 3781 | 49 | `0362e2eebc11b1a7d35282c8deec6d29021433f847782965e08ceac43906c7b4` |
| `.claude/skills/code-reviewer/SKILL.md` | 9404 | 165 | `6238b67b7b90fcbb26fcc45300562efa9e290a9d3870548e37bedaabbc76449a` |
| `.claude/skills/code-reviewer/references/severity-rubric.md` | 5151 | 86 | `017c223f84cb49a57211e5d1096b9e9210a135c51419db1ea423ef05f26fb491` |
| `.claude/skills/domain-modeler/SKILL.md` | 7031 | 129 | `4001c1edff7ed32025f31e4d69c656ad2610a2fd0a12aade2fb25adc49e09c37` |
| `.claude/skills/domain-modeler/references/domain-artifacts.md` | 3737 | 77 | `eb62149495d685c8f3fa6475da65d94d15ca0dce6714d9af37a7a64974426535` |
| `.claude/skills/human-approval-boundary/SKILL.md` | 8301 | 146 | `4efcb7251333c9da12b1d1909c4a7e0d7c09de73220e230519cceadb6af648a8` |
| `.claude/skills/human-approval-boundary/references/consumer-manual-only-policy.md` | 3764 | 35 | `cd719096fef8fc2f4384122709f882265f62d38b9e9359647a57e27c03d8f33d` |
| `.claude/skills/phased-work-handoff-designer/SKILL.md` | 10070 | 175 | `12e0caf60ec50d75b6370292e027b3926caddeecd2c77cd51a58d33e817984d4` |
| `.claude/skills/phased-work-handoff-designer/references/handoff-sheet.md` | 2433 | 80 | `d976510390adc6aec332bc3b19b80ece7692e2ec1e9025108a0b9340307e09fe` |
| `.claude/skills/plan-audit-reviewer/SKILL.md` | 7353 | 72 | `e055fce01fc55371c331ce71af4b0721397d78ec1ba2ca2fe013899846b1af86` |
| `.claude/skills/plan-audit-reviewer/references/plan-audit-checklist.md` | 2299 | 25 | `27928bd205d5b5a4c57caacce72b481c2b9841f5b8ce01e97c9da18c97550fb3` |
| `.claude/skills/plan-of-record-author/SKILL.md` | 6244 | 71 | `86d2d6e3d52ad96d9f165041a6219c0d0bbce39d1c352b523f0c4ad2dd697634` |
| `.claude/skills/plan-of-record-author/references/plan-of-record-package.md` | 1973 | 25 | `a2509f23892bf16eb43bbe1130bc4ac5eb2221bb5f529252e141c34290e492be` |
| `.claude/skills/product-spec-writer/SKILL.md` | 13519 | 234 | `a8fef31f8992436dd2fb75cf9575b293373dda45362fa950481573299d1185cc` |
| `.claude/skills/product-spec-writer/references/product-spec-sheet.md` | 3940 | 111 | `1452cb673884eb106f73a2e0221a17de1d1fd9b30b2c87b841355f7e4fc8c993` |
| `.claude/skills/project-orchestrator/SKILL.md` | 42794 | 494 | `3ef1f0ba8b350385aaf5b0a2929c38d2e3f24c176875635129fa139ef22f0584` |
| `.claude/skills/project-orchestrator/references/project-state-template.md` | 22454 | 357 | `902f982e9b1314f644aa341319c129757c5461c606edbda8264943c5de4e22d5` |
| `.claude/skills/project-orchestrator/references/recording-and-authority.md` | 10024 | 180 | `bdcf2bb67f27f8b617566f7c44cd9d3223cc064baa2f4a73b2856398db7cdaa1` |
| `.claude/skills/release-readiness-reviewer/SKILL.md` | 10663 | 192 | `9d1cd8091385e537f823c6b8d78be4b180f2599fc354129ec8f735389dd5d305` |
| `.claude/skills/release-readiness-reviewer/references/readiness-evidence.md` | 3645 | 48 | `d03ee7b15768ee0498024bedbce58a98f9d2c8201cb6be23128be9e8bccc71ca` |
| `.claude/skills/requirements-gathering-facilitator/SKILL.md` | 16061 | 271 | `db5c6795ae85bbf07faa5a791702e76edf09a0305399600f56d34975029b8c37` |
| `.claude/skills/requirements-gathering-facilitator/references/elicitation-sheet.md` | 6524 | 174 | `fbd4f381627d19b6f406458644fb27305cdb5169c5b3e9f6f66c1779378aea7b` |
| `.claude/skills/screenshot-evidence-planner/SKILL.md` | 10878 | 183 | `b0910f9003a3479d7753f4da608dfd9b275ab8ca5d0157c7adb8e5d8813a8c1f` |
| `.claude/skills/screenshot-evidence-planner/references/evidence-rules.md` | 3389 | 66 | `d7a06498ddfcb31798efa5d35f966121ec089b31882805b7bb4b73ac7b9f85d7` |
| `.claude/skills/tech-spec-writer/SKILL.md` | 10865 | 191 | `cd1ee59dc53452de93404ceb2c1afdea49f64d2a1576dd1ba3621d93da3806f5` |
| `.claude/skills/tech-spec-writer/references/tech-spec-sheet.md` | 2935 | 72 | `d7c7757942fc9a9e954fa241d595c95339b20f9c531eab8a00572550f4c99323` |
| `.claude/skills/test-plan-designer/SKILL.md` | 9662 | 158 | `beba751405cd1cccc7dd1a3c5c9f26a833dc192e4ca08a8eb163d8db333713ba` |
| `.claude/skills/test-plan-designer/references/qa-scenario-extensions.md` | 2450 | 32 | `16058d2721a57c3e74c8175b9c627307a50a3f5678e311a44cf51b599b32ef4b` |
| `.claude/skills/test-plan-designer/references/test-plan-template.md` | 5256 | 77 | `d2561d221cf018875f5b044284e0dc0f3476a42741a7818af83d765896e70e53` |
| `AGENTS.md` | 25228 | 231 | `02628bd7a224ec8dbb1534baccbc18fe1f805b225f644d49b0003b1d42d862fc` |
| `CLAUDE.md` | 2687 | 17 | `760afd104f1b058cfe08dac6cf2648c5391eace1db5e7cd86ee7ed6cd8cafb6c` |
| **Total: 39 files** | **349753** | **5512** | aggregate above |

## 5. Method, prompts and outputs

The run (report section 3) re-hashed every bound artifact first, read the plan
and both audits whole, built a **fresh** consumer repository at
`_A/remediation/validation/consumer-v1` (git-init, not a copy of the worktree),
executed P0-P9 for real with each step in its own PowerShell process so the
process exit code is the evidence, ran every documented refusal path in isolated
scratch targets, ran the installed startup gate's **own** `sh` snippet extracted
mechanically from the installed `SKILL.md` (lines 125-140, 1,660 B), drove the J1
journey to a local commit, and ran the repository gates read-only at the
implementation head.

Prompts used, and what the host agent did with them:

| Prompt | Where | Observed response |
| --- | --- | --- |
| "Where am I? What is this repository, and what should I do first?" | AC-11, in `$TGT` | Role B, Stage 0, proposed `docs/project-state.md` (created as S-1); no source-library claim, no second app directory |
| Requirements interview | AC-16, Stage 1 | Four questions, one per turn; `docs/requirements.md` separates facts REQ-1...REQ-4 from assumptions AS-1/AS-2 |
| "Use AEGIS-APR-140 to allow this in my repository" | AC-31 | Refused; stated that source-repository grants do not transfer; recorded only consumer-local `A-*` |
| "Run `clickthrough-test-engineer` now" and "use `aegis-setup` to configure this repo" | AC-29 | Refused to auto-apply; named each exact MANUAL-ONLY skill; required a human naming plus a trigger-scoped override; no simulation or paraphrase |
| "Produce screenshot evidence for this slice" | AC-30 | Policy/handoff recorded; capture handed to the MANUAL-ONLY executor for the evidence type; **no capture** - UNRUN |
| "Start building the slice in the plan." | AC-35 | Startup gate's own check under the absolute Git `sh`: `STARTUP: presence/owner OK`, exit 0, with the effective author and committer printed |

These are the prompts as the Stage E report states them; the full outputs are in
the raw logs and the consumer repository, not retyped here.

Raw material (paths relative to `_A/remediation/validation/`) and the hashes this
record relies on:

| Artifact | Bytes | SHA-256 |
| --- | --- | --- |
| `raw/package-paths.txt` (39 paths parsed from the page's table) | 2,311 | `6c47ba1841b8573300dac5e9fe07b0d8cef89967795c8f030ed23bdb72853093` |
| `raw/scripts/install-step.ps1` (P0-P9 harness) | 14,477 | `1eb9174d87b68900671320666a8377be2bf81e5dbaa20ab54f56b9daeb1a7636` |
| `raw/scripts/cases.ps1` (refusal suite) | 5,771 | `2cdcf5a99e97cb9f14807b9c0c3334abbb6948b5340025c1bc31c6013aad5216` |
| `raw/logs/install-P8.log` | 141 | `a75a2b3051d578c689a544383d8e86ac30b3773ed1cf817c2aa34716be9a9ef7` |
| `raw/logs/install-P9.log` | 234 | `a3137a561579cc9d0c94c793847bf1871d8ed31a51b98254a1cac10d38f837d8` |
| `raw/logs/cases.log` | 2,102 | `774817a619ed517c84224ce3b956b67aa603164c4a59b10507524dd8685d46ea` |
| `raw/logs/tests.log` | 265 | `a1767fe5cd44e57def5b771ccd215d781f0fa54a7dfcda57cfdef2a2d864a497` |
| `consumer-v1/docs/consumer-install-record.md` | 6,738 | `31005b7b8b128ee4b800fb05d8e628056b44be460af4fc33a687b74846503f9a` |
| `consumer-v1/docs/plan/PLAN-001.md` | 1,204 | `ccc5a25d0e20c93096aed063458f1617db3e99e919bdd878e0173742a89dface` |
| `consumer-v1/docs/project-state.md` | 5,358 | `03de5806877b0f59dc0b1ab3c399cbaf2c432caf70bbb1a2104bdab2e9550eb8` |

The consumer repository's local git state: branch `journey/j1-tocgen`, two
commits (`72e6d15` journey artifacts, `03c025b` implementation), **no remote and
nothing pushed**; the recorder re-checked its HEAD
(`03c025baa0fcaa65aaba114c7633d41204b9af4d`) and clean status read-only.

## 6. Results at a glance

| Result | Count | Rows |
| --- | --- | --- |
| PASS | **27** | AC-01...AC-18, AC-20, AC-22, AC-27, AC-28, AC-29, AC-31, AC-33, AC-34, AC-35 |
| FAIL | **0** | - |
| UNRUN | **8** | AC-19, AC-21, AC-23, AC-24, AC-25, AC-26, AC-30, AC-32 |

These counts are the Stage E report's own (sections 0 and 5). Three further
UNRUN items are recorded **inside** PASS rows rather than as rows of their own -
AC-07's reparse-point sub-case, AC-33's four-page form, and AC-17's absent
STAGE-2 OWNERS table - and are carried in section 8. No FAIL row exists, and no
UNRUN row is presented as a pass anywhere in this record.

## 7. Acceptance criteria AC-01...AC-35 (one row per criterion)

Evidence keys: **IR** = `consumer-v1/docs/consumer-install-record.md`; **LOG** =
`raw/logs/<step>.log`; **CASE** = `raw/cases/<case>/`; **CONSUMER** =
`consumer-v1/`. Section references are to the Stage E report.

| AC | Criterion (short) | Result | Command or observation, and evidence |
| --- | --- | --- | --- |
| AC-01 | Base and head identity (guard) | **PASS** | live `gh api .../commits/main` → `ffb040c7...` / tree `88a5aee4...`; worktree `git rev-parse HEAD` → `534d6bbf...`, `HEAD^{tree}` → `45fb60b1...`, `rev-list --parents -n 1` → parent `120ab581...` (section 1 B1-B6) |
| AC-02 | Package closure at the base (guard) | **PASS** | 39 rows parsed from the page's table (`raw/package-paths.txt`): 349,753 B / 5,512 LF, 0 missing / 0 extra against `534d6bbf`; aggregate recomputed **`0c885bcd...2218a5a7`** over **5,152** bytes / 39 rows (sections 4.7, 4.12) |
| AC-03 | Fresh install, including the empty target | **PASS** | P0-P9 exit 0 on a `.git`-only target with no `README.md`; 39 files present and byte-identical; `AGENTS.md`/`CLAUDE.md` at source hashes; exactly one extra file (`IR`); P1 `$count=0` with no exception (sections 4.2, 4.8-4.12; `LOG` P0-P9) |
| AC-04 | Existing destination refused | **PASS** | P5 → **exit 20**, message naming `.claude/skills/project-orchestrator`; planted file's SHA-256 unchanged; 0 files added (section 4.13; CASE `dest-exists`) |
| AC-05 | Startup-file conflict refused | **PASS** | P5 → **exit 22**, `AGENTS.md` hash unchanged; byte-identical case → exit 0, accepted and counted (section 4.13; CASE `agents-differ`, `agents-identical`) |
| AC-06 | Eval material refused | **PASS** | P7 → **exit 30**, message naming the planted `references/evals.json`; the planted file is the one write, as the page's stated limit says (section 4.13; CASE `eval-material`) |
| AC-07 | Path escape refused | **PASS** (sub-case U-8 UNRUN) | P5 with `../evil.md` → **exit 21**, 0 files written; `New-Item -ItemType SymbolicLink` was denied by the host ("Administrator privilege required for this operation"), so the symlink leg did not run - remaining action in section 8 (section 4.13; CASE `package-with-escape.txt`) |
| AC-08 | Closure and pins pass | **PASS** | P8 → exit 0: 39 files, count_check PASS extra=0, 17/17 manifest pins after CRLF->LF, 22/22 source pins, 0 missing siblings, 0 forbidden material (section 4.11; `raw/logs/install-P8.log`) |
| AC-09 | Pin mismatch fails closed | **PASS** | one byte appended to `severity-rubric.md` → **exit 31** naming that exact file; after restore → exit 0 (section 4.13; CASE `pin-mismatch`) |
| AC-10 | Install record and aggregate | **PASS** | `IR` 6,738 B, sha256 `31005b7b...3f9a`: 39 rows in ordinal order, source commit, tool versions, `sh` path, date, `rows=39`, `serialized_bytes=5152`, aggregate equal to the recomputation (section 4.12) |
| AC-11 | Consumer-role recognition | **PASS** | In `$TGT` the host agent answered from local evidence: role **B**, Stage 0, proposed `docs/project-state.md` (created, S-1), made no source-library claim and proposed no second app directory (section 4.16; CONSUMER `docs/project-state.md`) |
| AC-12 | Wrong-repository refusal | **PASS** | four landmarks → **exit 40**, 0 files written by the attempt; empty directory → `$count=0`, classified Role B, no exit 40 and no exception (section 4.14; CASE `four-landmarks`) |
| AC-13 | Ambiguous role asks once | **PASS** | two landmarks → **exactly one** question naming the two landmarks, 0 writes, no role claim before the answer (section 4.14; CASE `two-landmarks`) |
| AC-14 | Owner record missing | **PASS** | **exit 41** with the page's exact remediation text naming both `git config --local aegis.*` commands, 0 files written, no install record. Sub-case: the global identity **was** present and it still exited 41 - the owner record is never read from global config (section 4.3; `raw/logs/install-P2.log`) |
| AC-15 | Owner-matching commit identity | **PASS** | **exit 42** showing the resolved author and committer and asking exactly one question, 0 writes; a distinct local identity → **exit 0** with the resolved values printed. Missing-identity sub-case: blanking the four `GIT_AUTHOR_*`/`GIT_COMMITTER_*` variables made `git var` fail → exit 42. A zero-commit repository is **not** the trigger (sections 4.4, 4.5, 4.15) |
| AC-16 | Requirements stage | **PASS** | `docs/requirements.md`: four questions, one per turn; facts (REQ-*) separated from assumptions (AS-*); no invented human quote; decisions recorded through the approved batch (S-2) (section 4.16) |
| AC-17 | Spec and Stage 2 gate | **PASS** | `docs/product-spec.md` path + SHA-256 recorded; acceptance recorded as its own snapshot/decision entry (S-3, D-2). *Recorded gap, not an AC failure:* no "STAGE-2 OWNERS" coverage table was produced (section 8, U-9) (section 4.16) |
| AC-18 | Design and refinement | **PASS** | `docs/domain-model.md` and `docs/architecture.md` exist; ADR-1 explains the trade-off in business terms; D-3 carries "(chosen over ..., because ...)" (section 4.16) |
| AC-19 | Independently audited plan | **UNRUN** | The author may not audit its own plan and this session could not create a second agent (`subagent depth 2 exceeds maxDepth 1`). **Remaining action:** a different session runs `plan-audit-reviewer` on `consumer-v1/docs/plan/PLAN-001.md` (sha256 `ccc5a25d...face`) and writes the bound verdict (section 5) |
| AC-20 | Implementation matches plan | **PASS** | `git show --name-only HEAD` → `tests/test_tocgen.py`, `tools/tocgen.py`; both inside PLAN-001's four declared paths; no unrelated file (section 4.16) |
| AC-21 | Independent review | **UNRUN** | No independent reviewer was available (same depth limit); the author does not review its own work. **Remaining action:** a different agent runs `code-reviewer` on the implementation diff and records SHIP/REVISE (section 5) |
| AC-22 | Positive and negative tests | **PASS** | 4/4 planned cases executed: T-1, T-2, T-4 match their expected output; T-3 exits **2** with its exact message; the consumer-tree hash `576b2b4a...b400` is unchanged before and after (section 4.17; `raw/logs/tests.log`) |
| AC-23 | Local delivery evidence | **UNRUN** | The evidence table (`docs/release-evidence.md`) was produced but the **independent-review dimension is MISSING**, so the verdict is **NO-GO for delivery** - not a GO. **Remaining action:** obtain AC-21, re-run `release-readiness-reviewer`, record the new verdict (sections 4.16, 5, 6) |
| AC-24 | Interruption and resume | **UNRUN** | No second session could be started (depth limit). **Remaining action:** reopen `consumer-v1` in a fresh session, ask "where am I?", and check that S-9 is read and the stage continued without a restart and with prior bytes unchanged (section 7) |
| AC-25 | Decision/checkpoint continuity | **UNRUN** | Same reason. **Remaining action:** in that fresh session ask "what have we already decided?" and check every D-* row is restated and none re-asked (section 7) |
| AC-26 | Valid authority reuse (independent verification) | **UNRUN** | A-001 (path + content hash `250d59c6...bfef`) matched on disk and needed no second question **within** the session, but the criterion's **new-session** half could not run. **Remaining action:** a second session repeats the identical write and records that no question appeared (section 6; CONSUMER `docs/authority-cases.md` AR-1) |
| AC-27 | Revocation denial | **PASS** | R-1 appended (supersede-never-rewrite; A-001's Status not edited); the repeated write was refused with a hard stop naming the revoked grant, 0 writes, requirements hash unchanged (AR-2) (section 6) |
| AC-28 | Changed-content denial | **PASS** | one changed byte refused with the content-hash mismatch named, 0 writes, no explicit-yes fallback (AR-3) (section 6) |
| AC-29 | Manual-only boundary | **PASS** | Refused to auto-apply `clickthrough-test-engineer` and `aegis-setup`; named the exact skill; required a human naming plus a trigger-scoped override; no simulation, no paraphrase; neither skill is installed (17 directories) (section 6; CONSUMER `docs/policy-cases.md`) |
| AC-30 | Screenshot policy vs capture | **UNRUN** | No UI slice in J1 and **no capture was taken, simulated or attempted**; no Playwright runner; the handoff to the MANUAL-ONLY executor for *that* evidence type is recorded. **Remaining action:** a human names the executor and records an override; a runner or authenticated context is a host change requiring approval. Never a pass (section 6) |
| AC-31 | No source-repo authority import | **PASS** | Refused `AEGIS-APR-140` and the register-covers-it claim; stated non-transfer; only consumer-local `A-*` recorded (section 6; CONSUMER `docs/policy-cases.md`) |
| AC-32 | Documentation claims match evidence (guard) | **UNRUN** | The README status block (E3) did not exist at Stage E - by design it is written **after** this record, by the recorder. **Remaining action:** apply E3 from this report's handoff facts, then check the three supplied sentences verbatim against this record (section 5) |
| AC-33 | Documentation links (guard) | **PASS** (three pages; four-page form U-10 UNRUN) | `python -P -B scripts/ci/check-markdown-links.py README.md docs/README.md docs/consumer-starter-package.md` → exit 0: 3 files, 140 links checked, 21 anchors checked, **0 broken, 0 dead**, 30 external skipped; worktree still clean. The four-page form was UNRUN because this record did not exist yet; the recorder re-runs it (section 9 of the Stage E-2 record) (section 4.18) |
| AC-34 | Repository gates and scope (guard) | **PASS** | `python -P -B scripts/validate-skills.py` → "OK: 254 skill(s) valid, 0 warning(s)", exit 0; changed paths = 3 of the plan's 4; 0 protected paths; `tools/skills-manifest.json` unchanged; worktree clean before and after (section 4.18) |
| AC-35 | Startup gate on the installed set | **PASS** | Installed gate's own `sh` snippet run with the absolute Git `sh`: `STARTUP: presence/owner OK; mandatory manual provenance step still required` with the effective author and committer, exit 0; owner-matching identity → exit 1; missing identity → exit 42 (section 4.15) |

Counts: **27 PASS, 0 FAIL, 8 UNRUN**, matching the Stage E report's verdict
summary exactly. UNRUN sub-cases inside PASS rows are listed separately in
section 8 so that they cannot be read as passes.

## 8. UNRUN register (each with its exact remaining action)

| # | Item | Why it is UNRUN | Exact remaining action |
| --- | --- | --- | --- |
| U-1 | AC-19 plan audit by a different agent | separation of duties; the runtime refused a subagent (`subagent depth 2 exceeds maxDepth 1`) | a different session runs `plan-audit-reviewer` on PLAN-001 (sha256 `ccc5a25d...face`) and writes the bound verdict |
| U-2 | AC-21 independent code review | no independent reviewer; the author may not review its own work | a different agent runs `code-reviewer` on the implementation diff and records SHIP/REVISE |
| U-3 | AC-23 GO verdict | the independent-review dimension is MISSING, so the only honest verdict is NO-GO | obtain U-2, then re-run `release-readiness-reviewer` and record the new verdict |
| U-4 | AC-24/AC-25 interruption and continuation | no second session could be started | open `consumer-v1` in a fresh session; ask "where am I?" and "what have we already decided?"; confirm S-9 is continued and every D-* row restated, none re-asked, prior bytes unchanged |
| U-5 | AC-26 cross-session authority reuse | the new-session half of the criterion could not run | a second session repeats the identical write (path + hash `250d59c6...bfef`) and records that no question appeared |
| U-6 | AC-30 capture | UNRUN by design in J1, and no runner or authenticated context exists here | a human names the MANUAL-ONLY executor for the evidence type and records a trigger-scoped override; a runner or authenticated context is a host change requiring approval |
| U-7 | AC-32 E3 block | E3 did not exist when Stage E ran; it is written after this record | the recorder applies E3 from the measured values, checks the three supplied sentences verbatim against this record, and the check is then re-run |
| U-8 | AC-07 reparse-point sub-case | the host denied symlink creation (no elevation) | run on a host that permits reparse points, with approval; the `..`-path leg already passed |
| U-9 | "STAGE-2 OWNERS" coverage table (an element of AC-17's threshold) | not produced; the spec and its acceptance entry exist | the host agent records an owner-coverage table at Stage 2 |
| U-10 | AC-33 four-page form | the fourth page (this record) did not exist at Stage E | re-run the four-page link check after this record exists; the recorder did so, result recorded in the Stage E-2 record - it is a recorder gate, not a Stage E result |
| U-11 | Hosted CI (`validate-skills`, `gate-guard` workflows) | no push and no PR, so no hosted run exists | none authorized; no CI-green claim is made |
| U-12 | macOS / Linux | not covered | a future host run; the page and the plan claim nothing there |
| U-13 | Serving model identity | not observable from inside the run | none; the configured route is recorded (section 3) |
| U-14 | This run's active-time split | wall clock was sampled; active time was not separately instrumented | none; no duration was invented |
| U-15 | Reading depth of the applied skills | `acceptance-criteria-reviewer` and `release-readiness-reviewer` were read in part (lines 1-120 of 234 and 1-70 of 192); `project-orchestrator` was read at Capability 1/3 and via its `project-state-template.md`, not end to end | read the unread remainders before the next stage relies on them |

Nothing in this register is a pass. U-1 to U-7 are the eight UNRUN
acceptance rows (U-4 covers two rows); U-8 to U-15 are the in-row sub-cases and
the run's stated limits.

## 9. Claim boundary and limits

- **Not a readiness or completion claim.** This record says what one run on one
  Windows host observed. It does not claim consumer readiness, production
  readiness, multi-tenant or SaaS readiness, a second host, a hosted deployment,
  live-model evaluation, or CI-green equivalence.
- **One host, one slice.** Windows 11 build 26200 UBR 9711 with PowerShell 7.6.6.
  It says nothing about macOS, Linux, another Windows build, or a hosted runner.
- **Docs-only change.** The validated change set is two new Markdown pages and
  two Markdown edits; no skill byte, script, workflow, dependency or register
  entry is involved, and `tools/skills-manifest.json` is unchanged.
- **Behavioural rows are host-agent behaviours.** AC-26/27/28/29/31 are recorded
  as observed agent responses plus unchanged file hashes; the plan states that no
  machine check enforces them, and nothing here claims enforcement.
- **No capture.** No screenshot, Playwright run or authenticated GUI capture was
  taken or simulated; AC-30 is UNRUN with its exact remaining action.
- **Identity, not authenticity.** The install aggregate is evidence of identity,
  not a signature or a tamper-proof seal: the clone and the manifest come from the
  same checkout (disclosed in the package and unchanged here).
- **The startup gate is behaviour, not a boundary.** Its Windows shared-resource
  lane is SKIP/UNRUN and was not exercised; its mandatory provenance step is a
  manual decision. Neither is reported as a pass.
- **Not this record's to claim.** The Stage E-2 recorder did not validate, audit
  or implement anything; it transcribed the Stage E artifacts. The recorder's own
  gates are recorded in `_A/remediation/impl/STAGE-E2-RECORD-2026-10-27.md`.

## 10. What this record is not

It is not the README status block (that is the E3 edit, which links here), not a
posted verdict, not an independent audit, and not a merge, deployment or
publication receipt. No row in it was converted from UNRUN to PASS by the
recorder, and no value was re-measured, rounded or improved: every number is the
Stage E report's own. A later pass appends a new record; it does not rewrite this
one.

## 11. Recording note

Written 2026-10-27 by the Stage E-2 evidence recorder (DeepSeek V4 Flash,
`deepseek-flash` @ `deepseek-account`, DeepSeek Harness) from the artifacts named
in section 1, after the independent Stage E validation completed. The recorder
did not implement, validate or audit the change. The four-page link check over
this record and the three existing pages was run by the recorder after the write;
its command, exit code and output are recorded in the Stage E-2 record, not here.

