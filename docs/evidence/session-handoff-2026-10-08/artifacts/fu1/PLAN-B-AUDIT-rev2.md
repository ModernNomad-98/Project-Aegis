# PLAN-B audit rev2 — FU-1 Part B (PR template bound-field markers + the stale CI checklist line)

**Verdict: `SD-B: ACCEPT`** on the captured revision `…/fu1/PLAN-B-rev2.md`, sha256
`0e61269f3a5678a334d28a91a8fbdf1cfa2c3468f3193484805e4499abb5e408`. The accepted change is
`…/fu1/planB/PLAN-B-rev2.patch`, sha256
`dfe9af128dd04b1bc35700122971a8bda22de9176db00e379715647f7d5c0e9c`, whose result is
`…/fu1/planB/template.proposed.rev2.md`, sha256
`cfc26e12e0b950dc57a7337f2a206355ce0afbe49b9328292bfe935a3fc61346`. No blocking finding remains;
the nits in §3 do not need a rev3.

**Stage:** B, INDEPENDENT PLAN AUDIT, round 2 (`docs/delivery-workflow.md:28`; `SD-B` tokens at
`:129`, prefixed per `:56-61`).
**Auditor:** the same FU-1 Part B plan-audit subagent as round 1 (`PLAN-B-AUDIT-rev1.md`, sha256
`46810794…07bc`). I did not write either plan revision, and I hold no other FU-1 stage. Read-only
toward the repository and GitHub: no edit, commit or push in the project checkout, no GitHub write.
My only commit was in a scratch `git clone --shared` (`auditB2/sim/`), never pushed.
**Started** 2026-10-08T14:43:25Z. **Audit written** 2026-10-08T14:47Z.
**Base:** `git fetch origin main; git rev-parse HEAD origin/main` → both `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46`;
`git ls-remote origin refs/heads/main` → `c060a7cb…`; `git status --short | wc -l` → `0` at start and
after every step.
**Captured revisions checked at start** (`sha256sum`): rev2 plan `0e61269f…e408`, rev2 patch
`dfe9af12…0e9c`, rev2 template `cfc26e12…1346`, `bound_hash_check_v2.py` `c060ade0…b95d`,
`k-blocks.out` `54eb94fb…0f97` — all equal the coordinator's figures. rev1 is unchanged
(`55e40d5d…cda`). Brief `584ca29a…1ec9` (unchanged since round 1).

## Skills used

| Skill | How applied | Result |
| --- | --- | --- |
| *(none owns a plan-level ACCEPT/REVISE)* | `docs/delivery-workflow.md` stage map, row B: the verdict and the revision binding are procedural. | Procedural verdict above. |
| `acceptance-criteria-reviewer` (partial fit) | Re-checked AC-B1..AC-B13 for observable outcome, threshold and evidence, and ran every evidence block as written in a simulation (§2.4). | All 14 criteria (with AC-B6 split in two) TESTABLE or declared not verifiable with a reason. The round-1 gap (no criterion on the truth of the new prose) is closed by AC-B13. |
| `change-classification-gate` | Re-read rev2 §2: unchanged class (ai-agentic, no grant change), scope still one file. | No finding. |

No MANUAL-ONLY skill was used.

## 1. Round-1 findings — resolved

| Finding | Status | Evidence |
| --- | --- | --- |
| **BF-1** B-2 claim false under the literal reading | **Resolved** | New B-2 text (patched line 114-115): "the hash is taken only from the text between the markers, so a deleted or edited marker leaves the hash undefined or makes it cover the wrong text." "Cannot be posted" is gone (`grep -c 'cannot be posted'` on the rev2 template → 0). My own probe (§2.2) tries 42 deletions and edits of the six markers under two readings; the sentence holds in all 42. R1 and R2 are restated as reading-dependent and name both affected `end` markers with my figures. |
| **BF-2** K4 counted 0 as written | **Resolved** | Every command is in a fenced block. Run as written in my simulation: `6`; `skills 1`, `security 1`, `witness 1`, `end 3`; `6`. |
| **MF-1** K8 not declared | **Resolved** | AC-B6 split into AC-B6a (K7, local) and AC-B6b (K8, GitHub). §9.1 declares AC-B6b runnable only on a pushed head, with the fallback "`UNRUN` as declared here and runs at Stage E", so `SD-D` cannot be forced to REVISE by it. The statement that Stage C pushes before Stage D is attributed to the coordinator; it is not in BRIEF.md and I did not verify it, but the declaration makes the criterion safe either way. |
| **N-1** owner decision row | Resolved | §4 row cites `aegis-open-decisions-2026-09-23.md:106`. |
| **N-2** R2 undercount | Resolved | R2 names skills `end` `fb49fa6990f3f044` and security `end` `23d872f5a7161961`. |
| **N-3** brief hash | Resolved | Header records `584ca29a…`; FU-2 non-overlap cited. |
| **N-4** B-3 wording | Resolved | B-3 ends with a period, defines "head" in place ("the pull request's latest commit (its head)"), and names `changes`. |
| **N-5** "Three things" | Resolved | "Three things below are **always required**"; pandoc renders `<strong>always required</strong>` and `<strong>Aegis skills used</strong>` across the line break. |
| **N-6** API-created PRs | Resolved | §9.1 and R3. Labelled as GitHub's documented behaviour, not tested. |
| **N-7** AC wording | Resolved | AC-B10 is four mechanical checks; AC-B11 lists 11 tokens. My run of K18 prints exactly those 11 tokens, `accept` 0 and bare `PR` 0. |
| **N-8** separability | Moot | Coordinator includes B-4 and B-5; rev2 offers no strike path. |
| **N-9** K9 table cell | Resolved | K9 and the E7 regex are in fenced blocks. |

## 2. Verification of rev2

### 2.1 Patch, bytes and markers

- `git apply --check --verbose PLAN-B-rev2.patch` in the project checkout → exit 0;
  `git apply --check --3way` → exit 0; tree still clean.
- Applied in a scratch copy of the `origin/main` blob (`cmp` against `git show origin/main:…` → equal):
  sha256 `cfc26e12…1346`, `cmp` identical to `template.proposed.rev2.md`; `git hash-object` →
  `43c990a975e8e4eedd260f35d0047fd0e2e8abeb` (the patch's `index fcb6b87..43c990a`); numstat `29 7`;
  126 lines (newline count); 0 carriage returns. The plan's inline §6 diff also applies and gives
  the same sha256.
- **Six marker lines byte-identical to rev1**: `diff <(grep 'bound-field: ' rev1 | od -c) <(grep
  'bound-field: ' rev2 | od -c)` → no difference, same order. They moved down one line (rev1
  63/69/77/82/92/105 → rev2 64/70/78/83/93/106) because B-3 gained a line. `diff` of the rev1 and
  rev2 templates shows only three changed passages: B-5's sentence, B-3's item and B-2's clause.
- My round-1 hash implementation (`auditB/scripts/audit_bf.py`, sha256 `24daf991…2b3`, unchanged) on
  the rev2 template → `1b781aeee463d524`, the same as rev1; on the live bodies → #677
  `bae976a54deac6a9`, #678 `995807705e5a6a59` (the recorded figures), #676 `a530dad3acbc2a5e`.
  `auditB/scripts/r2_probe.py` (sha256 `f08d7ffa…c84`, unchanged) on rev2 → filled
  `e00f49324a54fce6`; skills `end` deleted → `fb49fa6990f3f044`; security `end` deleted →
  `23d872f5a7161961`; witness `end` and each opener → ERROR. These match rev2 §6.1 and R2.

### 2.2 Is the new B-2 sentence true under both readings?

New probe `auditB2/scripts/edit_probe.py` (sha256 `953c3551…cc57`, output `auditB2/edit_probe.out`,
sha256 `a0ec0ecf…87cf`). It takes the filled sample and, for each of the six markers, applies
seven changes: delete it, change one character, drop a space, add text on the same line, and turn
it into each of the other three marker strings. It scores two readings:

- **L, literal:** my `audit_bf.literal()` (first opener, the next `end`, no extensions);
- **S, strict:** written fresh for this probe — the marker lines must be exactly three
  opener-then-`end` pairs, each opener once; anything else is an ERROR.

The claim holds when each reading gives an ERROR or a hash different from the intact
`e00f49324a54fce6`. Result: `SUMMARY: 42 non-whitespace edits/deletions, 0 where B-2's claim
fails`. Under L, every change to an opener or to the witness `end` is an ERROR, and every change to
the skills or security `end` gives a defined but different hash (for example `37d021b4a0490555` and
`e1cc933d1ea2a74a` for a one-character edit, matching rev2 §6.1); under S, all 42 are ERRORs.

Whitespace-only changes around a marker (two leading spaces, trailing spaces) keep the hash
unchanged under both readings, because the method compares the stripped line (`:649-653`). The
sentinel text has not changed in that case, so B-2's "edited marker" does not cover it, and B-2's
instruction "keep every marker line exactly as it is" is stricter than the method needs. Not a
defect.

The planner's `bound_hash_check_v2.py` on my patched copy with my own live-body downloads →
`SUMMARY: 34 checks, 0 FAIL`; on the planner's arguments it reproduces `hashcheck.rev2.out` byte for
byte. Its negative control: on rev1's `template.proposed.md` it reports `FAIL template makes no
'cannot be posted' claim` — `SUMMARY: 32 checks, 1 FAIL` without the live-body arguments (as rev2
§6.1 states) and `34 checks, 1 FAIL` with them.

### 2.3 B-3 against the workflow

Re-read `.github/workflows/validate-skills.yml` at `c060a7cb` (my round-1 table, re-checked by K9 in
my simulation): jobs `changes` (`:56`, no `if:`), `validate-skills` (`:105`, no `if:`),
`windows-offline-checks` (`:275`, `offline`), `tools-tests-linux` / `-windows` (`:363`, `:413`,
`tools`), `gate-guard` (`:476`, pull request only); filters `^tools/` (`:94`) and
`(^tools/|^requirements-ci\.(in|txt)$)` (`:99`); trigger `pull_request` on `main` (`:16-19`). Every
condition rev2's B-3 states is true for pull requests, including the newly named `changes`. Part A's
proposed `docs/offline-ci.md` text (`PLAN-A-rev1.md:397-411`) states the same conditions and adds
the push-to-`main` behaviour; it was written against rev1's B-3, so the coordinator's Stage D
comparison (R5) should use rev2's wording, which now also names `changes`.

### 2.4 The check blocks, run as written

I extracted every fenced block from rev2 §8 (`auditB2/plan-kblocks.txt`). They match the planner's
`k-blocks.sh` exactly, except that K8 is skipped there (declared) and `H` is given a value. I then
built my own simulation: `git clone --shared` of the project into `auditB2/sim/`, detached at `B`,
applied the rev2 patch, committed with a sign-off as "Audit Sim" → simulated head
`67fe43fefbaaedb9fbc422ec5800d9d69d614a78` (never pushed). I ran the blocks in one bash shell with
`H` set to that SHA and `PB` pointed at a copy of the planner's scripts and bodies
(`auditB2/pb/`, so the planner's evidence was not overwritten), K8 removed (needs a pushed head).
Script `auditB2/run-kblocks.sh` (sha256 `9a1322f0…cdbcb`), output `auditB2/run-kblocks.out` (sha256
`01d3a238…0fdd`), exit 0. Results, all as the plan expects:

| Check | Observed |
| --- | --- |
| K1 | `.github/pull_request_template.md` only |
| K2 | `cfc26e12…1346` |
| K3 | `29 7` |
| K4 | `6`; `1/1/1/3`; `6` |
| K5 | `links: 8  bad: 0` |
| K6 | `SUMMARY: 34 checks, 0 FAIL`; live bodies match |
| K7 | `tables=3 raw=6 escaped=0` |
| K9 | conditions as in §2.3; `both Ubuntu` → `0` |
| K10 | no `MATCH` |
| K11 | `Ran 38 tests … OK (skipped=1)`; named test `OK` |
| K12 | `OK: 195 skill(s) valid, 0 warning(s)`; `OK: 181 …`; `Ran 23 tests … OK`; `OK: 76 …` |
| K13 | template: `broken: 0 dead: 0`; page set `files: 619 … broken: 0 dead: 0` |
| K14 | `OK: 1 commit(s) checked, all signed off or exempt.` |
| K15 | `PROVABLY PENDING … 119 yes 8ed59cd761d1` |
| K16 | `CR 0 U+2026 0 nonascii-ws 0` |
| K17 | no output |
| K18 | `0`, `0`, and exactly the 11 tokens of AC-B11 |

K8 was not run (no pushed head); its GET mechanism was proven in round 1 at `ref=c060a7cb…`.

### 2.5 Unchanged since round 1, re-confirmed where cheap

Gate-guard no-match (K10 in the simulation); near-miss test passes (K11); no code reads the
template's content (round-1 `git grep`; the template's path is still only a string at
`test_offline_ci.py:298`); readability: pending before the edit, no acceptance claimed (K15; §7
unchanged); top-comment `-->` hazard (round-1 pandoc variant; B-4 text unchanged); no review-bot
trigger mention in the plan, patch or template (`grep -c -i` → 0 each).

## 3. Nits (non-blocking; no rev3 needed — Stage C may note them)

- **n-1 Blob ID typo.** §6 gives the git blob as `43c990a975e8eedd260f35d0047fd0e2e8abeb` (38 hex
  characters); the actual blob is `43c990a975e8e4eedd260f35d0047fd0e2e8abeb`. No check relies on it
  (K2 uses sha256; the patch's `index …43c990a` is right).
- **n-2 Shared output folder.** K7 and K18 write `k7.html` and `added.txt` into `$PB`, the planner's
  folder, so each later stage that runs the blocks as written overwrites the previous stage's files.
  The files can be regenerated; a stage that wants to keep them can point `PB` at a copy, as I did.
- **n-3 Stale usage line.** `bound_hash_check_v2.py`'s docstring says `Usage: python -I -B
  bound_hash_check.py`.
- **n-4 Pre-fill wording.** §9.1 says GitHub pre-fills the template "only in its web form". The `gh`
  command-line tool also offers the template when `gh pr create` runs without `--body`. Labelled as
  untested in the plan; no effect on any criterion.

## 4. Not done, deliberately

- No repository or GitHub write; no edit to the plan, patch or scripts in `planB/`.
- K8 not run (needs a pushed head; declared in §9.1).
- No review of Part A beyond comparing its job conditions with B-3 (§2.3).
- No change proposed to the bound-field method (R2 stays an owner decision).
- Scratch written: `…/fu1/auditB2/` (base and patched copies, `scripts/edit_probe.py`, outputs,
  `pb/` copies, `sim/` shared clone with the never-pushed simulated head, `plan-kblocks*.txt`,
  `run-kblocks.*`) and this file.
