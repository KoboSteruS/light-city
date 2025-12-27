"""
Административная панель для контактов.
"""

from django.contrib import admin
from django.utils.html import format_html
from apps.contacts.models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Админка для обращений."""
    
    list_display = (
        'name', 'phone', 'status_badge', 'is_read',
        'created_at_formatted'
    )
    list_filter = ('status', 'is_read', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('name', 'phone', 'email', 'message')
        }),
        ('Обработка', {
            'fields': ('status', 'is_read', 'admin_notes')
        }),
        ('Служебная информация', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_in_progress', 'mark_as_completed']
    
    def status_badge(self, obj):
        """Цветной бейдж статуса."""
        colors = {
            'new': '#ffc107',
            'in_progress': '#17a2b8',
            'completed': '#28a745',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    
    status_badge.short_description = 'Статус'
    
    def created_at_formatted(self, obj):
        """Форматированная дата создания."""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    
    created_at_formatted.short_description = 'Дата обращения'
    created_at_formatted.admin_order_field = 'created_at'
    
    @admin.action(description='Отметить как прочитанное')
    def mark_as_read(self, request, queryset):
        """Массовая отметка как прочитанное."""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'Отмечено прочитанными: {updated}')
    
    @admin.action(description='Взять в обработку')
    def mark_as_in_progress(self, request, queryset):
        """Массовая отметка 'В обработке'."""
        updated = queryset.update(
            status=ContactMessage.Status.IN_PROGRESS,
            is_read=True
        )
        self.message_user(request, f'Взято в обработку: {updated}')
    
    @admin.action(description='Отметить как завершенное')
    def mark_as_completed(self, request, queryset):
        """Массовая отметка 'Завершено'."""
        updated = queryset.update(
            status=ContactMessage.Status.COMPLETED,
            is_read=True
        )
        self.message_user(request, f'Отмечено завершенными: {updated}')
    
    def save_model(self, request, obj, form, change):
        """При изменении автоматически отмечаем как прочитанное."""
        if change:
            obj.is_read = True
        super().save_model(request, obj, form, change)

