"""
Context processors для добавления глобальных переменных в шаблоны.
"""

from apps.main.models import SiteSettings
from loguru import logger


def format_phone(phone):
    """
    Форматирует телефонный номер в формат +7 (8142) 28-09-03
    """
    if not phone:
        return phone
    
    # Удаляем все нецифровые символы кроме плюса
    phone_digits = ''.join(filter(str.isdigit, str(phone).replace('+', '')))
    
    # Если номер начинается с 8, заменяем на 7
    if phone_digits.startswith('8'):
        phone_digits = '7' + phone_digits[1:]
    
    # Если номер не начинается с 7, добавляем 7
    if not phone_digits.startswith('7'):
        phone_digits = '7' + phone_digits
    
    # Форматируем: +7 (8142) 28-09-03
    if len(phone_digits) >= 11:
        return f"+7 ({phone_digits[1:5]}) {phone_digits[5:7]}-{phone_digits[7:9]}-{phone_digits[9:11]}"
    
    return phone


def site_settings(request):
    """
    Добавляет настройки сайта во все шаблоны.
    
    Использование:
        {{ settings.site_name }}
        {{ settings.phone }}
        {{ settings.phone_formatted }}
        {{ settings.email }}
        и т.д.
    """
    try:
        settings = SiteSettings.objects.filter(is_active=True).first()
        if settings:
            # Добавляем отформатированный телефон
            settings.phone_formatted = format_phone(settings.phone) if settings.phone else ''
        return {'settings': settings}
    except Exception as e:
        logger.error(f'Ошибка при загрузке настроек сайта: {e}')
        return {'settings': None}



