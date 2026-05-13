$content = Get-Content -Raw docker/backend/entrypoint.sh
$content = $content -replace "`r`n", "`n"
[System.IO.File]::WriteAllText('docker/backend/entrypoint.sh', $content, [System.Text.UTF8Encoding]::new($false))
Write-Host 'Fixed line endings'