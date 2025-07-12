# Production Deployment Checklist

## ✅ Pre-Deployment Checklist

### Environment Variables
- [ ] `SECRET_KEY` - Strong, unique secret key
- [ ] `DEBUG=False` - Debug mode disabled
- [ ] `ALLOWED_HOSTS` - Configured for your domain
- [ ] `GEMINI_API_KEY` - Valid Gemini API key
- [ ] `REDIS_URL` - Redis connection string
- [ ] `CORS_ALLOWED_ORIGINS` - Frontend domain(s)
- [ ] `STRIPE_*` - Stripe API keys (if using payments)

### Security
- [ ] Django secret key is secure and unique
- [ ] Debug mode is disabled
- [ ] CORS settings are properly configured
- [ ] HTTPS is enabled (production)
- [ ] Database credentials are secure
- [ ] API keys are not exposed in code

### Database
- [ ] Database migrations are applied
- [ ] Database is properly configured
- [ ] Backup strategy is in place

### Dependencies
- [ ] All required packages are in `requirements.txt`
- [ ] Package versions are pinned
- [ ] No development dependencies in production

### Static Files
- [ ] Static files are collected (`python manage.py collectstatic`)
- [ ] Static file serving is configured
- [ ] Media files are properly handled

## 🚀 Deployment Steps

### 1. Local Testing
```bash
# Test with production settings
export DEBUG=False
python manage.py check --deploy
python manage.py collectstatic --noinput
python manage.py runserver
```

### 2. Git Preparation
```bash
# Remove any sensitive files
git status
git add .
git commit -m "Production ready"
git push origin main
```

### 3. Environment Setup
- Create `.env` file in `gemini_backend/` folder
- Configure all environment variables
- Test environment variable loading

### 4. Database Setup
```bash
# Apply migrations
python manage.py migrate

# Create superuser (if needed)
python manage.py createsuperuser
```

### 5. Celery Setup
```bash
# Start Celery worker
celery -A gemini_backend worker --loglevel=info

# Start Celery beat (if using scheduled tasks)
celery -A gemini_backend beat --loglevel=info
```

## 🔧 Production Configuration

### Render Deployment
1. **Web Service**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn gemini_backend.wsgi:application`
   - Environment variables configured

2. **Worker Service**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `celery -A gemini_backend worker --loglevel=info`
   - Same environment variables as web service

### Environment Variables Template
```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com

# Database
DATABASE_URL=your-database-url

# Redis
REDIS_URL=your-redis-url

# CORS
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://your-frontend.com

# API Keys
GEMINI_API_KEY=your-gemini-api-key
STRIPE_PUBLISHABLE_KEY=your-stripe-key
STRIPE_SECRET_KEY=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-webhook-secret

# Celery
CELERY_BROKER_URL=your-redis-url
CELERY_RESULT_BACKEND=your-redis-url
```

## 📊 Monitoring & Maintenance

### Health Checks
- [ ] API endpoints are responding
- [ ] Database connections are working
- [ ] Redis is accessible
- [ ] Celery tasks are processing
- [ ] Static files are serving

### Logs
- [ ] Application logs are being collected
- [ ] Error logs are being monitored
- [ ] Performance metrics are tracked

### Backup Strategy
- [ ] Database backups are scheduled
- [ ] Static files are backed up
- [ ] Environment variables are documented

## 🚨 Troubleshooting

### Common Issues
1. **Environment Variables Not Loading**
   - Check `.env` file location
   - Verify variable names
   - Restart application

2. **Database Connection Issues**
   - Verify database URL
   - Check network connectivity
   - Ensure database exists

3. **Celery Worker Not Starting**
   - Check Redis connection
   - Verify Celery configuration
   - Check worker logs

4. **Static Files Not Loading**
   - Run `collectstatic`
   - Check static file settings
   - Verify file permissions

### Performance Optimization
- [ ] Database queries are optimized
- [ ] Caching is properly configured
- [ ] Static files are compressed
- [ ] Rate limiting is configured

## ✅ Post-Deployment Verification

1. **API Testing**
   - Test authentication endpoints
   - Test chatroom functionality
   - Test AI integration
   - Test subscription endpoints

2. **Performance Testing**
   - Load test critical endpoints
   - Monitor response times
   - Check memory usage

3. **Security Testing**
   - Verify HTTPS is working
   - Test CORS configuration
   - Check for exposed secrets

4. **Monitoring Setup**
   - Set up error alerting
   - Configure performance monitoring
   - Set up uptime monitoring 