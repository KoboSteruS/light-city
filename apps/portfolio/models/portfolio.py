"""
Модель работы в портфолио.
"""

from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from apps.core.models import BaseModel


def validate_image_size(image):
    """
    Валидатор размера изображения.
    Максимальный размер: 25 MB
    """
    max_size_mb = 25
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Размер файла не должен превышать {max_size_mb} MB. Текущий размер: {image.size / (1024 * 1024):.1f} MB')


def validate_image_extension(image):
    """
    Валидатор расширения изображения.
    Разрешены: jpg, jpeg, png, webp
    """
    import os
    ext = os.path.splitext(image.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        raise ValidationError(f'Недопустимый формат файла. Разрешены: {", ".join(valid_extensions)}')


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
        help_text='Главное изображение работы (рекомендуется 800x600px, максимум 25 MB, форматы: jpg, png, webp)',
        validators=[validate_image_size, validate_image_extension]
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
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
        help_text='Чем меньше число, тем выше в списке. Можно менять в списке работ в админке.'
    )
    
    is_featured = models.BooleanField(
        default=False,
        verbose_name='На главной',
        help_text='Показывать в блоке из 4 работ на главной странице (в своей категории). Сначала выводятся работы с этой галочкой.'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Отображать работу на сайте'
    )
    
    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Портфолио'
        ordering = ['order', '-date_completed', '-created_at']
    
    def __str__(self) -> str:
        return self.title

