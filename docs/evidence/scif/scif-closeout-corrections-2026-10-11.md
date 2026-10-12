# SCIF close-out corrections — the #723/#729 record corrected forward (2026-10-11)

*Dated addenda. Nothing here rewrites an existing record: each block states the
original claim or record, the primary evidence, and the correction. The earlier
texts stay byte-identical, so a reader can see both the original and the
correction.*

- **What this page corrects.** Three close-out records are corrected forward:
  (1) the MG3 status of PR #729 at its merge time; (2) the authority status of
  PR #729's failed `gate-guard` check; (3) the citation and identity claims of
  `_resume-2026-10-09\evidence\dirfd-probe-repair\HANDOFF-CORRECTION.md`.
  §4 lists what this page deliberately does not do.
- **Base revision.** `5a9adea0f2dce00c8ffe4be959ffb7e4a91ad566` — the commit
  this page was written at, where `git rev-parse HEAD` and
  `git ls-remote origin refs/heads/main` were equal and the worktree was clean.
  Every repository line anchor below was re-derived at this base unless it names
  another revision; the MG3 rule text is quoted from the merge-time revision
  `c4fbee1d9de13d9f8c79a46d1f7470810858011a` (the pre-#729-merge `main`).
- **Inputs (hashes recomputed from raw bytes).** `SCIF-recon.md` above-footer
  sha256 `a3c8a53faf0ba73798bcc6b7f0f38bc80188364c5389242c72c040469e1b5a41`
  (match); `HANDOFF-CORRECTION.md` whole-file sha256
  `f508eb4c57805631c8548abb57929665175089df68483672c3dcbf67fdec9c08` (match).
- **Honesty rules this page obeys.** A receipt is a record, not a gate.
  `UNRUN` and not-established are answers. Report the gap, never fill it.
- **Not an authority.** This page records corrections; it grants nothing,
  approves nothing, excuses nothing and creates no retrospective authority (D7).
  It does not edit the approval register, and it does not re-open #723 or #729.

## 1. #729 MG3 at merge time — NOT MET AT MERGE TIME (dated addendum, 2026-10-11)

**The rule in force at merge time**, quoted verbatim from `docs/delivery-workflow.md`
at `c4fbee1d9de13d9f8c79a46d1f7470810858011a` (L308-314):

> - **`MG3` — automated review.** The automated review has posted **a result for
>   that exact head**, or is confirmed unavailable **for that exact head** (a
>   usage-limit notice, for example); **and** every finding it raised at **P2 or
>   higher** — `P0`, `P1` and `P2`; this is a **floor, not a range** — is triaged —
>   fixed, or recorded in the pull request with the reason it is not a
>   defect. This is `AEGIS-APR-050`'s requirement and it is not optional. A result
>   at a superseded head does not satisfy `MG3`.

and the same revision's exact-head sentence (L250-255):

> All five are checked in the same turn against the **exact head being merged**.
> **A result at a superseded head does not satisfy the condition that cites it** —
> including `MG3` and `MG5`; a check result, an automated review or a conditional
> security review binds to one head and to that head only. Recording them in the
> receipt afterwards does not satisfy them — a receipt is a record, not a gate.

**Evidence state at `f356157c633a28fc09aa9c98b50bddd90469dec9`** (committer date
2026-10-11T18:10:38Z), **between 18:10:38Z and the 18:32:39Z merge** — primary API
records, re-fetched at this base:

- `repos/ModernNomad-98/Project-Aegis/pulls/729/reviews` returns **exactly one**
  review object: id `5484238846`, `chatgpt-codex-connector[bot]`,
  `state=COMMENTED`, submitted **2026-10-11T17:30:06Z**, whose body's bound line
  reads "**Reviewed commit:** `8959fd260d`" — the **superseded round-1 head**
  `8959fd260df6046f066ffbd5f4ee61ef1ece7674`, not the merged head. Its one
  inline comment is `4242513000` (P2,
  `tools/behavioral_eval_runner/tests/test_evidence.py:756`,
  `original_commit_id=8959fd260d…`, 17:30:06Z).
- `issues/729/comments` returns 13 comments. Exactly one is from the Codex bot —
  the review summary `6111681988` posted 17:25:38Z, **before** the merged head
  existed. **No comment records a Codex result for `f356157c`, and no comment is
  a usage-limit or unavailability notice for `f356157c`.** The head existed for
  about 22 minutes with zero Codex activity on it.

**Verdict: MG3 NOT MET AT MERGE TIME.** Neither branch of the condition existed
for the merged head: no automated-review result for `f356157c`, and no confirmed
unavailability for `f356157c`. Not "satisfied in purpose"; not "not
established"; and there is no retrospective satisfaction.

**What is real, and is recorded beside it — without changing the verdict.** The
triage trail existed and is real: P2 finding `4242513000` was triaged as fixed
(SD-C round-3 addendum `6111929206`) and the bytes at H were verified by the
receipt, and the merge receipt `6112299270` itself records "At H there is NO
Codex result and NO usage-limit notice — recorded honestly as no-result-at-H
(neither MG3 branch is claimed for H)". The merge proceeded on the coordinator's
recorded precedent — the **`MG3 EXACT-HEAD PRECEDENT`** entry of
`_resume-2026-10-09\FAST-CHECKPOINT-2026-10-11D.md` (coordinator decision,
2026-10-11 ~15:50 PT), cited here **by heading and date, not by line** — which
records the stricter rendering as "recorded as literally unmet in each receipt —
flagged, never hidden", and on APR-050's looser register wording. **Non-claim:
the triage trail does not create MG3 satisfaction, and this page does not
approve, excuse or re-decide the merge; the precedent is cited as a record, not
as a waiver.**

## 2. #729 gate-guard disposition — authority NOT ESTABLISHED FROM ACCESSIBLE EVIDENCE (dated addendum, 2026-10-11)

**Primary record.** `commits/f356157c633a28fc09aa9c98b50bddd90469dec9/check-runs`
(re-fetched at this base) shows `gate-guard` **failed in all three attempts**
(completed 18:10:53Z, 18:25:21Z and 18:27:54Z), while `changes`,
`validate-skills`, `tools-tests-linux`, `tools-tests-windows` and
`windows-offline-checks` all concluded `success` on that head.

**Authority check — the accessible evidence does not establish it.**

- **APR-047's four eligible paths do not include #729's changed files.** The
  register at this base holds `### AEGIS-APR-047: Standing gate-guard exception
  for four BER files` at L1224; the four eligible paths are at L1255-1259 —
  `tools/behavioral_eval_runner/reporting.py`,
  `tools/behavioral_eval_runner/aggregation.py`,
  `tools/behavioral_eval_runner/tests/test_reporting.py` and
  `tools/behavioral_eval_runner/tests/test_aggregation.py`. #729 changed
  `tools/behavioral_eval_runner/evidence.py` and
  `tools/behavioral_eval_runner/tests/test_evidence.py` — **neither is on the
  list.**
- **APR-047's Scope FORBIDDEN closes the gap rather than covering it**
  (L1272-1284): "a PR also touching any other protected file is ineligible as a
  whole; … and all other BER paths keep separate one-time owner decisions. …
  Expanding the four-path list needs a new owner decision."
- **No register or reconciliation entry names #729.** `git grep -n -i -E
  '#729|PR ?729' 5a9adea0f2dce00c8ffe4be959ffb7e4a91ad566 -- docs/approvals/APPROVAL_REGISTER.md
  docs/reconciliation/` at this base returns **no matches** (exit 1).
- **APR-100's own Scope FORBIDDEN excludes a gate-guard waiver** (L3121-3128):
  the delivery grant "does not … waive a failed local test or GitHub Actions
  check, waive a protected `gate-guard` (a protected-path failure still needs a
  one-time exact-head owner exception, or the standing AEGIS-APR-047 exception
  where all its conditions hold)".
- **The only accessible authority record** is the PR #729 body itself: the
  owner's blanket instruction quoted verbatim there — "Pre-aproved all
  troubleshooting, commit, push, and mergs once local and GH chekcs are green.
  If not, take it in thand fry to fix it." — together with the standing
  "continue to build until asked to stop", with the body recording the
  gate-guard trip **by design** on `evidence.py` and the disposition "never as
  green, never as waived". The register records that newer wording's provenance
  in APR-100's **ANNOT-Q3-005** (L3147, D95): carried by the merged PR #724
  body, with both texts recorded verbatim and "the divergence … recorded, not
  judged".

**Verdict: authority NOT ESTABLISHED FROM ACCESSIBLE EVIDENCE.** No register or
reconciliation entry establishes authority for a failed protected-path check on
#729; APR-047 does not cover #729's files; APR-100 by its own terms does not
waive a protected `gate-guard`.

**Explicit non-claims (D7).** This page does **not** establish authority, does
**not** claim APR-047 or APR-100 covered the failure, does **not** edit, annotate
or re-open the register (its diff in this change is zero lines), and does **not**
claim the failure was green or waived.

## 3. HANDOFF-CORRECTION.md corrections (dated addendum, 2026-10-11)

`HANDOFF-CORRECTION.md` (whole-file sha256 `f508eb4c…`) is **preserved, not
rewritten**; this section is the dated correction to three of its claims.

### 3a. Three of the seven cited comment IDs belong to PR #721, not #723

Per-ID API locators (`repos/ModernNomad-98/Project-Aegis/issues/comments/<id>`),
re-fetched at this base:

| Cited comment ID | Timestamp (Z) | Owning PR (`issue_url`) | What it actually is (`body` head) |
| --- | --- | --- | --- |
| 6104148527 | 01:21:48 | **721** | "SD-D: ACCEPT — BER guard-fix lane Stage …" |
| 6104196189 | 01:28:25 | **721** | "**SD-E: INCOMPLETE — UNRUN LISTED** …" |
| 6104213124 | 01:30:48 | **721** | "SD-F: ACCEPT — BER guard-fix lane Stage …" |
| 6107054131 | 08:17:58 | 723 | "SD-D: ACCEPT — dirfd-probe-repair PUBLIC …" |
| 6107118947 | 08:26:35 | 723 | "**SD-E: INCOMPLETE — UNRUN LISTED** …" |
| 6107142849 | 08:29:50 | 723 | "SD-F: ACCEPT — dirfd-probe-repair public …" |
| 6107164055 | 08:32:39 | 723 | "**SD-G: MERGED** — Stage G administrator merge …" |

The handoff's sentence "The A-F stage verdicts exist as posted PR comments on PR
#723 with distinct author identities" is therefore **partially inaccurate** for
three of its seven cited IDs: `6104148527`, `6104196189` and `6104213124` are
**the earlier BER guard-fix lane's (PR #721's) `SD-D`/`SD-E`/`SD-F` verdicts**,
not A/B-side or #723 verdicts. Recorded as **CORRECTED, not concealed**.

### 3b. Publisher identity is not distinct agent identity

Every one of the seven cited comments has `user.login = ModernNomad-98`
(re-fetched per ID at this base): one shared GitHub publisher account carries the
owner and every stage agent. Role labels occur only as in-text self-descriptions
inside some bodies — "stage-d-auditor" in `6107054131` and `6104148527`,
"stage-e-validator" in `6107118947` and `6104196189` — and "stage-b-auditor",
"pr-publisher" and "stage-f-reviewer" appear in **none** of the seven cited
comments. The handoff's "distinct author identities" is therefore not evidenced
by distinct GitHub identities; **no independently evidenced per-agent identity
exists at the API level**, and this is a structural limit rather than a citation
slip: `docs/delivery-workflow.md:652` (at this base) records the same — "Agent
identity is not separable on GitHub — every agent posts as the same account."

### 3c. Count provenance separated: 36 ≠ 620 ≠ 1107

- **36** is the module-level local WSL2 run of `test_evidence.py` recorded by the
  lane's own SD-C dirfd-publication record ("Ran 36 tests, OK (skipped=3), exit
  0"). It is a local module run, **not a gate count**.
- **620** is the CI `tools-tests-linux` scope at #723's head (job log: "Ran 620
  tests in 126.929s", "OK (skipped=10)").
- **1107** is the #729 post-merge BER suite scope (run `38164260605`, job
  `114543412177`: "Ran 1107 tests … OK (skipped=4)", the four skips being the
  Windows-specific assertions).

None contradicts another; they measure different scopes. The handoff's "36 tests
OK" is neither a CI gate count nor a suite total. Related but separate: the
checkpoint's "36 lanes merged (PR #694 → #729)" — re-derived at this base as
**36 merged PRs numbered #694..#729** (`gh pr list --state merged`, no unmerged
number in the range) — is a **merge count only**: it is **not** an
all-gates-audited claim, and it is not a test count.

## 4. What this page does not do (intentionally not done)

1. It does **not** rewrite `HANDOFF-CORRECTION.md`, any merged receipt, or any
   earlier record; the corrections are dated addenda.
2. It does **not** add or edit register entries:
   `docs/approvals/APPROVAL_REGISTER.md` has a zero-line diff in this change.
3. It does **not** re-run, re-open or re-label any GitHub check, and it does not
   re-open #723 or #729.
4. It does **not** correct the PR #723 body's loose "APR-047" reference that
   `HANDOFF-CORRECTION.md` §1.6 already flags; that is a **named follow-up**
   needing a metadata writer and owner authority.
5. It does **not** claim that any unrun check passed, and it creates no
   retrospective authority (D7).

## 5. How to re-derive the load-bearing facts

```
gh api repos/ModernNomad-98/Project-Aegis/pulls/729 --jq '{head:.head.sha,merge:.merge_commit_sha,merged_at:.merged_at}'
gh api repos/ModernNomad-98/Project-Aegis/pulls/729/reviews
gh api repos/ModernNomad-98/Project-Aegis/commits/f356157c633a28fc09aa9c98b50bddd90469dec9/check-runs
gh api repos/ModernNomad-98/Project-Aegis/issues/comments/6104148527 --jq .issue_url
git show c4fbee1d:docs/delivery-workflow.md   # then read L250-255 and L308-314
git grep -n -i -E '#729|PR ?729' 5a9adea0f2dce00c8ffe4be959ffb7e4a91ad566 -- docs/approvals/APPROVAL_REGISTER.md docs/reconciliation/
```

## 6. Dated addendum — the re-derivation recipe pinned (2026-10-12)

**The defect.** The §5 recipe's last command was merged unpinned. Run at the
revision that merged this page — `503c3b30`, the branch commit of PR #738
(merged as `09a5d2b3`) — `git grep -n -i -E '#729|PR ?729' --
docs/approvals/APPROVAL_REGISTER.md docs/reconciliation/` returns **9
matches**, all inside the D100 entry (L4566-4599) that the same change added to
`docs/reconciliation/step-0-reconciliation-v4.md`. The #729 close-out is
what D100 *corrects*; it is not what added D100, so the recipe cannot reproduce
the nil result §1 publishes beside it.

**The pin.** Both sites — the §1 bullet and the §5 fence — now carry the page's
own declared base, `5a9adea0f2dce00c8ffe4be959ffb7e4a91ad566` (L13), as
one argument before the `--` path separator:

```
git grep -n -i -E '#729|PR ?729' 5a9adea0f2dce00c8ffe4be959ffb7e4a91ad566 -- docs/approvals/APPROVAL_REGISTER.md docs/reconciliation/
```

At `…566` — the merge commit of PR #737, and `503c3b30`'s parent —
that command exits **1 with zero matches**, which is the result §1 states. The
original unpinned text is quoted here so it stays visible: `git grep -n -i -E
'#729|PR ?729'` over `docs/approvals/APPROVAL_REGISTER.md` and
`docs/reconciliation/`.

**Correct-forward note.** The two commands were edited **in place** on
2026-10-12 and nothing else in §1 or §5 changed. The SHA the repair prompt
printed, `5a9adea0f2dce00c8ffe4be959ffb7e4a91ad569`, **resolves to no
object**: `git cat-file -t` → `fatal: git cat-file: could not get
object info` (exit 128) and `git fetch origin …569` → `remote error:
upload-pack: not our ref`. The pin written is therefore `…566`, the
revision this page declares at L13 and the one on `origin/main`'s history.
