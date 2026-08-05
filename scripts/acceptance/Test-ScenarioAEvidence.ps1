#requires -Version 5.1
<#
.SYNOPSIS
    Focused negative + positive tests for Invoke-ScenarioAEvidence.ps1.

.DESCRIPTION
    Proves the harness's safety, append-only, manifest, commit-count, and link-boundary
    guarantees. Integration cases launch the harness in a CHILD process using the CURRENT
    PowerShell host executable (pwsh for Core, powershell.exe for Desktop) - never a
    hard-coded binary - so this suite runs under both Windows PowerShell 5.1 and PowerShell 7.

    Run: <current host> -NoProfile -ExecutionPolicy Bypass -File Test-ScenarioAEvidence.ps1
    Exit 0 = all passed; non-zero = one or more failed.
#>
[CmdletBinding()] param()
$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false) } catch { }

$ScriptDir      = $PSScriptRoot
$HarnessPath    = Join-Path $ScriptDir 'Invoke-ScenarioAEvidence.ps1'
$FixtureRoot    = Join-Path $ScriptDir 'scenario-a-fixture'
$RealFixtures   = Join-Path $FixtureRoot 'state-sequence'
$RealManifest   = Join-Path $FixtureRoot 'manifest.json'
$RealArtifactDir = Join-Path $FixtureRoot 'artifact'
$SkillsRepoRoot = [System.IO.Path]::GetFullPath((Join-Path $ScriptDir '..\..'))
$Utf8NoBom      = New-Object System.Text.UTF8Encoding($false)

# --- F4: resolve the executable of the CURRENTLY running PowerShell host --------------
function Get-PSHostExe {
    $p = $null
    try { $p = (Get-Process -Id $PID -ErrorAction Stop).Path } catch { }
    if ($p -and (Test-Path -LiteralPath $p)) { return $p }
    if ($PSVersionTable.PSEdition -eq 'Core') { $c = Get-Command pwsh -ErrorAction SilentlyContinue }
    else { $c = Get-Command powershell -ErrorAction SilentlyContinue }
    if ($c -and $c.Source) { return $c.Source }
    throw "Cannot resolve the current PowerShell host executable."
}
$HostExe   = Get-PSHostExe
$OnWindows = ($PSVersionTable.PSEdition -ne 'Core') -or ($IsWindows -eq $true)

$script:pass = 0; $script:fail = 0
$script:fails = New-Object System.Collections.Generic.List[string]
function Assert {
    param([bool] $Cond, [string] $Msg)
    if ($Cond) { $script:pass++; Write-Host "  [PASS] $Msg" -ForegroundColor Green }
    else { $script:fail++; $script:fails.Add($Msg); Write-Host "  [FAIL] $Msg" -ForegroundColor Red }
}

function Invoke-HarnessChild {
    param([string[]] $HarnessArgs)
    $a = @('-NoProfile')
    if ($OnWindows) { $a += @('-ExecutionPolicy', 'Bypass') }
    $a += @('-File', $HarnessPath) + $HarnessArgs
    $out = & $HostExe @a 2>&1
    return [pscustomobject]@{ ExitCode = $LASTEXITCODE; Output = (@($out) -join "`n") }
}

$tmp = New-Object System.Collections.Generic.List[string]
function New-TmpDir { param([string] $Tag)
    $p = Join-Path ([System.IO.Path]::GetTempPath()) ("sca-test-$Tag-" + ([guid]::NewGuid().ToString('N').Substring(0, 8)))
    New-Item -ItemType Directory -Force -Path $p | Out-Null; $tmp.Add($p); return $p
}
# Copy the fixtures + manifest into a temp scenario-a-fixture layout; return the state-sequence dir.
function New-FixtureCopy { param([string] $Tag)
    $root = New-TmpDir $Tag
    $seq = Join-Path $root 'state-sequence'
    New-Item -ItemType Directory -Force -Path $seq | Out-Null
    Get-ChildItem -LiteralPath $RealFixtures -Filter '*.md' -File | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $seq $_.Name) -Force }
    Copy-Item -LiteralPath $RealManifest -Destination (Join-Path $root 'manifest.json') -Force
    if (Test-Path -LiteralPath $RealArtifactDir) {
        Copy-Item -LiteralPath $RealArtifactDir -Destination (Join-Path $root 'artifact') -Recurse -Force
    }
    return $seq
}
function Strip-Rows { param([string] $Content, [string] $IdRegex)
    return (($Content -split "`r?`n") | Where-Object { $_ -notmatch $IdRegex }) -join "`n"
}

Write-Host "=== Test-ScenarioAEvidence ($($PSVersionTable.PSVersion), edition $($PSVersionTable.PSEdition)) ==="
Write-Host "PowerShell host exe selected: $HostExe`n"

# --- Part 1: append-only comparator (dot-source functions, -LoadOnly) -----------------
Write-Host "Part 1 - append-only comparator"
. $HarnessPath -LoadOnly
$v00 = [System.IO.File]::ReadAllText((Join-Path $RealFixtures '00-cold-start.md'))
$v01 = [System.IO.File]::ReadAllText((Join-Path $RealFixtures '01-discovery-recorded.md'))
$v02 = [System.IO.File]::ReadAllText((Join-Path $RealFixtures '02-lowrisk-batch-recorded.md'))
$r00 = Get-ImmutableRows -Content $v00; $r01 = Get-ImmutableRows -Content $v01; $r02 = Get-ImmutableRows -Content $v02
Assert ((Test-AppendOnly -PrevRows $r00 -CurRows $r01).Ok) "valid append (00 -> 01) succeeds"
Assert ((Test-AppendOnly -PrevRows $r01 -CurRows $r02).Ok) "low-risk batch append (01 -> 02) succeeds"
$v01proj = $v01 -replace 'front-desk receptionist \(internal\)', 'front-desk receptionist / reception team (internal)'
Assert ((Test-AppendOnly -PrevRows $r01 -CurRows (Get-ImmutableRows -Content $v01proj)).Ok) "projection-only refresh succeeds"
Assert (-not (Test-AppendOnly -PrevRows $r00 -CurRows (Get-ImmutableRows -Content (Strip-Rows $v01 '^\| \(none yet\) \|.*decision has been recorded'))).Ok) "placeholder deletion FAILS append-only"
Assert (-not (Test-AppendOnly -PrevRows $r01 -CurRows (Get-ImmutableRows -Content ($v01 -replace 'PS-001 \| 2026-03-03', 'PS-001 | 2026-03-99'))).Ok) "immutable row edit FAILS"
Assert (-not (Test-AppendOnly -PrevRows $r01 -CurRows (Get-ImmutableRows -Content (Strip-Rows $v01 '^\| PS-001 \|'))).Ok) "evidence row deletion FAILS"

# --- Part 2: manifest conformance (hash + exact IDs) ----------------------------------
Write-Host "`nPart 2 - manifest conformance (hash + IDs)"
$mf = (Get-Content -Raw $RealManifest) | ConvertFrom-Json
$step01 = $mf.steps | Where-Object { $_.file -eq '01-discovery-recorded.md' }
$f01 = Join-Path $RealFixtures '01-discovery-recorded.md'
Assert ((Test-ManifestStep -Step $step01 -FilePath $f01 -Content $v01).Ok) "manifest step conforms for the real fixture"
$badHashStep = [pscustomobject]@{ file = $step01.file; sha256 = 'sha256:deadbeef'; snapshots = $step01.snapshots; decisions = $step01.decisions; approvals = $step01.approvals }
Assert (-not (Test-ManifestStep -Step $badHashStep -FilePath $f01 -Content $v01).Ok) "hash mismatch FAILS (fixture modified without updating the manifest)"
# duplicate an immutable ID in the content (hash from the real file stays valid -> isolates the ID check)
$dupLines = New-Object System.Collections.Generic.List[string]
foreach ($l in ($v01 -split "`r?`n")) { $dupLines.Add($l); if ($l -match '^\| PS-001 \|') { $dupLines.Add($l) } }
Assert (-not (Test-ManifestStep -Step $step01 -FilePath $f01 -Content ($dupLines -join "`n")).Ok) "duplicated immutable ID FAILS the manifest ID check"
$unexpLines = New-Object System.Collections.Generic.List[string]
foreach ($l in ($v01 -split "`r?`n")) { $unexpLines.Add($l); if ($l -match '^\| PS-001 \|') { $unexpLines.Add('| PS-999 | 2026-03-03 | stray | user | yes | x |') } }
Assert (-not (Test-ManifestStep -Step $step01 -FilePath $f01 -Content ($unexpLines -join "`n")).Ok) "unexpected immutable ID FAILS the manifest ID check"

# --- Part 2b: semantic gates (owners-before-Stage-3; acceptance-before-completion) ----
Write-Host "`nPart 2b - semantic gates"
$sem = $mf.semantics
Assert ((Test-SemanticGates -Steps $mf.steps -Semantics $sem).Ok) "semantic gates pass for the real manifest"
function Drop-Id { param($Steps, [string] $Id)
    return @($Steps | ForEach-Object { [pscustomobject]@{ file = $_.file; sha256 = $_.sha256; snapshots = @($_.snapshots); decisions = @($_.decisions | Where-Object { $_ -ne $Id }); approvals = @($_.approvals) } })
}
Assert (-not (Test-SemanticGates -Steps (Drop-Id $mf.steps 'PS-010') -Semantics $sem).Ok) "a Stage 2 owner (PS-010) removed from every step FAILS the semantic gate"
Assert (-not (Test-SemanticGates -Steps (Drop-Id $mf.steps 'PS-006') -Semantics $sem).Ok) "missing user spec acceptance (PS-006) FAILS the semantic gate"
Assert (-not (Test-SemanticGates -Steps (Drop-Id $mf.steps 'PS-007') -Semantics $sem).Ok) "missing product-spec owner completion (PS-007) FAILS the semantic gate"

# --- Part 2c: spec-artifact verification (R4-1) ---------------------------------------
Write-Host "`nPart 2c - spec-artifact verification"
$saSem  = $mf.semantics
$v08    = [System.IO.File]::ReadAllText((Join-Path $RealFixtures '08-stage3-snapshot.md'))
$accRow = @(($v08 -split "`r?`n") | Where-Object { $_ -match '^\|\s*PS-006\s*\|' }) -join "`n"
function New-SaSem { param($File, $Sha, $DecId, $Ipp)
    return [pscustomobject]@{ spec_artifact = [pscustomobject]@{ file = $File; sha256 = $Sha; decision_id = $DecId; in_product_path = $Ipp } }
}
$sa = $saSem.spec_artifact
Assert ((Test-SpecArtifact -Semantics $saSem -FixtureRoot $FixtureRoot -AcceptanceRowText $accRow).Ok) "spec-artifact verification passes for the real artifact + acceptance row"
Assert (-not (Test-SpecArtifact -Semantics (New-SaSem $sa.file ($sa.sha256 + 'a') $sa.decision_id $sa.in_product_path) -FixtureRoot $FixtureRoot -AcceptanceRowText $accRow).Ok) "a malformed pinned digest (not sha256:+64-hex) FAILS"
Assert (-not (Test-SpecArtifact -Semantics (New-SaSem $sa.file ('sha256:' + ('0' * 64)) $sa.decision_id $sa.in_product_path) -FixtureRoot $FixtureRoot -AcceptanceRowText $accRow).Ok) "a well-formed but wrong pinned digest FAILS (recomputed hash mismatch)"
Assert (-not (Test-SpecArtifact -Semantics $saSem -FixtureRoot $FixtureRoot -AcceptanceRowText '| PS-006 | 2026-03-06 | accepted | user | yes | no anchor here |').Ok) "an acceptance row lacking the digest and artifact path FAILS"
Assert (-not (Test-SpecArtifact -Semantics (New-SaSem 'artifact/does-not-exist.md' $sa.sha256 $sa.decision_id $sa.in_product_path) -FixtureRoot $FixtureRoot -AcceptanceRowText $accRow).Ok) "a missing artifact file FAILS"

# --- Part 3: bad fixture dirs FAIL the full harness -----------------------------------
Write-Host "`nPart 3 - bad fixtures fail the full harness"
# Expected-FAILURE runs preserve their evidence by design; give each a TRACKED -WorkDir so the
# preserved run child lands under a dir this suite cleans up, never loose in system temp (R4-6).
function Invoke-BadFixture { param([string] $SeqDir, [string] $Tag)
    return Invoke-HarnessChild -HarnessArgs @('-FixtureDir', $SeqDir, '-WorkDir', (New-TmpDir "wd-$Tag"))
}
function Artifact-Of { param([string] $SeqDir)
    return Join-Path (Split-Path -Parent $SeqDir) 'artifact\clinic-appointment-tracker-v1.md'
}
$badRow = New-FixtureCopy 'badrow'
foreach ($fn in @('07-commitment-readiness-na.md', '08-stage3-snapshot.md')) {
    $fp = Join-Path $badRow $fn; [System.IO.File]::WriteAllText($fp, (Strip-Rows ([System.IO.File]::ReadAllText($fp)) '^\| PS-010 \|'), $Utf8NoBom) }
Assert ((Invoke-BadFixture $badRow 'badrow').ExitCode -ne 0) "harness FAILS when a required row (PS-010) is removed from every later version"
$badHash = New-FixtureCopy 'badhash'
$fp = Join-Path $badHash '03-product-spec-accepted.md'; [System.IO.File]::WriteAllText($fp, ([System.IO.File]::ReadAllText($fp) -replace 'physiotherapy clinic', 'physiotherapy  clinic'), $Utf8NoBom)
Assert ((Invoke-BadFixture $badHash 'badhash').ExitCode -ne 0) "harness FAILS a fixture modified without updating its manifest hash"
$badAccept = New-FixtureCopy 'badaccept'
Get-ChildItem -LiteralPath $badAccept -Filter '*.md' | ForEach-Object { [System.IO.File]::WriteAllText($_.FullName, (Strip-Rows ([System.IO.File]::ReadAllText($_.FullName)) '^\| PS-006 \|'), $Utf8NoBom) }
Assert ((Invoke-BadFixture $badAccept 'badaccept').ExitCode -ne 0) "harness FAILS when the product-spec acceptance row (PS-006) is missing"
$badOwner = New-FixtureCopy 'badowner'
Get-ChildItem -LiteralPath $badOwner -Filter '*.md' | ForEach-Object { [System.IO.File]::WriteAllText($_.FullName, (Strip-Rows ([System.IO.File]::ReadAllText($_.FullName)) '^\| PS-007 \|'), $Utf8NoBom) }
Assert ((Invoke-BadFixture $badOwner 'badowner').ExitCode -ne 0) "harness FAILS when the product-spec owner-completion row (PS-007) is missing"
$badExtra = New-FixtureCopy 'badextra'
[System.IO.File]::WriteAllText((Join-Path $badExtra '99-unexpected.md'), "# stray`n", $Utf8NoBom)
Assert ((Invoke-BadFixture $badExtra 'badextra').ExitCode -ne 0) "harness FAILS on an unexpected fixture file"

# R4-1: the accepted-spec ARTIFACT is verified. A tampered artifact (its digest no longer matches
# the manifest pin) and a MISSING artifact both FAIL the full harness.
$badArt = New-FixtureCopy 'badart'
[System.IO.File]::AppendAllText((Artifact-Of $badArt), "`nTAMPERED - a line not in the accepted spec.`n", $Utf8NoBom)
Assert ((Invoke-BadFixture $badArt 'badart').ExitCode -ne 0) "harness FAILS when the accepted-spec artifact is tampered (digest no longer matches the pin)"
$noArt = New-FixtureCopy 'noart'
Remove-Item -LiteralPath (Split-Path -Parent (Artifact-Of $noArt)) -Recurse -Force
Assert ((Invoke-BadFixture $noArt 'noart').ExitCode -ne 0) "harness FAILS when the accepted-spec artifact fixture is missing"

# R4-6: a run that FAILS AFTER creating its evidence (tampered artifact) preserves that evidence
# under the TRACKED -WorkDir, so nothing leaks into system temp.
$leakBad = New-FixtureCopy 'leakbad'
[System.IO.File]::AppendAllText((Artifact-Of $leakBad), "`ntamper`n", $Utf8NoBom)
$leakWd = New-TmpDir 'leakwd'
$rl = Invoke-HarnessChild -HarnessArgs @('-FixtureDir', $leakBad, '-WorkDir', $leakWd)
Assert ($rl.ExitCode -ne 0) "the leak-probe run fails (tampered artifact) after creating evidence"
Assert (@(Get-ChildItem -LiteralPath $leakWd -Directory -Filter 'scenario-a-run-*' -ErrorAction SilentlyContinue).Count -ge 1) "an expected-failure run's preserved evidence is contained under the tracked -WorkDir (not leaked to temp)"

$good = New-FixtureCopy 'good'
Assert ((Invoke-HarnessChild -HarnessArgs @('-FixtureDir', $good)).ExitCode -eq 0) "harness PASSES the real fixture sequence (with its accepted-spec artifact) via -FixtureDir"

# --- Part 4: external-WorkDir ownership + physical link resolution (F6) ----------------
Write-Host "`nPart 4 - external-WorkDir + link resolution"
$base = New-TmpDir 'owned'
$sentinel = Join-Path $base 'SENTINEL.txt'; [System.IO.File]::WriteAllText($sentinel, "keep`n", $Utf8NoBom)
$preRepo = Join-Path $base 'product-repo'; New-Item -ItemType Directory -Force -Path $preRepo | Out-Null
$preFile = Join-Path $preRepo 'preexisting.txt'; [System.IO.File]::WriteAllText($preFile, "caller`n", $Utf8NoBom)
Assert ((Invoke-HarnessChild -HarnessArgs @('-WorkDir', $base)).ExitCode -eq 0) "harness passes with a normal external physical -WorkDir"
Assert (Test-Path -LiteralPath $sentinel) "caller SENTINEL.txt survives"
Assert (Test-Path -LiteralPath $preFile) "caller pre-existing product-repo/preexisting.txt untouched"
Assert (@(Get-ChildItem -LiteralPath $base -Directory -Filter 'scenario-a-run-*' -ErrorAction SilentlyContinue).Count -eq 0) "owned run child cleaned up under the caller dir"

if ($OnWindows) {
    $jparent = New-TmpDir 'junc'
    $junction = Join-Path $jparent 'link-inside'
    try {
        $madeLink = $false
        try { New-Item -ItemType Junction -Path $junction -Target $SkillsRepoRoot -ErrorAction Stop | Out-Null; $madeLink = $true } catch { }
        if ($madeLink) {
            $rj = Invoke-HarnessChild -HarnessArgs @('-WorkDir', $junction)
            Assert ($rj.ExitCode -ne 0) "harness REJECTS a junction -WorkDir whose physical target is inside the repo"
            Assert (@(Get-ChildItem -LiteralPath $SkillsRepoRoot -Directory -Filter 'scenario-a-run-*' -ErrorAction SilentlyContinue).Count -eq 0) "no run dir leaked into the skills repo via the junction"
            # R4-3: a link is resolved at EVERY component. -WorkDir <junction>/<existing-child>
            # (the junction targets the repo; 'docs' is an ordinary dir under it) must also be
            # rejected - the deepest existing component alone looks like a plain dir.
            $nested = Join-Path $junction 'docs'
            $rn = Invoke-HarnessChild -HarnessArgs @('-WorkDir', $nested)
            Assert ($rn.ExitCode -ne 0) "harness REJECTS -WorkDir nested BELOW a junction whose target is the repo"
            Assert (@(Get-ChildItem -LiteralPath $SkillsRepoRoot -Directory -Filter 'scenario-a-run-*' -ErrorAction SilentlyContinue).Count -eq 0) "no run dir leaked into the repo via a nested-below-junction WorkDir"
        } else {
            Write-Host "  [NOT-A-PASS] junction could not be created here; the Windows link-boundary case was NOT verified" -ForegroundColor Yellow
            $script:fail++; $script:fails.Add("Windows junction link-boundary test could not be created (explicitly NOT counted as a pass)")
        }
    } finally {
        # ALWAYS unlink ONLY the junction (Delete(path,$false) removes the reparse point, never
        # its target) so the later recursive cleanup can never follow it into the repo.
        if (Test-Path -LiteralPath $junction) { try { [System.IO.Directory]::Delete($junction, $false) } catch { } }
    }
} else {
    $sparent = New-TmpDir 'sym'
    $symlink = Join-Path $sparent 'link-inside'
    try {
        New-Item -ItemType SymbolicLink -Path $symlink -Target $SkillsRepoRoot | Out-Null
        $rs = Invoke-HarnessChild -HarnessArgs @('-WorkDir', $symlink)
        Assert ($rs.ExitCode -ne 0) "harness REJECTS a symbolic-link -WorkDir whose physical target is inside the repo"
    } finally {
        if (Test-Path -LiteralPath $symlink) { try { [System.IO.File]::Delete($symlink) } catch { try { (Get-Item -LiteralPath $symlink -Force).Delete() } catch { } } }
    }
}

# --- Part 5: fail-closed commit-count (F5) --------------------------------------------
Write-Host "`nPart 5 - fail-closed commit-count"
Assert ((Test-ZeroCommitCount -ExitCode 0 -StdOut "0`n" -StdErr '').Ok) "exit 0 + clean '0' accepts zero"
Assert (-not (Test-ZeroCommitCount -ExitCode 1 -StdOut '' -StdErr 'fatal').Ok) "nonzero git exit FAILS"
Assert (-not (Test-ZeroCommitCount -ExitCode 0 -StdOut '' -StdErr '').Ok) "empty output FAILS"
Assert (-not (Test-ZeroCommitCount -ExitCode 0 -StdOut 'abc' -StdErr '').Ok) "non-numeric output FAILS"
Assert (-not (Test-ZeroCommitCount -ExitCode 0 -StdOut "0`n0" -StdErr '').Ok) "multiple values FAIL"
Assert (-not (Test-ZeroCommitCount -ExitCode 0 -StdOut '-1' -StdErr '').Ok) "negative value FAILS"
Assert (-not (Test-ZeroCommitCount -ExitCode 0 -StdOut '99999999999999999999' -StdErr '').Ok) "overflow value FAILS"
Assert (-not (Test-ZeroCommitCount -ExitCode 0 -StdOut '3' -StdErr '').Ok) "unexpected positive count FAILS"

# --- cleanup + summary ----------------------------------------------------------------
foreach ($d in $tmp) { try { if (Test-Path -LiteralPath $d) { Remove-Item -LiteralPath $d -Recurse -Force -ErrorAction SilentlyContinue } } catch { } }
Write-Host ""
if ($script:fail -eq 0) {
    Write-Host ("PASS - all {0} test(s) passed (host: {1})." -f $script:pass, $HostExe) -ForegroundColor Green
    exit 0
} else {
    Write-Host ("FAIL - {0} passed, {1} failed:" -f $script:pass, $script:fail) -ForegroundColor Red
    foreach ($m in $script:fails) { Write-Host "  - $m" -ForegroundColor Red }
    exit 1
}
