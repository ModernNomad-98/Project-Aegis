# BER R4/R5 Stage A: WSL2 Linux host proposal (revised platform decision)

> **Current reading, 2026-10-10.** This page is for the owner and the host
> reviewer. It records the revised choice of Linux test host for the
> Behavioral Eval Runner (BER, the repository evaluation tool) R4/R5 Stage A
> capability candidate. R4 is operating-system isolation and per-tool-path
> confinement; R5 is execution-profile observability and isolation. Stage A is
> the proposed offline host probe without model or provider calls.
>
> **Owner decision (2026-10-10, transcribed by the coordinator):** the owner
> selected **WSL2** as the platform for the BER R4/R5 Stage A Linux capability
> candidate, **superseding the VirtualBox path** chosen in
> [APR-028](../approvals/APPROVAL_REGISTER.md#aegis-apr-028-agent-assisted-disposable-virtualbox-vm-setup)
> reviewed proposal. The existing VirtualBox VM is **NOT deleted** — the owner
> rule stands: deletion requires separate approval plus operator confirmation;
> the VM stays untouched and unverified. This page proposes the WSL2 setup and
> its verification ONLY; it grants nothing. The
> [VirtualBox proposal](ber-virtualbox-stage-a-setup-proposal.md) remains
> published history; its platform choice is superseded for this candidate by
> the owner decision, and its stop-for-review wording is what this page
> honors: "Stop for review if the host, identity, isolation or software
> configuration differs materially from the approved setup" (APR-028).
> No BER Stage A host probe is authorized by this page.

## Why this host (updated platform-selection rationale)

Stage A would run existing **offline synthetic** checks on one named Linux
host. WSL2 (Windows Subsystem for Linux, version 2) is Microsoft built-in
lightweight Linux environment on Windows; a *distribution* is the installed
Linux userland. "Disposable" means the distribution can be removed after its
evidence is retained — removal is the same locked deletion rule as the VM
(§Separate decisions).

| Choice | Reason and advantage | Cost and disadvantage |
| --- | --- | --- |
| **WSL2 + Ubuntu 24.04, selected** | The WSL feature is already enabled and running on this host (probe facts below), so installing a distribution needs **no owner elevation**; the distribution arrives as a Microsoft-signed Store AppX (no third-party ISO download); kernel 6.18.33.2-2 and WSLg 1.0.73 are present; NAT networking is the default; it reuses the already-active Windows hypervisor platform with **no Windows feature change**. | Download and first-launch setup time; the distro image comes through the Microsoft Store channel, so the supply chain is Microsoft Store signing, not a publisher ISO checksum. |
| VirtualBox (APR-028 path), **superseded for this candidate** | Already installed and verified (7.2.20); the paused VM exists. | The owner selected WSL2 instead. The VM remains intact, powered-off, networking-disabled, and unverified; it is NOT deleted and NOT modified by this lane. |
| Hyper-V directly, **still rejected** | Built into Windows Professional. | Enabling or reconfiguring Hyper-V requires administrator access and changes Windows hypervisor features — explicitly forbidden. WSL2 already runs on the enabled platform; nothing is enabled or altered. |
| Cloud VM, **still rejected** | Avoids local installation. | Adds account, access, possible recurring charges and a different host boundary; no cloud spend or credential access is approved. |

**Probe facts (lead-run, read-only, 2026-10-10):** WSL 2.7.12.0 installed and
running on this host; kernel 6.18.33.2-2; WSLg 1.0.73; default distribution =
docker-desktop; WSL1 unsupported (irrelevant — the candidate is WSL2);
Windows build 10.0.26200.9448. Consequence: the WSL feature is already
enabled, so installing an Ubuntu distribution needs no elevation from the
owner.

**Distribution recommendation:** Ubuntu 24.04 LTS on WSL2. LTS is Ubuntu
long-term-support line; 24.04 matches the superseded proposal reviewed guest
choice, keeping the first proof on a documented combination. The WSL
distribution is installed from the Microsoft Store listing whose install name
is `Ubuntu-24.04`; the exact store name is **verified at C time** with
`wsl --list --online` (a documented WSL command) and quoted in the setup
receipt before install — this planning stage makes no network calls and
asserts no unverified listing detail.

**Supply-chain statement (honest):** the distribution arrives as a Microsoft
Store AppX — Windows enforces the Store signature chain at install; there is
**no third-party ISO** download, no manual checksum step of the kind the
VirtualBox path required, and no Extension Pack analogue. The Ubuntu WSL app
is Canonical published Store distribution delivered through the Microsoft
Store channel; inside the distro, any `apt` packages come from Canonical
archive over HTTPS, allowed **during setup only** (mirroring the superseded
proposal "public OS updates during setup only" boundary).

## Reviewable setup boundary

**Host alias:** `aegis-ber-stage-a-wsl` (distro name `Ubuntu-24.04`).
**Resources:** explicit `.wslconfig` entries `memory=8GB` and
`processors=4` to match the reviewed VirtualBox starting resources, written
only with owner confirmation; **defaults are acceptable** — WSL2 defaults
(capped host-memory share, all processors) are recorded in the receipt either
way. **Networking:** WSL2 NAT default; no port forwarding, no mirrored
networking, no `localhostForwarding` change. **No Windows interop changes:**
the default interop state is left exactly as WSL installed it (not a
boundary being claimed; the later, separately granted Stage A plan addresses
the guest-side interface state before tests, as the VirtualBox plan
disable-adapter step did). **No Windows security, hypervisor or feature
change** of any kind.

**Default user:** created by the owner at first launch (owner participation —
username choice, and a password **only if the owner wants one**; WSL own
behavior governs sudo prompting, and the plan asserts nothing beyond what the
owner actually configures, recorded in the receipt). The default user owns
`/home/<user>` and holds guest sudo. **Scratch root:**
`/home/<user>/aegis-stage-a`, created and owned by that user, mode 700.

No provider credentials, sealed holdouts, private labels or production
evidence enter the distribution. No source transfer is part of this lane
(mirroring APR-028 step-4 exclusion — a later, separately authorized
transfer pins its exact signed commit, archive boundary and method).

## Guided setup sequence (proposal; C executes only under the new grant)

1. At C, verify the store listing name with `wsl --list --online` and quote
   the `Ubuntu-24.04` entry in the receipt. Then `wsl --install -d
   Ubuntu-24.04` (no elevation required — feature already enabled).
2. First launch: the owner completes the Ubuntu default-user creation
   (username; password only if the owner wants one). Record
   `wsl --list -v` — the distro must show **VERSION 2**.
3. If the owner confirms explicit resources, write `.wslconfig` with
   `memory=8GB` / `processors=4`; otherwise record that defaults are in
   force. `wsl --shutdown` + relaunch applies any `.wslconfig` change.
4. Create the scratch root as the default user:
   `install -d -m 700 /home/$USER/aegis-stage-a`. No sudo-group additions,
   no password policy changes.
5. **Verification checklist — non-destructive commands ONLY** (each with a
   receipt): `cat /etc/os-release` (Ubuntu 24.04.x LTS),
   `uname -r` (kernel — expected 6.18.x series on this host),
   `ldd --version` (glibc), `id` (default user, uid 1000),
   `ls -ld /home/$USER` (ownership),
   `ls -ld /home/$USER/aegis-stage-a` (scratch root, mode 700 — the B-note
   addition), `df -h /`, `echo $PATH` (no
   repository paths), `wsl --status` (default version 2), `wsl --list -v`
   (the distro, VERSION 2, running). **This setup check does not run BER
   Stage A tests.**
6. Leave the distribution in its NAT-default, interop-default state; record
   the exact commands run and their outputs as sanitized evidence. No
   `wsl --unregister`, no `wsl --terminate` beyond step 3 shutdown
   application, and no action against the VirtualBox VM.

## Separate decisions and stop conditions

1. **Provisioning decision:** APR-028 scope is VirtualBox-specific, and the
   platform change is material, so APR-028 does **not** cover WSL2 work. Per
   the register conventions — "Grant entries are immutable. Append later
   revocation, expiry, consumption or supersession events with unique IDs and
   the affected grant ID; do not edit old entries. An action is covered only
   by an effectively ACTIVE human grant whose scope includes it" (register
   preamble, L8–12) — this lane records **both**: (a) a dated lifecycle event
   appended under APR-028 (annotate-don't-rewrite) stating the candidate
   platform supersession and that the VirtualBox VM remains intact,
   untouched and unverified; and (b) a **new AEGIS-APR-126 GRANT** whose
   scope mirrors APR-028 — one agent-assisted disposable WSL2 Ubuntu 24.04
   distribution setup with owner participation at first launch, NAT default
   networking, no sharing boundaries, and the same FORBIDDEN list plus the
   owner deletion rule. (Renumbering: the plan was audited as "APR-125";
   APR-125 was taken by the index-repair lane APR-114-CONSUMED event, per the
   D84 amendment, so this grant is **APR-126**.) The owner 2026-10-10 words
   are quoted verbatim in the entry. A separate BER-DEC grant is still
   required before the offline Stage A host probe.
2. **Deletion rule (owner, 2026-10-10, quoted):** the existing VirtualBox VM
   is NOT deleted — deletion requires separate approval plus operator
   confirmation. The same rule governs the WSL2 distribution:
   `wsl --unregister Ubuntu-24.04` IS deletion of the distro and is
   **FORBIDDEN** by this lane — disposability is by design, but disposal
   takes a separate owner approval plus operator confirmation.
3. **Stage A decision:** after the distribution exists and its facts are
   verified, a separately authorized BER-DEC decision pins this
   host/account/scratch root, the exact commands from the source-only test
   plan, allowed synthetic fixtures, evidence handling and stop conditions.
   This proposal does not authorize that probe.
4. **Later Stage B:** any tool-path or model-driven proof needs its own
   decision after Stage A review. No provider or private-data call is implied
   here.

Stop before host changes if the store listing name, WSL version, Windows
build, available resources, distro identity, guest permissions or scratch
ownership differs from this reviewed setup. Stop if any Windows
security/hypervisor/feature change would be needed as a workaround. Stop
Stage A (a later lane) if any required test skips or a host fact is unknown.

## Register, decision record and classification

- **Register treatment:** as above — an immutable-append lifecycle event under
  APR-028 plus the new APR-126 GRANT. The register conventions require the
  **new grant** (a material scope change is not covered by an entry whose
  scope names VirtualBox), and its immutability rule requires the **event**
  rather than any edit to APR-028.
- **Decision record:** §5 D-entry at the next free number after the latest
  entry at the implementation base — **D85** (D84 is the index-repair lane
  entry at this base; re-derived at base). Records the platform decision, the
  grant, the supersession event, and the deletion rule.
- **Classification:** the repository diff is **docs-only** (this proposal
  page, the register append, the D-entry — prose, no agent-instruction
  files). The host-side setup action itself is classified by effect and is
  covered by APR-126, not by a repository class. **Security answer: Yes** —
  the diff touches the
  [owner approval register](../approvals/APPROVAL_REGISTER.md), which
  CONTRIBUTING lists as a security-relevant surface; the PR template names it.
