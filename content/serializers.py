from rest_framework import serializers
from django.db.models import Prefetch

from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'text', 'created_at')

    def get_sender(self, obj):
        return {
            "id": obj.sender.id,
            "username": obj.sender.username
        }

class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('id', 'name', 'chat_type', 'last_message')

    def get_last_message(self, obj):
        message = getattr(obj, "prefetched_last_message", None)
        if message:
            return MessageSerializer(message).data
        return None