"""
Административная панель для главного приложения.
"""

from django.contrib import admin
from django.utils.html import format_html
from apps.main.models import Slider, AboutUs, SiteSettings, Testimonial


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    """Админка для управления слайдером."""
    
    list_display = ('title', 'order', 'is_active', 'image_preview', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    list_editable = ('order', 'is_active')
    ordering = ('order', '-created_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'subtitle', 'image')
        }),
        ('Кнопка', {
            'fields': ('button_text', 'button_link'),
            'classes': ('collapse',)
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active')
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


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    """Админка для блока 'О нас'."""
    
    list_display = ('title', 'is_active', 'image_preview', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    
    fieldsets = (
        ('Контент', {
            'fields': ('title', 'description', 'image')
        }),
        ('Настройки', {
            'fields': ('is_active',)
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
    
    image_preview.short_description = 'Фото'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Админка для настроек сайта."""
    
    list_display = ('site_name', 'phone', 'email', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('site_name', 'phone', 'email', 'address')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('site_name', 'phone', 'email', 'address', 'working_hours')
        }),
        ('Социальные сети', {
            'fields': ('vk_link', 'instagram_link', 'telegram_link'),
            'classes': ('collapse',)
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        """Ограничиваем создание только одной записи настроек."""
        if SiteSettings.objects.filter(is_active=True).exists():
            return False
        return super().has_add_permission(request)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Админка для управления отзывами."""
    
    list_display = ('name', 'position', 'rating_display', 'order', 'is_active', 'avatar_preview', 'created_at')
    list_filter = ('is_active', 'rating', 'created_at')
    search_fields = ('name', 'position', 'text')
    list_editable = ('order', 'is_active')
    ordering = ('order', '-created_at')
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('name', 'position', 'avatar')
        }),
        ('Отзыв', {
            'fields': ('rating', 'text')
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def avatar_preview(self, obj):
        """Превью аватара в списке."""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url
            )
        return '-'
    
    avatar_preview.short_description = 'Фото'
    
    def rating_display(self, obj):
        """Отображение рейтинга звездами."""
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color: #F8D12C; font-size: 1.2em;">{}</span>',
            stars
        )
    
    rating_display.short_description = 'Рейтинг'

