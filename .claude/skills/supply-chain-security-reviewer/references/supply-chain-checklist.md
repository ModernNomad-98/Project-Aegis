# Supply-Chain Checklist — CI/CD paths, triage, pinning, provenance

Progressive-disclosure detail for `supply-chain-security-reviewer`. SLSA-style
framing: care about provenance (where artifacts came from) and integrity (that
they weren't tampered), not just CVE counts.

## Reachability triage rubric (for scanner output)

For each flagged CVE / advisory:

1. Is the vulnerable package a **direct** or **transitive** dep? (from lockfile)
2. Is the vulnerable **code path called** by this project, or only present?
3. Is it a **runtime**, **build/dev-only**, or **test-only** dependency?
4. Is there a **fixed version**, and does upgrading break anything?

Sort into:
- **TP-reachable** — called on a real path → severity per impact.
- **TP-latent** — present but unreachable → low/informational, note for hygiene.
- **False-positive** — not applicable (wrong OS, unused feature) → dismiss with reason.
- **Duplicate** — same root advisory via multiple paths → collapse.

Presence ≠ exploitability. A "critical" in an unreachable dev dep can rank
below a "moderate" in a reachable parser.

## CI/CD compromise-path catalog

| Path | Signal | Remediation |
|---|---|---|
| Untrusted trigger + secrets | `pull_request_target` (or self-hosted runner) that checks out PR code AND has secrets available | Split: untrusted build without secrets; privileged step on trusted code only |
| Over-broad token | `permissions: write-all` or default broad `GITHUB_TOKEN` | Least-privilege `permissions:` per job |
| Unpinned third-party action | `uses: someorg/action@v3` (mutable tag) | Pin to full commit SHA; review the SHA'd code |
| Secret in logs/artifacts | secrets echoed, or uploaded in build artifacts | Mask; never upload secrets; scope artifact reads |
| Cache poisoning | shared cache key writable by untrusted jobs | Scope cache keys; don't restore untrusted caches into trusted jobs |
| Script injection | `${{ github.event.* }}` interpolated into `run:` shell | Pass via env, quote; never inline untrusted event data |

## Install/build execution review

- Enumerate `postinstall`/`preinstall`/`prepare` (npm), `build.rs` (cargo),
  `setup.py`/build hooks (python), Dockerfile `RUN`, Makefile targets.
- Flag: remote downloads (`curl | sh`, fetching a blob), obfuscated/encoded
  commands, credential/env access, network calls during install.
- These run with developer or CI privileges BEFORE tests — treat as code exec.

## Dependency-specific risk

- **Typosquatting:** name close to a popular package (`reqests`, `lodahs`).
- **Dependency confusion:** an internal package name also resolvable on a
  public registry → attacker publishes higher version. Check registry/scope
  config, not just the lockfile.
- **Maintainer/abandonment:** sudden new maintainer, long-dead package
  suddenly updated, or unmaintained package on a critical path.
- **Surface bloat:** heavy/native deps for trivial needs widen the attack
  surface.

## Pinning & provenance checks

- Lockfile committed and used in CI (`npm ci`, `--frozen-lockfile`)?
- Integrity hashes present (subresource/`integrity`, `go.sum`, hash-pinned
  requirements)?
- Third-party actions pinned to commit SHA?
- Vendored binaries: documented source + checksum, or unexplained?
- Releases signed/attested (Sigstore/provenance) where the ecosystem supports
  it? Frame maturity with SLSA levels (source→build→provenance→hardened).

## AI/ML supply chain (OWASP LLM03)

Acquired AI artifacts are dependencies too — third-party base models,
downloaded datasets, and fine-tuning adapters. Review them like any untrusted
package. Scope: ACQUISITION. Integrity of data you curate or pipelines you run
(training sets, feedback loops, RAG ingestion) is `model-poisoning-reviewer`.

- **Serialization / format (code execution on load):** pickle-based formats —
  `torch.load`, `pickle.load`, many `.bin`/`.pt`/`.ckpt` checkpoints, and
  Python-code custom layers — execute arbitrary code when loaded. A downloaded
  model in these formats is install-time RCE. Prefer **safetensors**; treat
  pickle artifacts from untrusted sources as a critical finding unless scanned
  and sandboxed.
- **Pinning:** pin models/datasets to an immutable revision (commit hash /
  content digest), never a mutable hub tag or `latest` — the remote can change
  under you. An unpinned model reference is unpinned dependency risk.
- **Provenance & source:** which registry/hub, which publisher, is it the
  official upstream or a look-alike (model-name typosquatting on public hubs)?
  Is there a model card, license, and documented training provenance?
- **Integrity:** checksum/signature on the downloaded artifact; does the hub
  support attestation? Vendored model weights checked in without a documented
  source are unexplained artifacts.
- **Transitive AI deps:** the ML framework, tokenizer, and model-loading libs
  are ordinary package dependencies — review them in the dependency set above.

Boundary: a backdoored/poisoned artifact you DOWNLOADED is this skill; poisoning
of data you COLLECT or a model you TRAIN is `model-poisoning-reviewer`.

## Agentic supply chain (OWASP Agentic ASI04)

Agentic components are dependencies whose compromise grants AGENCY, not just
code execution — an installed MCP server answers your agent's tool calls.
Scope: ACQUISITION and update. Live message security between installed
components is `inter-agent-comms-reviewer` (ASI07).

- **MCP servers & manifests:** which registry/source, which maintainer, is
  it the official upstream or a look-alike (server-name squatting on
  registries)? Diff the manifest's declared tools/permissions against what
  the use case needs — permission width is the blast radius your agent
  inherits; a note-taking server declaring shell/filesystem/network tools is
  a finding at install time. Local-stdio servers execute on your host with
  your privileges: treat like any install-script risk above.
- **Pinning & update path:** pin servers/plugins to immutable versions
  (digest/SHA); a registry entry that can silently update is an unpinned
  dependency WITH AGENCY. Manifest changes on update are reviewed like
  dependency-code changes — a benign v1 that adds `exec` in v1.1 is the
  agentic version of a maintainer-change attack.
- **Tool/skill registries:** registry entries (skills, tool definitions,
  agent templates) are behavior-steering artifacts — review who can publish,
  whether entries are signed/attested, and pin what you consume. A poisoned
  skill/tool DESCRIPTION steers the model's tool choice even when the code
  is clean (the description is part of the attack surface).
- **A2A dependencies:** external agents your agents delegate to are
  supply-chain endpoints — source/operator trust, contract pinning, and the
  attenuated-authority rules of `agent-identity-privilege-reviewer` apply at
  acquisition; runtime authn/integrity is ASI07.
- **Transitive agentic deps:** an MCP server's own dependency tree (and the
  packages a plugin pulls) go through the ordinary dependency review above.

## HIGH-severity gate

A HIGH/CRITICAL finding must state a compromise path: weakness → attacker
action → **code execution or secret theft**. Reachable runtime exploit,
install-time script execution, an untrusted-CI-to-secret path, or loading a
pickle-serialized model from an untrusted source qualifies. A latent
unreachable CVE does not — rank it low and say why.

## Handoffs

- First-party SAST/CodeQL findings → `static-analysis-reviewer`.
- Integrity of curated training data / feedback loops / RAG ingestion →
  `model-poisoning-reviewer` (acquire-vs-ingest split).
- Live agent/MCP message security (authn, integrity, replay) →
  `inter-agent-comms-reviewer` (install-vs-runtime split, ASI04 vs ASI07).
- Applying an upgrade/CI change → separate classified, approved change.
