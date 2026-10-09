# Signing-route audit — READABILITY-STALEROOT-1 and LINK-BOUND-1

Auditor: `/root/signing_route_audit`, Astra xhigh. This is a bounded read-only investigation, not delivery Stage C or D. Only this scratch report was written. Initial ETA: 10–20 active minutes. First captured start: **2026-10-09 13:58:53 UTC**. Finish and elapsed interval appear below; active time was not separately measured.

## Decision

The inspected checked-in Project Aegis policy requires a **Developer Certificate of Origin (DCO) signoff**. It does not establish a general requirement for a cryptographic commit signature. The installed Git help distinguishes the two: `git commit -s` adds a `Signed-off-by` trailer; `git commit -S` requests a cryptographic signature. The DCO checker reads commit messages and tests that trailer, without checking a cryptographic signature.

That repository policy does not silently erase an accepted task plan. READABILITY-STALEROOT-1 revision 1 explicitly says “signed-off/signed” and “No unsigned fallback”; LINK-BOUND-1's subsequent C/D records explicitly require signature verification. **Keep the existing C holds until a captured plan correction receives the required independent B acceptance.** The supported next step is a precise A/B terminology correction to require DCO signoff, retain immutable H/tree/base evidence and all other gates, and state that cryptographic signing is not added by that plan. This audit does not authorize a commit or supersede either plan.

No usable cryptographic signer was established by this audit. Both effective Git configurations have no `user.signingkey`, `commit.gpgsign`, or `gpg.*` setting. A bundled GPG executable exists, but its existence proves neither a usable secret key nor permission to use one. The coordinator reports that the chosen OpenPGP identity failed even in the elevated attempt. Key availability and live GitHub rules remain unverified.

The coordinator subsequently reported assigning READABILITY Stage A revision 2 and requiring fresh B acceptance before any Stage C retry. That is a routing update, not a claim that revision 2 or B is complete.

## Pinned local evidence and scope

Both inspected candidate checkouts resolved `HEAD` to `8e11c8f4c2777265e254057ce0fa1e52f0cf03bf` when read. This is a local source pin, **not a claim about current GitHub main**.

- READABILITY checkout: `C:\src\Codex Projects\Project Aegis\readability_staleroot\impl`.
- LINK-BOUND checkout: `C:\src\Codex Projects\Project Aegis\linkbound\impl`.
- Role A was verified locally: README starts `# Project Aegis`; `docs/skills-catalog.md`, `scripts/validate-skills.py`, and `artifacts/audits/skill-contract-audit-baseline.json` exist.
- `AGENTS.md` was read for role, evidence and stage rules. Its source bytes match across both checkouts. The same is true for CONTRIBUTING, delivery workflow, DCO checker and the applied skill, as independently hashed below.

| Artifact | SHA-256 observed |
| --- | --- |
| `AGENTS.md`, both checkouts | `BCEA3F367B80C6EF9D8FFC61AEB52A9868C907B94CE24C8989F697EA4931BCB1` |
| `CONTRIBUTING.md`, both | `2F52E51BB93FBAF0648409BA79368643AD8304621E1BC4AAE1EB50CAE4F650AF` |
| `docs/delivery-workflow.md`, both | `B509269A374C4570FBBB4F61F72B6DD1D6EBBE8D6A57BA30FC1D93B3E81F247A` |
| `scripts/check_dco.py`, both | `35F9575E26CCB9357AC7C93BE031B17883FF25C700B7AEF1B9204BB004641BB9` |
| READABILITY `PLAN-rev1.md` | `88B8EF6664C4FFF7F86E6E3DA988E5A206647831EC563450660FC7323AB9C1CB` |
| READABILITY `STAGE-B-AUDIT-rev1.md` | `36C28037B21A5345FA4C21815B85F9C4FB204835C8C16BEA21BF7BC57146F690` |
| LINK-BOUND `PLAN-rev1.md` | `82D2BC9B440C00C7A6AAF044C393CBCD8CAD509213D99BF14F168C9E35CF459C` |
| LINK-BOUND `STAGE-C-STATUS-ADDENDUM.md` | `AED72DF07B9C660BC9F699F52081F30F7A4E15BCED765A70D79C4329B51B5DEF` |

## Policy versus task requirement

| Claim and evidence | Type and reconciliation |
| --- | --- |
| `CONTRIBUTING.md:266–274`: “Sign off every commit” and “`git commit -s` adds the `Signed-off-by:` line.” `docs/reconciliation/step-0-reconciliation-v4.md:3013–3063` (D60) describes the well-formed trailer and its enforcement. | SHOULD: the canonical contribution requirement in the inspected source is DCO signoff. These passages do not require a cryptographic signature. |
| `.github/workflows/validate-skills.yml:238–260` invokes `scripts/check_dco.py` over the PR's commits. `scripts/check_dco.py:83,96–104,153–178,201–211` reads hash, author identity and message, then accepts a valid trailer or the two named bot exemptions. | IS: the inspected DCO implementation does not read or validate cryptographic signature headers. No exemption is being used or proposed for these human/agent contributions. |
| `docs/delivery-workflow.md:25–31` defines stage evidence; `:529–530` describes the DCO signoff check. `AGENTS.md:65–98` requires separated stages and the required reviewed head/checks. | SHOULD: immutable candidate evidence and independent review remain required. Neither these passages nor the exact-signature searches below establish a general cryptographic commit-signing mandate. |
| READABILITY `PLAN-rev1.md:101`: “create the signed-off/signed candidate … No unsigned fallback or approval-review workaround.” Its B audit `:81` repeats that the plan provides no unsigned fallback. | SHOULD: this accepted plan presently adds a signing constraint that C must not reinterpret silently. The targeted A/B correction is the proper place to make DCO-only wording explicit. |
| LINK-BOUND `PLAN-rev1.md:334`: “sign commits if publication is authorized.” C status addendum `:5` requires a signed commit and “verify its signature and DCO”; D audit `:71–81` calls for H/T/M plus signature/DCO evidence. | SHOULD: the original word “sign” is ambiguous, but the later agent records explicitly adopted cryptographic signing. Their C/D hold must be corrected transparently through the responsible stages, not ignored. H is still required; a staged tree alone remains insufficient. |

Negative-search scope was `AGENTS.md`, `CONTRIBUTING.md`, `docs/delivery-workflow.md`, `docs/approvals/APPROVAL_REGISTER.md`, `docs/reconciliation/auto-merge-policy.md`, `.github`, and broader docs/scripts results. Searches included `cryptographic`, `gpgsign`, `signingkey`, `gpg.format`, `gpg.program`, `gpgsig`, `signed commits`, `commit signatures`, `require_signatures`, `required_signatures`, and `signed_commits`. Historical “signed commit” or “DCO-signed” mentions are not treated as a universal cryptographic requirement. No current GitHub ruleset or branch-protection API was read, so an external required-signatures setting remains **UNKNOWN**.

## Owner-record check

Read the complete preserved `cifix/preg-d/owner-messages.md` (221 newline bytes) and `owner-askuserquestion-answers.md` (82 newline bytes), plus HANDOFF and the relevant redaction explanation. A second copy under `skillbatch/docs/evidence/session-handoff-2026-10-08/` has identical hashes:

- Owner messages SHA-256: `443F791038C41F7BFFABC0BB6841B1AA9191F351BFC52C8E31B8F2EF7392B061`.
- Owner answers SHA-256: `A4C4524FE069E8A7347D180F24C2E9E2EBAF5B73982C26B034705A620E45B255`.

The preserved owner words require separate stages, audited recommendations and green checks for merge. Searching both complete owner files for cryptographic/GPG/SSH/signing/signed/signature/signoff/DCO wording found no mandate for cryptographic commit signatures. The current task's pasted continuation request was also read; it adds no such requirement. A later session approval of publication for an already described “signed commit” is an approval of that finite action, not evidence of a standing cryptographic-signing rule.

Limits: the preserved owner record explicitly redacts two messages and excludes raw transcripts/per-agent transcripts. It does not prove that no owner has ever requested cryptographic signing. The referenced handoff commit `32f5ae25780c4802184a63d4063507fcf31b3a37` was unavailable in the READABILITY clone (`git cat-file -e`, exit 128 with lazy fetching disabled); this audit therefore relies on the matching preserved copies and their copy-log hashes, not a newly resolved GitHub snapshot. Reserved material was not retrieved.

## Actual meaning of an earlier “signed” handoff

`route002/STAGE-C-HANDOFF.md:3,16,40` describes H `8107f50a48cf31b68ab833976d5286b9f8a19c9e` as “signed” and separately names its DCO trailer. A read-only raw local object inspection in `route002/impl` gave:

```text
git --no-optional-locks cat-file commit 8107f50a48cf31b68ab833976d5286b9f8a19c9e
Read exit: 0
Header matches ^gpgsig(?:-sha256)? : False
Message matches ^Signed-off-by:   : True
```

The command output was retained in memory and reduced to these booleans, without printing identity details. Header and body were split at the first blank line; the header regex was anchored per line. `GIT_NO_LAZY_FETCH=1` prevented an object lookup from becoming a provider call. This proves that the cited local commit is DCO signed off and lacks a cryptographic signature header. It does **not** prove any live check outcome or authorize a different candidate. It does show why the word “signed” alone cannot support a cryptographic-signing requirement here.

## Nonsecret signing configuration and failure evidence

Executed in each candidate checkout:

```text
git --no-optional-locks config --show-origin --show-scope --get-regexp '^(user\.(name|email|signingkey)|commit\.gpgsign|tag\.gpgsign|gpg\..*)$'
git --no-optional-locks config --get-all user.signingkey
git --no-optional-locks config --get-all commit.gpgsign
git --no-optional-locks config --get-regexp '^gpg\.'
git --no-optional-locks config --get-regexp '^include(if\..*)?\.path$'
git --no-optional-locks rev-parse --show-toplevel --git-dir --git-common-dir
```

- READABILITY: only global `user.name` was returned from the allowed identity/signing filter. No persistent `user.email` or signing setting was returned. The coordinator's supplied commit command set name/email with command-scoped `-c` flags, explaining the attempted identity without assuming it was persistent configuration.
- LINK-BOUND: global name plus local `ModernNomad-98` name and GitHub noreply email were returned. Its Git common directory is `C:/src/Codex Projects/Project Aegis/cadence/impl/.git`; the worktree administration directory is that directory's `worktrees/impl`. Changes to common local configuration could affect other lanes; this audit made none.
- In both, the four individual signing/include queries above returned **exit 1 with no values**. No alternate SSH or X.509 signing route was configured in the settings read.
- `git --version` returned `2.55.0.windows.5`. `C:\Program Files\Git\usr\bin\gpg.exe` exists; its `--version` returned GnuPG `2.4.9`. The shell's `Get-Command` found Git and SSH keygen, not GPG on its direct PATH. Git's earlier attempted invocation nevertheless reached GPG; binary discovery alone is not the failure diagnosis.
- Installed primary documentation `C:\Program Files\Git\mingw64\share\doc\git-doc\git-config.html:5720–5734` says the default signing format is OpenPGP, with SSH/X.509 alternatives. `git-commit.html:975–983` says `-S` defaults to the committer identity; `git-config.html:10639–10649` says `user.signingKey` overrides key selection. These are local docs for the installed Git, not an external lookup.

**Failure evidence is reported, not independently reproduced.** LINK-BOUND `STAGE-C-HANDOFF.md:42` records the failed `git commit -S -s` with keyring permission errors followed by “No secret key.” The coordinator supplied the READABILITY command and sanitized failure details during this audit: command-scoped name/noreply email and `commit -s -S`; sandbox temp/pubring permission errors; elevated safe-directory retry ending with “No secret key”, `INV_SGNR 9`, `FAILURE sign 17`, exit 1. The safe-directory override addresses ownership trust; it is not a signer repair. No failed commit was retried in this investigation.

Inference, bounded: the attempted default signer was unavailable to those attempts. **Not established:** whether another key exists, whether an identity mismatch selected the wrong key, whether an agent/hardware signer is accessible elsewhere, whether a key is registered with GitHub, or whether remote policy requires cryptographic signatures. Absence of a Git setting is not absence of a secret key. No private-key directory, key contents, key list, credential/token store or provider setting was read.

## Audited recommendation and remaining work

1. Correct the ambiguous/agent-added task wording through a new captured A plan revision and a distinct B audit. Preserve DCO, immutable commit H/tree/base, exact-file scope, required checks, later independent stages and green-only merge authority. This follows observed repository policy; it is not a runtime fallback around the previously accepted text.
2. Keep C incomplete until that revised plan is accepted and the assigned C holder creates and validates its candidate under the existing authority. A GPG retry or configuration change is not supported by the current evidence, and is not recommended here.
3. Keep cryptographic status explicit in later reports: “DCO signed off” is demonstrated by its trailer/check; “cryptographically signed” requires separate evidence. The earlier ROUTE-002 handoff's word “signed” should not be reused as proof of cryptographic signing.
4. Before publication/merge, the responsible holder must establish the current applicable GitHub requirements. This offline audit does not decide remote required-signature policy, provider applicability, MG3, or the independent LINK-BOUND protected-file/green-only hold.

The recommendation was tested against the actual DCO code, canonical contribution text, both accepted plan records, owner-message copies, effective settings, installed Git documentation and a raw prior commit object. It does not depend on an assumption that missing config proves missing keys or that a historical PR determines current remote policy.

## Skill and intentional limits

Used `source-of-truth-reconciler`, `.claude/skills/source-of-truth-reconciler/SKILL.md`, SHA-256 `B5FD9FEDA97235430259913AEDD33447AB06E1C0DED281E9E131FA6BF9B78BE2`. Applied its IS/SHOULD split and evidence precedence to reconcile DCO policy, task wording, reported failures and observed configuration. No MANUAL-ONLY skill was invoked.

| Aegis skill | Agent / activity | Applied work | Evidence / limits |
| --- | --- | --- | --- |
| `source-of-truth-reconciler` | `/root/signing_route_audit` / read-only investigation, round 1 | Compared contribution policy, accepted plans, owner records, actual DCO code and nonsecret signing configuration; inspected one prior raw commit object. | DCO-only checked-in requirement proven at local M; agent-added cryptographic wording requires explicit A/B correction. No signer/key or current GitHub requirement proven. This is not a delivery-stage verdict. |

Intentionally not done: source/Git/configuration edits; commit/signing retry; key or credential inspection; signature verification; network/provider calls; new tests; PR publication; stage acceptance; merge. Only the requested scratch report was written. Existing source candidates were observed, not changed.

Timing: finish checkpoint **2026-10-09 14:04:51 UTC**, after the report was written and read back. Elapsed wall interval from the first captured start is **5 minutes 58 seconds**. Active time was not measured; this wall interval is an imperfect comparison to the initial 10–20 active-minute estimate. The timing line and final report hash were then finalized for handoff.
