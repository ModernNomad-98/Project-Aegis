#requires -Version 5.1
<#
.SYNOPSIS
    Focused negative + positive tests for Invoke-ScenarioAEvidence.ps1.

.DESCRIPTION
    Proves the harness's safety and append-only guarantees:
      * caller-owned directories are never deleted (only the owned run child is);
      * deleting a preserved "(none yet)" placeholder row FAILS append-only;
      * editing / deleting / reordering an immutable row FAILS;
      * a mutable projection-only refresh SUCCEEDS;
      * the complete low-risk batch (PS-002..PS-005 before the projection) SUCCEEDS;
      * an unexpected fixture file FAILS the run;
      * an additional commit in the disposable repo would be detected.

    Unit tests dot-source the harness with -LoadOnly (functions only, no main).
    Integration tests invoke the harness in a CHILD powershell.exe so its `exit`
    cannot terminate this script, and assert on the child's exit code.

    Run in Windows PowerShell 5.1:
      powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\acceptance\Test-ScenarioAEvidence.ps1
    Exit 0 = all tests passed; non-zero = one or more failed.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false) } catch { }

$ScriptDir   = $PSScriptRoot
$HarnessPath = Join-Path $ScriptDir 'Invoke-ScenarioAEvidence.ps1'
$RealFixtures = Join-Path $ScriptDir 'scenario-a-fixture\state-sequence'
$Utf8NoBom   = New-Object System.Text.UTF8Encoding($false)

$script:pass = 0
$script:fail = 0
$script:fails = New-Object System.Collections.Generic.List[string]
function Assert {
    param([bool] $Cond, [string] $Msg)
    if ($Cond) { $script:pass++; Write-Host "  [PASS] $Msg" -ForegroundColor Green }
    else { $script:fail++; $script:fails.Add($Msg); Write-Host "  [FAIL] $Msg" -ForegroundColor Red }
}

# Run the harness in a child process; return its exit code (its `exit` cannot kill us).
function Invoke-HarnessChild {
    param([string[]] $HarnessArgs)
    $out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $HarnessPath @HarnessArgs 2>&1
    $code = $LASTEXITCODE
    return [pscustomobject]@{ ExitCode = $code; Output = (@($out) -join "`n") }
}

$tmpRoots = New-Object System.Collections.Generic.List[string]
function New-TmpDir {
    param([string] $Tag)
    $p = Join-Path ([System.IO.Path]::GetTempPath()) ("sca-test-$Tag-" + ([guid]::NewGuid().ToString('N').Substring(0,8)))
    New-Item -ItemType Directory -Force -Path $p | Out-Null
    $tmpRoots.Add($p)
    return $p
}
function Copy-Fixtures {
    param([string] $Dest)
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    Get-ChildItem -LiteralPath $RealFixtures -Filter '*.md' -File | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $Dest $_.Name) -Force
    }
}

Write-Host "=== Test-ScenarioAEvidence ($($PSVersionTable.PSVersion)) ===`n"

# ---------------------------------------------------------------------------
# Part 1 - unit tests of the append-only comparator (dot-source, -LoadOnly)
# ---------------------------------------------------------------------------
Write-Host "Part 1 - append-only comparator unit tests"
. $HarnessPath -LoadOnly

$v00 = [System.IO.File]::ReadAllText((Join-Path $RealFixtures '00-cold-start.md'))
$v01 = [System.IO.File]::ReadAllText((Join-Path $RealFixtures '01-discovery-recorded.md'))
$v02 = [System.IO.File]::ReadAllText((Join-Path $RealFixtures '02-lowrisk-batch-recorded.md'))
$r00 = Get-ImmutableRows -Content $v00
$r01 = Get-ImmutableRows -Content $v01
$r02 = Get-ImmutableRows -Content $v02

Assert ((Test-AppendOnly -PrevRows $r00 -CurRows $r01).Ok) "valid append (00 -> 01: placeholder preserved, PS-001 + A-001 appended) succeeds"
Assert ((Test-AppendOnly -PrevRows $r01 -CurRows $r02).Ok) "complete low-risk batch (01 -> 02: PS-002..PS-005 appended) succeeds"

# projection-only refresh: same immutable rows, different projection prose -> OK
$v01proj = $v01 -replace 'front-desk receptionist \(internal\)', 'front-desk receptionist / reception team (internal)'
$aoProj = Test-AppendOnly -PrevRows $r01 -CurRows (Get-ImmutableRows -Content $v01proj)
Assert ($aoProj.Ok -and $aoProj.Added.Count -eq 0) "projection-only refresh (immutable rows unchanged) succeeds"

# placeholder deletion -> FAIL
$vDelPh = $v01 -replace '(?m)^\| \(none yet\) \| . \| \(none recorded . no decision has been recorded yet\).*$', ''
Assert (-not (Test-AppendOnly -PrevRows $r00 -CurRows (Get-ImmutableRows -Content $vDelPh)).Ok) "deleting a preserved (none yet) placeholder FAILS append-only"

# immutable row EDIT -> FAIL (change PS-001 date)
$vEdit = $v01 -replace 'PS-001 \| 2026-03-03', 'PS-001 | 2026-03-99'
Assert (-not (Test-AppendOnly -PrevRows $r01 -CurRows (Get-ImmutableRows -Content $vEdit)).Ok) "editing an existing immutable row (PS-001) FAILS append-only"

# immutable row DELETION -> FAIL (drop PS-001 from 01 vs 01)
$vDelRow = $v01 -replace '(?m)^\| PS-001 \|.*$', ''
Assert (-not (Test-AppendOnly -PrevRows $r01 -CurRows (Get-ImmutableRows -Content $vDelRow)).Ok) "deleting an existing evidence row (PS-001) FAILS append-only"

# immutable row REORDER -> FAIL (swap PS-002 and PS-003 in 02 vs 02)
$rowP2 = '| PS-002 | 2026-03-04 | Appointment slots'
$rowP3 = '| PS-003 | 2026-03-04 | The schedule screen'
$lines02 = $v02 -split "`r?`n"
$i2 = ($lines02 | Select-String -SimpleMatch $rowP2 | Select-Object -First 1).LineNumber - 1
$i3 = ($lines02 | Select-String -SimpleMatch $rowP3 | Select-Object -First 1).LineNumber - 1
$tmp = $lines02[$i2]; $lines02[$i2] = $lines02[$i3]; $lines02[$i3] = $tmp
$vReorder = ($lines02 -join "`n")
Assert (-not (Test-AppendOnly -PrevRows $r02 -CurRows (Get-ImmutableRows -Content $vReorder)).Ok) "reordering immutable rows (PS-002 <-> PS-003) FAILS append-only"

# ---------------------------------------------------------------------------
# Part 2 - integration: synthetic bad fixture dirs must FAIL the harness
# ---------------------------------------------------------------------------
Write-Host "`nPart 2 - bad fixture dirs must fail the full harness"

# (a) placeholder deleted in 01 -> harness FAILS
$badPh = Join-Path (New-TmpDir 'badph') 'seq'
Copy-Fixtures -Dest $badPh
$p01 = Join-Path $badPh '01-discovery-recorded.md'
$c01 = [System.IO.File]::ReadAllText($p01)
$c01 = $c01 -replace '(?m)^\| \(none yet\) \| . \| \(none recorded . no decision has been recorded yet\).*$', ''
[System.IO.File]::WriteAllText($p01, $c01, $Utf8NoBom)
$rPh = Invoke-HarnessChild -HarnessArgs @('-FixtureDir', $badPh)
Assert ($rPh.ExitCode -ne 0) "harness FAILS a fixture sequence whose 01 deletes a placeholder (exit $($rPh.ExitCode))"

# (b) an unexpected extra fixture file -> harness FAILS the exact-set check
$badExtra = Join-Path (New-TmpDir 'badextra') 'seq'
Copy-Fixtures -Dest $badExtra
[System.IO.File]::WriteAllText((Join-Path $badExtra '99-unexpected.md'), "# stray`n", $Utf8NoBom)
$rExtra = Invoke-HarnessChild -HarnessArgs @('-FixtureDir', $badExtra)
Assert ($rExtra.ExitCode -ne 0) "harness FAILS when an unexpected fixture file is present (exit $($rExtra.ExitCode))"

# (c) sanity: the copied REAL fixtures still pass through -FixtureDir
$good = Join-Path (New-TmpDir 'good') 'seq'
Copy-Fixtures -Dest $good
$rGood = Invoke-HarnessChild -HarnessArgs @('-FixtureDir', $good)
Assert ($rGood.ExitCode -eq 0) "harness PASSES the real fixture sequence via -FixtureDir (exit $($rGood.ExitCode))"

# ---------------------------------------------------------------------------
# Part 3 - caller-owned directory + sentinel is never deleted
# ---------------------------------------------------------------------------
Write-Host "`nPart 3 - caller-owned -WorkDir contents are never deleted"
$base = New-TmpDir 'owned'
$sentinel = Join-Path $base 'SENTINEL.txt'
[System.IO.File]::WriteAllText($sentinel, "do not delete me`n", $Utf8NoBom)
# a pre-existing product-repo/ that the harness must NOT touch
$preRepo = Join-Path $base 'product-repo'
New-Item -ItemType Directory -Force -Path $preRepo | Out-Null
$preFile = Join-Path $preRepo 'preexisting.txt'
[System.IO.File]::WriteAllText($preFile, "caller's own file`n", $Utf8NoBom)

$rOwned = Invoke-HarnessChild -HarnessArgs @('-WorkDir', $base)   # passing run, cleanup runs
Assert ($rOwned.ExitCode -eq 0) "harness run with caller -WorkDir passes (exit $($rOwned.ExitCode))"
Assert (Test-Path -LiteralPath $sentinel) "caller's SENTINEL.txt still exists after the run"
Assert (Test-Path -LiteralPath $preFile)  "caller's pre-existing product-repo/preexisting.txt is untouched"
$ownedChildren = @(Get-ChildItem -LiteralPath $base -Directory -Filter 'scenario-a-run-*' -ErrorAction SilentlyContinue)
Assert ($ownedChildren.Count -eq 0) "the harness's owned run child was cleaned up (none left under the caller dir)"

# ---------------------------------------------------------------------------
# Part 4 - additional-commit detection logic (the harness asserts 0 commits)
# ---------------------------------------------------------------------------
Write-Host "`nPart 4 - additional-commit detection"
$repo = Join-Path (New-TmpDir 'commit') 'r'
New-Item -ItemType Directory -Force -Path $repo | Out-Null
& git -C $repo init --quiet 2>&1 | Out-Null
& git -C $repo -c user.email='t@e.x' -c user.name='t' commit --allow-empty -m 'x' --quiet 2>&1 | Out-Null
$cnt = (& git -C $repo rev-list --count --all 2>&1 | Out-String).Trim()
Assert ($cnt -ne '0' -and $cnt -ne '') "git rev-list --count --all detects an added commit (count=$cnt); the harness's 0-commit assertion would fire"

# ---------------------------------------------------------------------------
# Cleanup + summary
# ---------------------------------------------------------------------------
foreach ($d in $tmpRoots) { try { if (Test-Path -LiteralPath $d) { Remove-Item -LiteralPath $d -Recurse -Force -ErrorAction SilentlyContinue } } catch { } }

Write-Host ""
if ($script:fail -eq 0) {
    Write-Host ("PASS - all {0} harness negative/positive test(s) passed." -f $script:pass) -ForegroundColor Green
    exit 0
} else {
    Write-Host ("FAIL - {0} passed, {1} failed:" -f $script:pass, $script:fail) -ForegroundColor Red
    foreach ($m in $script:fails) { Write-Host "  - $m" -ForegroundColor Red }
    exit 1
}
