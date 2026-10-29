## Carried-advisories checklist — folded here per owner decision 2026-10-29 (~06:26 PDT)

Single checklist for #966; no separate items; no action until **AEP3-I9** picks them up.

- [ ] Extra non-skill selector row accepted by the selector layer (I4 advisory F1; mitigated by the native install test requiring 42 installed paths).
- [ ] `_starter_git` catches only `TimeoutExpired` (I4 advisory F2; call sites pre-check `shutil.which`).
- [ ] Case-sensitive duplicate detection (I4 advisory F6; exact duplicates rejected, case-differing non-skill pair not).
- [ ] Snippet-path trimming: §7.3 `$Src`/`$Tgt` trailing-backslash trimming + `$PSNativeCommandArgumentPassing` hardening (I7 14th-review carried advisories).
- [ ] S4-8 second declared record path has no block flag (I7 carried advisory).
- [ ] (Also listed here for one-stop tracking) CP-12.7 manifest-symlink gap is separately authorized and will be fixed on the CP-12 guard route; not part of AEP3-I9 scope.

**AEP3-I9 scope (separate, authorized):** fail-closed refusal when an existing `-RecordPath` is present (C7 footgun), atomic record write, external `-RecordPath` semantics — Stage A/B on branch now; merge under SDP-1a only if every touched path is inside APR-140/APR-143; otherwise one OWNER DECISION REQUIRED with path list + needed grant.