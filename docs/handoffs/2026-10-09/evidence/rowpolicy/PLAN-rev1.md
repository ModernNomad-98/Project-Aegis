# ROWPOLICY-1 — Stage A PLAN, revision 1

**SD-A: COMPLETE — ready for independent Stage B on the captured file hash.** This is a plan, not a plan-audit verdict or permission to skip later stages.

Item: clarify exact publication of another stage agent's self-authored skills row in Project Aegis PR metadata.
Holder: `/root/cifix_plan`, Stage A only, Astra xhigh as assigned.
Actual start: `2026-10-08 19:43:23 UTC`, obtained from the clock tool. Initial estimate: **25–40 active minutes**, unverified. Active time is not separately measured; finish, wall time and SHA-256 will accompany the completed artifact.
Only write: `C:\src\Codex Projects\Project Aegis\rowpolicy\PLAN-rev1.md`.
Source clone, read-only: `C:\src\Project Aegis\Project-Aegis`.
Observed `origin/main`: `5228977920ee479e1fe1ec6b8d56f8fc24c14947` (M).

## 1. Owner choice, problem and intended result

Current direct owner choice, quoted verbatim as relayed by the coordinator in the ROWPOLICY-1 assignment of 2026-10-08:

> Allow exact sourced copying (recommended)

The question it answered, also quoted verbatim as relayed:

> For future Project Aegis PRs, should the workflow explicitly allow an authorized PR editor to copy another stage agent’s exact, self-authored four-column skills row? The editor would preserve the agent, stage round, source revision or digest, and any UNRUN limits; the final reviewer would compare every row with its source before hashing the completed table.

No additional option-description text or precise owner-answer timestamp was provided to this planner; do not invent either. The actual question and selected label above are sufficient proposal/selection context. This is a transcription from the current conversation through the coordinating agent, not an independently signed repository statement. The approval-register preamble recognizes current direct owner instructions before transcription.

At M, `docs/delivery-workflow.md:479` says:

> **Each agent reports its own usage.** No agent writes another stage's row.

The new owner choice distinguishes **authorship** (the stage agent determines and writes its own usage account) from **publication** (an already authorized editor copies that existing account exactly into the PR description). The literal old wording does not express this distinction. The chosen correction preserves stage independence while allowing a finite copying operation backed by a retrievable, fixed source.

The coordinator reports independent reviews of PRs #678–#680 showing stale-round and condensed-row risks and a previously unresolved literal-rule gap. Those reports motivate explicit cases below. This planner has not independently fetched those PRs in this item. Prior merged practices are historical evidence and **not authority** for the new policy. The current owner selection is its authority.

**Done state:** the canonical workflow unambiguously permits exact sourced publication by an editor who already has authority, forbids authoring or paraphrasing another agent's usage, preserves current round/revision and UNRUN evidence, and makes the row source checks fit the existing F hash/G receipt sequence. The template points to that one protocol. New append-only records preserve the selected question/answer and rationale without rewriting APR-105 or D72.

## 2. Scope, classification and evidence

### Exact intended paths

| Path | Change and reason |
| --- | --- |
| `docs/delivery-workflow.md` | Canonical row authorship/publication protocol; a narrow addition to the Stage handoff block; SD-F's table clause points to source verification; source-protocol ownership accounted for in the agreement check. Preserve the existing hash/invalidation procedure and other stage/gate conditions. |
| `.github/pull_request_template.md` | Replace ambiguous self-reporting sentence with a concise pointer to the canonical protocol; make the existing four-column example identify round; include an optional placeholder for source records within the existing skills sentinel pair. No duplicated rule list or new sentinel. |
| `docs/approvals/APPROVAL_REGISTER.md` | Append one POLICY DECISION recording the full owner question/selection and forward clarification; no old entry edits and no new execution/publication/merge grant. |
| `docs/reconciliation/step-0-reconciliation-v4.md` | Append a new dated D-entry at the end of §5, immediately before §6, describing the clarification and linking the policy record/canonical section. Preserve every existing byte outside the insertion. |

Four files, one policy intent, one seven-stage PR. No skill is added or edited. No change to `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, README, scripts, CI workflow, hash implementation, settings, protected paths, APIs, authority controls or reserved evaluation/VM/Stage4B/calibration/provider work. Do not emit the automated reviewer's trigger phrase. Keep the dirty clone and unmerged handoff branch untouched. Later implementation uses an isolated clone/worktree with one writer and exact-file staging.

`AGENTS.md` already points to the canonical workflow and preserves separation; it does not repeat the row-copying restriction. `CLAUDE.md` imports it. `CONTRIBUTING.md` rule9 links to the workflow. Thus none needs wording changes for this clarification; they are read in the preservation check. If an actual contradictory current statement is found later, flag the exact conflict and return to Stage A rather than adding a fifth path silently.

**CHANGE CLASSIFICATION**

- Deliverables: a documented instruction/procedure clarification, matching PR template guidance, and two historical decision records.
- Classes: **ai-agentic** governance instruction change for workflow/template; documentary POLICY DECISION and D-entry for records. Calling the whole change docs-only would understate its effect on agents.
- Governing route: existing direct owner selection for the narrow behavior; `human-approval-boundary` for any action exceeding it. Existing delivery grants govern separately authorized commits/pushes/merges; this plan does not assume its policy entry authorizes its own merge.
- Validation: independent scope/condition review, exact-source behavioral cases, link/Markdown sanity, repository validator and validator self-tests, ordinary exact-head CI, source-record readback and final bound-field verification. No new code or permanent tests are needed to document the procedure.
- Scope lock: only the four paths above; any new tool, automation, source-storage subsystem, fourth bound field, fifth table column, or enforcement-code change returns to Stage A.

### Observations actually made in this Stage A turn

`git rev-parse origin/main` returned M. Read current `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, workflow stage/skills/binding/agreement sections, template, approval preamble/APR-105/references, and D72 plus the current decision tail. The four source-library landmarks were already observed in this same task session at M; current ref identity is rechecked. The remote is the Project Aegis source repository, not a consumer copy.

| Blob at M | SHA-256 / relevant count |
| --- | --- |
| `docs/delivery-workflow.md` | `b509269a374c4570fbbb4f61f72b6dd1d6ebbe8d6a57ba30fc1d93b3e81f247a`; 894 newline bytes |
| `.github/pull_request_template.md` | `cfc26e12e0b950dc57a7337f2a206355ce0afbe49b9328292bfe935a3fc61346`; 126 newline bytes |
| `docs/approvals/APPROVAL_REGISTER.md` | `1a35c8c84de597319952a75d7ee5545a74829f0f07a7c12287e1fe43f6368970`; 5154 newline bytes |
| `docs/reconciliation/step-0-reconciliation-v4.md` | `09bc7337c5329f5f7d3406da81aec1597e83be919bf5a1e81b99455eddbc24a4`; 3985 newline bytes |
| `AGENTS.md` | `bcea3f367b80c6ef9d8ffc61aeb52a9868c907b94ce24c8989f697ea4931bcb1` |
| `CLAUDE.md` | `2dbec5694d010f2c57637b6f1d9ddc53d11710f8271f0f8dda7afee305d26722` |
| `CONTRIBUTING.md` | `2f52e51bb93fbaf0648409ba79368643ad8304621e1bc4aae1eb50cae4f650af` |

Hash method: Python `hashlib.sha256(subprocess.check_output(['git','show',M+':'+path]))`; line counts are `raw.count(b'\n')`, never nonblank-line counts. Register regex `^### AEGIS-APR-(\d+):` returned 119 headings, max119, zero duplicates. Decision regex `^- \*\*D(\d+)\b` returned 72 entry headers, max73, zero duplicates. The count is not an assertion that every integer exists.

Current `gate_pattern` extracted from `.github/workflows/validate-skills.yml` matched **none** of the four paths. In particular, `.github/pull_request_template.md` is not a protected-workflow path; current offline test fixtures list it among ordinary paths. No one-time failed-guard exception is justified for this scope. Nevertheless the template and approval register are security-relevant under CONTRIBUTING; the PR answers Yes, with those surfaces named. MG5's outside-contribution scope remains unchanged.

`git grep` found the literal prohibition only in the canonical workflow among current tracked files. Targeted searches for skills-row/bound-field/SD-F strings in `scripts/validate-skills.py` and `scripts/tests/test_validator.py` found no hits. That supports leaving scripts alone, not claiming no indirect validation can ever apply. Source `git status --porcelain` showed pre-existing untracked `artifacts/recovery/` and `artifacts/reviews/`, plus inaccessible user-ignore warnings; no source writes were made.

Current live GitHub state is not newly fetched by this planning item. M is locally observed and the coordinator has current-turn recovery evidence from the wider task; later author/merger must refresh rather than treat this snapshot as permanently current. Candidate head/PR/checks and ID allocation are future facts.

## 3. Reconciliation and rule-preservation inventory

| Claim/conflict | Kind and controlling evidence | Planned result |
| --- | --- | --- |
| “No agent writes another stage's row” versus authorized exact copying | SHOULD. Current owner choice outranks the older literal wording; source-of-truth rule and register preamble. | Replace “writes” ambiguity with authorship boundary plus bounded exact publication. |
| Historical condensed or stale rows versus chosen exact/current source | IS history versus SHOULD choice. Coordinator review reports are historical and not authorizing. | No grandfathering or retroactive ratification; current operative round/source must be checked. |
| Permission to publish a row versus permission to hold a stage/edit the PR | Different scopes. Owner question says **authorized PR editor**; existing stage/holder/authority rules remain. | Copying transfers no stage credit, PR ownership, tool permission or merge authority. |
| F must be represented before hashing, yet F verdict names the hash | Procedure ordering. F can self-author its usage after its checks and before its verdict. | F source row → serialized publication/readback → completed payload hash → F verdict outside fields. |
| G wants to add its row after F | Existing bound-field invalidation and receipt rule. | G records its own usage in its receipt; any later bound-field edit requires fresh F under the unchanged rule. |
| Source binding could be outside the hash | Owner requires source comparison before table hash; existing skills payload has room for provenance. | Source records sit inside the skills sentinel pair; hash method/three-field set unchanged. |

Preserve these invariants explicitly in the implementing agent's inventory:

1. Seven stage names, order, distinct holders, predecessor dispositions and no two holders of one PR.
2. Plan captured-revision binding; head/tree/base binding; moved-head invalidation.
3. MG1–MG5 text and all conditions, including exact-head checks, owner exceptions, automated-review triage, authority, and outside-only additional security review.
4. SD-A–E and SD-G text/statuses; SD-F ACCEPT/REVISE tokens, security answer, eight-site witness, exact head and existing bound-field hash. The only intended SD-F addition is explicit source verification of the row evidence.
5. UNRUN is not PASS; original agent, round, target revision, procedure/result and limits remain attributable.
6. Exactly four table columns and the existing three bound fields, sentinel strings, whitespace-normalized bound hash, first16 digest format and invalidation rule.
7. A stage agent may author only its own usage; actual skill reading/application is still mandatory; no-match is reported honestly.
8. Existing approval/decision bytes remain historical; no new grant is manufactured from a policy choice.
9. Metadata updates do not move candidate H; source artifacts live in existing handoffs/comments, not a new document created merely to list skills.
10. These are procedural checks. No CI prevention, atomic multiwriter guarantee, signature authentication or tamper-proof storage is claimed.

**Single-source placement:** the skills chapter owns the new row content/provenance protocol. SD-F's existing table clause links to it for the verification method; the Stage handoff owning block links to it for the self-authored row artifact. Other stage cells remain pointers. The existing agreement check must account explicitly for the new content/provenance owning block without adding another rendering of MG/SD conditions. It may name that block among the permitted owning blocks, with scope limited to row authorship/publication evidence. Do not scatter new “F may ACCEPT only if…” conditions into examples, template, receipts or stage table. The declaration of SD-F's condition remains in its normative row.

**Self-scrutiny:** a small wording clarification can accidentally widen editing roles or turn prose into a parallel gate definition. The narrow owner question, unchanged-stage inventory and single-source comparison are the counterweights. A proposed new role, permission, hash algorithm, permanent source store or condition repeated in multiple homes would change this plan and require re-audit.

## 4. Canonical protocol to write

Add a compact subsection under “Skills: mandatory use and per-PR reporting,” proposed anchor `#authoring-and-publishing-skills-rows`. Preserve the four-column table and existing actual-use/no-match/no-extra-document rules. Replace only the ambiguous authorship bullet and the minimum neighboring text needed for this protocol.

### 4.1 Author versus publisher

- The **stage agent authors** its complete four-column Markdown row or rows, reflecting only its own work. It identifies its agent identity, stage and round, actual procedure, result/evidence and every applicable UNRUN limitation. It supplies that text in its normal handoff or posted stage record, with the reviewed target: plan revision/digest for A/B, exact candidate head for head-bound stages, and any narrower evidence revision where relevant.
- An **already authorized PR editor publishes** that exact existing row. The editor may extract/copy it and add factual source-record metadata; it does not compose, summarize, merge, reword, translate or “improve” another agent's account, change its skill list, fill a missing result, or convert unavailable evidence to a pass. Invalid Markdown, missing fields or needed corrections return to the originating stage agent for a new self-authored source revision.
- Copying is a metadata operation, not performance of the copied stage. It conveys no author/reviewer credit, independent verdict, PR-holder role, commit/push/merge permission, extra tool access or exemption for a coordinator. Existing task authority and the current PR holder determine who may edit; this policy does not appoint editors.

### 4.2 Fixed source and round applicability

Use a retrievable source captured at a fixed revision: either an immutable artifact/commit revision with a locator, or a retained exact source capture with a content digest and locator. A mutable URL or comment ID by itself does not pin its contents. The source record must bind the self-authored row together with its author/stage/round and target revision; a digest of an unrelated file or an unretained string is not evidence. A captured digest is not a human signature.

Exact copying is checked on decoded Markdown text, not on a screenshot or rendered appearance. Compare the complete row string excluding its transport line terminator; UTF-8 character content, whitespace inside the row, escapes, links, backticks and all four cells stay unchanged. JSON escaping is decoded once as transport; no Unicode or whitespace normalization is used to excuse a different source row. The final bound-field hash's existing whitespace normalization is a separate procedure and never proves exact copying.

Each published row has a compact **source record inside the existing skills bound-field payload**, immediately after the four-column table. This is factual provenance, not a fifth table column or new bound field. Identify the row unambiguously (agent + stage + round + source row ordinal/locator), target plan digest or head, source locator, fixed source revision or capture digest, and retained limitations. The editor copies these facts from the author's source; it cannot invent a round or target. The source record may reference a group of rows only when every member and ordinal is explicit and all share the same captured source. The source digest covers the retained author record; it excludes a later publisher-added provenance block, avoiding self-reference.

An illustrative shape, to be documented as a format example rather than made into a new machine schema:

```text
Row source: agent=<author>; stage=<stage>; round=<round>; row=<source locator/ordinal>;
target=<plan digest or candidate head>; source=<retrievable locator>;
binding=<immutable source revision OR digest of retained exact author record>.
```

Do not require a repository file solely for this map; existing stage handoffs/comments and the PR's skills payload suffice. A source lost, inaccessible or changed so the bound capture cannot be recovered is unavailable evidence, not a license to reconstruct it. Corrections are new author records with a new binding; do not silently overwrite a cited source and preserve its old identifier as if unchanged.

An older row whose stage name matches is not automatically current. Match **author + stage + round + target revision** to the operative stage record. After implementation rework, an old D/E/F row does not cover H2. A/B rows can remain applicable when their captured plan and audit revision still bind; do not invent a new A/B run merely because H changes. If older rows are retained in the description, their source records distinguish them as historical/superseded and they cannot substitute for the current operative round. Stage history remains in the original records even if the current table replaces superseded rows.

**Self-scrutiny:** this source map adds metadata and exact text can be awkward to quote. It is kept within the existing payload and requires only evidence that the author already supplies; the alternative of rewriting the row would violate the selected choice. If four-column rendering or source recovery proves impractical, return the exact problem to Stage A rather than loosen “exact” to “same meaning.”

### 4.3 Serialized publication and readback

The current PR holder coordinates **one metadata writer at a time**. Source authors submit their records; they do not all race to update the description. Copying for a stage is not a second holder of its PR. If the holder delegates a finite authorized publication action, it serializes that action with its own edits and preserves stage ownership.

The publisher reads the latest raw PR description, checks that it is the expected revision, edits only the intended skills payload/source records, and uses a structured body argument or a UTF-8 body file containing real newlines. Do not build JSON-escaped newline strings into shell text. Immediately read back the server's decoded raw body and compare every inserted row with its captured source, verify all other sections are preserved, and verify exactly the existing sentinel pairs still delimit the intended payloads. A visible successful tool call or rendered table alone is not readback evidence. Record body revision/time/digest before and after in the existing stage handoff.

If another edit occurred between read and write, or readback loses a row, source record, marker or unrelated content, stop publication and reconcile from the latest body/source records. Do not overwrite an unexpected body using an old full-body copy. This is a procedural serialization rule, not an atomic API guarantee. No new automation, lock service or permanent tool is introduced.

### 4.4 Final reviewer row and completed table

Update SD-F's existing skills-table clause to require verification of each applicable row against its captured self-authored source, with a pointer to this procedure. Do not create a second condition definition elsewhere.

F's sequence is: finish the source/work comparisons it will report; self-author its own usage row and capture it in its existing stage record; arrange authorized publication of that row plus all current sources; read back the completed skills payload and compare it with all source captures, including its own row; then compute the canonical three-field hash over the current body and post its independent verdict naming H/hash. Its own row reports work actually done and any limits; it need not claim a verdict not yet posted. The final verdict itself is outside the bound fields. No row must contain the final body hash or its own source digest, avoiding a circular hash requirement.

The current table's F row is a report of F's own skill use, not F auditing its own implementation; all implementation/planning stage independence remains. Any missing or stale source is handled through the existing SD-F disposition and exact-head rules. Publication by an editor does not qualify the editor to supply F's content.

The existing post-F invalidation procedure remains unchanged: an edit to the skills payload **including its source map**, or another bound field, voids the prior verdict. The rule still applies when a whitespace-only edit happens to preserve the normalized digest; equal hashes do not authorize knowingly reusing a verdict after a bound-field edit. An unchanged head is not an exemption. F then reviews the current body and records a fresh verdict as the canonical workflow requires.

G records its own skill usage in the merge receipt. It does not append its row into the accepted skills payload and reuse the old F verdict. If a premerge bound-field update is actually required, route through fresh F before G; after merging, record G and later corrections in receipts without implying the old accepted body was the revised one.

**Self-scrutiny:** F self-row insertion could otherwise create a repeated hash/edit loop. Keeping the verdict/hash outside the row and finishing source publication before hashing gives a finite sequence. If F's source later changes or a table edit becomes necessary, a new F round is the existing consequence, not an exception to hide in formatting.

## 5. Decision records and authorization boundaries

### Approval register append

Append a new **POLICY DECISION**, not a GRANT and not a blanket supersession of APR-105. Name it “Exact sourced publication of stage skills rows” or equivalent factual title. Include:

- Status at recording, actual recording date/by, owner/date as known; no invented timestamp.
- The full question and chosen label in §1 on one physical line each, identified as selection/proposal wording relayed through the coordinator. Do not invent an option description.
- Reason: resolve “writes” versus “authors/publishes” while preserving accountability and source-checking.
- Selected policy: concise link to the canonical row protocol; author-owned exact four-column rows, fixed source, round/revision/UNRUN fidelity, final source comparison before hash. Label any detailed implementation mechanics as this reviewed procedure, not as verbatim owner prose.
- No additional permissions: the choice does not authorize another stage's authorship, new PR edits without task authority, extra stage ownership, history rewrite, relaxed checks, merges, settings, skills, or reserved work. It narrows only the old literal prohibition sufficiently to permit the chosen exact publication.
- Relation: APR-105 remains the seven-stage policy; this later choice clarifies the reporting part. Preserve its original bytes. Do not create SUPERSEDED/CONSUMED events for APR-105 or claim an old policy grant was consumed.
- Evidence: current direct owner question/selection as relayed, this captured plan and later stage evidence if available; specify which sources are transcription versus repository review. The new policy entry does not authorize the PR recording it to merge.
- No one-use/calendar limit was stated for “future Project Aegis PRs”; do not invent one. Apply until the owner later changes the policy.

### D-entry

Add a new D-entry at §5's end, before `## 6. Post-merge corrections`. It records date, why, chosen narrow policy, consequence/limits, canonical link and new approval record, no new authority, and procedural enforcement limitation. Quote or point to the full owner-choice context without restating every normative step. Preserve D72 and all other historical text. No new “post-merge correction” is appropriate before this PR merges.

### ID allocation and current delivery authority

At M, APR max119 and D max73 make APR120/D74 **candidates only**. CIFIX and the skill-batch planning lane can collide with both. Coordinator allocates after inspecting current main and all other open PRs touching either record; before this PR opens use self PR number0, afterward exclude its actual number in enumeration. Resolve every relevant head, read its entry definitions and take the next free ID. Recheck at merge. Missing PR/head evidence is not an empty set. Any collision or intervening policy change returns to the coordinator for rebase/reallocation and renewed head-bound D/E/F evidence.

This Stage A is authorized only to plan. Later C/G receive their own bounded brief and check current owner work scope and register history. The current selection supplies the policy choice before transcription; it grants no new provider/PR-edit credentials or permission to skip normal delivery gates. Standing APR-100/048/050 and applicable current task instructions govern delivery mechanics, not retroactive validation of old copies. No guard exception is expected: if gate-guard fails, inspect actual paths and stop for scope reconciliation instead of citing CIFIX's separate one-time grant.

**Self-scrutiny:** two records can become competing policy copies. The register keeps the owner choice; the D-entry keeps decision rationale; both link the canonical procedure. Neither should reproduce all operational steps. A claim of new authority or a reused ID is a defect, not a reason to rewrite historical entries.

## 6. Acceptance criteria and evidence plan

Let B be the current-main implementation base, H its immutable candidate, and R the actual PR number. Recipes below run only later in the clean isolated implementation/validation environment. Stage A has not run repository validation or behavioral cases.

**AC1 — Exact scope and truthful classification.** `git diff --name-only "$B...$H"` contains exactly the four §2 paths; `git diff --check "$B...$H"` exits0. No hidden code/config/tool changes. PR security answer Yes names `.github/` template and owner approval register; outside-contribution applicability is determined from actual provenance without widening MG5. Final reviewers check the ai-agentic classification and scope against the diff.

**AC2 — Rule and condition preservation.** C supplies the §3 inventory with per-item diff evidence; D resolves each preserved/changed item explicitly. Compare the MG block, SD-A–E/G rows, stage names/exit-ID column, dependency table, hash/sentinel algorithm, invalidation text and receipt rule against B. They remain byte-identical except the explicitly targeted SD-F pointer/table-verification clause and the Stage handoff row-source artifact addition. The agreement check gains only the minimum ownership/pointer accounting for the new row-content protocol. Re-read `AGENTS.md`, `CLAUDE.md`, CONTRIBUTING and D72/APR-105; unchanged files/old records are proven by diff/byte checks. No extra stage, execution authority, changed status token or fourth bound field.

**AC3 — Exact source, current round and limits.** Independent D applies the case table below to the actual new prose and a synthetic raw PR body with retained source records. Record source payloads, source binding, published payload and result per case. Expected treatment must be explicit in the text, not supplied only by reviewer intuition. No real PR edit is required for these cases.

| Case | Expected result |
| --- | --- |
| Another authorized editor copies an exact self-authored four-cell row, retaining author/round/target/source/UNRUN | Permitted publication; original agent remains author. |
| Editor condenses two rows, paraphrases a result, rewrites links/escaping, or invents a no-match row | Reject as exact copying; originating agent supplies corrected source. |
| Correct-looking D stage label from round1/H1 offered for operative round2/H2 | Does not satisfy current evidence; obtain round2/H2 source. |
| A/B row still bound to the same accepted plan digest after candidate H changes | May remain applicable; no fabricated rerun or automatic head binding. |
| Author or reviewed target is altered, or UNRUN limitation disappears | Reject mismatch; no green inference. |
| Source URL exists but mutable content changed and retained capture/digest cannot be verified | Unavailable evidence; no reconstruction from memory or rendered body. |
| Genuine immutable source revision resolves and raw row matches, or retained source capture matches its recorded digest | Source binding valid; still compare claimed work/limits and target applicability. |
| An unauthorized editor has an exact source | Copying policy confers no edit authority. |
| Two writers would publish full-body edits from the same old body | Serialize; unexpected intervening revision/readback loss halts and reconciles. |
| Literal JSON escape sequences are accidentally published instead of the intended Markdown/newlines | Readback comparison catches transport corruption; do not treat rendered/HTTP success as fidelity. Legitimate literal escape text already present in source is preserved. |
| F authors/captures its row before hash, body readback matches, verdict follows outside markers | Finite valid order; no self-referential row/hash requirement. |
| G appends its row to a bound field after F and wants to reuse F | Prior F invalidated; G's normal usage goes in receipt; required body update needs renewed F. |
| Whitespace-only bound-field change has equal normalized hash | Known edit still invalidates F under existing text; normalized hash equality is not exact-source proof. |

**AC4 — Records are additive and owner-faithful.** Register B blob is a strict byte prefix of H blob; numstat shows no register deletions and one EOF addition. For D record, identify the exact B byte prefix before `## 6. Post-merge corrections` and suffix from that heading; H is that same prefix + the new D-entry + the identical suffix. Count current definitions with the §2 regexes; unique allocated IDs checked against main and other in-flight PRs. The complete owner question and selected label from §1 each appear exactly as a one-line source string in the new register entry. No fabricated option prose, timestamp, supersession, approval grant or change to old bytes.

**AC5 — Four-column table, source binding and serialization.** The template retains exactly its six existing whole-line sentinel strings in order; no new sentinel or fifth column. Its source-record placeholder is inside the existing skills payload, and its guidance links the canonical subsection rather than duplicates the protocol. In synthetic body checks, parse by whole-line equality, use real newline serialization, compare raw rows with retained source strings, and recompute the existing witness→skills→security normalized SHA-256 first16. Changing a source record within the skills payload changes the input to that hash; absent/ambiguous marker pairs are reported as errors. This proves only fixture processing, not prevention of live concurrent edits.

**AC6 — Current repository/document checks.** In the real clean clone at H, run and retain commands/exit/summary:

```text
python -B -P scripts/validate-skills.py
python -B -P scripts/tests/test_validator.py
python -B -P scripts/ci/check-markdown-links.py docs/delivery-workflow.md .github/pull_request_template.md docs/approvals/APPROVAL_REGISTER.md docs/reconciliation/step-0-reconciliation-v4.md
git diff --check B...H
```

All must exit0; link report broken0/dead0. Markdown table/links/quotes are visually or structurally read back, not inferred from a file's existence. Any unavailable local dependency is UNRUN with the actual resolving command/environment, not a pass. No new tests mirroring the prose, no scripts edits and no reserved execution are included.

**AC7 — Agreement check, eight-site witness and divergence record.** Run `git grep -n -E 'MG[1-5]|SD-[A-G]' H -- docs/delivery-workflow.md`; inspect each changed/new hit under the canonical ownership procedure. New row rules live in their one designated block; stage-condition statements remain in the owning blocks. PR witness has exactly eight rows, statuses and evidence as §7. Because SD-F's condition is clarified, regenerate the current AGENTS marker/divergence table even though AGENTS itself remains unchanged; do not mark it not-applicable automatically. An independent reviewer verifies this accounting against changed text.

**AC8 — Published and merge-time evidence.** Ordinary CI at exact H is observed from all check runs and legacy statuses: current source predicts changes/validate-skills/gate-guard success and advisory path skips. Record actual skips as skipped, unexpected failures as failures. Later F verifies all actual A–F row sources and applicability, including its pre-hash self-row, posts H/current bound hash outside fields and accepts E's UNRUN list under the canonical rule. G rederives MG1–MG5, body/hash/source availability, IDs and active delivery authority in the same turn, then merges only if those gates actually hold and its brief authorizes it. Its usage is recorded in its receipt. No live PR exists yet for this item; these are future gate obligations.

**Declared not verifiable at this Stage A head:** AC8's future PR/CI/F/G evidence and actual live metadata serialization are not available before publication; the synthetic AC3/AC5 checks do not claim those facts. D can mark only those future portions UNRUN with this declared reason; E/F/G resolve them at the applicable stage. Core local checks and prose/record criteria are not automatically excused as UNRUN. If new unavailable criteria arise, follow SD-D's REVISE rule rather than silently expanding this list.

## 7. Eight-site witness and stage handoffs

This is the intended witness disposition to verify at H, not a claim that the change has been implemented:

| # | Site | Intended status | Evidence later required |
| --- | --- | --- | --- |
| 1 | MG block | unchanged-and-verified | B/H block comparison; all MG1–MG5 text unchanged. |
| 2 | SD block | changed | Diff shows only the SD-F skills-source clarification; all other rows/statuses preserved. |
| 3 | Dependency block | unchanged-and-verified | B/H table byte comparison; no new backward edge. |
| 4 | Handoff block | changed | Narrow source-row artifact pointer; existing decision/file/evidence/deviation/continuation duties preserved. |
| 5 | Pointer-shaped sites | changed | Both MG/SD grep sweeps plus updated ownership list; no duplicated conditions. |
| 6 | AGENTS summary | unchanged-and-verified | `git diff --quiet B...H -- AGENTS.md` exit0 plus human reread against clarified SD-F; marker/divergence evidence. |
| 7 | PR body | changed | Actual body uses current template, exact self-authored rows/source records and source-bound completed hash. No new rule text outside permitted witness/skills/divergence content. |
| 8 | Stage table exit column | unchanged-and-verified | Seven bare SD-ID cells unchanged. |

The actual PR witness contains IDs/statuses/pointers and evidence, not the normative wording in this explanatory plan table.

- **A:** this captured plan, owner quote/context, classification, scope, acceptance criteria and unavailable-future portions. Current owner selection is controlling before register transcription. A ends here.
- **B:** a different agent audits exact plan bytes/hash, especially no permission widening, source-map placement, no circular F hash, record fidelity and canonical-condition ownership. ACCEPT/REVISE explicitly names captured revision. No implementer begins before ACCEPT.
- **C:** separate authorized implementer refreshes main, checks collisions, uses an isolated branch, edits only the four paths, produces condition inventory/record byte proofs/local checks, and immutable H/tree/B. It provides its own exact four-column row and source record. No mass staging or dirty-root edits.
- **D:** different agent examines actual diff and criteria individually MET/NOT MET/UNRUN; verifies the behavioral cases and owner/source distinctions. Its own row names round and head, and its verdict is independent.
- **E:** another holder runs checks at H, reports every UNRUN with resolution/CI coverage and correct prefixed SD-E disposition. It authors only its own row.
- **F:** independent reviewer verifies prior rows against source/work/round/target and performs §4.4's own-row-before-hash sequence. It records the completed-body hash and exact H, checks witness/security/skills and E limits. Its verdict grants no merge authority.
- **G:** separate authorized merger refreshes head/main/records/checks/automated review/authority and body hash; confirms no reused stale round or changed source. A new head or invalidated body returns to the proper stage. It records its own usage in receipt and observes post-merge main checks. It holds no earlier stage of this change.

Every stage carries the existing SD/MG decision IDs, changed/not-touched lists, actual invocation evidence, deviations and continuation. No coordinator performs the authored change or merges it. Finite delegated row publication does not erase those role limits.

## 8. Drift, unknowns and timing

Before implementation, fetch current main in the authorized isolated checkout and compare the four paths plus governing AGENTS/CLAUDE/CONTRIBUTING sources to M. If only independent record appends landed, stop for coordinator ID/base reconciliation; preserve those bytes and capture the updated plan if its text/conditions change. Any new conflicting policy/source edit returns to Stage A and independent B. No silent ID reassignment or policy reconciliation. At merge, changes to H void head-bound dispositions; any bound-field change invokes fresh F even without H movement.

Known unknowns: live current PR inventory/record reservations; future B/H/PR number; available validation environment; future CI/review/automated-review/merge results; live publication races. No new owner policy decision is presently missing for the narrow choice. If implementation proposes a permission grant, different storage system, code enforcement or wider source rewrite, it is outside this plan and requires a separate decision.

The initial 25–40 minute active estimate has no measured active-time basis for this new work. Historical governance planning is not a current runtime benchmark. Final wall time will be reported as an imperfect comparison; no unproven duration is used to justify skipping checks or broadening scope.

**Self-scrutiny:** exact-source checks improve attribution but cannot prove an agent truly performed its claimed work. F still checks the reported actions against evidence, as the existing rule requires. Mutable hosted comments can disappear, and serialized edits are not an atomic transaction. Retained fixed source captures and readback make gaps observable; they do not turn this into machine enforcement. Evidence of an undisclosed automatic publisher or unresolvable current-source conflict changes the design and must be surfaced before implementation.

## 9. Stage A skills and closeout

These rows are self-authored by this Stage A holder. The source is this exact plan revision; its captured digest is supplied outside the file after writing so it is not self-referential. The source target is ROWPOLICY-1 PLAN-rev1, not a future implementation H. No later stage's work is claimed.

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [change-classification-gate](https://github.com/ModernNomad-98/Project-Aegis/blob/5228977920ee479e1fe1ec6b8d56f8fc24c14947/.claude/skills/change-classification-gate/SKILL.md) | ROWPOLICY-1 Stage A, round 1 / `/root/cifix_plan` | Classified the canonical agent instructions and template as ai-agentic governance work, separated documentary records, and locked the four-file scope and validation route. | PLAN-rev1 §§2/6; current source hashes and path-pattern results recorded. Repository validation and future CI are UNRUN in Stage A; this row does not claim implementation verification. |
| [source-of-truth-reconciler](https://github.com/ModernNomad-98/Project-Aegis/blob/5228977920ee479e1fe1ec6b8d56f8fc24c14947/.claude/skills/source-of-truth-reconciler/SKILL.md) | ROWPOLICY-1 Stage A, round 1 / `/root/cifix_plan` | Enumerated old canonical wording versus the current owner selection, applied explicit-owner precedence, and separated historical practice from current authority. | PLAN-rev1 §§1/3; exact question/selection quoted as relayed; no historical merge treated as authorization. Live historical PR inspection is UNRUN for this item. |
| [phased-work-handoff-designer](https://github.com/ModernNomad-98/Project-Aegis/blob/5228977920ee479e1fe1ec6b8d56f8fc24c14947/.claude/skills/phased-work-handoff-designer/SKILL.md) | ROWPOLICY-1 Stage A, round 1 / `/root/cifix_plan` | Designed the carried author/round/target/source record and serialized readback protocol within the existing seven stages, including F self-row before hash and G receipt placement. | PLAN-rev1 §§4/7; existing SD/MG bindings and role separation preserved in the planned inventory. Synthetic publication cases and actual PR readback are UNRUN in Stage A. |
| [scoped-approval-register](https://github.com/ModernNomad-98/Project-Aegis/blob/5228977920ee479e1fe1ec6b8d56f8fc24c14947/.claude/skills/scoped-approval-register/SKILL.md) | ROWPOLICY-1 Stage A, round 1 / `/root/cifix_plan` | Planned immutable policy transcription with complete proposal/selection provenance, distinguished POLICY DECISION from a new grant, and specified collision checks/additive proofs. | PLAN-rev1 §5; current register max119/zero duplicate IDs observed. No register entry, ID reservation, permission change or source-repository write performed. |
| [human-approval-boundary](https://github.com/ModernNomad-98/Project-Aegis/blob/5228977920ee479e1fe1ec6b8d56f8fc24c14947/.claude/skills/human-approval-boundary/SKILL.md) | ROWPOLICY-1 Stage A, round 1 / `/root/cifix_plan` | Applied the boundary between the owner's narrow policy choice and authority to execute later stages or external actions; classified this task as scratch-only planning. | PLAN-rev1 §§1/5/7/8; no new permission is inferred from copying a row, an existing merge grant or prior PR practice. Later-stage execution and provider writes are UNRUN and outside this Stage A assignment. |

`human-approval-boundary` was read earlier at the same M and applied to the already scoped owner choice as recorded above; no uncovered risky action is performed here. `docs-as-code-architect` was read/considered but not applied: its scope is tooling/pipelines, which this change excludes. No installed skill owns a single-change Stage A plan; disposition remains procedural. No MANUAL-ONLY skill was invoked.

Changed files: this scratch plan only. Intentionally not done: source/template/register/decision edits, code/tests execution, independent audit, PR metadata writes, credentials/provider actions, commits/push/merge, reserved work and skill builds. Relevant memory-registry search returned no matching row-policy/D72 context and supplied no premise.

Final artifact-integrity readback verified the exact owner question and selected label each occur once and all five skill links use M. A bare-Git ref recheck failed with child exit128 for repository ownership (the containing Python command exited1). Repeating the read-only command with process-only `-c safe.directory=C:/src/Project Aegis/Project-Aegis` and `--no-optional-locks` succeeded: ref M, the same four source-blob hashes/counts shown above, and unchanged untracked source status. No global Git configuration was written. The ignore-file access warning remains. The previously audited CIFIX plan was read only to confirm its SHA-256 remains `97c09c154034b050e80e996a55fceb1c22439cc32f44d62c34ed3536fe3fb487`. These are file/ref integrity checks, not Stage B audit or repository validation.

Continuation: give this exact file and final SHA-256, M and the current owner question/selection to a different Stage B holder. This agent supplies no audit verdict and holds no subsequent ROWPOLICY stage. Capture later deviations rather than silently modifying an accepted plan.
