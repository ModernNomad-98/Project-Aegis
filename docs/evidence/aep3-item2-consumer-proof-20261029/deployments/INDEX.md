# Deployments — index

The deployment and served-bytes records carried by this bundle. Paths are relative to this directory.
This index exists so that records copied from the workspace keep their relative `INDEX.md` link
resolving; it is part of the bundle and is bound by the same manifest.

| File | What it carries |
| --- | --- |
| [`A-RESTORABLE.md`](A-RESTORABLE.md) | empty-target record, retained A bytes and the restore primitive (CP-14) |
| [`ITEM2-RELEASE-B-RECORD.md`](ITEM2-RELEASE-B-RECORD.md) | release B candidate, readiness and deployment record (CP-16) |
| [`R-RB1-RECORD.md`](R-RB1-RECORD.md) | restoration of retained A by dispatch (R-RB1, CP-20) |
| [`R-RB2-RECORD.md`](R-RB2-RECORD.md) | re-advance of retained B by dispatch (R-RB2, CP-20) |
| [`RB-DEPLOY-RECORD.md`](RB-DEPLOY-RECORD.md) | baseline A deployment record (CP-15 provider half) |
| [`READINESS-B-RECORD.md`](READINESS-B-RECORD.md) | release B readiness record |
| [`live-capture-after.json`](live-capture-after.json) | measured live capture of the served release-B bytes |
| [`live-summary-20261029.json`](live-summary-20261029.json) | live A/B serving summary on 2026-10-29 |
| [`pre-dispatch-pages.yml`](pre-dispatch-pages.yml) | the reviewed dispatch-only workflow bytes (CP-13) |
| [`provider-after-summary.json`](provider-after-summary.json) | provider summary of deployments at the target |
| [`provider-facts-cp16.json`](provider-facts-cp16.json) | provider facts captured for the CP-16 decision |
| [`rb1post-summary.json`](rb1post-summary.json) | post-R-RB1 provider and served-state summary |
| [`rb2post-summary.json`](rb2post-summary.json) | post-R-RB2 provider and served-state summary |
| [`release-A-manifest.txt`](release-A-manifest.txt) | retained release A manifest with per-file hashes and aggregate |
| [`release-B-manifest.txt`](release-B-manifest.txt) | retained release B manifest with per-file hashes and aggregate |
