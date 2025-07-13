# 🤖 Gemini Backend Clone - API Endpoints Collection

**Base URL**: `https://gemini-back-clone.onrender.com`

---

## 🔐 Authentication Endpoints

### 1. User Registration
- **URL**: `https://gemini-back-clone.onrender.com/auth/signup/`
- **Method**: `POST`
- **Description**: Register a new user with mobile number and password
- **Request Body**:
```json
{
    "mobile": "1234567890",
    "password": "your_secure_password"
}
```
- **Response**:
```json
{
    "success": true,
    "message": "User registered successfully. Please verify your mobile number.",
    "data": {
        "mobile": "1234567890"
    }
}
```

### 2. Send OTP
- **URL**: `https://gemini-back-clone.onrender.com/auth/send-otp/`
- **Method**: `POST`
- **Description**: Send OTP to mobile number for verification
- **Request Body**:
```json
{
    "mobile": "1234567890",
    "purpose": "login"
}
```
- **Response**:
```json
{
    "success": true,
    "message": "OTP sent successfully to 1234567890"
}
```

### 3. Verify OTP
- **URL**: `https://gemini-back-clone.onrender.com/auth/verify-otp/`
- **Method**: `POST`
- **Description**: Verify OTP and get JWT tokens
- **Request Body**:
```json
{
    "mobile": "1234567890",
    "code": "123456",
    "purpose": "login"
}
```
- **Response**:
```json
{
    "success": true,
    "message": "OTP verified successfully",
    "data": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": 1,
            "mobile": "1234567890",
            "is_verified": true
        }
    }
}
```

### 4. Forgot Password
- **URL**: `https://gemini-back-clone.onrender.com/auth/forgot-password/`
- **Method**: `POST`
- **Description**: Send OTP for password reset
- **Request Body**:
```json
{
    "mobile": "1234567890"
}
```
- **Response**:
```json
{
    "success": true,
    "message": "Password reset OTP sent successfully"
}
```

### 5. Change Password
- **URL**: `https://gemini-back-clone.onrender.com/auth/change-password/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <access_token>`
- **Description**: Change user password
- **Request Body**:
```json
{
    "old_password": "old_password",
    "new_password": "new_secure_password"
}
```
- **Response**:
```json
{
    "success": true,
    "message": "Password changed successfully"
}
```

### 6. User Profile
- **URL**: `https://gemini-back-clone.onrender.com/auth/me/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <access_token>`
- **Description**: Get current user profile
- **Response**:
```json
{
    "success": true,
    "data": {
        "id": 1,
        "mobile": "1234567890",
        "is_verified": true,
        "date_joined": "2024-01-01T00:00:00Z"
    }
}
```

---

## 💬 Chatroom Endpoints

### 7. List Chatrooms
- **URL**: `https://gemini-back-clone.onrender.com/chatroom/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <access_token>`
- **Description**: Get all chatrooms for the authenticated user
- **Response**:
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "AI Assistant",
            "created_at": "2024-01-01T00:00:00Z",
            "last_message": {
                "content": "Hello! How can I help you today?",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }
    ]
}
```

### 8. Chatroom Detail
- **URL**: `https://gemini-back-clone.onrender.com/chatroom/{chatroom_id}/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <access_token>`
- **Description**: Get chatroom details and messages
- **Response**:
```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "AI Assistant",
        "created_at": "2024-01-01T00:00:00Z",
        "messages": [
            {
                "id": 1,
                "content": "Hello! How can I help you today?",
                "is_ai": true,
                "timestamp": "2024-01-01T12:00:00Z"
            },
            {
                "id": 2,
                "content": "Tell me a joke",
                "is_ai": false,
                "timestamp": "2024-01-01T12:01:00Z"
            }
        ]
    }
}
```

### 9. Send Message to AI
- **URL**: `https://gemini-back-clone.onrender.com/chatroom/{chatroom_id}/message/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <access_token>`
- **Description**: Send a message to AI and get response
- **Request Body**:
```json
{
    "content": "Tell me a joke about programming"
}
```
- **Response**:
```json
{
    "success": true,
    "message": "Message sent successfully",
    "data": {
        "user_message": {
            "id": 3,
            "content": "Tell me a joke about programming",
            "is_ai": false,
            "timestamp": "2024-01-01T12:02:00Z"
        },
        "ai_response": {
            "id": 4,
            "content": "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
            "is_ai": true,
            "timestamp": "2024-01-01T12:02:05Z"
        }
    }
}
```

---

## 💳 Subscription Endpoints

### 10. Subscribe to Pro
- **URL**: `https://gemini-back-clone.onrender.com/subscriptions/pro/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <access_token>`
- **Description**: Create a Stripe checkout session for pro subscription
- **Request Body**:
```json
{
    "price_id": "price_1234567890"
}
```
- **Response**:
```json
{
    "success": true,
    "data": {
        "checkout_url": "https://checkout.stripe.com/pay/cs_test_...",
        "session_id": "cs_test_..."
    }
}
```

### 11. Subscription Status
- **URL**: `https://gemini-back-clone.onrender.com/subscriptions/status/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <access_token>`
- **Description**: Get current user's subscription status
- **Response**:
```json
{
    "success": true,
    "data": {
        "is_pro": true,
        "subscription_id": "sub_1234567890",
        "current_period_end": "2024-02-01T00:00:00Z",
        "status": "active"
    }
}
```

### 12. Stripe Webhook
- **URL**: `https://gemini-back-clone.onrender.com/subscriptions/webhook/stripe/`
- **Method**: `POST`
- **Description**: Handle Stripe webhook events (for internal use)
- **Request Body**: Stripe webhook payload
- **Response**:
```json
{
    "success": true,
    "message": "Webhook processed successfully"
}
```

---

## 🔄 Token Management

### 13. Refresh Token
- **URL**: `https://gemini-back-clone.onrender.com/auth/token/refresh/`
- **Method**: `POST`
- **Description**: Get new access token using refresh token
- **Request Body**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
- **Response**:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 📋 Complete API Collection

### Authentication Flow
1. **Register**: `POST /auth/signup/`
2. **Send OTP**: `POST /auth/send-otp/`
3. **Verify OTP**: `POST /auth/verify-otp/`
4. **Get Profile**: `GET /auth/me/`

### Chat Flow
1. **List Chatrooms**: `GET /chatroom/`
2. **Get Chatroom**: `GET /chatroom/{id}/`
3. **Send Message**: `POST /chatroom/{id}/message/`

### Subscription Flow
1. **Subscribe**: `POST /subscriptions/pro/`
2. **Check Status**: `GET /subscriptions/status/`

---

## 🚀 Quick Testing with cURL

### Authentication
```bash
# 1. Register
curl -X POST https://gemini-back-clone.onrender.com/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"mobile": "1234567890", "password": "testpass123"}'

# 2. Send OTP
curl -X POST https://gemini-back-clone.onrender.com/auth/send-otp/ \
  -H "Content-Type: application/json" \
  -d '{"mobile": "1234567890", "purpose": "login"}'

# 3. Verify OTP
curl -X POST https://gemini-back-clone.onrender.com/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"mobile": "1234567890", "code": "123456", "purpose": "login"}'
```

### Chat
```bash
# 4. Get chatrooms
curl -X GET https://gemini-back-clone.onrender.com/chatroom/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 5. Send message to AI
curl -X POST https://gemini-back-clone.onrender.com/chatroom/1/message/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"content": "Hello AI! Tell me a joke."}'
```

### Subscription
```bash
# 6. Subscribe to Pro
curl -X POST https://gemini-back-clone.onrender.com/subscriptions/pro/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"price_id": "price_1234567890"}'

# 7. Check subscription status
curl -X GET https://gemini-back-clone.onrender.com/subscriptions/status/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📝 Error Responses

### Common Error Format
```json
{
    "success": false,
    "error": "Error message",
    "code": "ERROR_CODE"
}
```

### Common Error Codes
- `INVALID_CREDENTIALS`: Wrong mobile/password
- `INVALID_OTP`: Wrong OTP code
- `MOBILE_NOT_VERIFIED`: Mobile number not verified
- `INVALID_TOKEN`: Expired or invalid JWT token
- `PERMISSION_DENIED`: User not authorized
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `SUBSCRIPTION_REQUIRED`: Pro subscription needed

---

## 🔧 Environment Variables

For local development, create a `.env` file:

```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# AI Integration
GEMINI_API_KEY=your-gemini-api-key

# Payments (Optional)
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# CORS
CORS_ALLOW_ALL_ORIGINS=True
```

---

**🎯 All endpoints are production-ready and deployed at `https://gemini-back-clone.onrender.com`** 