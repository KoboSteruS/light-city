"""
Модель настроек сайта.
"""

from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import BaseModel


class SiteSettings(BaseModel):
    """
    Глобальные настройки сайта.
    
    Поля:
        site_name: Название сайта
        phone: Телефон
        email: Email
        address: Адрес
        working_hours: Часы работы
        vk_link: Ссылка на VK
        instagram_link: Ссылка на Instagram
        telegram_link: Ссылка на Telegram
        is_active: Активность настроек
    """
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Телефон должен быть в формате: '+999999999'. До 15 цифр."
    )
    
    site_name = models.CharField(
        max_length=100,
        verbose_name='Название сайта',
        default='Яркий Город'
    )
    
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name='Телефон',
        help_text='Формат: +7(999)999-99-99'
    )
    
    email = models.EmailField(
        verbose_name='Email',
        help_text='Контактный email'
    )
    
    address = models.CharField(
        max_length=300,
        verbose_name='Адрес',
        help_text='Физический адрес офиса'
    )
    
    working_hours = models.CharField(
        max_length=100,
        verbose_name='Часы работы',
        default='Мы открыты с 10:00 до 19:00'
    )
    
    vk_link = models.URLField(
        verbose_name='VK',
        blank=True,
        help_text='Ссылка на VK'
    )
    
    instagram_link = models.URLField(
        verbose_name='Instagram',
        blank=True,
        help_text='Ссылка на Instagram'
    )
    
    telegram_link = models.URLField(
        verbose_name='Telegram',
        blank=True,
        help_text='Ссылка на Telegram'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Использовать эти настройки'
    )
    
    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"{self.site_name} - Настройки"
    
    def save(self, *args, **kwargs):
        """Singleton паттерн - только одна активная запись."""
        if self.is_active:
            SiteSettings.objects.filter(is_active=True).exclude(
                uuid=self.uuid
            ).update(is_active=False)
        super().save(*args, **kwargs)

