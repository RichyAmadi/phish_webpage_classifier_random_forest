# Deploy this project to Railway using the Railway CLI
# Usage: .\deploy_to_railway.ps1

if (-not (Get-Command railway -ErrorAction SilentlyContinue)) {
    Write-Error 'Railway CLI is not installed. Install it from https://railway.app/cli'
    exit 1
}

railway login

# Initialize the Railway project if it does not exist.
# If prompted, follow the interactive setup steps.
railway init --name phishing-webpage-classifier

# Deploy the current project.
railway up

Write-Host 'Railway deployment complete. Check the Railway dashboard for the generated URL.'
