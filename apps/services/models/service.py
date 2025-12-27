"""
Модель услуги.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
from apps.core.models import BaseModel


class Service(BaseModel):
    """
    Модель услуги рекламного агентства.
    
    Поля:
        name: Название услуги
        category: Категория услуги
        icon: Иконка услуги (svg или изображение)
        image: Главное изображение для каталога
        description: Описание услуги
        price_from: Цена от
        price_unit: Единица измерения цены
        order: Порядок отображения
        is_active: Активность
    """
    
    name = models.CharField(
        max_length=100,
        verbose_name='Название услуги',
        help_text='Краткое название'
    )
    
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='URL-идентификатор',
        help_text='Автоматически генерируется из названия',
        null=True,
        blank=True
    )
    
    category = models.ForeignKey(
        'ServiceCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='services',
        verbose_name='Категория',
        help_text='Категория для фильтрации'
    )
    
    icon = models.ImageField(
        upload_to='services/icons/%Y/%m/',
        verbose_name='Иконка',
        help_text='Иконка услуги для главной страницы',
        blank=True,
        null=True
    )
    
    image = models.ImageField(
        upload_to='services/images/%Y/%m/',
        verbose_name='Изображение',
        help_text='Главное изображение для каталога',
        blank=True,
        null=True
    )
    
    description = RichTextField(
        verbose_name='Описание',
        help_text='Подробное описание услуги',
        config_name='default'
    )
    
    price_from = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена от',
        help_text='Начальная цена услуги',
        null=True,
        blank=True
    )
    
    price_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
        help_text='Например: ₽, ₽/м², ₽/шт',
        default='₽',
        blank=True
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
        help_text='Порядок отображения',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Отображать услугу на сайте'
    )
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order', 'name']
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        """Автоматическая генерация slug."""
        if not self.slug:
            from slugify import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Получение URL услуги."""
        from django.urls import reverse
        return reverse('services:detail', kwargs={'slug': self.slug})

