# The starter installer's record guard — fail closed on an existing record, write atomically

**Item:** AEP3-I9, from the #966 gaps carried by the item 7 closeout.
**Status: LOCAL CANDIDATE.** Executed on one Windows host against a disposable
target tree. Nothing here is hosted CI, and no merge claim is made.

| Field | Value |
| --- | --- |
| Change commit | `44556a91928cade6b3af59e35ed4687c98c3b8ce` (branch `aep3-i9/record-guard`, base `e6947039a7597698f7c5c8b4c7f6d866bac80107`) |
| Files | `docs/consumer-starter-package.md` (+82/-36), `scripts/tests/test_validator.py` (+65/-2) |
| Host | Windows, PowerShell 7, Git for Windows `sh`, Python 3 |
| Model | DeepSeek V4 Flash (configured route `deepseek-flash`, DeepSeek Harness); the serving model is not observable from inside the session |

## 1. What the installer does now

The runnable block under `### 7.1` of the page gained three things:

1. `[switch]$AllowExistingRecord` — the explicit resume switch issue #966 asks for.
2. A preflight refusal, after the record-path containment walk and before the
   first directory or package write: an existing `-RecordPath` stops the run at
   **exit 24** unless that switch is passed. This removes the observed C7 outcome
   (files installed, exit 0, no receipt) instead of re-labelling it.
3. An atomic record write: P9 writes `$RecordPath + '.tmp'` in the record's own
   directory and renames it into place with `[IO.File]::Move(..., $false)`; a
   failed write removes a leaf temp file and stops at **exit 25**, leaving nothing
   at `-RecordPath`.

Codes 24 and 25 are in the section 7.2 table. The `P9: install record already
present, left unchanged` line is unchanged and is now reachable only with
`-AllowExistingRecord`.

## 2. Published block identity

Block = fenced body plus one trailing LF. Extraction is by heading with the same
fence logic the validator suite uses.

| Block | At `e6947039` | At `44556a91` | Equal |
| --- | --- | --- | --- |
| P2 gate | 6,493 B, sha256 `fd01fce7806c74e92f0fdf877c1cb58ed7704e8f24a316cccbce91b1dd7398ea` | same | **yes** |
| Section 7.1 harness | 21,977 B, sha256 `5b0393cc40ee7d2518299cff49e25a02f77aca970a4a6ce61d8c4bb061f0a0a0` | 23,366 B, sha256 `d00e886c5a1fb83d436e2055633094d46f1a85d1ef4da565b66466aa30384c48` | changed by +1,389 B |

The base identities reproduce the P2 and section 7.1 values item 6 and item 7
published (`destination-links-v1.md` section 1,
`ITEM7-FINAL-RECORD.md` section 2). That is the control that the extraction reads
the delivered blocks rather than a retyped copy.

## 3. Before and after, same cases

`evidence/prefix_behaviour.py` in the item workspace runs the three cases against
the block extracted from `origin/main`; the validator suite runs them against the
candidate block as committed.

| Case | Pre-fix | Candidate |
| --- | --- | --- |
| Existing `-RecordPath`, second run on a completed target | exit **0**, record and target unchanged, `P9: ... left unchanged` | exit **24**, nothing written, record byte-identical |
| The same run with `-AllowExistingRecord` | exit **1**, `A parameter cannot be found that matches parameter name 'AllowExistingRecord'` | exit **0**, record byte-identical, no package write |
| A directory occupying <<BT><record>.tmp` | exit **0**, record written, 42 files | exit **25**, no record, 41 package files |

## 4. Validator suite

`python -P scripts/tests/test_validator.py` at `44556a91`: **OK: 353**
gate self-test assertion(s), exit 0 (baseline 350; the three added cases are
S4-10, S4-11 and S4-12). S4-1..S4-8 are unchanged and pass. S4-9 (file
symbolic-link leaf) is **UNRUN** — the host has no administrator privilege, as in
item 6 and item 7. Six Linux-lane cases are UNRUN for the same reason recorded
there.

## 5. Other checks

| Check | Command | Result |
| --- | --- | --- |
| Skills validator | `python -P scripts/validate-skills.py` | **OK: 254** skill(s) valid, 0 warning(s), exit 0 |
| Markdown links | `check-markdown-links.py` over the CI page set (880 pages, 3 batches) | **0 broken, 0 dead**; 4,162 links, 1,135 anchors, exit 0 |
| Whitespace | `git diff --check origin/main..HEAD` | clean, exit 0 |
| DCO | `python scripts/check_dco.py --range origin/main..HEAD` | signed off, exit 0 |
| PR-body bound fields | `python -P scripts/ci/check_pr_body_skills.py --body-file` | **OK**, exit 0 |

## 6. Limits and UNRUN

- **No real process kill during the P9 write was measured for this record.** The
  deterministic case above proves the failure branch leaves no record, and the
  rename means a partial file at `-RecordPath` cannot exist by construction; a
  timed kill probe is left to the audit rather than claimed.
- The section 7.3 completion rule, the v1-to-v2 transition and cases C1-C8 were
  **not** re-run: this change does not alter the package list, the pin, the
  aggregate or the P2 gate, and item 7's evidence record remains the measurement of
  that transition.
- The `agent-commit` route, an external record path beyond S4-6, and the file
  symbolic-link leaf remain as item 6 and item 7 recorded them.
- Hosted CI is unrun: the branch is local and was never pushed.

## 7. Grant route

The only changed protected path is `scripts/tests/test_validator.py` (under
`scripts/`), so the PR is an AEGIS-APR-140 candidate; the two documentation
paths are unprotected and need no exception. The mapping and the pattern probe are
in `_A/work-package-3/item9-local/I9-STAGE-A.md`.
