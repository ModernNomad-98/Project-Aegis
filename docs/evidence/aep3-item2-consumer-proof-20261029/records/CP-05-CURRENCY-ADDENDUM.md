# CP-05 currency addendum — fresh-session readback at the newest install-state head

Date: 2026-10-29 ~06:29 PDT. Model: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness); observed session model line `claude-sonnet-5-5` (Claude Code, different vendor from the record writer).

## Why
The CP-05 PASS (revised criterion) was observed at `aep3-i2/startup-readback` 338ba82, one commit behind the newest install-state head. Currency gap: re-run the same readback at the newest install head so the observation matches today's install state.

## Run
- Target: consumer repo branch `aep3-i2/next-action-record` @ `3998af11df2781ebc993d145c3863f1ad33cd500` (108 files; fresh clone at `C:\src\_aep3_cp05_currency`; checkout clean).
- Prompt: exactly 74-byte prompt `https://github.com/ModernNomad-98/aegis-consumer-proof Resume.`; genuinely new `claude -p` process, cwd = fresh clone, no resume/fork/context; session exit 0; transcript saved at `evidence/cp05-currency-readback-3998af1.txt` (2,959 chars; sha256 below).
- Observed: **Role B** ("this is your product repo, ModernNomad-98/aegis-consumer-proof (Role B)"; Aegis source-library landmarks absent), no sibling-app redirect, no inherited source authority; read the `docs/project-state.md` PS-001 snapshot and the next action; made no writes; "Stage 0" does not appear as a requirement (revised criterion removes it).
- It could not re-observe live provider state (gh api approval denied; connector auth error) and correctly stopped rather than guessing — that is UNRUN provider state, not a Role-B failure.

## Effect on CP-05
CP-05 PASS (revised criterion) **now stands at the newest install-state head 3998af1**, not only at 338ba82. It remains a PASS on the install branch and **never on consumer main** (main carries no install). The freeze change-control note (R2 + independent review + new digests required before a reworded acceptance is used after a result exists) is unchanged and still labelled: this row is not counted against `case_set_sha256 48a28ba1...` without that R2 record; the owner authorized the revision explicitly, and the R2 recording is a residual closeout item.

## Artifacts
- Transcript: `evidence/cp05-currency-readback-3998af1.txt` (2961 chars / sha256 802ea101fa9fb4cc27fa8a5c5b522214162279304b778b7cd1c736d22b3dbbc8)
- This addendum: sha256 below; INDEX.md updated to list it.