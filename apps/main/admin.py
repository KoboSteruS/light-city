"""
Административная панель для главного приложения.
"""

from django.contrib import admin
from django import forms
from django.utils.html import format_html
from apps.main.models import Slider, AboutUs, SiteSettings, Testimonial, TelegramChat, Statistic


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


class DecimalDotWidget(forms.TextInput):
    """Виджет для DecimalField, который использует точку вместо запятой."""
    
    input_type = 'text'
    
    def format_value(self, value):
        """Форматируем значение с точкой."""
        if value is None or value == '':
            return ''
        # Преобразуем Decimal в строку с точкой
        if hasattr(value, 'quantize'):
            # Это Decimal объект - форматируем с точкой
            return format(value, '.2f')
        # Это строка или число - заменяем запятую на точку
        value_str = str(value).strip()
        # Заменяем запятую на точку
        value_str = value_str.replace(',', '.')
        return value_str
    
    def value_from_datadict(self, data, files, name):
        """Получаем значение из формы и заменяем запятую на точку."""
        value = data.get(name)
        if value:
            # Преобразуем в строку
            value = str(value).strip()
            # Заменяем запятую на точку
            value = value.replace(',', '.')
            # Удаляем все символы кроме цифр и точки (оставляем только одну точку)
            import re
            # Разделяем на части до и после точки
            parts = value.split('.')
            if len(parts) > 2:
                # Если несколько точек, оставляем только первую
                value = parts[0] + '.' + ''.join(parts[1:])
            # Удаляем все нецифровые символы кроме точки
            value = re.sub(r'[^\d.]', '', value)
            return value
        return value


class AboutUsAdminForm(forms.ModelForm):
    """Форма для админки AboutUs с кастомными виджетами для Decimal полей."""
    
    subtitle_margin_bottom = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        required=False,
        widget=DecimalDotWidget(attrs={'step': '0.01', 'min': '0', 'placeholder': '1.0'}),
        localize=False
    )
    
    paragraph_margin_bottom = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        required=False,
        widget=DecimalDotWidget(attrs={'step': '0.01', 'min': '0', 'placeholder': '0.75'}),
        localize=False
    )
    
    class Meta:
        model = AboutUs
        fields = '__all__'
        field_classes = {
            'subtitle_margin_bottom': forms.DecimalField,
            'paragraph_margin_bottom': forms.DecimalField,
        }


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    """Админка для блока 'О нас'."""
    
    form = AboutUsAdminForm
    
    list_display = ('title', 'is_active', 'image_preview', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    
    fieldsets = (
        ('Заголовки', {
            'fields': ('title', 'subtitle'),
            'description': 'Заголовок и подзаголовок, отображаемые на странице "О нас"'
        }),
        ('Контент', {
            'fields': ('description', 'image')
        }),
        ('Отступы', {
            'fields': ('subtitle_margin_bottom', 'paragraph_margin_bottom'),
            'description': 'Настройка расстояний между элементами текста (в rem единицах). Используйте точку (.) в качестве разделителя, например: 1.0, 0.75'
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
        ('Telegram бот', {
            'fields': ('telegram_bot_token',),
            'classes': ('collapse',),
            'description': 'Токен бота для отправки уведомлений о новых заявках'
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


@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    """Админка для управления Telegram чатами."""
    
    list_display = ('chat_id', 'username', 'first_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('chat_id', 'username', 'first_name')
    list_editable = ('is_active',)
    readonly_fields = ('chat_id', 'username', 'first_name', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Информация о чате', {
            'fields': ('chat_id', 'username', 'first_name')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Запрещаем создание вручную - только через бота."""
        return False


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


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    """Админка для управления статистикой."""
    
    list_display = ('label', 'number_display', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('label',)
    list_editable = ('order', 'is_active')
    ordering = ('order', '-created_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('label', 'number', 'suffix', 'icon_class')
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def number_display(self, obj):
        """Отображение числа с суффиксом."""
        return f"{obj.number}{obj.suffix}"
    
    number_display.short_description = 'Значение'
