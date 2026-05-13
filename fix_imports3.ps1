# Fix subdirectory files that need `..` to go from views/ -> app root
$subdir_files = @(
    "backend/apps/accounts/views/auth.py",
    "backend/apps/payments/views/financial.py",
    "backend/apps/payments/serializers/financial.py",
    "backend/apps/payments/services/financial.py",
    "backend/apps/sessions/views/session.py",
    "backend/apps/sessions/services/scheduling.py",
    "backend/apps/sessions/serializers/session.py"
)

foreach ($file in $subdir_files) {
    $content = Get-Content -Raw $file
    $content = $content -replace 'from \.models import', 'from ..models import'
    $content = $content -replace 'from \.serializers import', 'from ..serializers import'
    $content = $content -replace 'from \.serializers\.', 'from ..serializers.'
    $content = $content -replace 'from \.services import', 'from ..services import'
    $content = $content -replace 'from \.services\.', 'from ..services.'
    [System.IO.File]::WriteAllText($file, $content, [System.Text.UTF8Encoding]::new($false))
    Write-Host "Fixed: $file"
}

# Files at app root level should have single dot (`.`) imports, not `..`
$root_level_files = @(
    "backend/apps/players/views.py",
    "backend/apps/players/serializers.py",
    "backend/apps/attendance/views.py",
    "backend/apps/attendance/serializers.py",
    "backend/apps/cancellations/views.py",
    "backend/apps/cancellations/serializers.py",
    "backend/apps/communication/views.py",
    "backend/apps/communication/serializers.py",
    "backend/apps/groups/views.py",
    "backend/apps/groups/serializers.py",
    "backend/apps/ratings/views.py",
    "backend/apps/ratings/serializers.py",
    "backend/apps/reports/views.py",
    "backend/apps/reports/serializers.py"
)

foreach ($file in $root_level_files) {
    $content = Get-Content -Raw $file
    $content = $content -replace 'from \.\.models import', 'from .models import'
    $content = $content -replace 'from \.\.serializers import', 'from .serializers import'
    $content = $content -replace 'from \.\.serializers\.', 'from .serializers.'
    $content = $content -replace 'from \.\.services import', 'from .services import'
    $content = $content -replace 'from \.\.services\.', 'from .services.'
    [System.IO.File]::WriteAllText($file, $content, [System.Text.UTF8Encoding]::new($false))
    Write-Host "Fixed: $file"
}
Write-Host "Done"