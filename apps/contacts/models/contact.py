"""
Модель контактного сообщения.
"""

from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import BaseModel


class ContactMessage(BaseModel):
    """
    Сообщение из формы обратной связи.
    
    Поля:
        name: Имя отправителя
        phone: Телефон
        email: Email (опционально)
        message: Текст сообщения
        status: Статус обработки
        is_read: Прочитано ли
    """
    
    class Status(models.TextChoices):
        """Статусы обработки обращения."""
        NEW = 'new', 'Новое'
        IN_PROGRESS = 'in_progress', 'В обработке'
        COMPLETED = 'completed', 'Завершено'
        CANCELLED = 'cancelled', 'Отменено'
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Телефон должен быть в формате: '+999999999'. До 15 цифр."
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name='Имя',
        help_text='Имя отправителя'
    )
    
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name='Телефон',
        help_text='Контактный телефон'
    )
    
    email = models.EmailField(
        verbose_name='Email',
        blank=True,
        help_text='Email для связи (опционально)'
    )
    
    message = models.TextField(
        verbose_name='Сообщение',
        help_text='Текст обращения'
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name='Статус',
        help_text='Статус обработки'
    )
    
    is_read = models.BooleanField(
        default=False,
        verbose_name='Прочитано',
        help_text='Отметка о прочтении'
    )
    
    admin_notes = models.TextField(
        verbose_name='Заметки администратора',
        blank=True,
        help_text='Внутренние заметки'
    )
    
    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['is_read', '-created_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.name} - {self.phone} ({self.get_status_display()})"
    
    def mark_as_read(self) -> None:
        """Отметить обращение как прочитанное."""
        self.is_read = True
        self.save(update_fields=['is_read', 'updated_at'])


