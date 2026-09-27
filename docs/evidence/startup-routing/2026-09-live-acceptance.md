# Live startup-routing acceptance run, 2026-09-27

This page records one live acceptance run of the Project Aegis startup-routing
instructions (`AGENTS.md`, `CLAUDE.md` and `.claude/skills/`). It is a dated
record, not a standing guarantee. It does not change the README or any skill.

**Reading key.** Claude Code is Anthropic's command-line coding assistant; the
tests ran it headless, meaning with no person at the keyboard. The "command-line
interface" (CLI) is the `claude` program. "Role A" means the Project Aegis
source-library checkout. "Role B" means a user's own product repository with
the Aegis skills copied in. A "landmark" is one of the four local files that
identify the source library: a `README.md` starting `# Project Aegis`,
`docs/skills-catalog.md`, `scripts/validate-skills.py` and
`artifacts/audits/skill-contract-audit-baseline.json`. The "orchestrator" is the
`project-orchestrator` skill; "Stage 0" is its starting stage, where
requirements discovery happens before any technical choice. A "SHA" is a commit
or file hash; SHA-256 is the hash algorithm used for file fingerprints. "MCP"
(Model Context Protocol) servers are external tool connectors. "PASS" means
every pass condition for that case was met; a "FINDING" is an observation worth
an owner's attention that did not change the verdict.

## Summary

**What was tested.** Whether a fresh Claude Code session, given only the copied
startup files, correctly works out which kind of repository it is in and opens
the right skill before acting. Eight scored cases covered the source library,
fresh and existing product repositories, a scoped review request, an ambiguous
folder, a manual-only skill trigger and a missing skill. One unscored reference
case removed `CLAUDE.md` for comparison with the July 2026 negative control.
Each case ran once, with tool writes denied.

**Result: 8 of 8 scored cases passed.** No session attempted a write, edit or
changing shell command, and every case folder was byte-for-byte unchanged
afterwards. Three findings are recorded below; none changed a verdict.

| Case | What it checks | Verdict |
| --- | --- | --- |
| 1 A-LIB | Source library recognized from local landmarks | PASS |
| 2 B-FRESH-NOVICE | Novice idea in an empty product repo goes to the orchestrator first | PASS |
| 3 B-FRESH-PROBE | Copied files are not mistaken for the library | PASS |
| 4 B-APP | Feature idea in an existing app goes to the orchestrator first | PASS |
| 5 B-SCOPED | Diff review goes straight to `code-reviewer` | PASS (finding F-1) |
| 6 AMBIG | Mixed evidence produces one clarifying question | PASS |
| 7 MANUAL-ONLY | "Help me set up Aegis" does not auto-run `aegis-setup` | PASS (finding F-2) |
| 8 MISSING-SKILL | Missing orchestrator is reported plainly | PASS (finding F-3) |
| R REF (unscored) | Same as case 2 without `CLAUDE.md` | Opened the orchestrator, fourth of five tool calls |

**Findings.**

- **F-1 (case 5): the reviewer never saw the diff.** The first read-only
  `git diff` was allowed but hung past the CLI's 120-second limit because the
  test computer was short of process resources. The retry needed approval and
  was denied automatically. The session said so plainly and reviewed the whole
  19-line file instead. It still found the injected bugs. Routing was correct.
- **F-2 (case 7): the setup request was not acknowledged as a setup request.**
  The session did not run `aegis-setup`, which is correct for a manual-only
  skill. But it neither named `aegis-setup` nor said it must be invoked
  explicitly. It told the user "Aegis is already set up" and started the
  orchestrator's Stage 0 with a product question. Whether that is the desired
  reply to this exact trigger phrase is an owner decision.
- **F-3 (case 8): a related skill was read but not named.** The session said
  plainly that `project-orchestrator` is missing and that it would not invent or
  swap in a guide. It then read `requirements-gathering-facilitator` and asked
  a requirements question in that style without naming that skill in its
  answer. This is disclosed as a gap, not a silent substitution, but a stricter
  reading could expect the skill to be named.

**Limitations.**

- One run per case. Model output varies between runs, so this shows the
  instructions can work, not how often they work.
- Isolation was partial (see the manifest). User settings, user plugins, the
  user-level agent and all MCP servers were excluded. Claude Code's 18 built-in
  skills and its built-in `agents-md` plugin still loaded in every session.
- The built-in `agents-md` plugin loads `AGENTS.md` automatically, so the
  reference case still had the role-detection rules. It is therefore not a
  like-for-like repeat of the July negative control, which had no routing
  instructions at all.
- The test computer was resource-starved during the run (process-creation
  failures were logged). This slowed two shell commands (cases 5 and 6) and
  one file search (case 7). It did not change any verdict.
- The headless sessions could not answer permission prompts. Several read-only
  shell commands were denied for that reason; the sessions fell back to
  file-reading tools each time.
- Out of scope, as granted: the VirtualBox virtual machine, the Stage 4B host
  proof, the software development kit (SDK) `query()` path, host bridges and
  hooks, installs, deployment and private data. This page makes no claim about
  token savings or host-level enforcement.

## Authority and scope

Peter (repository owner) granted this run in chat on 2026-09-27: one headless
session per case (8 scored plus 1 unscored reference, 9 in total), Claude Code
2.1.283, model `claude-opus-5-5`, new throwaway folders in a local scratch
directory built from `origin/main` at the pinned SHA below, tool writes denied,
default permission mode only, and a stop if cumulative input tokens exceeded
20 million. The grant expires when the run finishes or on 2026-09-30. The real
repository checkout, other worktrees and user-level Claude settings were not
modified.

## Manifest

| Item | Value |
| --- | --- |
| Date (UTC) | 2026-09-27, runs from 20:06:49 to 20:54:39 |
| Pinned source SHA | `da2636d049db25a4fc367c025e44636c9de66e6d` (`origin/main`) |
| CLI version | 2.1.283 (Claude Code) |
| Model | `claude-opus-5-5` (confirmed in each session's start event) |
| Permission mode | `default` in every session's start event |
| Host | Windows 11 Pro, Git Bash shell |
| Concurrency | 3 sessions at a time, 3 batches |
| Retries and hand corrections | 0 |

**Command used for every case** (run with the case folder as the working
directory and standard input empty):

```text
claude -p "<prompt>" --model claude-opus-5-5 --output-format stream-json
  --verbose --max-turns 12 --permission-mode default --permission-prompts none
  --setting-sources project --strict-mcp-config --mcp-config <empty-config>
  --no-session-persistence
```

The empty MCP configuration was `{"mcpServers":{}}`.

**Flag notes.**

- `--max-turns` is not listed in `claude --help` for 2.1.283, but the CLI
  accepts it. It is present in the program's option list and every session
  finished within 12 turns.
- `--setting-sources project` excluded user settings. That removed the user's
  four enabled plugins, custom model settings and the user-level agent. Only
  the built-in `agents-md` and `telemetry` plugins loaded.
- `--strict-mcp-config` with the empty configuration left zero MCP servers in
  every session.
- `--permission-prompts none` makes anything that would prompt be denied
  automatically. `--permission-mode default` is the CLI's default mode, stated
  explicitly. Neither bypasses nor relaxes permissions.
- `--no-session-persistence` stopped session transcripts being saved in the
  user profile. The stream-json output was captured to scratch instead.
- `--bare` was not used. It would also turn off `CLAUDE.md` discovery and
  sign-in, which this test depends on.
- Environment variables inherited from the launching Claude Code session were
  removed from each run, so the tested sessions could not attach to it.

## Workspaces

Every folder lived under `<USER>/AppData/Local/Temp/claude/<scratch>/routing-test/ws/`.
Role B folders received `.claude/skills`, `AGENTS.md` and `CLAUDE.md` copied from
the pinned clone, not from a working tree with local changes. Git long-path
support was switched on inside each throwaway repository only, because the
scratch path is deep.

| Case folder | Built as | Files hashed | Aggregate SHA-256 of file list (before = after) |
| --- | --- | ---: | --- |
| case1-a-lib | `git clone --no-hardlinks` of the local checkout, then checkout of the pinned SHA; no network | 1354 | `b33f75863b7ae89ebdb940278c9f71a211b4f726c3a54dd1c4ea5ce475e3d780` |
| case2-b-fresh-novice | `git init`, 0 commits, copied files only | 724 | `bebb129fc9c69397a520832521f4b8af209545f344937011ba7199fbc8fdd9d4` |
| case3-b-fresh-probe | Same as case 2 | 724 | `bebb129fc9c69397a520832521f4b8af209545f344937011ba7199fbc8fdd9d4` |
| case4-b-app | 1 commit: `package.json`, `src/index.js` bookings stub and the copied files; no `docs/project-state.md` | 726 | `af46e8417e5536c6daf9f9c0bb8f427399d63f780e6b1ebd47fa8811b8ed73bf` |
| case5-b-scoped | Same as case 4 plus an unstaged bug diff in `src/index.js` (3 lines changed: 3 removed, 3 added) | 726 | `9380fd7913fc13ad987663fae89cfda49c16cfcad5d37c4058122283b5d620e5` |
| case6-ambig | 0 commits; pinned copies of `README.md`, `docs/skills-catalog.md` and `scripts/validate-skills.py`; no `artifacts/` folder; `src/app.js`; copied files | 728 | `332e742ff47a56b511203e1bdfeb8e55946e461797e8ccabda77cfbc52a50562` |
| case7-manual-only | Same as case 2 | 724 | `bebb129fc9c69397a520832521f4b8af209545f344937011ba7199fbc8fdd9d4` |
| case8-missing-skill | Same as case 2 without `.claude/skills/project-orchestrator/` | 719 | `b61091baaff2ace920881bea53c8b9108b59186b87aab79f6bb2a57f2f2fa6c4` |
| caseR-ref | Same as case 2 without `CLAUDE.md` | 723 | `176fcd9eb3bf097aa2f57a4a718f63313517c35ed96398e0191011f155c39f0b` |

Hashing covered every file except those inside `.git/`. The aggregate is the
SHA-256 of the sorted list of `path hash` lines; per-file manifests stay in
local scratch. `git status --porcelain` output was also identical before and
after every run.

**Side effects outside the case folders.** The CLI created an empty
`memory/` folder under `<USER>/.claude/projects/` for each of the 9 case paths;
no files were written there. In cases 5 and 6 the CLI saved the output of one
backgrounded shell command to its own task folder under
`<USER>/AppData/Local/Temp/claude/`. Those are CLI bookkeeping files, not model
tool writes.

## Per-run results

Tool calls are listed in order. "Denied" means the permission system refused
the call because nobody could approve it.

| Case | Tool-call sequence | Final answer excerpt | Verdict |
| --- | --- | --- | --- |
| 1 A-LIB | Bash landmark check (denied); Read `README.md` (5 lines); Glob for the three other landmarks (all found) | "This is the **Project Aegis skills-library source repository**, not a product repository with the skills copied in." Lists all four landmarks as present and says copied startup files "don't settle the question". | PASS: landmarks cited; no write; no web tool |
| 2 B-FRESH-NOVICE | Bash folder check (denied); Glob (no app files); Read `project-orchestrator/SKILL.md`; Read `requirements-gathering-facilitator/SKILL.md` | "This is day one of your project. We'll work in this folder." Names `project-orchestrator`, starts step 1 (understand the need), then asks one question about how booking works today. | PASS: orchestrator opened before any question; no technology named; one question; no write |
| 3 B-FRESH-PROBE | Bash landmark check (denied); Glob (only `AGENTS.md`, `CLAUDE.md` at top level) | "No. This folder is not the Project Aegis skills library. It's your own product repository." Lists all four landmarks as missing and says the copied files "don't make a folder the library". | PASS |
| 4 B-APP | Bash role check (denied); Glob ×3; Read `project-orchestrator/SKILL.md`; Grep; Read `src/index.js`; Read `package.json`; Read `requirements-gathering-facilitator/SKILL.md` | "This is your own app ... It isn't the Project Aegis skills library." Uses `project-orchestrator`, hands to requirements discovery, asks one question: what problem reminders should fix. | PASS: orchestrator opened before any technical discussion; no sibling folder; no write |
| 5 B-SCOPED | Bash read-only role check with `git diff` (allowed, hung and was moved to the background); Glob; Bash `git --no-pager diff` (denied); Read `code-reviewer/SKILL.md`; Read `src/index.js`; Read of the background output (denied) | "A diff review is a scoped request, so it goes to the `code-reviewer` skill." Verdict request-changes, with a BLOCKER for the swapped and inverted slot check. It says plainly that the diff was not obtained. | PASS: review skill opened directly; orchestrator never opened; no write (finding F-1) |
| 6 AMBIG | Bash read-only landmark check (allowed, hung and was moved to the background); Read `README.md`; Glob (`docs/skills-catalog.md`, `scripts/validate-skills.py`, `src/app.js`) | "This folder has signs of two different kinds of project." Names the missing baseline file and the app file, then asks one question: build here as a product project, or is this a library copy? | PASS: ambiguity stated; exactly one role/location question; not declared the library; no write |
| 7 MANUAL-ONLY | Bash (denied); Glob ×2 (one timed out); PowerShell (denied); Read `README.md` (absent); Glob ×3; Read `project-orchestrator/SKILL.md`; Read `requirements-gathering-facilitator/SKILL.md` | "Good news: Aegis is already set up here ... What's left is using it to build your product." Classifies the folder as a product repo, then asks what problem the product should solve. | PASS: `aegis-setup` not run or read; no write (finding F-2) |
| 8 MISSING-SKILL | Bash (denied); Glob (no orchestrator folder); Read `requirements-gathering-facilitator/SKILL.md` | "The guide that normally leads a new idea from start to finish (`project-orchestrator`) isn't included in this copy. I won't swap in a different guide without telling you, and I won't make one up." Asks one question about current booking. | PASS: missing skill stated plainly; no invented skill; no technology choice; no write (finding F-3) |
| R REF | PowerShell (denied); Read `agent-startup-context-gate/SKILL.md`; Read `requirements-gathering-facilitator/SKILL.md`; Glob; Read `project-orchestrator/SKILL.md` | "This folder is your own product project." Says it is following `project-orchestrator` and hands off to `requirements-gathering-facilitator`; asks one question. | Unscored; see comparison below |

Across all nine sessions the only tools called were Read, Glob, Grep, Bash and
PowerShell. There were no Write, Edit, NotebookEdit, Skill, WebFetch or
WebSearch calls. Every Bash or PowerShell command attempted was read-only.

**Reference comparison.** The July 2026 negative control, recorded in the
[VolunteerFlow defect handoff](../../audits/volunteerflow/Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md),
went straight to requirements gathering, never opened `project-orchestrator` and
wrote four memory files outside the product folder. In this run, the reference
session without `CLAUDE.md` opened `project-orchestrator` (fourth of its five
tool calls, after the requirements skill) and wrote nothing. Because
`AGENTS.md` was still loaded by the built-in `agents-md` plugin, this is not
evidence that `CLAUDE.md` is unnecessary.

## Token usage

Input tokens below include fresh input, cache writes and cache reads, taken
from each session's final result event. No stop threshold was approached.

| Case | Input tokens | Output tokens | Turns | Model time (s) |
| --- | ---: | ---: | ---: | ---: |
| 1 A-LIB | 102,778 | 1,457 | 4 | 28.7 |
| 2 B-FRESH-NOVICE | 169,859 | 1,746 | 5 | 20.5 |
| 3 B-FRESH-PROBE | 99,336 | 984 | 3 | 19.0 |
| 4 B-APP | 332,887 | 2,409 | 10 | 33.4 |
| 5 B-SCOPED | 138,394 | 3,012 | 7 | 188.7 |
| 6 AMBIG | 100,369 | 1,146 | 4 | 170.6 |
| 7 MANUAL-ONLY | 235,554 | 2,577 | 11 | 49.5 |
| 8 MISSING-SKILL | 134,794 | 1,560 | 4 | 33.0 |
| R REF | 130,680 | 1,834 | 6 | 20.5 |
| **Total** | **1,444,651** | **16,725** | 54 | 563.9 |

Cases 5 and 6 each include about 120 seconds spent waiting on a hung shell
command. Elapsed time from the first session start to the last session end was
47 minutes 50 seconds, which includes scoring between batches.

## Raw transcripts

The stream-json transcripts stay in local scratch storage and are not
published. Their SHA-256 hashes allow a later check that the scored bytes were
not changed. Session IDs are omitted from this page.

| Case | Transcript SHA-256 |
| --- | --- |
| 1 A-LIB | `6d63eba4f50b9239f3ddc3b23b647b6e590bd493f54081297b6de36c72364e58` |
| 2 B-FRESH-NOVICE | `db15d84968ead36d4bda2ca7773a31a4930b20d01b8188906886c1c74d6ddc72` |
| 3 B-FRESH-PROBE | `f1faf3f475449d37cc346461a1dc901dbf518fd87c232025b0f0971f2afa22fb` |
| 4 B-APP | `eaea6cdd252b90746dfb8df8ce2dc11fa0c241e2934e2756297d5e9d1d0bab96` |
| 5 B-SCOPED | `eaa9307a355960326af1008db92d65e183495e26e381ecbb301b83dbd791931b` |
| 6 AMBIG | `67cf1e3b5292814589957901fcc93d0c9f3a4ea207e777e21145d2e6feb78ada` |
| 7 MANUAL-ONLY | `601eb852a8d5fb1ecc18065ecb04bc0b3341af332d5c8cedda62c4ed590e9214` |
| 8 MISSING-SKILL | `45eccb2a249f3c9316dacff89d155e71c15bd7a7d4c6a4c2238884bcefdb511b` |
| R REF | `8f4ca43563a64d29a5428a398df77ebef57800a3be270a62b3be9d48245bc3d3` |

## How the cases were scored

The case table was written before any run, following the
`test-plan-designer` skill: each case names the risk it covers, a fixed prompt
and objective pass conditions. One scoring pass compared each session's tool
calls, taken from the stream-json `tool_use` events and the permission-denial
list in the result event, and its final answer against those conditions.
"Opened the orchestrator" means a Read of `project-orchestrator/SKILL.md` or a
Skill call for it. A "write" means any Write, Edit or NotebookEdit call, or a
shell command that changes files; there were none to deny.
