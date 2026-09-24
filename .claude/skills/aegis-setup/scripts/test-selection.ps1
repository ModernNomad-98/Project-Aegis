Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'selection.ps1')
$sandbox = Join-Path ([IO.Path]::GetTempPath()) ('aegis-setup-test-' + [guid]::NewGuid().ToString('N'))
$project = Join-Path $sandbox 'checkout'
$state = Join-Path $sandbox 'state'
[IO.Directory]::CreateDirectory($project) | Out-Null
$checks = 0
function Assert-Selection($condition, $message) {
    if (-not $condition) { throw "FAIL: $message" }
    $script:checks++
}
function Expect-Error($operation, $message) {
    $failed = $false
    try { & $operation | Out-Null } catch { $failed = $true }
    Assert-Selection $failed $message
}
try {
    $fresh = Read-AegisSelection $project $state
    Assert-Selection ($fresh.Status -eq 'unselected') 'missing record is unselected'
    $first = Save-AegisOnlySelection $project $state
    Assert-Selection ($first.Status -eq 'selected' -and $first.Record.choice -eq 'aegis-only') 'fresh selection'
    Assert-Selection ($first.Record.setup_completed_at_utc -eq $first.Record.selected_at_utc) 'completion timestamp'
    $again = Read-AegisSelection $project $state
    Assert-Selection ($again.Record.project_key -eq $first.Record.project_key) 'later session reads same project'
    $forwardProject = $project.Replace('\', '/')
    Assert-Selection ((Get-AegisSelectionPath $forwardProject $state).Key -ceq $first.Record.project_key) 'ordinary slash spelling keeps project key'
    foreach ($alias in @('\\?\', '\\.\', '//?/', '//./')) {
        $aliasProject = $alias + $project
        $aliasState = $alias + $state
        Expect-Error { Get-AegisSelectionPath $aliasProject $state } 'namespace project alias rejected'
        Expect-Error { Get-AegisSelectionPath $project $aliasState } 'namespace state alias rejected'
        Expect-Error { Get-AegisSelectionPath $project ($alias + (Join-Path $project 'state')) } 'inside state alias rejected'
    }
    foreach ($invalid in @('C:relative', '\root-relative', '\\server\share\folder', '//server/share/folder')) {
        Expect-Error { Get-AegisSelectionPath $invalid $state } 'nonlocal or relative project rejected'
        Expect-Error { Get-AegisSelectionPath $project $invalid } 'nonlocal or relative state rejected'
    }
    Expect-Error { Get-AegisSelectionPath $project ([IO.Path]::GetPathRoot($project)) } 'drive-root state rejected'
    Start-Sleep -Milliseconds 20
    $second = Save-AegisOnlySelection $project $state
    Assert-Selection ($second.Record.selected_at_utc -eq $first.Record.selected_at_utc) 'overwrite keeps original selection time'
    Assert-Selection ($second.Record.updated_at_utc -ge $first.Record.updated_at_utc) 'overwrite updates time'
    $beforeFailure = [IO.File]::ReadAllText($second.Path)
    Expect-Error { Save-AegisOnlySelection $project $state -TestFailBeforeCommit } 'failed write reports failure'
    Assert-Selection ([IO.File]::ReadAllText($second.Path) -ceq $beforeFailure) 'failed write preserves previous record'
    $location = Get-AegisSelectionPath $project $state
    $heldLock = [IO.File]::Open((Join-Path $state ($location.Key + '.lock')), 'OpenOrCreate', 'ReadWrite', 'None')
    try { Expect-Error { Save-AegisOnlySelection $project $state } 'concurrent writer rejected' }
    finally { $heldLock.Dispose() }
    $moved = Join-Path $sandbox 'moved-checkout'
    [IO.Directory]::Move($project, $moved)
    Assert-Selection ((Read-AegisSelection $moved $state).Status -eq 'unselected') 'moved checkout starts unselected'
    $movedSelection = Save-AegisOnlySelection $moved $state
    Assert-Selection ($movedSelection.Record.project_key -cne $first.Record.project_key) 'moved checkout has distinct key'
    $bad = $movedSelection.Record
    $bad.schema_version = 9
    [IO.File]::WriteAllText($movedSelection.Path, ($bad | ConvertTo-Json -Compress))
    Expect-Error { Read-AegisSelection $moved $state } 'unknown version fails closed'
    Expect-Error { Save-AegisOnlySelection $moved $state } 'unknown version not overwritten silently'
    [IO.File]::WriteAllText($movedSelection.Path, '{broken')
    Expect-Error { Read-AegisSelection $moved $state } 'corrupt JSON fails closed'
    Expect-Error { Save-AegisOnlySelection $moved $state } 'corrupt JSON not overwritten silently'
    $repaired = Save-AegisOnlySelection $moved $state -Repair
    Assert-Selection ($repaired.Status -eq 'selected') 'explicit repair restores Aegis-only selection'
    Expect-Error { Save-AegisOnlySelection $moved $state -Repair } 'valid record cannot be repaired'
    $canonicalRecord = [IO.File]::ReadAllText($movedSelection.Path)
    [IO.File]::WriteAllText($movedSelection.Path, $canonicalRecord.Replace('"schema_version":1', '"schema_version":"1"'))
    Expect-Error { Read-AegisSelection $moved $state } 'string schema version rejected'
    $duplicate = $canonicalRecord.TrimEnd('}') + ',"choice":"aegis-only"}'
    [IO.File]::WriteAllText($movedSelection.Path, $duplicate)
    Expect-Error { Read-AegisSelection $moved $state } 'duplicate JSON field rejected'
    $escapedDuplicate = $canonicalRecord.TrimEnd('}') + ',"\u0063hoice":"aegis-only"}'
    [IO.File]::WriteAllText($repaired.Path, $escapedDuplicate)
    Expect-Error { Read-AegisSelection $moved $state } 'escaped duplicate JSON field rejected'
    Expect-Error { Get-AegisSelectionPath $moved (Join-Path $moved 'state') } 'state under checkout rejected'
    Write-Output "PASS: $checks selection assertions"
} finally {
    $sandboxFull = [IO.Path]::GetFullPath($sandbox)
    $tempPrefix = [IO.Path]::GetFullPath([IO.Path]::GetTempPath()).TrimEnd('\') + '\'
    if (-not $sandboxFull.StartsWith($tempPrefix, [StringComparison]::OrdinalIgnoreCase) -or
        [IO.Path]::GetFileName($sandboxFull) -notmatch '^aegis-setup-test-[0-9a-f]{32}$') {
        throw 'Test cleanup target is outside the generated temporary fixture.'
    }
    if ([IO.Directory]::Exists($sandboxFull)) { [IO.Directory]::Delete($sandboxFull, $true) }
}
