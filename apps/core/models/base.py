"""
Базовая модель проекта.
"""

import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Абстрактная базовая модель для всех моделей проекта.
    
    Поля:
        uuid: Уникальный идентификатор (UUID4)
        created_at: Дата и время создания
        updated_at: Дата и время последнего обновления
    """
    
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID',
        help_text='Уникальный идентификатор записи'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Автоматически устанавливается при создании'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
        help_text='Автоматически обновляется при изменении'
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        """Строковое представление модели."""
        return f"{self.__class__.__name__} ({self.uuid})"
