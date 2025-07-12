# Quick Stripe Setup (Without Webhooks)

If you can't find the webhooks section, let's set up the basic payment flow first.

## 🚀 Quick Setup Steps

### 1. Get Your Test Keys
1. Go to [https://dashboard.stripe.com/test/apikeys](https://dashboard.stripe.com/test/apikeys)
2. Copy your keys:
   - **Publishable key**: `pk_test_...`
   - **Secret key**: `sk_test_...`

### 2. Create .env File
Create a `.env` file in your project root:

```env
# Stripe Test Keys (Replace with your actual keys)
STRIPE_PUBLISHABLE_KEY=pk_test_your_actual_key_here
STRIPE_SECRET_KEY=sk_test_your_actual_key_here
STRIPE_WEBHOOK_SECRET=whsec_test_webhook_secret_here

# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here
```

### 3. Test Basic Payment Flow

#### Option A: Using the Test Script
```bash
python test_stripe_payment.py
```

#### Option B: Manual Testing
1. Start your server: `python manage.py runserver`
2. Send OTP: `POST /auth/send-otp/`
3. Verify OTP: `POST /auth/verify-otp/`
4. Create subscription: `POST /subscriptions/subscribe-pro/`
5. Open the checkout URL in browser
6. Use test card: `4242 4242 4242 4242`

## 🧪 Test Cards
- **Success**: `4242 4242 4242 4242`
- **Decline**: `4000 0000 0000 0002`
- **Requires Auth**: `4000 0025 0000 3155`

## 📋 What to Show for Assignment

### 1. Stripe Dashboard Evidence
- Screenshot of test mode enabled
- Screenshot of successful payment in Events/Logs
- Screenshot of your API keys page

### 2. Your Code Evidence
- `.env` file with test keys
- API responses showing checkout URLs
- Payment completion screenshots

### 3. Test Results
- Payment completion in Stripe dashboard
- Checkout URL generation
- Error handling for failed payments

## 🔧 Troubleshooting

### "Invalid API key" error
- Make sure you're using test keys (`pk_test_`, `sk_test_`)
- Check your `.env` file is in the project root
- Restart your Django server after adding `.env`

### "Webhook not found" error
- This is expected without webhooks
- The payment will still work, but subscription status won't update automatically
- You can manually check subscription status via API

## 🎯 Assignment Checklist

- [ ] Stripe account created
- [ ] Test keys obtained
- [ ] Environment variables set
- [ ] Payment flow tested
- [ ] Screenshots captured
- [ ] Code documented

## 📝 Next Steps

1. **Complete the basic setup above**
2. **Test the payment flow**
3. **Take screenshots for your assignment**
4. **Later, we can add webhooks if needed**

---

**Note**: This setup will work for your assignment demonstration. Webhooks are optional for basic testing. 