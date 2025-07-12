#!/usr/bin/env python3
"""
Quick Deployment Test Script
Tests if your deployed app is working
"""

import requests
import json

# Your deployed app URL
APP_URL = "https://gemini-back-clone.onrender.com"

def test_deployment():
    """Test the deployed application"""
    print("🧪 Testing Deployed Gemini Backend Clone")
    print("=" * 50)
    
    # Test 1: Check if app is running
    print("\n1️⃣ Testing if app is running...")
    try:
        response = requests.get(f"{APP_URL}/admin/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ App is running! (Django admin page loaded)")
        elif response.status_code == 404:
            print("✅ App is running! (404 expected for admin without setup)")
        else:
            print(f"⚠️  App responded with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error connecting to app: {e}")
        return
    
    # Test 2: Test authentication endpoint
    print("\n2️⃣ Testing authentication endpoint...")
    try:
        test_data = {
            "mobile": "1234567890",
            "purpose": "login"
        }
        response = requests.post(f"{APP_URL}/auth/send-otp/", json=test_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Authentication endpoint working!")
            print(f"Response: {response.json()}")
        else:
            print(f"⚠️  Authentication endpoint returned: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing auth: {e}")
    
    # Test 3: Test chatroom endpoint
    print("\n3️⃣ Testing chatroom endpoint...")
    try:
        response = requests.get(f"{APP_URL}/chatroom/")
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 401, 403]:
            print("✅ Chatroom endpoint responding!")
        else:
            print(f"⚠️  Chatroom endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing chatroom: {e}")
    
    print("\n🎉 Deployment test completed!")
    print("If you see ✅ marks, your app is working correctly!")

if __name__ == "__main__":
    test_deployment() 