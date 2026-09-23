# CP-WP-003A offline capability proof review

Date: 2026-09-23. Authority: AEGIS-APR-006, effective at grant merge
`1af342712d27d5e6ea482b3f451106b4dccaf125`. Implementation branch:
`feat/cp-wp-003a-offline-proofs`. Candidate commit and independent reviewer
verdict are recorded in the PR after the exact head is frozen.

This increment tests synthetic failure handling only. It does not select or
verify a real authority, host, operation, evidence store, or billing source.
The public CLI remains synthetic-only. CP-WP-003 and CP-WP-004 stay BLOCKED.

## Negative proof map

| Fixture and invariant | Expected denial | Observed local test |
| --- | --- | --- |
| `SyntheticClaimSource`, shared controller/manual token | One winner; revoke, expiry, supersession, source outage and replayed loser deny; a local copy cannot authorize a distinct source | `test_manual_and_controller_race_one_source_token`; `test_source_revoke_expire_supersede_outage_and_distinct_copy` |
| `FreshnessProof`, restored sequence 7 after sequence 8 effect/charge | Independent anchor or complete current-source mismatch, unavailable or contradictory proof denies | `test_rollback_after_later_effect_or_charge_is_denied` |
| `ContainmentProbe`, injected unsupported host, live child, escaped descendant, timeout, lost fence, path swap, ACL failure | Every injected defect denies; no host is declared production capable | `test_containment_negative_matrix` |
| Temporary checked file, identity swap and second hardlink | Changed identity and multiple links deny on read-only probe | `test_offline_owned_path_probe_denies_swap_and_hardlink` |
| Canonical original evidence bytes in temporary file | Byte/hash, version, writer, binding, stage and sensitive payload failures deny | `test_evidence_original_bytes_binding_writer_stage_and_sensitive` |
| `SyntheticLiabilityBook`, lost/duplicate/contradictory and post-cancel receipts, restart checkpoint | Unknown amount reserves worst case and retains slot; contradictory or over-cap receipts deny; final exact bill settles | `test_unknown_billing_retains_worst_case_and_slot` |
| Coordinator with lookalike target | Deny before intent commit or adapter contact; all-synthetic reports still deny real dispatch | `test_unproven_target_denied_before_any_intent_or_contact`; `test_offline_report_never_grants_real_dispatch` |

## Commands and results

Windows PowerShell, local Python 3.14.7, no provider or network call:

```text
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tools.aegis_delivery_control.tests.test_capabilities tools.aegis_delivery_control.tests.test_platform.PlatformContractTests.test_offline_owned_path_probe_denies_swap_and_hardlink tools.aegis_delivery_control.tests.test_dispatch.MediatedDispatchTests.test_unproven_target_denied_before_any_intent_or_contact -q
Ran 9 tests in 0.016s — OK (exit 0)

$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest discover -s tools/aegis_delivery_control/tests -q
Ran 552 tests in 162.978s — OK (exit 0)

$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tools.behavioral_eval_runner.tests.test_canonical tools.behavioral_eval_runner.tests.test_pathsafe -q
Ran 16 tests in 0.005s — OK (exit 0)
```

Linux, cached local image
`mcr.microsoft.com/playwright@sha256:9bd26ad900bb5e0f4dee75839e957a89ae89c2b7ab1e76050e559790e946b948`,
Python 3.12.3, `--network none`, read-only repository bind mount, `umask 077`:

```text
python3 -m unittest discover -s tools/aegis_delivery_control/tests -q
Ran 552 tests in 109.007s — OK (skipped=3), exit 0

python3 -m unittest tools.aegis_delivery_control.tests.test_capabilities tools.aegis_delivery_control.tests.test_platform.PlatformContractTests.test_offline_owned_path_probe_denies_swap_and_hardlink tools.aegis_delivery_control.tests.test_dispatch.MediatedDispatchTests.test_unproven_target_denied_before_any_intent_or_contact -q
Ran 9 tests in 0.005s — OK, exit 0
```

The first Linux attempt used the container's default `umask 022`; owner-private
fixture checks correctly rejected its files (8 failures, 12 errors). The
`umask 077` rerun above is the valid local Linux result. Independent review and
exact-head GitHub Actions remain PR closeout gates. The owner-specified prior
CP-WP-003 total ETA was 12–24 active hours; this first increment is forecast
at 8–10 active hours, ceiling 10. Selected backlog total is 191–426 hours,
or 207–466 if both optional helpers are chosen. Implementation started at
2026-09-23 16:29:59 UTC; actual active elapsed time will be stated in the PR.

## Real dispatch gate

`require_real_dispatch` rejects every offline report, even if every synthetic
family passes. The following are still UNPROVEN: a source-atomic claim shared
with every manual and host consumer; independent anchor or complete current
source reconciliation and its custody; selected-host process containment and
fencing across actual executable I/O; actual evidence root/readers/encryption/
retention/cleanup; actual receipt and billing authority, cap and dispute path.
The owned-path probe is read-only preflight, not an open-time proof against all
same-principal races. No synthetic pass promotes any of these gates.
