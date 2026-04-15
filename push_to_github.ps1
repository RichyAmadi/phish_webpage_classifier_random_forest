# Push this repository to GitHub from Windows PowerShell
# Usage: .\push_to_github.ps1

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error 'Git is not installed or not in PATH.'
    exit 1
}

if (-not (Test-Path .git)) {
    git init
}

git add -A

if (-not (git diff --cached --quiet)) {
    git commit -m 'Initial commit'
}

$repoUrl = Read-Host 'Enter GitHub repository URL (for example https://github.com/YOUR-USER/YOUR-REPO.git)'
if (-not $repoUrl) {
    Write-Error 'GitHub repository URL is required.'
    exit 1
}

git remote remove origin -ErrorAction SilentlyContinue
git remote add origin $repoUrl

git branch -M main

git push -u origin main

Write-Host 'Repository pushed to GitHub successfully.'
