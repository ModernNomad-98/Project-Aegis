# Aegis setup selection, Windows PowerShell 5.1. Dot-source for offline tests.
Set-StrictMode -Version Latest

function Get-AegisLocalFullPath {
    param([string]$Path, [string]$Label)
    # Namespace, UNC, rooted-relative, and drive-relative spellings can give
    # different project keys or defeat the state-inside-checkout comparison.
    if ($Path -notmatch '^[A-Za-z]:[\\/](?![\\/])') {
        throw "$Label path must be an ordinary absolute local drive path."
    }
    return [System.IO.Path]::GetFullPath($Path)
}

function Get-AegisCanonicalRoot {
    param([Parameter(Mandatory)][string]$ProjectRoot)
    $full = Get-AegisLocalFullPath $ProjectRoot 'Project'
    if ($full.Equals([System.IO.Path]::GetPathRoot($full), [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Project path must name a checkout directory.'
    }
    $full = $full.TrimEnd('\')
    if (-not [System.IO.Directory]::Exists($full)) { throw 'Project directory does not exist.' }
    $part = [System.IO.DirectoryInfo]$full
    while ($null -ne $part) {
        if (($part.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw 'Project path uses a redirect; choose its physical directory.'
        }
        $part = $part.Parent
    }
    return $full.ToUpperInvariant()
}

function Assert-AegisStateRoot {
    param([string]$StateRoot, [string]$ProjectRoot)
    $full = Get-AegisLocalFullPath $StateRoot 'State'
    if ($full.Equals([System.IO.Path]::GetPathRoot($full), [StringComparison]::OrdinalIgnoreCase)) {
        throw 'State path must name a directory below the drive root.'
    }
    $full = $full.TrimEnd('\')
    $project = Get-AegisCanonicalRoot $ProjectRoot
    if ($full.Equals($project, [StringComparison]::OrdinalIgnoreCase) -or
        $full.StartsWith($project + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw 'State path cannot be inside the checkout.'
    }
    $part = [System.IO.DirectoryInfo]$full
    while ($null -ne $part) {
        if ($part.Exists -and (($part.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)) {
            throw 'State path uses a redirect.'
        }
        $part = $part.Parent
    }
    return $full
}

function Get-AegisSelectionPath {
    param([string]$ProjectRoot, [string]$StateRoot)
    $root = Get-AegisCanonicalRoot $ProjectRoot
    $base = Assert-AegisStateRoot $StateRoot $ProjectRoot
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { $key = [BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($root))).Replace('-', '').ToLowerInvariant() }
    finally { $sha.Dispose() }
    return [pscustomobject]@{ Key = $key; Directory = $base; Path = [IO.Path]::Combine($base, "$key.json") }
}

function Get-AegisRecordPathKind {
    param([string]$Path)
    try { $attributes = [IO.File]::GetAttributes($Path) }
    catch [System.IO.FileNotFoundException] { return 'missing' }
    catch [System.IO.DirectoryNotFoundException] { return 'missing' }
    catch { throw "Selection record path cannot be inspected; inspect it manually before selecting again. $($_.Exception.Message)" }
    if (($attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw 'Selection record is a redirect; repair it manually.'
    }
    if (($attributes -band [IO.FileAttributes]::Directory) -ne 0) {
        throw 'Selection record path is occupied by a directory; inspect it manually before selecting again.'
    }
    return 'file'
}

function Read-AegisSelection {
    param([string]$ProjectRoot, [string]$StateRoot)
    $location = Get-AegisSelectionPath $ProjectRoot $StateRoot
    if ((Get-AegisRecordPathKind $location.Path) -eq 'missing') { return [pscustomobject]@{ Status='unselected'; Path=$location.Path; Record=$null } }
    try {
        $raw = [IO.File]::ReadAllText($location.Path, [Text.Encoding]::UTF8)
        $rawNames = @([regex]::Matches($raw, '"([A-Za-z_]+)"\s*:') | ForEach-Object { $_.Groups[1].Value.ToLowerInvariant() })
        if ($rawNames.Count -ne 8 -or @($rawNames | Select-Object -Unique).Count -ne 8) { throw 'Ambiguous record fields.' }
        $record = ConvertFrom-Json -InputObject $raw -ErrorAction Stop
        if ($raw -cne (ConvertTo-Json -InputObject $record -Compress -Depth 2)) {
            throw 'Noncanonical or ambiguous record encoding.'
        }
        $names = @($record.PSObject.Properties.Name | Sort-Object)
        $expected = @('choice','evidence_version','project_key','schema_version','selected_at_utc','setup_completed_at_utc','state','updated_at_utc' | Sort-Object)
        if (@(Compare-Object $names $expected -CaseSensitive).Count -ne 0) { throw 'Unexpected record fields.' }
        if (($record.schema_version -isnot [int] -and $record.schema_version -isnot [long]) -or
            $record.schema_version -ne 1 -or $record.project_key -cne $location.Key -or
            $record.choice -cne 'aegis-only' -or $record.state -cne 'selected' -or
            $record.evidence_version -cne 'package-2') { throw 'Unknown schema or unsupported choice/state.' }
        foreach ($field in @('selected_at_utc','updated_at_utc','setup_completed_at_utc')) {
            $value = [datetimeoffset]::MinValue
            if (-not [datetimeoffset]::TryParseExact($record.$field, 'yyyy-MM-ddTHH:mm:ss.fffZ',
                [Globalization.CultureInfo]::InvariantCulture,
                [Globalization.DateTimeStyles]::AssumeUniversal, [ref]$value)) { throw "Invalid $field." }
        }
        return [pscustomobject]@{ Status='selected'; Path=$location.Path; Record=$record }
    } catch { throw "Selection record is invalid or unsupported; choose 'Help me change my Aegis setup' to repair it. $($_.Exception.Message)" }
}

function Save-AegisOnlySelection {
    param([string]$ProjectRoot, [string]$StateRoot, [switch]$Repair, [switch]$TestFailBeforeCommit)
    if ($env:OS -ne 'Windows_NT') { throw 'Saved selections are supported only on tested Windows PowerShell.' }
    $location = Get-AegisSelectionPath $ProjectRoot $StateRoot
    [IO.Directory]::CreateDirectory($location.Directory) | Out-Null
    $null = Assert-AegisStateRoot $location.Directory $ProjectRoot
    $lockPath = [IO.Path]::Combine($location.Directory, "$($location.Key).lock")
    $lock = $null
    $deadline = [datetime]::UtcNow.AddSeconds(3)
    while ($null -eq $lock -and [datetime]::UtcNow -lt $deadline) {
        try { $lock = [IO.File]::Open($lockPath, [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None) }
        catch [System.IO.IOException] { Start-Sleep -Milliseconds 50 }
    }
    if ($null -eq $lock) { throw 'Another setup writer is active; retry later.' }
    $temp = $null
    try {
        $existing = (Get-AegisRecordPathKind $location.Path) -eq 'file'
        if ($Repair -and -not $existing) { throw 'No record needs repair.' }
        if ($Repair) {
            try { $null = Read-AegisSelection $ProjectRoot $StateRoot; throw 'Record is valid; use select.' }
            catch {
                if ($_.Exception.Message -notlike 'Selection record is invalid or unsupported*') { throw }
            }
            $prior = [pscustomobject]@{ Status='unselected'; Record=$null }
        } else { $prior = Read-AegisSelection $ProjectRoot $StateRoot }
        $now = [datetime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ss.fffZ', [Globalization.CultureInfo]::InvariantCulture)
        $selected = if ($prior.Status -eq 'selected') { $prior.Record.selected_at_utc } else { $now }
        $record = [ordered]@{ schema_version=1; project_key=$location.Key; choice='aegis-only'; state='selected'; selected_at_utc=$selected; updated_at_utc=$now; setup_completed_at_utc=$now; evidence_version='package-2' }
        $bytes = [Text.Encoding]::UTF8.GetBytes(($record | ConvertTo-Json -Compress))
        $temp = [IO.Path]::Combine($location.Directory, "$($location.Key).$([guid]::NewGuid().ToString('N')).tmp")
        $stream = [IO.File]::Open($temp, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
        try { $stream.Write($bytes, 0, $bytes.Length); $stream.Flush($true) } finally { $stream.Dispose() }
        if ($TestFailBeforeCommit) { throw 'Injected commit failure.' }
        if ($existing) {
            $backup = [IO.Path]::Combine($location.Directory, "$($location.Key).$([guid]::NewGuid().ToString('N')).bak")
            [IO.File]::Replace($temp, $location.Path, $backup)
            try { [IO.File]::Delete($backup) } catch { }
        } else { [IO.File]::Move($temp, $location.Path) }
        $temp = $null
        return Read-AegisSelection $ProjectRoot $StateRoot
    } finally {
        if ($null -ne $temp -and [IO.File]::Exists($temp)) { [IO.File]::Delete($temp) }
        $lock.Dispose()
    }
}

# From checkout root: $aegisProjectRoot = (Resolve-Path -LiteralPath .).ProviderPath
# Then: powershell -NoProfile -ExecutionPolicy Bypass -File .claude/skills/aegis-setup/scripts/selection.ps1 -Action status -ProjectRoot $aegisProjectRoot
# Replace status with select or repair for the requested action.
if ($MyInvocation.InvocationName -ne '.') {
    $arguments = @($args)
    if ($arguments.Length -ne 4 -or $arguments[0] -ne '-Action' -or $arguments[2] -ne '-ProjectRoot') {
        throw 'Usage: selection.ps1 -Action status|select|repair -ProjectRoot <absolute checkout path>'
    }
    $action = $arguments[1]; $project = $arguments[3]
    if ($PSVersionTable.PSEdition -ne 'Desktop' -or $env:OS -ne 'Windows_NT') {
        throw 'Saved-state commands are supported on Windows PowerShell 5.1 only.'
    }
    $local = [Environment]::GetFolderPath('LocalApplicationData')
    if ([string]::IsNullOrWhiteSpace($local)) { throw 'User-local application data path is unavailable.' }
    $state = [IO.Path]::Combine($local, 'ProjectAegis', 'setup', 'v1')
    if ($action -eq 'status') { Read-AegisSelection $project $state | ConvertTo-Json -Depth 4 }
    elseif ($action -eq 'select') { Save-AegisOnlySelection $project $state | ConvertTo-Json -Depth 4 }
    elseif ($action -eq 'repair') { Save-AegisOnlySelection $project $state -Repair | ConvertTo-Json -Depth 4 }
    else { throw 'Action must be status, select or repair.' }
}
