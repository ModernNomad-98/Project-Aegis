# C3.5 inbox configuration and disabled zero activity

**Scope.** The inbox is optional. This page records the explicit configuration,
the disabled-state verification and the local no-inbox path. It does not build
an inbox service, add a queue/provider/vendor, change the E1 installer beyond
the config surface or run an enabled inbox.

**Audience and reading key.** For Project Aegis maintainers and reviewers of the optional inbox configuration. **aegis.ops-inbox/v1** is the local synthetic config/evidence schema; **selected_by** records the selecting identity; **config_identity** is the canonical hash of the config; **INBOX_HIDDEN_ACTIVITY** is the refusal when a disabled inbox shows activity; **INBOX_CONFIG_INVALID** is the refusal for malformed values; **C4.1** is the qualification support matrix; **E2.4** is the independent consumer exercise; **E1** is the installer/config surface; **QUALIFIED** means independently exercised; **UNRUN** means not executed and never a pass.

## Configuration

`aegis.ops-inbox/v1` carries two explicit booleans:

- `config["inbox.supported"]`
- `config["inbox.enabled"]`

The selected configuration is recorded with `selected_by` and a
`config_identity` equal to the canonical hash of the config object. Missing,
non-boolean, whitespace or ambiguous values are refused. The inbox is never
inferred or auto-enabled. `enabled=true` requires a separate authority ref and
is **out of scope** for this slice; a disabled inbox does not carry or claim an
enabling authority.

The simplest configuration is no inbox. That is a supported state, not an
error.

## Disabled zero activity

A disabled claim needs an **end-to-end observation**, not just a static config:

```
"evidence": {
  "kind": "END_TO_END_OBSERVATION",
  "disabled_run_ref": "...",
  "activity": {
    "polling": false,
    "handshake": false,
    "external_reporting": false,
    "background_task": false,
    "network": false,
    "provider_call": false,
    "queue_activity": false
  },
  "observed_at": "...",
  "source_ref": "...",
  "independent_confirmation_ref": "..."
}
```

All seven activity fields must be present and `false`. One true field is
`INBOX_HIDDEN_ACTIVITY` and the claim fails. `independent_confirmation_ref` is
carried because the end-to-end run is primary; the static config is supporting
evidence only. This slice adds no telemetry of its own: the observation uses existing
process/event/network/queue evidence available to the programme.

## Display

The disabled display is exactly:

> inbox disabled - zero associated activity

It is not progress, not approval and not an implication of hidden activity. An
enabled/disabled state never grants authority and never hides assurance
limits.

**Claim status.** The disabled zero-activity claim is **NOT ASSERTABLE** in
this slice: the real disabled run, the independent confirmation and the E2.4
exercise are UNRUN.

## Local no-inbox path

A bounded local operation must complete without the inbox, with `local_path_evidence`
recorded, honest assurance limits and recovery from durable state. The C4.1
matrix records this as a configuration cell; an independent exercise (E2.4) is
required before a QUALIFIED claim.

## No new dependency

`dependencies` must be empty. No queue, service, provider or vendor is added;
the inbox remains optional and the simplest install has no inbox dependency.
This page does not change the E1 prerequisites; it consumes the existing E1 config surface by reference.

## Commands

Run from the repository root:

```
python -m tools.aegis_ops inbox --input tools/aegis_ops/tests/fixtures/inbox-disabled-valid.json
python -m tools.aegis_ops inbox --input tools/aegis_ops/tests/fixtures/inbox-invalid-value.json
python -m tools.aegis_ops inbox --input tools/aegis_ops/tests/fixtures/inbox-zero-activity-evidence.json
```

Expected: disabled-valid exits 0; invalid-value exits 1 with
**INBOX_CONFIG_INVALID**; hidden-activity exits 1 with
**INBOX_HIDDEN_ACTIVITY**. The complete input shape is the fixture set under
tools/aegis_ops/tests/fixtures/.

## UNRUN

A real disabled run, the independent confirmation and the E2.4 exercise are
**UNRUN**. The E1 config surface and E2/E4 presentation are consumed by
reference; this slice does not implement them.
