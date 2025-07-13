# 🤖 Gemini Backend Clone - AI-Powered Chat Platform

A sophisticated Django REST Framework backend that creates an AI-powered chat experience using Google's Gemini API. This project demonstrates real-time messaging, OTP authentication, subscription management, and intelligent AI responses.

##  Features

###  **Authentication & Security**
- **OTP-based Authentication**: Secure mobile verification system
- **JWT Token Management**: Stateless authentication with refresh tokens
- **Rate Limiting**: Per-user request throttling with Redis
- **CORS Protection**: Cross-origin resource sharing configuration

###  **AI-Powered Chatrooms**
- **Real-time Messaging**: Instant message delivery and responses
- **Google Gemini Integration**: Advanced AI responses using Google's latest model
- **Context Awareness**: AI remembers conversation history
- **Asynchronous Processing**: Background task processing with Celery

###  **Subscription Management**
- **Stripe Integration**: Secure payment processing
- **Tier-based Access**: Different features for free vs pro users
- **Webhook Handling**: Real-time subscription event processing
- **Payment Security**: PCI-compliant payment handling

###  **Production Ready**
- **Redis Caching**: High-performance data caching
- **Background Tasks**: Celery worker for async operations
- **Error Handling**: Comprehensive exception management
- **Logging**: Detailed application monitoring
- **Deployment Ready**: Configured for Render hosting

##  Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | Django 5.2.4 + DRF | RESTful API development |
| **Authentication** | JWT (SimpleJWT) | Stateless user sessions |
| **Database** | PostgreSQL (prod) / SQLite (dev) | Data persistence |
| **Cache & Message Broker** | Redis | Caching & task queuing |
| **Background Tasks** | Celery | Asynchronous processing |
| **AI Integration** | Google Gemini API | Intelligent responses |
| **Payments** | Stripe | Subscription management |
| **Deployment** | Render | Cloud hosting platform |

##  Quick Start

### Prerequisites
- Python 3.12+
- Redis server
- PostgreSQL (for production)
- Google Gemini API key
- Stripe account (for payments)

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/gemini-backend-clone.git
cd gemini-backend-clone
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the project root:



### 3. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Optional
```

### 4. Start Services
```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Celery Worker
celery -A gemini_backend worker --loglevel=info -P eventlet

# Terminal 3: Start Django Server
python manage.py runserver
```

##  API Endpoints

### Authentication Flow
```bash
# 1. Register User
POST /auth/signup/
{
  "mobile": "1234567890",
  "password": "securepassword123"
}

# 2. Send OTP
POST /auth/send-otp/
{
  "mobile": "1234567890",
  "purpose": "login"
}

# 3. Verify OTP & Get JWT
POST /auth/verify-otp/
{
  "mobile": "1234567890",
  "code": "123456",
  "purpose": "login"
}
```

### Chatroom Management
```bash
# Create Chatroom
POST /chatroom/create/
Authorization: Bearer <JWT_TOKEN>
{
  "name": "My AI Assistant"
}

# List User's Chatrooms
GET /chatroom/
Authorization: Bearer <JWT_TOKEN>

# Get Chatroom with Messages
GET /chatroom/{id}/
Authorization: Bearer <JWT_TOKEN>

# Send Message (Triggers AI Response)
POST /chatroom/{id}/message/
Authorization: Bearer <JWT_TOKEN>
{
  "content": "Hello AI! How are you today?"
}
```

### Subscription Management
```bash
# Create Pro Subscription
POST /subscription/pro/
Authorization: Bearer <JWT_TOKEN>

# Check Subscription Status
GET /subscription/status/
Authorization: Bearer <JWT_TOKEN>
```

## 🌐 Production Deployment

### Render Deployment (Recommended)

1. **Push to GitHub**
```bash
git add .
git commit -m "Production ready"
git push origin main
```



### Using Postman

1. **Import Collection**: Use the provided Postman collection
2. **Set Environment Variables**: Add your base URL and JWT tokens
3. **Test Flow**: Follow the authentication → chatroom → messaging flow


## 🔧 Key Components

### 1. **Authentication System** 🔐
- **Custom User Model**: Mobile-based user identification
- **OTP Verification**: Secure one-time password system
- **JWT Tokens**: Stateless authentication with refresh capability
- **Password Management**: Secure password change functionality

### 2. **AI Chat System** 🤖
- **Gemini Integration**: Google's latest AI model
- **Context Management**: Conversation history tracking
- **Async Processing**: Background AI response generation
- **Error Handling**: Graceful AI service failures

### 3. **Subscription System** 💳
- **Stripe Integration**: Professional payment processing
- **Webhook Handling**: Real-time subscription events
- **Tier Management**: Feature access based on subscription
- **Payment Security**: PCI-compliant handling

### 4. **Performance & Scalability** ⚡
- **Redis Caching**: High-performance data storage
- **Rate Limiting**: Request throttling per user
- **Background Tasks**: Celery for async operations
- **Error Monitoring**: Comprehensive logging system

## 🔒 Security Features

- **JWT Authentication**: Secure token-based sessions
- **Rate Limiting**: Protection against abuse
- **CORS Configuration**: Cross-origin security
- **Input Validation**: Comprehensive data sanitization
- **Error Handling**: Secure error responses

## 📊 Performance Optimizations

- **Redis Caching**: Frequently accessed data caching
- **Database Optimization**: Efficient query patterns
- **Async Processing**: Non-blocking AI operations
- **Connection Pooling**: Database connection management
- **Static File Handling**: Optimized file serving


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## 🎯  Features

| Feature | Status | Description |
|---------|--------|-------------|
| ✅ **Authentication** | Complete | OTP + JWT system |
| ✅ **AI Integration** | Complete | Gemini API integration |
| ✅ **Real-time Chat** | Complete | Async message processing |
| ✅ **Payment System** | Complete | Stripe subscription management |
| ✅ **Rate Limiting** | Complete | Per-user request throttling |
| ✅ **Caching** | Complete | Redis-based performance optimization |
| ✅ **Background Tasks** | Complete | Celery worker implementation |
| ✅ **Production Ready** | Complete | Render deployment configuration |
| ✅ **API Documentation** | Complete | Comprehensive endpoint documentation |

---

**Built with ❤️ using Django, Redis, Celery, and Google Gemini API**
