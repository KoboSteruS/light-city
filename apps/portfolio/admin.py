"""
Административная панель для портфолио.
"""

from django.contrib import admin
from django.utils.html import format_html
from apps.portfolio.models import PortfolioItem


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    """Админка для работ портфолио."""
    
    list_display = (
        'title', 'service', 'client', 'date_completed',
        'is_featured', 'is_active', 'image_preview'
    )
    list_filter = ('is_active', 'is_featured', 'service', 'date_completed')
    search_fields = ('title', 'client', 'description')
    list_editable = ('is_featured', 'is_active')
    date_hierarchy = 'date_completed'
    ordering = ('-date_completed', '-created_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'service', 'client', 'date_completed')
        }),
        ('Контент', {
            'fields': ('description', 'image')
        }),
        ('Настройки отображения', {
            'fields': ('is_featured', 'is_active')
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

