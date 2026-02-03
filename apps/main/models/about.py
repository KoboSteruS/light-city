"""
Модель информации "О нас".
"""

from django.db import models
from ckeditor.fields import RichTextField
from apps.core.models import BaseModel


class AboutUs(BaseModel):
    """
    Модель блока 'О нас' на главной странице.
    
    Поля:
        title: Заголовок секции
        description: Описание компании
        image: Фото команды
        is_active: Активность блока
    """
    
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Основной заголовок (например: Яркий город)',
        default='О нас'
    )
    
    subtitle = models.CharField(
        max_length=300,
        verbose_name='Подзаголовок',
        help_text='Подзаголовок под основным заголовком (например: Делаем ваш бизнес заметным в Петрозаводске)',
        blank=True,
        null=True
    )
    
    description = RichTextField(
        verbose_name='Описание',
        help_text='Текст о компании',
        config_name='default'
    )
    
    image = models.ImageField(
        upload_to='about/%Y/%m/',
        verbose_name='Фото команды',
        help_text='Рекомендуемый размер: 800x600px'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Отображать блок на сайте'
    )
    
    subtitle_margin_bottom = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.0,
        verbose_name='Отступ под подзаголовком (rem)',
        help_text='Расстояние между подзаголовком и текстом (в rem, например: 0.5, 1.0, 1.5). Используйте точку (.) в качестве разделителя.'
    )
    
    paragraph_margin_bottom = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.75,
        verbose_name='Отступ между абзацами (rem)',
        help_text='Расстояние между абзацами текста (в rem, например: 0.5, 0.75, 1.0). Используйте точку (.) в качестве разделителя.'
    )
    
    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        """Переопределяем save для singleton паттерна."""
        if not self.uuid:
            # Деактивируем все остальные записи
            AboutUs.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

