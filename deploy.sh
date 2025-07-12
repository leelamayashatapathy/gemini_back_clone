#!/bin/bash

echo "🚀 Gemini Backend Clone - Deployment Script"
echo "=========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
    git branch -M main
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env_sample.txt .env
    echo "✅ .env file created"
    echo "⚠️  Please update .env file with your actual API keys"
else
    echo "✅ .env file already exists"
fi

# Check requirements.txt
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Check render.yaml
if [ -f "render.yaml" ]; then
    echo "✅ render.yaml found"
else
    echo "❌ render.yaml not found"
    exit 1
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Update .env file with your API keys"
echo "2. Push to GitHub: git push origin main"
echo "3. Go to render.com and create new web service"
echo "4. Connect your GitHub repository"
echo "5. Set environment variables in Render dashboard"
echo "6. Deploy!"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions" 