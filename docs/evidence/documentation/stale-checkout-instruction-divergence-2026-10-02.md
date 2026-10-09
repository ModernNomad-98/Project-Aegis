# Stale root checkout serves divergent instruction and skill content — 2026-10-02

**Reading aid (2026-10-09; added after the original measurements).** This page is for a new maintainer or coding agent checking whether a checkout can supply current Project Aegis instructions.
It records what was observed on 2026-10-02; its paths, commits, counts, and tool availability are historical, not today's checkout state.
For normal work, use the current [startup instructions](../../../AGENTS.md) to identify the workspace and verify its state.
The [readability ledger](../../roadmaps/aegis-documentation-readability-backlog.md) tracks this page's review status.
See the dated erratum at the start of section 3 before using its historical count command.

**Reading key.** SHA stands for Secure Hash Algorithm; this page uses 'SHA' as shorthand for a Git commit identifier.
Short forms such as `00717aa4` name the leading characters of a full identifier. `HEAD` is the commit checked out locally. `origin/main` is a local remote-tracking reference to the last fetched `main`, not a live server query.
The *root* and `coord-main` names refer to the two historical local checkouts measured here; `canonical` refers to the fetched main revision used for that comparison. `L78` means line 78 of the cited file at that revision.
A *regex* is a text-matching pattern.
A Git blob holds file contents; a worktree is a checked-out working directory.
CRLF means carriage return plus line feed; LF means line feed.
They are two line-ending encodings. `pwsh` is PowerShell, VM means virtual machine, and `pip` is Python's package installer.
The named `acceptance-core` check examines Scenario A evidence; it was not run in the historical measurement.
The `M`, `A`, and `D` labels in the path table mean, respectively: present in both compared trees with different contents; added on main; and present only at the root revision.

**Command notation and effects.** Replace `<checkout>` or `<root>` with the intended checkout path, `<sha>` with a commit identifier, `<rev>` with a selected revision or commit, and `<path>` with a repository path; quote paths containing spaces.
These angle-bracket names are placeholders, never literal shell input or redirection. `file` and `f` are scratch output filenames, not repository objects.
For PowerShell .NET file methods, pass a quoted path string even when the path has no spaces (or a variable containing a path); for example, `[System.IO.File]::ReadAllBytes('f').Length`.
A displayed `git fetch` contacts the remote and updates local Git metadata; `git ls-remote` queries remote refs without updating those local refs.
The displayed `git diff`, `rev-list`, `rev-parse`, `show`, and `cat-file` queries read local state.
In `git ls-files --eol`, `w/` describes the working file, `i/` Git's index (staged copy), and `attr/` the applicable line-ending attribute.
Other displayed Git inspection commands (`merge-base`, `ls-tree`, `ls-files`) read local state; the PowerShell file inspectors read local files, while the validator executes a local check.
A `>` writes or overwrites the selected scratch file.
The command block below is historical evidence, not permission to run it or modify the measured checkouts.

**Scope.** Measured 2026-10-02, read-only, on `ModernNomad-98/Project-Aegis`. Base:
`origin/main` re-derived after `git fetch origin` = `2f01ac6aad7cb8df92b810d149adf954c9902d2b`
(`git ls-remote origin refs/heads/main` returned the same SHA), 15 commits past the
`38cd81ba` this round's brief named. This page records a hazard; it authorizes no edit to any
instruction file or skill.

## 1. The hazard — the stale checkout teaches a different rulebook

`C:\src\Project Aegis\Project-Aegis` owns `.git` and is checked out at `00717aa4`
(`docs/maintainer-guides-readable`). `git merge-base --is-ancestor HEAD origin/main` exits 0, so it
is a **1,217-commit-old ancestor** of main, not a divergent fork.

| Copy | `AGENTS.md` bytes | Command | Merge-gate rule present? |
| --- | --- | --- | --- |
| root working copy, `Project-Aegis\AGENTS.md` | **3,548** | `(Get-Item <path>).Length` | **NO** |
| `coord-main\AGENTS.md` | **11,410** | `(Get-Item <path>).Length`; `git cat-file -s 797ca687:AGENTS.md` = 11,410 | yes |
| canonical `origin/main:AGENTS.md` @ `2f01ac6a` | **12,022** | `cmd /c "git cat-file blob 2f01ac6a:AGENTS.md > f"` then `[System.IO.File]::ReadAllBytes(f).Length`; `git cat-file -s` agrees = 12,022 | yes |

Presence test — whole-file regex counts over `[System.IO.File]::ReadAllText(<path>)`:

| Probe | root | coord-main | canonical |
| --- | --- | --- | --- |
| `exact head being merged` | 0 | 0 | 0 |
| `head being merged` | 0 | 1 | 1 |
| `merge gate` | 0 | 1 | 1 |
| `every required review` | 0 | 1 | 1 |
| `merge authority` | 0 | 2 | 2 |

The sentence named in this round's brief is **hard-wrapped**: in `2f01ac6a:AGENTS.md`, L78 ends
"…passed at the exact" and L79 begins "head being merged…" (merge gate at L78–L80, L99). So
`'exact head being merged'` reads 0 in **all three** copies and cannot discriminate between them —
it counts line breaks, not rules. The other four probes discriminate, and they give the substantive
result: the stale root copy contains **zero** occurrences of every merge-gate phrase. It also
carries none of the canonical rules at L15 (teach build choices), L27 (dogfood skills), L46 (audit
your own state), L60–L101 (coordinator role, one stage per agent), or L102 (name and time every work
item). An agent that reads the root copy would not learn that the merge gate exists.

A prior agent reported — as relayed to this round, its session unavailable here — that it "hit stale
content on its first reads and re-verified everything", and that the stale `AGENTS.md` "does NOT
contain the merge-gate text". **Cited as reported-by-an-agent.** The byte counts and the zero-probe
row above are the verification that does not depend on that report.

## 2. Blast radius — the divergence is not confined to instruction files

`git -C <root> diff --name-status 00717aa4 2f01ac6a -- .claude/skills`, with the working tree first
shown to match HEAD (`git status --porcelain -- AGENTS.md CLAUDE.md .claude/skills` printed nothing;
both working copies are clean for these paths):

| Path group | content differs (M) | only on `origin/main` (A) | only at root HEAD (D) |
| --- | --- | --- | --- |
| `.claude/skills` | **591** | **58** | **4** |
| `AGENTS.md` + `CLAUDE.md` | `git diff --stat`: `AGENTS.md \| 105 +…`, `CLAUDE.md \| 4 +--`, combined `104 insertions(+), 5 deletions(-)` | | |

Files under `.claude/skills`: **764** on `origin/main` vs **710** at root HEAD and **710** on disk
(`git ls-tree -r --name-only <rev> -- .claude/skills`; `Get-ChildItem -Recurse -File`). `SKILL.md`
files: **196** vs **185** — the root checkout is missing 11 skills outright; the 4 files only at root
HEAD are the deleted `system-prompt-leakage-reviewer` skill.

The stale tree also validates differently. Run inside the root checkout,
`python -B scripts/validate-skills.py` prints `OK: 184 skill(s) valid, 0 warning(s)` and exits 0;
the same command in a worktree created at `2f01ac6a` prints `OK: 195 skill(s) valid, 0 warning(s)`.
An eleven-skill gap with zero warnings is the failure mode this page exists to make visible.

The "good" copy is not canonical either: `coord-main` is at `797ca687`, **15 behind and 2 ahead** of
`origin/main` (`git rev-list --count HEAD..origin/main`; `origin/main..HEAD`), its `AGENTS.md` is 612
bytes shorter than the canonical blob, and 7 of its `SKILL.md` files differ (8 changed paths: those
7 plus `AGENTS.md`).

Swept: `AGENTS.md`, `CLAUDE.md`, `.claude/skills/**`. **Not swept:** `.claude/agents/*.md` (7 files
on main) and any other instruction surface.

## 3. The rule — a detectable check, not advice

**Erratum (2026-10-09; original command and results preserved below).** The comment `"0" = at the tip` is too strong.
In `git rev-list --count HEAD..origin/main`, zero means no commit reachable from the locally cached `origin/main` is missing from `HEAD`; `HEAD` can still be ahead.
For a local comparison, run `git rev-parse HEAD origin/main` and compare the two full IDs: equality establishes that these two local refs name the same commit. `git rev-list --left-right --count HEAD...origin/main` shows the commits exclusive to each side: `1 0` is an ahead-only example, while `0 0` is the equal-ref case.
These are examples of command meaning, not new 2026-10-02 measurements.
Even equal IDs do not prove the local `origin/main` still matches the server; that reference reflects the last successful fetch.
The historical `0` below therefore cannot, by itself, certify equality or current server freshness.

Read instruction or skill content only from a checkout that passes this test; otherwise read the
blob directly.

```text
git -C <checkout> fetch origin
git -C <checkout> diff --quiet origin/main -- AGENTS.md CLAUDE.md .claude/skills   # exit 0 = safe to read
git -C <checkout> rev-list --count HEAD..origin/main                              # "0" = at the tip
```

Measured on 2026-10-02: the stale root exits **1** and prints **1217**; a worktree created at
`2f01ac6a` exits **0** and prints **0**. Either non-zero result means: read
`git show origin/main:<path>` instead of the working tree (use
`cmd /c "git cat-file blob <sha>:<path> > file"` when a byte count is needed), and do not treat that
checkout's own tool output — including its validator's skill count — as main's.

Cheap pre-read proxy, also measured: `(Get-Item AGENTS.md).Length` must equal
`git cat-file -s origin/main:AGENTS.md` (12,022 = 12,022 in the clean worktree). The proxy is
one-directional: a mismatch proves divergence, but a match does not prove identity, because line
endings move the on-disk count without changing content — root's working file is 3,548 bytes
`w/crlf` against its own 3,525-byte `i/lf` blob (`git ls-files --eol`), and git still reports it
clean.

## 4. Origin — self-attributed

The coordinator of this round owns this. It dispatched agents with instruction-file paths that
resolve under the stale root checkout while warning them not to trust that checkout, and it reported
the merge-gate presence test as `-match 'exact head being merged'` — a probe that reads 0 in all
three copies because the sentence is wrapped, so a verdict of "yes" for `coord-main`/canonical and
"no" for root came from a test that cannot separate them. No agent authored the divergence; that
working copy simply has not been updated in 1,217 commits.

Observed this round, recorded as an observation rather than a diagnosis: while the stale copy was
being measured, this session received the root checkout's `AGENTS.md` and `CLAUDE.md` as auto-loaded
instruction content. A session can therefore be governed by the stale rulebook without deliberately
reading it. The trigger (reading a path under the stale checkout) is inferred, not isolated by
experiment.

## 5. Honest limits

- The prior agent's report is cited as reported-by-an-agent; its session was not available here, and
  this page does not verify that it re-verified anything.
- Not determined: why the root working copy sits 1,217 commits back, whether anything consumes it
  deliberately, or why it has CRLF endings while `core.autocrlf=false` and no `.gitattributes` is
  present at root (`git ls-files --eol` → `i/lf w/crlf attr/`).
- Not swept: the other lane worktrees, `rv629b`, `wt-*`, `wt-baseline`. Only the root checkout and
  `coord-main` were measured against `origin/main`; their staleness is unknown, not assumed.
- Byte counting was done for `AGENTS.md` only. `CLAUDE.md` and the skill trees were compared with
  `git diff --name-status`/`--stat`, which is content-exact but not byte-counted.
- The model note named in this round's brief, `process-issues-and-prevention-2026-10-02.md`, is **not
  on `origin/main`**: `git cat-file -e 2f01ac6a:docs/evidence/documentation/process-issues-and-prevention-2026-10-02.md`
  exits 128 and no `process-issues` path exists on main. It lives only on the unmerged lane
  `docs/process-issues-and-prevention` at `3393520a`, which is not an ancestor of main
  (`merge-base --is-ancestor` exits 1), and was read from there read-only for structure. The only
  2026-10-02 note on main is `acceptance-conversion-process-2026-10-02.md`.
- No provider, host, or VM verification. `pwsh` is not installed on this host, so `acceptance-core`
  and the pip-install steps were not run: that is unrun coverage, not a pass.
- This page records a hazard and deliberately proposes no change to `AGENTS.md`, `CLAUDE.md`, or any
  skill. Those are security-relevant surfaces; any change owes its own review and its own author.
