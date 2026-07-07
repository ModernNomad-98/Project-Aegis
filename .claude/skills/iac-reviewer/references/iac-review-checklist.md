# IaC Review Checklist Reference

Detail file for `iac-reviewer`. Loaded on demand.

## Blast-radius checklist (run FIRST)

- [ ] Renames without `moved` blocks / state moves → delete+create.
- [ ] Immutable-attribute edits (names, AZs, engine versions, key schemas)
      → forced replacement of stateful resources.
- [ ] `for_each`/`count` key or ordering changes → sibling reindex →
      destroy/recreate.
- [ ] Explicit deletions: what data lives in the deleted resource?
- [ ] Deletion protection / prevent_destroy / retain policies removed.
- [ ] Provider version bumps with known behavior changes on touched types.
- [ ] Module version bumps: diff the module's DEFAULTS, not just the caller.

## Exposure checklist

- [ ] Security groups / NSGs / firewall rules: new 0.0.0.0/0 or ::/0, broad
      CIDRs, all-ports ranges.
- [ ] Storage: public access flags, public ACL/policy grants, disabled
      block-public-access.
- [ ] Data stores acquiring public IPs / public endpoints; private-endpoint
      enforcement removed.
- [ ] Load balancers/ingress exposing services that were internal.
- [ ] DNS records pointing at internal resources.

## IAM/RBAC width checklist

- [ ] Wildcards appearing in actions, resources, or principals.
- [ ] Trust-policy / role-assumption changes (who can become this role?).
- [ ] Tenant-scoping conditions (tags, leading keys) loosened or removed.
- [ ] Cross-account / cross-subscription grants added.
- [ ] Service accounts gaining scopes beyond their workload.
- Findings always cite before → after width, not just the end state.

## Secrets & state checklist

- [ ] Literal credentials/keys/tokens in source, tfvars, parameter files.
- [ ] Secret values passed as plain resource attributes → captured in state;
      should be secret-store references.
- [ ] State backend: encrypted, locked, access-controlled; state not
      committed to the repo.
- [ ] Outputs exporting sensitive values without sensitive marking.

## Hygiene, drift & cost checklist

- [ ] Providers and modules version-pinned; registry sources trusted
      (route registry/source risk to `supply-chain-security-reviewer`).
- [ ] New resources tagged per the repo standard (cost attribution).
- [ ] Diff matches documented architecture; undocumented dependencies noted
      as drift (`source-of-truth-reconciler` when contested).
- [ ] New always-on/sized-up resources and egress-generating paths flagged
      with order-of-magnitude cost notes.

## Tool-specific sharp edges

| Tool | Sharp edge |
| --- | --- |
| Terraform | `moved`/`import` blocks absent on renames; `-target` applies leaving partial state; sensitive values in plan JSON |
| Bicep/ARM | what-if noise on nested deployments; `existing` references masking cross-RG coupling; deployment scripts running arbitrary code |
| CloudFormation | UPDATE_REPLACE on immutable properties; stack policies absent; drift detection unrun |
| CDK/Pulumi | review the SYNTHESIZED template when logic is dynamic; context/config flags changing synth output per environment |
