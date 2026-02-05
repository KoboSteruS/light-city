"""
Модель работы в портфолио.
"""

from django.db import models
from ckeditor.fields import RichTextField
from apps.core.models import BaseModel


class PortfolioItem(BaseModel):
    """
    Работа в портфолио.
    
    Поля:
        title: Название работы
        description: Описание
        image: Главное изображение
        client: Клиент
        date_completed: Дата завершения
        is_featured: Показывать на главной
        is_active: Активность
    """
    
    title = models.CharField(
        max_length=200,
        verbose_name='Название работы',
        help_text='Название проекта'
    )
    
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='portfolio_works',
        verbose_name='Услуга',
        help_text='Связанная услуга'
    )
    
    description = RichTextField(
        verbose_name='Описание',
        help_text='Подробное описание проекта',
        config_name='default'
    )
    
    image = models.ImageField(
        upload_to='portfolio/%Y/%m/',
        verbose_name='Изображение',
        help_text='Главное изображение работы (рекомендуется 800x600px)'
    )
    
    client = models.CharField(
        max_length=200,
        verbose_name='Клиент',
        blank=True,
        help_text='Название клиента'
    )
    
    date_completed = models.DateField(
        verbose_name='Дата завершения',
        null=True,
        blank=True,
        help_text='Когда был завершен проект'
    )
    
    is_featured = models.BooleanField(
        default=False,
        verbose_name='На главной',
        help_text='Показывать на главной странице'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Отображать работу на сайте'
    )
    
    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Портфолио'
        ordering = ['-date_completed', '-created_at']
    
    def __str__(self) -> str:
        return self.title

