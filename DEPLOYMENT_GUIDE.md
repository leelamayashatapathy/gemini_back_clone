# 🚀 Deployment Guide - Gemini Backend Clone

This guide will help you deploy your Django project to Render.com

## 📋 Prerequisites

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Stripe Account** - For payment testing (already set up)
4. **Gemini API Key** - Optional for AI features

## 🔧 Step 1: Prepare Your Code

### 1.1 Create .env file (for local testing)
```bash
# Create .env file in your project root
cp env_sample.txt .env
```

### 1.2 Update .env with your keys
```env
# Django Settings
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com

# Stripe Test Keys (Get from Stripe Dashboard)
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Gemini API (Optional)
GEMINI_API_KEY=your_gemini_api_key_here

# Redis (Will be set by Render)
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=True
```

## 🌐 Step 2: Deploy to Render

### 2.1 Push to GitHub
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 2.2 Deploy on Render

1. **Go to [render.com](https://render.com)**
2. **Sign up/Login** with your GitHub account
3. **Click "New +"** → **"Web Service"**
4. **Connect your GitHub repository**
5. **Configure the service:**

#### Basic Settings:
- **Name**: `gemini-backend` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to you
- **Branch**: `main`

#### Build & Deploy Settings:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn gemini_backend.wsgi:application`

### 2.3 Set Environment Variables

In your Render dashboard, go to **Environment** tab and add:

```
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=false
ALLOWED_HOSTS=your-app-name.onrender.com
USE_SQLITE=true
CORS_ALLOW_ALL_ORIGINS=true
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2.4 Add Redis Service

1. **Go back to Render dashboard**
2. **Click "New +"** → **"Redis"**
3. **Configure:**
   - **Name**: `gemini-backend-redis`
   - **Region**: Same as your web service
   - **Plan**: Free (for testing)

### 2.5 Link Redis to Web Service

1. **Go to your web service settings**
2. **Add environment variable:**
   - **Key**: `REDIS_URL`
   - **Value**: Copy from your Redis service connection string

## 🔄 Step 3: Deploy and Test

### 3.1 Deploy
1. **Click "Deploy"** in your web service
2. **Wait for build to complete** (5-10 minutes)
3. **Check logs** for any errors

### 3.2 Test Your Deployment

Your app will be available at: `https://your-app-name.onrender.com`

#### Test Endpoints:
```bash
# Health check
curl https://your-app-name.onrender.com/

# Send OTP
curl -X POST https://your-app-name.onrender.com/auth/send-otp/ \
  -H "Content-Type: application/json" \
  -d '{"mobile": "1234567890", "purpose": "login"}'

# Create subscription
curl -X POST https://your-app-name.onrender.com/subscriptions/create-checkout/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"price_id": "price_test"}'
```

## 🔧 Step 4: Set Up Webhooks (After Deployment)

### 4.1 Configure Stripe Webhook
1. **Go to [Stripe Dashboard](https://dashboard.stripe.com/test/webhooks)**
2. **Click "Add endpoint"**
3. **Set URL**: `https://your-app-name.onrender.com/subscriptions/webhook/`
4. **Select events**:
   - `checkout.session.completed`
   - `customer.subscription.deleted`
   - `customer.subscription.updated`
5. **Copy the webhook secret** and add to Render environment variables

## 🚨 Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check `requirements.txt` is complete
   - Verify Python version in `runtime.txt`

2. **App Crashes**
   - Check logs in Render dashboard
   - Verify environment variables are set

3. **Database Issues**
   - Run migrations: `python manage.py migrate`
   - Check SQLite file permissions

4. **Redis Connection**
   - Verify Redis URL is correct
   - Check Redis service is running

### Debug Commands:
```bash
# Check logs
# In Render dashboard → Logs tab

# Test locally with production settings
python manage.py runserver --settings=gemini_backend.settings
```

## 📊 Step 5: Monitor and Scale

### 5.1 Monitor Performance
- **Render Dashboard** → **Metrics** tab
- **Check response times** and **error rates**

### 5.2 Scale if Needed
- **Upgrade to paid plan** for better performance
- **Add more workers** for Celery tasks
- **Use PostgreSQL** for production database

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render web service created
- [ ] Redis service created and linked
- [ ] Environment variables set
- [ ] Build successful
- [ ] App accessible via URL
- [ ] Authentication working
- [ ] Payment flow working
- [ ] Webhooks configured
- [ ] Error monitoring set up

## 🎯 Next Steps

1. **Test all features** on deployed app
2. **Set up monitoring** (optional)
3. **Configure custom domain** (optional)
4. **Set up CI/CD** for automatic deployments

## 📞 Support

If you encounter issues:
1. **Check Render logs** first
2. **Verify environment variables**
3. **Test endpoints** with curl/Postman
4. **Check Django logs** for detailed errors

---

**Your app will be live at**: `https://your-app-name.onrender.com`

**API Documentation**: `https://your-app-name.onrender.com/admin/` (Django admin) 