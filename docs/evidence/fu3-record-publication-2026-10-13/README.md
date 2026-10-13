# FU-3 record publication — 2026-10-13

**What this page is.** The publication record for four Behavioral Eval Runner (BER) FU-3
record-lane evidence files that this repository's append-only governance log cites, and that
until now existed only inside the session workspace archive. The four files are published in this
directory: **three byte-identically**, and **one as an explicitly labelled sanitized derivative** whose
difference is enumerated in section 1.1. This page records their digests, the citations the
copies make retrievable, every archive path a tracked record still cites with its disposition,
and the citation-durability rule that keeps this defect from recurring.

**Why it exists.** The automated reviewer raised finding `4261109123` — *in plain words, one
inline P2 finding posted by the repository's automated reviewer, Codex* — against
`docs/roadmaps/behavioral-eval-runner-backlog.md` line 4162, asking for "a retained capture with
an immutable revision or digest and locator". The finding is **true**, and the repository-wide
scope is wider than the three files it names.

**The finding this page answers, retained rather than merely cited.** Citing a mutable comment URL is the
failure mode this change exists to remove, so the finding is retained here with a digest and a locator, and
the locator's own limit is stated: a pull-request comment can be edited or deleted, so the **digest**, not the
URL, is what pins the text.

- **Locator:** pull request #765 review comment `4261109123`, on `docs/roadmaps/behavioral-eval-runner-backlog.md` line 4162, written against commit `e0a026e2...`:
  [discussion_r4261109123](https://github.com/ModernNomad-98/Project-Aegis/pull/765#discussion_r4261109123).
- **Digest of the retained text below:** sha256 `be0e3aab224a7384c0aedb734c3d1bffa65407b836b6b0a0dfa257bcdb266ecb` over its 913 characters, UTF-8, no trailing newline added.
- **Retained verbatim:**

```text
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Publish the evidence cited by the permanent log**

A target-tree and workspace-wide basename search finds none of the three `_resume-2026-10-09/...` files cited here, so a fresh checkout cannot inspect the Stage F/Stage G records or the claimed F-F1 precedent. The later bare comment IDs do not preserve those cited sections as immutable evidence; the workflow itself requires a retrievable fixed source rather than a mutable comment ID or unretained string. Publish a retained capture with an immutable revision or digest and locator, or explicitly mark these claims unavailable instead of presenting the missing files as auditable support.

AGENTS.md reference: [AGENTS.md:L49-L54](https://github.com/ModernNomad-98/Project-Aegis/blob/e0a026e2843e299d02180d31d7202a3598759a94/AGENTS.md#L49-L54)

Useful? React with 👍 / 👎.
```


**The defect is durability, not accuracy.** The citations were correct: the sections they name
really do sit at the lines they name (section 2 re-states each anchor). What failed was
**retrievability** — the archive directory sits outside every Git repository on this host, so no
clone, no fresh checkout and no future contributor could read the evidence. Editing or deleting
an accurate citation would destroy a true record, and the log's own rule forbids it, so the
correction is a publication plus a **superseding** log entry that names the entry it supersedes.

**Reading key.** A *finding* is a defect raised by an automated or human reviewer on a pull
request. *FU-3* — in plain words, *the Behavioral Eval Runner provider-usage reconciliation
attempt whose record lane merged as pull request #764*. *O-F1* — in plain words, *the carried
defect under which that lane's merged pull-request body published a skills table with no row for Stages D, E or F*.
The original shorthand for its cause - "no stage read a skill" - is **wrong as to Stage F**: the published Stage F
record lists three skills it used (`code-reviewer`, `acceptance-criteria-reviewer`, `source-of-truth-reconciler`) in
its section 11, `FU3-RECORD-FINAL-REVIEW-F.md` L214-L220. The missing rows were caused by those recorded rows **never
being inserted into the body**, not by an absence of skill use. The shorthand is corrected here, and a further
superseding entry carries the same correction into the append-only governance log.
The *archive* — in plain words, *the untracked
session workspace folder `_resume-2026-10-09/`, which is outside every repository on this host*.
A *self-digest footer* — in plain words, *the repository convention where a line reading
`sha256: <64 hex>` covers the file's bytes with that digest replaced by the literal placeholder
`{{SHA256}}`, UTF-8, LF, final newline included*. The *body digest* — in plain words, *the same
idea applied to every byte above a named footer heading instead of to the whole file*.

## 1. The four published files, and the one that is not verbatim

**Three of the four copies are byte-identical to their archive source. The fourth is a labelled sanitized
derivative**, and section 1.1 enumerates every difference. For each file the table gives BOTH sides: the
**source-side** digest, measured from the archive original when the copy was taken, and the **committed-side**
digest a fresh clone reproduces. Recording both is what makes the equality - or the enumerated difference -
checkable by a reader who does not have the archive.

| # | Published file | Status | Source bytes → committed | Source sha256 (archive original) | Committed sha256 (fresh clone) |
| --- | --- | --- | ---: | --- | --- |
| 1 | [BER-G3-FU3-EXECUTION.md](BER-G3-FU3-EXECUTION.md) | **SANITIZED DERIVATIVE** - see 1.1 | 25,606 → 27,721 | `ea521f84c4d0d88f8e888f3588147a6a63c659f8773f7d41339d9eeca47b9915` | `89005849d1d2ea5d7b12d9a13b0ff8f87973a103bf0f387f85c2b673fdf30ae0` |
| 2 | [FU3-RECORD-FINAL-REVIEW-F.md](FU3-RECORD-FINAL-REVIEW-F.md) | byte-identical | 30,777 → 30,777 | `c0b0c548fa6b8f2cc9b961814099e8e12e690729bfdaa16e6c4b96263d7dab8a` | `c0b0c548fa6b8f2cc9b961814099e8e12e690729bfdaa16e6c4b96263d7dab8a` |
| 3 | [FU3-RECORD-stage-g-summary.md](FU3-RECORD-stage-g-summary.md) | byte-identical | 25,454 → 25,454 | `d2ed1cfba306c12d993b5718b1d903de656409f1ff91af2e90c3ee1b178aa031` | `d2ed1cfba306c12d993b5718b1d903de656409f1ff91af2e90c3ee1b178aa031` |
| 4 | [REVIEWPATH-FINAL-REVIEW-F.md](REVIEWPATH-FINAL-REVIEW-F.md) | byte-identical | 21,023 → 21,023 | `f367d36eda52c45289dee5d2cbdcde82c534db8c97786d23b78d51531491cd55` | `f367d36eda52c45289dee5d2cbdcde82c534db8c97786d23b78d51531491cd55` |

**Each file's own integrity claim, recomputed from the published bytes:** file 1's self-digest footer is now
`9038e3e6…` (the full 64-hex value is stated in that file's own footer; it was recomputed over the derivative **three times** as it was
`f5a6b9ca66c99dd8baa61018fb60974a08ab92efcffce3583285ca6cd97b8b97` in the archive original and `3a4d3264…` after the first
revised - leaving the original's value would have made the published file carry a false claim); file 2's footer is
`059822aabffb13cb417adcd1714bb00a90244c0df040a457db7ba9ac895bb2d7`; file 4 carries a body digest,
`81884e0d49cb117c7f7884350ce23adcfac6788891c0a9bc8828dc19461abcc8`, over every byte above its footer heading.

**All four are LF-only** (zero CRLF byte pairs) and the repository root `.gitattributes` is `* text=auto eol=lf`.
For the three byte-identical copies the committed bytes therefore equal the archive bytes and every digest above
is reproducible from a clone alone; for the derivative, the committed-side digest is the one the clone reproduces,
and the source-side digest identifies the original it was derived from.

**Three copies were edited in no way at all.** No re-wrap, no trailing-whitespace fix, no link rewrite, no
re-encoding - a single changed byte in any of them would falsify both the self-digest and this page's whole-file
digest. Their internal citations to further out-of-tree artifacts are part of the frozen archival text and are
deliberately left as they are; the rule in section 4 binds new citations and the citations superseded by this
publication, not the archival body of a dated record.

### 1.1 The sanitized derivative: every difference from its source, and why

`BER-G3-FU3-EXECUTION.md` is **not** a verbatim copy. **Seven changes** were made, all named here: three are privacy
sanitizations, three are corrections of claims the published text got wrong, and one is the record's own integrity
footer. Nothing else differs.

| # | Location | Change | Why |
| --- | --- | --- | --- |
| 1 | the search-census row for the shell history | the shell-history artefact's filename is removed; the row now reads "the distro's interactive shell-history file" | the filename appears in **no tracked file at the base revision**, and the governing evidence-retention rule (backlog L4021-L4025: *no private identifiers in Git*) requires it out. The **substance is preserved**: the history was 16 bytes and no live provider command was recorded |
| 2 | the verification command that enumerated the bulk-storage roots | the command is replaced by a prose statement of the same search and the same result | the command's host-specific root list appears in **no tracked file at the base revision**; its substance - a recursive name-and-content search that found only the schema and never the data - is preserved |
| 3 | the verification command that sized the shell history | replaced by "the distro's interactive shell-history file, sized", with the same 16-byte result | same reason as 1 |
| 4 | five sites: the search-census row for the distro root, the 2.2 opening, the quoted stop record, the searched-roots list, and the enumeration command | **every occurrence of the host identity is removed** - the username, the distro release, the `wsl$` root and the project directory name - replaced by "the external distro-private evidence root on the WSL2 Linux distro (raw host path withheld)" | the evidence-retention rule this record's own lane is governed by says flatly *no private identifiers in Git*, and the raw host paths and users belong in the separately approved external root. **The Lead first ruled these identifiers could stay because they are already tracked at the base revision; Codex showed that prior publication is not an exception to the rule, and that the ruling was wrong twice over - see the note below. The ruling was overturned.** |
| 5 | the sentence about the authorized external evidence root | "No provider execution evidence was ever placed at the authorized root" becomes a **current-state** statement: the directory was not present when searched, and its **historical existence is UNKNOWN** | a `Test-Path` result cannot prove a historical absence, and this record's own governing packet says missing old evidence does not prove zero use |
| 6 | the worst-case arithmetic block | corrected to **200 charged judgment attempts plus at most one read-only metadata request = $158.00**; the previous "$158.79" implied 201 charged attempts, an impossible path | the approved maxima are 200 judgment attempts + 1 metadata availability request, and that request invokes no generation and submits no calibration content, so the attempt charge does not apply to it |
| 7 | the record's own self-digest footer | rewritten from `f5a6b9ca…` (the archive original's value) to `9038e3e6…` over the current derivative | the footer is the file's own integrity claim; leaving the original's value would have published a file carrying a **false** claim, which is the defect class this lane exists to remove. Recomputing it was correct - and the change belongs in this inventory rather than being left implicit |

**A ruling of the Lead's was overturned here, and it is recorded rather than quietly rewritten.** The first version of
this section said the host identifiers could stay because they are *already published at the base revision* - the username
in 4 tracked files, the distro release in 5, the root in 2. **That reasoning was wrong twice over.** First, the repository's
own evidence-retention rule is a blanket *no private identifiers in Git*; prior publication is not an exception to it.
Second, and decisively: **this publication directory does not exist at the base revision, so nothing inside it was
"already published"** - every occurrence in this new file is new to Git no matter what appears elsewhere in the repository.
The base-relative test answered a narrower question than the rule asks. The Lead withdrew the ruling, the identifiers are
removed at all five sites (item 4 above), and the original with them intact is retained only at its digest-pinned
external locator below.

**Where the unsanitized original is retained, and the plain limit.** The original remains at
`_resume-2026-10-09/evidence/docs-refresh-2026-10-12/BER-G3-FU3-EXECUTION.md`, 25,606 bytes, whole-file sha256
`ea521f84c4d0d88f8e888f3588147a6a63c659f8773f7d41339d9eeca47b9915` - *in plain words, the untracked session workspace archive*.
**That original is NOT retrievable from this repository.** The digest identifies it; it does not make it fetchable,
and nothing here should be read as claiming otherwise.

## 2. The citations these copies make retrievable

| Cited by | What the citation supports | Where it now resolves |
| --- | --- | --- |
| backlog line 4143 | the FU-3 execution record, "whose section 6 carries the stop verbatim" | [BER-G3-FU3-EXECUTION.md](BER-G3-FU3-EXECUTION.md) — section 6, "THE STOP RECORD (verbatim)", at L208 |
| backlog line 4160 (inside the frozen O-F1 note) | that Stage F raised the carried item and left the body unedited, in its section 10 | [FU3-RECORD-FINAL-REVIEW-F.md](FU3-RECORD-FINAL-REVIEW-F.md) — section 10, "O-F1 and two smaller notes", at L202 |
| backlog line 4162 (inside the frozen O-F1 note) | that Stage G recorded it as an open publication item, in its section 9 | [FU3-RECORD-stage-g-summary.md](FU3-RECORD-stage-g-summary.md) — section 9, at L176 |
| backlog line 4165 (inside the frozen O-F1 note) | the `F-F1` precedent | [REVIEWPATH-FINAL-REVIEW-F.md](REVIEWPATH-FINAL-REVIEW-F.md) — the `F-F1` paragraph at L68 |
| `docs/approvals/APPROVAL_REGISTER.md` line 5964 | the same execution record, as the entry's evidence | BER-G3-FU3-EXECUTION.md in this directory |

"Backlog" above is [the Behavioral Eval Runner backlog](../../roadmaps/behavioral-eval-runner-backlog.md).
The frozen note itself is **not edited** by this publication: it is bound to the digest under
which the merge of pull request #765 was recorded, and the correction is an appended entry in
the section 13 governance log that names the entry it supersedes.

## 3. Every archive path the pre-change records cite, and its disposition

Ten citation occurrences across the **four pre-change tracked records** - the four files that cited the
archive at the base revision this change is against - name **nine distinct** archive paths. Four are
published here; **five are owed** and are named in section 6 rather than dropped.

**Scope of this census, stated because the heading promises it.** The census was taken over the tracked
tree at the base revision, **before** this change. The re-publications in this directory (three byte-identical
copies and one sanitized derivative, section 1.1) are archival records in their own right - the derivative's
enumerated differences touch none of the references counted here - and they carry their own
out-of-tree references internally - for example the two source-archive paths inside
`BER-G3-FU3-EXECUTION.md` at L116-L117, and a row-source locator inside
`FU3-RECORD-FINAL-REVIEW-F.md` at L222. Those internal references are **not** counted above and are
**not** repaired by this change: rewriting them would falsify the copies' own integrity claims (section 1),
and widening the census to include them would breach this change's audited scope.

| # | Archive path cited | Cited in | Disposition |
| --- | --- | --- | --- |
| 1 | `_resume-2026-10-09/evidence/docs-refresh-2026-10-12/BER-G3-FU3-EXECUTION.md` | backlog line 4143; `APPROVAL_REGISTER.md` line 5964 | **PUBLISHED** → `docs/evidence/fu3-record-publication-2026-10-13/BER-G3-FU3-EXECUTION.md` |
| 2 | `_resume-2026-10-09/evidence/docs-refresh-2026-10-12/FU3-RECORD-FINAL-REVIEW-F.md` | backlog line 4160 | **PUBLISHED** → `docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-FINAL-REVIEW-F.md` |
| 3 | `_resume-2026-10-09/evidence/docs-refresh-2026-10-12/FU3-RECORD-stage-g-summary.md` | backlog line 4162 | **PUBLISHED** → `docs/evidence/fu3-record-publication-2026-10-13/FU3-RECORD-stage-g-summary.md` |
| 4 | `_resume-2026-10-09/evidence/docs-refresh-2026-10-12/REVIEWPATH-FINAL-REVIEW-F.md` | backlog line 4165 | **PUBLISHED** → `docs/evidence/fu3-record-publication-2026-10-13/REVIEWPATH-FINAL-REVIEW-F.md` |
| 5 | `_resume-2026-10-09/evidence/p0/P0A-A1-PLAN.md` | `aegis-ci-baseline-2026-10-11.md` line 43 | **OWED** |
| 6 | `_resume-2026-10-09/evidence/p0/P0A-A1-AUDIT-B.md` | `aegis-ci-baseline-2026-10-11.md` line 45 | **OWED** |
| 7 | `_resume-2026-10-09/evidence/p0/F0-source-authority-reconciliation.md` | `aegis-ci-baseline-2026-10-11.md` line 49 | **OWED** |
| 8 | `_resume-2026-10-09\evidence\dirfd-probe-repair\HANDOFF-CORRECTION.md` | `scif-closeout-corrections-2026-10-11.md` line 15 | **OWED** |
| 9 | `_resume-2026-10-09\FAST-CHECKPOINT-2026-10-11D.md` | `scif-closeout-corrections-2026-10-11.md` line 84 | **OWED** |

## 4. The citation-durability rule, stated once and reused

## Citation durability

A permanent record here — a governance log entry, a register entry, a dated evidence page or a roadmap
fact — supports each claim with evidence a fresh checkout can retrieve: a path inside this repository,
written as a Markdown link so the repository's own link checker proves it resolves. Where the artifact
cannot be published (an oversized archive, an external system, a private input), the record carries the
artifact's digest, names the locator it is known by, and says plainly that the artifact is **not
retrievable from this repository**. An out-of-tree path alone is not acceptable support. A digest pins
identity; it never makes an absent artifact retrievable.

This is a documented rule, not a machine-enforced one, and the difference is stated rather than blurred:
the "Run Markdown link checker over the repository's own pages" step of `validate-skills` validates the
links a record **already contains** - it goes red when a written link stops resolving - and it does
**not** require a record to contain a durable citation at all. A record can cite an out-of-tree path as
plain text, or omit its evidence entirely, and that step stays green. Supplying the citation this rule
requires is therefore a **documentation obligation that nothing machine-checks**; the *digest* half is
checked by nothing either, and a record that relies on it says so.
## 5. Credential and secret scan of the published bytes

The four files were scanned before publication for AWS access keys, private-key blocks, GitHub
tokens, ARNs, e-mail addresses, password- and secret-shaped assignments, and bare
12-digit account-shaped numbers. **No credential material is present.** Three broad-pattern hits were
read and dismissed as benign: a provider price line, a GitHub Actions job id inside a CI results
table, and a sha256 value inside a table row. The scan is repeated as an acceptance check at the
candidate head, so the result is a measurement rather than an assurance.

**A privacy and identifier check, added because a secret scan is not a privacy check.** The four files were scanned
for host-specific identifiers under the repository's own rule - *no private identifiers in Git*, backlog L4021-L4025 -
by extracting every path- and artefact-shaped token and testing it against the tracked tree at the base revision.
That check found the shell-history artefact's filename, the drive-enumeration command, **and the host identity itself at
five sites**: a username, a distro release, a `wsl$` root and a project directory name. **All of them are removed**
(section 1.1, items 1 to 4). One argument was tested and rejected: that the last group could stay because the same
identifiers already appear in tracked files. **Prior publication is not an exception to the rule, and the argument fails
on its own terms anyway** - this publication directory does not exist at the base revision, so nothing inside it was
already published. This paragraph exists because the credential scan passed while identifier-shaped content was
present: a scan for secrets does not answer whether an identifier is private.
1 to 3): the shell-history artefact's filename and the drive-enumeration command. Every other host identifier in
the copies, including the distro root and the username inside it, is **already published at the base revision** and
was deliberately left untouched. This paragraph exists because the credential scan passed while identifier-shaped
content was still present: a scan for secrets does not answer whether an identifier is already public, and the
repository's own evidence-retention rule asks a different question.

## 6. Owed, named so it is not forgotten

Publishing four files does not fix the other five cited paths, and this page does not claim it
does. Each owes its correction to a change that edits the citing record under **that record's
own** correction rules — a dated page that declares its earlier texts byte-identical except for
one sanctioned exception, and a roadmap fact bound to the tree `5ad973a2`, are each corrected by
their own procedure, not as a side effect of a publication.

- **OWED-1..5** — the five citing sites in section 3: three in
  `docs/roadmaps/aegis-ci-baseline-2026-10-11.md` (L43, L45, L49) and two in
  `docs/evidence/scif/scif-closeout-corrections-2026-10-11.md` (L15, L84). **Trigger:** the next
  change that edits any of those records carries that record's citation correction.
- **OWED-6** — the two remaining occurrences that cite the *published* path 1 from records this
  change does not edit: backlog line 4143 and `APPROVAL_REGISTER.md` line 5964. The evidence is
  now retrievable; the citing **line** still carries the archive path, and updating it is a
  correction to those records under their own rules. The approval register is a listed
  security-relevant surface and an append-only authority record, so it is deliberately not
  edited for a non-authority reason.
- **OWED-7** — codifying this rule in `AGENTS.md`, `CONTRIBUTING.md` or
  `docs/delivery-workflow.md`. Those are instruction and process texts: editing them is a
  different change class with its own approval path, and it carries a rule-preservation
  obligation. Deliberately separate.
- **OWED-8** — machine enforcement of the **digest** half: a check that fails when a governance
  page cites an out-of-tree path with no digest. It belongs under `scripts/`, which is a
  protected path and would make this a code-bearing change needing its own owner decision and
  merge review. The rule does not depend on the check existing, and the check must not be
  smuggled in to make the rule look enforced.

## 7. How to verify this page

From a clone of the candidate head, with the session workspace archive unavailable:

1. **Digests** — hash each of the four files in this directory with `Get-FileHash -Algorithm SHA256`
   or `sha256sum` and compare against the **committed-side** column in section 1. All four reproduce it.
   The source-side column identifies the archive originals: for the three byte-identical copies the two columns are
   equal, and for the derivative they differ by exactly the changes enumerated in section 1.1.
2. **Self-digests** — for files 1 to 3, replace the 64 hex characters on the line beginning
   `sha256:` with the literal placeholder and hash the UTF-8 bytes including the final newline,
   LF only; for file 4, hash every byte above the whole-line `## SHA-256 footer` heading (L103)
   the same way. All four reproduce the values stated for them in section 1; file 1's footer is over the
   derivative, as section 1.1 records, not over the original.
3. **Retrievability** — read the four files directly from the clone. No step of that path
   requires the archive, and no Markdown link on this page targets it.
4. **The citing entry** — read the newest entry of section 13 of the backlog linked in section 2,
   which names the entry it supersedes and links back to this page.
