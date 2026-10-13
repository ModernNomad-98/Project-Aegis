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
- **Digest of the retained text below:** sha256 `be0e3aab224a7384c0aedb734c3d1bffa65407b836b6b0a0dfa257bcdb266ecb` over its **918 UTF-8 bytes** (911 code points; 913 UTF-16 code units - the earlier label said "913 characters, UTF-8", which was wrong in both number and unit), no trailing newline added.
- **Retained verbatim:**

```text
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Publish the evidence cited by the permanent log**

A target-tree and workspace-wide basename search finds none of the three `_resume-2026-10-09/...` files cited here, so a fresh checkout cannot inspect the Stage F/Stage G records or the claimed F-F1 precedent. The later bare comment IDs do not preserve those cited sections as immutable evidence; the workflow itself requires a retrievable fixed source rather than a mutable comment ID or unretained string. Publish a retained capture with an immutable revision or digest and locator, or explicitly mark these claims unavailable instead of presenting the missing files as auditable support.

AGENTS.md reference: [AGENTS.md:L49-L54](https://github.com/ModernNomad-98/Project-Aegis/blob/e0a026e2843e299d02180d31d7202a3598759a94/AGENTS.md#L49-L54)

Useful? React with 👍 / 👎.
```


**The second finding, retained the same way.** The same review raised a second P2 finding that the log cites by
identifier alone. It is retained here on the same terms, and its own limit is stated the same way: **a pull-request
comment can be edited or deleted, so the digest - not the URL - is what pins the text, and neither makes the comment
retrievable from this repository.**

- **Locator:** pull request #766 review comment `4261109109`, on `docs/roadmaps/behavioral-eval-runner-backlog.md` line 4188,
  written against commit `e0a026e2...`:
  [discussion_r4261109109](https://github.com/ModernNomad-98/Project-Aegis/pull/766#discussion_r4261109109).
- **Digest of the retained text below:** sha256 `e1bf5013fe24913cb9cd4be586d695fc3a2b8fcd491ed939578b54c131f62acc` over its **903
  UTF-8 bytes**, no trailing newline added.
- **Retained verbatim:**

```text
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Do not close a mandatory Stage F failure by logging it**For O-F1, the missing D/E/F rows are themselves part of the `SD-F` acceptance threshold: `docs/delivery-workflow.md:182` requires a row for every stage that ran, and its pure-docs path explicitly requires every defect to be repaired and re-audited. Declaring the omission “discharged by a dated note” therefore records an unsatisfied final-review gate as closed and creates a precedent for carrying mandatory gate failures past merge. Record this as a historical process failure or keep it open; a later log entry cannot substitute for satisfying the canonical workflow.AGENTS.md reference: [AGENTS.md:L65-L70](https://github.com/ModernNomad-98/Project-Aegis/blob/e0a026e2843e299d02180d31d7202a3598759a94/AGENTS.md#L65-L70)Useful? React with 👍 / 👎.
```

**This one is the rule's own violation, caught by the review that found it.** The log carried a bare mutable comment
identifier with no digest, no locator and no availability statement - **the exact failure this change exists to
remove, committed inside the change itself**, and the second such instance (the first, `4261109123`, is retained
above). The repair is the same treatment: the text is retained here with a digest and a locator, the limitation is
stated rather than implied, and **the log entry's citation is corrected in place with that edit disclosed in an
appended entry**, because the entry's text is unmerged and the log's own rule against editing entries protects
**merged** content.
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

**Each file's own integrity claim, recomputed from the committed files rather than copied from this page:**
**file 1**'s self-digest footer is now `9038e3e6…` - its full 64-hex value is stated in that file's own footer, and it was
recomputed over the derivative each time the derivative changed (it was
`f5a6b9ca66c99dd8baa61018fb60974a08ab92efcffce3583285ca6cd97b8b97` in the archive original and `3a4d3264…` after the first
repair round; leaving the original's value would have made the published file carry a false claim). **File 2**'s footer is
`8f554598a04d91567fbb10e301d1a8bc1e0c2940b2a82fb8a5bac4be9258937b` and **file 3**'s is
`059822aabffb13cb417adcd1714bb00a90244c0df040a457db7ba9ac895bb2d7` - **each recomputed from its own file**, which is what
section 7's verification step asks a reader to do. **File 4** carries a body digest,
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

`BER-G3-FU3-EXECUTION.md` is **not** a verbatim copy. **Nine changes** were made, plus **one deliberate non-change**
recorded as item 5 so the inventory is exhaustive: four items are privacy sanitizations and five are corrections of
claims the published text got wrong - **two of which changed what the record concludes**, not merely how it is worded.
Nothing else differs.

| # | Location | Change | Why |
| --- | --- | --- | --- |
| 1 | the search-census row for the shell history | the shell-history artefact's filename is removed; the row now reads "the distro's interactive shell-history file" | the filename appears in **no tracked file at the base revision**, and the governing evidence-retention rule (backlog L4021-L4025: *no private identifiers in Git*) requires it out. The **substance is preserved**: the history was 16 bytes **when inspected**, and what that does and does not establish is stated in item 9 |
| 2 | the verification command that enumerated the bulk-storage roots | the command is replaced by a prose statement of the same search and the same result | the command's host-specific root list appears in **no tracked file at the base revision**; its substance - a recursive name-and-content search that found only the schema and never the data - is preserved |
| 3 | the verification command that sized the shell history | replaced by "the distro's interactive shell-history file, sized", with the same 16-byte result | same reason as 1 |
| 4 | **the private host identity, at four prose and table sites** - the census table's S2 row (original L46 to published L46), the section 2.2 opening (L66 to L69), the quoted stop record (L208 to L228) and the drafted lifecycle entry (L255 to L275). **The same raw path also appears at L330, L333 and L336 inside the three verification commands, which items 2 and 3 replace - seven source lines in total, all sanitized** | **every occurrence of the private host identity is removed** - the username, the distro release, the `wsl$` root and the distro-side directory name - replaced by "the external distro-private evidence root on the WSL2 Linux distro (raw host path withheld)" | the evidence-retention rule this record's own lane is governed by says flatly *no private identifiers in Git*, and the raw host paths and users belong in the separately approved external root. **The Lead first ruled these identifiers could stay because they are already tracked at the base revision; Codex showed that prior publication is not an exception to the rule, and that the ruling was wrong twice over - see the note below. The ruling was overturned.** An earlier revision of this row said *four sites* and named "the searched-roots list" - a site that never existed; the enumeration above replaces it and is checkable line by line |
| 5 | the **session workspace path** `C:\src\Project Aegis`, which appears in the searched-roots enumeration and in the S1 search-census row | **NOT sanitized, deliberately** - `C:\src\Project Aegis` is retained. It is the **project and session workspace path, not private host identity**: the removed tokens were the username, the distro release, the `wsl$` root and the distro-side directory name. Removing it would also delete the record's honest account of *where the search was performed* | it is a project path rather than a user or host identifier, so it is outside the token set item 4 removes; an earlier revision of this row wrongly called it "the searched-roots list" and listed it among the sanitized sites, which made the claim false in two ways, and it is now stated as the deliberate retention it is |
| 6 | the sentence about the authorized external evidence root | "No provider execution evidence was ever placed at the authorized root" becomes a **current-state** statement: the directory was not present when searched, and its **historical existence is UNKNOWN** | a `Test-Path` result cannot prove a historical absence, and this record's own governing packet says missing old evidence does not prove zero use |
| 7 | the worst-case arithmetic block | corrected to **200 charged judgment attempts plus at most one read-only metadata request = $158.00**; the previous "$158.79" implied 201 charged attempts, an impossible path | the approved maxima are 200 judgment attempts + 1 metadata availability request, and that request invokes no generation and submits no calibration content, so the attempt charge does not apply to it |
| 8 | the record's own self-digest footer | rewritten from `f5a6b9ca…` (the archive original's value) to `9038e3e6…` over the current derivative | the footer is the file's own integrity claim; leaving the original's value would have published a file carrying a **false** claim, which is the defect class this lane exists to remove. Recomputing it was correct - and the change belongs in this inventory rather than being left implicit |
| 9 | the shell-history **conclusion**, in the census table's S5 row and in the verification commands | the sentence `no live provider command ever recorded` becomes a **current-state** statement: the history was empty **when inspected**, that is equally consistent with its having been cleared, disabled or bypassed by non-interactive execution, and **whether any live provider command was ever recorded is UNKNOWN** | an effectively empty history file proves only what was true at inspection. The earlier wording inferred a historical fact from a present-tense measurement - the same defect as item 6, in the same copy, and it is enumerated separately because it changes the record's **conclusion** rather than its wording |
| 10 | the **census**, in section 2.2 and in the verification commands | the three top-directory rows sum to **1,915** against a recorded total of **1,719**, and the block now carries an explicit **UNRECONCILED** warning: both numbers are shown, no number was adjusted to make the sum work, and the rows, the total and the dependent 1,455-file scan figure are labelled **unreliable as a set** | this lane cannot re-derive the census - its boundaries forbid touching the WSL distro - so the honest form is a labelled gap rather than a balanced sum. A reader can now check the arithmetic and see that it does not add up, instead of trusting a total |

**A ruling of the Lead's was overturned here, and it is recorded rather than quietly rewritten.** The first version of
this section said the host identifiers could stay because they are *already published at the base revision* - the username
in 4 tracked files, the distro release in 5, the root in 2. **That reasoning was wrong twice over.** First, the repository's
own evidence-retention rule is a blanket *no private identifiers in Git*; prior publication is not an exception to it.
Second, and decisively: **this publication directory does not exist at the base revision, so nothing inside it was
"already published"** - every occurrence in this new file is new to Git no matter what appears elsewhere in the repository.
The base-relative test answered a narrower question than the rule asks. The Lead withdrew the ruling, the identifiers are
removed at the four prose and table sites enumerated in item 4 above, and at the three verification commands items 2 and 3 replace - seven source lines in all - while the session workspace path `C:\src\Project Aegis` alone is **deliberately retained** and named as such in item 5 - the distro-side directory name was **removed** with the other tokens, as item 4 records and as the derivative confirms (it contains no `aegis-stage-a` at all), and the original with them intact is retained only at its digest-pinned
external locator below.

**Where the unsanitized original is retained, and the plain limit.** The original remains at
`_resume-2026-10-09/evidence/docs-refresh-2026-10-12/BER-G3-FU3-EXECUTION.md`, 25,606 bytes, whole-file sha256
`ea521f84c4d0d88f8e888f3588147a6a63c659f8773f7d41339d9eeca47b9915` - *in plain words, the untracked session workspace archive*.
**That original is NOT retrievable from this repository.** The digest identifies it; it does not make it fetchable,
and nothing here should be read as claiming otherwise.

## 2. The citations these copies make retrievable

| Cited by | What the citation supports | Where it now resolves |
| --- | --- | --- |
| backlog line 4143 | the FU-3 execution record, "whose section 6 carries the stop verbatim" | [BER-G3-FU3-EXECUTION.md](BER-G3-FU3-EXECUTION.md) — section 6, "THE STOP RECORD (verbatim)", at L218 |
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
`BER-G3-FU3-EXECUTION.md` at L126-L127, and a row-source locator inside
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

**The rule is prospective, and this is its effective date.** It binds citations **added from this change forward** -
the change that states it, merged `2026-10-13`. It does **not** retroactively invalidate records already merged:
**five archive citations in earlier, merged records remain OWED**, enumerated with their dispositions in section 3 of the
publication record [docs/evidence/fu3-record-publication-2026-10-13/README.md](README.md) and tracked as open items. Those
records neither **violate** this rule nor are **silently excused** by it: they predate it, the work that would publish
their evidence is named and outstanding, and this paragraph exists so a reader can tell the two cases apart. **A rule
stated as a universal invariant while five known sites remain unmet is a false claim about its own scope** - Codex
raised exactly that, and the scope sentence is the repair.

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
12-digit account-shaped numbers. **No credential material is present.** **Four** broad-pattern hits were read and each is
dispositioned in section 5.1: a provider price line (credential-shape, the token-assignment
alternative), a GitHub Actions job id inside a CI results table (account-shape, twelve digits), a
sha256 value inside a table row (account-shape, twelve digits), and the derivative's own recomputed
sha256 footer (account-shape, twelve digits). **The pre-publication scan and the acceptance check
therefore examine the same four lines, which is the point of repeating the scan at the candidate
head.** The scan is repeated as an acceptance check at the
candidate head, so the result is a measurement rather than an assurance.

**A privacy and identifier check, added because a secret scan is not a privacy check.** The four files were scanned
for host-specific identifiers under the repository's own rule - *no private identifiers in Git*, backlog L4021-L4025 -
by extracting every path- and artefact-shaped token and testing it against the tracked tree at the base revision.
That check found the shell-history artefact's filename, the drive-enumeration command, **and the host identity itself at
four sites**: a username, a distro release, a `wsl$` root and the distro-side directory name. **All four are removed**
(section 1.1, items 1 to 4). One argument was tested and rejected: that the last group could stay because the same
identifiers already appear in tracked files. **Prior publication is not an exception to the rule, and the argument fails
on its own terms anyway** - this publication directory does not exist at the base revision, so nothing inside it was
already published. This paragraph exists because the credential scan passed while identifier-shaped content was
present: a scan for secrets does not answer whether an identifier is private.

### 5.1 The acceptance check, stated so it can be reproduced

The credential and account-shape scan is acceptance criterion **AC8**. Its pattern is taken **verbatim** from the
plan at `PLAN.md` L424-L425 and is **not** modified here. Its counting rule is **lines, not matches** - one count per
matching **line** - `Select-String` returns one match object per line that matches, however many hits that line contains:

```text
$pat='AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{20,}|arn:aws|'
$pat+='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}|password *[:=]|secret *[:=]|token *[:=]|[0-9]{12}'
```

Run it over the four published copies in this directory and count matching **lines**. **The measurement at this head
is 4 lines**, and which alternative matched each one is part of the result, because this single criterion bundles a
**credential-shape** scan with an **account-shape** scan:

| # | Line | Which alternative matched | Disposition |
| --- | --- | --- | --- |
| 1 | `BER-G3-FU3-EXECUTION.md` L168 | **credential-shape** - the token-assignment alternative, on the published provider-price line (a per-token rate stated in nano-USD) | read; a published provider price, not a credential |
| 2 | `BER-G3-FU3-EXECUTION.md` L367 | **account-shape** - the twelve-digit alternative, on a run inside the file's **own recomputed sha256 footer** | **accepted false positive**: a substring of a hex digest is not an account number |
| 3 | `FU3-RECORD-FINAL-REVIEW-F.md` L121 | **account-shape** - the twelve-digit alternative, on a GitHub Actions job id inside a CI results table | read; a job id, not an account |
| 4 | `REVIEWPATH-FINAL-REVIEW-F.md` L47 | **account-shape** - the twelve-digit alternative, on a sha256 value inside a table row | read; a digest, not an account |

**Scoping rule, stated so the two numbers are not confused.** The criterion's number is **what the plan's own command prints**, so the command
is printed here and both of its outputs are reported:

```powershell
$files = @('BER-G3-FU3-EXECUTION.md','FU3-RECORD-FINAL-REVIEW-F.md',
           'FU3-RECORD-stage-g-summary.md','REVIEWPATH-FINAL-REVIEW-F.md') |
         ForEach-Object { "docs/evidence/fu3-record-publication-2026-10-13/$_" }
$hits = Select-String -Path $files -Pattern $pat
"hits_on_copies = $($hits.Count)"
$hits | ForEach-Object { "{0}:{1}" -f (Split-Path $_.Path -Leaf), $_.LineNumber }
"hits_on_record = $((Select-String -Path docs/evidence/fu3-record-publication-2026-10-13/README.md -Pattern $pat).Count)"
# the substantive figure: this record's evidentiary prose only. Exclusion rule: the fenced quotation of the
# rule above is NOT a hit, so fenced blocks are stripped before counting.
$fence = '```'
$prose = ((Get-Content -Raw docs/evidence/fu3-record-publication-2026-10-13/README.md) -split ('(?ms)^' + $fence + '.*?^' + $fence)) -join ''
"hits_on_record_substantive = $((($prose -split [char]10) | Select-String -Pattern $pat).Count)"
```

**The command prints `hits_on_copies = 4` and `hits_on_record = 1`.** (The command above reuses the `$pat` set immediately above it.) The single record hit is the pattern text quoted from the plan **in this
very section** - the record states its own scan rule, so it necessarily contains a copy of it, and **the plan itself trips the same pattern at four
of its own sites** (L421, L422, L424, L673) for the same reason. The number is therefore **reported as the command produces it rather than
redefined**, and a second figure is printed beside it - **`hits_on_record_substantive = 0`**, counting this record's **evidentiary prose only**,
with the quotation of the rule excluded.

**Both numbers are printed because a criterion whose stated number is not what its stated command produces is the defect class this lane exists to
remove.** Without the second figure the first would read as an unread credential-shaped string; with it, a reader sees that the one hit is the rule
quoting itself, and that nothing in the record's substance matches the pattern at all.

**The threshold is amended on the record from the plan's 3 to 4**, exactly as AC1 is amended. The plan's own number
**reproduces at 3 for the four byte-identical *source* files** - measured, with the three hits landing at
`BER-G3-FU3-EXECUTION.md` L155, `FU3-RECORD-FINAL-REVIEW-F.md` L121 and `REVIEWPATH-FINAL-REVIEW-F.md` L47, which is
precisely what `PLAN.md` L421 records. The fourth line appears only in the **published** set, because the sanitized
derivative is a new artifact: the plan's prose is registered here as **historical, not amended** - the plan is frozen at
the revision Stage B accepted, so neither its pattern nor its prose is edited, and this record's amended criterion
supersedes L421 **for the four published copies at this head only**.

**The two citations of `PLAN.md` above, and their limit - this change's own rule applied to itself.** Two sentences in
this section rest on the plan: that the pattern is taken **verbatim** from it, and that its own threshold was **three**.
**`PLAN.md` is not in this repository** (`git ls-files` finds no such path), so those claims are recorded in the shape
this rule requires for an artifact that cannot be published:

- **Locator:** `_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/PLAN.md` - *in plain words, the
  untracked session workspace archive*.
- **Digest of the exact text relied on:** the pattern block at **L424-L425** is
  `18793b709c1826bfc078427b66e439e6b429c2e442d54b43071418d53b8014f3` (those two lines joined by LF plus one trailing LF);
  the plan as a whole is `d02022bcfeef11278feee0048f8ed259c6560e673cfabf7b1313af16a1cf05ee` (77,404 bytes, 700 lines), and the
  threshold sentence relied on is at **L421**.
- **Plain statement of retrievability: the plan is NOT retrievable from this repository and cannot be verified from a
  fresh checkout.** The digest identifies it; it does not make it fetchable, so **the verbatim-pattern claim is not
  checkable here** - only its digest is.

**What does not rest on the plan.** The three hits the plan's threshold names are reproduced **from the four source
files**, which are described above and digest-pinned in section 1: running the printed pattern over the archive
originals yields `BER-G3-FU3-EXECUTION.md` L155, `FU3-RECORD-FINAL-REVIEW-F.md` L121 and
`REVIEWPATH-FINAL-REVIEW-F.md` L47. That measurement is what establishes that the published set adds exactly one line to the
plan's three, and it needs no plan.
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

### OWED-9 - an unsanitized copy of the record survives in this branch's history, and no rewrite is done here

**What is true, measured rather than reasoned:** `bd210954` **is an ancestor of this head**
(`git merge-base --is-ancestor` exits 0). Five commits on this branch carry an **unsanitized** copy of the derivative at that
path, and three of them carry a byte-identical copy of the archive original:

| commit | bytes | sha256 | peternguyen | Ubuntu-24.04 | wsl$ |
| --- | ---: | --- | ---: | ---: | ---: |
| `bd210954` | 25,606 | `ea521f84c4d0d88f8e888f35…` | 7 | 8 | 7 |
| `b591e0d9` | 25,606 | `ea521f84c4d0d88f8e888f35…` | 7 | 8 | 7 |
| `c5f71554` | 25,606 | `ea521f84c4d0d88f8e888f35…` | 7 | 8 | 7 |
| `95351dda` | 26,345 | `cc183e4504a1b280d04e5726…` | 5 | 6 | 5 |
| `61e73442` | 26,345 | `cc183e4504a1b280d04e5726…` | 5 | 6 | 5 |

The seven later commits are clean (0 / 0 / 0). **Materiality:** the same identifiers are already in **4, 5 and 2 tracked files
at the base revision** respectively, so the history adds **a verbatim copy of a full unsanitized record**, not a new class
of identifier. **What a full purge would require:** rewriting five commits of a **twelve-commit** branch (5 unsanitized + 7 clean; `git rev-list --count bd210954^..HEAD` = 12). **What it would
invalidate:** every binding that names them - eleven Stage D records, eight Stage E validations, the Stage F verdicts and
MG2 - because a rewritten commit ceases to exist. **And it would still not free the repository**, since the identifiers
remain in tracked files at the base revision. **A partial purge that produces a clean-looking result without removing the
exposure is worse than an honest statement of the limit.** The owner's goal explicitly permits carried open publication
items; this is one, named so a future change can act on it.
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
4. **The citing entries** — the section 13 entries that link back to this page are the **first two**: the entry at
   **L4192-L4227** carries the links to this record and to three of the four copies, and the entry at **L4228-L4252**
   carries a further link to section 1.1. **The two newest entries - L4253-L4279 and L4280 and following - carry no
   link at all**; they correct counts, scope and an in-place edit. All four are named here so that a reader does not go
   looking for a link that is not there.
