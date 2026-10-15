# Workspace-citation-durability capture publication — 2026-10-15

**What this page is.** The publication record for the 27 supporting files that the merged pull
request #766 body's 56 skills-table **Row source** records cite — *in plain words, Row source is
the provenance record that binds each published skills-table row to the exact capture file its
author hashed* — from the untracked session workspace archive. **24 of the 27 are published
byte-identically; 3 are published as explicitly labelled sanitized derivatives**, and section 3
enumerates every difference for each of the three. This page records the measured gap, the
digests on both sides, the scan results, and what deliberately remains out-of-tree.

**Why it exists.** Sixteen of the 56 Row source records in the merged PR #766 body carry
`limits=none` — *in plain words, they declare no limitation on their cited source* — while the
files they cite live only in the session workspace archive and no fresh checkout can retrieve
them. This publication makes every artifact those 56 records cite retrievable from this
repository, under the repository's own evidence-retention rule
([the Behavioral Eval Runner backlog](../../roadmaps/behavioral-eval-runner-backlog.md) L4021–L4025):
*sanitized summary in Git; raw host paths, process IDs, users, secrets and evidence in the
separately approved external root under its access and retention rules; no private identifiers
in Git*.

**Attribution.** This page and the three sanitized derivatives' edits were produced by
**DeepSeek**, the Stage C (implementation) agent `d2-stage-c` for backlog item D2 — *in plain
words, the carried backlog item that publishes the supporting files the merged PR #766 body
cites* — on 2026-10-15. The published copies themselves are archival records authored by the
lane's earlier stage agents, whose own attributions stand inside those files.

**Base revision.** `e2a3e20b` — *in plain words, the merge commit of pull request #769, the
default-branch head this change branches from*.

**Reading key.** *Archive* — in plain words, the untracked session workspace folder
`_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/`, outside every repository
on this host. *Byte-identical* — a published copy whose sha256 equals its archive source.
*Sanitized derivative* — a published copy that deliberately differs from its source because
private identifiers were removed, with every difference enumerated in section 3. *Source-side
digest* — the sha256 of the archive original; *committed-side digest* — the sha256 a fresh clone
reproduces. *Self-digest footer* — the repository convention where a line reading
`sha256: <64 hex>` covers the file's bytes with that value replaced by the literal placeholder
`{{SHA256}}`, UTF-8, LF, final newline included. *PR #766* — the already-merged pull request
whose body carries the 56 records. *D2* — this backlog item.

## 1. The gap, re-measured before acting

The coordinator's brief measured the gap as **56 of 56 cite a session path; only 40 state a
non-retrievability limitation; 16 rest outside the repository and do not say so**. I re-measured
all of it before acting.

- Command: the merged PR #766 body was fetched with `gh pr view 766 --repo ModernNomad-98/Project-Aegis --json body`
  (140,650 bytes) and every `Row source:` occurrence was extracted with a regular-expression
  counter over that text.
- Measured: **56 Row source occurrences**, **all 56** citing a path under the archive;
  **40** carrying a non-retrievability statement; **16** carrying none.
- The 16 are all Stage D records (agent `of1-stage-d`) citing eight AUDIT-D files with
  `limits=none` — `AUDIT-D.md`, `AUDIT-D-round3.md`, `AUDIT-D-round4.md`, and
  `AUDIT-D-rows-round7R/8/9/10/11.txt`.
- **The re-measurement matches the brief's numbers exactly** — the difference, if any, is not in
  the counts but in what this publication does about them.

## 2. The published set — 27 files

**24 byte-identical copies and 3 sanitized derivatives.** Every published filename equals its
archive-relative name, except `wcd-c-rows.txt`, which the Stage C records cite at
`_resume-2026-10-09/_wcd-c-scratch/wcd-c-rows.txt`. For the 24 byte-identical copies the two
digest columns are equal by construction; for the derivatives they differ by exactly the
enumerated changes in section 3. All 27 are LF-only, no BOM, matching the archive bytes.

| # | Published file | Status | Source bytes → committed | Source-side sha256 (archive original) | Committed-side sha256 (fresh clone) |
| --- | --- | --- | ---: | --- | --- |
| 1 | [PLAN.md](PLAN.md) | byte-identical | 77,404 → 77,404 | `d02022bcfeef11278feee0048f8ed259c6560e673cfabf7b1313af16a1cf05ee` | same |
| 2 | [SD-C.md](SD-C.md) | byte-identical | 16,013 → 16,013 | `e0bb9017b7da1defcd7aedd23cb5e269a838aaafa7fa6db55b2907d913dfbbe1` | same |
| 3 | [AUDIT-B.md](AUDIT-B.md) | byte-identical | 40,291 → 40,291 | `c7938d642fdea1a3ccd8703009886c06d8fa2ab116c319adafea833908bf55cb` | same |
| 4 | [AUDIT-B-rev2.md](AUDIT-B-rev2.md) | byte-identical | 24,741 → 24,741 | `bbdbf9f50128211feefc1eaa3162a3d3803b8cca35fc9a41d62bf5272bfca728` | same |
| 5 | [AUDIT-D.md](AUDIT-D.md) | byte-identical | 36,252 → 36,252 | `ddfbc5fc79b0ee3c0f42fbeee3e018da5290ed22d4ec68599b57ce6b2d7d9808` | same |
| 6 | [AUDIT-D-round3.md](AUDIT-D-round3.md) | byte-identical | 28,776 → 28,776 | `1f67140863d84783fe561f9f08d1707ebb17c56a3ec9ac3ff8f9bdba30acb8d6` | same |
| 7 | [AUDIT-D-round4.md](AUDIT-D-round4.md) | **SANITIZED DERIVATIVE** — section 3.1 | 33,705 → 33,930 | `1f89b7c693399f8b91e5ae1e336c8e8a0c080bcc4817b0946767bd1a38fff22e` | `03308fe943b0dc056ab1e699fbac5a4f2e2a7883219dd85105b29829025faa96` |
| 8 | [AUDIT-D-rows-round7.txt](AUDIT-D-rows-round7.txt) | byte-identical | 2,054 → 2,054 | `b13a63a2b16d4bdbfc330239fc912986d33590b1aeec483f406ff84b6b30a290` | same |
| 9 | [AUDIT-D-rows-round7R.txt](AUDIT-D-rows-round7R.txt) | byte-identical | 2,850 → 2,850 | `4f6a2bd244d59120358f315c8e91a56f00d0b2d049a337663546ebf30b6fdd94` | same |
| 10 | [AUDIT-D-rows-round8.txt](AUDIT-D-rows-round8.txt) | byte-identical | 2,723 → 2,723 | `875fef7079eb9a91e063db58d3d6eda0100ad4e73cff1249a279592b9d23dbfb` | same |
| 11 | [AUDIT-D-rows-round9.txt](AUDIT-D-rows-round9.txt) | byte-identical | 2,915 → 2,915 | `fbd07ddc19f156f4e899a71eb1e8070e5df510ff35754198a082b2e16e8d0a67` | same |
| 12 | [AUDIT-D-rows-round10.txt](AUDIT-D-rows-round10.txt) | byte-identical | 3,468 → 3,468 | `6a5e0e6f722c06d3fe117e47450a9c3a56734bf9bd49e50822dd1f55b7da4a8e` | same |
| 13 | [AUDIT-D-rows-round11.txt](AUDIT-D-rows-round11.txt) | byte-identical | 3,148 → 3,148 | `99a305abaff9aaec24174848e5f3b49e8fe07821db7333f742325db3d0092e84` | same |
| 14 | [VALIDATE-E.md](VALIDATE-E.md) | byte-identical | 35,326 → 35,326 | `a78dedeceaf6ac66ddb28aab815598824657ebc0841ea5d4db800222c22df7b9` | same |
| 15 | [VALIDATE-E-round2.md](VALIDATE-E-round2.md) | byte-identical | 32,081 → 32,081 | `3de59148c4ab21d1ec05a273e0cf59eb57d1dccf3c728cdd4662d0d41bcfb140` | same |
| 16 | [VALIDATE-E-round3.md](VALIDATE-E-round3.md) | **SANITIZED DERIVATIVE** — section 3.2 | 29,674 → 29,746 | `6ec9a4fb5d3bee6b99bc83e1832ab84d9d5bde537e55b10bdf5fd4e814651193` | `f29a9c313de92336304b8a84c6f416be20e0328f316989df9a6cc26fd0eda25a` |
| 17 | [VALIDATE-E-round4.md](VALIDATE-E-round4.md) | **SANITIZED DERIVATIVE** — section 3.3 | 31,610 → 31,618 | `1cafca1e0953da270ee370074671033cf175d6787a6a90da99caefead578e4b3` | `93999207bc090df804f022a9c774752f127d003de39cca6eb864adce3bd99980` |
| 18 | [VALIDATE-E-round6.md](VALIDATE-E-round6.md) | byte-identical | 18,037 → 18,037 | `2f435f3c4f40af0ea3158fc3271ed4af51414a92cb912d7378dce2e426b20a19` | same |
| 19 | [F-ROW-capture.txt](F-ROW-capture.txt) | byte-identical — note 5.2 | 1,735 → 1,735 | `bd1ccf3fe8fe62127bada1d7065de6c7f6b644f9658ab11630e7ecf672ed0d5d` | same |
| 20 | [F-ROW-capture-round3-35acbbe8.txt](F-ROW-capture-round3-35acbbe8.txt) | byte-identical | 2,046 → 2,046 | `587cc3a1117055318e653d7c22462595e384b1b5bf72e86de0ee6a574e44ce2e` | same |
| 21 | [F-ROW-capture-round4-c53551d8.txt](F-ROW-capture-round4-c53551d8.txt) | byte-identical | 1,873 → 1,873 | `8cbda6fd9cc3e59b5d94ea3a57def498bdc0f4e310a0b1d24de6124ea415c60f` | same |
| 22 | [F-ROW-capture-round5-277a0f4d.txt](F-ROW-capture-round5-277a0f4d.txt) | byte-identical | 1,817 → 1,817 | `72a2c6711b55afaf5043b7e13b5bb95da38ecce338f14a965214f54db2791914` | same |
| 23 | [F-ROW-capture-round8-3ed6931c.txt](F-ROW-capture-round8-3ed6931c.txt) | byte-identical | 1,903 → 1,903 | `66025372b1710660cae29c06a477abef8be79ccdc94b056854b66d4e49cc9323` | same |
| 24 | [captures/VALIDATE-E-round7-SDE7-c53551d8.rows.txt](captures/VALIDATE-E-round7-SDE7-c53551d8.rows.txt) | byte-identical | 1,718 → 1,718 | `5fa8349d429ffc6679d38faa480544a47b54cd4d53aa953ea4bc30f966ff95c6` | same |
| 25 | [captures/VALIDATE-E-round8-SDE8-277a0f4d.rows.txt](captures/VALIDATE-E-round8-SDE8-277a0f4d.rows.txt) | byte-identical | 1,900 → 1,900 | `d4c804f995335366d54e8ad264bd5d4c50e49947eabe667033ea27a09a9ef476` | same |
| 26 | [captures/VALIDATE-E-round11-SDE11-3ed6931c.rows.txt](captures/VALIDATE-E-round11-SDE11-3ed6931c.rows.txt) | byte-identical | 1,987 → 1,987 | `895122506e82930e26d895260b55247e07e4ce470e5fcbdcbe4708fad0fffa42` | same |
| 27 | [wcd-c-rows.txt](wcd-c-rows.txt) | byte-identical (from `_wcd-c-scratch/`) | 2,575 → 2,575 | `3caaf88cf10096bf7d32fdb6112e246a0719dc0cae796512bbb383b5d93f444c` | same |

**How the 56 records map onto these files.** The records' cited sources fall on the 27 files
above: the Stage A records cite PLAN.md; Stage B cites AUDIT-B-rev2.md; Stage C cites
wcd-c-rows.txt (and SD-C.md, which reproduces it); the 16 Stage D records cite the eight
AUDIT-D files; the Stage E records cite the VALIDATE-E files and the three captures; the Stage F
records cite the five F-ROW captures. Every record's cited artifact is now inside this
repository.

## 3. The three sanitized derivatives — every difference, and why

The governing rule is *no private identifiers in Git* (the Behavioral Eval Runner backlog
L4021–L4025). The earlier FU-3 publication — *in plain words, the already-merged publication of
the four files the Behavioral Eval Runner backlog's O-F1 note cites, under
`docs/evidence/fu3-record-publication-2026-10-13/`* — established the treatment this section
follows: **the raw values are named by category, never by value; prior publication is not an
exception (a publication directory that does not exist at the base revision is new to Git
whatever appears elsewhere); and every difference is enumerated.** The removed token classes
are: the **username token**, the **distro-release token**, the **WSL UNC root token**, the
**distro-side directory-name token**, the **shell-history filename**, and the **searched local
drive-root list**. The raw values are withheld from this page for the same reason they are
withheld from the derivatives.

### 3.1 AUDIT-D-round4.md — 12 differences (11 sanitizations + the recomputed footer)

| # | Location (source line) | Change | Why |
| --- | --- | --- | --- |
| 1 | L130, the census table's first token row | the raw username token becomes "the username token (raw value withheld)" | the rule: no private identifiers in Git; the census's substance — how many tracked files contain the token — is preserved |
| 2 | L131, the census table's second token row | the raw distro-release token becomes "the distro-release token (raw value withheld)" | same reason |
| 3 | L132, the census table's WSL home-root row | the raw token string inside the parentheses becomes "the WSL UNC root token / the distro-release token / home" | same reason |
| 4 | L133, the census table's fourth token row | the raw distro-side directory-name token becomes "the distro-side directory-name token (raw value withheld)" | same reason |
| 5 | L134, the census table's fifth token row | the raw shell-history filename becomes "the shell-history filename" | same reason |
| 6 | L136, the census table's seventh token row | the raw searched drive-root list becomes "the searched local drive-root list" | same reason |
| 7 | L143, the occurrence-probe row | the quoted shell-history filename becomes "the shell-history filename" | same reason |
| 8 | L145, the occurrence-probe row | the raw drive-root list becomes "the searched local drive-root list" | same reason |
| 9 | L146, the occurrence-probe row | the raw `Get-Item` UNC-root command form becomes "the Get-Item WSL-UNC-root form" | same reason |
| 10 | L148, the prose sentence | the raw directory-name token in the sentence becomes "the distro-side directory name" | same reason |
| 11 | L300, the copy-ready skills row's parenthetical census | the two raw tokens become "the distro-side directory name" and "the shell-history filename" | same reason |
| 12 | L370, the self-digest footer | recomputed: `8b032f81…` → `29f31230441f8daa66fd314ece158a694d3f5fe7afc700c75b636aadf4b5a07d` | a derivative that kept its source's footer would carry a false integrity claim; the footer is recomputed over the derivative under the placeholder convention |

**Consequence, stated rather than hidden.** The Stage D round-4 records SDD4-1/SDD4-2 bind
sha256 `54c0eb27…` over the two row lines as they stand **in the archive** (2,225 bytes). The
published derivative's section-8 block is 2,255 bytes and hashes to
`15abddb0269007f600dd082c3e5de6a8ad6c1bd8a1d990e55df13e0b5383006d`, because difference 11
sanitizes one of those two lines. **The exact bound bytes therefore remain archive-only; the
sanitized row text is what the retention rule permits in Git.** The binding reproduces from the
archive original — measured — and is recorded here so no reader mistakes the sanitized block for
the bound one.

### 3.2 VALIDATE-E-round3.md — 5 differences (4 sanitizations + the recomputed footer)

| # | Location (source line) | Change | Why |
| --- | --- | --- | --- |
| 1 | L81, the finding prose | the raw shell-history filename becomes "the shell-history filename" | no private identifiers in Git |
| 2 | L87, the probe table row | the raw filename becomes "the shell-history filename" | same reason |
| 3 | L88, the second probe table row | the raw dotless filename becomes "the dotless shell-history filename" | same reason |
| 4 | L128, the prose sentence | the raw distro-release token inside the parentheses becomes "the distro-release token, raw value withheld" | same reason |
| 5 | L224, the self-digest footer | recomputed: `95c2e2e9…` → `a199e8318bfa5d8cdbd189195f0e3289e557b73498de4e054934623db5ff63d4` | false-claim prevention, as 3.1 item 12 |

### 3.3 VALIDATE-E-round4.md — 3 differences (2 sanitizations + the recomputed footer)

| # | Location (source line) | Change | Why |
| --- | --- | --- | --- |
| 1 | L12, the reading key | the raw WSL UNC root token in the definition becomes "the WSL UNC root" | no private identifiers in Git |
| 2 | L193, the E-8 row | two replacements on one line: the quoted raw root token becomes "the WSL UNC root", and the raw token in the S2 path description becomes "S2's WSL UNC-root path" | same reason |
| 3 | L264, the self-digest footer | recomputed: `078a6a5f…` → `6a9ddfdc9418c4dd40d0d9793e8e91c5e00764d03e159f725e7e8d33cdff8a58` | false-claim prevention, as 3.1 item 12 |

### 3.4 The deliberate non-change, recorded so the inventory is exhaustive

The project/session workspace path `C:\src\Project Aegis` appears in the published set — twice
in AUDIT-D-rows-round8.txt L1 and twice in VALIDATE-E-round4.md L193 — and is **deliberately
retained**, exactly as the FU-3 publication's item 5 retained it: it is the project and session
workspace path, not private host identity, and removing it would delete the records' honest
account of where the work was performed. No username, distro, UNC root, directory-name or
shell-history token survives anywhere in the published set (section 4's scan).

## 4. Integrity and scans, measured at this head

**Byte identity.** `Get-FileHash` over the 27 published files against their archive sources:
**24 equal, 3 differing** — the three derivatives of section 3. The count is measured, not
copied from the table above.

**Binding reproduction.** The PR #766 body's whole-file bindings over the `.txt` captures
reproduce from the published copies for all 14 (the five AUDIT-D-rows round files, the five
F-ROW captures, the three VALIDATE-E captures, and wcd-c-rows.txt). The two-row block bindings
reproduce from the published copies for 9 of 10: AUDIT-D.md (`f2182c82…`), AUDIT-D-round3.md
(`2f2e4c2b…`), VALIDATE-E.md (`d08418e5…`), VALIDATE-E-round2.md (`1ff5e868…`),
VALIDATE-E-round3.md (`cb7bca16…`), VALIDATE-E-round4.md (`db40662e…`),
VALIDATE-E-round6.md (`b9ad5aba…`), PLAN.md L590–L593 (`08cb06e4…`), and AUDIT-B-rev2.md
L223–L226 (`11c68ae3…`). The tenth — AUDIT-D-round4.md's `54c0eb27…` — reproduces from the
archive original only, as section 3.1 records. PLAN.md's footer seal `2dfe2f5f…` and
AUDIT-B-rev2.md's footer `03e7be7c…` both recompute under the placeholder convention from the
published copies.

**Privacy/token scan.** Every published file was scanned for the six token classes of section 3,
plus Windows user, temp and home path shapes, drive-root lists, e-mail addresses, and
credential-shaped keys. Result: **0 hits across the 27 published files.** The scan pattern
contains the raw token values, which is why this page states the classes and the count rather
than reprinting the pattern with its values.

**Credential scan — the FU-3 pattern, run as the plan's own AC8 shape.** The pattern
`AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{20,}|arn:aws|…|token *[:=]|[0-9]{12}`
(the same shape the merged lane used) prints **34 hits** over the 27 published copies, and every
one is read: **3 lines are the pattern quoting itself** (the rule text stating its own scan
rule), **12 lines are token-shape hits of which 8 are provider price lines** (published
nano-USD-per-token rates, not credentials), and **21 lines are twelve-digit account-shape hits**
— GitHub Actions job ids, CI run numbers, and sha256 digest substrings including the files' own
self-digest footers. **The three class counts sum to 36 over 34 distinct lines: two lines match
both the token shape and the twelve-digit shape, and both are among the 34 read.** This page
itself carries 7 shape hits of its own — one pattern self-quote and six twelve-digit runs inside
its own digest columns — all self-referential and benign. **No credential material is present.** A scan for secrets does not answer
whether an identifier is private; the token scan above is the privacy check, and it is zero.

## 5. What remains out-of-tree — the carried items

**The gap is closed for the artifacts the 56 records cite; it is NOT closed for every file in
the archive directory.** Four carried items remain, counted and named so a later change can act
on them:

- **CARRIED-1 — 48 archive files remain out-of-tree.** The archive directory holds 74 files;
27 are published here; **48 are not**, because the merged PR #766 body does not cite them
(superseded round records, superseded captures, and the lane's Stage F and Stage G records whose
cited forms are the F-ROW captures). Each is listed with its digest below so the debt is
measurable, not forgotten:

| # | Archive file | Bytes | sha256 |
| --- | --- | ---: | --- |
| 1 | AUDIT-D-round2.md | 28,462 | `ef2a6ba651aacb71db1a4bf4801c6e003595c647ece3c4c8e9cc3983d3d5e1dc` |
| 2 | AUDIT-D-round5.md | 32,243 | `02a8edbe336d27a6940b1fba6fd8d7c716b4f4bcf25a8911a71d2dfd23685f3e` |
| 3 | AUDIT-D-round6.md | 24,199 | `d7828600c484ddb77028240f8c75b521fb56c95559d0120d621fc30c62250554` |
| 4 | AUDIT-D-round7.md | 17,833 | `60197e403347997f5aabc70ac300e12f04eb29ee28c55674a4503ffdfa2e85ae` |
| 5 | AUDIT-D-round7-addendum.md | 9,974 | `9ce09facd72d7d09d729a1332d3bd7752ac765e8fa54b6805e2727e3f01bb860` |
| 6 | AUDIT-D-round7R-rows.md | 8,565 | `5b54ad67b978edcfd069851f260c74bf502b89ec80c499dcf0ccd851ccabc654` |
| 7 | AUDIT-D-round8-rows.md | 9,413 | `7ebfed56efc56ff0adf3dc42e7991ebe782a671dd58e09bc9cf02ae36bd8a9d2` |
| 8 | AUDIT-D-round9-rebind.md | 10,121 | `0147c4be07f8b62fcc645617c1a7a0dd963221599375f3273dbbc961f66bdc12` |
| 9 | AUDIT-D-round10-rebind.md | 11,580 | `8abe2923ccb75d4141d8118d5c02145635e663895eba4149aa9e9e46132deab8` |
| 10 | AUDIT-D-round11-rebind.md | 10,784 | `7bb6fb2a4ac047f9624307357503e2d23a0d80a0b5d9da550ca633b1147c0840` |
| 11 | AUDIT-D-rows-round5.txt | 2,533 | `d6b5b443f9bb9b6a7590a2f830cac2efe14f8985a01f9ab27f5df7e4cff45d73` |
| 12 | AUDIT-D-rows-round6.txt | 1,985 | `b495a114487b7d050a1d89d1c023904e62398d0ee1f55db7a5a866a4d3a5f08d` |
| 13 | captures/VALIDATE-E-round9-SDE9-9872c642.rows.txt | 1,914 | `c5a44a143dff77cea095dc2400b78f69f9cd84131070df2d81b8784ab992845f` |
| 14 | captures/VALIDATE-E-round10-SDE10-8e40488e.rows.txt | 1,970 | `c9ca8ab2063ba7e30c04d937af2f94458a10d79c522e365aafad01fa527b926d` |
| 15 | F-ROW-capture-round3.txt | 1,835 | `1625727240dda72235f6b9dc365fd54ff6374c17be58b091c6be03cd2f0ec0ff` |
| 16 | F-ROW-capture-round3-92437891.txt | 1,837 | `2cb894903aeca78587b766c48c04dd1bc6c4d1d160fde85d39ff1a524cf490d0` |
| 17 | F-ROW-capture-round3-c46d9057.txt | 2,047 | `5acfa9e3901d93677ab5cfd47c9dbad7765a853272e1f3b744831757e46b361c` |
| 18 | F-ROW-capture-round3-f7b7822f.txt | 1,805 | `6384ca74375e3505283050c4dabb8711fefb2a2501bf896758306056a09d7aed` |
| 19 | F-ROW-capture-round6-9872c642.txt | 1,826 | `d22985405da7670c692e19c98605e53fe6fc5cae96dbb7a5a900d0ab8a2f315b` |
| 20 | F-ROW-capture-round7-8e40488e.txt | 2,001 | `febf752ce2c53e6931b79ae387d4a06889d5b6f839d112f3c1bd9374173329b9` |
| 21 | F-ROW-capture-round9-eebe60f4.txt | 1,909 | `1b5fdbf1967e18a35f12639403379739528197da6d4e71e525a84bc4134649cb` |
| 22 | F-ROW-records.txt | 2,090 | `aa98e79729e3ec83019aca47f1e272a3d350aa04f09a66e94cff1bfb2d4b478c` |
| 23 | F-ROW-records-round3.txt | 2,123 | `bf4074b124c40ecaf7a52c1f82fcaf525b607c994bd9892d2cce1b38cafa2f73` |
| 24 | F-ROW-records-round3-35acbbe8.txt | 2,164 | `d09b20bb8a2db2a70b8ee9216b5fad807424a592c211dd4470f002cf87d6f4f1` |
| 25 | F-ROW-records-round3-92437891.txt | 2,262 | `26932ac666c330f8e7550d401e04f96172f5b83002dd2487df2e8131d260d183` |
| 26 | F-ROW-records-round3-c46d9057.txt | 2,168 | `332a5e5633bf1fd73ef4f94fb24a927c860d59a84c66d5d22d8942ab3586966b` |
| 27 | F-ROW-records-round3-f7b7822f.txt | 2,316 | `f49acd1feafe704629e89ebb30c1aca34f70530d8f1d1d2a5f2b7081dd492b4b` |
| 28 | F-ROW-records-round4-c53551d8.txt | 2,460 | `be42e8f4a341a406eec0d538c97cb4457c99bb5dfd40f8cf959931b0a52d0eff` |
| 29 | F-ROW-records-round5-277a0f4d.txt | 2,202 | `7b718e5b4389605215e805151535ec9c966f4f2c77cbd06e0abb7c8b3c4d6c75` |
| 30 | F-ROW-records-round6-9872c642.txt | 2,181 | `2cb79acade8b252a5c104ce68d5cfd6979a972c9ba1caed14c429a0f47fe5afd` |
| 31 | F-ROW-records-round7-8e40488e.txt | 2,190 | `fe2ba28f9cdf984a42f00d9fd802cc8c2d8415b9cdf576105c0f4b122d3eda1a` |
| 32 | F-ROW-records-round8-3ed6931c.txt | 2,123 | `02dbb7bfb21434efef46d16623a518c390e040c672c416cbec90bae55283bdc6` |
| 33 | F-ROW-records-round9-eebe60f4.txt | 2,123 | `cf20adefc38e8bb3773663c67b8b02b45796e13ce766e71a77f998ebed6910c3` |
| 34 | FINAL-REVIEW-F.md | 14,301 | `b4b54354c4297058b0f2245c59d585d2909672cb91ec67f46eafb7d82f540ba8` |
| 35 | FINAL-REVIEW-F-round1.md | 24,366 | `dbb397d05c68b32ef8b52e7ee2d5aa4db6017dbd574946591a4ead99145761c1` |
| 36 | FINAL-REVIEW-F-round2.md | 21,716 | `9abc57c47941db170a43b93eb13c68281132cccd2927f36917ecb51d9af866cc` |
| 37 | FINAL-REVIEW-F-round3.md | 18,354 | `ee3de126f8f6d626038fbcc5c84df51b050625378de0bbccf3fe4b2f5a0c1b38` |
| 38 | FINAL-REVIEW-F-round4.md | 17,414 | `cf28b02609c06434400623fa20669fdbc315d9a039b0aca45f2d9e7b5bd2b637` |
| 39 | FINAL-REVIEW-F-round5.md | 16,834 | `34183f7385c4834f0dd44c2e9b5328c67abd1d3a1bc728b296686c8cd2e070f9` |
| 40 | FINAL-REVIEW-F-round6.md | 15,672 | `4a2a27aff1b7425f0bc793f668dbacfb27d3f1e8532bf67691e0f55d8745e0b4` |
| 41 | stage-g-receipt.md | 58,841 | `bec76811517be3ad965f260207a4d28fa89dcbd95e17a8a93fa9e64fdcba06f6` |
| 42 | stage-g-summary.md | 59,470 | `cf92c227e39eda0e1c12be06865337435aacc10bc4c098ad82affa610dbc4907` |
| 43 | VALIDATE-E-round5.md | 19,774 | `21acb1b1e1d55af46eb66256451fc6a508a9ae9dc72ebf2b49f5f6c3c932f11c` |
| 44 | VALIDATE-E-round7.md | 23,874 | `ce5686a8bcd5bb80541edc65e532f1c62b54b8bc69f524c4b3e29f29176fe147` |
| 45 | VALIDATE-E-round8.md | 24,841 | `c7f016f3f0991d9f92716c223e8b41c8b90470c3f51ac24814a90f3446efb5da` |
| 46 | VALIDATE-E-round9.md | 24,126 | `2e449c654a671ce0a4aa276c07c5d7b2fdbf4e8220fcb8beea2f0af41d6b17ea` |
| 47 | VALIDATE-E-round10.md | 22,709 | `c0921c8ff4b6fb4dccd11ef0fb83b4c37e636da535727dbd70888ef15ef9285b` |
| 48 | VALIDATE-E-round11.md | 23,626 | `4b6051f2126f71241a6c4f6008a0eeb1f84fba2dfcb00802ee32e88ecb23ae42` |

- **CARRIED-2 — the Stage F round-1 capture bytes are lost, not merely out-of-tree.** The
  round-1 binding `eb42fc90…` (1,688 bytes) over `F-ROW-capture.txt` does not reproduce from
  the archive file, which now holds the round-2 capture (1,735 bytes, `bd1ccf3f…`) — the
  round-1 bytes were overwritten in place in the archive and survive nowhere in that directory.
  The round-2 bytes are published; the round-1 binding stays checkable only from whatever else
  may retain the earlier bytes, and this page records that the archive copy does not.
- **CARRIED-3 — the 16 `limits=none` records in the merged body are not edited.** A merged
  pull-request body is a record, not a working document; this publication makes their cited
  artifacts retrievable but does not rewrite the body's own text. The ledger keeper — *in plain
  words, the separate role that records documentation acceptances in the readability ledger
  under AEGIS-APR-101, which a Stage C author may not hold* — is the agent that can record this
  publication against the backlog, and it is a different agent from this one.
- **CARRIED-4 — the FU-3 publication record's own PLAN.md citations are now partially
  outdated.** Its section 5 states the plan "is NOT retrievable from this repository"; the plan
  is now published byte-identically in this directory. That dated record is deliberately not
  edited by this change; correcting it is a change to that record under its own rules.

**The honest bottom line.** 27 files published (24 byte-identical, 3 sanitized derivatives);
every artifact the 56 Row source records cite is now retrievable from a fresh checkout; **48
archive files, one lost capture revision, and the merged body's own 16 unamended
`limits=none` texts remain, each recorded above.**

## 6. How to verify this page

From a clone of this change's head, with the archive unavailable:

1. **Digests.** Hash each of the 27 files with `Get-FileHash -Algorithm SHA256` or
   `sha256sum` and compare against the committed-side column in section 2. All 27 reproduce
   it.
2. **Derivative footers.** For the three derivatives, replace the 64 hex characters on the line
   beginning `sha256:` with `{{SHA256}}` and hash the UTF-8 bytes including the final
   newline; the values in section 3's difference tables reproduce.
3. **Retrievability.** Read the files directly; no step of that path requires the archive.
4. **The sanitized difference.** For each derivative, diff its committed bytes against its
   source-side digest's archive original (archive required) — the only differing lines are the
   ones section 3 enumerates.
5. **Scans.** Run the two scans of section 4; the token scan prints 0 and the credential scan
   prints 34 read-and-benign lines.
