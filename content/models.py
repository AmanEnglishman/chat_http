from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Chat(models.Model):
    CHAT_TYPES = (
        ('private', 'Private'),
        ('group', 'Group'),
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название чата'
    )
    participants = models.ManyToManyField(
        User,
        related_name='chats'
    )
    chat_type = models.CharField(choices=CHAT_TYPES, default='private', max_length=10)

    def __str__(self):
        return self.name or f'Chat {self.id}'

class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True
    )
    text = models.TextField(
        verbose_name='Сообщение'
    )
    created_at = models.DateTimeField(
        verbose_name='Время отправки',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f'{self.sender} {self.text}'

    class Meta:
        ordering = ('created_at',)


class ChatParticipant(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('chat', 'user')
