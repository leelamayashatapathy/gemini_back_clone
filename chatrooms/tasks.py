from celery import shared_task
from .models import Message
from core.services.gemini import get_gemini_response

def get_message_content(message_id):
    try:
        message = Message.objects.get(id=message_id)
        return message.content
    except Message.DoesNotExist:
        return None

@shared_task
def process_gemini_message(message_id):
    content = get_message_content(message_id)
    if content:
        ai_response = get_gemini_response(content)
        Message.objects.filter(id=message_id).update(ai_response=ai_response) 