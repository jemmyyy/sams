$files = @(
    "backend/apps/attendance/models.py",
    "backend/apps/cancellations/models.py",
    "backend/apps/groups/models.py",
    "backend/apps/ratings/models.py",
    "backend/apps/reports/models.py"
)

foreach ($file in $files) {
    $content = Get-Content -Raw $file
    $content = $content -replace "'sessions\.([A-Z][a-zA-Z]+)'", "'training_sessions.$1'"
    [System.IO.File]::WriteAllText($file, $content, [System.Text.UTF8Encoding]::new($false))
    Write-Host "Fixed: $file"
}
Write-Host "Done"