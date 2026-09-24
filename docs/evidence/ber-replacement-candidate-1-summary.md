# BER replacement calibration candidate 1 — sanitized checkpoint

> **Current reading, checked 2026-09-24:** This page is a public, sanitized
> candidate-preparation record for the owner and reviewers. It contains no
> private cases or proposed per-item labels. The packet remains **PENDING**
> human label review; storage in the private repository is not approval to
> unseal holdout cases, call a provider, or ratify calibration. Use the
> [current Behavioral Eval Runner backlog](../roadmaps/behavioral-eval-runner-backlog.md#start-here-status-and-routes)
> for the remaining gates.

**Reading key:** Behavioral Eval Runner (BER) is the evaluation tool;
`BER-DEC` identifies an entry in its owner decision log; a pull request (PR)
proposes a repository change. Owner decision one (OD-1) is the later human
ratification of measured calibration. SHA-256 is the 256-bit Secure Hash
Algorithm used for exact-content identity; a command-line interface (CLI)
exposes commands. `OWNER_WAIT` means execution pauses for the owner's
required decision. `PASS` and `FAIL` are synthetic candidate-composition
labels in the table, not owner-approved gold verdicts. `CRITICAL` is the
highest reported quality-severity class. `LF` is the line-feed newline byte;
the checkout policy preserves the packet's exact bytes across platforms.
None of these labels changes the packet's PENDING status.

Prepared 2026-09-23 under BER-DEC-010 from Project Aegis source commit
`874750ea5d503b2f2711f520bd6de09bb1381b0b` (tree
`1339c9c6d2c95196899d72994d91136c73d2da55`); the preparation branch
was created directly from the BER-DEC-010 merge
`14e3f17c380dd26ddba1f27c7e041b6064509ba4`. The exact candidate inputs
are in the owner-only private repository
`ModernNomad-98/Project-Aegis-Calibration-Inputs`, proposed in its private
PR #1 at commit `6beba11e83e5e8a1655f33302e40959ecc6067e5`. No input
bytes or per-item candidate labels are reproduced here.

**Status: PENDING owner label review.** This is a candidate packet, not human
gold labels, a sealed-holdout freeze, provider authorization, measured
calibration, or OD-1 ratification. The private repository was verified PRIVATE
with only `ModernNomad-98` listed as collaborator and Actions disabled before
the first input push. Execution evidence remains under BER-DEC-008's external
root and 30-day controls; no provider request or execution evidence exists for
this candidate preparation.

## Opaque identities and local verification

| Artifact or check | Result |
| --- | --- |
| Candidate dataset semantic SHA-256 | `45b3279c382649a78cfc7d838cad81f7895b35841d48d3ca2563529e5c7e875a` |
| Candidate dataset file SHA-256 | `ca7304cbb59b98abdd883f3e9f7f323c82fc0df792a1d48f66d3208d621a1732` |
| Split map semantic SHA-256 | `7a6dcabbec1938c939ffa623e6c87834dcdb5e30dd4773d76bdee00cca5305d0` |
| Labeling guide file SHA-256 | `d36374797f45ef9bfc76ae0407d2beacdc34c3643cf981de4e949c291ac9d126` |
| Quality report file SHA-256 | `a2c7fbc9b6daeb869b820275421589e63fb5a38154fc2365a3fb711c51dd65be` |
| Repository contract and composition CLI | PASS, 160 distinct records; 40 development / 120 holdout; per control 2/2 development and 6/6 holdout candidate PASS/FAIL |
| Holdout distribution | 42 CRITICAL candidate FAIL; 40 adversarial, 20 candidate PASS / 20 candidate FAIL, 20 prompt injection / 20 role confusion; overlap reported in the private quality report |
| Same-control development/holdout normalized similarity | Worst 0.6275, below the 0.85 screening threshold; semantic independence still requires review |
| Full offline judgment input bound | Maximum 5,040 against the 8,000 ceiling; no provider call |
| Private manifest restore check | 10 packet files match SHA-256 manifest; staged Git bytes also matched; LF checkout policy pins bytes across platforms |

The private packet includes the versioned dataset, split map, guide, quality
report, hash manifest, source cards, builder/verification scripts and a full
owner review file. `owner-label-approval.json` is absent by design. The
builder uses the existing BER contract and closed judge-facing mapping. Its
quality report records the mechanical checks and explicitly leaves semantic
review pending. The public source contains no deterministic source for the
hidden holdout.

## Remaining gates

1. Peter Nguyen reviews all private transcripts, candidate labels, rationales,
   risk tags, split map and guide, then either requests a new version or
   explicitly approves exact bytes/hashes. The sole-human-labeler exception
   does not create an inter-rater-independence claim.
2. Reconcile changed dataset/guide/source pins and unknown historical usage;
   verify the current host, credential, provider project, remaining allowance
   and BER-DEC-008 preflight. A private commit alone grants no provider call.
3. Synthetic offline holdout execution support merged in
   [PR #249](https://github.com/ModernNomad-98/Project-Aegis/pull/249).
   Its production source and freeze pins remain unset. Development results
   lead to OWNER_WAIT; a later holdout freeze needs its own owner decision,
   and OD-1 follows measured holdout evidence.

The current `calibration_dataset.py` module docstring predates BER-DEC-010 and
describes the old external-only dataset location. BER-DEC-010 governs this
replacement input location; a future protected-source correction must be
reviewed under its own scope. No runtime loader or execution contract was
changed by this candidate packet.
