# Workspace-citation durability — Stage D independent implementation audit

**Item:** "Workspace-citation durability — Stage D: independent implementation audit" (shared task `task-11`).
**Agent:** `of1-stage-d` — in plain words, *the Stage D auditor, a different agent from the Stage A planner, the Stage B auditor and the Stage C implementer of this change*. **No subagents were used.**
**Audited head (40 characters):** `bd21095427f584eaf97fa3218b942d1c502594c8` — in plain words, *the one commit of pull request #766, which publishes the FU-3 evidence the frozen O-F1 note cites and states the citation-durability rule*.
**Pinned base:** `dbe2ee28559fef88950b2d8822cf72d3e595ba86` — in plain words, *the tip of `main` that pull request #766 targets, being the merge commit of pull request #765*.
**My own clone (not another stage's):** `_resume-2026-10-09/_wcd-d-clone`, cloned over HTTPS from `https://github.com/ModernNomad-98/Project-Aegis.git`, fetched and checked out detached at the audited head.

> **ERRATUM — 2026-10-13, authorship.** This record originally named its author as `wcd-stage-d`.
> The author is **`of1-stage-d`**: the header's agent line and the two `Row source` records in section 7
> were written from this lane's agent-name convention rather than from the agent that actually performed
> the audit. Corrected in place on the Lead's ruling of 2026-10-13; the correction changes this file's
> byte digest and footer seal, which is why the erratum is stated here rather than the file being
> silently rewritten. No finding, verdict, threshold, measured value or acceptance result is affected.

**Reading key — every label in this record, in plain English.**
- `O-F1` — *the earlier observation that a merged pull request's skills table had no row for some stages; it was discharged by pull request #765.*
- `FU-3` — *the Behavioral Eval Runner provider-usage reconciliation attempt whose record lane merged as pull request #764.*
- `SD-D` — *the Stage D independent implementation audit and its verdict; this record.*
- `AC1`–`AC11` — *the eleven acceptance criteria the revised Stage A plan defines for this change.*
- `gate_pattern` — *the regular expression in the skills-validation workflow that decides which changed paths are protected and force a manual merge.*
- `DCO` — *the Developer Certificate of Origin sign-off trailer every commit in the range must carry.*
- `bound fields` — *the three pull-request-body fields the process acts on: the reconciliation witness, the Aegis skills table and the security answer.*
- `Row source` — *the provenance line inside the skills field that binds a published skills row to the agent and revision that authored it.*
- `OWED` — *a citation this change deliberately does not correct, recorded with its file and line so a later change must carry it.*
- `docs-only` — *the change class for a diff that touches only Markdown under `docs/`.*

---

## 1. Verdict

**VERDICT: `SD-D: ACCEPT`** — in plain words, *the workflow's word for an implementation audit that passes: the change does what the plan says, only that, and the evidence re-derives independently*.

Every one of the Lead's six adversarial priorities and every one of the plan's eleven acceptance criteria **passes at the audited head**, each re-derived by my own commands against the committed git objects — never against the worktree copy and never from the Stage C report. I found **no defect** in the change.

Two items are recorded as **observations, not defects** (section 6): the four published copies necessarily still contain archive-path references *inside their frozen archival text* — a limit the accepted plan states explicitly as owed item O4 — and the pull request's skills table does not yet carry the Stage D/E/F rows, for which I author my own row in section 7.

**Skill applied (dogfooded, per the owner's source-library preference):** `code-reviewer` — in plain words, *the Aegis skill that reviews an actual obtained diff and reports severity-ranked findings anchored to file and line* (`.claude/skills/code-reviewer/SKILL.md`, sha256 CRLF-to-LF `6238b67b7b90fcbb26fcc45300562efa9e290a9d3870548e37bedaabbc76449a`, unchanged from the previous lane). I ran its five passes over the obtained diff (correctness, security, reliability, tests/migrations, maintainability) and used its output discipline — severity, anchor, failure scenario, remediation, an explicit "not reviewed" list. `reviewable-diff-discipline` was **not** applied: its description begins `MANUAL-ONLY` and no human named it.

I did **not** read the Stage C report (`SD-C.md`) before forming this verdict; every number below came from my own commands.

---

## 2. Method and verifier validation

**My clone.** Fresh HTTPS clone at `_wcd-d-clone`; `git rev-parse HEAD` and `git rev-parse origin/main` both returned the pinned base at clone time; `git status --porcelain` was empty. I fetched the head commit, checked it out detached, and re-verified `HEAD = bd21095427f584eaf97fa3218b942d1c502594c8` before measuring.

**The footer verifier was validated against known-good artifacts BEFORE it was pointed at anything**, as the brief requires — this session has already produced two false bad-seal accusations, and I did not add a third:

```text
placeholder verifier (64-hex on the "sha256:" line -> {{SHA256}}, UTF-8, final newline included):
  OF1-DISCHARGE-AUDIT-D.md    stated c2d106af9b990df9..  recomputed same  MATCH
  OF1-DISCHARGE-PLAN.md       stated 250cc3e8d3205870..  recomputed same  MATCH
  OF1-DISCHARGE-AUDIT-B.md    stated a17f1ecdbe37465f..  recomputed same  MATCH
verifier validated on 3/3 known-good artifacts: True
```

I also used a **second, different** convention where the artifact defines one — the body digest over every byte *above* a footer heading — and read which convention each artifact declares rather than assuming one.

**The citation checker was validated at the base state before being trusted at the head.** Run at `dbe2ee28` it reported exactly the 10 occurrences in 4 files and all 9 cited paths DEAD, which is the defect the change exists to fix. A checker that cannot see the defect cannot certify its removal.

---

## 3. The six adversarial checks

### CHECK 1 — BYTE-FIDELITY of every published file, from the COMMITTED BLOB

Command: `git show <head>:<path>` piped into sha256, compared against the workspace source file's own digest. Nothing was read from the worktree.

```text
docs/evidence/fu3-record-publication-2026-10-13/BER-G3-FU3-EXECUTION.md
    committed bytes=25606  sha256=ea521f84c4d0d88f8e888f3588147a6a63c659f8773f7d41339d9eeca47b9915
    IDENTICAL workspace source: evidence/docs-refresh-2026-10-12/BER-G3-FU3-EXECUTION.md
docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-FINAL-REVIEW-F.md
    committed bytes=30777  sha256=c0b0c548fa6b8f2cc9b961814099e8e12e690729bfdaa16e6c4b96263d7dab8a
    IDENTICAL workspace source: evidence/docs-refresh-2026-10-12/FU3-RECORD-FINAL-REVIEW-F.md
docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-stage-g-summary.md
    committed bytes=25454  sha256=d2ed1cfba306c12d993b5718b1d903de656409f1ff91af2e90c3ee1b178aa031
    IDENTICAL workspace source: evidence/docs-refresh-2026-10-12/FU3-RECORD-stage-g-summary.md
docs/evidence/fu3-record-publication-2026-10-13/REVIEWPATH-FINAL-REVIEW-F.md
    committed bytes=21023  sha256=f367d36eda52c45289dee5d2cbdcde82c534db8c97786d23b78d51531491cd55
    IDENTICAL workspace source: evidence/docs-refresh-2026-10-12/REVIEWPATH-FINAL-REVIEW-F.md
```

**PASS — 4 of 4 byte-identical**, and the four digests equal the plan's declared values exactly, which I had independently measured from the archive before the head existed. All four sources are LF-only with a final newline, so the repository's `* text=auto eol=lf` rule is a no-op and the committed bytes are the archive bytes.

**AC2 — the copies' own integrity claims still hold.** Three self-digest footers recompute from the committed blobs, and the fourth file's body digest recomputes over the bytes above its footer heading:

```text
BER-G3-FU3-EXECUTION.md       self-digest f5a6b9ca66c99d..   recomputed same  OK
FU3-RECORD-FINAL-REVIEW-F.md  self-digest 8f554598a04d91..   recomputed same  OK
FU3-RECORD-stage-g-summary.md self-digest 059822aabffb13..   recomputed same  OK
REVIEWPATH-FINAL-REVIEW-F.md  body digest over L1..L102 (bytes above the footer heading at L103):
    computed 81884e0d49cb117c7f7884350ce23adcfac6788891c0a9bc8828dc19461abcc8
    expected 81884e0d49cb117c7f7884350ce23adcfac6788891c0a9bc8828dc19461abcc8   MATCH
```
**PASS — 3 of 3 footers plus the body digest.** Publishing the files verbatim therefore falsifies none of their self-descriptions.

### CHECK 2 — FROZEN O-F1 NOTE UNTOUCHED

Command: whole-file byte comparison of `git show <base>:<path>` against `git show <head>:<path>` for `docs/roadmaps/behavioral-eval-runner-backlog.md`, plus a single-insertion decomposition over the whole file.

```text
base bytes=285010 lines=4275 | head bytes=288250 lines=4310 | delta 35 lines / 3240 bytes
insertion offset X = start of base L4192 = 279160 ; base[X-1]=b'\n' ; base[X:X+8]=b'## 14. C'
head == base[:X] + I + base[X:] : True
zero base bytes unpreserved        : True
all base lines survive in order    : True
I bytes=3240 lines=35 ; sha256(I)=4d64ce3b0b996d0f2f2aa320d3266a4fc0df2f1a091bf1480d62ffc21af5cefe
O-F1 heading index base=[4148] head=[4148]
42-line block sha256 base = f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d
42-line block sha256 head = f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d
block byte-identical base vs head: True
backlog diff: hunks=1 deletions=0 additions=35
    @@ -4191,0 +4192,35 @@ itself is a separate, later host phase that runs only under the merged grant.
```

**PASS.** The appended entry is a **pure insertion** of 3,240 bytes at byte offset 279,160 — exactly where base line 4192 begins — and **zero base bytes are unpreserved**. The Lead asked specifically that I check no existing line was altered *anywhere* in the file, not only around the note: the diff carries **0 deletions and 1 hunk**, and the byte decomposition proves it independently of the diff, so no line above or below the insertion was touched. The frozen O-F1 note's 42-line block is byte-identical and still hashes to `f29decc7…182d`, the digest under which the pull request #765 merge was recorded.

### CHECK 3 — NO ARCHIVE DUMP

```text
git diff --numstat dbe2ee28 bd210954
1	1	docs/README.md
18	2	docs/evidence/README.md
347	0	docs/evidence/fu3-record-publication-2026-10-13/BER-G3-FU3-EXECUTION.md
274	0	docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-FINAL-REVIEW-F.md
233	0	docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-stage-g-summary.md
157	0	docs/evidence/fu3-record-publication-2026-10-13/README.md
107	0	docs/evidence/fu3-record-publication-2026-10-13/REVIEWPATH-FINAL-REVIEW-F.md
35	0	docs/roadmaps/behavioral-eval-runner-backlog.md
files changed: 8 (added 5, modified 3, deleted 0, renamed 0)
ADDED FILE COUNT = 5
added under the archive prefix: 0
```

**PASS — the added-file count is 5.** Thousands would be an archive dump; five is the declared set. The archive holds 626,280 files by my own enumeration (the count is method- and time-dependent and no criterion binds it — the plan records 629,224–737,179 across measurement methods, and agents are writing into it continuously). Nothing under `_resume-2026-10-09/` is tracked at either revision, and the prefix contributes zero added paths.

### CHECK 4 — SUPERSEDING ENTRY

**Is it appended at the END of section 13, not spliced?** Yes — see CHECK 2: the single insertion point is immediately before `## 14.`, and the new entry is the last of the 22 section-13 entries.

```text
section-13 entries at head: 22 ; the new entry is the LAST one
new entry heading at head L4192 ; ## 14. at head L4227 (occurs exactly once)
entry inside section 13: True ; before ## 14.: True
lines immediately ABOVE the new entry:
   '- **Scope:** this entry records a closure. It creates no stage, gate, receipt row or bound'
   '  existing byte and touches no merged body. **New authority: None.**'
   ''
```

**Does it NAME the entry it supersedes?** Yes. It names the superseded entry by its heading text **and** its line range, and it says the word "superseded":

```text
contains 'O-F1 discharged' : True      <- the superseded entry's heading text
contains 'L4149'           : True      <- that entry's first line
contains 'L4190'           : True      <- that entry's last line
contains 'superseded'      : True
```
That satisfies the log's own rule at L2672–L2675 — *"entries are never edited or deleted; corrections append a superseding entry that names the entry it supersedes"* — which I read at the head to confirm it still says that.

**Is it the settled text, and a paraphrase rather than a verbatim block quote?** Both, exactly as the revised plan settled:

```text
appended region: 35 lines, 3240 bytes
plan section 7.3 block: 35 lines, 3240 bytes
BYTE-IDENTICAL to the plan's settled text: True
contains the rule block's opening words 'A permanent record here' : False
contains a block-quote marker ('> ' lines) : False
contains a fenced block : False
```
**PASS.** The entry is byte-for-byte the text the accepted plan settled, it names its predecessor, it sits at the end of the log, and it states the rule in the log's own bullet voice instead of quoting the rule block — a verbatim quote would have been a deviation from the settled plan, and there is none.

### CHECK 5 — INDEX COUNT

```text
base docs/evidence/README.md  "find **N selected decision and delivery evidence pages**" -> 16
base docs/evidence/README.md  "these N pages"                                          -> 16
base docs/README.md           "routes to N dated decision"                             -> 16
base docs/evidence/README.md  table rows carrying a link                               -> 16
head docs/evidence/README.md  "find **N selected decision and delivery evidence pages**" -> 17
head docs/evidence/README.md  "these N pages"                                          -> 17
head docs/README.md           "routes to N dated decision"                             -> 17
head docs/evidence/README.md  table rows carrying a link                               -> 17
head stale strings remaining ("16 selected", "these 16 pages") -> []
```
**PASS — 17 = 17 = 17 = 17.** The figure now equals the true number of pages the index lists, at all three live sites, and no stale "16" remains. *Method note:* the L3 figure **wraps across two source lines** ("find **17 selected decision" / "and delivery evidence pages**"), so a line-oriented byte grep for the whole phrase returns nothing — I compared whitespace-normalised text, which is the only method that measures the claim rather than the wrapping.

### CHECK 6 — CITATION RESOLVABILITY (the whole point)

Verified by **tree inspection**, not by reading prose: `git cat-file -e <head>:<path>` for every path, and Markdown link targets resolved against the committed tree.

```text
the five new publication paths exist at head:
  docs/evidence/fu3-record-publication-2026-10-13/README.md                     exists=True
  docs/evidence/fu3-record-publication-2026-10-13/BER-G3-FU3-EXECUTION.md        exists=True
  docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-FINAL-REVIEW-F.md   exists=True
  docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-stage-g-summary.md  exists=True
  docs/evidence/fu3-record-publication-2026-10-13/REVIEWPATH-FINAL-REVIEW-F.md   exists=True

Markdown link targets in the eight changed files: 288 ; UNRESOLVED: 1
  the single "unresolved" target is
  REVIEWPATH-FINAL-REVIEW-F.md:92 -> .claude/skills/agent-governance-audit/SKILL.md
  ... and that line sits INSIDE a fenced code block (fence parity = inside), so the
  repository's own checker does not treat it as a link. Not a defect.

archive_dependent_targets (link targets pointing into the archive): 0
  <- the decisive figure: nothing a reader can click depends on the archive

AC9 map measurement on the publication record:
  link_targets = 9 ; archive_dependent_targets = 0
  map_occurrences = 10 (the old-path -> new-path map, which the record must carry)
  occurrences_outside_map = 0
```

**Resolvability of the citations this change targets.** The frozen note's three archive citations (backlog L4160, L4162, L4165) are superseded by the new entry, whose three replacement citations are in-repo Markdown links to the published copies — including the two heading fragments, one of which is the unusual nine-hyphen slug the plan took from the checker's own anchor set. The repository's own checker resolves them:

```text
python -P scripts/ci/check-markdown-links.py docs/README.md docs/evidence/README.md docs/evidence/fu3-record-publication-2026-10-13/README.md docs/roadmaps/behavioral-eval-runner-backlog.md
files: 4   links checked: 198   anchors checked: 32   broken: 0   dead: 0   external-skipped: 80   other-skipped: 0
exit 0

corpus-wide (AC4, the step CI runs): 663 pages in 9 batches
batches failed: 0 ; TOTAL broken: 0 ; TOTAL dead: 0
```

**The owed citations are recorded as owed, not silently claimed fixed.** The publication record enumerates all nine cited paths with a per-path disposition — four PUBLISHED, five OWED — and names each owed site with its file **and line**:

```text
| 5 | _resume-2026-10-09/evidence/p0/P0A-A1-PLAN.md  | aegis-ci-baseline-2026-10-11.md line 43 | OWED |
| 6 | _resume-2026-10-09/evidence/p0/P0A-A1-AUDIT-B.md | aegis-ci-baseline-2026-10-11.md line 45 | OWED |
| 7 | _resume-2026-10-09/evidence/p0/F0-source-authority-reconciliation.md | aegis-ci-baseline-2026-10-11.md line 49 | OWED |
| 8 | _resume-2026-10-09/evidence/dirfd-probe-repair/HANDOFF-CORRECTION.md | scif-closeout-corrections-2026-10-11.md line 15 | OWED |
| 9 | _resume-2026-10-09/FAST-CHECKPOINT-2026-10-11D.md | scif-closeout-corrections-2026-10-11.md line 84 | OWED |
plus the two further sites found by re-derivation: backlog line 4143 and APPROVAL_REGISTER.md line 5964.
ci-baseline archive citations: base 3 -> head 3 (unchanged, as owed)
```
**PASS.** Every citation the change claims to fix now resolves inside the repository at that head; every citation it does not fix is named with its file and line as owed; and no link target on the retrieval path requires the archive.

---

## 4. Remaining acceptance criteria

**AC3 — links the change adds resolve.** The 4-page run above: `broken: 0, dead: 0, anchors checked: 32` (threshold: exit 0, broken 0, dead 0, anchors >= 4). **PASS.**

**AC4 — the corpus-wide link check CI runs stays green.** 663 pages (the plan's threshold exactly), 9 batches, 0 batch failures, 0 broken, 0 dead, against CI's floor of 600. **PASS.**

**AC5 — the stated count equals the measured row count.** 17 = 17 = 17 = 17 (CHECK 5). **PASS.**

**AC6 — append-only, frozen note unchanged.** 0 deletions, 1 hunk, block still `f29decc7…182d` (CHECK 2). **PASS.**

**AC7 — exactly the declared file set, exactly three lines replaced.**

```text
total deleted lines: 3
   DEL '-- [Evidence reading guide](evidence/README.md): routes to 16 dated decision and'
   DEL '-This index helps maintainers and reviewing agents find **16 selected decision'
   DEL '-page has been reviewed or that these 16 pages cover the full repository.'
deletions NOT containing "16": []
each is replaced by the same line with 17:
   '- [Evidence reading guide](evidence/README.md): routes to 17 dated decision and'
   'This index helps maintainers and reviewing agents find **17 selected decision'
   'page has been reviewed or that these 17 pages cover the full repository.'
total added lines: 1172 ; hunks: 10 (5 pure additions, 1 index-row insertion, 1 backlog insertion, 3 count-line replacements)
git diff --check -> no output
```
**PASS — 5 added + 3 modified = 8 paths; 3 deletions, every one a count line, each replaced by its 17 twin; 0 deletions containing anything else.** This is the scope contract exactly, and no ninth path appears.

**AC8 — no credential material, every hit named and read.** Run with the revised pattern (the one that includes the `token *[:=]` alternative):

```text
hits_on_copies = 3
BER-G3-FU3-EXECUTION.md:155      input 5,000 nano-USD/token = **$5.00 / 1M** ...
FU3-RECORD-FINAL-REVIEW-F.md:121 validate-skills job 115364466965 failed **step 20 pr-body-...
REVIEWPATH-FINAL-REVIEW-F.md:47  REVIEWPATH-VALIDATE-E.md ... 9dfc47f8...013569599029...
hits_on_record = 0
```
**PASS.** The three hits land on exactly the lines the revised threshold names — a provider price line, a CI job id, and a sha256 inside a table row — and the new publication record carries none. I independently read all three: none is credential material. *(My first scan used revision 1's pattern without the `token` alternative and printed 2; that is the very defect Stage B raised as D1 and the revision repaired. The revised criterion reproduces exactly.)*

**AC9 — a fresh checkout can retrieve the evidence.** The four files exist in the committed tree and hash to the recorded values from the committed blobs (CHECK 1); `archive_dependent_targets = 0` and `occurrences_outside_map = 0` (CHECK 6); the cited anchors resolve (AC3). **PASS.**

**AC10 — no protected path, with controls that fire.** The plan's own script, run verbatim at the head:

```text
pattern_len = 371
POS = 11 matched = 11
DOCUMENTED_NEGATIVES = 4 matched = 0
DECLARED_PATHS = 8 matched = 0
NEGATIVES_TOTAL = 12 matched = 0
CONTROL_FAILURES = 0
```
**PASS** — every number equals the revised threshold. Hosted confirmation: `gate-guard` **pass** on pull request #766.

**AC11 — the rule in all three placements, whitespace-normalised.** The plan's exact sentence, compared on whitespace-flattened text:

```text
sentence = 'An out-of-tree path alone is not acceptable support. A digest pins identity; it never makes an absent artifact retrievable.'
PRESENT  docs/evidence/README.md
PRESENT  docs/evidence/fu3-record-publication-2026-10-13/README.md
PRESENT  docs/roadmaps/behavioral-eval-runner-backlog.md
```
**PASS — 3 of 3.** Nobody re-wrapped correct text to satisfy a byte grep: I checked all four normative sentences of the rule block separately, and the two prose placements carry **4 of 4** while the log entry carries 1 of 4 — which is exactly the settlement the revision records (the log states the rule in its bullet voice; the two prose placements carry the block). The whitespace-normalised method is the right one because each placement wraps to its own width.

**Supporting checks.** DCO: `python -P scripts/check_dco.py --range origin/main..HEAD` -> exit 0, `OK: 1 commit(s) checked, all signed off or exempt.` Hosted checks on #766: `changes` pass, `gate-guard` pass, `validate-skills` pass; `tools-tests-linux`, `tools-tests-windows` and `windows-offline-checks` skipped by path filter, recorded as skipped and never as passed.

**Pull-request body (completeness).** Three whole-line sentinel pairs (skills L66, security L100, witness L111; ends L96/L105/L124), one further substring-only appearance at L126 which is a quoted reference and correctly **not** treated as a sentinel; the security answer is **No**; the skills table carries 7 data rows plus **3 explicit absence records** (Stage A shape, Stage B shape, Stage C shape) — no stage omitted. Bound-field first-16 recomputed by me: **`6f36dda81cf9f3cd`** (full `6f36dda81cf9f3cd9cf0ea960dd017a4e761124781bb378d90d006a2a46c27ee`) over a 17,127-byte collapsed payload, at body revision `updated_at 2026-10-13T18:00:10Z` (30,375 bytes, sha256 `e6bcb6d866de5d95…`). I report the revision I hashed; if the body moves before Stage F, that hash binds only the revision above.

---

## 5. Defects

**None.** I found no defect in the change, at any severity. Specifically, no BLOCKER, MAJOR, MINOR or NIT finding survives scrutiny: the byte-fidelity, append-only, scope, index-count, gate-pattern and citation-resolvability properties all hold, and the items below are stated limits of the accepted plan rather than faults in this implementation.

---

## 6. Observations — stated, not defects

**OBS-1 (INFO) — the published copies still contain archive-path references inside their frozen archival text.** The four verbatim copies carry archive references in their own body (for example `BER-G3-FU3-EXECUTION.md` L45, L113, L127, L273, L321 and L339). A reader who follows *those* still cannot retrieve the referenced artifacts. This is **explicitly accepted by the plan** as owed item O4 — those bytes are frozen archival text with self-digests, and editing them would falsify the record's own integrity claim that AC2 proves still holds. Choosing this limit is the plan's call and it is stated in the repository rather than hidden; I record it so the residual is visible.

**OBS-2 (INFO) — the pull-request body does not yet carry the Stage D/E/F skills rows.** By design: those stages had not run when Stage C published. My own Stage D rows are authored in section 7 below, copy-ready, so Stage D is not the obstacle. A row for every stage that ran must be in the body before Stage F computes its bound-field hash, or this change would repeat the class of defect the previous lane closed.

**OBS-3 (INFO, method) — two checks need a whitespace-normalised comparison, and here is why.** The evidence index's L3 figure wraps across two source lines, and the rule sentence wraps inside the clause "A digest pins / identity". A byte-oriented grep therefore returns nothing for text that is correct. I used whitespace-flattened comparison for both and state it, so a later reader does not mistake the empty byte grep for a failure.

---

## 7. Stage D skills usage (authored here; to be published verbatim by the authorized publisher)

**Copy-ready rows** — the exact Markdown to insert into the body's "Aegis skills used" table:

```text
| `code-reviewer` | Stage D / `of1-stage-d` | Read in full and applied its five-pass review to the obtained committed range dbe2ee28..bd210954: the real diff from git, the intent from the commit message and the pull-request body, then correctness, security, reliability, tests-and-migrations and maintainability passes, with every finding anchored to the artifact that evidences it | the audit's verdict and its evidence: 4 of 4 committed blobs byte-identical to their archive sources; the backlog proven a single 3,240-byte insertion with zero base bytes unpreserved; 5 added files and exactly 3 replaced count lines; 17 = 17 = 17 = 17; archive_dependent_targets = 0; CONTROL_FAILURES = 0; no defect found — recorded in AUDIT-D.md |
| `skill-usage-ledger` | Stage D / `of1-stage-d` | Read in full and emitted this stage's six-field usage records, resolving each skill name against `tools/skills-manifest.json` at the audited base and copying each digest from the manifest rather than remembering it | both names resolve and both digests recompute from `.claude/skills/<name>/SKILL.md` with CRLF-to-LF normalisation: `code-reviewer` = `6238b67b7b90fcbb26fcc45300562efa9e290a9d3870548e37bedaabbc76449a`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4`; manifest `tools/skills-manifest.json` sha256 `9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832`; the ledger block is in section 7 of `AUDIT-D.md` |
```

**Row source records** — for insertion inside the existing skills bound field, immediately after the table:

```text
<!-- Row source: agent=of1-stage-d; stage=D; round=1; row=SDD-1; target=bd21095427f584eaf97fa3218b942d1c502594c8 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/AUDIT-D.md section 7 fenced block row 1 (the exact bytes hashed); binding=sha256 f2182c824775790350a4d0a5e99b1f15d27b255d7bd2ee26bc1baaf81b1f7fd8 over the fenced block's UTF-8 bytes including the final newline (the two Stage D row lines joined by LF plus one trailing LF, 1460 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=none. -->
<!-- Row source: agent=of1-stage-d; stage=D; round=1; row=SDD-2; target=bd21095427f584eaf97fa3218b942d1c502594c8 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/AUDIT-D.md section 7 fenced block row 2 (the exact bytes hashed); binding=sha256 f2182c824775790350a4d0a5e99b1f15d27b255d7bd2ee26bc1baaf81b1f7fd8 over the fenced block's UTF-8 bytes including the final newline (the two Stage D row lines joined by LF plus one trailing LF, 1460 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=none. -->
```

**Captured row-block digest — computed from these exact bytes, never remembered:**
sha256 `f2182c824775790350a4d0a5e99b1f15d27b255d7bd2ee26bc1baaf81b1f7fd8` over the two row lines joined by LF plus one trailing LF (`1460` bytes). I validate that value by re-deriving it from the written file, because the previous lane published a `binding=` digest that did not recompute from the source it named — I do not repeat that defect.

**Six-field ledger (`skill@<manifest-sha256[:12]> / reason / applied / result / incomplete / by`):**

```text
code-reviewer@6238b67b7b90 / reason: Stage D must review an ACTUAL obtained diff rather than a description, and report anchored findings / applied: obtained the committed range dbe2ee28..bd210954 and the live pull-request body, ran the five passes, and re-derived every acceptance criterion from the committed git objects rather than the worktree / result: verdict SD-D ACCEPT with no defect found; 4 of 4 published blobs byte-identical; backlog a pure 3,240-byte insertion with the frozen 42-line block still at f29decc7...182d; 5 added files; 17 = 17 = 17 = 17; archive_dependent_targets = 0; CONTROL_FAILURES = 0 / incomplete: the Stage E and F stages and the merge receipt are not mine to run, and the D/E/F skills rows are not yet in the body by design / by: wcd-stage-d, Stage D, round 1
skill-usage-ledger@6a27b5c8e690 / reason: this lane's workflow requires each stage to record which skills it read, bound to the manifest hash so the exact instructions are pinned / applied: authored the two rows above and this ledger, resolving both names in tools/skills-manifest.json and recomputing both digests from .claude/skills/<name>/SKILL.md with CRLF-to-LF normalisation / result: both resolve and both recompute exactly - code-reviewer 6238b67b7b90fcbb26fcc45300562efa9e290a9d3870548e37bedaabbc76449a, skill-usage-ledger 6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4; manifest sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832 / incomplete: None / by: wcd-stage-d, Stage D, round 1
```

**Limits, stated rather than omitted.** This stage read no other Aegis skill. It deliberately did not apply `reviewable-diff-discipline` (`MANUAL-ONLY`, not named by a human); that is recorded as refused, not used. Per `docs/delivery-workflow.md` L720–L721 this row preclaims no other stage's verdict and embeds no digest of itself and no eventual body hash.

---

## 8. Not verified, and the limits of this audit

- **AC9's "fresh checkout" step was performed in my own fresh HTTPS clone**, fetched to the head and checked out detached, plus by tree inspection of the committed objects (`git cat-file -e`) at the head. I did not create a *second* clone solely for that step; the retrieval property is proven from the committed tree, which is what a fresh checkout contains.
- **The archive file count is not a stable number.** I measured 626,280 files by my own enumeration; the plan records 629,224, Stage B 737,158 and the Lead 733,980 across different methods and moments. No acceptance criterion binds this value, and I did not treat any figure as authoritative — the operative fact is that the archive is untracked and 5 files were added, not thousands.
- **The bound-field hash binds the body revision I hashed** (`updated_at 2026-10-13T18:00:10Z`). A later body edit — which the Stage D/E/F row insertion will require — changes it; that is expected and is not a defect, but Stage F must hash the body as it then stands.
- **I did not assess the governance question raised by the other P2 finding on the previous pull request** (whether a dated note may close a mandatory Stage F failure). The plan records it as an explicit non-claim, and it is not a citation-durability question. Out of this audit's scope.
- **Not reviewed:** the other 1,519 files of the checkout; the hosted CI logs beyond the `gh pr checks` conclusions; the internal content of the four published archival copies (they are verbatim by AC1 and byte-identity is the property claimed, so line-level review of their prose would be reviewing another lane's frozen record, not this change).
- **Environment limit, disclosed:** this host's sandbox blocks MSYS `sh.exe`, so the local-path clone route cannot run `git-upload-pack`. I cloned **directly from GitHub over HTTPS**, and ran `gh` directly rather than through a wrapper. Python subprocess capture worked normally here.

---

## 9. Timing

| | |
| --- | --- |
| **Item** | `Workspace-citation durability — Stage D: independent implementation audit` |
| **Start** | `2026-10-13T10:25:53-07:00` (America/Los_Angeles) — the stamp sampled at this item's first action; no earlier stamp is invented |
| **ETA at start** | **not stated** — the brief carried no estimated active-work duration for this item, so no ETA-versus-actual comparison is claimed as "met" |
| **Finish** | `2026-10-13T11:05:54-07:00` — sampled in the same program run that performed this file's final write |
| **Measured wall time** | `40 minutes (2401 seconds)` |
| **Active time** | **not separately instrumented.** The comparison is therefore **IMPERFECT and labelled as such**: the item was blocked on `task-10` (Stage C) for most of its wall time — the lane gained a repair round (`task-15` plan revision, `task-16` re-audit) before Stage C ran — so wall time materially overstates active audit work. |

---

## 10. Summary

| Check | Result |
| --- | --- |
| 1. Byte-fidelity of the four published files, from committed blobs | **PASS — 4 of 4 IDENTICAL** |
| 2. Frozen O-F1 note untouched; only change is the appended entry | **PASS — 0 deletions, block still `f29decc7…182d`** |
| 3. No archive dump | **PASS — 5 added files, 0 under the archive prefix** |
| 4. Superseding entry names its predecessor and is appended at the log's end | **PASS — byte-identical to the settled text; paraphrase, not a quote** |
| 5. Index count equals the pages it lists | **PASS — 17 = 17 = 17 = 17** |
| 6. Citation resolvability by tree inspection | **PASS — 0 archive-dependent link targets; owed sites named with file and line** |
| AC2 footers and body digest | **PASS — 3 of 3 plus the body digest** |
| AC3 / AC4 link checks | **PASS — changed pages 0 broken / 0 dead; corpus 663 pages 0 broken / 0 dead** |
| AC7 scope and replacements | **PASS — 8 paths, 3 deletions, all count lines** |
| AC8 credential scan | **PASS — hits_on_copies = 3 on the named lines, hits_on_record = 0** |
| AC10 protected paths with controls | **PASS — 8/8 clear, 11/11 positives fire, CONTROL_FAILURES = 0** |
| AC11 rule in three placements | **PASS — 3 of 3 PRESENT, whitespace-normalised** |
| DCO / hosted checks | **PASS — exit 0 with `OK:`; gate-guard, validate-skills, changes all pass** |
| Defects | **none** |

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes including the final newline. Line endings are LF only. -->
sha256: 9edc4aa96d1aea6aafe17f99bfa765312744a83faad27ebd15c69532701d06da
