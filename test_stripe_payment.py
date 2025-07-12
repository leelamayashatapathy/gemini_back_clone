#!/usr/bin/env python3
"""
Stripe Payment Test Script
This script helps you test the Stripe payment integration step by step.
"""

import requests
import json
import time

# Base URL for your Django server
BASE_URL = "http://localhost:8000"

def test_authentication():
    """Step 1: Test user authentication"""
    print("=== Step 1: Testing Authentication ===")
    
    # Send OTP
    send_otp_data = {
        "mobile": "1234567890",
        "purpose": "login"
    }
    
    response = requests.post(f"{BASE_URL}/auth/send-otp/", json=send_otp_data)
    print(f"Send OTP Response: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        otp_data = response.json()
        otp_code = otp_data.get('otp', '123456')  # Use the OTP from response or default
        
        # Verify OTP
        verify_otp_data = {
            "mobile": "1234567890",
            "code": otp_code,
            "purpose": "login"
        }
        
        response = requests.post(f"{BASE_URL}/auth/verify-otp/", json=verify_otp_data)
        print(f"Verify OTP Response: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            auth_data = response.json()
            return auth_data.get('access')  # Return the access token
        else:
            print("❌ OTP verification failed")
            return None
    else:
        print("❌ OTP sending failed")
        return None

def test_subscription_creation(access_token):
    """Step 2: Test subscription creation"""
    print("\n=== Step 2: Testing Subscription Creation ===")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{BASE_URL}/subscriptions/subscribe-pro/", headers=headers)
    print(f"Subscription Creation Response: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        subscription_data = response.json()
        checkout_url = subscription_data.get('checkout_url')
        print(f"✅ Checkout URL: {checkout_url}")
        print("📝 Open this URL in your browser to complete the payment")
        return checkout_url
    else:
        print("❌ Subscription creation failed")
        return None

def test_subscription_status(access_token):
    """Step 3: Test subscription status"""
    print("\n=== Step 3: Testing Subscription Status ===")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/subscriptions/status/", headers=headers)
    print(f"Subscription Status Response: {response.status_code}")
    print(f"Response: {response.json()}")

def main():
    print("🚀 Stripe Payment Test Script")
    print("=" * 50)
    
    # Step 1: Authentication
    access_token = test_authentication()
    if not access_token:
        print("❌ Authentication failed. Exiting.")
        return
    
    print(f"✅ Authentication successful. Access token: {access_token[:20]}...")
    
    # Step 2: Create subscription
    checkout_url = test_subscription_creation(access_token)
    if not checkout_url:
        print("❌ Subscription creation failed. Exiting.")
        return
    
    # Step 3: Check initial status
    test_subscription_status(access_token)
    
    print("\n" + "=" * 50)
    print("📋 Next Steps:")
    print("1. Open the checkout URL in your browser")
    print("2. Use Stripe test card: 4242 4242 4242 4242")
    print("3. Use any future expiry date (e.g., 12/25)")
    print("4. Use any 3-digit CVC (e.g., 123)")
    print("5. Complete the payment")
    print("6. Run this script again to check updated status")
    print("=" * 50)

if __name__ == "__main__":
    main() 