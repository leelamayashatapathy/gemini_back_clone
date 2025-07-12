from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from django.conf import settings
from .models import Chatroom, Message
from .serializers import ChatroomCreateSerializer, ChatroomListSerializer, ChatroomDetailSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .tasks import process_gemini_message
from core.services.gemini import get_gemini_response

CACHE_TTL = 300  # 5 minutes

class ChatroomCreateView(generics.CreateAPIView):
    serializer_class = ChatroomCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChatroomListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cache_key = f"chatrooms_user_{request.user.id}"
        data = cache.get(cache_key)
        if not data:
            chatrooms = Chatroom.objects.filter(user=request.user).order_by('-created_at')
            data = ChatroomListSerializer(chatrooms, many=True).data
            cache.set(cache_key, data, timeout=CACHE_TTL)
        return Response(data)

class ChatroomDetailView(generics.RetrieveAPIView):
    serializer_class = ChatroomDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Chatroom.objects.all()

    def get_queryset(self):
        return Chatroom.objects.filter(user=self.request.user)

class MessageCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            chatroom = Chatroom.objects.get(pk=pk, user=request.user)
        except Chatroom.DoesNotExist:
            return Response({'error': 'Chatroom not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = Message.objects.create(
                chatroom=chatroom,
                user=request.user,
                content=serializer.validated_data['content']
            )
            # Trigger Celery task for Gemini API
            process_gemini_message.delay(message.id)
            response_data = MessageSerializer(message).data
            response_data['message'] = 'Message sent. AI response will be processed asynchronously.'
            response_data['ai_processing'] = True
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id, chatroom__user=request.user)
            return Response(MessageSerializer(message).data)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

class SyncMessageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Send message and get immediate AI response (synchronous)"""
        try:
            chatroom = Chatroom.objects.get(pk=pk, user=request.user)
        except Chatroom.DoesNotExist:
            return Response({'error': 'Chatroom not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = Message.objects.create(
                chatroom=chatroom,
                user=request.user,
                content=serializer.validated_data['content']
            )
            
            # Get immediate AI response
            try:
                ai_response = get_gemini_response(message.content)
                message.ai_response = ai_response
                message.save()
                response_data = MessageSerializer(message).data
                response_data['message'] = 'Message sent with immediate AI response.'
                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                message.ai_response = f"Error getting AI response: {str(e)}"
                message.save()
                response_data = MessageSerializer(message).data
                response_data['message'] = 'Message sent but AI response failed.'
                return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
