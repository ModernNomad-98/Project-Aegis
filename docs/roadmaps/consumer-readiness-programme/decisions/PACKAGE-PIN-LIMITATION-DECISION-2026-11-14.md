# PACKAGE-PIN LIMITATION DECISION — 2026-11-14

**Status: DECIDED — KEEP THE 42-FILE PACKAGE PIN-BOUND TO `2fef11dd`.** Read-only planner record. No repository or GitHub edit, no install, no re-pin, no provider call. This record decides one question and names its limitation; it converts no UNRUN to a pass and grants no authority.

**Decision.** The published 42-file starter package stays bound to commit `2fef11dd43fe6e943e99c7948ebeaca95d138072` / tree `14133f917b2fc35ccac44fb844fd1664fb6839af`. The current head `2ef1d7ea51a788065c7752b9a224188aa4381283` cannot be installed under the published pins without a re-pin. No current-head install, current-head verification or re-pin is claimed, measured or authorised by this record.

## 1. Bound identities

| Artifact | Bytes | SHA-256 / identity | Role |
| --- | ---: | --- | --- |
| Repository head | — | `2ef1d7ea51a788065c7752b9a224188aa4381283`, tree `4713c3e3e45f4074ff5a6423f282315ac87cd468` | Current main; the head whose delta is measured |
| Install pin | — | `2fef11dd43fe6e943e99c7948ebeaca95d138072`, tree `14133f917b2fc35ccac44fb844fd1664fb6839af` | The only commit the published harness accepts |
| `docs/consumer-starter-package.md` at head | 171,444 | `e4f248a7ab51c4709621128648512339e3259ceb50868078fafa450d4acd566f` | Published procedure (§2.3 list, §7.1 harness, §9.2 aggregate) |
| Same page at the prior bound head `a5a4dea8` | 171,116 | `1a8ae25512ee63f64b3189aee5d200ef240f4448288081e54b852d49a806ca30` | Page used by the B1/B2 dry-run; byte-identical harness |
| Same page at the pin `2fef11dd` | 168,975 | `00558792c5214847b69ec101847e73e8af0cb5d79e816435e8578f4efa1e2a8f` | Still the **41-file v2** page (`$PinCommit ffb040c7`, `$AggRows 41`, `$AggBytes 5420`) |
| §7.1 harness block | 27,797 | `33fabe47c681c6c95a2d575d0554f9a2513fd94236e277a1570d8388c8f10f64` | Identical at `a5a4dea8` and `2ef1d7ea` |
| P2 gate block | 6,493 | `fd01fce7806c74e92f0fdf877c1cb58ed7704e8f24a316cccbce91b1dd7398ea` | Identical at `a5a4dea8` and `2ef1d7ea` |
| 42-file package at the pin | 393,600 (6,153 LF) | aggregate `d6b2439548871f9514cd1aa8eb64cc20e7cae4b204ebceeb8a2c2aab3033c958` over 5,539 serialized bytes / 42 rows | The only package identity with a published measurement |
| 42-file package at head | 393,836 (6,153 LF) | aggregate `e93935bb76efc28ac28fb315488b1682eb67948ed0027838f05f358c8bb745aa` over 5,539 serialized bytes / 42 rows | **Planner computation only** — not published, measured or accepted |

The harness at head still hard-codes `$PinCommit = 2fef11dd…`, `$PinTree = 14133f91…`, `$AggSha = d6b24395…`, `$AggRows = 42`, `$AggBytes = 5539` and the 42-entry `$package` array. The page moved 328 bytes from `a5a4dea8` to `2ef1d7ea` (10 insertions / 7 deletions), all count-wording corrections (41→42, historical §7.3 label, 18→19 skill count); the P2 and §7.1 code blocks are byte-identical, so the extraction hashes above are valid at the current head.

## 2. Evidence: exactly one package file differs at head

**Method (read-only).** The 42 paths were taken from the §7.1 `$package` array at head. For each path, the blob was read from the Git object store at the pin and at head (`git cat-file blob <commit>:<path>`), then bytes, LF count and SHA-256 were computed. Rows were sorted with ordinal comparison, serialized exactly per §9.2 (path TAB bytes TAB lf TAB sha256 LF, UTF-8 no BOM), and the aggregate was recomputed.

**Result.** 42 paths compared; **41 byte-identical**; **exactly one differs**:

| Path | Pin bytes / SHA-256 | Head bytes / SHA-256 | LF / CR | Delta |
| --- | --- | --- | --- | --- |
| `.claude/skills/model-routing-policy/SKILL.md` | 6,456 / `b0bf85910a7c58cb175283c6d842e95b6455f9ec78442046e0cb61f15fc7997f` | 6,692 / `0c863621e19671f466b2f5984a49eb96fb5f137f1a56d7cfdd8accf681c62cbe` | 78 / 0 at both | +236 B |

The content delta is 5 insertions / 5 deletions in three hunks: the Purpose/Workflow pointer sentence, the medium-effort default wording, the ordinary-task versus high-risk limitation at steps 4–5, and the high-risk-verification stop condition. It entered after the pin in `9f9a7e22` ("fix model-routing-policy page-review findings") and `66620739` ("page-review R1 wording fixes"). The head file is therefore a post-pin, page-review-revised text, not a byte-identical copy.

**Aggregate corroboration.** The recomputation reproduces the published pin value exactly: `rows=42`, package bytes 393,600, LF 6,153, serialized 5,539, aggregate `d6b24395…`. That matches page §2.3, §9.2 and the harness constants, and it matches the B2 dry-run observation at the pin (`rows=42 serialized_bytes=5539 aggregate=d6b2439548871f9514cd1aa8eb64cc20e7cae4b204ebceeb8a2c2aab3033c958`, 42/42 rows, 393,600 B, 6,153 LF). At head the same 42 rows serialize to the same 5,539 bytes only because the byte-count field keeps four digits and SHA-256 is fixed width; the aggregate changes to `e93935bb…`.

**What this does and does not prove.** It proves that the package bytes at the two commits are different in exactly one path and that a head install would have a different aggregate. It does **not** prove a head install fails, because no head install was run. The expected failure is P3 identity (exit 31) before any write; if that check were bypassed, P9 would fail on the aggregate while all five P8 lines could still pass.

## 3. Why the package is pin-bound, not merely "preferred"

1. **P3 identity.** The harness compares the source `HEAD` and tree with `$PinCommit`/`$PinTree` before any write and stops with exit 31 on a mismatch (page §7 P3; harness line `if ($head -ne $PinCommit) { Stop-Step 31 … }`). A clone at `2ef1d7ea` would be refused before a byte is written by the same check. The same refusal was observed at `a5a4dea8` on 2026-11-14 (exit 31, 0 files written); it is **UNRUN at `2ef1d7ea`** and is expected, not observed.
2. **P8/P9 verification.** P8 compares the installed set with the source clone and with `tools/skills-manifest.json`; P9 compares the row count, serialized length and aggregate with the published pin values. At head the manifest was already refreshed to the head hash (`0c863621…`), and the 23 source pins exclude `SKILL.md` rows, so a head install could pass **all five P8 lines** and still fail P9: its aggregate is `e93935bb…`, not `d6b24395…`. That is the precise risk — a head install looks green on the whole P8 block and produces a different package identity. It is unmeasured because P3 stops first.
3. **Published block.** Page §2.3 is headed "42 paths, bytes and LF at the pin `2fef11dd…`", and §9.2 fixes the base value at that pin. The published procedure is pin-bound by construction.
4. **No head measurement.** The only 42-file P8/P9 measurement is at the pin (`MODEL-ROUTING-LAYER2-C1-MEASUREMENT-2026-11-13.md`, 11,462 B / `1ce1fa2b…`), plus the B2 dry-run at the same pin. No P8/P9 run exists at `2ef1d7ea`.
5. **No head acceptance.** The page-review and acceptance record does not cover a head re-pin. The Batch 24 starter-package page review FAILED and took no keeper row; the Phase B acceptances (K-463..K-465) are readability-only and changed no page claim.

## 4. Provenance asymmetry — the limitation in the title

The pin precedes the page that defines its own 42-file package. At `2fef11dd` the page was still the **41-file v2** page pinned to `ffb040c7`; the 42-file definition and the harness that pins `2fef11dd` were added later, in `d70aea40` ("register the model-routing-policy skill and 42-file starter package", Layer 2 B), with the 42-entry `$package` array completed in `38eee856`. The current page is 31 commits after the pin.

Consequences, stated plainly:

- **L1 — main is not installable.** A beginner who clones the default branch and runs the published harness would get exit 31 by design. The procedure is "clone, then check out the pin", not "clone main".
- **L2 — the definition post-dates the bytes.** The 42-file identity is a later editorial act over an earlier commit. That is legitimate only because the pin is named explicitly; a citation of "the current package" without the pin is incomplete.
- **L3 — the pin installs the pre-fix routing text.** The one differing file is the routing policy, and the head version contains the page-review wording fixes. Keeping the pin installs the older text. This is an evidence-integrity choice, not a claim that the older text is better.
- **L4 — the aggregate is the discriminator.** Two packages can share 42 rows and 5,539 serialized bytes and still be different; the aggregate, not the count, decides identity. A record with `rows=42` but a different aggregate at the pin is a finding, not a variant.
- **L5 — no repair path for the delta.** The accepted remedy is a fresh pin install, not an in-place edit of the installed routing file; editing an installed package file breaks the record's identity.

## 5. Why no current-head install or re-pin is claimed

| Reason | State |
| --- | --- |
| Head ≠ pin; P3 refuses before write | Expected exit 31 at `2ef1d7ea`; **UNRUN** at this head (observed only at `a5a4dea8`) |
| No P8/P9 measurement at head | **UNRUN**; only the pin has a measurement |
| Head aggregate differs (`e93935bb…`) | Computed, not published or accepted; a head record would match no published value |
| No updated §2.3 block, §9.2 base value or harness constants for head | Not written; writing them without a measurement creates an unmeasured pin, while editing the published block to make head pass is a patched harness (stop S6) |
| No page review/acceptance for a re-pin | **UNRUN**; Batch 24 starter-page review FAILED, no keeper row |
| No authority for a host install or current-head exercise | AUTH-C4 consumed; no new grant (see `AUTH-C4-REQUEST-2026-11-14.md`) |
| Current checkout is dirty | The canonical checkout carries untracked `e14-pr1020-body-fix.md`; a clean clone is required for any future pin work |

Options considered:

| Option | Disposition |
| --- | --- |
| **A. Keep the pin; record the one-file delta; re-pin only as a separate measured slice** | **CHOSEN** |
| B. Re-pin to `2ef1d7ea` now | Rejected: no P8/P9 measurement, no page block, no acceptance, no authority |
| C. Install head with edited pins/constants | Rejected: patched harness is stop S6; its output is not evidence |
| D. Publish both pin and head packages | Rejected: no head measurement or acceptance; one page, one identity |
| E. Stop all installs until a re-pin | Rejected: the pin install is measured, reproducible and remains valid evidence |

## 6. What KEEP means operationally

- **K1.** Every install, verification, B3/B4 and review record states both identities: pin `2fef11dd` and the head at which the delta was measured (`2ef1d7ea`). "42-file package" without the pin is an incomplete citation.
- **K2.** B2/B3/B4 run on a target installed at the pin. B3/B4 never reinstall from head and never edit an installed package file.
- **K3.** B1 uses the current head as the refusal input; at `2ef1d7ea` the expected result is exit 31 with zero writes, and it stays **UNRUN** until a human runs it.
- **K4.** No one edits `$PinCommit`, `$PinTree`, `$AggSha`, `$AggRows`, `$AggBytes` or `$package` to make the head pass. A patched harness is a stop, not a workaround.
- **K5.** At the pin, `rows=42 serialized_bytes=5539 aggregate=d6b24395…` is the whole identity. A mismatch is a finding.
- **K6.** Page citations give the page blob at head (171,444 B / `e4f248a7…`) and the §7.1 harness hash (`33fabe47…`), so the procedure text and the package bytes are separately checkable.

## 7. What a future re-pin requires

A re-pin is a new package identity, not an edit. It is complete only after all eight steps; a partial re-pin is a draft and must not be installed or cited as a pin.

| Step | Requirement | Evidence that closes it |
| --- | --- | --- |
| R1 | Freeze a candidate commit/tree; clean clone; no untracked files; LF checkout; no reparse points | `git rev-parse HEAD`, `HEAD^{tree}`, `git status --porcelain` empty, `git ls-files --eol` |
| R2 | Recompute all 42 rows from the candidate commit: path, bytes, LF, SHA-256; update page §2.3 (bytes/LF) and the 42-row per-file SHA-256 table in the measurement record; update `$package` only if membership changes | 42-row table with hashes; 42/42 recomputation |
| R3 | Recompute the aggregate with §9.2 exactly (ordinal sort, TAB/LF, UTF-8 no BOM) and publish rows, serialized bytes and SHA-256. For the exact `2ef1d7ea` delta the planner value is `e93935bb…` over 5,539 / 42, but it **must be re-measured**, not adopted from this record | Recomputed aggregate + serialized byte count |
| R4 | Update the harness `$PinCommit`, `$PinTree`, `$AggSha`, `$AggRows`, `$AggBytes`; re-extract the P2 gate and §7.1; record both blocks' bytes and SHA-256 | New block hashes; no byte edited by hand |
| R5 | Run the full P0–P9 procedure at the candidate pin on a disposable target; capture the five P8 lines, the P9 line, the 42-row record and an independent 42/42 hash recomputation | Exit 0; five PASS lines; P9; record; independent check |
| R6 | Page review and acceptance of the new list, aggregate and claims (Phase B / named reviewer; keeper row); update the page status and any dependent runbook | Review record + acceptance row; no claim before it |
| R7 | Update B1's refusal input and every runbook/packet citation; mark the old pin superseded (retained, not deleted) | New runbook/packet versions; supersession note |
| R8 | Only then may a record say "the current package" without a pin qualifier | Accepted page + measured pin |

**Gate-pin note.** The "gate pin" is the pair of published code blocks (P2 gate and §7.1 harness) extracted from the page, plus the commit/tree they check. A re-pin changes the commit/tree constants and the aggregate, and re-extracts both blocks; it does not change the gate's logic. Any change to the gate's logic is a separate reviewed change, not a pin refresh.

## 8. Risks of a misread KEEP

1. **Head install attempts** produce exit 31 and may be misreported as a broken installer rather than a correct refusal.
2. **"Current main" language** in summaries can imply the head is installed; every record must name the pin.
3. **Routing-text drift**: the installed policy is the pre-fix text; a B5 independence decision taken from the head text would not match the installed policy.
4. **Re-pin drift**: if the page, harness and aggregate are updated in separate changes, one can pass while another still pins the old value.
5. **Aggregate treated as a rounding**: a different aggregate at 42 rows is a different package, not a tolerance.
6. **Silent supersession**: an old pin record must be marked superseded, not deleted, or the evidence chain loses its history.

## 9. Non-claims and record identity

This record is read-only planning. It does not install, verify, re-pin, review, approve or authorise anything. It does not claim current-head installability, human usability, readiness, support, deployment, recovery, role execution, C4.2 evidence or publication. It does not convert the B1/B2 dry-run into a current-head result; those observations remain pin-bound. The head aggregate `e93935bb…` is a planner computation and must not be cited as a measured or accepted package identity.

**Inputs:** page at head 171,444 B / `e4f248a7…`; harness 27,797 B / `33fabe47…`; gate 6,493 B / `fd01fce7…`; `INTEGRATION-PILOT-RUNBOOK-2026-11-14.md` 30,225 B / `752641bb…`; `INTEGRATION-PILOT-DRYRUN-EVIDENCE-2026-11-14.md` 8,203 B / `0dd2066c…`; `INTEGRATION-PILOT-REVIEW-2026-11-14.md` 7,736 B / `a299c852…`; `MODEL-ROUTING-LAYER2-C1-MEASUREMENT-2026-11-13.md` 11,462 B / `1ce1fa2b…`; `CX-CONTINUATION-CLOSEOUT-2026-11-14.md` 15,517 B / `a78a0f80…`.

Recorded by: read-only Aegis package-pin/authority planner (delegated), 2026-11-14, America/Los_Angeles. Local programme record only; not Git-tracked; not an approval.
