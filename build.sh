#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

# Run migrations with error handling
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Create superuser if needed (optional)
echo "✅ Build completed successfully!" 