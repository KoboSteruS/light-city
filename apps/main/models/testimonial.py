"""
Модель отзыва клиента.
"""

from django.db import models
from apps.core.models import BaseModel


class Testimonial(BaseModel):
    """
    Отзыв клиента.
    
    Поля:
        name: Имя клиента
        position: Должность/компания
        avatar: Фото клиента
        rating: Рейтинг (1-5)
        text: Текст отзыва
        order: Порядок отображения
        is_active: Активность
    """
    
    name = models.CharField(
        max_length=100,
        verbose_name='Имя клиента',
        help_text='ФИО клиента'
    )
    
    position = models.CharField(
        max_length=200,
        verbose_name='Должность',
        help_text='Должность и компания',
        blank=True
    )
    
    avatar = models.ImageField(
        upload_to='testimonials/%Y/%m/',
        verbose_name='Фото',
        help_text='Фото клиента',
        blank=True,
        null=True
    )
    
    rating = models.PositiveSmallIntegerField(
        default=5,
        verbose_name='Рейтинг',
        help_text='Оценка от 1 до 5',
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Содержание отзыва'
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
        help_text='Порядок отображения'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Отображать на сайте'
    )
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['order', '-created_at']
    
    def __str__(self) -> str:
        return f'{self.name} ({self.rating}★)'



