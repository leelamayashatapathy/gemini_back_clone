#!/usr/bin/env python3
"""
Payment Demo Script - No Webhooks Required
Perfect for assignment demonstration
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def demo_payment_flow():
    """Demonstrate the complete payment flow"""
    print("🚀 Stripe Payment Demo (No Webhooks Required)")
    print("=" * 60)
    
    # Step 1: Authentication
    print("\n📱 Step 1: User Authentication")
    print("-" * 40)
    
    # Send OTP
    send_otp_data = {
        "mobile": "1234567890",
        "purpose": "login"
    }
    
    response = requests.post(f"{BASE_URL}/auth/send-otp/", json=send_otp_data)
    print(f"Send OTP: {response.status_code} - {response.json()}")
    
    if response.status_code == 200:
        otp_data = response.json()
        otp_code = otp_data.get('otp', '123456')
        
        # Verify OTP
        verify_otp_data = {
            "mobile": "1234567890",
            "code": otp_code,
            "purpose": "login"
        }
        
        response = requests.post(f"{BASE_URL}/auth/verify-otp/", json=verify_otp_data)
        print(f"Verify OTP: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            auth_data = response.json()
            access_token = auth_data.get('access')
            print(f"✅ Authentication successful!")
            
            # Step 2: Create Subscription
            print("\n💳 Step 2: Create Subscription")
            print("-" * 40)
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(f"{BASE_URL}/subscriptions/subscribe-pro/", headers=headers)
            print(f"Create Subscription: {response.status_code}")
            
            if response.status_code == 200:
                subscription_data = response.json()
                checkout_url = subscription_data.get('checkout_url')
                print(f"✅ Checkout URL generated: {checkout_url}")
                
                # Step 3: Check Initial Status
                print("\n📊 Step 3: Check Subscription Status")
                print("-" * 40)
                
                response = requests.get(f"{BASE_URL}/subscriptions/status/", headers=headers)
                print(f"Status Check: {response.status_code} - {response.json()}")
                
                # Step 4: Instructions
                print("\n" + "=" * 60)
                print("📋 Assignment Demonstration Steps:")
                print("=" * 60)
                print("1. ✅ Authentication: User login with OTP")
                print("2. ✅ Subscription Creation: Stripe checkout URL generated")
                print("3. 📝 Payment: Open the checkout URL in browser")
                print("4. 📝 Use test card: 4242 4242 4242 4242")
                print("5. 📝 Complete payment in Stripe")
                print("6. 📸 Screenshot: Payment in Stripe dashboard")
                print("7. 📸 Screenshot: Your API responses")
                print("8. 📸 Screenshot: Your .env file (with test keys)")
                print("\n🎯 This demonstrates:")
                print("   - OTP-based authentication")
                print("   - Stripe integration")
                print("   - Payment processing")
                print("   - API responses")
                print("   - Error handling")
                print("\n💡 Note: Webhooks would automatically update subscription status")
                print("   For demo, you can manually check status via API")
                print("=" * 60)
                
            else:
                print(f"❌ Subscription creation failed: {response.json()}")
        else:
            print(f"❌ OTP verification failed: {response.json()}")
    else:
        print(f"❌ OTP sending failed: {response.json()}")

if __name__ == "__main__":
    demo_payment_flow() 