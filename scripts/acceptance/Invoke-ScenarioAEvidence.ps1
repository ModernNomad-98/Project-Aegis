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
    Root directory to create the disposable repo + evidence under. Must be OUTSIDE this
    skills repo (the harness refuses otherwise). Defaults to a fresh unique directory
    under the system temp folder.

.NOTES
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
    [string] $WorkDir
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
# lists of EVIDENCE rows (ID-bearing: SS-/PS-/A-) and PLACEHOLDER rows (empty-state
# scaffolding). Mutable projection sections are ignored entirely.
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
        $evidence    = New-Object System.Collections.Generic.List[string]
        $placeholder = New-Object System.Collections.Generic.List[string]

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

                # Classify the row.
                $isPlaceholder = $false
                if ($ln -match '(?i)\(none recorded') { $isPlaceholder = $true }

                $firstCell = ''
                if ($ln -match '^\s*\|') {
                    $cells = $ln.Trim().Trim('|').Split('|')
                    if ($cells.Count -gt 0) { $firstCell = $cells[0].Trim() }
                    if ($firstCell -in @('(none yet)', '(none)', '-', '-', '')) { $isPlaceholder = $true }
                }

                $isEvidence = ($firstCell -match '^(SS|PS|A)-\d+$')

                if ($isEvidence) {
                    $evidence.Add($ln.Trim())
                } elseif ($isPlaceholder) {
                    $placeholder.Add($ln.Trim())
                } else {
                    # Unknown non-empty immutable row - treat as evidence so an accidental
                    # edit surfaces as a violation rather than being silently ignored.
                    $evidence.Add($ln.Trim())
                }
            }
        }

        $result[$key] = [pscustomobject]@{
            Evidence    = @($evidence)
            Placeholder = @($placeholder)
        }
    }
    return $result
}

# Assert that CUR is an append-only successor of PREV: in every immutable section, the
# ordered list of PREV's evidence rows must be an exact prefix of CUR's, and CUR may
# only ADD rows at the end. Placeholder (empty-state) rows may exist only while a section
# has zero evidence rows and may be dropped exactly when the first evidence row arrives
# (project-state schema rule 9). Mutable projection sections are not checked here.
function Test-AppendOnly {
    param(
        [Parameter(Mandatory)] $PrevRows,
        [Parameter(Mandatory)] $CurRows
    )
    $problems = New-Object System.Collections.Generic.List[string]
    $added    = New-Object System.Collections.Generic.List[string]

    foreach ($key in @('State snapshots', 'Decision log', 'Approvals', 'Deviations')) {
        $prevEv = @($PrevRows[$key].Evidence)
        $curEv  = @($CurRows[$key].Evidence)

        if ($curEv.Count -lt $prevEv.Count) {
            $problems.Add("[$key] evidence rows DROPPED (prev $($prevEv.Count) -> now $($curEv.Count)).")
        } else {
            for ($i = 0; $i -lt $prevEv.Count; $i++) {
                if ($curEv[$i] -ne $prevEv[$i]) {
                    $problems.Add("[$key] immutable row #$($i + 1) was edited/reordered.")
                }
            }
            if ($curEv.Count -gt $prevEv.Count) {
                for ($i = $prevEv.Count; $i -lt $curEv.Count; $i++) {
                    $added.Add("[$key] +$($curEv[$i])")
                }
            }
        }

        $curPh = @($CurRows[$key].Placeholder)
        if (($curPh.Count -gt 0) -and ($curEv.Count -gt 0)) {
            $problems.Add("[$key] empty-state placeholder present alongside real evidence.")
        }
    }

    return [pscustomobject]@{
        Ok       = ($problems.Count -eq 0)
        Problems = @($problems)
        Added    = @($added)
    }
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
$exitCode  = 1
$runPassed = $false
$failures  = New-Object System.Collections.Generic.List[string]

# Populated inside the try so the finally can report/clean them.
$WorkRoot = $null
$Repo     = $null
$Evidence = $null
$weCreatedWorkRoot = $false

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
    $FixtureDir     = Join-Path $ScriptDir 'scenario-a-fixture\state-sequence'
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

    # Resolve the work root (OUTSIDE the skills repo).
    if ([string]::IsNullOrWhiteSpace($WorkDir)) {
        $stamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
        $rand  = ([guid]::NewGuid().ToString('N')).Substring(0, 8)
        $WorkRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("scenario-a-evidence-$stamp-$rand")
        $weCreatedWorkRoot = $true
    } else {
        $WorkRoot = $WorkDir
        $weCreatedWorkRoot = $false
    }
    $WorkRoot = [System.IO.Path]::GetFullPath($WorkRoot)

    # Safety: never operate inside the skills repo.
    if (Path-IsInside -Child $WorkRoot -Parent $SkillsRepoRoot) {
        throw "Refusing to run: work dir '$WorkRoot' is inside the skills repo '$SkillsRepoRoot'. Evidence must live OUTSIDE the skills repo."
    }

    $Repo     = Join-Path $WorkRoot 'product-repo'
    $Evidence = Join-Path $WorkRoot 'evidence'
    $RepoDocs = Join-Path $Repo 'docs'

    New-Item -ItemType Directory -Force -Path $WorkRoot | Out-Null
    New-Item -ItemType Directory -Force -Path $Repo     | Out-Null
    New-Item -ItemType Directory -Force -Path $RepoDocs | Out-Null
    New-Item -ItemType Directory -Force -Path $Evidence | Out-Null

    Write-Host ("work root  : {0}" -f $WorkRoot)
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
    #   * Keep everything when -KeepEvidence is set OR when the run failed (so a failure
    #     can be inspected).
    #   * Otherwise clean up. Only ever remove directories the harness created, and never
    #     anything inside the skills repo (guaranteed by the earlier Path-IsInside guard).
    $keep = ($KeepEvidence -or (-not $runPassed))
    if ($keep) {
        if ($Evidence) { Write-Host ("Evidence kept at : {0}" -f $Evidence) }
        if ($Repo)     { Write-Host ("Disposable repo  : {0}" -f $Repo) }
    } else {
        try {
            if ($weCreatedWorkRoot) {
                if ($WorkRoot -and (Test-Path -LiteralPath $WorkRoot)) {
                    Remove-Item -LiteralPath $WorkRoot -Recurse -Force -ErrorAction SilentlyContinue
                }
            } else {
                if ($Repo     -and (Test-Path -LiteralPath $Repo))     { Remove-Item -LiteralPath $Repo     -Recurse -Force -ErrorAction SilentlyContinue }
                if ($Evidence -and (Test-Path -LiteralPath $Evidence)) { Remove-Item -LiteralPath $Evidence -Recurse -Force -ErrorAction SilentlyContinue }
            }
            Write-Host "Cleaned up disposable repo and evidence (run passed; -KeepEvidence not set)."
        } catch {
            Write-Host ("Cleanup warning: {0}" -f $_.Exception.Message)
        }
    }
}

exit $exitCode
