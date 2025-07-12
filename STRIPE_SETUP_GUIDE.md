# Stripe Payment Setup Guide

This guide will help you set up Stripe payments for your Gemini Backend Clone assignment.

## 🚀 Quick Setup Steps

### 1. Create Stripe Account
1. Go to [https://stripe.com](https://stripe.com)
2. Click "Start now" and sign up
3. Choose "Individual" account type
4. Complete registration with your details

### 2. Get Your Test Keys
1. Login to Stripe Dashboard
2. Make sure you're in **Test Mode** (toggle in top-right)
3. Go to **Developers** → **API keys**
4. Copy your keys:
   - **Publishable key**: `pk_test_...`
   - **Secret key**: `sk_test_...`

### 3. Set Up Webhook
1. Go to **Developers** → **Webhooks**
2. Click **Add endpoint**
3. Set URL: `http://localhost:8000/subscriptions/webhook/`
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.deleted`
5. Click **Add endpoint**
6. Copy the **Signing secret**: `whsec_...`

### 4. Configure Environment Variables
1. Create `.env` file in your project root
2. Add your Stripe keys:

```env
# Stripe Test Keys
STRIPE_PUBLISHABLE_KEY=pk_test_your_actual_key_here
STRIPE_SECRET_KEY=sk_test_your_actual_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Other settings
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here
```

### 5. Test the Payment Flow

#### Option A: Using the Test Script
```bash
python test_stripe_payment.py
```

#### Option B: Manual Testing
1. Start your Django server: `python manage.py runserver`
2. Authenticate via `/auth/send-otp/` and `/auth/verify-otp/`
3. Create subscription via `/subscriptions/subscribe-pro/`
4. Open the checkout URL in browser
5. Use test card: `4242 4242 4242 4242`

## 🧪 Test Cards for Stripe

| Card Number | Description |
|-------------|-------------|
| 4242 4242 4242 4242 | Successful payment |
| 4000 0000 0000 0002 | Declined payment |
| 4000 0025 0000 3155 | Requires authentication |

## 📋 What to Show for Assignment

### 1. Stripe Dashboard Screenshots
- Test mode enabled
- Successful payment in Events/Logs
- Webhook endpoint configured

### 2. Your Code Evidence
- `.env` file with test keys (not real ones)
- API responses showing checkout URL
- Subscription status updates

### 3. Test Results
- Payment completion in Stripe
- User subscription upgraded in your app
- Webhook processing logs

## 🔧 Troubleshooting

### Common Issues:

1. **"Invalid API key" error**
   - Make sure you're using test keys (`pk_test_`, `sk_test_`)
   - Check your `.env` file is loaded

2. **Webhook not receiving events**
   - Use Stripe CLI: `stripe listen --forward-to localhost:8000/subscriptions/webhook/`
   - Or deploy to a public URL

3. **Payment fails**
   - Use the correct test card numbers
   - Check your Stripe account is in test mode

## 📝 Assignment Checklist

- [ ] Stripe account created
- [ ] Test keys obtained
- [ ] Webhook configured
- [ ] Environment variables set
- [ ] Payment flow tested
- [ ] Screenshots captured
- [ ] Code documented

## 🎯 Key Points for Assignment

1. **Always use test keys** - never real keys
2. **Show the complete flow** - auth → payment → subscription
3. **Demonstrate webhook processing** - show subscription status change
4. **Include error handling** - show what happens with failed payments
5. **Document the process** - explain how it works

## 🔗 Useful Links

- [Stripe Test Mode](https://stripe.com/docs/testing)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [Webhook Testing](https://stripe.com/docs/webhooks/test)
- [Test Cards](https://stripe.com/docs/testing#cards)

---

**Remember**: This is for demonstration purposes only. Use test keys and test cards only! 