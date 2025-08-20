from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from django.db.models.query import Prefetch

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return (
            Chat.objects
            .filter(participants=self.request.user)
            .prefetch_related(
                Prefetch(
                    "messages",
                    queryset=Message.objects.order_by("-created_at")[:1],
                    to_attr="prefetched_last_message"
                )
            )
        )


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        chat = get_object_or_404(Chat, id=self.kwargs['chat_id'], participants=self.request.user)
        last_id = self.request.query_params.get('last_id')
        qs = chat.messages.order_by("created_at")
        if last_id:
            qs = qs.filter(id__gt=last_id)
        return qs


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chat = get_object_or_404(Chat, id=self.kwargs['chat_id'], participants=self.request.user)
        serializer.save(chat=chat, sender=self.request.user)
