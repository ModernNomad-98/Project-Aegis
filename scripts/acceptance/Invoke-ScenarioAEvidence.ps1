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

                if ($sepIdx -ge 0) {
                    # Table section: real rows are pipe-rows AFTER the separator
                    # (indices <= sepIdx are the header row and the separator itself).
                    if ($i -le $sepIdx) { continue }
                    if ($ln -notmatch '^\s*\|') { continue }
                } else {
                    # Non-table section (Deviations): bullet lines only.
                    if ($ln -notmatch '^\s*-\s') { continue }
                }

                # EVERY immutable data row - placeholder OR evidence - is kept, in order.
                $rows.Add($ln.Trim())
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
    $SkillsRepoRoot = [System.IO.Path]::GetFullPath((Join-Path $ScriptDir '..\..'))
    if ([string]::IsNullOrWhiteSpace($FixtureDir)) {
        $FixtureDir = Join-Path $ScriptDir 'scenario-a-fixture\state-sequence'
    }
    $FixtureDir = [System.IO.Path]::GetFullPath($FixtureDir)
    if (-not (Test-Path -LiteralPath $FixtureDir)) {
        throw "Fixture directory not found: $FixtureDir"
    }
    Write-Host ("fixtures   : {0}" -f $FixtureDir)

    # The exact expected fixture set, in replay order.
    $expectedFiles = @(
        '00-cold-start.md',
        '01-discovery-recorded.md',
        '02-lowrisk-batch-recorded.md',
        '03-product-spec-complete.md',
        '04-prioritization-na.md',
        '05-roadmap-na.md',
        '06-commitment-readiness-na.md',
        '07-stage3-snapshot.md'
    )

    # Assert the fixture set is EXACTLY as expected (no unexpected / missing files).
    $actualFiles = @(Get-ChildItem -LiteralPath $FixtureDir -Filter '*.md' -File |
        Select-Object -ExpandProperty Name | Sort-Object)
    $expectedSorted = @($expectedFiles | Sort-Object)
    $missing = @($expectedSorted | Where-Object { $actualFiles -notcontains $_ })
    $extra   = @($actualFiles   | Where-Object { $expectedSorted -notcontains $_ })
    if (($missing.Count -gt 0) -or ($extra.Count -gt 0)) {
        throw ("Fixture set mismatch. Missing: [{0}]  Unexpected: [{1}]" -f ($missing -join ', '), ($extra -join ', '))
    }

    # Resolve the BASE directory (OUTSIDE the skills repo): system temp by default,
    # or the caller's -WorkDir. We NEVER delete or recurse the base or its existing
    # contents - we only ever create, own, and later remove a fresh unique child.
    if ([string]::IsNullOrWhiteSpace($WorkDir)) {
        $baseDir = [System.IO.Path]::GetTempPath()
    } else {
        $baseDir = [System.IO.Path]::GetFullPath($WorkDir)
        if (Path-IsInside -Child $baseDir -Parent $SkillsRepoRoot) {
            throw "Refusing to run: -WorkDir '$baseDir' is inside the skills repo. Evidence must live OUTSIDE the skills repo."
        }
        if (-not (Test-Path -LiteralPath $baseDir)) {
            New-Item -ItemType Directory -Force -Path $baseDir | Out-Null
        }
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

        $stepPass = ($stepFailures.Count -eq 0)
        foreach ($f in $stepFailures) { $failures.Add("[$fixName] $f") }

        $statusWord = 'PASS'
        if (-not $stepPass) { $statusWord = 'FAIL' }
        $logLine = ("{0}  STEP {1} ({2})  {3}  untracked={4}; {5}; {6}; sha256={7}" -f `
            (Now-Iso), $nn, $fixName, $statusWord, $untrackedOk, $diffNote, $appendNote, $hash)
        Append-Utf8Line -Path $EvidenceLog -Line $logLine

        $color = 'Green'
        if (-not $stepPass) { $color = 'Red' }
        Write-Host ("[{0}] {1}  {2}" -f $statusWord, $fixName, $appendNote) -ForegroundColor $color

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

    # SS-003 must be ABSENT (Scenario A stops at SS-002).
    if ($finalText -match 'SS-003') {
        $failures.Add("Final version unexpectedly contains SS-003 (Scenario A must stop at SS-002).")
        Write-Host "[FAIL] SS-003 present in final version" -ForegroundColor Red
    } else {
        Write-Host "[PASS] SS-003 absent in final version"
    }

    # SS-002 should be PRESENT (Scenario A reaches Stage 3 design) - sanity check.
    if ($finalText -match 'SS-002') {
        Write-Host "[PASS] SS-002 present in final version (Stage 3 reached)"
    } else {
        $failures.Add("Final version is missing SS-002 (Stage 3 design snapshot expected).")
        Write-Host "[FAIL] SS-002 missing from final version" -ForegroundColor Red
    }

    # NO commits may exist in the disposable repo.
    $rev = Invoke-GitCapture -GitArgs @('rev-list', '--count', '--all') -RepoDir $Repo
    $revText = $rev.StdOut.Trim()
    if ([string]::IsNullOrEmpty($revText)) { $revText = '0' }
    $commitCount = 0
    [void][int]::TryParse($revText, [ref]$commitCount)
    if ($commitCount -ne 0) {
        $failures.Add("Disposable repo unexpectedly has $commitCount commit(s); evidence must never be committed.")
        Write-Host "[FAIL] disposable repo has $commitCount commit(s)" -ForegroundColor Red
    } else {
        Write-Host "[PASS] disposable repo has 0 commits (evidence never committed)"
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
