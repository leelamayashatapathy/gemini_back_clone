# Gemini Backend Clone - Full Assessment Project

A complete Django REST Framework backend with OTP authentication, JWT, chatroom management, Google Gemini API integration, Stripe subscriptions, rate limiting, and Redis caching.

## Features

- **Authentication**: OTP-based authentication with JWT tokens
- **Chatrooms**: Real-time chat with AI responses via Google Gemini API
- **Subscriptions**: Stripe integration for subscription management
- **Rate Limiting**: Per-user rate limiting with Redis
- **Caching**: Redis-based caching for improved performance
- **Async Processing**: Celery for background tasks
- **Production Ready**: Configured for deployment on Render

## Tech Stack

- **Backend**: Django 5.2.4 + Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Cache & Broker**: Redis
- **Background Tasks**: Celery
- **AI Integration**: Google Gemini API
- **Payments**: Stripe
- **Deployment**: Render

## Production Deployment

### Environment Setup

Create a `.env` file in the `gemini_backend/` folder with:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database (for production, use PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com

# Stripe Settings
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key_here
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Gemini API Settings
GEMINI_API_KEY=your_gemini_api_key_here

# Celery Settings
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Quick Deployment on Render

1. **Push to GitHub**
```bash
git add .
git commit -m "Production ready"
git push origin main
```

2. **Deploy on Render**
- Go to [render.com](https://render.com) and sign up
- Click "New +" → "Blueprint"
- Connect your GitHub repository
- Click "Apply" to deploy

3. **Configure Environment Variables**
Add these in your Render web service settings:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
GEMINI_API_KEY=your-gemini-api-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
REDIS_URL=your-redis-url
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

4. **Deploy Worker Service**
Create a Background Worker service:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `celery -A gemini_backend worker --loglevel=info`
- Add the same environment variables

## API Endpoints

### Authentication
- `POST /auth/signup/` - User registration
- `POST /auth/send-otp/` - Send OTP (returns mock OTP)
- `POST /auth/verify-otp/` - Verify OTP and get JWT
- `POST /auth/forgot-password/` - Send password reset OTP
- `POST /auth/change-password/` - Change password (authenticated)

### Chatrooms
- `POST /chatroom/create/` - Create new chatroom
- `GET /chatroom/` - List user's chatrooms (cached)
- `GET /chatroom/{id}/` - Get chatroom details with messages
- `POST /chatroom/{id}/message/` - Send message (triggers AI response)

### Subscriptions
- `POST /subscription/pro/` - Create Stripe checkout session
- `GET /subscription/status/` - Get subscription status
- `POST /subscription/webhook/stripe/` - Stripe webhook handler

## Testing the API

### 1. Register a User
```bash
curl -X POST https://your-app-name.onrender.com/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"mobile": "1234567890", "password": "password123"}'
```

### 2. Send OTP
```bash
curl -X POST https://your-app-name.onrender.com/auth/send-otp/ \
  -H "Content-Type: application/json" \
  -d '{"mobile": "1234567890", "purpose": "login"}'
```

### 3. Verify OTP (get JWT)
```bash
curl -X POST https://your-app-name.onrender.com/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"mobile": "1234567890", "code": "123456", "purpose": "login"}'
```

### 4. Create Chatroom
```bash
curl -X POST https://your-app-name.onrender.com/chatroom/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"name": "My Chatroom"}'
```

### 5. Send Message (triggers AI response)
```bash
curl -X POST https://your-app-name.onrender.com/chatroom/1/message/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"content": "Hello AI!"}'
```

### 6. Subscribe to Pro
```bash
curl -X POST https://your-app-name.onrender.com/subscription/pro/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Project Structure

```
CLONE_GEMINI/
├── gemini_backend/          # Main Django project
│   ├── settings.py         # Production-ready settings
│   ├── urls.py            # URL configuration
│   ├── celery.py          # Celery configuration
│   └── wsgi.py           # WSGI application
├── authentication/         # OTP authentication app
├── chatrooms/            # Chatroom and messaging app
├── subscriptions/        # Stripe subscription app
├── core/                # Shared utilities and middleware
├── requirements.txt     # Python dependencies
├── render.yaml         # Render deployment config
├── Procfile           # Process definitions
└── runtime.txt        # Python version
```

## Key Components

### 1. **Authentication System**
- Custom User model with mobile number
- OTP-based verification
- JWT token authentication

### 2. **Chatroom Management**
- User-specific chatrooms
- Message history with AI responses
- Redis caching for performance

### 3. **AI Integration**
- Asynchronous Gemini API calls via Celery
- Context-aware conversations
- Error handling and retry logic

### 4. **Subscription System**
- Stripe integration for payments
- Webhook handling for subscription events
- Rate limiting based on subscription tier

### 5. **Production Features**
- Rate limiting middleware
- Global exception handling
- Comprehensive logging
- CORS configuration

## Environment Variables

### Required for Production
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `REDIS_URL`: Redis connection string
- `GEMINI_API_KEY`: Google Gemini API key

### Optional
- `STRIPE_*`: Stripe API keys for payment processing

## Development vs Production

### Local Development
- SQLite database
- Debug mode enabled
- Local Redis instance
- Celery with `--pool=solo` (Windows compatibility)

### Production (Render)
- SQLite database (or PostgreSQL)
- Debug mode disabled
- Redis service
- Gunicorn WSGI server
- Celery worker service

## Assessment Features

✅ **Working Authentication System**  
✅ **JWT Token Management**  
✅ **Chatroom Creation and Management**  
✅ **Real AI Integration with Gemini API**  
✅ **Stripe Payment Integration**  
✅ **Rate Limiting and Caching**  
✅ **Background Task Processing**  
✅ **Production Deployment Ready**  
✅ **Complete API Documentation**  

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start Redis (required for Celery and caching)
redis-server

# Start Celery worker (in new terminal)
celery -A gemini_backend worker --loglevel=info --pool=solo

# Run server
python manage.py runserver
```

## Notes for Assessment

- **Full AI Integration**: Real Google Gemini API calls
- **Complete Payment System**: Stripe subscription management
- **Advanced Caching**: Redis-based performance optimization
- **Background Processing**: Celery for async tasks
- **Rate Limiting**: Per-user request limiting
- **Production Ready**: Deploys successfully on Render

Perfect for comprehensive assessment! 🚀 