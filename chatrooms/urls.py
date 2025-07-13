from django.urls import path
from .views import ChatroomListView, ChatroomDetailView, MessageCreateView

urlpatterns = [
    path('', ChatroomListView.as_view(), name='chatroom-list'),
    path('<int:pk>/', ChatroomDetailView.as_view(), name='chatroom-detail'),
    path('<int:pk>/message/', MessageCreateView.as_view(), name='chatroom-message'),
] 