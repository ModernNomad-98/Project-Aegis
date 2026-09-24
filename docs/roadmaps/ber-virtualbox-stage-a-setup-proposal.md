# BER R4/R5 Stage A: disposable VirtualBox host proposal

> **Proposal, checked 2026-09-24.** The owner chose a new disposable Linux
> virtual machine (VM) under their control and selected VirtualBox as the
> platform. No VirtualBox installation, VM creation, host probe or BER Stage A
> grant has been approved by those choices. The [capability decision](ber-selected-host-capability-decision.md)
> remains the authority and test-plan source.

## Why this host

Stage A would run existing **offline synthetic** checks on one named Linux
host. This can test POSIX path and process behavior that the current Windows
host cannot prove. A VM is an isolated computer simulated on the Windows host;
"disposable" means this one can be removed after its evidence is retained.
Passing Stage A would be a capability observation, not a production isolation
claim, permission for provider calls, or a BER baseline result.

| Choice | Reason and advantage | Cost and disadvantage |
| --- | --- | --- |
| VirtualBox base package on Windows, **selected** | Local VM under the owner's control; versioned command-line control supports repeatable setup. The base package uses GPLv3. | Public installer download and setup time; Windows administrator approval may be needed for its drivers. The Windows hypervisor is active on the checked host, and Oracle warns VirtualBox may run substantially slower with Hyper-V. Do not change Windows security or hypervisor settings merely to speed it up. |
| Hyper-V, considered earlier | Built into Windows Professional; no separate platform download. | The owner selected VirtualBox instead. Enabling Hyper-V requires administrator access and can interfere with VirtualBox. |
| Cloud VM | Avoids local installation. | Adds account, access, possible recurring charges and a different host boundary; no cloud spend or credential access is approved. |

**Guest recommendation:** Ubuntu Desktop 24.04 LTS, 64-bit. "Guest" is the
Linux operating system inside the VM; LTS is Ubuntu's long-term-support line.
Desktop has a graphical installer and terminal, which makes initial operation
easier for an owner new to Linux. Ubuntu Server is smaller and has no graphical
interface, but that saves little on this host and increases setup friction.
Oracle's current VirtualBox 7.2 documentation lists Ubuntu 24.04 LTS among
supported guests. Ubuntu 26.04 LTS is newer, but it is not yet listed there;
choosing 24.04 keeps the first proof on a documented combination. Ubuntu and
the VirtualBox base package have no task-controlled license charge; downloads,
disk use and human setup time remain costs. The optional VirtualBox Extension
Pack is unnecessary and has separate license terms, so omit it.

Sources checked 2026-09-24: [Oracle's 7.2 Windows installation guide](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/installation.html),
[host/guest combinations](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Introduction.html),
[Windows hypervisor interaction](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Troubleshooting.html),
[official 7.2.18 files and checksums](https://download.virtualbox.org/virtualbox/7.2.18/),
[Ubuntu 24.04 installer and checksums](https://releases.ubuntu.com/24.04/), and
[Ubuntu's VirtualBox walkthrough](https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox).
Version and license terms should be rechecked immediately before downloading.

The version-pinned public downloads proposed for that later provisioning
decision are:

| File | Official source | SHA-256 in the publisher's 2026-09-24 checksum list |
| --- | --- | --- |
| `VirtualBox-7.2.18-175117-Win.exe` (170 MB) | [Oracle file](https://download.virtualbox.org/virtualbox/7.2.18/VirtualBox-7.2.18-175117-Win.exe) | `aae27200546a21b9b7dc11cfc42bd04802329a29f69ae0ada55682715a389d8d` |
| `ubuntu-24.04.5.1-desktop-amd64.iso` (5.8 GB) | [Ubuntu file](https://releases.ubuntu.com/24.04/ubuntu-24.04.5.1-desktop-amd64.iso) | `4da4a0c9035da8e68a59a838674f403f0a54472c78a83b4fb7f78d03588f85a7` |

Verify the downloaded file hashes against the independently retrieved
[Oracle checksum list](https://download.virtualbox.org/virtualbox/7.2.18/SHA256SUMS)
and [Ubuntu checksum list](https://releases.ubuntu.com/24.04/SHA256SUMS)
before running either installer. Do not download the Extension Pack.

## Reviewable setup boundary

The read-only Windows inventory found Windows 11 Professional, hardware
virtualization enabled, and enough reported CPU, memory and free disk for a
modest VM. It did not find `VBoxManage`, the Hyper-V PowerShell module, or
`vmrun` on `PATH`; no VirtualBox installation or Linux VM was verified. The
Windows hypervisor reports active. The administrator-only feature query was
unavailable, so do not infer which Windows feature activates it.

Proposed host alias: `aegis-ber-stage-a-vbox`. Proposed starting resources:
4 virtual CPUs, 8 GiB memory and one dynamically allocated 60 GiB virtual
disk, subject to an exact preflight before creation. A virtual CPU is a share
of the host processor; a dynamic disk consumes host space as the guest writes.
The VM should have no bridged adapter, USB passthrough, shared clipboard or
drag-and-drop. Use only base VirtualBox features. Network access, if required
for the Ubuntu installer or public package updates, is limited to setup via
NAT (outbound sharing of the host connection); disable the VM network adapter
after the separately authorized source transfer and before running Stage A.
Do not place private labels,
provider credentials, sealed holdouts or production evidence in the VM.

Proposed non-admin Linux account: `aegisprobe`. Proposed scratch root:
`/home/aegisprobe/aegis-stage-a`, created and owned by that account. Use a
temporary, local-only source-transfer method with the exact signed commit and
tree pinned in a later grant. Do not leave any VirtualBox shared-folder
mapping before a capability test; a shared host mount would change the path
boundary being tested. Do not clone the private repository with credentials
inside the VM. Record exact installer hashes, VM settings, guest OS/Python versions,
source identity and the absence of shared folders/network in protected raw
evidence, then publish only a sanitized summary.

### Guided setup sequence after a provisioning grant

These are the planned steps, **not instructions to execute yet**. The agent
can automate downloads, hash checks, VM configuration and evidence capture.
The owner may need to approve Windows administrator prompts and set the
initial Ubuntu password privately. A later provisioning grant must pin the
host storage location and exact actions before either party starts.

1. Download only the two version-pinned files above from their publisher
   links. In PowerShell, `Get-FileHash -Algorithm SHA256 <downloaded-file>`
   must equal the corresponding publisher checksum. Stop on any mismatch.
   Run the VirtualBox base installer with the owner's Windows administrator
   approval; leave the optional Extension Pack uninstalled. Verify
   `VBoxManage --version` reports 7.2.18.
2. In VirtualBox Manager choose **New**, select the verified Ubuntu ISO and
   VM name `aegis-ber-stage-a-vbox`, and use the approved host storage path.
   Choose the manual Ubuntu install so the initial administrator account is
   set privately. Set 4 CPUs, 8 GiB RAM and a dynamic 60 GiB disk. Use one
   NAT adapter during setup, with no port-forward, bridge, host-only adapter,
   shared folder, shared clipboard, drag-and-drop or USB passthrough. Stop if
   VirtualBox cannot run beside the existing Windows hypervisor; do not alter
   Windows security features as a workaround.
3. Install Ubuntu Desktop through its guided installer with a distinct
   initial administrator account and private password. That account has
   `sudo`, meaning it can perform administrator actions in the guest. Create
   a separate ordinary test account in the Ubuntu terminal:

   ```sh
   sudo adduser aegisprobe
   sudo install -d -m 700 -o aegisprobe -g aegisprobe /home/aegisprobe/aegis-stage-a
   id aegisprobe
   ```

   The owner enters passwords privately. Do not add `aegisprobe` to the
   `sudo` group. Record Ubuntu and Python versions. Public OS updates, if
   allowed by the provisioning grant, happen during setup only.
4. If the provisioning grant explicitly names and permits this source
   transfer, build an archive from its exact signed commit, plus a SHA-256
   checksum and commit/tree receipt. Transfer
   the archive without a repository credential: start a temporary Python
   file server bound only to Windows `127.0.0.1`, then fetch from the guest
   through VirtualBox NAT's default `10.0.2.2` host-loopback address. Verify
   the archive checksum in Ubuntu, stop the file server, and keep the source
   under the `aegisprobe` scratch root. This method needs no Guest Additions,
   shared host mount or private Git credential. Oracle documents the NAT
   [host-loopback mapping](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/networkingdetails.html).
   If that mapping is unavailable, stop and review a different transfer
   method; do not open the file server to the LAN.
5. Shut the VM down. In VirtualBox Manager set **Settings → Network →
   Adapter 1 → Enable Network Adapter** to off; verify all other adapters
   are off and no shared folders are configured. The automated equivalent is
   `VBoxManage modifyvm aegis-ber-stage-a-vbox --nic1 none`, followed by a
   `VBoxManage showvminfo ... --machinereadable` check for every adapter.
   Boot Ubuntu and verify only the local loopback interface remains. A
   screenshot or command output with the VM settings can be retained as raw
   host evidence. This setup check still does not run the BER Stage A tests.

## Separate decisions and stop conditions

1. **Provisioning decision:** Review the exact VirtualBox/Ubuntu versions,
   download links and hashes, VM file location, resource limits, administrator
   actions, network allowance during setup, transfer method, time ceiling and
   cleanup plan. Pin the exact signed commit and archive boundary for the
   proposed step-4 source transfer. If transfer is not granted, skip step 4
   but still disable networking in step 5; a later grant must cover transfer.
   Only an explicit grant can authorize installation or VM creation. The
   owner may choose manual guided setup or agent automation.
2. **Stage A decision:** After the VM exists and its facts are verified, review
   and merge a BER-DEC grant pinning this host/account/scratch root, signed
   source, exact commands from the [source-only test plan](ber-selected-host-capability-decision.md#source-only-stage-a-test-plan--prepared-2026-09-24),
   allowed synthetic fixtures, evidence handling and stop conditions. A
   provisioning grant does not authorize that probe.
3. **Later Stage B:** Any effective tool-path or model-driven proof needs its
   own decision after Stage A review. No provider or private-data call is
   implied here.

Stop before host changes if installer checksum, license terms, available
resources, Windows hypervisor behavior, VM identity, guest permissions,
transfer isolation or scratch ownership differs from the reviewed setup.
Stop Stage A if any required test skips, host fact is unknown, the source
revision changes or the VM still has an active host share or network adapter.
Do not disable Windows security controls to make the VM run faster.
