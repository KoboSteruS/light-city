"""
Административная панель для услуг.
"""

from django.contrib import admin
from django.utils.html import format_html
from apps.services.models import Service, ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """Админка для управления категориями услуг."""
    
    list_display = ('name', 'slug', 'order', 'is_active', 'services_count')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'name')
    prepopulated_fields = {'slug': ('name',)}
    
    def services_count(self, obj):
        """Количество услуг в категории."""
        return obj.services.count()
    
    services_count.short_description = 'Услуг'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Админка для управления услугами."""
    
    list_display = ('name', 'category', 'price_display', 'order', 'is_active', 'image_preview', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'name')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'description')
        }),
        ('Подробности об услуге', {
            'fields': ('materials', 'completion_time', 'features'),
            'description': 'Дополнительная информация об услуге, отображаемая на странице детального просмотра'
        }),
        ('Изображения', {
            'fields': ('icon', 'image')
        }),
        ('Цена', {
            'fields': ('price_from', 'price_unit')
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active')
        }),
    )
    
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

