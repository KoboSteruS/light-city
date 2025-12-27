"""
Модель слайдера для главной страницы.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import BaseModel


class Slider(BaseModel):
    """
    Модель слайдера на главной странице.
    
    Поля:
        title: Заголовок слайда
        subtitle: Подзаголовок
        image: Изображение для слайда
        button_text: Текст кнопки
        button_link: Ссылка кнопки
        order: Порядок отображения
        is_active: Активность слайда
    """
    
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Основной заголовок слайда'
    )
    
    subtitle = models.CharField(
        max_length=300,
        verbose_name='Подзаголовок',
        help_text='Описание под заголовком',
        blank=True
    )
    
    image = models.ImageField(
        upload_to='slider/%Y/%m/',
        verbose_name='Изображение',
        help_text='Рекомендуемый размер: 1920x800px'
    )
    
    button_text = models.CharField(
        max_length=50,
        verbose_name='Текст кнопки',
        default='Наши услуги',
        blank=True
    )
    
    button_link = models.CharField(
        max_length=200,
        verbose_name='Ссылка кнопки',
        default='#services',
        blank=True
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
        help_text='Порядок отображения слайда',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Отображать слайд на сайте'
    )
    
    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайдер'
        ordering = ['order', '-created_at']
    
    def __str__(self) -> str:
        return self.title

