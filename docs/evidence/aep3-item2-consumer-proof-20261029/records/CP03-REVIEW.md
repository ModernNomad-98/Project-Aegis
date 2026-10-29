# CP-03 INDEPENDENT SEMANTIC-CLOSURE REVIEW

**Case:** CP-03 — package integrity/closure (AEP#3 Item 2, frozen consumer case).
**Reviewer role:** independent, non-implementing. I did not build the fixtures, the installer,
the verifier, the install record or the pin. I re-derived every number from retained bytes.
**Date:** 2026-10-28 23:17–23:44 PDT (2026-10-29 06:17–06:44Z). Measured elapsed wall time:
**27 min** (start sampled at 23:17:32, finish 23:44:20; active/wall split not separately
instrumented — wall time is the reported figure).
**Writes:** only under `C:/src/Project Aegis/_A/work-package-3/item2-cp03-review/`.
Source repositories were read, never written; the one git clone I made was `--shared` into my own
evidence directory and was pruned after recording its identity.
**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not
observable.

---

## 1. VERDICT

**CP-03: PASS (observed)** — under the baseline declared below and with the three findings in
section 8 carried with the verdict.

The closure argument holds independently: I recomputed the manifest and the aggregate from the
installed bytes and reproduced the published values exactly, byte for byte, and I confirmed that
all 41 installed files are byte-identical to their `git cat-file` blobs at the pin
`ffb040c7`. I re-ran the four negative classes in disposable fixtures of my own making and
reproduced every recorded exit code and message. I re-derived the semantic closure of the
installed set from the installed text itself.

Nothing in this verdict rests on a value I copied from the records under review. Every number
below is accompanied by the command that produced it and, where it matters, by the artifact the
number was computed from.

### 1.1 The one clause this verdict is bound to

The frozen row requires "a missing reference, a changed byte and a stale pin each **fail** the
install check, plus an independent semantic-closure review of the installed set"
(REMAINING-ROWS.md §4). Both halves are now observed, but the word "fail" needs a precision that
the closeout record's table does not carry, and section 8.1 states exactly which reading is
supported. Under the reading "the check does not pass and the mismatch is reported with its own
message and its own aggregate", all three negatives hold. Under the stronger reading "the check
exits nonzero for a missing reference", it does not — the published installer heals a missing
packaged file and exits 0. That is documented resume behaviour (P6), not a defect, but no
record should describe it as a refusal.

### 1.2 The baseline this verdict is bound to

Semantic closure is only meaningful against a declared baseline. The package declares it in
`docs/consumer-starter-package.md` §1.2: "complete for J1" (Stage 0 → local delivery) under two
rules, and explicitly **not** complete for UI slices, AI features, hosted deployment, SaaS or
multi-tenant design, migrations, security-lens reviews or release-with-agents. I verified closure
against that baseline and no wider one. A PASS recorded without the baseline in the same row
would overclaim; section 7 gives the exact bound.

---

## 2. WHAT I WAS GIVEN, AND WHAT I REFUSED TO TAKE ON TRUST

| Input | Recorded identity | How I used it |
| --- | --- | --- |
| `item2-cp-closeout/CP-CLOSEOUT-RECORD.md` | 21,762 B, sha256 5b86a68c… | read as the claim under test, never as evidence |
| `item2-cp-closeout/LEDGER-UPDATE.md` | 4,148 B | read as the claim under test |
| `item2-cp-closeout/FIXTURE-RUNS/install-controls/install-controls.json` | 57,240 B, sha256 60ee6cc3… | compared field-by-field with my re-run |
| `item2-cp-ledger/CP-LEDGER.md` | 21,278 B, sha256 9f3d4f36… | the frozen row and its gap statement |
| `remediation/handshake/item2-build/evidence/consumer-install-record.md` (E-31) | 6,876 B, sha256 739a385c… | the 41-row manifest table; **re-derived, not trusted** |
| `remediation/handshake/item2-build/evidence/install-verification.tsv` | 5,483 B | cross-check of the same 41 rows |
| `work-package-3/item2-u8-vendor/manifest/HASH-MANIFEST.tsv` | 5,420 B | hashed it: its sha256 **is** the aggregate |
| `work-package-3/item2-u8-vendor/manifest/HASH-MANIFEST.md` | 7,996 B | the manifest's own statement of method |

I hashed all eight inputs at review time (`evidence/input-identity.json`). The four identities
quoted in the brief reproduce exactly: CP-CLOSEOUT-RECORD `5b86a68c2143…28aa`,
install-controls.json `60ee6cc3c88d…09da`, CP-LEDGER `9f3d4f369b7b…7f3d`, E-31
`739a385c2088…fc4e` — the first three agreeing with the brief's prefixes and the fourth with the
ledger's own §6 register entry. So the artifacts I reviewed are the artifacts named. Nothing in
sections 3–7 depends on that agreement: every number there is computed from bytes I read in this
session, not from the brief's identification of a file.

---

## 3. INDEPENDENT RECOMPUTATION OF THE MANIFEST AND THE AGGREGATE

### 3.1 Method

The aggregate algorithm is fully specified in two independent places: the published installer
(`install-starter.ps1:191-208`) and the earlier verifier (`evidence/verify-install.py`).
Both say: sort the 41 paths ordinally, serialise each row as
`path TAB bytes TAB lf TAB sha256 LF` in UTF-8, and take SHA-256 over the concatenation.

I implemented that serialisation myself, from the installed bytes, with no reference to any
recorded manifest. I ran it against two independent installed trees: the durable install target
(`item2-build/install-target`, 41 package files + 18 git metadata files) and a **fresh install I
performed myself** into an empty directory from the pinned source
(`evidence/replay/t0-fresh-install`).

### 3.2 Result

| Quantity | Recomputed | Published | Match |
| --- | ---: | ---: | --- |
| Rows | 41 | 41 | ✅ |
| Serialized bytes | 5,420 | 5,420 | ✅ |
| Aggregate | `fcff1124d9d15e7d7230fd317350e0eb3b097b453bb6b911cdc1e2485525b699` | same | ✅ |
| Total file bytes | 369,093 | 369,093 | ✅ |
| Total LF | 5,841 | 5,841 | ✅ |
| Rows missing vs E-31 table | 0 | — | ✅ |
| Extra rows vs E-31 table | 0 | — | ✅ |
| Byte/LF/SHA mismatches vs E-31 table | 0 | — | ✅ |

The strongest form of the check: **`HASH-MANIFEST.tsv` is 5,420 bytes, its SHA-256 is
`fcff1124…b699`, and it is byte-identical to the serialisation I recomputed from the installed
bytes** (`evidence/_hashmanifest.py` output: `recomputed bytes: 5420 identical_to_HASH-MANIFEST: True`).
The manifest *is* the serialisation; the aggregate *is* the hash of those bytes. There is no step
in that chain that requires trusting a table.

### 3.3 The installed set equals the pinned closure

I compared each installed file's bytes to `git -C pinned-src cat-file blob ffb040c7:<path>`:

- 41/41 byte-identical. **0 mismatches.**
- `pinned-src` `HEAD` = `ffb040c7a363648856475280646bbd142dfabe4e` (equals the pin).
- 18/18 SKILL.md files also match the `sha256` recorded for them in
  `pinned-src/tools/skills-manifest.json` — the "18 manifest pins" claim, recomputed rather than
  accepted. All 18 match on raw bytes, so the manifest's hash input and the file bytes agree.
- The 23 non-SKILL.md files are covered by the blob comparison above, which is stronger than the
  installer's own "23/23 source pins" (source-vs-target hash) because it is pin-vs-target.

**Conclusion:** the observed 41-row installed set is exactly the pinned closure — not merely a
set that hashes to the published aggregate, but the set of pinned blobs themselves.

---

## 4. RE-RUN OF THE NEGATIVE CONTROLS

All fixtures below are mine, created in this session under
`evidence/replay/`, from the pinned source at the pin. The installer
(`item2-build/evidence/install-starter.ps1`, used unmodified) and the read-only verifier
(`verify_install_readonly.py`, used unmodified) are the published artifacts. Fixture trees are retained
except the stale-pin clone, whose 47 MB git pack I pruned and replaced with
`src-stale-identity.txt` (HEAD `e5af1391…`, the same parent the recorded run used).

| # | Control | Exit | Message / result observed | Tree before→after | Recorded | Verdict |
| --- | --- | ---: | --- | --- | --- | --- |
| P0′ | fresh install, empty target, pin | **0** | `OK: 41 installed files… aggregate=fcff1124…b699` | 0→41 | 0, 0→41 | ✅ reproduced |
| V0′ | read-only verify of P0′ | 0 | 41 rows, 5,420 B, aggregate fcff1124…, 0 problems | unchanged | same | ✅ reproduced |
| N1′ | one packaged SKILL.md deleted, re-run installer | **0** | healed: file re-copied, aggregate back to fcff1124… | 40→41 | 0, 40→41 "healed" | ✅ reproduced |
| V1′ | same deletion, **verifier on an unhealed copy** | **0** ⚠ | `missing .claude/skills/code-reviewer/SKILL.md`; aggregate `12b66ae85f25802550defea83a6f58c2384e620ad931208081f1d8e9435474e5` | 40, unchanged | "n/a", 12b66ae8… | ✅ aggregate reproduced; **exit 0 — see 8.1** |
| N1b′ | one `references/*.md` deleted, re-run installer (new) | **0** | healed, aggregate restored | 40→41 | not recorded | new control, passes |
| V1b′ | same deletion, verifier unhealed (new) | **0** ⚠ | `missing .claude/skills/test-plan-designer/references/test-plan-template.md`; aggregate `40fdffdf4b73e0f044ffdc1ff39b04df7e79dd36c6a1a6a526624bb55f260fde` | 40, unchanged | not recorded | new control; same exit-0 property |
| N2′ | one byte changed in `AGENTS.md`, re-run installer | **22** | `exit 22: startup file differs: …\t2-changed-byte\AGENTS.md` | 41→41, **unchanged** | 22, same | ✅ reproduced |
| V2′ | same change, verifier | **0** ⚠ | `installed != pinned blob AGENTS.md`; aggregate `ada047f44d17b1e48f43dfc56aa1beebeadb6722921927a6bfccef04f6393237` | unchanged | "n/a", ada047f4… | ✅ aggregate reproduced; **exit 0 — see 8.1** |
| N2c′ | one byte changed in a `references/*.md` (new) | **31** | `exit 31: existing installed file differs from the pinned source` | 41→41, unchanged | not recorded | new control; **different exit class (31, not 22)** |
| N3′ | source clone at `HEAD~1` = `e5af1391…` | **31** | `exit 31: source HEAD e5af13911b07… is not the pinned commit ffb040c7…` | 0 files | 31, same message | ✅ reproduced |
| N4′ | two unrelated files planted, re-run | **0** | install passes; both files byte-identical after | 43→43, unchanged | 0, 43→43 | ✅ reproduced |
| N5′ | conflicting `AGENTS.md` | **22** | `exit 22: startup file differs` | 41→41, unchanged | 22, same | ✅ reproduced |
| N6′ | repeated identical install | **0** | same 41 rows, same aggregate, zero writes | 41→41, unchanged | 0, same | ✅ reproduced |

Full outputs, stderr and tree hashes: `evidence/replay-controls.json`.

### 4.1 Two things the re-run adds that the recorded matrix did not contain

1. **A changed byte in a non-startup installed file exits 31, not 22.** The recorded N2 changed
   `AGENTS.md` and got 22 (the startup-file pre-check, installer line 129). A change in a skill file
   is caught one step later by the existing-directory pre-check (line 123) and exits **31**. Both
   are refusals, both leave the tree unchanged; the exit code depends on which file class was
   touched. The recorded matrix should say "22 for a startup file, 31 for a packaged skill file".
2. **A missing `references/*.md` behaves identically to a missing `SKILL.md`.** Both heal on a
   re-run and both are reported by the verifier with a distinct aggregate. The deleted-file class
   is therefore uniform, which strengthens the negative control.

---

## 5. SEMANTIC CLOSURE OF THE INSTALLED SET — INDEPENDENTLY DERIVED

I treated the 41 installed files as the corpus and extracted every reference edge from the
installed bytes, then classified each edge. Method: markdown links, backticked path-like spans,
bare `docs/`/`scripts/`-rooted paths, and `@`-imports; resolved first against the citing file's own
directory, then against the workspace root. Raw edge list: `evidence/edges.tsv` (141 unique
edges), checks: `evidence/_closure_checks.py`.

### 5.1 File-link closure (pass 1)

| Edge class | Count | Resolution |
| --- | ---: | --- |
| Markdown links across the 39 skill files (non-HTTP) | 55 | — |
| …intra-skill (own `references/` or `../SKILL.md`) | 46 | **all resolve** |
| …sibling `../<skill>/SKILL.md` delegation | 4 | **all 4 resolve** (ai-sdlc-operating-model, change-classification-gate, requirements-gathering-facilitator, project-orchestrator) |
| …repo-root citations outside the package | **5** | do not resolve, by design; classified below |
| Root-relative workspace files (`AGENTS.md`, `CLAUDE.md` cited from skills) | 8 | resolve at the install root |

**SKILL.md ↔ references parity: 18/18 skills.** For every skill, the set of `references/*.md` it
cites equals the set it ships: no cited-but-absent file, no shipped-but-uncited file. The only
apparent exception is a false positive of my own parser — `project-orchestrator/SKILL.md` cites
`references/stage-gate-map.md`, which it does not ship, but line 83 attributes it explicitly to
`ai-sdlc-operating-model`'s directory and that file **is** installed. I read the passage rather
than trusting the parse; it is a correctly-attributed cross-skill citation, not a dangling edge.

The five repo-root citations, verified by reading each one in the installed bytes:

| # | Citation | Where | My classification |
| ---: | --- | --- | --- |
| 1 | `../../../docs/skills-catalog.md#…` | `ai-sdlc-operating-model/SKILL.md:21` | Background: names the source roster the reader is looking at; nothing reads it |
| 2 | `../../../docs/paths/add-ai-safely.md` | `project-orchestrator/SKILL.md:248` | **Conditional with a trigger**: "follow [AI path]" for an AI-agent runtime slice — outside J1 |
| 3 | `../../../docs/paths/design-and-build-ui.md` | `project-orchestrator/SKILL.md:259` | **Conditional with a trigger**: "also follow the [UI path]" for UI slices — outside J1; the sentence itself says "it adds no gate and removes none" |
| 4 | `../../../docs/paths/release-with-agents.md` | `project-orchestrator/SKILL.md:277` | **Conditional with a trigger**: several-reviewer release — outside J1 |
| 5 | `../../../docs/acceptance/scenario-a-runbook.md` | `project-orchestrator/SKILL.md:167` | Background: a provenance citation for a finding ("AR-A-008/AR-A-010 in …"); nothing reads it |

This is exactly the set the package's own §3 discloses, and exactly five, in exactly two skills.
I derived it before reading §3's table and it matched row for row; I record that as agreement
between an independent derivation and the package's claim, not as evidence for it.

### 5.2 Invocation closure (pass 2)

The routing surfaces that can invoke a skill are the stage map's "Enforcing skill" column
(10 lifecycle rows) and the orchestrator's per-stage lines. I extracted every skill name from
both and compared against the 18 installed skills:

- **30 distinct skill names** appear across those two surfaces.
- **20 are not installed.** Of those, **13 are individually named with owner + trigger in the
  package's §4.1 exclusion ledger** (`source-of-truth-reconciler`, `ai-task-decomposer`,
  `security-pr-reviewer`, `qa-strategy-architect`, `architecture-advisor`, `adr-writer`,
  `cloud-architecture-decider`, `risk-tiered-validation-selector`,
  `sharded-validation-with-resume`, `ai-closeout-reporter`, `ai-threat-modeler`,
  `threat-modeler`, `agent-authorization-matrix`).
- **7 are not individually named there** — see finding F3 in section 8.4.
- **0 of the 20 is auto-invocable on the J1 path.** Every one is either MANUAL-ONLY (never
  auto-invoked by rule), or gated behind an evidence trigger ("by evidence", "when the work is
  too big", "when the class requires the security lens"), or belongs to a lifecycle row J1 never
  enters (Merge, Close, Learn). The four sibling `SKILL.md` links that *are* delegation edges all
  point at installed skills.

**Closure statement.** For the installed set, under the declared baseline J1: no unresolved
required read edge, and no unresolved required invocation edge. For journeys outside J1 the
package makes no closure claim, and I make none.

---

## 6. DISCREPANCY LOG

| ID | Recorded | Observed in this review | Severity | Effect on CP-03 |
| --- | --- | --- | --- | --- |
| D1 | V1/V2 described as "fail closed"; table gives exit "n/a" | verifier exits **0** in both mismatch cases (measured twice each) | **material to wording** | does not negate the row, but the phrase "fail closed" must be qualified — see 8.1 |
| D2 | LEDGER-UPDATE: "missing reference, changed byte and stale pin each fail closed" | the missing-reference case on an existing install is **healed** by the installer (exit 0), not refused; only the verifier reports it, at exit 0 | material to wording | the check never *passes* with a missing file; but "fails closed" is the wrong verb for this leg |
| D3 | matrix covered a changed byte only in `AGENTS.md` (exit 22) | a changed byte in a packaged skill file exits **31** | minor, completeness | none — refusals either way |
| D4 | brief names the identity evidence as "HASH-MANIFEST.tsv" | it lives at `item2-u8-vendor/manifest/HASH-MANIFEST.tsv`, not beside E-31; it is 5,420 B and hashes to the aggregate | informational | none — located and used |
| D5 | CP-CLOSEOUT-RECORD §5 says "41 installed, 18/18 manifest pins, 23/23 source pins" | all three recomputed true | none | confirms the record |
| D6 | §3.2 of the package discloses "five MANUAL-ONLY owners … never named" | six manual-only owners are named on the routing surfaces without an individual §4.1 row (`local-ci-mirror-preflight` is the sixth) | minor, disclosure precision | none on closure; the category row still covers it |
| D7 | package §3.2 admits `agent-governance-audit` "is not classified on this page at all" | confirmed: not installed, not in §4.1, not MANUAL-ONLY | **disclosed gap**, outside J1 | none under baseline J1; blocks any wider closure claim |

No discrepancy was found in any exit code that was actually claimed as an exit code, in any
aggregate, in the row set, in the file bytes, or in the tree-hash before/after pairs.

---

## 7. WHAT THIS PASS DOES AND DOES NOT CERTIFY

**Certified (observed, in this session):**

1. The installed set is 41 files and is byte-identical to the pinned blobs at
   `ffb040c7a363648856475280646bbd142dfabe4e` — 41/41, 0 mismatches.
2. The manifest and aggregate are reproducible from installed bytes alone:
   41 rows / 5,420 B / `fcff1124…b699`, and `HASH-MANIFEST.tsv` is byte-identical to my
   recomputation and hashes to the same aggregate.
3. Changed-byte and stale-pin negatives refuse with nonzero exits (22/31 and 31) and leave the
   tree unchanged; the missing-file negative restores the file and restores the aggregate, and
   is reported with its own message and its own aggregate when not restored.
4. Collision behaviour: unrelated files preserved byte-identically, conflicting startup bytes
   stop the run, repeated identical install writes nothing.
5. Semantic closure of the installed set under baseline J1: 46 intra-skill links, 4 sibling
   delegation links, 18/18 reference parity, 5 classified repo-root citations, 0 unresolved
   required edges.

**Not certified — named so that no reader has to infer it:**

- Closure beyond J1 (merge, close, learn, hosted, security lens, UI/AI paths). The package
  disclaims it and I did not attempt it.
- Any pin other than `ffb040c7`.
- Process-level fail-closed behaviour of the read-only verifier (D1).
- Behaviour on a host where the destination tree contains a junction or symlink: the package
  says the harness does not check the destination for reparse points (§1.3), and I did not test
  it.

---

## 8. FINDINGS

### 8.1 F1 — the read-only verifier reports but does not fail (material to wording)

`verify_install_readonly.py` prints its JSON verdict and ends; it contains no `sys.exit` and no
nonzero path. I measured exit 0 with a missing file (aggregate `12b66ae8…`), with a changed byte
(aggregate `ada047f4…`), and with a changed reference file (aggregate `92a62c21…`). The recorded
evidence did not state an exit code for V1/V2 ("n/a"), so this is not a contradiction of the
record — it is the missing half of it.

Consequence: if "fail closed" is read as "a process gate returns nonzero", the missing-reference
leg does not satisfy it. If it is read as "the check cannot pass while bytes differ", it does,
because `aggregate_matches` is false and `row_problems` is non-empty in every mismatch case.

**Recommended ledger wording (exact):** "missing reference: installer heals on re-run (P6,
documented); verifier reports `missing <path>` and a differing aggregate, and exits 0. Changed byte:
installer refuses (22 startup / 31 skill file). Stale pin: installer refuses (31)." That sentence
is true under both readings and needs no reinterpretation later.

### 8.2 F2 — the closure certificate needs its baseline in the same row

"Semantic closure of the installed set" is only decidable against a declared journey. The
baseline is J1 (`docs/consumer-starter-package.md` §1.2). A ledger row that says "CP-03 PASS —
semantic closure independently reviewed" without "baseline J1" invites a later reader to assume
whole-lifecycle closure, which the package itself denies. **Recommended bound field:**
`baseline = J1 (Stage 0 → local delivery); out-of-baseline owners classified in §4.1`.

### 8.3 F3 — seven named owners have no individual §4.1 row

Of the 20 non-installed names on the routing surfaces, 7 are not individually named in the
exclusion ledger: `agent-memory-governance`, `agent-failure-recovery`,
`agent-instruction-consolidator`, `reviewable-diff-discipline`, `docs-first-implementer`,
`local-ci-mirror-preflight` (all six MANUAL-ONLY, covered by the ledger's category row) and
`agent-governance-audit` (not MANUAL-ONLY; admitted unclassified in the package's §3.2). The
package's own disclosure counts *five* manual-only owners; the count is six.

Effect on CP-03: none under baseline J1 — the six are never auto-invoked, and
`agent-governance-audit` belongs to the Learn row, which J1 does not enter. Effect on any wider
claim: real. Fix is one row in §4.1 or a corrected count in §3.2; it needs no re-run.

### 8.4 F4 — the recorded matrix under-describes the changed-byte class

`AGENTS.md` → 22; packaged skill file → 31. Same refusal, different code. Add one row to the
control matrix so a future reader does not read 22 as the general answer.

---

## 9. CAN CP-03 MOVE TO PASS IN THE CONSOLIDATED LEDGER?

**Yes — to PASS (observed), conditional on three bound fields being recorded with the row:**

1. `baseline = J1 (Stage 0 → local delivery)` (F2);
2. negative-control wording per 8.1, distinguishing "refuses (nonzero)" from "reports (exit 0)"
   (F1, F4);
3. the independence statement: this review recomputed the manifest, the aggregate and the
   pin membership from installed bytes, and re-ran the controls in fixtures it built itself.

With those three, the row is defensible. Without (1) it overclaims; without (2) it repeats a
verb the evidence does not support for one of its three legs.

**Ledger arithmetic if this PASS is accepted:** 8 PASS (CP-03, CP-04, CP-08, CP-09, CP-10,
CP-13, CP-14, CP-16), 11 UNRUN, 3 BLOCKED, 0 NOT-APPLICABLE, denominator 22.

### 9.1 Exact UNRUN residue (what would still have to be observed to widen the claim)

- An independent closure review at a **different pin** — nothing here transfers.
- Invocation closure for **Merge / Close / Learn** and the hosted/security/UI/AI branches —
  requires the excluded owners to be installed or classified individually (F3, D7).
- **Process-level** fail-closed behaviour of any read-only verifier shipped for consumers (F1).

None of these is a clause of the frozen CP-03 row. CP-03 itself has **no remaining UNRUN
clause**; the residue belongs to CP-05/CP-07 (U8 route) and to a future whole-lifecycle claim.

---

## 10. REPRODUCTION

```text
cd "C:/src/Project Aegis/_A/work-package-3/item2-cp03-review/evidence"
python _recompute.py          # 41 rows / 5420 B / fcff1124… from two installed trees + pin blob compare
python _hashmanifest.py       # HASH-MANIFEST.tsv sha256 == aggregate; byte-identical to recomputation
python _manifest_pins.py      # 18/18 SKILL.md pins against tools/skills-manifest.json
python _replay_controls.py    # P0', N1', N2', N2c', N3', N4', N5', N6' into evidence/replay/
python _replay_verify.py      # V1', V1b' on unhealed copies (aggregate + exit code)
python _closure_checks.py     # 55 links, 4 sibling delegation, 18/18 reference parity
python _routing.py            # 30 names / 20 uninstalled / 13 in §4.1
```

Note: `_replay_controls.py` expects a clean `evidence/replay/`; it deletes and rebuilds it. The
stale-pin clone is recreated by the script and pruned afterwards by hand (it is not needed to
read the result, which is in `replay-controls.json`).

**Model:** DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model
not observable.
