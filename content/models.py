from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Chat(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название чата'
    )
    participants = models.ManyToManyField(
        User,
        related_name='chats'
    )

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
    )
    text = models.TextField(
        verbose_name='Сообщение'
    )
    created_at = models.DateTimeField(
        verbose_name='Время отправки',
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.sender} {self.text}'

    class Meta:
        ordering = ('created_at',)


