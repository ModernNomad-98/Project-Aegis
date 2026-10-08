# CIFIX-1: Stage B INDEPENDENT PLAN AUDIT of PLAN-rev2 (round 2)

**Disposition: `SD-B: REVISE`** on the captured revision below. The required changes are numbered
RC11–RC16 in §7. They continue the round-1 numbering, so they do not collide with RC1–RC10.

- **Audited revision:** `$S/cifix/PLAN-rev2.md`, sha256
  `453c3beb1bea9ba3e2db5fab7e428950c9e9bab2d63fe91e6560c67be7ec9fe7`. `sha256sum` returned this value at
  the start (17:11:40Z) and again at 17:33:42Z. It equals the hash in my brief.
- **Stage held:** B only, round 2. The round-1 holder's session was interrupted, and I am a fresh agent.
  I did not write the plan. I will not implement it, audit the implementation, validate, review or merge
  P-FIX or P-REG. Repository writes: none. GitHub writes: none.
- **Role A.** The four landmarks are present: `head -3 README.md` shows `# Project Aegis`, and `ls` found
  `docs/skills-catalog.md`, `scripts/validate-skills.py` and
  `artifacts/audits/skill-contract-audit-baseline.json`.
- **Scratch root:** `S=/tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad`.
  All of my evidence is under `$S/cifix/b2-audit/`.

**Inputs read**

| Input | sha256 or state |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `docs/delivery-workflow.md` | Unchanged from `c060a7cb` to `origin/main` (`git diff --quiet c060a7cb origin/main -- CONTRIBUTING.md docs/delivery-workflow.md AGENTS.md CLAUDE.md` → rc 0). Read: workflow L1-460 and L805-830; CONTRIBUTING L180-276. |
| Register at `origin/main` (`git show` → `b2-audit/register-main.md`, 5154 lines) | Preamble L1-80. Entries APR-032/033/034 (L880-934), 047 (L1219), 048, 049, 050 (L1293-1380), 100 (L3070), 105, 106, 107 (L3380-3590). Heading count 119, maximum 119, 0 duplicates. |
| `$S/cifix/BRIEF.md` | `31dec83bb660d843f2f3c96f372284b8f535354f4c3f1f185f74205bb847d2fb`, read in full. This is the version with the OQ-A/OQ-B notes and the owner's 17:10:06Z scrutiny rule. **The plan cites `5729b391…`, an earlier version.** |
| `$S/cifix/owner-q2-q4-verbatim.json` | `74c8cd5a559b1398fe411d6d75f4da1be23fe788b0845cdb59dcfb09bc82f1c2`, which matches the brief |
| `$S/rcf/BRIEF-COMMON.md`, `$S/ci-diag/DIAGNOSIS.md` (`522ea312…`), `$S/ci-diag/proposed-fix.diff` (`339e1f22…`), `$S/cifix/prototype-reference.diff` (`a4ad6f9f…`) | Each hash matches the plan's input and evidence tables |
| `$S/cifix/PLAN-AUDIT-rev1.md` | `26609843…`, which matches the plan's input table |
| Planner scripts `ab_force.sh`, `trace_count.sh`, `test_names.py`, `count_fixtures.py`, `add_regtest.py` | Each hash matches the plan's §14 |

**Base.** `git ls-remote origin refs/heads/main` → `5228977920ee479e1fe1ec6b8d56f8fc24c14947`. Open pull
requests: 0 (`gh api 'repos/…/pulls?state=open&per_page=100' --jq length`).

**The test file is unchanged since `c060a7cb`:**
- `git diff --quiet c060a7cb origin/main -- scripts/tests/test_offline_ci.py` → rc 0;
- the same check over the plan's scope-lock set (test file, `.github/workflows/`, `scripts/ci/record-check.py`,
  `scripts/validate-skills.py`) → rc 0;
- it is 750 lines at `52289779` (`wc -l` on `git archive`).

---

## 0. Aegis skills used (dogfood rule)

`docs/delivery-workflow.md` (the Stage B row of "The enforcing skill for each stage") says no installed skill
owns a plan-level ACCEPT/REVISE audit. The verdict and the revision binding are therefore procedural. I read
each skill below and applied it only to the part it owns. Each description is free of the MANUAL-ONLY
prefix (`grep -m1 '^description:'`). The MANUAL-ONLY skills `systematic-debugger`, `flaky-test-detective`,
`reviewable-diff-discipline` and `agent-authorization-matrix` were not used.

| Skill | Why it applies now | What it produced |
| --- | --- | --- |
| `acceptance-criteria-reviewer` (partial fit) | The plan carries 20 criteria (AC-F1..F12, AC-R1..R8), and later stages will check them one by one | §5: 15 TESTABLE, 5 NEEDS-REWRITE, 0 UNTESTABLE. Its own contract says it "never decides whether work is done". The plan-level verdict is mine. |
| `scoped-approval-register` | The plan drafts a register GRANT (§6.4) that must quote the owner verbatim and invent nothing | §4: every owner quote present in the plan is byte-exact. The draft still holds placeholders, one wrapped label that breaks AC-R8, an untimed OQ-A record, and one overstated Evidence sentence (RC12). |
| `human-approval-boundary` | Three risky actions need a matching grant: an admin merge past a red required check, a register edit, and the response to a moved head | The grant and the Q2/Q4 answers cover the actions. The silence rule ("Silence … is not approval") governs how the 28-line disclosure (OQ-B) and the OQ-C reading may be recorded (RC11, RC12). |
| `change-classification-gate` | Confirms the bug-fix floor that justifies keeping the regression test (Q5) | `references/classification-matrix.md:24` reads "Reproduce the failure first; prove the fix flips it; regression test added". I reproduced all three (§3). |

---

## 1. Summary

**What holds.** The technical core is sound. I re-verified it with my own harnesses (§3).
- The forced race fails at base and passes with the fix.
- The regression test flips deterministically on Git 2.55.0 and 2.43.0.
- The trace census drops from 264 maintenance spawns to 0.
- With the prototype applied, the full file runs `Ran 39 tests … OK (skipped=1)` on both Gits.
- The repository checks keep the plan's reference values.
- RC1–RC10 are resolved in substance (§2).
- Every owner text the plan quotes is byte-exact against the brief and the JSON (§4).

**Why it is REVISE.**
- **Inputs moved after rev2 was written.** OQ-A is answered by the JSON. OQ-B is answered. The owner has
  added a binding scrutiny rule. Rev2 does not use any of them (RC11).
- **The draft entry is not yet fillable as written.**
  - Its Q2–Q4 placeholders are still open.
  - It breaks the label "Ask me again (Recommended)" across a line, so AC-R8 returns `0` on the draft
    (measured).
  - It would assign no source to the JSON record (RC12).
- **Five criteria cannot be run as written, or would give a false result** (RC13):
  - AC-R2 counts P-REG itself, so it fails falsely at the merge re-check.
  - AC-R7 has no commands, and a plain text search for "SD-F: ACCEPT" matched a REVISE comment on #677.
  - AC-F11 has no log command.
  - AC-F9 fails falsely if it is run in a `T(x)` archive tree.
  - AC-R8 is incomplete.
- **The merge mechanism rests on facts the plan does not cite** (RC14):
  - the evidence for an admin bypass of a failing required check;
  - the documented `sha` refusal;
  - the fact that P-FIX must not be updated after P-REG merges.
- **The Q4 procedure has a wording trap and an unhandled branch** (RC15).
- **The owner's 17:10:06Z rule needs per-recommendation self-scrutiny notes** (RC16).

---

## 2. RC1–RC10: resolved, or only mapped?

| RC | Verdict | Evidence |
| --- | --- | --- |
| RC1: apply Q2 | **Resolved** | §6.2 quotes the Q2 question and option. Both are byte-equal to the JSON (§4). §6.5 rests P-REG's authority on Q2 and quotes its terms. The Q1 reading is applied to P-REG. APR-100/048/050 are support only. `grep -n -i 'confirm' PLAN-rev2.md` finds no remaining "Q2 asks the coordinator to confirm" dependency; the remaining hits are the OQ-A/OQ-B requests and stage checks. The input-table hash is stale again, but that is new drift after rev2, handled in RC11. |
| RC2: apply Q3, remove P-CONS | **Resolved** | `grep -n 'P-CONS'` matches only L1075, "There is no P-CONS step in CIFIX-1". §6.6 lists the receipt facts and uses APR-107 as the template. "Expected 121" is gone. |
| RC3: apply Q4 as a procedure, flag the reading | **Resolved, with two refinements** | §6.3 covers a move before P-REG merges (rebuild in place) and after it merges (ask again). §9 P-FIX G step 8 and OQ-C flag the "recorded = merged on main" reading. The refinements are in RC15: "names the new head", and the EXPIRED event when the owner declines. |
| RC4: Stage F link out; Stage C entry condition | **Resolved** | The §6.4 Evidence cites only the Stage D audit and the `gate-guard` log. §6.3 (a)/(b) requires `SD-D: ACCEPT` at H plus a completed check set with the expected conclusions, read at run level. |
| RC5: P-REG merge timing | **Resolved** | §6.3 (a)–(d) and AC-R7. AC-R7's missing commands are RC13. |
| RC6: owner texts in the entry | **(b), (c), (d) resolved; (a) only mapped** | (b) The 588-character question is byte-equal at L449 and L609. (c) The 255-character option is byte-equal at L462 and L613 to the brief's one-line form, which the coordinator states is "on ONE line exactly as the owner saw it". (d) Done. **(a) is not done:** the draft still holds `<Q2 question …>`, `<Q2/Q3/Q4 option text, as confirmed>` and a conditional "unrelayed" clause. The texts now exist in the JSON, so RC12 applies. |
| RC7: append-only proof | **Resolved** | On my own simulation, an appended draft entry at `52289779` in scratch commit `5b3557c6…` (never pushed), AC-R1's commands gave: `74	0	docs/approvals/APPROVAL_REGISTER.md`; `cmp … ; echo $?` → `0`; one hunk `@@ -5154,0 +5155,74 @@ the entry governs.`; `wc -l < b.md` → `5154`; trailing `\n`. See N5 on the trailing context text. |
| RC8: separation | **Resolved** | §9 "All stages", rules (i) and (ii) |
| RC9: stale facts and attribution | **Resolved, all re-verified by me** | (a) #679 merged at 15:55:22Z as `c1acc075` (two parents). #680 merged at 16:13:04Z as `52289779` (one parent) (`gh api pulls/N`, `git log -1 --format=%P`). The reference values at `52289779` are re-measured in §3. (b) #663's body line 62 reads "The append-only rule governs **merged** entries" (`gh api …/pulls/663 --jq .body \| grep -n`). APR-105's sentence is wrapped at register L3440-3441: "Once / merged, any further change to it is an append." (c) Register L3463-3464. |
| RC10: five ACs made concrete | **Resolved** | AC-F3: `test_names.py` → `added: ['ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance'] removed: [] base=38 head=39`, and my own `ast.walk` count agrees (38 → 39). AC-F5: the `sed` removes exactly 2 lines (778 → 776); flip in §3. AC-F12: every TMPDIR I used ended empty. AC-R4: the `awk` extraction gave a 73-line `e.md`. AC-R2: the loop runs, but has the self-inclusion defect in RC13. |

---

## 3. Independent re-verification

**Harnesses.**
- `b2-audit/scripts/b2run.sh` (sha256 first 16 `266c62952043db77`): a scratch TMPDIR for each label,
  `GIT_CONFIG_GLOBAL=/dev/null`, `PYTHONDONTWRITEBYTECODE=1`, `python3 -B -P`, `GIT_CONFIG_PARAMETERS`
  unset. The force mode sets `maintenance.geometric-repack.auto=-1` through `GIT_CONFIG_COUNT`.
- `b2-audit/scripts/b2trace.sh` (`f0fef8ef9e6dbf7c`): a trace2 census.

**Trees.**
- `base` is `git archive 52289779`.
- `proto` is base plus `git apply prototype-reference.diff` (`--check` passed).
- `reverted` is proto with the AC-F5 `sed` applied.
- `clone` is a `git clone --shared` at `52289779` with the prototype committed as `6d3396e5…`
  (tree `8c7bf4b0…`, signed off, never pushed).

**Git.** `$S/git-build/install/bin/git --version` → `git version 2.55.0`. The system Git is 2.43.0.
Python is 3.13.16.

**Forced race (AC-F6).**
```
base-force-g55  git=2.55.0 force=1 runs=3  ok=0  bad=3 errno39_lines=49 tmp_leftover=49 results=[FAILED (errors=10); FAILED (errors=16); FAILED (errors=23)]
proto-force-g55 git=2.55.0 force=1 runs=10 ok=10 bad=0 errno39_lines=0  tmp_leftover=0  results=[10 OK]
```
- All 49 base tracebacks pass through `line 149, in run_guard`, the CI signature.
- The failing directories are `repo/.git/objects/pack` ×45, `repo/.git` ×3 and `repo/.git/objects` ×1.

**Flip (AC-F5).** The test method was run 5 times per cell:
```
flip-reverted-g55 ok=0 bad=5 [5 FAILED (failures=1)] maint_argv_in_assert=25   flip-proto-g55 ok=5 [5 OK]
flip-reverted-sys ok=0 bad=5 [5 FAILED (failures=1)] maint_argv_in_assert=25   flip-proto-sys ok=5 [5 OK]
```
The assertion reads `AssertionError: Lists differ: [] != [['git', 'maintenance', 'run', '--auto', …`.

**Census (AC-F4).**
```
base-g55  Ran 10 tests OK maint_spawns=264 by_parent={'commit': 176, 'fetch': 88} maint_process_starts=264 upload_pack_children=88
base-sys  Ran 10 tests OK maint_spawns=264 by_parent={'commit': 176, 'fetch': 88} maint_process_starts=264 upload_pack_children=88
proto-g55 Ran 11 tests OK maint_spawns=0 by_parent={} maint_process_starts=0 upload_pack_children=88
proto-sys Ran 11 tests OK maint_spawns=0 by_parent={} maint_process_starts=0 upload_pack_children=88
```
The guard's own `git fetch` reads the fixture's repository config: fetch-parented spawns go from 88 to 0.

**Git 2.55.0 source.** Each line the plan cites was re-read:
- `run-command.c:1956-1967` returns 0 when `maintenance.auto` is false; when that key is absent, the result
  is `gc.auto > 0`;
- L1974-1976 and L1980-1982 build `maintenance run --auto --detach`;
- `builtin/fetch.c:2868` checks `if (enable_auto_gc)`, and L2580 is the `auto-maintenance` option;
- `builtin/gc.c:1632-1637`: a negative value means `return 1`;
- the callers are only am, receive-pack, commit, merge, fetch and rebase;
- `RelNotes/2.54.0.adoc:58`: "git maintenance" starts using the "geometric" strategy by default.

**AC-F1, F2, F10 on the scratch commit.**
- AC-F1: `28	0	scripts/tests/test_offline_ci.py` and `0`.
- AC-F2: grep → rc 1.
- AC-F10: `0` ; `1` ; `1`.

**AC-F3.** See §2. `count_fixtures.py`: base `run_guard_fixtures=88 test_methods_total=38`, head `89` / `39`.

**AC-F8, in the clone.** Git 2.55 and 2.43 both give rc 0, `Ran 39 tests`, `OK (skipped=1)`, 0
`Errno 39`. Base in the clone: `Ran 38 tests … OK (skipped=1)`.

**AC-F7.** 20 runs of the full file in the clone on Git 2.55: `20 OK (skipped=1)`, `errno39_lines=0`,
`tmp_leftover=0`.

**AC-F9, at the scratch head, in the clone.**
- `OK: 195 skill(s) valid, 0 warning(s)`;
- `OK: 181 gate self-test assertion(s) passed.`;
- `OK: 76 contract-audit self-test assertion(s) passed.`;
- `Ran 23 tests … OK`;
- link check of the register: `files: 1 links checked: 49 anchors checked: 11 broken: 0 dead: 0`.

These equal the plan's reference values.

**Measured hazard: the archive tree is not a valid place for AC-F8 or AC-F9.** In `T(52289779)`, an
archive tree with no repository:
- `test_validator.py` gives rc 1;
- `test_markdown_links.py` gives `FAILED (errors=1)`;
- the full `test_offline_ci.py` gives `FAILED (failures=6, errors=2, skipped=1)`, with
  `fatal: not a git repository` from `record-check.py:63`.

So these must run in a clone (RC13e).

**P-REG simulation.** I appended the §6.4 draft to the register at `52289779` in the clone and ran the
AC-R checks against it:
- AC-R1: see §2.
- AC-R2: `0` duplicates; main maximum `119`.
- AC-R3: `1`.
- AC-R4: extraction works.
- AC-R5: `validate-skills.py` OK, `test_validator.py` OK, and link check `broken: 0 dead: 0`
  (`external-skipped: 174`, against 173 at base).
- **AC-R8 on the draft as written** (`grep -cF` on `e.md`):

  | String | Count |
  | --- | --- |
  | the 588-character question | `1` |
  | `Yes, one-time exception (Recommended)` | `1` |
  | `Yes, same terms (Recommended)` | `1` |
  | `Batch it later (Recommended)` | `1` |
  | **`Ask me again (Recommended)`** | **`0`** |

  The label is split across draft L620-621 (RC12b).

**CI facts.**
- **Check-run shapes.** #678 (`3797739c`, register plus docs) shows `changes`, `validate-skills` and
  `gate-guard` as success, with `tools-tests-linux`, `tools-tests-windows` and `windows-offline-checks` as
  skipped. #679 and #680 have the same shape. #661 (`4a9e09dd`) shows `gate-guard completed failure`
  (check run `111308911050`) and predates the `changes` job.
- **Path filter.** A change only to `scripts/tests/…` gives `tools=false` and `offline=false`
  (`validate-skills.yml:94-102`), so the three jobs skip. `windows-offline-checks` does run
  `test_offline_ci.py` (L310) when it is not skipped.
- **Job logs are retrievable.** `gh api repos/ModernNomad-98/Project-Aegis/actions/jobs/111585045661/logs`
  → rc 0, 868 lines. Running `awk '/Z Gate files touched:\r?$/{f=1;next} /Z This PR modifies the merge gate/{f=0} f' | sed -E 's/^[^ ]+ +//'`
  on that log printed exactly `scripts/tests/test_validator.py` and `scripts/validate-skills.py`. That
  confirms a runnable form of the AC-F11 log check.

---

## 4. The owner's words: byte-exact, and nothing invented

`b2-audit/scripts/quotecheck.py` (`94840f9816c6bca2`) compared every `> ` quote line in the plan against
two sources: the brief's one-line forms, and the JSON strings.

| Text | Length / sha256 first 16 | Plan lines that are byte-equal |
| --- | --- | --- |
| Grant question (brief, one line) | 588 / `87eee772606974b1` | L449, L609 |
| Grant option (brief, one line) | 255 / `95826ec00af9e24e` | L462, L613 |
| Q2 question (JSON) | 412 / `51235c50902a464f` | L470 (**not in the draft**: L617 is a placeholder) |
| Q2 option (JSON) | 178 / `ff4684325e17732f` | L474 (draft L619 is a placeholder) |
| Q3 question (JSON) | 213 / `31c08a19b4ec1923` | **none**. Newly available; the plan says it was not relayed. |
| Q3 option (JSON) | 199 / `9938d0d37743b726` | L479 (draft L622 is a placeholder) |
| Q4 question (JSON) | 195 / `b67305a3d3f25d42` | **none**. Newly available. |
| Q4 option (JSON) | 186 / `c07b81c3c8476558` | L484 (draft L621 is a placeholder) |

- **The labels are exact.** In the JSON, the chosen labels are `Yes, same terms (Recommended)`,
  `Batch it later (Recommended)` and `Ask me again (Recommended)`. The plan uses these, and the grant label
  `Yes, one-time exception (Recommended)` as given in the brief.
- **Invents nothing, with one exception.** I checked every FORBIDDEN clause and limit:
  - "only that test file", "for that exact commit" and "every other check green" are quotes;
  - one-time and one use come from "one-time exception … for that exact commit";
  - the moved-head clause comes from the Q4 answer;
  - "does not widen AEGIS-APR-047 / changes no gate_pattern, branch protection or workflow" is a statement
    of fact;
  - both APR-047 phrases exist: "guard scripts and tests" at register L1269, and "separate one-time owner
    decisions" in the L1269-1271 sentence.

  **The exception is the Evidence line.** It says "Repository artifacts that independently record the facts
  above: the Stage D audit … and the `gate-guard` job log". Neither of those artifacts records the owner's
  question or selections. That over-claims (RC12e).
- **One untimed record.** The brief's "OQ-A answer" section has no "Recorded by" line. The next section,
  OQ-B, carries 16:20:07Z. The entry must not assign the JSON a time the brief does not give (RC12c).

---

## 5. Acceptance-criteria review (`acceptance-criteria-reviewer`)

| AC | Verdict | Evidence, or the gap |
| --- | --- | --- |
| F1 | TESTABLE | Reproduced `28 0 …` and `0` |
| F2 | TESTABLE | rc 1 |
| F3 | TESTABLE | Reproduced (§2) |
| F4 | TESTABLE | 264 → 0, from my own census |
| F5 | TESTABLE | 5/5 FAILED, then 5/5 OK, on each Git |
| F6 | TESTABLE | Base 3/3 FAILED with 49 `Errno 39`; head 10/10 OK, 0, 0 |
| F7 | TESTABLE | 20/20 `OK (skipped=1)` |
| F8 | TESTABLE | Already says "in the same clone"; 39 OK on both Gits |
| F9 | **NEEDS-REWRITE** | "Run at H" does not say *in a clone*. In `T(x)`, two of the commands fail falsely (§3). Rewrite: "in the scratch clone checked out at H, never in `T(H)`". |
| F10 | TESTABLE | `0`, `1`, `1` |
| F11 | **NEEDS-REWRITE** | The check-runs command is concrete; "plus the job logs" is not. The rewrite is RC13d; its log commands were tested on job `111585045661`. |
| F12 | TESTABLE | Empty TMPDIRs |
| R1 | TESTABLE | Validated by simulation. Read the hunk header as a prefix (N5). |
| R2 | **NEEDS-REWRITE** | The loop does not implement "except P-REG itself". At the merge re-check P-REG is open, and its maximum equals the new ID, so "greater than every printed maximum" fails falsely (RC13a). |
| R3 | TESTABLE | `1` on the simulation |
| R4 | TESTABLE | Extraction works |
| R5 | TESTABLE | `broken: 0 dead: 0` |
| R6 | TESTABLE | Same shape as #678, #679 and #680 |
| R7 | **NEEDS-REWRITE** | Only the head check has a command. A text search for `SD-F: ACCEPT` on #677 matched comment `6044893720`, which `$S/rcf/MERGE-RECEIPT.md` identifies as the round-1 `SD-F: REVISE`. The check must bind to the verdict's comment ID (RC13b). |
| R8 | **NEEDS-REWRITE** | Returns `0` for the Q4 label on the draft as written. Its "once OQ-A is answered" texts can now be listed (RC13c). |

**Summary: 15 TESTABLE, 5 NEEDS-REWRITE, 0 UNTESTABLE.**

**Gap: boundary.** P-FIX's own size criterion, AC-F1 `a ≤ 40`, has no link to what the owner was told,
"about 28 lines". RC11b handles it.

---

## 6. Recommendations and procedure choices under the owner's scrutiny rule

The owner's rule (BRIEF 17:10:06Z, verbatim): "always audit and scrutinize your recommendations. Do not
make any assumptions on your recommendation, if you are unsure, look for evidence or research it first."

| Plan choice | Evidence it carries | Unproven basis | Outcome |
| --- | --- | --- | --- |
| Fix by repository-local `maintenance.auto false` + `gc.auto 0` (§3.6) | Source, census, forced race, flip (all re-verified) | Runner build options, and a possible runner-level command-line config, are unverified. **The plan misses that its own regression test settles this in CI:** it asserts that no maintenance spawn happens *in the runner's environment*, so a green `validate-skills` at H with `Ran 39 tests` is CI-side evidence. | Fine. Add the counter-argument note (RC16). |
| Keep the regression test (Q5) | Bug-fix floor at `classification-matrix.md:24`; the flip | Whether the owner's grant covers a +28 head after a question that said "adds two lines". The coordinator told the owner the size (16:20:07Z). The owner has not objected, but under `human-approval-boundary` silence is not approval. **The grant's scope is the option text, which scopes by file**, and that is evidence, not assumption. | Keep. Record the disclosure as a coordinator record, never as owner assent (RC11b, RC12d). |
| Q1: skips recorded as skipped | #677–#680 heads show the three skipped jobs with every other check green, and all merged (§3). MG1 says "every **applicable** check". | **Not disclosed:** `windows-offline-checks` would run the changed file itself (`validate-skills.yml:310`). This is a difference of degree only: #680's skipped Windows job would also have run `validate-skills.py` over its changed `README.md`. On Windows, the new method sits in the POSIX-only class (test file L137), but the module-level `from unittest import mock` does execute; it is standard library. | Non-blocking note N1. Q1 is the coordinator's position, and the precedent supports it. |
| Merge pinned with REST `PUT …/merge` `sha` (§6.3 b) | `gh api graphql` → `HTTP 403 … GitHub GraphQL is not available from Claude Code sessions` (re-run by me) | (1) "GitHub refuses that request if the head has moved" has no cite. GitHub's REST docs say `sha` is "SHA that pull request head must match to allow merge", with 409 "Conflict if sha was provided and pull request head did not match" (fetched). (2) **The plan never states its premise that an admin API merge can pass a failing *required* `gate-guard`.** `gh api repos/…/branches/main --jq .protection` shows required contexts `gate-guard` and `validate-skills` with `"enforcement_level":"non_admins"`; `rules/branches/main` → `[]`. GitHub's docs give that field no enum or description, so "admins exempt" is the field's plain reading. It is consistent with #661, admin-merged past a failing `gate-guard` with `gh pr merge --admin --match-head-commit` (receipt comment `5974654607` L118-119), but **an admin REST or MCP merge past a failing required check is unverified in this session.** (3) The only in-session precedent pin is RCF-1's `expectedHeadSha` (`MERGE-RECEIPT.md:7`). That is the MCP `merge_pull_request` parameter, not REST `sha`, and the plan conflates the two. | **RC14** |
| P-FIX merges after P-REG lands | §6.3 | **Not stated:** P-FIX's branch must not be updated onto the new `main`, because that moves H and triggers a Q4 re-ask. Precedent: #661's head `4a9e09dd` was `behind_by=3` against #663's merge `5eb63bb8` (`gh api …/compare`) and was admin-squash-merged as `cc8fd2cb`, whose parent is `5eb63bb8`. Also unstated: check that `main` did not move in a way that touches the fixture's surface. | **RC14** |
| Q4 procedure (§6.3) | APR-032 → 033 → 034 | "A fresh owner answer that names the new head". In the precedent, the owner's reply "parooved" answered a message that named the head (register L923-925); the reply did not name it. Also, the EXPIRED event is coupled to a re-grant, but APR-033 shows EXPIRED recorded by "Project Aegis agent" as a factual event, and Q3 covers consumption only. | **RC15** |
| ETAs (§10) | Labelled "estimates; none is measured" | No basis is given. The owner's rule names estimates explicitly. | RC16 |
| ID 120 | Re-derived: 119 headings, maximum 119, 0 duplicates, 0 open pull requests | none | Fine |
| "29 one-time exception entries" (§6.1) | My re-run of the plan's grep → `29` | none | Fine |

---

## 7. Required changes (for PLAN-rev3)

**RC11 — Re-base the plan on the current inputs and close OQ-A and OQ-B.**
- (a) **Update the inputs.**
  - Name BRIEF.md `31dec83bb660d843…` and the JSON `74c8cd5a559b1398…` in the input table.
  - Record the owner's 17:10:06Z rule verbatim as binding.
- (b) **OQ-A and OQ-B.**
  - Close OQ-A. §4's measurements show the plan's reconstructions of the Q2 question and the Q2/Q3/Q4
    options are byte-equal to the JSON. The Q3/Q4 question texts now exist. Delete the "Caveat on the Q2–Q4
    one-line forms" in §6.2, or turn it into a closed note.
  - Close OQ-B with the coordinator's 16:20:07Z record: the owner was told "about 28 lines", and the entry
    states the real size.
  - Add a guard. Stage C reports `a` from AC-F1. If `a` differs from 28, the coordinator is told before
    P-REG's Stage C, because the owner was told "about 28". This replaces the unexplained `a ≤ 40` as the
    operative check, or justifies 40.
- (c) **OQ-C.** Keep it open. The brief records only that the owner was told and has not objected. Do not
  describe that as acceptance.

**RC12 — Make the §6.4 draft fillable and exact.**
- (a) Replace every Q2–Q4 placeholder with the JSON strings, each on one line: the Q2 question, the Q2/Q3/Q4
  option texts and the Q3/Q4 question texts. Delete the conditional "If OQ-A leaves … unrelayed" clause.
- (b) Keep each owner label on one line. Draft L620-621 splits "Ask me again / (Recommended)". The
  measured AC-R8 count is `0`.
- (c) Evidence: cite the JSON as a session artifact by its sha256, "extracted programmatically from the
  session transcript's own AskUserQuestion call" (the brief's words). Give it no recording time unless the
  coordinator supplies one, because the OQ-A section has no "Recorded by" line.
- (d) Record the size disclosure as a coordinator record (16:20:07Z) and not as owner approval of the size.
  The authority stays the option text's file scope.
- (e) Narrow the over-claim to what is true. For example: the Stage D audit and the `gate-guard` job log at
  H record the head, the single path and the protected-path failure; the owner's question and selections
  are session artifacts only.

**RC13 — Make AC-R2, AC-R7, AC-R8, AC-F11 and AC-F9 runnable and correct.**
- (a) **AC-R2:** exclude P-REG in the command itself, for example
  `--jq '.[] | select(.number != <P-REG>) | .number'`.
- (b) **AC-R7:** give the commands.
  - **Final review.** Take the Stage F verdict's comment ID from Stage F's handoff, then run
    `gh api repos/ModernNomad-98/Project-Aegis/issues/comments/<id> --jq '.created_at, (.body|test("<H>"))'`
    and check its disposition line reads `SD-F: ACCEPT`. Do not text-search: on #677, `test("SD-F: ACCEPT")`
    matched the REVISE comment `6044893720`.
  - **MG3.** `gh api 'repos/…/pulls/<P-FIX>/reviews?per_page=100' --jq '.[]|"\(.user.login) \(.commit_id) \(.submitted_at)"'`,
    and `gh api 'repos/…/pulls/<P-FIX>/comments?per_page=100' --jq '.[]|"\(.id) \(.original_commit_id)"'`
    for each P0–P2 finding. An issue comment covers an unavailability notice, as on #661 (`5974241686`).
  - **Head.** `gh api …/pulls/<P-FIX> --jq .head.sha`.
  - **After the merge.** `gh api …/pulls/<P-REG> --jq .merged_at`, later than every timestamp above.
- (c) **AC-R8:** list the `grep -cF` strings: the 588-character question, the 255-character option, all
  four labels, and the eight JSON strings. Expected: each `≥1`.
- (d) **AC-F11:** give the log commands.
  - Retrieve each log with `gh api repos/ModernNomad-98/Project-Aegis/actions/jobs/<check-run id>/logs > <job>.log`.
    The check-run ID is the job ID: on #661, `gate-guard` check run `111308911050` = job `111308911050`.
  - **`gate-guard`:**
    `awk '/Z Gate files touched:\r?$/{f=1;next} /Z This PR modifies the merge gate/{f=0} f' gg.log | sed -E 's/^[^ ]+ +//; s/\r$//'`
    must print exactly `scripts/tests/test_offline_ci.py`. The `Z` anchor skips the echoed script source,
    which also contains the phrase.
  - **`validate-skills`:**
    `grep -nE 'Z (Ran [0-9]+ tests|OK \(skipped=[0-9]+\)|CHECK ci-tests: exit)' vs.log` must show
    `Ran <n+1> tests`, `OK (skipped=1)` and `CHECK ci-tests: exit 0`, then `OK (skipped=5)` for BER, as at
    attempt-2 L944-948 and L4524-4526.
- (e) **AC-F9 and §5.1:** state that every full-suite or repository check runs in the scratch clone at the
  revision, never in `T(x)`. Cite the measured false failures in §3. `T(x)` stays valid for the
  `ProtectedFileGuardTests`-only runs (AC-F4..F6).

**RC14 — Evidence the merge mechanism; add a fail-closed rule; do not update P-FIX after P-REG.**
- (a) §6.3(b) cites three things:
  - the REST doc for `sha`, with the 409 refusal;
  - the GraphQL 403 output;
  - the `branches/main` protection output (`enforcement_level: non_admins`, required `gate-guard` and
    `validate-skills`, rulesets `[]`) as the basis for the admin bypass. Label it **unverified in this
    session** for a failing required check, with #661 as the corroborating precedent.
- (b) Separate the two pin mechanisms: REST `sha`, and the MCP `merge_pull_request` `expectedHeadSha`, which
  is RCF-1's in-session precedent. Let the merge agent use either, as long as the receipt records which
  one and the pinned value.
- (c) **Fail closed.** If the pinned merge call is refused, for any reason, P-FIX is NOT MERGED and goes
  back to the coordinator. Never retry unpinned, never change protection or settings, and never update
  the branch to get past it.
- (d) **No update after P-REG.** After P-REG merges, P-FIX's branch must not be updated, rebased or merged
  with `main`, because that moves H. Cite the #661 behind-main precedent.
- (e) **At P-FIX Stage G:** run `git diff --name-only <B> origin/main`. Every path in it other than the
  register must avoid the scope-lock set: the test file, `.github/workflows/`, `scripts/ci/record-check.py`
  and `scripts/validate-skills.py`. If not, stop and return to Stage A.

**RC15 — Make the Q4 procedure exact.**
- (a) Replace "a fresh owner answer that names the new head" with "a fresh owner answer to a question that
  names the new 40-character head". Cite APR-034, where the owner's "parooved" answered a message naming
  `fd2e27e4…`.
- (b) **If the owner declines, or does not answer:** after P-REG has merged, APR-120's EXPIRED event is
  still a factual record. APR-033 was recorded by "Project Aegis agent". State that it is appended, with
  or without a new GRANT. Its timing is a coordinator decision, or an owner question; the Q3 answer covers
  consumption only, so it does not decide this. Do not assume Q3 extends to it.

**RC16 — Apply the owner's scrutiny rule inside the plan.**
- (a) End each recommendation section with a self-scrutiny note: the strongest counter-argument, and the
  evidence that would change it. The sections are §3.6 (fix choice), §4 (keep the test / OQ-B),
  §6.3 (vehicle, timing, merge mechanism, head move), §6.6 (consumption) and §10 (ETA).
- (b) In §3.6, add the CI-side evidence argument from §6 above.
- (c) In §10, label each ETA "unverified". Give a measured basis where one exists in this session, such as
  round-1 Stage B at 15:52:33Z–16:07:03Z, or say none exists. The owner's rule bars using an unproven
  estimate as a basis for a recommendation.

---

## 8. Non-blocking notes (carry into the evidence; no plan change needed)

- **N1. Windows.** `windows-offline-checks` would run the changed file, but on a pull request it is skipped
  by the path filter. On Windows, only the module-level `from unittest import mock` executes; the new
  method is in the class skipped by L137. The post-merge push run is the Windows evidence. Stage E should
  name this precisely.
- **N2. AC-F10 `rev-list --count = 1`.** A rework after a REVISE would need an amend and a force-push to
  stay at one commit. Either is a head move anyway, but the plan does not say whether a force-push is
  intended. "Every commit in `B..H` signed off" would be the less brittle form.
- **N3. P-FIX's PR body.** The body cites `#<P-REG>` and `AEGIS-APR-120` before P-REG exists. Both sit in
  "What & why", outside the bound fields. Adding or correcting them later leaves the bound-field hash and H
  unchanged. Say so, so that no one thinks the edit voids Stage F.
- **N4. Precedent fields.** APR-106's Evidence also cited the Stage A plan hash and the Stage B ACCEPT as
  corroborating session artifacts. Optional for APR-120.
- **N5. AC-R1's hunk line.** It carries git's trailing context (`@@ -5154,0 +5155,74 @@ the entry governs.`).
  Match on the `@@ … @@` prefix, or count hunks with `grep -c '^@@'` → `1`.
- **N6. Reviewer independence.** Consider not giving P-REG's D/F reviews to P-FIX's Stage D auditor. The
  entry cites that auditor's own audit, so a reviewer would be checking a record of its own work. No rule
  requires this.

---

## 9. Self-scrutiny (auditing my own recommendations)

- **REVISE versus ACCEPT-with-notes.** The strongest counter-argument: proportionality says a small change
  must not need multi-round review, and the code fix itself is proven. I hold REVISE for three reasons:
  - two criteria would give false results on the plan's own text (AC-R8 → `0`; AC-R2 self-inclusion);
  - two have no runnable command (AC-R7; AC-F11 logs);
  - the governance entry cannot be written from rev2 without a later stage choosing text the plan left
    open. That is the kind of later-stage invention SD-B exists to stop.

  What would change my mind: evidence that later stages are bound to take those texts and commands from
  this audit rather than from the plan. There is none: SD-B binds the plan revision.
- **RC14's admin-bypass premise is itself an inference from me.** I could not prove an admin REST merge past
  a failing required check without performing a write, which my stage forbids. So RC14 asks only that the
  plan *label* it unverified, cite the evidence that exists, and fail closed. It does not ask the plan to
  assert it.
- **RC15(b) could look like adding process.** The counter-argument: APR-120 is unspendable after a move
  anyway, and the preamble says historical ACTIVE text alone does not authorize. That is right for safety,
  but the register's own precedent (APR-033) records EXPIRED facts. The rule is that "lifecycle events
  append", so leaving it unrecorded is the departure.
- **Byte-exactness depends on the JSON being authentic.** I verified its hash against the brief's stated
  value. I cannot see the transcript the coordinator extracted it from, so its fidelity to what the owner
  saw is **the coordinator's attestation, unverified by me**.
- **My harness had a defect, now fixed.** The first natural-stress call passed an empty selector, which
  `${6:-…}` replaced with the class name, so it ran 11 tests, not 39. I caught it from `results=[20 OK]`
  lacking `skipped=1`, added the `ALL` selector, and re-ran: 20× `OK (skipped=1)`, `Ran 39 tests`. The
  harness hash above is the fixed one.
- **Not re-run:** the planner's `ab_force.sh` and `trace_count.sh`, because I used my own equivalents.
  Windows, Python 3.14 and pwsh remain **UNRUN** (no host).

---

## 10. Handoff block

1. **Decision IDs.** `SD-A`–`SD-G` and `MG1`–`MG5` still bind, unchanged. Relied on: AEGIS-APR-032/033/034,
   047, 048, 050, 100, 105, 106 and 107 as read at `52289779`, and the owner's 2026-10-08 grant, Q2/Q3/Q4
   answers and 17:10:06Z rule. This audit changes no decision.
2. **Changed files: none in the repository.**
   - Real checkout: `git status --porcelain | wc -l` → `0`; `HEAD` → `c060a7cb…`, detached;
     `git for-each-ref refs/remotes/pr | wc -l` → `0`.
   - I ran no `git fetch`. `.git/FETCH_HEAD` mtime is 17:10:34Z, before my start.
   - `git clone --shared` read from the repository and wrote only under scratch.
   - **Scratch written:** this file and `$S/cifix/b2-audit/**`: the scripts, `trees/{base,proto,reverted}`,
     `clone` (scratch commits `6d3396e5…` and `5b3557c6…`, never pushed; left detached at `52289779`),
     `out/**`, `register-main.md`, `wf-main.yml` and `CONTRIBUTING-main.md`.
   - **Not touched:** every repository path, `.github/`, the register, GitHub (reads only: GETs plus one
     refused GraphQL probe) and reserved scope. The MCP merge tool's schema was loaded to read its parameter
     names. It was never called.
3. **Proven invocation.** Every figure above carries its command and output.
   - **Unverified:** an admin REST or MCP merge past a failing required check in this session; the
     transcript fidelity of the JSON; the runner's Git build options.
   - **UNRUN:** Windows, Python 3.14, pwsh.
4. **Deviation flags.**
   - **Plan deviations:** stale inputs (RC11), an incomplete draft (RC12), non-runnable or false-result
     criteria (RC13), unevidenced merge premises (RC14), Q4 wording and the EXPIRED gap (RC15), no
     self-scrutiny notes (RC16).
   - **Own deviations:** none from my brief. The harness defect is disclosed in §9.
5. **Continuation.** The Stage A holder writes PLAN-rev3 applying RC11–RC16. A Stage B holder who is not the
   planner re-audits it at its new sha256. Stage C must not start on rev2.

**Timing.** Started 2026-10-08T17:11:40Z (`date -u`). The finish time and this file's sha256 are given in the
handoff, so that recording them does not change the hash. No ETA was given to me. The plan's §10 estimate for this re-audit, "10–20 min", is unverified and is
compared in the handoff. Active time was not measured separately.
