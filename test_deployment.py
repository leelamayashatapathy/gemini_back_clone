#!/usr/bin/env python3
"""
Quick Deployment Test Script
Tests if your deployed app is working
"""

import requests
import json

# Base URL for your deployed application
BASE_URL = "https://gemini-backend.onrender.com"

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health/")
        print(f"Health Check Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_database_check():
    """Test the database check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/db-check/")
        print(f"Database Check Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Database check failed: {e}")
        return False

def test_authentication():
    """Test authentication endpoints"""
    try:
        # Test send OTP
        send_otp_data = {
            "mobile": "1234567890",
            "purpose": "login"
        }
        response = requests.post(f"{BASE_URL}/auth/send-otp/", json=send_otp_data)
        print(f"Send OTP Status: {response.status_code}")
        print(f"Send OTP Response: {response.text}")
        
        if response.status_code == 200:
            # Test verify OTP (using the OTP from response)
            response_data = response.json()
            otp = response_data.get('otp', '123456')
            
            verify_otp_data = {
                "mobile": "1234567890",
                "code": otp,
                "purpose": "login"
            }
            response = requests.post(f"{BASE_URL}/auth/verify-otp/", json=verify_otp_data)
            print(f"Verify OTP Status: {response.status_code}")
            print(f"Verify OTP Response: {response.text}")
            
            if response.status_code == 200:
                return response.json().get('access')
        return None
    except Exception as e:
        print(f"Authentication test failed: {e}")
        return None

def test_chatroom_creation(access_token):
    """Test chatroom creation"""
    if not access_token:
        print("No access token available")
        return None
    
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        chatroom_data = {"name": "Test Chatroom"}
        response = requests.post(f"{BASE_URL}/chatroom/create/", json=chatroom_data, headers=headers)
        print(f"Create Chatroom Status: {response.status_code}")
        print(f"Create Chatroom Response: {response.text}")
        
        if response.status_code == 201:
            return response.json().get('id')
        return None
    except Exception as e:
        print(f"Chatroom creation test failed: {e}")
        return None

def main():
    print("🚀 Testing Gemini Backend Deployment")
    print("=" * 50)
    
    # Test health check
    print("\n1. Testing Health Check...")
    health_ok = test_health_check()
    
    # Test database check
    print("\n2. Testing Database Check...")
    db_ok = test_database_check()
    
    # Test authentication
    print("\n3. Testing Authentication...")
    access_token = test_authentication()
    
    # Test chatroom creation if authentication worked
    if access_token:
        print("\n4. Testing Chatroom Creation...")
        chatroom_id = test_chatroom_creation(access_token)
        if chatroom_id:
            print(f"✅ Chatroom created with ID: {chatroom_id}")
    
    print("\n" + "=" * 50)
    print("🎉 Deployment Test Complete!")
    
    if health_ok and db_ok:
        print("✅ Your deployment is working correctly!")
    else:
        print("❌ Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main() 