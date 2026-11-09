# v0.2.0 release notes — DRAFT (not published)

**Status: DRAFT — not published.** This page is release-evidence preparation
only. No GitHub Release has been created, no tag `v0.2.0` exists, no asset has
been uploaded and nothing has been announced. The only existing tag in this
repository is `v0.1.0`; `v0.2.0` is a draft label used by this document.

**Draft date:** 2026-11-09.
**Prepared from:** live `main` at `ffae0e78622c1ac445a39873b3a5c20bbc78bc2c`
(tree `07b1f1eefa03ab85f7013cbe2f85250915cc529f`).
**Publication authority:** none. The owner's 2026-11-09 default authorises a
draft Release record only; the external publication act remains not performed and
is not performed by this document.

## What this draft would describe

The v0.1.0 tag is the last tagged revision. Since then the repository has merged
consumer-qualification, host-record and governance work.

**Merged identity:** PR #1001 merged 2026-11-09 at `3a420ed7378f6c726bfc6633315143fd6f832298` (head `98b5996391f7792309b6fdaeb36b0aeb31e98003`, tree `c100113651558bf504f8665f76cca944c133f032`).

The re-bound consumer
qualification record is 43,269 B /
`eb3630dbbb19fba657e537d797312f9d63a4804066af50212c438ca622652f79`.

This draft adds, in the same pull request that carries it:

1. a bounded AI-product reference profile (synthetic retrieval-grounded support
   assistant) under `docs/profile/`;
2. a data-only offline evaluation qualification slice under `docs/evaluation/`;
3. this release-evidence package under `docs/release/`.

Those three items are **proposed by that pull request**. They are not merged, not
published and not consumer-qualified by this draft; if the pull request does not
merge, they are not part of any release.

## Highlights (as they would read if merged)

- **Consumer packaging and qualification:** the consumer packaging manifest and
  its read-only verification are merged; the re-bound qualification record B at
  `3a420ed7` covers outcomes 1, 2, 3, 5 and 8 only.
- **Host record:** the offline capability slice for host compatibility was
  delivered in PR #1001; real-host qualification remains **UNRUN** and no host
  profile is selected.
- **AI-product reference profile:** one synthetic workflow composed from five
  existing skills, with a data card, citation contract, output schema, cost model
  and seven fail-closed negative cases. Design only; execution UNRUN.
- **Offline evaluation qualification slice:** ten synthetic cases over four
  kinds, ten expected-observation fixtures, and a recorded mock/offline run with
  zero network calls; the provider-backed judge and every citable verdict remain
  UNRUN.
- **Release evidence:** this draft, an asset manifest naming
  `tools/skills-manifest.json` (52,706 B /
  `774ef7bf81969518b424005a0b6b7ccd6c5f7fedf2b616b0e22d5b07732a5222`) and a
  privacy review checklist.

## Known limits

- **No live or paid run.** No provider, judge, credential, host probe or spend is
  part of this release evidence; the environment figures are not claimed.
- **No consumer install.** There is no install target and the install record
  stays UNRUN.
- **Not consumer-qualified:** outcomes 4 (Host Compatibility Qualification), 6
  (Behavioral and Consumer-Outcome Evaluation), 7 (Live-Evaluation Admission and
  Budget Recovery), 9 (AI-Product Engineering Profile), 10 (Release Evidence and
  Documentation) and 11 (Bounded Real-Execution Integration) remain owner-gated
  and are not qualified by this draft.
- **No publication act.** A draft is reversible and invisible until explicitly
  published; this document is not a Release and does not create one.
- **Asset identity is a measurement, not an approval.** The manifest's bytes and
  SHA-256 verify the file at the measured commit; they do not approve its
  content.

## Verification performed for this draft

| Check | Result |
| --- | --- |
| Asset path exists at the measured commit | yes |
| Asset bytes / SHA-256 round-trip | 52,706 B / `774ef7bf81969518b424005a0b6b7ccd6c5f7fedf2b616b0e22d5b07732a5222` |
| `docs/README.md` evidence-index count | corrected from 18 to 19 |
| Publication performed | **no** |
| Tag created | **no** |
| Asset uploaded | **no** |
| Privacy checklist completed | [privacy-review-checklist.md](privacy-review-checklist.md) |

**Prepared by:** Aegis Delivery Agent (DeepSeek Harness; configured route
`deepseek-flash`; serving model not observable). Draft record only.
