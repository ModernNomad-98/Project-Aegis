# BorrowBoard v1 - consumer readiness worked install/run record

Status: readiness evidence artifact for a synthetic local fixture. Base main 36ee1554aec56ed60fa1d2534e9e70e8dfddaff4; bounded local readiness claim for this fixture only; no production readiness, real-user, second-host/production-deployment or live-model claim; no CI-green claim. Publication identity is ABSENT and post-merge-only; this record contains no self-hash of the JSON or of any publication. The exact readiness scope is section 9; historical no-readiness phrases retained in limit 6 and B10 are scoped to those historical records and superseded by the verification CONFIRM.

Claim labels used throughout: **OBSERVED** = recorded/observed in the evidence package named here; **REPORTED** = recorded input value; **UNVERIFIED** = not executed or not checked in this package. No label is a pass claim for CI.

## 1. Identities

| Item | Identity | Label |
| --- | --- | --- |
| Tested runtime | Node v24.19.0; Chrome 156.0.8078.47 (4,522,648 B); Python 3.14.7; Windows local synthetic host | OBSERVED |
| Tested product | BorrowBoard v1 app aggregate sha256 797e9f5a47b914c1f32024d659d038c88066e24d57e43fcc7ddf3b565b384322 | OBSERVED |
| App files | index.html 1,678 B / 34 LF / sha256 cd005dcd95059654c3a4c2f5d0d55b453f77f7cda62b6f744ac7c64627967739; styles.css 3,846 B / 57 LF / sha256 f1080bd08c5e8bd2ecc6980961474d96f448a76465beaa2dd74dcce59a43091e; app.js 20,775 B / 298 LF / sha256 648fef5d73dcadd353b9c56600e67c34e62c7b7428972c7cbfc278a234ba1d43 | OBSERVED |
| Runner | _A/consumer-workspaces/borrowboard-v1/runner/borrowboard-runner.mjs 26,985 B / 382 LF / sha256 e633937dd1c95c200ff7dafeaa2221428ebc9024b73a3b3df3b3755f5de4096f | OBSERVED |
| Serve | python -m http.server 8765 --bind 127.0.0.1 --directory "C:\src\Project Aegis\_A\consumer-workspaces\borrowboard-v1"; port 8765; verified HTTP 200, served 1,678 bytes, clean shutdown | OBSERVED |
| Design | DESIGN.md 9,423 B / 64 LF / sha256 695da1bb6b90faeb822dab457d8a98966af7ec08f9c01206bd24265a129033fd | OBSERVED |
| Owner verdict | OWNER-VERDICT-2026-10-26T1640-BORROWBOARD.md 3,495 B / 20 LF / sha256 8018b7531f25215788c81ab9f21e6d344a496276a1412382ec269c041357cdd0; APPROVE WITH CHANGES | OBSERVED |
| Publication | ABSENT / post-merge-only; no self-hash; to be bound via SD-F, merge receipt and immutable record after merge | OBSERVED rule, UNVERIFIED until post-merge |

The tested runtime and tested product are separate identities: the runtime is the local Windows host (Node, Chrome, Python); the product is the selected app files and runner at REV-3. The publication identity is intentionally absent: it is not the JSON, not this Markdown file and not any pre-merge self-hash.

## 2. Worked install/run record

The fixture was prebuilt at _A/consumer-workspaces/borrowboard-v1 by the build package; this record is the installed-run record, not a claim that the empty directory assembly was re-executed (see limit 1).

Commands executed from a fresh cmd process (literal quoted serve command):

    python -m http.server 8765 --bind 127.0.0.1 --directory "C:\src\Project Aegis\_A\consumer-workspaces\borrowboard-v1"

Then the fresh browser profile opened http://127.0.0.1:8765/index.html.

First-run observation (OBSERVED): HTTP status 200; served bytes 1,678; localStorage null; Home empty text "No tools yet. Add your first tool."; app data-state idle; h1 count 1; tool cards 0; accessibility node count 38; console borrowboard:ready observed. The recorded console also has a favicon.ico 404; favicon is not a required app asset and no app resource failed. Server shutdown record: stopped true; listening_after_stop false; clean_shutdown true. The local PID is omitted as non-essential; the local absolute workspace path is disclosed because it is part of the literal working command.

The quoted serve command itself was separately verified from a fresh process: STATUS=HTTP_200; CONTENT_LENGTH=1678; PORT_CLOSED_AFTER_SHUTDOWN=True (limit 5 records the earlier unquoted-path failure; no app change).

## 3. B01-B10 observation table

All rows observed at BUILD REV-3. Each row's result is PASS in the recorded journey evidence; the evidence column names the primary recorded artifact and its sha256. This table is a summary; raw CDP JSONL and result files remain the supporting evidence.

| Row | Result | Observed evidence (summary) | Primary evidence and hash |
| --- | --- | --- | --- |
| B01 | PASS | literal quoted serve; HTTP 200; fresh profile localStorage null; empty state; idle; h1 1; cards 0 | cdp-journey-2026-10-27T00-10-50-758Z.jsonl 4,709 B / sha256 e919d8cd54ac6369c1b6bc0facd040403d6385b9213f9eaa0e43deb1f7532d3e; serve evidence sha256 6c0c21847196a6748a0fc8197c6ef06508085569e97df29cfba72489dbff343f |
| B02 | PASS | design, plan, verdict and build identities recorded for the run | JOURNEY4.md 4,008 B / sha256 8321ae8da892dbc36c0b1890db493ce69f665f82a636867b2e61df8734b18d92 |
| B03 | PASS | owner design review APPROVE WITH CHANGES; design follows R1-R5 | owner verdict 3,495 B / sha256 8018b7531f25215788c81ab9f21e6d344a496276a1412382ec269c041357cdd0 |
| B03R | PASS | shipped runner preview; R1-R5 and R2_no_app_hook all true | cdp-preview-2026-10-27T00-12-29-302Z.jsonl 3,185 B / sha256 defbaa04f988ac141399e67c08ae46b6aeee9295f8d79ca75559ad3c3fa20d4e; summary sha256 a2c2d663c4ebb9e204058b99fe52f306868b3368c97a29f97c2bfa6e5d44901c |
| B04 | PASS | search filters to Hammer; no-results visible text "No tools match your search."; tool list hidden | cdp-journey2-2026-10-27T00-11-44-829Z.jsonl 3,018 B / sha256 4b3151f91fa9a493ff66081e4c08e8a4bbf6965bdc0540baa27146bfc554d74a |
| B05 | PASS | blank name "Enter a tool name." draft preserved; duplicate "This tool is already listed."; borrower "Enter the borrower's name."; due "Choose a due date." | same journey2 JSONL sha256 4b3151f91fa9a493ff66081e4c08e8a4bbf6965bdc0540baa27146bfc554d74a |
| B06 | PASS | one active loan; card Borrowed; loan borrower Alex, due 2026-11-02, returnedAt null; duplicate submit did not create a second active loan | same journey2 JSONL sha256 4b3151f9... |
| B07 | PASS | stale observer exact "This tool is not currently borrowed."; state unchanged; shipped runner stale-return also unchanged; return/cancel behaves with one loan | cdp-stale-return-2026-10-27T00-12-32-410Z.jsonl 465 B / sha256 320087260252c4ff474451c59c48aac2e546f6f1352a76f2f49d95ec0f20f363 |
| B08 | PASS | storage banner exact wording observed; state unchanged on failure; draft kept; retry recovered Hammer/Wrench/Pliers; banner hidden | cdp-journey2 JSONL sha256 4b3151f9... |
| B09 | PASS | 320/768/1280 innerWidth=scrollWidth; min button height 44; one h1; Search tools/Name/Note labels bound; ax node count 51 | same journey2 JSONL sha256 4b3151f9...; screenshots supporting-only (320/768/1280 hashes in journey package) |
| B10 | PASS | app hashes confirm tested product; recovery notes recorded. Historical executor note: the journey4 executor made no readiness claim at execution time; that note is superseded by verification3 CONFIRM and by this record's bounded section 9 statement. | primary: journey4.json 15,824 B / 464 LF / sha256 5150890eb930dee28583e59f4b58dbf2db401bbd4e48e76cc067fcd2e2084a33; app hashes above; prior journey2 JSONL 4b3151f9... is historical raw driver transcript only |

Journey summary (OBSERVED): B01-B10 all PASS at REV-3; B03R PASS; J-RES PASS; NEG-1..4 PASS; remaining UNRUN none. The complete journey record is journey4.json 15,824 B / 464 LF / sha256 5150890eb930dee28583e59f4b58dbf2db401bbd4e48e76cc067fcd2e2084a33.

## 4. Design review and R1-R5 refinement record

Owner operator Peter returned APPROVE WITH CHANGES at 2026-10-26 4:40 PM PDT in OWNER-VERDICT-2026-10-26T1640-BORROWBOARD.md (3,495 B / 20 LF / sha256 8018b7531f25215788c81ab9f21e6d344a496276a1412382ec269c041357cdd0). The design REV-2 (9,423 B / 64 LF / sha256 695da1bb6b90faeb822dab457d8a98966af7ec08f9c01206bd24265a129033fd) applies the five ordered refinements. Each refinement below is mapped to observed preview evidence from the shipped-runner preview (summary sha256 a2c2d663c4ebb9e204058b99fe52f306868b3368c97a29f97c2bfa6e5d44901c; raw JSONL defbaa04f988ac141399e67c08ae46b6aeee9295f8d79ca75559ad3c3fa20d4e).

| Refinement | Owner refinement (summary) | Observed preview evidence (OBSERVED) |
| --- | --- | --- |
| R1 | Home search trims and filters by name case-insensitively; no-results copy exact; search-input/search-empty hooks | filtered names [Hammer]; noResults searchEmpty true, text "No tools match your search.", list false |
| R2 | Runner overrides localStorage.setItem via CDP to throw QuotaExceededError once then restore; app keeps real try/catch, banner and Try again; no app fail switch | banner visible with exact R5 wording; state unchanged on failure; retry recovered persisted Hammer/Wrench/Pliers; appHasFailSwitch false; storage-save-failed event observed |
| R3 | Exact plan-5 state shape; one active loan per item; runner exports .borrowboard/state.json with sha256; checklist.json runner-only | keys items/loans/version; version 1; item keys id/name/note; loan keys id/itemId/borrower/dueDate/createdAt/returnedAt; activeLoanCount 1; exported state 402 B / sha256 1435b14e5577318ffd6a31fdab304f809174e9a2031dfee03cb8ae61f29a3f90 |
| R4 | Corrupted/unknown-version state copies raw bytes to borrowboard.v1.state.corrupt-<timestamp>; exact banner; all saves blocked until Start fresh confirmed | corruptBanner exact; corruptCopyMatchesRaw true; corrupt key present; blockedState still invalid; after fresh banner hidden and state null; unknown-version keys observed |
| R5 | Storage banner wording does not claim data preservation | banner text "Something went wrong saving your change. Your unsaved change may be lost. Try again."; noPreservationClaimInApp true |

Owner decisions recorded: Q1 approve (state shape per R3); Q2 approve (native date input); Q3 approve (disable plus one-active-loan check); Q4 alternative per R2 (runner-only storage-error injection); Q5 approve (inline plus aria-live summary). No new owner decision is requested by this record.

## 5. Interruption and resume record

Interrupted state (OBSERVED): runner-exported .borrowboard/state.json 326 B / 0 LF / sha256 d2ee9db958db0bdcb7859ee6c1b2171fbd79bdcb1a2d53cdcb3876befdfa4c1b. Fresh-session resume (OBSERVED): new Python server process and new headless Chrome profile/process; validates exported state; reads 2 items and cards [HammerBorrowedBorrowed by Alex, due 2026-11-02Return tool, WrenchAvailableBorrow]; state hash d2ee9db9... unchanged; J-RES PASS. No corrupted completion anchor was trusted. Evidence refs: state.json 326 B / 0 LF / sha256 d2ee9db958db0bdcb7859ee6c1b2171fbd79bdcb1a2d53cdcb3876befdfa4c1b; cdp-resume-2026-10-27T00-12-24-698Z.jsonl 425 B / sha256 7aa208de184034fa921b3d0d754749abc0b64f9412f2d77819a21d58447bffa7; journey4-binding-rev2.json 3,615 B / 114 LF / sha256 20b250da9b7d9bf88bbb4b1ace68c0dab33dd9da24568b73dcbfa93b11d91663.

## 6. NEG-1..4 isolated results

Each negative ran in its own clean copy/session. Before and after hashes are identical (OBSERVED), and the success-path state is unchanged.

| Negative | Result (OBSERVED) | Observed refusal | Before hash == after hash (full sha256) |
| --- | --- | --- | --- |
| NEG-1 missing required input | PASS / STOPPED | "Enter a tool name."; form still present; no write | d5e3ce6894e3bc1f75981d8026442d1110a1e2a1de8dae355c1236c8c8a5df5b (equal) |
| NEG-2 manual-only action without authority | PASS / REFUSED | manual-only action without authority; no state change | 30981d3ecf5be6169d92ad48891036ad2f72f8636eed8607170cc4c313e20acc (equal) |
| NEG-3 stale/revoked override | PASS / STOP | revoked/stale override; no state change | d70d868a2c903d7a34ffc2adb1595645e712b0d39dad14bed80673bee666e5cf (equal) |
| NEG-4 accepted-but-unrunnable | PASS / UNRUN | clickthrough host/runtime unavailable; success false; never treated as success | 59c7f21a9f3c4305ed247543e4964031dfd5a83a9cc629593383018df78aa499 (equal) |

NEG result evidence refs: cdp-negative1-2026-10-27T00-12-34-058Z-result.json 365 B / sha256 8bb1deff9c3cf8cd3b92c216216bcef30bdbb73c2745fc56abc6cfcab01ac409; cdp-negative2-2026-10-27T00-12-35-765Z-result.json 355 B / sha256 3ccbe899e2a776523f503820d18c4d85c5cc65141b473e6e9d67862f774901d5; cdp-negative3-2026-10-27T00-12-37-177Z-result.json 338 B / sha256 5f39a9571ffed774ea3e702e8ec06a19d291b749ac2f3a66e29f52972194600a; cdp-negative4-2026-10-27T00-12-38-609Z-result.json 384 B / sha256 8bcbbd244d431f3fe5f52990455b7f52f92b61129d02cf1fdf8411762753f28a. Each before hash equals its after hash as stated above.

## 7. Verification chain summary

| Stage | Record identity | Verdict |
| --- | --- | --- |
| verify1 | VERIFICATION.md 8,969 B / 83 LF / sha256 f0fe541ffb5fe66eea6052a5f326e24c59d9f5980fae6b0a7823bd610de1a4e6; verify-binding 2,357 B / 77 LF / sha256 3d3ae303e14806f6943da0e6559e0bde0f3baa04a28646314f9c989805cf38a9 | BLOCK (recorded; historical) |
| verify2 | VERIFICATION2.md 5,958 B / 49 LF / sha256 dff84a318d870b25e5fab03a2df725050a49b5547e020acf187f3da7a798dd38; verify-binding 4,588 B / 130 LF / sha256 08164b3646f503a8b1679043aeaed473426b3b43d7f05c9271e5b177d6856f02 | BLOCK on identity-chain references; content/coverage/aggregate checks pass (recorded) |
| verify3 | VERIFICATION3.md 4,735 B / 46 LF / sha256 d82d5e924eebd961581cae6da973177759c85bdbeb764133b90e8a7c2452bff7; verify-binding 3,441 B / 105 LF / sha256 8cf0dbc2d3ef13d13a3e82b33c94df68c7807d8d7bb5e7ef49c422b512f3d259 | CONFIRM (final; recorded) |

Final verification verdict: CONFIRM - identity correction and journey4-binding-rev2 resolve the verify2 blockers; aggregate recomputes; observations unchanged; artifacts may be authored/published with the disclosed limits. Verification itself makes no publication identity and no separate readiness claim; the CONFIRM supports the bounded fixture-readiness statement in section 9.

## 8. DISCLOSED LIMITS (verbatim from VERIFICATION3.md)

1. B01 empty-dir assembly was not re-executed; workspace prebuilt; literal quoted start and fresh first-run observed.
2. B07 resolution history: journey1 UNRUN -> journey2 GAP (invalid rewrite) -> journey3/4 REV-3 PASS; state history and final closure.
3. B08 first driver run false-negative from whitespace predicate; first raw run retained; final PASS.
4. B01-B10 used an independent evidence-directory driver because shipped runner has no journey mode; shipped runner preview/negative1-4/resume/stale-return independently re-run PASS.
5. Literal serve command first failed unquoted at path space; quoted literal verified HTTP200; no app change.
6. Tested-runtime vs tested-product separated; publication identity absent/post-merge only; screenshots supporting-only; no readiness claim.

Limit 6 is the verbatim executor/verification-stage limit; it does not contradict the bounded fixture-readiness statement in section 9, which the final verification CONFIRM supports. The production/real-user/second-host/live-model non-claims remain in force.

## 9. EXACT READINESS STATEMENT

**Readiness statement (OBSERVED, bounded local scope):** The accepted BorrowBoard acceptance journey (B01-B10 including the operator design review/refinement, interruption/resume and four isolated negatives) passed on the recorded tested-runtime and tested-product; this demonstrates local consumer-path readiness for the synthetic fixture. Not claimed: production readiness; real users; second-host or production deployment; live-model evaluation. No CI-green claim. Publication identity is absent and is bound only post-merge via SD-F, merge receipt and the immutable record.

Every claim above is labelled OBSERVED, REPORTED or UNVERIFIED where applicable; no unlabelled claim is made.

## 10. Evidence references and attribution

Primary package references (all relative to _A/evidence unless stated): borrowboard-design2/DESIGN.md; owner-decisions/OWNER-VERDICT-2026-10-26T1640-BORROWBOARD.md; borrowboard-build1/REVISION-3.md, REVISION-3-IDENTITY.md, AGGREGATE-PROOF.txt, build-binding-rev3.json, REV-3-TESTED-PRODUCT-IDENTITY.json; borrowboard-journey4/JOURNEY4.md, journey4.json, JOURNEY4-IDENTITY-CORRECTION.md, journey4-binding-rev2.json, INDEX.md, runtime-product-identity-rev3-verified.json; borrowboard-verify1/2/3 VERIFICATION*.md and verify-binding.json.

Identity corrections applied (OBSERVED): build-binding-rev3.json is 7,403 B / 241 LF / sha256 90fb59600af60ac93daf48b528cd25142d2a365adf5a510ec1fd6773605e1490; tested-product identity is 4,954 B / 140 LF / sha256 5494ca2a4b19745edea28f6a795044b5d1abca03da395489c3f8a464b5a17a4b (same bytes as validated copy); journey4-binding-rev2.json 3,615 B / 114 LF / sha256 20b250da9b7d9bf88bbb4b1ace68c0dab33dd9da24568b73dcbfa93b11d91663; identity correction 2,839 B / 34 LF / sha256 3edc24d3340b84b6010b9b37237d7c77da90f7e80f4a6be57cd4e6372a7ac39b; journey4 INDEX 6,071 B / 70 LF / sha256 c794f8088d0105b65f5baa0839b2ead1e4c9eb93ac084ab599e986f8b6dd3592. Superseded stale references are recorded in the correction; observations are unchanged.

Per-file sha256 is over raw bytes. index.html is CRLF (34 CR bytes), so its CR bytes are part of its raw hash; CR count is informational in the aggregate algorithm, while bytes and sha256 (hence CRLF) are inputs, so the aggregate is byte-sensitive. Recomputation from the current fixture files with the published algorithm produced aggregate 797e9f5a47b914c1f32024d659d038c88066e24d57e43fcc7ddf3b565b384322 (match); the recorded proof remains AGGREGATE-PROOF.txt 1,240 B / 26 LF / sha256 4b9833bbe3df3517152748967b76a67dacf47f6dc9a243661aa3e97577c12af4.

Evidence-store declaration: all _A/... references are an external immutable local evidence store, not committed by this PR; the two published artifacts are self-contained summaries. Every reference listed in this record and in the JSON carries a committed path plus byte/LF/sha256 identity, so a reviewer holding the local store can verify it; the PR does not copy the store into the repository. Local absolute paths are part of the literal working command and are disclosed; the operator name is disclosed because the owner design-review identity binds it; the local PID is omitted as non-essential.

Record authored by AI agent sd-a-pipeline-qa; model route DeepSeek-V41-Flash (registered id deepseek-flash @ deepseek-account; DeepSeek Harness). Evidence-authoring role only; this record is not a merge approval, not a CI pass and not a production/CI claim beyond the bounded readiness statement in section 9. No human intervention beyond the owner's operator design review/refinement (APPROVE WITH CHANGES; Q1-Q5; R1-R5) was required; no CI-green claim; publication post-merge only.
