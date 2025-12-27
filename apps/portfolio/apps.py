"""
Конфигурация приложения портфолио.
"""

from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    """Конфигурация приложения портфолио."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.portfolio'
    verbose_name = 'Портфолио'

