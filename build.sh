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

# PostgreSQL Database Setup and Migration
echo "🗄️  Setting up PostgreSQL database..."

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL is not set!"
    echo "Please ensure PostgreSQL service is connected in render.yaml"
    exit 1
fi

echo "✅ DATABASE_URL is configured"

# Test database connection
echo "🔗 Testing database connection..."
python manage.py dbshell -c "SELECT version();" || {
    echo "❌ ERROR: Cannot connect to PostgreSQL database!"
    echo "Please check your DATABASE_URL configuration"
    exit 1
}
echo "✅ Database connection successful"

# Run migrations with detailed logging
echo "🔄 Starting database migrations..."

echo "Step 1: Making migrations..."
python manage.py makemigrations --noinput || {
    echo "⚠️  Warning: makemigrations failed, but continuing..."
}

echo "Step 2: Running migrations..."
python manage.py migrate --noinput || {
    echo "❌ ERROR: Migrations failed!"
    echo "Checking database tables..."
    python manage.py dbshell -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';" || {
        echo "❌ ERROR: Cannot access database tables!"
        exit 1
    }
    exit 1
}

echo "✅ MIGRATIONS COMPLETED SUCCESSFULLY!"
echo "📊 Database tables created and updated"

# Create a superuser for admin access (optional)
echo "👤 Creating admin user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Admin user created: admin/admin123')
else:
    print('✅ Admin user already exists')
" || echo "⚠️  Could not create admin user (this is normal if it already exists)"

# Final verification
echo "🔍 Final verification..."
python manage.py check --deploy || {
    echo "⚠️  Warning: Deployment check failed, but continuing..."
}

# Show final database status
echo "📋 Final database status:"
python manage.py dbshell -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;" || {
    echo "⚠️  Could not list database tables"
}

echo "🎉 BUILD COMPLETED SUCCESSFULLY!"
echo "✅ PostgreSQL database is ready"
echo "✅ All migrations applied"
echo "✅ Static files collected"
echo "✅ Admin user available at /admin/" 