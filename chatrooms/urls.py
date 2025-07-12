from django.urls import path
from .views import ChatroomCreateView, ChatroomListView, ChatroomDetailView, MessageCreateView, MessageDetailView, SyncMessageView

urlpatterns = [
    path('', ChatroomListView.as_view(), name='chatroom-list'),
    path('create/', ChatroomCreateView.as_view(), name='chatroom-create'),
    path('<int:pk>/', ChatroomDetailView.as_view(), name='chatroom-detail'),
    path('<int:pk>/message/', MessageCreateView.as_view(), name='chatroom-message'),
    path('<int:pk>/sync-message/', SyncMessageView.as_view(), name='chatroom-sync-message'),
    path('message/<int:message_id>/', MessageDetailView.as_view(), name='message-detail'),
] 