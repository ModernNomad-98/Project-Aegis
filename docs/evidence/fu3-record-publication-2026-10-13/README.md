# FU-3 record publication — 2026-10-13

**What this page is.** The publication record for four Behavioral Eval Runner (BER) FU-3
record-lane evidence files that this repository's append-only governance log cites, and that
until now existed only inside the session workspace archive. The four files are published
**byte-identically** in this directory. This page records their digests, the citations the
copies make retrievable, every archive path a tracked record still cites with its disposition,
and the citation-durability rule that keeps this defect from recurring.

**Why it exists.** The automated reviewer raised finding `4261109123` — *in plain words, one
inline P2 finding posted by the repository's automated reviewer, Codex* — against
`docs/roadmaps/behavioral-eval-runner-backlog.md` line 4162, asking for "a retained capture with
an immutable revision or digest and locator". The finding is **true**, and the repository-wide
scope is wider than the three files it names.

**The defect is durability, not accuracy.** The citations were correct: the sections they name
really do sit at the lines they name (section 2 re-states each anchor). What failed was
**retrievability** — the archive directory sits outside every Git repository on this host, so no
clone, no fresh checkout and no future contributor could read the evidence. Editing or deleting
an accurate citation would destroy a true record, and the log's own rule forbids it, so the
correction is a publication plus a **superseding** log entry that names the entry it supersedes.

**Reading key.** A *finding* is a defect raised by an automated or human reviewer on a pull
request. *FU-3* — in plain words, *the Behavioral Eval Runner provider-usage reconciliation
attempt whose record lane merged as pull request #764*. *O-F1* — in plain words, *the carried
defect under which that lane's merged pull-request body published a skills table with no row for
Stages D, E or F, because no stage read a skill*. The *archive* — in plain words, *the untracked
session workspace folder `_resume-2026-10-09/`, which is outside every repository on this host*.
A *self-digest footer* — in plain words, *the repository convention where a line reading
`sha256: <64 hex>` covers the file's bytes with that digest replaced by the literal placeholder
`{{SHA256}}`, UTF-8, LF, final newline included*. The *body digest* — in plain words, *the same
idea applied to every byte above a named footer heading instead of to the whole file*.

## 1. The four published files

Each copy is **byte-identical** to the archive source it came from. The whole-file sha256 below
is the plain digest a fresh clone reproduces with `sha256sum` or `Get-FileHash`; the last column
is the record's **own** integrity claim, recomputed from the published bytes, so that publishing
is shown not to have falsified it.

| # | Published file | Bytes | Lines | Whole-file sha256 | Its own digest, recomputed here |
| --- | --- | ---: | ---: | --- | --- |
| 1 | [BER-G3-FU3-EXECUTION.md](BER-G3-FU3-EXECUTION.md) | 25,606 | 347 | `ea521f84c4d0d88f8e888f3588147a6a63c659f8773f7d41339d9eeca47b9915` | self-digest footer `f5a6b9ca66c99dd8baa61018fb60974a08ab92efcffce3583285ca6cd97b8b97` — recomputes |
| 2 | [FU3-RECORD-FINAL-REVIEW-F.md](FU3-RECORD-FINAL-REVIEW-F.md) | 30,777 | 274 | `c0b0c548fa6b8f2cc9b961814099e8e12e690729bfdaa16e6c4b96263d7dab8a` | self-digest footer `8f554598a04d91567fbb10e301d1a8bc1e0c2940b2a82fb8a5bac4be9258937b` — recomputes |
| 3 | [FU3-RECORD-stage-g-summary.md](FU3-RECORD-stage-g-summary.md) | 25,454 | 233 | `d2ed1cfba306c12d993b5718b1d903de656409f1ff91af2e90c3ee1b178aa031` | self-digest footer `059822aabffb13cb417adcd1714bb00a90244c0df040a457db7ba9ac895bb2d7` — recomputes |
| 4 | [REVIEWPATH-FINAL-REVIEW-F.md](REVIEWPATH-FINAL-REVIEW-F.md) | 21,023 | 107 | `f367d36eda52c45289dee5d2cbdcde82c534db8c97786d23b78d51531491cd55` | body digest `81884e0d49cb117c7f7884350ce23adcfac6788891c0a9bc8828dc19461abcc8` (bytes above the footer heading at L103) — recomputes |

**All four are LF-only** (zero CRLF byte pairs) and the repository root `.gitattributes` is
`* text=auto eol=lf`, so the committed bytes equal the archive bytes and every digest above
stays reproducible from a clone.

**Nothing in them was edited.** No re-wrap, no trailing-whitespace fix, no link rewrite, no
re-encoding — a single changed byte would falsify both the self-digest and this page's
whole-file digest. Their internal citations to further out-of-tree artifacts are part of the
frozen archival text and are deliberately left as they are; the rule in section 4 binds new
citations and the citations superseded by this publication, not the archival body of a dated
record.

## 2. The citations these copies make retrievable

| Cited by | What the citation supports | Where it now resolves |
| --- | --- | --- |
| backlog line 4143 | the FU-3 execution record, "whose section 6 carries the stop verbatim" | [BER-G3-FU3-EXECUTION.md](BER-G3-FU3-EXECUTION.md) — section 6, "THE STOP RECORD (verbatim)", at L198 |
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
tree at the base revision, **before** this change. The four published copies in this directory are frozen
verbatim re-publications: they are archival records in their own right, and they carry their own
out-of-tree references internally - for example the two source-archive paths inside
`BER-G3-FU3-EXECUTION.md` at L113-L114, and a row-source locator inside
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
   or `sha256sum` and compare against the whole-file column in section 1. All four reproduce.
2. **Self-digests** — for files 1 to 3, replace the 64 hex characters on the line beginning
   `sha256:` with the literal placeholder and hash the UTF-8 bytes including the final newline,
   LF only; for file 4, hash every byte above the whole-line `## SHA-256 footer` heading (L103)
   the same way. All four reproduce the values in section 1.
3. **Retrievability** — read the four files directly from the clone. No step of that path
   requires the archive, and no Markdown link on this page targets it.
4. **The citing entry** — read the newest entry of section 13 of the backlog linked in section 2,
   which names the entry it supersedes and links back to this page.
