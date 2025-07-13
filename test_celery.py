import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gemini_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from chatrooms.models import Chatroom, Message
from chatrooms.tasks import process_gemini_message

User = get_user_model()

def test_celery_async_processing():
    print("🧪 Testing Celery Async Gemini Processing...")
    
    # Create a test user if not exists
    user, created = User.objects.get_or_create(
        mobile='1234567890',
        defaults={'password': 'testpass123'}
    )
    
    # Create a test chatroom
    chatroom, created = Chatroom.objects.get_or_create(
        user=user,
        defaults={'name': 'Test Chatroom'}
    )
    
    # Create a test message
    message = Message.objects.create(
        chatroom=chatroom,
        user=user,
        content="Hello, can you tell me about Python programming?"
    )
    
    print(f"📝 Created test message: {message.content}")
    print(f"🆔 Message ID: {message.id}")
    
    # Test Celery task
    print("🚀 Triggering Celery task...")
    task = process_gemini_message.delay(message.id)
    
    print(f"📋 Task ID: {task.id}")
    print(f"📊 Task Status: {task.status}")
    
    # Wait for task completion
    print("⏳ Waiting for task completion...")
    result = task.get(timeout=60)
    
    print(f"✅ Task completed!")
    print(f"📊 Final Status: {task.status}")
    
    # Check if AI response was saved
    message.refresh_from_db()
    if message.ai_response:
        print(f"🤖 AI Response: {message.ai_response[:100]}...")
    else:
        print("❌ No AI response received")
    
    return message

if __name__ == "__main__":
    test_celery_async_processing() 