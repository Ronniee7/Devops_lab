$ErrorActionPreference = "Stop"

Write-Host "`n=== Running Ruff Lint ===" -ForegroundColor Cyan
ruff check .

if ($LASTEXITCODE -ne 0) {
    throw "Linting failed."
}

Write-Host "`n=== Checking Code Formatting ===" -ForegroundColor Cyan
ruff format --check .

if ($LASTEXITCODE -ne 0) {
    throw "Formatting check failed."
}

Write-Host "`n=== Running Automated Tests ===" -ForegroundColor Cyan
python -m pytest -v

if ($LASTEXITCODE -ne 0) {
    throw "Automated tests failed."
}

Write-Host "`nAll quality checks passed!" -ForegroundColor Green