"""
Модель категории услуг.
"""

from django.db import models
from django.utils.text import slugify
from apps.core.models import BaseModel


class ServiceCategory(BaseModel):
    """
    Категория услуг для фильтрации в каталоге.
    
    Поля:
        name: Название категории
        slug: URL-идентификатор
        order: Порядок отображения
        is_active: Активность
    """
    
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории',
        help_text='Название для фильтра'
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL-идентификатор',
        help_text='Автоматически генерируется из названия',
        blank=True
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
        help_text='Порядок отображения в фильтрах'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Отображать категорию на сайте'
    )
    
    class Meta:
        verbose_name = 'Категория услуг'
        verbose_name_plural = 'Категории услуг'
        ordering = ['order', 'name']
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        """Автоматическая генерация slug."""
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name, allow_unicode=False)
        super().save(*args, **kwargs)

