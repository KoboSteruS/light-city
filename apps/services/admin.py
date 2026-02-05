"""
Административная панель для услуг.
"""

from django.contrib import admin
from django.utils.html import format_html
from apps.services.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Админка для управления услугами."""
    
    list_display = ('name', 'price_display', 'order', 'is_active', 'icon_preview', 'image_preview', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'name')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description')
        }),
        ('Подробности об услуге', {
            'fields': ('materials', 'completion_time', 'features'),
            'description': 'Дополнительная информация об услуге, отображаемая на странице детального просмотра'
        }),
        ('Изображения', {
            'fields': ('icon', 'image'),
            'description': 'Иконка - для отображения на главной странице (рекомендуется 200x200px). Изображение - для каталога услуг (рекомендуется 800x600px).'
        }),
        ('Цена', {
            'fields': ('price_from', 'price_unit')
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def icon_preview(self, obj):
        """Превью иконки в списке."""
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-width: 60px; max-height: 60px; object-fit: contain; border-radius: 4px;" />',
                obj.icon.url
            )
        return '-'
    
    icon_preview.short_description = 'Иконка'
    
    def image_preview(self, obj):
        """Превью изображения в списке."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 80px; max-height: 80px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    
    image_preview.short_description = 'Изображение'
    
    def price_display(self, obj):
        """Отображение цены."""
        if obj.price_from:
            return f'от {obj.price_from} {obj.price_unit}'
        return '-'
    
    price_display.short_description = 'Цена'

