"""
Context processors для добавления глобальных переменных в шаблоны.
"""

from apps.main.models import SiteSettings
from loguru import logger


def site_settings(request):
    """
    Добавляет настройки сайта во все шаблоны.
    
    Использование:
        {{ settings.site_name }}
        {{ settings.phone }}
        {{ settings.email }}
        и т.д.
    """
    try:
        settings = SiteSettings.objects.filter(is_active=True).first()
        return {'settings': settings}
    except Exception as e:
        logger.error(f'Ошибка при загрузке настроек сайта: {e}')
        return {'settings': None}



