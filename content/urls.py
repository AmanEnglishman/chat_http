from django.urls import path

from .views import MessageCreateView, ChatListView, MessageListView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-list'),
    path('<int:chat_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('<int:chat_id>/messages/send', MessageCreateView.as_view(), name='message-create'),
]