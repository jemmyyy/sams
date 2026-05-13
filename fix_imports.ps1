# Fix relative imports in backend apps - change `from ..` to `from .` for intra-app imports
$directories = @(
    "backend/apps/attendance",
    "backend/apps/cancellations",
    "backend/apps/communication",
    "backend/apps/groups",
    "backend/apps/players",
    "backend/apps/ratings",
    "backend/apps/reports",
    "backend/apps/sessions/services",
    "backend/apps/sessions/views",
    "backend/apps/sessions/serializers",
    "backend/apps/payments/views",
    "backend/apps/payments/services",
    "backend/apps/payments/serializers",
    "backend/apps/accounts/views"
)

$patterns = @(
    @{from='from \.\.models import'; to='from .models import'},
    @{from='from \.\.serializers import'; to='from .serializers import'},
    @{from='from \.\.serializers\.'; to='from .serializers.'},
    @{from='from \.\.services import'; to='from .services import'},
    @{from='from \.\.services\.'; to='from .services.'}
)

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Get-ChildItem -Path $dir -Recurse -Filter "*.py" | ForEach-Object {
            $content = Get-Content -Raw $_.FullName
            $changed = $false
            foreach ($pattern in $patterns) {
                if ($content -match $pattern.from) {
                    $content = $content -replace $pattern.from, $pattern.to
                    $changed = $true
                }
            }
            if ($changed) {
                [System.IO.File]::WriteAllText($_.FullName, $content, [System.Text.UTF8Encoding]::new($false))
                Write-Host "Fixed: $($_.FullName)"
            }
        }
    }
}
Write-Host "Done fixing imports"