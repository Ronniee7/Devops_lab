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

Write-Host "`n=== Running Automated Tests and Coverage ===" -ForegroundColor Cyan

python -m pytest `
    --cov=app `
    --cov-report=term-missing `
    --cov-report=html `
    --cov-fail-under=85 `
    -v

if ($LASTEXITCODE -ne 0) {
    throw "Tests or coverage requirements failed."
}

Write-Host "`nAll quality checks passed!" -ForegroundColor Green