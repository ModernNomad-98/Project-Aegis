#requires -Version 5.1
<#
.SYNOPSIS
    Scenario A acceptance-evidence harness for the beginner-flow `docs/project-state.md`.

.DESCRIPTION
    Proves that a beginner-flow project-state.md file is written APPEND-ONLY for its
    IMMUTABLE evidence sections (State snapshots / Decision log / Approvals / Deviations)
    while its MUTABLE projection sections may be freely refreshed at checkpoints - and
    that the acceptance EVIDENCE is stored OUTSIDE the disposable product repo and is
    never committed to git.

    The harness replays the ordered fixture sequence under
    scenario-a-fixture/state-sequence/ against a throwaway git repo created in a fresh
    temp directory (OUTSIDE this skills repo). For every version it:
      * copies the version into the disposable repo as docs/project-state.md, leaving it
        UNTRACKED (never `git add`, never `git commit`);
      * asserts the file is untracked using BOTH `git status --short --untracked-files=all`
        and `git ls-files --others --exclude-standard`;
      * archives the version into an EXTERNAL evidence directory as project-state.NN.md;
      * records its SHA-256 (Get-FileHash) into sha256sums.txt;
      * compares it against the previous archived version with
        `git diff --no-index --unified=0`;
      * parses the immutable sections of prev vs curr and asserts APPEND-ONLY;
      * appends an ISO-8601-timestamped PASS/FAIL line to evidence-log.txt.

    Final assertions (any failure => non-zero exit): the exact expected fixture set was
    seen; SS-003 is ABSENT in the final version (Scenario A stops at SS-002); NO commits
    exist in the disposable repo; every per-step check passed.

.PARAMETER KeepEvidence
    Keep the work directory (disposable repo + evidence) after the run instead of
    cleaning it up. Evidence is ALSO always kept automatically when the run FAILS, so a
    failure can be inspected.

.PARAMETER WorkDir
    Base directory under which to create this run's OWNED work directory. Must be OUTSIDE
    this skills repo (the harness refuses otherwise). Defaults to the system temp folder.
    The harness NEVER deletes or recurses the base or its pre-existing contents: it always
    creates a fresh unique child directory ("scenario-a-run-<stamp>-<id>") that it owns via
    an ownership marker, and on a passing run it removes ONLY that owned child - and only
    after verifying the marker's run-id matches. A caller-supplied -WorkDir that already
    contains a `product-repo` or `evidence` directory is therefore safe.

.PARAMETER FixtureDir
    Override the fixture state-sequence directory (for tests). Defaults to the bundled
    scenario-a-fixture/state-sequence next to this script.

.PARAMETER LoadOnly
    Define the harness functions (Get-ImmutableRows, Test-AppendOnly, Remove-OwnedRunRoot,
    ...) and return WITHOUT running the main flow. Used by Test-ScenarioAEvidence.ps1 to
    dot-source and unit-test the functions.

.NOTES
    ### APPEND-ONLY over EVERY immutable row, placeholders INCLUDED
    Get-ImmutableRows returns, per immutable section, the ordered list of ALL data rows -
    real ID-bearing rows AND empty-state "(none yet)"/"(none recorded ...)" placeholders.
    Test-AppendOnly requires PREV's rows to be an exact PREFIX of CUR's, so deleting,
    editing, reordering, or replacing ANY previous row (a placeholder among them) is a
    violation. Per schema rule 9 the first real entry is appended AFTER the placeholder;
    the placeholder is preserved, never dropped.

    ### `git diff --no-index` EXIT-CODE SEMANTICS (important)
    `git diff --no-index a b` is a plain two-file comparator. It exits:
        0  -> the two files are IDENTICAL
        1  -> the two files DIFFER  <-- this is what we EXPECT and treat as SUCCESS
       >1  -> git itself failed (usage/error)
    Because each replayed version is expected to differ from the one before it, exit
    code 1 is the SUCCESS signal of the comparison, NOT a script failure. Only exit
    code 0 (unexpected: two consecutive versions identical) or >1 (a real git error)
    is treated as a problem. The evidence files live OUTSIDE the repo, so `--no-index`
    is the correct comparator; for a TRACKED-file comparison you would use ordinary
    `git diff`, which does not apply here.

    ### PowerShell 5.1 vs 7 UTF-8
    * The console output encoding is set to UTF-8 inside a try/catch (some hosts have no
      console and throw).
    * Every file WRITE uses an explicit no-BOM UTF-8 encoder via
      [System.IO.File]::WriteAllText/AppendAllText, so 5.1 (whose `-Encoding UTF8`
      emits a BOM) and 7 (whose `-Encoding UTF8` is BOM-less) produce byte-identical
      output. Fixture COPIES use Copy-Item (byte-exact), so archived SHA-256 values are
      stable across editions and machines.
    * Every file READ uses [System.IO.File]::ReadAllText (BOM auto-detected, UTF-8
      default), so an accidental BOM would not corrupt parsing.

    ### Robustness
    * $ErrorActionPreference = 'Stop' with try/catch around the main flow.
    * Native `git` is invoked through Invoke-GitCapture, which temporarily sets
      $ErrorActionPreference = 'Continue' and redirects stderr to a FILE (never `2>&1`),
      so a non-zero git exit (e.g. diff's exit 1) is captured as data and never becomes
      a terminating error.
    * All paths are passed via array splatting (no manual quoting), so spaces in paths
      - including this repo's own path - are handled correctly.
#>
[CmdletBinding()]
param(
    [switch] $KeepEvidence,
    [string] $WorkDir,
    [string] $FixtureDir,
    [string] $Manifest,
    [switch] $LoadOnly
)

$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# UTF-8 setup (guarded - a host without a console will throw on the assignment)
# ---------------------------------------------------------------------------
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
try {
    [Console]::OutputEncoding = $Utf8NoBom
} catch {
    # No console attached (some CI hosts) - safe to ignore; file I/O is explicitly UTF-8.
}
try {
    $OutputEncoding = $Utf8NoBom
} catch {
}

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
function Write-Utf8File {
    param([Parameter(Mandatory)][string] $Path, [string] $Content = '')
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
}

function Append-Utf8Line {
    param([Parameter(Mandatory)][string] $Path, [string] $Line = '')
    [System.IO.File]::AppendAllText($Path, ($Line + "`n"), $Utf8NoBom)
}

function Read-Utf8File {
    param([Parameter(Mandatory)][string] $Path)
    return [System.IO.File]::ReadAllText($Path)   # BOM auto-detected; UTF-8 default
}

function Split-IntoLines {
    param([string] $Text)
    if ([string]::IsNullOrEmpty($Text)) { return @() }
    return ($Text -split '\r?\n')      # single-quoted => regex \r?\n (handles CRLF and LF)
}

function Now-Iso {
    return (Get-Date).ToString('o')     # ISO-8601 with offset
}

function Path-IsInside {
    param([string] $Child, [string] $Parent)
    $sep = [System.IO.Path]::DirectorySeparatorChar
    $c = [System.IO.Path]::GetFullPath($Child)
    $p = [System.IO.Path]::GetFullPath($Parent)
    if (-not $c.EndsWith($sep)) { $c = $c + $sep }
    if (-not $p.EndsWith($sep)) { $p = $p + $sep }
    return $c.StartsWith($p, [System.StringComparison]::OrdinalIgnoreCase)
}

# SHA-256 of a file's content with CRLF/CR normalized to LF, so a working-tree that git
# smudged to CRLF (autocrlf) hashes the same as the LF blob the manifest was pinned from.
function Get-NormalizedSha256 {
    param([Parameter(Mandatory)][string] $Path)
    $text = [System.IO.File]::ReadAllText($Path)
    $norm = $text.Replace("`r`n", "`n").Replace("`r", "`n")
    $bytes = (New-Object System.Text.UTF8Encoding($false)).GetBytes($norm)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { $hash = $sha.ComputeHash($bytes) } finally { $sha.Dispose() }
    return "sha256:" + ([System.BitConverter]::ToString($hash).Replace("-", "").ToLower())
}

# First-cell ID of each immutable TABLE row, per section, in order (SS-/PS-/A- or a
# placeholder token like "(none yet)"). Deviations is not ID-checked here - its placeholder
# persistence is covered by the append-only check.
function Get-SectionIds {
    param([Parameter(Mandatory)][string] $Content)
    $rows = Get-ImmutableRows -Content $Content
    $out = @{}
    foreach ($key in @('State snapshots', 'Decision log', 'Approvals')) {
        $ids = New-Object System.Collections.Generic.List[string]
        foreach ($r in @($rows[$key])) {
            $t = $r.Trim()
            if ($t.StartsWith('|')) { $ids.Add($t.Trim('|').Split('|')[0].Trim()) }
        }
        $out[$key] = @($ids)
    }
    return $out
}

# Best-effort resolve reparse points (symlink / junction / mount) to the PHYSICAL target.
# Returns the resolved full path, or $null if it cannot be resolved confidently (fail
# closed). A path with NO reparse points along its existing chain resolves to its own
# lexical full path. This is what makes the external-WorkDir containment check honest: a
# junction/symlink that physically lands inside the repo is caught even though its lexical
# path looks external.
function Resolve-PhysicalDir {
    param([Parameter(Mandatory)][string] $Path)
    try {
        $full = [System.IO.Path]::GetFullPath($Path)
        $root = [System.IO.Path]::GetPathRoot($full)
        if ([string]::IsNullOrEmpty($root)) { return $null }
        $components = @(($full.Substring($root.Length)) -split '[\\/]+' | Where-Object { $_ -ne '' })
        $cur = $root.TrimEnd('\', '/')
        if (-not $cur) { $cur = $root }
        $guard = 0
        # Resolve EVERY path component from the root down, not just the deepest existing one:
        # if an INTERMEDIATE component is a reparse point (junction/symlink/mount), rewrite the
        # accumulated physical path to its target before appending the rest. This catches
        # `-WorkDir <link-inside-repo>/child` where `child` exists and looks like an ordinary dir.
        foreach ($comp in $components) {
            $guard++
            if ($guard -gt 4096) { return $null }        # pathological depth -> fail closed
            $cur = Join-Path $cur $comp
            $hops = 0
            while (Test-Path -LiteralPath $cur) {
                $item = Get-Item -LiteralPath $cur -Force -ErrorAction Stop
                if ((($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) -eq 0) { break }
                $target = $item.Target
                if ($target -is [System.Array]) { $target = $target[0] }
                if ([string]::IsNullOrWhiteSpace($target)) { return $null }   # unresolvable -> fail closed
                if (-not [System.IO.Path]::IsPathRooted($target)) {
                    $target = Join-Path (Split-Path -Parent $cur) $target
                }
                $cur = [System.IO.Path]::GetFullPath($target)
                $hops++
                if ($hops -gt 64) { return $null }        # link loop -> fail closed
            }
        }
        return [System.IO.Path]::GetFullPath($cur)
    } catch {
        return $null       # anything unexpected -> fail closed
    }
}

# Invoke native git, capturing exit code + stdout + stderr WITHOUT letting a non-zero
# exit (or stderr text) become a terminating PowerShell error. Never uses `2>&1`.
function Invoke-GitCapture {
    param(
        [Parameter(Mandatory)][string[]] $GitArgs,
        [string] $RepoDir
    )
    $eapPrev = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    $errFile = [System.IO.Path]::GetTempFileName()
    $out = $null
    $code = $null
    try {
        if ([string]::IsNullOrEmpty($RepoDir)) {
            $out = & git @GitArgs 2>$errFile
        } else {
            $out = & git -C $RepoDir @GitArgs 2>$errFile
        }
        $code = $LASTEXITCODE
        $errText = ''
        if (Test-Path -LiteralPath $errFile) {
            $errText = [System.IO.File]::ReadAllText($errFile)
        }
    } finally {
        Remove-Item -LiteralPath $errFile -Force -ErrorAction SilentlyContinue
        $ErrorActionPreference = $eapPrev
    }
    return [pscustomobject]@{
        ExitCode = $code
        StdOut   = (@($out) -join "`n")
        StdErr   = $errText
    }
}

# Parse the four IMMUTABLE sections of a project-state.md string, returning per-section
# an ORDERED list of EVERY immutable data row - both real ID-bearing rows (SS-/PS-/A-)
# AND empty-state placeholder rows (e.g. "(none yet)" / "(none recorded ...)"). Header
# and separator rows are excluded. Mutable projection sections are ignored entirely.
# Placeholders are treated as immutable rows exactly like evidence: the schema (rule 9)
# preserves them - the first real entry is APPENDED after the placeholder, and the
# placeholder is never edited, replaced, or deleted.
function Get-ImmutableRows {
    param([Parameter(Mandatory)][string] $Content)

    $lines = Split-IntoLines -Text $Content
    $wanted = @('State snapshots', 'Decision log', 'Approvals', 'Deviations')

    # Slice the document into sections keyed by their '## ' header.
    $rawBySection = @{}
    $curKey = $null
    foreach ($line in $lines) {
        if ($line -match '^\s*##\s+(.*)$') {
            $header = $Matches[1].Trim()
            $curKey = $null
            if ($header -like 'State snapshots*') { $curKey = 'State snapshots' }
            elseif ($header -like 'Decision log*') { $curKey = 'Decision log' }
            elseif ($header -like 'Approvals*')     { $curKey = 'Approvals' }
            elseif ($header -like 'Deviations*')     { $curKey = 'Deviations' }
            if ($curKey) { $rawBySection[$curKey] = New-Object System.Collections.Generic.List[string] }
            continue
        }
        if ($curKey) { $rawBySection[$curKey].Add($line) }
    }

    $result = @{}
    foreach ($key in $wanted) {
        $rows = New-Object System.Collections.Generic.List[string]

        if ($rawBySection.ContainsKey($key)) {
            $rawLines = @($rawBySection[$key])

            # Locate the markdown table separator row (dashes/pipes/colons only), if any.
            $sepIdx = -1
            for ($i = 0; $i -lt $rawLines.Count; $i++) {
                if ($rawLines[$i] -match '^\s*\|[\s:\-\|]+\|\s*$') { $sepIdx = $i; break }
            }

            for ($i = 0; $i -lt $rawLines.Count; $i++) {
                $ln = $rawLines[$i]
                if ([string]::IsNullOrWhiteSpace($ln)) { continue }
                if ($ln -match '^\s*<!--') { continue }        # marker comment lines

                # EVERY immutable data row - placeholder OR evidence - is kept, in order.
                if ($sepIdx -ge 0) {
                    # Table section: real rows are pipe-rows AFTER the separator
                    # (indices <= sepIdx are the header row and the separator itself).
                    if ($i -le $sepIdx) { continue }
                    if ($ln -notmatch '^\s*\|') { continue }
                    $rows.Add($ln.Trim())
                } else {
                    # Non-table section (Deviations): a '- ' bullet STARTS a row; any other
                    # non-empty, non-comment line is a wrapped CONTINUATION of the previous
                    # bullet and is FOLDED into that row (R7-4), so editing or deleting the
                    # continuation bytes of a past deviation violates the append-only prefix
                    # check. A stray continuation with no preceding bullet has nothing to
                    # attach to and is ignored.
                    if ($ln -match '^\s*-\s') {
                        $rows.Add($ln.Trim())
                    } elseif ($rows.Count -gt 0) {
                        $rows[$rows.Count - 1] = $rows[$rows.Count - 1] + ' ' + $ln.Trim()
                    }
                }
            }
        }

        $result[$key] = @($rows)
    }
    return $result
}

# Assert that CUR is an append-only successor of PREV. In every immutable section the
# ORDERED list of PREV's rows (placeholders AND evidence) must be an EXACT PREFIX of
# CUR's: no previous row may be deleted, edited, reordered, or replaced, and CUR may
# only ADD new rows at the end. Deleting a preserved "(none yet)" placeholder is therefore
# a violation, not a valid transition. Mutable projection sections are not checked here -
# they may be freely refreshed.
function Test-AppendOnly {
    param(
        [Parameter(Mandatory)] $PrevRows,
        [Parameter(Mandatory)] $CurRows
    )
    $problems = New-Object System.Collections.Generic.List[string]
    $added    = New-Object System.Collections.Generic.List[string]

    foreach ($key in @('State snapshots', 'Decision log', 'Approvals', 'Deviations')) {
        $prev = @($PrevRows[$key])
        $cur  = @($CurRows[$key])

        if ($cur.Count -lt $prev.Count) {
            $problems.Add("[$key] an immutable row was DELETED (prev $($prev.Count) row(s) -> now $($cur.Count)); previous rows, including empty-state placeholders, are preserved.")
        } else {
            for ($i = 0; $i -lt $prev.Count; $i++) {
                if ($cur[$i] -ne $prev[$i]) {
                    $problems.Add("[$key] immutable row #$($i + 1) was edited, reordered, or replaced (every previous row must be preserved byte-for-byte).")
                }
            }
            for ($i = $prev.Count; $i -lt $cur.Count; $i++) {
                $added.Add("[$key] +$($cur[$i])")
            }
        }
    }

    return [pscustomobject]@{
        Ok       = ($problems.Count -eq 0)
        Problems = @($problems)
        Added    = @($added)
    }
}

# Assert a fixture version conforms to its manifest step: the normalized SHA-256 matches
# (content pin - catches ANY content change, including a required row consistently removed
# from every later version), AND the ordered immutable IDs of each ID-bearing section
# exactly equal the manifest's expected IDs (catches a removed / duplicated / unexpected /
# missing-required row directly, not merely row-level append-only).
function Test-ManifestStep {
    param(
        [Parameter(Mandatory)] $Step,
        [Parameter(Mandatory)][string] $FilePath,
        [Parameter(Mandatory)][string] $Content
    )
    $problems = New-Object System.Collections.Generic.List[string]

    $actualSha = Get-NormalizedSha256 -Path $FilePath
    if ($actualSha -ne [string]$Step.sha256) {
        $problems.Add("content hash mismatch (manifest $($Step.sha256); actual $actualSha) - fixture modified without updating its approved manifest hash")
    }

    $ids = Get-SectionIds -Content $Content
    $map = @{
        'State snapshots' = @($Step.snapshots)
        'Decision log'    = @($Step.decisions)
        'Approvals'       = @($Step.approvals)
    }
    foreach ($key in @('State snapshots', 'Decision log', 'Approvals')) {
        $exp = @($map[$key] | ForEach-Object { [string]$_ })
        $act = @($ids[$key] | ForEach-Object { [string]$_ })
        if (($act -join '|') -ne ($exp -join '|')) {
            $problems.Add("[$key] immutable IDs [$($act -join ', ')] do not match the required manifest IDs [$($exp -join ', ')]")
        }
    }
    return [pscustomobject]@{ Ok = ($problems.Count -eq 0); Problems = @($problems) }
}

# FAIL CLOSED for the disposable-repo commit-count. A zero count is accepted ONLY when the
# git command exited 0 AND returned exactly one clean, parseable, non-negative 32-bit integer
# whose value is 0. A nonzero exit, empty / malformed / multi-line / non-numeric / negative /
# overflowing output, or any positive count is a FAILURE - so a broken git check can never be
# mistaken for "0 commits". This is a pure function so tests can drive it without touching git.
function Test-ZeroCommitCount {
    param([int] $ExitCode, [string] $StdOut, [string] $StdErr)
    if ($ExitCode -ne 0) {
        return [pscustomobject]@{ Ok = $false; Reason = "git rev-list exited $ExitCode (stderr: $StdErr)" }
    }
    $lines = @(($StdOut -split '\r?\n') | Where-Object { $_.Trim() -ne '' })
    if ($lines.Count -ne 1) {
        return [pscustomobject]@{ Ok = $false; Reason = "expected exactly one output line, got $($lines.Count): '$StdOut'" }
    }
    $raw = $lines[0].Trim()
    $parsed = 0
    if (-not [int]::TryParse($raw, [ref]$parsed)) {
        return [pscustomobject]@{ Ok = $false; Reason = "output is not a valid 32-bit integer: '$raw'" }
    }
    if ($parsed -lt 0) { return [pscustomobject]@{ Ok = $false; Reason = "negative commit count: $parsed" } }
    if ($parsed -ne 0) { return [pscustomobject]@{ Ok = $false; Reason = "unexpected commit count: $parsed" } }
    return [pscustomobject]@{ Ok = $true; Reason = "0 commits (git exit 0; one clean integer)" }
}

# First manifest step index (0-based) whose $Section list (snapshots|decisions|approvals)
# contains $Id, or -1. Used for the semantic ordering gates (owners-before-Stage-3;
# acceptance-before-owner-completion).
function Get-FirstStepIndex {
    param([Parameter(Mandatory)] $Steps, [Parameter(Mandatory)][string] $Section, [Parameter(Mandatory)][string] $Id)
    $arr = @($Steps)
    for ($i = 0; $i -lt $arr.Count; $i++) {
        $vals = @($arr[$i].$Section | ForEach-Object { [string]$_ })
        if ($vals -contains $Id) { return $i }
    }
    return -1
}

# Semantic ordering gates over the manifest step sequence (pure function, so tests can drive
# it on synthetic step data): forbidden snapshot ids never appear; the Stage 3 snapshot is in
# the final step; the four Stage 2 owner records are recorded BEFORE the Stage 3 snapshot step;
# and the user's product-spec acceptance is recorded BEFORE the product-spec owner completion.
function Test-SemanticGates {
    param([Parameter(Mandatory)] $Steps, [Parameter(Mandatory)] $Semantics)
    $problems = New-Object System.Collections.Generic.List[string]
    $passes   = New-Object System.Collections.Generic.List[string]
    $arr = @($Steps)
    $sem = $Semantics

    $allSnap = @($arr | ForEach-Object { $_.snapshots } | ForEach-Object { [string]$_ })
    $forbHit = @(@($sem.forbidden_snapshot_ids | ForEach-Object { [string]$_ }) | Where-Object { $allSnap -contains $_ })
    if ($forbHit.Count -gt 0) { $problems.Add("forbidden snapshot id(s) appear in the sequence: $($forbHit -join ', ')") }
    else { $passes.Add("no forbidden snapshot id (e.g. SS-003) in the sequence") }

    $s3 = [string]$sem.stage3_snapshot_id
    $finalSnap = @($arr[$arr.Count - 1].snapshots | ForEach-Object { [string]$_ })
    if ($finalSnap -contains $s3) { $passes.Add("Stage 3 snapshot $s3 present in the final version") }
    else { $problems.Add("final version is missing the Stage 3 snapshot $s3") }

    $stage3Idx = Get-FirstStepIndex -Steps $arr -Section 'snapshots' -Id $s3
    if ($stage3Idx -lt 1) {
        $problems.Add("Stage 3 snapshot appears at step index $stage3Idx; it must follow the recorded owner gate")
    } else {
        $pre = @($arr[$stage3Idx - 1].decisions | ForEach-Object { [string]$_ })
        $missing = @(@($sem.stage2_owner_ids | ForEach-Object { [string]$_ }) | Where-Object { $pre -notcontains $_ })
        if ($missing.Count -gt 0) { $problems.Add("Stage 2 owner record(s) [$($missing -join ', ')] are not recorded before the Stage 3 snapshot") }
        else { $passes.Add("all Stage 2 owner records ($($sem.stage2_owner_ids -join ', ')) recorded before the Stage 3 snapshot") }
    }

    $ai = Get-FirstStepIndex -Steps $arr -Section 'decisions' -Id ([string]$sem.spec_acceptance_id)
    $oi = Get-FirstStepIndex -Steps $arr -Section 'decisions' -Id ([string]$sem.spec_owner_completion_id)
    if ($ai -ge 0 -and $oi -gt $ai) { $passes.Add("user spec acceptance ($($sem.spec_acceptance_id)) recorded before product-spec owner completion ($($sem.spec_owner_completion_id))") }
    else { $problems.Add("product-spec owner completion ($($sem.spec_owner_completion_id), step $oi) must be recorded AFTER the user's spec acceptance ($($sem.spec_acceptance_id), step $ai)") }

    return [pscustomobject]@{ Ok = ($problems.Count -eq 0); Problems = @($problems); Passes = @($passes) }
}

# Verify the accepted-spec ARTIFACT is real and is the anchor recorded in the acceptance
# decision. The manifest's spec_artifact block names the artifact fixture, its pinned normalized
# SHA-256, the acceptance decision id, and the in-product path. This function: (1) requires a
# well-formed sha256:+64-hex digest; (2) requires the artifact fixture to exist; (3) recomputes
# its normalized digest and requires a match; (4) requires the acceptance decision ROW to carry
# BOTH that exact digest and the in-product path. A missing artifact, a tampered artifact, or a
# malformed/wrong digest in the fixture all FAIL - so the acceptance can be verified, not asserted.
function Test-SpecArtifact {
    param(
        [Parameter(Mandatory)] $Semantics,
        [Parameter(Mandatory)][string] $FixtureRoot,
        [Parameter(Mandatory)][string] $AcceptanceRowText
    )
    $problems = New-Object System.Collections.Generic.List[string]
    $passes   = New-Object System.Collections.Generic.List[string]
    $sa = $Semantics.spec_artifact
    if ($null -eq $sa) {
        $problems.Add("manifest semantics has no spec_artifact block")
        return [pscustomobject]@{ Ok = $false; Problems = @($problems); Passes = @($passes) }
    }
    $expected = [string]$sa.sha256
    if ($expected -notmatch '^sha256:[0-9a-f]{64}$') {
        $problems.Add("spec_artifact.sha256 is not a well-formed 'sha256:'+64-lowercase-hex digest: '$expected'")
    }
    $artPath = Join-Path $FixtureRoot ([string]$sa.file)
    if (-not (Test-Path -LiteralPath $artPath)) {
        $problems.Add("accepted-spec artifact fixture not found: $artPath")
        return [pscustomobject]@{ Ok = $false; Problems = @($problems); Passes = @($passes) }
    }
    $actual = Get-NormalizedSha256 -Path $artPath
    if ($actual -ne $expected) {
        $problems.Add("accepted-spec artifact digest mismatch: computed $actual, manifest pins $expected")
    } else {
        $passes.Add("accepted-spec artifact $($sa.file) matches its pinned digest")
    }
    if ($AcceptanceRowText -notlike ("*" + $expected + "*")) {
        $problems.Add("acceptance decision row ($($sa.decision_id)) does not carry the pinned digest $expected")
    }
    $ipp = [string]$sa.in_product_path
    if ($ipp -and ($AcceptanceRowText -notlike ("*" + $ipp + "*"))) {
        $problems.Add("acceptance decision row ($($sa.decision_id)) does not reference the artifact path $ipp")
    }
    if ($problems.Count -eq 0) { $passes.Add("acceptance decision $($sa.decision_id) anchors to $ipp @ its verified digest") }
    return [pscustomobject]@{ Ok = ($problems.Count -eq 0); Problems = @($problems); Passes = @($passes) }
}

# ---------------------------------------------------------------------------
# Cleanup: delete ONLY a run directory this run created and can PROVE it owns via
# a matching ownership marker. Never Remove-Item -Recurse an unverified directory,
# and never anything inside the skills repo. Returns $true only if it deleted.
# ---------------------------------------------------------------------------
function Remove-OwnedRunRoot {
    param(
        [string] $Root,
        [string] $ExpectedRunId,
        [string] $MarkerName,
        [Parameter(Mandatory)][string] $SkillsRepoRoot
    )
    if ([string]::IsNullOrWhiteSpace($Root)) { return $false }
    if (-not (Test-Path -LiteralPath $Root)) { return $false }
    if (Path-IsInside -Child $Root -Parent $SkillsRepoRoot) {
        Write-Host "Cleanup REFUSED: run dir resolves inside the skills repo - not deleting."
        return $false
    }
    $marker = Join-Path $Root $MarkerName
    if (-not (Test-Path -LiteralPath $marker)) {
        Write-Host ("Cleanup REFUSED: ownership marker '{0}' not found in '{1}' - not deleting an unverified directory." -f $MarkerName, $Root)
        return $false
    }
    $content = ''
    try { $content = Read-Utf8File -Path $marker } catch { }
    if ($content -notmatch [regex]::Escape("run-id: $ExpectedRunId")) {
        Write-Host ("Cleanup REFUSED: ownership marker run-id in '{0}' does not match this run - not deleting." -f $Root)
        return $false
    }
    Remove-Item -LiteralPath $Root -Recurse -Force -ErrorAction SilentlyContinue
    return $true
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if (-not $LoadOnly) {

$exitCode  = 1
$runPassed = $false
$failures  = New-Object System.Collections.Generic.List[string]

# Populated inside the try so the finally can report/clean them.
$MarkerName   = '.scenario-a-run-id'
$RunId        = [guid]::NewGuid().ToString('N')
$OwnedRunRoot = $null
$Repo         = $null
$Evidence     = $null

try {
    Write-Host "=== Scenario A acceptance-evidence harness ==="
    Write-Host ("PowerShell : {0}" -f $PSVersionTable.PSVersion.ToString())

    # git must be available.
    $gitCmd = Get-Command git -ErrorAction SilentlyContinue
    if (-not $gitCmd) { throw "git was not found on PATH - this harness requires git." }
    $gitVer = Invoke-GitCapture -GitArgs @('--version')
    Write-Host ("git        : {0}" -f ($gitVer.StdOut.Trim()))

    # Resolve the fixture directory relative to this script (READ-only; inside skills repo).
    $ScriptDir      = $PSScriptRoot
    # Platform-neutral joins (R8-2): backslash is not a separator on non-Windows
    # PowerShell, so multi-segment children are built one Join-Path component at a time.
    $SkillsRepoRoot = [System.IO.Path]::GetFullPath((Join-Path (Join-Path $ScriptDir '..') '..'))
    # R9-3: resolve the repo root PHYSICALLY too, so both sides of every Path-IsInside
    # containment check use the same representation. If the checkout path (or an ancestor)
    # is itself a symlink/junction, a -WorkDir under the repo's REAL target must still be
    # recognised as inside. Fail closed if the root cannot be resolved.
    $SkillsRepoRoot = Resolve-PhysicalDir -Path $SkillsRepoRoot
    if ($null -eq $SkillsRepoRoot) {
        throw "Refusing to run: the skills repo root cannot be resolved to a physical path (failing closed)."
    }
    if ([string]::IsNullOrWhiteSpace($FixtureDir)) {
        $FixtureDir = Join-Path (Join-Path $ScriptDir 'scenario-a-fixture') 'state-sequence'
    }
    $FixtureDir = [System.IO.Path]::GetFullPath($FixtureDir)
    if (-not (Test-Path -LiteralPath $FixtureDir)) {
        throw "Fixture directory not found: $FixtureDir"
    }
    Write-Host ("fixtures   : {0}" -f $FixtureDir)

    # Load the approved fixture MANIFEST (default: manifest.json beside the state-sequence
    # dir). It pins, per ordered step, the file's normalized SHA-256 and the exact expected
    # immutable IDs. The manifest - not a hard-coded list - is the source of truth.
    if ([string]::IsNullOrWhiteSpace($Manifest)) {
        $Manifest = Join-Path (Split-Path -Parent $FixtureDir) 'manifest.json'
    }
    $Manifest = [System.IO.Path]::GetFullPath($Manifest)
    if (-not (Test-Path -LiteralPath $Manifest)) {
        throw "Fixture manifest not found: $Manifest"
    }
    $manifestObj = (Read-Utf8File -Path $Manifest) | ConvertFrom-Json
    $steps = @($manifestObj.steps)
    if ($steps.Count -lt 1) { throw "Fixture manifest has no steps: $Manifest" }
    $expectedFiles = @($steps | ForEach-Object { [string]$_.file })
    Write-Host ("manifest   : {0}  ({1} steps)" -f $Manifest, $steps.Count)

    # Assert the fixture set is EXACTLY the manifest's file set (no unexpected / missing files).
    $actualFiles = @(Get-ChildItem -LiteralPath $FixtureDir -Filter '*.md' -File |
        Select-Object -ExpandProperty Name | Sort-Object)
    $expectedSorted = @($expectedFiles | Sort-Object)
    $missing = @($expectedSorted | Where-Object { $actualFiles -notcontains $_ })
    $extra   = @($actualFiles   | Where-Object { $expectedSorted -notcontains $_ })
    if (($missing.Count -gt 0) -or ($extra.Count -gt 0)) {
        throw ("Fixture set mismatch vs manifest. Missing: [{0}]  Unexpected: [{1}]" -f ($missing -join ', '), ($extra -join ', '))
    }

    # Resolve the BASE directory (OUTSIDE the skills repo): system temp by default,
    # or the caller's -WorkDir. We NEVER delete or recurse the base or its existing
    # contents - we only ever create, own, and later remove a fresh unique child.
    if ([string]::IsNullOrWhiteSpace($WorkDir)) {
        $baseDir = [System.IO.Path]::GetTempPath()
    } else {
        $baseDir = [System.IO.Path]::GetFullPath($WorkDir)
    }
    # Containment is checked on the PHYSICAL target, AFTER resolving any symlink / junction /
    # mount / reparse point, and BEFORE creating anything (R5-4). A lexical GetFullPath check
    # alone can be fooled by an external-looking link whose target is inside the repo, and
    # creating a missing -WorkDir first would put a caller directory inside the repo (or under
    # a link into the repo) only to reject it afterwards. Resolve-PhysicalDir resolves the
    # deepest existing ancestor (and any reparse point along it), appending a not-yet-existing
    # tail lexically, so a path we have NOT created is still checked correctly. Fail CLOSED if
    # the physical path cannot be resolved confidently.
    $basePhysical = Resolve-PhysicalDir -Path $baseDir
    if ($null -eq $basePhysical) {
        throw "Refusing to run: work dir '$baseDir' contains a symlink/junction/reparse point that cannot be resolved to a physical path (failing closed)."
    }
    if (Path-IsInside -Child $basePhysical -Parent $SkillsRepoRoot) {
        throw "Refusing to run: work dir '$baseDir' resolves (physically) INSIDE the skills repo '$SkillsRepoRoot'. Evidence must live OUTSIDE the skills repo."
    }
    # Only now, after the physical boundary is confirmed external, create a missing base.
    if (-not (Test-Path -LiteralPath $baseDir)) {
        New-Item -ItemType Directory -Force -Path $baseDir | Out-Null
    }

    # ALWAYS create a NEW unique run directory owned by THIS run, under the base.
    # A caller-supplied -WorkDir that already contains files is safe: we touch only
    # this owned child, never the caller's pre-existing product-repo/evidence/etc.
    $stamp   = (Get-Date).ToString('yyyyMMdd-HHmmss')
    $RunRoot = Join-Path $baseDir ("scenario-a-run-$stamp-" + $RunId.Substring(0, 12))
    if (Test-Path -LiteralPath $RunRoot) {
        throw "Run directory unexpectedly already exists (refusing to reuse): $RunRoot"
    }
    if (Path-IsInside -Child $RunRoot -Parent $SkillsRepoRoot) {
        throw "Refusing to run: run dir '$RunRoot' resolves inside the skills repo."
    }
    New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null
    $OwnedRunRoot = $RunRoot     # only this exact directory may be cleaned up

    # Ownership marker: cleanup will delete $RunRoot ONLY if this marker is present
    # and its run-id matches. This is what makes recursive cleanup safe.
    $MarkerPath = Join-Path $RunRoot $MarkerName
    Write-Utf8File -Path $MarkerPath -Content ("scenario-a-evidence-harness`nrun-id: $RunId`ncreated: {0}`n" -f (Now-Iso))

    $Repo     = Join-Path $RunRoot 'product-repo'
    $Evidence = Join-Path $RunRoot 'evidence'
    $RepoDocs = Join-Path $Repo 'docs'

    New-Item -ItemType Directory -Force -Path $Repo     | Out-Null
    New-Item -ItemType Directory -Force -Path $RepoDocs | Out-Null
    New-Item -ItemType Directory -Force -Path $Evidence | Out-Null

    Write-Host ("run dir    : {0}  (owned; run-id {1})" -f $RunRoot, $RunId.Substring(0,12))
    Write-Host ("repo       : {0}" -f $Repo)
    Write-Host ("evidence   : {0}" -f $Evidence)
    Write-Host ""

    # Initialize the disposable product repo. We NEVER `git add` or `git commit` in it.
    $init = Invoke-GitCapture -GitArgs @('init', '--quiet') -RepoDir $Repo
    if ($init.ExitCode -ne 0) {
        throw "git init failed (exit $($init.ExitCode)): $($init.StdErr)"
    }

    # Evidence log + SHA manifest.
    $EvidenceLog = Join-Path $Evidence 'evidence-log.txt'
    $ShaFile     = Join-Path $Evidence 'sha256sums.txt'
    Write-Utf8File -Path $EvidenceLog -Content ("# Scenario A evidence log - run started {0}`n" -f (Now-Iso))
    Write-Utf8File -Path $ShaFile     -Content "# SHA-256 of each archived project-state version (sha256sum format)`n"

    $repoStateFile = Join-Path $RepoDocs 'project-state.md'

    $stepResults          = @()
    $prevEvidenceSnapshot = $null
    $prevRows             = $null

    for ($idx = 0; $idx -lt $expectedFiles.Count; $idx++) {
        $fixName = $expectedFiles[$idx]
        $nn      = '{0:D2}' -f $idx
        $fixPath = Join-Path $FixtureDir $fixName
        if (-not (Test-Path -LiteralPath $fixPath)) { throw "Fixture missing at replay time: $fixPath" }

        $stepFailures = New-Object System.Collections.Generic.List[string]

        # (a) Copy the version into the disposable repo - UNTRACKED (no add / no commit).
        Copy-Item -LiteralPath $fixPath -Destination $repoStateFile -Force

        # (b) Assert untracked via BOTH git commands.
        $st     = Invoke-GitCapture -GitArgs @('status', '--short', '--untracked-files=all') -RepoDir $Repo
        $others = Invoke-GitCapture -GitArgs @('ls-files', '--others', '--exclude-standard') -RepoDir $Repo
        $inStatus = @(Split-IntoLines $st.StdOut     | Where-Object { $_ -match '^\?\?\s+docs/project-state\.md\s*$' })
        $inOthers = @(Split-IntoLines $others.StdOut | Where-Object { $_.Trim() -eq 'docs/project-state.md' })
        $untrackedOk = (($inStatus.Count -ge 1) -and ($inOthers.Count -ge 1))
        if (-not $untrackedOk) {
            $stepFailures.Add("docs/project-state.md not reported as untracked by git status AND ls-files")
        }

        # (c) Archive into the EXTERNAL evidence dir (byte-exact copy).
        $curEvidenceSnapshot = Join-Path $Evidence ("project-state.$nn.md")
        Copy-Item -LiteralPath $fixPath -Destination $curEvidenceSnapshot -Force

        # (d) SHA-256.
        $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $curEvidenceSnapshot).Hash.ToLower()
        Append-Utf8Line -Path $ShaFile -Line ("{0}  project-state.{1}.md" -f $hash, $nn)

        # (e) git diff --no-index vs the previous archived version.
        #     exit 1 == differences found == SUCCESS (see .NOTES). exit 0 == identical
        #     (unexpected). exit >1 == git error.
        $diffExit = $null
        $diffNote = 'baseline (no previous version to diff)'
        if ($prevEvidenceSnapshot) {
            $diff = Invoke-GitCapture -GitArgs @('diff', '--no-index', '--unified=0', '--', $prevEvidenceSnapshot, $curEvidenceSnapshot)
            $diffExit = $diff.ExitCode
            $diffFile = Join-Path $Evidence ('diff.{0:D2}-to-{1:D2}.txt' -f ($idx - 1), $idx)
            Write-Utf8File -Path $diffFile -Content $diff.StdOut
            if ($diffExit -eq 1) {
                $diffNote = "git diff --no-index exit=1 (differences found = SUCCESS)"
            } elseif ($diffExit -eq 0) {
                $diffNote = "git diff --no-index exit=0 (NO differences - versions must differ)"
                $stepFailures.Add("consecutive versions identical (git diff --no-index exit 0)")
            } else {
                $diffNote = "git diff --no-index exit=$diffExit (git error)"
                $stepFailures.Add("git diff --no-index failed with exit $diffExit : $($diff.StdErr)")
            }
        }

        # (f) Append-only assertion of the immutable sections vs previous version.
        $curRows    = Get-ImmutableRows -Content (Read-Utf8File -Path $curEvidenceSnapshot)
        $appendOk   = $true
        $appendNote = 'baseline (no previous version to compare)'
        if ($prevRows) {
            $ao = Test-AppendOnly -PrevRows $prevRows -CurRows $curRows
            $appendOk = $ao.Ok
            if ($ao.Ok) {
                if ($ao.Added.Count -gt 0) {
                    $appendNote = "append-only OK; added " + ($ao.Added -join ' ')
                } else {
                    $appendNote = "append-only OK; projection-only refresh (no immutable rows added)"
                }
            } else {
                $appendNote = "APPEND-ONLY VIOLATION: " + ($ao.Problems -join ' | ')
                $stepFailures.Add($appendNote)
            }
        }

        # (g) Manifest conformance: content hash pin + the EXACT expected immutable IDs for
        #     THIS step. This catches a required row removed consistently from every version,
        #     a duplicated / unexpected ID, or a fixture modified without updating the manifest.
        $manifestNote = 'manifest OK'
        $ms = Test-ManifestStep -Step $steps[$idx] -FilePath $curEvidenceSnapshot -Content (Read-Utf8File -Path $curEvidenceSnapshot)
        if (-not $ms.Ok) {
            $manifestNote = "MANIFEST VIOLATION: " + ($ms.Problems -join ' | ')
            $stepFailures.Add($manifestNote)
        }

        $stepPass = ($stepFailures.Count -eq 0)
        foreach ($f in $stepFailures) { $failures.Add("[$fixName] $f") }

        $statusWord = 'PASS'
        if (-not $stepPass) { $statusWord = 'FAIL' }
        $logLine = ("{0}  STEP {1} ({2})  {3}  untracked={4}; {5}; {6}; {7}; sha256={8}" -f `
            (Now-Iso), $nn, $fixName, $statusWord, $untrackedOk, $diffNote, $appendNote, $manifestNote, $hash)
        Append-Utf8Line -Path $EvidenceLog -Line $logLine

        $color = 'Green'
        if (-not $stepPass) { $color = 'Red' }
        Write-Host ("[{0}] {1}  {2}; {3}" -f $statusWord, $fixName, $appendNote, $manifestNote) -ForegroundColor $color

        $stepResults += [pscustomobject]@{
            Index      = $nn
            File       = $fixName
            Untracked  = $untrackedOk
            DiffExit   = $diffExit
            AppendOnly = $appendOk
            Pass       = $stepPass
        }

        $prevEvidenceSnapshot = $curEvidenceSnapshot
        $prevRows             = $curRows
    }

    # -----------------------------------------------------------------------
    # Final assertions
    # -----------------------------------------------------------------------
    Write-Host ""
    Write-Host "--- Final assertions ---"

    $finalSnapshot = Join-Path $Evidence ("project-state.{0:D2}.md" -f ($expectedFiles.Count - 1))
    $finalText     = Read-Utf8File -Path $finalSnapshot

    $sem = $manifestObj.semantics

    # Forbidden-id, Stage-3-present, four-owners-before-Stage-3, and acceptance-before-completion
    # gates (from the validated per-step manifest data). Test-SemanticGates is a pure function so
    # the negative tests can prove each gate fires on bad step data.
    $sg = Test-SemanticGates -Steps $steps -Semantics $sem
    foreach ($p in $sg.Passes)   { Write-Host "[PASS] $p" }
    foreach ($p in $sg.Problems) { $failures.Add($p); Write-Host "[FAIL] $p" -ForegroundColor Red }

    # Accepted-spec artifact: real file, digest matches the pin, and the acceptance decision row
    # anchors to that exact digest + path (so PS-006/PS-007/Stage-3 cannot pass on an unverifiable
    # or malformed anchor). The acceptance row is immutable, so the final version carries it.
    if ($sem.PSObject.Properties.Name -contains 'spec_artifact' -and $null -ne $sem.spec_artifact) {
        $accId  = [string]$sem.spec_artifact.decision_id
        $accRow = @(Split-IntoLines $finalText | Where-Object { $_ -match ("^\|\s*" + [regex]::Escape($accId) + "\s*\|") }) -join "`n"
        $spa = Test-SpecArtifact -Semantics $sem -FixtureRoot (Split-Path -Parent $FixtureDir) -AcceptanceRowText $accRow
        foreach ($p in $spa.Passes)   { Write-Host "[PASS] $p" }
        foreach ($p in $spa.Problems) { $failures.Add($p); Write-Host "[FAIL] $p" -ForegroundColor Red }
    } else {
        $failures.Add("manifest semantics is missing the required spec_artifact block")
        Write-Host "[FAIL] manifest semantics is missing the required spec_artifact block" -ForegroundColor Red
    }

    # NO commits may exist in the disposable repo - FAIL CLOSED (see Test-ZeroCommitCount).
    $rev = Invoke-GitCapture -GitArgs @('rev-list', '--count', '--all') -RepoDir $Repo
    $cc  = Test-ZeroCommitCount -ExitCode $rev.ExitCode -StdOut $rev.StdOut -StdErr $rev.StdErr
    if ($cc.Ok) {
        Write-Host "[PASS] disposable repo has exactly 0 commits ($($cc.Reason))"
    } else {
        $failures.Add("no-commits assertion failed: $($cc.Reason)")
        Write-Host "[FAIL] no-commits assertion: $($cc.Reason)" -ForegroundColor Red
    }

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    Write-Host ""
    Write-Host "--- Step summary ---"
    $stepResults | Format-Table -AutoSize | Out-String | ForEach-Object { Write-Host $_ }

    $runPassed = ($failures.Count -eq 0)
    if ($runPassed) {
        $exitCode = 0
        Append-Utf8Line -Path $EvidenceLog -Line ("{0}  RUN RESULT  PASS  {1} versions replayed; immutable sections append-only; 0 commits." -f (Now-Iso), $expectedFiles.Count)
        Write-Host ""
        Write-Host ("PASS - {0} versions replayed; immutable evidence append-only; mutable projections refreshed; 0 commits; evidence stored outside the skills repo." -f $expectedFiles.Count) -ForegroundColor Green
    } else {
        $exitCode = 1
        Append-Utf8Line -Path $EvidenceLog -Line ("{0}  RUN RESULT  FAIL  {1} problem(s)." -f (Now-Iso), $failures.Count)
        Write-Host ""
        Write-Host ("FAIL - {0} problem(s):" -f $failures.Count) -ForegroundColor Red
        foreach ($f in $failures) { Write-Host ("  - {0}" -f $f) -ForegroundColor Red }
    }
}
catch {
    $runPassed = $false
    $exitCode  = 1
    Write-Host ""
    Write-Host ("FATAL: {0}" -f $_.Exception.Message) -ForegroundColor Red
}
finally {
    # Cleanup policy:
    #   * Keep everything when -KeepEvidence is set OR when the run FAILED (so a failure
    #     can be inspected) - the run's evidence is preserved, never deleted.
    #   * Otherwise remove ONLY the owned run directory, and only after Remove-OwnedRunRoot
    #     proves ownership via the matching marker. The caller's -WorkDir and its other
    #     contents are never touched.
    $keep = ($KeepEvidence -or (-not $runPassed))
    if ($keep) {
        if ($Evidence)     { Write-Host ("Evidence kept at : {0}" -f $Evidence) }
        if ($Repo)         { Write-Host ("Disposable repo  : {0}" -f $Repo) }
        if ($OwnedRunRoot) { Write-Host ("Owned run dir    : {0}  (kept)" -f $OwnedRunRoot) }
    } else {
        $removed = Remove-OwnedRunRoot -Root $OwnedRunRoot -ExpectedRunId $RunId -MarkerName $MarkerName -SkillsRepoRoot $SkillsRepoRoot
        if ($removed) {
            Write-Host "Cleaned up the owned run directory (ownership marker verified; run passed; -KeepEvidence not set)."
        } else {
            Write-Host "Left the work area in place (cleanup found nothing it could prove it owned)."
        }
    }
}

    exit $exitCode
}
