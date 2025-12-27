"""
Конфигурация главного приложения.
"""

from django.apps import AppConfig


class MainConfig(AppConfig):
    """Конфигурация главного приложения."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main'
    verbose_name = 'Главная страница'

