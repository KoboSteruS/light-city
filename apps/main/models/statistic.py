"""
Модель статистики для главной страницы.
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import BaseModel


class Statistic(BaseModel):
    """
    Статистика компании для отображения на главной странице.
    
    Поля:
        icon_class: CSS класс иконки (Bootstrap Icons)
        number: Числовое значение
        suffix: Суффикс после числа (например, "+", "%")
        label: Текст под числом
        order: Порядок отображения
        is_active: Активность
    """
    
    icon_class = models.CharField(
        max_length=100,
        verbose_name='Класс иконки',
        help_text='CSS класс иконки из Bootstrap Icons (например: bi-check-circle-fill)',
        default='bi-check-circle-fill'
    )
    
    number = models.IntegerField(
        verbose_name='Число',
        help_text='Числовое значение статистики',
        validators=[MinValueValidator(0)]
    )
    
    suffix = models.CharField(
        max_length=10,
        verbose_name='Суффикс',
        help_text='Текст после числа (например: "+", "%", "м²")',
        blank=True,
        default=''
    )
    
    label = models.CharField(
        max_length=200,
        verbose_name='Подпись',
        help_text='Текст под числом (например: "Проектов реализовано")'
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
        help_text='Порядок отображения (меньше = выше)'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Отображать статистику на сайте'
    )
    
    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
        ordering = ['order', 'created_at']
    
    def __str__(self) -> str:
        return f"{self.number}{self.suffix} - {self.label}"
