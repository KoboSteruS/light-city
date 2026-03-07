"""
Административная панель для портфолио.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from reversion.admin import VersionAdmin
from apps.portfolio.models import PortfolioItem


@admin.register(PortfolioItem)
class PortfolioItemAdmin(VersionAdmin, admin.ModelAdmin):
    """Админка для работ портфолио."""
    
    list_display = (
        'order', 'title', 'service', 'client', 'date_completed',
        'is_featured', 'is_active', 'image_preview'
    )
    list_display_links = ('title',)
    list_filter = ('service', 'is_active', 'is_featured', 'date_completed')
    search_fields = ('title', 'client', 'description')
    list_editable = ('order', 'is_featured', 'is_active')
    date_hierarchy = 'date_completed'
    ordering = ('order', '-date_completed', '-created_at')
    list_per_page = 24
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'service', 'client', 'date_completed')
        }),
        ('Контент', {
            'fields': ('description', 'image'),
            'description': '⚠️ Требования к изображению: максимум 25 MB, форматы jpg/png/webp. Рекомендуемый размер: 800x600px.'
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_featured', 'is_active'),
            'description': 'Порядок: чем меньше число, тем выше в списке. «На главной» — работа попадёт в блок из 4 работ на главной странице в своей категории.'
        }),
    )
    
    def image_preview(self, obj):
        """Превью изображения в списке."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 60px;" />',
                obj.image.url
            )
        return '-'
    
    image_preview.short_description = 'Превью'
    
    def save_model(self, request, obj, form, change):
        """Переопределяем сохранение для лучшей обработки ошибок."""
        try:
            super().save_model(request, obj, form, change)
            if change:
                messages.success(request, f'Работа "{obj.title}" успешно обновлена.')
            else:
                messages.success(request, f'Работа "{obj.title}" успешно добавлена.')
        except Exception as e:
            messages.error(request, f'Ошибка при сохранении: {str(e)}')
            raise

