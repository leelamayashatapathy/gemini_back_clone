# PowerShell Deployment Script for Gemini Backend Clone

Write-Host "🚀 Gemini Backend Clone - Deployment Script" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit for deployment"
    git branch -M main
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item "env_sample.txt" ".env"
    Write-Host "✅ .env file created" -ForegroundColor Green
    Write-Host "⚠️  Please update .env file with your actual API keys" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Check requirements.txt
if (Test-Path "requirements.txt") {
    Write-Host "✅ requirements.txt found" -ForegroundColor Green
} else {
    Write-Host "❌ requirements.txt not found" -ForegroundColor Red
    exit 1
}

# Check render.yaml
if (Test-Path "render.yaml") {
    Write-Host "✅ render.yaml found" -ForegroundColor Green
} else {
    Write-Host "❌ render.yaml not found" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Update .env file with your API keys" -ForegroundColor White
Write-Host "2. Push to GitHub: git push origin main" -ForegroundColor White
Write-Host "3. Go to render.com and create new web service" -ForegroundColor White
Write-Host "4. Connect your GitHub repository" -ForegroundColor White
Write-Host "5. Set environment variables in Render dashboard" -ForegroundColor White
Write-Host "6. Deploy!" -ForegroundColor White
Write-Host ""
Write-Host "📖 See DEPLOYMENT_GUIDE.md for detailed instructions" -ForegroundColor Cyan 