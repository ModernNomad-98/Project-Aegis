# Workspace-citation durability — Stage D ROUND 4 independent implementation audit

**Item:** "Workspace-citation durability — Stage D ROUND 4" (shared task `task-25`).
**Agent:** `of1-stage-d` — in plain words, *the Stage D holder, auditing a fourth round after two further commits moved the head*. **No subagents were used.**
**Audited head (40 characters):** `95351dda27210f4b5707aa067cd138bf37710bd5` — in plain words, *the fifth commit on the branch, which appends the superseding section-13 entry correcting one word of the publication entry*. Tree `69068cc38bf4e63cbeeda417eb00c3ea0f7f88af`.
**Rounds it supersedes:** `c5f71554...` (round 3, ACCEPT), `b591e0d9...` (round 2, REVISE), `bd210954...` (round 1, ACCEPT).
**Pinned base:** `dbe2ee28559fef88950b2d8822cf72d3e595ba86`.
**My clone:** `_resume-2026-10-09/_wcd-d-clone` — my own HTTPS clone, detached at the audited head.

**Reading key — every label in plain English.**
- `P2` — *the middle severity band of the automated reviewer's findings; P2-and-higher is a floor that must be triaged.*
- `SD-D` — *the Stage D independent implementation audit verdict; this record.*
- `source-side` / `committed-side` digest — *the sha256 of the archive original as measured when the copy was taken, and the sha256 of the bytes actually committed.*
- `sanitized derivative` — *a published copy that is deliberately not byte-identical to its source, because identifiers present in no tracked file were removed.*
- `K-081/D98` — *a defect recorded earlier in this session: an impossible worst-case figure that counted a zero-charge metadata request as a charged attempt.*
- `bound field` — *one of the three PR-body fields the process acts on; the hash covers those three, and nothing else in the body.*
- `L2672-L2675` — *the append-only log's own rule: entries are never edited; corrections append a superseding entry that names the entry it supersedes.*

---

## 1. Verdict

**VERDICT: `SD-D: ACCEPT`** — in plain words, *the workflow's word for an implementation audit that passes and can be built on by the next stage*.

**All five Codex P2 fixes are genuinely correct, not merely present**, and I verified each against its own artifact rather than against the commit message or the Lead's summary: the budget arithmetic recomputed by hand, the dual digests recomputed from the committed blobs, the retained finding text re-hashed from its quoted characters, the historical-absence claim re-read as a scoped current-state statement, and the sanitization **basis re-derived against the base revision myself**. The superseding entry does what it claims, the anchor it uses resolves, and every invariant that must not have moved has not moved.

One **LOW** observation is recorded (section 7): the retained text's stated length, "913 characters", is reproducible only as a UTF-16 code-unit count — it is 911 Unicode code points and 918 UTF-8 bytes, and the record does not name the convention. The **digest**, which is the operative binding, recomputes exactly.

**Skill applied:** `code-reviewer` (`.claude/skills/code-reviewer/SKILL.md`, sha256 CRLF-to-LF `6238b67b7b90fcbb26fcc45300562efa9e290a9d3870548e37bedaabbc76449a`). `reviewable-diff-discipline` was **not** applied: `MANUAL-ONLY`, and no human named it.

**Verifier validated before use.** My footer verifier reproduced three known-good artifacts (`c2d106af...`, `250cc3e8...`, `a17f1ecd...`) **3 of 3** before it was pointed at the derivative — the standing caution, honoured again.

---

## 2. What moved, and the shape of the change

```text
git log --format='%H %ad %s' --date=iso dbe2ee28..95351dda
95351dda27210f4b5707aa067cd138bf37710bd5  2026-10-13 12:27:05 -0700  docs: supersede one word of the publication entry - the fourth file is a sanitized derivative
61e7344236849d8f9d535f230d74906995eaceb7  2026-10-13 12:24:35 -0700  docs: fix the four wrong claims and sanitize the two new identifiers in the FU-3 execution copy
c5f715544da64a43e0c900d33b298bce0957d504  2026-10-13 11:28:27 -0700  docs: enumerate every index row the 2026-09-23 sweep does not reach
b591e0d97dbc176a4bdc17128065e2bcf2daed35  2026-10-13 11:18:49 -0700  docs: narrow the citation rule's enforcement claim, scope its census, and date the new index row
bd21095427f584eaf97fa3218b942d1c502594c8  2026-10-13 10:55:55 -0700  docs: publish the FU-3 evidence the O-F1 note cites, and state the citation-durability rule

git diff --numstat dbe2ee28 95351dda
1       1       docs/README.md
29      2       docs/evidence/README.md
357     0       docs/evidence/fu3-record-publication-2026-10-13/BER-G3-FU3-EXECUTION.md
274     0       docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-FINAL-REVIEW-F.md
233     0       docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-stage-g-summary.md
238     0       docs/evidence/fu3-record-publication-2026-10-13/README.md
107     0       docs/evidence/fu3-record-publication-2026-10-13/REVIEWPATH-FINAL-REVIEW-F.md
60      0       docs/roadmaps/behavioral-eval-runner-backlog.md
```
Eight paths, five added, three modified, no archive dump. The publication record grew to 238 insertions and the derivative to 357; the backlog gained 60 lines of appended entry. **The three untouched copies' numstat did not move at all** (274/0, 233/0, 107/0) — the first evidence that the sanitization touched only the fourth file.

---

## 3. The five Codex P2 fixes

### 3.1 — P2 4262995856: the budget arithmetic — PASS

I recomputed the arithmetic rather than reading the corrected total:

```text
per attempt = 8,000 input x 5,000 + 25,000 output x 30,000 nano-USD
            = 40,000,000 + 750,000,000 = 790,000,000 nano-USD = USD $0.79
200 charged judgment attempts = 158,000,000,000 nano-USD = USD $158.00
201 x $0.79 (the impossible path)                        = USD $158.79

in the committed derivative:
  contains '158.79'                             -> False   (the impossible path is GONE)
  contains '158.00'                             -> True
  contains 'not charged by the attempt formula' -> True
```
The corrected block reads: *"200 judgment attempts (the judgment ceiling; each charged at the worst case) = ... USD $158.00 / + at most 1 read-only metadata availability request (the 201st request: ... it submits no calibration content and invokes no generation, so the worst-case attempt charge above does not apply to it) = not charged by the attempt formula / worst case on the permitted 201-request path = ... USD $158.00"*. The 200 + 1 split is the correct reading of the approved maxima, and the total no longer charges a zero-charge request. **The impossible $158.79 path is gone.** This was the `K-081/D98` re-exposure and it is genuinely closed.

### 3.2 — P2 4262995828: source-side AND committed-side digests — PASS

The record's section 1 table now carries both columns for all four files, and I recomputed every committed-side value from the committed blobs:

```text
| 1 | BER-G3-FU3-EXECUTION.md        | SANITIZED DERIVATIVE | 25,606 -> 26,345 | source ea521f84c4d0d88f8e888f3588147a6a63c659f8773f7d41339d9eeca47b9915 | committed cc183e4504a1b280d04e5726279c71daaa4593e1e5272ee43ce2110838cf6ac3 |
| 2 | FU3-RECORD-FINAL-REVIEW-F.md   | byte-identical       | 30,777 -> 30,777 | source c0b0c548fa6b8f2cc9b961814099e8e12e690729bfdaa16e6c4b96263d7dab8a | committed same |
| 3 | FU3-RECORD-stage-g-summary.md  | byte-identical       | 25,454 -> 25,454 | source d2ed1cfba306c12d993b5718b1d903de656409f1ff91af2e90c3ee1b178aa031 | committed same |
| 4 | REVIEWPATH-FINAL-REVIEW-F.md   | byte-identical       | 21,023 -> 21,023 | source f367d36eda52c45289dee5d2cbdcde82c534db8c97786d23b78d51531491cd55 | committed same |

recomputed from the blobs at the audited head:
  BER-G3-FU3-EXECUTION.md        26,345 bytes  cc183e4504a1b280d04e5726279c71daaa4593e1e5272ee43ce2110838cf6ac3  == table: True
  FU3-RECORD-FINAL-REVIEW-F.md   30,777 bytes  c0b0c548fa6b8f2cc9b961814099e8e12e690729bfdaa16e6c4b96263d7dab8a  == table: True
  FU3-RECORD-stage-g-summary.md  25,454 bytes  d2ed1cfba306c12d993b5718b1d903de656409f1ff91af2e90c3ee1b178aa031  == table: True
  REVIEWPATH-FINAL-REVIEW-F.md   21,023 bytes  f367d36eda52c45289dee5d2cbdcde82c534db8c97786d23b78d51531491cd55  == table: True
```
**These are real values, not placeholders**: each committed-side digest reproduces from a plain hash of the committed blob, and for the three byte-identical copies the two columns are equal by construction — which is exactly what makes the one inequality meaningful. The record also states the reading convention: the committed-side column is the one a clone reproduces, and the source-side column identifies the archive original.

### 3.3 — P2 4262995838: the finding text retained with a digest — PASS, with one LOW observation

The record retains the finding verbatim in a fenced `text` block (L28-L34) with its locator (review comment `4261109123`, backlog line 4162, written against `e0a026e2...`) and a link, and states plainly that a comment URL is mutable so the digest — not the URL — is what pins the text.

I extracted the quoted block and re-hashed it:

```text
fenced block L28..L34, 7 lines
sha256(no trailing newline)   = be0e3aab224a7384c0aedb734c3d1bffa65407b836b6b0a0dfa257bcdb266ecb   MATCH
sha256(with trailing newline) = 8ba09805a96cb1697590ae6c9a007477afbedac5df15bd6da125641b9c89cfe7   no match
published digest              = be0e3aab224a7384c0aedb734c3d1bffa65407b836b6b0a0dfa257bcdb266ecb
```
**The digest reproduces exactly** under the stated method ("UTF-8, no trailing newline added"), so the retention is verifiable by anyone holding the record. See section 7 for the length figure.

### 3.4 — P2 4262995850: historical absence is now a current-state statement — PASS

```text
BEFORE (round 3):  "Test-Path returns False; the directory does not exist. ... No provider
                    execution evidence was ever placed at the authorized root on this host."
AFTER  (round 4):  "Test-Path returns False; the directory was NOT PRESENT WHEN SEARCHED. ...
                    That is a current-state observation and nothing more: it does not establish
                    whether the directory, or any provider execution evidence at it, ever existed
                    on this host. Its historical existence is UNKNOWN, in line with this record's
                    own governing packet, which states that missing old evidence does not prove
                    zero use."
```
The over-claim is gone and the limit is stated in the record's own voice, citing the governing packet's rule. The derivative still contains `UNKNOWN` and `current-state observation` (verified by string search), and the evidentiary measurements it rests on (`1,719` files, the 16-byte history file) are retained. **PASS.**

### 3.5 — P2 4262995845: the sanitized derivative — PASS, basis re-derived by me

I re-derived the basis against the base revision rather than taking the Lead's numbers, by counting **tracked files** containing each token at `dbe2ee28`:

```text
token                                          tracked files at BASE   which
the username token (raw value withheld)                                    4    APPROVAL_REGISTER, step-0-reconciliation-v4, backlog, ber-wp2b3-owner-decision-chain
the distro-release token (raw value withheld)                                   5    the above four + ber-wsl2-stage-a-setup-proposal
the WSL home root (the WSL UNC root token / the distro-release token / home) 2    APPROVAL_REGISTER, backlog
the distro-side directory-name token (raw value withheld)                                  6    APPROVAL_REGISTER, step-0-reconciliation-v4, backlog, ber-virtualbox-stage-a-setup-proposal, ber-wp2b3-owner-decision-chain, ber-wsl2-stage-a-setup-proposal
the shell-history filename                                  0    --
the -Filter '*ledger*' command shape           0    --
the searched local drive-root list                  0    --
```
**My numbers reproduce the Lead's exactly**: the username and the WSL path are already in tracked files (4, 5, 2, 6), while the shell-history filename and the drive-enumeration command shape were in **zero** tracked files.

And in the published derivative:

```text
the shell-history filename            occurrences: 0     (2 in the archive source)
the -Filter ledger shape   occurrences: 0     (1 in the source)
the searched local drive-root list occurrences: 0    (1 in the source)
the Get-Item WSL-UNC-root form    occurrences: 0
```
**Exactly the two new identifiers are gone, and nothing else was touched.** The pre-existing identifiers were **not** altered: the S2 row still reads the full WSL path with the username and the distro-side directory name, and the diff shows that line unchanged. The two removals are done by re-wording, not by deleting findings:

```text
- the S5 row's shell-history filename  ->  "the distro's interactive shell-history file"
- the Get-Item history-size command     ->  "(the distro's interactive shell-history file, sized)"
- the Get-ChildItem drive-enumeration command with its explicit root list
                                        ->  "A recursive name-and-content search across the local
                                            bulk-storage roots and the distro home, for any ledger file"
```
**Evidentiary substance survives**: `1,719` files, the 16-byte history size, the "no live provider command ever recorded" finding, the ledger-schema-only result, and both ceilings all remain.

**The derivative's own self-digest was recomputed, not left stale**:

```text
stated     : 3a4d32645e0e2189ccef64fa0cfc3518e88884d18087ba2f0d7ca29d35d1b148
recomputed : 3a4d32645e0e2189ccef64fa0cfc3518e88884d18087ba2f0d7ca29d35d1b148   MATCH
differs from the original's footer f5a6b9ca66c99dd8baa61018fb60974a08ab92efcffce3583285ca6cd97b8b97: True
```
**PASS.** A derivative that removed identifiers while keeping its source's self-digest footer would have been a falsified integrity claim; the footer was recomputed over the new bytes, so the copy's own claim is true of the copy.

---

## 4. The superseding section-13 entry

```text
git log -1 --format=%s 95351dda
docs: supersede one word of the publication entry - the fourth file is a sanitized derivative

the new entry, at head L4228-L4251:
  L4228  ### 2026-10-13 — the publication entry above is corrected on one word: the fourth published file is a sanitized derivative, not a byte-identical copy
  L4231  - **Addresses:** the entry directly above (L4192–L4226, "2026-10-13 — the workspace-archive citations in the O-F1
  L4232    note are superseded by published, in-repo evidence"), and in particular its sentence that the three cited
  L4233    records "and the FU-3 execution record they rest on — are published, byte-identical".
  L4236  - **Correction:** the four files are published as **three byte-identical copies and one sanitized derivative**.
  L4237    BER-G3-FU3-EXECUTION.md is a **SANITIZED DERIVATIVE** (25,606 -> 26,345 bytes): two identifiers that
  L4238    appeared in no tracked file at this lane's base revision — a shell-history artefact's filename and a
  L4239    drive-enumeration command's root list — were removed ... and three published claims inside that copy
  L4240    were corrected (an impossible worst-case figure, a Test-Path result stated as proof of historical
  L4241    absence, and the copy's own self-digest footer, recomputed over the derivative). **The other three
  L4242    copies remain byte-identical to their archive sources and were not altered.**
  L4244  - **Evidence:** [the publication record's section 1.1](../evidence/fu3-record-publication-2026-10-13/README.md#11-the-sanitized-derivative-every-difference-from-its-source-and-why)
  L4246    ... The unsanitized original remains in the session workspace archive at
  L4247    _resume-2026-10-09/evidence/docs-refresh-2026-10-12/BER-G3-FU3-EXECUTION.md
  L4248    (sha256 ea521f84c4d0d88f8e888f3588147a6a63c659f8773f7d41339d9eeca47b9915), which is **not retrievable from this repository**.
  L4251  - **Scope:** ... **New authority: None.**
```

**Names its predecessor by heading AND line range** — it cites "the entry directly above (L4192–L4226, '2026-10-13 — the workspace-archive citations in the O-F1 note are superseded by published, in-repo evidence')" and quotes the exact sentence it corrects. I verified that the cited range is the right one: the predecessor entry's heading is at head L4192 and the new entry begins at L4228, so L4192–L4226 spans it with the blank separator at L4227. **PASS.**

**States the three copies remain byte-identical** — L4242-L4243, in the entry's own words. I verified it independently: three blobs equal their archive sources, the fourth does not and is labelled a derivative. **PASS.**

**Its section-1.1 anchor resolves.** The entry links `README.md#11-the-sanitized-derivative-every-difference-from-its-source-and-why`; the record's heading is `### 1.1 The sanitized derivative: every difference from its source, and why` at L89. I did not judge the fragment by eye — the repository's own checker resolved it:

```text
python -P scripts/ci/check-markdown-links.py docs/README.md docs/evidence/README.md \
  docs/evidence/fu3-record-publication-2026-10-13/README.md docs/roadmaps/behavioral-eval-runner-backlog.md
files: 4   links checked: 199   anchors checked: 33   broken: 0   dead: 0   external-skipped: 81   other-skipped: 0
exit 0
```
**PASS** — a dead anchor would have shown as a non-zero exit and a DEAD line; neither appears. (Stage C resolved the fragment through the repository's slugify rather than guessing, and the checker confirms the guess was right: the heading's code-free text slugs to a run of hyphens exactly as written.)

**The log diff is insert-only.** 

```text
git diff -U0 dbe2ee28 95351dda -- docs/roadmaps/behavioral-eval-runner-backlog.md
  hunks: ['@@ -4191,0 +4192,60 @@ itself is a separate, later host phase that runs only under the merged grant.']
  additions (including blank lines): 60 ; deletions: 0
```
**ONE hunk, 60 added, 0 deleted** — exactly as required, and the appended total is the round-1 entry (35) plus the round-4 superseding entry (25).

---

## 5. Invariants that must not have moved

**The three untouched copies are still byte-identical committed blobs to their archive sources:**

```text
FU3-RECORD-FINAL-REVIEW-F.md   blob == source: True   c0b0c548fa6b8f2cc9b961814099e8e12e690729bfdaa16e6c4b96263d7dab8a
FU3-RECORD-stage-g-summary.md  blob == source: True   d2ed1cfba306c12d993b5718b1d903de656409f1ff91af2e90c3ee1b178aa031
REVIEWPATH-FINAL-REVIEW-F.md   blob == source: True   f367d36eda52c45289dee5d2cbdcde82c534db8c97786d23b78d51531491cd55
the fourth is NOT byte-identical, and is labelled a SANITIZED DERIVATIVE in both the table and the log
```

**The frozen O-F1 note is untouched and the log is append-only:**

```text
base index 4148 ; head index 4148
42-line block sha256 = f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d
equals the bound digest: True ; byte-identical base vs head: True
```

**Cumulative deletions are still exactly three, and all three are count lines:**

```text
git diff -U0 dbe2ee28 95351dda   -> deleted lines: 3
   '-- [Evidence reading guide](evidence/README.md): routes to 16 dated decision and'
   '-This index helps maintainers and reviewing agents find **16 selected decision'
   '-page has been reviewed or that these 16 pages cover the full repository.'
all contain '16': True
```
*A method note worth recording:* my first count returned 2 because a PowerShell filter of `^-[^-]` silently excludes the `docs/README.md` line, whose content itself begins with `- ` (the diff renders it as `-- [Evidence...`). Counting diff deletions by line-prefix regex is a trap; the count above uses "starts with `-` and is not `---`", which is correct. I report the corrected number and the reason, so the earlier 2 is not mistaken for a finding.

---

## 6. The carried-over bound-field hash — confirm the hash, and do NOT re-bind the body

```text
live body: updated_at 2026-10-13T19:27:19Z ; 58,463 bytes as fetched
  sha256 52218969fa7b1bb38fe886d5e90a628a338f677c5852e900ebdf22b52b1de634
three whole-line sentinel pairs: skills L119, security L194, witness L205
collapsed lengths: witness 1468, skills 36007, security 45 ; joined 37522
bound-field first-16 = 9114b83bcfbd2cdb
full                 = 9114b83bcfbd2cdb680646abca86fa85fd5a0a0e9d07fab8206eaac37ea10883
matches the Lead's figure: True
security answer: No
```

**The hash is confirmed independently** — recomputed from the live body's three payloads under the published method (whole-line sentinels, whitespace collapsed, joined witness → skills → security, sha256 over UTF-8, first 16 hex).

**And I state the trap explicitly, because a carried-over hash value is not evidence that the body is unchanged.** The hash is a function of **three fields only**; it is not a digest of the body artifact. Measured on this revision:

```text
body total bytes            58,463
bytes INSIDE the 3 fields   37,714   <- the only bytes the hash covers (collapsed to 37,522 chars)
bytes OUTSIDE the 3 fields  20,749   <- 36% of the body, NOT covered by the hash at all
```
Those 20,749 bytes can be rewritten, and the published figure will not move. So the correct reading of "the hash did not change" is precisely and only: *the three bound fields did not change*. Everything else in the body must be **re-verified by reading it** — checked against the head, the file set and its own claims — and must **not** be re-bound to the previous value on the strength of the hash matching. I re-read the body at this revision for this audit rather than assuming it from round 3, and the fields it does bind are the ones I recomputed above.

---

## 7. Observations — stated, not defects

**OBS-1 (LOW) — the retained text's stated length does not name its counting convention.** The record says the finding text is "913 characters". Measured three ways:

```text
Unicode code points : 911
UTF-16 code units   : 913   <- reproduces the stated figure (two astral emoji count as two units each)
UTF-8 bytes         : 918
```
So the figure is **true under UTF-16 semantics** (what PowerShell's `.Length` reports) and false under Unicode code points, and the record does not say which it means. The **digest is unaffected and recomputes exactly**, which is why this is LOW and not a correctness finding. The repository has a rule that a published figure names its method; naming "913 UTF-16 code units" (or restating it as 911 characters) would close it. I do not repair it.

**OBS-2 (INFO) — the record now carries three different digest conventions side by side.** Section 1's columns are plain whole-file digests; the three byte-identical copies' self-digest footers use the placeholder convention; the derivative's footer was recomputed under that same convention; and file 4's own body digest uses a byte-boundary convention. The record states each one where it is used, and I verified each under its stated convention — noting it here because a reader who applies one convention to all five figures will get four apparent mismatches.

**OBS-3 (INFO, method) — the deletion-count trap.** Recorded in section 5 so a later auditor counting diff deletions with a line-prefix regex does not repeat my two-line undercount.

---

## 8. Stage D ROUND-4 skills usage (authored here; to be published verbatim by the publisher)

**Copy-ready rows** — bound to the FINAL audited head `95351dda27210f4b5707aa067cd138bf37710bd5`, per L694:

```text
| `code-reviewer` | Stage D round 4 / `of1-stage-d` | Re-applied its five-pass review to the round-4 diff and tested each of the five Codex P2 fixes against its own artifact: recomputed the worst-case budget by hand (200 x $0.79 = $158.00, the $158.79 path gone); recomputed all four committed-side digests from the committed blobs; re-hashed the retained finding text over its quoted characters; read the historical-absence paragraph as a scoped current-state statement; and re-derived the sanitization basis by counting tracked files containing each identifier at the base revision | verdict `SD-D: ACCEPT`: all five fixes are genuinely correct, not merely present; the sanitization basis reproduces the Lead's numbers exactly (username 4 files, WSL path 5, the home root 2, the distro-side directory name 6; the shell-history filename and the drive-enumeration shape 0) and exactly those two identifiers are gone while pre-existing ones are unaltered and the substantive findings survive; the derivative's self-digest footer was recomputed and verifies; the superseding entry names its predecessor by heading and line range, keeps the three copies byte-identical and its section-1.1 anchor resolves (checker: 0 broken, 0 dead); the log diff is one hunk, 60 added, 0 deleted; the frozen note still hashes to f29decc7...182d; cumulative deletions still 3, all count lines. One LOW observation: the retained text's "913 characters" is a UTF-16 count (911 code points), method unnamed; the digest is unaffected. Recorded in `AUDIT-D-round4.md` |
| `skill-usage-ledger` | Stage D round 4 / `of1-stage-d` | Emitted this round's six-field usage records, resolving each name against `tools/skills-manifest.json` at the audited base and copying each digest from the manifest rather than remembering it | both names resolve and both digests recompute from `.claude/skills/<name>/SKILL.md` with CRLF-to-LF normalisation: `code-reviewer` = `6238b67b7b90fcbb26fcc45300562efa9e290a9d3870548e37bedaabbc76449a`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4`; manifest `tools/skills-manifest.json` sha256 `9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832`; the ledger is in section 8 of `AUDIT-D-round4.md` |
```

**Row source records** — for insertion inside the existing skills bound field, after the table:

```text
<!-- Row source: agent=of1-stage-d; stage=D; round=4; row=SDD4-1; target=95351dda27210f4b5707aa067cd138bf37710bd5 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/AUDIT-D-round4.md section 8 fenced block row 1 (the exact bytes hashed); binding=sha256 54c0eb2792c897ded1fdd55ad29b3023c3756a51e561d1cf4635b969db369626 over the fenced block's UTF-8 bytes including the final newline (the two Stage D round-4 row lines joined by LF plus one trailing LF, 2225 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=none. -->
<!-- Row source: agent=of1-stage-d; stage=D; round=4; row=SDD4-2; target=95351dda27210f4b5707aa067cd138bf37710bd5 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/AUDIT-D-round4.md section 8 fenced block row 2 (the exact bytes hashed); binding=sha256 54c0eb2792c897ded1fdd55ad29b3023c3756a51e561d1cf4635b969db369626 over the fenced block's UTF-8 bytes including the final newline (the two Stage D round-4 row lines joined by LF plus one trailing LF, 2225 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=none. -->
```

**Captured row-block digest — computed from these exact bytes:**
sha256 `54c0eb2792c897ded1fdd55ad29b3023c3756a51e561d1cf4635b969db369626` over the two row lines joined by LF plus one trailing LF (`2225` bytes), re-derived from the written file after sealing.

**Six-field ledger** (`skill@<manifest-sha256[:12]> / reason / applied / result / incomplete / by`):

```text
code-reviewer@6238b67b7b90 / reason: a Stage D round must test each repair against the artifact it describes and against a stated basis re-derived independently, not against the repairer's account / applied: recomputed the budget arithmetic by hand, recomputed all four committed-side digests from the committed blobs, re-hashed the retained finding text under both trailing-newline conventions, read the historical-absence paragraph, and re-derived the sanitization basis by counting tracked files per identifier at the base revision / result: SD-D ACCEPT with no correctness defect; the two new identifiers are gone while the pre-existing ones are unaltered; the derivative footer recomputes to 3a4d3264...; the finding digest recomputes to be0e3aab... exactly; the superseding entry names its predecessor by heading and line range and its anchor resolves; log diff one hunk 60 added 0 deleted; frozen note f29decc7...182d; cumulative deletions 3, all count lines; one LOW observation on the unnamed counting convention behind "913 characters" / incomplete: Stages E, F and G and the merge receipt are not mine to run; the body's bound-field hash will change again when these rows are inserted and Stage F must hash the body as it then stands / by: of1-stage-d, Stage D, round 4
skill-usage-ledger@6a27b5c8e690 / reason: the workflow requires each stage round to record which skills it read, bound to the manifest hash so the exact instructions are pinned / applied: authored the two rows above and this ledger, resolving both names in tools/skills-manifest.json and recomputing both digests from .claude/skills/<name>/SKILL.md with CRLF-to-LF normalisation / result: both resolve and both recompute exactly - code-reviewer 6238b67b7b90fcbb26fcc45300562efa9e290a9d3870548e37bedaabbc76449a, skill-usage-ledger 6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4; manifest sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832 / incomplete: None / by: of1-stage-d, Stage D, round 4
```

**Limits.** This round read no other Aegis skill; `reviewable-diff-discipline` was refused as `MANUAL-ONLY` and unnamed by a human. Per L720–L721 these rows preclaim no other stage's verdict and embed no digest of themselves and no eventual body hash. Rounds 1–3 remain on disk unchanged.

---

## 9. Not verified, and the limits of this round

- **The five findings' original wording** comes from the Lead's brief and the commit message; I verified the **fixes** against the repository, not the reviewer's text, except for finding `4261109123`, whose retained text I re-hashed.
- **The unsanitized original** is in the untracked archive and is not retrievable from the repository, by design; I compared the derivative against it read-only and state the source-side digest the record publishes.
- **The archive file count** remains method- and time-dependent; no criterion binds it.
- **The bound-field hash binds the three fields only.** This is stated at length in section 6 because it is the trap this round turns on; the body's `20,749` uncovered bytes must be re-read at each revision, and I did so at this one.
- **AC4 corpus-wide link check** was not re-derived: the pages this round touched are covered by the AC3 run above with 0 broken and 0 dead.
- **Not reviewed:** the internal prose of the three byte-identical copies (verbatim by design), and hosted CI beyond the `gh pr checks` conclusions.
- **Environment limit, disclosed:** this host's sandbox blocks MSYS `sh.exe`, so the local-path clone route cannot run `git-upload-pack`; I clone over HTTPS and run `gh` directly. Python subprocess capture worked normally.

---

## 10. Timing

| | |
| --- | --- |
| **Item** | `Workspace-citation durability — Stage D ROUND 4` |
| **Start** | `2026-10-13T12:28:10-07:00` (America/Los_Angeles) — the stamp sampled at this item's first action |
| **ETA at start** | **not stated** in the brief, so no ETA-versus-actual comparison is claimed as met |
| **Finish** | `2026-10-13T12:31:52-07:00` — sampled in the same program run that performed this file's final write |
| **Measured wall time** | `3 minutes (222 seconds)` |
| **Active time** | **not separately instrumented**, so the comparison is **IMPERFECT and labelled as such**; no dependency blocked this round, so wall time is a closer approximation to active work than in rounds 1–3 — but it is still not an active-time measurement. |

---

## 11. Summary

| Check | Result |
| --- | --- |
| P2 4262995856 — budget arithmetic | **PASS** — 200 x $0.79 = $158.00 recomputed by hand; $158.79 absent |
| P2 4262995828 — source-side + committed-side digests | **PASS** — all four committed-side values reproduce from the blobs |
| P2 4262995838 — retained finding text + digest | **PASS** — be0e3aab... recomputes over the 7-line quoted text |
| P2 4262995850 — historical absence restated | **PASS** — current-state observation, historical existence UNKNOWN |
| P2 4262995845 — sanitized derivative | **PASS** — basis re-derived; exactly two identifiers removed; nothing pre-existing altered; substance intact; footer recomputed |
| Superseding entry — names predecessor, 3 copies identical, anchor resolves | **PASS** — heading + L4192–L4226; checker 0 broken / 0 dead |
| Log diff insert-only | **PASS** — one hunk, 60 added, 0 deleted |
| Frozen O-F1 note | **PASS** — `f29decc7...182d`, byte-identical |
| Cumulative deletions | **PASS** — exactly 3, all count lines |
| Bound-field hash, and the carried-over-hash trap | **PASS** — `9114b83bcfbd2cdb` confirmed; 20,749 body bytes are NOT covered by it, so the body is re-verified, not re-bound |
| Defects | **none** (one LOW observation, OBS-1) |

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes including the final newline. Line endings are LF only. -->
sha256: 29f31230441f8daa66fd314ece158a694d3f5fe7afc700c75b636aadf4b5a07d
