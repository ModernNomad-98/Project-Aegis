# CP-01 — host capability: a genuinely new consumer coding session, executed and observed

| field | value |
| --- | --- |
| Case | CP-01 (host capability), AEP#3 Item 2 |
| Frozen acceptance text | "Actual instruction discovery/readback, independent review contexts and a new coding session are demonstrated before investing in the build." (`TWENTY-TWO-CASE-FREEZE.md` line 58; `cases.json` case_set_sha256 48a28ba1…) |
| Plan row | "Actual discovery/readback, independent review contexts and genuinely new coding-session capability; host/profile/version and session evidence." (`02-hosted-consumer-proof.md` line 68) |
| Verdict | **PASS (observed)** — one component carries a stated residual (§8) |
| Authority | Owner decision CP-01 AUTHORIZED, 2026-10-29 ~06:26 PDT, recorded in `_A/work-package-3/OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md` |
| Session | `01a187dc-7a82-79b1-8680-d72b53899da9` (new thread, cold context) |
| Agent / model / vendor | `codex exec` (Codex CLI 0.163.0-alpha.10.2), model `gpt-6-astra`, **OpenAI** |
| Working root | `C:\src\_aep3_cp01_consumer` — fresh clone, branch `aep3-i2/startup-readback`, HEAD `338ba8240e74aa6b70083121ff4f495804ea63e7` |
| Window (UTC) | 2026-10-29T13:32:15.123Z → 13:37:10.657Z (295,523 ms = 4 min 56 s) |
| Exit | process exit code **0**; 0 failed turns; 0 file-change events |
| Adjudicated by | AEP3-I2 CP-01 AGENT (DeepSeek V4 Flash via DSH), a separate session from the one that produced the behaviour |

---

## 1. Verdict and what it rests on

The frozen sentence names three things and the plan row adds a fourth. Each is now an observation, not an inference:

| # | Required | Observed | Where |
| --- | --- | --- | --- |
| 1 | Actual instruction discovery **and readback** | The session located `AGENTS.md`, `CLAUDE.md` and the startup skill by reading the tree, read them, and returned a table of the governing rules with source paths and line anchors (§6) | transcript items 1–5; final message |
| 2 | Independent review contexts | The non-author plan re-audit (RV-1, 2026-10-28 16:19–16:26 PDT) returned ACCEPT with C-1/C-2 closed, and the independent code/pipeline review returned PASS; both are already PASS rows in `CP-LEDGER.md` (CP-08, CP-10) | `AUDIT-SUMMARY-v4.md`; `REVIEW-SUMMARY.md` (read first-hand for this record) |
| 3 | A new coding session | New process, new thread id, cold prompt, no resume/fork, cwd = the clone; 9 commands, 5 agent messages, no writes | `process.json`; `session.jsonl`; `READ-LEDGER.json` |
| 4 | Host/profile/version and session evidence | OS, shell, node, git, both Codex CLI versions, provider account, DSH profile, and the session id/window/exit | `evidence/host-profile.json`; §4 |

Nothing here is taken from what the session says about itself where a file can be checked instead. §6 verifies every quotation it made against the repository bytes.

---

## 2. Authority, and what changed

The owner decision is recorded verbatim in `OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md`:

> **CP-01 — AUTHORIZED**
> A fresh independent agent session, different vendor from every prior consumer session, started cold on the consumer repo with only the business prompt, recorded as the "genuinely new consumer coding session" (agent, not human). Score CP-01 on what it does, not what it reports.

Before this run the ledger had CP-01 **UNRUN**, with the gap "no genuinely new coding session has been started, so that component is unobserved" and the closing action "one new session demonstrating discovery/readback (see CP-18 route)". This record supplies that observation and nothing else: it does not touch CP-18, which asks the *receiver* to derive state, decisions, authority and next action from durable records.

---

## 3. Setup — exactly what the session was given, and what it was not

| Item | Value |
| --- | --- |
| Repository | `https://github.com/ModernNomad-98/aegis-consumer-proof.git`, branch `aep3-i2/startup-readback` |
| Clone | `C:\src\_aep3_cp01_consumer`, made by this task with `git clone --branch`; 107 tracked files; worktree clean before and after; `HEAD` unchanged at `338ba82…` |
| Installed profile present | `AGENTS.md` (25,228 B), `CLAUDE.md` (2,687 B), 39 files under `.claude/` |
| Prompt | 863 bytes, SHA-256 `3a23c063f9b4de4b1b92208aec4bbe2f0479061b13ccdbd1f7bfaa7701ab964c`; reproduced verbatim in `SESSION-TRANSCRIPT.md` |
| Environmental line added | "Work inside C:\src\_aep3_cp01_consumer — that is a fresh clone of the repository named below, and it is where all of your work happens." Disclosed because it is not literally part of the business request; it carries location only, no answer |
| Not supplied | no CP ids, no case text, no ledger, no prior transcript, no plan, no answer key, no repo summary, no continuation or fork |
| Answer-key scan of the clone | 0 files contain `work-package-3`, `_A/`, `OWNER-DECISION-BATCH` or `CP-LEDGER` (`evidence/clone-identity.json`) |
| Excluded by rule | `claude` 2.1.311 (Anthropic). All three prior consumer sessions ran `claude-sonnet-5-5` (§7), so Claude is the one vendor that could not be used |

---

## 4. Host, profile, version and session evidence

Host (`evidence/host-profile.json`, captured 13:32:28Z): Windows 11 Business 10.0.26200, 64-bit; PowerShell 7.6.6; node v24.19.0; git 2.55.0.windows.5; Codex CLI **0.149.1** on PATH and **0.163.0-alpha.10.2** bundled with the installed Codex app; `codex login status` = "Logged in using ChatGPT"; DSH app 44.0.0, profile `desktop`.

Session: thread `01a187dc-7a82-79b1-8680-d72b53899da9`, sandbox policy `workspace-write`, approvals non-interactive, 26 JSONL events, 9 command executions, 5 agent messages, 0 errors, 0 file changes; usage 840,337 input tokens (757,120 cached), 4,249 output tokens, 148 reasoning tokens.

### 4.1 Provider calls that were denied before the session could start

Recorded because they are part of what the host actually does (`evidence/denied-provider-attempts.json`, exact error text):

| # | Binary | Model asked for | Result |
| --- | --- | --- | --- |
| 1 | `codex` 0.149.1 (PATH) | `gpt-6-astra` (host config) | exit 1 after 13.9 s; HTTP 400 — "The 'gpt-6-astra' model requires a newer version of Codex. Please upgrade to the latest app or CLI and try again." |
| 2 | `codex` 0.149.1 | `gpt-5.1-codex` | HTTP 400 `model_not_found` — "not supported when using Codex with a ChatGPT account" |
| 3 | `codex` 0.149.1 | `gpt-5-codex` | same rejection |
| 4 | `copilot` 1.0.98 | `gpt-5.1` | exit 1 — model not available from the `--model` flag |

The session was then started with the newer CLI already present on the host (invoked directly; nothing was installed, upgraded or uninstalled). Every attempt also printed a non-fatal MCP transport error: `rmcp … AuthRequired … api.githubcopilot.com` — the session ran to completion regardless (`session.stderr.txt`).

---

## 5. What the session did — actions, writes, exit

Nine command executions, all inside the clone, all read-only:

| # | Command (abridged) | Exit | Output | What it establishes |
| --- | --- | --- | ---: | --- |
| 1 | `Get-Location; git remote -v; git status --short --branch; rg --files …` | 1 | 1,527 | located the clone, remote and branch; `rg` is not installed for its shell, so the search failed and was redone with PowerShell |
| 2 | `git ls-files; Get-ChildItem; Select-String …MEMORY.md…; Get-Content AGENTS.md; CLAUDE.md; README.md` | 0 | 38,889 | enumerated 107 files; checked its own host memory for prior knowledge; read the three instruction surfaces |
| 3 | `Test-Path` on the four source-library landmarks and `docs/project-state.md`; `git rev-parse` | 0 | 52,045 | role classification by landmark absence — the rule AGENTS.md itself prescribes |
| 4 | read `agent-startup-context-gate/SKILL.md` from line 270, its checklist reference, `docs/consumer-install-record.md` | 0 | 23,616 | followed the skill the startup rule requires |
| 5 | read `AGENTS.md` lines 86–145, skill lines 230–273, `human-approval-boundary` | 0 | 18,686 | found the authority/merge rules and the manual-only policy |
| 6 | `git log -5 --oneline`; `docs/evidence/release-readiness/B.md`; `HASH-MANIFEST.md`; `docs/evidence/index.md` | 0 | 27,072 | recovered durable release state and the integrity basis |
| 7 | `Select-String` for its own rule phrases across four files | 0 | 4,805 | re-checked the exact wording of the rules it intended to quote |
| 8 | loop over `HASH-MANIFEST.tsv` comparing bytes/LF/SHA-256 | 0 | 59,880 | the read-only integrity step it chose as the next authorized step |
| 9 | SHA-256 re-check via `[Security.Cryptography.SHA256]` | 0 | 743 | fallback after a hashing cmdlet was unavailable |

**Writes: none.** `file_changes` events = 0; `git status --porcelain` = 0 lines after the session; `HEAD` still `338ba82…`; no command wrote, staged, committed, pushed, dispatched or changed a setting. The session says "No files were written"; that claim is checked against the tree, not accepted.

**Out-of-clone reads: two, both disclosed.** Commands 1 and 2 grep the host memory file `<home-path withheld>\.codex\memories\MEMORY.md` for `consumer-proof|_aep3_cp01|startup-readback`. Both returned **0 matches** — the agent was checking whether it already knew this repository, and it did not. No planning-workspace path (`_A/`, `work-package-3`) appears in any command.

---

## 6. Discovery and readback — checked against the bytes, not taken on trust

The session returned a table of rules: source, exact wording, effect. I re-read every cited file independently and searched for each quoted string:

| Quoted passage | Cited | Found at | Verdict |
| --- | --- | --- | --- |
| "Copied startup files never prove source-library role." | AGENTS.md:5 | line 8 | wording exact, anchor off by 3 |
| "Before designing, reviewing, or fixing anything, find the matching skill there and follow its SKILL.md." | AGENTS.md:13 | line 13 | exact |
| "Skills whose description begins 'MANUAL-ONLY' must never be auto-applied" | AGENTS.md:14 | line 14 | exact |
| "Teach build choices before requesting a decision." | AGENTS.md:15 | line 15 | exact |
| "Audit your own state; assume nothing about your own work." | AGENTS.md:46 | line 46 | exact |
| "Report the gap, never fill it." | AGENTS.md:46 | line 59 | wording exact, anchor off by 13 |
| "the human remains the merge gate" | AGENTS.md:117 | line 122 | exact, anchor off by 5 |
| "For work that produces no PR, include the same record in the final report" | AGENTS.md:223 | line 223 | exact |
| "@AGENTS.md" | CLAUDE.md:1 | line 1 | exact |
| "Verify location and role before task writes or skill selection." | SKILL.md:42 | line 45 | exact, anchor off by 3 |
| "SDP-1 removes the wait, not the proof." | SDP-1.md:31 | lines 62–63 (sentence wraps) | exact, anchor off by 31 |
| "This record authorizes nothing." | B.md:182 | line 185 | exact, anchor off by 3 |

**Result: 13 quoted passages checked; 13 exist verbatim in the cited file; 7 cite the exact line; 6 cite a nearby line (offset +3 to +31). No fabricated quotation and no invented rule was found.** The imprecision is in the line anchors, not the content — that is the failure mode that matters, and it is recorded rather than smoothed over.

The readback also did the part that is not quotation: it classified the workspace as **Role B, the consumer product**, on the evidence AGENTS.md requires (README starts `# Checklist`; `docs/skills-catalog.md`, `scripts/validate-skills.py` and the audit baseline are absent), and refused to restart product discovery merely because `docs/project-state.md` is missing — calling that "a discoverability gap, not proof that development has never started."

---

## 7. Why the vendor claim holds

| Session | Agent | Model | Vendor | cwd |
| --- | --- | --- | --- | --- |
| `c00a03db-5ac6-4cb5-b74e-eb5e393ed7f8` | `claude -p` (Claude Code) | `claude-sonnet-5-5` | Anthropic | `C:\src\_aep3_cp05_consumer` |
| `6ff5bc92-9754-494b-a8e2-8449246cfd07` | `claude -p` | `claude-sonnet-5-5` | Anthropic | `C:\src\_aep3_cp05_consumer` |
| `4d77dc2d-a1aa-484d-b7b8-7dfbd3df77ac` | `claude -p` | `claude-sonnet-5-5` | Anthropic | `C:\src\_aep3_cp18_closure_consumer` |
| **`01a187dc-7a82-79b1-8680-d72b53899da9`** | **`codex exec`** | **`gpt-6-astra`** | **OpenAI** | `C:\src\_aep3_cp01_consumer` |

Extracted from the retained transcripts themselves (`evidence/prior-consumer-sessions.json`), not from a summary. The new session differs in CLI, model and vendor from all three.

---

## 8. Residuals and limits — stated, not buried

1. **Sequencing.** The frozen sentence says "before investing in the build". That ordering cannot be demonstrated retroactively: releases A and B already exist. What is observed is that the mechanism works on this host and repository. The owner's CP-01 authorization defines this run as the closing observation; if the owner wants the strict temporal reading, the row reverts to UNRUN and the reason is this clause alone.
2. **Independence is contextual.** The two review contexts in §1(2) are non-authors within one programme; the audit says so itself ("contextual independence within one harness, not organisational separation"). The adjudicator of this record is a separate session from the observed session but the same programme.
3. **The next authorized step was chosen by the session, not by me.** It chose a read-only integrity check and executed it, which the prompt permitted. That is not CP-18: no durable next-action record exists in the clone, so the derivation CP-18 asks for was not attempted and is not claimed.
4. **Host configuration needed a workaround.** The PATH CLI cannot use the configured model (§4.1). The session used the newer bundled binary. A host whose only CLI is 0.149.1 cannot start this session at all — a real host-capability limit, recorded as one.
5. **One shell tool was missing.** `rg` is not installed for the session shell; it fell back to PowerShell. That affects how it searched, not what it found.
6. **Out-of-clone read.** Its own memory file, 0 matches (§5). Disclosed because "cold start" should mean no prior knowledge, and the check is now evidence rather than assertion.

---

## 9. UNRUN register (this task deliberately did nothing else)

| Item | Status | Why |
| --- | --- | --- |
| CP-18 (new-agent recovery) | **UNRUN** | no durable next-action record exists in the clone; the session said so itself. This record does not convert CP-01 evidence into CP-18 evidence |
| Any write, commit, push, PR, merge | **UNRUN** | not granted; the tree is clean and the provider was not touched |
| Workflow dispatch, deploy, settings change | **UNRUN** | outside the CP-01 grant |
| Re-running the session on `main` or a later branch | **UNRUN** | `main` carries no instructions (`README.md`, `docs/`, `site/`, `.github/` only), so discovery/readback could not be shown there; the installed profile lives on `aep3-i2/startup-readback`, the same state the prior consumer sessions used |
| Organisational independence of reviewers | **UNRUN** | not achievable inside one programme |
| Upgrading the PATH Codex CLI | **UNRUN, deliberately** | a host mutation outside this task; the bundled binary was used instead |

---

## 10. Evidence

| File | Content |
| --- | --- |
| `evidence/prompt.txt` | the exact 863-byte prompt |
| `evidence/session.jsonl` | raw JSONL event stream, 259,611 bytes, SHA-256 `3cdcbac33b0306e0518588555b8aecd92d0f9fadf9c3d103ab2839a771ee5d2c` |
| `evidence/session.stderr.txt` | stderr, including the MCP auth error |
| `evidence/process.json` | start/end/elapsed/exit/binary/sandbox |
| `evidence/last-message.md` | the session final answer, 6,516 bytes (rendered into the transcript; not treated as evidence by itself) |
| `evidence/READ-LEDGER.json` | 9 commands, 15 files read with SHA-256, 0 writes, 2 out-of-clone reads |
| `evidence/host-profile.json` | OS/shell/node/git/CLI versions, provider account, DSH profile |
| `evidence/clone-identity.json` | HEAD, tree, file counts, key-file hashes, answer-key scan |
| `evidence/prior-consumer-sessions.json` | the three prior sessions, model and vendor, extracted from their transcripts |
| `evidence/denied-provider-attempts.json` | the four rejected provider calls, exact error text |
| `evidence/quote-verification.json` | the 13 passage checks behind §6 |
| `SESSION-TRANSCRIPT.md` | the full ordered transcript, generated from `session.jsonl` |

---

## 11. Elapsed and model line

- Task start 2026-10-29T06:22:18-07:00; session window 06:32:15–06:37:10 PDT (4 min 56 s); record written by ~06:42 PDT (about 19 minutes end to end).
- Observed session model: OpenAI `gpt-6-astra` via Codex CLI 0.163.0-alpha.10.2.
- Model: DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not observable.
