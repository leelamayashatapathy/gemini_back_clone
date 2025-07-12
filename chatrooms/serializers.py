from rest_framework import serializers
from .models import Chatroom, Message

class ChatroomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ['id', 'name']

class ChatroomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'created_at']

class ChatroomDetailSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'created_at', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.order_by('created_at')
        return MessageSerializer(messages, many=True).data

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'ai_response', 'created_at'] 