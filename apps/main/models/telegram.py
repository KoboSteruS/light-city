"""
Модель для хранения Telegram chat_id.
"""

from django.db import models
from apps.core.models import BaseModel


class TelegramChat(BaseModel):
    """
    Хранит chat_id для отправки уведомлений в Telegram.
    
    Поля:
        chat_id: ID чата в Telegram
        username: Имя пользователя (опционально)
        first_name: Имя (опционально)
        is_active: Активен ли чат для получения уведомлений
    """
    
    chat_id = models.BigIntegerField(
        unique=True,
        verbose_name='Chat ID',
        help_text='ID чата в Telegram'
    )
    
    username = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Username',
        help_text='Имя пользователя в Telegram'
    )
    
    first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Имя',
        help_text='Имя пользователя'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Получать уведомления'
    )
    
    class Meta:
        verbose_name = 'Telegram чат'
        verbose_name_plural = 'Telegram чаты'
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        name = self.first_name or self.username or f"Chat {self.chat_id}"
        return f"{name} ({self.chat_id})"
