from rest_framework import generics, permissions

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        last_id = self.request.query_params.get('last_id')
        qs = Message.objects.filter(chat_id=chat_id)
        if last_id:
            qs = qs.filter(id__gt=last_id)
        return qs


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        serializer.save(chat_id=chat_id, sender=self.request.user)
