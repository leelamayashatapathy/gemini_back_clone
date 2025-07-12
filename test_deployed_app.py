#!/usr/bin/env python3
"""
Test Deployed App Script
Replace YOUR_APP_URL with your actual Render URL
"""

import requests
import json
import time

# Replace with your actual Render URL
APP_URL = "https://your-app-name.onrender.com"

def test_deployed_app():
    """Test the deployed application"""
    print("🧪 Testing Deployed Gemini Backend Clone")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{APP_URL}/")
        print(f"Status: {response.status_code}")
        if response.status_code == 404:
            print("✅ App is running (404 expected for root URL)")
        else:
            print(f"Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Send OTP
    print("\n2️⃣ Testing Authentication...")
    try:
        otp_data = {
            "mobile": "1234567890",
            "purpose": "login"
        }
        response = requests.post(f"{APP_URL}/auth/send-otp/", json=otp_data)
        print(f"Send OTP Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ OTP sent successfully")
            otp_response = response.json()
            print(f"Response: {otp_response}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Verify OTP (if we got one)
    print("\n3️⃣ Testing OTP Verification...")
    try:
        verify_data = {
            "mobile": "1234567890",
            "code": "123456",  # Use the OTP from previous response
            "purpose": "login"
        }
        response = requests.post(f"{APP_URL}/auth/verify-otp/", json=verify_data)
        print(f"Verify OTP Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ OTP verified successfully")
            auth_response = response.json()
            print(f"Access Token: {auth_response.get('access', '')[:20]}...")
            return auth_response.get('access', '')
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def test_with_auth(token):
    """Test authenticated endpoints"""
    if not token:
        print("❌ No token available for authenticated tests")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 4: Create Chatroom
    print("\n4️⃣ Testing Chatroom Creation...")
    try:
        chatroom_data = {"name": "Test Chatroom"}
        response = requests.post(f"{APP_URL}/chatroom/create/", json=chatroom_data, headers=headers)
        print(f"Create Chatroom Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ Chatroom created successfully")
            chatroom_response = response.json()
            chatroom_id = chatroom_response.get('id')
            print(f"Chatroom ID: {chatroom_id}")
            return chatroom_id
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def test_payment_flow(token):
    """Test payment flow"""
    if not token:
        print("❌ No token available for payment tests")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 5: Create Checkout Session
    print("\n5️⃣ Testing Payment Flow...")
    try:
        payment_data = {"price_id": "price_test"}
        response = requests.post(f"{APP_URL}/subscriptions/create-checkout/", json=payment_data, headers=headers)
        print(f"Create Checkout Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Checkout session created")
            checkout_response = response.json()
            print(f"Checkout URL: {checkout_response.get('url', '')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all tests"""
    print(f"Testing app at: {APP_URL}")
    print("Make sure to replace YOUR_APP_URL with your actual Render URL")
    print("=" * 60)
    
    # Test basic functionality
    token = test_deployed_app()
    
    if token:
        # Test authenticated endpoints
        chatroom_id = test_with_auth(token)
        
        # Test payment flow
        test_payment_flow(token)
    
    print("\n" + "=" * 60)
    print("🎉 Deployment Test Complete!")
    print("If all tests passed, your app is successfully deployed!")
    print("\n📋 Next Steps:")
    print("1. Set up Stripe webhooks")
    print("2. Test payment flow with real Stripe test cards")
    print("3. Monitor app performance in Render dashboard")

if __name__ == "__main__":
    main() 