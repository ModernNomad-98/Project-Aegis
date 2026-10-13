# BER-G3 FU-3 EXECUTION — HISTORICAL PROVIDER-USAGE RECONCILIATION

**Item:** "Historical provider-usage reconciliation (FU-3) execution" (records-only).
**Agent:** `fu3-accounting-executor` — **no subagents were used**; **no provider call**, **no spend**, and
**no repository, GitHub or register write** was made by this pass.
**Written:** 2026-10-13T07:14:00-07:00 (America/Los_Angeles).
**Status:** **RECOVERY FAILED — STOP RECORDED.** This file grants nothing, renews no cap, authorizes no
dispatch and creates no new ceiling. The three recommended appended entries FU-3 was to draft **were not
issued**, because issuing them would require exactly the reconciliation that failed (§7).

**Reading aid (owner's permanent reporting rule).** Every label or identifier below carries a one-line
plain-English description beside it. Repository line numbers are at `main` = `878b7d46` unless stated;
`register` means `docs/approvals/APPROVAL_REGISTER.md` (the owner approval register — the file that
records who was allowed to do what); `backlog` means `docs/roadmaps/behavioral-eval-runner-backlog.md`
(the BER decision register); `open-decisions` means
`docs/roadmaps/aegis-open-decisions-2026-09-23.md` (the open question tracker).

---

## 1. What FU-3 asked for

The owner-approved G3 deliverable (measurement packet
`docs/roadmaps/ber-wp2b3-measurement-prerequisite-decision-packet.md` L17, item 3 — *the decision
checklist whose row 3 defines this accounting*) required, in order:

1. recover the authoritative **historical provider usage and reservations, including uncertain attempts**;
2. **reconcile the single durable ledger** — the one append-only, hash-chained event log in which every
   external interaction is recorded — before granting dispatch;
3. show **remaining headroom** against the lifetime maxima;
4. **recheck the current provider price** and recompute the worst permitted path;
5. record the **provider-side project spend limit** and a **stop-before-exceed** rule.

Steps 1–2 are the load-bearing ones: steps 3–5 are arithmetic over a **known** prior-usage number. This
pass executed step 1 exhaustively and could not complete it, so it stopped there rather than assume a zero.

---

## 2. RECOVERY RESULT — what was searched, found, and missing

Every location searched is an evidence root, archive store or source clone. Nothing was modified; every
read was read-only.

| # | Location searched | What it is (plain English) | Result |
| --- | --- | --- | --- |
| S1 | `C:\src\Project Aegis` and its `_resume-2026-10-09` subtree | the session workspace and the resumed work tree | **searched** — receipts, lane records, clones, no provider-usage bytes |
| S2 | `\\wsl$\Ubuntu-24.04\home\peternguyen\aegis-stage-a\` | the external distro-private evidence root on the WSL2 Linux distro | **reached; fully censused** — 1,719 files, **no usage artefact** (§2.2) |
| S3 | `C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Evidence` | the **authorized** external evidence root named by the owner's decision 24 | **DOES NOT EXIST on this host** (§2.1) |
| S4 | `C:\temp` (whole), `D:\` (whole), `C:\src\Project Aegis` (whole) | all other local bulk storage | **searched by name and by content** — no ledger file, no usage JSONL, no billing record |
| S5 | the distro's interactive shell-history file | the Linux shell history that would show a live-run command | **16 bytes — effectively empty**; no live provider command ever recorded |
| S6 | the public repository via the accounting clone at `878b7d46` | the published Git record | **searched** — the ledger *implementation* is published; no ledger *data* is in Git (and cannot be) |

### 2.1 The authorized evidence root does not exist

The owner-approved external evidence root is fixed by the authorization decision package
(`docs/roadmaps/behavioral-eval-runner-wp-2b-3-authorization-decision-package.md` **L631**, decision 24 —
*the row that fixes where calibration evidence must live*) as:

> `C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Evidence`

Measured this pass: **`Test-Path` returns `False`; the directory was NOT PRESENT WHEN
SEARCHED.** `C:\temp` exists and holds ~100 unrelated older work directories, none of them the
calibration evidence root. That is a **current-state observation and nothing more**: it does not establish
whether the directory, or any provider execution evidence at it, ever existed on this host. **Its historical
existence is UNKNOWN**, in line with this record's own governing packet, which states that missing old evidence
does not prove zero use.

### 2.2 The external distro root holds source code and host logs — not usage

`\\wsl$\Ubuntu-24.04\home\peternguyen\aegis-stage-a\` **is reachable and was read in full** (the distro
`Ubuntu-24.04` — *the WSL2 Linux distribution this project's host probe used* — reported `Stopped` at
this pass's first probe and `Running` shortly after; **this agent started, resumed and launched nothing**,
and the paused VM was not touched).

| Top directory | Files | What it actually is |
| --- | --- | --- |
| `raw`, `raw-rerun` | 12 | the six per-command host-phase log files from probe run 1 and the D90 re-run |
| `ber-src`, `ber-src-fixed`, `ber-src-repair`, `-repair-r2`, `-repair-r3`, `-src-verify`, `ber-stage-b` | 1,362 | extracted copies of the `tools/behavioral_eval_runner` **source tree** |
| `ber-followup`, `ber-followup-r2` | 541 | source trees plus two suite logs and one module log |
| **Total** | **1,719** | **source code (1,455 files), tests, schemas and host-phase logs. Zero data files.** |

Decisive negatives, each actively tested:

- **No archive of any kind** (`.tar`, `.tgz`, `.tar.gz`, `.zip`, `.jsonl`, `.db`) exists anywhere under
  the distro home — so the two named archive hashes can only refer to the two Windows-side tarballs (§3).
- **No file named** for a ledger, usage, spend, token, cost, price, quota or reservation record exists.
- A content scan for `usage|spend|tokens_used|input_tokens|output_tokens|cost_usd|billing|quota|reservation`
  swept **1,455** files and matched **377** — every match is inside the tool's **own source code**
  (`budget.py`, `calibration_ledger.py`, `calibration_provider.py` and their tests). **Not one match is
  recorded data.** The strings are the caps *declared in code*, not usage *observed at runtime*.

### 2.3 What is missing, and exactly where it should be

| Missing artefact | What it is (plain English) | Where it should be |
| --- | --- | --- |
| **The durable ledger event chain** — one append-only, hash-chained file (the tool names it via `CalibrationLedger(path)`; `tools/behavioral_eval_runner/judge/calibration_ledger.py` L313–L318, L488) | the single log in which every provider attempt, token count and dollar charge is written before and after each request | at the **authorized external evidence root** `C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Evidence\`, per decision 24 (L631) — **absent** |
| **The first-segment declaration** (the explicit, durably recorded record that opens a fresh ledger; ledger docstring L11–L13) | the marker that proves a ledger was started rather than silently reset | same root — **absent** |
| **Any provider usage / reservation record, including uncertain (orphan) attempts** (ledger docstring L15–L19: a `STARTED` attempt with no terminal event is an **orphan** — *an attempt that began and whose outcome was never recorded; it is never forgotten and counts against every ceiling at its reserved worst-case charge*) | the historical usage this reconciliation must recover | same root — **absent** |
| **Provider-side project spend limit record** (decision 32, L639) | the cap actually set on the provider's own project page | nowhere on this host; it is a provider-console fact, not a file |
| **The stage-a capability summary** | noted by the task brief as deferred/unpublished | not published anywhere searched |

**Uncertain attempts are specifically unrecoverable.** Because the ledger itself is absent, an orphaned
(or any other) historical attempt cannot be distinguished from no attempt at all. This is the precise
condition the governing rule addresses:

> **"Missing old evidence does not prove zero use."** — measurement packet L17 (the same row that defines
> this deliverable).

---

## 3. The two named archive hashes — verified, and shown to be the *wrong kind* of artefact

Both hashes named in the receipts were located and **verified byte-for-byte this pass**:

| Hash named in the receipts | File it is | Bytes | SHA-256 re-computed this pass | Verdict |
| --- | --- | --- | --- | --- |
| `d4c36739bb591419f37605f69f19025164c37e1603bf8a5d5a11839dc610e618` | `_resume-2026-10-09\evidence\ber-dec-lane\ber-source-3c384b25.tar` — the **git source archive** of pinned commit `3c384b25`, subtree `tools/behavioral_eval_runner` (run 1) | 1,914,880 | `D4C36739BB591419F37605F69F19025164C37E1603BF8A5D5A11839DC610E618` | **EXACT MATCH** |
| `ec7ef949045bcee62ea3d883994185ed7a72fbfb133b74df13472229b68c490d` | `_resume-2026-10-09\evidence\ber-dec-lane\ber-source-bd5d2ff5.tar` — the **git source archive** of pinned commit `bd5d2ff5` (the D90-authorized re-run) | 1,925,120 | `EC7EF949045BCEE62EA3D883994185ED7A72FBFB133B74DF13472229B68C490D` | **EXACT MATCH** |

**The finding that matters for FU-3:** both hashes are digests of the **program that was run** (its source
tarball), not of **what the program used** (its provider calls, tokens or dollars). They are, correctly,
the evidence for APR-130's host-phase consumption — the register says exactly this at **L5557** ("the
pinned source archives `d4c36739…` and `ec7ef949…`"). They are **not** provider-usage artefacts and cannot
discharge FU-3's step 1. The related probe results
(`...\evidence\ber-dec-lane\stage-a-probe\probe-results.json` and `stage-a-probe-rerun\probe-results.json`)
were also read in full: they record a **60-minute ceiling**, six commands, exit statuses and elapsed
seconds — **host-phase timing only; no tokens, no calls, no spend.**

An important correction to the premise as briefed: these artefacts are **not** exclusively outside Git.
The disposition receipts, both tarballs and both result JSONs are present in the session workspace tree at
`_resume-2026-10-09\evidence\ber-dec-lane\`; only their **publication** is the gap the register's
L5554–L5561 records. The **provider-usage** evidence, by contrast, was never in Git *and* is absent from
every root searched.

---

## 4. Ledger and allowance state, re-read from the durable record

| Item | What it is (plain English) | State as re-read at `878b7d46` |
| --- | --- | --- |
| `AEGIS-APR-128` (`register` L5438; use limit L5487–L5491) | the BER Stage A offline host-probe grant — the only BER-named allowance in the register | limit = "**One named offline Stage A host probe on the WSL2 distro; consumed when the host phase completes its receipts. No calendar expiry stated.**" |
| `AEGIS-APR-130` (`register` L5530–L5562) | the consumption event that closes APR-128 | **"Event: CONSUMED; target grant AEGIS-APR-128"**; "AEGIS-APR-128 has no remaining use"; "**Effective at:** 2026-10-11"; "**New authority:** None" |
| `BER-DEC-008` maxima (`backlog` L3371–L3384) | the lifetime call/token/dollar ceilings for the measurement work package | 200 judgment attempts incl. retries; 1 read-only metadata request; 201 total external requests; 8,000 input tokens per judgment; USD $175 total; USD $175 per day; **stop BEFORE any cap is exceeded** |
| `open-decisions` L360 | the standing operational posture for this allowance | "Operationally assume **zero available residual allowance** until independently reconciled, without changing the historical grant" |

**The decisive gap between these two records.** APR-128/APR-130 govern a **host probe** (a local
capability check with no provider request); BER-DEC-008 governs **provider** calls. The register shows no
provider-usage event at all — because, as this pass establishes, **no ledger data exists to hold one**.
Reconciling APR-128/APR-130 therefore yields a **host-phase** result (zero residual on a non-provider
grant) and **no provider-usage number**. That is the whole of what the durable record can support.

---

## 5. Current-price recheck and worst-path recompute (performed; informational only)

Step 4 of FU-3 **was** completed, because it depends only on published prices, not on the missing ledger.

**Price recorded in force** (`calibration_ledger.py` L68–L71 — *the constants the tool bills with*):
input `5,000` nano-USD/token = **$5.00 / 1M**; output `30,000` = **$30.00 / 1M**; cached input `500` =
**$0.50 / 1M**; `PRICE_VERIFIED_DATE = "2026-08-14"`. Authorized model
(`calibration_transport.py` L39): **`gpt-5.5-2026-04-23`**.

**Price recheck, 2026-10-13.** The current published per-million-token prices for GPT-5.5 were re-read
independently: **$5.00 input / $0.50 cached input / $30.00 output**, 1M context — an **exact match** to the
price the ledger uses. The recheck was taken from BenchLM's published OpenAI price table of 2026-10-13
(article modified `2026-10-13T00:00:00.000Z`), which lists GPT-5.5 at those three rates:
<https://benchlm.ai/openai/api-pricing> (markdown source:
<https://benchlm.ai/md/openai/api-pricing.md>). **Note the limit of this evidence:** it is a third-party
price table, not the provider's own page — the provider's own pricing and model pages were fetched but
returned only navigation chrome within the fetch limit and yielded no usable rate text. **A first-party
confirmation remains owed before any dispatch**, and the decision package itself requires the price to be
re-verified at implementation time.

**Worst permitted path, recomputed from the tool's own formula**
(`worst_case_attempt_charge_nanousd`, `calibration_ledger.py` L172–L179 — *the function that charges an
attempt its maximum possible cost*):

```text
per attempt = 8,000 input x 5,000 + 25,000 output x 30,000
            = 40,000,000 + 750,000,000 = 790,000,000 nano-USD = USD $0.79
200 judgment attempts (the judgment ceiling; each charged at the worst case)
                                     = 158,000,000,000 nano-USD  = USD $158.00
+ at most 1 read-only metadata availability request (the 201st request: the
  decision package section 17 row 17 caps the total at 200 judgment attempts
  plus 1 metadata request; it submits no calibration content and invokes no
  generation, so the worst-case attempt charge above does not apply to it)
                                     = not charged by the attempt formula
worst case on the permitted 201-request path
                                     = 158,000,000,000 nano-USD  = USD $158.00
spend ceiling                        = 175,000,000,000 nano-USD  = USD $175.00
request ceiling                      = 201
```

The $158 figure **reproduces exactly**, which is why the ledger's own authority gate asserts
`200 * worst_case_attempt_charge_nanousd() == 158_000_000_000` (`cli.py` L1115–L1117 — *the startup
self-check that refuses to run if the recorded worst-path math drifts*). The price is therefore **not**
"materially changed", and the USD $158 path is **still arithmetically valid at today's published price**.

**But the price was never the binding constraint.** The binding constraint is the **201-request ceiling**:
the tool models **any** external request — judgment attempt **or** metadata request — as incrementing the
same `total_external_requests` counter (definition L203; increment L840 — *one shared counter for every
outbound call*). The worst permitted path already consumes **201 of 201 requests**, leaving **zero**
request headroom even in a hypothetical from-zero state. Any prior attempt that exists and is
unaccounted-for therefore **overruns the external-request ceiling outright**. This is precisely why
"missing old evidence does not prove zero use" is decisive rather than pedantic.

---

## 6. THE STOP RECORD (verbatim)

> **STOP — BER-G3 FU-3 HISTORICAL PROVIDER-USAGE RECONCILIATION: NOT PERFORMED.**
>
> **Reason: the authoritative historical provider-usage evidence does not exist on any root reachable
> from this host, and missing old evidence does not prove zero use.**
>
> Specifically, the single durable ledger — the one append-only, hash-chained event log in which every
> external interaction is recorded before and after transport (reporting attempts, tokens, spend and
> day-spend) — **was not found**, in whole or in part, on the session workspace, on the external
> distro-private root `\\wsl$\Ubuntu-24.04\home\peternguyen\aegis-stage-a\`, on the authorized external
> evidence root `C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Evidence` (**which does not
> exist**), on `C:\temp`, on `D:\`, or in the public repository. The two archive hashes named in the
> receipts were recovered and verified **exactly**, but both are digests of the **probe's source tarball**,
> not of any provider usage; the associated `probe-results.json` files record host-phase timing only.
>
> **No historical usage figure may be inferred, and NO HEADROOM FIGURE IS ESTABLISHED.** The prior
> consumption of the BER-DEC-008 lifetime maxima — 200 judgment attempts including retries, 1 read-only
> metadata request, 201 total external requests, 8,000 input tokens per judgment, USD $175 total and
> USD $175 per day — **remains unknown and unreconciled.** Because an interrupted or orphaned attempt is
> indistinguishable from no attempt once the ledger is missing, zero use **cannot** be asserted.
>
> **Consequence, per the governing rule:** "Unknown or exhausted headroom, unavailable telemetry, or
> materially changed price stops all metadata and judgment calls until the owner resolves it"
> (measurement packet L17). **All metadata and judgment calls remain STOPPED.** The operational posture
> stands unchanged at **zero available residual allowance** until independently reconciled
> (`open-decisions` L360). Nothing here renews, widens or consumes any allowance; **New authority: None.**
>
> **This stop is not a finding of overspend.** The single AP/APR event that exists (APR-130) closes a
> **host-phase** grant with no provider request, and the durable record shows **no provider-usage event at
> all**. The stop is a finding of **unverifiable headroom**, which the rule treats identically.

---

## 7. The three recommended appended entries — DRAFTED BUT NOT ISSUABLE (and why)

FU-3's step (iv)–(v) asked for three new appended governance entries: **(1) remaining headroom**,
**(2) the provider-side project spend limit at or below the approved ceiling**, and **(3) a
stop-before-exceed rule** — each marked **"New authority: None"**.

**They are not drafted as operative entries, deliberately.** Each is a *positive assertion* that the
reconciliation succeeded: entry 1 would state a headroom number, entry 2 would certify a limit "at or below
the approved ceiling", and entry 3 would define the margin at which execution stops. With prior usage
unknown, **every one of those three assertions would be false or unsupported**, and entering them would
convert an unverifiable position into an apparently-governed one — the exact failure mode the rule against
assuming zero exists to prevent. Under the owner's own stop condition they are **not issuable** at this
time. Recording them anyway would be worse than recording the stop.

**What is issued instead — one recommended appended register lifecycle entry (drafted verbatim for the
follow-up docs PR; nothing was written to the repository by this pass):**

```markdown
### AEGIS-APR-13x: BER provider-usage reconciliation attempted — headroom UNVERIFIABLE; zero-residual posture stands

- **Event:** RECONCILIATION ATTEMPTED AND NOT COMPLETED; no allowance effect.
- **Recorded at / By:** 2026-10-13 / <records-lane agent id>.
- **Finding:** FU-3 (the execution of BER-G3's remaining-allowance reconciliation) searched the session
  workspace, the external distro-private root \\wsl$\Ubuntu-24.04\home\peternguyen\aegis-stage-a\, the
  authorized external evidence root
  C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Evidence (verified absent), C:\temp, D:\ and
  the public repository. The single durable provider ledger — the append-only hash-chained event log that
  records every external interaction, its attempts, tokens and spend — was not found on any of them. The
  two archive hashes named in the receipts were recovered and verified exactly, but both are digests of the
  probe's SOURCE TARBALL, not of provider usage; the probe-results.json files record host-phase timing only.
- **Status at recording:** headroom against the BER-DEC-008 lifetime maxima is **UNVERIFIABLE**, not zero
  and not positive. Prior consumption of the 200-attempt / 1-metadata / 201-total-request / 8,000-input-token
  / USD $175-total / USD $175-per-day ceilings remains unreconciled. An orphaned or uncertain attempt cannot
  be distinguished from no attempt once the ledger is missing, so zero use cannot be asserted.
- **Effective at:** 2026-10-13, on recording.
- **New authority:** None. This entry records a failed recovery and grants nothing. No metadata request, no
  judgment call, no dispatch, and no cap renewal is covered by it. The operational posture stands unchanged:
  zero available residual allowance until independently reconciled (open-decisions L360).
- **Reason:** "Missing old evidence does not prove zero use. Unknown or exhausted headroom, unavailable
  telemetry, or materially changed price stops all metadata and judgment calls until the owner resolves it"
  — docs/roadmaps/ber-wp2b3-measurement-prerequisite-decision-packet.md L17.
- **Evidence:** _resume-2026-10-09/evidence/docs-refresh-2026-10-12/BER-G3-FU3-EXECUTION.md (this record).
- **Unblocking action (owner):** supply the durable ledger event chain and its first-segment declaration
  from the authorized external evidence root, or restate the allowance; only then can headroom, the
  provider-side spend limit and the stop-before-exceed rule be recorded as facts.
```

*(The ID `AEGIS-APR-13x` is a placeholder — allocate the next free number at append time. Idempotency: that
single entry is the correct **and sufficient** record of this outcome; do not also add a separate
"headroom" entry, since a headroom assertion is exactly what cannot be made.)*

---

## 8. Statement of limits

- This record is **accounting only**. It grants no approval, renews no cap, authorizes no dispatch, no
  metadata request, no judgment call and no host step, and creates no new ceiling.
- **No provider call was made and no spend was incurred by this pass.** No repository, GitHub, register or
  backlog byte was written. The only write is this file.
- The **paused VM (OPEN-4 — *the open decision item that forbids resuming or deleting the paused virtual
  machine*) was not started, resumed or deleted**, and `clone-pq1`, `clone-pq2`, the legacy root and
  every `wt-*` worktree were **not touched**. The WSL distro moved from `Stopped` to `Running` between
  this pass's first and second probe; **that transition was not caused by any command this agent issued**,
  which were all listing and reading operations, and the pass read the distro **read-only**.
- The price recheck rests on a **third-party published price table**, not the provider's own page, which
  returned no usable rate text; **a first-party confirmation is owed before dispatch**.
- No historical usage figure is asserted anywhere in this file. All arithmetic in §5 is over **published
  ceilings and prices**, never over observed usage.

---

## 9. Timing — *Historical provider-usage reconciliation (FU-3) execution*

| Field | Value |
| --- | --- |
| Item | Historical provider-usage reconciliation (FU-3) execution |
| Start | `2026-10-13T06:43:37-07:00` (`13:43:37Z`) — sampled at the first action; ETA **≈25 minutes** stated there |
| Finish | 2026-10-13T07:15:00-07:00 (`2026-10-13T14:15:00Z`) — sampled at the final evidence write |
| Wall | **≈31 min** |
| ETA vs wall | **≈1.24×** — the ≈25-minute ETA against a ≈31-minute wall; the item overran its estimate, principally on full-tree content sweeps of three filesystems |

Wall is compared against the stated ETA and is an imperfect measure: active time was not separately timed,
and the elapsed time includes queueing on background filesystem sweeps.

---

## 10. Verification commands (read-only; reproducible)

```text
Get-FileHash '_resume-2026-10-09\evidence\ber-dec-lane\ber-source-3c384b25.tar' -Algorithm SHA256
  -> D4C36739BB591419F37605F69F19025164C37E1603BF8A5D5A11839DC610E618   (== receipt d4c36739…)

Get-FileHash '_resume-2026-10-09\evidence\ber-dec-lane\ber-source-bd5d2ff5.tar' -Algorithm SHA256
  -> EC7EF949045BCEE62EA3D883994185ED7A72FBFB133B74DF13472229B68C490D   (== receipt ec7ef949…)

Test-Path 'C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Evidence'
  -> False     (the authorized external evidence root, decision 24 / package L631, does NOT exist)

Get-ChildItem '\\wsl$\Ubuntu-24.04\home\peternguyen\aegis-stage-a' -Recurse -File | Measure-Object
  -> Count = 1719   (all source trees + host logs; zero ledger, usage, spend or billing files)

A recursive name-and-content search across the local bulk-storage roots and the distro home, for any ledger file
  -> only calibration-ledger-entry.schema.json (the SCHEMA, never the data)

(the distro's interactive shell-history file, sized)
  -> 16 bytes   (no live provider command ever recorded)

git -C _resume-2026-10-09\clone-ber-g3-accounting grep -n 'MAX_TOTAL_EXTERNAL_REQUESTS' -- tools/behavioral_eval_runner/judge/calibration_ledger.py
  -> 62: MAX_TOTAL_EXTERNAL_REQUESTS = 201
```

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes including the final newline. Line endings are LF only. -->
sha256: 3a4d32645e0e2189ccef64fa0cfc3518e88884d18087ba2f0d7ca29d35d1b148
