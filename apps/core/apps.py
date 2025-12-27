"""
Конфигурация приложения Core.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Конфигурация для базового приложения проекта."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Базовые настройки'

