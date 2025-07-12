#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Show environment info for debugging
echo "🔍 Environment check:"
echo "DATABASE_URL: ${DATABASE_URL:0:50}..."
echo "REDIS_URL: ${REDIS_URL:0:50}..."
echo "DEBUG: $DEBUG"
echo "ALLOWED_HOSTS: $ALLOWED_HOSTS"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

# Run migrations with detailed error handling
echo "🔄 Running database migrations..."
echo "Step 1: Making migrations..."
python manage.py makemigrations --noinput || {
    echo "⚠️  Warning: makemigrations failed, but continuing..."
}

echo "Step 2: Running migrations..."
python manage.py migrate --noinput || {
    echo "❌ Error: Migrations failed!"
    echo "Checking database connection..."
    python manage.py dbshell -c "SELECT version();" || {
        echo "❌ Database connection failed!"
        exit 1
    }
    exit 1
}

echo "✅ Migrations completed successfully!"

# Create a superuser for admin access (optional)
echo "👤 Creating admin user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created: admin/admin123')
else:
    print('Admin user already exists')
" || echo "⚠️  Could not create admin user (this is normal if it already exists)"

# Final verification
echo "🔍 Final verification..."
python manage.py check --deploy || {
    echo "⚠️  Warning: Deployment check failed, but continuing..."
}

echo "✅ Build completed successfully!" 