from rest_framework import serializers

from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender_name', 'sender', 'text', 'created_at')


class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('id', 'name', 'last_message')

    def get_last_message(self, obj):
        message = obj.messages  .last()
        if message:
            return MessageSerializer(message).data
        return None
